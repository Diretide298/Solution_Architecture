# WS72 — Waiver, Consent & Digital Form Management board 1

**10 screens · 12 operations · 19 schemas · 3 permissions**

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
  `GUEST_MANAGE, GUEST_VIEW, MARKETING_MANAGE`. A control nobody can use must say so,
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
| `CMS-041` | Waiver & Consent Command Center | B–D | 2 | 24 | 6 | 0 | 2 | 6 | — | notStarted (generated) |
| `CMS-042` | Waiver Template Library & Master Setup | B–D | 35 | 0 | 5 | 0 | 2 | 4 | — | notStarted (generated) |
| `CMS-043` | Digital Waiver & Form Builder | B–D | 26 | 0 | 6 | 75 | 2 | 4 | — | notStarted (generated) |
| `CMS-044` | Dynamic Fields, Questions & Conditional Logic | B–D | 18 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `CMS-045` | Signatory, Signature & Guardian Rule Configuration | B–D | 12 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `CMS-046` | Product, Event & Experience Association | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `CMS-047` | Waiver Trigger, Eligibility & Completion Rules | B–D | 15 | 0 | 5 | 0 | 1 | 4 | — | notStarted (generated) |
| `CMS-048` | Versioning, Effective Dates & Legal Change Control | B–D | 8 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `CMS-049` | Localization, Branding & Customer Experience Configuration | B–D | 0 | 32 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `CMS-050` | Waiver Approval, Testing & Publication Workspace | B–D | 4 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `CMS-041` Waiver & Consent Command Center

**Provide administrators with a centralized workspace for managing every waiver, consent form and digital declaration configured across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should display) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/waiver-consent-command-center-cms-041` |

**Known gaps.** **The pack names 16 actions on this screen and the screen declares 1 operation.** Unserved: Liability Waiver, Parent/Guardian Consent, Participation Consent, Media Consent, Rental Agreement, Terms …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Every waiver, consent form and declaration across the tenant at a glance: templates published, draft, pending approval, scheduled, expiring, archived; products requiring a waiver; versions needing review. Templates can be cloned, and there is no single standard template - a default may be offered but every business configures its own.

**Known correction pending (do not draw the wrong version)**

- **The waiver types (Liability Waiver, Parent/Guardian Consent) are drawn as action buttons.** Why: They are the type choice inside New waiver. *(source: screens/P13-white-label-cms.yaml#CMS-041; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search waiver consent | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by type, brand, venue, product, event, language and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Type | select | — | Liability waiver · Parent guardian consent · Participation consent · Medical declaration · Safety acknowledgement · Media consent · Rental agreement · Terms acceptance · Membership declaration · Custom form | `listWaiverConsent` ?type |
| Brand | picker: choose a brand | — | — | `listWaiverConsent` ?brandId |
| Product | picker: choose a product | — | — | `listWaiverConsent` ?productId |
| Event | picker: choose an event | — | — | `listWaiverConsent` ?eventId |
| Language | text field | — | max length 10 | `listWaiverConsent` ?language |
| Status | select | — | Draft · Review · Pending approval · Approved · Scheduled · Published · Suspended · Expired · Archived | `listWaiverConsent` ?status |
| Owner user | picker: choose an owner user | — | — | `listWaiverConsent` ?ownerUserId |
| Effective on | date and time picker | — | — | `listWaiverConsent` ?effectiveOn |
| Expiring within days | number field (days) | 30 | min 1; max 365 | `listWaiverConsent` ?expiringWithinDays |

#### Outputs: what the screen shows and produces

**Shown**

**Total Templates** (metric tile): Shows `kpis.totalTemplates` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over.

**Published** (metric tile): Shows `kpis.published` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over.

**Draft** (metric tile): Shows `kpis.draft` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over.

**Pending Approval** (metric tile): Shows `kpis.pendingApproval` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over.

**Scheduled** (metric tile): Shows `kpis.scheduled` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over.

**Expiring** (metric tile): Shows `kpis.expiring` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over.

**Archived** (metric tile): Shows `kpis.archived` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over.

**Products Requiring Waiver** (metric tile): Shows `kpis.productsRequiringWaiver` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over.

**Active Waiver Versions** (metric tile): Shows `kpis.activeWaiverVersions` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over.

**Waivers Requiring Review** (metric tile): Shows `kpis.waiversRequiringReview` of the `listWaiverConsent` response. That KPI object is inline in the response, not a named schema, so the binding names the row field the count is taken over.

**Every waiver consent** (data table, from `listWaiverConsent`)

| Shows | Format | Notes |
|---|---|---|
| Waiver | the name it points at, never the id | The `FormDefinition.id`. |
| Waiver name | text | — |
| Type | chip: Liability waiver, Parent guardian consent, Participation consent, Medical … | — |
| Version | 1,234 | The latest version, whatever its state. |
| Language | text | The default language from the master record. |
| Associated products | 1,234 | Products with an active association (the pack's usage indicator). |
| Signatory type | chip: Ticket holder, Purchaser, Participant, Parent, Legal guardian, Group leader… | The primary signatory from `setSignatorySignatureGuardian`. |
| Effective from | 1 Oct 2026, 14:30 | — |
| Effective to | 1 Oct 2026, 14:30 | — |
| Status | chip: Draft, Review, Pending approval, Approved, Scheduled, Published… | — |
| Owner | text | The owner's display name. |
| Last modified | 1 Oct 2026, 14:30 | — |

**The selected waiver consent** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Waiver | the name it points at, never the id | The `FormDefinition.id`. |
| Waiver name | text | — |
| Type | chip: Liability waiver, Parent guardian consent, Participation consent, Medical … | — |
| Version | 1,234 | The latest version, whatever its state. |
| Language | text | The default language from the master record. |
| Associated products | 1,234 | Products with an active association (the pack's usage indicator). |
| Signatory type | chip: Ticket holder, Purchaser, Participant, Parent, Legal guardian, Group leader… | The primary signatory from `setSignatorySignatureGuardian`. |
| Effective from | 1 Oct 2026, 14:30 | — |
| Effective to | 1 Oct 2026, 14:30 | — |
| Status | chip: Draft, Review, Pending approval, Approved, Scheduled, Published… | — |
| Owner | text | The owner's display name. |
| Last modified | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Liability Waiver (primary button) | navigation or local | — | — | — | — |
| Parent/Guardian Consent (secondary button) | navigation or local | — | — | — | — |
| Participation Consent (secondary button) | navigation or local | — | — | — | — |
| Media Consent (secondary button) | navigation or local | — | — | — | — |
| Rental Agreement (secondary button) | navigation or local | — | — | — | — |
| Terms Acceptance (secondary button) | navigation or local | — | — | — | — |
| Membership Declaration (secondary button) | navigation or local | — | — | — | — |
| Create Waiver (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Portfolio KPIs**: Counts per status, each opening the filtered list. *(source: contracts/satellite/marketing-crm.yaml#listWaiverConsent; DI-570)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **New waiver**: Start blank, duplicate an existing one, or from an approved corporate template. *(source: DI-571)*

**Data it reads**: `listWaiverConsent` (onLoad, Waiver & Consent Command Center)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-042` Waiver Template Library & Master Setup: *Works in Waiver Template Library & Master Setup*; calls `listWaiverConsent`
- → `CMS-043` Digital Waiver & Form Builder: *Works in Digital Waiver & Form Builder*; calls `listWaiverConsent`
- → `CMS-044` Dynamic Fields, Questions & Conditional Logic: *Works in Dynamic Fields, Questions & Conditional Logic*; calls `listWaiverConsent`
- → `CMS-045` Signatory, Signature & Guardian Rule Configuration: *Works in Signatory, Signature & Guardian Rule Configuration*; calls `listWaiverConsent`
- → `CMS-046` Product, Event & Experience Association: *Works in Product, Event & Experience Association*; calls `listWaiverConsent`
- → `CMS-047` Waiver Trigger, Eligibility & Completion Rules: *Works in Waiver Trigger, Eligibility & Completion Rules*; calls `listWaiverConsent`
- → `CMS-048` Versioning, Effective Dates & Legal Change Control: *Works in Versioning, Effective Dates & Legal Change Control*; calls `listWaiverConsent`
- → `CMS-049` Localization, Branding & Customer Experience Configuration: *Works in Localization, Branding & Customer Experience Configuration*; calls `listWaiverConsent`
- → `CMS-050` Waiver Approval, Testing & Publication Workspace: *Works in Waiver Approval, Testing & Publication Workspace*; calls `listWaiverConsent`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The waiver consent list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the waiver consent untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No waiver consent yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the waiver consent are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-844`: Back-office waiver screens duplicate this board (see the BO-844 correction).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  total: 14
  published: 9
  draft: 3
  pendingApproval: 1
  expiring30d: 2
  productsRequiringWaiver: 22
```

#### Permissions

