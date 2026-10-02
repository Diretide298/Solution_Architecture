# WS25 — Customer Service board 1

**10 screens · 20 operations · 36 schemas · 7 permissions**

Platform P12 Venue Support · ships as **venue-management** ·
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
  `AI_CONFIGURE, AI_USE, ASSET_LIBRARY_MANAGE, CASE_MANAGE, CASE_VIEW, ORDER_REFUND, ORDER_VIEW`. A control nobody can use must say so,
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
| `SUP-009` | Customer Service Command Center | B–D | 0 | 44 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `SUP-010` | Customer 360° Service Profile | B–D | 0 | 38 | 6 | 0 | 4 | 0 | — | notStarted (generated) |
| `SUP-011` | Unified Interaction & Communication History | B–D | 11 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `SUP-012` | Case Creation, Classification & Intelligent Routing | B–D | 30 | 7 | 5 | 8 | 2 | 0 | — | notStarted (generated) |
| `SUP-013` | Case Investigation & Resolution Workspace | B–D | 32 | 42 | 6 | 4 | 1 | 0 | — | notStarted (generated) |
| `SUP-014` | Order, Booking & Ticket Service Workspace | B–D | 2 | 37 | 6 | 5 | 2 | 6 | — | notStarted (generated) |
| `SUP-015` | Refund, Compensation & Service Exception Workspace | B–D | 0 | 16 | 6 | 0 | 2 | 6 | — | notStarted (generated) |
| `SUP-016` | Escalation, Collaboration & Internal Resolution | B–D | 8 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `SUP-017` | Case Resolution, Closure & Customer Feedback | B–D | 27 | 0 | 5 | 1 | 1 | 0 | — | notStarted (generated) |
| `SUP-018` | AI Customer Service Copilot & Knowledge Workspace | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**SUP-010, SUP-018 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `SUP-009` Customer Service Command Center

**Provide every customer-service agent with a personalized operational workspace showing customers, cases, tasks, SLAs, alerts and workload.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/customer-service-command-center-sup-009` |

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: New Case, Find Customer, Find Order, Find Ticket, Find Booking, Assign Case, Escalate, Open AI Assistant. …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The agent's personal workspace: their cases, tasks, SLAs, alerts and workload, with quick finds (customer, order, ticket, booking) and New Case.

**Known correction pending (do not draw the wrong version)**

- **SUP-002 Agent Dashboard and SUP-009 Customer Service Command Center are both "the agent's own workload" home.** Why: Two homes for one agent; merge or define SUP-009 as the board hub. *(source: screens/P12-support-agent-console.yaml#SUP-002; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Agent principal | picker: choose an agent principal | — | — | `listCustomerService` ?agentPrincipalId |
| Subject | picker: choose a subject | — | — | `listCustomerServiceProfile` ?subjectId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every customer service** (data table, from `listCustomerService`)

| Shows | Format | Notes |
|---|---|---|
| My open cases | 1,234 | Status not `resolved` or `closed`. |
| New cases | 1,234 | Assigned to the agent and still `open` (not yet picked up). |
| Cases due today | 1,234 | Open, with `slaDueAt` falling today. |
| Sla at risk | 1,234 | Open, not breached, with less than 25% of the SLA window left. |
| Sla breached | 1,234 | Open with `Case.isSlaBreached` true. |
| Awaiting customer | 1,234 | Status `awaitingGuest`. |
| Awaiting internal team | 1,234 | Open, with at least one open internal request. |
| Escalated cases | 1,234 | — |
| Resolved today | 1,234 | — |
| Average resolution seconds | 1,234 | Mean of `resolvedAt - recordedAt - slaPausedSeconds` over the agent's cases resolved in the last 30 days; null when none. |
| Case | the name it points at, never the id | — |
| Customer | text | The guest's name, resolved from `pii.subject` as `Case.guestName` is; null unless the caller holds GUEST_VIEW_PII. |
| Subject | text | — |
| Category | text | The category's display name. |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Priority | chip: Low, Normal, High, Urgent | — |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Assigned agent principal | the name it points at, never the id | — |
| Sla remaining seconds | 1,234 | Negative once breached. |
| Last interaction at | 1 Oct 2026, 14:30 | The latest `CaseMessage.recordedAt`. |
| Next action | chip: Respond to customer, Follow up internal request, Await approval, Propose … | — |
| Kind | chip: Call customer, Respond to complaint, Review refund request, Follow up finance … | — |

**The selected customer service** (detail panel): The pack groups this record's detail under its own headings: “Use”, “Customer Waiting”.

| Shows | Format | Notes |
|---|---|---|
| My open cases | 1,234 | Status not `resolved` or `closed`. |
| New cases | 1,234 | Assigned to the agent and still `open` (not yet picked up). |
| Cases due today | 1,234 | Open, with `slaDueAt` falling today. |
| Sla at risk | 1,234 | Open, not breached, with less than 25% of the SLA window left. |
| Sla breached | 1,234 | Open with `Case.isSlaBreached` true. |
| Awaiting customer | 1,234 | Status `awaitingGuest`. |
| Awaiting internal team | 1,234 | Open, with at least one open internal request. |
| Escalated cases | 1,234 | — |
| Resolved today | 1,234 | — |
| Average resolution seconds | 1,234 | Mean of `resolvedAt - recordedAt - slaPausedSeconds` over the agent's cases resolved in the last 30 days; null when none. |
| Case | the name it points at, never the id | — |
| Customer | text | The guest's name, resolved from `pii.subject` as `Case.guestName` is; null unless the caller holds GUEST_VIEW_PII. |
| Subject | text | — |
| Category | text | The category's display name. |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Priority | chip: Low, Normal, High, Urgent | — |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Assigned agent principal | the name it points at, never the id | — |
| Sla remaining seconds | 1,234 | Negative once breached. |
| Last interaction at | 1 Oct 2026, 14:30 | The latest `CaseMessage.recordedAt`. |
| Next action | chip: Respond to customer, Follow up internal request, Await approval, Propose … | — |
| Kind | chip: Call customer, Respond to complaint, Review refund request, Follow up finance … | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| New Case (primary button) | navigation or local | — | — | — | — |
| Find Customer (secondary button) | navigation or local | — | — | — | — |
| Find Order (secondary button) | navigation or local | — | — | — | — |
| Find Ticket (secondary button) | navigation or local | — | — | — | — |
| Find Booking (secondary button) | navigation or local | — | — | — | — |
| Assign Case (secondary button) | navigation or local | — | — | — | — |
| Escalate (secondary button) | navigation or local | — | — | — | — |
| Open AI Assistant (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **My KPIs**: Assigned, due today, breached, awaiting guest (SLA paused), resolved today. *(source: contracts/satellite/marketing-crm.yaml#listCustomerService; DI-539)*

**Data it reads**: `listCustomerService` (onLoad, Customer Service Command Center); `listCustomerServiceProfile` (onLoad, Customer 360° Service Profile)

**Where the user goes next**

- → `SUP-001` Venue Management Sign In: *Agent Login*
- → `SUP-010` Customer 360° Service Profile: *Works in Customer 360° Service Profile*; calls `listCustomerService`
- → `SUP-011` Unified Interaction & Communication History: *Works in Unified Interaction & Communication History*; calls `listCustomerService`
- → `SUP-012` Case Creation, Classification & Intelligent Routing: *Works in Case Creation, Classification & Intelligent Routing*; calls `listCustomerService`
- → `SUP-013` Case Investigation & Resolution Workspace: *Works in Case Investigation & Resolution Workspace*; carries `caseId`; calls `listCustomerService`
- → `SUP-014` Order, Booking & Ticket Service Workspace: *Works in Order, Booking & Ticket Service Workspace*; calls `listCustomerService`
- → `SUP-015` Refund, Compensation & Service Exception Workspace: *Works in Refund, Compensation & Service Exception Workspace*; calls `listCustomerService`
- → `SUP-016` Escalation, Collaboration & Internal Resolution: *Works in Escalation, Collaboration & Internal Resolution*; calls `listCustomerService`
- → `SUP-017` Case Resolution, Closure & Customer Feedback: *Works in Case Resolution, Closure & Customer Feedback*; carries `caseId`; calls `listCustomerService`
- → `SUP-018` AI Customer Service Copilot & Knowledge Workspace: *Works in AI Customer Service Copilot & Knowledge Workspace*; calls `listCustomerService`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer service list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer service untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer service yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer service are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SUP-002`: Overlaps the Agent Dashboard; both show the agent's own work.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  assigned: 11
  dueToday: 4
  breached: 1
  awaitingGuest: 3
  resolvedToday: 6
```

#### Permissions

- `listCustomerService` → `CASE_VIEW` (read) · staff
- `listCustomerServiceProfile` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Case dashboard shows total cases logged, due cases and per-agent case load, each governed by an SLA based on case type. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-539)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-009` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS42 Customer Service Board 1.dc.html#sup-009`
- Workshop pack: Customer Service_Reference.pdf board 1
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 1: Opens Customer Service Command Center → Provide every customer-service agent with a personalized operational workspace showing customers, cases, tasks, SLAs, alerts and workload.
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F134 branch at step 1 (expected): when Nothing has been set up on Customer Service Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F134 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: New Case, Find Customer, Find Order, Find Ticket, Find Booking, Assign Case, Escalate, Open AI Assistant.
- [ ] Every transition is wired: `SUP-001`, `SUP-010`, `SUP-011`, `SUP-012`, `SUP-013`, `SUP-014`, `SUP-015`, `SUP-016`, `SUP-017`, `SUP-018`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-010` Customer 360° Service Profile

**Provide the agent with a complete customer-service view of the customer. This should be one of the most important screens in the entire Customer Service module.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/customer-360-service-profile-sup-010` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The agent's complete service view of one guest: details, open cases and history, current products and entitlements with status (active, reserved, consumed, transferred, expired, refunded or cancelled), family composition, service alerts, permitted preferences and an AI summary.

**Known correction pending (do not draw the wrong version)**

- **The 360 is drawn as a data table of "every customer 360" with listCustomerService.** Why: It is one guest's view; open from a search or a case with the guest id. *(source: screens/P12-support-agent-console.yaml#SUP-010; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Subject | picker: choose a subject | — | — | `listCustomerServiceProfile` ?subjectId |
| Agent principal | picker: choose an agent principal | — | — | `listCustomerService` ?agentPrincipalId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every customer 360° service** (data table, from `listCustomerServiceProfile`)

| Shows | Format | Notes |
|---|---|---|
| Customer name | text | Null unless the caller holds GUEST_VIEW_PII. |
| Customer | the name it points at, never the id | The guest's `subjectId`. |
| Customer type | chip: Individual, Member, Group organiser, Corporate, Partner | — |
| Membership status | chip: None, Active, Expiring, Lapsed | — |
| Loyalty tier | text | — |
| Preferred language | text | — |
| Country | text | — |
| Contact details | grouped details | Masked (e.g. `j*@example.com`, `+971 * 4821`) unless the caller holds GUEST_VIEW_PII. |
| Customer since | 1 Oct 2026, 14:30 | — |
| Customer value | AED 1,234.50 | Lifetime net spend across the tenant. |
| Open cases | text | not in the schema: `Open Cases` |
| Risk attention indicator | chip: None, Attention, Risk | `attention` with an open complaint or an unresolved refund case; `risk` with a breached SLA or a repeat contact on the same issue. |
| 360° navigation | text | not in the schema: `360° Navigation` |
| Upcoming tickets | 1,234 | — |
| Active membership | grouped details | — |
| Wallet balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Active reservations | 1,234 | — |
| Future group bookings | 1,234 | — |
| Open orders | text | not in the schema: `Open Orders` |

**The selected customer 360° service** (detail panel): The pack groups this record's detail under its own headings: “Today”, “Yesterday”, “Last Month”, “Display permitted information such as”, “Sensitive information should be”, “Customer Summary”.

