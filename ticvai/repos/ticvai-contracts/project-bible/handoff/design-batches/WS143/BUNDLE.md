# WS143 — Marketing CRM Configuration Reference v1.0 board 9

**10 screens · 6 operations · 8 schemas · 3 permissions**

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
  `CASE_VIEW, MARKETING_MANAGE, MARKETING_VIEW`. A control nobody can use must say so,
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
| `BO-814` | Voice of Customer Center | D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-815` | Survey Builder | D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-816` | Survey Triggers & Distribution | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-817` | NPS, CSAT & CES Configuration | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-818` | Survey Responses & Insights | D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-819` | Review Collection & Rating Rules | D | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `BO-820` | Moderation & Publishing | D | 0 | 0 | 6 | 3 | 0 | 6 | — | notStarted (—) |
| `BO-821` | AI Sentiment & Topic Analysis | D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-822` | Service Recovery Automation | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-823` | VOC Analytics & Audit | D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-814, BO-815, BO-816, BO-817, BO-818, BO-819, BO-820, BO-821, BO-822, BO-823 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-814` Voice of Customer Center

**Provide a consolidated view of guest feedback and recovery performance. Show surveys sent, response rate, NPS, CSAT, CES, review count, average rating and negative- feedback volume. Visualize metric, rating, sentiment, topic and recovery trends by brand, venue, product, event and channel. Surface urgent detractors, repeated issues, moderation backlog and recovery cases at risk. Provide AI summaries with links to underlying responses and explainable topic evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-814 |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/voice-of-customer-center-bo-814` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Guest feedback and recovery at a glance: surveys sent, response rate, NPS, CSAT, CES, review count, average rating, negative feedback; trends by venue, product, event and channel; urgent detractors and moderation backlog; AI summaries linked to the responses behind them.

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

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **AI themes**: Labelled as AI with model version, each linking to example responses. *(source: contracts/satellite/marketing-crm.yaml#listCustomerSatisfactionFeedback; contracts/satellite/marketing-crm.yaml#/components/schemas/FeedbackClassification)*

**Data it reads**: `listCustomerSatisfactionFeedback` (onLoad, Feedback at a glance)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-815` Survey Builder: *Survey Builder*
- → `BO-816` Survey Triggers & Distribution: *Survey Triggers & Distribution*
- → `BO-817` NPS, CSAT & CES Configuration: *NPS, CSAT & CES Configuration*
- → `BO-818` Survey Responses & Insights: *Survey Responses & Insights*
- → `BO-819` Review Collection & Rating Rules: *Review Collection & Rating Rules*
- → `BO-820` Moderation & Publishing: *Moderation & Publishing*
- → `BO-821` AI Sentiment & Topic Analysis: *AI Sentiment & Topic Analysis*
- → `BO-822` Service Recovery Automation: *Service Recovery Automation*
- → `BO-823` VOC Analytics & Audit: *VOC Analytics & Audit*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The voice customer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the voice customer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No voice customer yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the voice customer are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  nps: 41
  csat: 4.3
  responseRate: 18%
  reviewsToModerate: 9
theme: Queues at Tornado Slide (negative, 63 mentions)
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

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-814` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-814`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 9
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 1: Opens Voice of Customer Center → Provide a consolidated view of guest feedback and recovery performance. Show surveys sent, response rate, NPS, CSAT, CES, review count, average rating and negative- feedback volume. Visualize metric …
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F252 branch at step 1 (expected): when Nothing has been set up on Voice of Customer Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F252 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-814?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-815`, `BO-816`, `BO-817`, `BO-818`, `BO-819`, `BO-820`, `BO-821`, `BO-822`, `BO-823`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-815` Survey Builder

