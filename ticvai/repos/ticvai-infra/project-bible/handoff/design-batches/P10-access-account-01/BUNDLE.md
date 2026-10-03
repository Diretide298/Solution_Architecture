# P10-access-account-01 — P10 · Access & Account

**5 screens · 27 operations · 22 schemas · 7 permissions**

Platform P10 Partner Web · ships as **ticvai-control** ·
partner audience · web ·
online only

## Who this is for

**partner on web.** Everything below is how you know what is
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
  `DEVELOPER_MANAGE, DEVELOPER_VIEW, GUEST_VIEW, MARKETING_SEND, PERMISSION_GRANT, PERMISSION_VIEW, USER_MANAGE`. A control nobody can use must say so,
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
| `PTR-001` | Partner Login / MFA | A | 16 | 51 | 10 | 6 | 2 | 0 | — | notStarted (generated) |
| `PTR-003` | Profile & Company Details | B | 12 | 14 | 6 | 1 | 0 | 0 | — | notStarted (generated) |
| `PTR-004` | Notifications | D | 4 | 10 | 5 | 10 | 0 | 0 | — | notStarted (generated) |
| `PTR-019` | API Credentials & Integration | B | 15 | 33 | 6 | 17 | 4 | 0 | — | notStarted (generated) |
| `PTR-020` | Sub-Agent Management | B | 9 | 14 | 6 | 56 | 2 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**PTR-004 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `PTR-001` Partner Login / MFA

**Get a partner user (reseller, OTA, developer) into the partner portal: username and password or the tenant's SSO, the second factor only for a listed permission, then the partner home with the allocation and credit.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Access & Account · wave 1 · needs the `partner` module |
| Block | Block A · task APP-PARTNER-PTR-001 |
| Who uses it | partner; in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | form (compact density): A sign-in: two fields, the organisation's SSO where configured, and the second-factor and role steps in place - a form, not a list to browse. |
| Offline | Not available, and the offline banner says why: signing in needs a connection. |
| Opens with | `challengeId` (navigation), `providerId` (deepLink), `methodId` (navigation) · cold entry: **Needs nothing; that is what makes it the door.** No workstation travels with a browser sign-in (CHG-DOOR-001). `providerId` arrives only on the identity … |
| Route | `/general/partner-login-mfa` |

**What the spec says about it.** **Rebuilt as a sign-in form on 2 October 2026 (CHG-DOOR-002/003; Chinmay, 2 October 2026: fix the Block A blockers now).** It was generated as a list over active sessions, MFA methods and SSO providers with Force logout and Revoke all sessions on the door, which a person who is not yet signed in can never use (platform-foundation process notes). The sequence is the same on every staff and partner door: credentials (or the organisation's SSO) -> the authentication code only when a permission demands it (R135) -> the role prompt when several roles are held (ADR-0003) -> the landing. Managing sessions moved to the staff directory (BO-053); managing MFA methods stays on each app's own security or profile screen. **The credit operations left the door** (getB2bCredit, setB2bCreditLimit, overrideCreditLimit, listPartnerAgreements): the partner reads credit on PTR-002 and PTR-013, and setting or overriding a limit is the tenant's act, not the partner's.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): A sign-in door shows no credit and no agreements: the credit read and the limit writes (getB2bCredit, setB2bCreditLimit, overrideCreditLimit) belong to the … Removed 2 October 2026 (CHG-WIR-021): A sign-in door shows no credit and no agreements: the credit read and the limit writes (getB2bCredit, setB2bCreditLimit, overrideCreditLimit) belong to the … Removed 2 October 2026 (CHG-WIR-021): A sign-in door shows no credit and no agreements: the credit read and the limit writes (getB2bCredit, setB2bCreditLimit, overrideCreditLimit) belong to the …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The partner portal's door for partner users (resellers, OTAs): username and password, the second factor only if they hold a listed permission, then the partner's home with their allocation and credit. Partner users are not TICVAI staff and land only on partner screens.