| Shows | Format | Notes |
|---|---|---|
| Customer name | text | Null unless the caller holds GUEST_VIEW_PII. |
| Customer | the name it points at, never the id | The guest's `subjectId`. |
| Customer type | chip: Individual, Member, Group organiser, Corporate, Partner | — |
| Membership status | chip: None, Active, Expiring, Lapsed | — |
| Loyalty tier | text | — |
| Preferred language | text | — |
| Country | text | — |
| Contact details | grouped details | Masked (e.g. `j*@example.com`, `+971 * 4821`) unless the caller holds GUEST_VIEW_PII. |
| Customer since | 1 Oct 2026, 14:30 | — |
| Customer value | AED 1,234.50 | Lifetime net spend across the tenant. |
| Open cases | text | not in the schema: `Open Cases` |
| Risk attention indicator | chip: None, Attention, Risk | `attention` with an open complaint or an unresolved refund case; `risk` with a breached SLA or a repeat contact on the same issue. |
| 360° navigation | text | not in the schema: `360° Navigation` |
| Upcoming tickets | 1,234 | — |
| Active membership | grouped details | — |
| Wallet balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Active reservations | 1,234 | — |
| Future group bookings | 1,234 | — |
| Open orders | text | not in the schema: `Open Orders` |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Entitlements portfolio**: One list across the visit with restrictions and wallet balance, the same view the guest app shows. *(source: DI-667; DI-670)*
- **Family**: A family ticket's composition with each dependant's entitlements. *(source: DI-668)*
- **Contactability**: Consent per channel and purpose before any outbound action. *(source: DI-378)*

**Data it reads**: `listCustomerServiceProfile` (onLoad, Customer 360° Service Profile); `listCustomerService` (onLoad, Customer Service Command Center)

**Where the user goes next**

- → `SUP-009` Customer Service Command Center: *Returns to the board's landing screen*; calls `listCustomerServiceProfile`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer 360° service list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer 360° service untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer 360° service yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer 360° service are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-737`: Same guest header.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
guest: Khalid Al Suwaidi - Gold - 3 open entitlements (2 adult, 1 child Day Pass, Sat 3 Oct) - wallet AED 240.00
  - open case CA-1120
```

#### Permissions

- `listCustomerServiceProfile` → `CASE_VIEW` (read) · staff
- `listCustomerService` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Entitlement statuses: active, reserved, consumed, transferred, expired, refunded/cancelled; views show entitlements nearing expiry, real-time consumption per customer, and whether a ticket has been upgraded. *(client request · MoM 7 Sep 2026, 4.10 / 4.11 Entitlements Lifecycle & Usage · DI-670)*
- Family/dependent view shows a family ticket's composition (e.g. two adults, two children) with each dependent's entitlements; equivalent views for school and corporate bookings. *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-668)*
- Entitlements portfolio is used both by the guest (mobile app) and by customer service: one view of restrictions, wallet balance and all entitlements; a unified list across a visit (e.g. four admissions, two fast passes, a meal package, a parking entitlement). *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-667)*
- Customer profile gives agents one view of customer details, open cases and case history; a communications & transactions screen shows the full history of prior communications and actions. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-540)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-010` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS42 Customer Service Board 1.dc.html#sup-010`
- Workshop pack: Customer Service_Reference.pdf board 1
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 2: Works in Customer 360° Service Profile → Provide the agent with a complete customer-service view of the customer. This should be one of the most important screens in the entire Customer Service module.
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (38 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-010?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SUP-009`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-011` Unified Interaction & Communication History

**Provide one chronological timeline of customer interactions across supported service channels.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/unified-interaction-communication-history-sup-011` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** One chronological timeline of a guest's interactions across service channels: case messages, chat messages, internal notes, calls and automated notifications, with direction, agent or system, and links to the related case, order or ticket.

**Known correction pending (do not draw the wrong version)**

- **The screen is a configEditor whose fields (Date/Time, Channel, Customer, Direction, Subject) are selects.** Why: These are timeline columns and filters; the screen is a read-only list. *(source: screens/P12-support-agent-console.yaml#SUP-011; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Date/Time | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Customer | select field | — | — | — | — | — | — |
| Agent/System | select field | — | — | — | — | — | — |
| Direction | select field | — | — | — | — | — | — |
| Subject | select field | — | — | — | — | — | — |
| Related Case | select field | — | — | — | — | — | — |
| Related Order | select field | — | — | — | — | — | — |
| Related Ticket | select field | — | — | — | — | — | — |
| Attachments | select field | — | — | — | — | — | — |
| Sentiment where enabled | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Subject | picker: choose a subject | — | — | `listUnifiedInteractionCommunication` ?subjectId |
| Keyword | text field | — | min length 2; max length 200 | `listUnifiedInteractionCommunication` ?keyword |
| From | date and time picker | — | — | `listUnifiedInteractionCommunication` ?from |
| To | date and time picker | — | — | `listUnifiedInteractionCommunication` ?to |
| Channel | select | — | Email · Phone · Live chat · Whatsapp · SMS · Web form · Mobile app · B2C portal · Social · POS front desk · Internal note · Automated notification | `listUnifiedInteractionCommunication` ?channel |
| Agent principal | picker: choose an agent principal | — | — | `listUnifiedInteractionCommunication` ?agentPrincipalId |
| Case | picker: choose a case | — | — | `listUnifiedInteractionCommunication` ?caseId |
| Order | picker: choose an order | — | — | `listUnifiedInteractionCommunication` ?orderId |
| Ticket | text field | — | — | `listUnifiedInteractionCommunication` ?ticketId |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Timeline item**: Date and time, channel, direction, who (agent, system, AI), subject, related records, sentiment where enabled; internal notes marked. *(source: contracts/satellite/marketing-crm.yaml#listUnifiedInteractionCommunication; DI-540)*

**Data it reads**: `listUnifiedInteractionCommunication` (onLoad, Unified Interaction & Communication History)

**Where the user goes next**

- → `SUP-009` Customer Service Command Center: *Returns to the board's landing screen*; calls `listUnifiedInteractionCommunication`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The unified interaction communication configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the unified interaction communication untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No unified interaction communication configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
items:
- 1 Oct 10:42 - WhatsApp - outbound - Aisha - reply on CA-1120
- 1 Oct 10:41 - WhatsApp - inbound - guest
- 30 Sep 18:00 - email - system - visit reminder
```

#### Permissions

- `listUnifiedInteractionCommunication` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Customer profile gives agents one view of customer details, open cases and case history; a communications & transactions screen shows the full history of prior communications and actions. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-540)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-011` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS42 Customer Service Board 1.dc.html#sup-011`
- Workshop pack: Customer Service_Reference.pdf board 1
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 4: Works in Unified Interaction & Communication History → Provide one chronological timeline of customer interactions across supported service channels.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-011?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SUP-009`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-012` Case Creation, Classification & Intelligent Routing

**Create structured customer-service cases and ensure they reach the correct team.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/case-creation-classification-intelligent-routing-sup-012` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Create a structured case and get it to the right team: customer, subject, description, source, category and subcategory, priority, venue, event, related records, attachments. The routing preview shows the recommended queue and agent (by skill, language, availability, workload, priority), which the agent can override before confirming.

**Known correction pending (do not draw the wrong version)**

- **Every field is a select field (Customer, Subject, Description, Attachments).** Why: Subject and description are text; customer is a search; attachments an upload. *(source: screens/P12-support-agent-console.yaml#SUP-012; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

**Fixed on main** (the package already carries these; draw what it says): createCaseClassificationIntelligent "stores nothing", and createCase is not declared. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Customer | select field | — | — | — | — | — | — |
| Subject | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Source | select field | — | — | — | — | — | — |
| Category | select field | — | — | — | — | — | — |
| Subcategory | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Related Order | select field | — | — | — | — | — | — |
| Related Ticket | select field | — | — | — | — | — | — |
| Related Payment | select field | — | — | — | — | — | — |
| Related Membership | select field | — | — | — | — | — | — |
| Attachments | select field | — | — | — | — | — | — |
| Parent category id | picker: choose a parent category (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?parentCategoryId=` to `listCaseCategories`. | `listCaseCategories` ?parentCategoryId |
| Top level only | toggle | optional | off | — | — | Sends `?topLevelOnly=` to `listCaseCategories`. | `listCaseCategories` ?topLevelOnly |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listCaseCategories`. | `listCaseCategories` ?isActive |

**Form: Create case** (modal, opened by *Create case*; *Create case* calls `createCase`, *Cancel* sends nothing)

**Collects what `createCase` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createCase` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `createCase` body |
| Subject `subject` | text field | required | — | max length 200 | — | — | `createCase` body |
| Description `description` | text area | required | — | max length 10000 | — | — | `createCase` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `createCase` body |
| Membership `membershipId` | picker: choose a membership | optional | — | — | shows names, sends the id | The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. | `createCase` body |
| Priority `priority` | radio group | optional | Normal | Low · Normal · High · Urgent | — | — | `createCase` body |
| Kind `kind` | select | optional | — | Lost property · Complaint · Question · Accessibility · Refund request · Other; Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.; A case raised as `other` must carry a non-empty `detail` … | — | What the guest says the case is about, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. | `createCase` body |
| Channel `channel` | select | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `createCase` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCase` body |
| Related order `relatedOrderId` | text field | optional | — | — | — | — | `createCase` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | Stored on the opening `CaseMessage`, not on the case. | `createCase` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time the case was raised. The server stamps `Case.syncedAt` on arrival. | `createCase` body |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Subject and description**: Text fields, not selects. *(source: contracts/satellite/marketing-crm.yaml#createCase)*
- **Category and subcategory**: From the two-level taxonomy; AI may suggest, the agent confirms. *(source: DI-541; contracts/satellite/marketing-crm.yaml#createCaseClassificationIntelligent)*

#### Outputs: what the screen shows and produces

**Shown**

**Every case category** (data table, from `listCaseCategories`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Parent category | the name it points at, never the id | Set on a subcategory; null on a top-level category. |
| Default priority | chip: Low, Normal, High, Urgent | The priority a case in this category starts at before routing factors apply. |
| Is active | yes / no (icon or chip) | — |
| Scope path | text | The partition key (ADR-0005). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create (primary button) | navigation or local | — | — | — | — |
| Create case (secondary button) | `createCase` POST `/cases` | CreateCaseRequest | Case | — | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Routing preview**: Recommended category, queue and agent with reasons; override is recorded. *(source: DI-545)*

**Data it reads**: `listCaseCategories` (onLoad, List case categories and subcategories)

**Where the user goes next**

- → `SUP-009` Customer Service Command Center: *Returns to the board's landing screen*; calls `createCaseClassificationIntelligent`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The case creation classification configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the case creation classification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No case creation classification configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
case:
  customer: Fatima Al Mansoori
  subject: Charged twice for parking
  source: Phone
  category: Payments > Duplicate charge
  priority: High
preview: Membership & billing queue - Joseph Mathew (Arabic/English, 2 of 5 load)
```

#### Permissions