**Create multilingual, accessible surveys without development. Provide rating, NPS, single choice, multiple choice, text, matrix, date, media and information- section elements. Support question library, templates, required fields, validation, page/section layout and conditional branching. Configure identified or anonymous response, consent statement, incentive and completion behavior. Preview by channel and language and version, approve and test before publication. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-815 |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/survey-builder-bo-815` |

**Known gaps.** **Survey Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Multilingual, accessible surveys without development: rating, NPS, choices, text, matrix, date, media; question library, branching, identified or anonymous responses, consent statement and incentive. A survey is a form version, immutable once answered.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Anonymous or identified**: Anonymous surveys never link to a guest profile, and say so to the respondent. *(source: screens/P08-venue-back-office.yaml#BO-815)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create form (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-814` Voice of Customer Center: *Back to Voice of Customer Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The survey list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the survey untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No survey yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the survey are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `WEB-026`: Guests answer surveys on WEB-026 and GST-035 (see their corrections).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
survey: Post-visit Coastal Aqua - NPS + 3 questions - EN/AR - version 2
```

#### Permissions

- `createForm` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-815` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-815`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 9
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 2: Works in Survey Builder → Create multilingual, accessible surveys without development. Provide rating, NPS, single choice, multiple choice, text, matrix, date, media and information- section elements. Support question …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-815?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create form, Cancel.
- [ ] Every transition is wired: `BO-814`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-816` Survey Triggers & Distribution

**Control when, where and to whom a survey is sent. Trigger after purchase, visit, event, reservation, membership interaction, case closure or inactivity. Distribute through email, SMS, WhatsApp, push, mobile app, web, kiosk and QR where supported. Configuration Scope of Work / Version 1.0 45 Configure delay, expiry, reminder, sample, quota, frequency cap, exclusions and incentive. Validate consent and eligibility and prevent duplicate or excessive survey requests. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-816 |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/survey-triggers-distribution-bo-816` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** When and to whom a survey goes: after purchase, visit (only when the ticket was scanned), event, reservation, membership interaction, case closure or inactivity; by email, SMS, WhatsApp, push, app, web, kiosk or QR; with delay, expiry, reminder, sampling, frequency cap and exclusions.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Trigger**: Post-visit means post-scan; a "how was your purchase" survey can trigger off the sale. *(source: DI-561; DI-391)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save message trigger (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-814` Voice of Customer Center: *Back to Voice of Customer Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The survey triggers distribution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the survey triggers distribution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No survey triggers distribution yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the survey triggers distribution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `sendTimeMode` `optimised` on a trigger whose `priority` is `operational` or `transactional` (29 September, build pass, group G2), or an `event` not in the … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
trigger: Ticket scanned -> 3 hours later -> WhatsApp survey link -> reminder after 2 days -> expires after 7 days
```

#### Permissions

- `setMessageTrigger` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Surveys trigger at configurable points: post-purchase, post-visit, post-ticket-scan, membership renewal and case closure. *(client request · MoM 20 Aug 2026, 4.9 Surveys & Gamification · DI-391)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-816` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-816`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 9
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 4: Works in Survey Triggers & Distribution → Control when, where and to whom a survey is sent. Trigger after purchase, visit, event, reservation, membership interaction, case closure or inactivity. Distribute through email, SMS, WhatsApp, push …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-816?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save message trigger, Cancel.
- [ ] Every transition is wired: `BO-814`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-817` NPS, CSAT & CES Configuration

**Define standardized experience metrics and follow-up thresholds. Configure metric definition, scale, labels, score bands, calculation and rounding. Set targets, benchmarks, venue/category mappings and reporting periods. Define detractor, low-CSAT and high-effort follow-up actions and case priority. Version metric rules and prevent historical results from being silently recalculated. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block B · ticket #29141 (VM-BO-817) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/nps-csat-ces-configuration-bo-817` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): Metric definitions and follow-up thresholds are not forms; createForm does not configure NPS, CSAT or CES (design-notes correction customer-marketing BO-817).

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Standard experience metrics: NPS, CSAT and CES definitions, scales, score bands, targets, benchmarks, and the follow-up when a guest is a detractor, low CSAT or high effort. Rules are versioned so past results are never silently recalculated.

