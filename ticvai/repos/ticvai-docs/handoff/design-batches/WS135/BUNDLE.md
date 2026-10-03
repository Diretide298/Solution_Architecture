# WS135 — Marketing CRM Configuration Reference v1.0 board 1

**10 screens · 20 operations · 26 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `CASE_VIEW, GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII, LEDGER_POST, MARKETING_MANAGE, MARKETING_VIEW`. A control nobody can use must say so,
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

### Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management)

Platform Foundation is everything the apps stand on. Five apps each have one door: the guest app and website (WEB-016, GST-042: a six-digit code to email or mobile, a password, Apple or Google, UAE Pass; never enterprise SSO), the till (POS-000: employee number and PIN, recent operators as tiles; the kitchen display is the same app), the staff handheld and scanner (EMP-001, SCN-001), Venue Management (SUP-001, the single door for the back office P08, the CMS P13, analytics P16 and the support desk P12) and TICVAI Control (ADM-001 for TICVAI's own platform operators, PTR-001 for partner users; the developer portal P14 and the sign-up P17 belong to this app too). A second factor is required by permission, not by role or device: ROLE_MANAGE, LEDGER_APPROVE and every PLATFORM_* permission, plus any the tenant adds; so a cashier never sees it and a platform operator always does. The factor is an authenticator app with an emailed code as fallback; five wrong codes lock step-up for the lockout minutes, never permanently. Guests get two-step verification only at a venue that switched it on. One person holds one session per workstation: a second sign-in is refused and only a supervisor ends the other session. Several roles mean a role prompt; one role goes straight in. The workstation decides the Sale Board, hardware and till identity, never what a person may do. Sensitive actions (refund approval, journal approval, credential reset, partner credit, commission rules, opening a platform-staff grant and 17 more) demand a fresh step-up on the operation itself, asked in place in the action's confirmation; the tenant may raise the strength, never remove it. Permission outcomes are three, never one word: self-authorised (proceeds, audited), escalated (a supervisor PIN in place), refused (the denied state, naming the permission); a missing permission is never an empty table, and a record outside the person's venues is "not found", indistinguishable from absent. The hierarchy is binding (tenant, brand, region, venue, department, sub-department, workstation; outlet beside department for F&B and retail); region owns currency, decimals, time zone, date format and fiscal year; configuration resolves nearest-ancestor across tenant, region and venue (outlet for F&B and retail), venue is the floor and a workstation is assigned a profile, never configured; every configuration screen says which level it writes and what it inherits. Venue Management is one tenant-level surface filtering across the venues in the session's scope. TICVAI's Console runs outside every cell: a platform operator picks a tenant and opens a time-boxed, audited platform-staff grant (with step-up) before any tenant action, and the tenant sees every action in its audit log (ADM-412 is the reference implementation). Approval workflows record authorisations and never perform the action; the requester cannot approve their own request; a venue may tighten and never loosen a rule from above; in-flight …
*(source: screens/P12-support-agent-console.yaml#SUP-001; R135; R126; R167; DI-1072; ADR-0002; ADR-0003; ADR-0004; R184; contracts/spine/identity.yaml#createMfaChallenge; contracts/spine/approvals.yaml#setStepUpPolicy; ADR-0011; ADR-0018; ADR-0029; R098; contracts/spine/approvals.yaml#decideApprovalRequest …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sign in / Sign out | Entering and leaving any app, staff or guest. | Login, Log in, Logon, Logout | screens/P04-point-of-sale.yaml#POS-000 … |
| Authentication code | The staff second factor from the authenticator app (or the emailed fallback). | OTP, 2FA code, token | screens/P09-platform-admin-console.yaml#ADM-001 |
| One-time code | The six-digit code a guest receives to sign in or prove a contact. | OTP, PIN, password | DI-1034; R167 |
| Two-step verification | The guest's optional second factor, asked only at venues that switched it on. | MFA, 2FA | DI-1072 |
| Tenant / Brand / Region / Venue / Department / Outlet | The binding hierarchy levels; region owns currency and dates; outlet is F&B or retail inside a venue. | Client, Customer, Org (for tenant), Site, Park, Property (for venue), Area, Territory (for region) | ADR-0011; ADR-0018 |
| Workstation (back office) / till (operator copy) | A configured device; decides Sale Board, hardware and till identity, never authorisation. | Terminal, Station, POS (for the device), till (for the Deposit Box) | ADR-0002; R156 |
| Sale Board | The configured front end a workstation loads (ticketing, F&B or retail). | Screen, Layout, Menu | ADR-0003 |
| Role | A named, fully configurable grouping of permissions; the seeded five are editable starting points. | Group, Profile | R229 |
| Staff member / Partner user / Platform operator | A tenant's staff principal; a partner's user; a TICVAI employee in the Console. | User (alone), Account, Agent (for venue staff) | F104 step 1; F104 step 4; F104 step 5 |
| Platform-staff grant | The time-boxed, audited access a platform operator opens into one tenant before acting in it. | Impersonation, Support login | R098 |
| Escalate / Refused | Escalate is supervisor approval captured in place; Refused is the denied state that names the permission. | Denied (for an action that can be escalated) | R197 |
| Approve / Reject / Return / Request information | The four decisions on an approval request; Withdraw is the requester's own act and never a rejection. | Accept, Decline, Cancel (for withdraw) | contracts/spine/approvals.yaml#decideApprovalRequest … |
| Subscription / Plan / Module / Licence | TICVAI's commercial relationship with a tenant, its plan, the modules it licenses and the limits. | Membership (that is the guest's pass) | R214 |
| Membership / Annual pass | A guest's pass product and its holder (BO-284 to BO-303). | Subscription (that is the tenant's TICVAI plan) | screens/P08-venue-back-office.yaml#BO-284 |
| Sandbox client / Production client | A developer's own test credential; a TICVAI-issued live credential after certification. | Test key, Live key, API key (without environment) | DI-927 |
| Asset (DAM) / Media (ticket) | A digital file in the library; ticket media is a wristband or card carrying entitlements. Never mix them. | Media (for a library asset) | contracts/satellite/assets.yaml#searchMedia … |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-734` | CRM Command Center | D | 1 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-735` | Guest Directory | D | 13 | 18 | 6 | 16 | 1 | 0 | — | notStarted (—) |
| `BO-736` | Guest Master Configuration | D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-737` | Customer 360 Profile | D | 0 | 70 | 6 | 12 | 3 | 0 | — | notStarted (—) |
| `BO-738` | Activity Timeline | D | 0 | 11 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-739` | Contact & Preferences | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-740` | Family & Guardians | D | 11 | 9 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `BO-741` | Corporate & Groups | D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-742` | Commerce & Documents | D | 0 | 11 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-743` | AI Guest Intelligence | D | 0 | 20 | 6 | 9 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-734, BO-736, BO-738, BO-741, BO-742, BO-743 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-734` CRM Command Center

**Give authorized users an operational and analytical overview of the customer base. Display total, new, active, inactive, registered and guest-checkout customers with tenant, brand, venue, region and date filters. Show VIP, high-value, family, corporate, group, churn-risk, duplicate and incomplete-profile indicators. Present LTV, engagement, growth, consent health and source-synchronization trends with drill- down to the underlying guests. Surface explainable AI insights and prioritized actions without bypassing consent, eligibility or access policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-734 |
| Who uses it | venue staff holding `GUEST_VIEW`, `MARKETING_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/crm-command-center-bo-734` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-007): No CRM summary operation for the command centre tiles.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The CRM command centre: the health of the guest base at a glance, with every number drilling down to the guests behind it. Totals (all, new, active, inactive, registered vs guest-checkout), indicator counts (VIP, high value, family, corporate, churn risk, possible duplicates, incomplete profiles), lifetime value, and consent health. Segmentation by source (individual, corporate, group, travel agent, OTA) is the client's own example.

**Known correction pending (do not draw the wrong version)**