- `createCaseClassificationIntelligent` → `CASE_MANAGE` (configure) · staff
- `listCaseCategories` → `CASE_VIEW` (read) · staff
- `createCase` → `CASE_MANAGE` (configure) · staff, guest, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.66 | Guest Support - System shall provide guest support channels. | Guest Mobile App & Branding | CONTRACTED | `createCase` |
| 19.2.70 | Complaint Management - System shall support guest complaints. | Guest Mobile App & Branding | CONTRACTED | `createCase` |
| 2.8.12 | System shall allow agents to create, assign, escalate, track, and resolve guest cases including complaints, refund requests, service requests, incidents, and operational issues. Cases shall be linked … | Ticketing Sales | CONTRACTED | `createCase` |
| 5.3.34 | Link guest profiles with customer service cases, complaints, incidents, refunds, investigations, and follow-up activities. | F&B & Guest Management | CONTRACTED | `createCase` |
| 22.3.1 | Case Creation | Marketing & CRM | CONTRACTED | `createCase` |
| 22.3.2 | Case Classification | Marketing & CRM | CONTRACTED | `createCase` |
| 22.3.3 | Case Assignment | Marketing & CRM | CONTRACTED | `createCase` |
| 22.8.12 | Case Creation & Escalation | Marketing & CRM | CONTRACTED | `createCase` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Intelligent routing assigns cases by skill, language, availability, workload and priority, showing an assignment preview that the user can manually override before confirming. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-545)*
- Case creation captures logging channel/source, category and subcategory (e.g. ticket issue > reschedule) and supports screenshot attachments; investigation tracks all activity and actions on the case. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-541)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-012` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS42 Customer Service Board 1.dc.html#sup-012`
- Workshop pack: Customer Service_Reference.pdf board 1
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 6: Works in Case Creation, Classification & Intelligent Routing → Create structured customer-service cases and ensure they reach the correct team.

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-012?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create, Create case.
- [ ] Every transition is wired: `SUP-009`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-013` Case Investigation & Resolution Workspace

**Provide the primary workspace in which an agent investigates and resolves a case.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `CASE_MANAGE`, `CASE_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `caseId` (navigation), `uploadId` (navigation) |
| Route | `/support/case-investigation-resolution-workspace-sup-013` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Action history. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Where the agent investigates and resolves a case: thread, activity, linked records (order, ticket, payment, refund, membership, wallet transaction), actions taken, and the AI summary of everything done.

**Fixed on main** (the package already carries these; draw what it says): The table is bound to setCaseInvestigationResolution (a write), and getCase, addCaseMessage and updateCase are not declared. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Form: Add message** (modal, opened by *Add message*; *Add message* calls `addCaseMessage`, *Cancel* sends nothing)

**Collects what `addCaseMessage` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `addCaseMessage` body |
| Body `body` | text area | required | — | min length 1; max length 10000 | — | — | `addCaseMessage` body |
| Is internal `isInternal` | toggle | required | — | — | — | — | `addCaseMessage` body |
| Channel `channel` | select | optional | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `addCaseMessage` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `addCaseMessage` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addCaseMessage` body |

**Form: Save case** (modal, opened by *Save case*; *Save case* calls `updateCase`, *Cancel* sends nothing)

**Collects what `updateCase` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | optional | — | Open · In progress · Awaiting guest · Escalated · Resolved · Closed | — | — | `updateCase` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent | — | — | `updateCase` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `updateCase` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateCase` body |
| Resolution note `resolutionNote` | text area | optional | — | max length 2000 | — | — | `updateCase` body |

Errors to draw in the form: 400 Resolving without a resolution note

**Form: Attach file** (modal, opened by *Attach file*; *Attach file* calls `createUpload`, *Cancel* sends nothing)

**Collects what `createUpload` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Filename `filename` | text area | required | — | max length 256 | — | — | `createUpload` body |
| Content type `contentType` | text field | required | — | — | — | — | `createUpload` body |
| Size bytes `sizeBytes` | number field | required | — | min 1 | — | — | `createUpload` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createUpload` body |

Errors to draw in the form: 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.

**Sent by *Confirm attachment*** (`completeUpload`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `completeUpload` body |
| Alt text `altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `completeUpload` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `completeUpload` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | — | `completeUpload` body |
| Rights `rights` | group | optional | — | — | — | Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item. | `completeUpload` body |
| Licence kind `rights.licenceKind` | select | optional | — | Owned · Royalty free · Rights managed · Creative commons · Editorial only · Unknown | — | — | `completeUpload` body |
| Licensor `rights.licensor` | text field | optional | — | — | — | — | `completeUpload` body |
| Licence reference `rights.licenceReference` | text field | optional | — | — | — | — | `completeUpload` body |
| Valid from `rights.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `completeUpload` body |
| Valid to `rights.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `completeUpload` body |
| Permitted uses `rights.permittedUses` | multi-select chips | optional | — | Web · Print · Social media · In venue · Advertising · Internal | — | — | `completeUpload` body |
| Attribution required `rights.attributionRequired` | toggle | optional | off | — | — | — | `completeUpload` body |
| Attribution text `rights.attributionText` | text field | optional | — | — | — | — | `completeUpload` body |
| Permitted territories `rights.permittedTerritories` | list of values (chips) | optional | — | — | — | ISO country or region codes. Empty means unrestricted, which is a claim rather than an absence — an unknown territory and a worldwide licence are not the same thing, and … | `completeUpload` body |
| Permitted channels `rights.permittedChannels` | list of values (chips) | optional | — | — | — | Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route. | `completeUpload` body |
| Model release held `rights.modelReleaseHeld` | toggle | optional | off | — | — | — | `completeUpload` body |
| Renewal owner `rights.renewalOwner` | picker: choose a renewal owner | optional | — | — | shows names, sends the id | — | `completeUpload` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every case investigation resolution** (data table, from `setCaseInvestigationResolution`)

| Shows | Format | Notes |
|---|---|---|
| Case | the name it points at, never the id | — |
| Customer | text | The guest's name, as `Case.guestName`; null unless the caller holds GUEST_VIEW_PII. |
| Subject | text | — |
| Category | text | The category's display name. |
| Priority | chip: Low, Normal, High, Urgent | — |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Sla | grouped details | — |
| Owner | the name it points at, never the id | The assigned agent's principal id (`Case.assignedToPrincipalId`). |
| Queue | text | — |
| Created | 1 Oct 2026, 14:30 | `Case.createdAt`. |
| Last updated | 1 Oct 2026, 14:30 | — |