**Fixed on main** (the package already carries these; draw what it says): The only operation is createForm. (CHG-WIR-005).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-814` Voice of Customer Center: *Back to Voice of Customer Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The nps csat ces list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the nps csat ces untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No nps csat ces yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the nps csat ces are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
nps: Detractor 0-6 -> case priority High; target +40
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-817` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-817`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 9
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 6: Works in NPS, CSAT & CES Configuration → Define standardized experience metrics and follow-up thresholds. Configure metric definition, scale, labels, score bands, calculation and rounding. Set targets, benchmarks, venue/category mappings …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-817?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-814`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-818` Survey Responses & Insights

**Review individual responses and their calculated insight. Show respondent/profile or anonymous status, survey/version, answers, channel, timestamps and incentive outcome. Display NPS, CSAT, CES, sentiment, topics, urgency and linked guest/transaction where permitted. Filter, search, export, tag, assign follow-up and open a service-recovery case. Protect anonymity and sensitive free text and preserve the submitted response unchanged. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-818 |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/survey-responses-insights-bo-818` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Individual responses with their insight: respondent or anonymous, survey version, answers, channel, scores, sentiment and topics, linked guest and transaction where permitted; follow-up and recovery cases. The submitted response is never changed.

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

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listCustomerSatisfactionFeedback` (onLoad, Responses and insight)

**Where the user goes next**

- → `BO-814` Voice of Customer Center: *Back to Voice of Customer Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The survey responses insights list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the survey responses insights untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No survey responses insights yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the survey responses insights are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
response: Anonymous - Post-visit v2 - NPS 3 - "Too crowded at the wave pool" - topic Crowding (AI)
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

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-818` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-818`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 9
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 8: Works in Survey Responses & Insights → Review individual responses and their calculated insight. Show respondent/profile or anonymous status, survey/version, answers, channel, timestamps and incentive outcome. Display NPS, CSAT, CES …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-818?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-814`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-819` Review Collection & Rating Rules

**Configure verified review and rating capture. Define review entities including attraction, event, ticket, product, membership, venue, dining and employee/service. Configure overall and category ratings, minimum/maximum scale, required comments and media support. Validate verified visits or purchases, identity, submission window, duplicates and fraud/spam signals. Map capture channels and decide which reviews require moderation before publication. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-819 |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/review-collection-rating-rules-bo-819` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Verified review capture: what can be reviewed (attraction, event, product, membership, venue, dining, service), scales, required comments, media, verified visit or purchase, submission window, duplicate and spam checks, and which reviews need moderation.

**Known correction pending (do not draw the wrong version)**

