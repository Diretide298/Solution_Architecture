# WS41 — Privacy  Consent   Preference Management board 1

**10 screens · 20 operations · 26 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW`. A control nobody can use must say so,
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
| `CMS-021` | Privacy & Consent Configuration Command Center | D | 13 | 0 | 6 | 0 | 1 | 4 | — | notStarted (generated) |
| `CMS-022` | Data Processing Purpose & Lawful Basis Registry | D | 21 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `CMS-023` | Consent Purpose & Consent Type Builder | D | 17 | 0 | 5 | 1 | 0 | 4 | — | notStarted (generated) |
| `CMS-024` | Communication Preference & Marketing Permission Configuration | D | 17 | 0 | 5 | 0 | 0 | 5 | — | notStarted (generated) |
| `CMS-025` | Cookie, Tracking & Digital Technology Registry | A | 44 | 67 | 6 | 3 | 1 | 4 | — | notStarted (generated) |
| `CMS-026` | Cookie Banner & Preference Center Designer | A | 33 | 4 | 5 | 1 | 2 | 4 | configures | notStarted (generated) |
| `CMS-027` | Consent Capture Point & Customer Journey Configuration | D | 28 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `CMS-028` | Privacy Notice, Policy & Terms Version Management | D | 9 | 0 | 6 | 0 | 0 | 4 | — | notStarted (generated) |
| `CMS-029` | Minor, Guardian & Age-Based Privacy Configuration | D | 8 | 0 | 5 | 0 | 0 | 4 | — | notStarted (generated) |
| `CMS-030` | Privacy Configuration Testing, Approval & Publication | D | 39 | 0 | 5 | 0 | 0 | 6 | — | notStarted (generated) |

## Thin screens in this batch

**CMS-022, CMS-028 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `CMS-021` Privacy & Consent Configuration Command Center

**Provide administrators with one central dashboard for configuring and governing TICVAI's privacy framework across tenants, brands, venues and customer channels.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-021 |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Display configuration indicators such as; Configuration Type Scope Status) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/privacy-consent-configuration-command-center-cms-021` |