**The case** (detail panel, from `getCase`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7. |
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Subject | the name it points at, never the id | — |
| Guest name | text | Resolved from `pii.subject` when the case is read, never stored on the case. A name copied onto a case row is personal data outside the … |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Kind | chip: Lost property, Complaint, Question, Accessibility, Refund request, Other | What the guest said it was about, where the guest raised it. |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`. |
| Recorded at | 1 Oct 2026, 14:30 | Device time the case was raised — the start of the SLA clock. |
| Synced at | 1 Oct 2026, 14:30 | Server time the case arrived. Equal to `recordedAt` for a case raised online. |
| Category | the name it points at, never the id | — |
| Queue | the name it points at, never the id | The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). |
| Membership | the name it points at, never the id | The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Priority | chip: Low, Normal, High, Urgent | — |
| Assigned to principal | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Related order | text | — |
| Sla due at | 1 Oct 2026, 14:30 | — |
| Is sla breached | yes / no (icon or chip) | Computed when read, never stored. True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` … |
| Sla paused seconds | 1,234 | Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock. |

**The selected case investigation resolution** (detail panel): The pack groups this record's detail under its own headings: “Agents can attach”, “Case Actions”.

| Shows | Format | Notes |
|---|---|---|
| Case | the name it points at, never the id | — |
| Customer | text | The guest's name, as `Case.guestName`; null unless the caller holds GUEST_VIEW_PII. |
| Subject | text | — |
| Category | text | The category's display name. |
| Priority | chip: Low, Normal, High, Urgent | — |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Sla | grouped details | — |
| Owner | the name it points at, never the id | The assigned agent's principal id (`Case.assignedToPrincipalId`). |
| Queue | text | — |
| Created | 1 Oct 2026, 14:30 | `Case.createdAt`. |
| Last updated | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Action history (primary button) | navigation or local | — | — | — | — |
| Add message (secondary button) | `addCaseMessage` POST `/cases/{caseId}/messages` | inline | CaseMessage | — | opens modal first |
| Save case (secondary button) | `updateCase` PATCH `/cases/{caseId}` | inline | Case | 400 Resolving without a resolution note | opens modal first |
| Attach file (secondary button) | `createUpload` POST `/media/uploads` | inline | UploadTicket | 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes. | opens modal first |
| Confirm attachment (secondary button) | `completeUpload` POST `/media/uploads/{uploadId}/complete` | inline | MediaAsset | 409 The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed … (UploadRefusedProblem) | — |

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Link record**: Links an order, ticket or payment to the case. *(source: contracts/satellite/marketing-crm.yaml#setCaseInvestigationResolution)*
- **Reply or note**: Explicit choice, recipient shown. *(source: F05 step 2)*

**Data it reads**: `getCase` (onLoad, The case with its thread)

**Where the user goes next**

- → `SUP-009` Customer Service Command Center: *Returns to the board's landing screen*; calls `setCaseInvestigationResolution`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The case investigation resolution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the case investigation resolution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No case investigation resolution yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the case investigation resolution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.; 400 Resolving without a resolution note; 400 Validation failed; 409 The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed … (UploadRefusedProblem) |

#### Consistency with other screens

- Match `BO-811`: Same workspace in the back office.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
case: CA-1120 - Charged twice for parking - linked payment PAY-77812 and PAY-77813 (AED 40.00 each)
```

#### Permissions

- `setCaseInvestigationResolution` → `CASE_MANAGE` (configure) · staff
- `getCase` → `CASE_VIEW` (read) · staff, partner
- `addCaseMessage` → `CASE_MANAGE` (configure) · staff, partner
- `updateCase` → `CASE_MANAGE` (configure) · staff, partner
- `createUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `completeUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.3.10 | Case Audit Trail | Marketing & CRM | CONTRACTED | `getCase` |
| 22.3.7 | Agent Notes & Attachments | Marketing & CRM | CONTRACTED | `addCaseMessage` |
| 22.3.4 | Case Workflow Management | Marketing & CRM | CONTRACTED | `updateCase` |
| 23.1.4 | Authorized users shall upload assets individually or in bulk through web interfaces and APIs. | Digital Asset Management | CONTRACTED | `createUpload` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Case creation captures logging channel/source, category and subcategory (e.g. ticket issue > reschedule) and supports screenshot attachments; investigation tracks all activity and actions on the case. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-541)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-013` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS42 Customer Service Board 1.dc.html#sup-013`
- Workshop pack: Customer Service_Reference.pdf board 1
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 8: Works in Case Investigation & Resolution Workspace → Provide the primary workspace in which an agent investigates and resolves a case.

#### Acceptance for the design

- [ ] Every input above is drawn (32), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-013?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Action history, Add message, Save case, Attach file, Confirm attachment.
- [ ] Every transition is wired: `SUP-009`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-014` Order, Booking & Ticket Service Workspace

**Allow customer-service agents to perform permitted ticket/order servicing without entering the underlying technical modules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `ORDER_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/order-booking-ticket-service-workspace-sup-014` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Agents service tickets and orders without entering the technical modules: change date, reschedule, resend tickets, upgrade (group upgrades only where configured, as a request). Every action is first evaluated (what is allowed, the price difference), then performed under the agent's authority.

**Fixed on main** (the package already carries these; draw what it says): The list is bound to setOrderBookingTicket (a write) and there is no order search read. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search order booking ticket | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by order number, ticket number, booking reference, customer, email, mobile and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Principal | picker: choose a principal | — | — | `listOrders` ?principalId |
| Shift | picker: choose a shift | — | — | `listOrders` ?shiftId |
| Status | select | — | Pending · Held · Paid · Partially paid · Completed · Voided · Refunded · Partially refunded · Failed; It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed. | `listOrders` ?status |
| Created from | date and time picker | — | — | `listOrders` ?createdFrom |
| Created to | date and time picker | — | — | `listOrders` ?createdTo |
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |

#### Outputs: what the screen shows and produces

**Shown**

**Orders** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |
| Principal | the name it points at, never the id | The cashier who raised it — what the held-orders list shows. |
| Hold label | text | As `Order.holdLabel`. |
| Held until | 1 Oct 2026, 14:30 | As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Every order booking ticket** (data table, from `setOrderBookingTicket`)

| Shows | Format | Notes |
|---|---|---|
| Order | text | The order number shown to the guest. |
| Customer | text | not in the schema: `Customer` |
| Purchase date | 1 Oct 2026, 14:30 | — |
| Channel | text | The sales channel the order came through. |
| Products | 1,234 | — |
| Tickets | 1,234 | — |
| Event | text | not in the schema: `Event` |
| Date time | 1 Oct 2026, 14:30 | The performance start. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Payment | chip: Paid, Partially paid, Unpaid, Partially refunded, Refunded | — |
| Fulfillment | chip: Pending, Issued, Delivered, Failed | — |
| Ticket status | chip: Valid, Partially used, Used, Expired, Cancelled | — |

**The selected order booking ticket** (detail panel): The pack groups this record's detail under its own headings: “Customer Entitlement”, “Current”, “Available”.

| Shows | Format | Notes |
|---|---|---|
| Order | text | The order number shown to the guest. |
| Customer | text | not in the schema: `Customer` |
| Purchase date | 1 Oct 2026, 14:30 | — |
| Channel | text | The sales channel the order came through. |
| Products | 1,234 | — |
| Tickets | 1,234 | — |
| Event | text | not in the schema: `Event` |
| Date time | 1 Oct 2026, 14:30 | The performance start. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Payment | chip: Paid, Partially paid, Unpaid, Partially refunded, Refunded | — |
| Fulfillment | chip: Pending, Issued, Delivered, Failed | — |
| Ticket status | chip: Valid, Partially used, Used, Expired, Cancelled | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listOrders` (onLoad, Find the guest's order)

**Where the user goes next**

- → `SUP-009` Customer Service Command Center: *Returns to the board's landing screen*; calls `setOrderBookingTicket`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order booking ticket list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order booking ticket untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order booking ticket yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the order booking ticket are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.; 422 The action is not permitted for this order under its policies; the problem names the policy. |

#### Edge cases to draw

- **A group asks to upgrade**: Off by default; where allowed it is a request, not a self-served change. *(source: DI-607)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
action: Resend tickets for ORD-55821 by WhatsApp - allowed
```

#### Permissions

- `setOrderBookingTicket` → `CASE_MANAGE` (configure) · staff
- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.3.7 | The system should allow access to their purchase history and ongoing orders and preferences. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 5.9.4 | The system should be able to provide a detailed log of transactions for each till. Detailed log of transaction should be always accessible, searchable and printable at back office. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 22.2.11 | Ticketing History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.12 | Membership History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.15 | Reservation History | Marketing & CRM | CONTRACTED | `listOrders` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group ticket upgrades are business-configurable (off by default); where allowed a group raises an upgrade request (e.g. via chat/support) rather than self-serving like an individual. *(agreed · MoM 1 Sep 2026, 4.9 Clarified (group upgrades) · DI-607)*
- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-014` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS42 Customer Service Board 1.dc.html#sup-014`
- Workshop pack: Customer Service_Reference.pdf board 1
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 10: Works in Order, Booking & Ticket Service Workspace → Allow customer-service agents to perform permitted ticket/order servicing without entering the underlying technical modules.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (37 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-014?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `SUP-009`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-015` Refund, Compensation & Service Exception Workspace

**Manage cases requiring money, compensation, goodwill or policy exceptions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_REFUND` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/refund-compensation-service-exception-workspace-sup-015` |

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Full Refund, Partial Refund, Wallet Credit, Voucher, Complimentary Ticket, Fee Waiver, Policy Exception. …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Cases involving money, compensation or exceptions: full or partial refund, service or wallet credit, voucher, complimentary ticket, fee waiver, policy exception. Each is a request routed for approval; no money moves here. Approved refunds go to the original payment method or the guest's wallet.

**Known correction pending (do not draw the wrong version)**

- **The list is bound to setRefundCompensationService (a write); no list read.** Why: Add a read of the requests. *(source: contracts/satellite/marketing-crm.yaml#setRefundCompensationService; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every refund compensation service** (data table, from `setRefundCompensationService`)

| Shows | Format | Notes |
|---|---|---|
| Original transaction | text | The order number. |
| Amount paid | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Amount used | AED 1,234.50 | Value of tickets already scanned or consumed. |
| Refundable amount | AED 1,234.50 | What the refund policy's time bands allow now, less previous refunds. |
| Previous refund | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Fees | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Proposed refund | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Proposed compensation | grouped details | — |

**The selected refund compensation service** (detail panel): The pack groups this record's detail under its own headings: “Requested Exception”, “Up to AED 200”, “Above AED 1,000”, “Compensation Budget”.

| Shows | Format | Notes |
|---|---|---|
| Original transaction | text | The order number. |
| Amount paid | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Amount used | AED 1,234.50 | Value of tickets already scanned or consumed. |
| Refundable amount | AED 1,234.50 | What the refund policy's time bands allow now, less previous refunds. |
| Previous refund | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Fees | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Proposed refund | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Proposed compensation | grouped details | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Full Refund (primary button) | navigation or local | — | — | — | — |
| Partial Refund (secondary button) | navigation or local | — | — | — | — |
| Service Credit (secondary button) | navigation or local | — | — | — | — |
| Wallet Credit (secondary button) | navigation or local | — | — | — | — |
| Voucher (secondary button) | navigation or local | — | — | — | — |
| Complimentary Ticket (secondary button) | navigation or local | — | — | — | — |
| Fee Waiver (secondary button) | navigation or local | — | — | — | — |
| Policy Exception (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Request status**: Draft, submitted, approved, rejected, paid; editable only in draft. *(source: contracts/satellite/marketing-crm.yaml#setRefundCompensationService; DI-673)*

**Where the user goes next**

- → `SUP-009` Customer Service Command Center: *Returns to the board's landing screen*; calls `setRefundCompensationService`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The refund compensation service list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the refund compensation service untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No refund compensation service yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the refund compensation service are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The request is no longer a draft, or the amount exceeds what remains refundable (`exceedsRefundable`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
request: Partial refund AED 40.00 - duplicate parking charge - submitted 1 Oct 2026 - awaiting Finance
```

#### Permissions

- `setRefundCompensationService` → `ORDER_REFUND` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approved refunds go back to the original payment method or are credited to the guest's wallet for future purchases. *(client request · MoM 7 Sep 2026, 4.11 Entitlements Usage, Upgrades & Refund/Credit Recovery · DI-673)*
- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A75** Design the refund engine: a six-step ledger-to-gateway refund flow with configurable time-banded percentages, an authorized-approver override, partial refunds, both operations- and customer-initiated requests, plus bulk … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 12 Aug 2026 · workshop tracker · keyword 'refund')*
- **A80** Implement a currency-locking rule for refunds/change: always issue in the local/base currency, locked at the value recorded at time of purchase; track foreign-currency activity only via a separate report *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 14 Aug 2026 · workshop tracker · keyword 'refund')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'refund')*
- **A140** Centralise policy management (reschedule, exchange, refund, cancellation, upgrade, downgrade, ownership transfer, membership conversion) with each product mapped to pricing, GL code, promotions and channels *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'refund')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'refund')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'refund')*

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-015` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS42 Customer Service Board 1.dc.html#sup-015`
- Workshop pack: Customer Service_Reference.pdf board 1
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 12: Works in Refund, Compensation & Service Exception Workspace → Manage cases requiring money, compensation, goodwill or policy exceptions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Full Refund, Partial Refund, Service Credit, Wallet Credit, Voucher, Complimentary Ticket, Fee Waiver, Policy Exception.
- [ ] Every transition is wired: `SUP-009`.
- [ ] Every gated control is gated: `ORDER_REFUND`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-016` Escalation, Collaboration & Internal Resolution

**Allow Customer Service to collaborate with other TICVAI departments without losing ownership of the customer case.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/support/escalation-collaboration-internal-resolution-sup-016` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-007): No operation raises an internal collaboration request on a case.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Customer service asks another department for work (Finance confirm a refund, Operations check a ride incident) while staying the guest-facing owner. The other department sees the request on its own app.

**Known correction pending (do not draw the wrong version)**