- `listWaiverConsent` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Waiver dashboard tracks templates (published vs draft) and completion status. Templates can be cloned and are built with drag-and-drop fields (name, DOB, custom fields, T&C checkboxes). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-570)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-041` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-041`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 1
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 1: Opens Waiver & Consent Command Center → Provide administrators with a centralized workspace for managing every waiver, consent form and digital declaration configured across TICVAI.
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F181 branch at step 1 (expected): when Nothing has been set up on Waiver & Consent Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F181 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-041?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Liability Waiver, Parent/Guardian Consent, Participation Consent, Media Consent, Rental Agreement, Terms Acceptance, Membership Declaration, Create Waiver.
- [ ] Every transition is wired: `CMS-001`, `CMS-042`, `CMS-043`, `CMS-044`, `CMS-045`, `CMS-046`, `CMS-047`, `CMS-048`, `CMS-049`, `CMS-050`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-042` Waiver Template Library & Master Setup

**Create the master definition of a waiver or consent form before individual content and questions are configured.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW`, `MARKETING_MANAGE` (1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/waiver-template-library-master-setup-cms-042` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Create New, Duplicate Existing, Create From Approved Corporate Template. Each needs an operation, or needs … **Waiver Template Library & Master Setup declares no operation that writes anything** — its only declared call is `listWaiverTemplateMaster`, a read. The name promises authoring and the contract …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The master record of a waiver before content is written: name, description, type, owner, department, brand, legal entity, default language, jurisdiction and status.

**Fixed on main** (the package already carries these; draw what it says): Every field (Waiver ID, Name, Description) is a select, and only a list read is declared. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Waiver ID | select field | — | — | — | — | — | — |
| Waiver Name | select field | — | — | — | — | — | — |
| Internal Description | select field | — | — | — | — | — | — |
| Waiver Type | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Department | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Legal Entity | select field | — | — | — | — | — | — |
| Default Language | select field | — | — | — | — | — | — |
| Applicable Country/Jurisdiction | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Waiver type | select | — | Liability waiver · Parent guardian consent · Participation consent · Medical declaration · Safety acknowledgement · Media consent · Rental agreement · Terms acceptance · Membership declaration · Custom form | `listWaiverTemplateMaster` ?waiverType |
| Brand | picker: choose a brand | — | — | `listWaiverTemplateMaster` ?brandId |
| Is master template | toggle | — | — | `listWaiverTemplateMaster` ?isMasterTemplate |
| Q | text field | — | max length 100 | `listWaiverTemplateMaster` ?q |

**Form: Create waiver form** (modal, opened by *Create waiver form*; *Create waiver form* calls `createForm`, *Cancel* sends nothing)

**Collects what `createForm` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | — | — | — | `createForm` body |
| Kind `kind` | select | required | — | Waiver · Survey · Data capture · Consent form · Incident report · Registration | — | — | `createForm` body |
| Consent purposes `consentPurposes` | multi-select chips | optional | — | Face pass · Face tag · Marketing · Photography · Waiver | — | What a `consentForm` consents to (Chinmay, 2 October, batch 4; follows BO-188: biometric capture needs consent on the venue's own form; CHG-CSA-026). | `createForm` body |
| Fields `fields` | repeatable rows | optional | — | — | — | — | `createForm` body |
| Key `fields[].key` | text field | required | — | — | — | — | `createForm` body |
| Label `fields[].label` | text field | required | — | — | — | — | `createForm` body |
| Label localised `fields[].labelLocalised` | key and value settings | optional | — | — | — | — | `createForm` body |
| Type `fields[].type` | select | required | — | Text · Long text · Number · Date · Select · Multi select · Boolean · Scale · Signature · File · Phone · Email | — | — | `createForm` body |
| Options `fields[].options` | list of values (chips) | optional | — | — | — | — | `createForm` body |
| Is required `fields[].isRequired` | toggle | optional | off | — | — | — | `createForm` body |
| Is personal data `fields[].isPersonalData` | toggle | optional | off | — | — | Marked at the field, because retention is decided at the field. A survey answer and a medical condition on the same form have different lifetimes, and a form-level flag makes the … | `createForm` body |
| Consent purpose `fields[].consentPurposeId` | picker: choose a consent purpose | optional | — | — | shows names, sends the id | — | `createForm` body |
| Show when `fields[].showWhen` | group | optional | — | — | — | — | `createForm` body |
| Field `fields[].showWhen.field` | text field | optional | — | — | — | — | `createForm` body |
| Equals `fields[].showWhen.equals` | text field | optional | — | — | — | — | `createForm` body |
| Requires signature `requiresSignature` | toggle | optional | off | — | — | What makes it a waiver. And 2.15.9 makes ticket issuance conditional on one, which puts this in the purchase path rather than beside it. | `createForm` body |
| Signature kind `signatureKind` | radio group | optional | None | Drawn · Typed · Checkbox · None | — | — | `createForm` body |
| Score scale `scoreScale` | select | optional | — | Nps · Csat · Ces · Likert5 · Likert7 · Stars; Named rather than free-form because a score whose scale is unknown cannot be compared to last quarter's. | — | What makes it a survey. Named rather than free-form because a score whose scale is unknown cannot be compared to last quarter's. | `createForm` body |
| Applies to products `appliesToProductIds` | multi-picker: choose applies to products | optional | — | — | — | — | `createForm` body |
| Valid for months `validForMonths` | number field | optional | — | — | — | How long an acceptance lasts. A waiver signed last summer may or may not still hold, and 2.15.x asks for a returning participant not to sign again — which only works if the expiry … | `createForm` body |
| Minimum age `minimumAge` | number field | optional | — | — | — | — | `createForm` body |
| Requires guardian for minors `requiresGuardianForMinors` | toggle | optional | on | — | — | A minor cannot waive their own rights. A guardian signs, and the record has to name them — an unsigned or self-signed minor waiver is worth nothing at the moment it matters. | `createForm` body |
| Legal reviewed by `legalReviewedBy` | text field | optional | — | — | — | — | `createForm` body |
| Legal reviewed at `legalReviewedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createForm` body |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Type**: Liability release, general consent, parental or guardian consent, medical declaration, risk acknowledgement, activity agreement. *(source: screens/P08-venue-back-office.yaml#BO-845)*
- **Default language**: English or Arabic; the other must be complete before publication. *(source: DI-019)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create New (primary button) | `createForm` POST `/forms` | FormDefinition | FormDefinition | — | opens modal first |
| Duplicate Existing (secondary button) | navigation or local | — | — | — | — |
| Create From Approved Corporate Template (secondary button) | navigation or local | — | — | — | — |
| Create waiver form (secondary button) | `createForm` POST `/forms` | FormDefinition | FormDefinition | — | opens modal first |

**Data it reads**: `listWaiverTemplateMaster` (onLoad, Waiver Template Library & Master Setup)

**Where the user goes next**

- → `CMS-041` Waiver & Consent Command Center: *Returns to the board's landing screen*; calls `listWaiverTemplateMaster`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The waiver template master configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the waiver template master untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No waiver template master configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
master: Water activity waiver - liability release - owner Legal - Coastal Aqua LLC - UAE - default English
```

#### Permissions

- `listWaiverTemplateMaster` → `GUEST_VIEW` (read) · staff
- `createForm` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam: no single standard waiver; a default/pre-set template can be offered, but the builder must stay fully configurable because each business has its own requirements. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-571)*
- Waiver dashboard tracks templates (published vs draft) and completion status. Templates can be cloned and are built with drag-and-drop fields (name, DOB, custom fields, T&C checkboxes). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-570)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-042` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-042`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 1
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 2: Works in Waiver Template Library & Master Setup → Create the master definition of a waiver or consent form before individual content and questions are configured.

#### Acceptance for the design

- [ ] Every input above is drawn (35), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-042?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create New, Duplicate Existing, Create From Approved Corporate Template, Create waiver form.
- [ ] Every transition is wired: `CMS-041`.
- [ ] Every gated control is gated: `GUEST_VIEW`, `MARKETING_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-043` Digital Waiver & Form Builder

**Provide a no-code visual builder for creating the actual customer-facing waiver or digital form.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `MARKETING_MANAGE` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/digital-waiver-form-builder-cms-043` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Information Box, Customer Details, Guardian Details. Each needs an operation, or needs removing from the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The no-code builder for the guest-facing waiver: sections and blocks (information box, customer details, guardian details, clauses, terms checkboxes, initials, signature) by drag and drop, EN and AR side by side, and a mobile-first guest preview.

**Known correction pending (do not draw the wrong version)**

- **The block palette (Information Box, Customer Details, Guardian Details) is drawn as action-bar buttons.** Why: They are palette items of a canvas. *(source: screens/P13-white-label-cms.yaml#CMS-043; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Form kind | select | optional | — | Waiver · Survey · Data capture · Consent form · Incident report · Registration | — | **The consent-form builder (decided by Chinmay, 2 October 2026; DEC-549):** the existing waiver builder extended, not a second builder. A form is a waiver or a `consentForm` with its … | `FormDefinition.kind` |
| Guardian consent for minors | toggle | optional | on | — | — | A child signs through a guardian on the venue's form; the minor age is the country's (DEC-237) (CHG-SGU-004). | `FormDefinition.requiresGuardianForMinors` |

**Form: New consent form** (modal, opened by *New consent form*; *New consent form* calls `createForm`, *Cancel* sends nothing)

Name, kind (waiver or consentForm) and the consent purposes it collects; fields are added in the builder.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | — | — | — | `createForm` body |
| Kind `kind` | select | required | — | Waiver · Survey · Data capture · Consent form · Incident report · Registration | — | — | `createForm` body |
| Consent purposes `consentPurposes` | multi-select chips | optional | — | Face pass · Face tag · Marketing · Photography · Waiver | — | What a `consentForm` consents to (Chinmay, 2 October, batch 4; follows BO-188: biometric capture needs consent on the venue's own form; CHG-CSA-026). | `createForm` body |
| Fields `fields` | repeatable rows | optional | — | — | — | — | `createForm` body |
| Key `fields[].key` | text field | required | — | — | — | — | `createForm` body |
| Label `fields[].label` | text field | required | — | — | — | — | `createForm` body |
| Label localised `fields[].labelLocalised` | key and value settings | optional | — | — | — | — | `createForm` body |
| Type `fields[].type` | select | required | — | Text · Long text · Number · Date · Select · Multi select · Boolean · Scale · Signature · File · Phone · Email | — | — | `createForm` body |
| Options `fields[].options` | list of values (chips) | optional | — | — | — | — | `createForm` body |
| Is required `fields[].isRequired` | toggle | optional | off | — | — | — | `createForm` body |
| Is personal data `fields[].isPersonalData` | toggle | optional | off | — | — | Marked at the field, because retention is decided at the field. A survey answer and a medical condition on the same form have different lifetimes, and a form-level flag makes the … | `createForm` body |
| Consent purpose `fields[].consentPurposeId` | picker: choose a consent purpose | optional | — | — | shows names, sends the id | — | `createForm` body |
| Show when `fields[].showWhen` | group | optional | — | — | — | — | `createForm` body |
| Field `fields[].showWhen.field` | text field | optional | — | — | — | — | `createForm` body |
| Equals `fields[].showWhen.equals` | text field | optional | — | — | — | — | `createForm` body |
| Requires signature `requiresSignature` | toggle | optional | off | — | — | What makes it a waiver. And 2.15.9 makes ticket issuance conditional on one, which puts this in the purchase path rather than beside it. | `createForm` body |
| Signature kind `signatureKind` | radio group | optional | None | Drawn · Typed · Checkbox · None | — | — | `createForm` body |
| Score scale `scoreScale` | select | optional | — | Nps · Csat · Ces · Likert5 · Likert7 · Stars; Named rather than free-form because a score whose scale is unknown cannot be compared to last quarter's. | — | What makes it a survey. Named rather than free-form because a score whose scale is unknown cannot be compared to last quarter's. | `createForm` body |
| Applies to products `appliesToProductIds` | multi-picker: choose applies to products | optional | — | — | — | — | `createForm` body |
| Valid for months `validForMonths` | number field | optional | — | — | — | How long an acceptance lasts. A waiver signed last summer may or may not still hold, and 2.15.x asks for a returning participant not to sign again — which only works if the expiry … | `createForm` body |
| Minimum age `minimumAge` | number field | optional | — | — | — | — | `createForm` body |
| Requires guardian for minors `requiresGuardianForMinors` | toggle | optional | on | — | — | A minor cannot waive their own rights. A guardian signs, and the record has to name them — an unsigned or self-signed minor waiver is worth nothing at the moment it matters. | `createForm` body |
| Legal reviewed by `legalReviewedBy` | text field | optional | — | — | — | — | `createForm` body |
| Legal reviewed at `legalReviewedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createForm` body |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Blocks**: Name, date of birth, custom fields, terms checkboxes, information text, signature; layout saved on a draft version only. *(source: contracts/satellite/marketing-crm.yaml#setDigitalWaiverForm; DI-570)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Information Box (primary button) | navigation or local | — | — | — | — |
| Customer Details (secondary button) | navigation or local | — | — | — | — |
| Guardian Details (secondary button) | navigation or local | — | — | — | — |
| New consent form (secondary button) | `createForm` POST `/forms` | FormDefinition | FormDefinition | — | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Guest preview**: Mobile view in English and Arabic (right-to-left), as opened from a QR code. *(source: DI-575; DI-019)*

**Where the user goes next**

- → `CMS-041` Waiver & Consent Command Center: *Returns to the board's landing screen*; calls `setDigitalWaiverForm`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital waiver form list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital waiver form untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital waiver form yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the digital waiver form are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The version is no longer a draft.; 422 A block names a field the version does not have, or a block kind needs content it lacks. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
layout:
- Information - Read before you dive
- Participant details
- Guardian details (if under 16)
- Clauses 1-8 with initials on 4 and 6
- I accept the risk checkbox
- Signature
```

