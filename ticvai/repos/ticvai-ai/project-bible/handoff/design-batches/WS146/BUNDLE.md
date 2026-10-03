# WS146 — Marketing CRM Configuration Reference v1.0 board 12

**10 screens · 12 operations · 16 schemas · 3 permissions**

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
| `BO-844` | Waiver Command Center | D | 0 | 0 | 6 | 0 | 1 | 4 | — | notStarted (—) |
| `BO-845` | Waiver Template Builder | D | 20 | 20 | 6 | 0 | 1 | 4 | — | notStarted (—) |
| `BO-846` | Assignment Rules | D | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-847` | Version, Expiry & Renewal | D | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-848` | Signature Experience Setup | D | 17 | 20 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-849` | Guardian & Group Signing | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-850` | Pre-Arrival Completion | D | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-851` | Verification & Access Control | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-852` | Documents, Search & Retention | D | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-853` | Legal Evidence & Audit | D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-844, BO-845, BO-846, BO-847, BO-848, BO-849, BO-850, BO-851, BO-853 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-844` Waiver Command Center

**Monitor waiver completion, expiry and operational access risk. Show required, completed, pending, expired and expiring waivers, blocked entries and guardian signatures. Analyze completion by venue, activity, event, product, channel, guest type and arrival date. Surface missing signatures, failed verification, version changes requiring re-sign and access-control exceptions. Provide operational drill-down and alerts without exposing document content to unauthorized roles. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-844 |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/waiver-command-center-bo-844` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Waiver readiness: required, completed, pending, expired and expiring waivers, blocked entries and guardian signatures, by venue, activity, product, channel and arrival date; upcoming activities most at risk, without exposing document content.

**Known correction pending (do not draw the wrong version)**

- **BO-844 to BO-853 duplicate the CMS waiver screens CMS-041 to CMS-060 (same operations, e.g. listWaiver, listParticipantWaiverStatus, setSignatorySignatureGuardian).** Why: As with the other Digital Experience screens (DI-996), build once. Proposal - the CMS owns waiver configuration (templates, fields, signatories, rules, versions, publication) and the back office keeps operations (status, verification at the gate, pre-arrival chasing). *(source: DI-996; contracts/satellite/marketing-crm.yaml#listWaiver; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **At-risk activities**: Activity, start time, participants, unsigned count; blocked entries today. *(source: contracts/satellite/marketing-crm.yaml#listWaiver; DI-576)*

**Data it reads**: `listWaiver` (onLoad, Waiver Operations Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-845` Waiver Template Builder: *Waiver Template Builder*
- → `BO-846` Assignment Rules: *Assignment Rules*
- → `BO-847` Version, Expiry & Renewal: *Version, Expiry & Renewal*
- → `BO-848` Signature Experience Setup: *Signature Experience Setup*
- → `BO-849` Guardian & Group Signing: *Guardian & Group Signing*
- → `BO-850` Pre-Arrival Completion: *Pre-Arrival Completion*
- → `BO-851` Verification & Access Control: *Verification & Access Control*
- → `BO-852` Documents, Search & Retention: *Documents, Search & Retention*
- → `BO-853` Legal Evidence & Audit: *Legal Evidence & Audit*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The waiver list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the waiver untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No waiver yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the waiver are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `CMS-051`: The same waiver operations command centre (listWaiver) exists in the CMS.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
atRisk: Deep Dive 14:00 - 12 participants - 3 unsigned (2 minors awaiting guardian)
```

#### Permissions

- `listWaiver` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Waiver dashboard tracks templates (published vs draft) and completion status. Templates can be cloned and are built with drag-and-drop fields (name, DOB, custom fields, T&C checkboxes). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-570)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-844` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-844`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 12
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 1: Opens Waiver Command Center → Monitor waiver completion, expiry and operational access risk. Show required, completed, pending, expired and expiring waivers, blocked entries and guardian signatures. Analyze completion by venue …
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F255 branch at step 1 (expected): when Nothing has been set up on Waiver Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F255 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-844?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-845`, `BO-846`, `BO-847`, `BO-848`, `BO-849`, `BO-850`, `BO-851`, `BO-852`, `BO-853`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-845` Waiver Template Builder

**Create legal waiver and declaration templates without development. Support liability release, general consent, parental consent, medical declaration, risk acknowledgement and activity agreement types. Provide sections, clauses, variables, conditional content, initials, attachments and signature blocks. Manage multilingual content, legal owner, jurisdiction, risk category, approval and preview. Version every legal change and prohibit publishing until required legal and business approvals complete. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-845 |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/waiver-template-builder-bo-845` |

**Known gaps.** **Waiver Template Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Waiver and declaration templates without development: liability release, general consent, parental consent, medical declaration, risk acknowledgement, activity agreement; sections, clauses, variables, conditional content, initials, signature blocks; EN and AR; legal owner and approval. Every legal change is a version.