- **Only a read is declared; no operation raises an internal request.** Why: The collaboration cannot be started. *(source: contracts/satellite/marketing-crm.yaml#listEscalationCollaborationInternal; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Department | select field | — | — | — | — | — | — |
| Assignee | select field | — | — | — | — | — | — |
| Request | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Due Date | select field | — | — | — | — | — | — |
| Related Case | select field | — | — | — | — | — | — |
| Related Transaction | select field | — | — | — | — | — | — |
| Attachments | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Case | picker: choose a case | — | — | `listEscalationCollaborationInternal` ?caseId |
| Department | select | — | Ticketing · Finance · Operations · Access control · Membership · Crm · Fnb · Retail · Group sales · Technical support · Venue management · Management | `listEscalationCollaborationInternal` ?department |
| Assignee principal | picker: choose an assignee principal | — | — | `listEscalationCollaborationInternal` ?assigneePrincipalId |
| Status | radio group | — | Open · In progress · Completed · Cancelled | `listEscalationCollaborationInternal` ?status |
| Escalation type | select | — | Functional · Supervisor · Management · Technical · Financial · Emergency event day | `listEscalationCollaborationInternal` ?escalationType |
| Overdue only | toggle | — | — | `listEscalationCollaborationInternal` ?overdueOnly |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Request**: Department, assignee, what is needed, priority, due date, related case and transaction. *(source: contracts/satellite/marketing-crm.yaml#listEscalationCollaborationInternal; DI-542)*

#### Outputs: what the screen shows and produces

**Data it reads**: `listEscalationCollaborationInternal` (onLoad, Escalation, Collaboration & Internal Resolution)

**Where the user goes next**

- → `SUP-009` Customer Service Command Center: *Returns to the board's landing screen*; calls `listEscalationCollaborationInternal`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The escalation collaboration internal configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the escalation collaboration internal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No escalation collaboration internal configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
request: Finance - confirm refund of duplicate charge PAY-77813 - due 2 Oct 2026 12:00
```

#### Permissions

- `listEscalationCollaborationInternal` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-016` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS42 Customer Service Board 1.dc.html#sup-016`
- Workshop pack: Customer Service_Reference.pdf board 1
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 14: Works in Escalation, Collaboration & Internal Resolution → Allow Customer Service to collaborate with other TICVAI departments without losing ownership of the customer case.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-016?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SUP-009`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-017` Case Resolution, Closure & Customer Feedback

**Govern how cases are resolved and formally closed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Where configured, send) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `caseId` (navigation) |
| Route | `/support/case-resolution-closure-customer-feedback-sup-017` |

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Resolution and formal closure: resolution category, summary, action taken, financial impact, compensation, root cause, customer notification and the CSAT survey. The AI summariser compiles every action for review.

**Fixed on main** (the package already carries these; draw what it says): Read-only; closing a case (updateCase with a resolution note) is not declared. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Resolution Category | select field | — | — | — | — | — | — |
| Resolution Summary | select field | — | — | — | — | — | — |
| Action Taken | select field | — | — | — | — | — | — |
| Financial Impact | select field | — | — | — | — | — | — |
| Compensation | select field | — | — | — | — | — | — |
| Root Cause | select field | — | — | — | — | — | — |
| Resolved By | select field | — | — | — | — | — | — |
| Resolution Date | select field | — | — | — | — | — | — |
| Customer Notification | select field | — | — | — | — | — | — |
| Customer | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Payment | select field | — | — | — | — | — | — |
| System | select field | — | — | — | — | — | — |
| Integration | select field | — | — | — | — | — | — |
| Operational | select field | — | — | — | — | — | — |
| Content | select field | — | — | — | — | — | — |
| Policy | select field | — | — | — | — | — | — |
| Staff | select field | — | — | — | — | — | — |
| Unknown | select field | — | — | — | — | — | — |
| CSAT survey | select field | — | — | — | — | — | — |
| Service rating | select field | — | — | — | — | — | — |
| Feedback request | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Case | picker: choose a case | — | — | `listCaseResolutionClosure` ?caseId |
| Resolution category | select | — | Information provided · Ticket reissued · Booking changed · Refund processed · Compensation issued · Technical issue resolved · Customer error · Policy applied · Duplicate · No action required · Other | `listCaseResolutionClosure` ?resolutionCategory |
| Root cause | select | — | Customer · Product · Payment · System · Integration · Operational · Content · Policy · Staff · Unknown | `listCaseResolutionClosure` ?rootCause |
| Can close | toggle | — | — | `listCaseResolutionClosure` ?canClose |
| From | date and time picker | — | — | `listCaseResolutionClosure` ?from |
| To | date and time picker | — | — | `listCaseResolutionClosure` ?to |

**Form: Close case** (modal, opened by *Close case*; *Close case* calls `updateCase`, *Cancel* sends nothing)

**Collects what `updateCase` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | optional | — | Open · In progress · Awaiting guest · Escalated · Resolved · Closed | — | — | `updateCase` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent | — | — | `updateCase` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `updateCase` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateCase` body |
| Resolution note `resolutionNote` | text area | optional | — | max length 2000 | — | — | `updateCase` body |

Errors to draw in the form: 400 Resolving without a resolution note

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Close case (secondary button) | `updateCase` PATCH `/cases/{caseId}` | inline | Case | 400 Resolving without a resolution note | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Closure checks**: Customer notified, resolution note present, compensation settled; closure blocked until they pass. *(source: contracts/satellite/marketing-crm.yaml#listCaseResolutionClosure; F70 step 4)*

**Data it reads**: `listCaseResolutionClosure` (onLoad, Case Resolution, Closure & Customer Feedback)

**Where the user goes next**

- → `SUP-009` Customer Service Command Center: *Returns to the board's landing screen*; calls `listCaseResolutionClosure`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The case resolution closure configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the case resolution closure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No case resolution closure configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Resolving without a resolution note |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
resolution: Root cause Payment - duplicate charge refunded AED 40.00 - customer notified by WhatsApp - CSAT sent
```

#### Permissions

- `listCaseResolutionClosure` → `CASE_VIEW` (read) · staff
- `updateCase` → `CASE_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.3.4 | Case Workflow Management | Marketing & CRM | CONTRACTED | `updateCase` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- On resolution the agent logs the outcome; an AI customer-service summariser compiles all actions taken on the case for quick review. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-543)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-017` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS42 Customer Service Board 1.dc.html#sup-017`
- Workshop pack: Customer Service_Reference.pdf board 1
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 16: Works in Case Resolution, Closure & Customer Feedback → Govern how cases are resolved and formally closed.

#### Acceptance for the design

- [ ] Every input above is drawn (27), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-017?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Close case.
- [ ] Every transition is wired: `SUP-009`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-018` AI Customer Service Copilot & Knowledge Workspace

**Configure the agent copilot and the assistant profile it answers with.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_CONFIGURE`, `AI_USE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `profileKey` (navigation) |
| Route | `/support/ai-customer-service-copilot-knowledge-workspace-sup-018` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Review → Execute. Each needs an operation, or needs removing from the screen; this is the Phase 3 … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Configuration of the customer-service copilot that works beside agents: which authorised data it may read (customer, orders, cases), which knowledge collections, which channels it may draft replies for, the brand tone, whether to reply in the customer's language, and whether anything may be sent without an agent (off by default). A venue can narrow the tenant's settings, never widen them. The one thing to get right: the copilot drafts and summarises (the case summariser compiles every action taken on the case); an agent sends.

**Known correction pending (do not draw the wrong version)**

- **requiresModule marketing.** Why: The copilot is an AI capability; it needs the AI module as well. *(source: contracts/satellite/ai.yaml#configureAssistantProfile; AI & Intelligence)*

**Fixed on main** (the package already carries these; draw what it says): purpose is a pasted board description; layout is a "Review → Execute" button and Cancel. (CHG-WIR-013).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Audience | segmented control | — | Staff · Guest · Support | `listAssistantProfiles` ?audience |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **autoSend**: Off by default and visibly risky; turning it on needs a confirmation naming the channels. *(source: contracts/satellite/marketing-crm.yaml#setCustomerServiceCopilot / ADR-0050)*
- **dataSources / draftChannels / knowledgeCollectionIds**: Checklists showing the tenant's allowed values; a venue cannot add one the tenant does not allow (422). *(source: contracts/satellite/marketing-crm.yaml#setCustomerServiceCopilot)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Review → Execute (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **preview**: A sample case with the copilot's draft reply and case summary, labelled as AI-drafted. *(source: DI-543 / designer default)*

**Data it reads**: `listAssistantProfiles` (onLoad, Assistant profiles)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer service copilot list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer service copilot untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer service copilot yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer service copilot are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A venue row would widen the tenant's configuration or the AI policy. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
copilot:
  dataSources:
  - customer profile
  - orders
  - cases
  channels:
  - email
  - whatsapp
  tone: Warm, concise
  replyInCustomerLanguage: true
  autoSend: false
summary: Guest Omar Haddad asked to move a cabana booking (BK-48213) from Sat to Sun; agent moved it, fee waived
  as goodwill, confirmation sent.
```

#### Permissions

- `setCustomerServiceCopilot` → `AI_CONFIGURE` (configure) · staff
- `configureAssistantProfile` → `AI_CONFIGURE` (configure) · staff
- `listAssistantProfiles` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The AI assistant answers natural-language business queries (e.g. "what was yesterday's ticketing revenue?") only within the user's role (a CEO sees full revenue, a cashier does not), shows grounded citations naming the policy or document an answer came from, and keeps conversation context ("compare that to this week"). *(client request · MoM 21 Sep 2026, 4.8 Core AI Platform — AI Assistant (Query & Knowledge) · DI-964)*
- On resolution the agent logs the outcome; an AI customer-service summariser compiles all actions taken on the case for quick review. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-543)*

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-018` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS42 Customer Service Board 1.dc.html#sup-018`
- Workshop pack: Customer Service_Reference.pdf board 1
- Flow F134 *Customer Service board 1: Customer Service Command Center*, step 18: Works in AI Customer Service Copilot & Knowledge Workspace → Create the AI intelligence layer assisting agents throughout the service journey. This should not be a simple chatbot added to the side of the screen. It should understand the customer + transaction …
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Review → Execute, Cancel.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P12 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for operator density.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P12 Venue Support

- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Client support staff log into TICVAI to view and respond to their own tickets/chats (keeps a full audit trail); adapters to clients' own support systems are phase two. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-257)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