- **Only listReviews is declared; nothing configures review rules.** Why: The purpose is configuration; add the rule operations. *(source: contracts/satellite/marketing-crm.yaml#listReviews; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Min rating | stepper or slider | — | min 1; max 5 | `listReviews` ?minRating |
| Has response | toggle | — | — | `listReviews` ?hasResponse |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listReviews` (onLoad, Reviews collected)

**Where the user goes next**

- → `BO-814` Voice of Customer Center: *Back to Voice of Customer Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The review collection rating list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the review collection rating untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No review collection rating yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the review collection rating are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: Attractions - 1-5 stars - verified scan required - within 14 days - comments optional
```

#### Permissions

- `listReviews` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.5.17 | Mobile App Review Center | Marketing & CRM | CONTRACTED | `listReviews` |
| 22.5.20 | Review Audit Trail | Marketing & CRM | CONTRACTED | `listReviews` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-819` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-819`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 9
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 10: Works in Review Collection & Rating Rules → Configure verified review and rating capture. Define review entities including attraction, event, ticket, product, membership, venue, dining and employee/service. Configure overall and category …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-819?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-814`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-820` Moderation & Publishing

**Review and publish guest feedback safely and consistently. Provide moderation queue with channel, rating, text, media, flags, sentiment, topic and SLA. Approve, reject, redact, escalate or request follow-up using reason codes and permission controls. Configure profanity, personal-data, fraud and policy checks and public response templates. Configuration Scope of Work / Version 1.0 46 Publish to approved TICVAI and external channels and retain original, moderated and published versions. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-820 |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `reviewId` (navigation) |
| Route | `/engagement-support/moderation-publishing-bo-820` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The moderation queue: approve, reject, redact or escalate guest reviews with reason codes, profanity and personal-data checks, and public response templates. Statuses pending moderation, published, hidden, rejected. The original text is retained.

**Known correction pending (do not draw the wrong version)**

- **Only respondToReview is declared; approve, reject, redact and publish have no operation.** Why: Moderation itself cannot be performed. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/Review; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Respond**: Public or private response shown under the guest's review. *(source: contracts/satellite/marketing-crm.yaml#respondToReview)*

**Where the user goes next**

- → `BO-814` Voice of Customer Center: *Back to Voice of Customer Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The moderation publishing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the moderation publishing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No moderation publishing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the moderation publishing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
review: 2 stars - "Lazy river queue 40 minutes" - pending moderation
```

#### Permissions

- `respondToReview` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.5.5 | Review Moderation Workflow | Marketing & CRM | CONTRACTED | `respondToReview` |
| 22.5.6 | Review Publishing | Marketing & CRM | CONTRACTED | `respondToReview` |
| 22.5.7 | Review Responses | Marketing & CRM | CONTRACTED | `respondToReview` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-820` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-820`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 9
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 12: Works in Moderation & Publishing → Review and publish guest feedback safely and consistently. Provide moderation queue with channel, rating, text, media, flags, sentiment, topic and SLA. Approve, reject, redact, escalate or request …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-820?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-814`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-821` AI Sentiment & Topic Analysis

**Analyze feedback at scale using explainable AI. Classify sentiment, emotion, urgency, topics, issue type and intent across survey and review text. Cluster recurring issues and summarize themes by venue, product, event, language and time period. Show confidence, supporting excerpts, model/version and correction controls for reviewers. Monitor quality, bias and drift and restrict use of sensitive data or unsupported inference. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-821 |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/ai-sentiment-topic-analysis-bo-821` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Explainable AI analysis of feedback text: sentiment, emotion, urgency, topics, clusters of recurring issues, with confidence, supporting excerpts, model and version, and reviewer corrections.

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

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listCustomerSatisfactionFeedback` (onLoad, Sentiment and topics)

**Where the user goes next**

- → `BO-814` Voice of Customer Center: *Back to Voice of Customer Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sentiment topic analysis list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sentiment topic analysis untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sentiment topic analysis yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the sentiment topic analysis are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cluster: Food ran out late afternoon - 38 responses - negative 0.79 - model feedback-v3
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

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-821` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-821`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 9
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 14: Works in AI Sentiment & Topic Analysis → Analyze feedback at scale using explainable AI. Classify sentiment, emotion, urgency, topics, issue type and intent across survey and review text. Cluster recurring issues and summarize themes by …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-821?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-814`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-822` Service Recovery Automation

**Turn negative feedback into governed service action. Create rules for detractors, low CSAT, high effort, negative review, urgent topic and repeated issue. Create and route a case, select priority, notify the owner and recommend an approved recovery offer. Require approval based on compensation amount, guest tier, issue severity and fraud risk. Schedule follow-up, capture resolution and measure recovery, rating change, satisfaction and retention. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/service-recovery-automation-bo-822` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): setRefundCompensationService raises one request; nothing in it defines the automation rules this screen configures (design-notes correction customer-marketing …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Turn negative feedback into governed action: rules for detractors, low CSAT, high effort, negative reviews, urgent topics; create and route a case, recommend an approved recovery offer, approval by amount, tier and risk; follow up and measure the change.

**Fixed on main** (the package already carries these; draw what it says): Only setRefundCompensationService (one request) is declared; nothing defines the automation rules. (CHG-WIR-005).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-814` Voice of Customer Center: *Back to Voice of Customer Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The service recovery automation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the service recovery automation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No service recovery automation yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the service recovery automation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: NPS 0-6 with topic Staff -> case High to Guest Services -> recommend 500 points (auto-approved)
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-822` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-822`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 9
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 16: Works in Service Recovery Automation → Turn negative feedback into governed service action. Create rules for detractors, low CSAT, high effort, negative review, urgent topic and repeated issue. Create and route a case, select priority …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-822?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-814`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-823` VOC Analytics & Audit

**Provide cross-source performance and governance reporting. Combine NPS, CSAT, CES, ratings, sentiment, topics and response rates without double-counting guests. Benchmark venues, products, events, categories, channels and periods and expose root-cause drivers. Measure moderation SLA, recovery volume, recovery success, compensation cost and guest impact. Audit survey/review setup, AI analysis, moderation, publishing, case creation, exports and administrative actions. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 47 Board 10 - Gamification & Loyalty Engagement Figure 10. High-definition configuration board with all 10 screens. Configuration Scope of Work / Version 1.0 48**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-823 |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/voc-analytics-audit-bo-823` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Cross-source VOC reporting without double-counting guests: NPS, CSAT, CES, ratings, sentiment and topics benchmarked by venue, product and period, root-cause drivers, moderation SLA and recovery effectiveness.

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

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listServiceRootCause` (onLoad, Analytics and root cause)

**Where the user goes next**

- → `BO-814` Voice of Customer Center: *Back to Voice of Customer Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The voc analytics audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the voc analytics audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No voc analytics audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the voc analytics audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
driver: Queue length explains 34% of detractors in September
```

#### Permissions

- `listServiceRootCause` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-823` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS78 Marketing CRM Configuration Reference v1.0 Board 9.dc.html#bo-823`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 9
- Flow F252 *Marketing CRM Configuration Reference v1.0 board 9: Voice of Customer Center*, step 18: Works in VOC Analytics & Audit → Provide cross-source performance and governance reporting. Combine NPS, CSAT, CES, ratings, sentiment, topics and response rates without double-counting guests. Benchmark venues, products, events …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-823?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-814`.
- [ ] Every gated control is gated: `CASE_VIEW`.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createForm": {"method":"POST","path":"/forms","contract":"marketing-crm","summary":"Define a waiver, survey or capture form","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FormDefinition","responds":"FormDefinition"},
"listCustomerSatisfactionFeedback": {"method":"GET","path":"/customer-satisfaction-feedback","contract":"marketing-crm","summary":"Customer Satisfaction, Feedback & Voice of Customer","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"source","in":"query","required":false},{"name":"groupBy","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"eventId","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"agentPrincipalId","in":"query","required":false},{"name":"sentiment","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false}],"requestBody":null,"responds":"CustomerSatisfactionFeedbackVoiceOfCustomerView"},
"listReviews": {"method":"GET","path":"/reviews","contract":"marketing-crm","summary":"List guest reviews and ratings","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"minRating","in":"query","required":null},{"name":"hasResponse","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listServiceRootCause": {"method":"GET","path":"/service-root-cause","contract":"marketing-crm","summary":"Service Analytics & Root-Cause Intelligence","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venueId","in":"query","required":false},{"name":"eventId","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"compare","in":"query","required":false},{"name":"compareId","in":"query","required":false}],"requestBody":null,"responds":"ServiceAnalyticsRootCauseIntelligenceView"},
"respondToReview": {"method":"POST","path":"/reviews/{reviewId}/respond","contract":"marketing-crm","summary":"Respond to a review","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Review"},
"setMessageTrigger": {"method":"POST","path":"/message-triggers","contract":"marketing-crm","summary":"Fire a message from a platform event","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MessageTrigger","responds":"MessageTrigger"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CustomerSatisfactionFeedbackVoiceOfCustomerView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.form_submission and marketing.form_definition (survey forms), marketing.review, marketing.case and marketing.feedback_classification (new, the AI sentiment and topic per feedback item)","description":"Voice-of-customer figures for the filters given. Rates are shares of feedback items in the period.","required":["responses","breakdown","comments"],"properties":{"responses":{"type":"integer","minimum":0,"description":"Feedback items in the period."},"csat":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Share of CSAT answers in the top two points of the scale."},"nps":{"type":"integer","minimum":-100,"maximum":100,"nullable":true,"description":"Null where the tenant runs no NPS survey."},"surveyResponseRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Surveys answered over surveys sent."},"positiveRate":{"type":"number","minimum":0,"maximum":1},"neutralRate":{"type":"number","minimum":0,"maximum":1},"negativeRate":{"type":"number","minimum":0,"maximum":1},"complaints":{"type":"integer","minimum":0},"repeatContactRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Customers with a second case within 7 days of the first, over customers with a case."},"customerEffortScore":{"type":"number","minimum":1,"maximum":7,"nullable":true,"description":"Mean CES answer; null where effort is not measured."},"csatChangeRate":{"type":"number","nullable":true,"description":"Relative change in `csat` against the previous period of equal length."},"aiSummary":{"type":"object","nullable":true,"description":"AI-derived narrative of the feedback matching the filters (22.5.12; 29 September, build pass, group G2), labelled as AI on screen. Null when AI is off or fewer than 5 items match.","required":["text","basedOnCount","modelVersion"],"properties":{"text":{"type":"string","maxLength":2000},"basedOnCount":{"type":"integer","minimum":0,"description":"The feedback items the summary was written from."},"modelVersion":{"type":"string","maxLength":60},"generatedAt":{"type":"string","format":"date-time"}}},"breakdown":{"type":"array","description":"One row per value of the `groupBy` dimension, most responses first.","items":{"type":"object","required":["key","label","responses"],"properties":{"key":{"type":"string","description":"The id or enum value of the group."},"label":{"type":"string"},"responses":{"type":"integer","minimum":0},"csat":{"type":"number","minimum":0,"maximum":1,"nullable":true},"negativeRate":{"type":"number","minimum":0,"maximum":1}}}},"themes":{"type":"array","maxItems":20,"description":"AI topic themes, largest share first. Empty when AI is disabled for the tenant.","items":{"type":"object","required":["topic","shareRate"],"properties":{"topic":{"type":"string","maxLength":100},"shareRate":{"type":"number","minimum":0,"maximum":1},"negativeRate":{"type":"number","minimum":0,"maximum":1},"changeRate":{"type":"number","nullable":true,"description":"Relative change in the theme's volume against the previous period."}}}},"trendAlerts":{"type":"array","maxItems":10,"items":{"type":"string","maxLength":300},"description":"AI-detected shifts, e.g. negative feedback on ticket delivery rising after a release."},"comments":{"type":"array","maxItems":50,"description":"The 50 latest comments with text, newest first.","items":{"type":"object","required":["feedbackId","source","receivedAt"],"properties":{"feedbackId":{"type":"string","format":"uuid"},"source":{"type":"string","enum":["csatSurvey","serviceRating","nps","postCaseSurvey","complaint","appFeedback","webFeedback","directComment"]},"receivedAt":{"type":"string","format":"date-time"},"comment":{"type":"string","maxLength":4000,"nullable":true},"rating":{"type":"number","nullable":true,"description":"The answer on its survey's own scale."},"ratingScale":{"type":"string","nullable":true,"enum":["nps","csat","ces","likert5","likert7","stars"]},"sentiment":{"type":"string","nullable":true,"enum":["positive","neutral","negative"]},"topic":{"type":"string","nullable":true},"caseId":{"type":"string","format":"uuid","nullable":true},"agentPrincipalId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true},"followUpCaseId":{"type":"string","format":"uuid","nullable":true}}}}}},
"FormDefinition": {"type":"object","x-ticvai-persistence":"marketing.form_definition + marketing.form_definition_field","description":"CF-129, CL-04. **A waiver, a survey and a data-capture form are one mechanism.**\nA waiver is this form with a signature. A survey is this form with a scale. A demographic capture is this form at the point of sale. They were raised as three separate gaps and share every part: field configuration, conditional display, versioning, an acceptance record and a stored artefact.\n**Three implementations would drift on the version rule first.** A waiver signed against version 3 must stay bound to version 3, and that is the same requirement a survey has when question wording changes mid-campaign — **an NPS score means nothing if you cannot say which question produced it.**\n","required":["id","name","kind","version","status"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["waiver","survey","dataCapture","consentForm","incidentReport","registration"]},"consentPurposes":{"type":"array","description":"**What a `consentForm` consents to** (Chinmay, 2 October, batch 4; follows BO-188: biometric capture needs consent on the venue's own form; CHG-CSA-026). A guardian-signed form for a minor carries the guardian fields of the waiver builder (workbook Q237: guardian consent, configurable per country). Empty for any other kind.","items":{"type":"string","enum":["facePass","faceTag","marketing","photography","waiver"]}},"version":{"readOnly":true,"type":"integer","description":"**Set by the server** — 1 on `createForm`, the next number on every change. **Immutable once anything is submitted against it.** A change creates a new version, and the old one stays readable forever — 2.15.13 requires the exact accepted version retained, which is legal evidence rather than a nicety.\n"},"fields":{"type":"array","items":{"$ref":"#/components/schemas/FormField"}},"requiresSignature":{"type":"boolean","default":false,"description":"**What makes it a waiver.** And 2.15.9 makes ticket issuance conditional on one, which puts this in the purchase path rather than beside it.\n"},"signatureKind":{"type":"string","enum":["drawn","typed","checkbox","none"],"default":"none"},"scoreScale":{"type":"string","nullable":true,"enum":["nps","csat","ces","likert5","likert7","stars"],"description":"**What makes it a survey.** Named rather than free-form because a score whose scale is unknown cannot be compared to last quarter's.\n"},"appliesToProductIds":{"type":"array","items":{"type":"string","format":"uuid"}},"validForMonths":{"type":"integer","nullable":true,"description":"**How long an acceptance lasts.** A waiver signed last summer may or may not still hold, and 2.15.x asks for a returning participant not to sign again — which only works if the expiry is stated.\n"},"minimumAge":{"type":"integer","nullable":true},"requiresGuardianForMinors":{"type":"boolean","default":true,"description":"**A minor cannot waive their own rights.** A guardian signs, and the record has to name them — an unsigned or self-signed minor waiver is worth nothing at the moment it matters.\n"},"status":{"readOnly":true,"type":"string","enum":["draft","published","superseded","retired"]},"legalReviewedBy":{"type":"string","nullable":true},"legalReviewedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"FormField": {"type":"object","description":"One field. **Conditional display is the shared requirement** — a survey branching on an answer and a waiver revealing a medical question on a yes are the same mechanism.\n","required":["key","label","type"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"labelLocalised":{"type":"object","additionalProperties":{"type":"string"}},"type":{"type":"string","enum":["text","longText","number","date","select","multiSelect","boolean","scale","signature","file","phone","email"]},"options":{"type":"array","items":{"type":"string"}},"isRequired":{"type":"boolean","default":false},"isPersonalData":{"type":"boolean","default":false,"description":"**Marked at the field, because retention is decided at the field.** A survey answer and a medical condition on the same form have different lifetimes, and a form-level flag makes the whole thing as sensitive as its most sensitive field.\n"},"consentPurposeId":{"type":"string","format":"uuid","nullable":true},"showWhen":{"type":"object","nullable":true,"properties":{"field":{"type":"string"},"equals":{"type":"string"}}}}},
"MessageTrigger": {"type":"object","x-ticvai-persistence":"marketing.message_trigger","description":"**What fires a message.** Before, during and after a visit are one mechanism with a different sign on the offset.\n","required":["id","event","templateId","isActive"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"event":{"type":"string","description":"The platform event that fires it — `order.completed`, `access.validated`, `queue.turnApproaching`. **Named from the event catalogue** (`BusinessEvent.eventType`), so a trigger cannot bind to something nothing publishes. Its conditions are `MessageTriggerCondition` rows.\n**`entitlement.expiringSoon` is in the catalogue since 29 September** (build pass, group G2; 5.5.30): the pre-expiry reminder for a ticket or pass. Its anchor is the event time; the notice period is the template's `expiryNoticeDays`, so `offsetMinutes` is normally 0.\n"},"templateId":{"type":"string","format":"uuid"},"offsetMinutes":{"type":"integer","default":0,"description":"Negative fires before the anchor, positive after. **A reminder the day before a visit is -1440 against the performance**, not a separate concept.\n"},"anchor":{"type":"string","enum":["eventTime","performanceStart","visitEnd"],"default":"eventTime"},"priority":{"type":"string","enum":["operational","transactional","marketing"],"default":"transactional","description":"**A queue-turn alert and a monthly newsletter are not the same urgency and were the same dispatch.** `operational` bypasses batching and quiet hours; `marketing` never does.\n"},"sendTimeMode":{"type":"string","enum":["fixed","optimised"],"default":"fixed","description":"**Only for `priority` `marketing`** (29 September, build pass, group G2; 22.9.16): `optimised` holds the notification to the recipient's suggested hour from `ai.requestSuggestion` (kind `sendTime`) within the next 24 hours, on the suggested consented channel. `operational` and `transactional` messages are never delayed for it, and a `setMessageTrigger` asking for it on them is refused (400)."},"isActive":{"type":"boolean","default":true},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Review": {"x-ticvai-persistence":"marketing.review","allOf":[{"$ref":"#/components/schemas/SubmitReviewRequest"},{"type":"object","required":["status"],"properties":{"status":{"type":"string","enum":["pendingModeration","published","hidden","rejected"]},"response":{"type":"string","nullable":true},"responseIsPublic":{"type":"boolean"},"respondedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"openedCaseId":{"type":"string","nullable":true,"description":"Case raised automatically where the rating fell below the venue's threshold. Feedback that goes nowhere is worse than no feedback mechanism.\n"}}}]},
"ServiceAnalyticsRootCauseIntelligenceView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.case, marketing.conversation, marketing.form_submission (CSAT) and the related orders and payments","description":"Service analytics for the filters given, with the comparison asked for.","required":["contactVolume","cases","drivers","comparison"],"properties":{"contactVolume":{"type":"integer","minimum":0,"description":"Conversations and cases opened, a conversation that became a case counted once."},"cases":{"type":"integer","minimum":0},"averageFirstResponseSeconds":{"type":"integer","minimum":0,"nullable":true},"averageResolutionSeconds":{"type":"integer","minimum":0,"nullable":true},"firstContactResolutionRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"reopenRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"escalationRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"slaComplianceRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"costPerCase":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"csat":{"type":"number","minimum":0,"maximum":1,"nullable":true},"refundRequests":{"type":"integer","minimum":0},"complaintRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"comparison":{"type":"object","required":["basis","kpis"],"properties":{"basis":{"type":"string","enum":["previousDay","previousWeek","previousMonth","event","venue","product"]},"compareId":{"type":"string","format":"uuid","nullable":true},"kpis":{"type":"array","items":{"type":"object","required":["kpi"],"properties":{"kpi":{"type":"string","description":"The KPI's property name above, e.g. `contactVolume`."},"current":{"type":"number","nullable":true},"previous":{"type":"number","nullable":true},"changeRate":{"type":"number","nullable":true}}}}}},"drivers":{"type":"array","description":"Contact drivers, most cases first.","items":{"type":"object","required":["driver","cases","shareRate"],"properties":{"driver":{"type":"string","enum":["ticketDelivery","refund","reschedule","paymentFailure","membership","accessIssue","groupBooking","generalInformation","other"]},"cases":{"type":"integer","minimum":0},"shareRate":{"type":"number","minimum":0,"maximum":1},"changeRate":{"type":"number","nullable":true}}}},"rootCauses":{"type":"array","maxItems":20,"description":"Case surges traced to one cause, largest first. Empty when AI is disabled for the tenant.","items":{"type":"object","required":["summary","cases"],"properties":{"summary":{"type":"string","maxLength":500},"driver":{"type":"string","nullable":true},"cases":{"type":"integer","minimum":0},"causeType":{"type":"string","enum":["paymentProvider","event","product","release","incident","venueArea","other"]},"causeRef":{"type":"string","nullable":true,"description":"The id of the provider, event, product or incident, where there is one."},"windowStart":{"type":"string","format":"date-time","nullable":true},"windowEnd":{"type":"string","format":"date-time","nullable":true}}}},"avoidableContacts":{"type":"array","description":"AI estimate of cases that could have been prevented, by remedy.","items":{"type":"object","required":["preventableBy","cases"],"properties":{"preventableBy":{"type":"string","enum":["betterB2cInformation","selfService","productConfiguration","improvedNotifications","technicalFixes","betterTicketDelivery"]},"cases":{"type":"integer","minimum":0},"recommendation":{"type":"string","maxLength":500,"nullable":true}}}}}},
"SubmitReviewRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","rating","venueId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"relatedOrderId":{"type":"string"},"rating":{"type":"integer","minimum":1,"maximum":5},"body":{"type":"string","maxLength":5000},"aspects":{"type":"array","description":"Aspect chips — the closed set the description always named.","uniqueItems":true,"items":{"type":"string","enum":["exhibitions","staff","cleanliness","food","value"]}},"recordedAt":{"type":"string","format":"date-time"}}}
}
```
