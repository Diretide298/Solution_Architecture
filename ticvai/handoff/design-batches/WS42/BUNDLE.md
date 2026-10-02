# WS42 — Privacy  Consent   Preference Management board 2

**10 screens · 14 operations · 22 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AUDIT_VIEW, GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII`. A control nobody can use must say so,
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
| `CMS-031` | Privacy Operations Command Center | B–D | 2 | 26 | 6 | 0 | 1 | 4 | — | notStarted (generated) |
| `CMS-032` | Customer Privacy, Consent & Preference 360° | B–D | 0 | 8 | 6 | 0 | 0 | 4 | — | notStarted (generated) |
| `CMS-033` | Consent Evidence, History & Withdrawal Management | B–D | 0 | 4 | 6 | 1 | 0 | 4 | — | notStarted (generated) |
| `CMS-034` | Data Subject / Customer Privacy Request Management | B–D | 0 | 8 | 6 | 0 | 0 | 4 | — | notStarted (generated) |
| `CMS-035` | Data Discovery, Access, Export & Correction Workspace | B–D | 0 | 4 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `CMS-036` | Deletion, Anonymization & Restriction Operations | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `CMS-037` | Data Retention, Expiry & Legal Hold Operations | B–D | 15 | 12 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `CMS-038` | Privacy Compliance, Exception & Investigation Workspace | B–D | 0 | 40 | 6 | 0 | 0 | 4 | — | notStarted (generated) |
| `CMS-039` | Privacy Audit, Evidence & Compliance Reporting | B–D | 14 | 0 | 5 | 1 | 0 | 4 | — | notStarted (generated) |
| `CMS-040` | Privacy Analytics & AI Compliance Intelligence | B–D | 2 | 26 | 6 | 1 | 0 | 4 | — | notStarted (generated) |

## Thin screens in this batch

**CMS-032, CMS-033, CMS-035 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `CMS-031` Privacy Operations Command Center

**Provide Privacy, Compliance and authorized operational teams with a centralized real-time overview of privacy operations across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/privacy-operations-command-center-cms-031` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Privacy operations overview: KPIs, consent health per category, the request queue by status and stage with deadlines, retention and deletion actions, exceptions, incidents. Separate permissions apply to viewing requests, handling PII and approving deletion.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search privacy operations | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, brand, country, customer, request type, consent purpose and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Brand | picker: choose a brand | — | — | `listPrivacy` ?brandId |
| Country | text field | — | pattern `^[A-Z]{2}$` | `listPrivacy` ?country |
| Request type | text field | — | max length 60 | `listPrivacy` ?requestType |
| Consent purpose | select | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | `listPrivacy` ?consentPurpose |
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listPrivacy` ?channel |
| Owner principal | picker: choose an owner principal | — | — | `listPrivacy` ?ownerPrincipalId |
| From | date and time picker | — | — | `listPrivacy` ?from |
| To | date and time picker | — | — | `listPrivacy` ?to |

#### Outputs: what the screen shows and produces

**Shown**

**Every privacy operations** (data table, from `listPrivacy`)

| Shows | Format | Notes |
|---|---|---|
| Total customer privacy profiles | 1,234 | — |
| Active consent records | 1,234 | — |
| Withdrawn consents | 1,234 | — |
| Marketing opt ins | 1,234 | — |
| Marketing opt outs | 1,234 | — |
| Pending data rights requests | 1,234 | Requests not yet `completed`. |
| Overdue requests | 1,234 | — |
| Pending deletion actions | 1,234 | — |
| Pending anonymization | 1,234 | — |
| Retention actions due | 1,234 | Records inside the 90-day notice window before their retention action (ADR-0047 §6). |
| Consent evidence exceptions | 1,234 | — |
| Privacy incidents exceptions | 1,234 | Open privacy exceptions plus open privacy incidents. |
| Policy re acceptance pending | 1,234 | Customers whose accepted notice version has been superseded. |

**The selected privacy operations** (detail panel): The pack groups this record's detail under its own headings: “Show breakdown by”, “Provide visibility into”.

| Shows | Format | Notes |
|---|---|---|
| Total customer privacy profiles | 1,234 | — |
| Active consent records | 1,234 | — |
| Withdrawn consents | 1,234 | — |
| Marketing opt ins | 1,234 | — |
| Marketing opt outs | 1,234 | — |
| Pending data rights requests | 1,234 | Requests not yet `completed`. |
| Overdue requests | 1,234 | — |
| Pending deletion actions | 1,234 | — |
| Pending anonymization | 1,234 | — |
| Retention actions due | 1,234 | Records inside the 90-day notice window before their retention action (ADR-0047 §6). |
| Consent evidence exceptions | 1,234 | — |
| Privacy incidents exceptions | 1,234 | Open privacy exceptions plus open privacy incidents. |
| Policy re acceptance pending | 1,234 | Customers whose accepted notice version has been superseded. |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Search Customer, Open Privacy Profile, Create Privacy Request, Review Withdrawal, Run Retention, Investigate Evidence, Export Compliance Report. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listPrivacy` (onLoad, Privacy Operations Command Center)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-032` Customer Privacy, Consent & Preference 360°: *Works in Customer Privacy, Consent & Preference 360°*; calls `listPrivacy`
- → `CMS-033` Consent Evidence, History & Withdrawal Management: *Works in Consent Evidence, History & Withdrawal Management*; calls `listPrivacy`
- → `CMS-034` Data Subject / Customer Privacy Request Management: *Works in Data Subject / Customer Privacy Request Management*; calls `listPrivacy`
- → `CMS-035` Data Discovery, Access, Export & Correction Workspace: *Works in Data Discovery, Access, Export & Correction Workspace*; calls `listPrivacy`
- → `CMS-036` Deletion, Anonymization & Restriction Operations: *Works in Deletion, Anonymization & Restriction Operations*; calls `listPrivacy`
- → `CMS-037` Data Retention, Expiry & Legal Hold Operations: *Works in Data Retention, Expiry & Legal Hold Operations*; calls `listPrivacy`
- → `CMS-038` Privacy Compliance, Exception & Investigation Workspace: *Works in Privacy Compliance, Exception & Investigation Workspace*; calls `listPrivacy`
- → `CMS-039` Privacy Audit, Evidence & Compliance Reporting: *Works in Privacy Audit, Evidence & Compliance Reporting*; calls `listPrivacy`
- → `CMS-040` Privacy Analytics & AI Compliance Intelligence: *Works in Privacy Analytics & AI Compliance Intelligence*; calls `listPrivacy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The privacy operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the privacy operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No privacy operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the privacy operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-744`: Same queue and counts; one owner.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  openRequests: 7
  dueThisWeek: 3
  consentHealthMarketing: 61%
  incidents: 0
```

#### Permissions

- `listPrivacy` → `GUEST_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-031` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-031`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 2
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 1: Opens Privacy Operations Command Center → Provide Privacy, Compliance and authorized operational teams with a centralized real-time overview of privacy operations across TICVAI.
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F151 branch at step 1 (expected): when Nothing has been set up on Privacy Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F151 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-031?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-001`, `CMS-032`, `CMS-033`, `CMS-034`, `CMS-035`, `CMS-036`, `CMS-037`, `CMS-038`, `CMS-039`, `CMS-040`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-032` Customer Privacy, Consent & Preference 360°

**Provide one authoritative privacy view for an individual customer or participant. This becomes the privacy equivalent of the customer 360° workspace. n ed el**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW_PII` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/customer-privacy-consent-preference-360-cms-032` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** One guest's whole privacy relationship: consent per purpose and channel (Given, Withdrawn, Not asked), source and notice version of each, preferences, accepted policies, cookie decisions claimed, data requests and retention status. Needs PII permission.

**Known correction pending (do not draw the wrong version)**

- **Drawn as a table of "every customer privacy consent".** Why: The 360 is one guest; open it from a search. *(source: screens/P13-white-label-cms.yaml#CMS-032; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Subject | picker: choose a subject | — | — | `listCustomerPrivacyConsent` ?subjectId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every customer privacy consent** (data table, from `listCustomerPrivacyConsent`)

| Shows | Format | Notes |
|---|---|---|
| Document type | chip: Privacy policy, Cookie notice, Biometric notice, Childrens privacy notice, Other | — |
| Accepted version | text | — |
| Current version | text | — |
| Requires reacceptance | yes / no (icon or chip) | — |

**The selected customer privacy consent** (detail panel): The pack groups this record's detail under its own headings: “Display appropriate information such as”, “Email Consente”, “SMS Withdraw”, “Consente”, “Personalizatio”, “Show current”.

| Shows | Format | Notes |
|---|---|---|
| Document type | chip: Privacy policy, Cookie notice, Biometric notice, Childrens privacy notice, Other | — |
| Accepted version | text | — |
| Current version | text | — |
| Requires reacceptance | yes / no (icon or chip) | — |

**Data it reads**: `listCustomerPrivacyConsent` (onLoad, Customer Privacy, Consent & Preference 360°)

**Where the user goes next**

- → `CMS-031` Privacy Operations Command Center: *Returns to the board's landing screen*; calls `listCustomerPrivacyConsent`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer privacy consent list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer privacy consent untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer privacy consent yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer privacy consent are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
guest: Sarah Thompson - Marketing email Given (checkout, v4, 1 Oct 2026) - WhatsApp Not asked - Privacy policy v4
  accepted - 1 open request
```

#### Permissions

- `listCustomerPrivacyConsent` → `GUEST_VIEW_PII` (operate) · staff

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

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-032` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-032`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 2
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 2: Works in Customer Privacy, Consent & Preference 360° → Provide one authoritative privacy view for an individual customer or participant. This becomes the privacy equivalent of the customer 360° workspace. n ed el

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-032?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-031`.
- [ ] Every gated control is gated: `GUEST_VIEW_PII`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-033` Consent Evidence, History & Withdrawal Management