**18 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addCaseMessage": {"method":"POST","path":"/cases/{caseId}/messages","contract":"marketing-crm","summary":"Add a message or internal note","permission":"CASE_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CaseMessage"},
"completeUpload": {"method":"POST","path":"/media/uploads/{uploadId}/complete","contract":"assets","summary":"Confirm an upload and create the asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaAsset"},
"configureAssistantProfile": {"method":"PUT","path":"/assistant-profiles/{profileKey}","contract":"ai","summary":"Define an assistant profile","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiAssistantProfile","responds":"AiAssistantProfile"},
"createCase": {"method":"POST","path":"/cases","contract":"marketing-crm","summary":"Raise a service case","permission":"CASE_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCaseRequest","responds":"Case"},
"createCaseClassificationIntelligent": {"method":"POST","path":"/case-classification-intelligent","contract":"marketing-crm","summary":"Case Creation, Classification & Intelligent Routing","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CaseCreationClassificationIntelligentRoutingInput","responds":"CaseCreationClassificationIntelligentRoutingView"},
"createUpload": {"method":"POST","path":"/media/uploads","contract":"assets","summary":"Request a signed upload URL","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"UploadTicket"},
"getCase": {"method":"GET","path":"/cases/{caseId}","contract":"marketing-crm","summary":"Read a case with its thread","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CaseDetail"},
"listAssistantProfiles": {"method":"GET","path":"/assistant-profiles","contract":"ai","summary":"Assistant profiles","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"audience","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCaseCategories": {"method":"GET","path":"/case-categories","contract":"marketing-crm","summary":"List case categories and subcategories","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"parentCategoryId","in":"query","required":false},{"name":"topLevelOnly","in":"query","required":false},{"name":"isActive","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCaseResolutionClosure": {"method":"GET","path":"/case-resolution-closure","contract":"marketing-crm","summary":"Case Resolution, Closure & Customer Feedback","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"caseId","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"resolutionCategory","in":"query","required":false},{"name":"rootCause","in":"query","required":false},{"name":"canClose","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCustomerService": {"method":"GET","path":"/customer-service","contract":"marketing-crm","summary":"Customer Service Command Center","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"agentPrincipalId","in":"query","required":false},{"name":"venueId","in":"query","required":false}],"requestBody":null,"responds":"CustomerServiceCommandCenterView"},
"listCustomerServiceProfile": {"method":"GET","path":"/customer-service-profile","contract":"marketing-crm","summary":"Customer 360° Service Profile","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"subjectId","in":"query","required":true}],"requestBody":null,"responds":"Customer360ServiceProfileView"},
"listEscalationCollaborationInternal": {"method":"GET","path":"/escalation-collaboration-internal","contract":"marketing-crm","summary":"Escalation, Collaboration & Internal Resolution","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"caseId","in":"query","required":false},{"name":"department","in":"query","required":false},{"name":"assigneePrincipalId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"escalationType","in":"query","required":false},{"name":"overdueOnly","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrders": {"method":"GET","path":"/orders","contract":"orders","summary":"List orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"createdFrom","in":"query","required":null},{"name":"createdTo","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"tender","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listUnifiedInteractionCommunication": {"method":"GET","path":"/unified-interaction-communication","contract":"marketing-crm","summary":"Unified Interaction & Communication History","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"subjectId","in":"query","required":false},{"name":"keyword","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"agentPrincipalId","in":"query","required":false},{"name":"caseId","in":"query","required":false},{"name":"orderId","in":"query","required":false},{"name":"ticketId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setCaseInvestigationResolution": {"method":"PUT","path":"/case-investigation-resolution","contract":"marketing-crm","summary":"Link a record to a case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CaseInvestigationResolutionWorkspaceInput","responds":"CaseInvestigationResolutionWorkspaceView"},
"setCustomerServiceCopilot": {"method":"PUT","path":"/customer-service-copilot","contract":"marketing-crm","summary":"Configure the customer-service copilot","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiCustomerServiceCopilotKnowledgeWorkspaceInput","responds":"AiCustomerServiceCopilotKnowledgeWorkspaceView"},
"setOrderBookingTicket": {"method":"PUT","path":"/order-booking-ticket","contract":"marketing-crm","summary":"Evaluate or perform a service action on an order from a case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OrderBookingTicketServiceWorkspaceInput","responds":"OrderBookingTicketServiceWorkspaceView"},
"setRefundCompensationService": {"method":"PUT","path":"/refund-compensation-service","contract":"marketing-crm","summary":"Raise or change a refund, compensation or policy-exception request on a case","permission":"ORDER_REFUND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RefundCompensationServiceExceptionWorkspaceInput","responds":"RefundCompensationServiceExceptionWorkspaceView"},
"updateCase": {"method":"PATCH","path":"/cases/{caseId}","contract":"marketing-crm","summary":"Assign, reprioritise or resolve a case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Case"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAssistantProfile": {"type":"object","x-ticvai-persistence":"ai.assistant_profile","description":"**One assistant runtime, many profiles** (design 5.10, C5; AIC-069..080). The profile decides the audience, roles, knowledge sources, tools, model task and guest scope: guest concierge, support chatbot and staff assistants by role.","required":["profileKey","audience"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"profileKey":{"type":"string"},"name":{"type":"string"},"audience":{"type":"string","enum":["staff","guest","support"]},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"module":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"}],"nullable":true},"collectionIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Knowledge collections it retrieves from."},"toolKeys":{"type":"array","items":{"type":"string"},"description":"Registered tools it may propose (an assistant only reads; a change request goes to the configuration assistant, AIC-078)."},"modelTask":{"type":"string","description":"The gateway task, e.g. `assistant.staff.answer`. The visit planner agent (29 September, MOB-6) is profile `planner.guest` with task `planner.guest.refine` and the five `venue-map` visit-plan tools. The app publishing guide (M24-08) is profile `guide.appPublishing` with task `assistant.staff.answer`, grounded on the platform's store-publishing collection only."},"guestCapabilityScope":{"type":"array","items":{"type":"string"},"description":"For a guest profile: the same values as `AiPolicy.guestCapabilityScope`, narrowed."},"locales":{"type":"array","items":{"type":"string"}},"handoverTarget":{"type":"string","nullable":true,"description":"Where \"ask a person\" goes: a support queue or a staff role."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiCustomerServiceCopilotKnowledgeWorkspaceInput": {"type":"object","x-ticvai-persistence":"marketing.service_copilot_config","description":"The customer-service copilot's configuration for one scope (pack 10.1.10). A field left out takes its default, not its old value.","required":["scopeLevel","dataSources","draftChannels"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopeLevel":{"type":"string","enum":["tenant","venue"]},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005), and the upsert key: one row per scope."},"isEnabled":{"type":"boolean","default":false},"dataSources":{"type":"array","description":"The authorised data the copilot may read, always within the asking agent's own permissions.","items":{"type":"string","enum":["customer","cases","orders","tickets","products","servicePolicies","pricing","payments","membership","wallet","groupBookings","interactionHistory","knowledgeBase"]}},"knowledgeCollectionIds":{"type":"array","description":"`ai.knowledge_collection` rows holding service procedures, product information, refund rules, ticket policies, venue instructions, FAQs and internal SOPs.","items":{"type":"string","format":"uuid"}},"draftChannels":{"type":"array","items":{"type":"string","enum":["email","chat","whatsapp","caseResponse","internalEscalation"]}},"brandTone":{"type":"string","maxLength":1000,"nullable":true,"description":"Tone guidance applied to every draft."},"replyInCustomerLanguage":{"type":"boolean","default":true},"autoSend":{"type":"array","default":[],"description":"Channels where an approved automation may send without an agent. Empty means every customer-facing message waits for a person.","items":{"type":"string","enum":["email","chat","whatsapp"]}},"patternDetection":{"type":"object","description":"Flags a systemic problem when many cases share one cause.","properties":{"isEnabled":{"type":"boolean","default":true},"minimumCases":{"type":"integer","minimum":2,"default":25},"windowHours":{"type":"integer","minimum":1,"maximum":720,"default":168}}},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AiCustomerServiceCopilotKnowledgeWorkspaceView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.service_copilot_config (new), ai.policy and ai.knowledge_collection","description":"The stored configuration and what is in effect at that scope after the tenant row and the AI policy are applied.","required":["configuration","effective"],"properties":{"configuration":{"$ref":"#/components/schemas/AiCustomerServiceCopilotKnowledgeWorkspaceInput"},"effective":{"type":"object","description":"The narrowest of this row, its tenant row and `getAiPolicy`.","properties":{"isEnabled":{"type":"boolean"},"dataSources":{"type":"array","items":{"type":"string"}},"draftChannels":{"type":"array","items":{"type":"string"}},"autoSend":{"type":"array","items":{"type":"string"}},"aiCapabilities":{"type":"array","description":"`AiPolicy.enabledCapabilities` at this scope.","items":{"type":"string"}}}},"knowledgeCollections":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"documentCount":{"type":"integer","minimum":0}}}}}},
"Case": {"x-ticvai-persistence":"marketing.case","x-ticvai-retired-columns":["guest_name","subject","is_sla_breached"],"type":"object","required":["id","caseNumber","subject","status","priority","createdAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."},"caseNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"},"subject":{"type":"string","x-ticvai-column":"title","description":"**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"},"kind":{"allOf":[{"$ref":"#/components/schemas/CaseKind"}],"nullable":true,"description":"What the guest said it was about, where the guest raised it."},"channel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"description":"How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised — the start of the SLA clock."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the case arrived. Equal to `recordedAt` for a case raised online."},"categoryId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"},"status":{"$ref":"#/components/schemas/CaseStatus"},"priority":{"$ref":"#/components/schemas/CasePriority"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"relatedOrderId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"isSlaBreached":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"},"slaPausedSeconds":{"type":"integer","description":"Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"},"escalationCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"CaseCategory": {"type":"object","x-ticvai-persistence":"marketing.case_category","description":"**The venue's case taxonomy**: categories and, under them, subcategories (`parentCategoryId`). `Case.categoryId` and the routing rules' `match.categoryIds` point here; `createCaseClassificationIntelligent` recommends one. Maintained by `setCaseCategoryDefinition`, read by `listCaseCategories` (decided 29 September, writers pass). (decided 29 September, data model for the agreed operations)\n","required":["id","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":60},"name":{"type":"string","maxLength":150},"parentCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Set on a subcategory; null on a top-level category."},"defaultPriority":{"allOf":[{"$ref":"#/components/schemas/CasePriority"}],"nullable":true,"description":"The priority a case in this category starts at before routing factors apply."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CaseCreationClassificationIntelligentRoutingInput": {"type":"object","x-ticvai-persistence":"none — request only; the case itself is raised with `createCase`","description":"The case as the agent has captured it so far (pack 10.1.4 Case Creation). Every field maps onto `CreateCaseRequest` or onto a linked record.","required":["subject","description","channel"],"properties":{"subjectId":{"type":"string","format":"uuid","description":"The customer."},"subject":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":10000},"channel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"description":"The source, as on `CreateCaseRequest.channel`."},"kind":{"$ref":"#/components/schemas/CaseKind"},"categoryId":{"type":"string","format":"uuid","description":"Where the agent has already chosen one."},"subcategoryId":{"type":"string","format":"uuid"},"customerSelectedPriority":{"$ref":"#/components/schemas/CasePriority"},"venueId":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid"},"language":{"type":"string","maxLength":10},"relatedRecords":{"type":"array","maxItems":20,"items":{"type":"object","required":["kind","referenceId"],"properties":{"kind":{"type":"string","enum":["order","ticket","payment","refund","membership","walletTransaction","groupBooking","accessEvent"]},"referenceId":{"type":"string"}}}},"attachmentRefs":{"type":"array","items":{"type":"string"}}}},
"CaseCreationClassificationIntelligentRoutingView": {"type":"object","x-ticvai-persistence":"none — computed from marketing.case, marketing.sla_policy, marketing.agent_availability, marketing.case_category (new) and the routing rules; nothing is stored","description":"The recommendation for one case. Every recommended value names why.","required":["recommendedPriority","routingFactors","duplicateCandidates"],"properties":{"recommendedCategoryId":{"type":"string","format":"uuid","nullable":true},"recommendedSubcategoryId":{"type":"string","format":"uuid","nullable":true},"recommendedPriority":{"$ref":"#/components/schemas/CasePriority"},"priorityBasis":{"type":"array","items":{"type":"string","enum":["customerSelected","businessRule","slaPolicy","aiAssessment"]}},"recommendedQueue":{"type":"string","nullable":true,"description":"The queue's code, e.g. `eventDaySupport`."},"recommendedAssigneePrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The preview; null when nobody with the skill is available."},"slaPolicyCode":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"routingFactors":{"type":"array","items":{"type":"object","required":["factor"],"properties":{"factor":{"type":"string","enum":["category","venue","product","language","customerType","agentSkill","workload","priority","eventProximity"]},"value":{"type":"string"}}}},"aiAssessment":{"type":"object","nullable":true,"description":"Where the AI policy enables `assist`; AI-derived and labelled as such.","properties":{"signals":{"type":"array","items":{"type":"string","maxLength":80},"description":"e.g. ticket issue, upcoming event, high urgency."},"explanation":{"type":"string","maxLength":1000}}},"duplicateCandidates":{"type":"array","maxItems":10,"description":"Open cases for the same customer and related records, best match first.","items":{"type":"object","required":["caseId","caseNumber","status"],"properties":{"caseId":{"type":"string","format":"uuid"},"caseNumber":{"type":"string"},"subject":{"type":"string"},"status":{"$ref":"#/components/schemas/CaseStatus"},"matchedOn":{"type":"array","items":{"type":"string","enum":["customer","relatedRecord","subjectText"]}}}}}}},
"CaseDetail": {"x-ticvai-persistence":"marketing.case","allOf":[{"$ref":"#/components/schemas/Case"},{"type":"object","properties":{"description":{"type":"string"},"resolutionNote":{"type":"string","nullable":true},"messages":{"type":"array","items":{"$ref":"#/components/schemas/CaseMessage"}}}}]},
"CaseInvestigationResolutionWorkspaceInput": {"type":"object","x-ticvai-persistence":"marketing.case_linked_record","x-ticvai-record-definition":"Related Records (agents can attach)","description":"One link between a case and a record another contract owns. The reference is a pointer, never a copy.","required":["caseId","kind","referenceId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"caseId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["order","ticket","payment","refund","membership","walletTransaction","groupBooking","accessEvent"]},"referenceId":{"type":"string","maxLength":64,"description":"The record's id in its owning contract (orders, payments, access, wallet)."},"note":{"type":"string","maxLength":500,"nullable":true},"isActive":{"type":"boolean","default":true,"description":"False unlinks; the row stays for the audit trail."},"linkedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CaseInvestigationResolutionWorkspaceView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.case, marketing.case_message, marketing.case_linked_record (new), marketing.sla_policy and ai.suggestion","description":"The case workspace (pack 10.1.5). Recommended actions and the summary keep verified data, policy and AI recommendation apart.","required":["caseId","caseNumber","subject","priority","status","created","lastUpdated","linkedRecords","recommendedActions"],"properties":{"caseId":{"type":"string","format":"uuid"},"caseNumber":{"type":"string"},"subjectId":{"type":"string","format":"uuid","nullable":true},"customer":{"type":"string","nullable":true,"description":"The guest's name, as `Case.guestName`; null unless the caller holds GUEST_VIEW_PII."},"subject":{"type":"string"},"categoryId":{"type":"string","format":"uuid","nullable":true},"category":{"type":"string","nullable":true,"description":"The category's display name."},"priority":{"$ref":"#/components/schemas/CasePriority"},"status":{"$ref":"#/components/schemas/CaseStatus"},"sla":{"type":"object","properties":{"policyCode":{"type":"string","nullable":true},"dueAt":{"type":"string","format":"date-time","nullable":true},"remainingSeconds":{"type":"integer","nullable":true,"description":"Negative once breached."},"isBreached":{"type":"boolean"},"isPaused":{"type":"boolean","description":"True while `awaitingGuest`."}}},"owner":{"type":"string","format":"uuid","nullable":true,"description":"The assigned agent's principal id (`Case.assignedToPrincipalId`)."},"queue":{"type":"string","nullable":true},"created":{"type":"string","format":"date-time","description":"`Case.createdAt`."},"lastUpdated":{"type":"string","format":"date-time"},"linkedRecords":{"type":"array","description":"Active links, newest first.","items":{"$ref":"#/components/schemas/CaseInvestigationResolutionWorkspaceInput"}},"recommendedActions":{"type":"array","maxItems":10,"items":{"type":"object","required":["action","basis"],"properties":{"action":{"type":"string","enum":["reply","call","reschedule","exchange","reissue","requestRefund","requestCompensation","raiseInternalRequest","escalate","resolve"]},"basis":{"type":"string","enum":["verifiedData","policy","aiRecommendation"]},"reason":{"type":"string","maxLength":500},"policyReference":{"type":"string","nullable":true,"description":"The policy the action rests on; an AI recommendation never invents one."}}}},"aiSummary":{"type":"object","nullable":true,"description":"Where the AI policy enables `summarise`; AI-derived and labelled as such.","properties":{"issue":{"type":"string"},"policy":{"type":"string","nullable":true},"currentStatus":{"type":"string","nullable":true},"commercialImpact":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"recommendedAction":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"}}}}},
"CaseKind": {"type":"string","description":"**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n","enum":["lostProperty","complaint","question","accessibility","refundRequest","other"]},
"CaseMessage": {"x-ticvai-persistence":"marketing.case_message","type":"object","required":["id","body","isInternal","authorKind","recordedAt"],"properties":{"resolution":{"type":"string","description":"**What was actually done about it.** Indexed for retrieval: an agent facing a complaint benefits more from how the last one was resolved than from a policy. Without this column `marketing.case` can only embed its subject line.\n"},"id":{"type":"string"},"body":{"type":"string"},"isInternal":{"type":"boolean"},"authorKind":{"type":"string","enum":["agent","guest","system","ai"]},"authorPrincipalId":{"type":"string","format":"uuid","nullable":true},"channel":{"$ref":"#/components/schemas/MessageChannel"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time","description":"Device time — `addCaseMessage` is offline-capable."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the message arrived."}}},
"CasePriority": {"type":"string","enum":["low","normal","high","urgent"]},
"CaseResolutionClosureCustomerFeedbackView": {"type":"object","x-ticvai-persistence":"marketing.case_resolution","description":"One case's resolution record (pack 10.1.9), with closure checks, feedback and reopen history computed on read from marketing.case, marketing.case_message, marketing.case_internal_request, marketing.case_compensation_request, approvals.request and marketing.form_submission.","required":["caseId","resolutionCategory","resolutionSummary","rootCause"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"caseId":{"type":"string","format":"uuid"},"caseNumber":{"type":"string","readOnly":true,"x-ticvai-persisted":false},"caseStatus":{"allOf":[{"$ref":"#/components/schemas/CaseStatus"}],"readOnly":true,"x-ticvai-persisted":false},"resolutionCategory":{"type":"string","enum":["informationProvided","ticketReissued","bookingChanged","refundProcessed","compensationIssued","technicalIssueResolved","customerError","policyApplied","duplicate","noActionRequired","other"]},"resolutionSummary":{"type":"string","minLength":3,"maxLength":2000},"actionTaken":{"type":"string","maxLength":2000,"nullable":true},"financialImpact":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net money refunded or credited; zero when none."},"compensationRequestIds":{"type":"array","description":"The case's compensation requests (`setRefundCompensationService`) this resolution relied on.","items":{"type":"string","format":"uuid"}},"rootCause":{"type":"string","enum":["customer","product","payment","system","integration","operational","content","policy","staff","unknown"]},"duplicateOfCaseId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `resolutionCategory` is `duplicate`."},"customerNotification":{"type":"object","nullable":true,"description":"How the customer was told; the message itself is a `CaseMessage` or a `MessageDispatch`.","properties":{"channel":{"$ref":"#/components/schemas/MessageChannel"},"messageId":{"type":"string","nullable":true},"sentAt":{"type":"string","format":"date-time","nullable":true}}},"resolvedBy":{"type":"string","format":"uuid","readOnly":true,"description":"The principal who recorded it."},"resolutionDate":{"type":"string","format":"date-time","readOnly":true},"closureChecks":{"type":"object","readOnly":true,"x-ticvai-persisted":false,"properties":{"requiredCustomerResponseSent":{"type":"boolean"},"financialActionCompleteOrTracked":{"type":"boolean"},"internalTasksCompleted":{"type":"boolean"},"requiredApprovalsComplete":{"type":"boolean"},"resolutionDocumented":{"type":"boolean"}}},"canClose":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false},"feedback":{"type":"object","readOnly":true,"nullable":true,"x-ticvai-persisted":false,"description":"Null where no survey is configured for case resolution.","properties":{"surveyStatus":{"type":"string","enum":["scheduled","sent","responded","expired"]},"formSubmissionId":{"type":"string","format":"uuid","nullable":true},"score":{"type":"number","nullable":true},"scaleMax":{"type":"integer","nullable":true},"respondedAt":{"type":"string","format":"date-time","nullable":true}}},"reopenCount":{"type":"integer","minimum":0,"readOnly":true,"x-ticvai-persisted":false},"lastReopenReason":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"`reopenCase`'s reason; `refundFailed` when the system reopened it after a refund failed."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CaseStatus": {"type":"string","enum":["open","inProgress","awaitingGuest","escalated","resolved","closed"]},
"ConsentDecision": {"type":"string","enum":["granted","withdrawn","notAsked"]},
"CreateCaseRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","subject","description","channel","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"subject":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":10000},"categoryId":{"type":"string","format":"uuid"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. Must belong to `subjectId` when both are given (422). (decided 29 September, coordinator decision DM4, writers pass)"},"priority":{"allOf":[{"$ref":"#/components/schemas/CasePriority"}],"default":"normal"},"kind":{"$ref":"#/components/schemas/CaseKind"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"venueId":{"type":"string","format":"uuid"},"relatedOrderId":{"type":"string"},"attachmentRefs":{"type":"array","description":"Stored on the opening `CaseMessage`, not on the case.","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised. The server stamps `Case.syncedAt` on arrival."}}},
"Customer360ServiceProfileView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.guest_profile, pii.subject, pii.subject_contact, marketing.loyalty_position, marketing.guest_preference, marketing.consent_record, marketing.suppression, marketing.case, orders.sales_order, orders.reservation, orders.group_booking, access.entitlement and wallet.balance","description":"The service view of one guest. Fields the caller may not see are null, never omitted.","required":["customerId","customerSince","openCases","serviceAlerts"],"properties":{"customerId":{"type":"string","format":"uuid","description":"The guest's `subjectId`."},"customerName":{"type":"string","nullable":true,"description":"Null unless the caller holds GUEST_VIEW_PII."},"customerType":{"type":"string","enum":["individual","member","groupOrganiser","corporate","partner"]},"membershipStatus":{"type":"string","enum":["none","active","expiring","lapsed"]},"loyaltyTier":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","maxLength":10,"nullable":true},"country":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"contactDetails":{"type":"object","description":"Masked (e.g. `j***@example.com`, `+971 ** *** 4821`) unless the caller holds GUEST_VIEW_PII.","properties":{"email":{"type":"string","nullable":true},"phone":{"type":"string","nullable":true}}},"customerSince":{"type":"string","format":"date-time"},"customerValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Lifetime net spend across the tenant."},"openCases":{"type":"integer","minimum":0},"riskAttentionIndicator":{"type":"string","enum":["none","attention","risk"],"description":"`attention` with an open complaint or an unresolved refund case; `risk` with a breached SLA or a repeat contact on the same issue."},"upcomingTickets":{"type":"integer","minimum":0},"activeMembership":{"type":"object","nullable":true,"properties":{"membershipId":{"type":"string"},"planName":{"type":"string"},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"walletBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"activeReservations":{"type":"integer","minimum":0},"futureGroupBookings":{"type":"integer","minimum":0},"openOrders":{"type":"integer","minimum":0},"serviceAlerts":{"type":"array","maxItems":20,"items":{"type":"object","required":["kind","message"],"properties":{"kind":{"type":"string","enum":["eventSoon","unresolvedRefundCase","membershipExpiring","openComplaint","communicationRestricted"]},"message":{"type":"string"},"referenceId":{"type":"string","nullable":true}}}},"preferredCommunicationChannel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"nullable":true},"marketingConsent":{"$ref":"#/components/schemas/ConsentDecision"},"accessibilityRequirements":{"type":"array","nullable":true,"description":"Null unless the caller holds GUEST_VIEW_PII.","items":{"type":"string"}},"communicationRestrictions":{"type":"array","description":"Channels the guest must not be contacted on (`getSuppressionList`).","items":{"$ref":"#/components/schemas/MessageChannel"}},"aiSummary":{"type":"object","nullable":true,"description":"Where the AI policy enables `summarise`. AI-derived and labelled as such.","properties":{"text":{"type":"string","maxLength":2000},"generatedAt":{"type":"string","format":"date-time"}}}}},
"CustomerServiceCommandCenterView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.case, marketing.case_message, marketing.case_internal_request (new), marketing.case_compensation_request (new), marketing.sla_policy and approvals.request","description":"One agent's workload for the filters given. \"Today\" is the venue's local day. Counts are of cases assigned to the agent unless the name says otherwise.","required":["myOpenCases","slaAtRisk","slaBreached","workQueue","todaysTasks","liveAlerts"],"properties":{"myOpenCases":{"type":"integer","minimum":0,"description":"Status not `resolved` or `closed`."},"newCases":{"type":"integer","minimum":0,"description":"Assigned to the agent and still `open` (not yet picked up)."},"casesDueToday":{"type":"integer","minimum":0,"description":"Open, with `slaDueAt` falling today."},"slaAtRisk":{"type":"integer","minimum":0,"description":"Open, not breached, with less than 25% of the SLA window left."},"slaBreached":{"type":"integer","minimum":0,"description":"Open with `Case.isSlaBreached` true."},"awaitingCustomer":{"type":"integer","minimum":0,"description":"Status `awaitingGuest`."},"awaitingInternalTeam":{"type":"integer","minimum":0,"description":"Open, with at least one open internal request."},"escalatedCases":{"type":"integer","minimum":0},"resolvedToday":{"type":"integer","minimum":0},"averageResolutionSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"Mean of `resolvedAt - recordedAt - slaPausedSeconds` over the agent's cases resolved in the last 30 days; null when none."},"workQueue":{"type":"array","maxItems":50,"description":"The agent's 50 most urgent open cases.","items":{"type":"object","required":["caseId","caseNumber","subject","status","priority"],"properties":{"caseId":{"type":"string","format":"uuid"},"caseNumber":{"type":"string"},"customer":{"type":"string","nullable":true,"description":"The guest's name, resolved from `pii.subject` as `Case.guestName` is; null unless the caller holds GUEST_VIEW_PII."},"subjectId":{"type":"string","format":"uuid","nullable":true},"subject":{"type":"string"},"categoryId":{"type":"string","format":"uuid","nullable":true},"category":{"type":"string","nullable":true,"description":"The category's display name."},"channel":{"$ref":"#/components/schemas/MessageChannel"},"priority":{"$ref":"#/components/schemas/CasePriority"},"status":{"$ref":"#/components/schemas/CaseStatus"},"assignedAgentPrincipalId":{"type":"string","format":"uuid","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaRemainingSeconds":{"type":"integer","nullable":true,"description":"Negative once breached."},"lastInteractionAt":{"type":"string","format":"date-time","nullable":true,"description":"The latest `CaseMessage.recordedAt`."},"nextAction":{"type":"string","nullable":true,"enum":["respondToCustomer","followUpInternalRequest","awaitApproval","proposeResolution","closeCase"]},"aiPriorityRank":{"type":"integer","minimum":1,"nullable":true,"description":"Where AI prioritisation is enabled (`getAiPolicy`), the case's rank in the queue."},"aiPriorityFactors":{"type":"array","description":"What raised the rank; AI-derived and labelled as such on screen.","items":{"type":"string","enum":["sla","customerImpact","transactionValue","eventProximity","customerSentiment","caseAge","operationalUrgency"]}}}}},"todaysTasks":{"type":"array","maxItems":100,"description":"Work due today derived from the agent's cases, earliest `dueAt` first.","items":{"type":"object","required":["kind","caseId"],"properties":{"kind":{"type":"string","enum":["callCustomer","respondToComplaint","reviewRefundRequest","followUpFinance","followUpInternalRequest","reissueTicket","requestSupervisorApproval"]},"caseId":{"type":"string","format":"uuid"},"referenceId":{"type":"string","nullable":true,"description":"The internal request, compensation request or approval request behind it."},"dueAt":{"type":"string","format":"date-time","nullable":true}}}},"liveAlerts":{"type":"array","maxItems":50,"description":"Newest first.","items":{"type":"object","required":["kind","caseId","raisedAt"],"properties":{"kind":{"type":"string","enum":["slaRisk","slaBreached","customerWaiting","internalRequestOverdue","approvalDecided"]},"caseId":{"type":"string","format":"uuid"},"message":{"type":"string"},"raisedAt":{"type":"string","format":"date-time"}}}}}},
"EscalationCollaborationInternalResolutionView": {"type":"object","x-ticvai-persistence":"marketing.case_internal_request","description":"One internal request from a case to a department (pack 10.1.8 Internal Request). The case keeps its owner; this is the department's piece of work.","required":["id","caseId","department","request","priority","escalationType"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7; equals the `Idempotency-Key` header on the write."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"caseId":{"type":"string","format":"uuid"},"department":{"type":"string","enum":["ticketing","finance","operations","accessControl","membership","crm","fnb","retail","groupSales","technicalSupport","venueManagement","management"]},"assigneePrincipalId":{"type":"string","format":"uuid","nullable":true},"request":{"type":"string","minLength":3,"maxLength":2000},"priority":{"$ref":"#/components/schemas/CasePriority"},"escalationType":{"type":"string","enum":["functional","supervisor","management","technical","financial","emergencyEventDay"]},"dueAt":{"type":"string","format":"date-time","nullable":true},"relatedTransaction":{"type":"object","nullable":true,"properties":{"kind":{"type":"string","enum":["order","payment","refund","walletTransaction","groupBooking"]},"referenceId":{"type":"string"}}},"attachmentRefs":{"type":"array","items":{"type":"string"}},"status":{"type":"string","enum":["open","inProgress","completed","cancelled"],"default":"open"},"response":{"type":"string","maxLength":2000,"nullable":true,"description":"The department's answer; required to complete."},"isOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"Computed on read; open or in progress past `dueAt`."},"aiRecommendedDepartment":{"type":"string","readOnly":true,"nullable":true,"x-ticvai-persisted":false,"description":"Where the AI policy enables `assist`; the department AI suggests from the case context."},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","readOnly":true,"nullable":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive"]},
"MediaRights": {"x-ticvai-persistence":"none — embedded in asset","type":"object","description":"Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n","properties":{"licenceKind":{"type":"string","enum":["owned","royaltyFree","rightsManaged","creativeCommons","editorialOnly","unknown"]},"licensor":{"type":"string","nullable":true},"licenceReference":{"type":"string","nullable":true},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"permittedUses":{"type":"array","items":{"type":"string","enum":["web","print","socialMedia","inVenue","advertising","internal"]}},"attributionRequired":{"type":"boolean","default":false},"attributionText":{"type":"string","nullable":true},"permittedTerritories":{"type":"array","items":{"type":"string"},"description":"ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"},"permittedChannels":{"type":"array","items":{"type":"string"},"description":"Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"},"modelReleaseHeld":{"type":"boolean","default":false},"renewalOwner":{"type":"string","format":"uuid","nullable":true}}},
"MediaStatus": {"type":"string","enum":["processing","ready","quarantined","failed","archived"]},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"OrderBookingTicketServiceWorkspaceInput": {"type":"object","x-ticvai-persistence":"marketing.case_service_action","x-ticvai-record-definition":"Permitted Service Actions (one per executed action)","description":"One service action on an order, taken from a case. Only an `execute` stores a row.","required":["id","mode","orderId"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7; equals the `Idempotency-Key` header."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"mode":{"type":"string","enum":["evaluate","execute"]},"caseId":{"type":"string","format":"uuid","description":"Required with `execute`; the action is recorded on this case."},"orderId":{"type":"string","format":"uuid"},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Omit for the whole order."},"action":{"type":"string","description":"Required with `execute`.","enum":["resendTicket","downloadTicket","reissue","transfer","changeName","reschedule","exchange","upgrade","cancel"]},"targetPerformanceId":{"type":"string","format":"uuid","description":"For `reschedule` and `exchange`, the option chosen from the evaluation."},"targetProductId":{"type":"string","format":"uuid","description":"For `exchange` and `upgrade`."},"recipientSubjectId":{"type":"string","format":"uuid","description":"For `transfer` and `changeName`, the new ticket holder."},"deliveryChannel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"description":"For `resendTicket`."},"reason":{"type":"string","maxLength":500},"status":{"type":"string","readOnly":true,"enum":["completed","pendingPayment","refused","failed"]},"downstreamOperation":{"type":"string","readOnly":true,"description":"The operation that performed it, e.g. `rescheduleOrder`."},"downstreamReference":{"type":"string","readOnly":true,"nullable":true},"performedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"OrderBookingTicketServiceWorkspaceView": {"type":"object","x-ticvai-persistence":"none — projection over orders.sales_order, orders.order_line, orders.payment, access.entitlement, marketing.case_service_action (new) and the policies each owning operation reads","description":"The order as a service agent sees it, what may be done to it, and what was done.","required":["orderId","order","availableActions"],"properties":{"orderId":{"type":"string","format":"uuid"},"order":{"type":"string","description":"The order number shown to the guest."},"subjectId":{"type":"string","format":"uuid","nullable":true},"purchaseDate":{"type":"string","format":"date-time"},"channel":{"type":"string","description":"The sales channel the order came through."},"products":{"type":"integer","minimum":0},"tickets":{"type":"integer","minimum":0},"eventId":{"type":"string","format":"uuid","nullable":true},"dateTime":{"type":"string","format":"date-time","nullable":true,"description":"The performance start."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"payment":{"type":"string","enum":["paid","partiallyPaid","unpaid","partiallyRefunded","refunded"]},"fulfillment":{"type":"string","enum":["pending","issued","delivered","failed"]},"ticketStatus":{"type":"string","enum":["valid","partiallyUsed","used","expired","cancelled"]},"availableActions":{"type":"array","items":{"type":"object","required":["action","isPermitted"],"properties":{"action":{"type":"string","enum":["resendTicket","downloadTicket","reissue","transfer","changeName","reschedule","exchange","upgrade","cancel","requestRefund"]},"isPermitted":{"type":"boolean"},"refusedBy":{"type":"string","nullable":true,"enum":["ticketPolicy","servicePolicy","orderStatus","eventDate","customerEntitlement","permission"]},"policyReference":{"type":"string","nullable":true},"options":{"type":"array","description":"Alternatives for `reschedule`, `exchange` and `upgrade`, earliest first.","items":{"type":"object","properties":{"performanceId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"startsAt":{"type":"string","format":"date-time","nullable":true},"available":{"type":"boolean"},"priceDifferencePerTicket":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"priceDifferenceTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}}},"lastAction":{"allOf":[{"$ref":"#/components/schemas/OrderBookingTicketServiceWorkspaceInput"}],"nullable":true,"description":"The action just executed; null on `evaluate`."}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"OrderSummary": {"x-ticvai-persistence":"none — projection","type":"object","required":["id","orderNumber","status","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"The same vocabulary as `Order.channel`, which this projects."},"lineCount":{"type":"integer"},"principalId":{"type":"string","format":"uuid","description":"The cashier who raised it — what the held-orders list shows."},"holdLabel":{"type":"string","nullable":true,"description":"As `Order.holdLabel`."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"description":"As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."},"createdAt":{"type":"string","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RefundCompensationServiceExceptionWorkspaceInput": {"type":"object","x-ticvai-persistence":"marketing.case_compensation_request","x-ticvai-record-definition":"Request Types","description":"One refund, compensation or policy-exception request raised from a case. The order, refund and approval are references, never copies.","required":["id","caseId","requestType","value","reason"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7; equals the `Idempotency-Key` header."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"caseId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"Required for `fullRefund`, `partialRefund`, `feeWaiver`, `upgrade` and `discount`."},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requestType":{"type":"string","enum":["fullRefund","partialRefund","serviceCredit","walletCredit","voucher","complimentaryTicket","feeWaiver","upgrade","discount","policyException"]},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"The money value requested; for a complimentary ticket or upgrade, its face value. This is what the approval thresholds are compared with."},"reason":{"type":"string","minLength":3,"maxLength":1000},"isPolicyException":{"type":"boolean","default":false,"description":"True when the standard policy would not allow it; always needs approval."},"exceptionReason":{"type":"string","maxLength":1000,"nullable":true,"description":"Required when `isPolicyException` is true."},"submit":{"type":"boolean","default":false,"description":"False saves a draft; true routes it.","writeOnly":true},"status":{"type":"string","readOnly":true,"enum":["draft","pendingApproval","approved","declined","fulfilled","failed","withdrawn"]},"approvalRequestId":{"type":"string","readOnly":true,"nullable":true},"fulfilmentOperation":{"type":"string","readOnly":true,"nullable":true,"description":"e.g. `createRefund`, `topUpWallet`."},"fulfilmentReference":{"type":"string","readOnly":true,"nullable":true,"description":"The refund, wallet transaction or voucher it produced."},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"RefundCompensationServiceExceptionWorkspaceView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.case_compensation_request (new), orders.sales_order, orders.refund, orders.order_fee, orders.refund_policy and approvals.request","description":"The request, the order's financial context, the policy evaluation and who must approve.","required":["request","approvalLevel"],"properties":{"request":{"$ref":"#/components/schemas/RefundCompensationServiceExceptionWorkspaceInput"},"originalTransaction":{"type":"string","nullable":true,"description":"The order number."},"amountPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amountUsed":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Value of tickets already scanned or consumed."},"refundableAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the refund policy's time bands allow now, less previous refunds."},"previousRefund":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"fees":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"proposedRefund":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"proposedCompensation":{"type":"object","nullable":true,"properties":{"requestType":{"type":"string"},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"policyEvaluation":{"type":"object","properties":{"standardPolicy":{"type":"string","description":"The rule that applies, as the venue's refund policy states it."},"isWithinPolicy":{"type":"boolean"},"policyReference":{"type":"string","nullable":true}}},"approvalLevel":{"type":"string","enum":["agent","secondUser","approver"],"description":"From the venue's `selfAuthoriseLimit`, `requiresSecondUserAbove` and `requiresApprovalAbove`; a policy exception is always `approver`."},"aiExplanation":{"type":"string","nullable":true,"maxLength":1000,"description":"AI-derived and labelled as such; cites a recorded policy or says none applies."}}},
"UnifiedInteractionCommunicationHistoryView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.case_message, marketing.conversation_message, marketing.conversation (telephony), marketing.message_dispatch and marketing.kiosk_assist_session","description":"One interaction on the timeline. `social` and `whatsapp` appear only where that channel is integrated.","required":["id","occurredAt","channel","direction","actorKind","source","recordId"],"properties":{"id":{"type":"string","description":"Stable across pages; the source and record id combined."},"occurredAt":{"type":"string","format":"date-time"},"channel":{"type":"string","enum":["email","phone","liveChat","whatsapp","sms","webForm","mobileApp","b2cPortal","social","posFrontDesk","internalNote","automatedNotification"]},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest; the name is resolved on screen through `getGuestProfile` under GUEST_VIEW_PII."},"actorKind":{"type":"string","enum":["guest","agent","system","ai"]},"actorPrincipalId":{"type":"string","format":"uuid","nullable":true},"direction":{"type":"string","enum":["inbound","outbound","internal"]},"subject":{"type":"string","nullable":true},"excerpt":{"type":"string","maxLength":500,"nullable":true},"relatedCaseId":{"type":"string","format":"uuid","nullable":true},"relatedOrderId":{"type":"string","nullable":true},"relatedTicketId":{"type":"string","nullable":true},"attachmentRefs":{"type":"array","items":{"type":"string"}},"sentiment":{"type":"string","nullable":true,"enum":["positive","neutral","negative"],"description":"Where sentiment analysis is enabled; AI-derived."},"source":{"type":"string","enum":["caseMessage","conversationMessage","call","messageDispatch","kioskAssist"]},"recordId":{"type":"string","description":"The row in the source table."}}},
"UploadTicket": {"x-ticvai-persistence":"assets.media_upload","type":"object","required":["uploadId","uploadUrl","method","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"uploadId":{"type":"string","format":"uuid"},"uploadUrl":{"type":"string","description":"Signed. PUT the file here, then confirm with `/complete`."},"method":{"type":"string","enum":["PUT","POST"]},"headers":{"type":"object","additionalProperties":{"type":"string"}},"maxSizeBytes":{"type":"integer"},"expiresAt":{"type":"string","format":"date-time"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"venueId":{"type":"string","format":"uuid","nullable":true},"assetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The asset this upload became — created by `completeUpload`, or the asset whose file `replaceMediaAsset` swapped. Null while the transfer is outstanding.\n"}}}
}
```
