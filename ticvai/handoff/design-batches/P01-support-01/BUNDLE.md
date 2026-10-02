# P01-support-01 — P01 · Support

**2 screens · 8 operations · 19 schemas · 1 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## Who this is for

**guest on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `CASE_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store. Offline, a screen shows what was already loaded, under the banner below.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
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

### White Label & CMS

A tenant (one operator, one or many venues) brands and arranges its own guest surfaces, the guest web (P01), the guest app (P02) and the kiosk (P05), from the Venue CMS (P13, a section of the Venue Management app), and TICVAI platform staff can do the same from the console (P09 ADM-016..018) only under a time-boxed grant into the tenant. Everything is configuration over a fixed structure: the guest flow, the page structure and the components are TICVAI's and stay the same for every tenant; the tenant chooses graphics, colours, fonts, which modules and tabs appear, the order of homepage sections and booking steps within allowed limits, copy in each language, and its domain. It never adds components. Work happens in ONE working draft per tenant; nothing a guest sees changes until a person with TENANT_PUBLISH publishes the draft as an immutable version (with a note), and a rollback is restore into the draft, review the diff, then publish, never one click. Three things are deliberately outside the draft and take effect at once: the live app status (maintenance, minimum app version, contact, sold out or closed), a venue's Help me choose publish, and policies (each save is a new version). Build-time parts (app icons, native splash, custom font files, wallet and payment integrations) reach guests only with a new store build, which the client publishes under its own Apple and Google accounts (CMS-104). Staff surfaces (POS, scanner, staff app, kitchen display) never take tenant branding; every guest surface carries the "Powered by TICVAI" credit, a toggle that is on by default (decided 2 October 2026, CHG-NOTE-009; DI-297 amended). Arabic is a first-class layout: enabling `ar` requires an Arabic font, the whole layout mirrors (numbers, times, codes and logos do not), and every authored text is a per-language value. The step-based Site Builder (CMS-102) walks a new tenant through seven steps from a venue-type preset so that a logo, four colours and a publish are enough for a working site in about 30 minutes; every step opens the full screen for its details. Vocabulary below; the element-by-element model follows; inputToOutput at the end gives worked examples.
*(source: contracts/satellite/white-label.yaml#/info; DI-223; DI-285; DI-111; DI-297; DI-296; DI-298; DI-997; DI-998; DI-1014; R139; R073; F22 step 5; F22 step 6; docs/architecture/rtl-and-theming.md)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Draft | The tenant's one working configuration. Every Save writes it; guests never see it. | Staging, Unsaved, Pending | contracts/satellite/white-label.yaml#/info |
| Publish | Make the draft the live version guests read, with a note. Needs TENANT_PUBLISH. | Go live, Deploy, Push, Save and publish | contracts/satellite/white-label.yaml#publishTenantConfig |
| Save | Write to the draft. Never publishes. | Apply, Update live | contracts/satellite/white-label.yaml#/info |
| Version | An immutable published snapshot, numbered, with who published it and the note. | Release, Revision, Backup | contracts/satellite/white-label.yaml#/components/schemas/ConfigVersion |
| Restore into draft | Copy an old version back into the draft. Publishes nothing. | Roll back, Revert, Undo | R139 |
| Live now | The changes that bypass the draft and apply at once (maintenance, availability, minimum app version, contact, Help me choose publish, policies). | Instant publish | contracts/satellite/white-label.yaml#setMaintenanceMode |
| Needs an app update | A build-time change (app icon, native splash, uploaded font, wallet or payment integration) that reaches app users only with a new store build. | Rebuild required, Build-time, Pending release | contracts/satellite/white-label.yaml#/components/schemas/ChangeScope |
| Theme | The tenant's colours, corner radius, surfaces and buttons. | Skin, Template, Style sheet | contracts/satellite/white-label.yaml#/components/schemas/Theme |
| Booking flow | The ordered steps a guest goes through to book one kind of product at one venue. | Checkout flow, Journey, Funnel, Wizard | contracts/satellite/white-label.yaml#/components/schemas/BookingFlow |
| Step | One stage of a booking flow (Date, Time, Tickets, Extras, Payment...). Marked Required, Optional or Conditional. | Page, Stage, Screen | contracts/satellite/white-label.yaml#/components/schemas/BookingFlowStepKey |
| Help me choose | The venue's short set of questions that filters the products shown. Never a consent step. | Quiz, Experience builder, Wizard, Recommender | DI-1005 |
| Module | A licensed product area a tenant switches on for guests (Dining, Shop, Map...). Off means hidden, not greyed. | Plugin, App, Feature | contracts/satellite/white-label.yaml#setModuleEnablement |
| Feature | A finer switch inside the guest app (guest checkout, AI concierge, Apple Wallet...). | Module, Add-on | contracts/satellite/white-label.yaml#setFeatureToggles |
| Buy tickets | The persistent button in the guest app that opens GST-003, and its label. | Book now, Shop, Purchase | DI-1081 |
| Powered by TICVAI | The platform credit on every guest surface; a toggle, on by default, off only where the venue's licence allows. | Built by TICVAI, Made by TICVAI | DI-297 / decided 2 October 2026 by Chinmay (CHG-NOTE-009) |
| Site Builder | The seven-step guided set-up (CMS-102). | Wizard, Onboarding, Setup assistant | DI-997 |
| Venue override | A booking setting one venue sets differently from the tenant; everything else is inherited. | Exception, Custom setting | DI-1063 |
| Sold out today / Closed | The two availability signals guests see; sold out means come another day, closed means the venue is not open. | Unavailable, Error | R073 |
| Maintenance | The tenant-branded page shown while the guest web and app are switched off, with when they are expected back. | Down, Outage, Offline | contracts/satellite/white-label.yaml#setMaintenanceMode |
| Domain | The web address the tenant's guests use; Verify proves the tenant controls it before a certificate is issued. | URL, Site address, DNS | contracts/satellite/white-label.yaml#claimCustomDomain |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `WEB-034` | Lost & Found | A | 11 | 28 | 6 | 1 | 1 | 0 | guest | review (client-verified) |
| `WEB-045` | Help Centre & Accessibility | A | 0 | 27 | 6 | 0 | 3 | 0 | guest | review (client-verified) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `WEB-034` Lost & Found

**Report something you left behind.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #18227 (APP-WEB-WEB-034) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listMyCases` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** Reports already loaded stay read-only with their age. **Reporting a loss and replying are disabled offline** — both need the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk or … |
| Opens with | `subjectId` (session), `caseId` (deepLink) · cold entry: A case opened from a notification or the list. **Optional** — the ordinary way in is to raise a new one, not to open an old one. |
| Route | `/lost-found` |