**Maintain legally and operationally useful evidence of every consent event and manage subsequent withdrawals.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/consent-evidence-history-withdrawal-management-cms-033` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Evidence of every consent event (presented, granted, declined, updated, withdrawn, expired, reconfirmed) and where each withdrawal has reached the downstream systems, plus the cookie decisions of visitors before they signed in.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Subject | picker: choose a subject | — | — | `listConsentEvidenceWithdrawal` ?subjectId |
| Consent purpose | select | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | `listConsentEvidenceWithdrawal` ?consentPurpose |
| Event | select | — | Presented · Granted · Declined · Updated · Withdrawn · Expired · Reconfirmed · Superseded | `listConsentEvidenceWithdrawal` ?event |
| Source | select | — | Guest app · Website · Kiosk · POS · Call centre · Import · Agent recorded · Cookie banner · Checkout | `listConsentEvidenceWithdrawal` ?source |
| Brand | picker: choose a brand | — | — | `listConsentEvidenceWithdrawal` ?brandId |
| Country | text field | — | pattern `^[A-Z]{2}$` | `listConsentEvidenceWithdrawal` ?country |
| Propagation status | select | — | Requested · Processed · Propagated · Acknowledged · Failed · Retry required | `listConsentEvidenceWithdrawal` ?propagationStatus |
| From | date and time picker | — | — | `listConsentEvidenceWithdrawal` ?from |
| To | date and time picker | — | — | `listConsentEvidenceWithdrawal` ?to |
| Channel | select | — | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | `listDeviceConsents` ?channel |
| Brand | picker: choose a brand | — | — | `listDeviceConsents` ?brandId |
| Action | radio group | — | Accept all · Reject non essential · Save preferences · Withdraw · Do not sell or share | `listDeviceConsents` ?action |
| Category | radio group | — | Strictly necessary · Functional · Analytics · Personalisation · Marketing | `listDeviceConsents` ?category |
| Country | text field | — | pattern `^[A-Z]{2}$` | `listDeviceConsents` ?country |
| Claimed | toggle | — | — | `listDeviceConsents` ?claimed |
| Consent key | text field | — | — | `listDeviceConsents` ?consentKey |
| … 2 more | | | | `operations.json` |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every consent evidence history** (data table, from `listConsentEvidenceWithdrawal`)

| Shows | Format | Notes |
|---|---|---|
| Target | chip: Crm, Marketing, Campaign audience, Connected system | — |
| Status | chip: Requested, Processed, Propagated, Acknowledged, Failed, Retry required | — |

**The selected consent evidence history** (detail panel): The pack groups this record's detail under its own headings: “Consent Evidence Record”, “Evidence Principle”, “Withdrawal”, “Central Consent Engine”.

| Shows | Format | Notes |
|---|---|---|
| Target | chip: Crm, Marketing, Campaign audience, Connected system | — |
| Status | chip: Requested, Processed, Propagated, Acknowledged, Failed, Retry required | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Withdrawal propagation**: Per withdrawal, each system it must reach (campaigns, journeys, providers) and whether it has. *(source: contracts/satellite/marketing-crm.yaml#listConsentEvidenceWithdrawal; contracts/satellite/marketing-crm.yaml#/components/schemas/ConsentPropagation)*

**Data it reads**: `listConsentEvidenceWithdrawal` (onLoad, Consent Evidence, History & Withdrawal Management); `listDeviceConsents` (onLoad, Visitors' cookie decisions as evidence)

**Where the user goes next**

- → `CMS-031` Privacy Operations Command Center: *Returns to the board's landing screen*; calls `listConsentEvidenceWithdrawal`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The consent evidence history list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the consent evidence history untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No consent evidence history yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the consent evidence history are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
event: Rahul Menon - Marketing WhatsApp - withdrawn 1 Oct 2026 09:14 (in app) - campaigns done, journeys done, WhatsApp
  provider list pending
```

#### Permissions

- `listConsentEvidenceWithdrawal` → `GUEST_VIEW` (read) · staff
- `listDeviceConsents` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.56 | Consent Audit Trail Maintain complete consent history. Track: - Initial consent - Updates to preferences - Consent withdrawals Generate audit reports for compliance reviews. | Ticketing Sales | CONTRACTED | `listDeviceConsents` |

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-033` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-033`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 2
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 4: Works in Consent Evidence, History & Withdrawal Management → Maintain legally and operationally useful evidence of every consent event and manage subsequent withdrawals.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-033?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-031`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-034` Data Subject / Customer Privacy Request Management

**Provide a governed case-management workflow for customer privacy requests.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/data-subject-customer-privacy-request-management-cms-034` |

**Known gaps.** **The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Email/manual entry, POS, API, Authorized Representative, ID Review where permitted. Each needs an operation …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Governed handling of privacy requests from customers, guardians or representatives received via portal, email, customer service, POS or API: identity review, statutory deadline, stage, owner. Status uses the meeting lifecycle submitted, in progress, completed.

**Fixed on main** (the package already carries these; draw what it says): The action bar lists intake channels (Customer Portal, POS, API, Authorized Representative) as buttons, and no write is declared. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | segmented control | — | Submitted · In progress · Completed | `listDataSubjectCustomer` ?status |
| Request type | text field | — | max length 60 | `listDataSubjectCustomer` ?requestType |
| Subject | picker: choose a subject | — | — | `listDataSubjectCustomer` ?subjectId |
| Jurisdiction | text field | — | pattern `^[A-Z]{2}$` | `listDataSubjectCustomer` ?jurisdiction |
| Sla state | radio group | — | On track · At risk · Overdue · Escalated · No deadline | `listDataSubjectCustomer` ?slaState |
| Owner principal | picker: choose an owner principal | — | — | `listDataSubjectCustomer` ?ownerPrincipalId |
| From | date and time picker | — | — | `listDataSubjectCustomer` ?from |
| To | date and time picker | — | — | `listDataSubjectCustomer` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every data subject customer** (data table, from `listDataSubjectCustomer`)

| Shows | Format | Notes |
|---|---|---|
| Days remaining | 1,234 | Negative once overdue; null without a deadline. |
| At risk | yes / no (icon or chip) | Inside the request type's configured warning window before `dueAt`. |
| Overdue | text | not in the schema: `Overdue` |
| Escalated | text | not in the schema: `Escalated` |

**The selected data subject customer** (detail panel): The pack groups this record's detail under its own headings: “Configurable request types may include”, “Guardian / Representative”.

| Shows | Format | Notes |
|---|---|---|
| Days remaining | 1,234 | Negative once overdue; null without a deadline. |
| At risk | yes / no (icon or chip) | Inside the request type's configured warning window before `dueAt`. |
| Overdue | text | not in the schema: `Overdue` |
| Escalated | text | not in the schema: `Escalated` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Customer Portal (primary button) | navigation or local | — | — | — | — |
| Email/manual entry (secondary button) | navigation or local | — | — | — | — |
| Customer Service (secondary button) | navigation or local | — | — | — | — |
| POS (secondary button) | navigation or local | — | — | — | — |
| API (secondary button) | navigation or local | — | — | — | — |
| Authorized Representative (secondary button) | navigation or local | — | — | — | — |
| ID Review where permitted (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listDataSubjectCustomer` (onLoad, Data Subject / Customer Privacy Request Management)

**Where the user goes next**

- → `CMS-031` Privacy Operations Command Center: *Returns to the board's landing screen*; calls `listDataSubjectCustomer`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data subject customer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data subject customer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data subject customer yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data subject customer are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-750`: Same queue; one owner.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
requests:
- DR-2026-00431 - erasure - via app - submitted 1 Oct - due 31 Oct
- DR-2026-00419 - access - via email by representative - ID review
```

#### Permissions

- `listDataSubjectCustomer` → `GUEST_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-034` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-034`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 2
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 6: Works in Data Subject / Customer Privacy Request Management → Provide a governed case-management workflow for customer privacy requests.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-034?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Customer Portal, Email/manual entry, Customer Service, POS, API, Authorized Representative, ID Review where permitted.
- [ ] Every transition is wired: `CMS-031`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-035` Data Discovery, Access, Export & Correction Workspace

**Allow authorized privacy teams to locate customer data across TICVAI and connected systems when fulfilling access, export or correction requests.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW_PII` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/data-discovery-access-export-correction-workspace-cms-035` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Locate a guest's data across systems to fulfil access, export or correction requests: discovery results per system, the export package (excluding other guests' data sharing a booking), and correction routing.

**Known correction pending (do not draw the wrong version)**

- **The list is bound to setDataDiscoveryAccess (a write).** Why: Needs a read of the request's discovery. *(source: contracts/satellite/marketing-crm.yaml#setDataDiscoveryAccess; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every data discovery access** (data table, from `setDataDiscoveryAccess`)

| Shows | Format | Notes |
|---|---|---|
| Source | text | A value of the input's `sources`. |
| Record count | 1,234 | — |

**The selected data discovery access** (detail panel): The pack groups this record's detail under its own headings: “Search using”, “Potential sources”, “Export Package”, “Correction”, “Before release”.

| Shows | Format | Notes |
|---|---|---|
| Source | text | A value of the input's `sources`. |
| Record count | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-031` Privacy Operations Command Center: *Returns to the board's landing screen*; calls `setDataDiscoveryAccess`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data discovery access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data discovery access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data discovery access yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data discovery access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 The request is not an access, export or correction request, is not `inProgress`, its identity is not verified, or the approver is the principal who generated … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
discovery: DR-2026-00412 - found in CRM, Orders (14), Wallet (3), Cases (2), Marketing (41 dispatches) - export
  PDF ready
```

#### Permissions

- `setDataDiscoveryAccess` → `GUEST_VIEW_PII` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-035` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-035`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 2
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 8: Works in Data Discovery, Access, Export & Correction Workspace → Allow authorized privacy teams to locate customer data across TICVAI and connected systems when fulfilling access, export or correction requests.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404, 422).
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-035?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `CMS-031`.
- [ ] Every gated control is gated: `GUEST_VIEW_PII`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-036` Deletion, Anonymization & Restriction Operations

**Govern privacy requests or policies requiring personal data to be deleted, anonymized or restricted. This screen requires strong controls because deletion may affect financial, ticketing, fraud, legal and operational records.**

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
| Route | `/policy/deletion-anonymization-restriction-operations-cms-036` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Delete, Pseudonymize where configured, Remove Biometric Reference. Each needs an operation, or needs … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Governed deletion, anonymisation, pseudonymisation, restriction, suppression and biometric removal, with strong controls because deletion touches financial, ticketing, fraud and legal records: ledger entries keep an anonymous reference; a biometric template is destroyed, not flagged.

**Known correction pending (do not draw the wrong version)**