- **The screen declares only searchGuests and listSegments; no operation returns the counts, trends or indicators the purpose lists.** Why: A command centre needs a summary read. Add a CRM summary operation, or the tiles cannot be built (R283 already bars counts without a summary operation). *(source: screens/P08-venue-back-office.yaml#BO-734; R283; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Search | text field | — | Requires `GUEST_VIEW_PII`: matching on personal data discloses it, so a caller without that permission who passes `search` is refused with 403 rather than having the parameter ignored. | `searchGuests` ?search |
| Segment | picker: choose a segment | — | — | `searchGuests` ?segmentId |
| Has consent for | select | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | `searchGuests` ?hasConsentFor |
| Search | text field | — | max length 200 | `listSegments` ?search |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Base totals**: Total, new this period, active, inactive, registered and guest-checkout profiles, with period comparison; each tile opens the directory filtered to it. *(source: DI-370; screens/P08-venue-back-office.yaml#BO-734)*
- **Consent health**: Share of guests reachable for marketing per channel (consent given), and consents needing renewal after a notice change. Never a single "opted in" figure. *(source: contracts/satellite/marketing-crm.yaml#getGuestConsents; DI-378)*
- **Possible duplicates**: Count awaiting review, linking to BO-746; labelled "possible duplicates", not "duplicates". *(source: DI-377; contracts/satellite/marketing-crm.yaml#listDuplicateCandidates)*
- **By source**: Individual, corporate, group, travel agent, OTA. *(source: DI-370)*

**Data it reads**: `searchGuests` (onLoad, Find a guest); `listSegments` (onLoad, Segment indicators)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-735` Guest Directory: *Guest Directory*; carries `subjectId`
- → `BO-736` Guest Master Configuration: *Guest Master Configuration*
- → `BO-737` Customer 360 Profile: *Customer 360 Profile*; carries `subjectId`
- → `BO-738` Activity Timeline: *Activity Timeline*; carries `subjectId`
- → `BO-739` Contact & Preferences: *Contact & Preferences*
- → `BO-740` Family & Guardians: *Family & Guardians*; carries `subjectId`
- → `BO-741` Corporate & Groups: *Corporate & Groups*
- → `BO-742` Commerce & Documents: *Commerce & Documents*
- → `BO-743` AI Guest Intelligence: *AI Guest Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The crm list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the crm untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No crm yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the crm are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-735`: Every tile drills into the directory with the matching filter applied and named.
- Match `BO-107`: The section landing's guest counts must equal these.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
totals:
  all: 48210
  new30d: 1932
  active: 21480
  inactive: 26730
  guestCheckout: 9120
indicators:
  vip: 412
  churnRisk: 3105
  possibleDuplicates: 512
  incomplete: 7880
consent:
  email: 61%
  whatsapp: 54%
  sms: 22%
  needsRenewal: 1204
ltv: AED 1,240.00 average lifetime value
```

#### Permissions

- `searchGuests` → `GUEST_VIEW` (read) · staff
- `listSegments` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.14.25 | Segmentation & Attribution Audit Trail | Marketing & CRM | CONTRACTED | `listSegments` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- CRM guest dashboard shows active/inactive/duplicate profile counts and lifetime value, plus guest directory/search and segmentation by source (individual, corporate, group, travel agent, OTA). *(client request · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-370)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-734` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-734`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 1: Opens CRM Command Center → Give authorized users an operational and analytical overview of the customer base. Display total, new, active, inactive, registered and guest-checkout customers with tenant, brand, venue, region and …
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F244 branch at step 1 (expected): when Nothing has been set up on CRM Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F244 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-734?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-735`, `BO-736`, `BO-737`, `BO-738`, `BO-739`, `BO-740`, `BO-741`, `BO-742`, `BO-743`.
- [ ] Every gated control is gated: `GUEST_VIEW`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-735` Guest Directory

**Provide a permission-controlled directory for locating and managing every guest record. Search by name, email, mobile, guest ID, external ID, ticket, booking, membership or loyalty identifier. Filter by profile status, segment, language, geography, membership, loyalty tier, wallet, LTV, engagement and churn risk. Support saved views, configurable columns, sorting, pagination, controlled export and auditable bulk actions. Open Customer 360 directly from a result while masking restricted personal or financial data by policy. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-735 |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW`, `LEDGER_POST` (1 configure, 1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/engagement-support/guest-directory-bo-735` |

**What the spec says about it.** **Guest record operations moved here from BO-036 Device Registry on 28 September (audit R254)** — `updateGuestProfile`, `mergeGuestProfiles`, `getGuestLoyalty`, `adjustLoyaltyPoints` and `getConsentHistory`, with their panels and forms. They had been attached to the device registry by module resemblance; managing a guest record is this screen's purpose.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The guest directory: find any guest by name, email, mobile, guest id, external id, ticket, booking, membership or loyalty number, filter the population, and act on one record (amend, adjust points, merge) or open the Customer 360. Personal fields are returned only to staff holding GUEST_VIEW_PII; everyone else sees an opaque reference and behaviour, and the table must render that honestly.

**Known correction pending (do not draw the wrong version)**

- **Two merge operations exist - mergeGuestProfiles (BO-735) and mergeGuests (BO-746, EMP-057).** Why: One decision, two operations; their rules on consent and loyalty may drift. Keep one merge operation. *(source: contracts/satellite/marketing-crm.yaml#mergeGuestProfiles; contracts/satellite/marketing-crm.yaml#mergeGuests; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*
- **adjustLoyaltyPoints requires LEDGER_POST, a finance permission.** Why: A CRM officer granting goodwill points would need ledger posting rights. Confirm the permission (points are a liability, so finance may be intended). *(source: contracts/satellite/marketing-crm.yaml#adjustLoyaltyPoints; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Search | text field | — | Requires `GUEST_VIEW_PII`: matching on personal data discloses it, so a caller without that permission who passes `search` is refused with 403 rather than having the parameter ignored. | `searchGuests` ?search |
| Segment | picker: choose a segment | — | — | `searchGuests` ?segmentId |
| Has consent for | select | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | `searchGuests` ?hasConsentFor |

**Form: Adjust loyalty points** (modal, opened by *Adjust loyalty points*; *Adjust loyalty points* calls `adjustLoyaltyPoints`, *Cancel* sends nothing)

**Collects what `adjustLoyaltyPoints` sends before it is called.** Required: `programmeId`, `points`, `reason`. Optional: `reversedLoyaltyPointsId`, `notes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Programme `programmeId` | picker: choose a programme | required | — | — | shows names, sends the id | — | `adjustLoyaltyPoints` body |
| Points `points` | number field | required | — | — | — | Signed. Negative removes points, and the balance may not go below zero. | `adjustLoyaltyPoints` body |
| Reason `reason` | segmented control | required | — | Goodwill · Correction · Expiry reversal | — | Goodwill, correction or expiry reversal, and nothing else (decided 28 September, audit R149). | `adjustLoyaltyPoints` body |
| Reversed loyalty points `reversedLoyaltyPointsId` | picker: choose a reversed loyalty points | optional | — | — | shows names, sends the id | The entry this reverses, when it is a reversal. Set it and the sign is checked against the original — a reversal that does not cancel what it names is a second grant wearing a … | `adjustLoyaltyPoints` body |
| Notes `notes` | text area | optional | — | max length 1000 | — | — | `adjustLoyaltyPoints` body |

Errors to draw in the form: 409 The entry being reversed is already reversed (`alreadyReversed`), or the balance would go negative (`balanceWouldGoNegative`) (LoyaltyRefusedProblem)

**Form: Save guest profile** (modal, opened by *Save guest profile*; *Save guest profile* calls `updateGuestProfile`, *Cancel* sends nothing)

**Collects what `updateGuestProfile` sends before it is called.** Nothing in the body is required. Optional: `displayName`, `preferredLanguage`, `preferredChannel`, `tags`, `notes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Display name `displayName` | text field | optional | — | max length 200 | — | — | `updateGuestProfile` body |
| Preferred language `preferredLanguage` | language picker | optional | — | — | ISO 639-1 code, shown as the language name | — | `updateGuestProfile` body |
| Preferred channel `preferredChannel` | select | optional | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `updateGuestProfile` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `updateGuestProfile` body |
| Notes `notes` | text area | optional | — | max length 2000 | — | — | `updateGuestProfile` body |

**Sent by *Merge guest profiles*** (`mergeGuestProfiles`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Duplicate subject `duplicateSubjectId` | picker: choose a duplicate subject | required | — | — | shows names, sends the id | — | `mergeGuestProfiles` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `mergeGuestProfiles` body |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Search**: One box for all identifiers; matching on personal data needs GUEST_VIEW_PII, so without it the box accepts only ids and membership or loyalty numbers and says so. *(source: contracts/satellite/marketing-crm.yaml#searchGuests)*
- **Filters**: Status, segment, consent for a purpose (hasConsentFor), language, tier, LTV band, churn risk; saved views; filters always named and clearable. *(source: contracts/satellite/marketing-crm.yaml#searchGuests; screens/P08-venue-back-office.yaml#BO-735)*
- **Adjust points**: Type goodwill, correction or expiry reversal; amount; reason required. It changes the balance only, never tier or lifetime points, and appears in the loyalty ledger report. *(source: contracts/satellite/marketing-crm.yaml#adjustLoyaltyPoints; R149)*
- **Amend profile**: Staff field set (wider than the guest's); at least one of email or mobile remains; the change is audited. *(source: contracts/satellite/marketing-crm.yaml#updateGuestProfile; DI-372)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**The loyalty position** (detail panel, from `getGuestLoyalty`)

| Shows | Format | Notes |
|---|---|---|
| Leaderboard nickname | text | BL-173. The name shown on a leaderboard, chosen by the guest. |
| Points balance | 1,234 | — |
| Lifetime points | 1,234 | — |
| Tier code | text | — |
| Tier name | text | — |
| Points to next tier | 1,234 | — |
| Next expiry points | 1,234 | — |
| Next expiry at | 1 Oct 2026, 14:30 | — |

**The consent** (detail panel, from `getConsentHistory`)

| Shows | Format | Notes |
|---|---|---|
| Purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |
| Decision | chip: Granted, Withdrawn, Not asked | — |
| Channels | list or chips (count when long) | Omit to apply to every channel the purpose covers. |
| Notice version | text | — |
| Source | chip: Guest app, Website, Kiosk, POS, Call centre, Import… | `checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` … |
| Recorded at | 1 Oct 2026, 14:30 | — |
| ID | text | — |
| Subject | the name it points at, never the id | — |
| Recorded by principal | the name it points at, never the id | — |
| Superseded at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Adjust loyalty points (secondary button) | `adjustLoyaltyPoints` POST `/guests/{subjectId}/loyalty/adjust` | AdjustLoyaltyPointsRequest | LoyaltyAdjustmentResult | 409 The entry being reversed is already reversed (`alreadyReversed`), or the balance would go negative (`balanceWouldGoNegative`) (LoyaltyRefusedProblem) | opens modal first |
| Merge guest profiles (destructive button) | `mergeGuestProfiles` POST `/guests/{subjectId}/merge` | inline | MergeResult | 409 Either profile is already merged (`alreadyMerged`), or they are the same profile (`sameProfile`) (MergeRefusedProblem) | — |
| Save guest profile (secondary button) | `updateGuestProfile` PATCH `/guests/{subjectId}` | inline | GuestProfileDetail | — | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Guest row**: Name (or masked reference without PII permission), masked contact, tier, last visit, LTV, flags (VIP, possible duplicate, incomplete). *(source: contracts/satellite/marketing-crm.yaml#searchGuests)*
- **Loyalty panel**: Read with getGuestLoyalty (the staff read of a named guest), per programme. *(source: contracts/satellite/marketing-crm.yaml#getGuestLoyalty)*
- **Consent history**: Every decision oldest first, with purpose, channel, decision, source, notice version and time; read-only evidence. *(source: contracts/satellite/marketing-crm.yaml#getConsentHistory)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Merge into this profile**: Confirmation shows both records with what transfers (orders, cases, loyalty per programme added and higher tier kept, consent taking the more restrictive position) and that the other record is superseded, not deleted. It never runs from a bulk selection. *(source: contracts/satellite/marketing-crm.yaml#mergeGuestProfiles; R149; DI-808)*
- **Export**: Controlled export; needs PII permission and is audited. *(source: screens/P08-venue-back-office.yaml#BO-735)*

**Data it reads**: `searchGuests` (onLoad, The directory)

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

**What opens over it**

- confirmDialog *Merge guest profiles*: **Names what `mergeGuestProfiles` changes and what it leaves alone**, in the consequence rather than the verb. A guest profile this affects should be identified in the dialog, not just counted. **Collects what `mergeGuestProfiles` sends before it is called.** Required: `duplicateSubjectId` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guest are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Either profile is already merged (`alreadyMerged`), or they are the same profile (`sameProfile`) (MergeRefusedProblem); 409 The entry being reversed is already reversed (`alreadyReversed`), or the balance would go negative (`balanceWouldGoNegative`) (LoyaltyRefusedProblem) |

#### Consistency with other screens

- Match `BO-746`: Merging is the same decision as on Duplicate Review and must use the same confirmation and the same operation.
- Match `BO-737`: Opening a row goes to the Customer 360.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- name: Fatima Al Mansoori
  contact: +971 50 *** 4567
  tier: Gold
  lastVisit: 26 Sep 2026
  ltv: AED 4
  860.0: null
  flags:
  - VIP
- name: Priya Nair
  contact: priya.n@ex***.ae
  tier: Bronze
  lastVisit: 2 Jun 2026
  ltv: AED 310.00
  flags:
  - Churn risk
adjustment: Goodwill +500 points - slide closed during visit, case CA-1019
```

#### Permissions

- `searchGuests` → `GUEST_VIEW` (read) · staff
- `getGuestProfile` → `GUEST_VIEW` (read) · staff, guest
- `adjustLoyaltyPoints` → `LEDGER_POST` (operate) · staff
- `getConsentHistory` → `GUEST_VIEW` (read) · staff
- `getGuestLoyalty` → `GUEST_VIEW` (read) · staff, service
- `mergeGuestProfiles` → `GUEST_MANAGE` (configure) · staff
- `updateGuestProfile` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.8 | APIs shall support guest profile creation, updates, segmentation, communication preferences and activity history retrieval. | Developer & API Management | CONTRACTED | `getGuestProfile` |
| 22.2.27 | CRM APIs | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 22.2.28 | CRM Audit Trail | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 1.1.58 | Earned benefit entitlement management | Ticketing Catalogue | CONTRACTED | `adjustLoyaltyPoints` |
| 22.13.5 | Consent Version Management | Marketing & CRM | CONTRACTED | `getConsentHistory` |
| 22.13.6 | Consent Audit Trail | Marketing & CRM | CONTRACTED | `getConsentHistory` |
| 5.3.4 | The system should allow specification of a field (e.g. email) or a combination of fields (e.g. name + date of birth) to serve as the unique identifier for each guest. The system should restrict … | F&B & Guest Management | CONTRACTED | `mergeGuestProfiles` |
| 5.3.22 | Identify duplicate guest profiles and allow administrative merge while preserving purchases, memberships, wallets, loyalty balances, reservations, and history. | F&B & Guest Management | CONTRACTED | `mergeGuestProfiles` |
| 7.3.7 | Identify duplicate customer profiles using email, mobile, passport, national ID or configurable matching rules. Allow authorized users to merge profiles into a master record while preserving purchase … | F&B POS | CONTRACTED | `mergeGuestProfiles` |
| 22.2.8 | Guest Identity Resolution | Marketing & CRM | CONTRACTED | `mergeGuestProfiles` |
| 22.2.9 | Guest Profile Merge | Marketing & CRM | CONTRACTED | `mergeGuestProfiles` |
| 2.8.4 | The system should allow call center agents to add and modify guest profile data | Ticketing Sales | CONTRACTED | `updateGuestProfile` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- CRM guest dashboard shows active/inactive/duplicate profile counts and lifetime value, plus guest directory/search and segmentation by source (individual, corporate, group, travel agent, OTA). *(client request · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-370)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-735` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-735`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 2: Works in Guest Directory → Provide a permission-controlled directory for locating and managing every guest record. Search by name, email, mobile, guest ID, external ID, ticket, booking, membership or loyalty identifier. Filter …

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-735?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Adjust loyalty points, Merge guest profiles, Save guest profile.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`, `LEDGER_POST`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-736` Guest Master Configuration

**Configure the shared guest data model without software changes. Configuration Scope of Work / Version 1.0 6 Maintain standard and custom attributes, field groups, labels, data types, defaults, required flags and validation rules. Define primary and external identifiers, source-system priority, survivorship rules and profile- completeness scoring. Configure field visibility and editability by role, tenant, brand, venue, region and jurisdiction. Version and audit schema changes and expose approved attributes consistently through UI, API and events. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-736 |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW`, `MARKETING_MANAGE` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/guest-master-configuration-bo-736` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Configure the guest data model without development: standard and custom attributes, field groups, types, defaults, required and unique flags, either/or rules, identifiers, survivorship and completeness scoring, and visibility by role. Every change is a version, because a field whose meaning changed in March makes every earlier value ambiguous.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Required rules**: Per field required, optional or either/or. Email and mobile are an either/or pair by default and cannot both be made optional. *(source: DI-372; DI-371)*
- **Custom field**: Label in English and Arabic, type, options, unique flag; nationality and country of residence are separate fields. *(source: DI-371; contracts/satellite/marketing-crm.yaml#setGuestExtraFields)*
- **Remove an option**: Options are set as a whole list; removing one still held by guests shows how many hold it before saving. *(source: contracts/satellite/marketing-crm.yaml#setGuestExtraFields)*
- **Group profile fields**: Group profiles (group name, description, contact person) are configured separately from individuals. *(source: DI-371)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save guest attribute model (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Version history**: Each saved model version with author, date and changed fields. *(source: contracts/satellite/marketing-crm.yaml#setGuestAttributeModel)*

**Data it reads**: `getGuestAttributeModel` (onLoad, The shared data model)

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest master list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest master untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest master yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guest master are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
fields:
- First name (required)
- Last name (required)
- Email or Mobile (either/or)
- Nationality (optional, list)
- Country of residence (optional)
- Emirates ID (unique, optional)
version: Model v6 - 30 Sep 2026 - added "Preferred park area"
```

#### Permissions

- `getGuestAttributeModel` → `GUEST_VIEW` (read) · staff
- `setGuestAttributeModel` → `GUEST_MANAGE` (configure) · staff
- `setGuestExtraFields` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: at least one of e-mail or mobile number is mandatory at profile creation (not both — some customers decline e-mail); the system supports conditional "either/or" mandatory-field rules. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 5. Key Decisions · DI-372)*
- Profile fields must be fully configurable/user-defined (e.g. nationality vs. country of residence), with per-field unique and required flags; group profiles (group name, description, contact person) are configured independently. *(client request · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-371)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-736` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-736`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 4: Works in Guest Master Configuration → Configure the shared guest data model without software changes. Configuration Scope of Work / Version 1.0 6 Maintain standard and custom attributes, field groups, labels, data types, defaults …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-736?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save guest attribute model, Cancel.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`, `MARKETING_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-737` Customer 360 Profile

**Present a consolidated, actionable view of one guest. Display identity, contacts, preferences, household, organization, membership, loyalty, wallet, tickets, bookings and visits. Show LTV, engagement, churn risk, communication eligibility, open cases, pending waivers and recent activity. Provide permission-controlled quick actions for communication, booking, case creation, campaign enrollment and profile maintenance. Allow role-based widget configuration while keeping the Customer Master Service as the system of record. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-737 |
| Who uses it | venue staff holding `CASE_VIEW`, `GUEST_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation), `guestId` (navigation) |
| Route | `/engagement-support/customer-360-profile-bo-737` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): listCustomerSegmentProfile is catalogue segment pricing rules, not a guest view; the CRM 360 is getGuestProfile, getGuestLoyalty, getGuestTimeline …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** One guest on one page: identity, contacts, preferences, household, organisation, memberships, loyalty, wallet, tickets, bookings, visits, LTV, churn risk, whether they can be contacted (per channel and purpose), open cases, pending waivers and recent activity, with quick actions. Communication eligibility is shown before any "send" action is offered.

**Fixed on main** (the package already carries these; draw what it says): The 360 is wired to listCustomerServiceProfile (the support service view) and listCustomerSegmentProfile (catalogue pricing eligibility … (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Subject | picker: choose a subject | — | — | `listCustomerServiceProfile` ?subjectId |
| Programme | picker: choose a programme | — | — | `getGuestLoyalty` ?programmeId |
| From | date and time picker | — | — | `getGuestTimeline` ?from |
| Kinds | text field | — | — | `getGuestTimeline` ?kinds |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Profile** (detail panel, from `getGuestProfile`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Subject | the name it points at, never the id | Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger. |
| Display name | text | — |
| Email | text | — |
| Phone | +971 50 123 4567 | — |
| Preferred language | text | — |
| Preferred channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Guest link | text | Present where the guest is linked across cells. Marketing acts locally. |
| Tags | list or chips (count when long) | — |
| Engagement score | 1,234 | 22.2.20 and 22.2.21. `lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not. |
| Engagement tier | chip: New, Active, Occasional, Lapsing, Lapsed, Dormant | 5.3.19. Automatic classification, computed rather than assigned. |
| Lifetime value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Visit count | 1,234 | — |
| Last visit at | 1 Oct 2026, 14:30 | — |
| Is active | yes / no (icon or chip) | — |
| Merged into subject | the name it points at, never the id | Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`, which retain it as a redirect rather than deleting it. |
| Merged at | 1 Oct 2026, 14:30 | — |
| Consents | grouped details | — |
| Subject | the name it points at, never the id | — |
| Purposes | list or chips (count when long) | — |

**Loyalty** (detail panel, from `getGuestLoyalty`)

| Shows | Format | Notes |
|---|---|---|
| Leaderboard nickname | text | BL-173. The name shown on a leaderboard, chosen by the guest. |
| Subject | the name it points at, never the id | — |
| Programme | the name it points at, never the id | — |
| Points balance | 1,234 | — |
| Lifetime points | 1,234 | — |
| Tier | the name it points at, never the id | The tier this row's `tierCode` and `tierName` are a copy of. Added 20 September with `marketing.programme_tier`: the two strings were a … |
| Tier code | text | — |
| Tier name | text | — |
| Points to next tier | 1,234 | — |
| Next expiry points | 1,234 | — |
| Next expiry at | 1 Oct 2026, 14:30 | — |

**Timeline** (data table, from `getGuestTimeline`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| At | 1 Oct 2026, 14:30 | — |
| Kind | chip: Purchase, Ticket used, Reservation, Visit, Membership change, Loyalty… | — |
| Nature | chip: Operational fact, User note, AI derived | A prediction and a gate scan are both useful and only one happened. |
| Summary | text | — |
| Channel | text | — |
| Venue | the name it points at, never the id | — |
| Source contract | text | — |
| Source reference | the name it points at, never the id | — |
| Value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Outcome | text | — |

**Consents** (detail panel, from `getGuestConsents`)

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Purposes | list or chips (count when long) | — |
| Purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |
| Decision | chip: Granted, Withdrawn, Not asked | — |
| Channels | list or chips (count when long) | — |
| Notice version | text | — |
| Requires renewal | yes / no (icon or chip) | True where the notice has been superseded since consent was given. |
| Decided at | 1 Oct 2026, 14:30 | — |

**Intelligence** (detail panel, from `getGuestIntelligence`)

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Scores | list or chips (count when long) | — |
| Kind | chip: Historical ltv, Predicted ltv, Engagement, Churn risk, Inactivity risk … | — |
| Value | 1,234.5 | — |
| Band | text | — |
| Confidence | 1,234.5 | — |
| Model | text | — |
| Model version | text | — |
| Computed at | 1 Oct 2026, 14:30 | — |
| Factors | list or chips (count when long) | — |
| Factor | text | — |
| Contribution | 1,234.5 | — |
| Limitations | list or chips (count when long) | Policy and data limitations travel with the score, so the rule that prediction never overrides consent cannot be forgotten downstream. |
| Affinities | list or chips (count when long) | — |
| Product category | the name it points at, never the id | — |
| Label | text | — |
| Strength | 1,234.5 | — |
| Next best actions | list or chips (count when long) | — |
| Action | text | — |
| Expected impact | text | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Header**: Name, tier badge, flags (VIP, minor, possible duplicate), preferred language and channel, and a contactability strip (Email Given, WhatsApp Not asked, SMS Withdrawn). *(source: contracts/satellite/marketing-crm.yaml#getGuestConsents; screens/P08-venue-back-office.yaml#BO-737)*
- **Value and risk**: LTV, engagement tier (new, active, occasional, lapsing, lapsed, dormant) and churn risk, each with its reasons; AI-derived values labelled as such. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/GuestProfile; contracts/satellite/marketing-crm.yaml#getGuestIntelligence)*
- **Portfolio**: Entitlements, wallet balance and restrictions in one list, the same view the guest app shows. *(source: DI-667)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Send a message**: Offered only on channels where the purpose is permitted; transactional resends are always allowed. *(source: DI-378)*
- **Create case**: Opens case creation with the guest attached. *(source: contracts/satellite/marketing-crm.yaml#createCase)*

**Data it reads**: `listCustomerServiceProfile` (onLoad, Customer 360° Service Profile); `getGuestProfile` (onLoad, The consolidated profile); `getGuestLoyalty` (onLoad, Points and tier); `getGuestTimeline` (onLoad, Commercial and document history); `getGuestConsents` (onLoad, Consents in force); `getGuestIntelligence` (onLoad, Value, engagement and risk)

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer 360 profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer 360 profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer 360 profile yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer 360 profile are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SUP-010`: The service 360 in the Support Console is the same guest view; same header and contactability strip.
- Match `POS-027`: Same tier badge and wallet split.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
guest:
  name: Omar Haddad
  tier: Silver
  language: Arabic
  channel: WhatsApp
  ltv: AED 2
  145.0: null
  engagement: lapsing
  churnRisk: High - no visit in 140 days
  last visit spend down 40%: null
openCases:
- CA-0998 Complaint - escalated
waivers:
- Deep Dive waiver v3 - not signed
```

#### Permissions

- `listCustomerServiceProfile` → `CASE_VIEW` (read) · staff
- `getGuestProfile` → `GUEST_VIEW` (read) · staff, guest
- `getGuestLoyalty` → `GUEST_VIEW` (read) · staff, service
- `getGuestTimeline` → `GUEST_VIEW` (read) · staff
- `getGuestConsents` → `GUEST_VIEW` (read) · staff, guest
- `getGuestIntelligence` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.8 | APIs shall support guest profile creation, updates, segmentation, communication preferences and activity history retrieval. | Developer & API Management | CONTRACTED | `getGuestProfile` |
| 22.2.27 | CRM APIs | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 22.2.28 | CRM Audit Trail | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 5.3.25 | Generate AI insights such as predicted next visit, churn risk, preferred products, preferred attractions, lifetime value, and upsell recommendations. | F&B & Guest Management | CONTRACTED_PARTIAL | `getGuestIntelligence` |
| 5.4.22 | Identify customers at risk of disengagement. | F&B & Guest Management | CONTRACTED | `getGuestIntelligence` |
| 5.4.33 | AI provides personalized engagement and retention recommendations. | F&B & Guest Management | CONTRACTED | `getGuestIntelligence` |
| 22.2.22 | AI Guest Insights | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.2.23 | AI Churn Prediction | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.2.24 | AI Next Best Action | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.6.19 | AI Engagement Optimization | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.14.13 | AI Churn Prediction Segments | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.14.14 | AI Upgrade Opportunities | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Repeat guest checkouts with the same email (or phone) consolidate into one profile automatically; a manual merge-customer-profile function remains for edge cases (e.g. slightly different name spelling under the same email). Allam cited a system where 10 transactions created 10 profiles. *(agreed · MoM 18 Sep 2026, 4.8 Guest Checkout & Profile Deduplication — Extended Discussion · DI-941)*
- Entitlements portfolio is used both by the guest (mobile app) and by customer service: one view of restrictions, wallet balance and all entitlements; a unified list across a visit (e.g. four admissions, two fast passes, a meal package, a parking entitlement). *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-667)*
- Decision: one unified customer profile across ticketing, F&B and retail gives a 360° view of guest activity and avoids duplicates; e.g. a guest who buys tickets online and later dines is matched by name/mobile to the same profile. *(agreed · MoM 18 Aug 2026, 4.9 Unified Customer Profile · DI-339)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-737` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-737`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 6: Works in Customer 360 Profile → Present a consolidated, actionable view of one guest. Display identity, contacts, preferences, household, organization, membership, loyalty, wallet, tickets, bookings and visits. Show LTV …
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (70 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-737?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `CASE_VIEW`, `GUEST_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-738` Activity Timeline

**Provide a chronological record of guest activity across the connected platform. Ingest purchases, ticket usage, reservations, visits, membership changes, loyalty, wallet, campaigns, messages, cases, surveys and waivers. Filter by date, channel, venue, event type, source system and outcome and open the related source transaction. Distinguish operational facts from user notes and AI-derived events and preserve event timestamps and source identifiers. Support reliable ordering, pagination and audit evidence without allowing historical events to be silently altered. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-738 |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `guestId` (navigation), `subjectId` (navigation) |
| Route | `/engagement-support/activity-timeline-bo-738` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): The timeline screen declared getGuestIntelligence (scores) and not getGuestTimeline, while BO-743 AI Guest Intelligence declared the reverse; the two reads were …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Everything one guest did, in order, across the platform: purchases, scans, reservations, visits, membership changes, loyalty, wallet, campaigns, messages, cases, surveys and waivers. Operational facts, staff notes and AI-derived events are visibly different kinds of entry.

**Fixed on main** (the package already carries these; draw what it says): The timeline screen declares getGuestIntelligence (scores) and not getGuestTimeline, while BO-743 AI Guest Intelligence declares … (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getGuestTimeline` ?from |
| Kinds | text field | — | — | `getGuestTimeline` ?kinds |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Filters**: Date range, channel, venue, event type, source system, outcome. *(source: screens/P08-venue-back-office.yaml#BO-738)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Activity timeline** (data table, from `getGuestTimeline`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| At | 1 Oct 2026, 14:30 | — |
| Kind | chip: Purchase, Ticket used, Reservation, Visit, Membership change, Loyalty… | — |
| Nature | chip: Operational fact, User note, AI derived | A prediction and a gate scan are both useful and only one happened. |
| Summary | text | — |
| Channel | text | — |
| Venue | the name it points at, never the id | — |
| Source contract | text | — |
| Source reference | the name it points at, never the id | — |
| Value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Outcome | text | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Timeline entry**: Time (venue time zone), icon by kind, one-line description, source and a link to the source record; AI-derived entries carry an "AI" tag and model version; notes show their author. *(source: contracts/satellite/marketing-crm.yaml#getGuestTimeline; screens/P08-venue-back-office.yaml#BO-738)*

**Data it reads**: `getGuestTimeline` (onLoad, Commercial and document history)

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The activity timeline list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the activity timeline untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No activity timeline yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the activity timeline are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entries:
- 26 Sep 2026 15:02 - Scan - Coastal Aqua main gate - admitted
- 26 Sep 2026 13:40 - Purchase - Beach Grill - AED 86.00 - 86 points
- 20 Sep 2026 09:00 - Message - Autumn comeback (WhatsApp) - read
- 21 Sep 2026 - AI - Churn risk raised to High (model churn-v2)
```

#### Permissions

- `getGuestProfile` → `GUEST_VIEW` (read) · staff, guest
- `getGuestRelationships` → `GUEST_VIEW` (read) · staff
- `getGuestTimeline` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.8 | APIs shall support guest profile creation, updates, segmentation, communication preferences and activity history retrieval. | Developer & API Management | CONTRACTED | `getGuestProfile` |
| 22.2.27 | CRM APIs | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 22.2.28 | CRM Audit Trail | Marketing & CRM | CONTRACTED | `getGuestProfile` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-738` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-738`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 8: Works in Activity Timeline → Provide a chronological record of guest activity across the connected platform. Ingest purchases, ticket usage, reservations, visits, membership changes, loyalty, wallet, campaigns, messages, cases …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-738?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-739` Contact & Preferences

**Maintain verified contact information and service preferences for each guest. Manage multiple email addresses, phone numbers, physical addresses, emergency contacts and social identifiers. Record preferred language, channel, contact time, frequency, interests, favorite attractions and visit preferences. Store accessibility and dietary requirements with suitable sensitivity and role restrictions. Configuration Scope of Work / Version 1.0 7 Show verification, suppression and consent status while delegating legal enforcement to the shared Consent Service. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block B · task VM-BO-739 |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW`, `GUEST_VIEW_PII` (1 configure, 1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `guestId` (navigation), `verificationId` (navigation) |
| Route | `/engagement-support/contact-preferences-bo-739` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A guest's contact details and preferences as staff see them, with identity verifications to decide. Personal data is shown only with the PII permission.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Pending · Verified · Rejected · Resubmission requested | `listGuestIdentityVerifications` ?status |
| Subject | picker: choose a subject | — | — | `listGuestIdentityVerifications` ?subjectId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listGuestIdentityVerifications` (onLoad, Guest ID documents awaiting review)

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The contact preferences list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the contact preferences untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No contact preferences yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the contact preferences are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already decided; 422 A rejection or resubmission request without a reason |

#### Edge cases to draw

- **Viewer without GUEST_VIEW_PII**: Contact values masked (f•••@gmail.com); verification decisions not offered. *(source: contracts/spine/identity.yaml#listGuestIdentityVerifications; ADR-0023)*
- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds GUEST_VIEW, GUEST_VIEW_PII only)**: Everything reads; the actions needing another permission are not offered as live buttons: GUEST_MANAGE for decideGuestIdentityVerification. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/identity.yaml#decideGuestIdentityVerification)*
- **decideGuestIdentityVerification answers 422**: Show it as something the person can act on, not a failure: A rejection or resubmission request without a reason *(source: contracts/spine/identity.yaml#decideGuestIdentityVerification)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
guest:
  name: Aisha Al Nuaimi
  email: a•••@outlook.com
  mobile: +971 50 ••• 4412
  language: Arabic
  channel: WhatsApp
```

#### Permissions

- `getGuestTimeline` → `GUEST_VIEW` (read) · staff
- `listGuestIdentityVerifications` → `GUEST_VIEW_PII` (operate) · staff
- `decideGuestIdentityVerification` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-739` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-739`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 10: Works in Contact & Preferences → Maintain verified contact information and service preferences for each guest. Manage multiple email addresses, phone numbers, physical addresses, emergency contacts and social identifiers. Record …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-739?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`, `GUEST_VIEW_PII`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-740` Family & Guardians

**Model households, dependants and guardians while preserving each person's individual identity. Create family groups and link parent, guardian, spouse and dependant relationships with effective dates. Configure purchasing, booking, profile-management and waiver-signing authority for minors and dependants. Support shared or separate benefits, memberships, bookings and communications without merging individual profiles. Record additions, removals, authority changes and exceptions in a complete relationship audit trail. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-740 |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation), `guestId` (navigation) |
| Route | `/engagement-support/family-guardians-bo-740` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Households, dependants and guardians, linked without merging anyone. Each person keeps their own profile; the link carries authority (who may buy, book, manage the profile or sign waivers for a minor), effective dates, and whether benefits and communications are shared. Wallet balances can be shared across a linked family, so a parent's top-up is spent from a child's wristband.

**Fixed on main** (the package already carries these; draw what it says): The screen's only write is updateGuestPreferences ("Save guest preferences"). (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Form: Save links** (modal, opened by *Save links*; *Save links* calls `setGuestRelationships`, *Cancel* sends nothing)

**Collects what `setGuestRelationships` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Relationships `relationships` | repeatable rows | required | — | — | — | — | `setGuestRelationships` body |
| ID `relationships[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `setGuestRelationships` body |
| Related subject `relationships[].relatedSubjectId` | picker: choose a related subject | required | — | — | shows names, sends the id | — | `setGuestRelationships` body |
| Organisation `relationships[].organisationId` | picker: choose an organisation | optional | — | — | shows names, sends the id | — | `setGuestRelationships` body |
| Kind `relationships[].kind` | select | required | — | Parent · Guardian · Spouse · Dependant · Household member · Employee · Student · Group leader · Travel agent · Reseller | — | — | `setGuestRelationships` body |
| Authorities `relationships[].authorities` | multi-select chips | optional | — | Purchase for · Book for · Manage profile · Sign waiver · View history · Receive communications | — | Four different permissions, not one relationship. A guardianship granting all of them forever survives the child becoming an adult. | `setGuestRelationships` body |
| Effective from `relationships[].effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setGuestRelationships` body |
| Effective to `relationships[].effectiveTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setGuestRelationships` body |
| Shared benefits `relationships[].sharedBenefits` | toggle | optional | off | — | — | — | `setGuestRelationships` body |
| Verified at `relationships[].verifiedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setGuestRelationships` body |
| Scope path `relationships[].scopePath` | text field | optional | — | — | — | — | `setGuestRelationships` body |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Relationship**: Parent, guardian, spouse, dependant, with effective from and to dates. *(source: contracts/satellite/marketing-crm.yaml#setGuestRelationships; DI-373)*
- **Authority for a minor**: Purchasing, booking, profile management, waiver signing, each a separate permission; a guest with no date of birth counts as a minor. *(source: screens/P08-venue-back-office.yaml#BO-740; R205)*
- **Shared wallet and spending limit**: Whether the family shares the wallet, and a daily limit per dependant (guests can also set this themselves). *(source: MoM 2026-08-20 4.1; DI-530)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Family and guardians** (data table, from `getGuestRelationships`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Related subject | the name it points at, never the id | — |
| Organisation | the name it points at, never the id | — |
| Kind | chip: Parent, Guardian, Spouse, Dependant, Household member, Employee… | — |
| Authorities | list or chips (count when long) | Four different permissions, not one relationship. A guardianship granting all of them forever survives the child becoming an adult. |
| Effective from | 1 Oct 2026 | — |
| Effective to | 1 Oct 2026 | — |
| Shared benefits | yes / no (icon or chip) | — |
| Verified at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save guest preferences (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Save links (secondary button) | `setGuestRelationships` PUT `/guests/{guestId}/relationships` | inline | GuestRelationship[] | — | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Household card**: Each member as their own profile chip, with relationship, authority icons, and "shared wallet" when on. Messages to one member are never addressed to the household. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/SegmentCriterion)*

**Data it reads**: `getGuestRelationships` (onLoad, Household, guardians and dependants)

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The family guardians list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the family guardians untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No family guardians yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the family guardians are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
household: Al Suwaidi family
members:
- Khalid (guardian - booking, waiver signing)
- Mariam (daughter, 9 - AED 100 a day)
- Saeed (son, 6 - AED 50 a day)
```

#### Permissions

- `updateGuestPreferences` → `GUEST_MANAGE` (configure) · staff, guest
- `getGuestProfile` → `GUEST_VIEW` (read) · staff, guest
- `getGuestRelationships` → `GUEST_VIEW` (read) · staff
- `setGuestRelationships` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.8 | APIs shall support guest profile creation, updates, segmentation, communication preferences and activity history retrieval. | Developer & API Management | CONTRACTED | `getGuestProfile` |
| 22.2.27 | CRM APIs | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 22.2.28 | CRM Audit Trail | Marketing & CRM | CONTRACTED | `getGuestProfile` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Family/guardian linking is core (e.g. father, spouse, daughter as one family unit), consistent with family tickets/memberships; the same linking model extends to operations-team entitlement relationships. *(agreed · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-373)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-740` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-740`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 12: Works in Family & Guardians → Model households, dependants and guardians while preserving each person's individual identity. Create family groups and link parent, guardian, spouse and dependant relationships with effective dates. …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-740?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save guest preferences, Cancel, Save links.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-741` Corporate & Groups

**Link guests to corporate, school, travel and group structures. Support corporate accounts, schools, tour operators, travel agencies, resellers, clubs, teams and event groups. Define contacts, participant roles, billing relationships, booking authority and relationship validity periods. Display associated bookings, memberships, agreements and activity while respecting organizational access boundaries. Expose relationships to B2B, reservations, cases and reporting through secured services and APIs. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-741 |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `guestId` (navigation) |
| Route | `/engagement-support/corporate-groups-bo-741` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Link guests to organisations: corporate accounts, schools, tour operators, travel agencies, resellers, clubs, teams, event groups. Each link has a role, billing relationship, booking authority and validity period. Linking never merges people.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Organisation link**: Organisation, participant role (contact, booker, member, teacher), billing relationship, booking authority, valid from and to. *(source: contracts/satellite/marketing-crm.yaml#setGuestRelationships)*
- **Corporate onboarding status**: Company profile (name, address, trade licence, VAT certificate), then admin approval or rejection, then rates and credentials. *(source: DI-375)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save guest relationships (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Organisation view**: Members, their bookings and memberships, agreements; respecting the organisation's access boundary. *(source: screens/P08-venue-back-office.yaml#BO-741)*

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The corporate groups list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the corporate groups untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No corporate groups yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the corporate groups are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-740`: Same relationship component, different kinds.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
organisation: Al Noor International School (school)
links:
- Ms Hana Yousef - teacher
- booking authority
- Ahmed Saleh - finance contact
- invoice
```

#### Permissions

- `getGuestRelationships` → `GUEST_VIEW` (read) · staff
- `setGuestRelationships` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- One unified flow for groups, schools and corporates: inquiry > package builder > quotation > approval > confirmed booking. *(agreed · MoM 31 Aug 2026, 4.7 Group Sales / 5. Key Decisions · DI-565)*
- Corporate/B2B profiles have a self-service onboarding flow: company profile (name, address, trade licence, VAT certificate) → admin approval/rejection → rate/product setup → credential issuance. *(client request · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-375)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-741` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-741`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 14: Works in Corporate & Groups → Link guests to corporate, school, travel and group structures. Support corporate accounts, schools, tour operators, travel agencies, resellers, clubs, teams and event groups. Define contacts …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-741?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save guest relationships, Cancel.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-742` Commerce & Documents

**Consolidate the guest's commercial, service and document history. Provide tabs for tickets, reservations, memberships, loyalty, wallet, refunds, exchanges, transfers, upgrades and attendance. Display communications, cases, survey responses, ratings, reviews, waivers, identification documents and signed agreements. Link every item to its source transaction and show status, value, channel, venue, timestamps and authorized actions. Apply RBAC/PBAC, masking, retention, download and audit policies to financial, identity and legal records. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 8**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-742 |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `guestId` (navigation) |
| Route | `/engagement-support/commerce-documents-bo-742` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): A history screen needs reads; its only operation was setGuestRelationships, and relationship editing belongs on BO-740 and BO-741 (design-notes correction …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The guest's commercial, service and document history in tabs: tickets, reservations, memberships, loyalty, wallet, refunds, exchanges, transfers, upgrades, attendance, communications, cases, surveys, reviews, waivers, ID documents and signed agreements. Each row links to its source with status, value, channel and time.

**Fixed on main** (the package already carries these; draw what it says): The screen's only operation is setGuestRelationships ("Save guest relationships"). (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getGuestTimeline` ?from |
| Kinds | text field | — | — | `getGuestTimeline` ?kinds |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Commerce and documents** (data table, from `getGuestTimeline`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| At | 1 Oct 2026, 14:30 | — |
| Kind | chip: Purchase, Ticket used, Reservation, Visit, Membership change, Loyalty… | — |
| Nature | chip: Operational fact, User note, AI derived | A prediction and a gate scan are both useful and only one happened. |
| Summary | text | — |
| Channel | text | — |
| Venue | the name it points at, never the id | — |
| Source contract | text | — |
| Source reference | the name it points at, never the id | — |
| Value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Outcome | text | — |

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Documents tab**: Kind, uploaded by, date, retain-until date (always present), and access is PII-permissioned; signed waivers open at the exact version signed. *(source: contracts/satellite/marketing-crm.yaml#uploadGuestDocument; contracts/satellite/marketing-crm.yaml#createForm)*

**Data it reads**: `getGuestTimeline` (onLoad, Commercial and document history)

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commerce documents list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commerce documents untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commerce documents yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commerce documents are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tickets:
- Coastal Aqua Day Pass x3 - 26 Sep 2026 - used
documents:
- Emirates ID - retain until 31 Dec 2027
- Deep Dive waiver v3 - signed 26 Sep 2026
```

#### Permissions

- `getGuestTimeline` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-742` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-742`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 16: Works in Commerce & Documents → Consolidate the guest's commercial, service and document history. Provide tabs for tickets, reservations, memberships, loyalty, wallet, refunds, exchanges, transfers, upgrades and attendance. Display …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-742?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-743` AI Guest Intelligence

**Turn the unified record into explainable customer insight and recommended actions. Calculate historical and predicted LTV, engagement, churn, inactivity, cancellation, affinity and upgrade propensity. Classify audiences and recommend the next campaign, offer, product, membership, reward, channel and next best action. Display contributing factors, confidence, model/version, expected impact and policy or data limitations. Require consent and eligibility checks, support accept/reject/feedback actions and audit all human and AI decisions. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 9 Board 2 - Identity Resolution, Consent & Data Privacy Figure 2. High-definition configuration board with all 10 screens. Configuration Scope of Work / Version 1.0 10**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-743 |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `guestId` (navigation) |
| Route | `/engagement-support/ai-guest-intelligence-bo-743` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): The reads were swapped with BO-738, and uploading documents has nothing to do with AI insight (design-notes corrections customer-marketing BO-738, BO-743).

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Explainable insight for one guest and for audiences: historical and predicted LTV, engagement, churn, cancellation, affinity, upgrade propensity, and the recommended next action. Every score shows its contributing factors, confidence, model and version, and the recommendation respects consent and eligibility before it is offered.

**Fixed on main** (the package already carries these; draw what it says): Declares getGuestTimeline and uploadGuestDocument but not getGuestIntelligence. (CHG-WIR-005).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Guest intelligence** (detail panel, from `getGuestIntelligence`)

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Scores | list or chips (count when long) | — |
| Kind | chip: Historical ltv, Predicted ltv, Engagement, Churn risk, Inactivity risk … | — |
| Value | 1,234.5 | — |
| Band | text | — |
| Confidence | 1,234.5 | — |
| Model | text | — |
| Model version | text | — |
| Computed at | 1 Oct 2026, 14:30 | — |
| Factors | list or chips (count when long) | — |
| Factor | text | — |
| Contribution | 1,234.5 | — |
| Limitations | list or chips (count when long) | Policy and data limitations travel with the score, so the rule that prediction never overrides consent cannot be forgotten downstream. |
| Affinities | list or chips (count when long) | — |
| Product category | the name it points at, never the id | — |
| Label | text | — |
| Strength | 1,234.5 | — |
| Next best actions | list or chips (count when long) | — |
| Action | text | — |
| Expected impact | text | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Score card**: Score, band, top contributing factors in plain words, confidence, model name and version, last computed. *(source: contracts/satellite/marketing-crm.yaml#getGuestIntelligence)*
- **Next best action**: A proposal with expected impact and why; actions a human accepts. A recommendation on a channel without consent is not shown. *(source: screens/P08-venue-back-office.yaml#BO-743; DI-378)*

**Data it reads**: `getGuestIntelligence` (onLoad, Value, engagement and risk)

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest intelligence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest intelligence yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guest intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
guest: Omar Haddad
churn:
  score: 0.78
  band: High
  factors:
  - No visit in 140 days
  - Annual pass expires 30 Nov 2026
  - Complaint unresolved
  model: churn-v2
nextAction: Offer pass renewal with 10% member discount on WhatsApp (consent given)
```

#### Permissions

- `getGuestIntelligence` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.3.25 | Generate AI insights such as predicted next visit, churn risk, preferred products, preferred attractions, lifetime value, and upsell recommendations. | F&B & Guest Management | CONTRACTED_PARTIAL | `getGuestIntelligence` |
| 5.4.22 | Identify customers at risk of disengagement. | F&B & Guest Management | CONTRACTED | `getGuestIntelligence` |
| 5.4.33 | AI provides personalized engagement and retention recommendations. | F&B & Guest Management | CONTRACTED | `getGuestIntelligence` |
| 22.2.22 | AI Guest Insights | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.2.23 | AI Churn Prediction | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.2.24 | AI Next Best Action | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.6.19 | AI Engagement Optimization | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.14.13 | AI Churn Prediction Segments | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.14.14 | AI Upgrade Opportunities | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-743` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-743`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 18: Works in AI Guest Intelligence → Turn the unified record into explainable customer insight and recommended actions. Calculate historical and predicted LTV, engagement, churn, inactivity, cancellation, affinity and upgrade …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-743?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
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

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"adjustLoyaltyPoints": {"method":"POST","path":"/guests/{subjectId}/loyalty/adjust","contract":"marketing-crm","summary":"Manually adjust points","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AdjustLoyaltyPointsRequest","responds":"LoyaltyAdjustmentResult"},
"decideGuestIdentityVerification": {"method":"POST","path":"/guest-identity-verifications/{verificationId}/decision","contract":"identity","summary":"Verify or refuse a guest's identity document","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"IdentityGuestVerification"},
"getConsentHistory": {"method":"GET","path":"/guests/{subjectId}/consents/history","contract":"marketing-crm","summary":"Full consent history","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getGuestAttributeModel": {"method":"GET","path":"/guest-attribute-model","contract":"marketing-crm","summary":"The shared guest data model","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"GuestAttributeModel"},
"getGuestConsents": {"method":"GET","path":"/guests/{subjectId}/consents","contract":"marketing-crm","summary":"Read a guest's consent state","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ConsentState"},
"getGuestIntelligence": {"method":"GET","path":"/guests/{guestId}/intelligence","contract":"marketing-crm","summary":"Value, engagement, churn and propensity, with their reasons","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestIntelligence"},
"getGuestLoyalty": {"method":"GET","path":"/guests/{subjectId}/loyalty","contract":"marketing-crm","summary":"A guest's loyalty position","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":true}],"requestBody":null,"responds":"LoyaltyPosition"},
"getGuestProfile": {"method":"GET","path":"/guests/{subjectId}","contract":"marketing-crm","summary":"Read a guest profile","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestProfileDetail"},
"getGuestRelationships": {"method":"GET","path":"/guests/{guestId}/relationships","contract":"marketing-crm","summary":"Household, guardians, corporate and group links","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestRelationship"},
"getGuestTimeline": {"method":"GET","path":"/guests/{guestId}/timeline","contract":"marketing-crm","summary":"Everything this guest did, in order, across the platform","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"kinds","in":"query","required":null},{"name":"venueId","in":"query","required":null}],"requestBody":null,"responds":"GuestTimelineEvent"},
"listCustomerServiceProfile": {"method":"GET","path":"/customer-service-profile","contract":"marketing-crm","summary":"Customer 360° Service Profile","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"subjectId","in":"query","required":true}],"requestBody":null,"responds":"Customer360ServiceProfileView"},
"listGuestIdentityVerifications": {"method":"GET","path":"/guest-identity-verifications","contract":"identity","summary":"Guest identity verifications, the review queue first","permission":"GUEST_VIEW_PII","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSegments": {"method":"GET","path":"/segments","contract":"marketing-crm","summary":"List segments","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"mergeGuestProfiles": {"method":"POST","path":"/guests/{subjectId}/merge","contract":"marketing-crm","summary":"Merge a duplicate profile into this one","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MergeResult"},
"searchGuests": {"method":"GET","path":"/guests","contract":"marketing-crm","summary":"Search guest profiles","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"search","in":"query","required":null},{"name":"segmentId","in":"query","required":null},{"name":"hasConsentFor","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setGuestAttributeModel": {"method":"PUT","path":"/guest-attribute-model","contract":"marketing-crm","summary":"Change the model, as a version","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestAttributeModel","responds":"GuestAttributeModel"},
"setGuestExtraFields": {"method":"PUT","path":"/guest-extra-fields","contract":"marketing-crm","summary":"Define the extra guest fields","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestExtraFieldDefinition","responds":"GuestExtraFieldDefinition"},
"setGuestRelationships": {"method":"PUT","path":"/guests/{guestId}/relationships","contract":"marketing-crm","summary":"Link people without merging them","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestRelationship"},
"updateGuestPreferences": {"method":"PUT","path":"/guests/{subjectId}/preferences","contract":"marketing-crm","summary":"The things a regular should not have to say twice","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"lastWriterWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestPreferences","responds":"GuestPreferences"},
"updateGuestProfile": {"method":"PATCH","path":"/guests/{subjectId}","contract":"marketing-crm","summary":"Amend a guest profile","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestProfileDetail"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AdjustLoyaltyPointsRequest": {"type":"object","x-ticvai-persistence":"none — writes marketing.loyalty_points","description":"**A correction is a new entry, never an edit.** Reversing an entry writes a row pointing at it through `reversedLoyaltyPointsId`; granting goodwill writes a row with no reversal target. Either way the movement has a reason and an author, and the history stays walkable.\n","required":["programmeId","points","reason"],"properties":{"programmeId":{"type":"string","format":"uuid"},"points":{"type":"integer","description":"Signed. Negative removes points, and the balance may not go below zero."},"reason":{"type":"string","description":"**Goodwill, correction or expiry reversal, and nothing else (decided 28 September, audit R149).** A service-recovery grant is `goodwill`, a fraud or migration fix is `correction`, and returning points that expired in error is `expiryReversal`. None of them moves the tier or `lifetimePoints`.\n","enum":["goodwill","correction","expiryReversal"]},"reversedLoyaltyPointsId":{"type":"string","format":"uuid","nullable":true,"description":"The entry this reverses, when it is a reversal. **Set it and the sign is checked against the original** — a reversal that does not cancel what it names is a second grant wearing a correction's label.\n"},"notes":{"type":"string","maxLength":1000,"nullable":true}}},
"ConsentDecision": {"type":"string","enum":["granted","withdrawn","notAsked"]},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"ConsentRecord": {"x-ticvai-persistence":"marketing.consent_record + marketing.consent_record_channel","allOf":[{"$ref":"#/components/schemas/RecordConsentRequest"},{"type":"object","required":["id","subjectId"],"properties":{"id":{"type":"string"},"subjectId":{"type":"string","format":"uuid"},"recordedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"The order whose checkout carried the opt-in (source `checkout`, M18-15): the UUIDv7 of orders.sales_order. Null for every other source.","x-ticvai-references":"orders.sales_order"},"verifiedContactRef":{"type":"string","nullable":true,"maxLength":128,"description":"The verified contact the checkout opt-in was given against (ADR-0045), as the keyed hash the guest match policy uses; never the raw address. It is how a checkout consent given without an account is attached to the profile when the contact later matches one."},"supersededAt":{"type":"string","format":"date-time","nullable":true}}}]},
"ConsentState": {"x-ticvai-persistence":"none — projection over consent_record","type":"object","required":["subjectId","purposes"],"properties":{"subjectId":{"type":"string","format":"uuid"},"purposes":{"type":"array","items":{"type":"object","required":["purpose","decision","requiresRenewal"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","nullable":true},"requiresRenewal":{"type":"boolean","description":"True where the notice has been superseded since consent was given."},"decidedAt":{"type":"string","format":"date-time","nullable":true}}}}}},
"CreateSegmentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","criteria"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid"},"match":{"type":"string","enum":["all","any"],"default":"all"},"criteria":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/SegmentCriterion"}},"excludeSegmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"ruleGroups":{"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","type":"array","description":"**Nested AND / OR / NOT groups** (contract gap CHG-WIR-007, BO-755; CHG-CSA-045). Where present, the segment matches `criteria` (combined by `match`) AND every group here. Absent keeps the flat list.","items":{"$ref":"#/components/schemas/SegmentRuleGroup"}},"effectiveFrom":{"type":"string","format":"date-time","nullable":true,"description":"The segment is evaluated for sends only from this time."},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who answers for the segment; defaults to its creator."},"requiresApproval":{"type":"boolean","default":false,"description":"Where true, a campaign may use the segment only after an `approvals` request on it is approved."}}},
"Customer360ServiceProfileView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.guest_profile, pii.subject, pii.subject_contact, marketing.loyalty_position, marketing.guest_preference, marketing.consent_record, marketing.suppression, marketing.case, orders.sales_order, orders.reservation, orders.group_booking, access.entitlement and wallet.balance","description":"The service view of one guest. Fields the caller may not see are null, never omitted.","required":["customerId","customerSince","openCases","serviceAlerts"],"properties":{"customerId":{"type":"string","format":"uuid","description":"The guest's `subjectId`."},"customerName":{"type":"string","nullable":true,"description":"Null unless the caller holds GUEST_VIEW_PII."},"customerType":{"type":"string","enum":["individual","member","groupOrganiser","corporate","partner"]},"membershipStatus":{"type":"string","enum":["none","active","expiring","lapsed"]},"loyaltyTier":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","maxLength":10,"nullable":true},"country":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"contactDetails":{"type":"object","description":"Masked (e.g. `j***@example.com`, `+971 ** *** 4821`) unless the caller holds GUEST_VIEW_PII.","properties":{"email":{"type":"string","nullable":true},"phone":{"type":"string","nullable":true}}},"customerSince":{"type":"string","format":"date-time"},"customerValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Lifetime net spend across the tenant."},"openCases":{"type":"integer","minimum":0},"riskAttentionIndicator":{"type":"string","enum":["none","attention","risk"],"description":"`attention` with an open complaint or an unresolved refund case; `risk` with a breached SLA or a repeat contact on the same issue."},"upcomingTickets":{"type":"integer","minimum":0},"activeMembership":{"type":"object","nullable":true,"properties":{"membershipId":{"type":"string"},"planName":{"type":"string"},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"walletBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"activeReservations":{"type":"integer","minimum":0},"futureGroupBookings":{"type":"integer","minimum":0},"openOrders":{"type":"integer","minimum":0},"serviceAlerts":{"type":"array","maxItems":20,"items":{"type":"object","required":["kind","message"],"properties":{"kind":{"type":"string","enum":["eventSoon","unresolvedRefundCase","membershipExpiring","openComplaint","communicationRestricted"]},"message":{"type":"string"},"referenceId":{"type":"string","nullable":true}}}},"preferredCommunicationChannel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"nullable":true},"marketingConsent":{"$ref":"#/components/schemas/ConsentDecision"},"accessibilityRequirements":{"type":"array","nullable":true,"description":"Null unless the caller holds GUEST_VIEW_PII.","items":{"type":"string"}},"communicationRestrictions":{"type":"array","description":"Channels the guest must not be contacted on (`getSuppressionList`).","items":{"$ref":"#/components/schemas/MessageChannel"}},"aiSummary":{"type":"object","nullable":true,"description":"Where the AI policy enables `summarise`. AI-derived and labelled as such.","properties":{"text":{"type":"string","maxLength":2000},"generatedAt":{"type":"string","format":"date-time"}}}}},
"GuestAttributeModel": {"type":"object","x-ticvai-persistence":"marketing.guest_attribute_model","description":"Board 1.3. **Visibility by jurisdiction is what makes this a model and not a form.**","properties":{"version":{"type":"integer"},"fieldGroups":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"label":{"type":"string"},"displayOrder":{"type":"integer"}}}},"attributes":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"label":{"type":"string"},"groupCode":{"type":"string"},"dataType":{"type":"string"},"standard":{"type":"boolean","default":false},"mandatory":{"type":"boolean","default":false},"defaultValue":{"nullable":true},"allowedValues":{"type":"array","items":{"type":"string"}},"validationExpression":{"type":"string","nullable":true},"sensitive":{"type":"boolean","default":false},"visibleToRoles":{"type":"array","items":{"type":"string"}},"editableByRoles":{"type":"array","items":{"type":"string"}},"lawfulInJurisdictions":{"type":"array","items":{"type":"string"},"description":"**Empty means everywhere.** A nationality field lawful in one jurisdiction and not another cannot be a column somebody ships.\n"},"countsTowardCompleteness":{"type":"boolean","default":false}}}},"identifiers":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"primary":{"type":"boolean","default":false},"sourceSystem":{"type":"string","nullable":true},"sourcePriority":{"type":"integer"}}}},"publishedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"GuestExtraFieldDefinition": {"type":"object","x-ticvai-persistence":"none — composed from a field and its options","description":"**A select with no options is not a field**, so the options come back with the definition rather than from a second call.\n","required":["field"],"properties":{"field":{"$ref":"#/components/schemas/MarketingGuestExtraField"},"options":{"type":"array","items":{"$ref":"#/components/schemas/MarketingGuestExtraOption"}}}},
"GuestIntelligence": {"type":"object","description":"Board 1.10. **Explainable, or an agent will ignore it or over-trust it.**","properties":{"subjectId":{"type":"string","format":"uuid"},"scores":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["historicalLtv","predictedLtv","engagement","churnRisk","inactivityRisk","cancellationRisk","upgradePropensity","nextPurchasePropensity"]},"value":{"type":"number"},"band":{"type":"string","nullable":true},"confidence":{"type":"number","nullable":true},"modelId":{"type":"string","nullable":true},"modelVersion":{"type":"string","nullable":true},"computedAt":{"type":"string","format":"date-time"},"factors":{"type":"array","items":{"type":"object","properties":{"factor":{"type":"string"},"contribution":{"type":"number"}}}},"limitations":{"type":"array","items":{"type":"string"},"description":"**Policy and data limitations travel with the score**, so the rule that prediction never overrides consent cannot be forgotten downstream.\n"}}}},"affinities":{"type":"array","items":{"type":"object","properties":{"productCategoryId":{"type":"string","format":"uuid"},"label":{"type":"string"},"strength":{"type":"number"}}}},"nextBestActions":{"type":"array","items":{"type":"object","properties":{"action":{"type":"string"},"expectedImpact":{"type":"string","nullable":true},"confidence":{"type":"number","nullable":true}}}}}},
"GuestPreferences": {"type":"object","x-ticvai-persistence":"marketing.guest_preference","description":"**What the guest likes, kept apart from what they permit** (consent) and from who they are (the profile). One row per subject. `dietary` and `accessibility` are here rather than as tags because BL-134 gives them their own consent purpose and retention.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid","readOnly":true},"seatingPreference":{"type":"string","nullable":true,"maxLength":200},"drinkPreferences":{"type":"array","items":{"type":"string"}},"dietary":{"type":"array","description":"Also written by `updateMyProfile`.","items":{"type":"string"}},"accessibility":{"type":"array","description":"Also written by `updateMyProfile`.","items":{"type":"string"}},"preferredChannel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"x-ticvai-persisted":false,"description":"**Stored on the profile** (`GuestProfile.preferredChannel`) — carried here because the preference screen edits it beside the rest.\n"},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GuestProfile": {"x-ticvai-persistence":"marketing.guest_profile","type":"object","required":["subjectId","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid","description":"Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"},"displayName":{"type":"string","nullable":true},"email":{"type":"string","nullable":true},"phone":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","nullable":true},"preferredChannel":{"$ref":"#/components/schemas/MessageChannel"},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells. Marketing acts locally."},"tags":{"type":"array","items":{"type":"string"}},"engagementScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"description":"22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"},"engagementTier":{"type":"string","nullable":true,"enum":["new","active","occasional","lapsing","lapsed","dormant"],"description":"5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"},"lifetimeValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"visitCount":{"type":"integer"},"lastVisitAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"},"mergedIntoSubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`**, which retain it as a redirect rather than deleting it. A read that lands here follows it; a second merge of a profile that has one is refused as `alreadyMerged`.\n"},"mergedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"GuestProfileDetail": {"x-ticvai-persistence":"marketing.guest_profile","allOf":[{"$ref":"#/components/schemas/GuestProfile"},{"type":"object","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"consents":{"$ref":"#/components/schemas/ConsentState"},"loyalty":{"$ref":"#/components/schemas/LoyaltyPosition"},"openCaseCount":{"type":"integer"},"recentOrderIds":{"type":"array","items":{"type":"string"}},"membershipIds":{"type":"array","items":{"type":"string","format":"uuid"}},"notes":{"type":"string","nullable":true}}}]},
"GuestRelationship": {"type":"object","x-ticvai-persistence":"marketing.guest_relationship","x-ticvai-retired-columns":["related_guest_id"],"description":"Boards 1.7 and 1.8. **Links people without merging them**, which is the whole design.\n","required":["relatedSubjectId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"relatedSubjectId":{"type":"string","format":"uuid","nullable":true},"organisationId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["parent","guardian","spouse","dependant","householdMember","employee","student","groupLeader","travelAgent","reseller"]},"authorities":{"type":"array","items":{"type":"string","enum":["purchaseFor","bookFor","manageProfile","signWaiver","viewHistory","receiveCommunications"]},"description":"**Four different permissions, not one relationship.** A guardianship granting all of them forever survives the child becoming an adult.\n"},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"sharedBenefits":{"type":"boolean","default":false},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"GuestTimelineEvent": {"type":"object","description":"Board 1.5. **Facts, notes and predictions distinguished on the row.**","properties":{"id":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"kind":{"type":"string","enum":["purchase","ticketUsed","reservation","visit","membershipChange","loyalty","wallet","campaign","message","case","survey","waiver","note","prediction"]},"nature":{"type":"string","enum":["operationalFact","userNote","aiDerived"],"description":"**A prediction and a gate scan are both useful and only one happened.**"},"summary":{"type":"string"},"channel":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"sourceContract":{"type":"string","nullable":true},"sourceReferenceId":{"type":"string","format":"uuid","nullable":true},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"outcome":{"type":"string","nullable":true}}},
"IdentityGuestVerification": {"type":"object","x-ticvai-persistence":"identity.guest_identity_verification","description":"**One guest identity-document verification** (5.3.21; decided 29 September, build pass): the document it checks, its status, the method and who decided. The document itself is `pii.subject_document`; this row holds no document number.","required":["id","subjectId","status","submittedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid"},"subjectDocumentId":{"type":"string","format":"uuid","description":"The `pii.subject_document` row submitted."},"documentKind":{"type":"string","enum":["passport","emiratesId","nationalId","drivingLicence","residencePermit","other"]},"documentNumberLast4":{"type":"string","maxLength":4,"nullable":true,"readOnly":true},"reason":{"type":"string","enum":["policyRequired","ageRestrictedPurchase","residentPricing","accountRecovery"]},"status":{"type":"string","enum":["pending","verified","rejected","resubmissionRequested"],"readOnly":true},"method":{"type":"string","enum":["manualReview","documentScanner","provider"],"nullable":true,"readOnly":true},"decisionReason":{"type":"string","maxLength":300,"nullable":true,"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"submittedAt":{"type":"string","format":"date-time","readOnly":true},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"documentImageDeletedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the scan (and any selfie) was deleted under the policy's retention."}}},
"LoyaltyAdjustmentResult": {"type":"object","x-ticvai-persistence":"none — composed from the entry posted and the resulting position","description":"**Both halves of an adjustment, because returning only the balance is the defect decision 8 named.** Until 20 September this operation moved `marketing.loyalty_position` and returned it, and posted nothing to `marketing.loyalty_points` — so a manual adjustment was the one movement in the system that could not be walked back to a reason.\n","required":["entry","position"],"properties":{"entry":{"$ref":"#/components/schemas/MarketingLoyaltyPoints"},"position":{"$ref":"#/components/schemas/LoyaltyPosition"}}},
"LoyaltyPosition": {"x-ticvai-persistence":"marketing.loyalty_position","type":"object","required":["subjectId","programmeId","pointsBalance","tierCode"],"properties":{"leaderboardNickname":{"type":"string","nullable":true,"maxLength":24,"description":"BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever they reach the board and changeable afterwards; `setLeaderboardNickname` is the only thing that writes it.\n**Null means the guest has not chosen one yet, and the board shows a generated `Player-4821` in its place** — never `pii.subject.display_name`, which would disclose silently on the day a guest first placed and is the case this field exists to prevent.\n**The generated name is computed at read time and not stored here.** Writing it would make *\"has this guest chosen a name\"* unanswerable, and that flag is what the prompt-on-reaching-the-board depends on.\n"},"subjectId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid"},"pointsBalance":{"type":"integer"},"lifetimePoints":{"type":"integer"},"tierId":{"type":"string","format":"uuid","nullable":true,"description":"**The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September with `marketing.programme_tier`: the two strings were a cache of something that did not exist, and a cache with no source cannot be rebuilt or audited.\n"},"tierCode":{"type":"string"},"tierName":{"type":"string"},"pointsToNextTier":{"type":"integer","nullable":true},"nextExpiryPoints":{"type":"integer","nullable":true},"nextExpiryAt":{"type":"string","format":"date-time","nullable":true}}},
"MarketingGuestExtraField": {"type":"object","x-ticvai-persistence":"marketing.guest_extra_field","description":"**Taken from the backend workbook, 20 September.** NEW TABLE. Defines an extra field that Admin wants to add to the customer form, such as Date of Birth, Emergency Contact, or Jersey Size.","required":["tenantId","name","type","isRequired","displayOrder","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":150},"type":{"type":"string","maxLength":30},"isRequired":{"type":"boolean"},"displayOrder":{"type":"integer"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"MarketingGuestExtraOption": {"type":"object","x-ticvai-persistence":"marketing.guest_extra_option","description":"**Taken from the backend workbook, 20 September.** NEW TABLE. Stores dropdown choices only when an extra field uses SELECT type, for example Language = English, Hindi, Marathi.","required":["fieldId","name","displayOrder","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"fieldId":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":150},"displayOrder":{"type":"integer"},"isActive":{"type":"boolean"}}},
"MarketingLoyaltyPoints": {"type":"object","x-ticvai-persistence":"marketing.loyalty_points","description":"**Taken from the backend workbook, 20 September.** Stores every loyalty point earn, redeem, expire, adjustment, or reversal transaction for a customer.","required":["programId","customerId","transactionType","points","balanceAfter","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"programId":{"type":"string","format":"uuid"},"customerId":{"type":"string","format":"uuid"},"transactionType":{"type":"string","maxLength":30},"points":{"type":"number"},"balanceAfter":{"type":"number"},"sourceType":{"type":"string","maxLength":50,"nullable":true},"sourceReferenceId":{"type":"string","format":"uuid","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true},"reversedLoyaltyPointsId":{"type":"string","format":"uuid","nullable":true},"notes":{"type":"string","maxLength":500,"nullable":true},"reason":{"type":"string","nullable":true,"description":"For a manual movement, `AdjustLoyaltyPointsRequest.reason`. Null for an accrual, a redemption or an expiry, whose `transactionType` and source already say why. The three manual types are the only ones (audit R149).","enum":["goodwill","correction","expiryReversal"]},"authorPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who posted a manual movement. Null where the platform posted it."},"createdAt":{"type":"string","format":"date-time"}}},
"MergeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["survivingSubjectId","absorbedSubjectId","transferred"],"properties":{"survivingSubjectId":{"type":"string","format":"uuid"},"absorbedSubjectId":{"type":"string","format":"uuid"},"transferred":{"type":"object","properties":{"orders":{"type":"integer"},"cases":{"type":"integer"},"loyaltyPoints":{"type":"integer","description":"The total points moved across every programme. The per-programme outcome is `loyaltyProgrammes`."}}},"loyaltyProgrammes":{"type":"array","description":"**One entry per loyalty programme either record belonged to (decided 28 September, audit R149).** Points are added and the higher tier is kept, per programme — a single points number cannot say which programme it belongs to.\n","items":{"type":"object","required":["programmeId","pointsAdded","resultingPoints"],"properties":{"programmeId":{"type":"string","format":"uuid"},"pointsAdded":{"type":"integer","description":"The absorbed record's balance in this programme, added to the survivor's."},"resultingPoints":{"type":"integer"},"tierKept":{"type":"string","nullable":true,"description":"The higher of the two records' tiers in this programme."}}}},"consentOutcome":{"type":"array","description":"Per purpose, the resulting position. Where the two profiles disagreed, the more restrictive position won.\n","items":{"type":"object","properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"result":{"$ref":"#/components/schemas/ConsentDecision"},"wasRestricted":{"type":"boolean"}}}}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RecordConsentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["purpose","decision","noticeVersion","source","recordedAt"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","description":"Omit to apply to every channel the purpose covers.","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string"},"source":{"$ref":"#/components/schemas/ConsentSource"},"recordedAt":{"type":"string","format":"date-time"}}},
"Segment": {"x-ticvai-persistence":"marketing.segment + marketing.segment_criterion","allOf":[{"$ref":"#/components/schemas/CreateSegmentRequest"},{"type":"object","required":["id","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"lastEvaluatedSize":{"type":"integer","nullable":true},"lastEvaluatedAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"}}}]}
}
```