#### Permissions

- `setDigitalWaiverForm` → `GUEST_MANAGE` (configure) · staff
- `createForm` → `MARKETING_MANAGE` (configure) · staff

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

- Allam: no single standard waiver; a default/pre-set template can be offered, but the builder must stay fully configurable because each business has its own requirements. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-571)*
- Waiver dashboard tracks templates (published vs draft) and completion status. Templates can be cloned and are built with drag-and-drop fields (name, DOB, custom fields, T&C checkboxes). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-570)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-043` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-043`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 1
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 4: Works in Digital Waiver & Form Builder → Provide a no-code visual builder for creating the actual customer-facing waiver or digital form.

#### Acceptance for the design

- [ ] Every input above is drawn (26), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-043?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Information Box, Customer Details, Guardian Details, New consent form.
- [ ] Every transition is wired: `CMS-041`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `MARKETING_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-044` Dynamic Fields, Questions & Conditional Logic

**Configure the information that must be collected from the participant or signatory.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Reusable fields can include; Each field can be; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/dynamic-fields-questions-conditional-logic-cms-044` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Single Select, Customer Lookup. Each needs an operation, or needs removing from the screen; this is the … Contract gap recorded 2 October 2026 (CHG-WIR-007): No write saves a waiver's dynamic fields, questions and conditional logic.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The information collected from the participant or signatory: each field's requirement (required, optional, conditional, read-only, auto-populated), validation and conditions. The client's examples: ask for the Emirate only if the country is UAE; ask extra questions only below an age.

**Known correction pending (do not draw the wrong version)**

- **Only a read is declared, and field names and rule types are select fields.** Why: The field editor needs a write; rule types are per-field controls. *(source: contracts/satellite/marketing-crm.yaml#listDynamicFieldQuestion; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Participant Name | select field | — | — | — | — | — | — |
| Date of Birth | select field | — | — | — | — | — | — |
| Customer ID | select field | — | — | — | — | — | — |
| Booking Reference | select field | — | — | — | — | — | — |
| Ticket Number | select field | — | — | — | — | — | — |
| Guardian Name | select field | — | — | — | — | — | — |
| Relationship | select field | — | — | — | — | — | — |
| Emergency Contact | select field | — | — | — | — | — | — |
| Required | select field | — | — | — | — | — | — |
| Optional | select field | — | — | — | — | — | — |
| Conditional | select field | — | — | — | — | — | — |
| Read Only | select field | — | — | — | — | — | — |
| Auto-Populated | select field | — | — | — | — | — | — |
| Minimum/Maximum | select field | — | — | — | — | — | — |
| Date range | select field | — | — | — | — | — | — |
| Format | select field | — | — | — | — | — | — |
| Character limit | select field | — | — | — | — | — | — |
| Allowed values | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Form | picker: choose a form | — | — | `listDynamicFieldQuestion` ?formId |
| Version | number field | — | min 1 | `listDynamicFieldQuestion` ?version |
| Standard only | toggle | — | — | `listDynamicFieldQuestion` ?standardOnly |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Condition**: Show when another answer matches (country = UAE -> Emirate) or by age band. *(source: DI-572; contracts/satellite/marketing-crm.yaml#listDynamicFieldQuestion)*
- **Auto-populated**: From the booking or profile (name, date of birth, booking reference) and read-only where so marked. *(source: contracts/satellite/marketing-crm.yaml#listDynamicFieldQuestion)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Single Select (primary button) | navigation or local | — | — | — | — |
| Customer Lookup (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listDynamicFieldQuestion` (onLoad, Dynamic Fields, Questions & Conditional Logic)

**Where the user goes next**

- → `CMS-041` Waiver & Consent Command Center: *Returns to the board's landing screen*; calls `listDynamicFieldQuestion`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic fields questions configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic fields questions untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic fields questions configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
fields:
- Country (required)
- Emirate (if UAE)
- Date of birth (required, auto from profile)
- Medical conditions (if age over 60)
- Emergency contact (required)
```

#### Permissions

- `listDynamicFieldQuestion` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Conditional fields: e.g. ask for the Emirates city only if country is UAE; ask extra questions only if age is below a threshold. Signatory config sets who signs (participant or parent/guardian). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-572)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-044` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-044`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 1
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 6: Works in Dynamic Fields, Questions & Conditional Logic → Configure the information that must be collected from the participant or signatory.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-044?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Single Select, Customer Lookup.
- [ ] Every transition is wired: `CMS-041`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-045` Signatory, Signature & Guardian Rule Configuration

**Define who is legally or operationally required to complete and sign the waiver.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; For group bookings, configure whether) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/signatory-signature-guardian-rule-configuration-cms-045` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Ticket Holder, Rental Customer, Other Authorized Signatory, Customer + Authorized Representative. Each needs …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Who must sign and how: signature, initials, typed or checkbox acceptance, identity verification; each participant individually, a guardian for each minor, or a group leader where permitted; per product kind (ticket holder, rental customer). Guardian signature age bands come from the product's eligibility rule.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Signature Required | select field | — | — | — | — | — | — |
| Initials Required | select field | — | — | — | — | — | — |
| Typed Acceptance | select field | — | — | — | — | — | — |
| Checkbox Acceptance | select field | — | — | — | — | — | — |
| Digital Signature | select field | — | — | — | — | — | — |
| Date/Time | select field | — | — | — | — | — | — |
| Signatory Name | select field | — | — | — | — | — | — |
| Relationship | select field | — | — | — | — | — | — |
| Identity Verification where required | text field | — | — | — | — | — | — |
| Each participant signs individually | text field | — | — | — | — | — | — |
| Guardian signs for each minor | text field | — | — | — | — | — | — |
| Group leader signs where legally/operationally permitted | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Minor rule**: Below the configured age a guardian signs; a missing date of birth counts as a minor. *(source: contracts/satellite/marketing-crm.yaml#setSignatorySignatureGuardian; R205; DG-3)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Ticket Holder (primary button) | navigation or local | — | — | — | — |
| Rental Customer (secondary button) | navigation or local | — | — | — | — |
| Other Authorized Signatory (secondary button) | navigation or local | — | — | — | — |
| Customer + Authorized Representative (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-041` Waiver & Consent Command Center: *Returns to the board's landing screen*; calls `setSignatorySignatureGuardian`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The signatory signature guardian configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the signatory signature guardian untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No signatory signature guardian configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The version is no longer a draft.; 422 A signatory or group mode the version's fields cannot collect (e.g. a guardian mode with no guardian signature field). |

#### Consistency with other screens

- Match `BO-849`: Same rules.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: Each participant 16+ signs; under 16 a guardian signs per child; school groups - teacher signs with parental
  consent on file
```

#### Permissions

- `setSignatorySignatureGuardian` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Conditional fields: e.g. ask for the Emirates city only if country is UAE; ask extra questions only if age is below a threshold. Signatory config sets who signs (participant or parent/guardian). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-572)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-045` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-045`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 1
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 8: Works in Signatory, Signature & Guardian Rule Configuration → Define who is legally or operationally required to complete and sign the waiver.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-045?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Ticket Holder, Rental Customer, Other Authorized Signatory, Customer + Authorized Representative.
- [ ] Every transition is wired: `CMS-041`.
- [ ] Every gated control is gated: `GUEST_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-046` Product, Event & Experience Association

**Determine which TICVAI products or activities require each waiver.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/product-event-experience-association-cms-046` |