**What the spec says about it.** Added 17 August for parity with GST-034. **Not on the wireframe board** — needs drawing. CF-93. **Guest case operations wired 24 August.** **No case operation was guest-callable** — a guest could raise nothing and read nothing, and `check-screens` refused the staff-permissioned ones on a guest surface. `listMyCases`, `raiseMyCase` and `replyToMyCase` are scoped to the caller rather than filtered by a subject parameter.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The guest reports something they lost and follows it until it is found or closed. Lost and found is a case. The guest who lost it and the steward who found it are in one conversation, and the guest can see the state without asking again. The form must capture what the lost-property desk needs to match (what, colour, brand, where, when, a photo), not just a sentence.

**Fixed on main** (the package already carries these; draw what it says): The guest report uses raiseMyCase (kind, summary, detail, venueId, orderRef), which has no item kind, colour, brand, location, time or … (CHG-SGU-017); The prototype has no lost-item form; it uses the generic case form. (CHG-SGU-017).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which operation records a guest's lost-item report so it is matchable - recordLostItem alongside the case, or an extended raiseMyCase?** → Drawn default stands (answer: "Default / recommended accepted"): Draw the item fields; send them as the case detail until the operation is chosen. *(decided by Chinmay, 2026-10-02; DEC-026 / CHG-NOTE-002)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| What did you lose? | select | optional | — | Bag · Phone · Wallet · Keys · Clothing · Jewellery · Documents · Toy · Buggy · Other | — | Kind (bag, phone, wallet, keys, clothing, jewellery, documents, toy, buggy, other), colour, brand, description, where and when it was last seen, and photos. Sent as `recordLostItem` with foundOrLost … | `LostItem.kind` |
| Colour, brand and description | text area | optional | — | — | — | — | `LostItem.description` |
| Photos | media picker (several) | optional | — | — | PNG, JPG, SVG or MP4 from the media library | Optional photos of the item. | `LostItem.photoAssetIds` |

**Form: Raise my case** (modal, opened by *Raise my case*; *Raise my case* calls `raiseMyCase`, *Cancel* sends nothing)

Raises the case (`raiseMyCase`, kind lost property) and records the lost item (`recordLostItem`, foundOrLost lost, caseId) in the same act; the guest fills one form.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Created on the device, so a retry after a dropped connection carries the same id and is the same case. | `raiseMyCase` body |
| Kind `kind` | select | required | — | Lost property · Complaint · Question · Accessibility · Refund request · Other; Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.; A case raised as `other` must carry a non-empty `detail` … | — | What the guest says the case is about, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. | `raiseMyCase` body |
| Summary `summary` | text field | required | — | max length 200 | — | Lands in `Case.subject` — the case's one-line title. | `raiseMyCase` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time when the guest raised it. The server stamps `syncedAt` on arrival; both are kept (naming-and-style 5.2), because the SLA clock starts at `recordedAt`, not at the … | `raiseMyCase` body |
| Detail `detail` | text field | optional | — | — | — | Required, and not empty, when `kind` is `other` (decided 28 September, audit R222); a 400 otherwise. | `raiseMyCase` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `raiseMyCase` body |
| Order ref `orderRef` | text field | optional | — | — | — | — | `raiseMyCase` body |

Errors to draw in the form: 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema

**Form: Reply to my case** (modal, opened by *Reply to my case*; *Reply to my case* calls `replyToMyCase`, *Cancel* sends nothing)