**Fixed on main** (the package already carries these; draw what it says): Credit operations (getB2bCredit, setB2bCreditLimit, overrideCreditLimit) and partner agreements are on the sign-in screen, and … (CHG-WIR-021); Generated as listDetail with session, MFA and SSO tables. (CHG-WIR-021); LoginRequest.workstationId is required. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every active session' drop sessionId, principalId, roleId, workstationId, venueId … (CHG-WIR-021).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Email or username | text field | — | — | — | — | Goes into `LoginRequest.username`. | — |
| Password | text field | — | — | — | — | Goes into `LoginRequest.credential` with `method: password`. Minimum 8, show/hide. **No workstation is sent: a browser is not a registered device** (CHG-DOOR-001), and no PIN is offered, because a … | — |
| Authentication code | text field | — | — | — | — | Shown only when the sign-in comes back `requiresMfa`: the person holds a permission in `PasswordPolicy.mfaRequiredForPermissions` (ROLE_MANAGE, LEDGER_APPROVE, every PLATFORM_* permission, or one the … | — |
| New password | text field | — | — | — | — | Only when the credential was reset and is temporary: a new one is set before anything else, twice, and the last five cannot be reused (audit R132). | — |

**Sent by *Sign in*** (`login`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Username `username` | text area | required | — | max length 256 | — | — | `login` body |
| Credential `credential` | text area | required | — | max length 512 | — | Password, PIN, card token or RFID token depending on `method`. | `login` body |
| Method `method` | radio group | optional | Password | Password · PIN · Card · RFID · Sso | — | `pin` is how a till is actually used. A cashier signs in at a shared terminal between guests, and a password on a touchscreen with somebody waiting is a password that gets … | `login` body |
| Workstation `workstationId` | picker: choose a workstation | optional | — | — | shows names, sends the id | Identifies the device. Determines Sale Board, connected hardware, till identity and Access Point inheritance. | `login` body |
| Device fingerprint `deviceFingerprint` | text area | optional | — | max length 256 | — | — | `login` body |

**Sent by *Verify*** (`verifyMfaChallenge`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `verifyMfaChallenge` body |

**Sent by *Email me a code instead*** (`createMfaChallenge`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | text field | required | — | — | — | What the step-up is for. Recorded in the audit trail. | `createMfaChallenge` body |
| Method `methodId` | picker: choose a method | optional | — | — | shows names, sends the id | — | `createMfaChallenge` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | For a guest, the venue whose `VenueSettings.identity.guestTwoStep` applies (sign-in venue, or the venue of the booking being acted on). | `createMfaChallenge` body |

**Sent by *Set up the authenticator app*** (`enrolMfaMethod`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Totp · SMS OTP · Email OTP · Biometric · Hardware token | — | — | `enrolMfaMethod` body |
| Target `target` | text field | optional | — | — | — | Phone or email for OTP methods. | `enrolMfaMethod` body |

**Sent by *Choose role*** (`selectRole`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Role `roleId` | picker: choose a role | required | — | — | shows names, sends the id | — | `selectRole` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Username and password**: Minimum 8; a temporary password from the approval email is changed at first sign-in. *(source: DI-166; contracts/spine/identity.yaml#changeOwnCredential)*

#### Outputs: what the screen shows and produces

**Shown**

**Sign in with your organisation** (card list, from `listSsoProviders`): One button per identity provider the tenant configured for partners; **absent, not disabled, when there is none.** Read before sign-in, unauthenticated. When a provider `isEnforced` for this person, the password field is hidden and only this remains.

| Shows | Format | Notes |
|---|---|---|
| Display name | text | — |
| Protocol | chip: Oidc, Saml2 | — |
| Is enforced | yes / no (icon or chip) | True disables password login for principals covered by this provider. |

**Finishing sign-in with your organisation** (progress indicator, from `completeSsoAuthorization`): On the provider's redirect back (`code` and `state` from the redirect, never typed). Returns the same `LoginResponse` as `login`, so the second factor and the role prompt follow exactly as below. 403: the provider proved who this is and no group maps to a role in this tenant, which grants nothing.

| Shows | Format | Notes |
|---|---|---|
| Access token | text | JWT carrying `sid`, validated per request against the session registry. |
| Refresh token | text | — |
| Expires in | 1,234 | Seconds |
| Requires role selection | yes / no (icon or chip) | — |
| Requires MFA | yes / no (icon or chip) | True when the principal holds any permission listed in `PasswordPolicy.mfaRequiredForPermissions` (decided 28 September, audit R135). |
| Has MFA method | yes / no (icon or chip) | Whether the principal has an active MFA method. With `requiresMfa` true and this false, the client must enrol one first (audit R135, R126 … |
| MFA methods | list or chips (count when long) | The principal's active methods, so the client can offer the right one for the `signIn` challenge. |
| ID | the name it points at, never the id | — |
| Kind | chip: Totp, SMS OTP, Email OTP, Biometric, Hardware token | — |
| Label | text | — |
| Masked target | text | Partially masked destination, so a person can tell two methods apart. |
| Is active | yes / no (icon or chip) | — |
| Is primary | yes / no (icon or chip) | — |
| Enrolled at | 1 Oct 2026, 14:30 | — |
| Last used at | 1 Oct 2026, 14:30 | — |
| Available roles | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Is primary | yes / no (icon or chip) | — |

**Recovery codes** (credential display, from `verifyMfaEnrolment`): The method is active once its first code is verified. Recovery codes are shown once, with copy and download, and never again.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Totp, SMS OTP, Email OTP, Biometric, Hardware token | — |
| Label | text | — |
| Masked target | text | Partially masked destination, so a person can tell two methods apart. |
| Is active | yes / no (icon or chip) | — |
| Is primary | yes / no (icon or chip) | — |
| Enrolled at | 1 Oct 2026, 14:30 | — |
| Last used at | 1 Oct 2026, 14:30 | — |

**Signed in as** (banner, from `getCurrentSession`): Read once the sign-in is complete (after the code and the role, where asked): the person's name and role, then straight on. A partner user lands on the partner home (PTR-002), which shows the allocation and credit; credit details live on PTR-013.

| Shows | Format | Notes |
|---|---|---|
| Session | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Role | the name it points at, never the id | — |
| Display name | text | — |
| Scope | list or chips (count when long) | Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. |
| ID | the name it points at, never the id | — |
| Level | chip: Tenant, Brand, Region, Venue, Department, Sub department… | The eight organisational levels, plus `subject`. Restored 24 August. |
| Path | text | Materialised ltree path. Prefix-comparable — `uae.dubai` contains `uae.dubai.marina`. |
| Code | text | — |
| Name | text | — |
| Effective permissions | list or chips (count when long) | Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. |
| Permissions by scope | list or chips (count when long) | Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves. |
| Permissions | list or chips (count when long) | — |
| Sale board | the name it points at, never the id | Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board. |
| Workstation | grouped details | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Venue | the name it points at, never the id | — |
| Region | the name it points at, never the id | — |
| Access point | the name it points at, never the id | Inherited from the workstation, never selected by the operator. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sign in (primary button) | `login` POST `/auth/login` | LoginRequest | LoginResponse | 400 Validation failed; 409 An active session already exists for this principal on another device. Per §3.1.3 the new login is refused. | — |
| Continue with your organisation (secondary button) | `startSsoAuthorization` GET `/auth/sso/{providerId}/authorize` | — | inline | — | — |
| Verify (primary button) | `verifyMfaChallenge` POST `/auth/mfa/challenge/{challengeId}/verify` | inline | inline | 410 The challenge has expired or was voided (by a fifth wrong code, or a newer challenge for the same purpose).; 422 A wrong code, attempts one to four (CHG-R1S-025; the r1 gate found only the fifth failure specified). | — |
| Email me a code instead (secondary button) | `createMfaChallenge` POST `/auth/mfa/challenge` | inline | inline | — | — |
| Set up the authenticator app (secondary button) | `enrolMfaMethod` POST `/auth/mfa/methods` | inline | MfaEnrolment | 403 A guest caller while no venue of the tenant has guest two-step verification on (rev 3 GAP-B1, per venue).; 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest … | — |
| Choose role (secondary button) | `selectRole` POST `/auth/select-role` | inline | Session | 403 Authenticated but not permitted at the requested scope | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Landing**: The partner home showing what they may sell and what they owe; credit details live on the credit screen. *(source: F10 step 1)*
- **Money columns (available, creditLimit, used)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listSsoProviders` (onLoad, Which identity providers this door offers; unauthenticated …); `completeSsoAuthorization` (background, Exchange the provider's code for the same LoginResponse as …)

**Where the user goes next**

- → `PTR-002` Partner Dashboard: *Partner Dashboard*
- → `PTR-003` Profile & Company Details: *Profile & Company Details*
- → `PTR-004` Notifications: *Notifications*
- → `PTR-022` Partner Management Command Center: *Opens the partner command centre*
- → `PTR-006` Product Catalog (B2B Pricing): *Product Catalog (B2B Pricing)*
- → `PTR-008` Booking Creation: *Booking Creation*
- → `PTR-009` Group / Bulk Booking: *Group / Bulk Booking*
- → `PTR-010` Cart & Quote: *Cart & Quote*
- → `PTR-011` Quote Management: *Quote Management*
- → `PTR-012` Checkout / Credit Purchase: *Checkout / Credit Purchase*
- → `PTR-013` Credit Limit & Balance: *Credit Limit & Balance*
- → `PTR-014` Settlement & Payment History: *Settlement & Payment History*
- → `PTR-015` Order History: *Order History*
- → `PTR-016` Voucher / Ticket Download: *Voucher / Ticket Download*
- → `PTR-017` Commission Statement: *Commission Statement*
- → `PTR-018` Reports & Sales Performance: *Reports & Sales Performance*
- → `PTR-019` API Credentials & Integration: *API Credentials & Integration*
- → `PTR-020` Sub-Agent Management: *Sub-Agent Management*
- → `PTR-021` Support & Contact: *Support & Contact*
- → `PTR-007` Availability Search: *Availability Search*
- → `PTR-032` Commercial Agreement Command Center: *Commercial Agreement Command Center*
- → `PTR-042` Partner Operations Command Center: *Partner Operations Command Center*
- → `PTR-005` Inventory & Allocation View: *Books against the allocation*; calls `login`
- → `SUP-001` Venue Management Sign In: *A back-office user signs in through the same door*; carries `challengeId`, `methodId`, `providerId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Checking the credential. The form stays visible and disabled. |
| Empty, first run (`?state=emptyFirstRun`) | **Nobody signed in** - the normal state of a door. The form offers username and password and, where the tenant configured one for partners, its SSO. |
| Error (`?state=error`) | Identity could not be reached. **Says so rather than saying the password is wrong**, and keeps what was typed. |
| Denied (`?state=denied`) | The credential does not match, or the account is locked. One message for both, with the attempts left before the lock; a locked account says when to try again. |
| Permission denied (`?state=emptyNoAccess`) | Signed in, and the person holds no role in this app. Says who at the tenant grants access; distinct from a wrong password. A door has no permission of its own to name, because the person is not signed in until it succeeds. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listSsoProviders` takes no filter; a tenant with no identity provider shows no SSO buttons at all, and the form is the whole door. |
| Session held (`?state=sessionHeld`) | `login` answered 409: this person already holds a session elsewhere (audit R184, ADR-0004). Says where and since when; only a holder of SESSION_FORCE_LOGOUT ends it, on the staff directory (BO-053), and signing in never ends it by itself. |
| MFA required (`?state=mfaRequired`) | **Signed in, not yet through.** The principal holds a permission that requires MFA (ROLE_MANAGE, LEDGER_APPROVE, any PLATFORM_* permission, or one the tenant added), so the screen calls `createMfaChallenge` (`action: signIn`) and asks for the authentication code; `verifyMfaChallenge` completes the sign-in. **Email me a code instead** is the fallback. Five wrong codes lock step-up for the policy's lockout minutes and the screen says until when (audit R135, R126). A person without such a … |
| MFA enrolment required (`?state=mfaEnrolmentRequired`) | **First sign-in, no method yet.** A person who requires MFA and has no active method enrols the authenticator app (email as the fallback) with `enrolMfaMethod`, confirms it with the first code (`verifyMfaEnrolment`), sees the recovery codes once, then continues to the code step (audit R135, R126 (5)). |
| Offline (`?state=offline`) | Not available, and the offline banner says why: signing in needs a connection. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 An active session already exists for this principal on another device. Per §3.1.3 the new login is refused.; 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest the same (rev 3 GAP-B1).; 422 A wrong code, attempts one to four (CHG-R1S-025; the r1 gate found only the fifth failure specified). |

#### Consistency with other screens

- Match `ADM-001`: Same form and second-factor step (F104 step 4).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
partnerUser:
  name: Hamad Al Ketbi
  organisation: Desert Gate Tours LLC
  username: hamad@desertgate.ae
  mfa: false
```

#### Permissions

- `login` → no permission · anonymous, partner
- `listSsoProviders` → no permission · anonymous, partner
- `startSsoAuthorization` → no permission · anonymous
- `completeSsoAuthorization` → no permission · anonymous
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest
- `enrolMfaMethod` → no permission · staff, partner, guest
- `verifyMfaEnrolment` → no permission · staff, partner, guest
- `selectRole` → no permission · staff, partner
- `changeOwnCredential` → no permission · staff, partner
- `getCurrentSession` → no permission · staff, partner

**A refused user sees:** Signed in, and the person holds no role in this app. Says who at the tenant grants access; distinct from a wrong password. A door has no permission of its own to name, because the person is not signed in until it succeeds.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.1.5 | The system should have the option to be used by several waiters at the same time. | F&B & Guest Management | CONTRACTED | `login` |
| 5.8.2 | The system should only allow one session per user. | F&B & Guest Management | CONTRACTED | `login` |
| 7.1.16 | The system shall support MFA using Email OTP, SMS OTP, Authenticator Apps, and future supported authentication mechanisms. | F&B POS | CONTRACTED | `enrolMfaMethod` |
| 7.1.4 | The system should be able to have a login override option for the supervisor level in order to login to the POS if the need arises and the previous user has not logged out. | F&B POS | CONTRACTED | `selectRole` |
| 3.3.28 | Authorization Caching - System shall support caching of authorization decisions. | Admission and Access | CONTRACTED | `getCurrentSession` |
| 7.1.50 | Cache authorization decisions securely to improve performance while ensuring policy changes invalidate outdated cache entries. | F&B POS | CONTRACTED | `getCurrentSession` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partner onboarding: partner signs up via a registration link/form on the B2B platform, then review and approval, with confirmation emails and back-office visibility of required next steps. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-548)*
- Partner review: operations validate documents and can reject (e.g. expired trade licence) with a message prompting resubmission; approval emails credentials with a temporary password, and the partner must set their own password at first login. *(client request · MoM 7 Aug 2026, 13. Tenant/B2B Onboarding & Self-Registration Flow · DI-166)*

Also apply: 1 for P10 · Access & Account, 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-001` · status **notStarted** · provenance generated
- Flow F104 *A platform operator signs in under MFA*, step 4: A partner user signs in through the same door. → **The second factor only where a permission requires it** — a partner user holding none of the listed permissions signs in with the password alone (audit R135).
- Flow F110 *A partner is onboarded onto the B2B portal*, step 1: The partner manager signs in → A session that can see partner applications
- ADR-0003 *Conditional role selection at login* (`docs/adr/0003-conditional-role-selection-at-login.md`)
- ADR-0004 *Single session per user* (`docs/adr/0004-single-session-per-user.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (400, 403, 409, 410, 422).
- [ ] Every output is drawn (51 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-001?state=<state>`: loading, emptyFirstRun, error, denied, emptyNoAccess, emptyNoResults, sessionHeld, mfaRequired, mfaEnrolmentRequired, offline.
- [ ] Every action is wired with its success and its failure: Sign in, Continue with your organisation, Verify, Email me a code instead, Set up the authenticator app, Choose role.
- [ ] Every transition is wired: `PTR-002`, `PTR-003`, `PTR-004`, `PTR-022`, `PTR-006`, `PTR-008`, `PTR-009`, `PTR-010`, `PTR-011`, `PTR-012`, `PTR-013`, `PTR-014`, `PTR-015`, `PTR-016`, `PTR-017`, `PTR-018`, `PTR-019`, `PTR-020`, `PTR-021`, `PTR-007`, `PTR-032`, `PTR-042`, `PTR-005`, `SUP-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-003` Profile & Company Details

**The partner's company details and its users, and what each may change.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Access & Account · wave 2 · needs the `partner` module |
| Block | Block B · task APP-PARTNER-PTR-003 |
| Who uses it | partner staff holding `USER_MANAGE` (1 configure) |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listPrincipals` reads the population and `getPrincipal` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `principalId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/profile-and-company-details` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The partner company's own details and its users; a partner admin invites and deactivates colleagues.

**Fixed on main** (the package already carries these; draw what it says): Purpose "What we hold about staff". (CHG-WIR-023); Tables show every schema field, plumbing included: 'Every principal' drop id, primaryRoleId. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scope path | text field | optional | — | — | — | Sends `?scopePath=` to `listPrincipals`. | `listPrincipals` ?scopePath |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listPrincipals`. | `listPrincipals` ?isActive |

**Form: Create principal** (modal, opened by *Create principal*; *Create principal* calls `createPrincipal`, *Cancel* sends nothing)

**Collects what `createPrincipal` sends before it is called.** Required: `username`, `displayName`. Optional: `initialCredential`, `mustChangeCredential`, `validTo`, `roleIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Username `username` | text area | required | — | max length 256 | — | — | `createPrincipal` body |
| Display name `displayName` | text field | required | — | max length 200 | — | — | `createPrincipal` body |
| Initial credential `initialCredential` | text area | optional | — | max length 512 | — | — | `createPrincipal` body |
| Must change credential `mustChangeCredential` | toggle | optional | on | — | — | — | `createPrincipal` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPrincipal` body |
| Roles `roleIds` | multi-picker: choose roles | optional | — | — | — | — | `createPrincipal` body |

Errors to draw in the form: 400 Validation failed; 409 Username already in use within this cell

**Form: Save principal** (modal, opened by *Save principal*; *Save principal* calls `updatePrincipal`, *Cancel* sends nothing)

**Collects what `updatePrincipal` sends before it is called.** Nothing in the body is required. Optional: `displayName`, `isActive`, `validTo`, `primaryRoleId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Display name `displayName` | text field | optional | — | max length 200 | — | — | `updatePrincipal` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updatePrincipal` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePrincipal` body |
| Primary role `primaryRoleId` | picker: choose a primary role | optional | — | — | shows names, sends the id | — | `updatePrincipal` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every principal** (data table, from `listPrincipals`): The role is shown by name (from `roles`); the principal id is in the detail panel with a copy action.

| Shows | Format | Notes |
|---|---|---|
| Username | text | — |
| Display name | text | — |
| Is active | yes / no (icon or chip) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Past this, resolution returns DENY regardless of grants. |
| Roles | list or chips (count when long) | — |
| Last login at | 1 Oct 2026, 14:30 | — |

**The selected principal** (detail panel, from `getPrincipal`)

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
| Create principal (primary button) | `createPrincipal` POST `/principals` | CreatePrincipalRequest | Principal | 400 Validation failed; 409 Username already in use within this cell | opens modal first |
| Save principal (secondary button) | `updatePrincipal` PATCH `/principals/{principalId}` | inline | Principal | — | opens modal first |

**Data it reads**: `getPrincipal` (onLoad, from page inventory); `listPrincipals` (onLoad, List principals)

**Where the user goes next**

- → `PTR-001` Partner Login / MFA: *Partner Login / MFA*
- → `PTR-004` Notifications: *Notifications*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The profile company list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the profile company untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No profile company yet. Offers Create principal (`createPrincipal`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on scopePath, isActive and the profile company are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `USER_MANAGE`, which `getPrincipal` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Username already in use within this cell |

#### Edge cases to draw

- **createPrincipal answers 409**: Show it as something the person can act on, not a failure: Username already in use within this cell *(source: contracts/spine/identity.yaml#createPrincipal)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every principal:
- username: fatima.almansoori
  displayName: Fatima Al Mansoori
  isActive: true
  validFrom: 01/10/2026 09:14
  validTo: 31/12/2026 23:59
  lastLoginAt: 01/10/2026 09:14
- username: '10482'
  displayName: Rahul Menon
  isActive: true
  validFrom: 30/09/2026 18:02
  validTo: 15/10/2026 00:00
  lastLoginAt: 30/09/2026 18:02
- username: omar.haddad
  displayName: Omar Haddad
  isActive: false
  validFrom: 28/09/2026 11:45
  validTo: 01/11/2026 06:00
  lastLoginAt: 28/09/2026 11:45
```

#### Permissions

- `getPrincipal` → `USER_MANAGE` (configure) · staff, partner
- `createPrincipal` → `USER_MANAGE` (configure) · staff, partner
- `listPrincipals` → `USER_MANAGE` (configure) · staff, partner
- `updatePrincipal` → `USER_MANAGE` (configure) · staff, partner

**A refused user sees:** Shown when the caller lacks `USER_MANAGE`, which `getPrincipal` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.1.6 | The system should be able to create a new Back Office/POS user and Logon to back office/POS using new user. | F&B POS | CONTRACTED | `createPrincipal` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P10 · Access & Account, 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-003` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create principal, Save principal.
- [ ] Every transition is wired: `PTR-001`, `PTR-004`.
- [ ] Every gated control is gated: `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-004` Notifications

**See the messages sent to this partner and whether each was delivered.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Access & Account · wave 3 · needs the `partner` module |
| Block | Block D · task APP-PARTNER-PTR-004 |
| Who uses it | partner staff holding `GUEST_VIEW`, `MARKETING_SEND` (1 read, 1 operate) |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getMessageStatus` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `messageId` (deepLink) · cold entry: **A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. … |
| Route | `/general/notifications` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The partner's notifications: messages about the partner's own bookings and their delivery status. Transactional messages are not marketing and are sent under contract performance, so no marketing consent applies, but the partner can never send marketing through this path.

**Fixed on main** (the package already carries these; draw what it says): The purpose ("Work with notifications for this venue") is a template, and the primary action sends a transactional message. (CHG-WIR-006).

#### Inputs: what the user enters or picks

**Form: Send transactional message** (modal, opened by *Send transactional message*; *Send transactional message* calls `sendTransactionalMessage`, *Cancel* sends nothing)

**Collects what `sendTransactionalMessage` sends before it is called.** Required: `subjectId`, `templateId`, `channel`. Optional: `mergeValues`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subjectId` | picker: choose a subject | required | — | — | shows names, sends the id | — | `sendTransactionalMessage` body |
| Template `templateId` | picker: choose a template | required | — | — | shows names, sends the id | — | `sendTransactionalMessage` body |
| Channel `channel` | select | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `sendTransactionalMessage` body |
| Merge values `mergeValues` | key and value settings | optional | — | A field the template does not declare is refused as a validation error. | — | Values for the template's `mergeFields`, by name. A field the template does not declare is refused as a validation error. | `sendTransactionalMessage` body |

Errors to draw in the form: 409 Address suppressed, or the guest has no address for that channel

#### Outputs: what the screen shows and produces

**Shown**

**The message dispatch** (detail panel, from `getMessageStatus`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | — |
| Subject | the name it points at, never the id | — |
| Campaign | the name it points at, never the id | — |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Template | the name it points at, never the id | — |
| Status | chip: Queued, Sent, Delivered, Opened, Clicked, Bounced… | — |
| Failure reason | text | — |
| Provider reference | text | — |
| Queued at | 1 Oct 2026, 14:30 | — |
| Delivered at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Send transactional message (primary button) | `sendTransactionalMessage` POST `/messages` | inline | MessageDispatch | 409 Address suppressed, or the guest has no address for that channel | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Delivery status**: Queued, sent, delivered, read, failed (with reason and the fallback channel used). *(source: contracts/satellite/marketing-crm.yaml#getMessageStatus)*

**Data it reads**: `getMessageStatus` (onLoad, Delivery status of one message)

**Where the user goes next**

- → `PTR-001` Partner Login / MFA: *Partner Login / MFA*
- → `PTR-003` Profile & Company Details: *Profile & Company Details*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The notifications, read by `getMessageStatus`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the notifications untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No notifications yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `GUEST_VIEW`, which `getMessageStatus` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MARKETING_SEND` for `sendTransactionalMessage`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Address suppressed, or the guest has no address for that channel |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
message: Booking confirmation - Desert Tours LLC group of 24 - WhatsApp - delivered 1 Oct 2026 11:05
```

#### Permissions

- `sendTransactionalMessage` → `MARKETING_SEND` (operate) · service, partner
- `getMessageStatus` → `GUEST_VIEW` (read) · staff, partner

**A refused user sees:** Shown when the caller lacks `GUEST_VIEW`, which `getMessageStatus` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MARKETING_SEND` for `sendTransactionalMessage`.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.61 | Reservation Notifications - System shall provide reservation reminders. | Guest Mobile App & Branding | CONTRACTED | `sendTransactionalMessage` |
| 19.2.62 | Ticket Notifications - System shall provide ticket reminders. | Guest Mobile App & Branding | CONTRACTED | `sendTransactionalMessage` |
| 19.2.64 | Operational Notifications - System shall provide operational notifications. | Guest Mobile App & Branding | CONTRACTED | `sendTransactionalMessage` |
| 2.7.21 | It is expected that confirmation email can be generated; the email shall include relevant visit information such as the number of tickets, the cost, the order number. | Ticketing Sales | CONTRACTED | `sendTransactionalMessage` |
| 4.4.8 | The system should be able to reduce the use of paper and send out receipts via phone as SMS or whatsapp or email for all transactions. | Bundles and Promotions | CONTRACTED | `sendTransactionalMessage` |
| 4.6.14 | The system should be able to reduce the use of paper and send out receipts via phone or email for all transactions. | Bundles and Promotions | CONTRACTED | `sendTransactionalMessage` |
| 13.3.15 | APIs shall support email, SMS, push notifications, WhatsApp notifications and notification status retrieval. | Developer & API Management | CONTRACTED | `sendTransactionalMessage` |
| 22.9.2 | Multi-Channel Delivery | Marketing & CRM | CONTRACTED | `sendTransactionalMessage` |
| 22.9.19 | Notification Delivery Tracking | Marketing & CRM | CONTRACTED | `getMessageStatus` |
| 22.9.23 | Communication History | Marketing & CRM | CONTRACTED | `getMessageStatus` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P10 · Access & Account, 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-004` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-004?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Send transactional message.
- [ ] Every transition is wired: `PTR-001`, `PTR-003`.
- [ ] Every gated control is gated: `GUEST_VIEW`, `MARKETING_SEND`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-019` API Credentials & Integration

**API Credentials & Integration — the screen a person opens when they need to deal with api credentials & integration.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Access & Account · wave 3 · needs the `developerApi` module |
| Block | Block B · task APP-PARTNER-PTR-019 |
| Who uses it | partner staff holding `DEVELOPER_MANAGE`, `DEVELOPER_VIEW` (1 configure, 1 read) |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listApiClients` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `clientId` (navigation) · cold entry: **Rotation and revocation act on one client**, which arrives from the row the partner chose. Opened cold the screen lists clients rather than offering an … |
| Route | `/general/api-credentials-and-integration` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Licensed on `developerApi`, not on `partner`.** The partner licence is what puts a partner on this portal at all; this screen's whole function is the developer API, and without that licence there is nothing on it to show. Declared `partner` it warned as a two-licence page, which is exactly the drift the rule exists to catch.

**Known gaps.**  Open: Blocked — Developer & API workshop

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A partner's API clients: sandbox clients, scopes, rotation, revocation and production-access requests, as on the developer portal.

**Fixed on main** (the package already carries these; draw what it says): formCreateApiClient asks the person for status, id. (CHG-SOT-015); Tables show every schema field, plumbing included: 'Every API client' drop id, developerId, clientId, allowedTenantIds. (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scopes, by module | multi select | — | — | — | — | **A scope picker grouped by module** (M17-05): `{module}.read` and `{module}.write`, with unlicensed modules shown and disabled rather than hidden. No scope opens a catalogue write (M17-04). | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | field | — | — | `listApiScopes` ?module |
| Status | radio group | — | Pending · Approved · Rejected · Withdrawn | `listProductionAccessRequests` ?status |

**Form: Request production access** (modal, opened by *Request production access*; *Request production access* calls `requestProductionAccess`, *Cancel* sends nothing)

**Collects what `requestProductionAccess` sends before it is called.** Required: `listingId` (a certified integration), `scopes`, `allowedTenantIds`, `ipAllowList` (at least one address, M17-07). Optional: `note`. The form says that a new production key is issued and the sandbox key stays a sandbox key.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Listing `listingId` | picker: choose a listing | required | — | — | shows names, sends the id | — | `requestProductionAccess` body |
| Scopes `scopes` | list of values (chips) | required | — | at least 1 | — | — | `requestProductionAccess` body |
| Allowed tenants `allowedTenantIds` | multi-picker: choose allowed tenants | required | — | at least 1 | — | — | `requestProductionAccess` body |
| Ip allow list `ipAllowList` | list of values (chips) | required | — | at least 1 | — | — | `requestProductionAccess` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `requestProductionAccess` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The listing is not certified, or its certification has lapsed (`certification-required`); or the client is not a sandbox client, or a request for it is already …; 422 An empty `ipAllowList` (`ip-allow-list-required`) or an unknown scope (`unknown-scope`).

**Form: Create API client** (modal, opened by *Create API client*; *Create API client* calls `createApiClient`, *Cancel* sends nothing)

**Collects what `createApiClient` sends before it is called.** The person enters `name`, picks `scopes` and an optional `ipAllowList`. **The environment is sandbox**: production clients are issued by TICVAI after certification (DI-927); `developerId` comes from the session; `clientId` and `lastUsedAt` are the server's. Never `id` or `status`: an id is a client UUIDv7 generated silently and the status and timestamps are the server's (design-notes correction, CHG-SOT-015). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Developer `developerId` | picker: choose a developer | required | — | — | shows names, sends the id | — | `createApiClient` body |
| Name `name` | text field | required | — | — | — | — | `createApiClient` body |
| Environment `environment` | segmented control | required | — | Sandbox · Production | — | Bound to one, stated on the object rather than by naming convention. A key that works in both is a key somebody will use in the wrong one. | `createApiClient` body |
| Scopes `scopes` | list of values (chips) | required | — | — | — | Resolved against the tenant's licence at token issue (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call … | `createApiClient` body |
| Certification listing `certificationListingId` | picker: choose a certification listing | optional | — | — | shows names, sends the id | For a production client, the certified integration it was issued against. | `createApiClient` body |
| Credential ttl days `credentialTtlDays` | number field (days) | optional | — | min 1; max 730 | — | Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry). | `createApiClient` body |
| Allowed tenants `allowedTenantIds` | multi-picker: choose allowed tenants | optional | — | — | — | 13.1.46. Which tenants this client may act for. | `createApiClient` body |
| Ip allow list `ipAllowList` | list of values (chips) | optional | — | — | — | 13.1.38. Required on a production client (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the internet); optional in the sandbox. | `createApiClient` body |

Errors to draw in the form: 409 A `production` client without a current certification, or asked for by a developer rather than issued by TICVAI (`certification-required`, M17-06).; 422 A `production` client with an empty `ipAllowList` (`ip-allow-list-required`, M17-07), or a scope that is not in the scope catalogue (`unknown-scope`, M17-05).

**Form: Rotate API credential** (modal, opened by *Rotate API credential*; *Rotate API credential* calls `rotateApiCredential`, *Cancel* sends nothing)

**Collects what `rotateApiCredential` sends before it is called.** Nothing in the body is required. Optional: `overlapHours`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Overlap hours `overlapHours` | number field (hours) | optional | 72 | — | — | — | `rotateApiCredential` body |

#### Outputs: what the screen shows and produces

**Shown**

**Production access** (banner, from `listProductionAccessRequests`): **Where production access stands** (M17-06): sandbox only, requested (pending), approved (a production client issued by TICVAI) or rejected with the reason. Production keys only after certification; a sandbox key is never promoted.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Developer | the name it points at, never the id | — |
| Sandbox client | the name it points at, never the id | — |
| Listing | the name it points at, never the id | — |
| Scopes | list or chips (count when long) | — |
| Allowed tenants | list or chips (count when long) | — |
| Ip allow list | list or chips (count when long) | — |
| Note | text | — |
| Status | chip: Pending, Approved, Rejected, Withdrawn | — |
| Decided by principal | the name it points at, never the id | — |
| Decided at | 1 Oct 2026, 14:30 | — |
| Reason | text | — |
| Production client | the name it points at, never the id | — |
| Requested at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Every API client** (data table, from `listApiClients`): Name, environment, scopes, IP allow-list, status and last used; the client id is in the detail panel with a copy action, allowed tenants by venue name.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Environment | chip: Sandbox, Production | Bound to one, stated on the object rather than by naming convention. A key that works in both is a key somebody will use in the wrong one. |
| Scopes | list or chips (count when long) | Resolved against the tenant's licence at token issue (13.3.24). A scope granted here and not licensed there produces no token — and the … |
| Ip allow list | list or chips (count when long) | 13.1.38. Required on a production client (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the … |
| Status | chip: Active, Suspended, Revoked | — |
| Last used at | 1 Oct 2026, 14:30 | A credential unused for a year is a credential nobody will notice being stolen. |

**The selected API client** (detail panel, from `listApiClients`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Developer | the name it points at, never the id | — |
| Name | text | — |
| Client | text | — |
| Environment | chip: Sandbox, Production | Bound to one, stated on the object rather than by naming convention. A key that works in both is a key somebody will use in the wrong one. |
| Scopes | list or chips (count when long) | Resolved against the tenant's licence at token issue (13.3.24). A scope granted here and not licensed there produces no token — and the … |
| Allowed tenants | list or chips (count when long) | 13.1.46. Which tenants this client may act for. |
| Ip allow list | list or chips (count when long) | 13.1.38. Required on a production client (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the … |
| Status | chip: Active, Suspended, Revoked | — |
| Last used at | 1 Oct 2026, 14:30 | A credential unused for a year is a credential nobody will notice being stolen. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Request production access (secondary button) | `requestProductionAccess` POST `/api-clients/{clientId}/production-access` | inline | ProductionAccessRequest | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The listing is not certified, or its certification has lapsed (`certification-required`); or the client is not … | opens modal first |
| Create API client (primary button) | `createApiClient` POST `/api-clients` | ApiClient | inline | 409 A `production` client without a current certification, or asked for by a developer rather than issued by TICVAI (`certification-required`, M17-06).; 422 A `production` client with an empty `ipAllowList` … | opens modal first |
| Rotate API credential (secondary button) | `rotateApiCredential` POST `/api-clients/{clientId}/credentials` | inline | inline | — | opens modal first |
| Revoke API credential (destructive button) | `revokeApiCredential` DELETE `/api-clients/{clientId}/credentials` | — | — | — | — |

**Data it reads**: `listApiScopes` (onLoad, Scopes to choose from, by module); `listProductionAccessRequests` (onLoad, Where production access stands for these clients); `listApiClients` (onLoad, Clients issued to this partner)

**Where the user goes next**

- → `PTR-001` Partner Login / MFA: *Partner Login / MFA*
- → `PTR-003` Profile & Company Details: *Profile & Company Details*

**What opens over it**

- confirmDialog *Revoke API credential*: **Names what `revokeApiCredential` changes and what it leaves alone**, in the consequence rather than the verb. A api credentials integration this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Detail loads |
| Error (`?state=error`) | Could not load |
| Empty, first run (`?state=emptyFirstRun`) | Not found — it may have been deleted or moved out of scope |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listApiClients` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `DEVELOPER_VIEW`, which `listApiScopes` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVELOPER_MANAGE` for `requestProductionAccess`, `createApiClient`, `rotateApiCredential`, `revokeApiCredential`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A `production` client without a current certification, or asked for by a developer rather than issued by TICVAI (`certification-required`, M17-06).; 409 The listing is not certified, or its certification has lapsed (`certification-required`); or the client is not a sandbox client, or a request for it is already …; 422 A `production` client with an empty `ipAllowList` … |

#### Edge cases to draw

- **Can read but not change (holds DEVELOPER_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: DEVELOPER_MANAGE for Request production access, Create API client, Rotate API credential. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/public-api.yaml#requestProductionAccess)*
- **requestProductionAccess answers 409**: Show it as something the person can act on, not a failure: The listing is not certified, or its certification has lapsed (`certification-required`); or the client is not a sandbox client, or a request for it is already pending (`production-access-pending`). *(source: contracts/satellite/public-api.yaml#requestProductionAccess)*
- **requestProductionAccess answers 422**: Show it as something the person can act on, not a failure: An empty `ipAllowList` (`ip-allow-list-required`) or an unknown scope (`unknown-scope`). *(source: contracts/satellite/public-api.yaml#requestProductionAccess)*
- **createApiClient answers 409**: Show it as something the person can act on, not a failure: A `production` client without a current certification, or asked for by a developer rather than issued by TICVAI (`certification-required`, M17-06). Use `requestProductionAccess`. *(source: contracts/satellite/public-api.yaml#createApiClient)*
- **createApiClient answers 422**: Show it as something the person can act on, not a failure: A `production` client with an empty `ipAllowList` (`ip-allow-list-required`, M17-07), or a scope that is not in the scope catalogue (`unknown-scope`, M17-05). *(source: contracts/satellite/public-api.yaml#createApiClient)*

#### Consistency with other screens

- Match `DEV-003`: Same rules; production clients only through the certified route.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every API client:
- name: Kiosk connector (sandbox)
  status: active
  lastUsedAt: 01/10/2026 09:14
- name: OTA availability feed
  status: pending
  lastUsedAt: 30/09/2026 18:02
- name: Wallet sync
  status: suspended
  lastUsedAt: 28/09/2026 11:45
```

#### Permissions

- `listApiScopes` → `DEVELOPER_VIEW` (read) · public, staff, partner
- `listProductionAccessRequests` → `DEVELOPER_VIEW` (read) · staff, partner
- `requestProductionAccess` → `DEVELOPER_MANAGE` (configure) · partner
- `listApiClients` → `DEVELOPER_VIEW` (read) · staff, partner
- `createApiClient` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `rotateApiCredential` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `revokeApiCredential` → `DEVELOPER_MANAGE` (configure) · staff, partner

**A refused user sees:** Shown when the caller lacks `DEVELOPER_VIEW`, which `listApiScopes` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVELOPER_MANAGE` for `requestProductionAccess`, `createApiClient`, `rotateApiCredential`, `revokeApiCredential`.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.24 | To provide the ability to enable license for the API only for the specific module. Example. APIs are exposed only for ticketing excluding resource management, Seating Module, etc | Developer & API Management | CONTRACTED | `listApiScopes` |
| 13.1.49 | API Certification Program - System shall support certification of integrations. | Developer & API Management | CONTRACTED | `requestProductionAccess` |
| 2.7.52 | System shall allow approved B2B partners to request, generate, manage, rotate, and revoke API credentials. Access shall be restricted by partner permissions, products, quotas, rate limits, IP … | Ticketing Sales | CONTRACTED | data `ApiClient` |
| 7.1.25 | The system shall support dedicated API users, integration users, service accounts, API keys, credential rotation, expiry controls, IP restrictions, and audit logging. | F&B POS | CONTRACTED | data `ApiClient` |
| 13.1.11 | API Key Management - System shall support API key generation and management. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.13 | OAuth Support - System shall support OAuth authentication. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.14 | Token Management - System shall support access token management. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.15 | Credential Revocation - System shall support credential revocation. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.21 | API Explorer - System shall provide interactive API testing tools. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.22 | SDK Availability - System shall provide SDKs for supported platforms. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.23 | Code Samples - System shall provide implementation examples. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.24 | Postman Collections - System shall provide Postman collections. | Developer & API Management | CONTRACTED | data `ApiClient` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partners never create products, prices or capacity: partner catalogue and inventory screens are read-only (a partner may still return its own unsold allocation). *(agreed · MoM 17 Sep 2026, M17-04 · DI-930)*
- Abnormal API volume is flagged, not only throttled (calls above the client's baseline, refusals outside the allow-list, calls to unused operations); a production access request requires at least one IP allow-list address. *(agreed · MoM 17 Sep 2026, M17-07 · DI-928)*
- Production access status is shown: sandbox only, requested (pending), approved, or rejected with the reason. Production keys only after certification; the request form says a new production key is issued and the sandbox key stays sandbox. *(agreed · MoM 17 Sep 2026, M17-06 · DI-927)*
- API scopes are picked from a list grouped by module ({module}.read / {module}.write), with unlicensed modules shown disabled rather than hidden; the API reference is grouped by licensable module, then contract. *(agreed · MoM 17 Sep 2026, M17-05, M17-12 · DI-926)*

Also apply: 1 for P10 · Access & Account, 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-019` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (33 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Request production access, Create API client, Rotate API credential, Revoke API credential.
- [ ] Every transition is wired: `PTR-001`, `PTR-003`.
- [ ] Every gated control is gated: `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-020` Sub-Agent Management

**Give the partner's own sub-agents access, and take it back.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Access & Account · wave 3 · needs the `partner` module |
| Block | Block B · task APP-PARTNER-PTR-020 |
| Who uses it | partner staff holding `PERMISSION_GRANT`, `PERMISSION_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listDelegatedAccess` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `delegatedAccessId` (deepLink) · cold entry: **A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. … |
| Route | `/general/sub-agent-management` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A partner's sub-agents: delegated access from the partner to its own sub-agents, with quotas. A sub-agent gets no more than the partner holds.

**Fixed on main** (the package already carries these; draw what it says): Purpose "for this venue". (CHG-WIR-023); Tables show every schema field, plumbing included: 'Every delegated access' drop id, principalId, roleId, subjectId, overSubjectId … (CHG-SOT-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listDelegatedAccess`. | `listDelegatedAccess` ?principalId |
| Role id | picker: choose a role (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?roleId=` to `listDelegatedAccess`. | `listDelegatedAccess` ?roleId |

**Form: Create delegated access** (modal, opened by *Create delegated access*; *Create delegated access* calls `createDelegatedAccess`, *Cancel* sends nothing)

**Collects what `createDelegatedAccess` sends before it is called.** Required: `permission`, `scopePath`, `effect`. Optional: `principalId`, `roleId`, `validFrom`, `validTo`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Principal `principalId` | picker: choose a principal | optional | — | — | shows names, sends the id | — | `createDelegatedAccess` body |
| Role `roleId` | picker: choose a role | optional | — | — | shows names, sends the id | — | `createDelegatedAccess` body |
| Permission `permission` | text field | required | — | — | — | — | `createDelegatedAccess` body |
| Scope path `scopePath` | text field | required | — | — | — | — | `createDelegatedAccess` body |
| Effect `effect` | segmented control | required | — | ALLOW · DENY | — | — | `createDelegatedAccess` body |
| Valid from `validFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createDelegatedAccess` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createDelegatedAccess` body |

Errors to draw in the form: 400 Wildcard on an ALLOW, or scope outside the caller's own grants

#### Outputs: what the screen shows and produces

**Shown**

**Every delegated access** (data table, from `listDelegatedAccess`): The sub-agent, the role and the subject are shown by name; the scope as the venue or branch it names; ids stay in the detail panel.

| Shows | Format | Notes |
|---|---|---|
| Permission | text | From the permission enum. `*` permitted on DENY only. |
| Over object ref | text | Where the authority is over a thing rather than a scope — a wallet, an entitlement, a booking. |
| Delegation kind | chip: Primary holder, Family member, Group leader, Attendee, Corporate admin, Corporate … | What kind of relationship this expresses, for display and for reporting. The mechanism does not branch on it — a family member and a group … |
| Quota | 1,234 | 2.14.15 and 4.3.11. How many the holder may assign. |
| Is revocable by subject | yes / no (icon or chip) | Whether the person it is over can end it. A guest who linked a family member should be able to unlink them; a corporate member should not … |
| Effect | chip: ALLOW, DENY | — |

**The selected delegated access** (detail panel, from `listDelegatedAccess`)

| Shows | Format | Notes |
|---|---|---|
| Permission | text | From the permission enum. `*` permitted on DENY only. |
| Over object ref | text | Where the authority is over a thing rather than a scope — a wallet, an entitlement, a booking. |
| Delegation kind | chip: Primary holder, Family member, Group leader, Attendee, Corporate admin, Corporate … | What kind of relationship this expresses, for display and for reporting. The mechanism does not branch on it — a family member and a group … |
| Quota | 1,234 | 2.14.15 and 4.3.11. How many the holder may assign. |
| Is revocable by subject | yes / no (icon or chip) | Whether the person it is over can end it. A guest who linked a family member should be able to unlink them; a corporate member should not … |
| Effect | chip: ALLOW, DENY | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create delegated access (primary button) | `createDelegatedAccess` POST `/delegated-access` | CreateGrantRequest | DelegatedAccess | 400 Wildcard on an ALLOW, or scope outside the caller's own grants | opens modal first |
| Delete delegated access (destructive button) | `deleteDelegatedAccess` DELETE `/delegated-access/{delegatedAccessId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Data it reads**: `listDelegatedAccess` (onLoad, List grants for a principal or role)

**Where the user goes next**

- → `PTR-001` Partner Login / MFA: *Partner Login / MFA*
- → `PTR-003` Profile & Company Details: *Profile & Company Details*

**What opens over it**

- confirmDialog *Delete delegated access*: **Names what `deleteDelegatedAccess` changes and what it leaves alone**, in the consequence rather than the verb. A sub-agent this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sub-agent list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sub-agent untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sub-agent yet. Offers Create delegated access (`createDelegatedAccess`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on principalId, roleId and the sub-agent are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PERMISSION_VIEW`, which `listDelegatedAccess` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PERMISSION_GRANT` for `createDelegatedAccess`, `deleteDelegatedAccess`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Wildcard on an ALLOW, or scope outside the caller's own grants |

#### Edge cases to draw

- **Can read but not change (holds PERMISSION_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PERMISSION_GRANT for Create delegated access, Delete delegated access. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/identity.yaml#createDelegatedAccess)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listDelegatedAccess (DelegatedAccess):
- delegationKind: primaryHolder
  quota: 12
  isRevocableBySubject: true
  effect: ALLOW
  revokedAt: 01/10/2026 09:14
  validFrom: 01/10/2026 09:14
- delegationKind: familyMember
  quota: 3
  isRevocableBySubject: false
  effect: DENY
  revokedAt: 30/09/2026 18:02
  validFrom: 30/09/2026 18:02
```

#### Permissions

- `createDelegatedAccess` → `PERMISSION_GRANT` (configure) · staff, partner
- `deleteDelegatedAccess` → `PERMISSION_GRANT` (configure) · staff, partner
- `listDelegatedAccess` → `PERMISSION_VIEW` (read) · staff, partner

**A refused user sees:** Shown when the caller lacks `PERMISSION_VIEW`, which `listDelegatedAccess` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PERMISSION_GRANT` for `createDelegatedAccess`, `deleteDelegatedAccess`.

#### Requirements it meets

56 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.32 | Least Privilege Enforcement - System shall support least-privilege access principles. | Admission and Access | CONTRACTED | `createDelegatedAccess` |
| 3.3.33 | Temporary Access Grants - System shall support temporary access permissions. | Admission and Access | CONTRACTED | `createDelegatedAccess` |
| 3.3.34 | Automatic Access Expiration - System shall automatically revoke expired permissions. | Admission and Access | CONTRACTED | `createDelegatedAccess` |
| 7.1.1 | The system should be able to assign rights to groups and further add the users to that particular groups (which should be tier based), | F&B POS | CONTRACTED | `createDelegatedAccess` |
| 7.1.2 | The system should be able to assign rights specific to individuals over and above being a part of a group and specific to location, attraction, complex (step level - hierarchy). | F&B POS | CONTRACTED | `createDelegatedAccess` |
| 7.1.3 | The system should be able to create users accounts which can be assigned under multiple groups and have the ability to add other specific rights as the need arises. | F&B POS | CONTRACTED | `createDelegatedAccess` |
| 7.1.12 | The system shall support configurable role-based access control allowing permissions to be grouped into roles and assigned to users. Roles shall be configurable for functions such as Administrator … | F&B POS | CONTRACTED | `createDelegatedAccess` |
| 7.1.30 | The system shall control access to APIs, webhooks, integrations, and external systems through role-based permissions, credentials, rate limits, and audit logs. | F&B POS | CONTRACTED | `createDelegatedAccess` |
| 7.1.38 | Support permission activation and expiration based on shifts, working hours, date ranges, holidays, seasonal periods and event schedules. Access rights should automatically change according to … | F&B POS | CONTRACTED | `createDelegatedAccess` |
| 7.1.41 | Allow temporary assignment of permissions for a defined duration. Automatically revoke access at expiration and maintain complete audit history. | F&B POS | CONTRACTED | `createDelegatedAccess` |
| 7.1.42 | Automatically revoke expired permissions, delegated access, temporary assignments and project-based permissions without administrator intervention. | F&B POS | CONTRACTED | `createDelegatedAccess` |
| 7.1.49 | Ensure users receive only the minimum permissions required to perform their job responsibilities. | F&B POS | CONTRACTED | `createDelegatedAccess` |
| … 44 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A partner has multiple agents/sub-agents who can each sell on its behalf; territory/market rights set the regions it may sell into; brand/venue association sets which venues and products it can sell, with distinct pricing per venue. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-549)*
- B2B account financial tab shows credit limit, credit days and a linked account-specific price list; accounts can be a main account with child (agent) accounts; every account shows its full sales/transaction history, as does a B2C customer profile. *(client request · MoM 7 Aug 2026, 11. Accounts Management (B2B and B2C) · DI-162)*

Also apply: 1 for P10 · Access & Account, 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-020` · status **notStarted** · provenance generated
- Flow F105 *A rate limit is set and a developer hits it*, step 3: Sub-Agent Management. → 3 operations, 3 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-020?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create delegated access, Delete delegated access.
- [ ] Every transition is wired: `PTR-001`, `PTR-003`.
- [ ] Every gated control is gated: `PERMISSION_GRANT`, `PERMISSION_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P10 as a whole** (12: 0 open, 12 closed). Open first; a closed row says where it went on 30 September.

- **A89** Build corporate/B2B self-service onboarding (trade licence & VAT upload → approve/reject → rate setup → credential issuance) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker)*
- **A135** Manage group, family and corporate/allocation ticket types inside the unified product screen rather than separate screens *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 25 Aug 2026 · workshop tracker)*
- **A170** Build family and corporate wallets (parent-funded child wristbands, per-member allowances, parent-only top-up, guest self-service family setup, department-segregated corporate funds, bidirectional transfer as a venue … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker)*
- **A178** Build B2B partner management (configurable profiles, onboarding workflow, sub-agents, territory and distribution rights, venue association with per-venue pricing, document compliance repository, action permissions … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A179** Support all three B2B/OTA routes (direct portal · bidirectional API with external OTAs · bulk pre-generated QR CSV for non-integrating partners), with an existing OTA integration reusable by configuration *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A180** Build B2B agreements & payment models (tiered volume discounts, commission rates, credit limit vs. prepaid wallet vs. card, partner-reserved inventory, booking limits) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A181** Build B2B settlement & reconciliation (per-partner operations dashboard, statements of account, exception management for unsettled transfers, dispute handling, AI partner performance view) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A184** Build group, school and corporate sales (inquiry dashboard, configurable customer categories, package builder against live inventory and resources, versioned quotations with discount approval, conversion to confirmed … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A208** Check amendments and cancellations against policy before allowing refund, cancellation or reschedule, track booking financial status, and support deposits for school and corporate bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 1 Sep 2026 · workshop tracker)*
- **A231** Build the live operations dashboard and group/B2B admission profile (real-time attendance by venue and gate, gate status, turnstile mode reconfigurable through the day, entry stats by category) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker)*
- **C35** Share the wallet-configuration reference documentation (foundation, funding, stored value, family/corporate, gift cards, payments, fraud/risk, API) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 27 Aug 2026 · workshop tracker)*
- **C44** Confirm how B2B/reseller-issued tickets are handled under a fully-dynamic-QR event policy *(Qossai · Pending → 30 Sep: Closed, Moved to T10 · 2 Sep 2026 · workshop tracker)*

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

### Across P10 Partner Web

- **Open question.** Qossai proposes a POS-style interface for high-volume resellers (hotels, travel agents) instead of a B2C-style site with login: assigned tickets and partner prices after login, optional cash drawer, sent-ticket history and resend, balance view. Chinmay wireframes both options; decide after review. *(open · MoM 29 Sep 2026, 3. B2B / reseller portal · DI-1023)*
- Qossai: partners may use the TICVAI B2B portal directly with a white-label-style B2B credential (similar to B2C), or integrate via API (preferred for OTAs such as Ticketmaster, Platinum List, BookMyShow). *(agreed · MoM 31 Aug 2026, 4.3 Clarified (integration models) · DI-552)*
- Partner access controls define which actions a partner may perform (e.g. refund, reschedule); the partner portal should only offer the actions granted. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-551)*
- Allam: B2B Portal option — partners without their own platform use a TICVAI B2B portal structured like the B2C store but behind login credentials, showing pre-configured partner pricing and products, with commission tracked the same way. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-134)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- Qossai: the target product is a white-label application supporting both B2C and B2B mobile use cases, built around three to four distinct flows (e.g. admission ticket flow, seat assignment flow). *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-056)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

### In P10 · Access & Account

- Corporate/B2B profiles have a self-service onboarding flow: company profile (name, address, trade licence, VAT certificate) → admin approval/rejection → rate/product setup → credential issuance. *(client request · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-375)*

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"changeOwnCredential": {"method":"POST","path":"/auth/credential","contract":"identity","summary":"Change the caller's own password or PIN","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChangeCredentialRequest","responds":null},
"completeSsoAuthorization": {"method":"POST","path":"/auth/sso/{providerId}/callback","contract":"identity","summary":"Exchange an SSO code for a session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LoginResponse"},
"createApiClient": {"method":"POST","path":"/api-clients","contract":"public-api","summary":"Create a client with scopes and an environment","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApiClient","responds":null},
"createDelegatedAccess": {"method":"POST","path":"/delegated-access","contract":"identity","summary":"Assign a grant","permission":"PERMISSION_GRANT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateGrantRequest","responds":"DelegatedAccess"},
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createPrincipal": {"method":"POST","path":"/principals","contract":"identity","summary":"Create a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePrincipalRequest","responds":"Principal"},
"deleteDelegatedAccess": {"method":"DELETE","path":"/delegated-access/{delegatedAccessId}","contract":"identity","summary":"Remove a grant","permission":"PERMISSION_GRANT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"enrolMfaMethod": {"method":"POST","path":"/auth/mfa/methods","contract":"identity","summary":"Enrol an MFA method","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MfaEnrolment"},
"getCurrentSession": {"method":"GET","path":"/auth/session","contract":"identity","summary":"Current session and effective permissions","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Session"},
"getMessageStatus": {"method":"GET","path":"/messages/{messageId}","contract":"marketing-crm","summary":"Delivery status of one message","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MessageDispatch"},
"getPrincipal": {"method":"GET","path":"/principals/{principalId}","contract":"identity","summary":"Read a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Principal"},
"listApiClients": {"method":"GET","path":"/api-clients","contract":"public-api","summary":"Registered clients for this developer","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ApiClient"},
"listApiScopes": {"method":"GET","path":"/api-scopes","contract":"public-api","summary":"The scope catalogue, one read and one write scope per module","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"module","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDelegatedAccess": {"method":"GET","path":"/delegated-access","contract":"identity","summary":"List grants for a principal or role","permission":"PERMISSION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"principalId","in":"query","required":null},{"name":"roleId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPrincipals": {"method":"GET","path":"/principals","contract":"identity","summary":"List principals","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopePath","in":"query","required":null},{"name":"isActive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductionAccessRequests": {"method":"GET","path":"/production-access-requests","contract":"public-api","summary":"Production access requests, pending first","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSsoProviders": {"method":"GET","path":"/auth/sso/providers","contract":"identity","summary":"Identity providers configured for this tenant","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SsoProvider"},
"login": {"method":"POST","path":"/auth/login","contract":"identity","summary":"Authenticate and open a session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LoginRequest","responds":"LoginResponse"},
"requestProductionAccess": {"method":"POST","path":"/api-clients/{clientId}/production-access","contract":"public-api","summary":"Ask for production keys for a sandbox client that passed certification","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductionAccessRequest"},
"revokeApiCredential": {"method":"DELETE","path":"/api-clients/{clientId}/credentials","contract":"public-api","summary":"Revoke immediately","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"rotateApiCredential": {"method":"POST","path":"/api-clients/{clientId}/credentials","contract":"public-api","summary":"Issue a new secret, with an overlap window","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"selectRole": {"method":"POST","path":"/auth/select-role","contract":"identity","summary":"Choose a role for a multi-role session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Session"},
"sendTransactionalMessage": {"method":"POST","path":"/messages","contract":"marketing-crm","summary":"Send a transactional message","permission":"MARKETING_SEND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"startSsoAuthorization": {"method":"GET","path":"/auth/sso/{providerId}/authorize","contract":"identity","summary":"Begin an SSO flow","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"redirectUri","in":"query","required":true}],"requestBody":null,"responds":null},
"updatePrincipal": {"method":"PATCH","path":"/principals/{principalId}","contract":"identity","summary":"Update or deactivate a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Principal"},
"verifyMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge/{challengeId}/verify","contract":"identity","summary":"Complete a sign-in or step-up challenge","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"verifyMfaEnrolment": {"method":"POST","path":"/auth/mfa/methods/{methodId}","contract":"identity","summary":"Complete enrolment","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MfaMethod"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApiClient": {"type":"object","x-ticvai-persistence":"control.api_client","description":"CF-135a. **The one credential model.** 2.7.52, 7.1.25 and 7.1.30 each asserted their own, so a partner API key, a POS integration credential and a webstore credential were three unrelated things with three lifecycles.\n","required":["id","developerId","name","environment","scopes","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid"},"name":{"type":"string"},"clientId":{"type":"string","readOnly":true},"environment":{"type":"string","enum":["sandbox","production"],"description":"**Bound to one, stated on the object rather than by naming convention.** A key that works in both is a key somebody will use in the wrong one.\n"},"scopes":{"type":"array","description":"**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing. **Module scopes** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, one of `listApiScopes`.\n","items":{"type":"string","pattern":"^[a-zA-Z]+\\.(read|write)$"}},"issuedBy":{"type":"string","enum":["partner","ticvai"],"readOnly":true,"description":"Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`.\n"},"certificationListingId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"control.integration_listing","description":"For a production client, the certified integration it was issued against."},"credentialTtlDays":{"type":"integer","minimum":1,"maximum":730,"nullable":true,"description":"Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry)."},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the key stops working unless rotated. No token is issued after it."},"allowedTenantIds":{"type":"array","description":"13.1.46. **Which tenants this client may act for.** A developer integrating for one venue must not reach another, and a client with an empty list reaches none.\n","items":{"type":"string","format":"uuid"}},"ipAllowList":{"type":"array","description":"13.1.38. **Required on a production client** (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the internet); optional in the sandbox. CIDR ranges. Checked at token issue and on every call.\n","items":{"type":"string"}},"status":{"type":"string","enum":["active","suspended","revoked"],"readOnly":true},"lastUsedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**A credential unused for a year is a credential nobody will notice being stolen.**\n"}}},
"ApiScope": {"type":"object","x-ticvai-persistence":"none — generated at release from x-ticvai-api-scope on each partner-callable operation","description":"**One module scope** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, and the operations it opens.\n**A write scope never opens a catalogue write** (M17-04): `ticketing.write` opens carts, orders and holds for a partner or developer client, and no product, price list, price, channel capacity, lifecycle or alternative-code write, since those operations are not partner-callable and carry no `x-ticvai-api-scope`. Only a platform-staff `ApiLicence.catalogueWriteException` opens one, for one named client.\n","required":["scope","module","access"],"properties":{"scope":{"type":"string","description":"e.g. `ticketing.read`."},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"access":{"type":"string","enum":["read","write"]},"description":{"type":"string"},"operations":{"type":"array","items":{"type":"object","properties":{"contract":{"type":"string"},"operationId":{"type":"string"}}}},"licensed":{"type":"boolean","description":"Whether the caller's tenant licenses the module (`ApiLicence.licensedModules`)."}}},
"ChangeCredentialRequest": {"type":"object","description":"Request only. The credential itself is stored hashed in `identity.principal_credential` and is never returned by any operation (`handoff/schema-storage-only.md`).\n","required":["method","currentCredential","newCredential"],"properties":{"method":{"type":"string","enum":["password","pin"],"description":"Which credential is being changed. Card, RFID and SSO are not secrets the principal holds, so they are not changed here."},"currentCredential":{"type":"string","maxLength":512,"writeOnly":true},"newCredential":{"type":"string","maxLength":512,"writeOnly":true}}},
"CreateGrantRequest": {"type":"object","required":["permission","scopePath","effect"],"properties":{"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"permission":{"type":"string"},"scopePath":{"type":"string"},"effect":{"type":"string","enum":["ALLOW","DENY"]},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"}}},
"CreatePrincipalRequest": {"type":"object","required":["username","displayName"],"properties":{"username":{"type":"string","maxLength":256},"displayName":{"type":"string","maxLength":200},"initialCredential":{"type":"string","maxLength":512,"writeOnly":true},"mustChangeCredential":{"type":"boolean","default":true},"validTo":{"type":"string","format":"date-time"},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"DelegatedAccess": {"x-ticvai-persistence":"identity.delegated_access","type":"object","required":["id","permission","scopePath","effect"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid","nullable":true},"roleId":{"type":"string","format":"uuid","nullable":true},"permission":{"type":"string","description":"From the permission enum. `*` permitted on DENY only."},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"CF-132, CL-05. **A grant held by a guest rather than a staff principal.**\nSection 5.5 asks for portfolios — a primary holder assigning entitlements, transfer between linked accounts, shared wallets with individual tracking — and it appears ten times across ten sections. **Every one of those reduces to the same question: who may act on whose behalf, over what, and until when.**\n**That is a grant, not a household table.** A primary holder assigning an entitlement is a grant. A group leader holding tickets for twelve is a grant. A corporate account enrolling members is a grant with a quota. **A shared wallet with individual tracking is a grant over a balance, and the transaction log already records who spent.**\n**A household table would answer one of those four.**\n"},"overSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"Whose behalf. **Null for a staff grant, which is the existing behaviour** — every grant written before 18 August means exactly what it meant before.\n"},"overObjectRef":{"type":"string","nullable":true,"description":"**Where the authority is over a thing rather than a scope** — a wallet, an entitlement, a booking. `scopePath` answers *where*; this answers *what*, and a guest's authority is almost always over a specific object rather than a branch of the tree.\n"},"delegationKind":{"type":"string","nullable":true,"enum":["primaryHolder","familyMember","groupLeader","attendee","corporateAdmin","corporateMember","carer"],"description":"**What kind of relationship this expresses**, for display and for reporting. The mechanism does not branch on it — a family member and a group attendee are the same grant with different words around them, which is the point.\n"},"quota":{"type":"integer","nullable":true,"description":"2.14.15 and 4.3.11. **How many the holder may assign.** A corporate account with fifty allocations and a family with four are the same structure with different numbers.\n"},"isRevocableBySubject":{"type":"boolean","default":true,"description":"**Whether the person it is over can end it.** A guest who linked a family member should be able to unlink them; a corporate member should not be able to revoke their employer's oversight — and **a delegation nobody can end is a delegation somebody will regret.**\n"},"scopePath":{"type":"string"},"effect":{"type":"string","enum":["ALLOW","DENY"]},"permissionId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from `identity.user_access`, 20 September, when that table was collapsed into this one.** `permission` above is free text; this names a row in `identity.permission`, the catalogue wired the same day. A grant that names a catalogue row can be checked against the keys the contracts actually enforce — which is the whole point of a catalogue that reported *154 on operations, 35 in roles.yaml, 0 shared*.\nNullable because a role grant carries no permission at all.\n"},"revokedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Taken from `identity.user_access`. This table recorded `revokedBy` and not when, so it could say who revoked a grant and not whether it was before or after the thing somebody is asking about.\n"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"createdByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"LoginRequest": {"type":"object","description":"**`workstationId` is required for a device door and absent from a browser door** (CHG-DOOR-001, 2 October 2026). It was required on every login, so no browser could sign in: the TICVAI Console (ADM-001), Venue Management (SUP-001) and the partner portal (PTR-001) have no workstation. Optional in the schema is additive against r1; the rule moved to where it belongs, the device-bound methods: `pin`, `card` and `rfid` without a `workstationId` are refused 400 (`workstation-required`). A `password` sign-in from a till, handheld or scanner still sends it, because the workstation decides the Sale Board, the hardware and the till identity (never a permission, ADR-0002).\n","required":["username","credential"],"properties":{"username":{"type":"string","maxLength":256},"credential":{"type":"string","description":"Password, PIN, card token or RFID token depending on `method`.\n","maxLength":512,"writeOnly":true},"method":{"type":"string","description":"**`pin` is how a till is actually used.** A cashier signs in at a shared terminal between guests, and a password on a touchscreen with somebody waiting is a password that gets shortened, shared or written on the drawer. The employee number goes in `username` and the PIN in `credential`, so the shape of the request does not change — only what the operator types.\n\n**A PIN is weaker than a password and the difference is bounded by the device, not by the secret.** A `pin` (like `card` and `rfid`) is accepted only with a `workstationId`, refused 400 `workstation-required` without one (CHG-DOOR-001), and the workstation is *NOT a permission source*: it says which till, and the till is on a venue network in a staff area. A PIN is a reasonable credential there and nowhere else, which is why this is an enum value and not a policy flag — a surface that wants it has to ask for it by name.\n\nAdded 10 September 2026 for `POS-000 Sign In`.\n","enum":["password","pin","card","rfid","sso"],"default":"password"},"workstationId":{"type":"string","format":"uuid","description":"Identifies the device. Determines Sale Board, connected hardware, till identity and Access Point inheritance. NOT a permission source.\n\n**Sent by a device door, never by a browser** (CHG-DOOR-001, 2 October 2026). Required in effect for the device-bound methods `pin`, `card` and `rfid` (400 `workstation-required` without it); absent on the TICVAI Console, Venue Management and partner portal sign-ins, which have no workstation.\n"},"deviceFingerprint":{"type":"string","maxLength":256}}},
"LoginResponse": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/TokenPair"},{"type":"object","required":["requiresRoleSelection","requiresMfa"],"properties":{"requiresRoleSelection":{"type":"boolean"},"requiresMfa":{"type":"boolean","description":"True when the principal holds any permission listed in `PasswordPolicy.mfaRequiredForPermissions` (decided 28 September, audit R135). The session is not usable until `verifyMfaChallenge` succeeds on a `signIn` challenge."},"hasMfaMethod":{"type":"boolean","description":"Whether the principal has an active MFA method. With `requiresMfa` true and this false, the client must enrol one first (audit R135, R126 (5))."},"mfaMethods":{"type":"array","description":"The principal's active methods, so the client can offer the right one for the `signIn` challenge. Empty when `requiresMfa` is false.","items":{"$ref":"#/components/schemas/MfaMethod"}},"availableRoles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"session":{"$ref":"#/components/schemas/Session"}}}]},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MessageDispatch": {"x-ticvai-append-only":"queuedAt","x-ticvai-persistence":"marketing.message_dispatch","type":"object","required":["id","subjectId","channel","status","queuedAt"],"properties":{"id":{"type":"string"},"subjectId":{"type":"string","format":"uuid"},"campaignId":{"type":"string","format":"uuid","nullable":true},"channel":{"$ref":"#/components/schemas/MessageChannel"},"templateId":{"type":"string","format":"uuid"},"messageTriggerId":{"type":"string","format":"uuid","nullable":true,"description":"The `MessageTrigger` that fired it, and through its `event` the `BusinessEvent` and source module; null for a campaign or a direct send. Attempts are in `MessageDispatchAttempt`. (decided 29 September, data model for the agreed operations)"},"campaignVariantId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"marketing.campaign_variant","description":"The A/B variant sent (22.1.17; 29 September, build pass, group G2). Null for a single-content campaign or a triggered message."},"plannedSendAt":{"type":"string","format":"date-time","nullable":true,"description":"The per-recipient hour chosen by `sendTimeMode` `optimised` (22.3.19, 22.9.16); null when sent at the scheduled time."},"status":{"type":"string","enum":["queued","sent","delivered","opened","clicked","bounced","failed","suppressed"]},"failureReason":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true},"queuedAt":{"type":"string","format":"date-time"},"deliveredAt":{"type":"string","format":"date-time","nullable":true},"isTest":{"type":"boolean","default":false,"description":"A `testSendCampaign` message. Excluded from `CampaignPerformance` and `Campaign.sentCount`."},"openedAt":{"type":"string","format":"date-time","nullable":true,"description":"From the provider's engagement events. `CampaignPerformance.opened` counts these."},"clickedAt":{"type":"string","format":"date-time","nullable":true},"complainedAt":{"type":"string","format":"date-time","nullable":true},"unsubscribedAt":{"type":"string","format":"date-time","nullable":true}}},
"MfaEnrolment": {"x-ticvai-persistence":"none — transient","type":"object","required":["methodId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"methodId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"secret":{"type":"string","nullable":true,"description":"TOTP shared secret. Returned once, at enrolment, and never again."},"qrCodeUri":{"type":"string","nullable":true},"recoveryCodes":{"type":"array","description":"Returned once, in this enrolment response (`enrolMfaMethod` writes them, hashed, to `identity.mfa_recovery_code`). Not retrievable afterwards — `verifyMfaEnrolment` does not return them.\n","items":{"type":"string"}},"expiresAt":{"type":"string","format":"date-time"}}},
"MfaKind": {"type":"string","enum":["totp","smsOtp","emailOtp","biometric","hardwareToken"]},
"MfaMethod": {"x-ticvai-persistence":"identity.mfa_method","type":"object","required":["id","kind","isActive","enrolledAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"label":{"type":"string","nullable":true},"maskedTarget":{"type":"string","nullable":true,"description":"Partially masked destination, so a person can tell two methods apart."},"isActive":{"type":"boolean"},"isPrimary":{"type":"boolean"},"enrolledAt":{"type":"string","format":"date-time"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Principal": {"x-ticvai-persistence":"identity.principal","type":"object","required":["id","username","displayName","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"username":{"type":"string"},"displayName":{"type":"string"},"isActive":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"Past this, resolution returns DENY regardless of grants."},"primaryRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Determines the landing screen when the principal holds several roles and picks one at login.\n"},"roles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"lastLoginAt":{"type":"string","format":"date-time","nullable":true}}},
"ProductionAccessRequest": {"type":"object","x-ticvai-persistence":"control.production_access_request","description":"**A developer's request for production keys** (17 September minutes, M17-06): sandbox, then certification, then production.\n","required":["id","developerId","sandboxClientId","listingId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid","readOnly":true},"sandboxClientId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"control.api_client"},"listingId":{"type":"string","format":"uuid","x-ticvai-references":"control.integration_listing"},"scopes":{"type":"array","items":{"type":"string"}},"allowedTenantIds":{"type":"array","items":{"type":"string","format":"uuid"}},"ipAllowList":{"type":"array","items":{"type":"string"}},"note":{"type":"string","nullable":true},"status":{"type":"string","enum":["pending","approved","rejected","withdrawn"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"reason":{"type":"string","nullable":true,"readOnly":true},"productionClientId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"control.api_client"},"requestedAt":{"type":"string","format":"date-time","readOnly":true}}},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n\n**Optional since 2 October 2026: only a till session carries it** (Chinmay, door follow-ups; CHG-CSP-002; breaking change against r1 approved as BC-001 to BC-005 in `docs/active/breaking-changes.yaml`). A browser door (ADM-001, SUP-001, PTR-001) and a staff handheld (EMP-001) sign in with no workstation since CHG-DOOR-001, so they have no board to land on and the field is absent. On a till it is the workstation's effective board: the outlet's board unless the till overrides it (`tenancy.Workstation.saleBoardSource`; CHG-CSP-006). A client reads its landing from this field when present and from its own platform otherwise.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"SsoProtocol": {"type":"string","enum":["oidc","saml2"]},
"SsoProvider": {"x-ticvai-persistence":"identity.sso_provider","type":"object","required":["id","displayName","protocol"],"properties":{"id":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"protocol":{"$ref":"#/components/schemas/SsoProtocol"},"iconAssetRef":{"type":"string","nullable":true},"isEnforced":{"type":"boolean","description":"True disables password login for principals covered by this provider."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope**; the server sets it and ignores it in a request."}}},
"TokenPair": {"x-ticvai-persistence":"none — transient","type":"object","required":["accessToken","refreshToken","expiresIn"],"properties":{"accessToken":{"type":"string","description":"JWT carrying `sid`, validated per request against the session registry."},"refreshToken":{"type":"string"},"expiresIn":{"type":"integer","description":"Seconds"}}},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
