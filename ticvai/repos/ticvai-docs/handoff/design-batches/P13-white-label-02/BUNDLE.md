# P13-white-label-02 — P13 · White Label (2 of 3)

**10 screens · 52 operations · 70 schemas · 11 permissions**

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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `AI_USE, GUEST_MANAGE, GUEST_VIEW, MARKETING_MANAGE, MARKETING_VIEW, PRODUCT_VIEW, ROLE_MANAGE, SCOPE_VIEW, TENANT_CONFIGURE, TENANT_PUBLISH, USER_MANAGE`. A control nobody can use must say so,
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
| `CMS-013` | SEO & Metadata | A | 25 | 14 | 5 | 12 | 0 | 0 | configures | notStarted (generated) |
| `CMS-011` | Translations | A | 4 | 27 | 5 | 10 | 2 | 0 | configures | notStarted (generated) |
| `CMS-012` | RTL Preview | A | 0 | 8 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `CMS-014` | Publishing Workflow | A | 9 | 27 | 5 | 1 | 2 | 6 | — | notStarted (generated) |
| `CMS-015` | Version History | A | 0 | 14 | 6 | 3 | 0 | 0 | — | notStarted (generated) |
| `CMS-016` | Site Settings | A | 71 | 24 | 6 | 6 | 3 | 6 | configures | notStarted (generated) |
| `CMS-017` | Domain & Certificate | A | 3 | 21 | 6 | 0 | 1 | 0 | configures | notStarted (generated) |
| `CMS-018` | Consent & Legal | A | 25 | 44 | 6 | 4 | 2 | 4 | configures | notStarted (generated) |
| `CMS-019` | User Access | A | 6 | 21 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `CMS-101` | Help Me Choose | A | 28 | 18 | 6 | 3 | 4 | 0 | configures | notStarted (generated) |

## Thin screens in this batch

**CMS-012 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `CMS-013` SEO & Metadata

**Control how a page looks everywhere it is not the page.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-013 |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the screen declares only writes (`setSeoMetadata`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/white-label/seo-metadata` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Control how a page, product, event or venue appears in search and when shared: title, description, canonical, slug, hreflang, Open Graph, schema type and noindex. Metadata is generated by default and overridable, because a venue with 400 products will not write 400 descriptions. Changing a slug is a redirect, not an edit.

**Fixed on main** (the package already carries these; draw what it says): The form is raw SeoMetadata fields, including id, entityKind, entityId, scopePath, isAutoGenerated and openGraph as text fields. (CHG-SGU-017); getSeoMetadata (the metadata in force for one page) is consumed by no screen. (CHG-WIR-005); A slug change needs createUrlRedirect, declared only on BO-842. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Page | picker: choose an entity | optional | — | — | shows names, sends the id | Pick the page (content page, product, event, performance, membership, promotion, venue) from a search, never by id; the kind follows from the pick. | `SeoMetadata.entityId` |
| Language | text field | optional | — | — | — | One tab per enabled locale; hreflang pairs are generated from the tabs. | `SeoMetadata.locale` |
| Title | text field | optional | — | — | — | Counter at about 60 characters; "Generated" badge until edited, with Revert to generated. | `SeoMetadata.title` |
| Description | text field | optional | — | — | — | Counter at about 160 characters. | `SeoMetadata.metaDescription` |
| Address (slug) | text field | optional | — | — | — | Editing a live slug warns that a 301 redirect from the old address is created (`createUrlRedirect`). | `SeoMetadata.slug` |
| Hide from search | toggle | optional | off | — | — | — | `SeoMetadata.noIndex` |
| Social share card | key and value settings | optional | — | — | — | Title, description and image; previewed beside the search snippet. | `SeoMetadata.openGraph` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Entity kind | select | — | Content page · Product · Event · Performance · Membership · Promotion · Venue | `getSeoMetadata` ?entityKind |
| Entity | picker: choose an entity | — | — | `getSeoMetadata` ?entityId |
| Locale | text field | — | — | `getSeoMetadata` ?locale |

**Form: Add redirect** (modal, opened by *Add redirect*; *Add redirect* calls `createUrlRedirect`, *Cancel* sends nothing)

**Collects what `createUrlRedirect` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| From path `fromPath` | text field | required | — | — | — | — | `createUrlRedirect` body |
| To path `toPath` | text field | required | — | — | — | — | `createUrlRedirect` body |
| Status code `statusCode` | radio group | required | — | 301 · 302 · 307 · 308 | — | — | `createUrlRedirect` body |
| Reason `reason` | radio group | optional | — | Content migrated · Page retired · Campaign expired · Restructure · Slug changed | — | — | `createUrlRedirect` body |
| Is active `isActive` | toggle | optional | on | — | — | — | `createUrlRedirect` body |

**Sent by *Save SEO metadata*** (`setSeoMetadata`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Entity kind `entityKind` | select | required | — | Content page · Product · Event · Performance · Membership · Promotion · Venue | — | — | `setSeoMetadata` body |
| Entity `entityId` | picker: choose an entity | required | — | — | shows names, sends the id | — | `setSeoMetadata` body |
| Locale `locale` | text field | optional | — | — | — | — | `setSeoMetadata` body |
| Title `title` | text field | optional | — | — | — | — | `setSeoMetadata` body |
| Meta description `metaDescription` | text field | optional | — | — | — | — | `setSeoMetadata` body |
| Keywords `keywords` | list of values (chips) | optional | — | — | — | — | `setSeoMetadata` body |
| Canonical URL `canonicalUrl` | text field | optional | — | — | — | — | `setSeoMetadata` body |
| Slug `slug` | text field | optional | — | — | — | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking and now is not. | `setSeoMetadata` body |
| Hreflang `hreflang` | key and value settings | optional | — | — | — | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page. | `setSeoMetadata` body |
| Schema org type `schemaOrgType` | text field | optional | — | — | — | — | `setSeoMetadata` body |
| Open graph `openGraph` | key and value settings | optional | — | — | — | — | `setSeoMetadata` body |
| Is auto generated `isAutoGenerated` | toggle | optional | on | — | — | 22.11.2. Generated by default and overridable. | `setSeoMetadata` body |
| No index `noIndex` | toggle | optional | off | — | — | — | `setSeoMetadata` body |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Page (entity)**: Pick the page (content page, product, event, performance, membership, promotion, venue) from a search, never by id. *(source: contracts/satellite/marketing-crm.yaml#setSeoMetadata)*
- **Language**: One tab per enabled locale (English, Arabic); hreflang pairs are generated from the tabs. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/SeoMetadata; DI-019)*
- **Title and description**: Counters at about 60 and 160 characters; a "Generated" badge until edited, with Revert to generated. *(source: contracts/satellite/marketing-crm.yaml#setSeoMetadata)*
- **Slug**: Human-readable. Editing a live slug warns that a 301 redirect from the old address will be created. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/SeoMetadata; contracts/satellite/marketing-crm.yaml#createUrlRedirect)*
- **Hide from search**: A toggle (noindex) with the consequence stated. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/SeoMetadata)*

#### Outputs: what the screen shows and produces

**Shown**

**Metadata in force** (detail panel, from `getSeoMetadata`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Entity kind | chip: Content page, Product, Event, Performance, Membership, Promotion… | — |
| Entity | the name it points at, never the id | — |
| Locale | text | — |
| Title | text | — |
| Meta description | text | — |
| Keywords | list or chips (count when long) | — |
| Canonical URL | text | — |
| Slug | text | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking … |
| Hreflang | grouped details | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of … |
| Schema org type | text | — |
| Open graph | grouped details | — |
| Is auto generated | yes / no (icon or chip) | 22.11.2. Generated by default and overridable. |
| No index | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save SEO metadata (primary button) | `setSeoMetadata` PUT `/seo-metadata` | SeoMetadata | SeoMetadata | — | — |
| Add redirect (secondary button) | `createUrlRedirect` POST `/seo-redirects` | UrlRedirect | UrlRedirect | — | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Previews**: A search-result snippet and a social share card, in both languages. *(source: designer default)*

**Data it reads**: `getSeoMetadata` (onLoad, The metadata in force for this page)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Detail loads |
| Error (`?state=error`) | Could not load |
| Empty, first run (`?state=emptyFirstRun`) | No metadata saved for this page yet: the generated title and description are shown with the "Generated" badge. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `MARKETING_VIEW`, which `getSeoMetadata` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MARKETING_MANAGE` for `setSeoMetadata`, `createUrlRedirect`. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-842`: Same fields and the redirect behaviour; BO-842 owns the redirect list.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entity: Product - Coastal Aqua Day Pass
en:
  title: Coastal Aqua Day Pass - Dubai Water Park Tickets
  slug: day-pass
ar:
  title: تذكرة يوم كوستال أكوا - حديقة مائية في دبي
  slug: day-pass-ar
```

#### Permissions

- `setSeoMetadata` → `MARKETING_MANAGE` (configure) · staff
- `getSeoMetadata` → `MARKETING_VIEW` (read) · staff
- `createUrlRedirect` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `MARKETING_VIEW`, which `getSeoMetadata` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MARKETING_MANAGE` for `setSeoMetadata`, `createUrlRedirect`.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.11.1 | SEO Metadata Management | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.2 | Dynamic SEO Generation | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.3 | AI SEO Optimization | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.4 | Sitemap Management | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.5 | Schema Markup Support | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.6 | SEO-Friendly URL Management | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.7 | Redirect Management | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.8 | SEO Content Analysis | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.9 | Internal Linking Recommendations | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.10 | SEO Analytics Dashboard | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.11 | Multi-Language SEO | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.12 | SEO Audit & Compliance | Marketing & CRM | CONTRACTED | data `SeoMetadata` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Entity kind (`seo.entityKind`) | Content page · Product · Event · Performance · Membership · Promotion · Venue | — | every website screen | — |
| Entity (`seo.entityId`) | shows names, sends the id | — | every website screen | — |
| Locale (`seo.locale`) | — | — | every website screen | — |
| SEO metadata title (`seo.title`) | — | — | every website screen | — |
| Meta description (`seo.metaDescription`) | — | — | every website screen | — |
| Keywords (`seo.keywords`) | — | — | every website screen | — |
| Canonical URL (`seo.canonicalUrl`) | — | — | every website screen | — |
| Slug (`seo.slug`) | — | — | every website screen | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking and now is not. |
| Hreflang (`seo.hreflang`) | — | — | every website screen | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page. |
| Schema org type (`seo.schemaOrgType`) | — | — | every website screen | — |
| Open graph (`seo.openGraph`) | — | — | every website screen | — |
| Is auto generated (`seo.isAutoGenerated`) | — | on | every website screen | 22.11.2. Generated by default and overridable. |
| No index (`seo.noIndex`) | — | off | every website screen | — |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-013` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-013?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save SEO metadata, Add redirect.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-011` Translations

**Fill in what every language is missing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-011 |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the screen declares only writes (`setLanguages`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `translationJobId` (CMS-011) |
| Route | `/white-label/translations` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. The CHG-WIR-017 gap (no read follows a proposeTranslations job) is closed: getTranslationProposals was built (CHG-CSA-045) and is bound here (CHG-SGU-022).

**Known gaps.** Removed 2 October 2026 (CHG-WIR-015): proposeTranslations answers 202 and nothing on the screen can follow the job (R288); the machine-translation step stays on BO-785 and BO-793 until a status read …

**From the White Label & CMS process.** Choose the guest languages and the default, then see, per language, how much authored content is still missing and go fill it. Enabling a language never translates anything; the screen exists so nobody publishes a half-translated app. Translation of interface strings is TICVAI's; this screen covers the tenant's own content.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The translation workflow the client asked for (enter English, machine-translate, the tenant's team reviews before publishing) has no operation on this screen. (CHG-WIR-017)

**Fixed on main** (the package already carries these; draw what it says): The screen declares only setLanguages and no read, so it cannot show the current languages or the gaps it exists for. (CHG-WIR-015); Default language is drawn as a free textField. (CHG-SGU-022).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How are Simplified and Traditional Chinese told apart with two-letter codes?** → Drawn default accepted: Treat zh as Simplified. *(decided by Chinmay, 2026-10-02; DEC-155 / CHG-NOTE-009)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Languages | multi select | — | — | — | — | Required. | — |
| Default language | select field | — | — | — | — | One of the enabled languages (`setLanguages` answers 400 otherwise). | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Version | text field | — | — | `getTenantConfig` ?version |

**Sent by *Save languages*** (`setLanguages`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Languages `languages` | list of values (chips) | required | — | at least 1 | — | — | `setLanguages` body |
| Default language `defaultLanguage` | language picker | required | — | — | ISO 639-1 code, shown as the language name | — | `setLanguages` body |

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **languages**: A list of language chips (English, العربية, Русский, 中文, Español...), each a two-letter ISO 639-1 code; at least one. Arabic carries an "RTL" tag (derived, rtlLanguages). Adding ar warns that an Arabic font is now required (CMS-003). *(source: contracts/satellite/white-label.yaml#setLanguages; DI-080; R163)*
- **defaultLanguage**: A select limited to the enabled languages (400 otherwise); the default is what a first-time guest sees before choosing. *(source: contracts/satellite/white-label.yaml#setLanguages)*

#### Outputs: what the screen shows and produces

**Shown**

**Languages** (detail panel, from `getTenantConfig`)

| Shows | Format | Notes |
|---|---|---|
| Brand | grouped details | Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB … |
| Logo | the image or video | The primary logo. |
| Logo dark image | the image or video | Used on dark backgrounds. Falls back to the primary logo. |
| Logo variant | chip: Light, Dark, Duotone | Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4). |
| Favicon | the image or video | The browser tab icon for the guest web app. |
| Splash image | list or chips (count when long) | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish … |
| Splash duration seconds | 1,234 | — |
| Splash background colour | colour swatch | — |
| Show loading indicator | yes / no (icon or chip) | — |
| Splash change scope | chip: Runtime, Build time | Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163). |
| Intro video | the image or video | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode | chip: Off, First launch, Every launch | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Show powered by | yes / no (icon or chip) | "Powered by TICVAI", a configuration toggle, on by default (Chinmay, 2 October, workbook Q160 and the pre-apply round; consistent with … |
| App icons | grouped details | — |
| Source image | the image or video | The `MediaAsset` id of the 1024×1024 source. |
| Derived | list or chips (count when long) | Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on … |
| Platform | chip: Ios, Android, Web | — |
| Size | text | — |
| Asset ref | the image or video | — |
| Change scope | chip: Runtime, Build time | Always `buildTime` — icons are baked into the binary. |

**Proposed translations** (data table, from `getTranslationProposals`): The machine-proposed strings for the missing languages, accepted or edited one by one.

| Shows | Format | Notes |
|---|---|---|
| Target locale | text | — |
| Translation job | the name it points at, never the id | The job to follow with `getTranslationProposals` (contract gap CHG-WIR-017, CMS-011; CHG-CSA-045). |
| Status | chip: Running, Completed, Failed | `running` while drafts are still being written; `drafts` then holds those done so far. |
| Drafts | list or chips (count when long) | — |
| Target kind | chip: Content block, Product name, Email template, Message template | — |
| Target ref | text | The id of the block, product or template the draft sits on. |
| Draft text | text | The first-pass translation, as saved on the draft. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save languages (primary button) | `setLanguages` PUT `/tenant-config/languages` | inline | LanguageConfig | 400 Default is not among the enabled languages | — |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Translation gaps**: Per enabled language, missingCount and the areas (pages, FAQs, banners, navigation labels, availability message), each a link to the screen that holds the text. 0 shows a tick. Sorted by missing count, largest first. *(source: contracts/satellite/white-label.yaml#/components/schemas/LanguageConfig; handoff/localisation.md)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Save languages**: Writes the draft and returns translationGaps; publish is blocked by missingTranslation findings (validateTenantConfig). *(source: contracts/satellite/white-label.yaml#setLanguages; contracts/satellite/white-label.yaml#validateTenantConfig)*
- **Translate gaps with AI**: Proposes drafts for the tenant's team to review (ai proposeTranslations on BO-793); nothing goes live unreviewed. *(source: DI-081; MATRIX 22.10.15; screens/P08-venue-back-office.yaml#BO-793)*

**Data it reads**: `getTenantConfig` (onLoad, Languages and translation gaps)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved translations. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the translations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No translations configured. The form opens empty and `setLanguages` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `setLanguages` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Default is not among the enabled languages |

#### Edge cases to draw

- **Removing a language that is the default**: Refused until another default is chosen. *(source: contracts/satellite/white-label.yaml#setLanguages)*
- **Chinese**: The two-letter code zh cannot say Simplified or Traditional; show "Chinese (Simplified)" and raise the question. *(source: DI-020; contracts/satellite/white-label.yaml#/components/schemas/LanguageConfig)*

#### Consistency with other screens

- Match `ADM-018`: Same language control for platform staff.
- Match `GST-043`: The guest language button lists exactly these languages in this order.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
languages:
- en
- ar
- ru
defaultLanguage: en
translationGaps:
- language: ar
  missingCount: 7
  areas:
  - pages
  - faqs
  - banners
- language: ru
  missingCount: 42
  areas:
  - pages
  - faqs
  - navigation
  - banners
  - availabilityMessage
```

#### Permissions

- `setLanguages` → `TENANT_CONFIGURE` (configure) · staff
- `getTenantConfig` → `TENANT_CONFIGURE` (configure) · staff, guest
- `getTranslationProposals` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `setLanguages` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.4.1 | The system should support multiple languages for the Ticketing POS, Self-Service Kiosks, websites mobile app and backend . | Ticketing Sales | CONTRACTED | `setLanguages` |
| 2.7.35 | The system should support: - Multilingual with language to be chosen by B2B client. Languages to include at a minimum Arabic and English. - Use of base system currency and all transactions performed … | Ticketing Sales | CONTRACTED | `setLanguages` |
| 2.16.12 | The system should allow usage of English and Arabic language on the ticket templates. | Ticketing Sales | CONTRACTED | `setLanguages` |
| 22.8.21 | Multi-Language Support | Marketing & CRM | CONTRACTED | `setLanguages` |
| 22.10.13 | Multi-Language Content Management | Marketing & CRM | CONTRACTED | `setLanguages` |
| 19.1.19 | Tenant-Specific Branding - System shall support tenant-specific branding. | Guest Mobile App & Branding | CONTRACTED | `getTenantConfig` |
| 22.10.1 | Multi-Site CMS | Marketing & CRM | CONTRACTED | `getTenantConfig` |
| 22.10.3 | Multi-Brand Management | Marketing & CRM | CONTRACTED | `getTenantConfig` |
| 19.1.21 | Tenant-Specific Notifications - System shall support tenant-specific notifications. | Guest Mobile App & Branding | CONTRACTED | data `TenantConfig` |
| 19.1.23 | Tenant-Specific Payment Methods - System shall support tenant-specific payment methods. | Guest Mobile App & Branding | CONTRACTED | data `TenantConfig` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A new language is added as a configuration change, not development. Qossai wants a table-driven workflow like his prior project: a translation spreadsheet with a column per language reviewed by native speakers, then fed back through an AI translation pass. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-083)*
- Translation workflow: text entered in English, machine-translated, then reviewed and validated by the tenant's own team in the back office/CMS before publishing; applies to website, POS and mobile app. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-081)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Languages (`languages.languages`) | at least 1 | — | every guest screen (web, app and kiosk) | the language button in the header; Arabic flips every screen right to left |
| Default language (`languages.defaultLanguage`) | ISO 639-1 code, shown as the language name | — | every guest screen (web, app and kiosk) | the language a first visit opens in |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-011` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-011?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save languages.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-012` RTL Preview

**See the site as an Arabic reader sees it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-012 |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getTenantConfig` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/white-label/rtl-preview` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**From the White Label & CMS process.** See the draft as an Arabic reader sees it, mirrored, on web and app, and run the checks that block a publish. Arabic is a mirror, not a translation: the preview must show what flips and what must not (prices, times, phone numbers, codes, logos, media controls).

