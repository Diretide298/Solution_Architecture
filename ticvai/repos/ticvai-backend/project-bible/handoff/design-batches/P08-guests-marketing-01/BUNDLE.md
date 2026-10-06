# P08-guests-marketing-01 — P08 · Guests & Marketing

**4 screens · 23 operations · 38 schemas · 11 permissions**

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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `AI_AUDIT_VIEW, AI_CONFIGURE, AI_USE, AUDIT_VIEW, CASE_MANAGE, CASE_VIEW, MARKETING_MANAGE, MARKETING_VIEW, REPORT_VIEW_VENUE, SCOPE_VIEW, TENANT_VIEW`. A control nobody can use must say so,
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

### AI & Intelligence

AI in TICVAI is one governed engine behind many screens. The guest meets it as Sahli, the concierge (WEB-044, GST-031, GST-033), as the planner agent that refines a rules-built day plan by chat (GST-054), and as upsell and cross-sell offers on a separate Extras step (WEB-008, GST-048). Staff meet it as the Staff App's AI tab (EMP-019/020, knowledge EMP-040/041), the kiosk assistant (KSK-015) and the support copilot (SUP-006, SUP-018). Venue managers meet it in Venue Management (BO-091 policy and spend, BO-919/BO-925..932 resource and staffing forecasts, BO-597/598 configuration drafts, BO-772/782 marketing optimisation, BO-793 translations, BO-970/975 seat-map generation, BO-1048 seat upsell, BO-1160 fraud cases) and in Analytics (ANL-010 suggestions, ANL-019 management insights, ANL-055 anomalies, ANL-057 forecasting studio, ANL-059 insight history, ANL-060 governance, ANL-071 AI maturity). The governance, configuration-assistant, forecasting, oversight, audit and monitoring boards sit on the TICVAI Console (P09: ADM-037 providers, ADM-469..498 configuration assistant, ADM-499..518 forecasting, ADM-519..558 governance, ADM-633/637 fraud, ADM-680..697 recommendation governance). Five rules hold on every one of these screens. (1) Baseline first, then it learns per tenant: every data-driven answer (forecast, suggestion, risk score, recommendation) exists from day one, from the venue AI profile, a starting pattern for the venue type, the UAE calendar and the weather, and shifts to the venue's own data as it trades; nothing says "comes later" or refuses for lack of history - a refusal only names a missing setting. (2) Every answer shows its basis and maturity: a "Based on" line, a stage badge (Starting, Learning, Established, Trained on your data), "Limited historical data" while the starting pattern carries more than half the weight, ranges or bands rather than a bare percentage, a confidence only where the producer really has one, a plain-words explanation always. (3) A trained model replaces the baseline only when it beats it in a shadow run of at least six weeks and an admin promotes it; the platform raises "Ready to promote" and never switches by itself. (4) The LLM never reads raw data: numbers come only from query results the platform runs (the answer shows the query), only the masked prompt and retrieved context leave the platform, and AI only drafts - the owning screen applies. (5) One autonomy scale, L0 Disabled to L4 Controlled auto, with first-release ceilings, separate from user permission and from the approval tier; impactful actions route to a person, who sees current against proposed, impact, risk and what is affected, and can approve within a limit, challenge, override or roll back; every decision is traceable (data, model, approver, time) and searchable by customer, venue and capability. In Block A (5 October to 20 November 2026) the guest concierge with retrieval, Help me choose, translations, the planner agent, the gateway and …
*(source: ADR-0051; ADR-0050; ADR-0020; ADR-0052; ADR-0053; ADR-0054; ADR-0059; ADR-0051 (AI-D01..AI-D20); ADR-0051 (AI functions review 30 Sep §2 §4 §9); MoM 18 Sep 4.1-4.10; MoM 21 Sep 4.1-4.14; MoM 30 Sep 4.1 4.7; ADR-0059 (Block A slice: tasks.csv))*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sahli | The guest concierge's name; the entry reads "Ask Sahli" and shows as mascot art when the venue's Concierge mascot setting is on (default), otherwise a plain button. | Chatbot, Bot, AI Concierge (as a visible label), Virtual agent | DI-1069 / screens/P01-guest-web-storefront.yaml#WEB-044 |
| Based on | The line on every AI answer that says what it was computed from, e.g. "Based on: your venue profile, UAE calendar, weather, 23 days of your sales". Always present. | Data sources, Model inputs, Powered by AI | ADR-0051 Maturity / contracts/satellite/ai.yaml#/components/schemas/AiMaturity |
| Starting / Learning / Established / Trained on your data | The four maturity stages (enum starting, learning, established, learned), shown as one badge. Moves by itself from Starting to Established as own data arrives; Trained on your data only after an admin promotion. | Beta, Experimental, Low confidence, Cold start (in UI), Not enough data | ADR-0051 / ADR-0051 (AI functions review 30 Sep §2) |
| Limited historical data | Shown while own data carries less than half the weight (AiMaturity.limitedHistory, ownDataShare < 0.5). An honest qualifier, never a refusal. | Insufficient data, Not available until, Comes later | ADR-0051 / contracts/satellite/ai.yaml#/components/schemas/AiMaturity |
| Range | The 10th-90th percentile band a forecast or estimate is shown with (e.g. "1,850-3,400 guests, most likely 2,600"). Never a bare accuracy percentage on an answer; measured accuracy (WAPE, bias, coverage) appears only on accuracy screens … | Accuracy 92%, Confidence 0.87 (on a heuristic), Exact | ADR-0051 / contracts/satellite/ai.yaml#getForecast / … |
| Running in the background | A trained model in shadow next to the live answer (AiRelease.stage shadow); it changes nothing a person sees. | Live, Active model, Testing in production | ADR-0051 Promotion / ADR-0051 (AI functions review 30 Sep §2) |
| Ready to promote / Promote | A shadow model passed its gate (governance alert promotionReady); an admin promotes it one stage at a time (canary, then production). The only way a model replaces the baseline. | Deploy, Go live, Auto-switch, Activate model, Upgrade AI | ADR-0051 (AI-D16) / contracts/satellite/ai.yaml#promoteAiRelease |
| L0 Disabled / L1 Advisory / L2 Prepare / L3 Execute with … | The one autonomy scale for every AI capability, shown as "L2 Prepare" etc. with the capability's ceiling beside it. Lower scopes tighten, never raise. | Autopilot, Copilot mode, Level 0-3 (CFG book), Approval level (for autonomy), Manual/Semi/Auto | ADR-0050 / ADR-0050 (AI-D04) / … |
| Approval tier | How many people must approve a proposed action (ProposedAction.approvalLevel, 1 or 2). Not an autonomy level. | Autonomy level, Approval level (ambiguous) | ADR-0050 |
| Suggestion / Draft | What AI produces. A suggestion advises; a draft is a ready-to-review change that a person applies in the owning screen. Copy says "Nothing is applied until you approve it." | AI changed, Auto-applied, AI updated your prices | ADR-0020 / ADR-0051 (AI functions review 30 Sep §4 Configuration assistant) / … |
| Why this? | The link or expander that opens an answer's explanation (Suggestion.explanation, recommendation template reason, decision trace). Plain words; for guests a template reason. | Explainability, SHAP, Feature importance (in operator copy) | ADR-0052 (AI-D09) / contracts/satellite/ai.yaml#/components/schemas/Suggestion |
| No thanks | The explicit decline on an offer. Only this counts as a decline and it is remembered across channels; scrolling past or closing the step is not a decline. | Dismiss (as a decline), Skip (as a decline), X (as a decline) | ADR-0052 (AI-D07) / DI-962 / … |
| Hold for review | What a high fraud or risk score does to a payment or order. The transaction goes through; it is held for a person. | Decline, Block, Reject (for a risk score), Fraud detected | ADR-0053 / ADR-0053 (AI-D06) |
| Hand over to a person | The concierge passes the whole conversation and its own summary to a live agent; the guest does not repeat themselves. | Escalate, Transfer, Contact bot | contracts/satellite/marketing-crm.yaml#handoverToAgent |
| Not available yet | The analytics assistant's answer to a question outside the semantic model; it records a knowledge gap and never improvises a number. | I cannot answer, Error, Unknown | ADR-0054 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-068` | Audit Log | B | 9 | 9 | 6 | 6 | 1 | 0 | — | notStarted (generated) |
| `BO-073` | Lost & Found Register | D | 4 | 18 | 6 | 1 | 1 | 0 | — | notStarted (generated) |
| `BO-091` | AI Policy & Spend | A | 40 | 38 | 6 | 37 | 1 | 0 | — | notStarted (generated) |
| `BO-107` | Guests & Marketing | A | 42 | 28 | 6 | 25 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-068` Audit Log

**See who changed what at this venue.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Guests & Marketing · wave 2 · needs the `core` module |
| Block | Block B · ticket #29110 (VM-BO-068) |
| Who uses it | venue staff holding `AUDIT_VIEW`, `SCOPE_VIEW` (2 read); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAuditRecords` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/audit-log` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried `listAiInteractions` alone** — an audit log showing only AI prompts. The platform audit record is `identity.audit_event`. **Rewired 20 August.** **`listAuditRecords` wired 24 August.** This screen declared zero operations — an audit log with nothing behind it — and `platform.audit_record` was written by nothing and read by nothing. **Found by mapping the POS pack**, where four separate frames wanted an audit view. **Retail board operations wired 24 August.** **Platform-staff access shown 28 September (audit R098)** — `listPlatformStaffGrants` lists every grant a TICVAI operator opened into this tenant, and the `platformStaffGrantId` filter of `listAuditRecords` shows what was done under each.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Resolve permissions (a permission simulator) was a button on the audit log; it belongs to role management and is declared on BO-054 (design-notes correction …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Who did what, where and when in the venues in scope, including every action a TICVAI platform operator took under a grant into the tenant. Audit records are read-only and immutable; the screen filters and exports, never edits.

**Fixed on main** (the package already carries these; draw what it says): Resolve permissions (simulate a principal's permissions) is a button on the audit log. (CHG-WIR-021); Filters are free-text id fields (org unit id, principal id, workstation id, subject ref). (CHG-SBO-015); Tables show every schema field, plumbing included: 'Every audit' drop id, principalId, orgUnitId, workstationId, platformStaffGrantId … (CHG-SBO-004); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Where | picker: choose an id | optional | — | — | shows names, sends the id | A pick list in words, never a typed id (design-note correction, 2 October 2026). | `OrgUnit.id` |
| Who | picker: choose a principal | optional | — | — | shows names, sends the id | A pick list of people by name. | `AuditRecord.principalId` |
| Till or device | picker: choose an id | optional | — | — | shows names, sends the id | A pick list in words, never a typed id (design-note correction, 2 October 2026). | `Workstation.id` |
| Action | text field | optional | — | — | — | Sends `?action=` to `listAuditRecords`. | `listAuditRecords` ?action |
| About | search field | — | — | — | — | Search by what the record is about (an order number, a product name), never a raw reference. | `listAuditRecords` |
| From | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?from=` to `listAuditRecords`. | `listAuditRecords` ?from |
| To | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?to=` to `listAuditRecords`. | `listAuditRecords` ?to |
| Under a TICVAI grant | select field | — | — | — | — | Pick one of the grants listed below, by operator and reason. | — |
| Open grants only | toggle | — | — | — | — | Sends `?activeOnly=true` to `listPlatformStaffGrants`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Org unit | picker: choose an org unit | — | — | `listAuditRecords` ?orgUnitId |
| Principal | picker: choose a principal | — | — | `listAuditRecords` ?principalId |
| Workstation | picker: choose a workstation | — | — | `listAuditRecords` ?workstationId |
| Subject ref | text field | — | — | `listAuditRecords` ?subjectRef |
| Platform staff grant | picker: choose a platform staff grant | — | — | `listAuditRecords` ?platformStaffGrantId |
| Active only | toggle | off | — | `listPlatformStaffGrants` ?activeOnly |
| Under | text field | — | — | `listOrgUnits` ?under |
| Level | select | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet; Modelling a restaurant as a department would put it in the staffing tree, which is why the two cannot be collapsed (CF-138, ADR-0018). | `listOrgUnits` ?level |
| Include inactive | toggle | off | — | `listOrgUnits` ?includeInactive |
| Sale board kind | radio group | — | Ticketing · Fnb · Retail · Mixed | `listWorkstations` ?saleBoardKind |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Filters**: Person (picker, not an id), venue or department (tree), workstation (picker), action (list), date range in the venue's time zone; "Platform staff only" toggle. *(source: contracts/spine/tenancy.yaml#listAuditRecords; contracts/spine/identity.yaml#listPlatformStaffGrants)*

#### Outputs: what the screen shows and produces

**Shown**

**Every audit** (data table, from `listAuditRecords`)

| Shows | Format | Notes |
|---|---|---|
| Action | text | What was done, as the writing operation names it. |
| Subject ref | text | The thing acted on — a profile, a shift, an order. The same value the `subjectRef` filter matches. |
| Occurred at | 1 Oct 2026, 14:30 | When. The list is ordered by this, most recent first. |

**Platform-staff grants** (data table, from `listPlatformStaffGrants`): **Every platform-staff grant into this tenant is visible here** — open, expired and ended, most recent first. Choosing a grant filters the audit log on `platformStaffGrantId` to show what was done under it (decided 28 September, audit R098).

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Reason | text | — |
| Ticket ref | text | — |
| Permissions | list or chips (count when long) | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Platform-staff grants**: Each grant with operator name, permissions, reason, ticket reference, opened and expiry; open grants highlighted; selecting one filters the log to its actions. *(source: contracts/spine/identity.yaml#listPlatformStaffGrants; R098)*

**Data it reads**: `listAuditRecords` (onLoad, Who did what, where, and when); `listPlatformStaffGrants` (onLoad, Every platform-staff grant into this tenant, so the tenant …); `listOrgUnits` (onLoad, List scope nodes visible to the session (the pick list)); `listWorkstations` (onLoad, List workstations (the pick list))

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audit log list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audit log untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audit log yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on orgUnitId, principalId, workstationId, action, subjectRef, from and platformStaffGrantId; the audit log is still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AUDIT_VIEW`, which `listAuditRecords` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds AUDIT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PERMISSION_VIEW for Resolve permissions. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/identity.yaml#resolvePermissions)*