**Known gaps.** **The pack names 9 actions on this screen and the screen declares 1 operation.** Unserved: Ticket Type, Attraction, Activity, Membership, Resource, Package, Venue. Each needs an operation, or needs … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Which products, ticket types, events, attractions, activities, memberships, resources and packages require each waiver. Buying an associated product triggers the waiver automatically.

**Known correction pending (do not draw the wrong version)**

- **Scope kinds are drawn as buttons and only a read is declared.** Why: Associations cannot be created here. *(source: contracts/satellite/marketing-crm.yaml#listProductEventExperience; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Form | picker: choose a form | — | — | `listProductEventExperience` ?formId |
| Target type | select | — | Global · Brand · Venue · Product · Ticket type · Event · Performance · Attraction · Activity · Membership · Camp · Rental … | `listProductEventExperience` ?targetType |
| Target | picker: choose a target | — | — | `listProductEventExperience` ?targetId |
| Requirement | radio group | — | Mandatory · Optional · Conditional · Informational | `listProductEventExperience` ?requirement |
| Include inherited | toggle | off | — | `listProductEventExperience` ?includeInherited |
| Include impact | toggle | off | — | `listProductEventExperience` ?includeImpact |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Product (primary button) | navigation or local | — | — | — | — |
| Ticket Type (secondary button) | navigation or local | — | — | — | — |
| Event (secondary button) | navigation or local | — | — | — | — |
| Attraction (secondary button) | navigation or local | — | — | — | — |
| Activity (secondary button) | navigation or local | — | — | — | — |
| Membership (secondary button) | navigation or local | — | — | — | — |
| Resource (secondary button) | navigation or local | — | — | — | — |
| Package (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Association row**: Scope (product, event...), waiver, version in force, timing. *(source: contracts/satellite/marketing-crm.yaml#listProductEventExperience; DI-573)*

**Data it reads**: `listProductEventExperience` (onLoad, Product, Event & Experience Association)

**Where the user goes next**

- → `CMS-041` Waiver & Consent Command Center: *Returns to the board's landing screen*; calls `listProductEventExperience`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product event experience list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product event experience untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product event experience yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product event experience are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
associations:
- Deep Dive session -> Water activity waiver v3
- Kids Club Explorer Pass -> Parental consent v2
- Bike rental -> Rental agreement v1
```

#### Permissions

- `listProductEventExperience` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Waiver is triggered automatically when an associated product is bought; timing is business-configurable: at checkout, post-purchase, or on-site before entry. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-573)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-046` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-046`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 1
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 10: Works in Product, Event & Experience Association → Determine which TICVAI products or activities require each waiver.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-046?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Product, Ticket Type, Event, Attraction, Activity, Membership, Resource, Package.
- [ ] Every transition is wired: `CMS-041`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-047` Waiver Trigger, Eligibility & Completion Rules

**Define when a waiver is required, when it must be completed and what happens if it is not completed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Configure whether incomplete status; Configure reminders such as) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/waiver-trigger-eligibility-completion-rules-cms-047` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-007): No write saves waiver trigger, eligibility and completion rules.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** When a waiver is required, by when it must be completed, and what an incomplete one blocks. Timing is business-configurable (at checkout, post-purchase, on-site before entry), and an incomplete waiver can warn only or block download, activation, check-in or access, or require a staff override.

**Known correction pending (do not draw the wrong version)**

- **Options are select fields and only a read is declared.** Why: The rules cannot be saved. *(source: contracts/satellite/marketing-crm.yaml#listWaiverTriggerEligibility; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Immediately | select field | — | — | — | — | — | — |
| Before Ticket Release | select field | — | — | — | — | — | — |
| X hours before event | text field | — | — | — | — | — | — |
| X days before visit | text field | — | — | — | — | — | — |
| Before arrival | select field | — | — | — | — | — | — |
| Before access | select field | — | — | — | — | — | — |
| Warns only | select field | — | — | — | — | — | — |
| Blocks Ticket Download | select field | — | — | — | — | — | — |
| Blocks Ticket Activation | select field | — | — | — | — | — | — |
| Blocks Check-In | select field | — | — | — | — | — | — |
| Blocks Access | select field | — | — | — | — | — | — |
| Requires Staff Override | select field | — | — | — | — | — | — |
| T−7 days | select field | — | — | — | — | — | — |
| T−3 days | select field | — | — | — | — | — | — |
| T−24 hours | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Form | picker: choose a form | — | — | `listWaiverTriggerEligibility` ?formId |
| Trigger point | select | — | During checkout · After purchase · Before ticket issuance · Before ticket download · Before event · Before check in · Before access · Before equipment collection · Before membership activation · Before activity start | `listWaiverTriggerEligibility` ?triggerPoint |
| Status | segmented control | — | Active · Inactive | `listWaiverTriggerEligibility` ?status |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Deadline**: Immediately, before ticket release, X hours before the event, X days before the visit, before arrival, before access. *(source: contracts/satellite/marketing-crm.yaml#listWaiverTriggerEligibility; DI-573)*
- **Consequence**: Warn only, block download, block activation, block check-in, block access, staff override. *(source: DI-574)*
- **Reminders**: T-7 days, T-3 days, T-24 hours; transactional messages. *(source: screens/P13-white-label-cms.yaml#CMS-047)*

#### Outputs: what the screen shows and produces

**Data it reads**: `listWaiverTriggerEligibility` (onLoad, Waiver Trigger, Eligibility & Completion Rules)

**Where the user goes next**

- → `CMS-041` Waiver & Consent Command Center: *Returns to the board's landing screen*; calls `listWaiverTriggerEligibility`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The waiver trigger eligibility configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the waiver trigger eligibility untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No waiver trigger eligibility configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: Water activity waiver - before access - reminders T-3 days and T-24 hours - incomplete blocks check-in
```

#### Permissions

- `listWaiverTriggerEligibility` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Waiver is triggered automatically when an associated product is bought; timing is business-configurable: at checkout, post-purchase, or on-site before entry. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-573)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-047` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-047`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 1
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 12: Works in Waiver Trigger, Eligibility & Completion Rules → Define when a waiver is required, when it must be completed and what happens if it is not completed.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-047?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-041`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-048` Versioning, Effective Dates & Legal Change Control

**Ensure TICVAI maintains a complete historical record of exactly which waiver wording each participant accepted.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/versioning-effective-dates-legal-change-control-cms-048` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Previous Version ↔ New Version. Each needs an operation, or needs removing from the screen; this is the …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The record of exactly which wording each participant accepted: version number, author, reason, legal reviewer, approval, effective from and to, and a side-by-side comparison of versions. Published versions are immutable once signed against.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Version Number | select field | — | — | — | — | — | — |
| Created By | select field | — | — | — | — | — | — |
| Created Date | select field | — | — | — | — | — | — |
| Change Reason | select field | — | — | — | — | — | — |
| Legal Reviewer | select field | — | — | — | — | — | — |
| Approval | select field | — | — | — | — | — | — |
| Effective From | select field | — | — | — | — | — | — |
| Effective To | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Form | picker: choose a form | — | — | `listVersioningEffectiveDate` ?formId |
| Compare with | number field | — | min 1 | `listVersioningEffectiveDate` ?compareWith |
| Status | radio group | — | Draft · Published · Superseded · Retired | `listVersioningEffectiveDate` ?status |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Previous Version ↔ New Version (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Version comparison**: Changed clauses highlighted; whether existing signers must re-sign. *(source: contracts/satellite/marketing-crm.yaml#listVersioningEffectiveDate; contracts/satellite/marketing-crm.yaml#createForm)*

**Data it reads**: `listVersioningEffectiveDate` (onLoad, Versioning, Effective Dates & Legal Change Control)

**Where the user goes next**

- → `CMS-041` Waiver & Consent Command Center: *Returns to the board's landing screen*; calls `listVersioningEffectiveDate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The versioning effective dates configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the versioning effective dates untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No versioning effective dates configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
versions:
- v3 - effective 1 Sep 2026 - clause 6 medical added - approved by Legal
- v2 - effective 1 Mar 2026 - superseded
```

#### Permissions

- `listVersioningEffectiveDate` → `GUEST_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-048` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-048`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 1
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 14: Works in Versioning, Effective Dates & Legal Change Control → Ensure TICVAI maintains a complete historical record of exactly which waiver wording each participant accepted.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-048?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Previous Version ↔ New Version.
- [ ] Every transition is wired: `CMS-041`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-049` Localization, Branding & Customer Experience Configuration

**Configure how the waiver appears across different brands, languages and customer channels.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each version should show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/localization-branding-customer-experience-configuration-cms-049` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Additional languages as configured. Each needs an operation, or needs removing from the screen; this is the …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** How a waiver appears across brands, languages and channels: translation status per language, branding and delivery channels per version.

**Fixed on main** (the package already carries these; draw what it says): The list is bound to setLocalizationBrandingCustomer (a write). (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Form | picker: choose a form | — | — | `getLocalizationBrandingCustomer` ?formId |
| Version | number field | — | min 1 | `getLocalizationBrandingCustomer` ?version |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every localization branding customer** (data table, from `setLocalizationBrandingCustomer`)

| Shows | Format | Notes |
|---|---|---|
| Source language | text | The language the legal text is written and reviewed in. |
| Translation status | chip: Not started, AI drafted, In translation, In review, Complete | — |
| Translator user | the name it points at, never the id | — |
| Reviewer user | the name it points at, never the id | — |
| Approval status | chip: Pending, Approved, Rejected | — |
| Last updated | 1 Oct 2026, 14:30 | — |

**Current configuration** (detail panel, from `getLocalizationBrandingCustomer`)

| Shows | Format | Notes |
|---|---|---|
| Form | the name it points at, never the id | — |
| Form version | 1,234 | — |
| Source language | text | The language the legal text is written and reviewed in. |
| Languages | list or chips (count when long) | Every language the version is offered in, the source language included. Arabic renders right to left. |
| Language | text | — |
| Required | yes / no (icon or chip) | Publication waits for this language's approval. |
| Translation status | chip: Not started, AI drafted, In translation, In review, Complete | — |
| Translator user | the name it points at, never the id | — |
| Reviewer user | the name it points at, never the id | — |
| Approval status | chip: Pending, Approved, Rejected | — |
| Last updated | 1 Oct 2026, 14:30 | — |
| Branding | grouped details | — |
| Brand logo | the image or video | — |
| Venue logo | the image or video | — |
| Theme | text | The white-label theme it takes colours and typography from. |
| Header | in the reader's language | — |
| Footer | in the reader's language | — |
| Customer instructions | in the reader's language | — |
| Confirmation message | in the reader's language | — |
| Support email | email, tap to write | — |

**The selected localization branding customer** (detail panel): The pack groups this record's detail under its own headings: “Preview for”, “Accessibility”.

| Shows | Format | Notes |
|---|---|---|
| Source language | text | The language the legal text is written and reviewed in. |
| Translation status | chip: Not started, AI drafted, In translation, In review, Complete | — |
| Translator user | the name it points at, never the id | — |
| Reviewer user | the name it points at, never the id | — |
| Approval status | chip: Pending, Approved, Rejected | — |
| Last updated | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Additional languages as configured (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Translation status**: Per language, complete or missing; Arabic missing blocks publication. *(source: contracts/satellite/marketing-crm.yaml#setLocalizationBrandingCustomer; DI-019)*

**Data it reads**: `getLocalizationBrandingCustomer` (onLoad, The waiver version's languages)

**Where the user goes next**

- → `CMS-041` Waiver & Consent Command Center: *Returns to the board's landing screen*; calls `setLocalizationBrandingCustomer`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The localization branding customer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the localization branding customer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No localization branding customer yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the localization branding customer are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A language of a published version was changed.; 422 An approval without a human reviewer, or approved by the translator. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
status: Water activity waiver v3 - EN complete, AR complete - channels web, app, kiosk - Coastal Aqua branding
```

#### Permissions

- `setLocalizationBrandingCustomer` → `GUEST_MANAGE` (configure) · staff
- `getLocalizationBrandingCustomer` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-049` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-049`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 1
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 16: Works in Localization, Branding & Customer Experience Configuration → Configure how the waiver appears across different brands, languages and customer channels.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (32 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-049?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Additional languages as configured.
- [ ] Every transition is wired: `CMS-041`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-050` Waiver Approval, Testing & Publication Workspace

**Provide the final governance gate before a waiver becomes operational. Board 1 configured what the waiver is, who must sign it, when it applies, and how it is published. Board 2 manages what happens operationally after a waiver requirement is assigned to a booking, ticket, participant, member, rental, group, or activity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Fields; Configuration experience; Board 1 Configuration Flow) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/waiver-approval-testing-publication-workspace-cms-050` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Publish Now, Schedule Publication, Publish to Selected Venues, Publish to Selected Products. Each needs an …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The final gate before a waiver is live: submit for review with a reason, operations review, legal approval, test, then publish now, on a schedule, or to selected venues or products.

**Known correction pending (do not draw the wrong version)**

- **Fields labelled "11.1.1" and "0" and a text field "-> Approve & Publish".** Why: Matrix references and placeholders leak into the UI. *(source: screens/P13-white-label-cms.yaml#CMS-050; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Required fields configured | select field | — | — | — | — | — | — |
| 11.1.1 | select field | — | — | — | — | — | — |
| 0 | select field | — | — | — | — | — | — |
| → Approve & Publish | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish Now (primary button) | navigation or local | — | — | — | — |
| Schedule Publication (secondary button) | navigation or local | — | — | — | — |
| Publish to Selected Venues (secondary button) | navigation or local | — | — | — | — |
| Publish to Selected Products (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Approve and publish**: Each step records who and why; publishing makes the version the one new signers see. *(source: contracts/satellite/marketing-crm.yaml#approveWaiverTesting; DI-575)*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The waiver approval testing configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the waiver approval testing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No waiver approval testing configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The action does not apply to the version's current stage.; 422 A critical checklist failure, or the approver is the submitter. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
approval: Water activity waiver v4 - submitted by Ops (clause 6) - legal approved 30 Sep - publish 1 Nov 2026 to
  Coastal Aqua
```

#### Permissions

- `approveWaiverTesting` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-050` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS184 Waiver, Consent & Digital Form Management Board 1.dc.html#cms-050`
- Workshop pack: Waiver, Consent & Digital Form Management_Reference.pdf board 1
- Flow F181 *Waiver, Consent & Digital Form Management board 1: Waiver & Consent Command …*, step 18: Works in Waiver Approval, Testing & Publication Workspace → Provide the final governance gate before a waiver becomes operational. Board 1 configured what the waiver is, who must sign it, when it applies, and how it is published. Board 2 manages what happens …

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-050?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish Now, Schedule Publication, Publish to Selected Venues, Publish to Selected Products.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `GUEST_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**13 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approveWaiverTesting": {"method":"PUT","path":"/waiver-testing","contract":"marketing-crm","summary":"Move a waiver version through review, approval and publication","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WaiverApprovalTestingPublicationWorkspaceInput","responds":"WaiverApprovalTestingPublicationWorkspaceView"},
"createForm": {"method":"POST","path":"/forms","contract":"marketing-crm","summary":"Define a waiver, survey or capture form","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FormDefinition","responds":"FormDefinition"},
"getLocalizationBrandingCustomer": {"method":"GET","path":"/localization-branding-customer","contract":"marketing-crm","summary":"Load a waiver version's languages, branding and channels","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"formId","in":"query","required":true},{"name":"version","in":"query","required":false}],"requestBody":null,"responds":"LocalizationBrandingCustomerExperienceConfigurationView"},
"listDynamicFieldQuestion": {"method":"GET","path":"/dynamic-field-question","contract":"marketing-crm","summary":"Dynamic Fields, Questions & Conditional Logic","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"formId","in":"query","required":true},{"name":"version","in":"query","required":false},{"name":"standardOnly","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductEventExperience": {"method":"GET","path":"/product-event-experience","contract":"marketing-crm","summary":"Product, Event & Experience Association","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"formId","in":"query","required":false},{"name":"targetType","in":"query","required":false},{"name":"targetId","in":"query","required":false},{"name":"requirement","in":"query","required":false},{"name":"includeInherited","in":"query","required":false},{"name":"includeImpact","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVersioningEffectiveDate": {"method":"GET","path":"/versioning-effective-date","contract":"marketing-crm","summary":"Versioning, Effective Dates & Legal Change Control","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"formId","in":"query","required":false},{"name":"compareWith","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWaiverConsent": {"method":"GET","path":"/waiver-consent","contract":"marketing-crm","summary":"Waiver & Consent Command Center","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"type","in":"query","required":false},{"name":"brandId","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"eventId","in":"query","required":false},{"name":"language","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"ownerUserId","in":"query","required":false},{"name":"effectiveOn","in":"query","required":false},{"name":"expiringWithinDays","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWaiverTemplateMaster": {"method":"GET","path":"/waiver-template-master","contract":"marketing-crm","summary":"Waiver Template Library & Master Setup","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"waiverType","in":"query","required":false},{"name":"brandId","in":"query","required":false},{"name":"isMasterTemplate","in":"query","required":false},{"name":"q","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWaiverTriggerEligibility": {"method":"GET","path":"/waiver-trigger-eligibility","contract":"marketing-crm","summary":"Waiver Trigger, Eligibility & Completion Rules","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"formId","in":"query","required":false},{"name":"triggerPoint","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setDigitalWaiverForm": {"method":"PUT","path":"/digital-waiver-form","contract":"marketing-crm","summary":"Save the layout of a draft waiver version","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DigitalWaiverFormBuilderInput","responds":"DigitalWaiverFormBuilderView"},
"setLocalizationBrandingCustomer": {"method":"PUT","path":"/localization-branding-customer","contract":"marketing-crm","summary":"Set a waiver version's languages, branding and channels","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LocalizationBrandingCustomerExperienceConfigurationInput","responds":"LocalizationBrandingCustomerExperienceConfigurationView"},
"setSignatorySignatureGuardian": {"method":"PUT","path":"/signatory-signature-guardian","contract":"marketing-crm","summary":"Set who must sign a draft waiver version, and how","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SignatorySignatureGuardianRuleConfigurationInput","responds":"SignatorySignatureGuardianRuleConfigurationView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"DigitalWaiverFormBuilderInput": {"description":"The request body of `setDigitalWaiverForm`, the layout record itself; read-only properties are ignored.","allOf":[{"$ref":"#/components/schemas/DigitalWaiverFormBuilderView"}]},
"DigitalWaiverFormBuilderView": {"type":"object","x-ticvai-persistence":"marketing.waiver_form_layout","description":"The layout of one waiver version (pack 11.1.3), keyed on `formId` + `formVersion`. Immutable once the version is published, like the version itself.","required":["formId","formVersion","sections"],"properties":{"formId":{"type":"string","format":"uuid"},"formVersion":{"type":"integer","minimum":1},"sections":{"type":"array","minItems":1,"items":{"type":"object","required":["sectionKey","kind","blocks"],"properties":{"sectionKey":{"type":"string","maxLength":60},"kind":{"type":"string","enum":["header","participantInformation","waiverTerms","safetyAcknowledgements","questions","consent","signature","custom"]},"title":{"$ref":"#/components/schemas/LocalisedText"},"numbered":{"type":"boolean","default":false},"mandatoryReading":{"type":"boolean","default":false,"description":"The signatory must tick \"I have read and understood this section\" before continuing."},"acknowledgementText":{"$ref":"#/components/schemas/LocalisedText"},"showWhen":{"type":"object","nullable":true,"description":"Shown only when the condition holds, e.g. `isMinor` equals `true` shows the guardian section.","required":["subject","operator"],"properties":{"subject":{"type":"string","maxLength":60,"description":"A field key of this version, or `isMinor` (resolved from the waiver's guardian threshold)."},"operator":{"type":"string","enum":["equals","notEquals","in","lessThan","greaterThan","isAnswered"]},"value":{"type":"string","maxLength":200,"nullable":true}}},"blocks":{"type":"array","items":{"type":"object","required":["blockKey","kind"],"properties":{"blockKey":{"type":"string","maxLength":60},"kind":{"type":"string","enum":["heading","paragraph","legalText","instructions","imageLogo","divider","informationBox","checkbox","acknowledgement","question","signature","initials","date","customerDetails","guardianDetails"]},"content":{"$ref":"#/components/schemas/LocalisedText"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"The image for an `imageLogo` block."},"fieldKey":{"type":"string","maxLength":60,"nullable":true,"description":"The `FormField.key` an input block collects; required for input kinds."},"mandatoryNotice":{"type":"boolean","default":false,"description":"Rendered as a notice that cannot be collapsed."}}}}}}},"status":{"type":"string","readOnly":true,"enum":["draft","published","superseded","retired"],"description":"`FormDefinition.status` of this version."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"DynamicFieldsQuestionsConditionalLogicView": {"type":"object","x-ticvai-persistence":"marketing.form_definition_field + marketing.waiver_field_rule","description":"One field of a waiver version (pack 11.1.4). `fieldType` is the builder's type; the stored `FormField.type` follows from it (shortText text, longText and address longText, yesNo and checkbox boolean, singleSelect and dropdown select, multiSelect multiSelect, mobile phone, the lookups text holding the record id, signature and initials signature).","required":["formId","formVersion","key","label","fieldType","requirement"],"properties":{"formId":{"type":"string","format":"uuid"},"formVersion":{"type":"integer","minimum":1},"key":{"type":"string","maxLength":60,"pattern":"^[a-zA-Z][a-zA-Z0-9_]*$"},"label":{"$ref":"#/components/schemas/LocalisedText"},"helpText":{"$ref":"#/components/schemas/LocalisedText"},"fieldType":{"type":"string","enum":["shortText","longText","number","date","yesNo","checkbox","singleSelect","multiSelect","dropdown","email","mobile","address","customerLookup","participantLookup","signature","initials"]},"standardField":{"type":"string","nullable":true,"enum":["participantName","dateOfBirth","customerId","bookingReference","ticketNumber","guardianName","guardianRelationship","emergencyContact"],"description":"Set when the field is one of the reusable standard fields."},"requirement":{"type":"string","enum":["required","optional","conditional","readOnly","autoPopulated"],"description":"`conditional` needs `conditions`; `autoPopulated` and `readOnly` need `mapsTo`."},"options":{"type":"array","items":{"type":"object","required":["value"],"properties":{"value":{"type":"string","maxLength":100},"label":{"$ref":"#/components/schemas/LocalisedText"}}},"description":"The allowed values of a select, dropdown or multi-select field."},"validation":{"type":"object","nullable":true,"properties":{"minimum":{"type":"number","nullable":true},"maximum":{"type":"number","nullable":true},"dateFrom":{"type":"string","format":"date","nullable":true},"dateTo":{"type":"string","format":"date","nullable":true},"pattern":{"type":"string","maxLength":200,"nullable":true,"description":"The required format, as a regular expression."},"maxLength":{"type":"integer","minimum":1,"nullable":true,"description":"The character limit."}}},"conditions":{"type":"array","description":"All must hold (AND). For `conditional` fields they decide whether the field is shown and required.","items":{"type":"object","required":["subject","operator"],"properties":{"subject":{"type":"string","maxLength":60,"description":"Another field's key, or `isMinor`."},"operator":{"type":"string","enum":["equals","notEquals","in","lessThan","greaterThan","isAnswered"]},"value":{"type":"string","maxLength":200,"nullable":true}}}},"mapsTo":{"type":"string","nullable":true,"enum":["guestName","guestDateOfBirth","guestEmail","guestMobile","guestAddress","guestId","ticketHolderName","orderReference","ticketNumber"],"description":"The existing TICVAI record the field reads from, where the caller may read it."},"isPersonalData":{"type":"boolean","default":false},"sortOrder":{"type":"integer","minimum":0,"default":0},"deleted":{"type":"boolean","writeOnly":true,"default":false,"description":"True removes the field from the draft version."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"FormDefinition": {"type":"object","x-ticvai-persistence":"marketing.form_definition + marketing.form_definition_field","description":"CF-129, CL-04. **A waiver, a survey and a data-capture form are one mechanism.**\nA waiver is this form with a signature. A survey is this form with a scale. A demographic capture is this form at the point of sale. They were raised as three separate gaps and share every part: field configuration, conditional display, versioning, an acceptance record and a stored artefact.\n**Three implementations would drift on the version rule first.** A waiver signed against version 3 must stay bound to version 3, and that is the same requirement a survey has when question wording changes mid-campaign — **an NPS score means nothing if you cannot say which question produced it.**\n","required":["id","name","kind","version","status"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["waiver","survey","dataCapture","consentForm","incidentReport","registration"]},"consentPurposes":{"type":"array","description":"**What a `consentForm` consents to** (Chinmay, 2 October, batch 4; follows BO-188: biometric capture needs consent on the venue's own form; CHG-CSA-026). A guardian-signed form for a minor carries the guardian fields of the waiver builder (workbook Q237: guardian consent, configurable per country). Empty for any other kind.","items":{"type":"string","enum":["facePass","faceTag","marketing","photography","waiver"]}},"version":{"readOnly":true,"type":"integer","description":"**Set by the server** — 1 on `createForm`, the next number on every change. **Immutable once anything is submitted against it.** A change creates a new version, and the old one stays readable forever — 2.15.13 requires the exact accepted version retained, which is legal evidence rather than a nicety.\n"},"fields":{"type":"array","items":{"$ref":"#/components/schemas/FormField"}},"requiresSignature":{"type":"boolean","default":false,"description":"**What makes it a waiver.** And 2.15.9 makes ticket issuance conditional on one, which puts this in the purchase path rather than beside it.\n"},"signatureKind":{"type":"string","enum":["drawn","typed","checkbox","none"],"default":"none"},"scoreScale":{"type":"string","nullable":true,"enum":["nps","csat","ces","likert5","likert7","stars"],"description":"**What makes it a survey.** Named rather than free-form because a score whose scale is unknown cannot be compared to last quarter's.\n"},"appliesToProductIds":{"type":"array","items":{"type":"string","format":"uuid"}},"validForMonths":{"type":"integer","nullable":true,"description":"**How long an acceptance lasts.** A waiver signed last summer may or may not still hold, and 2.15.x asks for a returning participant not to sign again — which only works if the expiry is stated.\n"},"minimumAge":{"type":"integer","nullable":true},"requiresGuardianForMinors":{"type":"boolean","default":true,"description":"**A minor cannot waive their own rights.** A guardian signs, and the record has to name them — an unsigned or self-signed minor waiver is worth nothing at the moment it matters.\n"},"status":{"readOnly":true,"type":"string","enum":["draft","published","superseded","retired"]},"legalReviewedBy":{"type":"string","nullable":true},"legalReviewedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"FormField": {"type":"object","description":"One field. **Conditional display is the shared requirement** — a survey branching on an answer and a waiver revealing a medical question on a yes are the same mechanism.\n","required":["key","label","type"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"labelLocalised":{"type":"object","additionalProperties":{"type":"string"}},"type":{"type":"string","enum":["text","longText","number","date","select","multiSelect","boolean","scale","signature","file","phone","email"]},"options":{"type":"array","items":{"type":"string"}},"isRequired":{"type":"boolean","default":false},"isPersonalData":{"type":"boolean","default":false,"description":"**Marked at the field, because retention is decided at the field.** A survey answer and a medical condition on the same form have different lifetimes, and a form-level flag makes the whole thing as sensitive as its most sensitive field.\n"},"consentPurposeId":{"type":"string","format":"uuid","nullable":true},"showWhen":{"type":"object","nullable":true,"properties":{"field":{"type":"string"},"equals":{"type":"string"}}}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"LocalizationBrandingCustomerExperienceConfigurationInput": {"description":"The request body of `setLocalizationBrandingCustomer`, the record itself; read-only properties are ignored.","allOf":[{"$ref":"#/components/schemas/LocalizationBrandingCustomerExperienceConfigurationView"}]},
"LocalizationBrandingCustomerExperienceConfigurationView": {"type":"object","x-ticvai-persistence":"marketing.waiver_localisation","description":"Languages, branding and channels of one waiver version (pack 11.1.9), keyed on `formId` + `formVersion`.","required":["formId","formVersion","sourceLanguage","languages"],"properties":{"formId":{"type":"string","format":"uuid"},"formVersion":{"type":"integer","minimum":1},"sourceLanguage":{"type":"string","maxLength":10,"description":"The language the legal text is written and reviewed in."},"languages":{"type":"array","minItems":1,"description":"Every language the version is offered in, the source language included. Arabic renders right to left.","items":{"type":"object","required":["language","required","translationStatus","approvalStatus"],"properties":{"language":{"type":"string","maxLength":10},"required":{"type":"boolean","description":"Publication waits for this language's approval."},"translationStatus":{"type":"string","enum":["notStarted","aiDrafted","inTranslation","inReview","complete"]},"translatorUserId":{"type":"string","format":"uuid","nullable":true},"reviewerUserId":{"type":"string","format":"uuid","nullable":true},"approvalStatus":{"type":"string","enum":["pending","approved","rejected"]},"lastUpdated":{"type":"string","format":"date-time","readOnly":true}}}},"branding":{"type":"object","properties":{"brandLogoAssetId":{"type":"string","format":"uuid","nullable":true},"venueLogoAssetId":{"type":"string","format":"uuid","nullable":true},"themeId":{"type":"string","nullable":true,"description":"The white-label theme it takes colours and typography from."},"header":{"$ref":"#/components/schemas/LocalisedText"},"footer":{"$ref":"#/components/schemas/LocalisedText"},"customerInstructions":{"$ref":"#/components/schemas/LocalisedText"},"confirmationMessage":{"$ref":"#/components/schemas/LocalisedText"},"supportEmail":{"type":"string","format":"email","nullable":true},"supportPhone":{"type":"string","maxLength":30,"nullable":true}}},"channels":{"type":"array","items":{"type":"string","enum":["b2cWeb","mobileApp","emailLink","qrLink","kiosk","posFrontDesk","groupPortal"]},"description":"Where the waiver is offered; every channel renders the same version and rules."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProductEventExperienceAssociationView": {"type":"object","x-ticvai-persistence":"marketing.waiver_association","description":"One waiver attached to one target (pack 11.1.6). The waiver's in-force version applies; the version a guest signed is on their signature.","required":["formId","targetType","requirement","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"formId":{"type":"string","format":"uuid","description":"The waiver (`FormDefinition.id`)."},"waiverName":{"type":"string","readOnly":true},"targetType":{"type":"string","enum":["global","brand","venue","product","ticketType","event","performance","attraction","activity","membership","camp","rental","resource","package","addOn"]},"targetId":{"type":"string","format":"uuid","nullable":true,"description":"The catalogue, event, venue or brand id; null only for `global`."},"targetName":{"type":"string","readOnly":true},"requirement":{"type":"string","enum":["mandatory","optional","conditional","informational"]},"conditionRuleId":{"type":"string","format":"uuid","nullable":true,"description":"The eligibility rule (`setWaiverTriggerRule`) that makes a conditional association apply."},"sequence":{"type":"integer","minimum":1,"default":1,"description":"The order the target's waivers are presented in."},"overridesAssociationId":{"type":"string","format":"uuid","nullable":true,"description":"The inherited association this one replaces for this target."},"inheritedFrom":{"type":"object","nullable":true,"readOnly":true,"properties":{"associationId":{"type":"string","format":"uuid"},"targetType":{"type":"string"},"targetId":{"type":"string","format":"uuid","nullable":true}}},"status":{"type":"string","enum":["active","removed"],"default":"active"},"impact":{"type":"object","nullable":true,"readOnly":true,"description":"What depends on this association now (pack Dependency Impact).","properties":{"products":{"type":"integer","minimum":0},"futureBookings":{"type":"integer","minimum":0},"tickets":{"type":"integer","minimum":0},"participants":{"type":"integer","minimum":0},"events":{"type":"integer","minimum":0}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"SignatorySignatureGuardianRuleConfigurationInput": {"description":"The request body of `setSignatorySignatureGuardian`, the rule record itself; read-only properties are ignored.","allOf":[{"$ref":"#/components/schemas/SignatorySignatureGuardianRuleConfigurationView"}]},
"SignatorySignatureGuardianRuleConfigurationView": {"type":"object","x-ticvai-persistence":"marketing.waiver_signatory_rule","description":"The signatory rules of one waiver version (pack 11.1.5), keyed on `formId` + `formVersion`; immutable once the version is published.","required":["formId","formVersion","primarySignatory","acceptanceMethod","requiresGuardianForMinors"],"properties":{"formId":{"type":"string","format":"uuid"},"formVersion":{"type":"integer","minimum":1},"primarySignatory":{"type":"string","enum":["ticketHolder","purchaser","participant","parent","legalGuardian","groupLeader","corporateRepresentative","member","rentalCustomer","otherAuthorizedSignatory"]},"allowedSignatories":{"type":"array","items":{"type":"string","enum":["ticketHolder","purchaser","participant","parent","legalGuardian","groupLeader","corporateRepresentative","member","rentalCustomer","otherAuthorizedSignatory"]},"description":"Who else may sign in the primary signatory's place."},"coSignature":{"type":"string","nullable":true,"enum":["participantAndGuardian","customerAndAuthorizedRepresentative"],"description":"Set when two people must both sign."},"signatureRequired":{"type":"boolean","default":true},"initialsRequired":{"type":"boolean","default":false},"acceptanceMethod":{"type":"string","enum":["drawnSignature","typedName","checkbox"],"description":"Kept equal to `FormDefinition.signatureKind` (drawn, typed, checkbox)."},"captureRelationship":{"type":"boolean","default":true,"description":"Whoever signs for someone else states their relationship."},"identityVerification":{"type":"string","enum":["none","signedInAccount","oneTimeCode","idDocumentCheck"],"default":"none"},"requiresGuardianForMinors":{"type":"boolean","description":"Written to `FormDefinition.requiresGuardianForMinors`."},"guardianThresholdAge":{"type":"integer","minimum":1,"maximum":25,"nullable":true,"description":"A participant under this age needs a guardian. Written to `FormDefinition.minimumAge`. No default."},"guardianThresholdByCountry":{"type":"array","items":{"type":"object","required":["country","age"],"properties":{"country":{"type":"string","pattern":"^[A-Z]{2}$"},"age":{"type":"integer","minimum":1,"maximum":25}}},"description":"Per-country thresholds that override `guardianThresholdAge`."},"guardianSignsForEachMinor":{"type":"boolean","default":true,"description":"One guardian signature per minor, never one for the family."},"groupSigningModes":{"type":"array","items":{"type":"string","enum":["eachParticipantIndividually","guardianForEachMinor","groupLeaderForGroup","organisationRepresentativeDeclaration"]},"description":"The modes a group booking may use. Empty means each participant signs individually."},"recordedEvidence":{"type":"array","readOnly":true,"items":{"type":"string","enum":["timestamp","waiverVersion","signatory","authenticationMethod","transactionReference","customerReference","documentHash","deviceInfo","consentEvidence"]},"description":"Always all of them; listed so the reviewer sees what is kept."},"legalApprovedBy":{"type":"string","nullable":true,"readOnly":true,"description":"`FormDefinition.legalReviewedBy`, set at the legal/compliance step of `approveWaiverTesting`."},"legalApprovedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"VersioningEffectiveDatesLegalChangeControlView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.form_definition, marketing.waiver_version_control (new), marketing.form_submission and marketing.waiver_signature","description":"One version of one waiver and its change control (pack 11.1.8).","required":["formId","versionNumber","status","createdAt"],"properties":{"formId":{"type":"string","format":"uuid"},"waiverName":{"type":"string"},"versionNumber":{"type":"integer","minimum":1},"status":{"type":"string","enum":["draft","published","superseded","retired"],"description":"`FormDefinition.status` (states/form-definition.yaml)."},"lifecycleStatus":{"type":"string","enum":["draft","review","pendingApproval","approved","scheduled","published","suspended","expired","archived"]},"createdByUserId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"changeReason":{"type":"string","maxLength":1000,"nullable":true},"legalReviewer":{"type":"string","nullable":true,"description":"`FormDefinition.legalReviewedBy`."},"legalReviewedAt":{"type":"string","format":"date-time","nullable":true},"approvedByUserId":{"type":"string","format":"uuid","nullable":true},"approvedAt":{"type":"string","format":"date-time","nullable":true},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"resignRule":{"type":"string","enum":["noResign","resignAtNextBooking","resignBeforeNextVisit"],"description":"Whether people who signed an earlier version must sign this one."},"suspended":{"type":"boolean","default":false},"suspensionReason":{"type":"string","maxLength":500,"nullable":true},"signatureCount":{"type":"integer","minimum":0,"description":"Signatures taken against this exact version."},"comparison":{"type":"object","nullable":true,"description":"Present when `compareWith` is given.","properties":{"comparedWithVersion":{"type":"integer","minimum":1},"addedText":{"type":"array","items":{"type":"object","properties":{"blockKey":{"type":"string"},"language":{"type":"string"},"text":{"type":"string"}}}},"removedText":{"type":"array","items":{"type":"object","properties":{"blockKey":{"type":"string"},"language":{"type":"string"},"text":{"type":"string"}}}},"changedQuestions":{"type":"array","items":{"type":"string"},"description":"Field keys added, removed or changed."},"changedSignatoryRules":{"type":"array","items":{"type":"string"},"description":"Names of the signatory-rule properties that differ."},"changedAssociations":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Associations added, removed or changed between the two versions' publication."}}}}},
"WaiverApprovalTestingPublicationWorkspaceInput": {"type":"object","x-ticvai-persistence":"none — request; appended to marketing.waiver_version_control","description":"One governance action on a waiver version (pack 11.1.10).","required":["formId","formVersion","action"],"properties":{"formId":{"type":"string","format":"uuid"},"formVersion":{"type":"integer","minimum":1},"action":{"type":"string","enum":["submitForReview","completeOperationsReview","completeLegalReview","approve","reject","publish","suspend","reinstate","archive"]},"comment":{"type":"string","maxLength":2000,"nullable":true,"description":"Required for `reject` and `suspend`."},"changeReason":{"type":"string","maxLength":1000,"nullable":true,"description":"Required for `submitForReview`."},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"resignRule":{"type":"string","enum":["noResign","resignAtNextBooking","resignBeforeNextVisit"],"description":"Required for `submitForReview` of a version after the first."},"publication":{"type":"object","nullable":true,"description":"Required for `publish`.","required":["mode"],"properties":{"mode":{"type":"string","enum":["publishNow","schedule","selectedVenues","selectedProducts","controlledRollout"]},"publishAt":{"type":"string","format":"date-time","nullable":true,"description":"Required for `schedule`."},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"productIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}}},
"WaiverApprovalTestingPublicationWorkspaceView": {"type":"object","x-ticvai-persistence":"marketing.waiver_version_control","description":"The governance record of one waiver version with its checklist (pack 11.1.10), keyed on `formId` + `formVersion`.","required":["formId","formVersion","lifecycleStatus","checklist"],"properties":{"formId":{"type":"string","format":"uuid"},"formVersion":{"type":"integer","minimum":1},"lifecycleStatus":{"type":"string","enum":["draft","review","pendingApproval","approved","scheduled","published","suspended","expired","archived"]},"checklist":{"type":"array","items":{"type":"object","required":["check","passed","severity"],"properties":{"check":{"type":"string","enum":["masterRecordComplete","requiredLegalTextPresent","requiredFieldsConfigured","conditionalRulesValid","signatureRulesConfigured","guardianThresholdSet","guardianSignatureFieldPresent","productsEventsAssigned","completionRulesConfigured","requiredTranslationsApproved","effectiveDatesValid"]},"passed":{"type":"boolean"},"severity":{"type":"string","enum":["critical","warning"]},"message":{"type":"string"}}}},"simulation":{"type":"object","nullable":true,"description":"Present when scenario parameters were given.","properties":{"requiredWaivers":{"type":"array","items":{"type":"object","properties":{"formId":{"type":"string","format":"uuid"},"waiverName":{"type":"string"},"version":{"type":"integer"},"requirement":{"type":"string","enum":["mandatory","optional","conditional","informational"]},"applies":{"type":"boolean"},"signatories":{"type":"array","items":{"type":"string"},"description":"e.g. participant, legalGuardian."}}}},"blockedAt":{"type":"array","items":{"type":"string","enum":["ticketDownload","ticketActivation","checkIn","access"]},"description":"What a missing signature would block, when `missingSignature` was set."}}},"aiFindings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["info","warning"]},"message":{"type":"string"}}}},"changeReason":{"type":"string","nullable":true},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"resignRule":{"type":"string","nullable":true,"enum":["noResign","resignAtNextBooking","resignBeforeNextVisit"]},"publication":{"type":"object","nullable":true,"properties":{"mode":{"type":"string","enum":["publishNow","schedule","selectedVenues","selectedProducts","controlledRollout"]},"publishAt":{"type":"string","format":"date-time","nullable":true},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"productIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},"suspended":{"type":"boolean","default":false},"suspensionReason":{"type":"string","nullable":true},"audit":{"type":"object","description":"Who moved it through each stage, and when (pack Audit).","properties":{"submittedByUserId":{"type":"string","format":"uuid","nullable":true},"submittedAt":{"type":"string","format":"date-time","nullable":true},"operationsReviewedByUserId":{"type":"string","format":"uuid","nullable":true},"operationsReviewedAt":{"type":"string","format":"date-time","nullable":true},"legalReviewedByUserId":{"type":"string","format":"uuid","nullable":true},"legalReviewedAt":{"type":"string","format":"date-time","nullable":true},"approvedByUserId":{"type":"string","format":"uuid","nullable":true},"approvedAt":{"type":"string","format":"date-time","nullable":true},"publishedByUserId":{"type":"string","format":"uuid","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true}}},"history":{"type":"array","description":"Every action with its comment, oldest first.","items":{"type":"object","properties":{"action":{"type":"string"},"byUserId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"comment":{"type":"string","nullable":true}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WaiverConsentCommandCenterView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.form_definition (kind waiver), marketing.waiver_master (new), marketing.waiver_version_control (new) and marketing.waiver_association (new)","description":"One row of the waiver directory (pack 11.1.1), a waiver at its latest version. `status` is the pack's lifecycle, derived from `FormDefinition.status` and the version-control record (draft, review, pendingApproval, approved and scheduled are a `draft` form version at that approval stage; suspended is a published version under an emergency suspension; expired is a version past `effectiveTo`; archived is `retired`).","required":["waiverId","waiverName","type","version","status","lastModified"],"properties":{"waiverId":{"type":"string","format":"uuid","description":"The `FormDefinition.id`."},"waiverName":{"type":"string"},"type":{"type":"string","enum":["liabilityWaiver","parentGuardianConsent","participationConsent","medicalDeclaration","safetyAcknowledgement","mediaConsent","rentalAgreement","termsAcceptance","membershipDeclaration","customForm"]},"version":{"type":"integer","minimum":1,"description":"The latest version, whatever its state."},"publishedVersion":{"type":"integer","minimum":1,"nullable":true,"description":"The version guests currently sign, when that is not the latest."},"language":{"type":"string","maxLength":10,"description":"The default language from the master record."},"languages":{"type":"array","items":{"type":"string","maxLength":10},"description":"Every language the version is published in."},"associatedProducts":{"type":"integer","minimum":0,"description":"Products with an active association (the pack's usage indicator)."},"associatedVenues":{"type":"integer","minimum":0},"signatoryType":{"type":"string","nullable":true,"enum":["ticketHolder","purchaser","participant","parent","legalGuardian","groupLeader","corporateRepresentative","member","rentalCustomer","otherAuthorizedSignatory"],"description":"The primary signatory from `setSignatorySignatureGuardian`."},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["draft","review","pendingApproval","approved","scheduled","published","suspended","expired","archived"]},"ownerUserId":{"type":"string","format":"uuid","nullable":true},"owner":{"type":"string","nullable":true,"description":"The owner's display name."},"brandId":{"type":"string","format":"uuid","nullable":true},"lastModified":{"type":"string","format":"date-time"}}},
"WaiverTemplateLibraryMasterSetupView": {"type":"object","x-ticvai-persistence":"marketing.waiver_master","description":"The master record of one waiver (pack 11.1.2), one per `FormDefinition` of kind `waiver`. The name, wording, fields and versions live on the form; this holds classification, ownership and business scope.","required":["waiverId","waiverType","ownerUserId","businessOwnerUserId","defaultLanguage","templateSource"],"properties":{"waiverId":{"type":"string","format":"uuid","description":"The `FormDefinition.id`; the natural key."},"waiverName":{"type":"string","readOnly":true,"description":"`FormDefinition.name`, shown here, written by `createForm`."},"internalDescription":{"type":"string","maxLength":2000,"nullable":true},"waiverType":{"type":"string","enum":["liabilityWaiver","parentGuardianConsent","participationConsent","medicalDeclaration","safetyAcknowledgement","mediaConsent","rentalAgreement","termsAcceptance","membershipDeclaration","customForm"]},"customTypeLabel":{"type":"string","maxLength":80,"nullable":true,"description":"The tenant's own classification name; required when `waiverType` is `customForm`."},"ownerUserId":{"type":"string","format":"uuid"},"department":{"type":"string","maxLength":100,"nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"Null for a corporate waiver every brand may use."},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"The finance legal entity the waiver is given in favour of."},"defaultLanguage":{"type":"string","maxLength":10},"applicableCountries":{"type":"array","items":{"type":"string","pattern":"^[A-Z]{2}$"},"description":"ISO 3166-1 alpha-2. Empty means the waiver is not yet scoped, which blocks publication."},"applicableJurisdiction":{"type":"string","maxLength":100,"nullable":true,"description":"A sub-national jurisdiction where the law differs within a country."},"status":{"type":"string","readOnly":true,"enum":["draft","review","pendingApproval","approved","scheduled","published","suspended","expired","archived"],"description":"The lifecycle status of the latest version (see `listWaiverConsent`)."},"templateSource":{"type":"string","enum":["createNew","duplicateExisting","masterTemplate","corporateTemplate"],"default":"createNew"},"sourceWaiverId":{"type":"string","format":"uuid","nullable":true,"description":"The waiver it was duplicated or created from; required unless `createNew`."},"sourceVersion":{"type":"integer","minimum":1,"nullable":true},"isMasterTemplate":{"type":"boolean","default":false,"description":"Offered in the reusable library. A corporate template is a master template with no `brandId`."},"businessOwnerUserId":{"type":"string","format":"uuid"},"legalReviewerUserId":{"type":"string","format":"uuid","nullable":true},"complianceOwnerUserId":{"type":"string","format":"uuid","nullable":true},"operationalOwnerUserId":{"type":"string","format":"uuid","nullable":true},"legalReviewRequired":{"type":"boolean","default":true,"description":"Whether the approval chain includes the legal/compliance step. On unless the tenant turns it off."},"usage":{"type":"object","readOnly":true,"description":"Where the waiver is used now (pack Usage Indicator, Template Dependency).","properties":{"products":{"type":"integer","minimum":0},"venues":{"type":"integer","minimum":0},"futureBookings":{"type":"integer","minimum":0}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WaiverTriggerEligibilityCompletionRulesView": {"type":"object","x-ticvai-persistence":"marketing.waiver_trigger_rule","description":"One trigger, eligibility and completion rule of a waiver (pack 11.1.7).","required":["formId","name","triggerPoint","completionDeadline","status"],"properties":{"id":{"type":"string","format":"uuid","description":"Absent on create."},"formId":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":150},"triggerPoint":{"type":"string","enum":["duringCheckout","afterPurchase","beforeTicketIssuance","beforeTicketDownload","beforeEvent","beforeCheckIn","beforeAccess","beforeEquipmentCollection","beforeMembershipActivation","beforeActivityStart"]},"eligibility":{"type":"array","description":"All must hold (AND). Empty means every participant the association reaches.","items":{"type":"object","required":["attribute","operator","values"],"properties":{"attribute":{"type":"string","enum":["age","isMinor","product","event","venue","activity","customerType","membership","country","channel","participantType","bookingType"]},"operator":{"type":"string","enum":["equals","notEquals","in","notIn","lessThan","greaterThan"]},"values":{"type":"array","minItems":1,"items":{"type":"string","maxLength":100}}}}},"completionDeadline":{"type":"object","required":["kind"],"properties":{"kind":{"type":"string","enum":["immediately","beforeTicketRelease","hoursBeforeEvent","daysBeforeVisit","beforeArrival","beforeAccess"]},"offset":{"type":"integer","minimum":1,"nullable":true,"description":"Hours for `hoursBeforeEvent`, days for `daysBeforeVisit`."}}},"enforcement":{"type":"array","items":{"type":"string","enum":["blockTicketDownload","blockTicketActivation","blockCheckIn","blockAccess"]},"description":"What an incomplete waiver blocks. Empty means warn only."},"allowStaffOverride":{"type":"boolean","default":false,"description":"An authorised operator may admit the participant anyway; the override is recorded."},"reminders":{"type":"array","items":{"type":"object","required":["offsetHours","channels"],"properties":{"offsetHours":{"type":"integer","minimum":1,"description":"Hours before the deadline, e.g. 168, 72, 24."},"channels":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/MessageChannel"}}}}},"status":{"type":"string","enum":["active","inactive"],"default":"active"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}}
}
```