**Fixed on main** (the package already carries these; draw what it says): The layout dumps the whole TenantConfig as a detail panel. (CHG-SGU-022).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **createPreview {language ar, platform, theme}**: Platform and theme toggles beside a direction toggle; language fixed to ar (or any enabled RTL language). *(source: contracts/satellite/white-label.yaml#createPreview; docs/architecture/rtl-and-theming.md)*

#### Outputs: what the screen shows and produces

**Shown**

**The site in Arabic** (live preview, from `createPreview`): `createPreview` with language ar: the draft mirrored right to left on web, iPhone and Android (F22 step 4).

| Shows | Format | Notes |
|---|---|---|
| Preview | the name it points at, never the id | — |
| URL | text | — |
| Platform | chip: Ios, Android, Web | — |
| Language | text | — |
| Output previews | list or chips (count when long) | The PDF ticket and the Apple and Google Wallet passes, previewed with the app (Chinmay, 2 October, workbook Q151: in Block A; CHG-CSA-041). |
| Output | chip: App, Pdf ticket, Apple wallet pass, Google wallet pass | — |
| URL | text | A short-lived link to the rendered output (the PDF, the `.pkpass`, or the Google pass preview), expiring with the preview. |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Validate tenant config (primary button) | `validateTenantConfig` POST `/tenant-config/validate` | — | ConfigValidationReport | — | — |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Mirrored preview**: Home, a booking step with the cart, the seat map and checkout in Arabic; the cart stays on the right unless cartSideInRtl is mirror; AED amounts and 09:00 – 17:00 stay left-to-right; untranslated strings are highlighted with the language they fell back to. *(source: DI-1051; DI-975; docs/architecture/rtl-and-theming.md)*
- **Findings**: validateTenantConfig findings filtered to missingTranslation and arabicFontMissing first, each linking to its screen. *(source: contracts/satellite/white-label.yaml#validateTenantConfig)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Check what blocks a publish**: Runs validateTenantConfig (writes nothing). *(source: contracts/satellite/white-label.yaml#validateTenantConfig)*

**Where the user goes next**

- → `CMS-014` Publishing Workflow: *Publishes*
- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The Arabic preview of the draft. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rtl preview untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rtl preview yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getTenantConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **ar not enabled**: Offers to enable it on CMS-011; no preview. *(source: contracts/satellite/white-label.yaml#setLanguages)*
- **Long descriptions without Arabic copy**: Shown in English inside the Arabic layout, highlighted, as agreed until final Arabic copy arrives. *(source: DI-975)*

#### Consistency with other screens

- Match `CMS-006`: Same renderer; this screen is its RTL view plus the checks.
- Match `GST-043`: What the guest sees in Arabic is exactly this preview.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
ar:
  home: الرئيسية
  buyTickets: اشترِ التذاكر
  total: الإجمالي AED 498.00
  hours: 09:00 – 17:00
```

#### Permissions

- `validateTenantConfig` → `TENANT_CONFIGURE` (configure) · staff
- `createPreview` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getTenantConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-012` · status **notStarted** · provenance generated
- Flow F22 *A tenant rebrands their app*, step 4: Previews in both directions → **Arabic is a mirror, not a translation** — the preview must show it
- Flow F22 branch at step 4 (recoverable): when Arabic layout breaks with the new logo, A wide logo that fits left-aligned may not fit mirrored. **This is why the preview toggles direction**, and it is the defect that reaches production without one.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-012?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Validate tenant config.
- [ ] Every transition is wired: `CMS-014`, `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-014` Publishing Workflow

**Move a change from draft to live, with someone accountable (Site Builder step 7).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-014 |
| Who uses it | venue staff holding `TENANT_CONFIGURE`, `TENANT_PUBLISH` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getTenantAppStatus` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `venueId` (session), `version` (navigation), `packageId` (navigation) |
| Route | `/white-label/publishing-workflow` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **A rollback arrives here as a draft (decided 28 September, audit R139 (b)).** Version History (CMS-015) restores an old version into the working draft with `restoreConfigVersion` and reviews it with `diffConfigVersion`; only this screen's `publishTenantConfig` puts it live, with a note. A rollback is never one click. The CHG-WIR-017 gap (getTenantAppStatus and getPublishedBookingFlow need the staff audience) is closed by CHG-CSA-045 (CHG-SGU-022).

**From the White Label & CMS process.** Move the draft to live with someone accountable: see what changed since the live version, what still blocks, what will not reach app users until an app update, then publish now or at a set time with a note. Site Builder step 7. The one thing to get right: nobody presses Publish meaning Save; the gate states the consequence first.

**Fixed on main** (the package already carries these; draw what it says): The screen does not declare diffConfigVersion or createPreview. (CHG-WIR-015); The detail panel shows maintenance fields as if publish affected them. (CHG-SGU-022).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does a publish go through the approval matrix (ApprovalKind configurationChange), and must the approver differ from the author as for content blocks?** → Publishing: simulate (preview), then a single publish by a permission holder. An optional review/approval step the venue can switch on. *(decided by Chinmay, 2026-10-02; DEC-156 / CHG-NOTE-009 / CHG-SGU-010)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Review before publishing | toggle | optional | off | — | — | **Simulate, then a single publish by a permission holder** (decided by Chinmay, 2 October 2026; DEC-156). The venue may switch on an optional review step; then Publish answers 202 and the version … | `PublishReviewPolicy.enabled` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Flow type key | select | — | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour by language · Transport … | `listBookingFlows` ?flowTypeKey |

**Form: Publish** (modal, opened by *Publish*; *Publish* calls `publishTenantConfig`, *Cancel* sends nothing)

**Collects what `publishTenantConfig` sends before it is called.** Required: `note`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | required | — | min length 3; max length 500 | — | — | `publishTenantConfig` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Publish at a future time. Useful for a campaign launch. | `publishTenantConfig` body |

Errors to draw in the form: 409 Validation failed. (ConfigValidationProblem)

**Form: Simulate** (modal, opened by *Simulate*; *Simulate* calls `createPreview`, *Cancel* sends nothing)

**Collects what `createPreview` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Platform `platform` | segmented control | optional | — | Ios · Android · Web | — | — | `createPreview` body |
| Language `language` | language picker | optional | — | — | ISO 639-1 code, shown as the language name | — | `createPreview` body |
| Outputs `outputs` | multi-select chips | optional | — | App · Pdf ticket · Apple wallet pass · Google wallet pass | — | What to render besides the app (CHG-CSA-041). Absent means `app` only. | `createPreview` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | The product whose ticket and passes to render; a sample ticket where absent. | `createPreview` body |
| Expires in hours `expiresInHours` | number field (hours) | optional | 24 | min 1; max 168 | — | — | `createPreview` body |

**Form: Generate site package** (confirmDialog, opened by *Generate site package*; *Generate site package* calls `exportSitePackage`, *Cancel* sends nothing)

Generates the package from the published version; the download link follows when it is ready.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Version `version` | text field | optional | — | — | — | The published version to package; the current one where absent. | `exportSitePackage` body |

Errors to draw in the form: 409 Nothing is published yet (`nothing-published`).

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **note**: Required, 3-500 characters, plain words ("Summer theme and new homepage order"). *(source: contracts/satellite/white-label.yaml#publishTenantConfig)*
- **scheduledFor**: Optional date and time in the tenant's time zone (GST); a scheduled job activates it; must be in the future. *(source: contracts/satellite/white-label.yaml#publishTenantConfig)*
- **Review step (optional)**: A venue can switch on a review or approval step; otherwise a permission holder simulates (preview) and publishes in one step. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-009))*

#### Outputs: what the screen shows and produces

**Shown**

**The tenant app status** (detail panel, from `getTenantAppStatus`): What is published and what is waiting in the draft. Maintenance is live state, never published or restored, so it is shown only as context, apart from what Publish changes.

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
| Recent changes | list or chips (count when long) | Staff only. Names the principal behind each change, so it never reaches a public response. |

**Review changes** (detail panel, from `diffConfigVersion`)

| Shows | Format | Notes |
|---|---|---|
| From version | text | — |
| To version | text | — |
| Changes | list or chips (count when long) | — |
| Area | text | — |
| Path | text | — |
| Change kind | chip: Added, Removed, Modified | — |
| Before | text | — |
| After | text | — |
| Change scope | chip: Runtime, Build time | Whether a change reaches guests on publish or needs a store release. |

**Review policy** (detail panel, from `getPublishReviewPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Enabled | yes / no (icon or chip) | — |
| Reviewer must differ from author | yes / no (icon or chip) | — |
| Applies to | list or chips (count when long) | What the review covers. Empty means both. |

**Site package** (detail panel, from `getSitePackage`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Status | chip: Building, Ready, Failed | — |
| Download URL | text | Short-lived; present when `ready`. |
| Expires at | 1 Oct 2026, 14:30 | — |
| Requested by principal | the name it points at, never the id | — |
| Platform staff grant | the name it points at, never the id | The platform-staff grant it was made under, where platform staff made it (R098). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Generate site package (secondary button) | `exportSitePackage` POST `/site-package` | inline | SitePackage | 409 Nothing is published yet (`nothing-published`). | opens confirmDialog first |
| Publish (primary button) | `publishTenantConfig` POST `/tenant-config/publish` | inline | ConfigVersion | 409 Validation failed. (ConfigValidationProblem) | opens modal first |
| Validate tenant config (secondary button) | `validateTenantConfig` POST `/tenant-config/validate` | — | ConfigValidationReport | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
| Simulate (secondary button) | `createPreview` POST `/tenant-config/preview` | inline | Preview | — | opens modal first |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **What changes**: diffConfigVersion of the live version against the draft, grouped by area (Theme, Fonts, Homepage, Navigation, Booking flows by venue, Pages), each change as before and after, with the products whose booking steps change. *(source: contracts/satellite/white-label.yaml#diffConfigVersion; DI-194)*
- **Blocking findings**: Errors first (publish disabled with the count), then warnings; each links to the screen that fixes it. *(source: contracts/satellite/white-label.yaml#/components/schemas/ConfigValidationReport)*
- **Needs an app update**: pendingBuildTimeChanges listed by area and platform, with a link to CMS-104. *(source: contracts/satellite/white-label.yaml#/components/schemas/ConfigVersion)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Publish now / Schedule**: Validates, snapshots and makes the new version current atomically. Web guests see it on next load; app guests on next launch. 409 lists every finding. Success shows the version number and the build-time items not yet shipped. *(source: contracts/satellite/white-label.yaml#publishTenantConfig; F22 step 5)*
- **Preview**: Opens CMS-006 / CMS-012 for the draft. *(source: screens/P13-white-label-cms.yaml#CMS-102)*

**Data it reads**: `getTenantAppStatus` (onLoad, App status and recent changes); `listBookingFlows` (onLoad, The venue's flows and whether each is valid, for the gate …); `getPublishReviewPolicy` (onLoad, Whether publishing needs a review (off by default, DEC-156))

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*
- → `CMS-103` Booking Flows: *Fix a booking flow*; carries `bookingFlowId`
- → `CMS-104` App Build & Store Publishing: *Build the mobile app*
- → `CMS-102` Site Builder: *Back to the Site Builder*
- → `CMS-015` Version History: *Rolls back when something is wrong*; carries `version`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The publishing workflow, read by `getTenantAppStatus`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the publishing workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No publishing workflow yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listBookingFlows` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TENANT_PUBLISH` for `publishTenantConfig`, `setPublishReviewPolicy`, `exportSitePackage`, `getSitePackage`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Nothing is published yet (`nothing-published`).; 409 Validation failed. (ConfigValidationProblem) |

#### Edge cases to draw

- **Nothing changed since the live version**: Publish disabled with "No changes since version 14". *(source: contracts/satellite/white-label.yaml#/components/schemas/TenantAppStatus)*
- **Invalid booking flow at one venue**: Finding bookingFlowInvalid names the venue and flow and links to CMS-103 with the flow open. *(source: contracts/satellite/white-label.yaml#validateTenantConfig)*
- **User lacks TENANT_PUBLISH**: The diff and findings are visible; Publish replaced by "Ask someone with publish rights". *(source: contracts/satellite/white-label.yaml#publishTenantConfig)*
- **Arriving after a restore (from CMS-015)**: Banner "Draft restored from version 12"; the diff is the live version against the restored draft. *(source: R139)*

#### Consistency with other screens

- Match `CMS-015`: Same diff component.
- Match `CMS-103`: Its Publish site dialog is this gate.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
live: version 14, 2026-09-30 18:05 GST, by Mariam Al Hashimi, "Autumn hours"
draft: 'theme (primary #0B6E78 to #0E7C86), homepage (dining moved above shop), Kids Club Mirdif booking flow (extras
  turned off)'
buildTime: app icon (iOS, Android)
note: New teal and simpler Kids Club booking
```

#### Permissions

- `publishTenantConfig` → `TENANT_PUBLISH` (configure) · staff
- `validateTenantConfig` → `TENANT_CONFIGURE` (configure) · staff
- `getTenantAppStatus` → no permission · device, guest, staff
- `listBookingFlows` → `TENANT_CONFIGURE` (configure) · staff
- `diffConfigVersion` → `TENANT_CONFIGURE` (configure) · staff
- `createPreview` → `TENANT_CONFIGURE` (configure) · staff
- `getPublishReviewPolicy` → `TENANT_CONFIGURE` (configure) · staff
- `setPublishReviewPolicy` → `TENANT_PUBLISH` (configure) · staff
- `exportSitePackage` → `TENANT_PUBLISH` (configure) · staff
- `getSitePackage` → `TENANT_PUBLISH` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listBookingFlows` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `TENANT_PUBLISH` for `publishTenantConfig`, `setPublishReviewPolicy`, `exportSitePackage`, `getSitePackage`.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.24 | White Label Configuration Portal - System shall provide self-service white label configuration. | Guest Mobile App & Branding | CONTRACTED | `publishTenantConfig` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each client owns its Apple and Google developer accounts; the app is built in the CMS from a published configuration, with an in-platform guide (D-U-N-S number, opening accounts, store listing, store review). *(agreed · MoM 24 Sep 2026, M24-08 · DI-998)*
- The builder flow ends in a Review & Publish step before configuration goes live. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-194)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-014` · status **notStarted** · provenance generated
- Flow F102 *A brand is set, previewed, published and rolled back*, step 4: White-Label Branding Management. → 5 operations, 5 of them previously unwalked.
- Flow F22 *A tenant rebrands their app*, step 5: Publishes → Live on web immediately; the app picks it up on next launch
- Flow F22 *A tenant rebrands their app*, step 7: Publishes the restored draft → The previous brand is live again, through the same publish gate as any other change
- Flow F22 branch at step 5 (recoverable): when Published mid-transaction, A guest partway through checkout keeps the config version they started with. **A rebrand must not change a price or a layout under someone mid-purchase.**
- Flow F22 branch at step 5 (requiresStaff): when The app store build is older than the config, Config is data and the shell is a release. **Anything needing a new shell does not publish** — an app icon change is a store submission, not a config change (ADR-0006).

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-014?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Generate site package, Publish, Validate tenant config, What publishing changes, Simulate.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`, `CMS-103`, `CMS-104`, `CMS-102`, `CMS-015`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`, `TENANT_PUBLISH`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-015` Version History

**See who changed what and go back if it was wrong — by restoring into the draft, reviewing, then publishing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-015 |
| Who uses it | venue staff holding `TENANT_CONFIGURE`, `TENANT_PUBLISH` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listConfigVersions` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `version` (deepLink) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/white-label/version-history` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Absorbed CMS-020 on 28 September (audit R276)**: the Change Log listed the same `listConfigVersions` rows (who published what, when, with which note) and nothing else, so it brought no operation; its entry from the Tenant Workspace (CMS-001) now lands here. **Rollback is restore, then review, then publish — never one click (decided 28 September, audit R139 (b)).** **Restore config version** calls `restoreConfigVersion`, which copies the chosen version into the working draft and publishes nothing. The screen then shows **Diff config version** of the live version against the restored draft (`diffConfigVersion`) as the review, and **Review and publish the restored draft** goes to the Publishing Workflow (CMS-014), where `publishTenantConfig` puts it live with a note.

**From the White Label & CMS process.** Who published what, when and why, and the way back: restore a version into the draft, review the diff, then publish on CMS-014. Never a one-click rollback.

**Fixed on main** (the package already carries these; draw what it says): emptyNoAccess cites only TENANT_CONFIGURE. (CHG-SGU-022).

#### Inputs: what the user enters or picks

**Form: Restore config version** (confirmDialog, opened by *Restore config version*; *Restore into draft* calls `restoreConfigVersion`, *Cancel* sends nothing)

**Restores the chosen version into the working draft and publishes nothing** (decided 28 September, audit R139 (b)). Names the version and says that any unpublished changes in the draft are replaced. Guests keep seeing the live version until the restored draft is reviewed (`diffConfigVersion`) and published on CMS-014.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every config version** (data table, from `listConfigVersions`)

| Shows | Format | Notes |
|---|---|---|
| Published at | 1 Oct 2026, 14:30 | — |
| Published by name | text | — |
| Note | text | — |
| Is current | yes / no (icon or chip) | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |

**The selected config version** (detail panel, from `listConfigVersions`)

| Shows | Format | Notes |
|---|---|---|
| Published at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published by name | text | — |
| Note | text | — |
| Is current | yes / no (icon or chip) | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Content hash | text | — |
| Pending build time changes | list or chips (count when long) | Changes in this version that will not reach guests until the next store release. |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Diff config version (primary button) | `diffConfigVersion` GET `/tenant-config/versions/{version}/diff` | — | ConfigDiff | — | — |
| Restore config version (secondary button) | `restoreConfigVersion` POST `/tenant-config/versions/{version}/restore` | — | TenantConfig | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `TENANT_PUBLISH`; opens confirmDialog first |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Version list**: Newest first; version, published at (GST), by name, note, Current badge, Scheduled for, Needs an app update chips. contentHash and scopePath are not shown. *(source: contracts/satellite/white-label.yaml#/components/schemas/ConfigVersion)*
- **Compare**: diffConfigVersion of the selected version against the draft (or ?against another version), grouped by area, before and after, changeScope tag. *(source: contracts/satellite/white-label.yaml#diffConfigVersion)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Restore into draft**: Confirmation names the version and says unpublished draft changes are replaced and guests still see the live version; then lands on the diff with "Review and publish" to CMS-014. Needs TENANT_PUBLISH. *(source: contracts/satellite/white-label.yaml#restoreConfigVersion; R139; F22 step 6)*

**Data it reads**: `listConfigVersions` (onLoad, Version history)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*
- → `CMS-014` Publishing Workflow: *Review and publish the restored draft*; carries `version`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The version history list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the version history untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No version history yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listConfigVersions` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listConfigVersions` requires, and names it. A user with `TENANT_CONFIGURE` and not `TENANT_PUBLISH` sees the versions with Restore hidden and the reason named, because `restoreConfigVersion` needs `TENANT_PUBLISH`. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Restoring while the draft has unpublished changes**: The dialog lists them (from the diff) before they are overwritten. *(source: contracts/satellite/white-label.yaml#restoreConfigVersion)*
- **Old version with a different app icon**: After restore and publish, the icon still needs an app update; say so. *(source: contracts/satellite/white-label.yaml#/components/schemas/ConfigVersion)*
- **Maintenance or availability**: Not part of any version; the restore leaves them as they are and says so. *(source: contracts/satellite/white-label.yaml#setMaintenanceMode)*

#### Consistency with other screens

- Match `CMS-014`: Same diff component; restore always ends there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
versions:
- version: '14'
  at: 2026-09-30 18:05
  by: Mariam Al Hashimi
  note: Autumn hours
  current: true
- version: '13'
  at: 2026-09-21 10:12
  by: Omar Saeed
  note: Water park map tab
- version: '12'
  at: 2026-09-14 09:40
  by: Mariam Al Hashimi
  note: Launch theme
```

#### Permissions

- `listConfigVersions` → `TENANT_CONFIGURE` (configure) · staff
- `diffConfigVersion` → `TENANT_CONFIGURE` (configure) · staff
- `restoreConfigVersion` → `TENANT_PUBLISH` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listConfigVersions` requires, and names it. A user with `TENANT_CONFIGURE` and not `TENANT_PUBLISH` sees the versions with Restore hidden and the reason named, because `restoreConfigVersion` needs `TENANT_PUBLISH`.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.10.30 | CMS Audit Trail | Marketing & CRM | CONTRACTED | `listConfigVersions` |
| 22.10.10 | Version Management | Marketing & CRM | CONTRACTED | `restoreConfigVersion` |
| 22.10.11 | Rollback & Recovery | Marketing & CRM | CONTRACTED | `restoreConfigVersion` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-015` · status **notStarted** · provenance generated
- Flow F22 *A tenant rebrands their app*, step 6: Rolls back when something is wrong → **Restore, then review, then publish — not one click** (decided 28 September, audit R139 (b)). `restoreConfigVersion` copies the earlier version into the draft without publishing it, and …
- Flow F22 branch at step 6 (recoverable): when Rollback after guests have seen the new brand, Fine for a homepage, awkward for an app icon that is cached on a device. **The two roll back at different speeds** and the interface should say so.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Diff config version, Restore config version.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`, `CMS-014`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`, `TENANT_PUBLISH`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-016` Site Settings

**The values the whole site inherits from, and the venue-wide booking settings each venue may override (decided 29 September, rev 3 CFG-11); the settings of one flow are on CMS-103 (W12).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-016 |
| Who uses it | venue staff holding `SCOPE_VIEW`, `TENANT_CONFIGURE` (1 read, 1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getTenantConfig` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/white-label/site-settings` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**From the White Label & CMS process.** The venue-wide booking presentation every booking screen inherits, at tenant level with a per-venue override: preset, step indicator, card and cart layout, density, hero and embed, seated and timed rules, guest-checkout fields, plus the analytics platforms. The one thing to get right: at venue level each field shows the inherited tenant value and whether this venue overrides it; clearing a field returns to inheritance.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- stepIndicator values (bar, numbered, dots, segmented, breadcrumb, pills, ticks, none) do not match the client's words (bars, dots, counters, step names) or the prototypes (web Bar / Numbered steps / Dots; mobile Bars / … (CHG-SGU-024)
- The mobile prototype offers controls the contract lacks (continue button Bottom bar / Floating pill / Full-width block; date picker Grid / Strip / List; step order Tailored per product / One decision per screen). (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): The layout dumps the whole TenantConfig, and listAnalyticsProviders / setAnalyticsProvider have no component. (CHG-SGU-022); No guest booking screen declares stepIndicator, embedMode, singleEventPage or HeaderConfig. (CHG-SGU-022).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Map the stepIndicator values to labels.** → Drawn default accepted: bar = Bar, numbered = Numbered steps (counter), dots = Dots, breadcrumb = Step names, segmented = Segments, pills = Pills, ticks = Ticks, none = None. *(decided by Chinmay, 2026-10-02; DEC-157 / CHG-NOTE-009)*
- **Staging and production environments per site (asked 20 August).** → Drawn default accepted: Not modelled; the preview link (CMS-006) is the staging view. *(decided by Chinmay, 2026-10-02; DEC-158 / CHG-NOTE-009)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Settings for | select field | — | — | — | — | **Which level is being edited** (decided 29 September, rev 3 CFG-11). *All venues* edits the tenant settings; picking a venue edits that venue's entry in `venueOverrides` and shows beside each field … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Effective for venue | picker: choose an effective for venue | — | — | `getBookingFlowConfig` ?effectiveForVenueId |
| Under | text field | — | — | `listOrgUnits` ?under |
| Level | select | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet · Subject | `listOrgUnits` ?level |
| Include inactive | toggle | off | — | `listOrgUnits` ?includeInactive |

**Form: Save booking flow config** (modal, opened by *Save booking flow config*; *Save booking flow config* calls `setBookingFlowConfig`, *Cancel* sends nothing)

**Collects what `setBookingFlowConfig` sends before it is called.** Nothing in the body is required. Optional: `preset`, `stepIndicator`, `cartLayout`, `cardLayout`, `cardSize`, `seatPicker`, `mapView`, `density`, `embedMode`, `heroBanner`, `searchInBanner`, `singleEventPage`, `quantitiesOnAddOns`, the venue-wide rev 3 booking rules on the panel above, `guestContactFields` (W1), `dateStripDays` (M17-08) and `venueOverrides` (decided 29 September, rev 3 CFG-11). **The body is the tenant settings plus every venue override**: saving a venue's override sends the whole configuration with that venue's row changed. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Preset `preset` | select | optional | Auto | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | — | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. | `setBookingFlowConfig` body |
| Step indicator `stepIndicator` | select | optional | Bar | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | — | — | `setBookingFlowConfig` body |
| Cart layout `cartLayout` | select | optional | Sidebar right | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | — | `floatingIcon` is a round basket button with the item count that opens the cart (decided 29 September, rev 3 REV3-10). | `setBookingFlowConfig` body |
| Cart side in RTL `cartSideInRtl` | segmented control | optional | Keep right | Keep right · Mirror | — | The cart side when the guest reads Arabic or another right-to-left language (decided 29 September, rev 3 REV3-10). | `setBookingFlowConfig` body |
| Card layout `cardLayout` | radio group | optional | Stacked rows | Stacked rows · Split rows · Cards across · Poster cards | — | How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked rows, Split rows, Cards across and Poster … | `setBookingFlowConfig` body |
| Card size `cardSize` | radio group | optional | Compact | Compact · Standard · Large · Extra large | — | Labels Compact, Standard, Large, Extra large (decided 29 September, rev 3 DG-6). | `setBookingFlowConfig` body |
| Seat picker `seatPicker` | radio group | optional | Bowl | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | — | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. | `setBookingFlowConfig` body |
| Map view `mapView` | segmented control | optional | 3D | 2D · 3D | — | — | `setBookingFlowConfig` body |
| Density `density` | segmented control | optional | Compact | Compact · Standard · Roomy | — | Labels Compact, Standard, Roomy, default Compact as the design has it (decided 29 September, rev 3 DG-6). | `setBookingFlowConfig` body |
| Embed mode `embedMode` | segmented control | optional | Full page | Full page · Embedded | — | `embedded` hides the hero banner, event page and venue header, for a flow placed inside the venue's own site. | `setBookingFlowConfig` body |
| Hero banner `heroBanner` | toggle | optional | on | — | — | — | `setBookingFlowConfig` body |
| Search in banner `searchInBanner` | toggle | optional | off | — | — | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). | `setBookingFlowConfig` body |
| Event banner dates `eventBannerDates` | toggle | optional | off | — | — | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. | `setBookingFlowConfig` body |
| Single event page `singleEventPage` | toggle | optional | off | — | — | — | `setBookingFlowConfig` body |
| Quantities on add ons `quantitiesOnAddOns` | toggle | optional | on | — | — | — | `setBookingFlowConfig` body |
| Times per page `timesPerPage` | radio group | optional | 24 | 8 · 12 · 24 · All | — | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many … | `setBookingFlowConfig` body |
| Day part filter `dayPartFilter` | toggle | optional | on | — | — | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). | `setBookingFlowConfig` body |
| Day part boundaries `dayPartBoundaries` | group | optional | — | `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400. | — | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). | `setBookingFlowConfig` body |
| Afternoon starts at `dayPartBoundaries.afternoonStartsAt` | time picker | optional | 12:00 | — | HH:mm, 24-hour | — | `setBookingFlowConfig` body |
| Evening starts at `dayPartBoundaries.eveningStartsAt` | time picker | optional | 17:00 | — | HH:mm, 24-hour | — | `setBookingFlowConfig` body |
| Seat view position `seatViewPosition` | radio group | optional | Bottom | Bottom · Right · Left · Top | — | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). | `setBookingFlowConfig` body |
| Seat time bar `seatTimeBar` | toggle | optional | on | — | — | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or change the date; switching releases the … | `setBookingFlowConfig` body |
| Ticket categories `ticketCategories` | segmented control | optional | Category then subcategory | Category then subcategory · Flat list | — | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one … | `setBookingFlowConfig` body |
| Ticket tags `ticketTags` | toggle | optional | on | — | — | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. | `setBookingFlowConfig` body |
| Card info `cardInfo` | toggle | optional | on | — | — | Extra info on cards (decided 29 September, rev 3 23SEP-6). Shows each ticket type's description, who it is for and what it includes, under its name. | `setBookingFlowConfig` body |
| Concierge mascot `conciergeMascot` | toggle | optional | on | Read only where the `aiConciergeChat` feature is on. | — | The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5). | `setBookingFlowConfig` body |
| Show info only `showInfoOnly` | toggle | optional | on | — | — | Show info-only products (decided 29 September, rev 3 REV3-14). On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its … | `setBookingFlowConfig` body |
| Location switcher `locationSwitcher` | toggle | optional | off | — | — | Location switcher (decided 29 September, rev 3 REV3-18). On, the booking screens carry a "Booking at" bar with Change location, reusing the guest's venue choice (audit R267). | `setBookingFlowConfig` body |
| Guest contact fields `guestContactFields` | multi-select chips | optional | Email | Email · Mobile · Name; at least 1; at most 3; no duplicates; Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.; matchBy`), or 400. | — | What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1). | `setBookingFlowConfig` body |
| Date strip days `dateStripDays` | stepper or slider (days) | optional | 7 | min 3; max 31 | — | The date strip (decided 17 September, M17-08). How many days from today the date step shows as a strip before the calendar icon that opens the full month; later dates are picked … | `setBookingFlowConfig` body |
| Venue overrides `venueOverrides` | repeatable rows | optional | — | at most 200; Per-venue overrides, at most one per venue.; A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. | — | Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. | `setBookingFlowConfig` body |
| Venue `venueOverrides[].venueId` | picker: choose a venue | required | — | At most one override per venue. | shows names, sends the id | One of the tenant's active venues. At most one override per venue. | `setBookingFlowConfig` body |
| Settings `venueOverrides[].settings` | group | required | — | — | — | Every guest booking-flow setting, once. `BookingFlowConfig` is these at tenant level plus `venueOverrides`; a `BookingFlowVenueOverride` carries any subset of them for one venue … | `setBookingFlowConfig` body |
| Preset `venueOverrides[].settings.preset` | select | optional | Auto | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | — | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. | `setBookingFlowConfig` body |
| Step indicator `venueOverrides[].settings.stepIndicator` | select | optional | Bar | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | — | — | `setBookingFlowConfig` body |
| Cart layout `venueOverrides[].settings.cartLayout` | select | optional | Sidebar right | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | — | `floatingIcon` is a round basket button with the item count that opens the cart (decided 29 September, rev 3 REV3-10). | `setBookingFlowConfig` body |
| Cart side in RTL `venueOverrides[].settings.cartSideInRtl` | segmented control | optional | Keep right | Keep right · Mirror | — | The cart side when the guest reads Arabic or another right-to-left language (decided 29 September, rev 3 REV3-10). | `setBookingFlowConfig` body |
| Card layout `venueOverrides[].settings.cardLayout` | radio group | optional | Stacked rows | Stacked rows · Split rows · Cards across · Poster cards | — | How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked rows, Split rows, Cards across and Poster … | `setBookingFlowConfig` body |
| Card size `venueOverrides[].settings.cardSize` | radio group | optional | Compact | Compact · Standard · Large · Extra large | — | Labels Compact, Standard, Large, Extra large (decided 29 September, rev 3 DG-6). | `setBookingFlowConfig` body |
| Seat picker `venueOverrides[].settings.seatPicker` | radio group | optional | Bowl | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | — | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. | `setBookingFlowConfig` body |
| Map view `venueOverrides[].settings.mapView` | segmented control | optional | 3D | 2D · 3D | — | — | `setBookingFlowConfig` body |
| Density `venueOverrides[].settings.density` | segmented control | optional | Compact | Compact · Standard · Roomy | — | Labels Compact, Standard, Roomy, default Compact as the design has it (decided 29 September, rev 3 DG-6). | `setBookingFlowConfig` body |
| Embed mode `venueOverrides[].settings.embedMode` | segmented control | optional | Full page | Full page · Embedded | — | `embedded` hides the hero banner, event page and venue header, for a flow placed inside the venue's own site. | `setBookingFlowConfig` body |
| Hero banner `venueOverrides[].settings.heroBanner` | toggle | optional | on | — | — | — | `setBookingFlowConfig` body |
| Search in banner `venueOverrides[].settings.searchInBanner` | toggle | optional | off | — | — | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). | `setBookingFlowConfig` body |
| … 16 more | | | | | | the rest are in `schemas.json` | `setBookingFlowConfig` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Save analytics platform** (modal, opened by *Save analytics platform*; *Save analytics platform* calls `setAnalyticsProvider`, *Cancel* sends nothing)

The platform, its measurement id and whether it is on; it loads only with the visitor's analytics or marketing consent.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setAnalyticsProvider` body |
| Provider `provider` | select | required | — | Google analytics4 · Google tag manager · Adobe analytics · Meta pixel · Matomo · Other | — | — | `setAnalyticsProvider` body |
| Provider label `providerLabel` | text field | optional | — | max length 100 | — | The name, when `provider` is `other`. | `setAnalyticsProvider` body |
| Measurement `measurementId` | text field | required | — | max length 100 | — | What the tag or SDK reports to (GA4 `G-...`, Tag Manager `GTM-...`, a pixel id). | `setAnalyticsProvider` body |
| Surfaces `surfaces` | multi-select chips | required | — | Guest web · Guest app; at least 1 | — | — | `setAnalyticsProvider` body |
| Consent category `consentCategory` | radio group | required | Analytics | Functional · Analytics · Personalisation · Marketing | — | The cookie category the visitor must grant before this provider loads (marketing-crm `CookieCategory`). | `setAnalyticsProvider` body |
| Is enabled `isEnabled` | toggle | required | on | — | — | — | `setAnalyticsProvider` body |
| Reporting property `reportingPropertyId` | text field | optional | — | max length 100 | — | The property `getStorefrontInsights` asks the reporting API about (a GA4 property id). | `setAnalyticsProvider` body |
| Reporting credential ref `reportingCredentialRef` | text field | optional | — | max length 200 | — | The vault reference of the reporting credential. Accepted, never returned. | `setAnalyticsProvider` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 A `measurementId` that does not match the provider's format, or a `venueId` not among the tenant's active venues

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Settings for**: All venues (tenant) or one venue; sends effectiveForVenueId to show the resolved values. Overridden fields carry an "Overrides tenant" chip and a Reset. *(source: DI-1063; contracts/satellite/white-label.yaml#/components/schemas/BookingFlowVenueOverride)*
- **preset**: Auto (by venue type) / Ticket box / Play centre / Venue site / Marketplace / Single event / Season / Custom; picking one fills the fields below, which stay editable (then Custom). *(source: DI-1065)*
- **stepIndicator**: Thumbnails of Bar, Numbered, Dots, Segmented, Breadcrumb (step names), Pills, Ticks, None; default Bar. *(source: DI-1093; DI-1070)*
- **cardLayout, cardSize, density**: Stacked rows (default) / Split rows / Cards across / Poster cards; Compact (default) / Standard / Large / Extra large; Compact (default) / Standard / Roomy. Thumbnails, not words. *(source: DI-1040)*
- **cartLayout, cartSideInRtl**: Six cart thumbnails (default sidebar right; floating basket icon with count); Arabic cart side Keep right (default) / Mirror. *(source: DI-1051)*
- **heroBanner, searchInBanner, eventBannerDates, embedMode, singleEventPage**: Hero on (default) for venues without their own site; search off; event dates in banner off; Full page / Embedded (embedded keeps the powered-by strip and progress). *(source: DI-945; DI-1033; DI-431; sources/designs/guest-rev3-30-september/TICVAI Engine Controls Manual.dc.html)*
- **timesPerPage, dayPartFilter, dayPartBoundaries**: 8 / 12 / 24 (default) / All; chips on; afternoon starts 12:00 and evening 17:00 by default, afternoon before evening (400). *(source: DI-1041)*
- **dateStripDays**: Stepper 3-31, default 7. *(source: DI-920)*
- **guestContactFields**: Email only (default) / Email + name / Email + mobile + name; must include the contact the code is sent to (400). Shown only when the guestCheckout feature is on. *(source: MoM 29 Sep 1 W1; contracts/satellite/white-label.yaml#/components/schemas/BookingFlowSettings)*
- **analytics providers**: Provider, measurement id (G-..., GTM-..., pixel id; format checked, 422), surfaces web / app, consent category (Analytics default; never Strictly necessary), tenant-wide or per venue, enabled; reporting credential write-only. *(source: contracts/satellite/white-label.yaml#setAnalyticsProvider; DI-393)*

#### Outputs: what the screen shows and produces

**Shown**

**The booking flow config** (detail panel, from `getBookingFlowConfig`): **Venue-wide booking settings only (decided 29 September, W12).** The settings that belong to one flow (`performanceReveal`, `signInAt`, `seatEventDateMode`, `extrasStep`, `quickTour`, the flow's consent questions) moved to each flow on CMS-103, and `categoryDisplay` is gone (W7, superseding 23SEP-18: `cardLayout` carries rows or grid). Here: `timesPerPage` and the day-part chips (REV3-1) …

| Shows | Format | Notes |
|---|---|---|
| Cart layout | chip: Sidebar right, Sidebar left, Slide in right, Slide up bottom, Single column … | `floatingIcon` is a round basket button with the item count that opens the cart (decided 29 September, rev 3 REV3-10). |
| Card layout | chip: Stacked rows, Split rows, Cards across, Poster cards | How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked … |
| Density | chip: Compact, Standard, Roomy | Labels Compact, Standard, Roomy, default Compact as the design has it (decided 29 September, rev 3 DG-6). |
| Cart side in RTL | chip: Keep right, Mirror | The cart side when the guest reads Arabic or another right-to-left language (decided 29 September, rev 3 REV3-10). |
| Event banner dates | yes / no (icon or chip) | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Times per page | chip: 8, 12, 24, All | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 … |
| Seat view position | chip: Bottom, Right, Left, Top | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). |
| Seat time bar | yes / no (icon or chip) | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or … |

**Venues that differ from the tenant** (data table, from `getBookingFlowConfig`): **One row per venue that overrides anything** (decided 29 September, rev 3 CFG-11). The editor sets only the fields that differ; a field left empty inherits the tenant value, and clearing one removes it from the override. A venue that is not one of the tenant's active venues, or a second row for the same venue, is refused `400` and the row is marked. An override kept for a closed venue is shown …

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | One of the tenant's active venues. At most one override per venue. |
| Settings | grouped details | Every guest booking-flow setting, once. `BookingFlowConfig` is these at tenant level plus `venueOverrides`; a `BookingFlowVenueOverride` … |

**Analytics platforms** (data table, from `listAnalyticsProviders`): The platforms the storefront and app report to (GA4, Meta pixel and the like), each with its id and on/off.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Provider | chip: Google analytics4, Google tag manager, Adobe analytics, Meta pixel, Matomo, Other | — |
| Provider label | text | The name, when `provider` is `other`. |
| Measurement | text | What the tag or SDK reports to (GA4 `G-...`, Tag Manager `GTM-...`, a pixel id). |
| Surfaces | list or chips (count when long) | — |
| Consent category | chip: Functional, Analytics, Personalisation, Marketing | The cookie category the visitor must grant before this provider loads (marketing-crm `CookieCategory`). |
| Is enabled | yes / no (icon or chip) | — |
| Reporting property | text | The property `getStorefrontInsights` asks the reporting API about (a GA4 property id). |
| Reporting credential ref | text | The vault reference of the reporting credential. Accepted, never returned. |
| Has reporting credential | yes / no (icon or chip) | Whether a reporting credential is held, since the reference itself is never returned. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save analytics platform (primary button) | `setAnalyticsProvider` PUT `/tenant-config/analytics-providers` | StorefrontAnalyticsProvider | StorefrontAnalyticsProvider | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 A `measurementId` that does not match the provider's format, or a `venueId` not among the tenant's active venues | opens modal first |
| Save booking flow config (primary button) | `setBookingFlowConfig` PUT `/tenant-config/booking-flow` | BookingFlowConfig | BookingFlowConfig | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Mini preview per setting**: Every option shows the guest result (a card, the cart, the step indicator) because the client wants every option to visibly change something. *(source: DI-988)*
- **Venues that differ**: One row per venue override listing only the changed fields; a closed venue's override greyed with "No effect". *(source: DI-1063; contracts/satellite/white-label.yaml#/components/schemas/BookingFlowConfig)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Save booking settings**: Sends the tenant settings plus every override (the whole BookingFlowConfig) to the draft; guests see it after publish. *(source: contracts/satellite/white-label.yaml#setBookingFlowConfig)*
- **Save analytics platform**: Upsert keyed on venue and provider; effective with the publish. *(source: contracts/satellite/white-label.yaml#setAnalyticsProvider)*

**Data it reads**: `getBookingFlowConfig` (onLoad, How the guest booking flow looks and steps); `listOrgUnits` (onLoad, The tenant's venues, for the per-venue override picker (rev …); `listAnalyticsProviders` (onLoad, Connected analytics platforms)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*
- → `CMS-017` Domain & Certificate: *Domain & Certificate*
- → `CMS-018` Consent & Legal: *Consent & Legal*
- → `CMS-103` Booking Flows: *Booking flows*
- → `CMS-101` Help Me Choose: *Help me choose*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The site settings, read by `getTenantConfig`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the site settings untouched. |
| Empty, no results (`?state=emptyNoResults`) | A venue picked in Settings for with no override shows the tenant settings it inherits, labelled as inherited, rather than an empty form (rev 3 CFG-11). |
| Empty, first run (`?state=emptyFirstRun`) | No site settings yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getBookingFlowConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A `measurementId` that does not match the provider's format, or a `venueId` not among the tenant's active venues |

#### Edge cases to draw

- **Two admins edit different venues' overrides at once**: The body is the whole configuration, so the second save overwrites the first; warn on load when the draft changed since opening. *(source: contracts/satellite/white-label.yaml#setBookingFlowConfig)*
- **Tenant with one venue**: Hide Settings for and the location switcher (no effect). *(source: contracts/satellite/white-label.yaml#/components/schemas/BookingFlowSettings)*

#### Consistency with other screens

- Match `CMS-103`: Flow-level settings (performance reveal, sign-in point, extras, quick tour, consent questions) are there, not here; link both ways.
- Match `WEB-005`: The step indicator and cart styles are drawn there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tenant:
  preset: venueSite
  stepIndicator: numbered
  cardLayout: cardsAcross
  cardSize: compact
  cartLayout: sidebarRight
  dateStripDays: 7
  guestContactFields:
  - email
  - mobile
  - name
override:
  venue: Kids Club Mirdif (كيدز كلوب مردف)
  settings:
    cardLayout: posterCards
    cartLayout: floatingIcon
    timesPerPage: '12'
analytics:
  provider: googleAnalytics4
  measurementId: G-7Q2K9XW4LM
  surfaces:
  - guestWeb
  - guestApp
  consentCategory: analytics
```

#### Permissions

- `getBookingFlowConfig` → `TENANT_CONFIGURE` (configure) · staff
- `setBookingFlowConfig` → `TENANT_CONFIGURE` (configure) · staff
- `listOrgUnits` → `SCOPE_VIEW` (read) · staff
- `listAnalyticsProviders` → `TENANT_CONFIGURE` (configure) · staff, guest
- `setAnalyticsProvider` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getBookingFlowConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.41 | Venue-Specific Policies - System shall support venue-specific access policies. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 3.3.43 | Policy Inheritance - System shall support inheritance of policies across organizational structures. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 7.1.13 | The system shall support permission assignment at company, department, venue, park, attraction, facility, event, sales channel, POS terminal, and product levels. | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.27 | The system shall support management of companies, business units, departments, parks, venues, attractions, facilities, cost centers, and reporting structures. | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.37 | Allow administrators to restrict access by venue, park, facility, attraction, sales channel, POS terminal, country, region, IP address and network range. Policies should support allow/deny logic and … | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.52 | Support policies spanning multiple parks, venues, attractions, departments and business units while maintaining centralized governance. | F&B POS | CONTRACTED | `listOrgUnits` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Guest date picking shows a strip of the next seven days (venue setting dateStripDays, default 7, range 3-31) with a calendar icon that opens the full month for later dates. *(agreed · MoM 17 Sep 2026, M17-08 · DI-920)*
- CMS manages multiple sites/venues: branding, colour palette including custom hex codes, fonts, Google Analytics site IDs, production/staging environments. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-393)*
- One client can run multiple branded sites from the same setup, e.g. two brands sharing a footer but with distinct headers and hero banners. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-110)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Booking settings preset (`bookingFlow.preset`) | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | Auto | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. |
| Step indicator (`bookingFlow.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | GST-007, GST-008, GST-009, GST-041, GST-051, WEB-005, WEB-006, WEB-007 … (13) | the step indicator above every booking step: bar, numbered, dots, segmented, breadcrumb, pills, ticks, or none |
| Cart layout (`bookingFlow.cartLayout`) | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | Sidebar right | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | where the cart sits: a sidebar right or left, sliding in, sliding up, a single column, or a floating basket icon |
| Cart side in RTL (`bookingFlow.cartSideInRtl`) | Keep right · Mirror | Keep right | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | the cart's side in Arabic: kept right, or mirrored left |
| Card layout (`bookingFlow.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | GST-002, GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-002, WEB-005 … (14) | ticket and product cards: stacked rows, split rows, cards across, or poster cards |
| Card size (`bookingFlow.cardSize`) | Compact · Standard · Large · Extra large | Compact | GST-007, GST-008, GST-009, GST-041, WEB-002, WEB-005, WEB-006, WEB-007 … (12) | card size: compact, standard, large, extra large |
| Seat picker (`bookingFlow.seatPicker`) | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | Bowl | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. |
| Map view (`bookingFlow.mapView`) | 2D · 3D | 3D | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Booking settings density (`bookingFlow.density`) | Compact · Standard · Roomy | Compact | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | spacing of the booking screens: compact, standard, roomy |
| Embed mode (`bookingFlow.embedMode`) | Full page · Embedded | Full page | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | full page, or embedded in the venue's own site (no hero, event page or venue header) |
| Hero banner (`bookingFlow.heroBanner`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | the hero banner at the top of the booking pages |
| Search in banner (`bookingFlow.searchInBanner`) | — | off | GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-005, WEB-006, WEB-007 … (12) | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). |
| Event banner dates (`bookingFlow.eventBannerDates`) | — | off | GST-004, GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-004, WEB-005 … (14) | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Single event page (`bookingFlow.singleEventPage`) | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Quantities on add ons (`bookingFlow.quantitiesOnAddOns`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Times per page (`bookingFlow.timesPerPage`) | 8 · 12 · 24 · All | 24 | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` … |
| Day part filter (`bookingFlow.dayPartFilter`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). |
| Day part boundaries (`bookingFlow.dayPartBoundaries`) | `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). |
| Day part boundaries: afternoon starts at (`bookingFlow.dayPartBoundaries.afternoonStartsAt`) | HH:mm, 24-hour | 12:00 | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Day part boundaries: evening starts at (`bookingFlow.dayPartBoundaries.eveningStartsAt`) | HH:mm, 24-hour | 17:00 | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Seat view position (`bookingFlow.seatViewPosition`) | Bottom · Right · Left · Top | Bottom | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). |
| Seat time bar (`bookingFlow.seatTimeBar`) | — | on | GST-007, GST-008, GST-009, GST-041, GST-049, WEB-005, WEB-006, WEB-007 … (12) | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one. |
| Ticket categories (`bookingFlow.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | GST-002, GST-003, GST-007, GST-008, GST-009, GST-041, WEB-002, WEB-005 … (14) | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |
| Ticket tags (`bookingFlow.ticketTags`) | — | on | GST-004, GST-007, GST-008, GST-009, GST-013, GST-041, WEB-004, WEB-005 … (14) | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. |
| Card info (`bookingFlow.cardInfo`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Extra info on cards (decided 29 September, rev 3 23SEP-6). Shows each ticket type's description, who it is for and what it includes, under its name. |
| Concierge mascot (`bookingFlow.conciergeMascot`) | Read only where the `aiConciergeChat` feature is on. | on | GST-007, GST-008, GST-009, GST-031, GST-041, WEB-005, WEB-006, WEB-007 … (13) | The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5). |
| Show info only (`bookingFlow.showInfoOnly`) | — | on | GST-003, GST-007, GST-008, GST-009, GST-041, GST-063, WEB-002, WEB-003 … (15) | Show info-only products (decided 29 September, rev 3 REV3-14). On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it. |
| Location switcher (`bookingFlow.locationSwitcher`) | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Location switcher (decided 29 September, rev 3 REV3-18). On, the booking screens carry a "Booking at" bar with Change location, reusing the guest's venue choice (audit R267). |
| Guest contact fields (`bookingFlow.guestContactFields`) | Email · Mobile · Name; at least 1; at most 3; no duplicates; Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.; matchBy`), or 400. | Email | GST-007, GST-008, GST-009, GST-041, GST-042, WEB-005, WEB-006, WEB-007 … (13) | What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1). |
| Date strip days (`bookingFlow.dateStripDays`) | min 3; max 31 | 7 | GST-007, GST-008, GST-009, GST-041, WEB-004, WEB-005, WEB-006, WEB-007 … (12) | The date strip (decided 17 September, M17-08). How many days from today the date step shows as a strip before the calendar icon that opens the full month; later dates are picked from the calendar. |
| Venue overrides (`bookingFlow.venueOverrides`) | at most 200; Per-venue overrides, at most one per venue.; A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. | — | GST-001, GST-002, GST-003, GST-007, GST-008, GST-009, GST-041, GST-049 … (17) | Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. |
| Venue overrides: venue (`bookingFlow.venueOverrides[].venueId`) | At most one override per venue. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | One of the tenant's active venues. At most one override per venue. |
| Venue overrides: settings (`bookingFlow.venueOverrides[].settings`) | — | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Every guest booking-flow setting, once. `BookingFlowConfig` is these at tenant level plus `venueOverrides`; a `BookingFlowVenueOverride` carries any subset of them for one venue (decided 29 September, rev 3 CFG-11). |
| Settings: preset (`bookingFlow.venueOverrides[].settings.preset`) | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | Auto | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. |
| Settings: step indicator (`bookingFlow.venueOverrides[].settings.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | GST-007, GST-008, GST-009, GST-041, GST-051, WEB-005, WEB-006, WEB-007 … (13) | — |
| Settings: cart layout (`bookingFlow.venueOverrides[].settings.cartLayout`) | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | Sidebar right | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | `floatingIcon` is a round basket button with the item count that opens the cart (decided 29 September, rev 3 REV3-10). |
| Settings: cart side in RTL (`bookingFlow.venueOverrides[].settings.cartSideInRtl`) | Keep right · Mirror | Keep right | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The cart side when the guest reads Arabic or another right-to-left language (decided 29 September, rev 3 REV3-10). |
| Settings: card layout (`bookingFlow.venueOverrides[].settings.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | GST-002, GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-002, WEB-005 … (14) | How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked rows, Split rows, Cards across and Poster cards. |
| Settings: card size (`bookingFlow.venueOverrides[].settings.cardSize`) | Compact · Standard · Large · Extra large | Compact | GST-007, GST-008, GST-009, GST-041, WEB-002, WEB-005, WEB-006, WEB-007 … (12) | Labels Compact, Standard, Large, Extra large (decided 29 September, rev 3 DG-6). |
| Settings: seat picker (`bookingFlow.venueOverrides[].settings.seatPicker`) | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | Bowl | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. |
| Settings: map view (`bookingFlow.venueOverrides[].settings.mapView`) | 2D · 3D | 3D | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Settings: density (`bookingFlow.venueOverrides[].settings.density`) | Compact · Standard · Roomy | Compact | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Labels Compact, Standard, Roomy, default Compact as the design has it (decided 29 September, rev 3 DG-6). |
| Settings: embed mode (`bookingFlow.venueOverrides[].settings.embedMode`) | Full page · Embedded | Full page | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | `embedded` hides the hero banner, event page and venue header, for a flow placed inside the venue's own site. |
| Settings: hero banner (`bookingFlow.venueOverrides[].settings.heroBanner`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Settings: search in banner (`bookingFlow.venueOverrides[].settings.searchInBanner`) | — | off | GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-005, WEB-006, WEB-007 … (12) | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). |
| Settings: event banner dates (`bookingFlow.venueOverrides[].settings.eventBannerDates`) | — | off | GST-004, GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-004, WEB-005 … (14) | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Settings: single event page (`bookingFlow.venueOverrides[].settings.singleEventPage`) | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Settings: quantities on add ons (`bookingFlow.venueOverrides[].settings.quantitiesOnAddOns`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Settings: times per page (`bookingFlow.venueOverrides[].settings.timesPerPage`) | 8 · 12 · 24 · All | 24 | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` … |
| Settings: day part filter (`bookingFlow.venueOverrides[].settings.dayPartFilter`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). |
| Settings: day part boundaries (`bookingFlow.venueOverrides[].settings.dayPartBoundaries`) | `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). |
| Settings: seat view position (`bookingFlow.venueOverrides[].settings.seatViewPosition`) | Bottom · Right · Left · Top | Bottom | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). |
| Settings: seat time bar (`bookingFlow.venueOverrides[].settings.seatTimeBar`) | — | on | GST-007, GST-008, GST-009, GST-041, GST-049, WEB-005, WEB-006, WEB-007 … (12) | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one. |
| Settings: ticket categories (`bookingFlow.venueOverrides[].settings.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | GST-002, GST-003, GST-007, GST-008, GST-009, GST-041, WEB-002, WEB-005 … (14) | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |
| Settings: ticket tags (`bookingFlow.venueOverrides[].settings.ticketTags`) | — | on | GST-004, GST-007, GST-008, GST-009, GST-013, GST-041, WEB-004, WEB-005 … (14) | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. |
| Settings: card info (`bookingFlow.venueOverrides[].settings.cardInfo`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Extra info on cards (decided 29 September, rev 3 23SEP-6). Shows each ticket type's description, who it is for and what it includes, under its name. |
| Settings: concierge mascot (`bookingFlow.venueOverrides[].settings.conciergeMascot`) | Read only where the `aiConciergeChat` feature is on. | on | GST-007, GST-008, GST-009, GST-031, GST-041, WEB-005, WEB-006, WEB-007 … (13) | The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5). |
| Settings: show info only (`bookingFlow.venueOverrides[].settings.showInfoOnly`) | — | on | GST-003, GST-007, GST-008, GST-009, GST-041, GST-063, WEB-002, WEB-003 … (15) | Show info-only products (decided 29 September, rev 3 REV3-14). On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it. |
| Settings: location switcher (`bookingFlow.venueOverrides[].settings.locationSwitcher`) | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Location switcher (decided 29 September, rev 3 REV3-18). On, the booking screens carry a "Booking at" bar with Change location, reusing the guest's venue choice (audit R267). |
| Settings: guest contact fields (`bookingFlow.venueOverrides[].settings.guestContactFields`) | Email · Mobile · Name; at least 1; at most 3; no duplicates; Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.; matchBy`), or 400. | Email | GST-007, GST-008, GST-009, GST-041, GST-042, WEB-005, WEB-006, WEB-007 … (13) | What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1). |
| … 10 more | | | | `WHITE-LABEL.md` |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-016` · status **notStarted** · provenance generated
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (71), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-016?state=<state>`: loading, error, emptyNoResults, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save analytics platform, Save booking flow config.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`, `CMS-017`, `CMS-018`, `CMS-103`, `CMS-101`.
- [ ] Every gated control is gated: `SCOPE_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-017` Domain & Certificate

**Point the tenant’s own domain at their site.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-017 |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listCustomDomains` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `domainId` (navigation) · cold entry: **Verification and release act on one domain**, taken from the row. A release issued against a domain nobody can see is a site going dark with no record of who … |
| Route | `/white-label/domain-certificate` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**From the White Label & CMS process.** Point the tenant's own domain at its guest web (or app links, partner or developer portal): claim, publish the DNS record shown, and let the platform verify and issue the certificate. The screen is opened when something is wrong, so the status and the exact record to publish matter most.

**Fixed on main** (the package already carries these; draw what it says): The table shows verificationToken but not verificationRecord. (CHG-SGU-012); emptyFirstRun reads "Not found — it may have been deleted or moved out of scope". (CHG-SGU-012); Nothing in the contract returns the tenant's default TICVAI subdomain. (CHG-SGU-012).

#### Inputs: what the user enters or picks

**Form: Claim custom domain** (modal, opened by *Claim custom domain*; *Claim custom domain* calls `claimCustomDomain`, *Cancel* sends nothing)

**Collects what `claimCustomDomain` sends before it is called.** Required: `hostname`, `kind`. Optional: `verificationMethod`. Dismissing sends nothing; the screen behind is unchanged. A CNAME (e.g. tickets.venue.com) straight to the Front Door endpoint, validated by TXT `_dnsauth`, with a managed certificate; a delegated subdomain is an option and the apex only on request (DEC-547) (CHG-SGU-012).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Hostname `hostname` | text field | required | — | — | — | — | `claimCustomDomain` body |
| Kind `kind` | radio group | required | — | Guest web · Guest app · Partner portal · Developer portal | — | — | `claimCustomDomain` body |
| Verification method `verificationMethod` | segmented control | optional | Dns txt | Dns txt · Cname · Http file | — | — | `claimCustomDomain` body |

Errors to draw in the form: 409 Already claimed. Named as unavailable rather than attributed.

**Form: Make primary** (confirmDialog, opened by *Make primary*; *Make primary* calls `setPrimaryDomain`, *Cancel* sends nothing)

Names the domain that becomes primary and the ones that will redirect to it.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The domain is not `active` (`domain-not-active`).

**Form: New validation token** (confirmDialog, opened by *New validation token*; *New validation token* calls `regenerateDomainToken`, *Cancel* sends nothing)

The old TXT record stops working; publish the new one shown next.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The domain is `revoked` (`domain-revoked`); claim it again instead.

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **hostname**: A fully qualified host such as tickets.coastalaqua.ae (lowercase, no scheme, no path). *(source: contracts/satellite/white-label.yaml#claimCustomDomain)*
- **kind**: Guest website / Guest app links / Partner portal / Developer portal. *(source: contracts/satellite/white-label.yaml#/components/schemas/CustomDomain)*
- **verificationMethod**: DNS TXT (default) / CNAME / HTTP file, with one line on when to use each. *(source: contracts/satellite/white-label.yaml#claimCustomDomain)*

#### Outputs: what the screen shows and produces

**Shown**

**Your TICVAI address** (banner, from `getPlatformSubdomain`): venue.<cell>.ticvai.app, always working, shown above the custom domains; small tenants run on it and share links use it (DI-283).

| Shows | Format | Notes |
|---|---|---|
| Hostname | text | e.g. `aquaventure.ae.ticvai.app`. |
| Cell | text | — |
| Certificate | chip: Wildcard | — |
| Is primary | yes / no (icon or chip) | True while no custom domain is primary. |

**Every custom domain** (data table, from `listCustomDomains`)

| Shows | Format | Notes |
|---|---|---|
| Hostname | text | — |
| Kind | chip: Guest web, Guest app, Partner portal, Developer portal | — |
| Status | chip: Pending, Verifying, Verified, Issuing, Active, Failed… | — |
| Routing | chip: Cname, Delegated subdomain, Apex | How the hostname reaches TICVAI (Chinmay, 2 October: "subdomain plus CNAME"; CHG-CSA-043). |
| Revalidation | chip: None, Pending revalidation, Timed out | The two waits CMS-017 shows beside `status` (CHG-CSA-043). `pendingRevalidation`: an `active` domain whose validation must be renewed (the … |
| Is primary | yes / no (icon or chip) | The tenant's primary domain for its `kind`; the others redirect to it (`setPrimaryDomain`). |
| Certificate expires at | 1 Oct 2026, 14:30 | Renewal is a job, not a reminder. A certificate that expires on a Saturday takes a tenant's storefront down, and nobody reads a reminder … |
| Last checked at | 1 Oct 2026, 14:30 | — |
| Failure reason | text | — |

**The selected custom domain** (detail panel, from `listCustomDomains`): **The records to publish** (`dnsRecords`: TXT `_dnsauth`, CNAME to the Front Door endpoint, CAA or NS, each with its observed value and status, with copy buttons); pending revalidation and timed-out states; a takeover warning when the CNAME no longer points at TICVAI (`cnameLost`); per-domain readiness (UAE Pass redirect, Apple Pay domain, app links) (decided by Chinmay, 2 October 2026; DEC-547 …

| Shows | Format | Notes |
|---|---|---|
| Hostname | text | — |
| Dns records | list or chips (count when long) | Every record the tenant must publish, with what is observed now (CHG-CSA-043): the TXT `_dnsauth` record, the CNAME, and CAA or NS where … |
| Verification record | grouped details | The record the tenant must publish, which `claimCustomDomain` promises and the claim had nowhere to hold. |
| Status | chip: Pending, Verifying, Verified, Issuing, Active, Failed… | — |
| Revalidation | chip: None, Pending revalidation, Timed out | The two waits CMS-017 shows beside `status` (CHG-CSA-043). `pendingRevalidation`: an `active` domain whose validation must be renewed (the … |
| Cname lost | yes / no (icon or chip) | Takeover warning (CHG-CSA-043). True when a scheduled check finds that an `active` or released hostname's CNAME still points at TICVAI with … |
| Readiness | grouped details | Per-domain setup a guest needs (CHG-CSA-043): the UAE Pass redirect URI registered for this hostname, the Apple Pay merchant domain … |
| Failure reason | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Claim custom domain (primary button) | `claimCustomDomain` POST `/tenant-domains` | inline | CustomDomain | 409 Already claimed. Named as unavailable rather than attributed. | opens modal first |
| Verify custom domain (secondary button) | `verifyCustomDomain` POST `/tenant-domains/{domainId}/verify` | — | CustomDomain | 409 The hostname is already routed to another tenant (`hostname-taken`, from tenancy `setTenantDomainMapping`, SD-021); nothing was verified or issued. | — |
| Release custom domain (secondary button) | `relinquishCustomDomain` DELETE `/tenant-domains/{domainId}` | — | — | 409 The only active domain for a live app. Refused, naming what would break. | — |
| Make primary (secondary button) | `setPrimaryDomain` POST `/tenant-domains/{domainId}/primary` | — | CustomDomain | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The domain is not `active` (`domain-not-active`). | opens confirmDialog first |
| New validation token (secondary button) | `regenerateDomainToken` POST `/tenant-domains/{domainId}/token` | — | CustomDomain | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The domain is `revoked` (`domain-revoked`); claim it again instead. | opens confirmDialog first |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Record to publish**: verificationRecord type, name and value, each with a copy button, exactly as the DNS provider needs them. *(source: contracts/satellite/white-label.yaml#/components/schemas/CustomDomain)*
- **Status**: Pending, Verifying, Verified, Issuing certificate, Active, Failed (with failureReason), Expired, Revoked; last checked time; certificate expiry date, amber within 30 days. *(source: contracts/satellite/white-label.yaml#listCustomDomains; contracts/satellite/white-label.yaml#/components/schemas/CustomDomain)*
- **Default address**: The tenant's TICVAI subdomain, always working, shown above the custom domains. *(source: DI-283)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Claim**: 201 with the record; 409 "This domain is not available" without saying who holds it. *(source: contracts/satellite/white-label.yaml#claimCustomDomain)*
- **Check now**: Verification is retried by a job; the button only triggers an early check and says DNS can take hours. *(source: contracts/satellite/white-label.yaml#verifyCustomDomain)*
- **Release**: Refused 409 while it is the only active domain for a published app, naming what would break; otherwise unroutes at once. *(source: contracts/satellite/white-label.yaml#relinquishCustomDomain; R096)*

**Data it reads**: `listCustomDomains` (onLoad, Domains claimed, and their state); `getPlatformSubdomain` (onLoad, The tenant's platform subdomain (DEC-547))

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Detail loads |
| Error (`?state=error`) | Could not load |
| Empty, first run (`?state=emptyFirstRun`) | No custom domain yet: "Your site is at venue.<cell>.ticvai.app", with Claim custom domain. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCustomDomains` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listCustomDomains` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already claimed. Named as unavailable rather than attributed.; 409 The domain is `revoked` (`domain-revoked`); claim it again instead.; 409 The domain is not `active` (`domain-not-active`).; 409 The hostname is already routed to another tenant (`hostname-taken`, from tenancy `setTenantDomainMapping`, SD-021); nothing was verified or issued. |

#### Edge cases to draw

- **Hostname already routed to another tenant at verify**: 409 hostname-taken; "This domain is in use elsewhere. Contact support." *(source: contracts/satellite/white-label.yaml#verifyCustomDomain)*
- **Certificate renewal fails on a weekend**: Renewal is a job; a failed renewal shows Failed with the reason and the expiry countdown. *(source: contracts/satellite/white-label.yaml#/components/schemas/CustomDomain)*

#### Consistency with other screens

- Match `ADM-017`: Same list and actions for platform staff through a grant.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
default: coastal-leisure.ticvai.com
domains:
- hostname: tickets.coastalaqua.ae
  kind: guestWeb
  status: active
  certificateExpiresAt: 2026-12-28
- hostname: book.summitpeaks.ae
  kind: guestWeb
  status: verifying
  record:
    type: TXT
    name: _ticvai-verify.book.summitpeaks.ae
    value: ticvai-site-verification=4f9c2e81b7
```

#### Permissions

- `listCustomDomains` → `TENANT_CONFIGURE` (configure) · staff
- `claimCustomDomain` → `TENANT_CONFIGURE` (configure) · staff
- `verifyCustomDomain` → `TENANT_CONFIGURE` (configure) · staff
- `relinquishCustomDomain` → `TENANT_CONFIGURE` (configure) · staff
- `getPlatformSubdomain` → `TENANT_CONFIGURE` (configure) · staff
- `setPrimaryDomain` → `TENANT_CONFIGURE` (configure) · staff
- `regenerateDomainToken` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listCustomDomains` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Guest web hosting: small tenants run under a subdomain/subpath of the TICVAI domain; larger clients get a dedicated URL on their own domain. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-283)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Custom domain hostname (`domains.hostname`) | — | — | every website screen | — |
| Custom domain kind (`domains.kind`) | Guest web · Guest app · Partner portal · Developer portal | — | every website screen | — |
| Verification method (`domains.verificationMethod`) | Dns txt · Cname · Http file | Dns txt | every website screen | — |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-017` · status **notStarted** · provenance generated
- Flow F103 *A tenant claims a domain and gets a certificate*, step 1: The tenant claims the hostname for an app (guest web, guest app links, partner or developer portal). → **Claiming is not owning.** The claim answers with every record to publish (`dnsRecords`): the TXT `_dnsauth` validation record and the CNAME to the Front Door endpoint (decided 2 October 2026 …
- Flow F103 *A tenant claims a domain and gets a certificate*, step 2: The tenant publishes the records at their DNS provider and the domain is verified. → **Retried by a job, not by the tenant.** The records list shows each record with the value observed now and its status; verification routes the hostname (tenancy `setTenantDomainMapping`) and Front …
- Flow F103 *A tenant claims a domain and gets a certificate*, step 3: The domain is live; the tenant checks its readiness and makes it the primary domain. → **A live domain is not a ready one.** Per-domain readiness shows the UAE Pass redirect, the Apple Pay merchant domain and the app links (`CustomDomain.readiness`). The primary domain for each kind …
- Flow F103 *A tenant claims a domain and gets a certificate*, step 4: Later, the tenant gives a domain up. → **The takeover warning is in the confirmation** (DEC-547): remove the CNAME and the TXT record from your DNS, because a record left pointing at TICVAI could be claimed by somebody else. Releasing …
- Flow F103 branch at step 1 (requiresStaff): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.
- Flow F103 branch at step 1 (abandonsFlow): when Another tenant already holds the hostname., **Refused as unavailable, never attributed** (409). Telling one tenant that another owns a hostname is telling them something about a customer.
- Flow F103 branch at step 2 (recoverable): when The records are not published within the validation window., **The claim times out and says so** (`CustomDomain.revalidation` `timedOut`, DEC-547). The tenant starts again with a new `_dnsauth` token; the old one stops validating. The records list shows which …
- Flow F103 branch at step 2 (recoverable): when A record is published with the wrong value, or a CAA record forbids the certificate authority., **The records list names the record, the value expected and the value observed** (`dnsRecords` with CAA/NS rows), so the tenant fixes the one record that is wrong rather than all of them.
- Flow F103 branch at step 2 (abandonsFlow): when The hostname is already routed to another tenant when verification runs., **Refused 409 `hostname-taken`; nothing is verified or issued.**

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (21 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-017?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Claim custom domain, Verify custom domain, Release custom domain, Make primary, New validation token.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-018` Consent & Legal

**Manage the notices every consent is captured against, and the booking consent questions a venue asks ("Are you able to swim?", "I accept the risk"), with the record of every answer (decided 29 September, rev 3 REV3-26).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-018 |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW`, `TENANT_CONFIGURE` (2 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listPolicies` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `policyKind` (navigation), `questionId` (navigation) |
| Route | `/white-label/consent-legal` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Rewired 23 September (L7).** The screen called the maintenance equipment register, guest CRM or subscription billing where its purpose names White Labelling. Its operations now match its purpose. **Two permission families on one screen (DI-387; CHG-SGU-017).** Policies need `TENANT_CONFIGURE`; consent purposes and questions need `GUEST_MANAGE` (reads `GUEST_VIEW`). A role holding one and not the other sees the other section read-only, or hidden with the permission named, never a broken page.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The venue manages the legal texts every consent is captured against (terms, privacy, cookie, refund policies), the consent purposes and their channels, and the booking consent questions ("Are you able to swim?", "I accept the risk"). It also holds a read-only record of every answer. Every change is a new version, never an edit, because a guest who consented to version 3 consented to version 3.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says the screen "offers no create action - this screen declares no operation that makes one". (CHG-SGU-017); Two permission families on one screen (policies need TENANT_CONFIGURE; purposes and questions need GUEST_MANAGE). (CHG-SGU-017).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Include history | toggle | off | — | `listPolicies` ?includeHistory |
| Kind | radio group | — | Privacy · Terms and conditions · Refund · Cookie · Accessibility | `listPolicies` ?kind |
| Kind | radio group | — | Swim · Scuba · Risk · Custom | `listConsentQuestions` ?kind |
| Status | segmented control | — | Active · Retired | `listConsentQuestions` ?status |

**Form: Save policy** (modal, opened by *Save policy*; *Save policy* calls `setPolicy`, *Cancel* sends nothing)

**Collects what `setPolicy` sends before it is called.** Required: `body`, `requiresReconsent`. Optional: `effectiveFrom`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Body `body` | rich text, one per language | required | — | — | English and Arabic (Arabic right to left) | Keyed by language code. Values are sanitised HTML. | `setPolicy` body |
| Requires reconsent `requiresReconsent` | toggle | required | — | — | — | True prompts existing guests to consent again on next launch. Material changes to a privacy notice generally require it. | `setPolicy` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setPolicy` body |

Errors to draw in the form: 400 The English (`en`) or Arabic (`ar`) version is missing (audit R096)

**Form: Save consent purposes** (modal, opened by *Save consent purposes*; *Save consent purposes* calls `setConsentPurposes`, *Cancel* sends nothing)

**Collects what `setConsentPurposes` sends before it is called.** Required: `purposes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Purposes `purposes` | repeatable rows | required | — | — | — | — | `setConsentPurposes` body |
| Purpose `purposes[].purpose` | select | required | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | — | — | `setConsentPurposes` body |
| Display name `purposes[].displayName` | text field | optional | — | — | — | — | `setConsentPurposes` body |
| Description `purposes[].description` | text area | optional | — | — | — | — | `setConsentPurposes` body |
| Channels `purposes[].channels` | multi-select chips | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `setConsentPurposes` body |
| Notice version `purposes[].noticeVersion` | text field | required | — | — | — | Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured. | `setConsentPurposes` body |
| Is required for service `purposes[].isRequiredForService` | toggle | required | — | Withdrawing it means the service cannot be delivered, so it is presented differently. | — | True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently. | `setConsentPurposes` body |
| Expires after months `purposes[].expiresAfterMonths` | number field | optional | — | — | — | — | `setConsentPurposes` body |

**Form: New consent question** (modal, opened by *New consent question*; *Create question* calls `createConsentQuestion`, *Cancel* sends nothing)

**Collects what `createConsentQuestion` sends before it is called.** Required: `kind`, `text` (every tenant language). Optional: `helpText`, `scope` (`perPerson`, the default, or `perBooking`), `required` (default true: checkout waits for it) and `blockingAnswer` (`yes`, `no` or `none`, the default: the answer that stops the booking for the person or booking it covers). Created at version 1 (rev 3 REV3-26). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Swim · Scuba · Risk · Custom | — | What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others are recorded and checked as the venue … | `createConsentQuestion` body |
| Text `text` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | The question as the guest reads it, per locale. | `createConsentQuestion` body |
| Help text `helpText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `createConsentQuestion` body |
| Scope `scope` | segmented control | required | Per person | Per person · Per booking | — | Asked for each declared person, or once for the whole booking. | `createConsentQuestion` body |
| Required `required` | toggle | required | on | — | — | Checkout waits until it is answered (`orders.checkoutCart` 422 `consentRequired`). | `createConsentQuestion` body |
| Blocking answer `blockingAnswer` | segmented control | required | None | Yes · No · None | — | The answer that stops the booking, for the person or the booking it covers. `none` records the answer and blocks nothing. | `createConsentQuestion` body |
| Status `status` | segmented control | required | Active | Active · Retired | — | — | `createConsentQuestion` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Save as new version** (modal, opened by *Save as new version*; *Save new version* calls `updateConsentQuestion`, *Cancel* sends nothing)

**Says, before saving, that the guest will be asked version N+1 from the next cart read** and that answers already given keep their version (rev 3 REV3-26). Optional: `text`, `helpText`, `scope`, `required`, `blockingAnswer`, `status`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Swim · Scuba · Risk · Custom | — | What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others are recorded and checked as the venue … | `updateConsentQuestion` body |
| Text `text` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | The question as the guest reads it, per locale. | `updateConsentQuestion` body |
| Help text `helpText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateConsentQuestion` body |
| Scope `scope` | segmented control | required | Per person | Per person · Per booking | — | Asked for each declared person, or once for the whole booking. | `updateConsentQuestion` body |
| Required `required` | toggle | required | on | — | — | Checkout waits until it is answered (`orders.checkoutCart` 422 `consentRequired`). | `updateConsentQuestion` body |
| Blocking answer `blockingAnswer` | segmented control | required | None | Yes · No · None | — | The answer that stops the booking, for the person or the booking it covers. `none` records the answer and blocks nothing. | `updateConsentQuestion` body |
| Status `status` | segmented control | required | Active | Active · Retired | — | — | `updateConsentQuestion` body |

Errors to draw in the form: 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Policy text**: Rich text in English AND Arabic (both required before publishing). "Ask guests to agree again" is required for material changes. The effective date can be in the future. *(source: contracts/satellite/white-label.yaml#setPolicy; R096)*
- **Consent purposes**: Per purpose, the channels it covers, whether it is required for service (transactional only), and the notice version in force. Adding a purpose does not grant it to existing guests; they are asked. *(source: contracts/satellite/marketing-crm.yaml#setConsentPurposes)*
- **Consent question**: Kind (swim, scuba, risk, custom), text and help text per language, asked per person or once per booking, required or not, and which answer blocks the booking. *(source: contracts/satellite/marketing-crm.yaml#createConsentQuestion; DI-1062)*
- **Refund policy display**: The tiered refund text guests see (e.g. no refund under 24h, 50% at 24-48h, 100% over 48h) comes from back-office rules and is shown, not retyped. *(source: DI-192)*

#### Outputs: what the screen shows and produces

**Shown**

**Every policy** (data table, from `listPolicies`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Privacy, Terms and conditions, Refund, Cookie, Accessibility | — |
| Title | text | The heading a guest sees, and the field a refund question retrieves against. |
| Body | in the reader's language | Keyed by language code. Values are sanitised HTML. |
| Requires reconsent | yes / no (icon or chip) | — |
| Effective from | 1 Oct 2026 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Every consent purpose config** (data table, from `listConsentPurposes`)

| Shows | Format | Notes |
|---|---|---|
| Purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |
| Display name | text | — |
| Description | text | — |
| Notice version | text | Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured. |
| Is required for service | yes / no (icon or chip) | True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently. |
| Expires after months | 1,234 | — |

**Every booking consent question** (data table, from `listConsentQuestions`): **A consent, not a data field** (decided 29 September, rev 3 REV3-26). Each question has its own text per locale, a version, and whether it is asked for each person or once per booking. Filter by `kind` and `status`. **Attaching** is done where the question is used: to a booking flow on CMS-016 (`BookingFlowConfig.consentQuestionIds`, per venue), to a product on BO-008 …

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Swim, Scuba, Risk, Custom | What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others … |
| Text | in the reader's language | The question as the guest reads it, per locale. |
| Version | 1,234 | Raised by one each time the question changes (`updateConsentQuestion`). |
| Scope | chip: Per person, Per booking | Asked for each declared person, or once for the whole booking. |
| Required | yes / no (icon or chip) | Checkout waits until it is answered (`orders.checkoutCart` 422 `consentRequired`). |
| Blocking answer | chip: Yes, No, None | The answer that stops the booking, for the person or the booking it covers. `none` records the answer and blocks nothing. |
| Status | chip: Active, Retired | — |
| Updated at | 1 Oct 2026, 14:30 | — |

**Consent records** (data table, from `listConsentAnswers`): **What was asked, at which version, what was answered, for whom, by whom and when** (rev 3 REV3-26). Filter by order, guest or question. Read-only: an answer is never edited here, and a superseded answer stays listed with `supersededAt`.

| Shows | Format | Notes |
|---|---|---|
| Answered at | 1 Oct 2026, 14:30 | — |
| Question version | 1,234 | — |
| Answer | chip: Yes, No | — |
| Scope | chip: Per person, Per booking | — |
| Person name | text | — |
| Superseded at | 1 Oct 2026, 14:30 | — |

**The selected policy** (detail panel, from `listPolicies`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Privacy, Terms and conditions, Refund, Cookie, Accessibility | — |
| Title | text | The heading a guest sees, and the field a refund question retrieves against. |
| Body | in the reader's language | Keyed by language code. Values are sanitised HTML. |
| Requires reconsent | yes / no (icon or chip) | — |
| Effective from | 1 Oct 2026 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected consent question** (detail panel, from `listConsentQuestions`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Swim, Scuba, Risk, Custom | What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others … |
| Text | in the reader's language | The question as the guest reads it, per locale. |
| Help text | in the reader's language | — |
| Version | 1,234 | Raised by one each time the question changes (`updateConsentQuestion`). |
| Scope | chip: Per person, Per booking | Asked for each declared person, or once for the whole booking. |
| Required | yes / no (icon or chip) | Checkout waits until it is answered (`orders.checkoutCart` 422 `consentRequired`). |
| Blocking answer | chip: Yes, No, None | The answer that stops the booking, for the person or the booking it covers. `none` records the answer and blocks nothing. |
| Status | chip: Active, Retired | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save policy (primary button) | `setPolicy` PUT `/tenant-config/policies/{policyKind}` | inline | Policy | 400 The English (`en`) or Arabic (`ar`) version is missing (audit R096) | gated `TENANT_CONFIGURE`; opens modal first |
| Save consent purposes (secondary button) | `setConsentPurposes` PUT `/consent-purposes` | inline | ConsentPurposeConfig[] | — | gated `GUEST_MANAGE`; opens modal first |
| New consent question (secondary button) | `createConsentQuestion` POST `/consent-questions` | ConsentQuestion | ConsentQuestion | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | gated `GUEST_MANAGE`; opens modal first |
| Save as new version (secondary button) | `updateConsentQuestion` PATCH `/consent-questions/{questionId}` | ConsentQuestion | ConsentQuestion | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `GUEST_MANAGE`; opens modal first |
| Retire question (destructive button) | `updateConsentQuestion` PATCH `/consent-questions/{questionId}` | ConsentQuestion | ConsentQuestion | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `GUEST_MANAGE`; opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Version history**: Every published version of each policy, newest first, with publisher and date; any old version can be opened. *(source: contracts/satellite/white-label.yaml#listPolicies; R163)*
- **Consent records**: What was asked (and at which version), the answer, for whom, by whom and when. Superseded answers carry their superseded date. Read-only. *(source: contracts/satellite/marketing-crm.yaml#listConsentAnswers)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Save as new version (consent question)**: Changing text, scope, required or blocking answer raises the version; answers already given keep theirs. Carts ask the new version on their next read. *(source: contracts/satellite/marketing-crm.yaml#updateConsentQuestion)*
- **Retire question**: Stops it being asked on every product and flow it is attached to; answers stay on record. *(source: contracts/satellite/marketing-crm.yaml#updateConsentQuestion)*

**Data it reads**: `listPolicies` (onLoad, Privacy, terms and cookie notices); `listConsentPurposes` (onLoad, What guests can consent to); `listConsentQuestions` (onLoad, The venue's booking consent questions (rev 3 REV3-26))

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The consent legal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the consent legal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No policy, purpose or consent question yet. Offers Save policy (`setPolicy`), Save consent purposes (`setConsentPurposes`) and New consent question (`createConsentQuestion`). |
| Empty, no results (`?state=emptyNoResults`) | `listPolicies` takes no filter. The consent questions (kind, status) and the consent records (order, guest, question) do: an empty result names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listPolicies` requires to show this screen, and names that permission (the screen's other reads need `GUEST_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `GUEST_MANAGE` for `setConsentPurposes`, `createConsentQuestion` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The English (`en`) or Arabic (`ar`) version is missing (audit R096); 400 Validation failed |

#### Edge cases to draw

- **A privacy notice is republished with "ask again"**: Guests whose consent was given against the old version see "needs renewing" on their profile and are asked on next launch. *(source: contracts/satellite/white-label.yaml#setPolicy; contracts/satellite/marketing-crm.yaml#getGuestConsents)*

#### Consistency with other screens

- Match `CMS-028`: Privacy notice and terms versions are also managed on CMS-028; the two screens must share one version history.
- Match `WEB-011`: The questions defined here are the ones asked at the details step.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policies:
- Terms of sale v7 (12 Sep 2026)
- Privacy notice v4 (1 Oct 2026, ask again)
- Cookie policy v2
- Refund policy v3
question: '{kind: Swim, text: Are you able to swim?, textAr: هل تستطيع السباحة؟, scope: per person, required: yes,
  blocking: No}'
```

#### Permissions

- `listPolicies` → `TENANT_CONFIGURE` (configure) · staff
- `setPolicy` → `TENANT_CONFIGURE` (configure) · staff
- `listConsentPurposes` → `GUEST_VIEW` (read) · staff, guest
- `setConsentPurposes` → `GUEST_MANAGE` (configure) · staff
- `listConsentQuestions` → `GUEST_VIEW` (read) · staff
- `createConsentQuestion` → `GUEST_MANAGE` (configure) · staff
- `updateConsentQuestion` → `GUEST_MANAGE` (configure) · staff
- `listConsentAnswers` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listPolicies` requires to show this screen, and names that permission (the screen's other reads need `GUEST_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `GUEST_MANAGE` for `setConsentPurposes`, `createConsentQuestion` …

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.17 | Policy Management - System shall support configurable policies. | Guest Mobile App & Branding | CONTRACTED | `setPolicy` |
| 19.1.18 | Terms & Conditions Management - System shall support configurable terms and conditions. | Guest Mobile App & Branding | CONTRACTED | `setPolicy` |
| 2.6.59 | Policy Management Manage cookie policy content centrally. Version control for policy updates. Publish updated policies automatically. Maintain historical policy versions. | Ticketing Sales | CONTRACTED | `setPolicy` |
| 22.13.7 | Consent Expiration Management | Marketing & CRM | CONTRACTED | `setConsentPurposes` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Refund policy shown to guests is tiered and driven by back-office rules per business, e.g. no refund <24h, 50% between 24–48h, 100% >48h. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-192)*
- Configurable FAQ section plus Terms & Conditions, Privacy Policy and Cookie Policy with an accept/deny prompt. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-191)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Body (`policies.body`) | English and Arabic (Arabic right to left) | — | the content and policy pages | Keyed by language code. Values are sanitised HTML. |
| Requires reconsent (`policies.requiresReconsent`) | — | — | the content and policy pages | True prompts existing guests to consent again on next launch. Material changes to a privacy notice generally require it. |
| Effective from (`policies.effectiveFrom`) | 1 Oct 2026 (dd MMM yyyy) | — | the content and policy pages | — |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-018` · status **notStarted** · provenance generated
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save policy, Save consent purposes, New consent question, Save as new version, Retire question.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-019` User Access

**Say who in the tenant may change what.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-019 |
| Who uses it | venue staff holding `ROLE_MANAGE`, `USER_MANAGE` (2 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listPrincipals` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `principalId` (session) |
| Route | `/white-label/user-access` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Who in the tenant may change what in the CMS: the people with CMS roles and the roles' CMS permissions (brand, pages, publish). It should be the staff directory filtered to CMS rights with the ability to grant or remove a CMS role, not a separate user store.

**Fixed on main** (the package already carries these; draw what it says): The screen declares only reads; nothing grants or removes a role. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every principal' drop id, primaryRoleId; 'Every role' drop id, inheritsFromRoleId. (CHG-SGU-019); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SGU-019).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scope path | text field | optional | — | — | — | Sends `?scopePath=` to `listPrincipals`. | `listPrincipals` ?scopePath |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listPrincipals`. | `listPrincipals` ?isActive |

**Form: Change access** (modal, opened by *Change access*; *Change access* calls `updatePrincipal`, *Cancel* sends nothing)

**Collects what `updatePrincipal` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Display name `displayName` | text field | optional | — | max length 200 | — | — | `updatePrincipal` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updatePrincipal` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePrincipal` body |
| Primary role `primaryRoleId` | picker: choose a primary role | optional | — | — | shows names, sends the id | — | `updatePrincipal` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every principal** (data table, from `listPrincipals`): The role a principal holds and the role another inherits from are shown by name; raw ids only in the detail panel's copy action.

| Shows | Format | Notes |
|---|---|---|
| Username | text | — |
| Display name | text | — |
| Is active | yes / no (icon or chip) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Past this, resolution returns DENY regardless of grants. |
| Roles | list or chips (count when long) | — |
| Last login at | 1 Oct 2026, 14:30 | — |

**Every role** (data table, from `listRoles`): The role a principal holds and the role another inherits from are shown by name; raw ids only in the detail panel's copy action.

| Shows | Format | Notes |
|---|---|---|
| Code | text | Unique within the tenant (decided 28 September, audit R108). A seeded role's code is reserved in every tenant. |
| Name | text | — |
| Description | text | — |
| Permissions | list or chips (count when long) | A role that grants no permissions is not a role. `Role` carried a code, a name and two counts until 18 August, and … |
| Is system | yes / no (icon or chip) | Seeded roles ship and are editable; deleting one is refused. A venue that removes `cashier` and rebuilds it has two roles with one name in … |
| Principal count | 1,234 | — |
| Grant count | 1,234 | — |

**The selected principal** (detail panel, from `listPrincipals`)

| Shows | Format | Notes |
|---|---|---|
| Username | text | — |
| Display name | text | — |
| Is active | yes / no (icon or chip) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Past this, resolution returns DENY regardless of grants. |
| Roles | list or chips (count when long) | — |
| Last login at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Change access (secondary button) | `updatePrincipal` PATCH `/principals/{principalId}` | inline | Principal | — | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **People with CMS rights**: Name, roles that carry CMS permissions, scope (tenant or venue), last sign-in; Publish permission highlighted because it puts content live. *(source: contracts/spine/identity.yaml#listPrincipals; contracts/spine/identity.yaml#listRoles)*

**Data it reads**: `listPrincipals` (onLoad, List principals); `listRoles` (onLoad, List roles)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The user access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the user access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nobody but the tenant owner has access yet: an empty list here is normal on a new tenant. Change access is offered on each person once they exist; people are invited from the platform's user management, not here. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on scopePath, isActive and the user access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Consistency with other screens

- Match `BO-053`: Same directory, filtered.
- Match `BO-054`: Roles defined there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
people:
- name: Aisha Al Nuaimi
  roles:
  - Tenant Admin
  scope: tenant
  canPublish: true
- name: Noura Al Hammadi
  roles:
  - Content Editor
  scope: AquaCove Dubai
  canPublish: false
```

#### Permissions

- `listPrincipals` → `USER_MANAGE` (configure) · staff, partner
- `listRoles` → `ROLE_MANAGE` (configure) · staff
- `updatePrincipal` → `USER_MANAGE` (configure) · staff, partner

**A refused user sees:** Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-019` · status **notStarted** · provenance generated
- ADR-0051 *Every AI function ships on a baseline and learns per tenant; a model goes live only on evidence* (`docs/adr/0051-ai-ships-on-a-baseline-and-learns-per-tenant.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (21 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Change access.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `ROLE_MANAGE`, `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-101` Help Me Choose

**Set up a venue's Help me choose so its answers filter the catalogue, review the question set the assistant proposes from the venue's products, preview the filtered list and publish it (Site Builder step 4).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-101 |
| Who uses it | venue staff holding `AI_USE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`, `TENANT_PUBLISH` (1 operate, 1 read, 2 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listGuidedChoices` reads the venue's set-ups and the editor acts on one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `guidedChoiceId` (navigation), `suggestionId` (navigation) · cold entry: Resolves the venue from the session and opens on the suggestions awaiting review, or on the list when there are none. |
| Route | `/white-label/help-me-choose` |

**What the spec says about it.** **Added 29 September for rev 3 REV3-11: Help me choose is venue configuration, never hard-coded.** A venue sets up one to four questions, each with two to four answers (title, one-liner, icon, optional badge), and the answer picked on the last question opens the product, category, event or booking module that fits through a result card. **Two sources, one review**: staff write a set-up here, and once the venue's products are uploaded the `ai` service proposes set-ups (`source` `aiSuggested`), which land here as drafts. **A suggestion is never published by itself**: a person reviews it, edits it or dismisses it, previews it and publishes it. One published set-up per venue; publishing another returns the old one to draft.

**From the White Label & CMS process.** Set up a venue's Help me choose: a few questions whose answers filter the products a guest sees (or end on one recommended result), review the set the AI proposes from the venue's products, preview the filtered list, and publish. It is never a consent step. The one thing to get right: an answer that leaves nothing bookable must be visible before publishing.

**Fixed on main** (the package already carries these; draw what it says): Notes and formCreateGuidedChoice say one or two questions and a target per answer. (CHG-SGU-022).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue | select field | — | — | — | — | The venue whose set-ups are shown (path `venueId`); defaults to the session venue. | — |
| Source | select field | — | — | — | — | Sends `?source=`, `manual` or `aiSuggested`. **Suggestions awaiting review** is `aiSuggested` with status `draft`, and is the default view while any exist. | — |
| Status | select field | — | — | — | — | Sends `?status=`, `draft` or `published`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | segmented control | Draft | Draft · Published | `listGuidedChoices` ?status |
| Source | segmented control | — | Manual · AI suggested | `listGuidedChoices` ?source |

**Form: New set-up** (modal, opened by *New set-up*; *Create draft* calls `createGuidedChoice`, *Cancel* sends nothing)

**Collects what `createGuidedChoice` sends before it is called.** Required: `name` (staff-facing), `mode`, `questions` (one or two, each with two to four answers and a target per answer). Optional: `showBanner` (default on). Created as a draft; guests see nothing until it is published. Dismissing sends nothing; the screen behind is unchanged. **One to four questions; the answers filter the catalogue by default and a target per answer is optional** (W4, 29 September) (CHG-SGU-022).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 80 | — | Staff-facing name, e.g. "Water park day planner". | `createGuidedChoice` body |
| Mode `mode` | segmented control | required | Button | Button · Popup on arrival · Off | — | How the guest reaches it (rev 3 REV3-11). `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on the guest's first arrival at the … | `createGuidedChoice` body |
| Show banner `showBanner` | toggle | optional | on | — | — | The dark banner under the products ("Choose from the experiences above or let us help you decide") with a Help me choose button. | `createGuidedChoice` body |
| Behaviour `behaviour` | segmented control | optional | Filter | Filter · Recommend | — | `filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4). | `createGuidedChoice` body |
| Show everything `showEverything` | toggle | optional | on | — | — | The "Show everything" link under a filtered list, which clears the answers (W4). | `createGuidedChoice` body |
| Questions `questions` | repeatable rows | required | — | at least 1; at most 4 | — | One to four questions (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). | `createGuidedChoice` body |
| Title `questions[].title` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createGuidedChoice` body |
| Kind `questions[].kind` | radio group | optional | Choice | Choice · Yes no · Age · Level · Certification | — | What the question asks (decided 29 September, W4). `choice` free answers; `yesNo` two answers (e.g. | `createGuidedChoice` body |
| Sort order `questions[].sortOrder` | number field | required | — | min 0 | — | — | `createGuidedChoice` body |
| Answers `questions[].answers` | repeatable rows | required | — | at least 2; at most 4 | — | Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11). | `createGuidedChoice` body |
| Title `questions[].answers[].title` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createGuidedChoice` body |
| Body `questions[].answers[].body` | text, one per language | optional | — | The one-liner under the title, at most 140 characters in each language. | English and Arabic (Arabic right to left) | The one-liner under the title, at most 140 characters in each language. | `createGuidedChoice` body |
| Icon `questions[].answers[].icon` | text field | optional | — | max length 40 | — | An icon name from the guest app's icon set. | `createGuidedChoice` body |
| Badge `questions[].answers[].badge` | text, one per language | optional | — | At most 24 characters in each language. | English and Arabic (Arabic right to left) | Optional, e.g. "Best value". | `createGuidedChoice` body |
| Sort order `questions[].answers[].sortOrder` | number field | required | — | min 0 | — | — | `createGuidedChoice` body |
| Target `questions[].answers[].target` | group | optional | — | — | — | Required with `behaviour` `recommend` on the last question; optional with `filter`, where it is the card shown above the filtered list. | `createGuidedChoice` body |
| Filter `questions[].answers[].filter` | group | optional | — | — | — | What this answer keeps in the list (decided 29 September, W4). Every field set must hold; answers to different questions are combined with AND. | `createGuidedChoice` body |
| Consent prefill `questions[].answers[].consentPrefill` | group | optional | — | — | — | Pre-fills a REV3-26 consent question from this answer (decided 29 September, W4). | `createGuidedChoice` body |
| Result `questions[].answers[].result` | group | optional | — | — | — | The result card when this answer decides the result. Absent fields fall back to the target's own name, summary and image. | `createGuidedChoice` body |

Errors to draw in the form: 400 A target is not in this venue, a required target id is missing for its `kind`, or the question and answer counts are outside their bounds

**Form: Publish** (confirmDialog, opened by *Publish*; *Publish to guests* calls `publishGuidedChoice`, *Cancel* sends nothing)

**Names the venue and the set-up that stops showing there**, since only one is published per venue. An answer whose target is not on sale or not enabled blocks the publish and is named (`422`).

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already `published`; 422 An answer's target is not on sale or not enabled, or an answer lacks the filter or target its behaviour needs; the problem names the answer

**Form: Delete draft or dismiss suggestion** (confirmDialog, opened by *Delete draft or dismiss suggestion*; *Delete* calls `deleteGuidedChoice`, *Keep it* sends nothing)

Names the set-up and, for an AI suggestion, says that dismissing it removes it and the assistant's reasoning with it. A published set-up cannot be deleted (`409`).

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The choice is `published`

**Sent by *Save draft*** (`updateGuidedChoice`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 80 | — | — | `updateGuidedChoice` body |
| Mode `mode` | segmented control | optional | — | Button · Popup on arrival · Off | — | — | `updateGuidedChoice` body |
| Show banner `showBanner` | toggle | optional | — | — | — | — | `updateGuidedChoice` body |
| Behaviour `behaviour` | segmented control | optional | — | Filter · Recommend | — | — | `updateGuidedChoice` body |
| Show everything `showEverything` | toggle | optional | — | — | — | — | `updateGuidedChoice` body |
| Questions `questions` | repeatable rows | optional | — | at least 1; at most 4 | — | Replaces the whole question list; same shape and bounds as `GuidedChoice.questions`. | `updateGuidedChoice` body |

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **questions[]**: 1 to 4 questions, each of a kind Choice / Yes-No / Age / Level / Certification, title per language, in order. *(source: contracts/satellite/white-label.yaml#/components/schemas/GuidedChoice; MoM 29 Sep 1 W4)*
- **answers[]**: 2 to 4 per question; title, one-liner (at most 140 characters per language), icon, optional badge (at most 24 characters, e.g. Best value). With behaviour filter each answer needs a filter (products, categories, segment tags, age range, swimmer yes or no, certificate held or not); with recommend each last-question answer needs a target. *(source: contracts/satellite/white-label.yaml#/components/schemas/GuidedChoice; DI-984)*
- **consentPrefill**: An answer may pre-fill one booking consent question (e.g. Can everyone swim? -> Are you able to swim?); the guest still ticks it. *(source: MoM 29 Sep 1 W4; DI-1005)*
- **mode, showBanner, showEverything**: Button on the booking page (default) / Also a pop-up on first arrival / Off; dark banner under the products on by default; Show everything link on by default. *(source: DI-1052; contracts/satellite/white-label.yaml#/components/schemas/GuidedChoice)*

#### Outputs: what the screen shows and produces

**Shown**

**Every Help me choose set-up at this venue** (data table, from `listGuidedChoices`): **An AI suggestion is labelled as one** on its row, and keeps `source` `aiSuggested` after a person edits it, so a report can count how many proposals were published.

| Shows | Format | Notes |
|---|---|---|
| Name | text | Staff-facing name, e.g. "Water park day planner". |
| Status | chip: Draft, Published | Draft until a person publishes it (decided 29 September, rev 3 REV3-11). Guests see only a `published` choice. |
| Source | chip: Manual, AI suggested | `manual` when staff created it; `aiSuggested` when the `ai` service proposed it (a service caller). |
| Mode | chip: Button, Popup on arrival, Off | How the guest reaches it (rev 3 REV3-11). `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on … |
| Show banner | yes / no (icon or chip) | The dark banner under the products ("Choose from the experiences above or let us help you decide") with a Help me choose button. |
| Published at | 1 Oct 2026, 14:30 | — |
| Updated at | 1 Oct 2026, 14:30 | — |

**The selected set-up** (detail panel, from `listGuidedChoices`): **The editor.** `mode`: a button on the booking page, a pop-up on the guest's first arrival as well, or off (configured but not shown). `showBanner`: the dark banner under the products. One or two questions, two to four answers each: title, one-liner (140 characters), icon, badge (24 characters), target (a product, category, event or booking module, picked from `listProducts` …

| Shows | Format | Notes |
|---|---|---|
| Name | text | Staff-facing name, e.g. "Water park day planner". |
| Mode | chip: Button, Popup on arrival, Off | How the guest reaches it (rev 3 REV3-11). `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on … |
| Show banner | yes / no (icon or chip) | The dark banner under the products ("Choose from the experiences above or let us help you decide") with a Help me choose button. |
| Behaviour | chip: Filter, Recommend | `filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4). |
| Show everything | yes / no (icon or chip) | The "Show everything" link under a filtered list, which clears the answers (W4). |
| Questions | list or chips (count when long) | One to four questions (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). |
| Status | chip: Draft, Published | Draft until a person publishes it (decided 29 September, rev 3 REV3-11). Guests see only a `published` choice. |
| Source | chip: Manual, AI suggested | `manual` when staff created it; `aiSuggested` when the `ai` service proposed it (a service caller). |
| Suggestion ref | text | For `aiSuggested`, the id of the `ai` job that proposed it. Null for `manual`. |
| Published at | 1 Oct 2026, 14:30 | — |
| Published by | the name it points at, never the id | The person who published it. Never a service. |

**Preview** (live preview): **Renders the draft as a guest would meet it**: the button or pop-up, the banner, each question and the result card, in each language and in both directions. Drawn from the record in hand; it calls nothing and publishes nothing, and guests keep seeing the published set-up until Publish. **Preview the filtered list**: for each combination of answers, the products left (read with `listProducts` and …

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
| New set-up (primary button) | `createGuidedChoice` POST `/venues/{venueId}/guided-choices` | GuidedChoice | GuidedChoice | 400 A target is not in this venue, a required target id is missing for its `kind`, or the question and answer counts are outside their bounds | opens modal first |
| Save draft (secondary button) | `updateGuidedChoice` PATCH `/guided-choices/{guidedChoiceId}` | inline | GuidedChoice | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The choice is `published`; unpublish it first | — |
| Publish (secondary button) | `publishGuidedChoice` POST `/guided-choices/{guidedChoiceId}/publish` | — | GuidedChoice | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already `published` | opens confirmDialog first |
| Unpublish (secondary button) | `unpublishGuidedChoice` POST `/guided-choices/{guidedChoiceId}/unpublish` | — | GuidedChoice | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not `published` | — |
| Delete draft or dismiss suggestion (destructive button) | `deleteGuidedChoice` DELETE `/guided-choices/{guidedChoiceId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The choice is `published` | opens confirmDialog first |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **AI suggestion review**: A suggestion is labelled "Suggested by AI" and shows why each question and answer was proposed (ai getGuidedChoiceSuggestion); the label stays after editing. *(source: contracts/satellite/white-label.yaml#proposeGuidedChoice; DI-1006)*
- **Filtered-list preview**: For each answer combination, the products left; a combination with none bookable is flagged red. *(source: screens/P13-white-label-cms.yaml#CMS-101)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Publish to guests**: Live at once at this venue (not part of the site publish); the venue's previous published set-up returns to draft. 422 names the answer whose target is not on sale or whose filter is missing. *(source: contracts/satellite/white-label.yaml#publishGuidedChoice)*
- **Unpublish**: Guests stop seeing it at once; back to draft. *(source: contracts/satellite/white-label.yaml#unpublishGuidedChoice)*
- **Edit a published set-up**: Refused 409; offer "Unpublish to edit" or "Duplicate as draft". *(source: contracts/satellite/white-label.yaml#updateGuidedChoice)*

**Data it reads**: `listGuidedChoices` (onLoad, The venue's set-ups, filtered by source and status (rev 3 …)

**Where the user goes next**

- → `CMS-016` Site Settings: *Back to Site Settings*
- → `CMS-102` Site Builder: *Back to the Site Builder*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue's Help me choose set-ups, read by `listGuidedChoices`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the set-ups untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **No Help me choose at this venue, so guests see none.** Offers New set-up, and says that once the venue's products are uploaded the assistant proposes set-ups here as drafts for review. |
| Empty, no results (`?state=emptyNoResults`) | The source or status filter matched nothing and the venue's other set-ups are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listGuidedChoices` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `suggestGuidedChoice`, `getGuidedChoiceSuggestion`; `PRODUCT_VIEW` for `listProducts`, `listProductCategories`, `listEvents` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 A target is not in this venue, a required target id is missing for its `kind`, or the question and answer counts are outside their bounds; 400 Validation failed; 409 A suggestion for this venue is already running … |

#### Edge cases to draw

- **Product in an answer's filter goes off sale after publish**: The guest list simply narrows; the next publish attempt flags it. *(source: contracts/satellite/white-label.yaml#publishGuidedChoice)*

#### Consistency with other screens

- Match `WEB-005`: The Help me choose button, banner and pop-up drawn there come from this set-up.
- Match `KSK-003`: The kiosk shows the same filtered list (server applies the filter).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
name: Water park day planner
questions:
- kind: yesNo
  title:
    en: Can everyone in your group swim?
    ar: هل يستطيع جميع أفراد مجموعتك السباحة؟
  answers:
  - All of us
  - Some of us
  - None of us
- kind: age
  title:
    en: How old is the youngest?
    ar: كم عمر الأصغر سنًا؟
  answers:
  - Under 4
  - 4 to 11
  - 12 and over
result: None of us -> Splash and river pass (Adult AED 175, Junior AED 135, Child AED 125)
```

#### Permissions

- `listGuidedChoices` → `TENANT_CONFIGURE` (configure) · staff
- `createGuidedChoice` → `TENANT_CONFIGURE` (configure) · staff
- `updateGuidedChoice` → `TENANT_CONFIGURE` (configure) · staff
- `deleteGuidedChoice` → `TENANT_CONFIGURE` (configure) · staff
- `publishGuidedChoice` → `TENANT_PUBLISH` (configure) · staff
- `unpublishGuidedChoice` → `TENANT_PUBLISH` (configure) · staff
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listProductCategories` → `PRODUCT_VIEW` (read) · staff, guest
- `listEvents` → `PRODUCT_VIEW` (read) · staff
- `listBookingFlows` → `TENANT_CONFIGURE` (configure) · staff
- `suggestGuidedChoice` → `AI_USE` (operate) · staff
- `getGuidedChoiceSuggestion` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listGuidedChoices` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `suggestGuidedChoice`, `getGuidedChoiceSuggestion`; `PRODUCT_VIEW` for `listProducts`, `listProductCategories`, `listEvents` …

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Help me choose needs a configuration page per venue; AI may propose the question set from the product catalogue for the operator to validate and edit. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W4 Help me choose · DI-1006)*
- "Help me choose" (experience builder) is not a consent step: its questions (yes/no, age, certified or not, etc.) filter the catalogue so only suitable products are shown (Deep Dive Dubai reference). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W4 Help me choose · DI-1005)*
- Help me choose setup per venue: up to 2 questions, 3 answers each (title, one-line description, icon, optional badge e.g. "Best value"), each answer mapped to one booking flow, a result card (title, description, image) per recommendable product, and placement (button above products, pop-up on arrival, off). *(agreed · design review 23 Sep 2026, What the venue sets up in the CMS (per venue) · DI-984)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Help me choose name (`guidedChoices.name`) | max length 80 | — | GST-003, GST-008, WEB-002, WEB-005 | Staff-facing name, e.g. "Water park day planner". |
| Help me choose mode (`guidedChoices.mode`) | Button · Popup on arrival · Off | Button | GST-003, GST-008, WEB-002, WEB-005 | How the guest reaches it (rev 3 REV3-11). `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on the guest's first arrival at the booking page (whether it was seen is kept on … |
| Show banner (`guidedChoices.showBanner`) | — | on | GST-003, GST-008, WEB-002, WEB-005 | The dark banner under the products ("Choose from the experiences above or let us help you decide") with a Help me choose button. |
| Help me choose behaviour (`guidedChoices.behaviour`) | Filter · Recommend | Filter | GST-003, GST-008, WEB-002, WEB-005 | `filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4). |
| Show everything (`guidedChoices.showEverything`) | — | on | GST-003, GST-008, WEB-002, WEB-005 | The "Show everything" link under a filtered list, which clears the answers (W4). |
| Help me choose questions (`guidedChoices.questions`) | at least 1; at most 4 | — | GST-003, GST-008, WEB-002, WEB-005 | One to four questions (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). |
| Questions: title (`guidedChoices.questions[].title`) | English and Arabic (Arabic right to left) | — | GST-003, GST-008, WEB-002, WEB-005 | — |
| Questions: kind (`guidedChoices.questions[].kind`) | Choice · Yes no · Age · Level · Certification | Choice | GST-003, GST-008, WEB-002, WEB-005 | What the question asks (decided 29 September, W4). `choice` free answers; `yesNo` two answers (e.g. |
| Questions: sort order (`guidedChoices.questions[].sortOrder`) | min 0 | — | GST-003, GST-008, WEB-002, WEB-005 | — |
| Questions: answers (`guidedChoices.questions[].answers`) | at least 2; at most 4 | — | GST-003, GST-008, WEB-002, WEB-005 | Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11). |
| Answers: title (`guidedChoices.questions[].answers[].title`) | English and Arabic (Arabic right to left) | — | GST-003, GST-008, WEB-002, WEB-005 | — |
| Answers: body (`guidedChoices.questions[].answers[].body`) | The one-liner under the title, at most 140 characters in each language. | — | GST-003, GST-008, WEB-002, WEB-005 | The one-liner under the title, at most 140 characters in each language. |
| Answers: icon (`guidedChoices.questions[].answers[].icon`) | max length 40 | — | GST-003, GST-008, WEB-002, WEB-005 | An icon name from the guest app's icon set. |
| Answers: badge (`guidedChoices.questions[].answers[].badge`) | At most 24 characters in each language. | — | GST-003, GST-008, WEB-002, WEB-005 | Optional, e.g. "Best value". |
| Answers: sort order (`guidedChoices.questions[].answers[].sortOrder`) | min 0 | — | GST-003, GST-008, WEB-002, WEB-005 | — |
| Answers: target (`guidedChoices.questions[].answers[].target`) | — | — | GST-003, GST-008, WEB-002, WEB-005 | Required with `behaviour` `recommend` on the last question; optional with `filter`, where it is the card shown above the filtered list. |
| Answers: filter (`guidedChoices.questions[].answers[].filter`) | — | — | GST-003, GST-008, WEB-002, WEB-005 | What this answer keeps in the list (decided 29 September, W4). Every field set must hold; answers to different questions are combined with AND. |
| Answers: consent prefill (`guidedChoices.questions[].answers[].consentPrefill`) | — | — | GST-003, GST-008, WEB-002, WEB-005 | Pre-fills a REV3-26 consent question from this answer (decided 29 September, W4). |
| Answers: result (`guidedChoices.questions[].answers[].result`) | — | — | GST-003, GST-008, WEB-002, WEB-005 | The result card when this answer decides the result. Absent fields fall back to the target's own name, summary and image. |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-101` · status **notStarted** · provenance generated
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (28), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-101?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes, New set-up, Save draft, Publish, Unpublish, Delete draft or dismiss suggestion.
- [ ] Every transition is wired: `CMS-016`, `CMS-102`.
- [ ] Every gated control is gated: `AI_USE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`, `TENANT_PUBLISH`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 1 edge case(s) from the process notes are drawn.
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

### In P13 · White Label

- Font, header/footer (not yet in the current wireframe build), card size and layout are configurable in the mobile app, consistent with the web app's white-labelling approach. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1097)*
- Qossai (rated the CMS prototype ~70%): a client should be able to build a working site "within 30 minutes", easily adding header, footer, fonts and its own images/graphics self-service; Allam: every CMS option must visibly change something and the interface must be intuitive to navigate. *(client request · MoM 24 Sep 2026, 4.8 Guest Web App CMS Prototype — Feedback on Maturity & Scope Expectations · DI-988)*
- The reviewed prototype is the actual guest-facing B2C site customers browse and book from, not a CMS tool. A separate, more limited white-label interface lets a client adjust colours, fonts and layout from a menu of options; not yet built in the prototype. *(agreed · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-887)*
- Base structure (header, footer, layout) is fixed across tenants; logo, colour, font and module visibility (e.g. hide Dining or Retail) are configurable per tenant, and independently for web and mobile (e.g. a different mobile header). *(agreed · MoM 14 Aug 2026, 4. White-Labeling and Customization Boundaries · DI-285)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- Modules enabled/disabled per tenant by licence: Ticketing & Booking, Membership, Events, Attractions, Virtual Queue, F&B, Retail, Parking; add-ons (Lost & Found, AI Concierge Chat, multi-language, integrations) toggle the same way and appear automatically as new integrations are built. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-193)*
- Allam: banner, header, footer and background color are CMS-configurable per client, but site structure and navigation flow are fixed and adapt automatically to product configuration (dated, non-dated, seated, membership products surface the right fields). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-119)*
- A "powered by [platform]" footer credit is fixed and not client-editable. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-111)*
- White-label sites share one platform/template but each is configured independently: header, footer, logo, colors, fonts and hero banner are client-editable from the backend. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-108)*

**14 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"claimCustomDomain": {"method":"POST","path":"/tenant-domains","contract":"white-label","summary":"Claim a domain and get a verification token","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CustomDomain"},
"createConsentQuestion": {"method":"POST","path":"/consent-questions","contract":"marketing-crm","summary":"Define a consent question","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConsentQuestion","responds":"ConsentQuestion"},
"createGuidedChoice": {"method":"POST","path":"/venues/{venueId}/guided-choices","contract":"white-label","summary":"Set up Help me choose for a venue","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuidedChoice","responds":"GuidedChoice"},
"createPreview": {"method":"POST","path":"/tenant-config/preview","contract":"white-label","summary":"Generate a preview link","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Preview"},
"createUrlRedirect": {"method":"POST","path":"/seo-redirects","contract":"marketing-crm","summary":"301, 302 and custom redirects","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"UrlRedirect","responds":"UrlRedirect"},
"deleteGuidedChoice": {"method":"DELETE","path":"/guided-choices/{guidedChoiceId}","contract":"white-label","summary":"Delete a Help me choose set-up, or dismiss a suggestion","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"diffConfigVersion": {"method":"GET","path":"/tenant-config/versions/{version}/diff","contract":"white-label","summary":"Compare a version against the working draft","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"against","in":"query","required":null}],"requestBody":null,"responds":"ConfigDiff"},
"exportSitePackage": {"method":"POST","path":"/site-package","contract":"white-label","summary":"Generate a site package (self-hosted)","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getBookingFlowConfig": {"method":"GET","path":"/tenant-config/booking-flow","contract":"white-label","summary":"How the guest booking flow looks and steps","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"effectiveForVenueId","in":"query","required":false}],"requestBody":null,"responds":"BookingFlowConfig"},
"getGuidedChoiceSuggestion": {"method":"GET","path":"/guided-choice-suggestions/{suggestionId}","contract":"ai","summary":"The reasons behind a Help me choose suggestion","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiGuidedChoiceSuggestion"},
"getPlatformSubdomain": {"method":"GET","path":"/platform-subdomain","contract":"white-label","summary":"The tenant's platform subdomain","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"PlatformSubdomain"},
"getPublishReviewPolicy": {"method":"GET","path":"/publish-review-policy","contract":"white-label","summary":"Whether publishing needs a review","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"PublishReviewPolicy"},
"getSeoMetadata": {"method":"GET","path":"/seo-metadata","contract":"marketing-crm","summary":"The metadata in force for one page","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"entityKind","in":"query","required":true},{"name":"entityId","in":"query","required":true},{"name":"locale","in":"query","required":null}],"requestBody":null,"responds":"SeoMetadata"},
"getSitePackage": {"method":"GET","path":"/site-package/{packageId}","contract":"white-label","summary":"A site package and its download link","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SitePackage"},
"getTenantAppStatus": {"method":"GET","path":"/tenant-config/status","contract":"white-label","summary":"App status and recent changes","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantAppStatus"},
"getTenantConfig": {"method":"GET","path":"/tenant-config","contract":"white-label","summary":"Full working configuration","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"version","in":"query","required":null}],"requestBody":null,"responds":"TenantConfig"},
"getTranslationProposals": {"method":"GET","path":"/ai/translate/{translationJobId}","contract":"ai","summary":"Follow a translation job","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TranslationProposals"},
"listAnalyticsProviders": {"method":"GET","path":"/tenant-config/analytics-providers","contract":"white-label","summary":"The analytics platforms the storefront and app report to","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBookingFlows": {"method":"GET","path":"/venues/{venueId}/booking-flows","contract":"white-label","summary":"A venue's booking flows, in the working draft","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"flowTypeKey","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConfigVersions": {"method":"GET","path":"/tenant-config/versions","contract":"white-label","summary":"Version history","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConsentAnswers": {"method":"GET","path":"/consent-answers","contract":"marketing-crm","summary":"The consent records given at booking","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"orderId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"questionId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConsentPurposes": {"method":"GET","path":"/consent-purposes","contract":"marketing-crm","summary":"Configured consent purposes","permission":"GUEST_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConsentQuestions": {"method":"GET","path":"/consent-questions","contract":"marketing-crm","summary":"The consent questions a venue asks at booking","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCustomDomains": {"method":"GET","path":"/tenant-domains","contract":"white-label","summary":"The domains this tenant has claimed","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"CustomDomain"},
"listEvents": {"method":"GET","path":"/events","contract":"catalogue","summary":"List events","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGuidedChoices": {"method":"GET","path":"/venues/{venueId}/guided-choices","contract":"white-label","summary":"List a venue's Help me choose set-ups","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"source","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrgUnits": {"method":"GET","path":"/org-units","contract":"tenancy","summary":"List scope nodes visible to the session","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"under","in":"query","required":null},{"name":"level","in":"query","required":null},{"name":"includeInactive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPolicies": {"method":"GET","path":"/tenant-config/policies","contract":"white-label","summary":"List legal policies","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"includeHistory","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"Policy"},
"listPrincipals": {"method":"GET","path":"/principals","contract":"identity","summary":"List principals","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopePath","in":"query","required":null},{"name":"isActive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductCategories": {"method":"GET","path":"/product-categories","contract":"catalogue","summary":"The merchandise hierarchy — categories, brands, collections","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProductCategoryNode"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRoles": {"method":"GET","path":"/roles","contract":"identity","summary":"List roles","permission":"ROLE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishGuidedChoice": {"method":"POST","path":"/guided-choices/{guidedChoiceId}/publish","contract":"white-label","summary":"Publish a Help me choose set-up to guests","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuidedChoice"},
"publishTenantConfig": {"method":"POST","path":"/tenant-config/publish","contract":"white-label","summary":"Publish the working draft","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConfigVersion"},
"regenerateDomainToken": {"method":"POST","path":"/tenant-domains/{domainId}/token","contract":"white-label","summary":"Issue a new validation token","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CustomDomain"},
"relinquishCustomDomain": {"method":"DELETE","path":"/tenant-domains/{domainId}","contract":"white-label","summary":"Give the domain up","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"restoreConfigVersion": {"method":"POST","path":"/tenant-config/versions/{version}/restore","contract":"white-label","summary":"Restore a previous version","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TenantConfig"},
"setAnalyticsProvider": {"method":"PUT","path":"/tenant-config/analytics-providers","contract":"white-label","summary":"Connect the storefront and app to an analytics platform","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"StorefrontAnalyticsProvider","responds":"StorefrontAnalyticsProvider"},
"setBookingFlowConfig": {"method":"PUT","path":"/tenant-config/booking-flow","contract":"white-label","summary":"Set how the guest booking flow looks and steps","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BookingFlowConfig","responds":"BookingFlowConfig"},
"setConsentPurposes": {"method":"PUT","path":"/consent-purposes","contract":"marketing-crm","summary":"Configure consent purposes","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConsentPurposeConfig"},
"setLanguages": {"method":"PUT","path":"/tenant-config/languages","contract":"white-label","summary":"Set enabled languages and default","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LanguageConfig"},
"setPolicy": {"method":"PUT","path":"/tenant-config/policies/{policyKind}","contract":"white-label","summary":"Publish a policy version","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Policy"},
"setPrimaryDomain": {"method":"POST","path":"/tenant-domains/{domainId}/primary","contract":"white-label","summary":"Make a domain the primary one","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CustomDomain"},
"setPublishReviewPolicy": {"method":"PUT","path":"/publish-review-policy","contract":"white-label","summary":"Switch the publish review step on or off","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PublishReviewPolicy","responds":"PublishReviewPolicy"},
"setSeoMetadata": {"method":"PUT","path":"/seo-metadata","contract":"marketing-crm","summary":"Titles, descriptions, canonicals and hreflang","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SeoMetadata","responds":"SeoMetadata"},
"suggestGuidedChoice": {"method":"POST","path":"/venues/{venueId}/guided-choice-suggestions","contract":"ai","summary":"Suggest a Help me choose set-up from the venue's catalogue","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"unpublishGuidedChoice": {"method":"POST","path":"/guided-choices/{guidedChoiceId}/unpublish","contract":"white-label","summary":"Take a Help me choose set-up off the guest app","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuidedChoice"},
"updateConsentQuestion": {"method":"PATCH","path":"/consent-questions/{questionId}","contract":"marketing-crm","summary":"Reword, re-scope or retire a consent question","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConsentQuestion","responds":"ConsentQuestion"},
"updateGuidedChoice": {"method":"PATCH","path":"/guided-choices/{guidedChoiceId}","contract":"white-label","summary":"Edit a Help me choose set-up, or review a suggestion","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuidedChoice"},
"updatePrincipal": {"method":"PATCH","path":"/principals/{principalId}","contract":"identity","summary":"Update or deactivate a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Principal"},
"validateTenantConfig": {"method":"POST","path":"/tenant-config/validate","contract":"white-label","summary":"Validate the working draft","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConfigValidationReport"},
"verifyCustomDomain": {"method":"POST","path":"/tenant-domains/{domainId}/verify","contract":"white-label","summary":"Check the record and issue the certificate","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CustomDomain"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessibilitySettings": {"type":"object","description":"BL-065, 2.1.27. **POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated.**\n**A kiosk is the hard case.** A guest with low vision using a website brings their own assistive technology; a guest at a kiosk gets whatever the kiosk offers, so the settings have to be on the device rather than in the browser.\n","properties":{"largeTextAvailable":{"type":"boolean","default":true},"highContrastAvailable":{"type":"boolean","default":true},"simplifiedNavigationAvailable":{"type":"boolean","default":true},"screenReaderSupported":{"type":"boolean","default":true},"reachableHeightModeAvailable":{"type":"boolean","default":false,"description":"**Moves the interface to the lower half of the screen** for a guest using a wheelchair. A kiosk mounted at standing height is unusable otherwise, and no software setting fixes the mounting — this is the mitigation.\n"},"sessionTimeoutMultiplier":{"type":"number","default":1,"description":"**Timeouts are an accessibility barrier nobody counts.** A guest who needs three times as long to read a screen should not lose their basket to a 90-second inactivity timer.\n"}}},
"AiGuidedChoiceSuggestion": {"type":"object","x-ticvai-persistence":"ai.guided_choice_suggestion","description":"**One Help me choose suggestion for a venue** (design 3.11, decided 29 September; C7 at autonomy \"suggest\"). Holds the reasons: the products read, the one or two attributes chosen, the split each makes, the answer mapping and where the wording came from. Its `id` is the `suggestionRef` on the white-label draft (`white-label.proposeGuidedChoice`). Nothing is ever published from here.","required":["venueId","trigger","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"trigger":{"type":"string","enum":["productsUploaded","mappedProductWithdrawn","productsUncovered","manual"]},"status":{"type":"string","enum":["running","proposed","noSuggestion","failed","superseded"],"readOnly":true},"productCount":{"type":"integer","minimum":0,"readOnly":true},"questions":{"type":"array","items":{"type":"object","properties":{"attribute":{"type":"string","description":"The catalogue attribute asked about: audience, level, minimum height or age, duration, price band, format, language."},"order":{"type":"integer","minimum":1},"split":{"type":"object","additionalProperties":true,"description":"How evenly it divides the bookable products: products per answer."},"droppedBecause":{"type":"string","nullable":true,"description":"Set where an attribute was considered and dropped (an answer would leave nothing bookable)."},"answers":{"type":"array","items":{"type":"object","properties":{"value":{"type":"string"},"leadsTo":{"type":"string","enum":["product","category","flow"]},"targetRef":{"type":"string"}}}}}},"readOnly":true,"description":"The questions chosen, in the order asked. Deterministic: the same catalogue gives the same questions."},"wordingSource":{"type":"string","enum":["model","attributeNames"],"readOnly":true,"description":"Where the text came from. `attributeNames` when no model was available: the rules alone still make a usable draft."},"modelVersion":{"type":"string","nullable":true,"readOnly":true},"promptTemplateVersion":{"type":"string","nullable":true,"readOnly":true},"guidedChoiceId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The white-label draft `GuidedChoice` it produced."},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AppAvailability": {"type":"string","description":"**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n","enum":["open","soldOut","closed"],"default":"open"},
"AppIcons": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["sourceAssetRef","changeScope"],"properties":{"sourceAssetRef":{"type":"string","format":"uuid","description":"The `MediaAsset` id of the 1024×1024 source."},"derived":{"type":"array","readOnly":true,"x-ticvai-derived":"onWrite","description":"Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on `setAppIcons` (audit R163).","items":{"type":"object","properties":{"platform":{"type":"string","enum":["ios","android","web"]},"size":{"type":"string"},"assetRef":{"type":"string","format":"uuid"}}}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` — icons are baked into the binary."},"liveVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Icon currently shipped. Differs from the draft until the next release."},"requiresRebuild":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onRead","description":"True while the draft's source differs from the icon in `liveVersion`."}}},
"BookingConsentRecord": {"type":"object","x-ticvai-persistence":"marketing.booking_consent_record","description":"**One answer to one consent question, as given** (decided 29 September, rev 3 REV3-26). Append-only: a changed answer is a new record and this one gets `supersededAt`. Distinct from `ConsentRecord`, which is a guest's standing decision about a data-processing purpose; this is an answer given for a booking.\n","required":["id","questionId","questionVersion","questionKind","answer","scope","source","answeredAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"questionId":{"type":"string","format":"uuid"},"questionVersion":{"type":"integer","minimum":1},"questionKind":{"$ref":"#/components/schemas/ConsentQuestionKind"},"answer":{"type":"string","enum":["yes","no"]},"scope":{"type":"string","enum":["perPerson","perBooking"]},"blocksBooking":{"type":"boolean","readOnly":true,"description":"The answer is the question's `blockingAnswer` at that version."},"cartId":{"type":"string","format":"uuid","nullable":true},"cartLineId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Set by `orders.checkoutCart` when the cart becomes an order."},"orderLineId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"personIndex":{"type":"integer","minimum":0,"nullable":true},"personName":{"type":"string","maxLength":120,"nullable":true},"personSubjectId":{"type":"string","format":"uuid","nullable":true},"answeredBySubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The guest who answered, from the session. Null for an anonymous cart."},"answeredByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The staff member who answered on the guest's behalf."},"source":{"$ref":"#/components/schemas/ConsentSource"},"answeredAt":{"type":"string","format":"date-time"},"supersededAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"BookingFlow": {"x-ticvai-persistence":"whitelabel.booking_flow","type":"object","description":"**A venue's booking flow (decided 29 September, W12: operators pick their flows, see which steps are required, set their own order).** Made from a `BookingFlowType`; lives in the working draft and reaches guests with `publishTenantConfig`, which copies the venue's flows into the version's snapshot. A product or category names its flow (catalogue `bookingFlowId`); otherwise the venue's default for the type serving its kind applies.\n","required":["flowTypeKey","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createBookingFlowDefinition`."},"flowTypeKey":{"$ref":"#/components/schemas/BookingFlowTypeKey"},"name":{"type":"string","maxLength":80,"description":"Staff-facing, e.g. \"Day pass, date first\". Not shown to guests."},"isDefaultForType":{"type":"boolean","default":false,"description":"At most one per venue and type; setting it takes it from the previous default."},"isEnabled":{"type":"boolean","default":true,"description":"A disabled flow is kept and not published; products naming it fall back to the default."},"steps":{"type":"array","maxItems":30,"description":"Every step of the type, in the venue's order. Filled from the type when left out on create.","items":{"$ref":"#/components/schemas/BookingFlowStep"}},"settings":{"$ref":"#/components/schemas/BookingFlowLevelSettings"},"isValid":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. `publishTenantConfig` refuses a draft holding an invalid enabled flow."},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"BookingFlowConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","description":"**Set per tenant, with a per-venue override (decided 29 September, rev 3 CFG-11).** One tenant with several venues (the Kids Club branches, Coastal Aqua beside Union Arena) needs them to differ. The settings in force at a venue are the tenant's, with that venue's entry in `venueOverrides` laid over them field by field. The guest app resolves them for the venue the guest picked (audit R267); `effectiveForVenueId` on `getBookingFlowConfig` returns them resolved.\n","allOf":[{"$ref":"#/components/schemas/BookingFlowSettings"},{"type":"object","properties":{"venueOverrides":{"type":"array","maxItems":200,"default":[],"description":"Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. An override for a venue later closed is kept and has no effect.","items":{"$ref":"#/components/schemas/BookingFlowVenueOverride"}}}}]},
"BookingFlowLevelSettings": {"x-ticvai-persistence":"none — jsonb column on whitelabel.booking_flow","type":"object","description":"**The settings that belong to one flow, not to the venue (decided 29 September, W12).** Moved here from `BookingFlowSettings`, which keeps the venue-wide ones. Each keeps its rev 3 meaning and default. A field left out takes its default.\n","properties":{"performanceReveal":{"type":"string","enum":["dateTimeTicket","allAtOnce"],"default":"dateTimeTicket","description":"**Performance reveal (rev 3 REV3-2).** `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. Product-first (W8) is the step order of `experienceWorkshop`, not a value here.\n"},"signInAt":{"type":"string","enum":["afterAddOns","atPayment"],"default":"afterAddOns","description":"**Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3).** `afterAddOns` asks as the guest leaves the extras step; `atPayment` asks at payment. The basket is kept either way.\n"},"seatEventDateMode":{"type":"string","enum":["inlineStep","popupOnSeatMap"],"default":"inlineStep","description":"**Date and time on a seated event (rev 3 REV3-4).** `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. Read only by the seated flow types.\n"},"extrasStep":{"type":"string","enum":["auto","always","never"],"default":"auto","description":"`auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off."},"quickTour":{"type":"boolean","default":false,"description":"**Quick tour (rev 3 REV3-20).** A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. Seen-state kept on the device only.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"default":[],"description":"**The flow's own consent questions (rev 3 REV3-26).** Asked on every booking through this flow, together with those of each product in the cart, each question once. Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. A Help me choose answer may pre-fill one (`GuidedChoice` `consentPrefill`); the guest still confirms it.\n","items":{"type":"string","format":"uuid"}}}},
"BookingFlowSettings": {"type":"object","x-ticvai-persistence":"none — embedded in tenant_config","description":"**Every guest booking-flow setting, once.** `BookingFlowConfig` is these at tenant level plus `venueOverrides`; a `BookingFlowVenueOverride` carries any subset of them for one venue (decided 29 September, rev 3 CFG-11). The Rev 3 settings (`timesPerPage` onwards) are the options the client's rev 3 prototype shows under Config → Booking rules and Build your experience.\n**Venue-wide only (decided 29 September, W12).** The settings that belong to one flow moved to `BookingFlowLevelSettings` on each `BookingFlow`; `categoryDisplay` was removed (W7).\n","properties":{"preset":{"type":"string","enum":["auto","ticketBox","playCentre","venueSite","marketplace","singleEvent","season","custom"],"default":"auto","description":"L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. The UI preset of the prototype's drawer (rev 3 CFG-1, no change)."},"stepIndicator":{"type":"string","enum":["bar","numbered","dots","segmented","breadcrumb","pills","ticks","none"],"default":"bar"},"cartLayout":{"type":"string","enum":["sidebarRight","sidebarLeft","slideInRight","slideUpBottom","singleColumn","floatingIcon"],"default":"sidebarRight","description":"`floatingIcon` is a round basket button with the item count that opens the cart (decided 29 September, rev 3 REV3-10). Which side a sidebar or the icon sits on in a right-to-left language is `cartSideInRtl`."},"cartSideInRtl":{"type":"string","enum":["keepRight","mirror"],"default":"keepRight","description":"**The cart side when the guest reads Arabic or another right-to-left language (decided 29 September, rev 3 REV3-10).** `keepRight` keeps the cart (and the floating icon) on the right, as the client confirmed; `mirror` flips it to the left with the rest of the layout.\n"},"cardLayout":{"type":"string","enum":["stackedRows","splitRows","cardsAcross","posterCards"],"default":"stackedRows","description":"How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked rows, Split rows, Cards across and Poster cards."},"cardSize":{"type":"string","enum":["compact","standard","large","extraLarge"],"default":"compact","description":"Labels Compact, Standard, Large, Extra large (decided 29 September, rev 3 DG-6). `standard` replaces `regular`."},"seatPicker":{"type":"string","enum":["bowl","zonesThenSeats","zonesOnly","seatsOnly"],"default":"bowl","description":"Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event."},"mapView":{"type":"string","enum":["2d","3d"],"default":"3d"},"density":{"type":"string","enum":["compact","standard","roomy"],"default":"compact","description":"Labels Compact, Standard, Roomy, default Compact as the design has it (decided 29 September, rev 3 DG-6). `standard` and `roomy` replace `comfortable` and `airy`."},"embedMode":{"type":"string","enum":["fullPage","embedded"],"default":"fullPage","description":"`embedded` hides the hero banner, event page and venue header, for a flow placed inside the venue's own site."},"heroBanner":{"type":"boolean","default":true},"searchInBanner":{"type":"boolean","default":false,"description":"Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6)."},"eventBannerDates":{"type":"boolean","default":false,"description":"**Dates in event banner (decided 29 September, rev 3 23SEP-19).** On, the event banner lists the next dates; off by default. Either way the date picker sits at the top of the booking step.\n"},"singleEventPage":{"type":"boolean","default":false},"quantitiesOnAddOns":{"type":"boolean","default":true},"timesPerPage":{"type":"string","enum":["8","12","24","all"],"default":"24","description":"**Times per page (decided 29 September, rev 3 REV3-1).** When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` shows every one. A string because `all` is one of the values.\n"},"dayPartFilter":{"type":"boolean","default":true,"description":"**Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1).** Where each part begins is `dayPartBoundaries`.\n"},"dayPartBoundaries":{"type":"object","description":"**Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1).** Morning is before `afternoonStartsAt`, afternoon runs to `eveningStartsAt`, evening is from `eveningStartsAt`. A venue sets its own through `venueOverrides`. `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400.\n","properties":{"afternoonStartsAt":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","default":"12:00"},"eveningStartsAt":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","default":"17:00"}}},"seatViewPosition":{"type":"string","enum":["bottom","right","left","top"],"default":"bottom","description":"**Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5).** Web only; on mobile and on a narrow screen it is always below the map.\n"},"seatTimeBar":{"type":"boolean","default":true,"description":"**Time bar above the seat map (decided 29 September, rev 3 REV3-6).** Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one.\n"},"ticketCategories":{"type":"string","enum":["categoryThenSubcategory","flatList"],"default":"categoryThenSubcategory","description":"**How tickets are grouped (decided 29 September, rev 3 REV3-16).** `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once.\n"},"ticketTags":{"type":"boolean","default":true,"description":"**Tags on tickets (decided 29 September, rev 3 23SEP-3).** Shows a product's display tags (such as \"2 Hours\", \"Min 1.10 m\", \"Valid 90 days\") on its card.\n"},"cardInfo":{"type":"boolean","default":true,"description":"**Extra info on cards (decided 29 September, rev 3 23SEP-6).** Shows each ticket type's description, who it is for and what it includes, under its name.\n"},"conciergeMascot":{"type":"boolean","default":true,"description":"**The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5).** Read only where the `aiConciergeChat` feature is on.\n"},"showInfoOnly":{"type":"boolean","default":true,"description":"**Show info-only products (decided 29 September, rev 3 REV3-14).** On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it.\n"},"locationSwitcher":{"type":"boolean","default":false,"description":"**Location switcher (decided 29 September, rev 3 REV3-18).** On, the booking screens carry a \"Booking at\" bar with Change location, reusing the guest's venue choice (audit R267). Off unless the tenant or venue enables it; it has no effect for a tenant with one venue.\n"},"guestContactFields":{"type":"array","minItems":1,"maxItems":3,"uniqueItems":true,"default":["email"],"items":{"type":"string","enum":["email","mobile","name"]},"description":"**What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1).** The prototype's Email only, + name and + mobile. Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.matchBy`), or 400. After the code is verified the guest is not asked for these again: the flow goes to the terms and payment, and the profile is completed later (WEB-020, GST-039). Read only where the `guestCheckout` feature is on.\n"},"dateStripDays":{"type":"integer","minimum":3,"maximum":31,"default":7,"description":"**The date strip (decided 17 September, M17-08).** How many days from today the date step shows as a strip before the calendar icon that opens the full month; later dates are picked from the calendar.\n"}}},
"BookingFlowStep": {"x-ticvai-persistence":"whitelabel.booking_flow_step","type":"object","description":"One step of a venue's flow, in the venue's order (decided 29 September, W12).","required":["stepKey","enabled","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"bookingFlowId":{"type":"string","format":"uuid","readOnly":true},"stepKey":{"$ref":"#/components/schemas/BookingFlowStepKey"},"enabled":{"type":"boolean","description":"A `required` step cannot be off; the flow saves and `isValid` turns false."},"sortOrder":{"type":"integer","minimum":0},"requirement":{"type":"string","enum":["required","optional","conditional"],"readOnly":true,"x-ticvai-derived":"onRead","description":"From the flow type, so the CMS can mark the step without a second read."},"settings":{"type":"object","additionalProperties":true,"default":{},"description":"The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. `languages` on `language`, `minHours` on `duration`). A name the type does not give is refused with 400."}}},
"BookingFlowTypeKey": {"type":"string","description":"**The flow types the system catalogue offers (decided 29 September, W12; impact.md b).** `seatedFixedPerformance` and `seatedDateTimeSeatMap` are the two seated flows; `cabanaMap` and `cabanaBySize` are the two cabana flows (W6); `experienceWorkshop` puts the product before the date (W8); `multiLocation` opens on the location switcher.\n","enum":["datedDayPass","timedEntry","openDated","seatedFixedPerformance","seatedDateTimeSeatMap","experienceWorkshop","surfSession","meetingRoomHourly","cabanaMap","cabanaBySize","guidedTourByLanguage","transport","tableReservation","membership","giftCard","multiLocation"]},
"BookingFlowVenueOverride": {"type":"object","x-ticvai-persistence":"none — embedded in tenant_config","description":"**One venue's booking-flow settings where they differ from the tenant's (decided 29 September, rev 3 CFG-11).** `settings` carries only the fields the venue changes; a field left out inherits the tenant value, and the schema defaults do not apply inside an override.\n","required":["venueId","settings"],"properties":{"venueId":{"type":"string","format":"uuid","description":"One of the tenant's active venues. At most one override per venue."},"settings":{"$ref":"#/components/schemas/BookingFlowSettings"}}},
"BrandIdentity": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","description":"Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB (decided 28 September, audit R270).\n","required":["logoAssetRef"],"properties":{"logoAssetRef":{"type":"string","format":"uuid","description":"The primary logo."},"logoDarkAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"Used on dark backgrounds. Falls back to the primary logo."},"logoVariant":{"type":"string","enum":["light","dark","duotone"],"default":"light","description":"**Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4).** `light` uses `logoAssetRef`, `dark` uses `logoDarkAssetRef` (falling back to the primary logo), and `duotone` the two-colour reading of the primary logo.\n"},"faviconAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"The browser tab icon for the guest web app."},"splashImageAssetRefs":{"type":"array","description":"Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163).","items":{"type":"string","format":"uuid"}},"splashDurationSeconds":{"type":"integer","minimum":0,"maximum":10,"default":3},"splashBackgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"showLoadingIndicator":{"type":"boolean","default":true},"splashChangeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163)."},"introVideoAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"**The optional intro video (decided 29 September, MOB-5).** A video `MediaAsset` from the media library (CMS-010). Streamed, so a change reaches guests with the publish and needs no app build.\n"},"introVideoMode":{"type":"string","enum":["off","firstLaunch","everyLaunch"],"default":"off","description":"When GST-001 plays it full screen. \"Skip introduction\" is always shown. Anything but `off` needs `introVideoAssetRef`, or 400."},"showPoweredBy":{"type":"boolean","default":true,"description":"**\"Powered by TICVAI\", a configuration toggle, on by default** (Chinmay, 2 October, workbook Q160 and the pre-apply round; consistent with DI-297; CHG-CSA-036). Shown on the launch screen and at the foot of Account and the web footer while true. **Switching it off needs the tenant's licence to allow it**: `setBrandIdentity` refuses `false` with `403 powered-by-locked` unless the tenant's plan carries the `poweredByRemoval` add-on (subscription `LicencePosition.poweredByRemovable`)."}}},
"ChangeScope": {"type":"string","description":"Whether a change reaches guests on publish or needs a store release.\n","enum":["runtime","buildTime"]},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ConfigDiff": {"x-ticvai-persistence":"none — computed","type":"object","required":["fromVersion","toVersion","changes"],"properties":{"fromVersion":{"type":"string"},"toVersion":{"type":"string"},"changes":{"type":"array","items":{"type":"object","required":["area","path","changeKind"],"properties":{"area":{"type":"string"},"path":{"type":"string"},"changeKind":{"type":"string","enum":["added","removed","modified"]},"before":{"type":"string","nullable":true},"after":{"type":"string","nullable":true},"changeScope":{"$ref":"#/components/schemas/ChangeScope"}}}}}},
"ConfigFindingKind": {"type":"string","enum":["missingTranslation","navigationTargetsDisabledModule","homepageReferencesMissingContent","contrastFailure","missingRequiredAsset","policyVersionMissing","noVisibleNavigationItems","unlicensedModuleEnabled","arabicFontMissing","bookingFlowInvalid","bookingFlowMissing"]},
"ConfigValidationReport": {"x-ticvai-persistence":"none — computed","type":"object","required":["passed","errorCount","warningCount","findings"],"properties":{"passed":{"type":"boolean"},"errorCount":{"type":"integer"},"warningCount":{"type":"integer"},"findings":{"type":"array","items":{"type":"object","required":["kind","severity","message"],"properties":{"kind":{"$ref":"#/components/schemas/ConfigFindingKind"},"severity":{"type":"string","enum":["error","warning"]},"message":{"type":"string"},"area":{"type":"string"},"reference":{"type":"string","nullable":true}}}}}},
"ConfigVersion": {"x-ticvai-persistence":"whitelabel.config_version","type":"object","required":["version","publishedAt","publishedByPrincipalId","note","isCurrent"],"properties":{"version":{"type":"string"},"publishedAt":{"type":"string","format":"date-time"},"publishedByPrincipalId":{"type":"string","format":"uuid"},"publishedByName":{"type":"string"},"note":{"type":"string"},"reviewStatus":{"type":"string","readOnly":true,"enum":["notRequired","pending","approved","rejected"],"default":"notRequired","description":"The review step, where the tenant's publish-review policy is on (CHG-CSA-042)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"isCurrent":{"type":"boolean"},"scheduledFor":{"type":"string","format":"date-time","nullable":true},"contentHash":{"type":"string"},"pendingBuildTimeChanges":{"type":"array","description":"Changes in this version that will not reach guests until the next store release. Surfaced at publish so nobody expects a new icon tomorrow.\n","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"platforms":{"type":"array","items":{"type":"string","enum":["ios","android","web"]}}}}},"snapshot":{"type":"object","additionalProperties":true,"readOnly":true,"description":"**What this version contained.** The working draft exactly as published, in the shape `getTenantConfig` returns (`TenantConfig`) — so `restoreConfigVersion` has something to copy back and `diffConfigVersion` something to compare. Deliberately an open object here: its shape is `TenantConfig`, and a `$ref` would make it a key to a `tenant_config` row rather than a copy. Written once by `publishTenantConfig` and never changed. Left out of `listConfigVersions` items; a version's content is read with `getTenantConfig?version=`.\n"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"ConsentPurposeConfig": {"x-ticvai-persistence":"marketing.consent_purpose + marketing.consent_purpose_channel","type":"object","required":["purpose","channels","noticeVersion","isRequiredForService"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"displayName":{"type":"string"},"description":{"type":"string"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","description":"Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured.\n"},"isRequiredForService":{"type":"boolean","description":"True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently.\n"},"expiresAfterMonths":{"type":"integer","nullable":true}}},
"ConsentQuestion": {"type":"object","x-ticvai-persistence":"marketing.consent_question + marketing.consent_question_version","description":"**A venue-defined consent question asked at booking** (decided 29 September, rev 3 REV3-26). Each version's text is kept in `consent_question_version`, so an answer always points at the exact words the guest saw. Attached to products by the catalogue and to booking flows by the white-label flow configuration; one or several per flow, as the venue chooses.\n","required":["id","kind","text","version","scope","required","blockingAnswer","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ConsentQuestionKind"},"text":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"The question as the guest reads it, per locale."},"helpText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"version":{"type":"integer","minimum":1,"readOnly":true,"description":"Raised by one each time the question changes (`updateConsentQuestion`)."},"scope":{"type":"string","enum":["perPerson","perBooking"],"default":"perPerson","description":"Asked for each declared person, or once for the whole booking."},"required":{"type":"boolean","default":true,"description":"Checkout waits until it is answered (`orders.checkoutCart` 422 `consentRequired`)."},"blockingAnswer":{"type":"string","enum":["yes","no","none"],"default":"none","description":"The answer that stops the booking, for the person or the booking it covers. `none` records the answer and blocks nothing."},"status":{"type":"string","enum":["active","retired"],"default":"active"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ConsentQuestionKind": {"type":"string","description":"What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others are recorded and checked as the venue set them.","enum":["swim","scuba","risk","custom"]},
"ConsentSource": {"type":"string","enum":["guestApp","website","kiosk","pos","callCentre","import","agentRecorded","cookieBanner","checkout"],"description":"`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."},
"CustomDomain": {"type":"object","x-ticvai-persistence":"whitelabel.custom_domain","description":"24 August. **`ADM-017 Domain & Certificate Management` declared 41 operations and not one of them was about a domain** — it carried the same bulk-attached set as every other white-label screen, and **no domain or certificate operation existed anywhere in 1,010.**\nA white-label platform whose tenants cannot use their own domain is a white-label platform in name only.\n**Verification before issuance, always.** A certificate issued for a domain the tenant does not control is a certificate issued to whoever asked.\n","required":["id","tenantId","hostname","status"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"hostname":{"type":"string"},"kind":{"type":"string","enum":["guestWeb","guestApp","partnerPortal","developerPortal"]},"status":{"type":"string","enum":["pending","verifying","verified","issuing","active","failed","expired","revoked"]},"verificationMethod":{"type":"string","enum":["dnsTxt","cname","httpFile"]},"verificationToken":{"type":"string","readOnly":true},"verificationRecord":{"type":"object","readOnly":true,"description":"**The record the tenant must publish**, which `claimCustomDomain` promises and the claim had nowhere to hold. Set when the claim is made, from `hostname`, `verificationMethod` and `verificationToken`: a TXT record for `dnsTxt`, a CNAME for `cname`, and for `httpFile` the URL path to serve and the file's content.\n","required":["type","name","value"],"properties":{"type":{"type":"string","enum":["TXT","CNAME","httpFile"]},"name":{"type":"string","description":"The DNS name to create, or for `httpFile` the URL path on `hostname`."},"value":{"type":"string","description":"The record's value, CNAME target or file content."}}},"certificateExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**Renewal is a job, not a reminder.** A certificate that expires on a Saturday takes a tenant's storefront down, and nobody reads a reminder email on a Saturday.\n"},"lastCheckedAt":{"type":"string","format":"date-time","nullable":true},"failureReason":{"type":"string","nullable":true},"routing":{"type":"string","enum":["cname","delegatedSubdomain","apex"],"default":"cname","description":"**How the hostname reaches TICVAI** (Chinmay, 2 October: \"subdomain plus CNAME\"; CHG-CSA-043). `cname`, the default: a CNAME (e.g. `tickets.venue.com`) straight to the Front Door endpoint, validated by the TXT `_dnsauth` record, with a Front Door managed certificate. `delegatedSubdomain`: the tenant delegates a subdomain to TICVAI's name servers (NS). `apex`: the bare domain, only on request. There is no path proxy."},"dnsRecords":{"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","type":"array","readOnly":true,"description":"**Every record the tenant must publish, with what is observed now** (CHG-CSA-043): the TXT `_dnsauth` record, the CNAME, and CAA or NS where they apply. CMS-017 lists them with their status.","items":{"type":"object","required":["type","name","expectedValue","status"],"properties":{"type":{"type":"string","enum":["TXT","CNAME","CAA","NS"]},"name":{"type":"string"},"expectedValue":{"type":"string"},"observedValue":{"type":"string","nullable":true},"status":{"type":"string","enum":["ok","missing","wrong"]}}}},"revalidation":{"type":"string","readOnly":true,"enum":["none","pendingRevalidation","timedOut"],"default":"none","description":"**The two waits CMS-017 shows beside `status`** (CHG-CSA-043). `pendingRevalidation`: an `active` domain whose validation must be renewed (the managed certificate's periodic revalidation, or a record that changed); it keeps serving while the job re-checks. `timedOut`: a claim whose records were not published within the validation window; `regenerateDomainToken` starts it again. Kept beside `status`, not inside it, because a new status value would break a client built at r1 (CHG-CSA-043 notes)."},"cnameLost":{"type":"boolean","readOnly":true,"description":"**Takeover warning** (CHG-CSA-043). True when a scheduled check finds that an `active` or released hostname's CNAME still points at TICVAI with no tenant serving it, or no longer points at us while `active`. Relinquishing a domain tells the tenant to remove the CNAME first, so nobody else can claim the dangling record."},"isPrimary":{"type":"boolean","readOnly":true,"description":"The tenant's primary domain for its `kind`; the others redirect to it (`setPrimaryDomain`)."},"readiness":{"type":"object","readOnly":true,"description":"**Per-domain setup a guest needs** (CHG-CSA-043): the UAE Pass redirect URI registered for this hostname, the Apple Pay merchant domain verified, and the app links (Apple app-site association, Android asset links) served.","properties":{"uaePassRedirect":{"type":"string","enum":["ready","pending","notApplicable"]},"applePayDomain":{"type":"string","enum":["ready","pending","notApplicable"]},"appLinks":{"type":"string","enum":["ready","pending","notApplicable"]}}}}},
"Event": {"x-ticvai-persistence":"catalogue.event","type":"object","required":["id","code","name","venueId","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentEventId":{"type":"string","format":"uuid","nullable":true,"description":"For grouped events."},"performanceCount":{"type":"integer","readOnly":true,"description":"How many performances the event has. Counted by the server; never sent by a client."},"isActive":{"type":"boolean"}}},
"FeatureToggle": {"x-ticvai-persistence":"whitelabel.feature_toggle","type":"object","required":["featureKey","isEnabled","changeScope"],"properties":{"featureKey":{"allOf":[{"$ref":"#/components/schemas/FeatureKey"}],"description":"`guestCheckout` is **off by default** (decided 17 September 2026, matrix 2.6.28, placement settled by [ADR-0045](../../docs/adr/0045-every-order-carries-a-proven-contact.md) 18 September): **the venue sets this from the configuration menu**, and it decides which routes the checkout page offers — off, the guest signs in verified at checkout; on, a guest may also check out without an account after proving their contact with a one-time code. **It gates checkout, never the cart.** The kiosk is not governed by it. Rule on `identity` `verifyGuestEmail`.\n"},"displayName":{"type":"string"},"isEnabled":{"type":"boolean"},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Wallet and payment integrations are `buildTime` on native apps — enabling one needs a release, not a publish.\n"},"requiresConfiguration":{"type":"boolean","description":"True where the feature needs credentials or setup elsewhere first."}}},
"FontConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["primaryLatin"],"properties":{"primaryLatin":{"type":"string"},"primaryArabic":{"type":"string","nullable":true,"description":"Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match.\n"},"secondaryLatin":{"type":"string","nullable":true},"secondaryArabic":{"type":"string","nullable":true,"description":"Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163)."},"customFontAssetRefs":{"type":"array","description":"Uploaded font files, as `MediaAsset` ids.","items":{"type":"string","format":"uuid"}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"x-ticvai-derived":"onRead","description":"Custom font files are `buildTime`; selecting a bundled face is `runtime`."}}},
"FooterConfig": {"type":"object","x-ticvai-persistence":"whitelabel.footer_config + whitelabel.footer_config_column + whitelabel.footer_config_social_link","description":"BL-002. **`setHeader` and `HeaderConfig` exist and the footer does not**, which looked like symmetry until you notice it is not: **a header is chrome and a footer is a link surface.**\nA footer carries the legal links — terms, privacy, accessibility statement, cookie preferences — and **those are the ones a regulator checks.** Treating it as a mirror of the header would have given it a logo and no way to reach a privacy notice.\n**Where it is stored.** `legalLinks` and `copyrightText` are columns of `whitelabel.footer_config`; each entry of `columns` is a `whitelabel.footer_config_column` row and each entry of `socialLinks` a `whitelabel.footer_config_social_link` row. Part of the working draft (see the header). **In the tenant's own database, not the control plane (decided 28 September, audit R163)**: it moved from `control.footer_config` and its two child tables.\n","required":["id","scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `tenant` scope by the server."},"columns":{"type":"array","items":{"type":"object","properties":{"heading":{"type":"string"},"links":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string"},"url":{"type":"string"},"opensCookiePreferences":{"type":"boolean","default":false}}}}}}},"legalLinks":{"type":"object","description":"**Required links, held separately from the free-form columns** — a tenant reorganising their footer must not be able to remove the privacy notice by accident.\n","properties":{"termsUrl":{"type":"string"},"privacyUrl":{"type":"string"},"accessibilityUrl":{"type":"string","nullable":true},"cookiePolicyUrl":{"type":"string","nullable":true}}},"copyrightText":{"type":"string"},"socialLinks":{"type":"array","items":{"type":"object","properties":{"platform":{"type":"string"},"url":{"type":"string"}}}}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"GuidedChoice": {"x-ticvai-persistence":"whitelabel.guided_choice + whitelabel.guided_choice_question + whitelabel.guided_choice_answer","type":"object","description":"**Help me choose (decided 29 September, rev 3 REV3-11).** A venue's short set of questions that ends on a result card opening the booking flow, product, category or event that fits. Each question has a few answers with a title, a one-line body, an icon and an optional badge; **the answer the guest picks on the last question decides the result**, and each earlier answer carries a target too, so a one-question setting still ends on a result. Venue configuration, never hard-coded: set up in Venue Management, off unless the venue publishes one.\n**Two sources, one review.** `manual` is written by staff; `aiSuggested` is proposed by the `ai` service from the venue's uploaded products (a suggestion, reviewed and published by a person, never auto-published). Both arrive as `draft`.\n**Help me choose filters the catalogue (decided 29 September, W4).** With `behaviour` `filter`, the default, each answer's `filter` narrows the products the guest sees (web, mobile and kiosk alike, through catalogue `listProducts` and `searchCatalogue` `guidedAnswerIds`), with a \"Show everything\" link; `recommend` keeps the rev 3 result card from the last answer's `target`. **It is never a consent step**: an answer may pre-fill a REV3-26 consent question (`consentPrefill`), which the guest still confirms, so the question is not asked twice and the consent stays explicit.\n","required":["id","venueId","name","mode","questions","status","source"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createGuidedChoice`."},"name":{"type":"string","maxLength":80,"description":"Staff-facing name, e.g. \"Water park day planner\". Not shown to guests."},"mode":{"type":"string","enum":["button","popupOnArrival","off"],"default":"button","description":"**How the guest reaches it (rev 3 REV3-11).** `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on the guest's first arrival at the booking page (whether it was seen is kept on the device only); `off` keeps a published choice configured but not shown.\n"},"showBanner":{"type":"boolean","default":true,"description":"The dark banner under the products (\"Choose from the experiences above or let us help you decide\") with a Help me choose button. Ignored when `mode` is `off`."},"behaviour":{"type":"string","enum":["filter","recommend"],"default":"filter","description":"**`filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4).** With `filter`, every answer needs a `filter` and `target` is optional; with `recommend`, every answer on the last question needs a `target`. `publishGuidedChoice` refuses the other case with 422.\n"},"showEverything":{"type":"boolean","default":true,"description":"The \"Show everything\" link under a filtered list, which clears the answers (W4)."},"questions":{"type":"array","minItems":1,"maxItems":4,"description":"**One to four questions** (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). Shown in `sortOrder`.\n","items":{"type":"object","required":["title","sortOrder","answers"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7. The row's own key."},"title":{"$ref":"#/components/schemas/LocalisedText"},"kind":{"type":"string","enum":["choice","yesNo","age","level","certification"],"default":"choice","description":"**What the question asks (decided 29 September, W4).** `choice` free answers; `yesNo` two answers (e.g. \"Can everyone swim?\"); `age` answers carrying an age range; `level` answers carrying a level tag; `certification` answers saying whether the guest holds a certificate (e.g. a diving licence). The kind decides which `filter` fields its answers use.\n"},"sortOrder":{"type":"integer","minimum":0},"answers":{"type":"array","minItems":2,"maxItems":4,"description":"Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11).","items":{"type":"object","required":["title","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7. The row's own key."},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"The one-liner under the title, at most 140 characters in each language."},"icon":{"type":"string","maxLength":40,"nullable":true,"description":"An icon name from the guest app's icon set."},"badge":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Optional, e.g. \"Best value\". At most 24 characters in each language."},"sortOrder":{"type":"integer","minimum":0},"target":{"allOf":[{"$ref":"#/components/schemas/GuidedChoiceTarget"}],"nullable":true,"description":"Required with `behaviour` `recommend` on the last question; optional with `filter`, where it is the card shown above the filtered list."},"filter":{"type":"object","nullable":true,"description":"**What this answer keeps in the list (decided 29 September, W4).** Every field set must hold; answers to different questions are combined with AND. Required with `behaviour` `filter`. The server applies it (catalogue `guidedAnswerIds`), so web, mobile and kiosk show the same list.\n","properties":{"productIds":{"type":"array","items":{"type":"string","format":"uuid"}},"productCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"segmentTags":{"type":"array","description":"Catalogue `Product.segmentTags`, e.g. a level tag.","items":{"type":"string"}},"minAgeYears":{"type":"integer","minimum":0,"nullable":true},"maxAgeYears":{"type":"integer","minimum":0,"nullable":true,"description":"With `minAgeYears`, checked against each product's age rule (catalogue `ProductEligibilityRule`)."},"requiresSwimmer":{"type":"boolean","nullable":true,"description":"False hides products whose eligibility needs a swimmer; true keeps only those."},"certificationCode":{"type":"string","nullable":true,"maxLength":40,"description":"Keeps products that need this certificate, or with `holdsCertification` false, hides them."},"holdsCertification":{"type":"boolean","nullable":true}}},"consentPrefill":{"type":"object","nullable":true,"description":"**Pre-fills a REV3-26 consent question from this answer (decided 29 September, W4).** The guest still ticks it at the consent step; nothing is recorded as consent until they do.\n","required":["consentQuestionId","answer"],"properties":{"consentQuestionId":{"type":"string","format":"uuid"},"answer":{"type":"boolean"}}},"result":{"type":"object","nullable":true,"description":"The result card when this answer decides the result. Absent fields fall back to the target's own name, summary and image.","properties":{"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedText"},"imageAssetRef":{"type":"string","format":"uuid","nullable":true}}}}}}}}},"status":{"allOf":[{"$ref":"#/components/schemas/GuidedChoiceStatus"}],"readOnly":true},"source":{"type":"string","enum":["manual","aiSuggested"],"readOnly":true,"description":"`manual` when staff created it; `aiSuggested` when the `ai` service proposed it (a service caller). Kept after a person edits a suggestion, so a report can say how many AI proposals were published."},"suggestionRef":{"type":"string","nullable":true,"readOnly":true,"description":"For `aiSuggested`, the id of the `ai` job that proposed it. Null for `manual`."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"publishedBy":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The person who published it. Never a service."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GuidedChoiceStatus": {"type":"string","description":"**Draft until a person publishes it (decided 29 September, rev 3 REV3-11).** Guests see only a `published` choice. An AI-proposed choice arrives as `draft` and is never published by the system. Moves as `states/guided-choice.yaml` says: `publishGuidedChoice` and `unpublishGuidedChoice`, and a publish returns the venue's previously published choice to `draft`.\n","enum":["draft","published"],"default":"draft"},
"GuidedChoiceTarget": {"x-ticvai-persistence":"none — embedded","type":"object","description":"**What an answer opens (decided 29 September, rev 3 REV3-11).** A product (its kind picks the booking flow), a product category (its tickets, as `ticketCategories` shows them), an event, or a module such as `membership`. Each id must belong to the choice's venue and be on sale or enabled when the choice is published, or `publishGuidedChoice` refuses it.\n","required":["kind"],"properties":{"kind":{"type":"string","enum":["product","productCategory","event","module","bookingFlow"]},"productId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `product`. A catalogue `Product`."},"productCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `productCategory`. A catalogue `ProductCategory`."},"eventId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `event`."},"moduleKey":{"allOf":[{"$ref":"#/components/schemas/ModuleKey"}],"nullable":true,"description":"Required when `kind` is `module`. The module must be enabled."},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `bookingFlow` (decided 29 September, W12; BUILD-YOUR-EXPERIENCE \"each answer points to one booking flow\"). One of the venue's enabled `BookingFlow`s."}}},
"HeaderConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["layout"],"properties":{"layout":{"type":"string","enum":["logoLeft","logoCentre","logoWithMenu"]},"showLogo":{"type":"boolean","default":true},"showMenu":{"type":"boolean","default":true},"showNotifications":{"type":"boolean","default":true},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},
"HomepageLayout": {"x-ticvai-persistence":"whitelabel.homepage_section","type":"object","description":"**The client-approved web and app wireframes are the layout** (Chinmay, 2 October, workbook Q163; CHG-CSA-040): sections, their order and their options follow the approved wireframes and change only where the spec breaks. **Landing-page templates** (workbook Q41 batch 2; CHG-CSA-037): a tenant with no landing page of its own starts from a TICVAI template (`templateKey`, `listLandingPageTemplates`); a tenant with its own site links into the storefront with deep links (`getDeepLinkScheme`, `buildDeepLink`).","required":["sections"],"properties":{"templateKey":{"type":"string","nullable":true,"description":"The landing-page template this layout started from (`listLandingPageTemplates`), or null for a layout composed from scratch (CHG-CSA-037)."},"landingSource":{"type":"string","enum":["storefront","ownSite"],"default":"storefront","description":"`storefront`: this home is the tenant's landing page. `ownSite`: the tenant's own website is the landing page and links in with deep links; this home is still served at the storefront address."},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"sections":{"type":"array","items":{"type":"object","required":["kind","sortOrder","isVisible"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"kind":{"$ref":"#/components/schemas/HomepageSectionKind"},"title":{"$ref":"#/components/schemas/LocalisedText"},"sortOrder":{"type":"integer"},"isVisible":{"type":"boolean"},"contentPageId":{"type":"string","format":"uuid","nullable":true},"maxItems":{"type":"integer","nullable":true,"description":"**How many cards the section shows, the venue's choice** (Chinmay, 2 October, workbook Q152: every customisation option of the approved wireframe, including the card count per section; CHG-CSA-040). Replaces the fixed 1 or 2 highlights of MOB-3: the CMS offers the counts the approved wireframe offers."},"scrollAnimation":{"type":"string","enum":["rise","scale","slide","blur","none"],"default":"rise","description":"**How the section enters as the guest scrolls** (Chinmay, 2 October, workbook Q153: \"must be there\"; DI-1088; CHG-CSA-040). Rise, Scale, Slide, Blur or None, as the v4 prototype offers; `none` for guests who asked the device for reduced motion is applied whatever is set."},"heroStyle":{"type":"string","nullable":true,"enum":["carousel","video","poster","split",null],"description":"For `heroBanner` only (decided 29 September, MOB-3)."}}}}}},
"LanguageConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["languages","defaultLanguage"],"properties":{"languages":{"type":"array","description":"**A tenant may add or select interface languages beyond English and Arabic** (Chinmay, 2 October, workbook Q145; CHG-CSA-039). Any ISO 639-1 language. English and Arabic ship with complete interface strings; for any other, the interface strings come as a TICVAI string pack drafted by AI translation and reviewed (T03), and a string with no translation falls back to English. Content (pages, products, banners) is the tenant's to translate (`translationGaps`).","items":{"type":"string","pattern":"^[a-z]{2}$"}},"defaultLanguage":{"type":"string","pattern":"^[a-z]{2}$"},"uiStringCoverage":{"type":"array","readOnly":true,"description":"How complete the interface strings are in each enabled language (CHG-CSA-039). English and Arabic are always complete.","items":{"type":"object","properties":{"language":{"type":"string"},"coveragePercent":{"type":"number","minimum":0,"maximum":100},"status":{"type":"string","enum":["complete","draft","missing"]}}}},"rtlLanguages":{"type":"array","readOnly":true,"x-ticvai-derived":"onRead","description":"The enabled languages written right to left — those whose Unicode CLDR character order is `right-to-left` (Arabic, `ar`, among them). Not configured; it follows from `languages`.","items":{"type":"string","pattern":"^[a-z]{2}$"}},"translationGaps":{"type":"array","readOnly":true,"description":"Content lacking a version in an enabled language.","items":{"type":"object","properties":{"language":{"type":"string"},"missingCount":{"type":"integer"},"areas":{"type":"array","items":{"type":"string"}}}}}}},
"LocalisedRichText": {"x-ticvai-persistence":"none — jsonb column","type":"object","description":"Keyed by language code. Values are sanitised HTML.","additionalProperties":{"type":"string"}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MinimumAppVersion": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n","properties":{"ios":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"},"android":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"}}},
"ModuleEnablement": {"x-ticvai-persistence":"whitelabel.module_enablement","type":"object","required":["moduleKey","isLicensed","isEnabled"],"properties":{"moduleKey":{"$ref":"#/components/schemas/ModuleKey"},"displayName":{"type":"string"},"isLicensed":{"type":"boolean","description":"From the tenant's subscription. False makes enablement impossible."},"isEnabled":{"type":"boolean"},"referencedBy":{"type":"array","readOnly":true,"x-ticvai-derived":"onWrite","description":"Navigation items and homepage sections pointing at this module. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write.","items":{"type":"string"}}}},
"NavigationConfig": {"x-ticvai-persistence":"whitelabel.navigation_item","type":"object","description":"**The mobile tab set is venue configuration (decided 29 September, MOB-1; 29 September brief decision 6).** Before a tenant saves its own, `bottomNavigation` is Home, Explore, Plan and Tickets (each an `appSection` link), with the Buy tickets button beside them; Map is an optional tab. Plan is left out while `visitPlanner` is off.\n","required":["kind","items"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"kind":{"type":"string","enum":["bottomNavigation","drawer","tabs"]},"items":{"type":"array","maxItems":12,"items":{"type":"object","required":["label","target","isVisible","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"label":{"$ref":"#/components/schemas/LocalisedText"},"icon":{"type":"string"},"target":{"$ref":"#/components/schemas/LinkTarget"},"isVisible":{"type":"boolean","description":"At most five may be visible in bottom navigation; the rest overflow."},"sortOrder":{"type":"integer"}}}},"buyButton":{"type":"object","nullable":true,"description":"**The persistent Buy tickets button (decided 29 September, MOB-2).** On every screen of the mobile app except the booking and checkout steps; it opens GST-003. Read with `bottomNavigation`.\n","properties":{"style":{"type":"string","enum":["raised","floating","flat","hidden"],"default":"raised","description":"`raised` sits in the centre of the tab bar, as the v4 prototype shows; `hidden` turns it off."},"label":{"$ref":"#/components/schemas/LocalisedText"}}}}},
"OrgUnit": {"x-ticvai-persistence":"platform.scope","type":"object","required":["id","level","path","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","nullable":true},"path":{"type":"string","description":"Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"isActive":{"type":"boolean","description":"False causes every permission query at or beneath this node to resolve to DENY.\n"},"childCount":{"type":"integer","minimum":0}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PlatformSubdomain": {"x-ticvai-persistence":"none — derived from the tenant's slug and its cell","type":"object","description":"**Every tenant's own address on TICVAI** (Chinmay, 2 October: \"subdomain plus CNAME\"; DI-283; CHG-CSA-043). Given at provisioning, one stem per cell (`<venue>.<cell>.ticvai.app`, e.g. `*.ae.ticvai.app`), under a wildcard certificate, with host-only cookies. Always live, whether or not a custom domain is claimed; a custom domain is added on top of it.","required":["hostname","cell"],"properties":{"hostname":{"type":"string","description":"e.g. `aquaventure.ae.ticvai.app`."},"cell":{"type":"string"},"certificate":{"type":"string","enum":["wildcard"]},"isPrimary":{"type":"boolean","description":"True while no custom domain is primary."}}},
"Policy": {"x-ticvai-persistence":"whitelabel.policy","type":"object","required":["kind","version","body","effectiveFrom","publishedAt"],"properties":{"kind":{"$ref":"#/components/schemas/PolicyKind"},"title":{"type":"string","description":"The heading a guest sees, and the field a refund question retrieves against.\n"},"version":{"type":"string","description":"Immutable. A guest who consented to version 3 consented to version 3, and a policy that changes under a recorded consent is a compliance failure.\n"},"body":{"$ref":"#/components/schemas/LocalisedRichText"},"requiresReconsent":{"type":"boolean"},"effectiveFrom":{"type":"string","format":"date"},"publishedByPrincipalId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"PolicyKind": {"type":"string","enum":["privacy","termsAndConditions","refund","cookie","accessibility"]},
"Preview": {"x-ticvai-persistence":"none — short-lived, cache only","type":"object","required":["previewId","url","expiresAt"],"properties":{"previewId":{"type":"string","format":"uuid"},"url":{"type":"string"},"platform":{"type":"string","enum":["ios","android","web"]},"theme":{"type":"string","deprecated":true,"enum":["light","dark"],"description":"Deprecated with `Theme.darkMode` (CHG-CSA-035); the preview always renders the venue's theme."},"language":{"type":"string","pattern":"^[a-z]{2}$"},"outputPreviews":{"type":"array","readOnly":true,"description":"**The PDF ticket and the Apple and Google Wallet passes, previewed with the app** (Chinmay, 2 October, workbook Q151: in Block A; CHG-CSA-041). One entry per output asked for in `outputs`.","items":{"type":"object","required":["output","url"],"properties":{"output":{"type":"string","enum":["app","pdfTicket","appleWalletPass","googleWalletPass"]},"url":{"type":"string","description":"A short-lived link to the rendered output (the PDF, the `.pkpass`, or the Google pass preview), expiring with the preview."}}}},"expiresAt":{"type":"string","format":"date-time"}}},
"Principal": {"x-ticvai-persistence":"identity.principal","type":"object","required":["id","username","displayName","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"username":{"type":"string"},"displayName":{"type":"string"},"isActive":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"Past this, resolution returns DENY regardless of grants."},"primaryRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Determines the landing screen when the principal holds several roles and picks one at login.\n"},"roles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"lastLoginAt":{"type":"string","format":"date-time","nullable":true}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true}}},
"ProductCategory": {"type":"object","x-ticvai-persistence":"catalogue.product_category","description":"Retail Board 2 of the client's design set, 20 August. **`listSeatCategories` existed and a product category did not** — a seat category prices a seat, and a merchandise hierarchy groups a catalogue.\n**Brand sits here rather than as its own entity.** A venue with four brands and a hierarchy five levels deep can express that with a parent; a venue with one brand should not have to maintain a table containing one row.\n**`displayOrder` is not alphabetical and that is the point.** A retail category list runs in the order the merchandiser wants a guest to see it, and sorting by name puts *Accessories* above *Apparel* forever.\n","required":["id","name","kind"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"code":{"type":"string","maxLength":64,"nullable":true,"x-ticvai-unique":"tenant","description":"**Taken from their category tables, 20 September.** Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a display string that a venue is free to translate.\n**Unique per tenant where set** (decided 28 September, audit R108): two categories in one tenant never share a code, and `setProductCategories` refuses a body that would, with `409 duplicate-code`.\n"},"nameLocalised":{"type":"object","additionalProperties":{"type":"string"}},"kind":{"type":"string","enum":["category","brand","collection","season","department"]},"parentId":{"type":"string","format":"uuid","nullable":true,"description":"**One tree, not four.** A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each level cannot express a venue that nests them differently.\n"},"scopePath":{"type":"string","readOnly":true,"description":"Set by the server from the venue the caller acts at; not sent."},"displayOrder":{"type":"integer","default":100},"imageAssetId":{"type":"string","format":"uuid","nullable":true},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September, rev 3 REV3-19). Each language value at most 200 characters.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow for every product filed here** that names none of its own (decided 29 September, W12, BO-115). Null means the venue's flow for each product's `kind`. A white-label `BookingFlow` of the venue; `setProductCategories` refuses any other id with `422`.\n"},"isActive":{"type":"boolean","default":true,"description":"**Deactivated rather than deleted.** A category with a season behind it still names the products sold under it, and removing it rewrites last year's report.\n"}}},
"ProductCategoryNode": {"x-ticvai-persistence":"none — projection over catalogue.product_category","description":"**One node of the tree `listProductCategories` returns.** A `ProductCategory` with its children nested under it, in `displayOrder`, so no caller reassembles the hierarchy from `parentId`. `setProductCategories` still takes the flat list, because a write names each parent by id.\n","allOf":[{"$ref":"#/components/schemas/ProductCategory"},{"type":"object","required":["children"],"properties":{"children":{"type":"array","description":"Empty on a leaf.","items":{"$ref":"#/components/schemas/ProductCategoryNode"}}}}]},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"PublishReviewPolicy": {"x-ticvai-persistence":"whitelabel.publish_review_policy","type":"object","description":"Whether publishing goes through a review step (CHG-CSA-042). One row per tenant; off by default.","required":["enabled"],"properties":{"enabled":{"type":"boolean","default":false},"reviewerMustDifferFromAuthor":{"type":"boolean","default":true},"appliesTo":{"type":"array","description":"What the review covers. Empty means both.","items":{"type":"string","enum":["tenantConfig","contentBlocks"]}},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `tenant` scope."}}},
"Role": {"x-ticvai-persistence":"identity.role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique within the tenant** (decided 28 September, audit R108). A seeded role's code is reserved in every tenant. Unique per tenant, not per venue, because a grant names a role anywhere in the tree; `createRole` refuses a duplicate with `409 duplicate-code`.\n"},"name":{"type":"string"},"description":{"type":"string"},"permissions":{"type":"array","description":"**A role that grants no permissions is not a role.** `Role` carried a code, a name and two counts until 18 August, and `identity.role_permission` derived from it with exactly one column — `role_id`. **A join table that joins to nothing**, found by Hrushikant in review and missed by the schema audit that ran the same day.\n**The audit asked whether every table had columns, a relationship and an owner, and this table had all three.** What it did not ask is whether a table with one column can do the job its name claims.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"inheritsFromRoleId":{"type":"string","format":"uuid","nullable":true,"description":"**Role composition, one level deep and no deeper.** A supervisor role that is a cashier plus three permissions is how venues actually describe them.\n**Cycles are refused and depth is capped at one**, because a permission set nobody can read off the screen is a permission set nobody audits.\n"},"isSystem":{"type":"boolean","default":false,"description":"**Seeded roles ship and are editable; deleting one is refused.** A venue that removes `cashier` and rebuilds it has two roles with one name in the audit log.\n**The seeded system roles are Cashier, Supervisor, Venue Manager, Finance and Tenant Admin** (proposed in `docs/active/seed-data-proposal.md` section 2, client to correct; audit R229).\n\n**Superseded 2 October 2026: no fixed default roles** (Chinmay; DEC-007; CHG-CSP-003). The five are presets (`CapabilityTemplate`, `isPreset`) a role starts from, not roles a tenant is given. The field stays for clients built at r1 and is false on every role created from 2 October.\n"},"presetCode":{"type":"string","nullable":true,"readOnly":true,"maxLength":64,"description":"**The preset this role was started from, for the record only** (decided 2 October 2026, Chinmay; DEC-007; CHG-CSP-003): the first of `createRole.presetCodes`, or null for a role ticked by hand. It binds nothing; a later edit of the preset never changes this role.\n"},"principalCount":{"type":"integer"},"grantCount":{"type":"integer"}}},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"ScopeLevel": {"type":"string","description":"**The eight organisational levels, plus `subject`.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition of the eight levels and this mirrors them so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n\n**`subject` is the one value tenancy does not have, and it is not a level.** It is here because `check-package` reads this enum as the closed vocabulary for `x-ticvai-scope-level`, and some operations act on one guest's own resources, which sit in no node of the venue hierarchy. So `subject` is valid as an operation's scope level and never as a `ScopeRef.level`: every `ScopeRef` is a row of `platform.scope`, and those carry one of the eight.\n","enum":["tenant","brand","region","venue","department","subDepartment","workstation","outlet","subject"]},
"SeoMetadata": {"type":"object","x-ticvai-persistence":"control.seo_metadata","description":"22.11.1 to 22.11.12, CF-137. **Twelve requirements, checked against the matrix.**\n**SEO is not a marketing nicety for a venue selling online** — an attraction that does not appear in search sells through OTAs at OTA commission, which is the cost this avoids.\n","required":["id","entityKind","entityId"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"entityKind":{"type":"string","enum":["contentPage","product","event","performance","membership","promotion","venue"]},"entityId":{"type":"string","format":"uuid"},"locale":{"type":"string"},"title":{"type":"string","nullable":true},"metaDescription":{"type":"string","nullable":true},"keywords":{"type":"array","items":{"type":"string"}},"canonicalUrl":{"type":"string","nullable":true},"slug":{"type":"string","nullable":true,"description":"22.11.6. **Human-readable, and changing one is a redirect rather than an edit** — a slug that changes without a 301 is a page that was ranking and now is not.\n"},"hreflang":{"type":"object","additionalProperties":{"type":"string"},"description":"22.11.11. **Which URL serves which language**, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page.\n"},"schemaOrgType":{"type":"string","nullable":true},"openGraph":{"type":"object","additionalProperties":{"type":"string"}},"isAutoGenerated":{"type":"boolean","default":true,"description":"22.11.2. **Generated by default and overridable.** A venue with 400 products will not write 400 meta descriptions, and one with an important landing page will not accept a generated one.\n"},"noIndex":{"type":"boolean","default":false},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"SitePackage": {"x-ticvai-persistence":"whitelabel.site_package","type":"object","description":"A self-hosting package of one published version (`exportSitePackage`, CHG-CSA-038).","required":["id","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"version":{"type":"string"},"status":{"type":"string","enum":["building","ready","failed"]},"downloadUrl":{"type":"string","nullable":true,"description":"Short-lived; present when `ready`."},"expiresAt":{"type":"string","format":"date-time","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"platformStaffGrantId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The platform-staff grant it was made under, where platform staff made it (R098)."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `tenant` scope."}}},
"StorefrontAnalyticsProvider": {"type":"object","x-ticvai-persistence":"whitelabel.analytics_provider","description":"**One analytics platform the storefront or app reports to** (22.10.29, 29 September build). Venue configuration: a null `venueId` is the tenant-wide default a venue's own row replaces.","required":["provider","measurementId","surfaces","consentCategory","isEnabled"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","nullable":true},"provider":{"type":"string","enum":["googleAnalytics4","googleTagManager","adobeAnalytics","metaPixel","matomo","other"]},"providerLabel":{"type":"string","maxLength":100,"nullable":true,"description":"The name, when `provider` is `other`."},"measurementId":{"type":"string","maxLength":100,"description":"What the tag or SDK reports to (GA4 `G-...`, Tag Manager `GTM-...`, a pixel id)."},"surfaces":{"type":"array","minItems":1,"items":{"type":"string","enum":["guestWeb","guestApp"]}},"consentCategory":{"type":"string","enum":["functional","analytics","personalisation","marketing"],"default":"analytics","description":"The cookie category the visitor must grant before this provider loads (marketing-crm `CookieCategory`)."},"isEnabled":{"type":"boolean","default":true},"reportingPropertyId":{"type":"string","maxLength":100,"nullable":true,"description":"The property `getStorefrontInsights` asks the reporting API about (a GA4 property id). Staff only."},"reportingCredentialRef":{"type":"string","maxLength":200,"nullable":true,"writeOnly":true,"description":"The vault reference of the reporting credential. Accepted, never returned."},"hasReportingCredential":{"type":"boolean","readOnly":true,"description":"Whether a reporting credential is held, since the reference itself is never returned."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"TenantAppStatus": {"x-ticvai-persistence":"none — computed","type":"object","description":"Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n","required":["tenantId","isPublished","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"isPublished":{"type":"boolean","x-ticvai-derived":"onRead","description":"True once any version has been published."},"publishedVersion":{"type":"string","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"draftVersion":{"type":"string","description":"Staff only."},"hasUnpublishedChanges":{"type":"boolean","x-ticvai-derived":"onRead","description":"Staff only. The working draft differs from the current version's `snapshot`."},"activeModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isEnabled` true."},"licensedModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isLicensed` true."},"activePageCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. Content pages that are `published` and enabled."},"isInMaintenance":{"type":"boolean"},"maintenanceMessage":{"$ref":"#/components/schemas/LocalisedText"},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"contact":{"$ref":"#/components/schemas/VenueContact"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"What the sold-out or closed screen says (WEB-029). Null shows the default wording."},"venues":{"type":"array","maxItems":200,"x-ticvai-derived":"onRead","description":"**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid","description":"**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."},"name":{"type":"string","maxLength":200,"description":"The venue's name (`tenancy.OrgUnit.name`)."},"city":{"type":"string","maxLength":120,"nullable":true,"description":"Shown under the name so two venues with similar names can be told apart."},"openingHoursToday":{"type":"object","nullable":true,"description":"Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.","properties":{"opens":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"},"closes":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"}}}}}},"whatsNew":{"type":"array","maxItems":10,"x-ticvai-derived":"onRead","description":"**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n","items":{"type":"object","required":["version","publishedAt","notes"],"properties":{"version":{"type":"string","description":"The release version."},"publishedAt":{"type":"string","format":"date-time","description":"When the release reached the tenant's cell."},"notes":{"$ref":"#/components/schemas/LocalisedText"}}}},"recentChanges":{"type":"array","description":"Staff only. Names the principal behind each change, so it never reaches a public response.","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}}}},
"TenantConfig": {"x-ticvai-persistence":"whitelabel.tenant_config","type":"object","description":"**The tenant's working draft**, one row per tenant (see the header). Published versions are `ConfigVersion.snapshot`, not further rows here.\n**Only `tenantId` and `version` are required**, because the draft is built one part at a time: the first `set*` call creates the row with that part alone. A part that is still unset is what `validateTenantConfig` reports (`missingRequiredAsset` and the like) and what blocks `publishTenantConfig` — a storage rule that every part exist would stop the first save.\n","required":["tenantId","version"],"properties":{"tenantId":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The draft's working version label; the published one is `ConfigVersion.version`."},"isDraft":{"type":"boolean","readOnly":true,"description":"True for the working draft, which is the only row."},"brand":{"$ref":"#/components/schemas/BrandIdentity"},"appIcons":{"$ref":"#/components/schemas/AppIcons"},"bookingFlow":{"$ref":"#/components/schemas/BookingFlowConfig"},"bookingFlows":{"type":"array","readOnly":true,"x-ticvai-derived":"onRead","description":"Every venue's booking flows in the draft (`whitelabel.booking_flow`), so a publish snapshots them with the rest (decided 29 September, W12).","items":{"$ref":"#/components/schemas/BookingFlow"}},"theme":{"$ref":"#/components/schemas/Theme"},"fonts":{"$ref":"#/components/schemas/FontConfig"},"footer":{"$ref":"#/components/schemas/FooterConfig"},"notificationBranding":{"type":"object","nullable":true,"description":"BL-003. **`marketing-crm` holds the templates and nothing said whose identity they wear.** A message sent on behalf of a venue carries that venue's sender name, reply-to and logo — **an operational alert arriving from `noreply@ticvai.com` is one a guest marks as spam.**\nResolved on the template at send time rather than duplicated per template.\n","properties":{"senderName":{"type":"string"},"replyToEmail":{"type":"string","format":"email"},"smsSenderId":{"type":"string","nullable":true},"whatsappBusinessId":{"type":"string","nullable":true},"logoAssetId":{"type":"string","format":"uuid","nullable":true}}},"enabledPaymentMethods":{"type":"array","nullable":true,"description":"BL-004. **`FeatureToggle` could turn Apple Pay on and could not say which cards a tenant accepts.** Resolved against `orders.PaymentProvider.supportedMethods` — the tenant's choice within what the gateway offers, and **a tenant enabling a method their provider does not support should fail here rather than at checkout.**\n","items":{"type":"string"}},"accessibility":{"$ref":"#/components/schemas/AccessibilitySettings"},"header":{"$ref":"#/components/schemas/HeaderConfig"},"navigation":{"$ref":"#/components/schemas/NavigationConfig"},"homepage":{"$ref":"#/components/schemas/HomepageLayout"},"modules":{"type":"array","items":{"$ref":"#/components/schemas/ModuleEnablement"}},"features":{"type":"array","items":{"$ref":"#/components/schemas/FeatureToggle"}},"languages":{"$ref":"#/components/schemas/LanguageConfig"},"updatedAt":{"type":"string","format":"date-time"},"isInMaintenance":{"type":"boolean","default":false,"description":"Written by `setMaintenanceMode`; read by `getTenantAppStatus`."},"maintenanceMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The message on the branded maintenance screen."},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"allOf":[{"$ref":"#/components/schemas/MinimumAppVersion"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"contact":{"allOf":[{"$ref":"#/components/schemas/VenueContact"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"availability":{"allOf":[{"$ref":"#/components/schemas/AppAvailability"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"venues":{"type":"array","x-ticvai-derived":"onRead","description":"The tenant's active venues, for the guest venue picker on WEB-001 and GST-001 (decided 28 September, audit R267). Public: returned without a session and cached with the rest of the response. Read from `tenancy` venues; a closed or archived venue is left out.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid"},"name":{"$ref":"#/components/schemas/LocalisedText"},"city":{"type":"string","nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Today's hours as shown to a guest, e.g. \"10:00 to 22:00\"."}}}}}},
"Theme": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","x-ticvai-contrast-pairs":[{"foreground":"textColour","background":"backgroundColour","use":"text","ratio":4.5},{"foreground":"textColour","background":"backgroundColour","use":"largeText","ratio":3.0},{"foreground":"primaryColour","background":"backgroundColour","use":"nonText","ratio":3.0},{"foreground":"secondaryColour","background":"backgroundColour","use":"nonText","ratio":3.0},{"foreground":"accentColour","background":"backgroundColour","use":"nonText","ratio":3.0},{"foreground":"componentColours.*.text","background":"componentColours.*.background","use":"text","ratio":4.5},{"foreground":"componentColours.*.background","background":"backgroundColour","use":"nonText","ratio":3.0}],"required":["primaryColour","secondaryColour","backgroundColour","textColour"],"properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"secondaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"accentColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"darkMode":{"type":"object","deprecated":true,"description":"**Deprecated and ignored** (Chinmay, 2 October, workbook Q150 and the pre-apply round; CHG-CSA-035). White label has no dark or light mode: the venue's chosen theme is applied, on every device setting. The field is kept so a client built at r1 still parses, is accepted on `setTheme` and returned as stored, and **is never used to render anything or drawn on any screen**; the guest app has no Light/Dark switch.","properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},"cornerRadius":{"type":"integer","minimum":0,"maximum":32,"description":"The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). Its named palettes, font pairs and background tones are presets over the colours here and `FontConfig`, not stored values."},"surfaceStyle":{"type":"string","enum":["glass","solid"],"default":"glass","description":"Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3)."},"buttonStyle":{"type":"string","enum":["solid","outline","pill"],"default":"solid","description":"Button shape (decided 29 September, rev 3 CFG-3)."},"componentColours":{"type":"object","description":"**Colours for single interactive elements (decided 17 September, M17-11).** Each is optional and falls back to the theme colours. Every pair passes the same contrast check as the theme (`ContrastProblem`), or `setTheme` refuses it with 400. The guest flow stays the standard one; only the colours change.\n","properties":{"primaryCta":{"$ref":"#/components/schemas/ThemeComponentColour"},"payButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"addToCart":{"$ref":"#/components/schemas/ThemeComponentColour"},"buyTicketsButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"link":{"$ref":"#/components/schemas/ThemeComponentColour"},"badge":{"$ref":"#/components/schemas/ThemeComponentColour"}}}}},
"TranslationProposals": {"type":"object","x-ticvai-persistence":"none — each draft is written on the block it translates","description":"What `proposeTranslations` drafted. **Every entry is a draft, never a publish** — a person edits and publishes it through the contract that owns the block.\n","required":["targetLocale","drafts"],"properties":{"targetLocale":{"type":"string"},"translationJobId":{"type":"string","format":"uuid","readOnly":true,"description":"The job to follow with `getTranslationProposals` (contract gap CHG-WIR-017, CMS-011; CHG-CSA-045)."},"status":{"type":"string","readOnly":true,"enum":["running","completed","failed"],"description":"`running` while drafts are still being written; `drafts` then holds those done so far."},"drafts":{"type":"array","items":{"type":"object","required":["targetKind","targetRef","draftText"],"properties":{"targetKind":{"type":"string","enum":["contentBlock","productName","emailTemplate","messageTemplate"]},"targetRef":{"type":"string","description":"The id of the block, product or template the draft sits on."},"draftText":{"type":"string","description":"The first-pass translation, as saved on the draft."}}}}}},
"UrlRedirect": {"type":"object","x-ticvai-persistence":"control.url_redirect","description":"22.11.7. **Retired pages, expired campaigns and migrated content**, which is most of a website's history.\n**A redirect chain is the failure mode.** A → B → C loses ranking at every hop, so a new redirect whose target is itself a redirect is collapsed rather than appended.\n","required":["id","fromPath","toPath","statusCode"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"fromPath":{"type":"string"},"toPath":{"type":"string"},"statusCode":{"type":"integer","enum":[301,302,307,308]},"reason":{"type":"string","enum":["contentMigrated","pageRetired","campaignExpired","restructure","slugChanged"]},"createdAt":{"type":"string","format":"date-time","readOnly":true,"nullable":true,"description":"**Taken from their `whitelabel.redirect`, 20 September.** This table counts hits and could not say when a redirect was added — a record of a site's history with no date on its own rows. Ours had `hitCount` and no timestamp of any kind.\n"},"hitCount":{"type":"integer","readOnly":true},"isActive":{"type":"boolean","default":true},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"VenueContact": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n","properties":{"phone":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"whatsapp":{"type":"string","nullable":true},"address":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Prose, as the guest reads it. The bookable hours are the catalogue's."}}}
}
```
