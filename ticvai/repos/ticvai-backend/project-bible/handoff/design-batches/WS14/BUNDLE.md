# WS14 — Approval Workflows and Governance board 2

**9 screens · 7 operations · 15 schemas · 3 permissions**

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
  `APPROVAL_CONFIGURE, APPROVAL_VIEW, PRODUCT_CONFIGURE`. A control nobody can use must say so,
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
| `ADM-319` | Approval Workflow Library | B | 0 | 20 | 6 | 0 | 0 | 3 | — | notStarted (—) |
| `ADM-320` | Create Approval Workflow | B | 17 | 0 | 5 | 0 | 1 | 3 | — | notStarted (—) |
| `ADM-322` | Approval Stage Configuration | B | 14 | 0 | 5 | 0 | 1 | 3 | — | notStarted (—) |
| `ADM-323` | Condition & Decision Rule Builder | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-324` | Approval Sequence & Parallel Routing | B | 0 | 0 | 6 | 0 | 1 | 3 | — | notStarted (—) |
| `ADM-325` | Workflow Outcome & Action Configuration | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-326` | Workflow Validation & Simulation | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-327` | Workflow Publication & Lifecycle | B | 6 | 0 | 5 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-328` | Workflow Versioning & Change History | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-319, ADM-322, ADM-323, ADM-324, ADM-325, ADM-326, ADM-328 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-319` Approval Workflow Library

**Provide a centralized directory of every approval workflow configured within the tenant.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29466 (VM-ADM-319) |
| Who uses it | venue staff holding `APPROVAL_VIEW`, `PRODUCT_CONFIGURE` (1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/approval-workflow-library-adm-319` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys. **Exits to the moved workshop-pack screens dropped 2 October 2026** (CHG-SBO-023; DEC-100, CHG-MOV-001): ADM-241 are Venue Management screens now, reached by the venue's own staff or by TICVAI staff under a platform-staff grant into the tenant (R098), not by a console link.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Every approval workflow configured in the tenant with status and version.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- approveWorkflow requires PRODUCT_CONFIGURE. (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: listRuleWorkflow (APPROVAL_VIEW), approveWorkflow … (CHG-SBO-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Type | text field | — | — | `listRuleWorkflow` ?type |
| Status | text field | — | — | `listRuleWorkflow` ?status |
| Source module | text field | — | — | `listRuleWorkflow` ?sourceModule |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table, from `listRuleWorkflow`): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Rule workflow | text | Rule/Workflow ID |
| Name | text | Name |
| Type | chip: Business rule, Approval workflow, Operational workflow, Decision rule, Validation … | Kind of configuration |
| Source module | text | Source Module |
| Business process | text | Business Process |
| Owner | text | Owner |
| Effective date | 1 Oct 2026, 14:30 | Effective Date |
| Status | chip: Draft, Testing, Review, Pending approval, Approved, Scheduled… | Lifecycle status |
| Last modified | 1 Oct 2026, 14:30 | Last Modified |
| Usage | text | Usage |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active rules | 1,234 | Active Rules |
| Active workflows | 1,234 | Active Workflows |
| Approval workflows | 1,234 | Approval Workflows |
| Draft configurations | 1,234 | Draft Configurations |
| Pending approval | 1,234 | Pending Approval |
| Scheduled changes | 1,234 | Scheduled Changes |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve workflow (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listRuleWorkflow` (onLoad, Every approval workflow definition)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-328` Workflow Versioning & Change History: *Workflow Versioning & Change History*
- → `ADM-320` Create Approval Workflow: *Create Approval Workflow*
- → `ADM-322` Approval Stage Configuration: *Approval Stage Configuration*
- → `ADM-323` Condition & Decision Rule Builder: *Condition & Decision Rule Builder*
- → `ADM-324` Approval Sequence & Parallel Routing: *Approval Sequence & Parallel Routing*
- → `ADM-325` Workflow Outcome & Action Configuration: *Workflow Outcome & Action Configuration*
- → `ADM-326` Workflow Validation & Simulation: *Workflow Validation & Simulation*
- → `ADM-327` Workflow Publication & Lifecycle: *Workflow Publication & Lifecycle*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval workflow list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval workflow yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval workflow are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PRODUCT_CONFIGURE for approveWorkflow. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/catalogue.yaml#approveWorkflow)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listRuleWorkflow (RulesWorkflowCommandCenterView):
- name: Refund above AED 500 - Abu Dhabi
  type: standard
  effectiveDate: 01/10/2026 09:14
  status: active
- name: Group discount approval
  type: standard
  effectiveDate: 30/09/2026 18:02
  status: pending
```

#### Permissions

- `listRuleWorkflow` → `APPROVAL_VIEW` (read) · staff
- `approveWorkflow` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-319` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-319`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 2
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 1: Opens Approval Workflow Library → Provide a centralized directory of every approval workflow configured within the tenant.
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F124 branch at step 1 (expected): when Nothing has been set up on Approval Workflow Library yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F124 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-319?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve workflow, Cancel.
- [ ] Every transition is wired: `BO-100`, `ADM-328`, `ADM-320`, `ADM-322`, `ADM-323`, `ADM-324`, `ADM-325`, `ADM-326`, `ADM-327`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-320` Create Approval Workflow

**Provide a guided setup wizard for creating a new approval workflow. Step 1 — Basic Information**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29454 (VM-ADM-320) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/create-approval-workflow-adm-320` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A wizard for a new approval workflow: basic information, applicability, behaviour (automatic approval, delegation, escalation, comments, MFA, signature), stages, outcome.

**Fixed on main** (the package already carries these; draw what it says): Step headings ("Step 2 — Applicability") are rendered as fields. (CHG-SBO-015); Calls tenant-permission operations with no tenant picker and no platform-staff grant: setVisualWorkflow (APPROVAL_CONFIGURE). (CHG-SBO-001); Fields drawn as drop-downs that cannot be choices: text field: Workflow Name, Business Process. (CHG-SBO-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workflow name | text field | optional | — | — | — | Workflow Name | `VisualWorkflowDesignerInput.workflowName` |
| Description | select field | — | — | — | — | — | — |
| Business process | text field | optional | — | — | — | Business Process | `VisualWorkflowDesignerInput.businessProcess` |
| Source Module | select field | — | — | — | — | — | — |
| Request Type | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Department | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Workflow Owner | select field | — | — | — | — | — | — |
| Require approval | select field | — | — | — | — | — | — |
| Allow automatic approval | select field | — | — | — | — | — | — |
| Allow delegation | select field | — | — | — | — | — | — |
| Allow escalation | select field | — | — | — | — | — | — |
| Require comments | select field | — | — | — | — | — | — |
| Require rejection reason | select field | — | — | — | — | — | — |
| Require MFA | select field | — | — | — | — | — | — |
| Require digital signature | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Applicability** (progress indicator): A wizard step header (1 Basics, 2 Applicability, 3 Controls), not a field.

**Where the user goes next**

- → `ADM-319` Approval Workflow Library: *Back to Approval Workflow Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The create approval workflow configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the create approval workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No create approval workflow configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Workflow Name: 233
  Description: 19
  Business Process: 312
  Source Module: 128
  Request Type: Price change
  Tenant: Arabian Trails
  Department: Ticketing
  Venue: AquaCove Dubai
  Workflow Owner: Omar Haddad
  Step 2 — Applicability: 11
  Require approval: 312
  Allow automatic approval: 74
  Allow delegation: 19
  Allow escalation: 233
```

#### Permissions

- `setVisualWorkflow` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workflow builder defines who approves a request type and how many levels (e.g. a refund needs both a department head and the finance director). *(client request · MoM 8 Sep 2026, 4.13 Approval Workflow Builder & Authority/Amount-Based Rules · DI-725)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-320` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-320`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 2
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 2: Works in Create Approval Workflow → Provide a guided setup wizard for creating a new approval workflow. Step 1 — Basic Information

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-320?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-319`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-322` Approval Stage Configuration

**Configure each approval stage in detail. When the administrator clicks an Approval Node in Screen 3, this screen/panel opens.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29455 (VM-ADM-322) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/approval-stage-configuration-adm-322` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The detail of one approval stage: approvers, decision rule, SLA, escalation, required comments.

**Fixed on main** (the package already carries these; draw what it says): The only field is "Stage Name - Finance Manager Approval". (CHG-SBO-015); Calls tenant-permission operations with no tenant picker and no platform-staff grant: setVisualWorkflow (APPROVAL_CONFIGURE). (CHG-SBO-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Stage name | text field | optional | — | — | — | Each stage of `definition`: its name, approvers, SLA and outcome; "Finance Manager Approval" is sample data. | `VisualWorkflowDesignerInput.definition` |

**Form: Save stages** (modal, opened by *Save stages*; *Save stages* calls `setVisualWorkflow`, *Cancel* sends nothing)

**Collects what `setVisualWorkflow` sends before it is called.** Required: `workflowName`, `module`, `definition`. Optional: `nodeTypes`, `businessProcess`, `owner`, `version`, `priority`, `effectiveFrom`, `validationIssues`, `workflowId`, `trigger`, `effectiveTo`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Definition `definition` | text field | required | — | — | — | The workflow graph (nodes and connections) as a JSON document | `setVisualWorkflow` body |
| Node types `nodeTypes` | multi-select chips | optional | — | Start · Trigger · Task · Decision · Approval · System action · Notification · Wait · Timer · Parallel branch · Merge · Escalation … | — | Node kinds used in this workflow | `setVisualWorkflow` body |
| Workflow name `workflowName` | text field | required | — | — | — | Workflow Name | `setVisualWorkflow` body |
| Module `module` | text field | required | — | — | — | Module | `setVisualWorkflow` body |
| Business process `businessProcess` | text field | optional | — | — | — | Business Process | `setVisualWorkflow` body |
| Owner `owner` | text field | optional | — | — | — | Owner | `setVisualWorkflow` body |
| Version `version` | text field | optional | — | — | — | Version | `setVisualWorkflow` body |
| Priority `priority` | text field | optional | — | — | — | Priority | `setVisualWorkflow` body |
| Effective from `effectiveFrom` | text field | optional | — | — | — | Effective Dates | `setVisualWorkflow` body |
| Validation issues `validationIssues` | multi-select chips | optional | — | Dead ends · Missing outcomes · Circular loops · Missing assignee · Invalid actions | — | Design problems the designer found (read-only) | `setVisualWorkflow` body |
| Workflow `workflowId` | text field | optional | — | — | — | Workflow identifier; absent on input to create a new workflow | `setVisualWorkflow` body |
| Trigger `trigger` | text field | optional | — | — | — | What starts the workflow | `setVisualWorkflow` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Effective to | `setVisualWorkflow` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save stages (primary button) | `setVisualWorkflow` PUT `/visual-workflow` | VisualWorkflowDesignerInput | VisualWorkflowDesignerView | — | opens modal first |

**Where the user goes next**

- → `ADM-319` Approval Workflow Library: *Back to Approval Workflow Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval stage configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval stage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval stage configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
stage: Finance Manager Approval
approvers: role Finance
decision: any one
sla: 8 h
escalation: to Finance Director after SLA
```

#### Permissions

- `setVisualWorkflow` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workflow builder defines who approves a request type and how many levels (e.g. a refund needs both a department head and the finance director). *(client request · MoM 8 Sep 2026, 4.13 Approval Workflow Builder & Authority/Amount-Based Rules · DI-725)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-322` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-322`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 2
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 4: Works in Approval Stage Configuration → Configure each approval stage in detail. When the administrator clicks an Approval Node in Screen 3, this screen/panel opens.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-322?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save stages.
- [ ] Every transition is wired: `ADM-319`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-323` Condition & Decision Rule Builder

**Allow administrators to determine when a particular approval path should apply. The rule builder should use business-friendly configuration rather than programming.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29456 (VM-ADM-323) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `APPROVAL_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/condition-decision-rule-builder-adm-323` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **Condition & Decision Rule Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** When a particular approval path applies, in business terms rather than code.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: setVisualBusinessRule (APPROVAL_CONFIGURE) … (CHG-SBO-001).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setVisualBusinessRule: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/approvals.yaml#setVisualBusinessRule)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save visual business rule (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listConditionDecisionLogic` (onLoad, Rules already defined)

**Where the user goes next**

- → `ADM-319` Approval Workflow Library: *Back to Approval Workflow Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The condition decision rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the condition decision rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No condition decision rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the condition decision rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_CONFIGURE for setVisualBusinessRule. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#setVisualBusinessRule)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listConditionDecisionLogic (ConditionsDecisionLogicDecisionTablesView):
- name: Refund above AED 500 - Abu Dhabi
  resolutionStrategy: priority
  onMatch: stopProcessing
- name: Group discount approval
  resolutionStrategy: sequence
  onMatch: continueEvaluation
```

#### Permissions

- `setVisualBusinessRule` → `APPROVAL_CONFIGURE` (configure) · staff
- `listConditionDecisionLogic` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-323` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-323`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 2
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 6: Works in Condition & Decision Rule Builder → Allow administrators to determine when a particular approval path should apply. The rule builder should use business-friendly configuration rather than programming.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-323?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save visual business rule, Cancel.
- [ ] Every transition is wired: `ADM-319`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-324` Approval Sequence & Parallel Routing

**Configure complex multi-level approval structures.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29457 (VM-ADM-324) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/approval-sequence-parallel-routing-adm-324` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Sequential and parallel routing structures for multi-level approval.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: setVisualWorkflow (APPROVAL_CONFIGURE). (CHG-SBO-001).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save visual workflow (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-319` Approval Workflow Library: *Back to Approval Workflow Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval sequence parallel list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval sequence parallel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval sequence parallel yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval sequence parallel are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
route: 'Level 1 Supervisor, then Level 2 in parallel: Finance and Venue Manager (both required)'
```

#### Permissions

- `setVisualWorkflow` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workflow builder defines who approves a request type and how many levels (e.g. a refund needs both a department head and the finance director). *(client request · MoM 8 Sep 2026, 4.13 Approval Workflow Builder & Authority/Amount-Based Rules · DI-725)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-324` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-324`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 2
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 8: Works in Approval Sequence & Parallel Routing → Configure complex multi-level approval structures.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-324?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save visual workflow, Cancel.
- [ ] Every transition is wired: `ADM-319`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-325` Workflow Outcome & Action Configuration

**Define what TICVAI should actually do after the approval process reaches an outcome. This is important because approval and execution should be separated.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29458 (VM-ADM-325) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/workflow-outcome-action-configuration-adm-325` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** What happens after the outcome (execute, notify, release a hold), kept separate from the approval itself.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: setTriggerActionCross (APPROVAL_CONFIGURE). (CHG-SBO-001).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save trigger action cross (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-319` Approval Workflow Library: *Back to Approval Workflow Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow outcome action list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow outcome action untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow outcome action yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow outcome action are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
onApproved: Execute refund
onRejected: Notify requester
onExpired: Release hold and notify
```

#### Permissions

- `setTriggerActionCross` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-325` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-325`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 2
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 10: Works in Workflow Outcome & Action Configuration → Define what TICVAI should actually do after the approval process reaches an outcome. This is important because approval and execution should be separated.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-325?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save trigger action cross, Cancel.
- [ ] Every transition is wired: `ADM-319`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-326` Workflow Validation & Simulation

**Allow administrators to test workflows before putting them into production. This is something I strongly recommend adding to the UX because these workflows can directly affect money, access and customer operations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29459 (VM-ADM-326) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/workflow-validation-simulation-adm-326` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Test a workflow with sample requests before production; nothing is executed.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: simulateWorkflowTestingImpact (APPROVAL_CONFIGURE). (CHG-SBO-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-319` Approval Workflow Library: *Back to Approval Workflow Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow validation simulation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow validation simulation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow validation simulation yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow validation simulation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
sample: Price change -15% on Day Pass
path: Revenue manager then Commercial director
result: 2 approvals, 6 h expected
```

#### Permissions

- `simulateWorkflowTestingImpact` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-326` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-326`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 2
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 12: Works in Workflow Validation & Simulation → Allow administrators to test workflows before putting them into production. This is something I strongly recommend adding to the UX because these workflows can directly affect money, access and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-326?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-319`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-327` Workflow Publication & Lifecycle

**Govern the transition of workflow configurations into production.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29460 (VM-ADM-327) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `APPROVAL_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/workflow-publication-lifecycle-adm-327` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Publish a workflow version for a tenant or venue from a date, with an activation schedule.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: listRuleWorkflow (APPROVAL_VIEW), setVisualWorkflow … (CHG-SBO-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Effective From | select field | — | — | — | — | — | — |
| Effective Until | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Deployment scope | select field | — | — | — | — | — | — |
| Activation schedule | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Type | text field | — | — | `listRuleWorkflow` ?type |
| Status | text field | — | — | `listRuleWorkflow` ?status |
| Source module | text field | — | — | `listRuleWorkflow` ?sourceModule |

#### Outputs: what the screen shows and produces

**Data it reads**: `listRuleWorkflow` (onLoad, The workflow definitions and their lifecycle)

**Where the user goes next**

- → `ADM-319` Approval Workflow Library: *Back to Approval Workflow Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow publication lifecycle configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow publication lifecycle untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow publication lifecycle configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_CONFIGURE for setVisualWorkflow. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#setVisualWorkflow)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Effective From: 01/10/2026 09:14
  Effective Until: 15/10/2026 00:00
  Tenant: Arabian Trails
  Venue: AquaCove Abu Dhabi
  Deployment scope: 19
  Activation schedule: 128
```

#### Permissions

- `listRuleWorkflow` → `APPROVAL_VIEW` (read) · staff
- `setVisualWorkflow` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-327` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-327`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 2
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 14: Works in Workflow Publication & Lifecycle → Govern the transition of workflow configurations into production.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-327?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-319`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-328` Workflow Versioning & Change History

**Maintain complete governance over changes made to approval workflows. The matrix specifically requires Approval Workflow Versioning.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29461 (VM-ADM-328) |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/workflow-versioning-change-history-adm-328` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): listVersioningEffectiveDate lists waiver versions; workflow versions come from the approvals contract's workflow history (listRuleWorkflow, declared) …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Versions and change history of approval workflows, which the matrix requires (approval workflow versioning): who changed what, when, effective dates, and rollback.

**Fixed on main** (the package already carries these; draw what it says): listVersioningEffectiveDate (waiver form versions) is declared. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Type | text field | — | — | `listRuleWorkflow` ?type |
| Status | text field | — | — | `listRuleWorkflow` ?status |
| Source module | text field | — | — | `listRuleWorkflow` ?sourceModule |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listRuleWorkflow` (onLoad, The workflow being versioned)

**Where the user goes next**

- → `ADM-319` Approval Workflow Library: *Back to Approval Workflow Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow versioning change list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow versioning change untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow versioning change yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow versioning change are still there. The pack's own statuses are n By — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
version: Refund approval workflow v4 - threshold raised to AED 1,000 - effective 1 Nov 2026 - by Hana Yousef
```

#### Permissions

- `listRuleWorkflow` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-328` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-328`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 2
- Flow F124 *Approval Workflows and Governance board 2: Approval Workflow Library*, step 16: Works in Workflow Versioning & Change History → Maintain complete governance over changes made to approval workflows. The matrix specifically requires Approval Workflow Versioning.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-328?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-319`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
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

**3 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approveWorkflow": {"method":"PUT","path":"/workflow","contract":"catalogue","summary":"Approval Workflow Designer","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalWorkflowDesignerInput","responds":"ApprovalWorkflowDesignerView"},
"listConditionDecisionLogic": {"method":"GET","path":"/condition-decision-logic","contract":"approvals","summary":"Conditions, Decision Logic & Decision Tables","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ConditionsDecisionLogicDecisionTablesView"},
"listRuleWorkflow": {"method":"GET","path":"/rule-workflow","contract":"approvals","summary":"Rules & Workflow Command Center","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"type","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"sourceModule","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setTriggerActionCross": {"method":"PUT","path":"/trigger-action-cross","contract":"approvals","summary":"Trigger, Action & Cross-Module Orchestration Configuration","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TriggerActionCrossModuleOrchestrationConfigurationInput","responds":"TriggerActionCrossModuleOrchestrationConfigurationView"},
"setVisualBusinessRule": {"method":"PUT","path":"/visual-business-rule","contract":"approvals","summary":"Visual Business Rule Builder","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisualBusinessRuleBuilderInput","responds":"VisualBusinessRuleBuilderView"},
"setVisualWorkflow": {"method":"PUT","path":"/visual-workflow","contract":"approvals","summary":"Visual Workflow Designer","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisualWorkflowDesignerInput","responds":"VisualWorkflowDesignerView"},
"simulateWorkflowTestingImpact": {"method":"PUT","path":"/workflow-testing-impact","contract":"approvals","summary":"Workflow Testing, Simulation & Impact Analysis","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkflowTestingSimulationImpactAnalysisInput","responds":"WorkflowTestingSimulationImpactAnalysisView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalWorkflowDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Approval Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"workflowName":{"type":"string","description":"Workflow name"},"applicableProductTypes":{"type":"array","items":{"$ref":"#/components/schemas/ProductKind"},"description":"Applicable product types; empty = all"},"venue":{"type":"string","description":"Venue id; empty = all venues","nullable":true},"department":{"type":"string","description":"Department","nullable":true},"changeTypes":{"type":"array","items":{"type":"string","enum":["newProduct","description","price","validity","capacity","entitlement","eligibility","tax","channel","media","policy","relationship","retirement"]},"description":"Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"},"approvalStages":{"type":"array","items":{"type":"object","properties":{"order":{"type":"integer","description":"Stage order; stages sharing an order run in parallel, otherwise sequential"},"name":{"type":"string"},"approverRole":{"type":"string","nullable":true},"specificApproverId":{"type":"string","nullable":true},"approvalGroupId":{"type":"string","nullable":true},"mandatory":{"type":"boolean"},"slaHours":{"type":"integer","description":"SLA in hours"},"escalateToRole":{"type":"string","nullable":true,"description":"Escalation when the SLA is missed"},"delegationAllowed":{"type":"boolean"},"reminderEveryHours":{"type":"integer","nullable":true,"description":"Reminder frequency"}}},"description":"Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"},"rejectionBehavior":{"type":"string","enum":["returnToDraft","returnToPreviousStage","closeRequest"],"description":"What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"},"resubmissionBehavior":{"type":"string","enum":["restartFromFirstStage","resumeAtRejectingStage"],"description":"Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"},"workflowId":{"type":"string","description":"Existing workflow to change; empty to create","format":"uuid","nullable":true}}},
"ApprovalWorkflowDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Approval Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowName":{"type":"string","description":"Workflow name"},"applicableProductTypes":{"type":"array","items":{"$ref":"#/components/schemas/ProductKind"},"description":"Applicable product types; empty = all"},"venue":{"type":"string","description":"Venue id; empty = all venues","nullable":true},"department":{"type":"string","description":"Department","nullable":true},"changeTypes":{"type":"array","items":{"type":"string","enum":["newProduct","description","price","validity","capacity","entitlement","eligibility","tax","channel","media","policy","relationship","retirement"]},"description":"Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"},"approvalStages":{"type":"array","items":{"type":"object","properties":{"order":{"type":"integer","description":"Stage order; stages sharing an order run in parallel, otherwise sequential"},"name":{"type":"string"},"approverRole":{"type":"string","nullable":true},"specificApproverId":{"type":"string","nullable":true},"approvalGroupId":{"type":"string","nullable":true},"mandatory":{"type":"boolean"},"slaHours":{"type":"integer","description":"SLA in hours"},"escalateToRole":{"type":"string","nullable":true,"description":"Escalation when the SLA is missed"},"delegationAllowed":{"type":"boolean"},"reminderEveryHours":{"type":"integer","nullable":true,"description":"Reminder frequency"}}},"description":"Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"},"rejectionBehavior":{"type":"string","enum":["returnToDraft","returnToPreviousStage","closeRequest"],"description":"What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"},"resubmissionBehavior":{"type":"string","enum":["restartFromFirstStage","resumeAtRejectingStage"],"description":"Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"},"workflowId":{"type":"string","description":"Workflow id","format":"uuid"}}},
"ConditionsDecisionLogicDecisionTablesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.decision_table and decision_table_row (schema DecisionTable) (data model for the agreed operations, 29 September)","description":"**What Conditions, Decision Logic & Decision Tables displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string","description":"Name"},"decisionTableId":{"type":"string","description":"Decision table or condition set identifier"},"resolutionStrategy":{"type":"string","enum":["priority","sequence","specificity"],"description":"How to choose when multiple rules apply"},"onMatch":{"type":"string","enum":["stopProcessing","continueEvaluation"],"description":"Whether evaluation stops at the first match"},"conflicts":{"type":"array","items":{"type":"string","enum":["contradictoryRules","overlappingConditions","unreachableOutcomes","circularLogic","missingOutcomes"]},"description":"Conflicts detected in this decision logic (read-only)"}},"required":["decisionTableId","name"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"RulesWorkflowCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_definition, workflow_version, business_rule, decision_table, automation, matrix and rule; one row per configuration (data model for the agreed operations, 29 September)","description":"**What Rules & Workflow Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleWorkflowId":{"type":"string","description":"Rule/Workflow ID"},"name":{"type":"string","description":"Name"},"type":{"type":"string","enum":["businessRule","approvalWorkflow","operationalWorkflow","decisionRule","validationRule","escalationRule","automation","crossModuleWorkflow"],"description":"Kind of configuration"},"sourceModule":{"type":"string","description":"Source Module"},"businessProcess":{"type":"string","description":"Business Process"},"version":{"type":"string","description":"Version"},"owner":{"type":"string","description":"Owner"},"effectiveDate":{"type":"string","format":"date-time","description":"Effective Date"},"status":{"type":"string","enum":["draft","testing","review","pendingApproval","approved","scheduled","active","suspended","retired"],"description":"Lifecycle status"},"lastModified":{"type":"string","format":"date-time","description":"Last Modified"},"usage":{"type":"string","description":"Usage"}},"required":["ruleWorkflowId"]},
"RulesWorkflowCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"activeRules":{"type":"integer","description":"Active Rules"},"activeWorkflows":{"type":"integer","description":"Active Workflows"},"approvalWorkflows":{"type":"integer","description":"Approval Workflows"},"draftConfigurations":{"type":"integer","description":"Draft Configurations"},"pendingApproval":{"type":"integer","description":"Pending Approval"},"scheduledChanges":{"type":"integer","description":"Scheduled Changes"},"rulesWithErrors":{"type":"integer","description":"Rules With Errors"},"workflowsWithWarnings":{"type":"integer","description":"Workflows With Warnings"},"recentlyModified":{"type":"integer","description":"Configurations modified in the recent period"},"modulesCovered":{"type":"integer","description":"Number of modules using configured rules and workflows"}}},
"TriggerActionCrossModuleOrchestrationConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; writes approvals.workflow_trigger (schema WorkflowTrigger) (data model for the agreed operations, 29 September)","description":"**What Trigger, Action & Cross-Module Orchestration Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"triggerType":{"type":"string","enum":["event","dataCondition","schedule","manual"],"description":"What starts the workflow"},"workflowId":{"type":"string","description":"Workflow this trigger and action set belongs to"},"allowedActions":{"type":"array","items":{"type":"string","enum":["createApproval","createTask","updateStatus","applyHold","releaseHold","createNotification","generateDocument","executeRefund","updateAllocation","activateMembership","suspendPartner","callApprovedApi","callApprovedService","startSubWorkflow"]},"description":"Actions this workflow may call"},"onFailure":{"type":"string","enum":["retry","rollback","compensate","exceptionQueue","humanIntervention"],"description":"What happens when an action fails"},"triggerDefinition":{"type":"string","description":"Event name, data condition (e.g. Balance > Limit) or schedule"},"maxRetries":{"type":"integer","description":"Retries before the failure handling applies"}},"required":["workflowId","triggerType"]},
"TriggerActionCrossModuleOrchestrationConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_trigger (schema WorkflowTrigger) (data model for the agreed operations, 29 September)","description":"**What Trigger, Action & Cross-Module Orchestration Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"triggerType":{"type":"string","enum":["event","dataCondition","schedule","manual"],"description":"What starts the workflow"},"workflowId":{"type":"string","description":"Workflow this trigger and action set belongs to"},"allowedActions":{"type":"array","items":{"type":"string","enum":["createApproval","createTask","updateStatus","applyHold","releaseHold","createNotification","generateDocument","executeRefund","updateAllocation","activateMembership","suspendPartner","callApprovedApi","callApprovedService","startSubWorkflow"]},"description":"Actions this workflow may call"},"onFailure":{"type":"string","enum":["retry","rollback","compensate","exceptionQueue","humanIntervention"],"description":"What happens when an action fails"},"triggerDefinition":{"type":"string","description":"Event name, data condition (e.g. Balance > Limit) or schedule"},"maxRetries":{"type":"integer","description":"Retries before the failure handling applies"}},"required":["workflowId","triggerType"]},
"VisualBusinessRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; writes approvals.business_rule (schema BusinessRule) (data model for the agreed operations, 29 September)","description":"**What Visual Business Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"outcome":{"type":"string","enum":["allow","reject","requireApproval","requireAdditionalInformation","applyHold","createTask","generateAlert","startWorkflow","executeApprovedAction"],"description":"THEN outcome when the conditions match"},"businessObjectField":{"type":"string","description":"Governed field from a registered module, e.g. Refund.Amount"},"name":{"type":"string","description":"Rule name"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","contains","inList","exists","doesNotExist","beforeAfter","percentageThreshold","boolean"],"description":"Comparison operator of the condition"},"ruleId":{"type":"string","description":"Rule identifier; absent on input to create a new rule"},"value":{"type":"string","description":"Comparison value"},"explanation":{"type":"string","description":"Plain-language rule explanation"}},"required":["name","businessObjectField","operator","outcome"]},
"VisualBusinessRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.business_rule, the row setVisualBusinessRule writes (data model for the agreed operations, 29 September)","description":"**What Visual Business Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"outcome":{"type":"string","enum":["allow","reject","requireApproval","requireAdditionalInformation","applyHold","createTask","generateAlert","startWorkflow","executeApprovedAction"],"description":"THEN outcome when the conditions match"},"businessObjectField":{"type":"string","description":"Governed field from a registered module, e.g. Refund.Amount"},"name":{"type":"string","description":"Rule name"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","contains","inList","exists","doesNotExist","beforeAfter","percentageThreshold","boolean"],"description":"Comparison operator of the condition"},"ruleId":{"type":"string","description":"Rule identifier; absent on input to create a new rule"},"value":{"type":"string","description":"Comparison value"},"explanation":{"type":"string","description":"Plain-language rule explanation"}},"required":["name","businessObjectField","operator","outcome"]},
"VisualWorkflowDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; writes approvals.workflow_definition and a draft approvals.workflow_version (data model for the agreed operations, 29 September)","description":"**What Visual Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"definition":{"type":"string","description":"The workflow graph (nodes and connections) as a JSON document"},"nodeTypes":{"type":"array","items":{"type":"string","enum":["start","trigger","task","decision","approval","systemAction","notification","wait","timer","parallelBranch","merge","escalation","subWorkflow","end"]},"description":"Node kinds used in this workflow"},"workflowName":{"type":"string","description":"Workflow Name"},"module":{"type":"string","description":"Module"},"businessProcess":{"type":"string","description":"Business Process"},"owner":{"type":"string","description":"Owner"},"version":{"type":"string","description":"Version"},"priority":{"type":"string","description":"Priority"},"effectiveFrom":{"type":"string","description":"Effective Dates"},"validationIssues":{"type":"array","items":{"type":"string","enum":["deadEnds","missingOutcomes","circularLoops","missingAssignee","invalidActions"]},"description":"Design problems the designer found (read-only)"},"workflowId":{"type":"string","description":"Workflow identifier; absent on input to create a new workflow"},"trigger":{"type":"string","description":"What starts the workflow"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective to"}},"required":["workflowName","module","definition"]},
"VisualWorkflowDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_definition and its draft approvals.workflow_version (data model for the agreed operations, 29 September)","description":"**What Visual Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"definition":{"type":"string","description":"The workflow graph (nodes and connections) as a JSON document"},"nodeTypes":{"type":"array","items":{"type":"string","enum":["start","trigger","task","decision","approval","systemAction","notification","wait","timer","parallelBranch","merge","escalation","subWorkflow","end"]},"description":"Node kinds used in this workflow"},"workflowName":{"type":"string","description":"Workflow Name"},"module":{"type":"string","description":"Module"},"businessProcess":{"type":"string","description":"Business Process"},"owner":{"type":"string","description":"Owner"},"version":{"type":"string","description":"Version"},"priority":{"type":"string","description":"Priority"},"effectiveFrom":{"type":"string","description":"Effective Dates"},"validationIssues":{"type":"array","items":{"type":"string","enum":["deadEnds","missingOutcomes","circularLoops","missingAssignee","invalidActions"]},"description":"Design problems the designer found (read-only)"},"workflowId":{"type":"string","description":"Workflow identifier; absent on input to create a new workflow"},"trigger":{"type":"string","description":"What starts the workflow"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective to"}},"required":["workflowName","module","definition"]},
"WorkflowTestingSimulationImpactAnalysisInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; the outcome is recorded as approvals.workflow_version test results (data model for the agreed operations, 29 September)","description":"**What Workflow Testing, Simulation & Impact Analysis submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"workflowId":{"type":"string","description":"Workflow under test"},"testMode":{"type":"string","enum":["manualTestCase","sampleTransaction","historicalReplay","scenarioSimulation","batchTest"],"description":"How the workflow is tested"},"version":{"type":"string","description":"Version under test"},"compareWithVersion":{"type":"string","description":"Existing version to compare against for regression"},"inputPayload":{"type":"string","description":"Sample transaction as a JSON document, for manual and sample tests"},"replayFrom":{"type":"string","format":"date","description":"Historical replay start"},"replayTo":{"type":"string","format":"date","description":"Historical replay end"}},"required":["workflowId","testMode"]},
"WorkflowTestingSimulationImpactAnalysisView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — computed by simulation over approvals.workflow_version and the rules it calls; never executes actions (data model for the agreed operations, 29 September)","description":"**What Workflow Testing, Simulation & Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowId":{"type":"string","description":"Workflow under test"},"testMode":{"type":"string","enum":["manualTestCase","sampleTransaction","historicalReplay","scenarioSimulation","batchTest"],"description":"How the workflow is tested"},"rulesEvaluated":{"type":"integer","description":"Rules Evaluated"},"conditionsMatched":{"type":"integer","description":"Conditions Matched"},"decisions":{"type":"integer","description":"Decisions"},"approvalPath":{"type":"string","description":"Approval Path"},"actions":{"type":"integer","description":"Actions"},"notifications":{"type":"integer","description":"Notifications"},"sla":{"type":"string","description":"SLA"},"expectedOutcome":{"type":"string","description":"Expected Outcome"},"version":{"type":"string","description":"Version under test"},"compareWithVersion":{"type":"string","description":"Existing version to compare against for regression"},"inputPayload":{"type":"string","description":"Sample transaction as a JSON document, for manual and sample tests"},"replayFrom":{"type":"string","format":"date","description":"Historical replay start"},"replayTo":{"type":"string","format":"date","description":"Historical replay end"}},"required":["workflowId","testMode"]}
}
```