**Fixed on main** (the package already carries these; draw what it says): Declares only listWaiver (the operations command centre read). (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Waiver type | select | — | Liability waiver · Parent guardian consent · Participation consent · Medical declaration · Safety acknowledgement · Media consent · Rental agreement · Terms acceptance · Membership declaration · Custom form | `listWaiverTemplateMaster` ?waiverType |
| Brand | picker: choose a brand | — | — | `listWaiverTemplateMaster` ?brandId |
| Is master template | toggle | — | — | `listWaiverTemplateMaster` ?isMasterTemplate |
| Q | text field | — | max length 100 | `listWaiverTemplateMaster` ?q |

**Form: Save layout** (modal, opened by *Save layout*; *Save layout* calls `setDigitalWaiverForm`, *Cancel* sends nothing)

**Collects what `setDigitalWaiverForm` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Form `formId` | picker: choose a form | required | — | — | shows names, sends the id | — | `setDigitalWaiverForm` body |
| Form version `formVersion` | number field | required | — | min 1 | — | — | `setDigitalWaiverForm` body |
| Sections `sections` | repeatable rows | required | — | at least 1 | — | — | `setDigitalWaiverForm` body |
| Section key `sections[].sectionKey` | text field | required | — | max length 60 | — | — | `setDigitalWaiverForm` body |
| Kind `sections[].kind` | select | required | — | Header · Participant information · Waiver terms · Safety acknowledgements · Questions · Consent · Signature · Custom | — | — | `setDigitalWaiverForm` body |
| Title `sections[].title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setDigitalWaiverForm` body |
| Numbered `sections[].numbered` | toggle | optional | off | — | — | — | `setDigitalWaiverForm` body |
| Mandatory reading `sections[].mandatoryReading` | toggle | optional | off | — | — | The signatory must tick "I have read and understood this section" before continuing. | `setDigitalWaiverForm` body |
| Acknowledgement text `sections[].acknowledgementText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setDigitalWaiverForm` body |
| Show when `sections[].showWhen` | group | optional | — | Shown only when the condition holds, e. | — | Shown only when the condition holds, e.g. `isMinor` equals `true` shows the guardian section. | `setDigitalWaiverForm` body |
| Subject `sections[].showWhen.subject` | text field | required | — | max length 60 | — | A field key of this version, or `isMinor` (resolved from the waiver's guardian threshold). | `setDigitalWaiverForm` body |
| Operator `sections[].showWhen.operator` | select | required | — | Equals · Not equals · In · Less than · Greater than · Is answered | — | — | `setDigitalWaiverForm` body |
| Value `sections[].showWhen.value` | text field | optional | — | max length 200 | — | — | `setDigitalWaiverForm` body |
| Blocks `sections[].blocks` | repeatable rows | required | — | — | — | — | `setDigitalWaiverForm` body |
| Block key `sections[].blocks[].blockKey` | text field | required | — | max length 60 | — | — | `setDigitalWaiverForm` body |
| Kind `sections[].blocks[].kind` | select | required | — | Heading · Paragraph · Legal text · Instructions · Image logo · Divider · Information box · Checkbox · Acknowledgement · Question · Signature · Initials … | — | — | `setDigitalWaiverForm` body |
| Content `sections[].blocks[].content` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setDigitalWaiverForm` body |
| Asset `sections[].blocks[].assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The image for an `imageLogo` block. | `setDigitalWaiverForm` body |
| Field key `sections[].blocks[].fieldKey` | text field | optional | — | max length 60 | — | The `FormField.key` an input block collects; required for input kinds. | `setDigitalWaiverForm` body |
| Mandatory notice `sections[].blocks[].mandatoryNotice` | toggle | optional | off | Rendered as a notice that cannot be collapsed. | — | Rendered as a notice that cannot be collapsed. | `setDigitalWaiverForm` body |

Errors to draw in the form: 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The version is no longer a draft.; 422 A block names a field the version does not have, or a block kind needs content it lacks.

#### Outputs: what the screen shows and produces

**Shown**

**Templates** (data table, from `listWaiverTemplateMaster`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Waiver | the name it points at, never the id | The `FormDefinition.id`; the natural key. |
| Waiver name | text | `FormDefinition.name`, shown here, written by `createForm`. |
| Internal description | text | — |
| Waiver type | chip: Liability waiver, Parent guardian consent, Participation consent, Medical … | — |
| Custom type label | text | The tenant's own classification name; required when `waiverType` is `customForm`. |
| Owner user | the name it points at, never the id | — |
| Department | text | — |
| Brand | the name it points at, never the id | Null for a corporate waiver every brand may use. |
| Legal entity | the name it points at, never the id | The finance legal entity the waiver is given in favour of. |
| Default language | text | — |
| Applicable countries | list or chips (count when long) | ISO 3166-1 alpha-2. Empty means the waiver is not yet scoped, which blocks publication. |
| Applicable jurisdiction | text | A sub-national jurisdiction where the law differs within a country. |
| Status | chip: Draft, Review, Pending approval, Approved, Scheduled, Published… | The lifecycle status of the latest version (see `listWaiverConsent`). |
| Template source | chip: Create new, Duplicate existing, Master template, Corporate template | — |
| Source waiver | the name it points at, never the id | The waiver it was duplicated or created from; required unless `createNew`. |
| Source version | 1,234 | — |
| Is master template | yes / no (icon or chip) | Offered in the reusable library. A corporate template is a master template with no `brandId`. |
| Business owner user | the name it points at, never the id | — |
| Legal reviewer user | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save layout (secondary button) | `setDigitalWaiverForm` PUT `/digital-waiver-form` | DigitalWaiverFormBuilderInput | DigitalWaiverFormBuilderView | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The version is no longer a draft. | opens modal first |

**Data it reads**: `listWaiverTemplateMaster` (onLoad, The waiver templates)

**Where the user goes next**

- → `BO-844` Waiver Command Center: *Back to Waiver Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The waiver template list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the waiver template untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No waiver template yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the waiver template are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The version is no longer a draft.; 422 A block names a field the version does not have, or a block kind needs content it lacks. |

#### Consistency with other screens

- Match `CMS-043`: The CMS builder.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
template: Deep Dive liability release v3 - EN/AR - owner Legal - approved
```

#### Permissions

- `listWaiverTemplateMaster` → `GUEST_VIEW` (read) · staff
- `setDigitalWaiverForm` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Waiver dashboard tracks templates (published vs draft) and completion status. Templates can be cloned and are built with drag-and-drop fields (name, DOB, custom fields, T&C checkboxes). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-570)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-845` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-845`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 12
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 2: Works in Waiver Template Builder → Create legal waiver and declaration templates without development. Support liability release, general consent, parental consent, medical declaration, risk acknowledgement and activity agreement …

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-845?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save layout.
- [ ] Every transition is wired: `BO-844`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-846` Assignment Rules

**Determine which waiver or form each guest must complete. Build rules using product, attraction, event, activity, venue, age, membership, risk category and jurisdiction. Configuration Scope of Work / Version 1.0 58 Assign one or multiple required documents with priority, effective dates and exception handling. Detect conflicting, missing or circular rules and simulate results for sample guests/bookings. Version, approve and audit rules and retain the rule/version used for each assignment. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-846 |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/assignment-rules-bo-846` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): setDigitalWaiverForm saves a waiver's layout; assignment is the trigger and eligibility rules (listWaiverTriggerEligibility, as on CMS-047) (design-notes …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Which waiver each guest must complete: rules by product, attraction, event, activity, venue, age, membership, risk category; priority, effective dates and exceptions; conflict detection and simulation.

**Fixed on main** (the package already carries these; draw what it says): setDigitalWaiverForm (saves a waiver's layout) is the write on the assignment rules screen. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Waiver type | select | — | Liability waiver · Parent guardian consent · Participation consent · Medical declaration · Safety acknowledgement · Media consent · Rental agreement · Terms acceptance · Membership declaration · Custom form | `listWaiverTemplateMaster` ?waiverType |
| Brand | picker: choose a brand | — | — | `listWaiverTemplateMaster` ?brandId |
| Is master template | toggle | — | — | `listWaiverTemplateMaster` ?isMasterTemplate |
| Q | text field | — | max length 100 | `listWaiverTemplateMaster` ?q |
| Form | picker: choose a form | — | — | `listWaiverTriggerEligibility` ?formId |
| Trigger point | select | — | During checkout · After purchase · Before ticket issuance · Before ticket download · Before event · Before check in · Before access · Before equipment collection · Before membership activation · Before activity start | `listWaiverTriggerEligibility` ?triggerPoint |
| Status | segmented control | — | Active · Inactive | `listWaiverTriggerEligibility` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Assignment rules** (data table, from `listWaiverTriggerEligibility`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | Absent on create. |
| Form | the name it points at, never the id | — |
| Name | text | — |
| Trigger point | chip: During checkout, After purchase, Before ticket issuance, Before ticket download … | — |
| Eligibility | list or chips (count when long) | All must hold (AND). Empty means every participant the association reaches. |
| Attribute | chip: Age, Is minor, Product, Event, Venue, Activity… | — |
| Operator | chip: Equals, Not equals, In, Not in, Less than, Greater than | — |
| Values | list or chips (count when long) | — |
| Completion deadline | grouped details | — |
| Kind | chip: Immediately, Before ticket release, Hours before event, Days before visit, Before … | — |
| Offset | 1,234 | Hours for `hoursBeforeEvent`, days for `daysBeforeVisit`. |
| Enforcement | list or chips (count when long) | What an incomplete waiver blocks. Empty means warn only. |
| Allow staff override | yes / no (icon or chip) | An authorised operator may admit the participant anyway; the override is recorded. |
| Reminders | list or chips (count when long) | — |
| Offset hours | 1,234 | Hours before the deadline, e.g. 168, 72, 24. |
| Channels | list or chips (count when long) | — |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Data it reads**: `listWaiverTemplateMaster` (onLoad, Templates); `listWaiverTriggerEligibility` (onLoad, The assignment rules)

**Where the user goes next**

- → `BO-844` Waiver Command Center: *Back to Waiver Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rules yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: Deep Dive and Flow Rider products -> Water activity waiver v3 required before entry; under 16 -> guardian
  signs
```

#### Permissions

- `listWaiverTemplateMaster` → `GUEST_VIEW` (read) · staff
- `listWaiverTriggerEligibility` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-846` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-846`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 12
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 4: Works in Assignment Rules → Determine which waiver or form each guest must complete. Build rules using product, attraction, event, activity, venue, age, membership, risk category and jurisdiction. Configuration Scope of Work / …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-846?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-844`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-847` Version, Expiry & Renewal

**Control legal-document lifecycle and re-sign requirements. Maintain version history, effective dates, changed clauses, approver, status and expiry period. Configure whether a change or elapsed period requires all, selected or future guests to sign again. Define renewal reminders, grace period, replacement behavior and treatment of active bookings. Preserve every signed version and prevent current templates from altering historical evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-847 |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/version-expiry-renewal-bo-847` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): BO-847 Version, Expiry & Renewal declared listWaiverTriggerEligibility while BO-848 declared listVersioningEffectiveDate; the reads were swapped, and versions …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Lifecycle of the legal document: version history, effective dates, changed clauses, approver, expiry; whether a change requires all, selected or future guests to sign again; renewal reminders and grace periods. Every signed version is preserved; a new template never alters past evidence.

**Fixed on main** (the package already carries these; draw what it says): Declares listWaiverTriggerEligibility, while BO-848 Signature Experience declares listVersioningEffectiveDate. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Form | picker: choose a form | — | — | `listVersioningEffectiveDate` ?formId |
| Compare with | number field | — | min 1 | `listVersioningEffectiveDate` ?compareWith |
| Status | radio group | — | Draft · Published · Superseded · Retired | `listVersioningEffectiveDate` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Versions** (data table, from `listVersioningEffectiveDate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Form | the name it points at, never the id | — |
| Waiver name | text | — |
| Version number | 1,234 | — |
| Status | chip: Draft, Published, Superseded, Retired | `FormDefinition.status` (states/form-definition.yaml). |
| Lifecycle status | chip: Draft, Review, Pending approval, Approved, Scheduled, Published… | — |
| Created by user | the name it points at, never the id | — |
| Change reason | text | — |
| Legal reviewer | text | `FormDefinition.legalReviewedBy`. |
| Legal reviewed at | 1 Oct 2026, 14:30 | — |
| Approved by user | the name it points at, never the id | — |
| Approved at | 1 Oct 2026, 14:30 | — |
| Effective from | 1 Oct 2026, 14:30 | — |
| Effective to | 1 Oct 2026, 14:30 | — |
| Resign rule | chip: No resign, Resign at next booking, Resign before next visit | Whether people who signed an earlier version must sign this one. |
| Suspended | yes / no (icon or chip) | — |
| Suspension reason | text | — |
| Signature count | 1,234 | Signatures taken against this exact version. |
| Comparison | grouped details | Present when `compareWith` is given. |
| Compared with version | 1,234 | — |

**Data it reads**: `listVersioningEffectiveDate` (onLoad, Version history, effective dates and expiry)

**Where the user goes next**

- → `BO-844` Waiver Command Center: *Back to Waiver Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The version expiry renewal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the version expiry renewal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No version expiry renewal yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the version expiry renewal are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
version: v4 effective 1 Nov 2026 - clause 6 medical changed - all future bookings must re-sign
```

#### Permissions

- `listVersioningEffectiveDate` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-847` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-847`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 12
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 6: Works in Version, Expiry & Renewal → Control legal-document lifecycle and re-sign requirements. Maintain version history, effective dates, changed clauses, approver, status and expiry period. Configure whether a change or elapsed period …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-847?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-844`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-848` Signature Experience Setup

**Configure secure signing across supported guest touchpoints. Support website, mobile app, kiosk, tablet, POS and dedicated waiver-station channels. Configure identity verification, signature, initials, witness, review-before-submit and completion receipt. Define accessible, multilingual flow, timeout, session recovery, device controls and offline behavior. Test the end-to-end experience and map every captured element to the evidence record. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-848 |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/signature-experience-setup-bo-848` |

**Known gaps.** **Signature Experience Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Secure signing at every touchpoint (website, app, kiosk, tablet, POS, waiver station): identity check, signature, initials, witness, review before submit, receipt; accessible and multilingual; timeout, recovery and offline behaviour. Group waivers may need a signature pad.

**Fixed on main** (the package already carries these; draw what it says): Declares listVersioningEffectiveDate (version history). (CHG-WIR-005).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which signature-capture device (USB stylus pad) is supported for group waivers?** → Drawn default accepted: Finger signature on the tablet; pad support shown as "coming". *(decided by Chinmay, 2026-10-02; DEC-281 / CHG-NOTE-002)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Form | picker: choose a form | — | — | `getSignatorySignatureGuardian` ?formId |
| Version | number field | — | min 1 | `getSignatorySignatureGuardian` ?version |

**Form: Save signing setup** (modal, opened by *Save signing setup*; *Save signing setup* calls `setSignatorySignatureGuardian`, *Cancel* sends nothing)

**Collects what `setSignatorySignatureGuardian` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Form `formId` | picker: choose a form | required | — | — | shows names, sends the id | — | `setSignatorySignatureGuardian` body |
| Form version `formVersion` | number field | required | — | min 1 | — | — | `setSignatorySignatureGuardian` body |
| Primary signatory `primarySignatory` | select | required | — | Ticket holder · Purchaser · Participant · Parent · Legal guardian · Group leader · Corporate representative · Member · Rental customer · Other authorized signatory | — | — | `setSignatorySignatureGuardian` body |
| Allowed signatories `allowedSignatories` | multi-select chips | optional | — | Ticket holder · Purchaser · Participant · Parent · Legal guardian · Group leader · Corporate representative · Member · Rental customer · Other authorized signatory | — | Who else may sign in the primary signatory's place. | `setSignatorySignatureGuardian` body |
| Co signature `coSignature` | segmented control | optional | — | Participant and guardian · Customer and authorized representative | — | Set when two people must both sign. | `setSignatorySignatureGuardian` body |
| Signature required `signatureRequired` | toggle | optional | on | — | — | — | `setSignatorySignatureGuardian` body |
| Initials required `initialsRequired` | toggle | optional | off | — | — | — | `setSignatorySignatureGuardian` body |
| Acceptance method `acceptanceMethod` | segmented control | required | — | Drawn signature · Typed name · Checkbox | — | Kept equal to `FormDefinition.signatureKind` (drawn, typed, checkbox). | `setSignatorySignatureGuardian` body |
| Capture relationship `captureRelationship` | toggle | optional | on | — | — | Whoever signs for someone else states their relationship. | `setSignatorySignatureGuardian` body |
| Identity verification `identityVerification` | radio group | optional | None | None · Signed in account · One time code · ID document check | — | — | `setSignatorySignatureGuardian` body |
| Requires guardian for minors `requiresGuardianForMinors` | toggle | required | — | — | — | Written to `FormDefinition.requiresGuardianForMinors`. | `setSignatorySignatureGuardian` body |
| Guardian threshold age `guardianThresholdAge` | stepper or slider | optional | — | min 1; max 25 | — | A participant under this age needs a guardian. Written to `FormDefinition.minimumAge`. | `setSignatorySignatureGuardian` body |
| Guardian threshold by country `guardianThresholdByCountry` | repeatable rows | optional | — | — | — | Per-country thresholds that override `guardianThresholdAge`. | `setSignatorySignatureGuardian` body |
| Country `guardianThresholdByCountry[].country` | text field | required | — | pattern `^[A-Z]{2}$` | — | — | `setSignatorySignatureGuardian` body |
| Age `guardianThresholdByCountry[].age` | stepper or slider | required | — | min 1; max 25 | — | — | `setSignatorySignatureGuardian` body |
| Guardian signs for each minor `guardianSignsForEachMinor` | toggle | optional | on | — | — | One guardian signature per minor, never one for the family. | `setSignatorySignatureGuardian` body |
| Group signing modes `groupSigningModes` | multi-select chips | optional | — | Each participant individually · Guardian for each minor · Group leader for group · Organisation representative declaration | — | The modes a group booking may use. Empty means each participant signs individually. | `setSignatorySignatureGuardian` body |

Errors to draw in the form: 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The version is no longer a draft.; 422 A signatory or group mode the version's fields cannot collect (e.g. a guardian mode with no guardian signature field).

#### Outputs: what the screen shows and produces

**Shown**

**Signatory rules** (detail panel, from `getSignatorySignatureGuardian`)

| Shows | Format | Notes |
|---|---|---|
| Form | the name it points at, never the id | — |
| Form version | 1,234 | — |
| Primary signatory | chip: Ticket holder, Purchaser, Participant, Parent, Legal guardian, Group leader… | — |
| Allowed signatories | list or chips (count when long) | Who else may sign in the primary signatory's place. |
| Co signature | chip: Participant and guardian, Customer and authorized representative | Set when two people must both sign. |
| Signature required | yes / no (icon or chip) | — |
| Initials required | yes / no (icon or chip) | — |
| Acceptance method | chip: Drawn signature, Typed name, Checkbox | Kept equal to `FormDefinition.signatureKind` (drawn, typed, checkbox). |
| Capture relationship | yes / no (icon or chip) | Whoever signs for someone else states their relationship. |
| Identity verification | chip: None, Signed in account, One time code, ID document check | — |
| Requires guardian for minors | yes / no (icon or chip) | Written to `FormDefinition.requiresGuardianForMinors`. |
| Guardian threshold age | 1,234 | A participant under this age needs a guardian. Written to `FormDefinition.minimumAge`. |
| Guardian threshold by country | list or chips (count when long) | Per-country thresholds that override `guardianThresholdAge`. |
| Country | text | — |
| Age | 1,234 | — |
| Guardian signs for each minor | yes / no (icon or chip) | One guardian signature per minor, never one for the family. |
| Group signing modes | list or chips (count when long) | The modes a group booking may use. Empty means each participant signs individually. |
| Recorded evidence | list or chips (count when long) | Always all of them; listed so the reviewer sees what is kept. |
| Legal approved by | text | `FormDefinition.legalReviewedBy`, set at the legal/compliance step of `approveWaiverTesting`. |
| Legal approved at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save signing setup (secondary button) | `setSignatorySignatureGuardian` PUT `/signatory-signature-guardian` | SignatorySignatureGuardianRuleConfigurationInput | SignatorySignatureGuardianRuleConfigurationView | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The version is no longer a draft. | opens modal first |

**Data it reads**: `getSignatorySignatureGuardian` (onLoad, Who must sign a waiver version)

**Where the user goes next**

- → `BO-844` Waiver Command Center: *Back to Waiver Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The signature experience list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the signature experience untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No signature experience yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the signature experience are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The version is no longer a draft.; 422 A signatory or group mode the version's fields cannot collect (e.g. a guardian mode with no guardian signature field). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
setup: Waiver station at Deep Dive desk - tablet - signature + initials on clause 4 - receipt by email
```

#### Permissions

- `getSignatorySignatureGuardian` → `GUEST_VIEW` (read) · staff
- `setSignatorySignatureGuardian` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Group waivers need a digital signature-capture device (stylus pad); Chinmay says a USB signature pad should integrate. Hardware reference pending from Qossai. *(open · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-756)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-848` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-848`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 12
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 8: Works in Signature Experience Setup → Configure secure signing across supported guest touchpoints. Support website, mobile app, kiosk, tablet, POS and dedicated waiver-station channels. Configure identity verification, signature …

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-848?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save signing setup.
- [ ] Every transition is wired: `BO-844`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-849` Guardian & Group Signing

**Manage authority and multi-participant signing for minors and groups. Use Customer Master family/guardian relationships and record the authority basis for each dependant. Support one authorized signer for multiple family members, students or group participants where permitted. Configure minimum self-sign age, one/both guardian requirement, partial group signing and exceptions. Show roster status and require individual signatures for documents or participants that cannot be delegated. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-849 |
| Who uses it | venue staff holding `GUEST_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/guardian-group-signing-bo-849` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Authority and multi-participant signing for minors and groups: guardian relationships from the guest master, one signer for several family members or students where permitted, minimum self-sign age, one or both guardians, partial group signing. A missing date of birth counts as a minor.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Signatory**: Participant or parent/guardian; minimum self-sign age; individual signatures where the document requires them. *(source: contracts/satellite/marketing-crm.yaml#setSignatorySignatureGuardian; DI-572; R205)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-844` Waiver Command Center: *Back to Waiver Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guardian group signing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guardian group signing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guardian group signing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guardian group signing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The version is no longer a draft.; 422 A signatory or group mode the version's fields cannot collect (e.g. a guardian mode with no guardian signature field). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: Under 16 - one guardian signs for up to 5 linked children; school groups - teacher signs with parental consent
  on file
```

#### Permissions

- `setSignatorySignatureGuardian` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Conditional fields: e.g. ask for the Emirates city only if country is UAE; ask extra questions only if age is below a threshold. Signatory config sets who signs (participant or parent/guardian). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-572)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-849` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-849`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 12
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 10: Works in Guardian & Group Signing → Manage authority and multi-participant signing for minors and groups. Use Customer Master family/guardian relationships and record the authority basis for each dependant. Support one authorized …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-849?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-844`.
- [ ] Every gated control is gated: `GUEST_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-850` Pre-Arrival Completion

**Collect required waivers before the guest reaches the venue. Link the request to booking, ticket, event, activity, participants and scheduled arrival. Configuration Scope of Work / Version 1.0 59 Send secure email, SMS or WhatsApp link/QR in the guest's language with a completion deadline. Configure reminder schedule, resend, authentication, expiry and status synchronization. Show completed, pending and not-started participants and stop reminders immediately after valid completion. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-850 |
| Who uses it | venue staff holding `GUEST_VIEW_PII` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/pre-arrival-completion-bo-850` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Get waivers signed before arrival: a secure link or QR by email, SMS or WhatsApp in the guest's language, a deadline, reminders, and status per participant. Reminders stop when everyone has signed. These are transactional messages, not marketing.

**Fixed on main** (the package already carries these; draw what it says): Declares only listMinorGuardianGroup. (CHG-WIR-005).

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
| Q | text field | — | max length 200 | `listParticipantWaiverStatus` ?q |
| Participant subject | picker: choose a participant subject | — | — | `listParticipantWaiverStatus` ?participantSubjectId |
| Order | picker: choose an order | — | — | `listParticipantWaiverStatus` ?orderId |
| Ticket | picker: choose a ticket | — | — | `listParticipantWaiverStatus` ?ticketId |
| Group booking | picker: choose a group booking | — | — | `listParticipantWaiverStatus` ?groupBookingId |
| Form | picker: choose a form | — | — | `listParticipantWaiverStatus` ?formId |
| Performance | picker: choose a performance | — | — | `listParticipantWaiverStatus` ?performanceId |
| Visit from | date and time picker | — | — | `listParticipantWaiverStatus` ?visitFrom |
| Visit to | date and time picker | — | — | `listParticipantWaiverStatus` ?visitTo |
| … 1 more | | | | `operations.json` |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Participants to chase** (data table, from `listParticipantWaiverStatus`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Participant | the name it points at, never the id | The participant's subject id. |
| Participant | text | The participant's name. |
| Customer purchaser | grouped details | Who bought the booking; may differ from the participant. |
| Subject | the name it points at, never the id | — |
| Name | text | — |
| Booking | the name it points at, never the id | The order id. |
| Ticket | the name it points at, never the id | The ticket (entitlement) id. |
| Product | grouped details | — |
| Product | the name it points at, never the id | — |
| Name | text | — |
| Event | grouped details | — |
| Event | the name it points at, never the id | — |
| Performance | the name it points at, never the id | — |
| Name | text | — |
| Visit date | 1 Oct 2026, 14:30 | — |
| Age category | chip: Adult, Minor | From the participant's date of birth against the age of majority configured for the venue's jurisdiction (no shipped default). |
| Group | grouped details | — |
| Group booking | the name it points at, never the id | — |
| Name | text | — |

**Data it reads**: `listMinorGuardianGroup` (onLoad, Guardian and group signing); `listParticipantWaiverStatus` (onLoad, Which participants still have to sign before arrival)

**Where the user goes next**

- → `BO-844` Waiver Command Center: *Back to Waiver Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pre-arrival completion list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pre-arrival completion untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pre-arrival completion yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pre-arrival completion are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
booking: ORD-55821 - Deep Dive Sat 3 Oct 14:00 - 3 participants - 1 signed, 2 pending - reminder sent 1 Oct
```

#### Permissions

- `listMinorGuardianGroup` → `GUEST_VIEW_PII` (operate) · staff
- `listParticipantWaiverStatus` → `GUEST_VIEW_PII` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-850` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-850`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 12
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 12: Works in Pre-Arrival Completion → Collect required waivers before the guest reaches the venue. Link the request to booking, ticket, event, activity, participants and scheduled arrival. Configuration Scope of Work / Version 1.0 59 …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-850?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-844`.
- [ ] Every gated control is gated: `GUEST_VIEW_PII`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-851` Verification & Access Control

**Enforce waiver requirements during check-in and access validation. Return real-time valid, missing, expired or wrong-version status during ticket scan or check-in. Show required documents and participant while minimizing sensitive content at the gate. Configure admit/block outcomes, supervisor override, reason, approval and offline cache/freshness. Record scan, decision, waiver evidence reference, device, operator, override and final access outcome. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-851 |
| Who uses it | venue staff holding `GUEST_VIEW_PII` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/verification-access-control-bo-851` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Waiver checks at check-in and scan: valid, missing, expired or wrong version, in real time, with minimal sensitive content at the gate; admit or block, supervisor override with reason; offline cache freshness. An incomplete waiver can block download, activation, check-in or access.

#### Inputs: what the user enters or picks

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Gate result**: Participant name, which waiver is missing, and Sign now (QR) or Override; never the waiver content. *(source: DI-574; contracts/satellite/marketing-crm.yaml#getWaiverStatus)*

**Data it reads**: `listParticipantWaiverStatus` (onLoad, Pre-arrival completion)

**Where the user goes next**

- → `BO-844` Waiver Command Center: *Back to Waiver Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The verification access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the verification access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No verification access yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the verification access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
result: Layla Haddad - Water activity waiver v3 missing - guardian must sign - BLOCKED
```

#### Permissions

- `listParticipantWaiverStatus` → `GUEST_VIEW_PII` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Qossai: where a waiver is required before entry, an incomplete waiver can block ticket download, activation, check-in or access; ticket and scan screens need a waiver-incomplete state. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-574)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-851` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-851`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 12
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 14: Works in Verification & Access Control → Enforce waiver requirements during check-in and access validation. Return real-time valid, missing, expired or wrong-version status during ticket scan or check-in. Show required documents and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-851?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-844`.
- [ ] Every gated control is gated: `GUEST_VIEW_PII`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-852` Documents, Search & Retention

**Securely store and retrieve signed waiver evidence. Search by guest, guardian, participant, booking, ticket, activity, event, date, version and status. Store signed PDF/evidence package, metadata, relationships, status and authorized view/download actions. Apply encryption, RBAC/PBAC, retention, legal hold, archive and deletion/anonymization policies. Track every access, download, policy action and downstream reference and prevent silent alteration. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-852 |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW`, `GUEST_VIEW_PII` (1 configure, 1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/engagement-support/documents-search-retention-bo-852` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Signed waiver evidence stored and retrieved securely: search by guest, guardian, participant, booking, activity, date, version; signed PDF and metadata; retention, legal hold, deletion; every access logged.

**Fixed on main** (the package already carries these; draw what it says): Declares setWaiverVerificationValidation (a reviewer's decision) and getWaiverStatus, but no evidence search. (CHG-WIR-005).

#### Inputs: what the user enters or picks

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Signed waivers** (data table, from `listComplianceEvidenceWaiver`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Submission | the name it points at, never the id | — |
| Signature | the name it points at, never the id | The `MarketingWaiverSignature` row. |
| Waiver | the name it points at, never the id | The waiver form (`FormDefinition.id`). |
| Waiver name | text | — |
| Exact version | 1,234 | The form version presented and signed; `getForm` with this `version` returns its wording and questions. |
| Participant | grouped details | — |
| Subject | the name it points at, never the id | — |
| Name | text | — |
| Date of birth | 1 Oct 2026 | — |
| Signatory | grouped details | — |
| Subject | the name it points at, never the id | — |
| Name | text | — |
| Signed name | text | The name as typed or drawn at signing. |
| Signatory type | chip: Participant, Guardian, Organisation representative | — |
| Guardian relationship | the name it points at, never the id | The `GuestRelationship` relied on when a guardian or representative signed. |
| Submitted at | 1 Oct 2026, 14:30 | Device time of signing. |
| Synced at | 1 Oct 2026, 14:30 | Server time the submission arrived. |
| Channel | text | `FormSubmission.capturedAtChannel`. |
| Collection method | chip: Email, SMS, Whatsapp, Guest web, Guest app, Group portal… | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Evidence record**: Opens the exact version signed; access requires PII permission and is logged. *(source: contracts/satellite/marketing-crm.yaml#createForm)*

**Data it reads**: `listComplianceEvidenceWaiver` (onLoad, Signed waiver evidence)

**Where the user goes next**

- → `BO-844` Waiver Command Center: *Back to Waiver Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The documents search retention list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the documents search retention untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No documents search retention yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the documents search retention are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.; 422 `verified` while an automatic check fails or no signature is present (`checksFailing`), or a required `note` or `escalatedTo` is missing (`reasonRequired`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
record: Fatima Al Mansoori - Water activity waiver v3 - signed 26 Sep 2026 10:12 - retain until 26 Sep 2033
```

#### Permissions

- `setWaiverVerificationValidation` → `GUEST_MANAGE` (configure) · staff
- `getWaiverStatus` → `GUEST_VIEW` (read) · staff, guest, device
- `listComplianceEvidenceWaiver` → `GUEST_VIEW_PII` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-852` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-852`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 12
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 16: Works in Documents, Search & Retention → Securely store and retrieve signed waiver evidence. Search by guest, guardian, participant, booking, ticket, activity, event, date, version and status. Store signed PDF/evidence package, metadata …
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-852?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-844`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`, `GUEST_VIEW_PII`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-853` Legal Evidence & Audit

**Provide a defensible record of signing and subsequent operational use. Record signer and participant identity, authority, timestamp, timezone, IP/device, channel and verification method. Store consent/template version, content hash, signature/initials, witness, attachments and completion receipt. Include access-control decisions, overrides, renewals, revocations and related communications in the timeline. Export a controlled evidence bundle with integrity validation and full audit history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 60**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-853 |
| Who uses it | venue staff holding `GUEST_VIEW_PII` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/legal-evidence-audit-bo-853` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** A defensible record of signing and later use: signer and participant identity, authority, time and time zone, IP or device, channel, verification method, template version and content hash, signature, witness, receipt; access decisions, overrides, renewals and revocations; controlled evidence export.

#### Inputs: what the user enters or picks

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listComplianceEvidenceWaiver` (onLoad, Documents, search and retention)

**Where the user goes next**

- → `BO-844` Waiver Command Center: *Back to Waiver Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The legal evidence audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the legal evidence audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No legal evidence audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the legal evidence audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `CMS-058`: Same evidence repository.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
evidence: v3 hash 9f2c...e1 - signed by guardian Khalid Al Suwaidi for Mariam (9) - kiosk 4 - 26 Sep 2026 10:12
  GST
```

#### Permissions

- `listComplianceEvidenceWaiver` → `GUEST_VIEW_PII` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-853` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS81 Marketing CRM Configuration Reference v1.0 Board 12.dc.html#bo-853`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 12
- Flow F255 *Marketing CRM Configuration Reference v1.0 board 12: Waiver Command Center*, step 18: Works in Legal Evidence & Audit → Provide a defensible record of signing and subsequent operational use. Record signer and participant identity, authority, timestamp, timezone, IP/device, channel and verification method. Store …
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-853?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-844`.
- [ ] Every gated control is gated: `GUEST_VIEW_PII`.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getSignatorySignatureGuardian": {"method":"GET","path":"/signatory-signature-guardian","contract":"marketing-crm","summary":"Load the signatory rules of a waiver version","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"formId","in":"query","required":true},{"name":"version","in":"query","required":false}],"requestBody":null,"responds":"SignatorySignatureGuardianRuleConfigurationView"},
"getWaiverStatus": {"method":"GET","path":"/guests/{subjectId}/waiver-status","contract":"marketing-crm","summary":"Whether this guest may be issued a ticket that requires a waiver","permission":"GUEST_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":null}],"requestBody":null,"responds":null},
"listComplianceEvidenceWaiver": {"method":"GET","path":"/compliance-evidence-waiver","contract":"marketing-crm","summary":"Compliance Evidence, Audit & Waiver Repository","permission":"GUEST_VIEW_PII","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"participantSubjectId","in":"query","required":false},{"name":"customerSubjectId","in":"query","required":false},{"name":"signatorySubjectId","in":"query","required":false},{"name":"ticketId","in":"query","required":false},{"name":"orderId","in":"query","required":false},{"name":"eventId","in":"query","required":false},{"name":"formId","in":"query","required":false},{"name":"formVersion","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMinorGuardianGroup": {"method":"GET","path":"/minor-guardian-group","contract":"marketing-crm","summary":"Minor, Guardian & Group Consent Management","permission":"GUEST_VIEW_PII","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"groupBookingId","in":"query","required":false},{"name":"guardianSubjectId","in":"query","required":false},{"name":"orderId","in":"query","required":false},{"name":"performanceId","in":"query","required":false},{"name":"consentStatus","in":"query","required":false},{"name":"visitFrom","in":"query","required":false},{"name":"visitTo","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listParticipantWaiverStatus": {"method":"GET","path":"/participant-waiver-statu","contract":"marketing-crm","summary":"Participant Waiver Status & Tracking","permission":"GUEST_VIEW_PII","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"q","in":"query","required":false},{"name":"participantSubjectId","in":"query","required":false},{"name":"orderId","in":"query","required":false},{"name":"ticketId","in":"query","required":false},{"name":"groupBookingId","in":"query","required":false},{"name":"formId","in":"query","required":false},{"name":"performanceId","in":"query","required":false},{"name":"visitFrom","in":"query","required":false},{"name":"visitTo","in":"query","required":false},{"name":"completionStatus","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVersioningEffectiveDate": {"method":"GET","path":"/versioning-effective-date","contract":"marketing-crm","summary":"Versioning, Effective Dates & Legal Change Control","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"formId","in":"query","required":false},{"name":"compareWith","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWaiver": {"method":"GET","path":"/waiver","contract":"marketing-crm","summary":"Waiver Operations Command Center","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"brandId","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"eventId","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"formId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"participantType","in":"query","required":false},{"name":"bookingChannel","in":"query","required":false},{"name":"breakdownBy","in":"query","required":false}],"requestBody":null,"responds":"WaiverOperationsCommandCenterView"},
"listWaiverTemplateMaster": {"method":"GET","path":"/waiver-template-master","contract":"marketing-crm","summary":"Waiver Template Library & Master Setup","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"waiverType","in":"query","required":false},{"name":"brandId","in":"query","required":false},{"name":"isMasterTemplate","in":"query","required":false},{"name":"q","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWaiverTriggerEligibility": {"method":"GET","path":"/waiver-trigger-eligibility","contract":"marketing-crm","summary":"Waiver Trigger, Eligibility & Completion Rules","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"formId","in":"query","required":false},{"name":"triggerPoint","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setDigitalWaiverForm": {"method":"PUT","path":"/digital-waiver-form","contract":"marketing-crm","summary":"Save the layout of a draft waiver version","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DigitalWaiverFormBuilderInput","responds":"DigitalWaiverFormBuilderView"},
"setSignatorySignatureGuardian": {"method":"PUT","path":"/signatory-signature-guardian","contract":"marketing-crm","summary":"Set who must sign a draft waiver version, and how","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SignatorySignatureGuardianRuleConfigurationInput","responds":"SignatorySignatureGuardianRuleConfigurationView"},
"setWaiverVerificationValidation": {"method":"PUT","path":"/waiver-verification-validation","contract":"marketing-crm","summary":"Record a reviewer's verification decision on a waiver submission","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WaiverVerificationValidationWorkspaceInput","responds":"WaiverVerificationValidationWorkspaceView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ComplianceEvidenceAuditWaiverRepositoryView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.form_submission, marketing.waiver_signature, marketing.form_definition + marketing.form_definition_field, marketing.guest_document, marketing.waiver_verification (new), marketing.waiver_requirement (new) and marketing.waiver_requirement_event (new); names from pii.subject","description":"One signed waiver as evidence. Nothing here changes after signing except the verification and the audit events appended to it.","required":["submissionId","waiverId","exactVersion","participant","signatory","submittedAt","documentHash","auditEvents"],"properties":{"submissionId":{"type":"string","format":"uuid"},"signatureId":{"type":"string","format":"uuid","nullable":true,"description":"The `MarketingWaiverSignature` row."},"waiverId":{"type":"string","format":"uuid","description":"The waiver form (`FormDefinition.id`)."},"waiverName":{"type":"string"},"exactVersion":{"type":"integer","minimum":1,"description":"The form version presented and signed; `getForm` with this `version` returns its wording and questions."},"participant":{"type":"object","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"dateOfBirth":{"type":"string","format":"date","nullable":true}}},"signatory":{"type":"object","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"signedName":{"type":"string","description":"The name as typed or drawn at signing."}}},"signatoryType":{"type":"string","enum":["participant","guardian","organisationRepresentative"]},"guardianRelationshipId":{"type":"string","format":"uuid","nullable":true,"description":"The `GuestRelationship` relied on when a guardian or representative signed."},"submittedAt":{"type":"string","format":"date-time","description":"Device time of signing."},"syncedAt":{"type":"string","format":"date-time","description":"Server time the submission arrived."},"channel":{"type":"string","description":"`FormSubmission.capturedAtChannel`."},"collectionMethod":{"type":"string","nullable":true,"enum":["email","sms","whatsapp","guestWeb","guestApp","groupPortal","qrCode","pos","kiosk","staffAssistedDevice"]},"assistedByStaffId":{"type":"string","format":"uuid","nullable":true,"description":"The staff member who helped on a staff-assisted device; never the signer."},"responses":{"type":"object","description":"`FormSubmission.answers`, keyed by field key.","additionalProperties":true},"acknowledgements":{"type":"array","items":{"type":"object","required":["key","accepted"],"properties":{"key":{"type":"string"},"label":{"type":"string","description":"The wording as presented in `exactVersion`."},"accepted":{"type":"boolean"}}}},"signatureEvidence":{"type":"object","properties":{"signatureKind":{"type":"string","enum":["drawn","typed","checkbox"]},"signatureAssetId":{"type":"string","format":"uuid","nullable":true},"signedDocumentId":{"type":"string","format":"uuid","nullable":true,"description":"The rendered document as signed (`GuestDocument`, kind `signedWaiver`)."}}},"documentHash":{"type":"string","maxLength":128,"description":"Hash of the rendered document as signed."},"deviceEvidence":{"type":"object","nullable":true,"description":"Personal data (ADR-0023); null once the subject is erased.","properties":{"ipAddress":{"type":"string","nullable":true},"deviceInfo":{"type":"string","nullable":true}}},"verification":{"type":"object","nullable":true,"properties":{"result":{"type":"string","enum":["automaticallyValidated","pendingManualVerification","verified","correctionRequired","rejected","escalated"]},"reviewedBy":{"type":"string","format":"uuid","nullable":true},"reviewedAt":{"type":"string","format":"date-time","nullable":true}}},"relatedBooking":{"type":"string","format":"uuid","nullable":true},"relatedTicket":{"type":"string","format":"uuid","nullable":true},"applicableProductId":{"type":"string","format":"uuid","nullable":true},"applicablePerformanceId":{"type":"string","format":"uuid","nullable":true},"retainUntil":{"type":"string","format":"date-time","nullable":true,"description":"From the retention policy in force."},"auditEvents":{"type":"array","description":"The requirement's timeline, oldest first (link issued, opened, completed, signed, validated, verified and every staff action).","items":{"type":"object","required":["at","event","actor"],"properties":{"at":{"type":"string","format":"date-time"},"event":{"type":"string","enum":["linkIssued","linkOpened","participantIdentified","guardianInformationCompleted","questionsCompleted","acknowledgementsAccepted","signatureSubmitted","validationPassed","validationFailed","markedComplete","verified","rejected","correctionRequested","signatoryReplaced","exceptionApproved","evidenceViewed"]},"actor":{"type":"string","enum":["participant","guardian","staff","system"]},"staffId":{"type":"string","format":"uuid","nullable":true}}}}}},
"DigitalWaiverFormBuilderInput": {"description":"The request body of `setDigitalWaiverForm`, the layout record itself; read-only properties are ignored.","allOf":[{"$ref":"#/components/schemas/DigitalWaiverFormBuilderView"}]},
"DigitalWaiverFormBuilderView": {"type":"object","x-ticvai-persistence":"marketing.waiver_form_layout","description":"The layout of one waiver version (pack 11.1.3), keyed on `formId` + `formVersion`. Immutable once the version is published, like the version itself.","required":["formId","formVersion","sections"],"properties":{"formId":{"type":"string","format":"uuid"},"formVersion":{"type":"integer","minimum":1},"sections":{"type":"array","minItems":1,"items":{"type":"object","required":["sectionKey","kind","blocks"],"properties":{"sectionKey":{"type":"string","maxLength":60},"kind":{"type":"string","enum":["header","participantInformation","waiverTerms","safetyAcknowledgements","questions","consent","signature","custom"]},"title":{"$ref":"#/components/schemas/LocalisedText"},"numbered":{"type":"boolean","default":false},"mandatoryReading":{"type":"boolean","default":false,"description":"The signatory must tick \"I have read and understood this section\" before continuing."},"acknowledgementText":{"$ref":"#/components/schemas/LocalisedText"},"showWhen":{"type":"object","nullable":true,"description":"Shown only when the condition holds, e.g. `isMinor` equals `true` shows the guardian section.","required":["subject","operator"],"properties":{"subject":{"type":"string","maxLength":60,"description":"A field key of this version, or `isMinor` (resolved from the waiver's guardian threshold)."},"operator":{"type":"string","enum":["equals","notEquals","in","lessThan","greaterThan","isAnswered"]},"value":{"type":"string","maxLength":200,"nullable":true}}},"blocks":{"type":"array","items":{"type":"object","required":["blockKey","kind"],"properties":{"blockKey":{"type":"string","maxLength":60},"kind":{"type":"string","enum":["heading","paragraph","legalText","instructions","imageLogo","divider","informationBox","checkbox","acknowledgement","question","signature","initials","date","customerDetails","guardianDetails"]},"content":{"$ref":"#/components/schemas/LocalisedText"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"The image for an `imageLogo` block."},"fieldKey":{"type":"string","maxLength":60,"nullable":true,"description":"The `FormField.key` an input block collects; required for input kinds."},"mandatoryNotice":{"type":"boolean","default":false,"description":"Rendered as a notice that cannot be collapsed."}}}}}}},"status":{"type":"string","readOnly":true,"enum":["draft","published","superseded","retired"],"description":"`FormDefinition.status` of this version."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MinorGuardianGroupConsentManagementView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.guest_relationship, marketing.waiver_requirement (new), marketing.form_submission, orders.group_booking and orders.order_line; names and contacts from pii.subject and pii.subject_contact","description":"One minor participant on one booking, their guardians and their group.","required":["minor","booking","guardians","consentStatus"],"properties":{"minor":{"type":"object","required":["subjectId","name"],"properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"age":{"type":"integer","minimum":0,"nullable":true}}},"booking":{"type":"string","format":"uuid","description":"The order id."},"visitDate":{"type":"string","format":"date-time","nullable":true},"guardians":{"type":"array","description":"Everyone holding a parent or guardian relationship to the minor; empty when none is recorded.","items":{"type":"object","required":["subjectId","name","relationship","verificationStatus","signatureStatus"],"properties":{"relationshipId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"relationship":{"type":"string","enum":["parent","guardian"]},"contact":{"type":"string","nullable":true,"description":"The address the guardian link goes to (email or mobile)."},"mayWaive":{"type":"boolean","description":"The relationship carries the `signWaiver` authority and is in effect."},"verificationStatus":{"type":"string","enum":["verified","unverified"],"description":"`verified` when `GuestRelationship.verifiedAt` is set."},"signatureStatus":{"type":"string","enum":["notRequested","sent","opened","signed","rejected","expired"]}}}},"consentStatus":{"type":"string","enum":["complete","pending","rejected"],"description":"`complete` when every mandatory guardian consent for the minor on this booking is signed by an authorised signatory."},"group":{"type":"object","nullable":true,"description":"The group booking the minor is part of, and its leader.","properties":{"groupBookingId":{"type":"string","format":"uuid"},"organization":{"type":"string","nullable":true,"description":"The school, club or company."},"groupLeader":{"type":"object","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"contact":{"type":"string","nullable":true,"description":"The leader's email or mobile."},"groupBooking":{"type":"string","format":"uuid","description":"The group's order id."},"responsibility":{"type":"string","enum":["coordinatorOnly","supervisingAdult","organisationRepresentative"],"description":"`organisationRepresentative` when the leader's `GuestRelationship` (kind `groupLeader`) carries `signWaiver`; `supervisingAdult` when the leader is a participant on the booking; otherwise `coordinatorOnly`."},"permittedActions":{"type":"array","description":"What the leader may do for this group under the form's signatory rule.","items":{"type":"string","enum":["viewStatus","sendLinks","receiveNotifications","signOnBehalf"]}}}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ParticipantWaiverStatusTrackingView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.waiver_requirement (new), marketing.form_definition, marketing.form_submission, marketing.waiver_verification (new), marketing.waiver_exception (new), orders.order_line, orders.group_booking and catalogue.performance; names from pii.subject","description":"One participant on one booking and the waivers that participant needs. Purchaser, participant and each waiver's signatory are separate people.","required":["participantId","participant","booking","waiverRequirements","completionStatus"],"properties":{"participantId":{"type":"string","format":"uuid","description":"The participant's subject id."},"participant":{"type":"string","description":"The participant's name."},"customerPurchaser":{"type":"object","nullable":true,"description":"Who bought the booking; may differ from the participant.","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"booking":{"type":"string","format":"uuid","description":"The order id."},"ticket":{"type":"string","format":"uuid","nullable":true,"description":"The ticket (entitlement) id."},"product":{"type":"object","properties":{"productId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"event":{"type":"object","nullable":true,"properties":{"eventId":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"visitDate":{"type":"string","format":"date-time","nullable":true},"ageCategory":{"type":"string","enum":["adult","minor"],"description":"From the participant's date of birth against the age of majority configured for the venue's jurisdiction (no shipped default). A participant whose age cannot be established is treated as a minor."},"group":{"type":"object","nullable":true,"properties":{"groupBookingId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"waiverRequirements":{"type":"array","description":"Each waiver this participant needs on this booking.","items":{"type":"object","required":["requirementId","formId","formName","mandatory","status"],"properties":{"requirementId":{"type":"string","format":"uuid"},"formId":{"type":"string","format":"uuid"},"formName":{"type":"string"},"formVersion":{"type":"integer","minimum":1,"nullable":true,"description":"The version assigned, or signed once completed."},"mandatory":{"type":"boolean","description":"False for an optional consent (e.g. media), which never blocks readiness."},"status":{"type":"string","enum":["notAssigned","assigned","sent","opened","inProgress","completed","verified","rejected","expired","superseded"]},"declined":{"type":"boolean","default":false,"description":"An optional consent answered no."},"signatory":{"type":"object","nullable":true,"properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"signatoryType":{"type":"string","enum":["participant","guardian","organisationRepresentative"]}}},"deliveryChannel":{"type":"string","nullable":true,"enum":["email","sms","whatsapp","push","inApp","qrCode","pos","kiosk","staffAssistedDevice","groupPortal"]},"lastSentAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true},"submissionId":{"type":"string","format":"uuid","nullable":true},"blocks":{"type":"array","description":"What an incomplete requirement blocks, from the trigger configuration.","items":{"type":"string","enum":["ticketDownload","activation","checkIn","access"]}}}}},"completionStatus":{"type":"string","enum":["ready","notReady","exceptionApproved"],"description":"`ready` when every mandatory requirement is completed or verified; `exceptionApproved` when the gap is covered by an approved exception."}}},
"SignatorySignatureGuardianRuleConfigurationInput": {"description":"The request body of `setSignatorySignatureGuardian`, the rule record itself; read-only properties are ignored.","allOf":[{"$ref":"#/components/schemas/SignatorySignatureGuardianRuleConfigurationView"}]},
"SignatorySignatureGuardianRuleConfigurationView": {"type":"object","x-ticvai-persistence":"marketing.waiver_signatory_rule","description":"The signatory rules of one waiver version (pack 11.1.5), keyed on `formId` + `formVersion`; immutable once the version is published.","required":["formId","formVersion","primarySignatory","acceptanceMethod","requiresGuardianForMinors"],"properties":{"formId":{"type":"string","format":"uuid"},"formVersion":{"type":"integer","minimum":1},"primarySignatory":{"type":"string","enum":["ticketHolder","purchaser","participant","parent","legalGuardian","groupLeader","corporateRepresentative","member","rentalCustomer","otherAuthorizedSignatory"]},"allowedSignatories":{"type":"array","items":{"type":"string","enum":["ticketHolder","purchaser","participant","parent","legalGuardian","groupLeader","corporateRepresentative","member","rentalCustomer","otherAuthorizedSignatory"]},"description":"Who else may sign in the primary signatory's place."},"coSignature":{"type":"string","nullable":true,"enum":["participantAndGuardian","customerAndAuthorizedRepresentative"],"description":"Set when two people must both sign."},"signatureRequired":{"type":"boolean","default":true},"initialsRequired":{"type":"boolean","default":false},"acceptanceMethod":{"type":"string","enum":["drawnSignature","typedName","checkbox"],"description":"Kept equal to `FormDefinition.signatureKind` (drawn, typed, checkbox)."},"captureRelationship":{"type":"boolean","default":true,"description":"Whoever signs for someone else states their relationship."},"identityVerification":{"type":"string","enum":["none","signedInAccount","oneTimeCode","idDocumentCheck"],"default":"none"},"requiresGuardianForMinors":{"type":"boolean","description":"Written to `FormDefinition.requiresGuardianForMinors`."},"guardianThresholdAge":{"type":"integer","minimum":1,"maximum":25,"nullable":true,"description":"A participant under this age needs a guardian. Written to `FormDefinition.minimumAge`. No default."},"guardianThresholdByCountry":{"type":"array","items":{"type":"object","required":["country","age"],"properties":{"country":{"type":"string","pattern":"^[A-Z]{2}$"},"age":{"type":"integer","minimum":1,"maximum":25}}},"description":"Per-country thresholds that override `guardianThresholdAge`."},"guardianSignsForEachMinor":{"type":"boolean","default":true,"description":"One guardian signature per minor, never one for the family."},"groupSigningModes":{"type":"array","items":{"type":"string","enum":["eachParticipantIndividually","guardianForEachMinor","groupLeaderForGroup","organisationRepresentativeDeclaration"]},"description":"The modes a group booking may use. Empty means each participant signs individually."},"recordedEvidence":{"type":"array","readOnly":true,"items":{"type":"string","enum":["timestamp","waiverVersion","signatory","authenticationMethod","transactionReference","customerReference","documentHash","deviceInfo","consentEvidence"]},"description":"Always all of them; listed so the reviewer sees what is kept."},"legalApprovedBy":{"type":"string","nullable":true,"readOnly":true,"description":"`FormDefinition.legalReviewedBy`, set at the legal/compliance step of `approveWaiverTesting`."},"legalApprovedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"VersioningEffectiveDatesLegalChangeControlView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.form_definition, marketing.waiver_version_control (new), marketing.form_submission and marketing.waiver_signature","description":"One version of one waiver and its change control (pack 11.1.8).","required":["formId","versionNumber","status","createdAt"],"properties":{"formId":{"type":"string","format":"uuid"},"waiverName":{"type":"string"},"versionNumber":{"type":"integer","minimum":1},"status":{"type":"string","enum":["draft","published","superseded","retired"],"description":"`FormDefinition.status` (states/form-definition.yaml)."},"lifecycleStatus":{"type":"string","enum":["draft","review","pendingApproval","approved","scheduled","published","suspended","expired","archived"]},"createdByUserId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"changeReason":{"type":"string","maxLength":1000,"nullable":true},"legalReviewer":{"type":"string","nullable":true,"description":"`FormDefinition.legalReviewedBy`."},"legalReviewedAt":{"type":"string","format":"date-time","nullable":true},"approvedByUserId":{"type":"string","format":"uuid","nullable":true},"approvedAt":{"type":"string","format":"date-time","nullable":true},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"resignRule":{"type":"string","enum":["noResign","resignAtNextBooking","resignBeforeNextVisit"],"description":"Whether people who signed an earlier version must sign this one."},"suspended":{"type":"boolean","default":false},"suspensionReason":{"type":"string","maxLength":500,"nullable":true},"signatureCount":{"type":"integer","minimum":0,"description":"Signatures taken against this exact version."},"comparison":{"type":"object","nullable":true,"description":"Present when `compareWith` is given.","properties":{"comparedWithVersion":{"type":"integer","minimum":1},"addedText":{"type":"array","items":{"type":"object","properties":{"blockKey":{"type":"string"},"language":{"type":"string"},"text":{"type":"string"}}}},"removedText":{"type":"array","items":{"type":"object","properties":{"blockKey":{"type":"string"},"language":{"type":"string"},"text":{"type":"string"}}}},"changedQuestions":{"type":"array","items":{"type":"string"},"description":"Field keys added, removed or changed."},"changedSignatoryRules":{"type":"array","items":{"type":"string"},"description":"Names of the signatory-rule properties that differ."},"changedAssociations":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Associations added, removed or changed between the two versions' publication."}}}}},
"WaiverOperationsCommandCenterView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.waiver_requirement (new), marketing.form_definition, marketing.form_submission, marketing.waiver_signature, marketing.waiver_verification (new), marketing.waiver_exception (new), orders.order_line, orders.group_booking and catalogue.performance","description":"Waiver readiness for the filters given. Counts are of participant waiver requirements for activities in the window unless the name says otherwise.","required":["waiversRequired","completed","pending","completionRate","byPeriod","breakdown","upcomingActivities"],"properties":{"waiversRequired":{"type":"integer","minimum":0,"description":"Requirements assigned, excluding `superseded`."},"completed":{"type":"integer","minimum":0,"description":"Requirements `completed` or `verified`."},"pending":{"type":"integer","minimum":0,"description":"Requirements `assigned`, `sent` or `opened`, not yet started."},"partiallyCompleted":{"type":"integer","minimum":0,"description":"Requirements `inProgress`, and participants with some but not all waivers complete."},"expiring":{"type":"integer","minimum":0,"description":"Completed requirements whose acceptance (`FormSubmission.expiresAt`) ends before the activity starts."},"invalid":{"type":"integer","minimum":0,"description":"Requirements `expired`, or completed against a superseded version."},"rejected":{"type":"integer","minimum":0},"guardianConsentPending":{"type":"integer","minimum":0,"description":"Minor participants whose guardian has not yet signed."},"upcomingParticipantsMissingWaiver":{"type":"integer","minimum":0,"description":"Participants with at least one mandatory requirement not complete."},"accessBlocked":{"type":"integer","minimum":0,"description":"Participants whose ticket download, activation, check-in or access is currently blocked by a waiver."},"manualExceptions":{"type":"integer","minimum":0,"description":"Approved exceptions (`setWaiverException`) in force."},"completionRate":{"type":"number","minimum":0,"maximum":1,"description":"`completed` / `waiversRequired`."},"byPeriod":{"type":"array","description":"Today, tomorrow and this week, in that order, whatever the window.","items":{"type":"object","required":["period","waiversRequired","completed","missing"],"properties":{"period":{"type":"string","enum":["today","tomorrow","thisWeek"]},"waiversRequired":{"type":"integer","minimum":0},"completed":{"type":"integer","minimum":0},"missing":{"type":"integer","minimum":0}}}},"breakdown":{"type":"array","maxItems":100,"description":"One entry per value of `breakdownBy`, lowest completion first.","items":{"type":"object","required":["key","label","waiversRequired","completed","completionRate"],"properties":{"key":{"type":"string","description":"The id of the venue, event, product, performance, group booking, booking or waiver form."},"label":{"type":"string"},"waiversRequired":{"type":"integer","minimum":0},"completed":{"type":"integer","minimum":0},"missing":{"type":"integer","minimum":0},"completionRate":{"type":"number","minimum":0,"maximum":1}}}},"upcomingActivities":{"type":"array","maxItems":100,"description":"Performances in the window, most at risk first, then by `dateTime`.","items":{"type":"object","required":["performanceId","eventActivity","dateTime","participants","waiversRequired","completed","missing","completion","operationalRisk"],"properties":{"performanceId":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"eventActivity":{"type":"string","description":"The event or activity name."},"venueId":{"type":"string","format":"uuid"},"venue":{"type":"string","description":"The venue name."},"dateTime":{"type":"string","format":"date-time","description":"When the performance starts."},"participants":{"type":"integer","minimum":0},"waiversRequired":{"type":"integer","minimum":0},"completed":{"type":"integer","minimum":0},"missing":{"type":"integer","minimum":0},"completion":{"type":"number","minimum":0,"maximum":1,"description":"The performance's waiver readiness (the pack's Readiness Score)."},"guardianPending":{"type":"integer","minimum":0},"exceptions":{"type":"integer","minimum":0},"admissionAtRisk":{"type":"boolean","description":"At least one missing requirement is configured to block check-in or access."},"operationalRisk":{"type":"string","enum":["ready","attention","critical"],"description":"`critical` when a missing requirement would block admission; `attention` when anything is missing; otherwise `ready`."}}}},"insights":{"type":"array","maxItems":20,"description":"Advisory predictions, e.g. participants unlikely to complete before arrival without another reminder. Never change a status.","items":{"type":"object","required":["message"],"properties":{"performanceId":{"type":"string","format":"uuid","nullable":true},"predictedIncomplete":{"type":"integer","minimum":0,"nullable":true},"message":{"type":"string","maxLength":500}}}}}},
"WaiverTemplateLibraryMasterSetupView": {"type":"object","x-ticvai-persistence":"marketing.waiver_master","description":"The master record of one waiver (pack 11.1.2), one per `FormDefinition` of kind `waiver`. The name, wording, fields and versions live on the form; this holds classification, ownership and business scope.","required":["waiverId","waiverType","ownerUserId","businessOwnerUserId","defaultLanguage","templateSource"],"properties":{"waiverId":{"type":"string","format":"uuid","description":"The `FormDefinition.id`; the natural key."},"waiverName":{"type":"string","readOnly":true,"description":"`FormDefinition.name`, shown here, written by `createForm`."},"internalDescription":{"type":"string","maxLength":2000,"nullable":true},"waiverType":{"type":"string","enum":["liabilityWaiver","parentGuardianConsent","participationConsent","medicalDeclaration","safetyAcknowledgement","mediaConsent","rentalAgreement","termsAcceptance","membershipDeclaration","customForm"]},"customTypeLabel":{"type":"string","maxLength":80,"nullable":true,"description":"The tenant's own classification name; required when `waiverType` is `customForm`."},"ownerUserId":{"type":"string","format":"uuid"},"department":{"type":"string","maxLength":100,"nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"Null for a corporate waiver every brand may use."},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"The finance legal entity the waiver is given in favour of."},"defaultLanguage":{"type":"string","maxLength":10},"applicableCountries":{"type":"array","items":{"type":"string","pattern":"^[A-Z]{2}$"},"description":"ISO 3166-1 alpha-2. Empty means the waiver is not yet scoped, which blocks publication."},"applicableJurisdiction":{"type":"string","maxLength":100,"nullable":true,"description":"A sub-national jurisdiction where the law differs within a country."},"status":{"type":"string","readOnly":true,"enum":["draft","review","pendingApproval","approved","scheduled","published","suspended","expired","archived"],"description":"The lifecycle status of the latest version (see `listWaiverConsent`)."},"templateSource":{"type":"string","enum":["createNew","duplicateExisting","masterTemplate","corporateTemplate"],"default":"createNew"},"sourceWaiverId":{"type":"string","format":"uuid","nullable":true,"description":"The waiver it was duplicated or created from; required unless `createNew`."},"sourceVersion":{"type":"integer","minimum":1,"nullable":true},"isMasterTemplate":{"type":"boolean","default":false,"description":"Offered in the reusable library. A corporate template is a master template with no `brandId`."},"businessOwnerUserId":{"type":"string","format":"uuid"},"legalReviewerUserId":{"type":"string","format":"uuid","nullable":true},"complianceOwnerUserId":{"type":"string","format":"uuid","nullable":true},"operationalOwnerUserId":{"type":"string","format":"uuid","nullable":true},"legalReviewRequired":{"type":"boolean","default":true,"description":"Whether the approval chain includes the legal/compliance step. On unless the tenant turns it off."},"usage":{"type":"object","readOnly":true,"description":"Where the waiver is used now (pack Usage Indicator, Template Dependency).","properties":{"products":{"type":"integer","minimum":0},"venues":{"type":"integer","minimum":0},"futureBookings":{"type":"integer","minimum":0}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WaiverTriggerEligibilityCompletionRulesView": {"type":"object","x-ticvai-persistence":"marketing.waiver_trigger_rule","description":"One trigger, eligibility and completion rule of a waiver (pack 11.1.7).","required":["formId","name","triggerPoint","completionDeadline","status"],"properties":{"id":{"type":"string","format":"uuid","description":"Absent on create."},"formId":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":150},"triggerPoint":{"type":"string","enum":["duringCheckout","afterPurchase","beforeTicketIssuance","beforeTicketDownload","beforeEvent","beforeCheckIn","beforeAccess","beforeEquipmentCollection","beforeMembershipActivation","beforeActivityStart"]},"eligibility":{"type":"array","description":"All must hold (AND). Empty means every participant the association reaches.","items":{"type":"object","required":["attribute","operator","values"],"properties":{"attribute":{"type":"string","enum":["age","isMinor","product","event","venue","activity","customerType","membership","country","channel","participantType","bookingType"]},"operator":{"type":"string","enum":["equals","notEquals","in","notIn","lessThan","greaterThan"]},"values":{"type":"array","minItems":1,"items":{"type":"string","maxLength":100}}}}},"completionDeadline":{"type":"object","required":["kind"],"properties":{"kind":{"type":"string","enum":["immediately","beforeTicketRelease","hoursBeforeEvent","daysBeforeVisit","beforeArrival","beforeAccess"]},"offset":{"type":"integer","minimum":1,"nullable":true,"description":"Hours for `hoursBeforeEvent`, days for `daysBeforeVisit`."}}},"enforcement":{"type":"array","items":{"type":"string","enum":["blockTicketDownload","blockTicketActivation","blockCheckIn","blockAccess"]},"description":"What an incomplete waiver blocks. Empty means warn only."},"allowStaffOverride":{"type":"boolean","default":false,"description":"An authorised operator may admit the participant anyway; the override is recorded."},"reminders":{"type":"array","items":{"type":"object","required":["offsetHours","channels"],"properties":{"offsetHours":{"type":"integer","minimum":1,"description":"Hours before the deadline, e.g. 168, 72, 24."},"channels":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/MessageChannel"}}}}},"status":{"type":"string","enum":["active","inactive"],"default":"active"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WaiverVerificationValidationWorkspaceInput": {"type":"object","x-ticvai-persistence":"marketing.waiver_verification","description":"A reviewer's decision on one waiver submission. The automatic checks are the server's and are not sent; the reviewer records the checks only a person can make.","required":["submissionId","result"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"submissionId":{"type":"string","format":"uuid","description":"The `FormSubmission` reviewed; the natural key."},"result":{"type":"string","enum":["verified","rejected","correctionRequired","escalated"]},"participantMatch":{"type":"boolean","nullable":true,"description":"The reviewer confirmed the signed participant is the booked participant."},"bookingMatch":{"type":"boolean","nullable":true},"guardianRelationshipPresent":{"type":"boolean","nullable":true,"description":"The reviewer confirmed the signatory's guardianship under the configured policy."},"requiredEvidencePresent":{"type":"boolean","nullable":true,"description":"Any supporting document the form requires was seen."},"reasonCode":{"type":"string","nullable":true,"enum":["signatoryNotAuthorised","participantMismatch","wrongVersion","incompleteAnswers","evidenceMissing","suspectedFraud","other"]},"note":{"type":"string","maxLength":2000,"nullable":true,"description":"Required for `rejected`, `correctionRequired`, `escalated`, and for changing an earlier decision."},"escalatedTo":{"type":"string","format":"uuid","nullable":true,"description":"The staff member the review is escalated to; required for `escalated`."},"reviewedBy":{"type":"string","format":"uuid","readOnly":true},"reviewedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WaiverVerificationValidationWorkspaceView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.form_submission, marketing.waiver_signature, marketing.form_definition, marketing.waiver_verification (new) and marketing.waiver_requirement (new); names from pii.subject","description":"One waiver submission in the verification queue, with its automatic checks, the reviewer's findings and any anomalies flagged.","required":["submissionId","participant","waiver","version","submitted","status","checks"],"properties":{"submissionId":{"type":"string","format":"uuid"},"requirementId":{"type":"string","format":"uuid","nullable":true},"participant":{"type":"object","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"age":{"type":"integer","minimum":0,"nullable":true}}},"waiver":{"type":"object","properties":{"formId":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"version":{"type":"integer","minimum":1,"description":"The form version signed."},"booking":{"type":"string","format":"uuid","nullable":true},"signatory":{"type":"object","properties":{"subjectId":{"type":"string","format":"uuid"},"name":{"type":"string"},"signatoryType":{"type":"string","enum":["participant","guardian","organisationRepresentative"]}}},"submitted":{"type":"string","format":"date-time","description":"`FormSubmission.submittedAt`, the device time of signing."},"verificationReason":{"type":"string","enum":["configuredManualReview","automaticCheckFailed","minorSignedAsAdult","guardianDiscrepancy","participantMismatch","evidenceRequired","aiAnomaly","sampleReview"]},"risk":{"type":"string","enum":["low","medium","high"]},"status":{"type":"string","enum":["automaticallyValidated","pendingManualVerification","verified","correctionRequired","rejected","escalated"]},"checks":{"type":"object","description":"Each check the form's configuration applies; null when it does not apply. The first seven are evaluated by the server, the last three recorded by the reviewer.","properties":{"requiredFieldsComplete":{"type":"boolean","nullable":true},"requiredQuestionsAnswered":{"type":"boolean","nullable":true},"requiredAcknowledgementsAccepted":{"type":"boolean","nullable":true},"signaturePresent":{"type":"boolean","nullable":true},"correctWaiverVersion":{"type":"boolean","nullable":true},"effectiveDateValid":{"type":"boolean","nullable":true,"description":"The version signed was in effect at signing and the acceptance covers the visit."},"guardianRelationshipPresent":{"type":"boolean","nullable":true,"description":"Evaluated from `GuestRelationship` where recorded, otherwise the reviewer's."},"participantMatch":{"type":"boolean","nullable":true},"bookingMatch":{"type":"boolean","nullable":true},"requiredEvidencePresent":{"type":"boolean","nullable":true}}},"anomalies":{"type":"array","description":"Advisory flags for the reviewer; never a decision.","items":{"type":"object","required":["code","message"],"properties":{"code":{"type":"string","enum":["minorSignedAsAdult","guardianSurnameDiffers","signatoryIsMinor","signedAfterActivity","duplicateSubmission","other"]},"message":{"type":"string","maxLength":500},"source":{"type":"string","enum":["rule","ai"]}}}},"reviewedBy":{"type":"string","format":"uuid","nullable":true},"reviewedAt":{"type":"string","format":"date-time","nullable":true},"note":{"type":"string","nullable":true}}}
}
```