- **Delete, Pseudonymize, Restrict and Remove Biometric buttons have no operation; only a list is declared.** Why: The actions cannot be performed or approved. *(source: contracts/satellite/marketing-crm.yaml#listDeletionAnonymizationRestriction; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Action type | select | — | Delete · Anonymise · Pseudonymise · Restrict processing · Suppress marketing · Remove biometric reference · Disconnect third party profile · Other | `listDeletionAnonymizationRestriction` ?actionType |
| Status | select | — | Planned · Awaiting approval · Approved · Rejected · Executing · Completed · Completed with retention · Failed · Manual action required · Cancelled | `listDeletionAnonymizationRestriction` ?status |
| Subject | picker: choose a subject | — | — | `listDeletionAnonymizationRestriction` ?subjectId |
| Request | picker: choose a request | — | — | `listDeletionAnonymizationRestriction` ?requestId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Delete (destructive button) | navigation or local | — | — | — | — |
| Pseudonymize where configured (secondary button) | navigation or local | — | — | — | — |
| Restrict Processing (secondary button) | navigation or local | — | — | — | — |
| Remove Biometric Reference (destructive button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Impact preview**: What will be deleted, what is anonymised, what is kept and why (legal hold, finance). *(source: contracts/satellite/marketing-crm.yaml#listDeletionAnonymizationRestriction; contracts/spine/identity.yaml#deleteGuestAccount)*

**Data it reads**: `listDeletionAnonymizationRestriction` (onLoad, Deletion, Anonymization & Restriction Operations)

**Where the user goes next**

- → `CMS-031` Privacy Operations Command Center: *Returns to the board's landing screen*; calls `listDeletionAnonymizationRestriction`

**What opens over it**

- confirmDialog *Delete*: **Delete on a deletion anonymization restriction is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Remove Biometric Reference*: **Remove Biometric Reference on a deletion anonymization restriction is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The deletion anonymization restriction list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deletion anonymization restriction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No deletion anonymization restriction yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the deletion anonymization restriction are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
action: Erase Rahul Menon - delete profile and documents, anonymise 14 orders, remove Face Pass - approval by DPO
```

#### Permissions

- `listDeletionAnonymizationRestriction` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-036` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-036`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 2
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 10: Works in Deletion, Anonymization & Restriction Operations → Govern privacy requests or policies requiring personal data to be deleted, anonymized or restricted. This screen requires strong controls because deletion may affect financial, ticketing, fraud …
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-036?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Delete, Pseudonymize where configured, Restrict Processing, Remove Biometric Reference.
- [ ] Every transition is wired: `CMS-031`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-037` Data Retention, Expiry & Legal Hold Operations

**Operationalize retention policies associated with Board 1 processing purposes and data categories.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/data-retention-expiry-legal-hold-operations-cms-037` |

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Review, Extend where authorized, Delete, Archive, Place Hold, Release Hold. Each needs an operation, or …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** What retention will do next, per policy, and the holds that stop it: review, extend where authorised, archive, delete, place and release legal holds.

**Fixed on main** (the package already carries these; draw what it says): Review, Extend, Archive, Delete, Place Hold and Release Hold have no operation. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Data category | text field | — | — | `listDataRetentionExpiry` ?dataCategory |
| Jurisdiction | text field | — | pattern `^[A-Z]{2}$` | `listDataRetentionExpiry` ?jurisdiction |
| Hold status | segmented control | — | Pending approval · Active · Released | `listDataRetentionExpiry` ?holdStatus |

**Form: Run retention** (modal, opened by *Run retention*; *Run retention* calls `runDataRetention`, *Cancel* sends nothing)

**Collects what `runDataRetention` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Policy `policyId` | picker: choose a policy | optional | — | — | shows names, sends the id | — | `runDataRetention` body |
| Mode `mode` | segmented control | optional | Preview | Preview · Execute | — | — | `runDataRetention` body |
| As of `asOf` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `runDataRetention` body |

**Form: Place or release hold** (modal, opened by *Place or release hold*; *Place or release hold* calls `setLegalHold`, *Cancel* sends nothing)

**Collects what `setLegalHold` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | optional | Legal | Legal · Operational · Fraud investigation · Regulator request | — | — | `setLegalHold` body |
| Reason `reason` | text area | required | — | max length 1000 | — | — | `setLegalHold` body |
| Scope `scope` | group | required | — | — | — | At least one selector. | `setLegalHold` body |
| Subjects `scope.subjectIds` | multi-picker: choose subjects | optional | — | — | — | — | `setLegalHold` body |
| Data categories `scope.dataCategories` | list of values (chips) | optional | — | — | — | — | `setLegalHold` body |
| Retention policy codes `scope.retentionPolicyCodes` | list of values (chips) | optional | — | — | — | — | `setLegalHold` body |
| Case `scope.caseId` | picker: choose a case | optional | — | — | shows names, sends the id | — | `setLegalHold` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `setLegalHold` body |
| Starts at `startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Defaults to approval time. | `setLegalHold` body |
| Review date `reviewDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setLegalHold` body |
| Status `status` | segmented control | optional | Pending approval | Pending approval · Active · Released | — | Set `active` to approve, `released` to release. | `setLegalHold` body |
| Release reason `releaseReason` | text area | optional | — | max length 1000 | — | — | `setLegalHold` body |

Errors to draw in the form: 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 Approved by the principal who placed it, released without a reason, or a change to a released hold.

#### Outputs: what the screen shows and produces

**Shown**

**Every data retention expiry** (data table, from `listDataRetentionExpiry`)

| Shows | Format | Notes |
|---|---|---|
| Records approaching expiry | 1,234 | Inside the 90-day notice window before their retention action. |
| Eligible for deletion | 1,234 | — |
| Eligible for anonymization | 1,234 | — |
| Under legal hold | 1,234 | — |
| Processing failures | 1,234 | — |
| Retention exceptions | 1,234 | Open `retentionFailure` / `deletionFailure` privacy exceptions. |

**The selected data retention expiry** (detail panel): The pack groups this record's detail under its own headings: “Hold information includes”, “Retention jobs may run”, “Dry Run”.

| Shows | Format | Notes |
|---|---|---|
| Records approaching expiry | 1,234 | Inside the 90-day notice window before their retention action. |
| Eligible for deletion | 1,234 | — |
| Eligible for anonymization | 1,234 | — |
| Under legal hold | 1,234 | — |
| Processing failures | 1,234 | — |
| Retention exceptions | 1,234 | Open `retentionFailure` / `deletionFailure` privacy exceptions. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Review (primary button) | navigation or local | — | — | — | — |
| Extend where authorized (secondary button) | navigation or local | — | — | — | — |
| Delete (destructive button) | navigation or local | — | — | — | — |
| Archive (destructive button) | navigation or local | — | — | — | — |
| Place Hold (secondary button) | navigation or local | — | — | — | — |
| Release Hold (secondary button) | navigation or local | — | — | — | — |
| Run retention (secondary button) | `runDataRetention` POST `/retention-runs` | inline | RetentionRunResult | — | opens modal first |
| Place or release hold (secondary button) | `setLegalHold` PUT `/data-retention-expiry` | PrivacyLegalHold | PrivacyLegalHold | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 Approved by the principal who placed it, released without a reason, or a change to a … | opens modal first |

**Data it reads**: `listDataRetentionExpiry` (onLoad, Data Retention, Expiry & Legal Hold Operations)

**Where the user goes next**

- → `CMS-031` Privacy Operations Command Center: *Returns to the board's landing screen*; calls `listDataRetentionExpiry`

**What opens over it**

- confirmDialog *Delete*: **Delete on a data retention expiry is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Archive*: **Archive on a data retention expiry is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data retention expiry list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data retention expiry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data retention expiry yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data retention expiry are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 Approved by the principal who placed it, released without a reason, or a change to a released hold. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
next: 1,204 inactive profiles reach 5 years on 1 Nov 2026 - anonymise - 3 on legal hold
```

#### Permissions

- `listDataRetentionExpiry` → `GUEST_VIEW` (read) · staff
- `runDataRetention` → `GUEST_MANAGE` (configure) · staff
- `setLegalHold` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-037` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-037`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 2
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 12: Works in Data Retention, Expiry & Legal Hold Operations → Operationalize retention policies associated with Board 1 processing purposes and data categories.
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-037?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Review, Extend where authorized, Delete, Archive, Place Hold, Release Hold, Run retention, Place or release hold.
- [ ] Every transition is wired: `CMS-031`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-038` Privacy Compliance, Exception & Investigation Workspace

**Provide a centralized workspace for privacy configuration and operational exceptions requiring investigation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/privacy-compliance-exception-investigation-workspace-cms-038` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Security, Operations, Data Owner. Each needs an operation, or needs removing from the screen; this is the …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Privacy exceptions (configuration and operational) investigated through detected, triaged, assigned, investigated, corrective action, reviewed and closed, with security, operations and data-owner involvement.

**Fixed on main** (the package already carries these; draw what it says): The list is bound to setPrivacyComplianceException (a write); buttons are team names. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | select | — | Missing consent evidence · Consent propagation failure · Marketing after withdrawal · Policy version mismatch · Missing guardian consent · Retention failure · Deletion failure · Unknown tracking technology · Unauthorised data access · Unmapped processing … | `listPrivacyComplianceExceptions` ?category |
| Severity | radio group | — | Low · Medium · High · Critical | `listPrivacyComplianceExceptions` ?severity |
| Status | select | — | Detected · Triaged · Assigned · Investigated · Corrective action · Reviewed · Closed | `listPrivacyComplianceExceptions` ?status |
| Owner principal | picker: choose an owner principal | — | — | `listPrivacyComplianceExceptions` ?ownerPrincipalId |
| Subject | picker: choose a subject | — | — | `listPrivacyComplianceExceptions` ?subjectId |
| Brand | picker: choose a brand | — | — | `listPrivacyComplianceExceptions` ?brandId |
| Country | text field | — | pattern `^[A-Z]{2}$` | `listPrivacyComplianceExceptions` ?country |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every privacy compliance exception** (data table, from `setPrivacyComplianceException`)

| Shows | Format | Notes |
|---|---|---|
| Severity | chip: Low, Medium, High, Critical | — |
| Category | chip: Missing consent evidence, Consent propagation failure, Marketing after withdrawal … | — |
| Subject | the name it points at, never the id | — |
| System | text | — |
| Brand | the name it points at, never the id | — |
| Country | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Owner principal | the name it points at, never the id | — |
| Sla due at | 1 Oct 2026, 14:30 | From the SLA policy for the severity (`setSlaPolicy`). |
| Status | chip: Detected, Triaged, Assigned, Investigated, Corrective action, Reviewed… | — |

**Privacy exceptions** (data table, from `listPrivacyComplianceExceptions`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | Absent to raise; present to update. |
| Category | chip: Missing consent evidence, Consent propagation failure, Marketing after withdrawal … | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Summary | text | — |
| Subject | the name it points at, never the id | — |
| System | text | — |
| Brand | the name it points at, never the id | — |
| Country | text | — |
| Owner principal | the name it points at, never the id | — |
| Status | chip: Detected, Triaged, Assigned, Investigated, Corrective action, Reviewed… | — |
| Related evidences | list or chips (count when long) | Consent evidence ids and audit event ids. |
| Policy reference | text | The configuration or policy version involved. |
| Root cause | text | — |
| Corrective action | text | — |
| Notes | text | — |
| Attachment assets | list or chips (count when long) | — |
| Escalated to | chip: Privacy, Legal, Security, It, Marketing, Operations… | — |
| Privacy incident | the name it points at, never the id | The `recordPrivacyIncident` record, when the exception is also a breach. |
| Detected at | 1 Oct 2026, 14:30 | — |

**The selected privacy compliance exception** (detail panel): The pack groups this record's detail under its own headings: “Provide”, “Workflow”, “Important Boundary”.

| Shows | Format | Notes |
|---|---|---|
| Severity | chip: Low, Medium, High, Critical | — |
| Category | chip: Missing consent evidence, Consent propagation failure, Marketing after withdrawal … | — |
| Subject | the name it points at, never the id | — |
| System | text | — |
| Brand | the name it points at, never the id | — |
| Country | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Owner principal | the name it points at, never the id | — |
| Sla due at | 1 Oct 2026, 14:30 | From the SLA policy for the severity (`setSlaPolicy`). |
| Status | chip: Detected, Triaged, Assigned, Investigated, Corrective action, Reviewed… | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Security (primary button) | navigation or local | — | — | — | — |
| Operations (secondary button) | navigation or local | — | — | — | — |
| Data Owner (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPrivacyComplianceExceptions` (onLoad, The privacy exception queue)

**Where the user goes next**

- → `CMS-031` Privacy Operations Command Center: *Returns to the board's landing screen*; calls `setPrivacyComplianceException`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The privacy compliance exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the privacy compliance exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No privacy compliance exception yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the privacy compliance exception are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 Closed without root cause and corrective action, or a change to a closed exception. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
exception: Marketing SMS sent to 12 guests with withdrawn consent - corrective action - provider list sync fixed
```

#### Permissions

- `setPrivacyComplianceException` → `GUEST_MANAGE` (configure) · staff
- `listPrivacyComplianceExceptions` → `GUEST_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-038` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-038`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 2
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 14: Works in Privacy Compliance, Exception & Investigation Workspace → Provide a centralized workspace for privacy configuration and operational exceptions requiring investigation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-038?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Security, Operations, Data Owner.
- [ ] Every transition is wired: `CMS-031`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-039` Privacy Audit, Evidence & Compliance Reporting

**Provide immutable auditability and management/compliance reporting across privacy operations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AUDIT_VIEW`, `GUEST_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture significant activities such as) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/privacy-audit-evidence-compliance-reporting-cms-039` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The immutable privacy audit trail and compliance reports: consent granted and withdrawn, preferences, policy acceptance, requests, identity checks, exports, corrections, deletions, anonymisation, retention, holds, overrides and configuration changes; visitor cookie decisions as evidence.

**Known correction pending (do not draw the wrong version)**

- **Event types are drawn as select fields in a configEditor.** Why: They are filters on a read-only list. *(source: screens/P13-white-label-cms.yaml#CMS-039; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Consent Granted | select field | — | — | — | — | — | — |
| Consent Withdrawn | select field | — | — | — | — | — | — |
| Preference Changed | select field | — | — | — | — | — | — |
| Policy Accepted | select field | — | — | — | — | — | — |
| Privacy Request Created | select field | — | — | — | — | — | — |
| Identity Verified | select field | — | — | — | — | — | — |
| Data Export Generated | select field | — | — | — | — | — | — |
| Correction Requested | select field | — | — | — | — | — | — |
| Deletion Approved | select field | — | — | — | — | — | — |
| Anonymization Executed | select field | — | — | — | — | — | — |
| Retention Action | select field | — | — | — | — | — | — |
| Legal Hold | select field | — | — | — | — | — | — |
| Administrative Override | select field | — | — | — | — | — | — |
| Configuration Change | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Action | select | — | Consent granted · Consent withdrawn · Preference changed · Policy accepted · Privacy request created · Identity verified · Data export generated · Correction requested · Deletion approved · Anonymisation executed · Retention action · Legal hold … | `listPrivacyEvidenceCompliance` ?action |
| Report | select | — | Consent status · Consent withdrawal · Marketing permission · Privacy request sla · Deletion anonymisation · Retention · Policy acceptance · Minor guardian privacy · Cookie tracking compliance · Biometric privacy · Exception | `listPrivacyEvidenceCompliance` ?report |
| Subject | picker: choose a subject | — | — | `listPrivacyEvidenceCompliance` ?subjectId |
| Request | picker: choose a request | — | — | `listPrivacyEvidenceCompliance` ?requestId |
| Actor principal | picker: choose an actor principal | — | — | `listPrivacyEvidenceCompliance` ?actorPrincipalId |
| From | date and time picker | — | — | `listPrivacyEvidenceCompliance` ?from |
| To | date and time picker | — | — | `listPrivacyEvidenceCompliance` ?to |
| Channel | select | — | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | `listDeviceConsents` ?channel |
| Brand | picker: choose a brand | — | — | `listDeviceConsents` ?brandId |
| Action | radio group | — | Accept all · Reject non essential · Save preferences · Withdraw · Do not sell or share | `listDeviceConsents` ?action |
| Category | radio group | — | Strictly necessary · Functional · Analytics · Personalisation · Marketing | `listDeviceConsents` ?category |
| Country | text field | — | pattern `^[A-Z]{2}$` | `listDeviceConsents` ?country |
| Claimed | toggle | — | — | `listDeviceConsents` ?claimed |
| Consent key | text field | — | — | `listDeviceConsents` ?consentKey |
| From | date and time picker | — | — | `listDeviceConsents` ?from |
| To | date and time picker | — | — | `listDeviceConsents` ?to |

#### Outputs: what the screen shows and produces

**Data it reads**: `listPrivacyEvidenceCompliance` (onLoad, Privacy Audit, Evidence & Compliance Reporting); `listDeviceConsents` (onLoad, Cookie consent log for compliance reports)

**Where the user goes next**

- → `CMS-031` Privacy Operations Command Center: *Returns to the board's landing screen*; calls `listPrivacyEvidenceCompliance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The privacy audit evidence configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the privacy audit evidence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No privacy audit evidence configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-753`: Same trail.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entry: 1 Oct 2026 09:14 - Consent withdrawn - Rahul Menon - Marketing WhatsApp - source guestApp - notice v4
```

#### Permissions

- `listPrivacyEvidenceCompliance` → `AUDIT_VIEW` (read) · staff
- `listDeviceConsents` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.56 | Consent Audit Trail Maintain complete consent history. Track: - Initial consent - Updates to preferences - Consent withdrawals Generate audit reports for compliance reviews. | Ticketing Sales | CONTRACTED | `listDeviceConsents` |

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-039` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-039`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 2
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 16: Works in Privacy Audit, Evidence & Compliance Reporting → Provide immutable auditability and management/compliance reporting across privacy operations.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-039?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-031`.
- [ ] Every gated control is gated: `AUDIT_VIEW`, `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-040` Privacy Analytics & AI Compliance Intelligence

**Provide executives, Privacy Officers and Compliance teams with actionable privacy analytics and AI-assisted risk detection. This should be the intelligence layer across both Privacy Boards.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Policy · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AUDIT_VIEW`, `GUEST_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/policy/privacy-analytics-ai-compliance-intelligence-cms-040` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Privacy analytics and AI-assisted risk detection for executives and the privacy officer: consent rates, request resolution and SLA, deletion and retention, with AI findings a human investigates.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search privacy analytics compliance | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, brand, country, venue, channel, consent purpose and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listPrivacyCompliance` ?from |
| To | date and time picker | — | — | `listPrivacyCompliance` ?to |
| Brand | picker: choose a brand | — | — | `listPrivacyCompliance` ?brandId |
| Country | text field | — | pattern `^[A-Z]{2}$` | `listPrivacyCompliance` ?country |
| Channel | select | — | Guest app · Website · Kiosk · POS · Call centre · Import · Agent recorded · Cookie banner · Checkout | `listPrivacyCompliance` ?channel |
| Consent purpose | select | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | `listPrivacyCompliance` ?consentPurpose |
| Segment | picker: choose a segment | — | — | `listPrivacyCompliance` ?segmentId |
| Product | picker: choose a product | — | — | `listPrivacyCompliance` ?productId |
| Policy version | text field | — | — | `listPrivacyCompliance` ?policyVersion |
| Language | text field | — | — | `listPrivacyCompliance` ?language |
| Action | select | — | Consent granted · Consent withdrawn · Preference changed · Policy accepted · Privacy request created · Identity verified · Data export generated · Correction requested · Deletion approved · Anonymisation executed · Retention action · Legal hold … | `listPrivacyEvidenceCompliance` ?action |
| Report | select | — | Consent status · Consent withdrawal · Marketing permission · Privacy request sla · Deletion anonymisation · Retention · Policy acceptance · Minor guardian privacy · Cookie tracking compliance · Biometric privacy · Exception | `listPrivacyEvidenceCompliance` ?report |
| Subject | picker: choose a subject | — | — | `listPrivacyEvidenceCompliance` ?subjectId |
| Request | picker: choose a request | — | — | `listPrivacyEvidenceCompliance` ?requestId |
| Actor principal | picker: choose an actor principal | — | — | `listPrivacyEvidenceCompliance` ?actorPrincipalId |
| From | date and time picker | — | — | `listPrivacyEvidenceCompliance` ?from |
| … 1 more | | | | `operations.json` |

#### Outputs: what the screen shows and produces

**Shown**

**Every privacy analytics compliance** (data table, from `listPrivacyCompliance`)

| Shows | Format | Notes |
|---|---|---|
| Consent rate | 12.5% | Granted over presented. |
| Withdrawal rate | 12.5% | — |
| Marketing opt in rate | 12.5% | — |
| Cookie acceptance by category | list or chips (count when long) | — |
| Privacy requests | 1,234 | Requests submitted in the period. |
| Average resolution seconds | 1,234 | — |
| Sla compliance rate | 12.5% | Completed within `dueAt`, over completed requests that had one. |
| Deletion completion rate | 12.5% | — |
| Retention compliance rate | 12.5% | Records actioned by their due date, over records due. |
| Policy acceptance rate | 12.5% | — |
| Guardian consent completion rate | 12.5% | — |
| Privacy exceptions | 1,234 | — |
| Consent propagation failures | 1,234 | — |

**The selected privacy analytics compliance** (detail panel): The pack groups this record's detail under its own headings: “Privacy request cases”, “Locate/export/correct data”, “Final Area 17 Architecture”, “Compliance”.

| Shows | Format | Notes |
|---|---|---|
| Consent rate | 12.5% | Granted over presented. |
| Withdrawal rate | 12.5% | — |
| Marketing opt in rate | 12.5% | — |
| Cookie acceptance by category | list or chips (count when long) | — |
| Privacy requests | 1,234 | Requests submitted in the period. |
| Average resolution seconds | 1,234 | — |
| Sla compliance rate | 12.5% | Completed within `dueAt`, over completed requests that had one. |
| Deletion completion rate | 12.5% | — |
| Retention compliance rate | 12.5% | Records actioned by their due date, over records due. |
| Policy acceptance rate | 12.5% | — |
| Guardian consent completion rate | 12.5% | — |
| Privacy exceptions | 1,234 | — |
| Consent propagation failures | 1,234 | — |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** “Show overdue deletion requests.”, “Show minors with incomplete guardian privacy consent.”. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listPrivacyCompliance` (onLoad, Privacy Analytics & AI Compliance Intelligence); `listPrivacyEvidenceCompliance` (onLoad, Privacy Audit, Evidence & Compliance Reporting)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The privacy analytics compliance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the privacy analytics compliance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No privacy analytics compliance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the privacy analytics compliance are still there. The pack's own statuses are 7 Operations — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
finding: Consent withdrawal on WhatsApp up 3x after the 28 Sep campaign (AI, model privacy-v1) - investigate frequency
```

#### Permissions

- `listPrivacyCompliance` → `GUEST_VIEW` (read) · staff
- `listPrivacyEvidenceCompliance` → `AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.63 | Reporting and Analytics Reports should include: Consent acceptance rate. Rejection rate. Preference selections by category. Geographic consent statistics. Compliance audit reports. | Ticketing Sales | CONTRACTED | `listPrivacyCompliance` |

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-040` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS103 Privacy  Consent   Preference Management Board 2.dc.html#cms-040`
- Workshop pack: Privacy__Consent___Preference_Management_Reference.pdf board 2
- Flow F151 *Privacy Consent Preference Management board 2: Privacy Operations Command Center*, step 18: Works in Privacy Analytics & AI Compliance Intelligence → Provide executives, Privacy Officers and Compliance teams with actionable privacy analytics and AI-assisted risk detection. This should be the intelligence layer across both Privacy Boards.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-040?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `AUDIT_VIEW`, `GUEST_VIEW`.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listConsentEvidenceWithdrawal": {"method":"GET","path":"/consent-evidence-withdrawal","contract":"marketing-crm","summary":"Consent Evidence, History & Withdrawal Management","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"subjectId","in":"query","required":false},{"name":"consentPurpose","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"source","in":"query","required":false},{"name":"brandId","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"propagationStatus","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCustomerPrivacyConsent": {"method":"GET","path":"/customer-privacy-consent","contract":"marketing-crm","summary":"Customer Privacy, Consent & Preference 360°","permission":"GUEST_VIEW_PII","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"subjectId","in":"query","required":true}],"requestBody":null,"responds":"CustomerPrivacyConsentPreference360View"},
"listDataRetentionExpiry": {"method":"GET","path":"/data-retention-expiry","contract":"marketing-crm","summary":"Data Retention, Expiry & Legal Hold Operations","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"dataCategory","in":"query","required":false},{"name":"jurisdiction","in":"query","required":false},{"name":"holdStatus","in":"query","required":false}],"requestBody":null,"responds":"DataRetentionExpiryLegalHoldOperationsView"},
"listDataSubjectCustomer": {"method":"GET","path":"/data-subject-customer","contract":"marketing-crm","summary":"Data Subject / Customer Privacy Request Management","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":false},{"name":"requestType","in":"query","required":false},{"name":"subjectId","in":"query","required":false},{"name":"jurisdiction","in":"query","required":false},{"name":"slaState","in":"query","required":false},{"name":"ownerPrincipalId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDeletionAnonymizationRestriction": {"method":"GET","path":"/deletion-anonymization-restriction","contract":"marketing-crm","summary":"Deletion, Anonymization & Restriction Operations","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"actionType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"subjectId","in":"query","required":false},{"name":"requestId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDeviceConsents": {"method":"GET","path":"/consent/device","contract":"marketing-crm","summary":"Visitors' cookie decisions, as evidence","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":"brandId","in":"query","required":false},{"name":"action","in":"query","required":false},{"name":"category","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"claimed","in":"query","required":false},{"name":"consentKey","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPrivacy": {"method":"GET","path":"/privacy","contract":"marketing-crm","summary":"Privacy Operations Command Center","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"brandId","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"requestType","in":"query","required":false},{"name":"consentPurpose","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"ownerPrincipalId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false}],"requestBody":null,"responds":"PrivacyOperationsCommandCenterView"},
"listPrivacyCompliance": {"method":"GET","path":"/privacy-compliance","contract":"marketing-crm","summary":"Privacy Analytics & AI Compliance Intelligence","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"brandId","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"consentPurpose","in":"query","required":false},{"name":"segmentId","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"policyVersion","in":"query","required":false},{"name":"language","in":"query","required":false}],"requestBody":null,"responds":"PrivacyAnalyticsAiComplianceIntelligenceView"},
"listPrivacyComplianceExceptions": {"method":"GET","path":"/privacy-compliance-exception","contract":"marketing-crm","summary":"The privacy exception queue","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"category","in":"query","required":false},{"name":"severity","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"ownerPrincipalId","in":"query","required":false},{"name":"subjectId","in":"query","required":false},{"name":"brandId","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPrivacyEvidenceCompliance": {"method":"GET","path":"/privacy-evidence-compliance","contract":"marketing-crm","summary":"Privacy Audit, Evidence & Compliance Reporting","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"action","in":"query","required":false},{"name":"report","in":"query","required":false},{"name":"subjectId","in":"query","required":false},{"name":"requestId","in":"query","required":false},{"name":"actorPrincipalId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"runDataRetention": {"method":"POST","path":"/retention-runs","contract":"marketing-crm","summary":"Preview or execute a retention pass","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RetentionRunResult"},
"setDataDiscoveryAccess": {"method":"PUT","path":"/data-discovery-access","contract":"marketing-crm","summary":"Data Discovery, Access, Export & Correction Workspace","permission":"GUEST_VIEW_PII","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DataDiscoveryAccessExportCorrectionWorkspaceInput","responds":"DataDiscoveryAccessExportCorrectionWorkspaceView"},
"setLegalHold": {"method":"PUT","path":"/data-retention-expiry","contract":"marketing-crm","summary":"Place, approve or release a legal or operational hold","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PrivacyLegalHold","responds":"PrivacyLegalHold"},
"setPrivacyComplianceException": {"method":"PUT","path":"/privacy-compliance-exception","contract":"marketing-crm","summary":"Raise, investigate or close a privacy exception","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PrivacyComplianceExceptionInvestigationWorkspaceInput","responds":"PrivacyComplianceExceptionInvestigationWorkspaceView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ConsentEvidenceHistoryWithdrawalManagementView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.consent_record, marketing.consent_record_channel, marketing.consent_capture_point, marketing.consent_propagation (new)","description":"One consent event and, for a withdrawal, its propagation (pack 17.2.3 Consent Evidence Record, Consent Events, Withdrawal Propagation).","required":["evidenceId","subjectId","purpose","event","occurredAt"],"properties":{"evidenceId":{"type":"string","description":"The `ConsentRecord.id`."},"subjectId":{"type":"string","format":"uuid","description":"The customer or participant."},"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"consentVersion":{"type":"string","nullable":true,"description":"The notice version consented against."},"wordingReference":{"type":"string","maxLength":200,"nullable":true,"description":"The exact wording/version reference shown at capture."},"event":{"type":"string","enum":["presented","granted","declined","updated","withdrawn","expired","reconfirmed","superseded"]},"currentStatus":{"type":"string","enum":["granted","declined","withdrawn","expired"],"description":"The purpose's state now, which may differ from this event's."},"occurredAt":{"type":"string","format":"date-time"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"source":{"$ref":"#/components/schemas/ConsentSource"},"withdrawalRoute":{"type":"string","nullable":true,"enum":["customerPortal","mobileApp","preferenceCenter","customerService","authorisedStaff","api"],"description":"Only on `withdrawn`."},"brandId":{"type":"string","format":"uuid","nullable":true},"country":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"capturePointId":{"type":"string","format":"uuid","nullable":true},"actorType":{"type":"string","enum":["customer","guardian","staff","system"]},"actorPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The staff member for proxy capture (`recordedByPrincipalId`)."},"sourceSystem":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"deviceSessionReference":{"type":"string","maxLength":200,"nullable":true,"description":"Only where the capture point's configuration permits storing it."},"guardianSubjectId":{"type":"string","format":"uuid","nullable":true},"propagation":{"type":"array","description":"Per target, for a withdrawal.","items":{"type":"object","required":["target","status"],"properties":{"target":{"type":"string","enum":["crm","marketing","campaignAudience","connectedSystem"]},"targetName":{"type":"string","nullable":true},"status":{"type":"string","enum":["requested","processed","propagated","acknowledged","failed","retryRequired"]},"attempts":{"type":"integer","minimum":0},"updatedAt":{"type":"string","format":"date-time"},"error":{"type":"string","maxLength":500,"nullable":true}}}}}},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"ConsentSource": {"type":"string","enum":["guestApp","website","kiosk","pos","callCentre","import","agentRecorded","cookieBanner","checkout"],"description":"`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."},
"CookieCategory": {"type":"string","enum":["strictlyNecessary","functional","analytics","personalisation","marketing"],"description":"2.6.53. The five categories the banner design (`CookieBannerPreferenceCenterDesignerView.categories`) offers; the matrix's \"preference\" category is `personalisation` (British spelling, as `ConsentPurpose`)."},
"CookieConsentChannel": {"type":"string","enum":["b2cWebsite","customerPortal","mobileApp","embeddedCheckout","whiteLabelSite","partnerMicrosite"],"description":"The six governed surfaces, as the registry and the banner design name them (pack 17.1.5-17.1.6)."},
"CustomerPrivacyConsentPreference360View": {"type":"object","x-ticvai-persistence":"none — projection over marketing.guest_profile, marketing.consent_record, marketing.consent_record_channel, marketing.consent_purpose, marketing.privacy_request (new), marketing.tracking_technology, pii.subject","description":"One customer's privacy position (pack 17.2.2). Consent entries are current state; history is `listConsentEvidenceWithdrawal`.","required":["subjectId","consents","policyAcceptance"],"properties":{"subjectId":{"type":"string","format":"uuid"},"displayName":{"type":"string","nullable":true},"accountStatus":{"type":"string","enum":["active","guest","suspended","archived","erased"],"description":"`archived` and `erased` are the ADR-0047 lifecycle stages."},"country":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"preferredLanguage":{"type":"string","nullable":true,"description":"BCP 47 tag."},"ageCategory":{"type":"string","enum":["adult","minor","unknown"]},"guardianSubjectId":{"type":"string","format":"uuid","nullable":true},"guardianRelationship":{"type":"string","nullable":true,"enum":["parent","legalGuardian","other"]},"openExceptionCount":{"type":"integer","minimum":0,"description":"The privacy risk/exception indicator; open exceptions naming this customer."},"consents":{"type":"array","items":{"type":"object","required":["purpose","decision"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"channel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"nullable":true},"decision":{"type":"string","enum":["granted","declined","withdrawn","expired","notAsked"]},"noticeVersion":{"type":"string","nullable":true},"capturedAt":{"type":"string","format":"date-time","nullable":true},"source":{"allOf":[{"$ref":"#/components/schemas/ConsentSource"}],"nullable":true},"requiresRenewal":{"type":"boolean"}}}},"preferences":{"type":"object","properties":{"channels":{"type":"array","items":{"type":"object","required":["channel","optedIn"],"properties":{"channel":{"$ref":"#/components/schemas/MessageChannel"},"optedIn":{"type":"boolean"}}}},"brandIds":{"type":"array","items":{"type":"string","format":"uuid"}},"marketingCategories":{"type":"array","items":{"type":"string","maxLength":80}},"personalisationEnabled":{"type":"boolean"}}},"policyAcceptance":{"type":"array","items":{"type":"object","required":["documentType","currentVersion"],"properties":{"documentType":{"type":"string","enum":["privacyPolicy","cookieNotice","biometricNotice","childrensPrivacyNotice","other"]},"documentName":{"type":"string","nullable":true},"acceptedVersion":{"type":"string","nullable":true},"acceptedAt":{"type":"string","format":"date-time","nullable":true},"currentVersion":{"type":"string"},"requiresReacceptance":{"type":"boolean"}}}},"trackingChoices":{"type":"array","description":"Only where the preference is tied to this customer (a signed-in consent).","items":{"type":"object","required":["category","decision"],"properties":{"category":{"type":"string","enum":["strictlyNecessary","functional","analytics","personalisation","marketing","other"]},"decision":{"type":"string","enum":["granted","declined"]},"decidedAt":{"type":"string","format":"date-time"}}}},"privacyRequests":{"type":"array","description":"Open requests and the 20 most recent completed ones.","items":{"type":"object","required":["requestId","requestType","status"],"properties":{"requestId":{"type":"string","format":"uuid"},"requestType":{"type":"string"},"status":{"type":"string","enum":["submitted","inProgress","completed"]},"submittedAt":{"type":"string","format":"date-time"},"dueAt":{"type":"string","format":"date-time","nullable":true}}}},"dataFootprint":{"type":"array","description":"Where this customer's data exists, as counts; the records are reached through `setDataDiscoveryAccess`.","items":{"type":"object","required":["system","recordCount"],"properties":{"system":{"type":"string","enum":["crm","ticketing","membership","orders","loyalty","wallet","marketing","waiver","biometricProviderReference","connectedSystem"]},"systemName":{"type":"string","nullable":true,"description":"The connected system's name, when `system` is `connectedSystem`."},"recordCount":{"type":"integer","minimum":0}}}},"timeline":{"type":"array","description":"The 50 most recent privacy events, newest first.","items":{"type":"object","required":["occurredAt","event"],"properties":{"occurredAt":{"type":"string","format":"date-time"},"event":{"type":"string","enum":["accountCreated","policyAccepted","consentGranted","consentDeclined","consentWithdrawn","preferenceChanged","privacyRequestCreated","privacyRequestCompleted","dataExportGenerated","anonymised","archived"]},"summary":{"type":"string","maxLength":300}}}}}},
"DataDiscoveryAccessExportCorrectionWorkspaceInput": {"type":"object","x-ticvai-persistence":"marketing.privacy_export_package","description":"What a privacy user sends for one request (pack 17.2.5 Data Discovery, Export Package, Correction, Review).","required":["requestId"],"properties":{"requestId":{"type":"string","format":"uuid","description":"The privacy request (`setPrivacyRequest`); the natural key."},"identifiers":{"type":"array","description":"Extra identifiers to search by; the request's subject is always included.","items":{"type":"object","required":["type","value"],"properties":{"type":{"type":"string","enum":["customerId","email","mobile","membershipId","orderId","participantId","other"]},"value":{"type":"string","maxLength":200}}}},"sources":{"type":"array","description":"Sources to search; empty means all.","items":{"type":"string","enum":["customerProfile","orders","tickets","membership","loyalty","wallet","crm","marketing","paymentReferences","waiverRecords","resourceBookings","eventRegistrations","consentRecords","credentialReferences","connectedApplications"]}},"exportPackage":{"type":"object","nullable":true,"description":"Present to generate or progress the export package.","properties":{"includedSources":{"type":"array","items":{"type":"string","description":"A value of `sources`."}},"includedCategories":{"type":"array","items":{"type":"string","maxLength":80}},"exclusions":{"type":"array","items":{"type":"string","maxLength":200},"description":"Records withheld, each with a reason (e.g. another person's data, a legal hold)."},"sensitiveFieldHandling":{"type":"string","enum":["include","mask","exclude"],"default":"mask"},"format":{"type":"string","enum":["json","csv","pdf"],"default":"json"},"language":{"type":"string","description":"BCP 47 tag for the cover letter and field labels."},"passwordProtected":{"type":"boolean","default":true},"expiresAt":{"type":"string","format":"date-time"},"reviewAction":{"type":"string","nullable":true,"enum":["submitForReview","approve","reject","deliver"],"description":"Moves the package through generated -> privacyReview -> approved -> delivered."}}},"corrections":{"type":"array","description":"Correction requests to route to the system of record.","items":{"type":"object","required":["field","proposedValue"],"properties":{"field":{"type":"string","maxLength":100,"description":"e.g. `email`, `dateOfBirth`."},"proposedValue":{"type":"string","maxLength":500},"note":{"type":"string","maxLength":500,"nullable":true}}}}}},
"DataDiscoveryAccessExportCorrectionWorkspaceView": {"type":"object","x-ticvai-persistence":"marketing.privacy_export_package","description":"One request's discovery results, export package and routed corrections.","required":["requestId","results"],"properties":{"requestId":{"type":"string","format":"uuid"},"discoveredAt":{"type":"string","format":"date-time","readOnly":true},"results":{"type":"array","description":"Record counts per source; the records themselves go only into the export package.","items":{"type":"object","required":["source","recordCount"],"properties":{"source":{"type":"string","description":"A value of the input's `sources`."},"systemName":{"type":"string","nullable":true},"recordCount":{"type":"integer","minimum":0},"searchFailed":{"type":"boolean","default":false}}}},"exportPackage":{"type":"object","nullable":true,"readOnly":true,"properties":{"status":{"type":"string","enum":["generating","generated","privacyReview","approved","rejected","delivered","expired"]},"format":{"type":"string","enum":["json","csv","pdf"]},"generatedAt":{"type":"string","format":"date-time","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"deliveredAt":{"type":"string","format":"date-time","nullable":true},"expiresAt":{"type":"string","format":"date-time"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"The encrypted package in the asset store."},"dsarRequestId":{"type":"string","nullable":true,"description":"The cross-region fan-out that assembled it."}}},"corrections":{"type":"array","readOnly":true,"items":{"type":"object","required":["field","systemOfRecord","status"],"properties":{"field":{"type":"string"},"systemOfRecord":{"type":"string","description":"The owning contract/table, e.g. `pii.subject_contact`."},"operation":{"type":"string","nullable":true,"description":"The operation that performs it, e.g. `updateGuestProfile`."},"status":{"type":"string","enum":["routed","applied","rejected","manualActionRequired"]},"updatedAt":{"type":"string","format":"date-time"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"DataRetentionExpiryLegalHoldOperationsView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.retention_policy, marketing.legal_hold (new), marketing.privacy_action (new), marketing.guest_profile, pii.subject","description":"The retention dashboard (pack 17.2.7) against ADR-0047's lifecycle.","required":["recordsApproachingExpiry","policies","holds"],"properties":{"recordsApproachingExpiry":{"type":"integer","minimum":0,"description":"Inside the 90-day notice window before their retention action."},"eligibleForDeletion":{"type":"integer","minimum":0},"eligibleForAnonymization":{"type":"integer","minimum":0},"eligibleForArchive":{"type":"integer","minimum":0},"underLegalHold":{"type":"integer","minimum":0},"processingFailures":{"type":"integer","minimum":0},"retentionExceptions":{"type":"integer","minimum":0,"description":"Open `retentionFailure` / `deletionFailure` privacy exceptions."},"lifecycle":{"type":"object","description":"Guest subjects by ADR-0047 stage.","properties":{"active":{"type":"integer","minimum":0},"archived":{"type":"integer","minimum":0},"erased":{"type":"integer","minimum":0}}},"policies":{"type":"array","items":{"type":"object","required":["policyId","code","action"],"properties":{"policyId":{"type":"string","format":"uuid"},"code":{"type":"string"},"dataCategory":{"type":"string"},"action":{"type":"string","enum":["archive","anonymise","pseudonymise","delete"]},"retainMonths":{"type":"integer","minimum":0},"isSystemDefault":{"type":"boolean","description":"True when inherited from the system default; false when the tenant or venue overrode it."},"floorMonths":{"type":"integer","minimum":0,"nullable":true},"ceilingMonths":{"type":"integer","minimum":0,"nullable":true},"anchor":{"type":"string","enum":["lastActivity","creation","eventEnd","transactionDate"]},"approachingExpiry":{"type":"integer","minimum":0},"eligibleNow":{"type":"integer","minimum":0},"heldBack":{"type":"integer","minimum":0},"schedule":{"type":"string","enum":["daily","weekly","monthly","custom","manual"]},"nextRunAt":{"type":"string","format":"date-time","nullable":true},"lastRun":{"type":"object","nullable":true,"properties":{"runId":{"type":"string","format":"uuid"},"completedAt":{"type":"string","format":"date-time","nullable":true},"recordsAffected":{"type":"integer","minimum":0},"failed":{"type":"integer","minimum":0}}}}}},"holds":{"type":"array","description":"Holds in the requested states, by `reviewDate` ascending.","items":{"$ref":"#/components/schemas/PrivacyLegalHold"}},"asOf":{"type":"string","format":"date-time"}}},
"DataSubjectCustomerPrivacyRequestManagementView": {"type":"object","x-ticvai-persistence":"marketing.privacy_request","description":"One customer privacy request (pack 17.2.4 Case Information). The case layer over the cross-region `platform.dsar_request` fan-out, which it references when it raises one.","required":["subjectId","requestType","source","requesterRole","jurisdiction"],"properties":{"requestId":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid","description":"The person the request is about."},"requestType":{"type":"string","maxLength":60,"description":"A configured request type code (`setPrivacyRequestTypes`), e.g. `access`, `dataExport`, `correction`, `deletion`, `anonymisation`, `restriction`, `objection`, `consentWithdrawal`, `marketingOptOut`."},"source":{"type":"string","enum":["customerPortal","b2c","mobileApp","emailManual","customerService","pos","api"]},"requesterRole":{"type":"string","enum":["self","guardian","authorisedRepresentative"]},"requesterSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guardian or representative, when not `self`; verified like the subject."},"jurisdiction":{"type":"string","pattern":"^[A-Z]{2}$","description":"Selects the response period configured for this request type."},"submittedAt":{"type":"string","format":"date-time","readOnly":true},"dueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"`submittedAt` plus the jurisdiction's configured response period; null when none is configured."},"deadlineConfigured":{"type":"boolean","readOnly":true},"daysRemaining":{"type":"integer","nullable":true,"readOnly":true,"description":"Negative once overdue; null without a deadline."},"atRisk":{"type":"boolean","readOnly":true,"description":"Inside the request type's configured warning window before `dueAt`."},"slaState":{"type":"string","readOnly":true,"enum":["onTrack","atRisk","overdue","escalated","noDeadline"]},"priority":{"type":"string","enum":["P1","P2","P3","P4"],"default":"P3"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"verificationMethod":{"type":"string","nullable":true,"enum":["accountLogin","otp","emailVerification","mobileVerification","idReview","manualVerification"],"description":"One of the methods the request type allows."},"verificationStatus":{"type":"string","enum":["notStarted","pending","verified","failed"],"default":"notStarted"},"status":{"type":"string","enum":["submitted","inProgress","completed"],"default":"submitted","description":"MoM 20 Aug lifecycle."},"stage":{"type":"string","maxLength":60,"nullable":true,"description":"The configured workflow step within `inProgress` (a stage code of the request type)."},"outcome":{"type":"string","nullable":true,"enum":["fulfilled","partiallyFulfilled","refused","withdrawnByRequester"],"description":"Required to complete. `refused` and `partiallyFulfilled` need `outcomeReason`."},"outcomeReason":{"type":"string","maxLength":1000,"nullable":true},"escalated":{"type":"boolean","default":false},"dsarRequestId":{"type":"string","nullable":true,"readOnly":true,"description":"The cross-region `DsarRequest.requestId`, when fulfilment fanned out."},"caseId":{"type":"string","format":"uuid","nullable":true,"description":"The customer-service case it came in through, if any."},"notes":{"type":"string","maxLength":4000,"nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"DeletionAnonymizationRestrictionOperationsView": {"type":"object","x-ticvai-persistence":"marketing.privacy_action","description":"One governed privacy action on one subject (pack 17.2.6).","required":["subjectId","actionType"],"properties":{"actionId":{"type":"string","format":"uuid","readOnly":true},"requestId":{"type":"string","format":"uuid","nullable":true,"description":"The privacy request it fulfils; null when a retention run raised it."},"retentionRunId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"subjectId":{"type":"string","format":"uuid"},"actionType":{"type":"string","enum":["delete","anonymise","pseudonymise","restrictProcessing","suppressMarketing","removeBiometricReference","disconnectThirdPartyProfile","other"],"description":"`pseudonymise` only where the tenant has configured it."},"otherActionLabel":{"type":"string","maxLength":100,"nullable":true},"requiresApproval":{"type":"boolean","readOnly":true},"impact":{"type":"array","readOnly":true,"description":"Affected areas and what will happen to each, shown before execution.","items":{"type":"object","required":["area","outcome"],"properties":{"area":{"type":"string","enum":["customerProfile","marketingProfile","biometricReference","orders","invoices","ticketUsage","fraudInvestigation","consentEvidence","waiverRecords","connectedSystem"]},"outcome":{"type":"string","enum":["delete","anonymise","pseudonymise","restrict","retain","hold"]},"reason":{"type":"string","maxLength":300,"nullable":true,"description":"Required for `retain` and `hold`, e.g. the retention policy code."}}}},"checks":{"type":"array","readOnly":true,"items":{"type":"object","required":["kind","blocking"],"properties":{"kind":{"type":"string","enum":["retentionRequirement","legalHold","financialRecord","activeTransaction","securityFraud","contractualObligation","jurisdictionRule"]},"blocking":{"type":"boolean"},"detail":{"type":"string","maxLength":300}}}},"approvals":{"type":"array","readOnly":true,"items":{"type":"object","properties":{"step":{"type":"string","enum":["privacyOfficer","dataOwner"]},"outcome":{"type":"string","enum":["approved","rejected"]},"principalId":{"type":"string","format":"uuid"},"reason":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}}},"decision":{"type":"object","writeOnly":true,"nullable":true,"description":"Sent to record an approval step or cancel.","required":["step","outcome"],"properties":{"step":{"type":"string","enum":["privacyOfficer","dataOwner","cancel"]},"outcome":{"type":"string","enum":["approved","rejected"]},"reason":{"type":"string","maxLength":500,"nullable":true}}},"status":{"type":"string","readOnly":true,"enum":["planned","awaitingApproval","approved","rejected","executing","completed","completedWithRetention","failed","manualActionRequired","cancelled"]},"systemResults":{"type":"array","readOnly":true,"description":"The execution monitor, per system.","items":{"type":"object","required":["system","status"],"properties":{"system":{"type":"string","maxLength":100},"status":{"type":"string","enum":["pending","processing","completed","retainedWithReason","failed","manualActionRequired"]},"reason":{"type":"string","maxLength":300,"nullable":true},"updatedAt":{"type":"string","format":"date-time"}}}},"dsarRequestId":{"type":"string","nullable":true,"readOnly":true},"evidenceAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Completion evidence, as `runDataRetention` produces."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"DeviceConsent": {"type":"object","x-ticvai-persistence":"marketing.device_consent + marketing.device_consent_category","description":"**One cookie decision by a visitor nobody has identified yet** (BL-073 §4b, decided 29 September). Append-only: a change of mind is a new row. Keyed for the visitor by `consentKey`, which the platform mints; the categories are child rows. The IP address and user agent, where recorded at all, are in `pii.consent_identifier` (`ConsentCaptureIdentifier`), never here.","required":["consentKey","channel","action","categories","noticeVersion","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"consentKey":{"type":"string","maxLength":64,"readOnly":true,"description":"**Opaque, minted by us, not a device fingerprint.** It answers 2.6.55's \"user identifier/session ID\" and is the join key `claimDeviceConsent` needs. Shared by all the tenant's domains (2.6.62), never across tenants."},"channel":{"$ref":"#/components/schemas/CookieConsentChannel"},"brandId":{"type":"string","format":"uuid","nullable":true},"bannerDesignId":{"type":"string","format":"uuid","nullable":true,"description":"The published `CookieBannerPreferenceCenterDesignerView` version the visitor was shown."},"action":{"$ref":"#/components/schemas/DeviceConsentAction"},"categories":{"type":"array","minItems":1,"description":"Every category of the design, with the decision this row gives it.","items":{"type":"object","required":["category","decision"],"properties":{"category":{"$ref":"#/components/schemas/CookieCategory"},"decision":{"type":"string","enum":["granted","declined"]}}}},"noticeVersion":{"type":"string","description":"The cookie notice version decided against (white-label `setPolicy`, kind `cookie`)."},"language":{"type":"string","maxLength":10,"nullable":true},"globalPrivacyControl":{"type":"boolean","default":false,"description":"The browser sent a Global Privacy Control signal; honoured as a CCPA/CPRA opt-out of sale and sharing."},"source":{"$ref":"#/components/schemas/ConsentSource"},"country":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true,"readOnly":true,"description":"The edge's geolocation of the request, for the geographic statistics (2.6.63). The address is not kept here."},"decidedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**A device consent expires and a subject consent does not.** Set from the tenant's device-consent term; after it the banner asks again."},"claimedBySubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Set once, by `claimDeviceConsent`. Never cleared."},"claimedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005), tenant-scoped: a decision with no subject still belongs to one tenant."}}},
"DeviceConsentAction": {"type":"string","enum":["acceptAll","rejectNonEssential","savePreferences","withdraw","doNotSellOrShare"],"description":"What the visitor pressed. `doNotSellOrShare` is the CCPA/CPRA opt-out link, shown where the design's `regulatoryRegimes` include `ccpaCpra`."},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PrivacyAnalyticsAiComplianceIntelligenceView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.consent_record, marketing.privacy_request (new), marketing.privacy_action (new), marketing.retention_policy, marketing.privacy_exception (new), marketing.consent_propagation (new), marketing.tracking_technology","description":"Privacy KPIs for a period (pack 17.2.10). Rates are 0-1 over the period's denominators.","required":["consentRate","withdrawalRate","marketingOptInRate"],"properties":{"consentRate":{"type":"number","minimum":0,"maximum":1,"description":"Granted over presented."},"withdrawalRate":{"type":"number","minimum":0,"maximum":1},"marketingOptInRate":{"type":"number","minimum":0,"maximum":1},"cookieAcceptanceByCategory":{"type":"array","items":{"type":"object","required":["category","acceptanceRate"],"properties":{"category":{"type":"string","enum":["functional","analytics","personalisation","marketing","other"]},"acceptanceRate":{"type":"number","minimum":0,"maximum":1}}}},"privacyRequests":{"type":"integer","minimum":0,"description":"Requests submitted in the period."},"privacyRequestsByType":{"type":"array","items":{"type":"object","properties":{"requestType":{"type":"string"},"count":{"type":"integer","minimum":0}}}},"averageResolutionSeconds":{"type":"integer","minimum":0,"nullable":true},"slaComplianceRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Completed within `dueAt`, over completed requests that had one."},"deletionCompletionRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"retentionComplianceRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Records actioned by their due date, over records due."},"policyAcceptanceRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"guardianConsentCompletionRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"privacyExceptions":{"type":"integer","minimum":0},"consentPropagationFailures":{"type":"integer","minimum":0},"consentFunnel":{"type":"array","description":"In order, each step's count and rate over the first step.","items":{"type":"object","required":["step","count"],"properties":{"step":{"type":"string","maxLength":80,"description":"e.g. privacyNoticeDisplayed, marketingConsentPresented, emailOptIn."},"count":{"type":"integer","minimum":0},"rate":{"type":"number","minimum":0,"maximum":1}}}},"riskFindings":{"type":"array","description":"AI findings for human investigation; none is acted on automatically.","items":{"type":"object","required":["kind","summary"],"properties":{"kind":{"type":"string","enum":["trendAnomaly","abandonmentByLanguage","supersededPolicyInUse","configurationMismatch","other"]},"summary":{"type":"string","maxLength":500},"severity":{"type":"string","enum":["low","medium","high"]},"detectedAt":{"type":"string","format":"date-time"},"exceptionId":{"type":"string","format":"uuid","nullable":true,"description":"Set once someone raised an exception from it."}}}},"asOf":{"type":"string","format":"date-time"}}},
"PrivacyAuditEvidenceComplianceReportingView": {"type":"object","x-ticvai-persistence":"marketing.privacy_audit_event","description":"One privacy audit event (pack 17.2.9 Audit Fields). Append-only; written by the operation that performed the event, never through an API.","required":["eventId","action","occurredAt"],"properties":{"eventId":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"action":{"type":"string","enum":["consentGranted","consentWithdrawn","preferenceChanged","policyAccepted","privacyRequestCreated","identityVerified","dataExportGenerated","correctionRequested","deletionApproved","anonymisationExecuted","retentionAction","legalHold","administrativeOverride","configurationChange"]},"actorType":{"type":"string","enum":["customer","guardian","staff","system","ai"]},"actorPrincipalId":{"type":"string","format":"uuid","nullable":true},"actorRole":{"type":"string","nullable":true,"description":"The role the actor held at the time."},"source":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"channel":{"type":"string","nullable":true,"description":"A `ConsentSource` value or the staff surface it came through."},"occurredAt":{"type":"string","format":"date-time"},"before":{"type":"object","nullable":true,"additionalProperties":true,"description":"The changed fields before, masked where the field is sensitive."},"after":{"type":"object","nullable":true,"additionalProperties":true},"reason":{"type":"string","maxLength":1000,"nullable":true},"approvalReference":{"type":"string","nullable":true,"description":"The approval that authorised it (privacy action approval, hold approval, package approval)."},"relatedRequestId":{"type":"string","format":"uuid","nullable":true},"relatedCaseId":{"type":"string","format":"uuid","nullable":true},"evidenceReference":{"type":"string","nullable":true,"description":"e.g. the consent evidence id, the policy version, the export asset id."}}},
"PrivacyComplianceExceptionInvestigationWorkspaceInput": {"type":"object","x-ticvai-persistence":"marketing.privacy_exception","description":"What a user may send to raise or progress a privacy exception (pack 17.2.8).","required":["category","severity","summary"],"properties":{"id":{"type":"string","format":"uuid","description":"Absent to raise; present to update."},"category":{"type":"string","enum":["missingConsentEvidence","consentPropagationFailure","marketingAfterWithdrawal","policyVersionMismatch","missingGuardianConsent","retentionFailure","deletionFailure","unknownTrackingTechnology","unauthorisedDataAccess","unmappedProcessingPurpose","biometricPrivacyException","dataExportFailure","other"]},"severity":{"type":"string","enum":["low","medium","high","critical"]},"summary":{"type":"string","maxLength":1000},"subjectId":{"type":"string","format":"uuid","nullable":true},"system":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"brandId":{"type":"string","format":"uuid","nullable":true},"country":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["detected","triaged","assigned","investigated","correctiveAction","reviewed","closed"],"default":"detected"},"relatedEvidenceIds":{"type":"array","items":{"type":"string"},"description":"Consent evidence ids and audit event ids."},"policyReference":{"type":"string","maxLength":200,"nullable":true,"description":"The configuration or policy version involved."},"rootCause":{"type":"string","maxLength":2000,"nullable":true},"correctiveAction":{"type":"string","maxLength":2000,"nullable":true},"notes":{"type":"string","maxLength":4000,"nullable":true},"attachmentAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"escalatedTo":{"type":"string","nullable":true,"enum":["privacy","legal","security","it","marketing","operations","dataOwner"]},"privacyIncidentId":{"type":"string","format":"uuid","nullable":true,"description":"The `recordPrivacyIncident` record, when the exception is also a breach."}}},
"PrivacyComplianceExceptionInvestigationWorkspaceView": {"type":"object","x-ticvai-persistence":"marketing.privacy_exception","description":"One privacy exception as stored, with its investigation fields and timeline.","allOf":[{"$ref":"#/components/schemas/PrivacyComplianceExceptionInvestigationWorkspaceInput"},{"type":"object","required":["id","detectedAt"],"properties":{"detectedAt":{"type":"string","format":"date-time","readOnly":true},"detectedBy":{"type":"string","readOnly":true,"enum":["platformCheck","aiDetection","user"]},"slaDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"From the SLA policy for the severity (`setSlaPolicy`)."},"timeline":{"type":"array","readOnly":true,"items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"status":{"type":"string"},"principalId":{"type":"string","format":"uuid","nullable":true},"note":{"type":"string","nullable":true}}}},"closedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}}]},
"PrivacyLegalHold": {"type":"object","x-ticvai-persistence":"marketing.legal_hold","description":"A legal or operational hold (pack 17.2.7 Hold information). Overrides scheduled deletion in its scope once approved.","required":["reason","scope"],"properties":{"holdId":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["legal","operational","fraudInvestigation","regulatorRequest"],"default":"legal"},"reason":{"type":"string","maxLength":1000},"scope":{"type":"object","description":"At least one selector.","properties":{"subjectIds":{"type":"array","items":{"type":"string","format":"uuid"}},"dataCategories":{"type":"array","items":{"type":"string"}},"retentionPolicyCodes":{"type":"array","items":{"type":"string"}},"caseId":{"type":"string","format":"uuid","nullable":true}}},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"startsAt":{"type":"string","format":"date-time","nullable":true,"description":"Defaults to approval time."},"reviewDate":{"type":"string","format":"date","nullable":true},"status":{"type":"string","enum":["pendingApproval","active","released"],"default":"pendingApproval","description":"Set `active` to approve, `released` to release."},"placedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"approvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"releaseReason":{"type":"string","maxLength":1000,"nullable":true},"releasedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"PrivacyOperationsCommandCenterView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.guest_profile, marketing.consent_record, marketing.privacy_request (new), marketing.privacy_action (new), marketing.retention_policy, marketing.privacy_exception (new), marketing.privacy_incident","description":"The privacy operations position for the caller's scope and filters (pack 17.2.1).","required":["totalCustomerPrivacyProfiles","consentHealth","requestQueue"],"properties":{"totalCustomerPrivacyProfiles":{"type":"integer","minimum":0},"activeConsentRecords":{"type":"integer","minimum":0},"withdrawnConsents":{"type":"integer","minimum":0},"marketingOptIns":{"type":"integer","minimum":0},"marketingOptOuts":{"type":"integer","minimum":0},"pendingDataRightsRequests":{"type":"integer","minimum":0,"description":"Requests not yet `completed`."},"overdueRequests":{"type":"integer","minimum":0},"requestsWithoutDeadline":{"type":"integer","minimum":0,"description":"Open requests whose jurisdiction has no configured response period."},"pendingDeletionActions":{"type":"integer","minimum":0},"pendingAnonymization":{"type":"integer","minimum":0},"retentionActionsDue":{"type":"integer","minimum":0,"description":"Records inside the 90-day notice window before their retention action (ADR-0047 §6)."},"consentEvidenceExceptions":{"type":"integer","minimum":0},"privacyIncidentsExceptions":{"type":"integer","minimum":0,"description":"Open privacy exceptions plus open privacy incidents."},"policyReAcceptancePending":{"type":"integer","minimum":0,"description":"Customers whose accepted notice version has been superseded."},"consentHealth":{"type":"array","items":{"type":"object","required":["category","granted","withdrawn","declined"],"properties":{"category":{"type":"string","enum":["emailMarketing","smsMarketing","whatsappMarketing","pushMarketing","personalisation","analytics","location","biometrics","other"]},"otherLabel":{"type":"string","nullable":true,"description":"The configured purpose name, when `category` is `other`."},"granted":{"type":"integer","minimum":0},"withdrawn":{"type":"integer","minimum":0},"declined":{"type":"integer","minimum":0},"requiresRenewal":{"type":"integer","minimum":0}}}},"requestQueue":{"type":"array","description":"Open and recently completed requests by status and configured stage.","items":{"type":"object","required":["status","count"],"properties":{"status":{"type":"string","enum":["submitted","inProgress","completed"]},"stage":{"type":"string","nullable":true},"count":{"type":"integer","minimum":0},"atRisk":{"type":"integer","minimum":0},"overdue":{"type":"integer","minimum":0}}}},"alerts":{"type":"array","items":{"type":"object","required":["kind","count"],"properties":{"kind":{"type":"string","enum":["requestsApproachingDeadline","requestsOverdue","requestsWithoutDeadline","supersededNoticeAccepted","withdrawnConsentInMarketingExport","consentPropagationFailed","retentionActionFailed"]},"count":{"type":"integer","minimum":0},"detail":{"type":"string","maxLength":300,"nullable":true}}}},"asOf":{"type":"string","format":"date-time"}}},
"RetentionRunResult": {"type":"object","x-ticvai-persistence":"marketing.retention_run","description":"Board 2.8. **Completion evidence is the half that gets forgotten until an audit.**","properties":{"runId":{"type":"string","format":"uuid","x-ticvai-column":"id","description":"The run, stored as `marketing.retention_run`; `PrivacyAction.retentionRunId` points here. Preview runs are stored too, so an executed pass can be compared with what it previewed."},"policyId":{"type":"string","format":"uuid"},"mode":{"type":"string","enum":["preview","execute"]},"recordsAffected":{"type":"integer"},"byAction":{"type":"object","additionalProperties":{"type":"integer"}},"heldBack":{"type":"integer"},"heldBackReasons":{"type":"object","additionalProperties":{"type":"integer"}},"dependencies":{"type":"array","x-ticvai-persisted":false,"description":"Computed for the response; the executed run's detail is in the evidence asset.","items":{"type":"object","properties":{"surface":{"type":"string"},"count":{"type":"integer"},"consequence":{"type":"string"}}}},"evidenceAssetId":{"type":"string","format":"uuid","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true}}}
}
```