#### Consistency with other screens

- Match `ADM-412`: Every action taken under a Console grant appears here, visible to the tenant.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
records:
- when: 01/10/2026 10:12
  who: Omar Haddad
  where: Main Gate Till 3
  action: Refund approved
  subject: Order AQC-AUH-260930-0412
- when: 01/10/2026 09:30
  who: Sara Khalil (TICVAI, grant SUP-8812)
  where: AquaCove Muscat
  action: Payment provider changed
```

#### Permissions

- `listAuditRecords` → `AUDIT_VIEW` (read) · staff
- `listPlatformStaffGrants` → `AUDIT_VIEW` (read) · staff
- `listOrgUnits` → `SCOPE_VIEW` (read) · staff
- `listWorkstations` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `AUDIT_VIEW`, which `listAuditRecords` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

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

- Audit history shows logins, shift start/end and every change made (old value vs new value) on every screen and transaction; logging can be switched on/off and archived. *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-158)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-068` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 6.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 6.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 6.dc.html#ret-6j`
- Flow F106 *A security dashboard surfaces something and it is investigated*, step 3: Audit Log. → 2 operations, 0 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-068?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `AUDIT_VIEW`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-073` Lost & Found Register

**Match what was lost to what was handed in.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Guests & Marketing · wave 2 · needs the `marketing` module |
| Block | Block D · task VM-BO-073 |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listLostItems` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `itemId` (deepLink) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/venue-operations/lost-found-register` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried `listCases` and `createCase`.** `LostItem` exists — CL-07 built it as one entity in two directions, lost and found — and a service case is a different thing. **Rewired 20 August.**

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Staff match what was lost to what was handed in, and hand it back. The match is the capability: a guest reports a lost phone, a cleaner hands one in, and without both sides in one register somebody searches by hand. Lost and found items are one entity in two directions (lost, found).

**Known correction pending (do not draw the wrong version)**

- **recordLostItem is not on BO-073, so staff cannot hand in a found item here.** Why: The register needs its "found" side. Add recordLostItem. *(source: contracts/satellite/marketing-crm.yaml#recordLostItem; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*
- **Guest reports are cases (raiseMyCase) and never become LostItem rows.** Why: See WEB-034; without it the register's "lost" side is empty. *(source: contracts/satellite/marketing-crm.yaml#raiseMyCase; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*
- **emptyNoResults says "listLostItems takes no filter".** Why: A register with hundreds of items needs filters (lost or found, status, kind, date). Add filter parameters. *(source: contracts/satellite/marketing-crm.yaml#listLostItems; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

**Fixed on main** (the package already carries these; draw what it says): getLostItemMatches ("candidate matches, scored") is consumed by no screen; the "Find matches" button is wired to matchLostItem, which ties … (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Form: Decide: tie, return or dispose** (modal, opened by *Decide: tie, return or dispose*; *Decide: tie, return or dispose* calls `matchLostItem`, *Cancel* sends nothing)

**Collects what `matchLostItem` sends before it is called.** Required: `action`. Optional: `otherItemId`, `claimantSubjectId`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | radio group | required | — | Match · Unmatch · Claim · Return · Dispose | — | — | `matchLostItem` body |
| Other item `otherItemId` | picker: choose an other item | optional | — | — | shows names, sends the id | — | `matchLostItem` body |
| Claimant subject `claimantSubjectId` | picker: choose a claimant subject | optional | — | — | shows names, sends the id | — | `matchLostItem` body |
| Note `note` | text area | optional | — | — | — | — | `matchLostItem` body |

Errors to draw in the form: 409 The item's `status` does not allow the action (`states/lost-item.yaml`) — `match` and `return` need `open`, `unmatch` and `claim` need `matched`, `dispose` … (StateTransitionProblem)

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Record found item**: Kind, colour, brand, description, where found, when, photos, storage location; the "dispose after" date defaults from the venue's retention setting. *(source: contracts/satellite/marketing-crm.yaml#recordLostItem; DI-380)*
- **Filters**: Lost or found, status, kind, date range, area. *(source: designer default)*

#### Outputs: what the screen shows and produces

**Shown**

**Every lost** (data table, from `listLostItems`)

| Shows | Format | Notes |
|---|---|---|
| Found or lost | chip: Lost, Found | One entity, two directions. A guest reports a loss and a steward reports a find, and modelling them separately means matching across two … |
| Kind | chip: Bag, Phone, Wallet, Keys, Clothing, Jewellery… | — |
| Description | text | — |
| Colour | text | — |
| Reported at | 1 Oct 2026, 14:30 | Device time — `recordLostItem` is offline-capable, so this is when the loss was reported or the find handed in, not when the device synced. |
| Status | chip: Open, Matched, Claimed, Disposed, Returned | — |

**Suggested matches** (data table, from `getLostItemMatches`)

| Shows | Format | Notes |
|---|---|---|
| Lost item | the name it points at, never the id | — |
| Found item | the name it points at, never the id | — |
| Score | 1,234.5 | — |
| Matched on | list or chips (count when long) | What agreed — kind, colour, brand, location, date. |

**The selected lost** (detail panel, from `listLostItems`)

| Shows | Format | Notes |
|---|---|---|
| Found or lost | chip: Lost, Found | One entity, two directions. A guest reports a loss and a steward reports a find, and modelling them separately means matching across two … |
| Kind | chip: Bag, Phone, Wallet, Keys, Clothing, Jewellery… | — |
| Description | text | — |
| Colour | text | — |
| Brand | text | — |
| Reported at | 1 Oct 2026, 14:30 | Device time — `recordLostItem` is offline-capable, so this is when the loss was reported or the find handed in, not when the device synced. |
| Storage location | text | — |
| Status | chip: Open, Matched, Claimed, Disposed, Returned | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Decide: tie, return or dispose (primary button) | `matchLostItem` POST `/lost-items/{itemId}/match` | inline | LostItem | 409 The item's `status` does not allow the action (`states/lost-item.yaml`) — `match` and `return` need `open`, `unmatch` and `claim` need `matched`, `dispose` … (StateTransitionProblem) | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Register**: Two columns of the same list (Lost reports, Found items), with possible matches linked between them and a match score with its reasons (kind, colour, place, time). *(source: contracts/satellite/marketing-crm.yaml#listLostItems; contracts/satellite/marketing-crm.yaml#getLostItemMatches)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Match**: Ties a report to a found item; the guest's case shows "Possible match" and asks them to confirm. *(source: contracts/satellite/marketing-crm.yaml#matchLostItem)*
- **Claim and return**: Records the claimant (verified against the report) and the hand-back; the case is resolved. *(source: contracts/satellite/marketing-crm.yaml#matchLostItem)*
- **Dispose**: After the dispose-after date only; needs a note. *(source: contracts/satellite/marketing-crm.yaml#matchLostItem)*

**Data it reads**: `listLostItems` (onLoad, Reported and found, with suggested matches)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The lost found register list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the lost found register untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No lost found register yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listLostItems` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `CASE_VIEW`, which `listLostItems` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CASE_MANAGE` for `matchLostItem`, `recordLostItem`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The item's `status` does not allow the action (`states/lost-item.yaml`) — `match` and `return` need `open`, `unmatch` and `claim` need `matched`, `dispose` … (StateTransitionProblem) |

#### Consistency with other screens

- Match `WEB-034`: The guest's report and status words match the register.
- Match `EMP-028`: Stewards hand items in from the staff app; they appear here as found.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
lost:
  ref: L-2026-0311
  kind: Bag
  colour: Black
  brand: Herschel
  where: Wave Pool loungers
  when: 26 Sep 15:00
  case: CA-1042
found:
  ref: F-2026-0587
  kind: Bag
  colour: Black
  where: Lockers B
  when: 26 Sep 16:40
  storage: Guest Services shelf 3
  disposeAfter: 26 Oct 2026
matchReason: Same kind and colour, 200 m apart, 1h 40m later
```

#### Permissions

- `listLostItems` → `CASE_VIEW` (read) · staff, guest
- `matchLostItem` → `CASE_MANAGE` (configure) · staff
- `recordLostItem` → `CASE_MANAGE` (configure) · staff, guest
- `getLostItemMatches` → `CASE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `CASE_VIEW`, which `listLostItems` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CASE_MANAGE` for `matchLostItem`, `recordLostItem`.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.69 | Lost & Found - System shall support lost and found requests. | Guest Mobile App & Branding | CONTRACTED | data `LostItem` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Lost & Found: guests log lost items in the app; back-office staff match and mark items found for collection, with full tracking. *(client request · MoM 10 Aug 2026, 4.6 AI Functions, Lost & Found, Reviews, Loyalty · DI-208)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-073` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-073?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Decide: tie, return or dispose.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-091` AI Policy & Spend