**Collects what `replyToMyCase` sends before it is called.** Required: `message`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Message `message` | text area | required | — | min length 1; max length 10000 | — | — | `replyToMyCase` body |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **What did you lose**: Chips from the item kinds (Bag, Phone, Wallet, Keys, Clothing, Jewellery, Documents, Toy, Buggy, Other), plus colour and brand. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/LostItem)*
- **Where and when**: The area last seen (a list of the venue's points, e.g. Wave Pool, Lockers B) and the approximate time on the visit date. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/LostItem)*
- **Photo**: Optional, up to a few photos; useful for matching. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/LostItem)*
- **Contact**: Taken from the signed-in profile; the case number is the reference. *(source: contracts/satellite/marketing-crm.yaml#raiseMyCase)*

#### Outputs: what the screen shows and produces

**Shown**

**Every case** (data table, from `listMyCases`)

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

**The selected case** (detail panel, from `listMyCases`)

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
| Is sla breached | yes / no (icon or chip) | Computed when read, never stored. True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` … |
| Sla paused seconds | 1,234 | Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock. |
| Escalation count | 1,234 | — |
| Resolved at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Raise my case (primary button) | `raiseMyCase` POST `/my/cases` | inline | Case | 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema | opens modal first |
| Reply to my case (secondary button) | `replyToMyCase` POST `/my/cases/{caseId}/messages` | inline | CaseDetail | — | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Report status**: Case number and status. When staff tie a found item to the report, show "Possible match - is this yours?" with the found item's photo. Once confirmed, show where to collect it and until when it is kept. *(source: contracts/satellite/marketing-crm.yaml#matchLostItem; contracts/satellite/marketing-crm.yaml#/components/schemas/LostItem)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Reply**: Adds a guest message to the case thread (never an internal note). *(source: contracts/satellite/marketing-crm.yaml#replyToMyCase)*

**Data it reads**: `listMyCases` (onLoad, The cases this guest raised)

**Where the user goes next**

- → `GST-034` Lost & Found: *They track it*; carries `caseId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The lost found list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the lost found untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No lost found yet. Offers Raise my case (`raiseMyCase`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listMyCases` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** Reports already loaded stay read-only with their age. **Reporting a loss and replying are disabled offline** — both need the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk or lost-property point, or any member of staff. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema |

#### Edge cases to draw

- **Offline**: Reporting and replying are disabled and the page shows the lost-property point and how to reach staff in person. *(source: R148)*
- **The item is not found before the disposal date**: The report closes with "Not found by 30 Nov 2026"; the guest can reply to reopen within the venue's window. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/LostItem; contracts/satellite/marketing-crm.yaml#reopenCase)*

#### Consistency with other screens

- Match `GST-034`: Same form, same statuses, same "Possible match" wording.
- Match `BO-073`: The guest's report must appear in the register as a lost item so staff can match it to found items.
- Match `EMP-028`: A steward handing in an item creates the found side of the match.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
report:
  number: CA-1042
  item: Bag
  colour: Black
  brand: Herschel
  where: Wave Pool loungers
  when: Sat 26 Sep 2026 about 15:00
match: Black backpack handed in at Lockers B, Sat 26 Sep 2026 16:40 - collect from Guest Services, kept until 26
  Oct 2026
```

#### Permissions

- `listMyCases` → no permission · guest
- `raiseMyCase` → no permission · guest
- `replyToMyCase` → no permission · guest
- `recordLostItem` → `CASE_MANAGE` (configure) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.69 | Lost & Found - System shall support lost and found requests. | Guest Mobile App & Branding | CONTRACTED | data `LostItem` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Lost & Found: guests log lost items in the app; back-office staff match and mark items found for collection, with full tracking. *(client request · MoM 10 Aug 2026, 4.6 AI Functions, Lost & Found, Reviews, Loyalty · DI-208)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-034` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match partial): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Account → 'Lost & found, reports'; Help → 'Your cases' → Raise a case → topic 'Lost property'*. Differences: No lost-item report form (item, where, when, photo); reported via the generic case form. The prototype has no lost-item form; it uses the generic case form. A prototype gap: the build follows this screen (kind, colour, brand, where last seen, photos), not the prototype (CHG-SGU-017).
- Flow F54 *Something goes wrong in the venue*, step 3: They report something lost. → **Lost and found is a case.** F70 is the staff side of the same object — the guest who lost it and the steward who found it are in one conversation.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-034?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Raise my case, Reply to my case.
- [ ] Every transition is wired: `GST-034`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-045` Help Centre & Accessibility

**Answers, policies and the accessibility statement.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Support · wave 2 · needs the `core` module |
| Block | Block A · ticket #18096 (APP-WEB-WEB-045) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listFaqs` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** Help already loaded stays readable, marked with its age. **Raising a case is disabled offline** — it needs the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk, or any member of staff. |
| Opens with | nothing: it opens on its own · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a … |
| Route | `/help-centre-and-accessibility` |

**What the spec says about it.** **P01 Board 4 drew *Help Centre* and *Accessibility Statement* and neither could load content.** `listFaqs` and `listContentPages` were app-only. **Rev 3 (decided 29 September).** Shows *What's new* (GAP-B2). One implementation with WEB-025, both ids kept (GAP-D3).

**Known gaps.** Replaced by `listPublishedFaqs`, the guest read of the same data. Replaced by `listPublishedContentPages`, the guest read of the same data.

**From the White Label & CMS process.** One Help view with tabs FAQ, My cases, Policies, Accessibility, plus app status and What's new. Public: a guest who is not signed in can read every answer and policy. All text is the tenant's, per language.

**Fixed on main** (the package already carries these; draw what it says): listPolicies is staff-only (TENANT_CONFIGURE, no guest security), so the Policies tab has nothing a guest can read. (CHG-GST-002); emptyNoAccess says "Sign in to see this"; listFaqs and listContentPages need a guest session. (CHG-GST-002); No rule says which content page is the accessibility statement (a categoryCode, a slug, FooterConfig.legalLinks.accessibilityUrl or the … (CHG-GST-003).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where does the accessibility statement live?** → Drawn default accepted: The accessibility Policy is the statement; content pages with categoryCode accessibility are the practical guides. *(decided by Chinmay, 2026-10-02; DEC-165 / CHG-NOTE-009)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category code | text field | — | — | `listPublishedContentPages` ?categoryCode |
| Slug | text field | — | pattern `^[a-z0-9-]+$` | `listPublishedContentPages` ?slug |
| Kind | radio group | — | Privacy · Terms and conditions · Refund · Cookie · Accessibility | `listPublishedPolicies` ?kind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Questions and answers** (card list, from `listPublishedFaqs`): Categories in their order, each opening to its questions. Was the generated table 'Every faq category'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Name | in the reader's language | — |
| Entries | list or chips (count when long) | — |

**Help and accessibility pages** (card list, from `listPublishedContentPages`): The accessibility statement is the page in the `accessibility` category. Was the generated table 'Every content page'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Title | in the reader's language | — |
| Icon | the image or video | — |

**Policies** (card list, from `listPublishedPolicies`): The current terms, privacy, refund, cookie and accessibility policies; a card opens the policy's `body` in the guest's language.

| Shows | Format | Notes |
|---|---|---|
| Title | text | — |
| Version | text | The version a consent records (a guest who consented to version 3 consented to version 3). |
| Effective from | 1 Oct 2026 | — |

**Help Centre & Accessibility** (card list)

**Detail** (detail panel)

**What's new** (card list, from `getTenantAppStatus`): Public, localised release notes from `getTenantAppStatus` `whatsNew`, newest first.

| Shows | Format | Notes |
|---|---|---|
| Is published | yes / no (icon or chip) | True once any version has been published. |
| Published version | text | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Draft version | text | Staff only. |
| Has unpublished changes | yes / no (icon or chip) | Staff only. The working draft differs from the current version's `snapshot`. |
| Active module count | 1,234 | Staff only. `ModuleEnablement` rows with `isEnabled` true. |
| Licensed module count | 1,234 | Staff only. `ModuleEnablement` rows with `isLicensed` true. |
| Active page count | 1,234 | Staff only. Content pages that are `published` and enabled. |
| Is in maintenance | yes / no (icon or chip) | — |
| Maintenance message | in the reader's language | — |
| Expected back at | 1 Oct 2026, 14:30 | — |
| Minimum app version | grouped details | The oldest guest app build still allowed to run (decided 28 September, audit R073). |
| Ios | text | — |
| Android | text | — |
| Contact | grouped details | How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided … |
| Phone | +971 50 123 4567 | — |
| Email | email, tap to write | — |
| Whatsapp | text | — |
| Address | in the reader's language | — |
| Opening hours | in the reader's language | Prose, as the guest reads it. The bookable hours are the catalogue's. |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **FAQ**: Categories in the tenant's order, published entries only, search across questions, answers as sanitised rich text. *(source: contracts/satellite/white-label.yaml#listFaqs)*
- **Policies**: Current version of each policy, with version number and effective date. *(source: contracts/satellite/white-label.yaml#/components/schemas/Policy)*
- **Accessibility**: The tenant's accessibility statement and pages (step-free routes, facilities, what to expect). *(source: DI-190; DI-243)*
- **What's new**: Up to 10 public release notes, newest first, localised. *(source: DI-1073; contracts/satellite/white-label.yaml#/components/schemas/TenantAppStatus)*

**Data it reads**: `listPublishedFaqs` (onLoad, The published FAQs, readable before sign-in (GFIX-2)); `listPublishedContentPages` (onLoad, The live help and accessibility pages, readable before …); `getTenantAppStatus` (onLoad, App status and the public *What's new*); `listPublishedPolicies` (onLoad, Terms, privacy, refund, cookie and accessibility policies …)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content resolves in place. |
| Error (`?state=error`) | Could not load. **The rest of the site is unaffected.** |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel. |
| Empty, no results (`?state=emptyNoResults`) | No question or page matches what was typed; the categories stay. Names the search and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | **Nothing here needs a sign-in** (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-2)): the screen reads only what the tenant has published, which is public, so there is no no-access case. A host that belongs to no tenant shows the platform's neutral holding page. |
| Offline (`?state=offline`) | **The offline banner shows.** Help already loaded stays readable, marked with its age. **Raising a case is disabled offline** — it needs the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk, or any member of staff. |

#### Edge cases to draw

- **No FAQs published**: Show contact options (WEB-028) instead of an empty list. *(source: contracts/satellite/white-label.yaml#listFaqs)*

#### Consistency with other screens

- Match `GST-040`: Same tabs and wording in the app.
- Match `WEB-025`: One implementation, both ids.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
faq:
  question:
    en: Can I bring my own food?
    ar: هل يمكنني إحضار طعامي الخاص؟
  answer:
    en: Sealed snacks and water are welcome. Glass is not allowed.
```

#### Permissions

- `listPublishedFaqs` → no permission · anonymous, guest, device
- `listPublishedContentPages` → no permission · anonymous, guest, device
- `getTenantAppStatus` → no permission · device, guest, staff
- `listPublishedPolicies` → no permission · anonymous, guest, device

**A refused user sees:** **Nothing here needs a sign-in** (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-2)): the screen reads only what the tenant has published, which is public, so there is no no-access case. A host that belongs to no tenant shows the platform's neutral holding page.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- The guest Help screen shows app status and a public, localised "what's new" (release notes). *(agreed · design review 29 Sep 2026, GAP-B2 · B. Help: app status + recent changes · DI-1073)*
- Custom content pages per venue (e.g. "Plan Your Visit", Accessibility) that follow accessibility guidelines. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-190)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Availability and maintenance*, set in `CMS-001` Tenant Workspace:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Availability and maintenance message (`maintenance.message`) | English and Arabic (Arabic right to left) | — | — |
| Expected back at (`maintenance.expectedBackAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | — |
| Minimum app version: ios (`maintenance.minimumAppVersion.ios`) | pattern `^\d+\.\d+\.\d+$` | — | — |
| Minimum app version: android (`maintenance.minimumAppVersion.android`) | pattern `^\d+\.\d+\.\d+$` | — | — |
| Contact: phone (`maintenance.contact.phone`) | +971 5X XXX XXXX (E.164) | — | — |
| Contact: email (`maintenance.contact.email`) | name@example.ae | — | — |
| Contact: address (`maintenance.contact.address`) | English and Arabic (Arabic right to left) | — | — |
| Contact: opening hours (`maintenance.contact.openingHours`) | English and Arabic (Arabic right to left) | — | Prose, as the guest reads it. The bookable hours are the catalogue's. |
| Availability (`maintenance.availability`) | Open · Sold out · Closed | Open | The sold-out or closed signal (decided 28 September, audit R073). `open` is the normal state. |
| Availability message (`maintenance.availabilityMessage`) | English and Arabic (Arabic right to left) | — | — |

Also set there, as content the tenant writes: is in maintenance, minimum app version, contact, contact: whatsapp.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-045` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match partial): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Header 'Help' → 'Policies and accessibility'; footer 'Accessibility'*. Differences: Not a separate screen: part of the WEB-025 Help centre page.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-045?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

## Tenant configuration on every guest screen

Every guest screen in this batch is white-label. These elements are set by the tenant in the CMS and apply to every screen of the guest app (each screen's block lists the ones particular to it). **Draw with the default theme; on the key screens add one alternate tenant theme** (below), so a reviewer sees the brand is configuration, not paint. The full map, with the input-to-output examples: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Element | Configured in | Allowed values | Default | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | Light · Dark · Duotone | Light | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG, JPG, SVG or MP4 from the media library | — | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | min 0; max 10 | 3 | — |
| Splash background colour (`brand.splashBackgroundColour`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | #RRGGBB | — | — |
| Show loading indicator (`brand.showLoadingIndicator`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | — | on | — |
| Intro video (`brand.introVideoAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Powered by TICVAI credit (`brand.showPoweredBy`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | — | on | the *Powered by TICVAI* credit on the launch screen, at the foot of Account and in the web footer; on by default, and switching it off needs the licence add-on (403 … |
| Primary colour (`theme.primaryColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | body text on the background |
| Corner radius (`theme.cornerRadius`) | `CMS-005`, `ADM-016` | min 0; max 32 | — | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | `CMS-005`, `ADM-016` | Glass · Solid | Glass | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | `CMS-005`, `ADM-016` | Solid · Outline · Pill | Solid | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | `CMS-005`, `ADM-016` | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Primary latin (`fonts.primaryLatin`) | `CMS-003` | — | — | headings and body text in English |
| Primary arabic (`fonts.primaryArabic`) | `CMS-003` | Required when `ar` is among the tenant's languages (audit R163). | — | headings and body text in Arabic |
| Secondary latin (`fonts.secondaryLatin`) | `CMS-003` | — | — | the secondary face (eyebrows, numbers) in English |
| Secondary arabic (`fonts.secondaryArabic`) | `CMS-003` | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | the secondary face in Arabic |
| Custom font images (`fonts.customFontAssetRefs`) | `CMS-003` | PNG, JPG, SVG or MP4 from the media library | — | Uploaded font files, as `MediaAsset` ids. |
| Header layout (`header.layout`) | `CMS-009` | Logo left · Logo centre · Logo with menu | — | the header: logo left, logo centred, or logo with the menu |
| Show logo (`header.showLogo`) | `CMS-009` | — | on | — |
| Show menu (`header.showMenu`) | `CMS-009` | — | on | — |
| Show notifications (`header.showNotifications`) | `CMS-009` | — | on | — |
| Background colour (`header.backgroundColour`) | `CMS-009` | #RRGGBB | — | — |
| Navigation kind (`navigation.kind`) | `CMS-009` | Bottom navigation · Drawer · Tabs | — | the main navigation: bottom tab bar, drawer, or tabs |
| Navigation items (`navigation.items`) | `CMS-009` | at most 12 | — | — |
| Buy button (`navigation.buyButton`) | `CMS-009` | — | — | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. |
| Footer columns (`footer.columns`) | `CMS-009` | — | — | — |
| Legal links (`footer.legalLinks`) | `CMS-009` | — | — | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. |
| Copyright text (`footer.copyrightText`) | `CMS-009` | — | — | — |
| Social links (`footer.socialLinks`) | `CMS-009` | — | — | — |
| Languages (`languages.languages`) | `CMS-011`, `ADM-018` | at least 1 | — | the language button in the header; Arabic flips every screen right to left |
| Default language (`languages.defaultLanguage`) | `CMS-011`, `ADM-018` | ISO 639-1 code, shown as the language name | — | the language a first visit opens in |
| Modules (`modules.modules`) | `CMS-001`, `ADM-424` | — | — | — |
| Features (`features.features`) | `CMS-001` | — | — | — |
| Custom domain hostname (`domains.hostname`) | `CMS-017`, `ADM-017` | — | — | — |
| Custom domain kind (`domains.kind`) | `CMS-017`, `ADM-017` | Guest web · Guest app · Partner portal · Developer portal | — | — |
| Verification method (`domains.verificationMethod`) | `CMS-017`, `ADM-017` | Dns txt · Cname · Http file | Dns txt | — |
| Entity kind (`seo.entityKind`) | `CMS-013` | Content page · Product · Event · Performance · Membership · Promotion · Venue | — | — |
| Entity (`seo.entityId`) | `CMS-013` | shows names, sends the id | — | — |
| Locale (`seo.locale`) | `CMS-013` | — | — | — |
| SEO metadata title (`seo.title`) | `CMS-013` | — | — | — |
| Meta description (`seo.metaDescription`) | `CMS-013` | — | — | — |
| Keywords (`seo.keywords`) | `CMS-013` | — | — | — |
| Canonical URL (`seo.canonicalUrl`) | `CMS-013` | — | — | — |
| Slug (`seo.slug`) | `CMS-013` | — | — | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking and now is not. |
| Hreflang (`seo.hreflang`) | `CMS-013` | — | — | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page. |
| Schema org type (`seo.schemaOrgType`) | `CMS-013` | — | — | — |
| Open graph (`seo.openGraph`) | `CMS-013` | — | — | — |
| Is auto generated (`seo.isAutoGenerated`) | `CMS-013` | — | on | 22.11.2. Generated by default and overridable. |
| No index (`seo.noIndex`) | `CMS-013` | — | off | — |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | `CMS-005`, `ADM-016` | — | — | the one main call to action on each screen, when it should differ from the brand colour |
| Component colours: pay button (`theme.componentColours.payButton`) | `CMS-005`, `ADM-016` | — | — | the Pay button at checkout |
| Buy button: style (`navigation.buyButton.style`) | `CMS-009` | Raised · Floating · Flat · Hidden | Raised | the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden |

**The alternate tenant theme (Coastal Aqua)**: Primary colour #0077B6; Secondary colour #023E8A; Accent colour #FFB703; Background colour #F5FAFC; Text colour #0B1324; Corner radius 18; Surface style Solid; Button style Pill; Logo variant Duotone; Header layout Logo centre; Step indicator Dots; Card layout Cards across; Card size Standard; Cart layout Floating icon; Fonts Poppins / Tajawal.
**Key screens to show in it:** `WEB-001`, `WEB-005`, `WEB-006`, `WEB-010`, `WEB-012`, `GST-001`, `GST-007`, `GST-041`, `KSK-002`, `KSK-003`.

**Decided for every guest screen:** **No dark or light mode.** The venue's chosen theme applies on every device setting; `Theme.darkMode` is deprecated and ignored, never drawn, and the guest app has no Light/Dark switch (Chinmay, 2 October, Q150; CHG-CSA-035). ***Powered by TICVAI* is a tenant toggle, on by default** (`brand.showPoweredBy`): shown on the launch screen, at the foot of Account and in the web footer; switching it off needs the licence add-on, or 403 `powered-by-locked` (Chinmay, 2 October, Q160; DI-297; CHG-CSA-036). **Each homepage section sets its card count and its scroll animation** (`maxItems`; `scrollAnimation` rise, scale, slide, blur or none, default rise): every customisation option of the approved wireframe (Chinmay, 2 October, Q152 and Q153; DI-1088; CHG-CSA-040). **Landing-page templates.** A tenant with no landing page of its own starts from a TICVAI template (`listLandingPageTemplates`, kept as `HomepageLayout.templateKey`); one with its own site links in with deep links (`landingSource` ownSite) (Chinmay, 2 October, batch 2 #41; CHG-CSA-037).

**Never configurable:** A dark or light mode: the guest surfaces have one theme, the venue's (Chinmay, 2 October; CHG-CSA-035). Semantic colour pairs (success, warning, danger, neutral) are not overridable: a tenant who recolours danger to their brand green has made a destructive confirmation look like a success (`screens/_design-tokens.yaml` whiteLabel). Site structure and the navigation flow are fixed and adapt to the product configuration (MoM 3 Aug, DI-119); a guest always books a product or package, never a resource (DI-502). A colour pair that fails 4.5:1 contrast is refused by the CMS, not warned (setTheme 400 ContrastProblem, audit R139).

## Reference designs and the trackers for this platform

**P01 reference designs** (from `handoff/design-batches/apps/1-guest-app/README.md`)

- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the website. Rev 3 with the 29 September fixes and the 30 September feedback (group booking with a headcount, multi-park counters, surf session tickets, the swim-ability answer, transport stations and departures, popular route cards; `CLIENT-RESPONSE-30SEP.md` beside it). The client approved it for development once W1 to W10 are in.
- `sources/designs/guest-rev3-30-september/TICVAI Visit Planner.dc.html`: the visit planner. WEB-050 Plan Your Visit is this file.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-038, DI-040, DI-042, DI-044, DI-045, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P01 as a whole** (23: 3 open, 20 closed). Open first; a closed row says where it went on 30 September.

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker)*
- **S9** Final UI/UX for the website and the mobile app *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **T1** Feedback on the revised website and mobile wireframes *(Allam / Qossai · Open · due 1 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A28** Review the 'Viva Ticket' website as a reference for ticket-flow variations *(Softlabs Design Team · Low · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A29** Collate design references/inspiration and share with TICVAI, organized by mobile app, website, and admin/back-office pages *(Softlabs (Sahil & Aishwarya) · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A55** Implement per-tenant module visibility toggles (e.g., hide Dining, Retail, or other services) configurable independently for the guest website and mobile app *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker)*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker)*
- **A115** Apply HA selectively to revenue-critical components (ticketing, POS, B2C) same-region, with multi-region DR as an optional add-on *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Aug 2026 · workshop tracker)*
- **A118** Commission the third-party penetration test before go-live (ticketing, B2C, B2B, mobile apps) and resolve all severities *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 24 Aug 2026 · workshop tracker)*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker)*
- **A174** Cross-check the six previously-scoped wallet types against Allam's documentation and deliver the three wireframe flows (ticketing, F&B, retail) plus the revised B2C flow *(Chinmay Parab / Pradnya Yeram / Allam · High · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker)*
- … 9 more in `handoff/design-inputs/task-tracker-index.json`

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

### Across P01 Guest Web

- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)*
- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Guest-facing copy may say "session" (surf sessions, timed sessions) as a glossary exception, like "Booking". *(agreed · design review 29 Sep 2026, CFG-10 · 'Sessions can be added, edited or closed from Config -> Sessions' · DI-1064)*
- Never ask the same thing twice: table zone is picked on the table map (no zone step before it); height is asked once (height bands on the water-park day pass are the eligibility check); party/school summaries prefill headcount, child's name and age from the earlier form. *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): repeated steps removed · DI-1000)*
- Confirmed final: cart sliding in from the right or bottom, card size options, and cart-sidebar placement left or right; Qossai specifically liked the compact card size. No further changes requested. *(agreed · MoM 24 Sep 2026, 4.10 Guest Web App — Card Layout & Cart Configuration Confirmed · DI-991)*
- Headers are reserved for standard elements only (venue image, category tabs, language bar, profile icon), applied consistently; date/availability selection belongs in the main content below the header, never in the header. Header/layout patterns must be adapted for mobile, which looks and behaves differently. *(agreed · MoM 24 Sep 2026, 4.9 Guest Web App — Specific UX Feedback (Header/Date Placement Standardization) · DI-990)*
- A language button (EN / العربية) sits in the header next to the profile icon, web and mobile. Arabic flips the whole layout right-to-left and switches interface text (navigation, buttons, booking steps, ticket names and tags, cart, seat map, checkout, account). Venue, show and dish names stay as written. *(client request · design review 23 Sep 2026, Header 2. Language icon in the header · DI-975)*
- Replace "Sign in / Create account" in the header with a single profile icon. It opens one screen with Log in and Register tabs; signed-in guests get their account menu from the same icon. *(client request · design review 23 Sep 2026, Header 1. One profile icon in the header that opens login / register · DI-974)*
- Allam's model reference: a simple card-based family-entertainment-centre site with minimal clicks, a right-side cart drawer, "help me choose", clear categories, video that autoplays when a guest taps "read more", adapting seamlessly between desktop and mobile. Allam and Qossai want this simplicity to guide the guest experience. *(client request · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-952)*
- **Open question.** Allam expects a large volume of feedback on the guest web/mobile prototype; detailed feedback goes to a separate dedicated session with Qossai and Allam. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-888)*
- The reviewed prototype is the actual guest-facing B2C site customers browse and book from, not a CMS tool. A separate, more limited white-label interface lets a client adjust colours, fonts and layout from a menu of options; not yet built in the prototype. *(agreed · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-887)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- Qossai is dissatisfied with the current B2C guest platform build and wants a separate vision session; references: the "Little Explorer" site and Six Flags. Six Flags cues: single-page flow. *(client request · MoM 8 Sep 2026, 4.20 Planning & Next Steps · DI-736)*
- Allam: most guests book from a smartphone, so the mobile version of the booking flows is the higher priority to validate (only desktop shown). *(client request · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough · DI-684)*
- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*
- Configurable cookie consent banner (accept/reject) per website; some cookies flagged mandatory (non-rejectable), others optional; templated and configurable in the system. *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-617)*
- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Six Flags Kidiya reference: fixed header with configurable navigation (logo, Explore/Tickets/Passes, sub-menus), every item toggleable via the CMS. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-424)*
- Allam: the venue's main website is fully venue-managed; after "Book Now" the white-label B2C flow keeps the venue's header/footer branding while product selection, cart and checkout are TICVAI-managed. Header/footer links to non-checkout pages redirect to the main venue site. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-397)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- Qossai: present products with video rather than static images (as Talabat-style apps do); see benchmark app "222" for further inspiration. *(client request · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-222)*
- Qossai shared reference apps (Al Qadiya / Six Flags Saudi Arabia, and "The District" by Zomato) and cited their use of video over static images as design inspiration. *(client request · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-146)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Base ticket-booking UX (web and mobile) on current market best practice rather than the demoed references as-is; Allam recommends the "Viva Ticket" website as a reference for the flow variations. *(agreed · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-125)*
- A multi-language toggle switches the entire site's content. *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-120)*
- Allam: banner, header, footer and background color are CMS-configurable per client, but site structure and navigation flow are fixed and adapt automatically to product configuration (dated, non-dated, seated, membership products surface the right fields). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-119)*
- All sites are fully mobile-responsive; e.g. the desktop calendar view collapses into a mobile-optimized layout. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-113)*
- A "powered by [platform]" footer credit is fixed and not client-editable. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-111)*
- One client can run multiple branded sites from the same setup, e.g. two brands sharing a footer but with distinct headers and hero banners. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-110)*
- White-label sites share one platform/template but each is configured independently: header, footer, logo, colors, fonts and hero banner are client-editable from the backend. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-108)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getTenantAppStatus": {"method":"GET","path":"/tenant-config/status","contract":"white-label","summary":"App status and recent changes","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantAppStatus"},
"listMyCases": {"method":"GET","path":"/my/cases","contract":"marketing-crm","summary":"The cases this guest raised","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPublishedContentPages": {"method":"GET","path":"/storefront/pages","contract":"white-label","summary":"The live content pages, readable before sign-in","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"categoryCode","in":"query","required":false},{"name":"slug","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPublishedFaqs": {"method":"GET","path":"/storefront/faqs","contract":"white-label","summary":"The published FAQs, readable before sign-in","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"PublishedFaqCategory"},
"listPublishedPolicies": {"method":"GET","path":"/storefront/policies","contract":"white-label","summary":"The tenant's current legal policies, readable before sign-in","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"kind","in":"query","required":false}],"requestBody":null,"responds":"PublishedPolicy"},
"raiseMyCase": {"method":"POST","path":"/my/cases","contract":"marketing-crm","summary":"Report something — lost property, a complaint, a question","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Case"},
"recordLostItem": {"method":"POST","path":"/lost-items","contract":"marketing-crm","summary":"Report something lost, or hand something in","permission":"CASE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LostItem","responds":"LostItem"},
"replyToMyCase": {"method":"POST","path":"/my/cases/{caseId}/messages","contract":"marketing-crm","summary":"Reply on a case the guest raised","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CaseDetail"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AppAvailability": {"type":"string","description":"**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n","enum":["open","soldOut","closed"],"default":"open"},
"Case": {"x-ticvai-persistence":"marketing.case","x-ticvai-retired-columns":["guest_name","subject","is_sla_breached"],"type":"object","required":["id","caseNumber","subject","status","priority","createdAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."},"caseNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"},"subject":{"type":"string","x-ticvai-column":"title","description":"**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"},"kind":{"allOf":[{"$ref":"#/components/schemas/CaseKind"}],"nullable":true,"description":"What the guest said it was about, where the guest raised it."},"channel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"description":"How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised — the start of the SLA clock."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the case arrived. Equal to `recordedAt` for a case raised online."},"categoryId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"},"status":{"$ref":"#/components/schemas/CaseStatus"},"priority":{"$ref":"#/components/schemas/CasePriority"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"relatedOrderId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"isSlaBreached":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"},"slaPausedSeconds":{"type":"integer","description":"Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"},"escalationCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"CaseDetail": {"x-ticvai-persistence":"marketing.case","allOf":[{"$ref":"#/components/schemas/Case"},{"type":"object","properties":{"description":{"type":"string"},"resolutionNote":{"type":"string","nullable":true},"messages":{"type":"array","items":{"$ref":"#/components/schemas/CaseMessage"}}}}]},
"CaseKind": {"type":"string","description":"**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n","enum":["lostProperty","complaint","question","accessibility","refundRequest","other"]},
"CaseMessage": {"x-ticvai-persistence":"marketing.case_message","type":"object","required":["id","body","isInternal","authorKind","recordedAt"],"properties":{"resolution":{"type":"string","description":"**What was actually done about it.** Indexed for retrieval: an agent facing a complaint benefits more from how the last one was resolved than from a policy. Without this column `marketing.case` can only embed its subject line.\n"},"id":{"type":"string"},"body":{"type":"string"},"isInternal":{"type":"boolean"},"authorKind":{"type":"string","enum":["agent","guest","system","ai"]},"authorPrincipalId":{"type":"string","format":"uuid","nullable":true},"channel":{"$ref":"#/components/schemas/MessageChannel"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time","description":"Device time — `addCaseMessage` is offline-capable."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the message arrived."}}},
"CasePriority": {"type":"string","enum":["low","normal","high","urgent"]},
"CaseStatus": {"type":"string","enum":["open","inProgress","awaitingGuest","escalated","resolved","closed"]},
"LocalisedRichText": {"x-ticvai-persistence":"none — jsonb column","type":"object","description":"Keyed by language code. Values are sanitised HTML.","additionalProperties":{"type":"string"}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"LostItem": {"type":"object","x-ticvai-persistence":"marketing.lost_item","description":"BL-021. **Screens existed on three platforms and `lostAndFound` is a `ModuleKey`, and there was no item, no claim and no match between them** — which is the whole capability.\nGeneric case management holds a conversation about a lost bag. **It cannot tell you that the bag somebody handed in on Tuesday is the one somebody asked about on Monday**, and that match is the only thing the module is for.\n","required":["id","kind","foundOrLost","venueId","reportedAt"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"foundOrLost":{"type":"string","enum":["lost","found"],"description":"**One entity, two directions.** A guest reports a loss and a steward reports a find, and modelling them separately means matching across two tables that drift.\n"},"kind":{"type":"string","enum":["bag","phone","wallet","keys","clothing","jewellery","documents","toy","buggy","other"]},"description":{"type":"string"},"colour":{"type":"string","nullable":true},"brand":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid"},"lastSeenPointId":{"type":"string","format":"uuid","nullable":true,"description":"A point on the venue map. **Where a guest thinks they lost it is the strongest signal for a match**, and it is also the thing they are least sure about.\n"},"reportedAt":{"type":"string","format":"date-time","description":"**Device time** — `recordLostItem` is offline-capable, so this is when the loss was reported or the find handed in, not when the device synced. The `recorded_at` of naming-and-style 5.2 for this row.\n"},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the record arrived. Equal to `reportedAt` for one recorded online."},"reportedBySubjectId":{"type":"string","format":"uuid","nullable":true},"storageLocation":{"type":"string","nullable":true},"status":{"readOnly":true,"type":"string","enum":["open","matched","claimed","disposed","returned"]},"photoAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"matchedItemId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The other side of the match — set by `matchLostItem` `match` (to `otherItemId`) and cleared by `unmatch`, on both items."},"caseId":{"type":"string","format":"uuid","nullable":true,"description":"The case the guest raised about it (`raiseMyCase` with `kind` `lostProperty`), where there is one."},"disposeAfter":{"type":"string","format":"date","nullable":true,"description":"**A retention date, because unclaimed property has one.** A storeroom with no disposal date is a storeroom that fills, and the date is a venue policy rather than a default.\n"}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MinimumAppVersion": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n","properties":{"ios":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"},"android":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PolicyKind": {"type":"string","enum":["privacy","termsAndConditions","refund","cookie","accessibility"]},
"PublishedContentPage": {"x-ticvai-persistence":"none — a public projection of whitelabel.content_page","type":"object","x-ticvai-agreed":"2 October: decided by Chinmay, fix before Block A starts (GFIX-2)","description":"A live content page as a guest reads it (`listPublishedContentPages`). Only published and enabled pages exist in this view, so it carries no status.","required":["id","slug","title","body"],"properties":{"id":{"type":"string","format":"uuid"},"slug":{"type":"string","pattern":"^[a-z0-9-]+$"},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedRichText"},"iconAssetRef":{"type":"string","format":"uuid","nullable":true},"categoryCode":{"type":"string","nullable":true},"sortOrder":{"type":"integer"}}},
"PublishedFaqCategory": {"x-ticvai-persistence":"none — a public projection of whitelabel.faq_category + whitelabel.faq_entry","type":"object","x-ticvai-agreed":"2 October: decided by Chinmay, fix before Block A starts (GFIX-2)","description":"One FAQ category with its published entries only (`listPublishedFaqs`).","required":["code","name","entries"],"properties":{"code":{"type":"string"},"name":{"$ref":"#/components/schemas/LocalisedText"},"sortOrder":{"type":"integer"},"entries":{"type":"array","items":{"type":"object","required":["id","question","answer"],"properties":{"id":{"type":"string","format":"uuid"},"question":{"$ref":"#/components/schemas/LocalisedText"},"answer":{"$ref":"#/components/schemas/LocalisedRichText"},"sortOrder":{"type":"integer"}}}}}},
"PublishedPolicy": {"x-ticvai-persistence":"none — a public projection of whitelabel.policy","type":"object","x-ticvai-agreed":"2 October: decided by Chinmay, fix before Block A starts (GFIX-2)","description":"The current version of one policy as a guest reads it (`listPublishedPolicies`). Who published it and the partition key stay on `Policy`.","required":["kind","version","body","effectiveFrom"],"properties":{"kind":{"$ref":"#/components/schemas/PolicyKind"},"title":{"type":"string"},"version":{"type":"string","description":"The version a consent records (a guest who consented to version 3 consented to version 3)."},"body":{"$ref":"#/components/schemas/LocalisedRichText"},"effectiveFrom":{"type":"string","format":"date"},"requiresReconsent":{"type":"boolean","description":"True when guests who consented to an earlier version are asked again on next launch."}}},
"TenantAppStatus": {"x-ticvai-persistence":"none — computed","type":"object","description":"Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n","required":["tenantId","isPublished","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"isPublished":{"type":"boolean","x-ticvai-derived":"onRead","description":"True once any version has been published."},"publishedVersion":{"type":"string","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"draftVersion":{"type":"string","description":"Staff only."},"hasUnpublishedChanges":{"type":"boolean","x-ticvai-derived":"onRead","description":"Staff only. The working draft differs from the current version's `snapshot`."},"activeModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isEnabled` true."},"licensedModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isLicensed` true."},"activePageCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. Content pages that are `published` and enabled."},"isInMaintenance":{"type":"boolean"},"maintenanceMessage":{"$ref":"#/components/schemas/LocalisedText"},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"contact":{"$ref":"#/components/schemas/VenueContact"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"What the sold-out or closed screen says (WEB-029). Null shows the default wording."},"venues":{"type":"array","maxItems":200,"x-ticvai-derived":"onRead","description":"**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid","description":"**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."},"name":{"type":"string","maxLength":200,"description":"The venue's name (`tenancy.OrgUnit.name`)."},"city":{"type":"string","maxLength":120,"nullable":true,"description":"Shown under the name so two venues with similar names can be told apart."},"openingHoursToday":{"type":"object","nullable":true,"description":"Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.","properties":{"opens":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"},"closes":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"}}}}}},"whatsNew":{"type":"array","maxItems":10,"x-ticvai-derived":"onRead","description":"**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n","items":{"type":"object","required":["version","publishedAt","notes"],"properties":{"version":{"type":"string","description":"The release version."},"publishedAt":{"type":"string","format":"date-time","description":"When the release reached the tenant's cell."},"notes":{"$ref":"#/components/schemas/LocalisedText"}}}},"recentChanges":{"type":"array","description":"Staff only. Names the principal behind each change, so it never reaches a public response.","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}}}},
"VenueContact": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n","properties":{"phone":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"whatsapp":{"type":"string","nullable":true},"address":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Prose, as the guest reads it. The bookable hours are the catalogue's."}}}
}
```
