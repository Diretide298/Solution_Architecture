# P12-conversations-01 — P12 · Conversations

**2 screens · 13 operations · 13 schemas · 2 permissions**

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
| `SUP-004` | Conversation Queue | B–D | 3 | 12 | 6 | 7 | 1 | 6 | — | notStarted (generated) |
| `SUP-005` | Live Chat Workspace | B–D | 41 | 60 | 6 | 22 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**SUP-004 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `SUP-004` Conversation Queue

**Find the right one quickly, and act on it without opening it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Conversations · wave 2 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as guest |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCases` reads the population and `getCase` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `conversationId` (deepLink) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. |
| Route | `/general/conversation-queue` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Pulled to Wave 2 (CF-101). **The guest concierge is Phase 1 and a handover needs somewhere to land** — the queue and the workspace move; the rest of the console stays Wave 3.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-005): The conversation queue carried the full case toolset; the queue is about conversations and case work happens in SUP-013 and SUP-005. Keep listConversations … Removed 2 October 2026 (CHG-WIR-005): The conversation queue carried the full case toolset; the queue is about conversations and case work happens in SUP-013 and SUP-005. Keep listConversations … Removed 2 October 2026 (CHG-WIR-005): The conversation queue carried the full case toolset; the queue is about conversations and case work happens in SUP-013 and SUP-005. Keep listConversations …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The conversation queue: people waiting now, oldest first, each with the assistant's summary so the agent opens with context and the guest does not repeat themselves. Claim takes it, Transfer passes it with its context.

**Fixed on main** (the package already carries these; draw what it says): The queue screen carries the full case toolset (case filters as text fields, Create case, Escalate, Reopen, Save case, Add case message). (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| State | select | — | With assistant · Queued · With agent · Waiting on guest · Resolved · Abandoned · Timed out | `listConversations` ?state |
| Assigned to me | toggle | — | — | `listConversations` ?assignedToMe |
| Channel | select | — | Web chat · In app chat · Whatsapp · SMS · Email · Kiosk · Voice | `listConversations` ?channel |

**Form: Transfer conversation** (modal, opened by *Transfer conversation*; *Transfer conversation* calls `transferConversation`, *Cancel* sends nothing)

**Collects what `transferConversation` sends before it is called.** Nothing in the body is required. Optional: `toPrincipalId`, `toQueueId`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To principal `toPrincipalId` | picker: choose a to principal | optional | — | — | shows names, sends the id | — | `transferConversation` body |
| To queue `toQueueId` | picker: choose a to queue | optional | — | — | shows names, sends the id | — | `transferConversation` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `transferConversation` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every conversation** (data table, from `listConversations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Telephony | grouped details | BL-083. `ConversationChannel` included `voice` with nothing behind it — the model anticipated telephony and stopped at the enum. |
| Assist session | the name it points at, never the id | BL-094. `startKioskAssist` recorded a staff member helping a guest and `createCase` recorded a service interaction, and neither referenced … |
| Channel | chip: Web chat, In app chat, Whatsapp, SMS, Email, Kiosk… | — |
| State | chip: With assistant, Queued, With agent, Waiting on guest, Resolved, Abandoned… | `withAssistant` and `queued` are different, and the second has a person waiting. |
| Subject | the name it points at, never the id | 22.8.3. Resolved from phone, email, membership number or a signed-in session. |
| Venue | the name it points at, never the id | — |
| Assigned principal | the name it points at, never the id | — |
| Queue | the name it points at, never the id | — |
| Queue position | 1,234 | Place among the unclaimed conversations in `queueId`, from the live agent queue (audit R149). |
| Estimated wait seconds | 1,234 | From the live agent queue — the conversations ahead divided across that queue's agents online now (audit R149). |
| Handover reason | chip: Guest requested, Assistant refused, Assistant failed, Out of scope, Negative … | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Claim conversation (secondary button) | `claimConversation` POST `/conversations/{conversationId}/claim` | — | Conversation | 409 Already claimed by another agent | — |
| Transfer conversation (secondary button) | `transferConversation` POST `/conversations/{conversationId}/transfer` | inline | Conversation | — | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Conversation row**: Channel, guest, state (queued vs with assistant vs with agent), wait in seconds, the assistant's one-line summary, language. *(source: F24 step 3; contracts/satellite/marketing-crm.yaml#listConversations)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Claim**: Opens the live chat (SUP-005); stops a second agent answering. *(source: contracts/satellite/marketing-crm.yaml#claimConversation)*
- **Transfer**: To an agent or queue; context travels. *(source: contracts/satellite/marketing-crm.yaml#transferConversation)*

**Data it reads**: `listConversations` (onLoad, The omnichannel inbox)

**Where the user goes next**

- → `SUP-001` Venue Management Sign In: *Agent Login*
- → `SUP-002` Agent Dashboard: *Agent Dashboard*; carries `caseId`
- → `SUP-005` Live Chat Workspace: *The agent answers*; carries `caseId`, `conversationId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The conversation queue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the conversation queue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No conversation queue yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, assignedToPrincipalId, breachedSla, priority and the conversation queue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `CASE_VIEW`, which `listConversations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already claimed by another agent |

#### Consistency with other screens

- Match `BO-795`: Same inbox.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- '{channel: WhatsApp, guest: Priya Nair, state: queued, wait: 48s, summary: Wants to move Day Pass to Sunday}'
- '{channel: Web chat, guest: Unknown visitor, state: with assistant, summary: Asking about prayer rooms}'
```

#### Permissions

- `listConversations` → `CASE_VIEW` (read) · staff
- `claimConversation` → `CASE_MANAGE` (configure) · staff
- `transferConversation` → `CASE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `CASE_VIEW`, which `listConversations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.8.1 | Omnichannel Inbox | Marketing & CRM | CONTRACTED | `listConversations` |
| 22.8.6 | Agent Workspace | Marketing & CRM | CONTRACTED | `claimConversation` |
| 22.8.17 | Conversation Routing | Marketing & CRM | CONTRACTED | `claimConversation` |
| 22.8.18 | Queue Management | Marketing & CRM | CONTRACTED | `claimConversation` |
| 2.8.11 | System shall support integration with telephony platforms such as Genesys, Avaya, Amazon Connect, Microsoft Teams, 3CX, or equivalent solutions. Features shall include click-to-call, caller … | Ticketing Sales | CONTRACTED | data `Conversation` |
| 2.13.20 | Users “staff-assist” screen to create, change, or resend tickets on behalf of guests—linked to CRM case ID for traceability | Ticketing Sales | CONTRACTED | data `Conversation` |
| 22.8.16 | AI Sentiment Analysis | Marketing & CRM | CONTRACTED | data `Conversation` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Support chat is native to TICVAI: a built-in AI chat assistant answers first, then escalates to a human "CR representative" role in the platform; offered white-labelled as a subscription add-on for smaller clients. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-256)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-004` · status **notStarted** · provenance generated
- Flow F24 *A guest asks the assistant and ends up with a person*, step 3: The conversation appears in the queue → With the assistant’s own summary, so the agent opens with context
- Flow F24 branch at step 3 (recoverable): when Two agents claim it at once, `claimConversation` refuses the second. **Two agents answering one guest reads as chaos** from the guest’s side and is common on a busy queue.
- Flow F24 branch at step 3 (abandonsFlow): when Nobody claims it before the guest gives up, `abandoned` from `queued` — **the number to watch.** A guest who asked for a person and left before getting one is a staffing failure, and it looks identical to a resolved conversation in any report …

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-004?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Claim conversation, Transfer conversation.
- [ ] Every transition is wired: `SUP-001`, `SUP-002`, `SUP-005`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-005` Live Chat Workspace

**Serve one live conversation to its end, with the guest's case beside it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Conversations · wave 2 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as agent, guest |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCases` reads the population and `getCase` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `caseId` (SUP-004), `conversationId` (SUP-004) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/live-chat-workspace` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Pulled to Wave 2 (CF-101) with SUP-004. An agent needs a queue and a place to answer from; canned responses and SLA reporting can wait.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The live chat with a guest: the whole thread (it came with the handover), guest context, composer with rich messages, and the case beside it. Internal notes and guest replies are distinct and the choice is required. Closing records an outcome that tells resolved from abandoned from a case raised.

**Fixed on main** (the package already carries these; draw what it says): Purpose is "Work with live chat workspace for this venue" and the case filters appear as text fields. (CHG-WIR-006).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Open · In progress · Awaiting guest · Escalated · Resolved · Closed | — | Sends `?status=` to `listCases`. | `listCases` ?status |
| Assigned to principal id | picker: choose an assigned to principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?assignedToPrincipalId=` to `listCases`. | `listCases` ?assignedToPrincipalId |
| Breached sla | toggle | optional | — | — | — | Sends `?breachedSla=` to `listCases`. | `listCases` ?breachedSla |
| Priority | radio group | optional | — | Low · Normal · High · Urgent | — | Sends `?priority=` to `listCases`. | `listCases` ?priority |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Membership | picker: choose a membership | — | — | `listCases` ?membershipId |

**Form: Add case message** (modal, opened by *Add case message*; *Add case message* calls `addCaseMessage`, *Cancel* sends nothing)

**Collects what `addCaseMessage` sends before it is called.** Required: `id`, `body`, `isInternal`, `recordedAt`. Optional: `channel`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `addCaseMessage` body |
| Body `body` | text area | required | — | min length 1; max length 10000 | — | — | `addCaseMessage` body |
| Is internal `isInternal` | toggle | required | — | — | — | — | `addCaseMessage` body |
| Channel `channel` | select | optional | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `addCaseMessage` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `addCaseMessage` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addCaseMessage` body |

**Form: Save case** (modal, opened by *Save case*; *Save case* calls `updateCase`, *Cancel* sends nothing)

**Collects what `updateCase` sends before it is called.** Nothing in the body is required. Optional: `status`, `priority`, `assignedToPrincipalId`, `categoryId`, `resolutionNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | optional | — | Open · In progress · Awaiting guest · Escalated · Resolved · Closed | — | — | `updateCase` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent | — | — | `updateCase` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `updateCase` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateCase` body |
| Resolution note `resolutionNote` | text area | optional | — | max length 2000 | — | — | `updateCase` body |

Errors to draw in the form: 400 Resolving without a resolution note

**Form: Escalate case** (modal, opened by *Escalate case*; *Escalate case* calls `escalateCase`, *Cancel* sends nothing)

**Collects what `escalateCase` sends before it is called.** Required: `reason`. Optional: `assignToPrincipalId`, `newPriority`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `escalateCase` body |
| Assign to principal `assignToPrincipalId` | picker: choose an assign to principal | optional | — | — | shows names, sends the id | — | `escalateCase` body |
| New priority `newPriority` | radio group | optional | — | Low · Normal · High · Urgent | — | — | `escalateCase` body |

**Form: Create case** (modal, opened by *Create case*; *Create case* calls `createCase`, *Cancel* sends nothing)

**Collects what `createCase` sends before it is called.** Required: `id`, `subject`, `description`, `channel`, `recordedAt`. Optional: `subjectId`, `categoryId`, `priority`, `kind`, `venueId`, `relatedOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createCase` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `createCase` body |
| Subject `subject` | text field | required | — | max length 200 | — | — | `createCase` body |
| Description `description` | text area | required | — | max length 10000 | — | — | `createCase` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `createCase` body |
| Membership `membershipId` | picker: choose a membership | optional | — | — | shows names, sends the id | The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. | `createCase` body |
| Priority `priority` | radio group | optional | Normal | Low · Normal · High · Urgent | — | — | `createCase` body |
| Kind `kind` | select | optional | — | Lost property · Complaint · Question · Accessibility · Refund request · Other; Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.; A case raised as `other` must carry a non-empty `detail` … | — | What the guest says the case is about, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. | `createCase` body |
| Channel `channel` | select | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `createCase` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCase` body |
| Related order `relatedOrderId` | text field | optional | — | — | — | — | `createCase` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | Stored on the opening `CaseMessage`, not on the case. | `createCase` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time the case was raised. The server stamps `Case.syncedAt` on arrival. | `createCase` body |

**Form: Reopen case** (modal, opened by *Reopen case*; *Reopen case* calls `reopenCase`, *Cancel* sends nothing)

**Collects what `reopenCase` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `reopenCase` body |

Errors to draw in the form: 409 The case is not `resolved` — a `closed` case is past its reopen window, and an open one has nothing to reopen. (StateTransitionProblem)

**Form: Send conversation message** (modal, opened by *Send conversation message*; *Send conversation message* calls `sendConversationMessage`, *Cancel* sends nothing)

**Collects what `sendConversationMessage` sends before it is called.** Required: `body`. Optional: `attachments`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Body `body` | text area | required | — | max length 4000 | — | — | `sendConversationMessage` body |
| Attachments `attachments` | repeatable rows | optional | — | — | — | — | `sendConversationMessage` body |
| Asset `attachments[].assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `sendConversationMessage` body |
| Kind `attachments[].kind` | select | optional | — | Image · Video · Document · Ticket · QR · Payment link | — | — | `sendConversationMessage` body |

**Form: Transfer conversation** (modal, opened by *Transfer conversation*; *Transfer conversation* calls `transferConversation`, *Cancel* sends nothing)

**Collects what `transferConversation` sends before it is called.** Nothing in the body is required. Optional: `toPrincipalId`, `toQueueId`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To principal `toPrincipalId` | picker: choose a to principal | optional | — | — | shows names, sends the id | — | `transferConversation` body |
| To queue `toQueueId` | picker: choose a to queue | optional | — | — | shows names, sends the id | — | `transferConversation` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `transferConversation` body |

**Sent by *Close conversation*** (`closeConversation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | radio group | required | — | Resolved · Case raised · Abandoned by guest · Timed out · Spam | — | — | `closeConversation` body |
| Case `caseId` | picker: choose a case | optional | — | — | shows names, sends the id | — | `closeConversation` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every case** (data table, from `listCases`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7. |
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Subject | the name it points at, never the id | — |
| Guest name | text | Resolved from `pii.subject` when the case is read, never stored on the case. A name copied onto a case row is personal data outside the … |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Category | the name it points at, never the id | — |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Priority | chip: Low, Normal, High, Urgent | — |
| Assigned to principal | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Related order | text | — |
| Sla due at | 1 Oct 2026, 14:30 | — |

**The selected case** (detail panel, from `listCases`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7. |
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Subject | the name it points at, never the id | — |
| Guest name | text | Resolved from `pii.subject` when the case is read, never stored on the case. A name copied onto a case row is personal data outside the … |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Kind | chip: Lost property, Complaint, Question, Accessibility, Refund request, Other | What the guest said it was about, where the guest raised it. |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`. |
| Recorded at | 1 Oct 2026, 14:30 | Device time the case was raised — the start of the SLA clock. |
| Synced at | 1 Oct 2026, 14:30 | Server time the case arrived. Equal to `recordedAt` for a case raised online. |
| Category | the name it points at, never the id | — |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Priority | chip: Low, Normal, High, Urgent | — |
| Assigned to principal | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Related order | text | — |
| Sla due at | 1 Oct 2026, 14:30 | — |

**The conversation** (detail panel, from `getConversation`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Telephony | grouped details | BL-083. `ConversationChannel` included `voice` with nothing behind it — the model anticipated telephony and stopped at the enum. |
| Assist session | the name it points at, never the id | BL-094. `startKioskAssist` recorded a staff member helping a guest and `createCase` recorded a service interaction, and neither referenced … |
| Channel | chip: Web chat, In app chat, Whatsapp, SMS, Email, Kiosk… | — |
| State | chip: With assistant, Queued, With agent, Waiting on guest, Resolved, Abandoned… | `withAssistant` and `queued` are different, and the second has a person waiting. |
| Subject | the name it points at, never the id | 22.8.3. Resolved from phone, email, membership number or a signed-in session. |
| Venue | the name it points at, never the id | — |
| Assigned principal | the name it points at, never the id | — |
| Queue | the name it points at, never the id | — |
| Queue position | 1,234 | Place among the unclaimed conversations in `queueId`, from the live agent queue (audit R149). |
| Estimated wait seconds | 1,234 | From the live agent queue — the conversations ahead divided across that queue's agents online now (audit R149). |
| Handover reason | chip: Guest requested, Assistant refused, Assistant failed, Out of scope, Negative … | — |
| Handover summary | text | The assistant's own account of what the guest wants, so an agent opens with context rather than reading a transcript while somebody waits. |
| Sentiment | chip: Positive, Neutral, Negative, Escalating | 22.8.16. `escalating` is a routing signal, not a report line. |
| Intent | text | 22.8.13. What the guest appears to want, used for routing. |
| Locale | text | — |

**The case** (detail panel, from `getCase`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7. |
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Subject | the name it points at, never the id | — |
| Guest name | text | Resolved from `pii.subject` when the case is read, never stored on the case. A name copied onto a case row is personal data outside the … |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Kind | chip: Lost property, Complaint, Question, Accessibility, Refund request, Other | What the guest said it was about, where the guest raised it. |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`. |
| Recorded at | 1 Oct 2026, 14:30 | Device time the case was raised — the start of the SLA clock. |
| Synced at | 1 Oct 2026, 14:30 | Server time the case arrived. Equal to `recordedAt` for a case raised online. |
| Category | the name it points at, never the id | — |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Priority | chip: Low, Normal, High, Urgent | — |
| Assigned to principal | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Related order | text | — |
| Sla due at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add case message (primary button) | `addCaseMessage` POST `/cases/{caseId}/messages` | inline | CaseMessage | — | opens modal first |
| Save case (secondary button) | `updateCase` PATCH `/cases/{caseId}` | inline | Case | 400 Resolving without a resolution note | opens modal first |
| Escalate case (secondary button) | `escalateCase` POST `/cases/{caseId}/escalate` | inline | Case | — | opens modal first |
| Create case (secondary button) | `createCase` POST `/cases` | CreateCaseRequest | Case | — | opens modal first |
| Reopen case (secondary button) | `reopenCase` POST `/cases/{caseId}/reopen` | inline | Case | 409 The case is not `resolved` — a `closed` case is past its reopen window, and an open one has nothing to reopen. (StateTransitionProblem) | opens modal first |
| Send conversation message (secondary button) | `sendConversationMessage` POST `/conversations/{conversationId}/messages` | inline | ConversationMessage | — | opens modal first |
| Close conversation (destructive button) | `closeConversation` POST `/conversations/{conversationId}/close` | inline | Conversation | — | — |
| Transfer conversation (secondary button) | `transferConversation` POST `/conversations/{conversationId}/transfer` | inline | Conversation | — | opens modal first |

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Send**: As the agent; a note is visibly internal. *(source: contracts/satellite/marketing-crm.yaml#sendConversationMessage; F05 step 2)*
- **Close**: Resolved, abandoned by the guest, or timed out, never merged into one number; or Raise case, which names the case. *(source: contracts/satellite/marketing-crm.yaml#closeConversation; F24 step 5)*
- **Resolve case**: Requires a resolution note. *(source: F05 step 3)*

**Data it reads**: `getCase` (onLoad, Case with its thread); `listCases` (onLoad, List service cases); `getConversation` (onLoad, One conversation and everything before it)

**Where the user goes next**

- → `SUP-001` Venue Management Sign In: *Agent Login*
- → `SUP-002` Agent Dashboard: *Agent Dashboard*; carries `caseId`

**What opens over it**

- confirmDialog *Close conversation*: **Names what `closeConversation` changes and what it leaves alone**, in the consequence rather than the verb. A live chat this affects should be identified in the dialog, not just counted. **Collects what `closeConversation` sends before it is called.** Required: `outcome`. Optional: `caseId`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The live chat list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live chat untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live chat yet. Offers Add case message (`addCaseMessage`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, assignedToPrincipalId, breachedSla, priority and the live chat are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `CASE_VIEW`, which `getCase` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Resolving without a resolution note; 409 The case is not `resolved` — a `closed` case is past its reopen window, and an open one has nothing to reopen. (StateTransitionProblem) |

#### Edge cases to draw

- **The guest asks for a refund**: The agent raises a refund request; above the venue threshold it goes to approval. Never a direct refund. *(source: F05 step 2)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
thread:
- 'Guest (WhatsApp, 10:41): Can I move my Day Pass to Sunday?'
- 'Assistant (10:41): Let me get a colleague.'
- '"Aisha (10:42): Hi Priya'
- yes - Sunday 4 Oct is available at no charge."
```

#### Permissions

- `addCaseMessage` → `CASE_MANAGE` (configure) · staff, partner
- `getCase` → `CASE_VIEW` (read) · staff, partner
- `updateCase` → `CASE_MANAGE` (configure) · staff, partner
- `escalateCase` → `CASE_MANAGE` (configure) · staff, partner
- `createCase` → `CASE_MANAGE` (configure) · staff, guest, partner
- `listCases` → `CASE_VIEW` (read) · staff, guest, partner
- `reopenCase` → `CASE_MANAGE` (configure) · staff, partner
- `getConversation` → `CASE_VIEW` (read) · staff
- `sendConversationMessage` → `CASE_MANAGE` (configure) · staff, guest
- `closeConversation` → `CASE_MANAGE` (configure) · staff
- `transferConversation` → `CASE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `CASE_VIEW`, which `getCase` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

22 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.3.7 | Agent Notes & Attachments | Marketing & CRM | CONTRACTED | `addCaseMessage` |
| 22.3.10 | Case Audit Trail | Marketing & CRM | CONTRACTED | `getCase` |
| 22.3.4 | Case Workflow Management | Marketing & CRM | CONTRACTED | `updateCase` |
| 22.3.6 | Case Escalation Management | Marketing & CRM | CONTRACTED | `escalateCase` |
| 19.2.66 | Guest Support - System shall provide guest support channels. | Guest Mobile App & Branding | CONTRACTED | `createCase` |
| 19.2.70 | Complaint Management - System shall support guest complaints. | Guest Mobile App & Branding | CONTRACTED | `createCase` |
| 2.8.12 | System shall allow agents to create, assign, escalate, track, and resolve guest cases including complaints, refund requests, service requests, incidents, and operational issues. Cases shall be linked … | Ticketing Sales | CONTRACTED | `createCase` |
| 5.3.34 | Link guest profiles with customer service cases, complaints, incidents, refunds, investigations, and follow-up activities. | F&B & Guest Management | CONTRACTED | `createCase` |
| 22.3.1 | Case Creation | Marketing & CRM | CONTRACTED | `createCase` |
| 22.3.2 | Case Classification | Marketing & CRM | CONTRACTED | `createCase` |
| 22.3.3 | Case Assignment | Marketing & CRM | CONTRACTED | `createCase` |
| 22.8.12 | Case Creation & Escalation | Marketing & CRM | CONTRACTED | `createCase` |
| … 10 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Support chat is native to TICVAI: a built-in AI chat assistant answers first, then escalates to a human "CR representative" role in the platform; offered white-labelled as a subscription add-on for smaller clients. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-256)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-005` · status **notStarted** · provenance generated
- Flow F05 *Agent resolves a guest complaint*, step 1: Picks up the case → Sees SLA state and priority, breached first
- Flow F05 *Agent resolves a guest complaint*, step 2: Reads the history and replies → Internal notes and guest replies are distinct, and the distinction is required rather than defaulted
- Flow F05 *Agent resolves a guest complaint*, step 3: Resolves or escalates → Resolution requires a note. A case closed with no findings is a lesson nobody learned
- Flow F24 *A guest asks the assistant and ends up with a person*, step 4: The agent answers → **The guest has not repeated themselves.** The whole thread came with the handover
- Flow F24 *A guest asks the assistant and ends up with a person*, step 5: Resolves it, or raises a case → Closed with an outcome that distinguishes resolved from a case raised
- Flow F05 branch at step 2 (requiresStaff): when The guest asks for a refund, The agent raises a refund request rather than refunding. Above the venue threshold it enters the approval queue — a guest cannot self-serve money out of the ledger and neither can a first-line agent.
- Flow F05 branch at step 2 (dataLoss): when An internal note is sent to the guest by mistake, isInternal is required, never defaulted, and the reply target is shown in the composer. Once sent it cannot be recalled — the prevention is the control.
- Flow F05 branch at step 3 (recoverable): when SLA breaches while awaiting an internal team, The clock does not pause. It pauses only while awaiting the guest — otherwise every breach becomes someone else queue and the metric stops meaning anything.
- Flow F24 branch at step 4 (recoverable): when The agent needs to take over the kiosk, `startKioskAssist`. Acts on the kiosk session **under their own permission** — a cashier completing a guest’s checkout remotely is a staff action on a guest cart, recorded as theirs. The guest sees …
- Flow F24 branch at step 4 (recoverable): when The conversation needs another team, `transferConversation`. **The context travels again** — a guest transferred twice should still not have repeated themselves.

#### Acceptance for the design

- [ ] Every input above is drawn (41), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (60 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add case message, Save case, Escalate case, Create case, Reopen case, Send conversation message, Close conversation, Transfer conversation.
- [ ] Every transition is wired: `SUP-001`, `SUP-002`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
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

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addCaseMessage": {"method":"POST","path":"/cases/{caseId}/messages","contract":"marketing-crm","summary":"Add a message or internal note","permission":"CASE_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CaseMessage"},
"claimConversation": {"method":"POST","path":"/conversations/{conversationId}/claim","contract":"marketing-crm","summary":"An agent takes it","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Conversation"},
"closeConversation": {"method":"POST","path":"/conversations/{conversationId}/close","contract":"marketing-crm","summary":"End it","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Conversation"},
"createCase": {"method":"POST","path":"/cases","contract":"marketing-crm","summary":"Raise a service case","permission":"CASE_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCaseRequest","responds":"Case"},
"escalateCase": {"method":"POST","path":"/cases/{caseId}/escalate","contract":"marketing-crm","summary":"Escalate a case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Case"},
"getCase": {"method":"GET","path":"/cases/{caseId}","contract":"marketing-crm","summary":"Read a case with its thread","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CaseDetail"},
"getConversation": {"method":"GET","path":"/conversations/{conversationId}","contract":"marketing-crm","summary":"One conversation and everything before it","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"Conversation"},
"listCases": {"method":"GET","path":"/cases","contract":"marketing-crm","summary":"List service cases","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"assignedToPrincipalId","in":"query","required":null},{"name":"breachedSla","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"membershipId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConversations": {"method":"GET","path":"/conversations","contract":"marketing-crm","summary":"The omnichannel inbox","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"state","in":"query","required":null},{"name":"assignedToMe","in":"query","required":null},{"name":"channel","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"reopenCase": {"method":"POST","path":"/cases/{caseId}/reopen","contract":"marketing-crm","summary":"Reopen a resolved case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Case"},
"sendConversationMessage": {"method":"POST","path":"/conversations/{conversationId}/messages","contract":"marketing-crm","summary":"Say something, as a guest or an agent","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConversationMessage"},
"transferConversation": {"method":"POST","path":"/conversations/{conversationId}/transfer","contract":"marketing-crm","summary":"Pass it to another agent or queue","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Conversation"},
"updateCase": {"method":"PATCH","path":"/cases/{caseId}","contract":"marketing-crm","summary":"Assign, reprioritise or resolve a case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Case"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Case": {"x-ticvai-persistence":"marketing.case","x-ticvai-retired-columns":["guest_name","subject","is_sla_breached"],"type":"object","required":["id","caseNumber","subject","status","priority","createdAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."},"caseNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"},"subject":{"type":"string","x-ticvai-column":"title","description":"**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"},"kind":{"allOf":[{"$ref":"#/components/schemas/CaseKind"}],"nullable":true,"description":"What the guest said it was about, where the guest raised it."},"channel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"description":"How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised — the start of the SLA clock."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the case arrived. Equal to `recordedAt` for a case raised online."},"categoryId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"},"status":{"$ref":"#/components/schemas/CaseStatus"},"priority":{"$ref":"#/components/schemas/CasePriority"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"relatedOrderId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"isSlaBreached":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"},"slaPausedSeconds":{"type":"integer","description":"Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"},"escalationCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"CaseDetail": {"x-ticvai-persistence":"marketing.case","allOf":[{"$ref":"#/components/schemas/Case"},{"type":"object","properties":{"description":{"type":"string"},"resolutionNote":{"type":"string","nullable":true},"messages":{"type":"array","items":{"$ref":"#/components/schemas/CaseMessage"}}}}]},
"CaseKind": {"type":"string","description":"**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n","enum":["lostProperty","complaint","question","accessibility","refundRequest","other"]},
"CaseMessage": {"x-ticvai-persistence":"marketing.case_message","type":"object","required":["id","body","isInternal","authorKind","recordedAt"],"properties":{"resolution":{"type":"string","description":"**What was actually done about it.** Indexed for retrieval: an agent facing a complaint benefits more from how the last one was resolved than from a policy. Without this column `marketing.case` can only embed its subject line.\n"},"id":{"type":"string"},"body":{"type":"string"},"isInternal":{"type":"boolean"},"authorKind":{"type":"string","enum":["agent","guest","system","ai"]},"authorPrincipalId":{"type":"string","format":"uuid","nullable":true},"channel":{"$ref":"#/components/schemas/MessageChannel"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time","description":"Device time — `addCaseMessage` is offline-capable."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the message arrived."}}},
"CasePriority": {"type":"string","enum":["low","normal","high","urgent"]},
"CaseStatus": {"type":"string","enum":["open","inProgress","awaitingGuest","escalated","resolved","closed"]},
"Conversation": {"type":"object","x-ticvai-persistence":"marketing.conversation","description":"22.8. **A conversation is not a case.** A case is a ticket measured in hours; a conversation is a live session measured in seconds, with somebody waiting. A conversation may create a case; it is not one.\n","required":["id","channel","state"],"properties":{"id":{"type":"string","format":"uuid"},"telephony":{"type":"object","nullable":true,"description":"BL-083. **`ConversationChannel` included `voice` with nothing behind it** — the model anticipated telephony and stopped at the enum.\n**Not an integration, a binding.** Genesys, Avaya, Amazon Connect, Teams and 3CX all do call control themselves; what the platform needs is the call bound to the guest and the case, so **an agent who answers already knows who is calling and what about.**\n","properties":{"providerCallId":{"type":"string"},"direction":{"type":"string","enum":["inbound","outbound","transferred"]},"fromNumberMasked":{"type":"string","nullable":true,"description":"**Masked, and it is still personal data.** A phone number identifies a person more reliably than a name does.\n"},"recordingRef":{"type":"string","nullable":true,"description":"Held by the provider, referenced here. **Recording consent is jurisdictional and the platform does not assume it** — a reference with no consent record is a recording nobody may play.\n"},"agentState":{"type":"string","enum":["available","onCall","wrapUp","away","offline"],"nullable":true}}},"assistSessionId":{"type":"string","format":"uuid","nullable":true,"description":"BL-094. **`startKioskAssist` recorded a staff member helping a guest and `createCase` recorded a service interaction, and neither referenced the other** — so the traceability 2.13.20 asks for had no link to follow.\n**The link is here rather than on the assist session**, because a case may span several assists and an assist belongs to at most one case.\n"},"channel":{"$ref":"#/components/schemas/ConversationChannel"},"state":{"$ref":"#/components/schemas/ConversationState"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"22.8.3. Resolved from phone, email, membership number or a signed-in session. **A conversation with none of those stays anonymous rather than being guessed at.**\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"assignedPrincipalId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true},"queuePosition":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onRead","description":"Place among the unclaimed conversations in `queueId`, from the live agent queue (audit R149). Null once claimed."},"estimatedWaitSeconds":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onRead","description":"From the live agent queue — the conversations ahead divided across that queue's agents online now (audit R149). Null once claimed."},"handoverReason":{"type":"string","nullable":true,"enum":["guestRequested","assistantRefused","assistantFailed","outOfScope","negativeSentiment","complexIntent","paymentIssue"]},"handoverSummary":{"type":"string","nullable":true,"description":"**The assistant's own account of what the guest wants**, so an agent opens with context rather than reading a transcript while somebody waits.\n"},"sentiment":{"type":"string","nullable":true,"enum":["positive","neutral","negative","escalating"],"description":"22.8.16. **`escalating` is a routing signal**, not a report line."},"intent":{"type":"string","nullable":true,"description":"22.8.13. What the guest appears to want, used for routing."},"locale":{"type":"string"},"caseId":{"type":"string","format":"uuid","nullable":true,"description":"22.8.12. Where the conversation raised one."},"messages":{"type":"array","items":{"$ref":"#/components/schemas/ConversationMessage"}},"firstResponseSeconds":{"type":"integer","nullable":true,"readOnly":true},"startedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"outcome":{"type":"string","nullable":true,"enum":["resolved","caseRaised","abandonedByGuest","timedOut","spam"]}}},
"ConversationChannel": {"type":"string","enum":["webChat","inAppChat","whatsapp","sms","email","kiosk","voice"]},
"ConversationMessage": {"type":"object","x-ticvai-persistence":"marketing.conversation_message + marketing.conversation_message_attachment","required":["id","sender","body","sentAt"],"properties":{"id":{"type":"string","format":"uuid"},"sender":{"type":"string","enum":["guest","agent","assistant","system"],"description":"**Resolved, never declared.** The assistant is labelled as one — a guest talking to a bot that presents as a person is a complaint waiting for the moment they find out.\n"},"senderPrincipalId":{"type":"string","format":"uuid","nullable":true},"body":{"type":"string"},"attachments":{"type":"array","items":{"type":"object","properties":{"assetId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["image","video","document","ticket","qr","paymentLink"]}}}},"aiInteractionId":{"type":"string","format":"uuid","nullable":true,"description":"Where the assistant sent it. **Links the message to its tokens and cost**, so a conversation's spend is attributable (CF-14).\n"},"sentAt":{"type":"string","format":"date-time"},"readAt":{"type":"string","format":"date-time","nullable":true}}},
"ConversationState": {"type":"string","description":"**`withAssistant` and `queued` are different, and the second has a person waiting.** Merging them makes the service level unmeasurable, because time with a bot is not time in a queue.\n","enum":["withAssistant","queued","withAgent","waitingOnGuest","resolved","abandoned","timedOut"]},
"CreateCaseRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","subject","description","channel","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"subject":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":10000},"categoryId":{"type":"string","format":"uuid"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. Must belong to `subjectId` when both are given (422). (decided 29 September, coordinator decision DM4, writers pass)"},"priority":{"allOf":[{"$ref":"#/components/schemas/CasePriority"}],"default":"normal"},"kind":{"$ref":"#/components/schemas/CaseKind"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"venueId":{"type":"string","format":"uuid"},"relatedOrderId":{"type":"string"},"attachmentRefs":{"type":"array","description":"Stored on the opening `CaseMessage`, not on the case.","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised. The server stamps `Case.syncedAt` on arrival."}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