**What the assistant may do here, what it has cost, and what happens at the ceiling.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Guests & Marketing · wave 1 · needs the `ai` module |
| Block | Block A · ticket #28939 (APP-SETUP-BO-091) |
| Who uses it | venue staff holding `AI_AUDIT_VIEW`, `AI_CONFIGURE`, `AI_USE` (1 read, 1 configure, 1 operate); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listIndexFailures` reads the population and `getAiPolicy` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `profileKey` (navigation), `tenantId` (navigation) |
| Route | `/ai/policy` |

**What the spec says about it.** Added 17 August. **Staff and guest spend shown separately** — a venue can manage the first and cannot stop guests asking questions. At the ceiling the manager decides whether to continue; the assistant does not stop on its own (CF-14). **Index failures sit beside spend on purpose** - both answer the same two questions, is the assistant working and what is it costing, and a failure rate is the cheaper half of that answer.

**From the AI & Intelligence process.** The venue manager's AI control panel: what the assistants may do at this venue, what AI has cost this month and will cost by month end, and what happens at the budget ceiling. It answers two questions at a glance - is the AI working, and what is it costing - with staff and guest spend shown apart, because a venue can manage the first and cannot stop guests asking. The one thing to get right: a venue can only narrow what the tenant set, never widen it, and the screen must show which values are inherited.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Staff and guest spend shown separately (notes, CF-14), but getAiUsage groupBy has no audience. (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The main dataTable is "Every index failure" (listIndexFailures) with job id and stage filters. (CHG-SBO-007); The policy form carries retainInteractionsDays. (CHG-SBO-007); getAiByokEnablement is not declared, though its description says BO-091 reads it. (CHG-WIR-012); The form exposes engine tuning (retrieveTopK, rerankTopK, semanticCacheThreshold, negativeCacheTtlSeconds, chunking, quantisation, hnsw … (CHG-SBO-007).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the ceiling expressed to the venue in AED or in tokens?** → The AI spend ceiling is shown and set in the tenant's selected currency (default USD), with tokens shown alongside. *(decided by Chinmay, 2026-10-02; DEC-008 / CHG-NOTE-001)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Scope path | text field | — | — | `getAiPolicy` ?scopePath |
| From | date picker | — | — | `getAiUsage` ?from |
| Group by | select | — | Tenant · Venue · Principal · Provider · Capability · Day · Agent · Model · Task | `getAiUsage` ?groupBy |
| Job | picker: choose a job | — | — | `listIndexFailures` ?jobId |
| Stage | radio group | — | Fetch · Parse · Chunk · Embed · Upsert | `listIndexFailures` ?stage |
| Family | select | — | Gateway and models · Governance · Action pipeline · Knowledge retrieval · Assistants · Analytics insights · Configuration assistant · Forecasting · Anomaly detection · Risk intelligence · Recommendations · Decision records … | `listAiCapabilities` ?family |
| Status | segmented control | — | Active · Paused | `listAiCapabilities` ?status |
| Risk class | radio group | — | Low · Medium · High · Critical | `listAiCapabilities` ?riskClass |
| Capability key | text field | — | — | `getEffectiveAiPolicy` ?capabilityKey |
| Scope path | text field | — | — | `getEffectiveAiPolicy` ?scopePath |
| Environment | radio group | — | Development · Sandbox · Staging · Production | `getEffectiveAiPolicy` ?environment |
| Audience | segmented control | — | Staff · Guest · Support | `listAssistantProfiles` ?audience |

**Form: Save AI policy** (modal, opened by *Save AI policy*; *Save AI policy* calls `setAiPolicy`, *Cancel* sends nothing)

**Collects what `setAiPolicy` sends before it is called.** Required: `scopeLevel`, `scopePath` (from the session, not typed), `enabledCapabilities`. Optional: `allowedRoleIds`, `maskedFields`, `requiresApprovalFor`, `ceilingBehaviour`, `ceilingWarningPercent`, `guestCapabilityScope`, `cacheAnswers`, `cacheTtlMinutes`. **Not drawn:** `retainInteractionsDays` (deprecated 29 September, AI-D05; retention is a tenant setting per data class) and the engine tuning (`retrieveTopK`, `rerankTopK`, `semanticCacheThreshold`, `negativeCacheTtlSeconds`, chunking, quantisation, hnsw, cascade), which is platform tuning left to the console, not a venue manager's decision. The money ceiling is set with Save …

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope level `scopeLevel` | segmented control | required | — | Tenant · Venue | — | Tenant sets the default; a venue may narrow it and never widen it. | `setAiPolicy` body |
| Scope path `scopePath` | text field | required | — | — | — | The node this row belongs to, and the key it is written under — the tenant's node where `scopeLevel` is `tenant`, a venue's where it is `venue`. | `setAiPolicy` body |
| Enabled capabilities `enabledCapabilities` | multi-select chips | required | — | Assist · Search · Generate configuration · Generate layout · Summarise · Explain · Gateway and models · Governance · Action pipeline · Knowledge retrieval · Assistants · Analytics insights …; `governance`, `decisionRecords` and `residencyPrivacy` cannot be … | — | Extended on 29 September to the fourteen capabilities of the AI design (section 1.1, `AiCapabilityFamily`). | `setAiPolicy` body |
| Allowed roles `allowedRoleIds` | multi-picker: choose allowed roles | optional | — | — | — | — | `setAiPolicy` body |
| Masked fields `maskedFields` | list of values (chips) | optional | — | An entry naming no column is refused at save rather than silently masking nothing. | — | Redacted before a prompt leaves the platform (8.3.73). Defaults to every field in the pii schema — a masking list nobody filled in should send nothing rather than everything. | `setAiPolicy` body |
| Requires approval for `requiresApprovalFor` | multi-select chips | optional | — | Pricing · Promotion · Operational · Financial · Configuration | — | 8.3.61–8.3.64. Nothing in this list executes without a decision. | `setAiPolicy` body |
| Monthly token ceiling `monthlyTokenCeiling` | number field | optional | — | — | — | — | `setAiPolicy` body |
| Ceiling behaviour `ceilingBehaviour` | segmented control | optional | Warn | Warn · Warn then disable · Block | — | Decided 17 August: warn, and let the venue manager choose. A cap that stops the assistant mid-visit turns a cost control into a guest-facing outage, and the venue has no warning … | `setAiPolicy` body |
| Ceiling behaviour by capability `ceilingBehaviourByCapability` | repeatable rows | optional | — | — | — | Ceiling behaviour per capability (AI design 5.9, AIC-227), so a budget never silently disables fraud scoring, which spends no tokens, or a critical capability. | `setAiPolicy` body |
| Capability `ceilingBehaviourByCapability[].capability` | text field | required | — | — | — | An `AiCapabilityFamily` value, or a registered capability key. | `setAiPolicy` body |
| Behaviour `ceilingBehaviourByCapability[].behaviour` | radio group | required | — | Warn · Warn then disable · Block · Never restrict | — | — | `setAiPolicy` body |
| Autonomy overrides `autonomyOverrides` | repeatable rows | optional | — | — | — | Tighten only (AI design 3.8, AIC-151). A level per capability at or below the capability's ceiling, and on a venue row at or below the tenant row's. | `setAiPolicy` body |
| Capability key `autonomyOverrides[].capabilityKey` | text field | required | — | — | — | — | `setAiPolicy` body |
| Autonomy level `autonomyOverrides[].autonomyLevel` | stepper or slider | required | — | min 0; max 4; 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after … | — | One autonomy scale for every capability (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). | `setAiPolicy` body |
| Ceiling warning percent `ceilingWarningPercent` | number field | optional | 80 | — | — | Warn before the ceiling, not at it. A manager told at 100% has already spent it; one told at 80% can decide with a week left. | `setAiPolicy` body |
| Guest capability scope `guestCapabilityScope` | multi-select chips | optional | — | Ticket selection · Promotions · FAQ · Recommendations · Checkout · Wait times · Wayfinding · Visit planning | — | What a guest-facing assistant may help with, and nothing else (2.1.28). Bounding the capability is what makes the cost predictable and the safety posture tractable — an assistant … | `setAiPolicy` body |
| Retrieve top k `retrieveTopK` | number field | optional | 30 | — | — | How many chunks retrieval returns before reranking. | `setAiPolicy` body |
| Rerank top k `rerankTopK` | number field | optional | 5 | — | — | How many survive the rerank and reach the model. Reranking reduces cost as well as improving quality, which is unusual — retrieval is cheap and the tokens sent to the model are … | `setAiPolicy` body |
| Cache answers `cacheAnswers` | toggle | optional | on | — | — | The largest cost lever available at a kiosk. Guest questions are extraordinarily repetitive — forty questions, thousands of times a day — where staff questions are diverse. | `setAiPolicy` body |
| Cache ttl minutes `cacheTtlMinutes` | number field (minutes) | optional | 60 | — | — | An upper bound on top of event invalidation, not instead of it. The key carries `scope_path` — a cache keyed on the question alone is a cross-venue leak wearing a performance hat. | `setAiPolicy` body |
| Semantic cache threshold `semanticCacheThreshold` | stepper or slider | optional | 0.95 | min 0; max 1 | — | Similarity above which a cached answer serves a new question. `cache:answer` is exact-match on question, scope and locale — *what time do you close* and *when do you shut* are two … | `setAiPolicy` body |
| Negative cache ttl seconds `negativeCacheTtlSeconds` | number field (seconds) | optional | 300 | — | — | How long *no answer found* is remembered. A miss costs a full retrieval and a completion. | `setAiPolicy` body |
| Cascade `cascade` | group | optional | — | — | — | A small model answers and escalates only below a confidence threshold. `ai.suggestion.confidence` exists and nothing routes on it. | `setAiPolicy` body |
| Small model `cascade.smallModel` | text field | optional | — | — | — | — | `setAiPolicy` body |
| Large model `cascade.largeModel` | text field | optional | — | — | — | — | `setAiPolicy` body |
| Escalate below `cascade.escalateBelow` | number field | optional | 0.7 | — | — | — | `setAiPolicy` body |
| Chunking `chunking` | group | optional | — | — | — | The single biggest lever on retrieval quality, and currently nowhere. A venue FAQ and a maintenance manual do not chunk the same way. | `setAiPolicy` body |
| Size tokens `chunking.sizeTokens` | number field | optional | 512 | — | — | — | `setAiPolicy` body |
| Overlap tokens `chunking.overlapTokens` | number field | optional | 64 | — | — | — | `setAiPolicy` body |
| Strategy `chunking.strategy` | segmented control | optional | Sentence | Fixed · Sentence · Semantic | — | — | `setAiPolicy` body |
| Quantisation `quantisation` | segmented control | optional | None | None · Scalar · Binary | — | A decision, never a default. `scalar` int8 is roughly four times smaller — 49 GB becomes 12 — and it costs recall. | `setAiPolicy` body |
| Hnsw `hnsw` | group | optional | — | — | — | Defaults are tuned for neither our recall nor our latency. A collection built with the wrong ones needs a rebuild, which is why this is a creation decision like the sparse index. | `setAiPolicy` body |
| M `hnsw.m` | number field | optional | 16 | — | — | — | `setAiPolicy` body |
| Ef construct `hnsw.efConstruct` | number field | optional | 128 | — | — | — | `setAiPolicy` body |
| Ef search `hnsw.efSearch` | number field | optional | 64 | — | — | — | `setAiPolicy` body |
| Per request token ceiling `perRequestTokenCeiling` | number field | optional | — | — | — | One runaway conversation can spend a tenant's month. `monthlyTokenCeiling` discovers that after it has happened. | `setAiPolicy` body |
| Streams by capability `streamsByCapability` | list of values (chips) | optional | — | — | — | Time to first token and total latency are separate targets. A concierge that starts answering in 300 ms and finishes in 4 seconds is better than one silent for 2. | `setAiPolicy` body |
| Fallback provider `fallbackProviderId` | picker: choose a fallback provider | optional | — | — | shows names, sends the id | BL-151: a provider outage with no fallback is every AI surface going dark at once. | `setAiPolicy` body |
| Guardrail short circuit `guardrailShortCircuit` | toggle | optional | on | — | — | A refusal a rule can decide never reaches a model. Cheaper, faster and more consistent than asking a model to refuse. | `setAiPolicy` body |

**Form: Save spend ceiling** (modal, opened by *Save spend ceiling*; *Save spend ceiling* calls `setAiSpendCeiling`, *Cancel* sends nothing)

**Collects what `setAiSpendCeiling` sends before it is called.** Required: `spend`. `spend` is Money in the tenant's selected currency (USD by default); the token equivalent is shown, not typed. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Spend `spend` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Per month, in the tenant's selected currency; until the tenant changes it, the tenant's billing currency (AED for a UAE tenant), not USD (CHG-RUL-017). | `setAiSpendCeiling` body |

Errors to draw in the form: 400 Validation failed

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **monthlyTokenCeiling / ceilingBehaviour / ceilingWarningPercent**: Ceiling as a monthly amount with the behaviour as three explained choices - Warn (default: "Sahli keeps answering; you are told at 80% and at the ceiling"), Warn then switch off, Block. Warning percent defaults to 80. Empty ceiling means no ceiling, said in words. *(source: contracts/satellite/ai.yaml#/components/schemas/AiPolicy / screens/P08-venue-back-office.yaml#BO-091 (notes, CF-14))*
- **ceilingBehaviourByCapability**: Per-capability override list; fraud and risk scoring default to "Never restrict" (it spends no tokens) and the guest concierge to Warn. A capability not listed follows the general behaviour - say so in the row. *(source: contracts/satellite/ai.yaml#/components/schemas/AiPolicy (ceilingBehaviourByCapability))*
- **maskedFields**: Shown as the list of personal-data fields that never leave the platform, all ticked by default. Clearing the list does not send everything - the default (every pii field) applies; the UI must say "An empty list masks every personal field" and never offer "send all". *(source: contracts/satellite/ai.yaml#/components/schemas/AiPolicy (maskedFields) / ADR-0020)*
- **enabledCapabilities / guestCapabilityScope / autonomyOverrides / requiresApprovalFor**: Toggles and selects showing the tenant's value beside each venue value ("From tenant: on"). A venue can switch off or lower, never switch on what the tenant switched off or raise autonomy above the capability ceiling; values above are drawn disabled with the reason. governance, decisionRecords and residencyPrivacy are always on and not drawn as toggles. *(source: contracts/satellite/ai.yaml#setAiPolicy / ADR-0050 / ADR-0018)*
- **assistant profiles**: One row per profile (guest concierge, support chatbot, staff by role, planner): audience, roles, knowledge collections, languages, hand-over target, active. A guest profile's scope can only be a subset of the policy's guest scope. *(source: contracts/satellite/ai.yaml#configureAssistantProfile)*

#### Outputs: what the screen shows and produces

**Shown**

**Spend ceiling** (detail panel, from `getAiSpendCeiling`): **In the tenant's selected currency, USD by default, with tokens shown alongside (decided 2 October 2026 by Chinmay, DEC-008; CHG-CSA-004).** At the ceiling the manager decides whether to continue (CF-14).

| Shows | Format | Notes |
|---|---|---|
| Spend | AED 1,234.50 | Per month, in the tenant's selected currency; until the tenant changes it, the tenant's billing currency (AED for a UAE tenant), not USD … |
| Token equivalent | 1,234 | What `spend` buys at the current blended rate, shown beside it on BO-091. |
| Updated at | 1 Oct 2026, 14:30 | — |

**Bring your own key** (detail panel, from `getAiByokEnablement`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Enabled | yes / no (icon or chip) | — |
| Coverage | chip: Per task, All tasks | Whether the tenant may supply a key per task or one key for everything. |
| Allowed tasks | list or chips (count when long) | Where `coverage` is `perTask`: the gateway tasks a tenant key may serve. Empty means any. |
| Task model map | list or chips (count when long) | The provider's equivalent model for each task, chosen by TICVAI (Chinmay, 2 October, workbook Q1; closes AI-D20; CHG-CSA-001). |
| Task key | text | — |
| Tier | text | — |
| Model | the name it points at, never the id | — |
| Compatibility passed | yes / no (icon or chip) | Whether the provider's compatibility test passed for this task (`AiProviderCompatibility`, CHG-FUP-008); a task that has not passed stays … |
| Reason | text | — |
| Platform staff grant | the name it points at, never the id | The open platform-staff grant the change was made under (audit R098). |
| Decided by principal | the name it points at, never the id | — |
| Decided at | 1 Oct 2026, 14:30 | — |

**The AI usage report** (detail panel, from `getAiUsage`)

| Shows | Format | Notes |
|---|---|---|
| Currency | text | The tenant's selected currency, by default its billing currency (AED for a UAE tenant), not USD (CHG-RUL-017; Chinmay, 2 October, workbook … |
| Ceiling | grouped details | The spend ceiling in force (`getAiSpendCeiling`), with the tokens it equals at the current blended rate and what is used so far … |
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | text | — |
| Rows | list or chips (count when long) | — |
| Forecast | grouped details | A month-end projection, labelled a forecast (AI design 2.3, 4.5). Present where `to` is inside the current month. |

**The AI policy** (detail panel, from `getAiPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Scope level | chip: Tenant, Venue | Tenant sets the default; a venue may narrow it and never widen it. |
| Enabled capabilities | list or chips (count when long) | Extended on 29 September to the fourteen capabilities of the AI design (section 1.1, `AiCapabilityFamily`). |
| Allowed roles | list or chips (count when long) | — |
| Masked fields | list or chips (count when long) | Redacted before a prompt leaves the platform (8.3.73). Defaults to every field in the pii schema — a masking list nobody filled in should … |
| Requires approval for | list or chips (count when long) | 8.3.61–8.3.64. Nothing in this list executes without a decision. |
| Monthly token ceiling | 1,234 | — |
| Ceiling behaviour | chip: Warn, Warn then disable, Block | Decided 17 August: warn, and let the venue manager choose. A cap that stops the assistant mid-visit turns a cost control into a … |
| Ceiling warning percent | 1,234 | Warn before the ceiling, not at it. A manager told at 100% has already spent it; one told at 80% can decide with a week left. |
| Guest capability scope | list or chips (count when long) | What a guest-facing assistant may help with, and nothing else (2.1.28). Bounding the capability is what makes the cost predictable and the … |
| Cache answers | yes / no (icon or chip) | The largest cost lever available at a kiosk. Guest questions are extraordinarily repetitive — forty questions, thousands of times a day — … |
| Cache ttl minutes | 1,234 | An upper bound on top of event invalidation, not instead of it. The key carries `scope_path` — a cache keyed on the question alone is a … |

**Index health** (detail panel, from `listIndexFailures`): Secondary: records the assistant could not embed, beside spend, because both answer "is the assistant working and what is it costing".