**Known gaps.** **The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Create Consent Purpose, Create Policy, Configure Preferences, Configure Cookies, Configure Capture Point … Removed 2 October 2026 (CHG-WIR-005): listCustomerPrivacyConsent is one guest's privacy 360, which is CMS-032's; a configuration command centre shows counts (design-notes correction …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The privacy configuration hub: active consent purposes, policies, communication preference types, cookie categories, capture points, languages, pending approvals, scheduled changes and configuration warnings, with the latest changes. Every detail screen of the privacy configuration board opens from here and returns here.

**Fixed on main** (the package already carries these; draw what it says): The KPIs are drawn as select fields (Active Consent Purposes, Pending Policy Approvals) and listCustomerPrivacyConsent (one guest's privacy … (CHG-WIR-005).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search privacy consent | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, brand, country, venue, channel, consent type and 4 more — which are present is a decision the pack already made. | — |
| Active Consent Purposes | select field | — | — | — | — | — | — |
| Active Privacy Policies | select field | — | — | — | — | — | — |
| Communication Preference Types | select field | — | — | — | — | — | — |
| Cookie Categories | select field | — | — | — | — | — | — |
| Active Consent Capture Points | text field | — | — | — | — | — | — |
| Supported Languages | select field | — | — | — | — | — | — |
| Pending Policy Approvals | select field | — | — | — | — | — | — |
| Scheduled Policy Changes | select field | — | — | — | — | — | — |
| Configuration Warnings | select field | — | — | — | — | — | — |
| Consent Configurations Requiring Review | text field | — | — | — | — | — | — |
| n From | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Brand | picker: choose a brand | — | — | `listPrivacyConsent` ?brandId |
| Country | text field | — | pattern `^[A-Z]{2}$` | `listPrivacyConsent` ?country |
| Channel | select | — | Guest app · Website · Kiosk · POS · Call centre · Import · Agent recorded · Cookie banner · Checkout | `listPrivacyConsent` ?channel |
| Consent purpose | select | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | `listPrivacyConsent` ?consentPurpose |
| Policy | picker: choose a policy | — | — | `listPrivacyConsent` ?policyId |
| Language | text field | — | max length 10 | `listPrivacyConsent` ?language |
| Status | select | — | Draft · Review · Approved · Scheduled · Published · Retired | `listPrivacyConsent` ?status |
| Effective from | date and time picker | — | — | `listPrivacyConsent` ?effectiveFrom |
| Effective to | date and time picker | — | — | `listPrivacyConsent` ?effectiveTo |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create Consent Purpose (primary button) | navigation or local | — | — | — | — |
| Create Policy (secondary button) | navigation or local | — | — | — | — |
| Configure Preferences (secondary button) | navigation or local | — | — | — | — |
| Configure Cookies (secondary button) | navigation or local | — | — | — | — |
| Configure Capture Point (secondary button) | navigation or local | — | — | — | — |
| Test Configuration (secondary button) | navigation or local | — | — | — | — |
| Submit for Approval (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Configuration warnings**: Missing Arabic text, a purpose with no capture point, a capture point with no notice, a policy pending approval; each links to the fix. *(source: contracts/satellite/marketing-crm.yaml#listPrivacyConsent; DI-653)*

**Data it reads**: `listPrivacyConsent` (onLoad, Privacy & Consent Configuration Command Center)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-022` Data Processing Purpose & Lawful Basis Registry: *Works in Data Processing Purpose & Lawful Basis Registry*; calls `listPrivacyConsent`
- → `CMS-023` Consent Purpose & Consent Type Builder: *Works in Consent Purpose & Consent Type Builder*; calls `listPrivacyConsent`
- → `CMS-024` Communication Preference & Marketing Permission Configuration: *Works in Communication Preference & Marketing Permission Configuration*; calls `listPrivacyConsent`
- → `CMS-025` Cookie, Tracking & Digital Technology Registry: *Works in Cookie, Tracking & Digital Technology Registry*; calls `listPrivacyConsent`
- → `CMS-026` Cookie Banner & Preference Center Designer: *Works in Cookie Banner & Preference Center Designer*; calls `listPrivacyConsent`
- → `CMS-027` Consent Capture Point & Customer Journey Configuration: *Works in Consent Capture Point & Customer Journey Configuration*; calls `listPrivacyConsent`
- → `CMS-028` Privacy Notice, Policy & Terms Version Management: *Works in Privacy Notice, Policy & Terms Version Management*; calls `listPrivacyConsent`
- → `CMS-029` Minor, Guardian & Age-Based Privacy Configuration: *Works in Minor, Guardian & Age-Based Privacy Configuration*; calls `listPrivacyConsent`
- → `CMS-030` Privacy Configuration Testing, Approval & Publication: *Works in Privacy Configuration Testing, Approval & Publication*; calls `listPrivacyConsent`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The privacy consent configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the privacy consent untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No privacy consent configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the privacy consent are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  purposes: 6
  policies: 4
  capturePoints: 12
  languages:
  - EN
  - AR
  pendingApprovals: 2
  warnings: 3
```

#### Permissions

- `listPrivacyConsent` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-021` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-021`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 1
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 1: Opens Privacy & Consent Configuration Command Center → Provide administrators with one central dashboard for configuring and governing TICVAI's privacy framework across tenants, brands, venues and customer channels.
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F150 branch at step 1 (expected): when Nothing has been set up on Privacy & Consent Configuration Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F150 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-021?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create Consent Purpose, Create Policy, Configure Preferences, Configure Cookies, Configure Capture Point, Test Configuration, Submit for Approval.
- [ ] Every transition is wired: `CMS-001`, `CMS-022`, `CMS-023`, `CMS-024`, `CMS-025`, `CMS-026`, `CMS-027`, `CMS-028`, `CMS-029`, `CMS-030`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-022` Data Processing Purpose & Lawful Basis Registry

**Create a central registry explaining why customer data is being collected or processed. This becomes the foundation used by consent forms, policies, customer journeys and downstream systems. Ticket Purchase & Fulfillment Customer Account Management Membership Administration Customer Support Transactional Communication Marketing Communication Personalization Analytics Fraud Prevention Security Biometric Processing Location-Based Services Loyalty Customer Research**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-022 |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/data-processing-purpose-lawful-basis-registry-cms-022` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The register of why personal data is processed (ticket purchase and fulfilment, account management, membership, support, transactional and marketing communication, personalisation, analytics, fraud prevention, security, biometrics, location, loyalty), each with its lawful basis, data categories and retention. Consent forms, policies and journeys build on it.

**Fixed on main** (the package already carries these; draw what it says): Read-only; no write for processing purposes. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | segmented control | — | Draft · Active · Retired | `listDataProcessingPurpose` ?status |
| Lawful basis | select | — | Consent · Contractual necessity · Legal obligation · Legitimate interest · Vital interest · Public interest · Other · Unclassified | `listDataProcessingPurpose` ?lawfulBasis |
| Sensitive only | toggle | — | — | `listDataProcessingPurpose` ?sensitiveOnly |

**Form: Save purpose** (modal, opened by *Save purpose*; *Save purpose* calls `setDataProcessingPurpose`, *Cancel* sends nothing)

**Collects what `setDataProcessingPurpose` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Purpose code `purposeCode` | text field | required | — | max length 60 | — | The natural key, e.g. `ticketPurchase`, `marketingCommunication`. | `setDataProcessingPurpose` body |
| Purpose name `purposeName` | text field | required | — | max length 150 | — | — | `setDataProcessingPurpose` body |
| Description `description` | text area | optional | — | max length 2000 | — | — | `setDataProcessingPurpose` body |
| Business owner `businessOwner` | text field | optional | — | max length 150 | — | The accountable team or person. | `setDataProcessingPurpose` body |
| Data controller applicable organization `dataControllerApplicableOrganization` | text field | optional | — | max length 200 | — | The legal entity acting as controller for this purpose. | `setDataProcessingPurpose` body |
| Data categories `dataCategories` | list of values (chips) | optional | — | — | — | e.g. contact details, payment, date of birth, images. | `setDataProcessingPurpose` body |
| Data subject categories `dataSubjectCategories` | multi-select chips | optional | — | Guest · Member · Minor · Guardian · Partner · Employee · Other | — | — | `setDataProcessingPurpose` body |
| Processing activities `processingActivities` | list of values (chips) | optional | — | — | — | — | `setDataProcessingPurpose` body |
| Systems modules `systemsModules` | multi-select chips | optional | — | Core · Ticketing · Access · Fnb · Retail · Inventory · Seating · Membership · Marketing · Resources · Queue · Transport … | — | — | `setDataProcessingPurpose` body |
| Countries jurisdictions `countriesJurisdictions` | list of values (chips) | optional | — | — | — | — | `setDataProcessingPurpose` body |
| Lawful basis `lawfulBasis` | select | required | Unclassified | Consent · Contractual necessity · Legal obligation · Legitimate interest · Vital interest · Public interest · Other · Unclassified | — | Set by the privacy administrator. `unclassified` is flagged, never assumed. | `setDataProcessingPurpose` body |
| Lawful basis note `lawfulBasisNote` | text area | optional | — | max length 500; Required when `lawfulBasis` is `other`. | — | Required when `lawfulBasis` is `other`. | `setDataProcessingPurpose` body |
| Sensitive categories `sensitiveCategories` | multi-select chips | optional | — | Biometrics · Childrens data · Identity documents · Precise location · Health · Other | — | — | `setDataProcessingPurpose` body |
| Consent purposes `consentPurposes` | multi-select chips | optional | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | — | The consent purposes that rely on this processing purpose. | `setDataProcessingPurpose` body |
| Policys `policyIds` | multi-picker: choose policys | optional | — | — | — | Notices and policies that describe it (white-label `listPolicies`). | `setDataProcessingPurpose` body |
| Capture points `capturePointIds` | multi-picker: choose capture points | optional | — | — | — | — | `setDataProcessingPurpose` body |
| Retention policy codes `retentionPolicyCodes` | list of values (chips) | optional | — | — | — | `DataRetentionPolicy.code` values that govern its data. | `setDataProcessingPurpose` body |
| Third party processors `thirdPartyProcessors` | list of values (chips) | optional | — | — | — | — | `setDataProcessingPurpose` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDataProcessingPurpose` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setDataProcessingPurpose` body |
| Status `status` | segmented control | required | Draft | Draft · Active · Retired | — | — | `setDataProcessingPurpose` body |

Errors to draw in the form: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save purpose (secondary button) | `setDataProcessingPurpose` PUT `/data-processing-purpose` | DataProcessingPurposeLawfulBasisRegistryView | DataProcessingPurposeLawfulBasisRegistryView | 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types. | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Purpose row**: Purpose, lawful basis (consent, contract, legal obligation, legitimate interest), data categories, retention, owner; marketing and biometrics show consent as the basis. *(source: contracts/satellite/marketing-crm.yaml#listDataProcessingPurpose)*

**Data it reads**: `listDataProcessingPurpose` (onLoad, Data Processing Purpose & Lawful Basis Registry)

**Where the user goes next**

- → `CMS-021` Privacy & Consent Configuration Command Center: *Returns to the board's landing screen*; calls `listDataProcessingPurpose`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data processing purpose list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data processing purpose untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data processing purpose yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data processing purpose are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- Ticket purchase - contract - name
- contact
- payment - 7 years
- Marketing communication - consent - contact
- preferences - until withdrawn
- Biometric processing - consent - face template - end of pass
```

#### Permissions

- `listDataProcessingPurpose` → `GUEST_VIEW` (read) · staff
- `setDataProcessingPurpose` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-022` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-022`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 1
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 2: Works in Data Processing Purpose & Lawful Basis Registry → Create a central registry explaining why customer data is being collected or processed. This becomes the foundation used by consent forms, policies, customer journeys and downstream systems. Ticket …

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-022?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save purpose.
- [ ] Every transition is wired: `CMS-021`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-023` Consent Purpose & Consent Type Builder

**Configure the actual consent objects that TICVAI may request from customers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-023 |
| Who uses it | venue staff holding `GUEST_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/consent-purpose-consent-type-builder-cms-023` |

**What the spec says about it.** **Consent purposes are captured on the venue's consent forms** (DEC-549): each purpose here is the `consentPurposes` value a consent form built on CMS-043 (BO-747 in Venue Management) collects; there is one form builder, not a second one on this screen (CHG-SGU-014).

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Configure the consent objects guests are asked for: name, processing purpose, consent text (EN and AR), mandatory or optional, explicit method, default state, withdrawal, renewal, expiry, age and guardian rules, channels and countries. The default state of any optional consent is off; adding one never grants it to existing guests.

**Known correction pending (do not draw the wrong version)**

- **Every field is a select (Name, Description, Consent Text).** Why: Texts are typed per language. *(source: screens/P13-white-label-cms.yaml#CMS-023; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Consent ID | select field | — | — | — | — | — | — |
| Name | select field | — | — | — | — | — | — |
| Processing Purpose | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Consent Text | select field | — | — | — | — | — | — |
| Mandatory / Optional | select field | — | — | — | — | — | — |
| Explicit / Other configured consent method | text field | — | — | — | — | — | — |
| Default state | select field | — | — | — | — | — | — |
| Withdrawal permitted | select field | — | — | — | — | — | — |
| Renewal required | select field | — | — | — | — | — | — |
| Expiry | select field | — | — | — | — | — | — |
| Reconfirmation interval | select field | — | — | — | — | — | — |
| Age restrictions | select field | — | — | — | — | — | — |
| Guardian requirement | select field | — | — | — | — | — | — |
| Channel applicability | select field | — | — | — | — | — | — |
| Country applicability | select field | — | — | — | — | — | — |
| Brand applicability | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Default state**: Off for every optional purpose; the control does not offer "on" (no pre-ticked consent under PDPL). *(source: M18-15 (audit R-M18-15); DI-954)*
- **Withdrawal permitted**: Always yes for consent-based purposes; withdrawal as easy as granting. *(source: screens/P01-guest-web-storefront.yaml#WEB-020)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-021` Privacy & Consent Configuration Command Center: *Returns to the board's landing screen*; calls `setConsentPurposes`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The consent purpose consent configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the consent purpose consent untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No consent purpose consent configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-747`: Same purposes; one owner (proposal - CMS).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
consent: Marketing communication - purpose Marketing - optional - default off - email, SMS, WhatsApp, push - UAE
  - renewal every 24 months
```

#### Permissions

- `setConsentPurposes` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.13.7 | Consent Expiration Management | Marketing & CRM | CONTRACTED | `setConsentPurposes` |

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-023` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-023`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 1
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 4: Works in Consent Purpose & Consent Type Builder → Configure the actual consent objects that TICVAI may request from customers.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-023?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `CMS-021`.
- [ ] Every gated control is gated: `GUEST_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-024` Communication Preference & Marketing Permission Configuration

**Define how customers control the communications they wish to receive. This screen should integrate strongly with CRM and Marketing but remain governed by the central Privacy Engine.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-024 |
| Who uses it | venue staff holding `GUEST_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Administrators define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/communication-preference-marketing-permission-configurat-cms-024` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Channel + Purpose + Brand. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** How guests control what they receive: preference categories per channel and brand, marketing or transactional classification, customer-editable, default behaviour and consent dependency. Governed by the central privacy engine, integrated with CRM.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Email | select field | — | — | — | — | — | — |
| SMS | select field | — | — | — | — | — | — |
| WhatsApp | select field | — | — | — | — | — | — |
| Push Notification | select field | — | — | — | — | — | — |
| Phone | select field | — | — | — | — | — | — |
| Direct Mail | select field | — | — | — | — | — | — |
| Other future channels | select field | — | — | — | — | — | — |
| Preference category | select field | — | — | — | — | — | — |
| Communication type | select field | — | — | — | — | — | — |
| Marketing/transactional classification | select field | — | — | — | — | — | — |
| Applicable brands | select field | — | — | — | — | — | — |
| Applicable countries | select field | — | — | — | — | — | — |
| Available channels | select field | — | — | — | — | — | — |
| Customer-editable status | select field | — | — | — | — | — | — |
| Default behavior | select field | — | — | — | — | — | — |
| Consent dependency | select field | — | — | — | — | — | — |
| Expiry/reconfirmation if applicable | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Classification**: Marketing (needs consent, default off) or transactional (needs none, cannot carry marketing). *(source: contracts/satellite/marketing-crm.yaml#setCommunicationPreferenceMarketing)*
- **Consent dependency**: A marketing category is available on a channel only where the marketing consent for that channel is given. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/MarketingSubscription; DI-378)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Channel + Purpose + Brand (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-021` Privacy & Consent Configuration Command Center: *Returns to the board's landing screen*; calls `setCommunicationPreferenceMarketing`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The communication preference marketing configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the communication preference marketing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No communication preference marketing configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A marketing category that defaults to on, or names no consent purpose. |

#### Consistency with other screens

- Match `BO-749`: Same configuration; one owner.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
category: Member offers - marketing - email, WhatsApp - Coastal Aqua - customer-editable - default off
```

#### Permissions

- `setCommunicationPreferenceMarketing` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-024` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-024`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 1
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 6: Works in Communication Preference & Marketing Permission Configuration → Define how customers control the communications they wish to receive. This screen should integrate strongly with CRM and Marketing but remain governed by the central Privacy Engine.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (400, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-024?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Channel + Purpose + Brand.
- [ ] Every transition is wired: `CMS-021`.
- [ ] Every gated control is gated: `GUEST_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-025` Cookie, Tracking & Digital Technology Registry

**Maintain a centralized registry of cookies, SDKs, pixels and other governed tracking technologies used by TICVAI digital channels. This should cover more than traditional browser cookies.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 1 · needs the `core` module |
| Block | Block A · ticket #28918 (APP-SETUP-CMS-025) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `scanRunId` (navigation) |
| Route | `/policy/cookie-tracking-digital-technology-registry-cms-025` |

**What the spec says about it.** **The generator's 'needs a person' gaps removed 4 October 2026: the registry is defined, and the pack's three kinds (analytics tracker, embedded service, other) are values of the technology type, not separate operations** (CHG-FXS-005)

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The registry of every cookie, SDK, pixel and storage key on the venue's channels, including the mobile app and embedded checkout. It runs on the strictest posture: anything not strictly necessary needs consent before it loads, and a technology a scan detects is blocked until an administrator classifies and approves it.

**Fixed on main** (the package already carries these; draw what it says): The action bar holds "Analytics Tracker", "Embedded Service" and "Other tracking technology" as buttons. (CHG-SGU-017).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the scanner bought or built (CF-127)?** → Cookie scanner: buy a scanner API (hybrid). Our banner, runtime, registry and consent logs stay; a bought scanner API feeds recordCookieScan; the manual 'Upload scan report' path stays. *(decided by Chinmay, 2026-10-02; DEC-019 / CHG-NOTE-002 / CHG-SGU-013)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Technology type | select | optional | — | First party cookie · Third party cookie · Mobile sdk · Analytics tracker · Advertising pixel · Session technology · Personalisation technology · Embedded service · Local storage item · Other | — | A filter over the registry (first-party cookie, third-party cookie, mobile SDK, analytics tracker, advertising pixel, embedded service, local storage, other); not an action. | `CookieTrackingDigitalTechnologyRegistryView.technologyType` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Technology type | select | — | First party cookie · Third party cookie · Mobile sdk · Analytics tracker · Advertising pixel · Session technology · Personalisation technology · Embedded service · Local storage item · Other | `listCookieTrackingDigital` ?technologyType |
| Category | select | — | Strictly necessary · Functional · Analytics · Personalisation · Marketing · Other | `listCookieTrackingDigital` ?category |
| Channel | select | — | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | `listCookieTrackingDigital` ?channel |
| Status | radio group | — | Detected · Approved · Blocked · Retired | `listCookieTrackingDigital` ?status |
| Country | text field | — | pattern `^[A-Z]{2}$` | `listCookieTrackingDigital` ?country |
| Channel | select | — | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | `listCookieScans` ?channel |
| Search | text field | — | max length 200 | `listTrackingTechnologyCatalogue` ?search |
| Category | radio group | — | Strictly necessary · Functional · Analytics · Personalisation · Marketing | `listTrackingTechnologyCatalogue` ?category |

**Form: Add technology** (modal, opened by *Add technology*; *Add technology* calls `setTrackingTechnology`, *Cancel* sends nothing)

Name, provider, domain or app, type, category, purpose, expiry in days, first or third party, channels, and consent required (off only for strictly necessary).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | The cookie, SDK, pixel or storage key as it appears on the device. | `setTrackingTechnology` body |
| Provider `provider` | text field | required | — | max length 150 | — | — | `setTrackingTechnology` body |
| Domain application `domainApplication` | text field | optional | — | max length 255 | — | The domain, or the app and version, it was found on. | `setTrackingTechnology` body |
| Technology type `technologyType` | select | required | — | First party cookie · Third party cookie · Mobile sdk · Analytics tracker · Advertising pixel · Session technology · Personalisation technology · Embedded service · Local storage item · Other | — | — | `setTrackingTechnology` body |
| Category `category` | select | optional | — | Strictly necessary · Functional · Analytics · Personalisation · Marketing · Other | — | Null until an administrator classifies it. | `setTrackingTechnology` body |
| Other category label `otherCategoryLabel` | text field | optional | — | max length 80 | — | The organisation-defined category, when `category` is `other`. | `setTrackingTechnology` body |
| Purpose `purpose` | text area | optional | — | max length 500 | — | — | `setTrackingTechnology` body |
| Data collected `dataCollected` | text area | optional | — | max length 500 | — | — | `setTrackingTechnology` body |
| Duration days `durationDays` | number field (days) | optional | — | min 0 | — | Null for session storage. | `setTrackingTechnology` body |
| Is third party `isThirdParty` | toggle | required | — | — | — | — | `setTrackingTechnology` body |
| Channels `channels` | multi-select chips | required | — | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite; at least 1 | — | — | `setTrackingTechnology` body |
| Countries `countries` | list of values (chips) | optional | — | — | — | Empty means every country. | `setTrackingTechnology` body |
| Processing purpose code `processingPurposeCode` | text field | optional | — | — | — | The `DataProcessingPurposeLawfulBasisRegistryView.purposeCode` it serves. | `setTrackingTechnology` body |
| Consent required `consentRequired` | toggle | optional | on | False only for `strictlyNecessary`. | — | False only for `strictlyNecessary`. | `setTrackingTechnology` body |
| Privacy information `privacyInformation` | text area | optional | — | max length 1000 | — | What the preference centre tells the guest about it. | `setTrackingTechnology` body |
| Status `status` | radio group | required | — | Detected · Approved · Blocked · Retired | — | `detected` is treated as `blocked` until approved. | `setTrackingTechnology` body |

Errors to draw in the form: 400 Validation failed; 422 Approved with no category, or a non-essential technology marked as needing no consent.

**Form: Upload scan report** (modal, opened by *Upload scan report*; *Upload scan report* calls `recordCookieScan`, *Cancel* sends nothing)

The scan report file from another scanner, its channel and scan time; findings are matched to the registry and the catalogue.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scanned at `scannedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordCookieScan` body |
| Channel `channel` | select | required | — | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | — | The six governed surfaces, as the registry and the banner design name them (pack 17.1.5-17.1.6). | `recordCookieScan` body |
| Domain application `domainApplication` | text field | optional | — | max length 255 | — | The domain, or the app and version, scanned. | `recordCookieScan` body |
| Scanner ref `scannerRef` | text field | optional | — | max length 200 | — | The vendor and scan id where the scanner is bought; null for ours or a manual upload. | `recordCookieScan` body |
| Findings `findings` | repeatable rows | required | — | — | — | — | `recordCookieScan` body |
| Name `findings[].name` | text field | required | — | max length 200 | — | — | `recordCookieScan` body |
| Provider `findings[].provider` | text field | required | — | max length 150 | — | — | `recordCookieScan` body |
| Technology type `findings[].technologyType` | select | required | — | First party cookie · Third party cookie · Mobile sdk · Analytics tracker · Advertising pixel · Session technology · Personalisation technology · Embedded service · Local storage item · Other | — | — | `recordCookieScan` body |
| Is third party `findings[].isThirdParty` | toggle | required | — | — | — | — | `recordCookieScan` body |
| Duration days `findings[].durationDays` | number field (days) | optional | — | min 0 | — | — | `recordCookieScan` body |
| Domain application `findings[].domainApplication` | text field | optional | — | max length 255 | — | — | `recordCookieScan` body |
| Consent state `findings[].consentState` | segmented control | optional | — | No decision · Rejected all · Accepted all | — | The consent state the page was loaded in when the technology was seen (CHG-FUP-009). | `recordCookieScan` body |
| Page URL `findings[].pageUrl` | URL field | optional | — | max length 2000 | https:// | The page the technology was seen on. | `recordCookieScan` body |
| Initiator URL `findings[].initiatorUrl` | URL field | optional | — | max length 2000 | https:// | The script or frame that set it, so a violation names its cause (a tag manager, an embed). | `recordCookieScan` body |
| Cookie domain `findings[].cookieDomain` | text field | optional | — | max length 255 | — | — | `recordCookieScan` body |
| Same site `findings[].sameSite` | segmented control | optional | — | Strict · Lax · None | — | — | `recordCookieScan` body |
| Secure `findings[].secure` | toggle | optional | — | — | — | — | `recordCookieScan` body |
| Suggested category `findings[].suggestedCategory` | radio group | optional | — | Strictly necessary · Functional · Analytics · Personalisation · Marketing | — | The category the scanner or the catalogue suggests. A suggestion only; the venue's administrator classifies it with `setTrackingTechnology`. | `recordCookieScan` body |
| Classification source `findings[].classificationSource` | radio group | optional | — | Open cookie database · Vendor · Platform catalogue · None | — | Where `suggestedCategory` came from (CHG-FUP-009, CHG-FUP-010). | `recordCookieScan` body |

Errors to draw in the form: 400 Validation failed

**Form: Save scan schedule** (modal, opened by *Save scan schedule*; *Save scan schedule* calls `setCookieScanPolicy`, *Cancel* sends nothing)

Channel, frequency, who is alerted, and the source: the bought scanner (default) or manual upload, with the scanner vendor reference.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Channel `channel` | select | required | — | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | — | The six governed surfaces, as the registry and the banner design name them (pack 17.1.5-17.1.6). | `setCookieScanPolicy` body |
| Domain application `domainApplication` | text field | optional | — | max length 255 | — | — | `setCookieScanPolicy` body |
| Frequency `frequency` | radio group | required | — | Daily · Weekly · Monthly · False | — | — | `setCookieScanPolicy` body |
| Day of week `dayOfWeek` | stepper or slider | optional | — | min 1; max 7 | — | ISO day, for `weekly`. | `setCookieScanPolicy` body |
| Day of month `dayOfMonth` | stepper or slider | optional | — | min 1; max 28 | — | For `monthly`. | `setCookieScanPolicy` body |
| Alert recipient principals `alertRecipientPrincipalIds` | multi-picker: choose alert recipient principals | optional | — | — | — | — | `setCookieScanPolicy` body |
| Scan source `scanSource` | segmented control | optional | Bought scanner | Bought scanner · Manual upload | — | Who scans this channel (Chinmay, 2 October: buy a scanner API, hybrid; CHG-CSA-023). | `setCookieScanPolicy` body |
| Scanner vendor ref `scannerVendorRef` | text field | optional | — | max length 200 | — | The scanner vendor and the account or domain group the adapter uses; set by TICVAI when the vendor is contracted. | `setCookieScanPolicy` body |

Errors to draw in the form: 400 Validation failed; 422 A weekly schedule with no `dayOfWeek`, or a monthly one with no `dayOfMonth`

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Technology**: Name, provider, domain or app and version, type (first-party cookie, third-party cookie, mobile SDK, analytics tracker, advertising pixel, session technology, etc.), category, purpose, expiry. *(source: contracts/satellite/marketing-crm.yaml#setTrackingTechnology)*
- **Consent required**: Can be off only for strictly necessary; otherwise the save is refused with the reason. *(source: contracts/satellite/marketing-crm.yaml#setTrackingTechnology)*
- **Scan schedule**: Per channel and domain or app, daily, weekly, monthly or off, and who is alerted on a new finding. *(source: contracts/satellite/marketing-crm.yaml#setCookieScanPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Tracking technologies** (data table, from `listCookieTrackingDigital`): Detected (blocked, needs review) first, then approved, blocked and retired; retired rather than deleted, as evidence of what a site did on a date.

| Shows | Format | Notes |
|---|---|---|
| Name | text | The cookie, SDK, pixel or storage key as it appears on the device. |
| Provider | text | — |
| Technology type | chip: First party cookie, Third party cookie, Mobile sdk, Analytics tracker, Advertising … | — |
| Category | chip: Strictly necessary, Functional, Analytics, Personalisation, Marketing, Other | Null until an administrator classifies it. |
| Duration days | 1,234 | Null for session storage. |
| Status | chip: Detected, Approved, Blocked, Retired | `detected` is treated as `blocked` until approved. |
| Source | chip: Manual, Scan | — |

**Scan runs** (data table, from `listCookieScans`): **A bought scanner API (hybrid) runs the scheduled scans** (decided by Chinmay, 2 October 2026; DEC-019; CHG-CSA-023): it feeds `recordCookieScan` through TICVAI's adapter, and the manual "Upload scan report" path stays for a venue that scans elsewhere. The source column says Scanner or Upload per run. Our banner, runtime, registry and consent logs stay ours (CHG-SGU-013).

| Shows | Format | Notes |
|---|---|---|
| Scanned at | 1 Oct 2026, 14:30 | — |
| Channel | chip: B2C website, Customer portal, Mobile app, Embedded checkout, White label site … | The six governed surfaces, as the registry and the banner design name them (pack 17.1.5-17.1.6). |
| Source | chip: Bought scanner, Own crawler, Manual upload | — |
| Findings count | 1,234 | — |
| Newly detected count | 1,234 | What the administrator alert is raised from. |
| Missing count | 1,234 | Registry entries for this channel the scan did not see. |

**Loaded before consent** (metric tile, from `listCookieScans`): **The compliance output, shown first and prominently:** the scan run's `preConsentViolationCount`, the technologies seen loading before the visitor decided (CHG-FUP-009) (CHG-SGU-013).

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Channel | chip: B2C website, Customer portal, Mobile app, Embedded checkout, White label site … | The six governed surfaces, as the registry and the banner design name them (pack 17.1.5-17.1.6). |
| Domain application | text | — |
| Source | chip: Bought scanner, Own crawler, Manual upload | — |
| Scanner ref | text | — |
| Scanned at | 1 Oct 2026, 14:30 | — |
| Findings count | 1,234 | — |
| Newly detected count | 1,234 | What the administrator alert is raised from. |
| Missing count | 1,234 | Registry entries for this channel the scan did not see. |
| Pre consent violation count | 1,234 | Findings seen with no decision or after reject-all whose category is not `strictlyNecessary` (CHG-FUP-009). |
| Alerted at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**What the scan saw** (data table, from `listCookieScanFindings`): Per finding of the selected run: the consent state it was seen in (no decision, rejected all, accepted all), the page, the script that set it, its attributes (domain, SameSite, Secure) and the suggested category (CHG-FUP-009) (CHG-SGU-013).

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Scan run | the name it points at, never the id | — |
| Technology | the name it points at, never the id | The registry entry the finding matched or created (`name` + `provider` + `domainApplication`). |
| Name | text | — |
| Provider | text | — |
| Technology type | text | As `RecordCookieScanRequest.findings[].technologyType`. |
| Is third party | yes / no (icon or chip) | — |
| Duration days | 1,234 | — |
| Domain application | text | — |
| Consent state | chip: No decision, Rejected all, Accepted all | — |
| Page URL | text | — |
| Initiator URL | text | — |
| Cookie domain | text | — |
| Same site | chip: Strict, Lax, None | — |
| Secure | yes / no (icon or chip) | — |
| Suggested category | chip: Strictly necessary, Functional, Analytics, Personalisation, Marketing | 2.6.53. The five categories the banner design (`CookieBannerPreferenceCenterDesignerView.categories`) offers; the matrix's "preference" … |
| Classification source | chip: Open cookie database, Vendor, Platform catalogue, None | — |
| Is pre consent violation | yes / no (icon or chip) | Seen with no decision or after reject-all, and its category (the registry's, else the suggested one) is not `strictlyNecessary`. |
| Next cursor | text | — |

**Known cookies catalogue** (card list, from `listTrackingTechnologyCatalogue`): The platform-wide catalogue of known cookies and trackers, read-only for the venue; a finding that matches it comes with its category suggested (CHG-FUP-010) (CHG-SGU-013).

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Entry key | text | The stable key the entry is written under (`setTrackingTechnologyCatalogueEntry`), such as `google-analytics-ga`; taken from the path. |
| Name pattern | text | The cookie or key name, with `*` as a wildcard (`_ga_*`). |
| Provider | text | — |
| Category | chip: Strictly necessary, Functional, Analytics, Personalisation, Marketing | 2.6.53. The five categories the banner design (`CookieBannerPreferenceCenterDesignerView.categories`) offers; the matrix's "preference" … |
| Technology type | text | As `RecordCookieScanRequest.findings[].technologyType`. |
| Purpose | text | — |
| Typical duration days | 1,234 | — |
| Is third party | yes / no (icon or chip) | — |
| Privacy information URL | text | — |
| Source | chip: Open cookie database, Platform curation | Imported, or added or corrected by platform staff. |
| Is active | yes / no (icon or chip) | A retired entry stops suggesting; it is kept for the findings that cited it. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Scan schedule and source** (detail panel, from `listCookieScanPolicies`): Per channel: daily, weekly, monthly or off, who is alerted on a new finding, and the source (bought scanner, the default, or manual upload) (CHG-SGU-013).

| Shows | Format | Notes |
|---|---|---|
| Channel | chip: B2C website, Customer portal, Mobile app, Embedded checkout, White label site … | The six governed surfaces, as the registry and the banner design name them (pack 17.1.5-17.1.6). |
| Frequency | chip: Daily, Weekly, Monthly, False | — |
| Scan source | chip: Bought scanner, Manual upload | Who scans this channel (Chinmay, 2 October: buy a scanner API, hybrid; CHG-CSA-023). |
| Scanner vendor ref | text | The scanner vendor and the account or domain group the adapter uses; set by TICVAI when the vendor is contracted. |
| Next run at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add technology (primary button) | `setTrackingTechnology` PUT `/cookie-tracking-digital` | CookieTrackingDigitalTechnologyRegistryView | CookieTrackingDigitalTechnologyRegistryView | 400 Validation failed; 422 Approved with no category, or a non-essential technology marked as needing no consent. | opens modal first |
| Upload scan report (secondary button) | `recordCookieScan` POST `/cookie-tracking-digital/scans` | RecordCookieScanRequest | CookieScanRun | 400 Validation failed | opens modal first |
| Save scan schedule (secondary button) | `setCookieScanPolicy` PUT `/cookie-scan-policy` | CookieScanPolicy | CookieScanPolicy | 400 Validation failed; 422 A weekly schedule with no `dayOfWeek`, or a monthly one with no `dayOfMonth` | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Status**: Detected (blocked, needs review) first, then approved, blocked and retired. Retired rather than deleted, because the registry is evidence of what a site did on a date. *(source: contracts/satellite/marketing-crm.yaml#listCookieTrackingDigital)*
- **Scan runs**: Each run with source, channel, findings, newly detected and missing counts. *(source: contracts/satellite/marketing-crm.yaml#listCookieScans)*
- **Where a scan comes from**: A bought scanner API (hybrid) runs the scheduled scans and feeds recordCookieScan; the manual "Upload scan report" path stays for a venue that scans elsewhere. The source column says Scanner or Upload per run. The banner, its runtime, the registry and the consent logs stay TICVAI's own. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-002))*

**Data it reads**: `listCookieTrackingDigital` (onLoad, Cookie, Tracking & Digital Technology Registry); `listCookieScans` (onLoad, Scan runs and what each found); `listCookieScanPolicies` (onLoad, Scan schedules per channel); `listTrackingTechnologyCatalogue` (onLoad, The platform's catalogue of known cookies and trackers …)

**Where the user goes next**

- → `CMS-021` Privacy & Consent Configuration Command Center: *Returns to the board's landing screen*; calls `listCookieTrackingDigital`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cookie tracking digital list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cookie tracking digital untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No technology registered and no scan yet: offers Add technology and Save scan schedule; the first scheduled scan fills the registry. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the technology type chosen; names it and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A weekly schedule with no `dayOfWeek`, or a monthly one with no `dayOfMonth`; 422 Approved with no category, or a non-essential technology marked as needing no consent. |

#### Consistency with other screens

- Match `CMS-026`: Approved technologies appear in the banner's preference centre per category.
- Match `WEB-024`: Guests see only approved technologies, with name, provider, purpose, expiry and party.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
technologies:
- name: _ga
  provider: Google
  type: Analytics tracker
  category: Analytics
  status: Approved
  expiry: 400 days
- name: fbp
  provider: Meta
  type: Advertising pixel
  category: Marketing
  status: Detected - blocked
- name: ticvai_consent_key
  provider: TICVAI
  type: First-party cookie
  category: Strictly necessary
  status: Approved
```

#### Permissions

- `listCookieTrackingDigital` → `GUEST_VIEW` (read) · staff
- `setTrackingTechnology` → `GUEST_MANAGE` (configure) · staff
- `recordCookieScan` → `GUEST_MANAGE` (configure) · staff, service
- `listCookieScans` → `GUEST_VIEW` (read) · staff
- `listCookieScanPolicies` → `GUEST_VIEW` (read) · staff
- `setCookieScanPolicy` → `GUEST_MANAGE` (configure) · staff
- `listCookieScanFindings` → `GUEST_VIEW` (read) · staff
- `listTrackingTechnologyCatalogue` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.53 | Cookie Categorization The system should classify cookies into categories such as: Strictly Necessary - Required for website functionality Functional - Enhances user experience Analytics - Tracks … | Ticketing Sales | CONTRACTED | `setTrackingTechnology` |
| 2.6.57 | Automatic Cookie Scanning Scan websites to detect cookies automatically. Identify: - New cookies - Third-party cookies - Tracking technologies - Pixel tags - Local storage items Alert administrators … | Ticketing Sales | CONTRACTED | `recordCookieScan` |
| 2.6.64 | Administration Portal Administrators should be able to: - Configure cookie categories. - Design consent banners. - Manage translations. - Review consent logs. - Generate compliance reports. - … | Ticketing Sales | CONTRACTED | `setCookieScanPolicy` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Configurable cookie consent banner (accept/reject) per website; some cookies flagged mandatory (non-rejectable), others optional; templated and configurable in the system. *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-617)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-025` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-025`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 1
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 8: Works in Cookie, Tracking & Digital Technology Registry → Maintain a centralized registry of cookies, SDKs, pixels and other governed tracking technologies used by TICVAI digital channels. This should cover more than traditional browser cookies.

#### Acceptance for the design

- [ ] Every input above is drawn (44), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (67 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-025?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add technology, Upload scan report, Save scan schedule.
- [ ] Every transition is wired: `CMS-021`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-026` Cookie Banner & Preference Center Designer

**Provide a no-code designer for privacy/cookie interfaces displayed on digital channels.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 1 · needs the `core` module |
| Block | Block A · ticket #28919 (APP-SETUP-CMS-026) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/cookie-banner-preference-center-designer-cms-026` |

**What the spec says about it.** **Channel and brand, the upsert key, are fields on the form and choosing a row of the list loads that design (4 October 2026); the remaining selects are bound to the design's properties** (CHG-FXS-002)

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Additional configured languages. Each needs an operation, or needs removing from the screen; this is the … **Cookie Banner & Preference Center Designer declares no operation that writes anything** — its only declared call is `listCookieBannerPreference`, a read. The name promises authoring and the …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** A no-code designer for the cookie banner and preference centre, one design per brand and channel, each saved as a new version and published through privacy testing and approval. The posture is fixed: "Reject non-essential" is always offered and one click, every non-essential category starts off, and strictly necessary is always on with a description.

**Fixed on main** (the package already carries these; draw what it says): Title, Description, Buttons, Links and Category descriptions are select fields. (CHG-SGU-017); The primary action is "Additional configured languages". (CHG-SGU-017).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Logo | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | A media asset id from the library. | `CookieBannerPreferenceCenterDesignerView.logoAssetId` |
| Title | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Text per language (English and Arabic required). | `CookieBannerPreferenceCenterDesignerView.title` |
| Description | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Text per language (English and Arabic required). | `CookieBannerPreferenceCenterDesignerView.body` |
| Position | radio group | optional | — | Top · Bottom · Popup · Modal | — | — | `CookieBannerPreferenceCenterDesignerView.position` |
| Theme | text field | optional | — | — | — | The white-label theme it takes colours and fonts from. | `CookieBannerPreferenceCenterDesignerView.themeId` |
| Language | list of values (chips) | optional | — | at least 1 | — | Languages are tabs of the text fields; English and Arabic are required. | `CookieBannerPreferenceCenterDesignerView.languages` |
| Links | repeatable rows | optional | — | — | — | A list of links (privacy notice, cookie notice) per language. | `CookieBannerPreferenceCenterDesignerView.links` |
| Category descriptions | repeatable rows | optional | — | at least 1 | — | The description of each category per language. | `CookieBannerPreferenceCenterDesignerView.categories` |
| Channel | select | optional | — | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | — | Required; with the brand, the key the save upserts on. | `CookieBannerPreferenceCenterDesignerView.channel` |
| Brand | picker: choose a brand (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | The brand the design is for; picking a row of the list fills channel and brand and loads that design. | `CookieBannerPreferenceCenterDesignerView.brandId` |
| Reject in one click | toggle | optional | on | — | — | Must be true. | `CookieBannerPreferenceCenterDesignerView.rejectIsOneClick` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Brand | picker: choose a brand | — | — | `listCookieBannerPreference` ?brandId |
| Channel | select | — | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | `listCookieBannerPreference` ?channel |
| Status | segmented control | — | Draft · Published · Superseded | `listCookieBannerPreference` ?status |

**Form: Save version** (confirmDialog, opened by *Save version*; *Save version* calls `setCookieBannerDesign`, *Cancel* sends nothing)

Saves this design as version N+1 for its channel and brand; the published version stays until the new one is approved.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Brand `brandId` | picker: choose a brand | optional | — | — | shows names, sends the id | Null for the corporate design every brand inherits. | `setCookieBannerDesign` body |
| Inherits from `inheritsFromId` | picker: choose an inherits from | optional | — | — | shows names, sends the id | — | `setCookieBannerDesign` body |
| Channel `channel` | select | required | — | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | — | — | `setCookieBannerDesign` body |
| Logo `logoAssetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `setCookieBannerDesign` body |
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Text keyed by locale code, one entry per locale the venue publishes. | `setCookieBannerDesign` body |
| Body `body` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Text keyed by locale code, one entry per locale the venue publishes. | `setCookieBannerDesign` body |
| Position `position` | radio group | required | — | Top · Bottom · Popup · Modal | — | — | `setCookieBannerDesign` body |
| Theme `themeId` | text field | optional | — | — | — | The white-label theme it takes colours and fonts from. | `setCookieBannerDesign` body |
| Buttons `buttons` | repeatable rows | optional | — | — | — | — | `setCookieBannerDesign` body |
| Action `buttons[].action` | radio group | required | — | Accept all · Reject non essential · Manage preferences · Save preferences · Do not sell or share | — | — | `setCookieBannerDesign` body |
| Label `buttons[].label` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Text keyed by locale code, one entry per locale the venue publishes. | `setCookieBannerDesign` body |
| Reject is one click `rejectIsOneClick` | toggle | required | on | — | — | Must be true. | `setCookieBannerDesign` body |
| Links `links` | repeatable rows | optional | — | — | — | — | `setCookieBannerDesign` body |
| Label `links[].label` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | Text keyed by locale code, one entry per locale the venue publishes. | `setCookieBannerDesign` body |
| Policy kind `links[].policyKind` | segmented control | required | — | Privacy · Cookie · Terms and conditions | — | — | `setCookieBannerDesign` body |
| Categories `categories` | repeatable rows | required | — | at least 1 | — | — | `setCookieBannerDesign` body |
| Category `categories[].category` | radio group | required | — | Strictly necessary · Functional · Analytics · Personalisation · Marketing | — | — | `setCookieBannerDesign` body |
| Description `categories[].description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Text keyed by locale code, one entry per locale the venue publishes. | `setCookieBannerDesign` body |
| Default on `categories[].defaultOn` | toggle | required | — | True only for `strictlyNecessary`, which is always active. | — | True only for `strictlyNecessary`, which is always active. | `setCookieBannerDesign` body |
| Languages `languages` | list of values (chips) | required | — | at least 1 | — | Every language the storefront serves; Arabic renders right to left. | `setCookieBannerDesign` body |
| Regulatory regimes `regulatoryRegimes` | multi-select chips | optional | — | Gdpr · E privacy · Ccpa cpra · Lgpd · Uae pdpl · Saudi pdpl | — | 2.6.60 (29 September, build). The laws this design is published to satisfy, so compliance is stated rather than assumed. | `setCookieBannerDesign` body |
| Record ip address `recordIpAddress` | toggle | optional | off | — | — | 2.6.55, "if legally permitted" (29 September, build). On, `recordDeviceConsent` writes the IP address and user agent to `pii.consent_identifier`; off, they are not kept anywhere. | `setCookieBannerDesign` body |

Errors to draw in the form: 400 Validation failed; 422 A design that makes rejecting harder than accepting, pre-ticks a non-essential category, or names `ccpaCpra` without a `doNotSellOrShare` button.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Channel and brand**: B2C website, customer portal, mobile app, embedded checkout, white-label site, partner microsite. A brand inherits the corporate design and overrides only approved elements. *(source: contracts/satellite/marketing-crm.yaml#setCookieBannerDesign)*
- **Title and body**: Text per language (English, Arabic required); text fields, not selects. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/CookieBannerPreferenceCenterDesignerView; DI-019)*
- **Position and theme**: Top, bottom, pop-up or modal; theme from the brand. *(source: contracts/satellite/marketing-crm.yaml#setCookieBannerDesign)*
- **Regulatory regimes**: Where CCPA/CPRA is selected, the "Do not sell or share" link is shown. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/DeviceConsentAction)*

#### Outputs: what the screen shows and produces

**Shown**

**Buttons** (detail panel): Fixed by the posture, not chosen: Accept all, Reject non-essential (always one click) and Choose.

**Designs** (data table, from `listCookieBannerPreference`)

| Shows | Format | Notes |
|---|---|---|
| Channel | chip: B2C website, Customer portal, Mobile app, Embedded checkout, White label site … | — |
| Brand | the name it points at, never the id | Null for the corporate design every brand inherits. |
| Position | chip: Top, Bottom, Popup, Modal | — |
| Languages | list or chips (count when long) | Every language the storefront serves; Arabic renders right to left. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save version (primary button) | `setCookieBannerDesign` PUT `/cookie-banner-preference` | CookieBannerPreferenceCenterDesignerView | CookieBannerPreferenceCenterDesignerView | 400 Validation failed; 422 A design that makes rejecting harder than accepting, pre-ticks a non-essential category, or names `ccpaCpra` without a `doNotSellOrShare` button. | opens confirmDialog first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Live preview**: Desktop and mobile, English and Arabic (right-to-left), banner and preference centre. *(source: MATRIX 2.6.52; DI-019)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Save version**: Saved as a draft. A design with one-click reject off, a non-essential category on by default, or a missing strictly-necessary description is refused, with the reason shown. *(source: contracts/satellite/marketing-crm.yaml#setCookieBannerDesign)*
- **Send for approval**: Opens privacy testing and approval (CMS-030); publishing happens there. *(source: contracts/satellite/marketing-crm.yaml#approvePrivacyTesting)*

**Data it reads**: `listCookieBannerPreference` (onLoad, Cookie Banner & Preference Center Designer)

**Where the user goes next**

- → `CMS-021` Privacy & Consent Configuration Command Center: *Returns to the board's landing screen*; calls `listCookieBannerPreference`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cookie banner preference configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cookie banner preference untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cookie banner preference configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A design that makes rejecting harder than accepting, pre-ticks a non-essential category, or names `ccpaCpra` without a `doNotSellOrShare` button. |

#### Consistency with other screens

- Match `CMS-025`: Category descriptions list the approved technologies from the registry.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
design: Coastal Aqua - B2C website - v3 draft
title: We use cookies
titleAr: نحن نستخدم ملفات تعريف الارتباط
buttons:
- Accept all
- Reject non-essential
- Choose
```

#### Permissions

- `listCookieBannerPreference` → `GUEST_VIEW` (read) · staff
- `setCookieBannerDesign` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.60 | Regulatory Compliance Support compliance requirements including: GDPR ePrivacy Directive CCPA / CPRA LGPD PDPL (UAE and Saudi Arabia, where applicable) | Ticketing Sales | CONTRACTED | data `CookieBannerPreferenceCenterDesignerView` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Configurable cookie consent banner (accept/reject) per website; some cookies flagged mandatory (non-rejectable), others optional; templated and configurable in the system. *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-617)*
- Configurable FAQ section plus Terms & Conditions, Privacy Policy and Cookie Policy with an accept/deny prompt. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-191)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Brand (`cookieBanner.brandId`) | shows names, sends the id | — | GST-001, GST-066, WEB-001, WEB-024 | Null for the corporate design every brand inherits. |
| Inherits from (`cookieBanner.inheritsFromId`) | shows names, sends the id | — | GST-001, GST-066, WEB-001, WEB-024 | — |
| Cookie banner channel (`cookieBanner.channel`) | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | — | GST-001, GST-066, WEB-001, WEB-024 | — |
| Logo (`cookieBanner.logoAssetId`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | GST-001, GST-066, WEB-001, WEB-024 | — |
| Cookie banner title (`cookieBanner.title`) | English and Arabic (Arabic right to left) | — | GST-001, GST-066, WEB-001, WEB-024 | Text keyed by locale code, one entry per locale the venue publishes. |
| Body (`cookieBanner.body`) | English and Arabic (Arabic right to left) | — | GST-001, GST-066, WEB-001, WEB-024 | Text keyed by locale code, one entry per locale the venue publishes. |
| Position (`cookieBanner.position`) | Top · Bottom · Popup · Modal | — | GST-001, GST-066, WEB-001, WEB-024 | — |
| Theme (`cookieBanner.themeId`) | — | — | GST-001, GST-066, WEB-001, WEB-024 | The white-label theme it takes colours and fonts from. |
| Buttons (`cookieBanner.buttons`) | — | — | GST-001, GST-066, WEB-001, WEB-024 | — |
| Buttons: action (`cookieBanner.buttons[].action`) | Accept all · Reject non essential · Manage preferences · Save preferences · Do not sell or share | — | GST-001, GST-042, GST-066, WEB-001, WEB-016, WEB-024 | — |
| Buttons: label (`cookieBanner.buttons[].label`) | English and Arabic (Arabic right to left) | — | GST-001, GST-066, WEB-001, WEB-024 | Text keyed by locale code, one entry per locale the venue publishes. |
| Reject is one click (`cookieBanner.rejectIsOneClick`) | — | on | GST-001, GST-066, WEB-001, WEB-024 | Must be true. |
| Links (`cookieBanner.links`) | — | — | GST-001, GST-066, WEB-001, WEB-024 | — |
| Links: label (`cookieBanner.links[].label`) | English and Arabic (Arabic right to left) | — | GST-001, GST-066, WEB-001, WEB-024 | Text keyed by locale code, one entry per locale the venue publishes. |
| Links: policy kind (`cookieBanner.links[].policyKind`) | Privacy · Cookie · Terms and conditions | — | GST-001, GST-066, WEB-001, WEB-024 | — |
| Categories (`cookieBanner.categories`) | at least 1 | — | GST-001, GST-066, WEB-001, WEB-024 | — |
| Categories: category (`cookieBanner.categories[].category`) | Strictly necessary · Functional · Analytics · Personalisation · Marketing | — | GST-001, GST-066, WEB-001, WEB-024 | — |
| Categories: description (`cookieBanner.categories[].description`) | English and Arabic (Arabic right to left) | — | GST-001, GST-066, WEB-001, WEB-024 | Text keyed by locale code, one entry per locale the venue publishes. |
| Categories: default on (`cookieBanner.categories[].defaultOn`) | True only for `strictlyNecessary`, which is always active. | — | GST-001, GST-066, WEB-001, WEB-024 | True only for `strictlyNecessary`, which is always active. |
| Cookie banner languages (`cookieBanner.languages`) | at least 1 | — | GST-001, GST-066, WEB-001, WEB-024 | Every language the storefront serves; Arabic renders right to left. |
| Regulatory regimes (`cookieBanner.regulatoryRegimes`) | Gdpr · E privacy · Ccpa cpra · Lgpd · Uae pdpl · Saudi pdpl | — | GST-001, GST-066, WEB-001, WEB-024 | 2.6.60 (29 September, build). The laws this design is published to satisfy, so compliance is stated rather than assumed. |
| Record ip address (`cookieBanner.recordIpAddress`) | — | off | GST-001, GST-066, WEB-001, WEB-024 | 2.6.55, "if legally permitted" (29 September, build). On, `recordDeviceConsent` writes the IP address and user agent to `pii.consent_identifier`; off, they are not kept anywhere. |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-026` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-026`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 1
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 10: Works in Cookie Banner & Preference Center Designer → Provide a no-code designer for privacy/cookie interfaces displayed on digital channels.

#### Acceptance for the design

- [ ] Every input above is drawn (33), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-026?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save version.
- [ ] Every transition is wired: `CMS-021`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-027` Consent Capture Point & Customer Journey Configuration

**Define where, when and under what circumstances privacy notices and consent requests appear. This prevents each channel from implementing consent independently.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-027 |
| Who uses it | venue staff holding `GUEST_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Potential capture points include; For each capture point define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/consent-capture-point-customer-journey-configuration-cms-027` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Where, when and how notices and consent requests appear, so no channel implements consent on its own: registration, guest checkout, ticket purchase, membership and pass enrolment, app registration, POS customer creation, kiosk, CRM creation, wallet, face enrolment, newsletter, portal, competitions, partner API. The guest checkout capture point carries the open client question on marketing consent and its default.

**Known correction pending (do not draw the wrong version)**

- **Each capture point is a select field.** Why: Capture points are rows each opening their own configuration. *(source: screens/P13-white-label-cms.yaml#CMS-027; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is an opt-in ticked at guest checkout sufficient marketing consent under PDPL?** → Drawn default stands (answer: "From WEB-011: as above"): Draw it unticked and record it with source checkout; nothing is sent without it. *(decided by Chinmay, 2026-10-02; DEC-282 / CHG-NOTE-002)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Account Registration | select field | — | — | — | — | — | — |
| Guest Checkout | select field | — | — | — | — | — | — |
| Ticket Purchase | select field | — | — | — | — | — | — |
| Membership Enrollment | select field | — | — | — | — | — | — |
| Annual Pass Enrollment | select field | — | — | — | — | — | — |
| Mobile App Registration | select field | — | — | — | — | — | — |
| POS Customer Creation | select field | — | — | — | — | — | — |
| Kiosk | select field | — | — | — | — | — | — |
| CRM Customer Creation | select field | — | — | — | — | — | — |
| Wallet Enrollment | select field | — | — | — | — | — | — |
| Face Enrollment | select field | — | — | — | — | — | — |
| Newsletter Signup | select field | — | — | — | — | — | — |
| Customer Portal | select field | — | — | — | — | — | — |
| Competition/Promotion | select field | — | — | — | — | — | — |
| API/Partner Journey | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| Customer type | select field | — | — | — | — | — | — |
| Processing purpose | select field | — | — | — | — | — | — |
| Required notice | select field | — | — | — | — | — | — |
| Required consent | select field | — | — | — | — | — | — |
| Optional preferences | select field | — | — | — | — | — | — |
| Consent wording | select field | — | — | — | — | — | — |
| Policy version | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Display order | select field | — | — | — | — | — | — |
| Mandatory/optional behavior | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Guest checkout capture point**: Shows the notice link and an unticked marketing opt-in per channel beside the terms, plus preferred contact method; recorded with source checkout. Nothing marketing is sent without the tick. *(source: DI-616; DI-954; M18-15 (audit R-M18-15))*
- **Order of questions**: Per capture point and channel, what is asked in what order. *(source: contracts/satellite/marketing-crm.yaml#setConsentCapturePoint)*
- **Face enrolment**: Explicit biometric consent; for minors, guardian consent (age set by counsel). *(source: R205; DI-1085)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-021` Privacy & Consent Configuration Command Center: *Returns to the board's landing screen*; calls `setConsentCapturePoint`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The consent capture point configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the consent capture point untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No consent capture point configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A consent step naming no consent purpose, or a notice step naming no policy kind. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
capturePoint: Guest checkout - web - Coastal Aqua - 1) Terms (implied) 2) Send me offers and news by email (unticked)
  3) by WhatsApp (unticked) 4) Preferred contact email/phone
```

#### Permissions

- `setConsentCapturePoint` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Checkout captures marketing/newsletter opt-in and preferred contact method (email vs phone). *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-616)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-027` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-027`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 1
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 12: Works in Consent Capture Point & Customer Journey Configuration → Define where, when and under what circumstances privacy notices and consent requests appear. This prevents each channel from implementing consent independently.

#### Acceptance for the design

- [ ] Every input above is drawn (28), with its required mark, default, format and its error state (400, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-027?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `CMS-021`.
- [ ] Every gated control is gated: `GUEST_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-028` Privacy Notice, Policy & Terms Version Management

**Manage customer-facing privacy notices and related governed documents with complete version control.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-028 |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/privacy-notice-policy-terms-version-management-cms-028` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Every version of every privacy document (privacy policy, terms, cookie policy) with its governance: owner, approval, effective date, and whether guests must accept again. Documents are never overwritten; English and Arabic are both required before publishing.

**Known correction pending (do not draw the wrong version)**

- **The primary button is labelled "Privacy Policy" and a secondary "No Customer Action".** Why: These are document kinds and a re-acceptance option, not actions. *(source: screens/P13-white-label-cms.yaml#CMS-028; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Document type | select | — | Privacy policy · Privacy notice · Cookie notice · Marketing notice · Biometric privacy notice · Childrens privacy notice · Location services notice · Other | `listPrivacyNoticePolicy` ?documentType |
| Status | select | — | Draft · Review · Approved · Scheduled · Published · Superseded · Archived | `listPrivacyNoticePolicy` ?status |
| Language | text field | — | max length 10 | `listPrivacyNoticePolicy` ?language |

**Form: Save privacy notice policy governance** (modal, opened by *Save privacy notice policy governance*; *Save privacy notice policy governance* calls `setPrivacyNoticePolicyGovernance`, *Cancel* sends nothing)

**Collects what `setPrivacyNoticePolicyGovernance` sends before it is called.** Required: `policyId`, `documentType`, `status`. Optional: `changeClassification`, `requiresReAcceptance`, `requiresNotification`, `ownerPrincipalId`, `approvedByPrincipalId`, `approvedAt`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `approvalRequestId`, `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Policy `policyId` | picker: choose a policy | required | — | — | shows names, sends the id | The white-label `Policy` version this governs (`documentId` on the view). | `setPrivacyNoticePolicyGovernance` body |
| Document type `documentType` | select | required | — | Privacy policy · Privacy notice · Cookie notice · Marketing notice · Biometric privacy notice · Childrens privacy notice · Location services notice · Other | — | — | `setPrivacyNoticePolicyGovernance` body |
| Status `status` | select | required | Draft | Draft · Review · Approved · Scheduled · Published · Superseded · Archived | — | — | `setPrivacyNoticePolicyGovernance` body |
| Change classification `changeClassification` | segmented control | optional | — | Minor · Material | — | Set by an authorised user, never by AI. | `setPrivacyNoticePolicyGovernance` body |
| Requires re acceptance `requiresReAcceptance` | toggle | optional | off | — | — | — | `setPrivacyNoticePolicyGovernance` body |
| Requires notification `requiresNotification` | toggle | optional | off | — | — | — | `setPrivacyNoticePolicyGovernance` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `setPrivacyNoticePolicyGovernance` body |
| Approved by principal `approvedByPrincipalId` | picker: choose an approved by principal | optional | — | — | shows names, sends the id | — | `setPrivacyNoticePolicyGovernance` body |
| Approved at `approvedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setPrivacyNoticePolicyGovernance` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A status move the lifecycle does not allow, approval fields sent by the caller, or a change to the classification after approval.; 422 `review` without a `changeClassification`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Privacy Policy (primary button) | navigation or local | — | — | — | — |
| No Customer Action (secondary button) | navigation or local | — | — | — | — |
| Save privacy notice policy governance (secondary button) | `setPrivacyNoticePolicyGovernance` PUT `/privacy-notice-policy` | PrivacyNoticeGovernance | PrivacyNoticeGovernance | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `GUEST_MANAGE`; opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Version list**: Newest first with effective date, status (draft, approved, published, superseded) and whether re-acceptance is required. *(source: contracts/satellite/marketing-crm.yaml#listPrivacyNoticePolicy; contracts/satellite/white-label.yaml#setPolicy)*

**Data it reads**: `listPrivacyNoticePolicy` (onLoad, Privacy Notice, Policy & Terms Version Management)

**Where the user goes next**

- → `CMS-021` Privacy & Consent Configuration Command Center: *Returns to the board's landing screen*; calls `listPrivacyNoticePolicy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The privacy notice policy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the privacy notice policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No privacy notice policy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the privacy notice policy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A status move the lifecycle does not allow, approval fields sent by the caller, or a change to the classification after approval.; 422 `review` without a `changeClassification`. |

#### Consistency with other screens

- Match `CMS-018`: Same documents (white-label Policy); one version history.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
versions:
- Privacy policy v4 - effective 1 Oct 2026 - re-accept required - published
- Privacy policy v3 - superseded
```

#### Permissions

- `listPrivacyNoticePolicy` → `GUEST_VIEW` (read) · staff
- `setPrivacyNoticePolicyGovernance` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-028` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-028`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 1
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 14: Works in Privacy Notice, Policy & Terms Version Management → Manage customer-facing privacy notices and related governed documents with complete version control.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-028?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Privacy Policy, No Customer Action, Save privacy notice policy governance.
- [ ] Every transition is wired: `CMS-021`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-029` Minor, Guardian & Age-Based Privacy Configuration

**Provide specialized privacy configuration for journeys involving children and guardians. This is especially important for TICVAI customers operating: Theme parks Attractions Camps Academies Family entertainment Children's events**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-029 |
| Who uses it | venue staff holding `GUEST_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Where required/configured) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/minor-guardian-age-based-privacy-configuration-cms-029` |

**What the spec says about it.** **Children's biometric data: as BO-187, guardian consent, configurable** (decided by Chinmay, 2 October 2026; DEC-283, DEC-237). Allowed with a guardian-signed consent on the venue's form; the minor age per country and whether minors may be enrolled at all are the venue's settings (`RegionSettings.minorAgeThreshold`, `VenueSettings.biometrics.allowMinors`); `setMinorGuardianAge` keeps the privacy rules per country (CHG-SGU-004).

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Age rules per jurisdiction for children and guardians (theme parks, camps, academies, family entertainment): age of digital consent, guardian verification, what a guardian may consent to. No global age is hard-coded or shipped as a default; until counsel sets it, a missing date of birth counts as a minor.

**Known correction pending (do not draw the wrong version)**

- **The fields are one guardian's record (Guardian name, Email, Mobile, Consent status).** Why: This is a configuration screen; guardian records belong to CMS-054 and BO-740. *(source: screens/P13-white-label-cms.yaml#CMS-029; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Children's biometric data - exclude entirely, or allow with a guardian-signed consent?** → Children's biometric data: as BO-187 (guardian consent, configurable). *(decided by Chinmay, 2026-10-02; DEC-283 / CHG-NOTE-002 / CHG-SGU-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Guardian name | select field | — | — | — | — | — | — |
| Relationship | select field | — | — | — | — | — | — |
| Email | select field | — | — | — | — | — | — |
| Mobile | select field | — | — | — | — | — | — |
| Verification status | select field | — | — | — | — | — | — |
| Consent status | select field | — | — | — | — | — | — |
| Consent version | select field | — | — | — | — | — | — |
| Date/time | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Country rule**: Age below which a guardian consents; verification method; purposes a minor may never be asked for (marketing, biometrics only with guardian consent on the venue's form, and only where the venue has not switched minors off). *(source: contracts/satellite/marketing-crm.yaml#setMinorGuardianAge; R205 / decided 2 October 2026 by Chinmay (CHG-NOTE-002))*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-021` Privacy & Consent Configuration Command Center: *Returns to the board's landing screen*; calls `setMinorGuardianAge`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The minor guardian age-based configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the minor guardian age-based untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No minor guardian age-based configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 `guardianRequiredBelowAge` above `minorBelowAge`, or no verification method. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: UAE - guardian consent under 18 (to be confirmed by counsel) - guardian verified by OTP - marketing to minors
  not allowed
```

#### Permissions

- `setMinorGuardianAge` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-029` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-029`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 1
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 16: Works in Minor, Guardian & Age-Based Privacy Configuration → Provide specialized privacy configuration for journeys involving children and guardians. This is especially important for TICVAI customers operating: Theme parks Attractions Camps Academies Family …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-029?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `CMS-021`.
- [ ] Every gated control is gated: `GUEST_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-030` Privacy Configuration Testing, Approval & Publication

**Act as the final governance gate before privacy configurations are deployed into production. No major privacy configuration should move directly from editing to production without validation. Board 1 defines what TICVAI's privacy rules are. Board 2 manages what happens after those rules are live and customers begin interacting with them.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | Block D · task APP-CMS-CMS-030 |
| Who uses it | venue staff holding `GUEST_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Detect configuration problems such as; Central configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/privacy-configuration-testing-approval-publication-cms-030` |

**Known gaps.** **The pack names 6 actions on this screen; 2 are served since the writers pass (29 September): Publish Now, Schedule Publication by `setPrivacyNoticePolicyGovernance`.** Still unserved: Selected …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The gate every privacy configuration change passes before production: test a change set against sample guests (country, brand, channel, age, status, existing consents, language) and see missing policies, mappings, languages, conflicting rules and invalid dates; then approve and publish.

**Known correction pending (do not draw the wrong version)**

- **Test inputs and findings are all select fields.** Why: Inputs are a test form; findings are results. *(source: screens/P13-white-label-cms.yaml#CMS-030; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Country | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Customer age | select field | — | — | — | — | — | — |
| Customer status | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Existing consents | select field | — | — | — | — | — | — |
| Existing policy acceptance | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Requested processing | select field | — | — | — | — | — | — |
| Missing policy | select field | — | — | — | — | — | — |
| Missing consent mapping | select field | — | — | — | — | — | — |
| Missing language | select field | — | — | — | — | — | — |
| Conflicting consent rules | select field | — | — | — | — | — | — |
| Missing processing purpose | select field | — | — | — | — | — | — |
| Invalid effective dates | select field | — | — | — | — | — | — |
| Unmapped tracking technology | select field | — | — | — | — | — | — |
| Missing guardian rule | select field | — | — | — | — | — | — |
| Unpublished dependency | select field | — | — | — | — | — | — |
| Circular configuration dependency | select field | — | — | — | — | — | — |
| 1 Center | select field | — | — | — | — | — | — |
| 2 Registry processed | select field | — | — | — | — | — | — |
| # Backend Screen Core Responsibility | text field | — | — | — | — | — | — |
| 3 | select field | — | — | — | — | — | — |
| 17.1. Communication Preference & Marketing Marketing/channel | text field | — | — | — | — | — | — |
| 4 Permission Configuration permissions | text field | — | — | — | — | — | — |
| 17.1. Cookie/SDK/tracker | select field | — | — | — | — | — | — |
| Cookie, Tracking & Digital Technology Registry | text field | — | — | — | — | — | — |
| 5 inventory | select field | — | — | — | — | — | — |

**Form: Save privacy notice policy governance** (modal, opened by *Save privacy notice policy governance*; *Save privacy notice policy governance* calls `setPrivacyNoticePolicyGovernance`, *Cancel* sends nothing)

**Collects what `setPrivacyNoticePolicyGovernance` sends before it is called.** Required: `policyId`, `documentType`, `status`. Optional: `changeClassification`, `requiresReAcceptance`, `requiresNotification`, `ownerPrincipalId`, `approvedByPrincipalId`, `approvedAt`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `approvalRequestId`, `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Policy `policyId` | picker: choose a policy | required | — | — | shows names, sends the id | The white-label `Policy` version this governs (`documentId` on the view). | `setPrivacyNoticePolicyGovernance` body |
| Document type `documentType` | select | required | — | Privacy policy · Privacy notice · Cookie notice · Marketing notice · Biometric privacy notice · Childrens privacy notice · Location services notice · Other | — | — | `setPrivacyNoticePolicyGovernance` body |
| Status `status` | select | required | Draft | Draft · Review · Approved · Scheduled · Published · Superseded · Archived | — | — | `setPrivacyNoticePolicyGovernance` body |
| Change classification `changeClassification` | segmented control | optional | — | Minor · Material | — | Set by an authorised user, never by AI. | `setPrivacyNoticePolicyGovernance` body |
| Requires re acceptance `requiresReAcceptance` | toggle | optional | off | — | — | — | `setPrivacyNoticePolicyGovernance` body |
| Requires notification `requiresNotification` | toggle | optional | off | — | — | — | `setPrivacyNoticePolicyGovernance` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `setPrivacyNoticePolicyGovernance` body |
| Approved by principal `approvedByPrincipalId` | picker: choose an approved by principal | optional | — | — | shows names, sends the id | — | `setPrivacyNoticePolicyGovernance` body |
| Approved at `approvedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setPrivacyNoticePolicyGovernance` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A status move the lifecycle does not allow, approval fields sent by the caller, or a change to the classification after approval.; 422 `review` without a `changeClassification`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish Now (primary button) | navigation or local | — | — | — | — |
| Schedule Publication (secondary button) | navigation or local | — | — | — | — |
| Selected Tenant (secondary button) | navigation or local | — | — | — | — |
| Selected Brand (secondary button) | navigation or local | — | — | — | — |
| Selected Country (secondary button) | navigation or local | — | — | — | — |
| Selected Channel (secondary button) | navigation or local | — | — | — | — |
| Save privacy notice policy governance (secondary button) | `setPrivacyNoticePolicyGovernance` PUT `/privacy-notice-policy` | PrivacyNoticeGovernance | PrivacyNoticeGovernance | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `GUEST_MANAGE`; opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Test result**: For a sample guest, which notices and consents each capture point would show, and every blocking issue. *(source: contracts/satellite/marketing-crm.yaml#approvePrivacyTesting)*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The privacy testing approval configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the privacy testing approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No privacy testing approval configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A status move the lifecycle does not allow, approval fields sent by the caller, or a change to the classification after approval.; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.; 422 `review` without a `changeClassification`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
test: Guest checkout, UAE, Arabic, age 15 - BLOCK - consent text missing in Arabic for WhatsApp marketing; minor
  shown marketing opt-in
```

#### Permissions

- `approvePrivacyTesting` → `GUEST_MANAGE` (configure) · staff
- `setPrivacyNoticePolicyGovernance` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-030` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS102 Privacy  Consent   Preference Management Board 1.dc.html#cms-030`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 1
- Flow F150 *Privacy Consent Preference Management board 1: Privacy & Consent Configuration …*, step 18: Works in Privacy Configuration Testing, Approval & Publication → Act as the final governance gate before privacy configurations are deployed into production. No major privacy configuration should move directly from editing to production without validation. Board 1 …

#### Acceptance for the design

- [ ] Every input above is drawn (39), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-030?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish Now, Schedule Publication, Selected Tenant, Selected Brand, Selected Country, Selected Channel, Save privacy notice policy governance.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `GUEST_MANAGE`.
- [ ] The module and platform inputs below are applied.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approvePrivacyTesting": {"method":"PUT","path":"/privacy-testing","contract":"marketing-crm","summary":"Privacy Configuration Testing, Approval & Publication","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PrivacyConfigurationTestingApprovalPublicationInput","responds":"PrivacyConfigurationTestingApprovalPublicationView"},
"listCookieBannerPreference": {"method":"GET","path":"/cookie-banner-preference","contract":"marketing-crm","summary":"Cookie Banner & Preference Center Designer","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"brandId","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCookieScanFindings": {"method":"GET","path":"/cookie-tracking-digital/scans/{scanRunId}/findings","contract":"marketing-crm","summary":"What one scan saw, in each consent state","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"consentState","in":"query","required":false},{"name":"preConsentOnly","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCookieScanPolicies": {"method":"GET","path":"/cookie-scan-policy","contract":"marketing-crm","summary":"Scan schedules per channel","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCookieScans": {"method":"GET","path":"/cookie-tracking-digital/scans","contract":"marketing-crm","summary":"Scan runs and what each found","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCookieTrackingDigital": {"method":"GET","path":"/cookie-tracking-digital","contract":"marketing-crm","summary":"Cookie, Tracking & Digital Technology Registry","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"technologyType","in":"query","required":false},{"name":"category","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDataProcessingPurpose": {"method":"GET","path":"/data-processing-purpose","contract":"marketing-crm","summary":"Data Processing Purpose & Lawful Basis Registry","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":false},{"name":"lawfulBasis","in":"query","required":false},{"name":"sensitiveOnly","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPrivacyConsent": {"method":"GET","path":"/privacy-consent","contract":"marketing-crm","summary":"Privacy & Consent Configuration Command Center","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"brandId","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"consentPurpose","in":"query","required":false},{"name":"policyId","in":"query","required":false},{"name":"language","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"effectiveFrom","in":"query","required":false},{"name":"effectiveTo","in":"query","required":false}],"requestBody":null,"responds":"PrivacyConsentConfigurationCommandCenterView"},
"listPrivacyNoticePolicy": {"method":"GET","path":"/privacy-notice-policy","contract":"marketing-crm","summary":"Privacy Notice, Policy & Terms Version Management","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"documentType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"language","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTrackingTechnologyCatalogue": {"method":"GET","path":"/cookie-tracking-digital/platform-catalogue","contract":"marketing-crm","summary":"The platform's catalogue of known cookies and trackers","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"search","in":"query","required":false},{"name":"category","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"recordCookieScan": {"method":"POST","path":"/cookie-tracking-digital/scans","contract":"marketing-crm","summary":"Take in the result of a site or app scan","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecordCookieScanRequest","responds":null},
"setCommunicationPreferenceMarketing": {"method":"PUT","path":"/communication-preference-marketing","contract":"marketing-crm","summary":"Communication Preference & Marketing Permission Configuration","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CommunicationPreferenceMarketingPermissionConfiguratInput","responds":"CommunicationPreferenceMarketingPermissionConfiguratView"},
"setConsentCapturePoint": {"method":"PUT","path":"/consent-capture-point","contract":"marketing-crm","summary":"Consent Capture Point & Customer Journey Configuration","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConsentCapturePointCustomerJourneyConfigurationInput","responds":"ConsentCapturePointCustomerJourneyConfigurationView"},
"setConsentPurposes": {"method":"PUT","path":"/consent-purposes","contract":"marketing-crm","summary":"Configure consent purposes","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConsentPurposeConfig"},
"setCookieBannerDesign": {"method":"PUT","path":"/cookie-banner-preference","contract":"marketing-crm","summary":"Save a cookie banner design as a new version","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CookieBannerPreferenceCenterDesignerView","responds":"CookieBannerPreferenceCenterDesignerView"},
"setCookieScanPolicy": {"method":"PUT","path":"/cookie-scan-policy","contract":"marketing-crm","summary":"Set how often a channel is scanned and who is alerted","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CookieScanPolicy","responds":"CookieScanPolicy"},
"setDataProcessingPurpose": {"method":"PUT","path":"/data-processing-purpose","contract":"marketing-crm","summary":"Create or change a processing purpose","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DataProcessingPurposeLawfulBasisRegistryView","responds":"DataProcessingPurposeLawfulBasisRegistryView"},
"setMinorGuardianAge": {"method":"PUT","path":"/minor-guardian-age","contract":"marketing-crm","summary":"Minor, Guardian & Age-Based Privacy Configuration","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MinorGuardianAgeBasedPrivacyConfigurationInput","responds":"MinorGuardianAgeBasedPrivacyConfigurationView"},
"setPrivacyNoticePolicyGovernance": {"method":"PUT","path":"/privacy-notice-policy","contract":"marketing-crm","summary":"Set the privacy governance of one version of a privacy document","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PrivacyNoticeGovernance","responds":"PrivacyNoticeGovernance"},
"setTrackingTechnology": {"method":"PUT","path":"/cookie-tracking-digital","contract":"marketing-crm","summary":"Add, classify or retire a tracking technology","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CookieTrackingDigitalTechnologyRegistryView","responds":"CookieTrackingDigitalTechnologyRegistryView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CommunicationPreferenceMarketingPermissionConfiguratInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"One communication preference category, as the privacy administrator defines it (pack 17.1.4 Configuration).","required":["categoryCode","name","classification","availableChannels","defaultBehavior","customerEditable"],"properties":{"categoryCode":{"type":"string","maxLength":60,"description":"The natural key, e.g. `orderConfirmation`, `promotions`, `birthdayCampaigns`."},"name":{"type":"string","maxLength":150},"description":{"type":"string","maxLength":1000,"nullable":true},"classification":{"type":"string","enum":["transactional","marketing"],"description":"The pack's critical principle. Decides whether consent is needed at all."},"communicationType":{"type":"string","enum":["orderConfirmation","ticketDelivery","paymentInformation","eventChanges","securityMessages","promotions","newEvents","membershipOffers","loyaltyOffers","birthdayCampaigns","partnerOffers","surveys","other"]},"consentPurpose":{"allOf":[{"$ref":"#/components/schemas/ConsentPurpose"}],"nullable":true,"description":"Required for `marketing`. The purpose whose consent a send checks first."},"availableChannels":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/MessageChannel"}},"applicableBrandIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Empty means every brand of the tenant."},"applicableCountries":{"type":"array","items":{"type":"string","pattern":"^[A-Z]{2}$"},"description":"Empty means every country."},"customerEditable":{"type":"boolean","description":"Whether the guest may change it in the preference centre."},"defaultBehavior":{"type":"string","enum":["on","off"],"description":"`off` for every `marketing` category (opt-in)."},"reconfirmAfterMonths":{"type":"integer","minimum":1,"nullable":true,"description":"Ask the guest again after this long; null never."},"status":{"type":"string","enum":["active","retired"],"default":"active"}}},
"CommunicationPreferenceMarketingPermissionConfiguratView": {"x-ticvai-persistence":"marketing.communication_preference_type","description":"A stored communication preference category.","allOf":[{"$ref":"#/components/schemas/CommunicationPreferenceMarketingPermissionConfiguratInput"},{"type":"object","required":["id","version"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"version":{"type":"integer","minimum":1,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}}]},
"ConsentCapturePointCustomerJourneyConfigurationInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"One capture point's journey configuration (pack 17.1.7 Journey Configuration).","required":["capturePoint","channel","steps"],"properties":{"capturePoint":{"type":"string","enum":["accountRegistration","guestCheckout","ticketPurchase","membershipEnrolment","annualPassEnrolment","mobileAppRegistration","posCustomerCreation","kiosk","crmCustomerCreation","walletEnrolment","faceEnrolment","newsletterSignup","customerPortal","competitionPromotion","apiPartnerJourney"]},"channel":{"$ref":"#/components/schemas/ConsentSource"},"brandId":{"type":"string","format":"uuid","nullable":true},"country":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"customerType":{"type":"string","enum":["individual","member","corporate","group","school"],"nullable":true},"steps":{"type":"array","minItems":1,"maxItems":20,"items":{"type":"object","required":["stepKind","displayOrder","mandatory"],"properties":{"stepKind":{"type":"string","enum":["privacyNotice","terms","consent","preferences"]},"displayOrder":{"type":"integer","minimum":1},"processingPurposeCode":{"type":"string","nullable":true},"policyKind":{"type":"string","nullable":true,"description":"For a notice or terms step, the white-label policy kind shown (its current published version is shown; the guest's acceptance records that version)."},"consentPurpose":{"allOf":[{"$ref":"#/components/schemas/ConsentPurpose"}],"nullable":true,"description":"For a consent step."},"preferenceCategoryCodes":{"type":"array","items":{"type":"string"},"description":"For a preferences step, `setCommunicationPreferenceMarketing` categories."},"wording":{"allOf":[{"$ref":"#/components/schemas/marketing-crm::LocalisedText"}],"nullable":true,"description":"Consent wording shown at this step, per language."},"mandatory":{"type":"boolean","description":"A mandatory step blocks the journey until answered; a marketing consent is never mandatory."},"showWhen":{"type":"string","enum":["always","biometricEnrolmentSelected","belowGuardianAge"],"default":"always"}}}},"skipIfCurrentVersionAccepted":{"type":"boolean","default":true},"languages":{"type":"array","items":{"type":"string","maxLength":10}},"status":{"type":"string","enum":["active","retired"],"default":"active"}}},
"ConsentCapturePointCustomerJourneyConfigurationView": {"x-ticvai-persistence":"marketing.consent_capture_point","description":"A stored capture point and its journey, at its current version.","allOf":[{"$ref":"#/components/schemas/ConsentCapturePointCustomerJourneyConfigurationInput"},{"type":"object","required":["id","version","publicationStatus"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"version":{"type":"integer","minimum":1,"readOnly":true},"publicationStatus":{"type":"string","enum":["draft","review","approved","published","superseded"],"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}}]},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"ConsentPurposeConfig": {"x-ticvai-persistence":"marketing.consent_purpose + marketing.consent_purpose_channel","type":"object","required":["purpose","channels","noticeVersion","isRequiredForService"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"displayName":{"type":"string"},"description":{"type":"string"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","description":"Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured.\n"},"isRequiredForService":{"type":"boolean","description":"True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently.\n"},"expiresAfterMonths":{"type":"integer","nullable":true}}},
"ConsentSource": {"type":"string","enum":["guestApp","website","kiosk","pos","callCentre","import","agentRecorded","cookieBanner","checkout"],"description":"`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."},
"CookieBannerPreferenceCenterDesignerView": {"type":"object","x-ticvai-persistence":"marketing.cookie_banner_design","description":"One version of a cookie banner and preference-centre design (pack 17.1.6).","required":["channel","position","languages","rejectIsOneClick","categories"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"Null for the corporate design every brand inherits."},"inheritsFromId":{"type":"string","format":"uuid","nullable":true},"channel":{"type":"string","enum":["b2cWebsite","customerPortal","mobileApp","embeddedCheckout","whiteLabelSite","partnerMicrosite"]},"logoAssetId":{"type":"string","format":"uuid","nullable":true},"title":{"$ref":"#/components/schemas/marketing-crm::LocalisedText"},"body":{"$ref":"#/components/schemas/marketing-crm::LocalisedText"},"position":{"type":"string","enum":["top","bottom","popup","modal"]},"themeId":{"type":"string","nullable":true,"description":"The white-label theme it takes colours and fonts from."},"buttons":{"type":"array","items":{"type":"object","required":["action"],"properties":{"action":{"type":"string","enum":["acceptAll","rejectNonEssential","managePreferences","savePreferences","doNotSellOrShare"]},"label":{"$ref":"#/components/schemas/marketing-crm::LocalisedText"}}}},"rejectIsOneClick":{"type":"boolean","default":true,"description":"Must be true."},"links":{"type":"array","items":{"type":"object","required":["label","policyKind"],"properties":{"label":{"$ref":"#/components/schemas/marketing-crm::LocalisedText"},"policyKind":{"type":"string","enum":["privacy","cookie","termsAndConditions"]}}}},"categories":{"type":"array","minItems":1,"items":{"type":"object","required":["category","defaultOn"],"properties":{"category":{"type":"string","enum":["strictlyNecessary","functional","analytics","personalisation","marketing"]},"description":{"$ref":"#/components/schemas/marketing-crm::LocalisedText"},"defaultOn":{"type":"boolean","description":"True only for `strictlyNecessary`, which is always active."}}}},"languages":{"type":"array","minItems":1,"items":{"type":"string","maxLength":10},"description":"Every language the storefront serves; Arabic renders right to left."},"regulatoryRegimes":{"type":"array","items":{"type":"string","enum":["gdpr","ePrivacy","ccpaCpra","lgpd","uaePdpl","saudiPdpl"]},"description":"2.6.60 (29 September, build). **The laws this design is published to satisfy**, so compliance is stated rather than assumed. The strictest posture (opt-in, one-click reject, every non-essential category off) already meets GDPR/ePrivacy, LGPD and both PDPLs; `ccpaCpra` adds the \"Do not sell or share\" button (`doNotSellOrShare`) and honours a Global Privacy Control signal as that opt-out."},"recordIpAddress":{"type":"boolean","default":false,"description":"2.6.55, \"if legally permitted\" (29 September, build). On, `recordDeviceConsent` writes the IP address and user agent to `pii.consent_identifier`; off, they are not kept anywhere. Off by default."},"noticeVersion":{"type":"string","readOnly":true,"description":"Moves with the cookie policy (white-label `setPolicy`, kind `cookie`)."},"version":{"type":"integer","minimum":1,"readOnly":true},"status":{"type":"string","enum":["draft","published","superseded"],"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CookieCategory": {"type":"string","enum":["strictlyNecessary","functional","analytics","personalisation","marketing"],"description":"2.6.53. The five categories the banner design (`CookieBannerPreferenceCenterDesignerView.categories`) offers; the matrix's \"preference\" category is `personalisation` (British spelling, as `ConsentPurpose`)."},
"CookieConsentChannel": {"type":"string","enum":["b2cWebsite","customerPortal","mobileApp","embeddedCheckout","whiteLabelSite","partnerMicrosite"],"description":"The six governed surfaces, as the registry and the banner design name them (pack 17.1.5-17.1.6)."},
"CookieScanFinding": {"type":"object","x-ticvai-persistence":"marketing.cookie_scan_finding","description":"**One technology one scan saw, in one consent state** (Chinmay, 2 October, contract follow-ups; CHG-FUP-009). Written by `recordCookieScan` from `findings[]`, never edited; read by `listCookieScanFindings`. Kept with its run, so an audit can show what loaded before consent on a given day.","required":["scanRunId","name","provider","technologyType","isThirdParty","isPreConsentViolation"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scanRunId":{"type":"string","format":"uuid","x-ticvai-references":"marketing.cookie_scan_run"},"technologyId":{"type":"string","format":"uuid","nullable":true,"description":"The registry entry the finding matched or created (`name` + `provider` + `domainApplication`)."},"name":{"type":"string","maxLength":200},"provider":{"type":"string","maxLength":150},"technologyType":{"type":"string","maxLength":40,"description":"As `RecordCookieScanRequest.findings[].technologyType`."},"isThirdParty":{"type":"boolean"},"durationDays":{"type":"integer","minimum":0,"nullable":true},"domainApplication":{"type":"string","maxLength":255,"nullable":true},"consentState":{"type":"string","enum":["noDecision","rejectedAll","acceptedAll"],"nullable":true},"pageUrl":{"type":"string","maxLength":2000,"nullable":true},"initiatorUrl":{"type":"string","maxLength":2000,"nullable":true},"cookieDomain":{"type":"string","maxLength":255,"nullable":true},"sameSite":{"type":"string","enum":["strict","lax","none"],"nullable":true},"secure":{"type":"boolean","nullable":true},"suggestedCategory":{"allOf":[{"$ref":"#/components/schemas/CookieCategory"}],"nullable":true},"classificationSource":{"type":"string","enum":["openCookieDatabase","vendor","platformCatalogue","none"],"nullable":true},"isPreConsentViolation":{"type":"boolean","description":"Seen with no decision or after reject-all, and its category (the registry's, else the suggested one) is not `strictlyNecessary`. An unclassified technology counts as a violation, as `detected` is treated as blocked."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."}}},
"CookieScanPolicy": {"type":"object","x-ticvai-persistence":"marketing.cookie_scan_policy","description":"How often one channel's domain or app is scanned and who is alerted (2.6.64).","required":["channel","frequency"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"channel":{"$ref":"#/components/schemas/CookieConsentChannel"},"domainApplication":{"type":"string","maxLength":255,"nullable":true},"frequency":{"type":"string","enum":["daily","weekly","monthly",false]},"dayOfWeek":{"type":"integer","minimum":1,"maximum":7,"nullable":true,"description":"ISO day, for `weekly`."},"dayOfMonth":{"type":"integer","minimum":1,"maximum":28,"nullable":true,"description":"For `monthly`."},"alertRecipientPrincipalIds":{"type":"array","items":{"type":"string","format":"uuid"}},"scanSource":{"type":"string","enum":["boughtScanner","manualUpload"],"default":"boughtScanner","description":"**Who scans this channel** (Chinmay, 2 October: buy a scanner API, hybrid; CHG-CSA-023). `boughtScanner`: the scheduled run calls the bought scanner API through TICVAI's adapter, which feeds `recordCookieScan`. `manualUpload`: no scheduled scan; an administrator uploads a scan report."},"scannerVendorRef":{"type":"string","maxLength":200,"nullable":true,"description":"The scanner vendor and the account or domain group the adapter uses; set by TICVAI when the vendor is contracted."},"lastRunAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"nextRunAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CookieScanRun": {"type":"object","x-ticvai-persistence":"marketing.cookie_scan_run","description":"One scan taken in by `recordCookieScan` (2.6.57).","required":["channel","scannedAt","source","findingsCount","newlyDetectedCount"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"channel":{"$ref":"#/components/schemas/CookieConsentChannel"},"domainApplication":{"type":"string","maxLength":255,"nullable":true},"source":{"type":"string","enum":["boughtScanner","ownCrawler","manualUpload"]},"scannerRef":{"type":"string","maxLength":200,"nullable":true},"scannedAt":{"type":"string","format":"date-time"},"findingsCount":{"type":"integer","minimum":0},"newlyDetectedCount":{"type":"integer","minimum":0,"description":"What the administrator alert is raised from."},"missingCount":{"type":"integer","minimum":0,"description":"Registry entries for this channel the scan did not see."},"preConsentViolationCount":{"type":"integer","minimum":0,"description":"Findings seen with no decision or after reject-all whose category is not `strictlyNecessary` (CHG-FUP-009). Above zero, the administrator alert is raised."},"alertedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."}}},
"CookieTrackingDigitalTechnologyRegistryView": {"type":"object","x-ticvai-persistence":"marketing.tracking_technology","description":"One governed tracking technology (pack 17.1.5 Registry Fields; BL-073 §4a).","required":["name","provider","technologyType","isThirdParty","channels","status"],"properties":{"technologyId":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string","maxLength":200,"description":"The cookie, SDK, pixel or storage key as it appears on the device."},"provider":{"type":"string","maxLength":150},"domainApplication":{"type":"string","maxLength":255,"nullable":true,"description":"The domain, or the app and version, it was found on."},"technologyType":{"type":"string","enum":["firstPartyCookie","thirdPartyCookie","mobileSdk","analyticsTracker","advertisingPixel","sessionTechnology","personalisationTechnology","embeddedService","localStorageItem","other"]},"category":{"type":"string","enum":["strictlyNecessary","functional","analytics","personalisation","marketing","other"],"nullable":true,"description":"Null until an administrator classifies it."},"otherCategoryLabel":{"type":"string","maxLength":80,"nullable":true,"description":"The organisation-defined category, when `category` is `other`."},"purpose":{"type":"string","maxLength":500,"nullable":true},"dataCollected":{"type":"string","maxLength":500,"nullable":true},"durationDays":{"type":"integer","minimum":0,"nullable":true,"description":"Null for session storage."},"isThirdParty":{"type":"boolean"},"channels":{"type":"array","minItems":1,"items":{"type":"string","enum":["b2cWebsite","customerPortal","mobileApp","embeddedCheckout","whiteLabelSite","partnerMicrosite"]}},"countries":{"type":"array","items":{"type":"string","pattern":"^[A-Z]{2}$"},"description":"Empty means every country."},"processingPurposeCode":{"type":"string","nullable":true,"description":"The `DataProcessingPurposeLawfulBasisRegistryView.purposeCode` it serves."},"consentRequired":{"type":"boolean","default":true,"description":"False only for `strictlyNecessary`."},"privacyInformation":{"type":"string","maxLength":1000,"nullable":true,"description":"What the preference centre tells the guest about it."},"source":{"type":"string","enum":["manual","scan"],"default":"manual","readOnly":true},"status":{"type":"string","enum":["detected","approved","blocked","retired"],"description":"`detected` is treated as `blocked` until approved."},"firstDetectedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"lastSeenAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"DataProcessingPurposeLawfulBasisRegistryView": {"type":"object","x-ticvai-persistence":"marketing.processing_purpose","description":"One processing purpose in the tenant's register (pack 17.1.2). The lawful basis is the privacy administrator's classification, never the platform's.","required":["purposeCode","purposeName","lawfulBasis","status"],"properties":{"purposeId":{"type":"string","format":"uuid","readOnly":true},"purposeCode":{"type":"string","maxLength":60,"description":"The natural key, e.g. `ticketPurchase`, `marketingCommunication`."},"purposeName":{"type":"string","maxLength":150},"description":{"type":"string","maxLength":2000,"nullable":true},"businessOwner":{"type":"string","maxLength":150,"nullable":true,"description":"The accountable team or person."},"dataControllerApplicableOrganization":{"type":"string","maxLength":200,"nullable":true,"description":"The legal entity acting as controller for this purpose."},"dataCategories":{"type":"array","items":{"type":"string","maxLength":80},"description":"e.g. contact details, payment, date of birth, images."},"dataSubjectCategories":{"type":"array","items":{"type":"string","enum":["guest","member","minor","guardian","partner","employee","other"]}},"processingActivities":{"type":"array","items":{"type":"string","maxLength":150}},"systemsModules":{"type":"array","items":{"$ref":"#/components/schemas/common::ModuleKey"}},"countriesJurisdictions":{"type":"array","items":{"type":"string","pattern":"^[A-Z]{2}$"}},"lawfulBasis":{"type":"string","enum":["consent","contractualNecessity","legalObligation","legitimateInterest","vitalInterest","publicInterest","other","unclassified"],"default":"unclassified","description":"Set by the privacy administrator. `unclassified` is flagged, never assumed."},"lawfulBasisNote":{"type":"string","maxLength":500,"nullable":true,"description":"Required when `lawfulBasis` is `other`."},"sensitiveCategories":{"type":"array","items":{"type":"string","enum":["biometrics","childrensData","identityDocuments","preciseLocation","health","other"]}},"consentPurposes":{"type":"array","items":{"$ref":"#/components/schemas/ConsentPurpose"},"description":"The consent purposes that rely on this processing purpose."},"policyIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Notices and policies that describe it (white-label `listPolicies`)."},"capturePointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"retentionPolicyCodes":{"type":"array","items":{"type":"string"},"description":"`DataRetentionPolicy.code` values that govern its data."},"thirdPartyProcessors":{"type":"array","items":{"type":"string","maxLength":150}},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["draft","active","retired"],"default":"draft"},"version":{"type":"integer","minimum":1,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MinorGuardianAgeBasedPrivacyConfigurationInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"One jurisdiction's age and guardian rule (pack 17.1.9 Age Rules, Guardian Verification).","required":["country","minorBelowAge","guardianRequiredBelowAge","ageVerificationMethod","guardianVerificationMethods"],"properties":{"country":{"type":"string","pattern":"^[A-Z]{2}$","description":"The jurisdiction the rule applies to."},"minorBelowAge":{"type":"integer","minimum":1,"maximum":25,"description":"A guest younger than this is a minor. Set by the tenant; no default."},"guardianRequiredBelowAge":{"type":"integer","minimum":1,"maximum":25,"description":"A guardian must give privacy consent for a guest younger than this. Not above `minorBelowAge`."},"ageVerificationMethod":{"type":"string","enum":["selfDeclaredDateOfBirth","identityDocument","staffVerification","accountRecord"]},"guardianVerificationMethods":{"type":"array","minItems":1,"items":{"type":"string","enum":["emailOtp","smsOtp","accountAuthentication","staffVerification","otherApproved"]}},"guardianDataRequired":{"type":"array","items":{"type":"string","enum":["name","relationship","email","mobile"]},"description":"What is captured about the guardian."},"restrictMarketing":{"type":"boolean","default":true,"description":"No marketing to a minor, whatever consent is given."},"restrictTracking":{"type":"boolean","default":true},"restrictPersonalisation":{"type":"boolean","default":true},"restrictedProcessingPurposeCodes":{"type":"array","items":{"type":"string"},"description":"Further processing purposes refused for minors (e.g. biometrics without guardian consent)."},"consentPurposesRequiringGuardian":{"type":"array","items":{"$ref":"#/components/schemas/ConsentPurpose"}}}},
"MinorGuardianAgeBasedPrivacyConfigurationView": {"x-ticvai-persistence":"marketing.minor_privacy_rule","description":"A stored jurisdiction age rule.","allOf":[{"$ref":"#/components/schemas/MinorGuardianAgeBasedPrivacyConfigurationInput"},{"type":"object","required":["id"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"version":{"type":"integer","minimum":1,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PrivacyConfigurationTestingApprovalPublicationInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"One action on a privacy change set (pack 17.1.10).","required":["action"],"properties":{"changeSetId":{"type":"string","format":"uuid","nullable":true,"description":"Null on the first action, which opens a change set."},"action":{"type":"string","enum":["simulate","validate","submit","publish","rollback"]},"items":{"type":"array","items":{"type":"object","required":["configurationType","configurationId"],"properties":{"configurationType":{"type":"string","enum":["processingPurpose","consentPurpose","communicationPreference","capturePoint","cookieBanner","trackingTechnology","minorPrivacyRule","privacyNotice"]},"configurationId":{"type":"string","format":"uuid"},"version":{"type":"integer","minimum":1}}},"description":"The draft versions in the change set. Required when the set is opened."},"scenario":{"type":"object","description":"For `simulate` (the pack's Test Inputs).","properties":{"country":{"type":"string","pattern":"^[A-Z]{2}$"},"brandId":{"type":"string","format":"uuid","nullable":true},"channel":{"$ref":"#/components/schemas/ConsentSource"},"capturePoint":{"type":"string","nullable":true},"customerAge":{"type":"integer","minimum":0,"nullable":true},"customerStatus":{"type":"string","enum":["new","returning","member"]},"productId":{"type":"string","format":"uuid","nullable":true},"existingConsents":{"type":"array","items":{"$ref":"#/components/schemas/ConsentPurpose"}},"acceptedPolicyVersions":{"type":"array","items":{"type":"string"}},"language":{"type":"string","maxLength":10}}},"publishAt":{"type":"string","format":"date-time","nullable":true,"description":"For `publish`; null publishes now."},"target":{"type":"object","description":"For `publish`; an empty list means all.","properties":{"brandIds":{"type":"array","items":{"type":"string","format":"uuid"}},"countries":{"type":"array","items":{"type":"string","pattern":"^[A-Z]{2}$"}},"channels":{"type":"array","items":{"$ref":"#/components/schemas/ConsentSource"}}}},"reason":{"type":"string","maxLength":1000,"description":"Required for `submit`, `publish` and `rollback`."}}},
"PrivacyConfigurationTestingApprovalPublicationView": {"type":"object","x-ticvai-persistence":"marketing.privacy_change_set","description":"A privacy change set, its validation, approval, publication and audit trail.","required":["changeSetId","status"],"properties":{"changeSetId":{"type":"string","format":"uuid","readOnly":true},"status":{"type":"string","enum":["draft","validated","submitted","approved","scheduled","published","rolledBack","rejected"]},"items":{"type":"array","items":{"type":"object","properties":{"configurationType":{"type":"string"},"configurationId":{"type":"string","format":"uuid"},"version":{"type":"integer"}}}},"validationIssues":{"type":"array","items":{"type":"object","required":["code"],"properties":{"code":{"type":"string","enum":["missingPolicy","missingConsentMapping","missingLanguage","conflictingConsentRules","missingProcessingPurpose","invalidEffectiveDates","unmappedTrackingTechnology","missingGuardianRule","unpublishedDependency","circularDependency"]},"configurationId":{"type":"string","format":"uuid","nullable":true},"message":{"type":"string"}}}},"simulation":{"type":"array","description":"What the scenario's guest would be shown, step by step (from `simulate`; not stored).","items":{"type":"object","required":["item","outcome"],"properties":{"item":{"type":"string","description":"e.g. \"Privacy Notice v5.1\", \"Email Marketing\"."},"outcome":{"type":"string","enum":["display","consentRequired","optional","noConsentRequired","notApplicable","guardianFlow"]},"lawfulBasis":{"type":"string","nullable":true}}}},"approvalRequestId":{"type":"string","nullable":true,"description":"The approvals-engine request, once submitted."},"publishAt":{"type":"string","format":"date-time","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"audit":{"type":"array","items":{"type":"object","required":["action","byPrincipalId","at"],"properties":{"action":{"type":"string"},"byPrincipalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"reason":{"type":"string","nullable":true},"before":{"type":"object","additionalProperties":true,"nullable":true},"after":{"type":"object","additionalProperties":true,"nullable":true}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"PrivacyConsentConfigurationCommandCenterView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.consent_purpose, marketing.consent_capture_point (new), marketing.communication_preference_type (new), the cookie categories and white-label's whitelabel.policy (read through listPolicies)","description":"The privacy command centre's figures for the filters given, and the latest configuration changes. Counts are of items currently in force unless the name says otherwise.","required":["activeConsentPurposes","activePrivacyPolicies","pendingPolicyApprovals","configurationWarnings","configurationDirectory"],"properties":{"activeConsentPurposes":{"type":"integer","minimum":0},"activePrivacyPolicies":{"type":"integer","minimum":0},"communicationPreferenceTypes":{"type":"integer","minimum":0},"cookieCategories":{"type":"integer","minimum":0},"activeConsentCapturePoints":{"type":"integer","minimum":0},"supportedLanguages":{"type":"integer","minimum":0},"pendingPolicyApprovals":{"type":"integer","minimum":0},"scheduledPolicyChanges":{"type":"integer","minimum":0,"description":"Published items with an `effectiveFrom` still in the future."},"consentConfigurationsRequiringReview":{"type":"integer","minimum":0,"description":"Items in `review`, or whose reconfirmation interval has passed."},"configurationWarnings":{"type":"array","maxItems":100,"description":"Configuration checks that failed, most severe first.","items":{"type":"object","required":["code","message"],"properties":{"code":{"type":"string","enum":["capturePointWithoutNotice","purposeWordingDiffersByChannel","purposeWithoutLawfulBasis","translationMissing","policyExpired","other"]},"message":{"type":"string"},"configurationType":{"type":"string","nullable":true},"configurationId":{"type":"string","format":"uuid","nullable":true}}}},"configurationDirectory":{"type":"array","maxItems":50,"description":"The 50 most recently changed configuration items, newest `effectiveFrom` first.","items":{"type":"object","required":["configurationType","configurationId","name","version","status"],"properties":{"configurationType":{"type":"string","enum":["consentPurpose","privacyPolicy","cookieCategory","capturePoint","communicationPreference","minorPrivacy"]},"configurationId":{"type":"string","format":"uuid"},"name":{"type":"string"},"scope":{"type":"string","description":"Where it applies, as the scope path's label (a brand, country or channel)."},"version":{"type":"string"},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["draft","review","approved","scheduled","published","retired"]}}}}}},
"PrivacyNoticeGovernance": {"type":"object","x-ticvai-persistence":"marketing.privacy_notice_governance","description":"**The privacy governance of one version of one privacy document.** The document itself is white-label's `Policy` (`setPolicy`, never overwritten); this row adds what the privacy administrator decides about it: lifecycle status, the change classification (set by an authorised user, **never by AI**), re-acceptance and notification, owner and approval. One row per policy version. Read by `listPrivacyNoticePolicy`; written by `setPrivacyNoticePolicyGovernance` (decided 29 September, writers pass). (decided 29 September, data model for the agreed operations)\n","required":["id","policyId","documentType","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"policyId":{"type":"string","format":"uuid","description":"The white-label `Policy` version this governs (`documentId` on the view)."},"documentType":{"type":"string","enum":["privacyPolicy","privacyNotice","cookieNotice","marketingNotice","biometricPrivacyNotice","childrensPrivacyNotice","locationServicesNotice","other"]},"status":{"type":"string","enum":["draft","review","approved","scheduled","published","superseded","archived"],"default":"draft"},"changeClassification":{"type":"string","enum":["minor","material"],"nullable":true,"description":"Set by an authorised user, never by AI."},"requiresReAcceptance":{"type":"boolean","default":false},"requiresNotification":{"type":"boolean","default":false},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The approvals request raised when the row entered `review` (`setPrivacyNoticePolicyGovernance`); its decision stamps `approvedByPrincipalId` and `approvedAt`. (decided 29 September, writers pass)"},"approvedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"PrivacyNoticePolicyTermsVersionManagementView": {"type":"object","x-ticvai-persistence":"none — projection over whitelabel.policy (read through white-label listPolicies), marketing.privacy_notice_governance and marketing.consent_record","description":"One version of one privacy document, with its governance (pack 17.1.8 Version Information).","required":["documentId","documentType","version","status"],"properties":{"documentId":{"type":"string","format":"uuid"},"documentType":{"type":"string","enum":["privacyPolicy","privacyNotice","cookieNotice","marketingNotice","biometricPrivacyNotice","childrensPrivacyNotice","locationServicesNotice","other"]},"title":{"type":"string"},"version":{"type":"string"},"language":{"type":"string","maxLength":10},"owner":{"type":"string","nullable":true},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["draft","review","approved","scheduled","published","superseded","archived"]},"changeClassification":{"type":"string","enum":["minor","material"],"nullable":true,"description":"Set by an authorised user, never by AI."},"requiresReAcceptance":{"type":"boolean","description":"Guests are asked to accept this version at their next capture point."},"requiresNotification":{"type":"boolean","description":"Guests are told of the change by a transactional message."},"acceptedCount":{"type":"integer","minimum":0,"description":"Guests whose recorded acceptance is of this version."}}},
"RecordCookieScanRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["scannedAt","channel","findings"],"properties":{"scannedAt":{"type":"string","format":"date-time"},"channel":{"$ref":"#/components/schemas/CookieConsentChannel"},"domainApplication":{"type":"string","maxLength":255,"nullable":true,"description":"The domain, or the app and version, scanned."},"scannerRef":{"type":"string","maxLength":200,"nullable":true,"description":"The vendor and scan id where the scanner is bought; null for ours or a manual upload."},"findings":{"type":"array","items":{"type":"object","required":["name","provider","technologyType","isThirdParty"],"properties":{"name":{"type":"string","maxLength":200},"provider":{"type":"string","maxLength":150},"technologyType":{"type":"string","enum":["firstPartyCookie","thirdPartyCookie","mobileSdk","analyticsTracker","advertisingPixel","sessionTechnology","personalisationTechnology","embeddedService","localStorageItem","other"]},"isThirdParty":{"type":"boolean"},"durationDays":{"type":"integer","minimum":0,"nullable":true},"domainApplication":{"type":"string","maxLength":255,"nullable":true},"consentState":{"type":"string","enum":["noDecision","rejectedAll","acceptedAll"],"description":"The consent state the page was loaded in when the technology was seen (CHG-FUP-009). Absent from a scanner that tests one state only; such a finding proves nothing about consent."},"pageUrl":{"type":"string","format":"uri","maxLength":2000,"nullable":true,"description":"The page the technology was seen on."},"initiatorUrl":{"type":"string","format":"uri","maxLength":2000,"nullable":true,"description":"The script or frame that set it, so a violation names its cause (a tag manager, an embed)."},"cookieDomain":{"type":"string","maxLength":255,"nullable":true},"sameSite":{"type":"string","enum":["strict","lax","none"],"nullable":true},"secure":{"type":"boolean","nullable":true},"suggestedCategory":{"allOf":[{"$ref":"#/components/schemas/CookieCategory"}],"nullable":true,"description":"The category the scanner or the catalogue suggests. A suggestion only; the venue's administrator classifies it with `setTrackingTechnology`."},"classificationSource":{"type":"string","enum":["openCookieDatabase","vendor","platformCatalogue","none"],"nullable":true,"description":"Where `suggestedCategory` came from (CHG-FUP-009, CHG-FUP-010)."}}}}}},
"TrackingTechnologyCatalogueEntry": {"type":"object","x-ticvai-persistence":"marketing.tracking_technology_catalogue","description":"**The platform's catalogue of known cookies and trackers** (Chinmay, 2 October, contract follow-ups: \"a platform-wide catalogue of known cookies\"; CHG-FUP-010). One row per known technology, matched on `namePattern` + `provider`, with the category TICVAI's privacy owner approved. Seeded from the Open Cookie Database (Apache-2.0) and curated by platform staff; mastered in the control plane and replicated read-only into every cell with the platform root as `scopePath`, as the platform model catalogue is. **It suggests, it does not decide**: a scan finding that matches takes `suggestedCategory` from it with `classificationSource` `platformCatalogue`, and each venue still approves its own registry entry (`setTrackingTechnology`), so `_ga` is suggested once for every tenant rather than researched by each.","required":["namePattern","provider","category","technologyType"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"entryKey":{"type":"string","readOnly":true,"pattern":"^[a-z0-9][a-z0-9-]{1,119}$","description":"The stable key the entry is written under (`setTrackingTechnologyCatalogueEntry`), such as `google-analytics-ga`; taken from the path."},"namePattern":{"type":"string","maxLength":200,"description":"The cookie or key name, with `*` as a wildcard (`_ga_*`)."},"provider":{"type":"string","maxLength":150},"category":{"$ref":"#/components/schemas/CookieCategory"},"technologyType":{"type":"string","maxLength":40,"description":"As `RecordCookieScanRequest.findings[].technologyType`."},"purpose":{"type":"string","maxLength":1000,"nullable":true},"typicalDurationDays":{"type":"integer","minimum":0,"nullable":true},"isThirdParty":{"type":"boolean","nullable":true},"privacyInformationUrl":{"type":"string","maxLength":2000,"nullable":true},"source":{"type":"string","enum":["openCookieDatabase","platformCuration"],"description":"Imported, or added or corrected by platform staff."},"isActive":{"type":"boolean","default":true,"description":"A retired entry stops suggesting; it is kept for the findings that cited it."},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005): the platform root on every replicated row."}}}
}
```