| Shows | Format | Notes |
|---|---|---|
| Stage | chip: Fetch, Parse, Chunk, Embed, Upsert | Where it failed decides who fixes it. A parse failure is a document problem; an embed failure is a provider one. |
| Error | text | — |
| Attempts | 1,234 | — |
| Document ref | text | What would not index. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save AI policy (primary button) | `setAiPolicy` PUT `/policy` | AiPolicy | AiPolicy | — | opens modal first |
| Save spend ceiling (secondary button) | `setAiSpendCeiling` PUT `/policy/spend-ceiling` | AiSpendCeiling | AiSpendCeiling | 400 Validation failed | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **spend**: Month to date in AED against the ceiling with the 80% line; the month-end projection drawn dashed and labelled "Forecast" with its basis (e.g. "run rate of the last 7 days"); never added into the month-to-date figure. Split by staff and guest, then by agent/capability. Interactions, p95 latency and refusal rate per row. *(source: contracts/satellite/ai.yaml#getAiUsage (AiUsageReport.forecast) / DI-968)*
- **rejection rate**: Shown per capability as "proposals your team refused" - the measure of whether an assistant is worth having. *(source: contracts/satellite/ai.yaml#getAiUsage (rows.rejectionRate))*
- **knowledge indexing health**: A small secondary panel: failures by stage. parse failures are the venue's document to fix (link to it); embed/upsert failures are the platform's. Not the screen's main table. *(source: contracts/satellite/ai.yaml#listIndexFailures / screens/P08-venue-back-office.yaml#BO-091 (notes))*
- **bring your own key**: Read-only line saying whether this tenant may use its own provider key (decided by TICVAI per tenant). *(source: contracts/satellite/ai.yaml#getAiByokEnablement / MoM 21 Sep 4.10 (AI-D14))*
- **Ceiling currency**: The ceiling is shown and set in the tenant's selected currency (USD unless the tenant picks another, e.g. AED), with the token count beside it as the second figure. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-001))*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Save AI policy**: Saves the venue row (scopeLevel venue). A change that would widen the tenant's policy is refused and the field says why. Saving a lower ceiling than spend so far warns before saving. *(source: contracts/satellite/ai.yaml#setAiPolicy)*
- **Save assistant profile**: Replaces (200) or creates (201) the profile; a guest scope wider than the policy is refused on the field. *(source: contracts/satellite/ai.yaml#configureAssistantProfile)*

**Data it reads**: `getAiPolicy` (onLoad, What the assistant may do here); `getAiUsage` (onLoad, Usage, cost and performance); `listIndexFailures` (onLoad, Records an index could not embed, and at which stage); `listAiCapabilities` (onLoad, The capability registry); `getEffectiveAiPolicy` (onLoad, The policy in force for a capability at a scope); `listAssistantProfiles` (onLoad, Assistant profiles); `getAiByokEnablement` (onLoad, Whether the venue may bring its own key); `getAiSpendCeiling` (onLoad, The spend ceiling in the tenant's selected currency, with …)

**Where the user goes next**

- → `ADM-004` Platform Audit Log: *Platform Audit Log*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The policy spend list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the policy spend untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No policy spend yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: nothing on this screen filters. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_CONFIGURE`, which `getAiPolicy` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Ceiling reached with Warn**: Banner "You've reached this month's AI budget. Assistants keep working until you change it." with Change ceiling / Switch off guest concierge. *(source: contracts/satellite/ai.yaml#/components/schemas/AiPolicy (ceilingBehaviour "decided 17 August"))*
- **No venue row yet**: The tenant's policy is shown as in force ("Using your organisation's AI settings") with Customise for this venue; never an empty state. *(source: contracts/satellite/ai.yaml#getAiPolicy ("nearest ancestor wins"))*
- **Caller lacks AI_AUDIT_VIEW but has AI_CONFIGURE**: Policy is editable; the spend panel says which permission shows spend. *(source: contracts/satellite/ai.yaml#getAiUsage / contracts/satellite/ai.yaml#getAiPolicy)*

#### Consistency with other screens

- Match `ADM-037`: The provider and key are set by TICVAI on the console; this screen only shows which provider serves the venue and whether BYOK is allowed.
- Match `ADM-522`: The same L0-L4 labels and ceilings as the console's autonomy screen.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Coastal Aqua
policy:
  ceiling: AED 3,000.00 / month
  behaviour: Warn
  warnAt: 80%
  guestScope:
  - ticketSelection
  - faq
  - waitTimes
  - wayfinding
  - recommendations
spend:
  monthToDate: AED 1,742.50
  forecast: AED 2,610.00 by 31 Oct (run rate of the last 7 days)
  rows:
  - agent: Guest concierge (Sahli)
    audience: guest
    interactions: 18420
    cost: AED 1,206.30
    refusalRate: 3%
  - agent: Staff assistant
    audience: staff
    interactions: 2310
    cost: AED 391.10
    rejectionRate: '-'
  - agent: Configuration assistant
    audience: staff
    interactions: 96
    cost: AED 145.10
    rejectionRate: 12%
indexFailures:
- document: Refund policy v3.pdf
  stage: parse
  error: Scanned PDF with no text layer
  attempts: 3
```

#### Permissions

- `getAiPolicy` → `AI_CONFIGURE` (configure) · staff
- `setAiPolicy` → `AI_CONFIGURE` (configure) · staff
- `getAiUsage` → `AI_AUDIT_VIEW` (read) · staff
- `listIndexFailures` → `AI_CONFIGURE` (configure) · staff
- `listAiCapabilities` → `AI_USE` (operate) · staff
- `getEffectiveAiPolicy` → `AI_USE` (operate) · staff
- `configureAssistantProfile` → `AI_CONFIGURE` (configure) · staff
- `listAssistantProfiles` → `AI_USE` (operate) · staff
- `getAiByokEnablement` → `AI_CONFIGURE` (configure) · staff
- `getAiSpendCeiling` → `AI_CONFIGURE` (configure) · staff
- `setAiSpendCeiling` → `AI_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `AI_CONFIGURE`, which `getAiPolicy` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

37 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.1 | Provides control, transparency and accountability over AI-generated outputs. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.55 | System shall log all AI prompts. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.56 | System shall log all AI responses. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.57 | System shall log all AI actions. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.58 | System shall maintain AI audit trails. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.59 | System shall maintain AI decision history. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.60 | System shall maintain AI execution history. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.61 | System shall require approval before AI-driven pricing changes. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.62 | System shall require approval before AI-driven promotions. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.63 | System shall require approval before AI-driven operational changes. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.64 | System shall require approval before AI-driven financial actions. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.65 | System shall support multi-level AI approvals. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| … 25 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI operations monitoring shows health, cost/budget tracking and which AI agents consume the most resources and for what purpose, so the business can manage AI spend. *(client request · MoM 21 Sep 2026, 4.11 Core AI Platform — Operations & Consumption Monitoring · DI-968)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-091` · status **notStarted** · provenance generated
- Flow F100 *An AI provider is configured, budgeted and audited*, step 2: AI Policy & Spend. → 3 operations, 3 of them previously unwalked.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)
- ADR-0033 *Every asynchronous handoff has an outbox and a place to fail* (`docs/adr/0033-outbox-and-dead-letters.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (40), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (38 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-091?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save AI policy, Save spend ceiling.
- [ ] Every transition is wired: `ADM-004`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `AI_CONFIGURE`, `AI_USE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-107` Guests & Marketing

**Everything in guests & marketing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Guests & Marketing · wave 1 · needs the `core` module |
| Block | Block A · ticket #28902 (VM-BO-107) |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW`, `REPORT_VIEW_VENUE`, `TENANT_VIEW` (1 configure, 2 read, 1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCampaigns` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more … |
| Route | `/guests-marketing` |

**What the spec says about it.** Section landing. **3 screens reach the entry point through here** — before 20 August they reached it through nothing.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The section landing for Guests & Marketing in the back office. It should route a CRM officer or marketer to the guest directory, segments, campaigns, journeys, communications, cases, VOC and loyalty, and show what needs attention. RBAC decides which tiles are visible: a role without Journeys does not see the tile at all.

**Known correction pending (do not draw the wrong version)**

- **The landing's navigation exits only to BO-068 Audit Log, BO-073 Lost & Found and BO-091 AI Policy & Spend.** Why: None of the CRM and marketing screens (BO-734 onwards, BO-754, BO-764, BO-774, BO-784, BO-804, BO-814, BO-824) is reachable from the section landing. *(source: screens/P08-venue-back-office.yaml#BO-107; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*
- **The "Create campaign" modal collects the whole CreateCampaignRequest in one form.** Why: Campaign creation is staged (BO-766); a single modal skips the consent and reach review. *(source: screens/P08-venue-back-office.yaml#BO-766; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Draft · Scheduled · Sending · Paused · Completed · Stopped · Failed | — | Sends `?status=` to `listCampaigns`. | `listCampaigns` ?status |
| Search guests & marketing | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | select | — | Core · Ticketing · Access · Fnb · Retail · Inventory · Seating · Membership · Marketing · Resources · Queue · Transport … | `getKpiValues` ?module |

**Form: Create campaign** (modal, opened by *Create campaign*; *Create campaign* calls `createCampaign`, *Cancel* sends nothing)

**Collects what `createCampaign` sends before it is called.** Required: `name`, `kind`, `channel`, `segmentId`, `content`. Optional: `venueId`, `trigger`, `scheduledFor`, `consentPurpose`, `sendWindow`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createCampaign` body |
| Kind `kind` | radio group | required | — | One off · Scheduled · Triggered · Recurring | — | — | `createCampaign` body |
| Channel `channel` | select | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `createCampaign` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCampaign` body |
| Segment `segmentId` | picker: choose a segment | required | — | — | shows names, sends the id | — | `createCampaign` body |
| Content `content` | group | required | — | — | — | — | `createCampaign` body |
| Template `content.templateId` | picker: choose a template | required | — | — | shows names, sends the id | — | `createCampaign` body |
| Subject override `content.subjectOverride` | key and value settings | optional | — | — | — | — | `createCampaign` body |
| Merge defaults `content.mergeDefaults` | key and value settings | optional | — | — | — | Fallback values for the template's `mergeFields`, by name, used where a guest has no value. | `createCampaign` body |
| Promotion `content.promotionId` | picker: choose a promotion | optional | — | — | shows names, sends the id | Offer carried by the campaign. Coupon codes are issued from it. | `createCampaign` body |
| Trigger `trigger` | group | optional | — | — | — | — | `createCampaign` body |
| Event `trigger.event` | select | optional | — | Booking confirmed · Visit completed · Membership expiring · Birthday · Abandoned cart · First visit · Inactivity · Entitlement expiring | — | `entitlementExpiring` (29 September, build pass, group G2; 5.5.30) fires on `entitlement.expiringSoon`: a ticket or pass the guest still holds comes within its template's … | `createCampaign` body |
| Delay hours `trigger.delayHours` | number field (hours) | optional | — | — | — | — | `createCampaign` body |
| Conditions `trigger.conditions` | repeatable rows | optional | — | — | — | — | `createCampaign` body |
| Attribute `trigger.conditions[].attribute` | text field | required | — | — | — | Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language. | `createCampaign` body |
| Operator `trigger.conditions[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Exists · Not exists · Within days | — | — | `createCampaign` body |
| Value `trigger.conditions[].value` | field | optional | — | — | — | — | `createCampaign` body |
| Values `trigger.conditions[].values` | list of values (chips) | optional | — | — | — | — | `createCampaign` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCampaign` body |
| Consent purpose `consentPurpose` | select | optional | Marketing | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | — | — | `createCampaign` body |
| Send window `sendWindow` | group | optional | — | — | — | Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen. | `createCampaign` body |
| Start time `sendWindow.startTime` | text field | optional | — | — | — | — | `createCampaign` body |
| End time `sendWindow.endTime` | text field | optional | — | — | — | — | `createCampaign` body |
| Time zone `sendWindow.timeZone` | text field | optional | — | — | — | — | `createCampaign` body |
| Send time mode `sendTimeMode` | segmented control | optional | Fixed | Fixed · Optimised | — | `optimised` sends each recipient at the hour `ai.requestSuggestion` (kind `sendTime`) gives for them, inside `sendWindow` (29 September, build pass, group G2; 22.3.19). | `createCampaign` body |
| Optimise channel `optimiseChannel` | toggle | optional | off | — | — | With `sendTimeMode` `optimised`, route each recipient to the channel the suggestion names, among the channels they consented to (22.9.16). | `createCampaign` body |
| Variants `variants` | repeatable rows | optional | — | at most 5 | — | A/B (or up to five-way) content and subject variants (29 September, build pass, group G2; 22.1.17, BO-772). | `createCampaign` body |
| Label `variants[].label` | text field | required | — | max length 20 | — | A, B, C... | `createCampaign` body |
| Subject override `variants[].subjectOverride` | key and value settings | optional | — | — | — | Subject line by locale. | `createCampaign` body |
| Template `variants[].templateId` | picker: choose a template | optional | — | — | shows names, sends the id | A different template for this variant; null uses the campaign's `content.templateId`. | `createCampaign` body |
| Split percent `variants[].splitPercent` | stepper or slider | optional | — | min 1; max 100 | — | Share of the test group; null splits evenly. | `createCampaign` body |
| Source `variants[].source` | segmented control | optional | Manual | Manual · AI draft | — | — | `createCampaign` body |
| AI decision record `variants[].aiDecisionRecordId` | text field | optional | — | — | — | The decision record of the `ai.proposeMarketingContent` draft it came from, for `aiDraft`. | `createCampaign` body |
| Ab test `abTest` | group | optional | — | Required when `variants` has two or more. | — | How the variants are tested. Required when `variants` has two or more. | `createCampaign` body |
| Test percent `abTest.testPercent` | stepper or slider | optional | 20 | min 5; max 100 | — | Share of the audience the variants are tested on; 100 splits everyone and picks no winner. | `createCampaign` body |
| Success metric `abTest.successMetric` | radio group | optional | Click rate | Open rate · Click rate · Conversion rate · Attributed revenue | — | — | `createCampaign` body |
| Decide after hours `abTest.decideAfterHours` | number field (hours) | optional | 4 | min 1; max 168 | — | — | `createCampaign` body |
| Winner rule `abTest.winnerRule` | segmented control | optional | Automatic | Automatic · Manual | — | — | `createCampaign` body |
| Minimum sample per variant `abTest.minimumSamplePerVariant` | number field | optional | 500 | min 1 | — | Below this many sends per variant no winner is declared automatically; a person picks. | `createCampaign` body |
| Winning variant `abTest.winningVariantId` | picker: choose a winning variant | optional | — | — | shows names, sends the id | Set by the automatic rule, or by a person through `updateCampaign`. | `createCampaign` body |

Errors to draw in the form: 400 Validation failed

#### Outputs: what the screen shows and produces

**Shown**

**Every campaign** (data table, from `listCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: One off, Scheduled, Triggered, Recurring | — |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Consent purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |

**Takings and admissions today** (metric tile, from `getKpiValues`): **Takings and admissions**, from `getKpiValues?kpiCodes=takings,admissions`; with no `period` the period is today in the venue's time zone (decided 28 September, audit R283).

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Period | text | — |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Card list** (card list): 3 screens. **No attention counts** until a summary operation exists to supply them (decided 28 September, audit R283).

**The selected campaign** (detail panel, from `listCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: One off, Scheduled, Triggered, Recurring | — |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Content | grouped details | — |
| Trigger | grouped details | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Consent purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |
| Status | chip: Draft, Scheduled, Sending, Paused, Completed, Stopped… | — |

**The venue settings** (detail panel, from `getVenueSettings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | From the path of `setVenueSettings`. |
| Currency code | text | `readOnly` is the freeze. `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the … |
| Currency scale | 1,234 | Scale travels with currency (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency … |
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| Biometrics | grouped details | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. |
| Segregated access | grouped details | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a … |
| Alerting | grouped details | CF-134. On-platform notification, marked as read. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create campaign (primary button) | `createCampaign` POST `/campaigns` | CreateCampaignRequest | Campaign | 400 Validation failed | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Tiles**: One per sub-area the role can see (hidden areas disappear; view-only areas open read-only). Counts appear only when a summary operation supplies them. *(source: DI-387; R283)*
- **Campaigns**: Recent campaigns with status and sent count; a status filter. *(source: contracts/satellite/marketing-crm.yaml#listCampaigns)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Create campaign**: Opens the Campaign Builder (BO-766) rather than a one-shot modal, because a campaign needs audience, offer, consent and schedule stages. *(source: screens/P08-venue-back-office.yaml#BO-766)*

**Data it reads**: `getKpiValues` (onLoad, Today's takings and admissions tiles — …); `getVenueSettings` (onLoad, What is enabled here); `listCampaigns` (onLoad, Campaigns and their reach)

**Where the user goes next**

- → `BO-073` Lost & Found Register: *Lost & Found Register*
- → `BO-091` AI Policy & Spend: *AI Policy & Spend*
- → `BO-755` Dynamic Segment Builder: *Opens Dynamic Segment Builder*; carries `segmentId`
- → `BO-766` Campaign Builder: *Opens Campaign Builder*; carries `campaignId`
- → `BO-772` A/B & AI Optimization: *Opens A/B & AI Optimization*; carries `campaignId`
- → `BO-785` Template Library: *Opens Template Library*; carries `templateId`
- → `BO-798` Intent & Knowledge Management: *Opens Intent & Knowledge Management*
- → `BO-799` Agent Workspace: *Opens Agent Workspace*
- → `BO-825` Challenge Builder: *Opens Challenge Builder*
- → `BO-826` Achievement & Badge Engine: *Opens Achievement & Badge Engine*
- → `BO-827` Points & Activity Rules: *Opens Points & Activity Rules*
- → `BO-828` Milestones & Reward Rules: *Opens Milestones & Reward Rules*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list, with counts. |
| Error (`?state=error`) | Could not load. Venue Home is still reachable. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing configured in guests & marketing yet.** The action is the first thing to set up, not a blank list. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter. |
| Permission denied (`?state=emptyNoAccess`) | You do not have permission for guests & marketing. **Said plainly** — an empty section reads as broken. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `BO-734`: The CRM command centre is the CRM half of this landing; avoid two landings with different counts.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
- Guests 48,210
- Segments 37
- Campaigns 4 live
- Journeys 6 active
- Open cases 23
- Reviews to moderate 9
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `listCampaigns` → `MARKETING_VIEW` (read) · staff
- `createCampaign` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** You do not have permission for guests & marketing. **Said plainly** — an empty section reads as broken.

#### Requirements it meets

25 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.1.1 | Campaign Creation | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.4 | Campaign Scheduling | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.12 | Ticketing Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.13 | Membership Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.14 | Loyalty Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.4.8 | Product & Event Integration | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.9.14 | Marketing Notifications | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.8 | Campaign Budget Management | Marketing & CRM | CONTRACTED | data `Campaign` |
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| 3.2.46 | Face Pass shouldt restrict male guests attempting to enter during Friday Ladies Night, which needs to be validated with rule-based facial recognition validation. | Admission and Access | CONTRACTED | data `VenueSettings` |
| 8.9.3 | System shall display queue lengths, estimated wait times, queue utilization, queue alerts, and queue prediction metrics. | Unified Operations Dashboard | CONTRACTED | data `VenueSettings` |
| 11.1.15 | Approval Breach Alerts - System shall notify users when approval SLA thresholds are exceeded. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| … 13 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-107` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (42), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-107?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create campaign.
- [ ] Every transition is wired: `BO-073`, `BO-091`, `BO-755`, `BO-766`, `BO-772`, `BO-785`, `BO-798`, `BO-799`, `BO-825`, `BO-826`, `BO-827`, `BO-828`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`, `REPORT_VIEW_VENUE`, `TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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
"configureAssistantProfile": {"method":"PUT","path":"/assistant-profiles/{profileKey}","contract":"ai","summary":"Define an assistant profile","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiAssistantProfile","responds":"AiAssistantProfile"},
"createCampaign": {"method":"POST","path":"/campaigns","contract":"marketing-crm","summary":"Create a campaign","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCampaignRequest","responds":"Campaign"},
"getAiByokEnablement": {"method":"GET","path":"/tenants/{tenantId}/byok","contract":"ai","summary":"Whether a tenant may bring its own key","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AiByokEnablement"},
"getAiPolicy": {"method":"GET","path":"/policy","contract":"ai","summary":"What the assistant may do here","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopePath","in":"query","required":false}],"requestBody":null,"responds":"AiPolicy"},
"getAiSpendCeiling": {"method":"GET","path":"/policy/spend-ceiling","contract":"ai","summary":"The AI spend ceiling, in money","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiSpendCeiling"},
"getAiUsage": {"method":"GET","path":"/usage","contract":"ai","summary":"Usage, cost and performance","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"AiUsageReport"},
"getEffectiveAiPolicy": {"method":"GET","path":"/governance/effective-policy","contract":"ai","summary":"The policy in force for a capability at a scope","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"capabilityKey","in":"query","required":true},{"name":"scopePath","in":"query","required":null},{"name":"environment","in":"query","required":null}],"requestBody":null,"responds":"AiEffectivePolicy"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getLostItemMatches": {"method":"GET","path":"/lost-items/{itemId}/matches","contract":"marketing-crm","summary":"Candidate matches, scored","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"LostItemMatch"},
"getVenueSettings": {"method":"GET","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Operational settings for this venue","permission":"TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"listAiCapabilities": {"method":"GET","path":"/governance/capabilities","contract":"ai","summary":"The capability registry","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"family","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"riskClass","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAssistantProfiles": {"method":"GET","path":"/assistant-profiles","contract":"ai","summary":"Assistant profiles","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"audience","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAuditRecords": {"method":"GET","path":"/audit-records","contract":"tenancy","summary":"Who did what, where, and when","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"orgUnitId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"action","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"platformStaffGrantId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCampaigns": {"method":"GET","path":"/campaigns","contract":"marketing-crm","summary":"List campaigns","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listIndexFailures": {"method":"GET","path":"/index-failures","contract":"ai","summary":"Records an index could not embed","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"jobId","in":"query","required":null},{"name":"stage","in":"query","required":null}],"requestBody":null,"responds":"IndexFailure"},
"listLostItems": {"method":"GET","path":"/lost-items","contract":"marketing-crm","summary":"Reported and found items","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrgUnits": {"method":"GET","path":"/org-units","contract":"tenancy","summary":"List scope nodes visible to the session","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"under","in":"query","required":null},{"name":"level","in":"query","required":null},{"name":"includeInactive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants","contract":"identity","summary":"Which platform staff have acted in this tenant, and under what grant","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkstations": {"method":"GET","path":"/workstations","contract":"tenancy","summary":"List workstations","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"saleBoardKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"matchLostItem": {"method":"POST","path":"/lost-items/{itemId}/match","contract":"marketing-crm","summary":"Tie a report to a found item, or hand it back","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LostItem"},
"recordLostItem": {"method":"POST","path":"/lost-items","contract":"marketing-crm","summary":"Report something lost, or hand something in","permission":"CASE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LostItem","responds":"LostItem"},
"setAiPolicy": {"method":"PUT","path":"/policy","contract":"ai","summary":"Set the policy","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiPolicy","responds":"AiPolicy"},
"setAiSpendCeiling": {"method":"PUT","path":"/policy/spend-ceiling","contract":"ai","summary":"Set the AI spend ceiling, in money","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiSpendCeiling","responds":"AiSpendCeiling"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAssistantProfile": {"type":"object","x-ticvai-persistence":"ai.assistant_profile","description":"**One assistant runtime, many profiles** (design 5.10, C5; AIC-069..080). The profile decides the audience, roles, knowledge sources, tools, model task and guest scope: guest concierge, support chatbot and staff assistants by role.","required":["profileKey","audience"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"profileKey":{"type":"string"},"name":{"type":"string"},"audience":{"type":"string","enum":["staff","guest","support"]},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"module":{"allOf":[{"$ref":"#/components/schemas/common::ModuleKey"}],"nullable":true},"collectionIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Knowledge collections it retrieves from."},"toolKeys":{"type":"array","items":{"type":"string"},"description":"Registered tools it may propose (an assistant only reads; a change request goes to the configuration assistant, AIC-078)."},"modelTask":{"type":"string","description":"The gateway task, e.g. `assistant.staff.answer`. The visit planner agent (29 September, MOB-6) is profile `planner.guest` with task `planner.guest.refine` and the five `venue-map` visit-plan tools. The app publishing guide (M24-08) is profile `guide.appPublishing` with task `assistant.staff.answer`, grounded on the platform's store-publishing collection only."},"guestCapabilityScope":{"type":"array","items":{"type":"string"},"description":"For a guest profile: the same values as `AiPolicy.guestCapabilityScope`, narrowed."},"locales":{"type":"array","items":{"type":"string"}},"handoverTarget":{"type":"string","nullable":true,"description":"Where \"ask a person\" goes: a support queue or a staff role."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiAutonomyLevel": {"type":"integer","minimum":0,"maximum":4,"description":"**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."},
"AiByokEnablement": {"type":"object","x-ticvai-persistence":"ai.byok_enablement","description":"**Whether a tenant may bring its own model key** (decided 29 September, design 8 on 5.9). TICVAI decides it per tenant with `PLATFORM_AI_MANAGE`; it is not tenant self-service. Until it is enabled, `setAiProvider` refuses `managedBy: tenant`. One row per tenant.","required":["tenantId","enabled"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"tenantId":{"type":"string","format":"uuid"},"enabled":{"type":"boolean"},"coverage":{"type":"string","enum":["perTask","allTasks"],"default":"perTask","description":"Whether the tenant may supply a key per task or one key for everything."},"allowedTasks":{"type":"array","items":{"type":"string"},"description":"Where `coverage` is `perTask`: the gateway tasks a tenant key may serve. Empty means any."},"taskModelMap":{"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","type":"array","readOnly":true,"description":"**The provider's equivalent model for each task, chosen by TICVAI** (Chinmay, 2 October, workbook Q1; closes AI-D20; CHG-CSA-001). For each task the tenant key serves, the model of the tenant's provider at the tier the task needs, taken from TICVAI's curated range (`AiModel.curatedRange`). The tenant does not choose it; a task with no curated equivalent at the tenant's provider stays on the TICVAI-managed model and is listed with `modelId` null.","items":{"type":"object","properties":{"taskKey":{"type":"string"},"tier":{"type":"string"},"modelId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.model"},"compatibilityPassed":{"type":"boolean","nullable":true,"description":"Whether the provider's compatibility test passed for this task (`AiProviderCompatibility`, CHG-FUP-008); a task that has not passed stays on the TICVAI-managed model."}}}},"reason":{"type":"string","maxLength":1000},"platformStaffGrantId":{"type":"string","format":"uuid","readOnly":true,"description":"The open platform-staff grant the change was made under (audit R098)."},"decidedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"decidedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiCapabilityFamily": {"type":"string","enum":["gatewayAndModels","governance","actionPipeline","knowledgeRetrieval","assistants","analyticsInsights","configurationAssistant","forecasting","anomalyDetection","riskIntelligence","recommendations","decisionRecords","operationsEvaluation","residencyPrivacy"],"description":"The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point, action pipeline and human oversight, knowledge and retrieval, assistants, analytics assistant and insights, configuration assistant, forecasting and operational requirements, anomaly detection, fraud and risk intelligence, recommendation and upsell engine, decision records and audit, operations/evaluation/cost, residency/privacy/tenancy. **Every registered capability belongs to exactly one**, which is what `AiPolicy.enabledCapabilities` and the usage report group by."},
"AiCapabilityRegistration": {"type":"object","x-ticvai-persistence":"ai.capability","description":"**An entry in the capability registry** (design 3.1 Registry, AIC-144, AIC-145; ADM-520). Nothing becomes an operational AI capability without a row here: owner, function, risk class, autonomy, data categories and lifecycle per environment. `autonomyCeiling` is the platform ceiling for the tenant; a tenant or venue may lower `autonomyLevel`, never raise it (AIC-151).","required":["capabilityKey","family","riskClass","autonomyLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string","description":"Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`."},"family":{"$ref":"#/components/schemas/AiCapabilityFamily"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal","description":"The accountable business owner (AIC-144)."},"businessFunction":{"type":"string","nullable":true},"riskClass":{"$ref":"#/components/schemas/AiRiskClass"},"autonomyCeiling":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"readOnly":true,"description":"The first-release ceiling for this capability (design 3.8 table). Read-only to a tenant."},"autonomyLevel":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"description":"The level in force at this scope. At most `autonomyCeiling`."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories the capability reads (ADM-524)."},"lifecycle":{"type":"object","description":"Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.","properties":{"development":{"type":"string","enum":["draft","pilot","active","retired"]},"staging":{"type":"string","enum":["draft","pilot","active","retired"]},"production":{"type":"string","enum":["draft","pilot","active","retired"]}}},"degradationMode":{"type":"string","enum":["rulesOnly","searchOnly","humanHandoff","hidden","failOpen","lastPublished"],"description":"What the capability does when its model or the service is unavailable (design 3.7, AIC-241)."},"status":{"type":"string","enum":["active","paused"],"readOnly":true,"description":"Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed."},"pausedReason":{"type":"string","nullable":true,"readOnly":true},"pausedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiEffectivePolicy": {"type":"object","x-ticvai-persistence":"none — resolved from published policy versions, exceptions and ai.policy","description":"**The policy in force for a capability at a scope** (AIC-153, AIC-165; ADM-525, ADM-528): the intersection of the capability, governance policy and the tenant or venue AI policy, with where each part came from.","required":["capabilityKey","autonomyLevel","rules"],"properties":{"capabilityKey":{"type":"string"},"scopePath":{"type":"string"},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"autonomyCeiling":{"$ref":"#/components/schemas/AiAutonomyLevel"},"rules":{"type":"array","items":{"type":"object","properties":{"rule":{"$ref":"#/components/schemas/AiGovernanceRule"},"policyKey":{"type":"string"},"version":{"type":"integer"},"scopePath":{"type":"string"}}}},"exceptions":{"type":"array","items":{"$ref":"#/components/schemas/AiPolicyException"}},"conflicts":{"type":"array","items":{"type":"object","properties":{"description":{"type":"string"},"resolvedTo":{"$ref":"#/components/schemas/AiGovernanceOutcome"}}},"description":"Conflicting rules and the more restrictive result they resolved to (AIC-161)."},"resolvedAt":{"type":"string","format":"date-time"}}},
"AiGovernanceOutcome": {"type":"string","enum":["allow","allowWithConditions","prepareOnly","approvalRequired","escalate","block"],"description":"What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). `block` is an answer, not an error, and is logged as outcome `refused`."},
"AiGovernanceRule": {"type":"object","x-ticvai-persistence":"none — held in the jsonb rules column of ai.governance_policy_version, through AiGovernanceRuleList","description":"One rule of a governance policy version: which actions on which data, under which conditions, get which outcome (AIC-147..160).","required":["effect"],"properties":{"effect":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"capabilityKeys":{"type":"array","items":{"type":"string"},"description":"Registered capabilities it applies to. Empty means every capability the policy names."},"actions":{"type":"array","items":{"type":"string","enum":["read","analyze","recommend","generate","prepare","create","modify","publish","execute","delete"]},"description":"ADM-523: what AI may do, from reading to executing."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories (ADM-524), e.g. `customerContact`, `payment`, `financial`, `operational`."},"purposes":{"type":"array","items":{"type":"string"},"description":"Permitted purposes for those categories (AIC-156, AIR-182)."},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Above this value the effect escalates one step (for example to `approvalRequired`)."},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Roles the rule applies to; empty means every role."},"environments":{"type":"array","items":{"type":"string","enum":["development","sandbox","staging","production"]},"description":"ADM-525. Empty means every environment. **`sandbox`** (18 September minutes, M18-01): the developer sandbox and a tenant's trial environment, governed apart from staging so a rule can allow in sandbox what it blocks in production."},"conditions":{"type":"object","additionalProperties":true,"nullable":true,"description":"Conditions attached to an `allowWithConditions` effect, for example `maskFields` or `requireCitation`."}}},
"AiPolicy": {"type":"object","x-ticvai-persistence":"ai.policy","required":["scopeLevel","scopePath","enabledCapabilities"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"scopeLevel":{"type":"string","enum":["tenant","venue"],"description":"Tenant sets the default; a venue may narrow it and never widen it."},"scopePath":{"type":"string","description":"**The node this row belongs to, and the key it is written under** — the tenant's node where `scopeLevel` is `tenant`, a venue's where it is `venue`. One row per `scopePath`; `setAiPolicy` writes the row it names and `getAiPolicy` resolves nearest ancestor first (ADR-0018).\n"},"enabledCapabilities":{"type":"array","description":"**Extended on 29 September to the fourteen capabilities of the AI design** (section 1.1, `AiCapabilityFamily`). The six earlier values stay: they are finer switches inside `assistants`, `knowledgeRetrieval` and `configurationAssistant`, and a tenant that set them keeps them. `governance`, `decisionRecords` and `residencyPrivacy` cannot be switched off; listing them is accepted and changes nothing.\n","items":{"type":"string","enum":["assist","search","generateConfiguration","generateLayout","summarise","explain","gatewayAndModels","governance","actionPipeline","knowledgeRetrieval","assistants","analyticsInsights","configurationAssistant","forecasting","anomalyDetection","riskIntelligence","recommendations","decisionRecords","operationsEvaluation","residencyPrivacy"]}},"allowedRoleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"maskedFields":{"type":"array","description":"Redacted before a prompt leaves the platform (8.3.73). **Defaults to every field in the pii schema** — a masking list nobody filled in should send nothing rather than everything.\nEach entry is a column named `schema.table.column`, as the DDL names it — `pii.subject_contact.email`. **Omitted, null and an empty array all take the default**, because each of them is a list nobody filled in. An entry naming no column is refused at save rather than silently masking nothing.\n**Column masking is in addition to the gateway scrubber, never instead of it** (CHG-CSA-003): free text a guest types is not a column, so every prompt also passes the offline scrubber (`scrubbing`).\n","items":{"type":"string","pattern":"^[a-z][a-z0-9_]*\\.[a-z][a-z0-9_]*\\.[a-z][a-z0-9_]*$"}},"requiresApprovalFor":{"type":"array","description":"8.3.61–8.3.64. Nothing in this list executes without a decision.","items":{"type":"string","enum":["pricing","promotion","operational","financial","configuration"]}},"scrubbing":{"type":"object","readOnly":true,"description":"**Mandatory offline PII scrubbing and moderation on every LLM call** (Chinmay, 2 October: \"we may need to scrub personal info no matter what\"; ADR-0020 amended; CHG-CSA-003). Not a setting: it applies whatever the tenant's residency class, and a tenant cannot switch it off. Before a prompt leaves the cell the gateway runs Microsoft Presidio (offline) with UAE recognisers (Emirates ID, UAE phone, passport, IBAN, Luhn-checked card, email) and an Arabic NER model; each value found becomes a reversible placeholder (`[GUEST_1]`) whose map never leaves the cell, and the reply is re-filled before it reaches the user. An input and output guard checks both directions: **the provider's content-safety service, not a model we host** (Chinmay, 3 October: we host no LLM unless a client asks, and a guard model is an LLM; CHG-R1S-002): Azure AI Content Safety in UAE North for `uaeOnly`, the provider's own moderation for BYOK and `globalAllowed`. Presidio and the Arabic NER run on the AI GPU node pool in our own cell, beside the embedding model (Chinmay, 4 October, CHG-R11-001), and scrubbing is mandatory in every residency class. **Fails closed**: with the scrubber, its GPU node or the safety service down, the call is refused (`503 scrubber-unavailable`), never sent raw. This object reports what is in force.\n\n**A second, deterministic pass after Presidio** (3 October 2026, CHG-R1S-016; the legal research `docs/active/research/openai-key-uae-3-october.md`, item 5: Presidio itself says it will not find everything). Fixed patterns run over the scrubbed text: Emirates ID (`784-...`), `+971` numbers, Luhn-valid card numbers (PAN), IBAN and email. **Any survivor blocks the call**, fail closed, `503 scrubber-unavailable` with no provider fallback, never sent. The Presidio version is pinned (`scrubberVersion`): it is community-maintained now, so a release is taken on purpose, after the golden corpus passes.\n","properties":{"mode":{"type":"string","enum":["mandatory"]},"scrubberVersion":{"type":"string","readOnly":true,"description":"The pinned Presidio release (and recogniser set) in force, e.g. `presidio-2.2.355+uae-1` (CHG-R1S-016). Recorded on every call's activity row."},"residualPatternCheck":{"type":"array","readOnly":true,"items":{"type":"string","enum":["emiratesId","uaePhone","cardPan","iban","email"]},"description":"The deterministic patterns run after Presidio; a match blocks the call (fail closed, `503 scrubber-unavailable`). Always all five (CHG-R1S-016)."},"recognisers":{"type":"array","items":{"type":"string"},"description":"The recogniser set in force, e.g. `emiratesId`, `uaePhone`, `passport`, `iban`, `card`, `email`, `arabicPersonName`."},"reversibleTokens":{"type":"boolean","description":"Always true; the placeholder map stays in the cell."},"guardModel":{"type":"string","description":"The input and output guard in force, e.g. `azureContentSafety` (the provider''s content-safety service, CHG-R1S-002); a self-hosted guard model appears only where a client asked for self-hosting."}}},"globalEndpointExclusions":{"type":"object","readOnly":true,"description":"**What never goes to a global endpoint** (3 October 2026, CHG-R1S-016; the legal research `docs/active/research/openai-key-uae-3-october.md`, item 6). A field-level exclusion list applied by the prompt builders when the resolved endpoint is outside the UAE (`globalAllowed`): the fields are dropped from the prompt, not masked, and the media kinds are refused. Not a setting: it applies to every tenant.","properties":{"fieldCategories":{"type":"array","items":{"type":"string","enum":["allergy","accessibility","familyAndChildren","health","biometric","religion","payment"]},"description":"Allergy, accessibility and family or children data in F&B and booking prompts, and health, biometric, religion and payment data anywhere."},"fields":{"type":"array","items":{"type":"string"},"description":"The schema fields held under those categories, e.g. `Allergen.contains`, `Attendee.accessibilityNeeds`, `Attendee.dateOfBirth`."},"blockedMedia":{"type":"array","items":{"type":"string","enum":["image","audio","file"]},"description":"Images, audio and files are never sent to a global endpoint."}}},"monthlyTokenCeiling":{"type":"integer","nullable":true},"ceilingBehaviour":{"type":"string","enum":["warn","warnThenDisable","block"],"default":"warn","description":"**Decided 17 August: warn, and let the venue manager choose.** A cap that stops the assistant mid-visit turns a cost control into a guest-facing outage, and the venue has no warning it is about to happen.\nAt the ceiling a notification reaches the venue manager with the spend and the remaining period, and **the assistant keeps answering until somebody decides otherwise**. `warnThenDisable` and `block` exist for a tenant who asks for a hard limit; neither is the default.\n**Now the default for capabilities without their own entry** in `ceilingBehaviourByCapability` (AI design 5.9).\n"},"ceilingBehaviourByCapability":{"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**Ceiling behaviour per capability** (AI design 5.9, AIC-227), so a budget never silently disables fraud scoring, which spends no tokens, or a critical capability. A capability not listed takes `ceilingBehaviour`. The guest concierge defaults to `warn` (decided 17 August).\n","items":{"type":"object","required":["capability","behaviour"],"properties":{"capability":{"type":"string","description":"An `AiCapabilityFamily` value, or a registered capability key."},"behaviour":{"type":"string","enum":["warn","warnThenDisable","block","neverRestrict"]}}}},"autonomyOverrides":{"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**Tighten only** (AI design 3.8, AIC-151). A level per capability at or below the capability's ceiling, and on a venue row at or below the tenant row's. Autonomy is separate from user permission (AIC-154).\n","items":{"type":"object","required":["capabilityKey","autonomyLevel"],"properties":{"capabilityKey":{"type":"string"},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"}}}},"ceilingWarningPercent":{"type":"integer","default":80,"description":"**Warn before the ceiling, not at it.** A manager told at 100% has already spent it; one told at 80% can decide with a week left.\n"},"guestCapabilityScope":{"type":"array","description":"**What a guest-facing assistant may help with, and nothing else** (2.1.28). Bounding the capability is what makes the cost predictable and the safety posture tractable — an assistant that answers anything is one that can be asked anything.\n","items":{"type":"string","enum":["ticketSelection","promotions","faq","recommendations","checkout","waitTimes","wayfinding","visitPlanning"]}},"retrieveTopK":{"type":"integer","default":30,"description":"How many chunks retrieval returns before reranking."},"rerankTopK":{"type":"integer","nullable":true,"default":5,"description":"How many survive the rerank and reach the model. **Reranking reduces cost as well as improving quality**, which is unusual — retrieval is cheap and the tokens sent to the model are not.\nNull disables reranking, and a venue with no rerank provider configured runs without it rather than failing.\n"},"cacheAnswers":{"type":"boolean","default":true,"description":"**The largest cost lever available at a kiosk.** Guest questions are extraordinarily repetitive — forty questions, thousands of times a day — where staff questions are diverse.\n**Invalidation runs on the same events that invalidate the index.** A cached answer that outlives a price change has misled a guest on the venue's behalf, which is worse than a slow one.\n"},"cacheTtlMinutes":{"type":"integer","default":60,"description":"An upper bound on top of event invalidation, not instead of it. **The key carries `scope_path`** — a cache keyed on the question alone is a cross-venue leak wearing a performance hat.\n"},"retainInteractionsDays":{"type":"integer","deprecated":true,"description":"How long prompts and responses are kept. **Deprecated 29 September (decision 5):** AI data retention is one tenant configuration with a period per data class, 90 days by default, kept with the tenant's other data-retention settings in `tenancy`, not here. Read for one release and ignored once the tenant setting exists.\n"},"semanticCacheThreshold":{"type":"number","minimum":0,"maximum":1,"default":0.95,"description":"**Similarity above which a cached answer serves a new question.** `cache:answer` is exact-match on question, scope and locale — *what time do you close* and *when do you shut* are two misses and two provider calls.\n\n**Per capability, not global.** A factual venue question tolerates 0.95; a recommendation tolerates nothing. **A tenant who finds it wrong can move it**, which is why it is policy rather than a constant."},"negativeCacheTtlSeconds":{"type":"integer","default":300,"description":"**How long *no answer found* is remembered.** A miss costs a full retrieval and a completion.\n\n**Shorter than a hit deliberately** — the answer may exist tomorrow because somebody indexed it."},"cascade":{"type":"object","nullable":true,"description":"**A small model answers and escalates only below a confidence threshold.** `ai.suggestion.confidence` exists and nothing routes on it.","properties":{"smallModel":{"type":"string"},"largeModel":{"type":"string"},"escalateBelow":{"type":"number","default":0.7}}},"chunking":{"type":"object","description":"**The single biggest lever on retrieval quality**, and currently nowhere. **A venue FAQ and a maintenance manual do not chunk the same way.** Per collection, not global.","properties":{"sizeTokens":{"type":"integer","default":512},"overlapTokens":{"type":"integer","default":64},"strategy":{"type":"string","enum":["fixed","sentence","semantic"],"default":"sentence"}}},"quantisation":{"type":"string","enum":["none","scalar","binary"],"default":"none","description":"**A decision, never a default.** `scalar` int8 is roughly four times smaller — 49 GB becomes 12 — **and it costs recall**. `binary` is smaller again and needs rescoring against full vectors to be usable.\n\n**A creation decision**: changing it means a rebuild, which is what `shadow_collection` is for. **A tenant whose search quality drops after an infrastructure change should be able to find the line that did it.**"},"hnsw":{"type":"object","nullable":true,"description":"**Defaults are tuned for neither our recall nor our latency.** A collection built with the wrong ones needs a rebuild, which is why this is a creation decision like the sparse index.","properties":{"m":{"type":"integer","default":16},"efConstruct":{"type":"integer","default":128},"efSearch":{"type":"integer","default":64}}},"perRequestTokenCeiling":{"type":"integer","nullable":true,"description":"**One runaway conversation can spend a tenant's month.** `monthlyTokenCeiling` discovers that after it has happened."},"streamsByCapability":{"type":"array","items":{"type":"string"},"description":"**Time to first token and total latency are separate targets.** A concierge that starts answering in 300 ms and finishes in 4 seconds is better than one silent for 2.\n\n**`chat` streams; `generateConfiguration` does not** — nobody watches a config draft assemble."},"fallbackProviderId":{"type":"string","format":"uuid","nullable":true,"description":"BL-151: **a provider outage with no fallback is every AI surface going dark at once.**\n\n**`residencyRefused` is never failed over.** It is a correct answer, and moving the call elsewhere would defeat the refusal."},"guardrailShortCircuit":{"type":"boolean","default":true,"description":"**A refusal a rule can decide never reaches a model.** Cheaper, faster and more consistent than asking a model to refuse."},"suggestionProviders":{"allOf":[{"$ref":"#/components/schemas/SuggestionProviderAssignments"}],"readOnly":true,"description":"**Which producer answers each `SuggestionKind`**, and what `requestSuggestion` routes by. Written only by `setSuggestionProvider`; `setAiPolicy` leaves it as it was. Held on the tenant row — a venue row does not carry its own.\n"}}},
"AiPolicyException": {"type":"object","x-ticvai-persistence":"ai.policy_exception","description":"**A temporary, recorded exception to a governance policy** (AIC-162, ADM-526): an expiry, an approver and compensating controls. Governance is never bypassed silently.","required":["policyId","reason","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"policyId":{"type":"string","format":"uuid","x-ticvai-references":"ai.governance_policy"},"capabilityKey":{"type":"string","nullable":true},"reason":{"type":"string","maxLength":2000},"compensatingControls":{"type":"array","items":{"type":"string"}},"startsAt":{"type":"string","format":"date-time","nullable":true},"expiresAt":{"type":"string","format":"date-time","description":"Required. An exception with no end is a policy change, and goes through publication."},"status":{"type":"string","enum":["active","expired","revoked"],"readOnly":true},"approvedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"revokedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"revokedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"revokeReason":{"type":"string","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRiskClass": {"type":"string","enum":["low","medium","high","critical"],"description":"Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). The governance decision point scores against it."},
"AiSpendCeiling": {"type":"object","x-ticvai-persistence":"ai.spend_ceiling","description":"**The AI spend ceiling in money** (Chinmay, 2 October, workbook Q8; CHG-CSA-004). One row per `scopePath`, as `AiPolicy`: the tenant's default and a venue's narrowing.","required":["spend"],"properties":{"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005); the tenant's node or a venue's."},"spend":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Per month, in the tenant's selected currency; until the tenant changes it, the tenant's billing currency (AED for a UAE tenant), not USD (CHG-RUL-017)."},"tokenEquivalent":{"type":"integer","readOnly":true,"nullable":true,"description":"What `spend` buys at the current blended rate, shown beside it on BO-091."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AiUsageReport": {"type":"object","x-ticvai-persistence":"none — aggregated from ai.activity","properties":{"currency":{"type":"string","minLength":3,"maxLength":3,"readOnly":true,"description":"**The tenant's selected currency, by default its billing currency (AED for a UAE tenant), not USD** (CHG-RUL-017; Chinmay, 2 October, workbook Q8; CHG-CSA-004). Every `cost` here is in it; token counts sit beside each cost."},"ceiling":{"type":"object","nullable":true,"readOnly":true,"description":"The spend ceiling in force (`getAiSpendCeiling`), with the tokens it equals at the current blended rate and what is used so far (CHG-CSA-004).","properties":{"spend":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tokens":{"type":"integer","nullable":true},"usedSpend":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"usedTokens":{"type":"integer"}}},"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"groupBy":{"type":"string"},"rows":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"interactions":{"type":"integer"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"p95LatencyMs":{"type":"integer"},"refusalRate":{"type":"number"},"rejectionRate":{"type":"number","description":"Proposals a person refused. **The number that says whether the assistant is worth having**, and the one nobody thinks to measure.\n"}}}},"forecast":{"type":"object","nullable":true,"description":"**A month-end projection, labelled a forecast** (AI design 2.3, 4.5). Present where `to` is inside the current month. Never added into `rows`.\n","properties":{"label":{"type":"string","enum":["forecast"]},"periodEnd":{"type":"string","format":"date"},"projectedTokens":{"type":"integer"},"projectedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"basis":{"type":"string","description":"How it was projected, e.g. the run rate of the last 7 days."}}}}},
"AuditRecord": {"x-ticvai-append-only":"occurredAt","type":"object","x-ticvai-persistence":"platform.audit_record","description":"26 September, pull audit R198. **One row of the platform audit trail, as `listAuditRecords` returns it.** It was a free-form object, so nothing said what an audit row carries. These are the fields the operation already filters on — who, where, on which workstation, what action, on what, and when — and nothing more. Written by the operations that audit themselves; never edited and never deleted.\n","required":["id","action","occurredAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid","description":"Who acted."},"orgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The scope node the action happened in."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation it was done from, where there was one."},"action":{"type":"string","description":"What was done, as the writing operation names it."},"subjectRef":{"type":"string","nullable":true,"description":"**The thing acted on** — a profile, a shift, an order. The same value the `subjectRef` filter matches.\n"},"occurredAt":{"type":"string","format":"date-time","description":"When. The list is ordered by this, most recent first."},"platformStaffGrantId":{"type":"string","format":"uuid","nullable":true,"description":"**Set when a TICVAI platform operator acted, naming the grant they acted under** (`identity.openPlatformStaffGrant`; decided 28 September, audit R098). Null for the tenant's own staff. Every platform action in a tenant carries one, so the tenant can see all of them.\n"}}},
"Campaign": {"x-ticvai-persistence":"marketing.campaign","allOf":[{"$ref":"#/components/schemas/CreateCampaignRequest"},{"type":"object","required":["id","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"budgetCap":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"budgetSpent":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"BL-169. **A campaign could spend without limit** — following the promotions `budgetCap` precedent. **Sending stops at the cap rather than overspending and reporting it**, because a marketing budget discovered after it was exceeded is a budget nobody set.\n"},"status":{"$ref":"#/components/schemas/CampaignStatus"},"isPaused":{"type":"boolean"},"createdByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"launchedAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true},"sentCount":{"type":"integer","readOnly":true,"x-ticvai-persisted":false,"description":"**How many messages went out**, counted from `marketing.message_dispatch` at read time rather than kept as a counter on the campaign row, so it cannot drift from the dispatch records it summarises. Test sends are not dispatches of the campaign and are not counted.\n"}}}]},
"CampaignContent": {"x-ticvai-persistence":"none — embedded in campaign","type":"object","required":["templateId"],"properties":{"templateId":{"type":"string","format":"uuid"},"subjectOverride":{"type":"object","additionalProperties":{"type":"string"}},"mergeDefaults":{"type":"object","description":"Fallback values for the template's `mergeFields`, by name, used where a guest has no value.","additionalProperties":{"type":"string"}},"promotionId":{"type":"string","format":"uuid","nullable":true,"description":"Offer carried by the campaign. Coupon codes are issued from it."}}},
"CampaignKind": {"type":"string","enum":["oneOff","scheduled","triggered","recurring"]},
"CampaignStatus": {"type":"string","enum":["draft","scheduled","sending","paused","completed","stopped","failed"]},
"CampaignTrigger": {"x-ticvai-persistence":"none — embedded in campaign","type":"object","properties":{"event":{"type":"string","enum":["bookingConfirmed","visitCompleted","membershipExpiring","birthday","abandonedCart","firstVisit","inactivity","entitlementExpiring"],"description":"`entitlementExpiring` (29 September, build pass, group G2; 5.5.30) fires on `entitlement.expiringSoon`: a ticket or pass the guest still holds comes within its template's `expiryNoticeDays` of `validTo`. The notice period is set on the template, so `delayHours` shifts the send within it rather than setting it. An entitlement belonging to a membership is left to `membershipExpiring`, so a member is not told twice."},"delayHours":{"type":"integer"},"conditions":{"type":"array","items":{"$ref":"#/components/schemas/SegmentCriterion"}}}},
"CatalogueState": {"x-ticvai-persistence":"none — computed from workstation bundle_version","type":"object","description":"The workstation's local catalogue position. A terminal beyond `staleAfter` must refuse to trade rather than transact against stale prices.\n","required":["appliedBundleVersion","appliedAt","staleAfter","isStale"],"properties":{"appliedBundleVersion":{"type":"string"},"appliedAt":{"type":"string","format":"date-time"},"staleAfter":{"type":"string","format":"date-time","description":"Beyond this the terminal refuses to trade."},"isStale":{"type":"boolean"},"pendingBundleVersion":{"type":"string","nullable":true,"description":"Published but not yet applied."}}},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"CreateCampaignRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","kind","channel","segmentId","content"],"properties":{"name":{"type":"string","maxLength":200},"kind":{"$ref":"#/components/schemas/CampaignKind"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"venueId":{"type":"string","format":"uuid"},"segmentId":{"type":"string","format":"uuid"},"content":{"$ref":"#/components/schemas/CampaignContent"},"trigger":{"$ref":"#/components/schemas/CampaignTrigger"},"scheduledFor":{"type":"string","format":"date-time"},"consentPurpose":{"allOf":[{"$ref":"#/components/schemas/ConsentPurpose"}],"default":"marketing"},"sendWindow":{"type":"object","description":"Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen.\n","properties":{"startTime":{"type":"string"},"endTime":{"type":"string"},"timeZone":{"type":"string"}}},"sendTimeMode":{"type":"string","enum":["fixed","optimised"],"default":"fixed","description":"`optimised` sends each recipient at the hour `ai.requestSuggestion` (kind `sendTime`) gives for them, inside `sendWindow` (29 September, build pass, group G2; 22.3.19). `fixed` is the behaviour before. Falls back to `scheduledFor` per recipient where there is no suggestion or AI is off."},"optimiseChannel":{"type":"boolean","default":false,"description":"With `sendTimeMode` `optimised`, route each recipient to the channel the suggestion names, among the channels they consented to (22.9.16). Off keeps `channel`."},"variants":{"type":"array","maxItems":5,"nullable":true,"description":"**A/B (or up to five-way) content and subject variants** (29 September, build pass, group G2; 22.1.17, BO-772). Each is a subject override and optionally a different template, written by a person or taken from an AI draft (`ai.proposeMarketingContent`, `source` `aiDraft`). Held as rows of `marketing.campaign_variant`. Null or empty is a single-content campaign.","items":{"$ref":"#/components/schemas/MarketingCampaignVariant"}},"abTest":{"type":"object","nullable":true,"description":"How the variants are tested. Required when `variants` has two or more.","properties":{"testPercent":{"type":"integer","minimum":5,"maximum":100,"default":20,"description":"Share of the audience the variants are tested on; 100 splits everyone and picks no winner."},"successMetric":{"type":"string","enum":["openRate","clickRate","conversionRate","attributedRevenue"],"default":"clickRate"},"decideAfterHours":{"type":"integer","minimum":1,"maximum":168,"default":4},"winnerRule":{"type":"string","enum":["automatic","manual"],"default":"automatic"},"minimumSamplePerVariant":{"type":"integer","minimum":1,"default":500,"description":"Below this many sends per variant no winner is declared automatically; a person picks."},"winningVariantId":{"type":"string","format":"uuid","nullable":true,"description":"Set by the automatic rule, or by a person through `updateCampaign`."}}}}},
"DeploymentProfile": {"type":"string","description":"How this workstation obtains catalogue and inventory (ADR-0013).\n- `terminalLocal` — own SQLite, leases direct from the cell. Small venues, 4G sites - `venueEdge` — own SQLite, distributed via the venue edge node which holds the\n  venue lease and sub-leases to terminals. Mid and large venues, stadium gates\n- `thin` — no local catalogue, server reads. Non-transactional surfaces only\n","enum":["terminalLocal","venueEdge","thin"]},
"DeviceBinding": {"x-ticvai-persistence":"platform.device","type":"object","required":["kind","driver"],"properties":{"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen.\n"},"identifier":{"type":"string","description":"Serial","port or network address.":null},"isRequired":{"type":"boolean","default":false,"description":"When true, the workstation refuses to open a shift if the device is absent.\n"}}},
"IndexFailure": {"type":"object","x-ticvai-persistence":"ai.index_failure","description":"ADR-0033. **Failure is a row somebody works, not a log line.**\n\n`ai.index_job` already counts `records_failed` and holds a `failure_sample`; **this is where the other 4,999 go.**","required":["id"],"properties":{"id":{"type":"string","format":"uuid"},"jobId":{"type":"string","format":"uuid"},"sourceId":{"type":"string","format":"uuid"},"documentRef":{"type":"string","description":"What would not index."},"stage":{"type":"string","enum":["fetch","parse","chunk","embed","upsert"],"description":"**Where it failed decides who fixes it.** A parse failure is a document problem; an embed failure is a provider one."},"error":{"type":"string"},"attempts":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.index_failure` had no scope column and no declared owner, so no policy. The indexed source's scope, copied when the failure is written.\n"}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"LostItem": {"type":"object","x-ticvai-persistence":"marketing.lost_item","description":"BL-021. **Screens existed on three platforms and `lostAndFound` is a `ModuleKey`, and there was no item, no claim and no match between them** — which is the whole capability.\nGeneric case management holds a conversation about a lost bag. **It cannot tell you that the bag somebody handed in on Tuesday is the one somebody asked about on Monday**, and that match is the only thing the module is for.\n","required":["id","kind","foundOrLost","venueId","reportedAt"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"foundOrLost":{"type":"string","enum":["lost","found"],"description":"**One entity, two directions.** A guest reports a loss and a steward reports a find, and modelling them separately means matching across two tables that drift.\n"},"kind":{"type":"string","enum":["bag","phone","wallet","keys","clothing","jewellery","documents","toy","buggy","other"]},"description":{"type":"string"},"colour":{"type":"string","nullable":true},"brand":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid"},"lastSeenPointId":{"type":"string","format":"uuid","nullable":true,"description":"A point on the venue map. **Where a guest thinks they lost it is the strongest signal for a match**, and it is also the thing they are least sure about.\n"},"reportedAt":{"type":"string","format":"date-time","description":"**Device time** — `recordLostItem` is offline-capable, so this is when the loss was reported or the find handed in, not when the device synced. The `recorded_at` of naming-and-style 5.2 for this row.\n"},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the record arrived. Equal to `reportedAt` for one recorded online."},"reportedBySubjectId":{"type":"string","format":"uuid","nullable":true},"storageLocation":{"type":"string","nullable":true},"status":{"readOnly":true,"type":"string","enum":["open","matched","claimed","disposed","returned"]},"photoAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"matchedItemId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The other side of the match — set by `matchLostItem` `match` (to `otherItemId`) and cleared by `unmatch`, on both items."},"caseId":{"type":"string","format":"uuid","nullable":true,"description":"The case the guest raised about it (`raiseMyCase` with `kind` `lostProperty`), where there is one."},"disposeAfter":{"type":"string","format":"date","nullable":true,"description":"**A retention date, because unclaimed property has one.** A storeroom with no disposal date is a storeroom that fills, and the date is a venue policy rather than a default.\n"}}},
"LostItemMatch": {"type":"object","description":"**The point of the module.** A found item and a lost report, proposed as the same thing.\n","properties":{"lostItemId":{"type":"string","format":"uuid"},"foundItemId":{"type":"string","format":"uuid"},"score":{"type":"number"},"matchedOn":{"type":"array","description":"What agreed — kind, colour, brand, location, date.","items":{"type":"string"}}}},
"MarketingCampaignVariant": {"type":"object","x-ticvai-persistence":"marketing.campaign_variant","description":"One content or subject variant of a campaign, for an A/B test (22.1.17; 29 September, build pass, group G2, from group G1's handoff). Written with its campaign by `createCampaign` and `updateCampaign`.","required":["label"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"campaignId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"marketing.campaign"},"label":{"type":"string","maxLength":20,"description":"A, B, C..."},"subjectOverride":{"type":"object","nullable":true,"description":"Subject line by locale.","additionalProperties":{"type":"string"}},"templateId":{"type":"string","format":"uuid","nullable":true,"description":"A different template for this variant; null uses the campaign's `content.templateId`."},"splitPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Share of the test group; null splits evenly."},"source":{"type":"string","enum":["manual","aiDraft"],"default":"manual"},"aiDecisionRecordId":{"type":"string","nullable":true,"description":"The decision record of the `ai.proposeMarketingContent` draft it came from, for `aiDraft`."},"isWinner":{"type":"boolean","default":false,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005), the campaign's."}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"OrgUnit": {"x-ticvai-persistence":"platform.scope","type":"object","required":["id","level","path","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"level":{"$ref":"#/components/schemas/tenancy::ScopeLevel"},"parentId":{"type":"string","format":"uuid","nullable":true},"path":{"type":"string","description":"Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"isActive":{"type":"boolean","description":"False causes every permission query at or beneath this node to resolve to DENY.\n"},"childCount":{"type":"integer","minimum":0}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"SaleBoardKind": {"type":"string","enum":["ticketing","fnb","retail","mixed"]},
"SuggestionProviderAssignments": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The routing table for `requestSuggestion`, held on the tenant's `ai.policy` row** as one `jsonb` column (`suggestion_providers`). At most one entry per `kind`.\n","items":{"$ref":"#/components/schemas/SuggestionProviderAssignment"}},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"},"consentFormId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's own consent form, which every biometric capture is taken on** (decided 2 October 2026, Chinmay, batch 4, BO-188: \"Consent first, on the venue's consent form\"; DEC-128, DEC-549; CHG-CSP-018). A form from the venue's consent-form builder in Venue Management (the one builder Face Pass, Face Tag, marketing and waivers share; marketing-crm `setDigitalWaiverForm`). Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access `enrolFacePass`, `enrolFaceTag`).\n"},"templatesHeldByTicvai":{"type":"boolean","readOnly":true,"description":"**True where TICVAI's platform stores this venue's biometric templates** (rather than the venue's own on-premises reader estate). Derived from the venue's access deployment. While true, Venue Management shows the venue a standing warning that every guest must accept the venue's consent form before capture, because the data sits with TICVAI as the venue's processor (decided 2 October 2026, Chinmay, batch 4, BO-188: \"If we store the data, highlight or notify the venue that the client must accept a consent form\"; DEC-128; CHG-CSP-018).\n"},"allowMinors":{"type":"boolean","default":true,"description":"**Whether this venue enrols minors at all** (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: \"Guardian consent on the venue's form; minor age per country; the venue can switch minors off\"; supersedes the GST-069 default; DEC-237; CHG-CSP-019). On: a minor (below `RegionSettings.minorAgeThreshold`) is enrolled only with a guardian's consent on the venue's consent form. Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method.\n"},"accreditationFaceMatching":{"type":"object","nullable":true,"description":"**Face matching to find duplicate accreditation applicants, off unless the venue enables it** (decided 2 October 2026, Chinmay, critical set 3, BO-631: \"Only where the venue enables it, with applicant consent and the venue's legal sign-off; off by default\"; DEC-461; CHG-CSP-022). Enabling it is refused without `legalSignOffReference` (`422 legal-sign-off-required`); each applicant matched must have consented on the application (accreditation's own record). Null is off.\n","properties":{"isEnabled":{"type":"boolean","default":false},"legalSignOffReference":{"type":"string","nullable":true,"maxLength":200,"description":"The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when."},"signedOffByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"signedOffAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"chargeCurrencies":{"type":"array","nullable":true,"description":"**Which currencies a guest may select and pay in** (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). A subset of `displayCurrencies`: each code must also be one the venue's payment provider can charge (`orders.PaymentProvider.presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. Null or empty: guests pay in the trading (base) currency only and the other display currencies stay approximate. The ledger is always in the base currency, with the rate recorded on every payment and refund.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).** The client's policy of 6 October 2026 (tracker answer T10.1, `sources/client/2026-10-06-tracker-answers.md`; CHG-R4-019): the tolerance is configurable, a difference within it closes only with a reason (`shift.giveShiftVarianceReason`), and beyond it needs supervisor or manager approval (OVERSHORT_ACCEPT).\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**The most cash a till drawer should hold before some is lifted to the safe** (decided 2 October 2026, Chinmay, batch 6 set 3, BO-042: \"Add drawer limit setting (warn + offer cash lift)\"; DEC-179; CHG-CSP-016; DI-274: on a busy day the cashier unloads excess cash mid-shift and it is reconciled at close). The venue default; a till may set its own (`Workstation.cashDrawerLimit`). When the cash a till has taken since its last count takes the drawer over it, the till warns and offers a cash lift (`shift.createCashMovement` kind `lift`) and BO-042 flags the box (`shift.DepositBox.overDrawerLimit`). A warning, never a block: a sale is not refused because the drawer is full. Null sets no limit. **No proposed default: the client's finance team sets it.**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"tableReservedLeadMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":240,"default":30,"deprecated":true,"description":"**Deprecated (2 October 2026, CHG-CLN-009): `fnb.FnbReservationPolicy.reservedLeadMinutes` is canonical.** The table state model reads the reservation policy (`states/table.yaml`); this venue setting is kept for compatibility, never read, and not drawn. Its former meaning: **How long before a pre-allocated booking its table shows Reserved** (decided 2 October 2026, Chinmay, batch 6 set 6b, EMP-052: \"Reserved when a booking names the table, or N minutes (venue-set) before a pre-allocated booking\"; DEC-202; CHG-CSP-017; DI-689, DI-336). A booking that names its table holds it as Reserved for the booking's whole slot; a booking the host pre-allocated shows its table Reserved from this many minutes before it. Zero shows Reserved only once the booking is due. The fnb table state model applies it (`states/table.yaml`, owned by fnb). Proposed default 30 minutes, client to correct.\n"},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}},
"Workstation": {"x-ticvai-persistence":"platform.workstation","type":"object","required":["id","code","name","venueId","regionId","scopePath","saleBoard","currency","currencyScale","timeZone"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"**The outlet this till stands in** (CHG-CSP-006). Its board is the till's board unless the till overrides it. Null on a workstation that belongs to no outlet (a ticket office counter set up before outlets), which must then carry its own board.\n"},"scopePath":{"type":"string"},"saleBoard":{"type":"object","description":"Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. What the operator may then DO within it is governed by their permissions.\n**The effective board** since 2 October 2026 (DEC-183; CHG-CSP-006): the till's own when it overrides the outlet, otherwise the outlet's (`saleBoardSource`).\n","required":["id","kind"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"name":{"type":"string"}}},"saleBoardSource":{"type":"string","enum":["outlet","workstation"],"readOnly":true,"description":"**Where `saleBoard` came from** (decided 2 October 2026, Chinmay, BO-109: \"Per outlet, with a till override\"; DEC-183; CHG-CSP-006): `outlet` when the till uses its outlet's layout, `workstation` when this till overrides it. BO-109 shows which tills differ from their outlet.\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**This till's drawer limit, overriding the venue's** (`VenueSettings.cashDrawerLimit`; DEC-179; CHG-CSP-016). Null inherits the venue's. Above it the till warns and offers a cash lift.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point.\n"},"devices":{"type":"array","items":{"$ref":"#/components/schemas/DeviceBinding"}},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"timeZone":{"type":"string"},"deploymentProfile":{"$ref":"#/components/schemas/DeploymentProfile"},"edgeNodeId":{"type":"string","format":"uuid","nullable":true,"description":"Present when `deploymentProfile` is `venueEdge`."},"healthScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"readOnly":true,"description":"Board 1 of the client's POS set. **A number a manager can sort by** — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a score.\nThe client's board shows 1,248 workstations at 96% healthy, and **the value of that figure is that it ranks**: a fleet dashboard exists so somebody can open the worst one first.\n**Derived from its devices, its heartbeat age, its firmware currency and its error rate.** Read-only, because a workstation that could set its own score would.\n**The formula, proposed, client to correct (audit R096 (2)):** score = 40% device online share (the share of its devices reporting online) + 25% heartbeat freshness (100 at one minute old or less, 0 at 15 minutes or more, linear between) + 20% firmware and profile currency (100 on the latest, 50 one version behind, 0 older) + 15% error rate (100 at 0 errors an hour, 0 at 10 or more, linear between), rounded to a whole number. **Below 80 is a warning and below 60 a failure.**\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"description":"Which profile this workstation runs, and at which version. **The client's board shows a fleet split four ways — 72% latest, 18.8% one behind, 6.1% outdated** — and the package had a firmware version field and no profile.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks*.\n"},"catalogueState":{"$ref":"#/components/schemas/CatalogueState"},"offlineCapable":{"type":"boolean","description":"Derived from `deploymentProfile`. False only for `thin`. Under local-first, catalogue READS are always local on transactional surfaces; this flag governs whether WRITES can be queued.\n"},"isActive":{"type":"boolean"}}}
}
```
