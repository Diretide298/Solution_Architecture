# WS122 — AI Governance board 2

**10 screens · 29 operations · 40 schemas · 10 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 10 permissions apply here:
  `AI_APPROVE, AI_AUDIT_VIEW, AI_CONFIGURE, AI_USE, APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_REQUEST, APPROVAL_VIEW, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
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
| `ADM-529` | AI Human Oversight Command Center | D | 8 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-530` | AI Approval Requirement & Routing Configuration | D | 32 | 26 | 7 | 56 | 1 | 3 | — | notStarted (—) |
| `ADM-531` | AI Approval Review Workspace | D | 8 | 6 | 7 | 2 | 2 | 3 | — | notStarted (—) |
| `ADM-532` | Conditional Approval & Approval Conditions | D | 6 | 66 | 7 | 8 | 2 | 3 | — | notStarted (—) |
| `ADM-533` | Human Review, Challenge & AI Clarification Workspace | D | 6 | 22 | 7 | 12 | 1 | 0 | — | notStarted (—) |
| `ADM-534` | Escalation, Delegation & Approval SLA Management | B | 31 | 52 | 7 | 5 | 2 | 3 | — | notStarted (—) |
| `ADM-535` | Live AI Execution Oversight & Human Intervention | D | 11 | 26 | 7 | 1 | 3 | 0 | — | notStarted (—) |
| `ADM-536` | Human Override & Manual Control Center | D | 12 | 38 | 7 | 5 | 1 | 0 | — | notStarted (—) |
| `ADM-537` | Approval & Intervention History / Decision Timeline | D | 8 | 6 | 7 | 5 | 1 | 3 | — | notStarted (—) |
| `ADM-538` | Human Oversight Workflow Simulator & Readiness Center | D | 13 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-529` AI Human Oversight Command Center

**Provide one central operational view of all AI activities requiring human oversight across TICVAI. This should become the control room for AI actions waiting for human intervention.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-529 |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `planId` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-human-oversight-command-center-adm-529` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getActionPlan` (AI_USE), `listProposedActions` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**From the AI & Intelligence process.** The human-oversight control room: every AI action waiting for or under human oversight - pending approvals by risk, items awaiting a second approver, conditional approvals, requested changes, escalations, overdue reviews, executions in progress and today's interventions. The one thing to get right: SLA is visible on every pending item and overdue items sort first.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Search human oversight | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, ai capability, module, risk, approver and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Pending AI Approvals** (metric tile)

**High-Risk Reviews** (metric tile)

**Critical Reviews** (metric tile)

**Awaiting Additional Approver** (metric tile)

**Conditional Approvals** (metric tile)

**Requested Changes** (metric tile)

**Escalated Cases** (metric tile)

**Overdue Reviews** (metric tile)

**Active AI Executions Under Oversight** (metric tile)

**Human Interventions Today** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **queue**: Proposal, capability, risk, approval tier, approver, waiting time vs SLA, expiry; filters by venue, capability, risk, status. *(source: contracts/satellite/ai.yaml#listProposedActions / DI-956)*

**Data it reads**: `listProposedActions` (onLoad, What the assistant has proposed and nobody has decided); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-530` AI Approval Requirement & Routing Configuration: *AI Approval Requirement & Routing Configuration*; carries `tenantId`
- → `ADM-531` AI Approval Review Workspace: *AI Approval Review Workspace*; carries `planId`
- → `ADM-532` Conditional Approval & Approval Conditions: *Conditional Approval & Approval Conditions*; carries `planId`
- → `ADM-533` Human Review, Challenge & AI Clarification Workspace: *Human Review, Challenge & AI Clarification Workspace*; carries `tenantId`
- → `ADM-534` Escalation, Delegation & Approval SLA Management: *Escalation, Delegation & Approval SLA Management*; carries `planId`
- → `ADM-535` Live AI Execution Oversight & Human Intervention: *Live AI Execution Oversight & Human Intervention*; carries `planId`
- → `ADM-536` Human Override & Manual Control Center: *Human Override & Manual Control Center*; carries `planId`
- → `ADM-537` Approval & Intervention History / Decision Timeline: *Approval & Intervention History / Decision Timeline*; carries `tenantId`
- → `ADM-538` Human Oversight Workflow Simulator & Readiness Center: *Human Oversight Workflow Simulator & Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The human oversight list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the human oversight untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No human oversight yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the human oversight are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  pending: 12
  highRisk: 3
  critical: 0
  awaitingSecond: 2
  overdue: 1
  executing: 1
  interventionsToday: 4
```

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `listProposedActions` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-529` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-529`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 1: Opens AI Human Oversight Command Center → Provide one central operational view of all AI activities requiring human oversight across TICVAI. This should become the control room for AI actions waiting for human intervention.
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F231 branch at step 1 (expected): when Nothing has been set up on AI Human Oversight Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F231 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-529?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-002`, `ADM-530`, `ADM-531`, `ADM-532`, `ADM-533`, `ADM-534`, `ADM-535`, `ADM-536`, `ADM-537`, `ADM-538`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-530` AI Approval Requirement & Routing Configuration

**Translate Board 1 governance decisions into the correct human approval workflow.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-530 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 configure, 2 operate, 2 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/platform/ai-approval-requirement-routing-configuration-adm-530` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `createAiGovernancePolicyDraft` (AI_CONFIGURE), `listAiGovernancePolicyVersions` (AI_USE), `listAiTools` (AI_USE), `listApprovalMatrices` (APPROVAL_CONFIGURE), `setApprovalMatrix` (APPROVAL_CONFIGURE), `evaluateApprovalRequirement` (APPROVAL_VIEW) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack names 11 actions on this screen and the screen declares 0 operations.** Unserved: Single Approval, Sequential Approval, Parallel Approval, Conditional Approval, Risk-Based Approval, → … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Who approves which AI action, in what order and within what time, based on risk and amount - through the shared approval matrix, not a separate AI approval system (kind aiRecommendation). The client's example: a pricing change routes commercial manager → venue GM → commercial director. The one thing to get right: test a routing before saving - "an AI price increase of +12% on Adult Saturday goes to: Commercial manager, then GM".

**Known correction pending (do not draw the wrong version)**

- **Routing types and routes drawn as buttons.** Why: They are the matrix's rows and options. *(source: screens/P09-platform-admin-console.yaml#ADM-530; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Policy | picker: choose a policy | — | — | `listAiGovernancePolicyVersions` ?policyId |
| Status | radio group | — | Draft · Simulated · Published · Superseded | `listAiGovernancePolicyVersions` ?status |
| Kind | select | — | Action · Data · Scope · Autonomy · Approval · Environment | `listAiGovernancePolicyVersions` ?kind |
| Target contract | text field | — | — | `listAiTools` ?targetContract |
| Effect | segmented control | — | Read · Write · Destructive | `listAiTools` ?effect |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalMatrices` ?kind |
| Effective | toggle | off | — | `listApprovalMatrices` ?effective |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Save approval matrix** (modal, opened by *Save approval matrix*; *Save approval matrix* calls `setApprovalMatrix`, *Cancel* sends nothing)

**Collects the matrix for kind `aiRecommendation`** before `setApprovalMatrix` is called: levels, the value range each approver may approve, and the escalation above it. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | — | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. | `setApprovalMatrix` body |
| Scope level `scopeLevel` | segmented control | required | — | Tenant · Region · Venue | — | — | `setApprovalMatrix` body |
| Rules `rules` | repeatable rows | required | — | — | — | — | `setApprovalMatrix` body |
| Order `rules[].order` | number field | required | — | — | — | First match wins. Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about. | `setApprovalMatrix` body |
| Min amount `rules[].minAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setApprovalMatrix` body |
| Max amount `rules[].maxAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setApprovalMatrix` body |
| Risk score above `rules[].riskScoreAbove` | number field | optional | — | — | — | 11.1.12. Not matched against the AI risk score (29 September, build pass, group G2). | `setApprovalMatrix` body |
| Condition `rules[].condition` | text field | optional | — | — | — | 11.1.13. Evaluated against the attributes the caller supplied. | `setApprovalMatrix` body |
| Approver roles `rules[].approverRoleIds` | multi-picker: choose approver roles | required | — | at least 1 | — | Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. | `setApprovalMatrix` body |
| Approver scope level `rules[].approverScopeLevel` | radio group | optional | — | Venue · Department · Region · Tenant | — | 11.1.39. Which organisational level the approver must sit at. | `setApprovalMatrix` body |
| Mode `rules[].mode` | radio group | required | — | Sequential · Parallel · Consensus · Majority | — | 11.1.43–11.1.46. Sequential asks one at a time, parallel asks everyone at once, consensus needs all of them, majority needs more than half. | `setApprovalMatrix` body |
| Levels `rules[].levels` | number field | optional | 1 | — | — | 11.1.3. Multi-level chains ask each level in turn. | `setApprovalMatrix` body |
| Requires MFA `rules[].requiresMfa` | toggle | optional | off | — | — | — | `setApprovalMatrix` body |
| Requires signature `rules[].requiresSignature` | toggle | optional | off | — | — | — | `setApprovalMatrix` body |
| Sla minutes `rules[].slaMinutes` | number field (minutes) | optional | — | — | — | 11.1.14. Null means no SLA, which is different from a long one. | `setApprovalMatrix` body |
| Escalate after minutes `rules[].escalateAfterMinutes` | number field (minutes) | optional | — | — | — | — | `setApprovalMatrix` body |
| Escalate to roles `rules[].escalateToRoleIds` | multi-picker: choose escalate to roles | optional | — | — | — | Role ids from `identity.listRoles`, as `approverRoleIds`. | `setApprovalMatrix` body |
| Expires after minutes `rules[].expiresAfterMinutes` | number field (minutes) | optional | — | — | — | 11.1.53. An unanswered request eventually stops waiting. | `setApprovalMatrix` body |
| Subject types `rules[].subjectTypes` | list of values (chips) | optional | — | — | — | Which subjects of the kind this rule matches (decided 2 October 2026, Chinmay; CHG-CSP-028, CHG-CSP-036, CHG-CSP-031): the `CreateApprovalRequest.subjectType` values, for example … | `setApprovalMatrix` body |
| Signature methods `rules[].signatureMethods` | multi-select chips | optional | — | Platform key · Uae pass · External certificate · Drawn signature | — | The signature methods this level accepts, where `requiresSignature` is true (design-notes correction on ADM-344, Block B: "Configuring which stages need a signature is a policy … | `setApprovalMatrix` body |
| External provider `rules[].externalProviderId` | picker: choose an external provider | optional | — | — | shows names, sends the id | 11.1.65 (29 September). This level is decided in an external workflow system (`ApprovalExternalProvider`) rather than by a person in TICVAI. | `setApprovalMatrix` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `setApprovalMatrix` body |

Errors to draw in the form: 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold … (ApprovalMatrixRefusedProblem)

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_CONFIGURE`, `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_VIEW` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Sent by *Test a routing*** (`evaluateApprovalRequirement`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | — | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. | `evaluateApprovalRequirement` body |
| Scope path `scopePath` | text field | required | — | — | — | — | `evaluateApprovalRequirement` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `evaluateApprovalRequirement` body |
| Attributes `attributes` | key and value settings | optional | — | — | — | Whatever the conditional rules match on (11.1.13). | `evaluateApprovalRequirement` body |

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **approval matrix rows**: Kind, amount or % thresholds, stages (single, sequential, parallel), approver roles, SLA and escalation. *(source: contracts/spine/approvals.yaml#setApprovalMatrix / DI-956 / MoM 18 Sep 4.2)*

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Approval matrix for AI actions** (data table, from `listApprovalMatrices`): **AI actions route through the shared approval matrix** (18 September minutes, M18-02), kind `aiRecommendation`: an approver is authorised up to a limit and anything above it escalates.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Scope level | chip: Tenant, Region, Venue | — |
| Rules | list or chips (count when long) | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Order | 1,234 | First match wins. Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason … |
| Min amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Max amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Risk score above | 1,234.5 | 11.1.12. Not matched against the AI risk score (29 September, build pass, group G2). |
| Condition | text | 11.1.13. Evaluated against the attributes the caller supplied. |
| Approver roles | list or chips (count when long) | Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. |
| Approver scope level | chip: Venue, Department, Region, Tenant | 11.1.39. Which organisational level the approver must sit at. |
| Mode | chip: Sequential, Parallel, Consensus, Majority | 11.1.43–11.1.46. Sequential asks one at a time, parallel asks everyone at once, consensus needs all of them, majority needs more than half. |
| Levels | 1,234 | 11.1.3. Multi-level chains ask each level in turn. |
| Requires MFA | yes / no (icon or chip) | — |
| Requires signature | yes / no (icon or chip) | — |
| Sla minutes | 1,234 | 11.1.14. Null means no SLA, which is different from a long one. |
| Escalate after minutes | 1,234 | — |
| Escalate to roles | list or chips (count when long) | Role ids from `identity.listRoles`, as `approverRoleIds`. |
| Expires after minutes | 1,234 | 11.1.53. An unanswered request eventually stops waiting. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Single Approval (primary button) | navigation or local | — | — | — | — |
| Sequential Approval (secondary button) | navigation or local | — | — | — | — |
| Parallel Approval (secondary button) | navigation or local | — | — | — | — |
| Conditional Approval (secondary button) | navigation or local | — | — | — | — |
| Risk-Based Approval (secondary button) | navigation or local | — | — | — | — |
| → Commercial Manager (secondary button) | navigation or local | — | — | — | — |
| → Commercial Manager + General Manager (secondary button) | navigation or local | — | — | — | — |
| → Commercial Director + General Manager (secondary button) | navigation or local | — | — | — | — |
| Save approval matrix (primary button) | `setApprovalMatrix` PUT `/approval-matrices` | ApprovalMatrix | ApprovalMatrix | 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which … | opens modal first |
| Test a routing (secondary button) | `evaluateApprovalRequirement` POST `/approval-requests/evaluate` | inline | ApprovalRequirement | — | — |
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Test a routing**: Shows the approvers, their limits and whether the example is within them or escalates. *(source: contracts/spine/approvals.yaml#evaluateApprovalRequirement)*

**Data it reads**: `listAiGovernancePolicyVersions` (onLoad, Governance policies and their versions); `listAiTools` (onLoad, The tool registry); `listApprovalMatrices` (onLoad, The matrices AI actions route through); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`, `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval requirement routing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval requirement routing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval requirement routing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval requirement routing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold … (ApprovalMatrixRefusedProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- range: price change ≤ 5%
  route: Commercial manager
- range: 5-15%
  route: Commercial manager + General manager
- range: '> 15%'
  route: Commercial director + General manager
```

#### Permissions

- `createAiGovernancePolicyDraft` → `AI_CONFIGURE` (configure) · staff
- `listAiGovernancePolicyVersions` → `AI_USE` (operate) · staff
- `listAiTools` → `AI_USE` (operate) · staff
- `listApprovalMatrices` → `APPROVAL_CONFIGURE` (configure) · staff
- `setApprovalMatrix` → `APPROVAL_CONFIGURE` (configure) · staff
- `evaluateApprovalRequirement` → `APPROVAL_VIEW` (read) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

56 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.51 | System shall support reservation approvals. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 1.2.76 | System shall support configurable approval workflows. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 2.12.4 | The system should support configuration of required access level to allow refund, exchange and/or void actions. At minimum, the system should provide: - Ability to enable/disable supervisor access … | Ticketing Sales | CONTRACTED | `setApprovalMatrix` |
| 3.3.31 | Segregation of Duties - System shall enforce segregation of duties in access policies. | Admission and Access | CONTRACTED | `setApprovalMatrix` |
| 7.1.22 | The system shall support approval workflows for user creation, role assignment, permission changes, privileged access requests, and user deactivation. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.1.24 | The system shall support configurable approval requirements for refunds, ticket cancellations, price changes, promotion changes, membership changes, wallet adjustments, and manual overrides. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.5.10 | Support multi-level approval processes for complimentary tickets, VIP invitations and sponsor allocations with full audit history. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 11.1.1 | Provides configurable workflows requiring one or more approvals before sensitive actions can be executed. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.2 | Approval Workflow Configuration System shall allow administrators to configure approval workflows for different business processes. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.3 | Multi-Level Approval System shall support single-level and multi-level approval chains. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.4 | Role-Based Approval Routing System shall automatically route approval requests based on organizational hierarchy and user roles. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.5 | Escalation Rules System shall automatically escalate pending approvals after configurable time thresholds. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| … 44 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI actions route through the shared approval matrix: the screen shows the approver's limit for the kind and amount and whether the action is within it or must escalate; escalation, delegation and SLA apply as to any approval. *(agreed · MoM 18 Sep 2026, M18-02 · DI-956)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-530` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-530`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 2: Works in AI Approval Requirement & Routing Configuration → Translate Board 1 governance decisions into the correct human approval workflow.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (32), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-530?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Single Approval, Sequential Approval, Parallel Approval, Conditional Approval, Risk-Based Approval, → Commercial Manager, → Commercial Manager + General Manager, → Commercial Director + General Manager, Save approval matrix, Test a routing, Open access grant.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-531` AI Approval Review Workspace

**Give the human approver enough information to make an informed decision without having to navigate across many TICVAI modules. This should be one of the strongest screens in the board.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-531 |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration Current Proposed) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `actionId` (navigation), `planId` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-approval-review-workspace-adm-531` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getActionPlan` (AI_USE), `simulateActionPlan` (AI_USE), `decideProposedAction` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**From the AI & Intelligence process.** The approver's workspace: everything needed to decide without visiting other modules - current vs proposed, effective date, impact (channels it publishes to, whether future bookings are affected), risk, affected objects, the AI's explanation and evidence, and the simulation. The one thing to get right: current and proposed side by side with the difference highlighted, and the approver's own limit shown.

**Known correction pending (do not draw the wrong version)**

- **Values pasted into field labels ("Adult Weekend Price AED 140 AED 150").** Why: Sample data. *(source: screens/P09-platform-admin-console.yaml#ADM-531; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Adult Weekend Price AED 140 AED 150 | text field | — | — | — | — | — | — |
| Effective Date Current 1 Oct 2026 | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **current vs proposed**: Two columns with change and % ("Adult weekend price AED 140 → AED 150, +7.1%; effective 1 Oct 2026"); affected channels and bookings below. *(source: DI-931 / contracts/satellite/ai.yaml#simulateActionPlan)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Approve / Reject**: Reason required on reject; approve within the approver's limit, otherwise "Escalate" replaces Approve. *(source: contracts/satellite/ai.yaml#decideProposedAction / DI-932 / DI-956)*

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval review configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval review untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval review configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213).; 409 The plan is executing or finished; simulate a rollback plan instead. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
proposal:
  item: Adult Weekend Price
  current: AED 140.00
  proposed: AED 150.00
  effective: 1 Nov 2026
  channels:
  - Website
  - App
  - POS
  futureBookings: 1,204 unaffected (already purchased)
```

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `simulateActionPlan` → `AI_USE` (operate) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.4 | Approval Before Execution AI recommendations affecting pricing or financial operations shall require approval before execution | Unified Operations Dashboard | CONTRACTED | `decideProposedAction` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval is not binary: conditional approval lets an approver approve with restrictions, e.g. a commercial manager may approve price increases only up to a ceiling, anything higher escalates. An approver can also challenge a proposal and request evidence or alternatives. *(agreed · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-932)*
- The AI approval review workspace gives the approver everything needed to decide: current vs proposed value, impact, risk and affected objects (e.g. a weekend price increase shown with the channels it publishes to and whether future bookings are affected). *(client request · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-931)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-531` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-531`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 4: Works in AI Approval Review Workspace → Give the human approver enough information to make an informed decision without having to navigate across many TICVAI modules. This should be one of the strongest screens in the board.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-531?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-532` Conditional Approval & Approval Conditions

**Allow humans to approve an AI action subject to explicit conditions rather than treating approval as simply Yes/No.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-532 |
| Who uses it | ticvai staff holding `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 configure, 2 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `actionId` (navigation), `planId` (navigation), `tenantId` (navigation) |
| Route | `/platform/conditional-approval-approval-conditions-adm-532` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getActionPlan` (AI_USE), `decideProposedAction` (AI_USE), `evaluateApprovalRequirement` (APPROVAL_VIEW), `listApprovalMatrices` (APPROVAL_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Approve with conditions instead of yes/no: e.g. approve the price increase only up to a ceiling, only for given dates, only on some channels; anything beyond escalates. The one thing to get right: each condition is explicit and enforced at execution, and the approver's threshold range from the matrix is shown.

**Known correction pending (do not draw the wrong version)**

- **decideProposedAction takes only approve/reject and a reason; there is no place for conditions.** Why: Conditional approval (DI-932, DI-956) needs approveWithConditions and a conditions object, or the governance outcome allowWithConditions surfaced to approvers. *(source: contracts/satellite/ai.yaml#decideProposedAction / contracts/satellite/ai.yaml#/components/schemas/AiGovernanceOutcome; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalMatrices` ?kind |
| Effective | toggle | off | — | `listApprovalMatrices` ?effective |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_VIEW` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **conditions**: Typed conditions (maximum value or %, date range, channels, venues) added to the approval. *(source: DI-932 / MoM 18 Sep 4.2)*

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Detail panel** (detail panel, from `getActionPlan`): One record, read-only.

| Shows | Format | Notes |
|---|---|---|
| Plan | grouped details | A plan: plan, validate, simulate, approve, execute, with rollback (design 2.2 D, 3.8; AIC-086..107). |
| ID | the name it points at, never the id | — |
| Origin | chip: Configuration session, Generate configuration, Assistant, Risk case, Operational … | — |
| Origin ref | text | — |
| Summary | text | — |
| Status | chip: Draft, Validated, Simulated, Awaiting approval, Approved, Executing… | — |
| Autonomy level | 1,234 | One autonomy scale for every capability (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). |
| Approval tier | 1,234 | The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). |
| Approval request | the name it points at, never the id | The `approvals` request, where tier 2 or the matrix caught the plan. |
| Proposed action | the name it points at, never the id | The `ai.proposed_action` the plan is presented as for a decision. |
| Change set hash | text | — |
| Governance outcome | chip: Allow, Allow with conditions, Prepare only, Approval required, Escalate, Block | What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). |
| Policy version ref | text | The governance policy version that decided it. |
| Simulation | grouped details | Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4). |
| Partial completion allowed | yes / no (icon or chip) | Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134). |
| Rollback of plan | the name it points at, never the id | — |
| Requested by principal | the name it points at, never the id | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Steps | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |

**Approval condition for this action** (detail panel, from `evaluateApprovalRequirement`): **Conditional authority** (M18-02): the approver's limit for this kind and amount, and whether the action is within it or must escalate.

| Shows | Format | Notes |
|---|---|---|
| Is required | yes / no (icon or chip) | — |
| Matched rule | grouped details | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Order | 1,234 | First match wins. Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason … |
| Min amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Max amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Risk score above | 1,234.5 | 11.1.12. Not matched against the AI risk score (29 September, build pass, group G2). |
| Condition | text | 11.1.13. Evaluated against the attributes the caller supplied. |
| Approver roles | list or chips (count when long) | Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. |
| Approver scope level | chip: Venue, Department, Region, Tenant | 11.1.39. Which organisational level the approver must sit at. |
| Mode | chip: Sequential, Parallel, Consensus, Majority | 11.1.43–11.1.46. Sequential asks one at a time, parallel asks everyone at once, consensus needs all of them, majority needs more than half. |
| Levels | 1,234 | 11.1.3. Multi-level chains ask each level in turn. |
| Requires MFA | yes / no (icon or chip) | — |
| Requires signature | yes / no (icon or chip) | — |
| Sla minutes | 1,234 | 11.1.14. Null means no SLA, which is different from a long one. |
| Escalate after minutes | 1,234 | — |
| Escalate to roles | list or chips (count when long) | Role ids from `identity.listRoles`, as `approverRoleIds`. |
| Expires after minutes | 1,234 | 11.1.53. An unanswered request eventually stops waiting. |
| Subject types | list or chips (count when long) | Which subjects of the kind this rule matches (decided 2 October 2026, Chinmay; CHG-CSP-028, CHG-CSP-036, CHG-CSP-031): the … |
| Signature methods | list or chips (count when long) | The signature methods this level accepts, where `requiresSignature` is true (design-notes correction on ADM-344, Block B: "Configuring … |

**Threshold ranges** (data table, from `listApprovalMatrices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Scope level | chip: Tenant, Region, Venue | — |
| Rules | list or chips (count when long) | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Order | 1,234 | First match wins. Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason … |
| Min amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Max amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Risk score above | 1,234.5 | 11.1.12. Not matched against the AI risk score (29 September, build pass, group G2). |
| Condition | text | 11.1.13. Evaluated against the attributes the caller supplied. |
| Approver roles | list or chips (count when long) | Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. |
| Approver scope level | chip: Venue, Department, Region, Tenant | 11.1.39. Which organisational level the approver must sit at. |
| Mode | chip: Sequential, Parallel, Consensus, Majority | 11.1.43–11.1.46. Sequential asks one at a time, parallel asks everyone at once, consensus needs all of them, majority needs more than half. |
| Levels | 1,234 | 11.1.3. Multi-level chains ask each level in turn. |
| Requires MFA | yes / no (icon or chip) | — |
| Requires signature | yes / no (icon or chip) | — |
| Sla minutes | 1,234 | 11.1.14. Null means no SLA, which is different from a long one. |
| Escalate after minutes | 1,234 | — |
| Escalate to roles | list or chips (count when long) | Role ids from `identity.listRoles`, as `approverRoleIds`. |
| Expires after minutes | 1,234 | 11.1.53. An unanswered request eventually stops waiting. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `evaluateApprovalRequirement` (onLoad, Whether this action is within the approver's limit); `listApprovalMatrices` (onLoad, The threshold ranges); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The conditional approval approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the conditional approval approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No conditional approval approval yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the conditional approval approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
condition: Approve up to +5% (AED 147.00); above that escalates to the General manager
```

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff
- `evaluateApprovalRequirement` → `APPROVAL_VIEW` (read) · staff
- `listApprovalMatrices` → `APPROVAL_CONFIGURE` (configure) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.4 | Approval Before Execution AI recommendations affecting pricing or financial operations shall require approval before execution | Unified Operations Dashboard | CONTRACTED | `decideProposedAction` |
| 2.7.39 | The system should support: - Multiple credit terms and approval routing processes which can prevent order fulfilment prior to obtaining necessary approvals by client. - Supervisor level authorization … | Ticketing Sales | CONTRACTED | `evaluateApprovalRequirement` |
| 2.9.19 | Price creation, modification, activation, and publication shall support configurable approval workflows with audit trails and role-based authorization. | Ticketing Sales | CONTRACTED | `evaluateApprovalRequirement` |
| 3.6.38 | Promotion creation, modification, activation, and deactivation shall support configurable approval workflows with multi-level authorization and audit tracking. | Admission and Access | CONTRACTED | `evaluateApprovalRequirement` |
| 4.8.10 | Require approval before recipe changes become active. | Bundles and Promotions | CONTRACTED | `evaluateApprovalRequirement` |
| 4.8.11 | Track all recipe creation, modification and approval activities. | Bundles and Promotions | CONTRACTED | `evaluateApprovalRequirement` |
| 5.12.79 | Approval workflow for financial rule changes. | F&B & Guest Management | CONTRACTED | `evaluateApprovalRequirement` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI actions route through the shared approval matrix: the screen shows the approver's limit for the kind and amount and whether the action is within it or must escalate; escalation, delegation and SLA apply as to any approval. *(agreed · MoM 18 Sep 2026, M18-02 · DI-956)*
- Approval is not binary: conditional approval lets an approver approve with restrictions, e.g. a commercial manager may approve price increases only up to a ceiling, anything higher escalates. An approver can also challenge a proposal and request evidence or alternatives. *(agreed · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-932)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-532` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-532`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 6: Works in Conditional Approval & Approval Conditions → Allow humans to approve an AI action subject to explicit conditions rather than treating approval as simply Yes/No.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (66 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-532?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Cancel.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-533` Human Review, Challenge & AI Clarification Workspace

**Allow the approver to question the AI proposal before making a decision. Human oversight should not mean simply clicking Approve.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-533 |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_AUDIT_VIEW`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (3 operate, 2 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `conversationId` (navigation), `decisionRecordId` (navigation), `tenantId` (navigation) |
| Route | `/platform/human-review-challenge-ai-clarification-workspace-adm-533` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `overrideAiDecision` (AI_APPROVE), `getAiDecisionTrace` (AI_AUDIT_VIEW), `sendAiMessage` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the AI & Intelligence process.** Challenge the AI before deciding: ask why, request evidence or alternatives, see the decision trace, and override with a human decision. The one thing to get right: the challenge conversation is attached to the proposal, and the AI's answers cite the evidence in the trace - it cannot invent new numbers.

**Known correction pending (do not draw the wrong version)**

- **"Ask AI" is a table column.** Why: An action. *(source: screens/P09-platform-admin-console.yaml#ADM-533; AI & Intelligence)*
- **No "request changes" decision; decideProposedAction has approve/reject only.** Why: The minutes ask for challenge and request more information (also the approval engine's Return / Request more information). *(source: TRACKER Actions row 76 / contracts/satellite/ai.yaml#decideProposedAction; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Depth | segmented control | Business | Business · Governance · Technical | `getAiDecisionTrace` ?depth |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_APPROVE`, `AI_AUDIT_VIEW`, `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Every human review challenge** (data table)

| Shows | Format | Notes |
|---|---|---|
| Proposed action | text | not in the schema: `Proposed Action` |
| Business context | text | not in the schema: `Business Context` |
| Risk | text | not in the schema: `Risk` |
| Impact | text | not in the schema: `Impact` |
| AI recommendation | text | not in the schema: `AI Recommendation` |
| Validation | text | not in the schema: `Validation` |
| Alternatives | text | not in the schema: `Alternatives` |
| Ask AI | text | not in the schema: `Ask AI` |

**The selected human review challenge** (detail panel): The pack groups this record's detail under its own headings: “Other Example Questions”, “Important Requirement”, “If evidence is unavailable”.

| Shows | Format | Notes |
|---|---|---|
| Proposed action | text | not in the schema: `Proposed Action` |
| Business context | text | not in the schema: `Business Context` |
| Risk | text | not in the schema: `Risk` |
| Impact | text | not in the schema: `Impact` |
| AI recommendation | text | not in the schema: `AI Recommendation` |
| Validation | text | not in the schema: `Validation` |
| Alternatives | text | not in the schema: `Alternatives` |
| Ask AI | text | not in the schema: `Ask AI` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **proposal context**: Proposed action, business context, risk, impact, the AI's recommendation and validation, alternatives considered. *(source: contracts/satellite/ai.yaml#getAiDecisionTrace / MoM 18 Sep 4.2)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Ask AI**: Conversation scoped to this proposal; answers cite trace evidence. *(source: contracts/satellite/ai.yaml#sendAiMessage / ADR-0054)*
- **Override**: Records the human decision beside the AI's. *(source: contracts/satellite/ai.yaml#overrideAiDecision)*

**Data it reads**: `getAiDecisionTrace` (onLoad, The full trace of a decision); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The human review challenge list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the human review challenge untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No human review challenge yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the human review challenge are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_APPROVE`, `AI_AUDIT_VIEW`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 The guard (the provider''s content-safety service, CHG-R1S-002) blocked the message or the reply (`guard-refused`, CHG-CSA-003). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
challenge:
- Why +12% and not +8%?
- Saturday bookings are 31% above forecast high end for 3 weeks; +12% keeps the forecast inside capacity.
```

#### Permissions

- `overrideAiDecision` → `AI_APPROVE` (operate) · staff
- `getAiDecisionTrace` → `AI_AUDIT_VIEW` (read) · staff
- `sendAiMessage` → `AI_USE` (operate) · staff, guest
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.5 | Explainability System shall provide reasoning and confidence indicators where available. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.19 | System shall support AI-powered ticketing assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.20 | System shall support AI-powered support assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 18.10.1 | AI Assistant - System shall provide an AI assistant for employees. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.3 | Operational Queries - Users shall retrieve operational information through AI. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.4 | Work Order Assistance - AI shall assist users with work order activities. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.5 | Knowledge Base Assistance - AI shall provide access to operational knowledge and procedures. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 22.8.4 | AI Chatbot Assistant | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.13 | AI Intent Recognition | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.14 | AI Knowledge Base Integration | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.15 | AI Product Recommendations | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval is not binary: conditional approval lets an approver approve with restrictions, e.g. a commercial manager may approve price increases only up to a ceiling, anything higher escalates. An approver can also challenge a proposal and request evidence or alternatives. *(agreed · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-932)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-533` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-533`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 8: Works in Human Review, Challenge & AI Clarification Workspace → Allow the approver to question the AI proposal before making a decision. Human oversight should not mean simply clicking Approve.
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-533?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_AUDIT_VIEW`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-534` Escalation, Delegation & Approval SLA Management

**Ensure AI approvals do not remain indefinitely pending and provide controlled routing when approvers are unavailable or additional authority is required.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-534 |
| Who uses it | ticvai staff holding `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_DECIDE`, `APPROVAL_REQUEST`, `APPROVAL_VIEW`, `PLATFORM_TENANT_ACCESS`… (4 operate, 1 configure, 2 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `planId` (navigation), `requestId` (navigation), `tenantId` (navigation) |
| Route | `/platform/escalation-delegation-approval-sla-management-adm-534` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getActionPlan` (AI_USE), `listProposedActions` (AI_USE), `listApprovalDelegations` (APPROVAL_VIEW), `escalateApprovalRequest` (APPROVAL_REQUEST), `createApprovalDelegation` (APPROVAL_DECIDE), `setApprovalSlaPolicy` (APPROVAL_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** AI-proposed actions waiting for approval: SLA, escalation and delegation so they never wait forever. An expired AI proposal lapses; it is never applied by default.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: getActionPlan (AI_USE), listProposedActions (AI_USE) … (CHG-SBO-001); requiresModule is 'ai' on a TICVAI Console screen. (CHG-SBO-003).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_DECIDE`, `APPROVAL_REQUEST`, `APPROVAL_VIEW` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Sent by *Escalate*** (`escalateApprovalRequest`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 300 | — | — | `escalateApprovalRequest` body |

**Sent by *Delegate*** (`createApprovalDelegation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Delegator principal `delegatorPrincipalId` | picker: choose a delegator principal | required | — | — | shows names, sends the id | A principal id (`identity.Principal.id`). This contract stores the id only; the name to show, and the people to pick from, come from `identity.listPrincipals` and … | `createApprovalDelegation` body |
| Delegate principal `delegatePrincipalId` | picker: choose a delegate principal | required | — | — | shows names, sends the id | A principal id, resolved to a name the same way as `delegatorPrincipalId`. | `createApprovalDelegation` body |
| Kinds `kinds` | multi-select chips | optional | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry … | — | Absent means everything the delegator may approve. | `createApprovalDelegation` body |
| Max amount `maxAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | A delegate may be given less authority than the delegator, never more. | `createApprovalDelegation` body |
| From `from` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createApprovalDelegation` body |
| To `to` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Required. An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it. | `createApprovalDelegation` body |
| Reason `reason` | text area | optional | — | — | — | — | `createApprovalDelegation` body |
| Scope path `scopePath` | text field | optional | — | — | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row … | `createApprovalDelegation` body |

**Sent by *Save approval SLA*** (`setApprovalSlaPolicy`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `setApprovalSlaPolicy` body |
| Code `code` | text field | required | — | — | — | — | `setApprovalSlaPolicy` body |
| Applies to request kinds `appliesToRequestKinds` | multi-select chips | optional | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry … | — | — | `setApprovalSlaPolicy` body |
| Target minutes `targetMinutes` | number field (minutes) | optional | — | — | — | — | `setApprovalSlaPolicy` body |
| Business hours only `businessHoursOnly` | toggle | optional | on | — | — | A four-hour SLA starting at five in the afternoon is breached by nine the next morning with nobody having done anything wrong. | `setApprovalSlaPolicy` body |
| Calendar `calendarId` | picker: choose a calendar | optional | — | — | shows names, sends the id | — | `setApprovalSlaPolicy` body |
| Reminders `reminders` | repeatable rows | optional | — | — | — | — | `setApprovalSlaPolicy` body |
| At percent of target `reminders[].atPercentOfTarget` | number field | optional | — | — | — | — | `setApprovalSlaPolicy` body |
| Notify `reminders[].notify` | radio group | optional | — | Approver · Approver manager · Requester · Escalation group | — | — | `setApprovalSlaPolicy` body |
| First reminder at percent `firstReminderAtPercent` | stepper or slider | optional | — | min 1; max 100 | — | Percent of `targetMinutes` at which the first reminder goes (decided 29 September, readiness close-out: the reminder steps are percentages of target). | `setApprovalSlaPolicy` body |
| Second reminder at percent `secondReminderAtPercent` | stepper or slider | optional | — | min 1; max 100 | — | Percent of `targetMinutes` at which the second reminder goes; above `firstReminderAtPercent` | `setApprovalSlaPolicy` body |
| Escalate at percent `escalateAtPercent` | stepper or slider | optional | — | min 1; max 100 | — | Percent of `targetMinutes` at which the request or workflow escalates; at or above `secondReminderAtPercent` | `setApprovalSlaPolicy` body |
| On breach `onBreach` | radio group | optional | Escalate | Notify only · Escalate · Auto approve · Auto reject | — | — | `setApprovalSlaPolicy` body |
| Auto action allowed `autoActionAllowed` | toggle | optional | off | — | — | Auto-approval on breach is off unless somebody says otherwise, in writing. A queue that approves itself when nobody looks is not an approval process. | `setApprovalSlaPolicy` body |
| Escalation group `escalationGroupId` | picker: choose an escalation group | optional | — | — | shows names, sends the id | — | `setApprovalSlaPolicy` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setApprovalSlaPolicy` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setApprovalSlaPolicy: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/approvals.yaml#setApprovalSlaPolicy)*
- **Delegation window and limits**: Always time-bounded: 'to' must follow 'from' (refused invalidWindow); the delegate cannot exceed the delegator's kinds or maxAmount and must hold the permission (exceedsDelegatorAuthority, delegateLacksPermission); a delegate never approves a request the delegator raised. *(source: contracts/spine/approvals.yaml#createApprovalDelegation)*

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Detail panel** (detail panel, from `getActionPlan`): One record, read-only.

| Shows | Format | Notes |
|---|---|---|
| Plan | grouped details | A plan: plan, validate, simulate, approve, execute, with rollback (design 2.2 D, 3.8; AIC-086..107). |
| ID | the name it points at, never the id | — |
| Origin | chip: Configuration session, Generate configuration, Assistant, Risk case, Operational … | — |
| Origin ref | text | — |
| Summary | text | — |
| Status | chip: Draft, Validated, Simulated, Awaiting approval, Approved, Executing… | — |
| Autonomy level | 1,234 | One autonomy scale for every capability (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). |
| Approval tier | 1,234 | The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). |
| Approval request | the name it points at, never the id | The `approvals` request, where tier 2 or the matrix caught the plan. |
| Proposed action | the name it points at, never the id | The `ai.proposed_action` the plan is presented as for a decision. |
| Change set hash | text | — |
| Governance outcome | chip: Allow, Allow with conditions, Prepare only, Approval required, Escalate, Block | What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). |
| Policy version ref | text | The governance policy version that decided it. |
| Simulation | grouped details | Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4). |
| Partial completion allowed | yes / no (icon or chip) | Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134). |
| Rollback of plan | the name it points at, never the id | — |
| Requested by principal | the name it points at, never the id | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Steps | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |

**Data table** (data table, from `listProposedActions`): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Interaction | the name it points at, never the id | — |
| Kind | chip: Pricing, Promotion, Operational, Financial, Configuration, Content… | `content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from … |
| Target contract | text | Which contract would perform it. The assistant never performs it itself. |
| Target operation | text | — |
| Payload | grouped details | The request body a person would submit, ready to review. Open on purpose: its shape is the request body of `targetOperation` in … |
| Summary | text | — |
| Status | chip: Proposed, Approved, Rejected, Applied, Expired | Expiry (decided 28 September, audit R213): a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires … |
| Expires at | 1 Oct 2026, 14:30 | When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once … |
| Approval level | 1,234 | 8.3.65. Multi-level, because a discount and a pricing change differ in authority. |
| Decided by principal | the name it points at, never the id | — |
| Decision reason | text | Required on rejection. The only signal the assistant is proposing badly, and without it a poor model degrades silently. |
| Proposed at | 1 Oct 2026, 14:30 | — |
| Decided at | 1 Oct 2026, 14:30 | — |
| Plan | the name it points at, never the id | The plan this action presents for a decision (AI design 2.2 D, 3.8). |
| Approval request | the name it points at, never the id | The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3). |
| Change set hash | text | Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181). |

**Delegations in force** (data table, from `listApprovalDelegations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Delegator principal | the name it points at, never the id | A principal id (`identity.Principal.id`). This contract stores the id only; the name to show, and the people to pick from, come from … |
| Delegate principal | the name it points at, never the id | A principal id, resolved to a name the same way as `delegatorPrincipalId`. |
| Kinds | list or chips (count when long) | Absent means everything the delegator may approve. |
| Max amount | AED 1,234.50 | A delegate may be given less authority than the delegator, never more. |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | Required. An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it. |
| Reason | text | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Escalate (secondary button) | `escalateApprovalRequest` POST `/approval-requests/{requestId}/escalate` | inline | ApprovalRequest | — | — |
| Delegate (secondary button) | `createApprovalDelegation` POST `/delegations` | ApprovalDelegation | ApprovalDelegation | 400 The delegation is malformed. `refusedReason` is `invalidWindow` where `to` is not after `from`, or `delegateIsDelegator` where both principals are the same … (DelegationRefusedProblem); 403 The delegation would hand … | — |
| Save approval SLA (secondary button) | `setApprovalSlaPolicy` PUT `/approval-sla-policies` | ApprovalSlaPolicy | ApprovalSlaPolicy | — | — |

**Data it reads**: `listProposedActions` (onLoad, What the assistant has proposed and nobody has decided); `listApprovalDelegations` (onLoad, Who is acting for whom); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The escalation delegation approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the escalation delegation approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No escalation delegation approval yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the escalation delegation approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_DECIDE`, `APPROVAL_REQUEST`, `APPROVAL_VIEW`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The delegation is malformed. `refusedReason` is `invalidWindow` where `to` is not after `from`, or `delegateIsDelegator` where both principals are the same … (DelegationRefusedProblem); 400 Validation failed |

#### Edge cases to draw

- **Can read but not change (holds AI_USE, APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_REQUEST for Escalate; APPROVAL_DECIDE for Delegate; APPROVAL_CONFIGURE for Save approval SLA. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#escalateApprovalRequest)*
- **createApprovalDelegation answers 403**: Show it as something the person can act on, not a failure: The delegation would hand over authority that is not there. `refusedReason` is `delegateLacksPermission` where the delegate does not hold the permission being delegated, or `exceedsDelegatorAuthority` where `kinds` or `maxAmount` go beyond what the delegator may approve. The shared `Forbidden`, with no `refusedReason`, is the ca... *(source: contracts/spine/approvals.yaml#createApprovalDelegation)*

#### Consistency with other screens

- Match `BO-087`: Delegations are the same objects.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listProposedActions (ProposedAction):
- kind: standard
  summary: Guest charged twice at Main Gate Till 3
  status: active
  expiresAt: 31/12/2026 23:59
  approvalLevel: 12
- kind: standard
  summary: Group of 40 from Desert Gate Tours
  status: pending
  expiresAt: 15/10/2026 00:00
  approvalLevel: 3
```

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `listProposedActions` → `AI_USE` (operate) · staff
- `listApprovalDelegations` → `APPROVAL_VIEW` (read) · staff
- `escalateApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff
- `createApprovalDelegation` → `APPROVAL_DECIDE` (operate) · staff
- `setApprovalSlaPolicy` → `APPROVAL_CONFIGURE` (configure) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.47 | Multi-Level Escalation - System shall support escalation through multiple organizational levels. | Approval Workflows & Governance | CONTRACTED | `escalateApprovalRequest` |
| 11.1.48 | Escalation History - System shall maintain complete escalation history. | Approval Workflows & Governance | CONTRACTED | `escalateApprovalRequest` |
| 11.1.8 | Approval Delegation - System shall allow approvers to delegate approval authority to designated users. | Approval Workflows & Governance | CONTRACTED | `createApprovalDelegation` |
| 11.1.9 | Temporary Delegation - System shall support delegation periods with automatic expiration. | Approval Workflows & Governance | CONTRACTED | `createApprovalDelegation` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI actions route through the shared approval matrix: the screen shows the approver's limit for the kind and amount and whether the action is within it or must escalate; escalation, delegation and SLA apply as to any approval. *(agreed · MoM 18 Sep 2026, M18-02 · DI-956)*
- SLA rules set how fast a request must be approved (e.g. within one day); if not actioned it auto-escalates to the next level so someone can investigate (e.g. approver on leave) and reassign. *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-724)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-534` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-534`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 10: Works in Escalation, Delegation & Approval SLA Management → Ensure AI approvals do not remain indefinitely pending and provide controlled routing when approvers are unavailable or additional authority is required.

#### Acceptance for the design

- [ ] Every input above is drawn (31), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (52 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-534?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Escalate, Delegate, Save approval SLA.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_DECIDE`, `APPROVAL_REQUEST`, `APPROVAL_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-535` Live AI Execution Oversight & Human Intervention

**Allow authorized humans to monitor and intervene after an AI-driven action has been approved and entered execution. This is different from approval.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-535 |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (3 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§High-impact intervention should show) and no metric row |
| Offline | online only |
| Opens with | `planId` (navigation), `tenantId` (navigation) |
| Route | `/platform/live-ai-execution-oversight-human-intervention-adm-535` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getActionPlan` (AI_USE), `pauseActionPlan` (AI_APPROVE), `resumeActionPlan` (AI_APPROVE), `cancelActionPlan` (AI_USE), `rollbackActionPlan` (AI_APPROVE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the AI & Intelligence process.** Live oversight after approval: watch an AI-driven process step by step (the configuration assistant creating a venue, then products, then performances) and intervene - pause, resume, cancel, roll back. The one thing to get right: before each intervention the impact is stated - "completed objects remain; 4 actions will remain pending; no active transaction affected".

**Known correction pending (do not draw the wrong version)**

- **The pause impact sentences are table columns.** Why: They are the content of the pause confirmation. *(source: screens/P09-platform-admin-console.yaml#ADM-535; AI & Intelligence)*
- **cancelActionPlan needs only AI_USE while pause needs AI_APPROVE.** Why: Cancelling an executing plan is at least as consequential as pausing it; align the permission. *(source: contracts/satellite/ai.yaml#cancelActionPlan / contracts/satellite/ai.yaml#pauseActionPlan; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_APPROVE`, `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Sent by *Pause*** (`pauseActionPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `pauseActionPlan` body |

**Sent by *Resume*** (`resumeActionPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 1000 | — | — | `resumeActionPlan` body |

**Sent by *Cancel plan*** (`cancelActionPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `cancelActionPlan` body |

**Sent by *Roll back*** (`rollbackActionPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `rollbackActionPlan` body |
| Prefer forward fix `preferForwardFix` | toggle | optional | off | — | — | — | `rollbackActionPlan` body |

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Every live execution oversight** (data table, from `getActionPlan`)

| Shows | Format | Notes |
|---|---|---|
| Impact of pausing | text | not in the schema: `Impact of Pausing` |
| Completed objects remain | text | not in the schema: `Completed objects remain` |
| 4 actions will remain pending | text | not in the schema: `4 actions will remain pending` |
| No active transaction affected | text | not in the schema: `No active transaction affected` |
| Emergency stop | text | not in the schema: `Emergency Stop` |
| Emergency stop AI execution | text | not in the schema: `Emergency Stop AI Execution` |
| Authorized role | text | not in the schema: `Authorized Role` |
| Reason | text | not in the schema: `Reason` |
| Confirmation | text | not in the schema: `Confirmation` |
| Audit record | text | not in the schema: `Audit Record` |

**The selected live execution oversight** (detail panel, from `getActionPlan`): The pack groups this record's detail under its own headings: “Approval answers”, “Step Action Module Status”, “Administrator notices”.

| Shows | Format | Notes |
|---|---|---|
| Impact of pausing | text | not in the schema: `Impact of Pausing` |
| Completed objects remain | text | not in the schema: `Completed objects remain` |
| 4 actions will remain pending | text | not in the schema: `4 actions will remain pending` |
| No active transaction affected | text | not in the schema: `No active transaction affected` |
| Emergency stop | text | not in the schema: `Emergency Stop` |
| Emergency stop AI execution | text | not in the schema: `Emergency Stop AI Execution` |
| Authorized role | text | not in the schema: `Authorized Role` |
| Reason | text | not in the schema: `Reason` |
| Confirmation | text | not in the schema: `Confirmation` |
| Audit record | text | not in the schema: `Audit Record` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Pause (secondary button) | `pauseActionPlan` POST `/action-plans/{planId}/pause` | inline | AiActionPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The plan is not executing. | — |
| Resume (secondary button) | `resumeActionPlan` POST `/action-plans/{planId}/resume` | inline | AiActionPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not resumable: the plan is not paused (`plan-not-paused`), or a target object changed since planning … | — |
| Cancel plan (destructive button) | `cancelActionPlan` POST `/action-plans/{planId}/cancel` | inline | AiActionPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The plan is already finished. | — |
| Roll back (destructive button) | `rollbackActionPlan` POST `/action-plans/{planId}/rollback` | inline | AiActionPlanDetail | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Nothing to roll back: the plan has no completed step (`plan-not-applied`). | — |

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Pause / Resume / Cancel / Roll back**: Each with a confirmation stating its impact; rollback plans compensating steps in reverse dependency order and is approved like any plan. *(source: contracts/satellite/ai.yaml#pauseActionPlan / contracts/satellite/ai.yaml#rollbackActionPlan / DI-972)*

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

**What opens over it**

- confirmDialog *Cancel plan*: **Names the plan, the steps already executed and what stays applied**: cancelling stops the remaining steps; it does not undo the executed ones (that is Roll back).
- confirmDialog *Roll back*: **Names each executed step and its compensation**, and that the rollback plan goes for approval before it runs.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The live execution oversight list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live execution oversight untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live execution oversight yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the live execution oversight are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_APPROVE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Not resumable: the plan is not paused (`plan-not-paused`), or a target object changed since planning (`plan-drifted`).; 409 Nothing to roll back: the plan has no completed step (`plan-not-applied`).; 409 The plan is already finished. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
impactOfPausing:
- Completed objects remain
- 4 actions will remain pending
- No active transaction affected
```

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `pauseActionPlan` → `AI_APPROVE` (operate) · staff
- `resumeActionPlan` → `AI_APPROVE` (operate) · staff
- `cancelActionPlan` → `AI_USE` (operate) · staff
- `rollbackActionPlan` → `AI_APPROVE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Roll back on partial failure: plans the compensating steps in reverse dependency order, approved like any plan. *(agreed · MoM 21 Sep 2026, M21-12 · DI-972)*
- AI actions in progress are shown step by step in an AI action command center; if a process only partly completes (e.g. missing information) it rolls back rather than leaving a product half-configured, and a full change history records everything AI modified. *(client request · MoM 21 Sep 2026, 4.9 Core AI Platform — AI Tools, Agents & Action Orchestration · DI-965)*
- Live AI execution oversight lets a user watch an in-progress AI process step by step (e.g. the configuration assistant creating a venue, then products, then performances), and an authorised person can reject, modify or replace an AI decision at any point, with full intervention history. *(client request · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-933)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-535` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-535`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 12: Works in Live AI Execution Oversight & Human Intervention → Allow authorized humans to monitor and intervene after an AI-driven action has been approved and entered execution. This is different from approval.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-535?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Pause, Resume, Cancel plan, Roll back.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-536` Human Override & Manual Control Center

**Provide controlled mechanisms for humans to override an AI recommendation or take control when AI output is inappropriate. Human override should always be possible where governance requires it.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-536 |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_AUDIT_VIEW`, `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (3 operate, 2 read, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `capabilityKey` (navigation), `decisionRecordId` (navigation), `planId` (navigation), `tenantId` (navigation) |
| Route | `/platform/human-override-manual-control-center-adm-536` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `pauseAiCapability` (AI_CONFIGURE), `resumeAiCapability` (AI_APPROVE), `pauseActionPlan` (AI_APPROVE), `overrideAiDecision` (AI_APPROVE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Human override and manual control: the kill switch for an AI capability, the pause on an executing plan, and the override of a single AI decision - always possible where governance requires it. Stopping is always safe and needs less authority than starting again. The one thing to get right: before pausing, the person sees exactly what the capability will do instead (its degradation mode); after an override, the original and the human decision stay side by side.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- In Block A only resumeAiCapability is in the slice; pauseAiCapability is not. (CHG-SBO-006)
- The layout has only an unlabelled primary button and Cancel. (CHG-SBO-005)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |
| Family | select | — | Gateway and models · Governance · Action pipeline · Knowledge retrieval · Assistants · Analytics insights · Configuration assistant · Forecasting · Anomaly detection · Risk intelligence · Recommendations · Decision records … | `listAiCapabilities` ?family |
| Status | segmented control | — | Active · Paused | `listAiCapabilities` ?status |
| Risk class | radio group | — | Low · Medium · High · Critical | `listAiCapabilities` ?riskClass |
| Capability key | text field | — | — | `searchAiDecisions` ?capabilityKey |
| Outcome | select | — | Answered · Refused · Allowed · Blocked · Executed · Failed · Approved then failed · Published · Suggested | `searchAiDecisions` ?outcome |
| Subject ref | text field | — | — | `searchAiDecisions` ?subjectRef |
| Trace | text field | — | — | `searchAiDecisions` ?traceId |
| Policy version | text field | — | — | `searchAiDecisions` ?policyVersion |
| Model version | text field | — | — | `searchAiDecisions` ?modelVersion |
| From | date and time picker | — | — | `searchAiDecisions` ?from |
| To | date and time picker | — | — | `searchAiDecisions` ?to |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_APPROVE`, `AI_CONFIGURE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Pause capability** (modal, opened by *Pause capability*; *Pause capability* calls `pauseAiCapability`, *Cancel* sends nothing)

**Collects what `pauseAiCapability` sends before it is called.** Required: `reason`. Optional: `incidentId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `pauseAiCapability` body |
| Incident `incidentId` | picker: choose an incident | optional | — | — | shows names, sends the id | — | `pauseAiCapability` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already paused.

**Form: Resume capability** (modal, opened by *Resume capability*; *Resume capability* calls `resumeAiCapability`, *Cancel* sends nothing)

**Collects what `resumeAiCapability` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `resumeAiCapability` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not paused.

**Form: Pause plan** (modal, opened by *Pause plan*; *Pause plan* calls `pauseActionPlan`, *Cancel* sends nothing)

**Collects what `pauseActionPlan` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `pauseActionPlan` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The plan is not executing.

**Form: Override decision** (modal, opened by *Override decision*; *Override decision* calls `overrideAiDecision`, *Cancel* sends nothing)

**Collects what `overrideAiDecision` sends before it is called.** Required: `humanDecision`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Human decision `humanDecision` | key and value settings | required | — | — | — | — | `overrideAiDecision` body |
| Reason `reason` | text area | required | — | max length 2000 | — | — | `overrideAiDecision` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **pause reason / incident**: Reason required; optionally link an open AI incident. *(source: contracts/satellite/ai.yaml#pauseAiCapability)*
- **override (humanDecision, reason)**: The human decision is the replacement answer (e.g. "keep price at AED 199"), reason required; it changes what AI does next and does not reach into the owning module. *(source: contracts/satellite/ai.yaml#overrideAiDecision)*

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**AI capabilities** (data table, from `listAiCapabilities`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Family | chip: Gateway and models, Governance, Action pipeline, Knowledge retrieval, Assistants … | The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point … |
| Status | chip: Active, Paused | Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed. |
| Autonomy level | 1,234 | The level in force at this scope. At most `autonomyCeiling`. |
| Paused reason | text | — |
| Paused at | 1 Oct 2026, 14:30 | — |

**Action plan** (detail panel, from `getActionPlan`): Opened by `planId` from the oversight screens; no list of plans exists yet (logged, CHG-SBO-005).

| Shows | Format | Notes |
|---|---|---|
| Plan | grouped details | A plan: plan, validate, simulate, approve, execute, with rollback (design 2.2 D, 3.8; AIC-086..107). |
| ID | the name it points at, never the id | — |
| Origin | chip: Configuration session, Generate configuration, Assistant, Risk case, Operational … | — |
| Origin ref | text | — |
| Summary | text | — |
| Status | chip: Draft, Validated, Simulated, Awaiting approval, Approved, Executing… | — |
| Autonomy level | 1,234 | One autonomy scale for every capability (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). |
| Approval tier | 1,234 | The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). |
| Approval request | the name it points at, never the id | The `approvals` request, where tier 2 or the matrix caught the plan. |
| Proposed action | the name it points at, never the id | The `ai.proposed_action` the plan is presented as for a decision. |
| Change set hash | text | — |
| Governance outcome | chip: Allow, Allow with conditions, Prepare only, Approval required, Escalate, Block | What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). |
| Policy version ref | text | The governance policy version that decided it. |
| Simulation | grouped details | Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4). |
| Partial completion allowed | yes / no (icon or chip) | Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134). |
| Rollback of plan | the name it points at, never the id | — |
| Requested by principal | the name it points at, never the id | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Steps | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |

**Find the decision** (data table, from `searchAiDecisions`)

| Shows | Format | Notes |
|---|---|---|
| Capability key | text | — |
| Task | text | — |
| Subject ref | text | — |
| Outcome | chip: Answered, Refused, Allowed, Blocked, Executed, Failed… | `approvedThenFailed` is kept distinct from `executed` (design 1.2 Audit). |
| Governance outcome | chip: Allow, Allow with conditions, Prepare only, Approval required, Escalate, Block | What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). |
| Created at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Pause capability (destructive button) | `pauseAiCapability` POST `/governance/capabilities/{capabilityKey}/pause` | inline | AiCapabilityRegistration | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already paused. | opens modal first |
| Resume capability (secondary button) | `resumeAiCapability` POST `/governance/capabilities/{capabilityKey}/resume` | inline | AiCapabilityRegistration | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not paused. | opens modal first |
| Pause plan (secondary button) | `pauseActionPlan` POST `/action-plans/{planId}/pause` | inline | AiActionPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The plan is not executing. | opens modal first |
| Override decision (primary button) | `overrideAiDecision` POST `/decision-records/{decisionRecordId}/override` | inline | AiIntervention | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **capability status**: Active or Paused (by whom, when, why), with the degradation mode in words, e.g. "Recommendations paused - checkout shows no offers", "Fraud scoring paused - owners' rules still apply", "Concierge paused - guests are offered a person". *(source: contracts/satellite/ai.yaml#pauseAiCapability)*
- **decision side by side**: Original AI decision and human decision as two columns with the reason and the person; marked as an intervention on the decision record. *(source: contracts/satellite/ai.yaml#overrideAiDecision)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Pause capability (kill switch)**: Immediate; in-flight plans pause at their next checkpoint; confirmation states the degradation mode. AI_CONFIGURE. *(source: contracts/satellite/ai.yaml#pauseAiCapability)*
- **Resume capability**: Needs AI_APPROVE (more than pausing). Plans paused by the pause stay paused and are resumed one by one after revalidation - say so in the confirmation. *(source: contracts/satellite/ai.yaml#resumeAiCapability)*
- **Pause plan**: The executor stops at the next step boundary; nothing half-applies; recorded as an intervention. *(source: contracts/satellite/ai.yaml#pauseActionPlan)*
- **Override decision**: Recorded side by side; a link to the owning module where the person must make the actual correction. *(source: contracts/satellite/ai.yaml#overrideAiDecision)*

**Data it reads**: `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …); `listAiCapabilities` (onLoad, The capabilities with their status, to pause or resume one); `getActionPlan` (onLoad, The plan opened by its id, to pause it); `searchAiDecisions` (onLoad, Find the decision to override)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The human override manual list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the human override manual untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No human override manual yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the human override manual are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_APPROVE`, `AI_CONFIGURE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Already paused.; 409 Not paused.; 409 The plan is not executing. |

#### Edge cases to draw

- **Person with AI_CONFIGURE but not AI_APPROVE after pausing**: Resume is visible but disabled with "Resuming needs AI approval rights". *(source: contracts/satellite/ai.yaml#resumeAiCapability)*

#### Consistency with other screens

- Match `ADM-535`: Live execution oversight shows the same plan states and the same pause.
- Match `ADM-556`: Containment of an incident pauses capabilities through the same operation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
capability:
  key: recommend.checkout
  status: Paused
  by: Priya Nair
  at: Thu 1 Oct 14:22
  reason: Offers showing sold-out cabanas
  degradation: Checkout shows no offers
override:
  decision: Suggested Adult Day Pass +12% for Sat 3 Oct
  human: Keep AED 199.00
  reason: Price ceiling agreed with the group commercial director
```

#### Permissions

- `pauseAiCapability` → `AI_CONFIGURE` (configure) · staff
- `resumeAiCapability` → `AI_APPROVE` (operate) · staff
- `pauseActionPlan` → `AI_APPROVE` (operate) · staff
- `overrideAiDecision` → `AI_APPROVE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `listAiCapabilities` → `AI_USE` (operate) · staff
- `getActionPlan` → `AI_USE` (operate) · staff
- `searchAiDecisions` → `AI_AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.6 | AI-based Dynamic Pricing Promotion | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.2.58 | System shall maintain forecasting audit logs. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.3.53 | System shall maintain fraud audit trails. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.6.29 | System shall support recommendation audit trails. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live AI execution oversight lets a user watch an in-progress AI process step by step (e.g. the configuration assistant creating a venue, then products, then performances), and an authorised person can reject, modify or replace an AI decision at any point, with full intervention history. *(client request · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-933)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-536` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-536`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 14: Works in Human Override & Manual Control Center → Provide controlled mechanisms for humans to override an AI recommendation or take control when AI output is inappropriate. Human override should always be possible where governance requires it.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (38 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-536?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Pause capability, Resume capability, Pause plan, Override decision.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_AUDIT_VIEW`, `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-537` Approval & Intervention History / Decision Timeline

**Provide complete operational history of human involvement in AI activity. This is the human-oversight timeline; Board 3 will later provide deeper enterprise AI explainability and audit.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-537 |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionRecordId` (navigation), `tenantId` (navigation) |
| Route | `/platform/approval-intervention-history-decision-timeline-adm-537` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `searchAiDecisions` (AI_AUDIT_VIEW), `getAiDecisionTrace` (AI_AUDIT_VIEW) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** The human-oversight timeline: every approval, rejection, condition, challenge, override, pause and rollback, searchable by capability, user, approver, module, decision, risk and venue. The one thing to get right: each entry opens the full decision trace.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Search approval intervention history | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by ai capability, user, approver, module, decision, risk and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Capability key | text field | — | — | `searchAiDecisions` ?capabilityKey |
| Outcome | select | — | Answered · Refused · Allowed · Blocked · Executed · Failed · Approved then failed · Published · Suggested | `searchAiDecisions` ?outcome |
| Subject ref | text field | — | — | `searchAiDecisions` ?subjectRef |
| Trace | text field | — | — | `searchAiDecisions` ?traceId |
| Policy version | text field | — | — | `searchAiDecisions` ?policyVersion |
| Model version | text field | — | — | `searchAiDecisions` ?modelVersion |
| From | date and time picker | — | — | `searchAiDecisions` ?from |
| To | date and time picker | — | — | `searchAiDecisions` ?to |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_AUDIT_VIEW` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **timeline**: Time, capability, action, human decision, by whom, reason; link to trace. *(source: contracts/satellite/ai.yaml#searchAiDecisions / contracts/satellite/ai.yaml#getAiDecisionTrace)*

**Data it reads**: `searchAiDecisions` (onLoad, Find AI decisions); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval intervention history list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval intervention history untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval intervention history yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval intervention history are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_AUDIT_VIEW`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entry:
  when: 2 Oct 11:05
  capability: Configuration assistant
  action: Price change Adult weekend
  decision: Approved with condition ≤ +5%
  by: Priya Nair
```

#### Permissions

- `searchAiDecisions` → `AI_AUDIT_VIEW` (read) · staff
- `getAiDecisionTrace` → `AI_AUDIT_VIEW` (read) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.6 | AI-based Dynamic Pricing Promotion | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.2.58 | System shall maintain forecasting audit logs. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.3.53 | System shall maintain fraud audit trails. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.6.29 | System shall support recommendation audit trails. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live AI execution oversight lets a user watch an in-progress AI process step by step (e.g. the configuration assistant creating a venue, then products, then performances), and an authorised person can reject, modify or replace an AI decision at any point, with full intervention history. *(client request · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-933)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-537` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-537`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 16: Works in Approval & Intervention History / Decision Timeline → Provide complete operational history of human involvement in AI activity. This is the human-oversight timeline; Board 3 will later provide deeper enterprise AI explainability and audit.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-537?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-538` Human Oversight Workflow Simulator & Readiness Center

**Allow Soft Labs/TICVAI administrators to test the entire human-in-the-loop workflow before activating it in production.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-538 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Board 1 defines) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `planId` (navigation), `versionId` (navigation), `tenantId` (navigation) |
| Route | `/platform/human-oversight-workflow-simulator-readiness-center-adm-538` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `simulateAiGovernancePolicy` (AI_CONFIGURE), `simulateActionPlan` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: but Operations Assistant lacks Pricing approval rights,. Each needs an operation, or needs removing from …

**From the AI & Intelligence process.** Test the whole human-in-the-loop workflow before switching it on in production: pick a scenario (risk, autonomy, permissions, data use, policy) and see what the decision point decides and who would approve. The one thing to get right: the boundary with owning modules - e.g. the operations assistant may prepare a price change but lacks pricing approval rights, so it routes to a commercial approver.

**Known correction pending (do not draw the wrong version)**

- **A sentence fragment is a button label ("but Operations Assistant lacks Pricing approval rights,").** Why: Board text. *(source: screens/P09-platform-admin-console.yaml#ADM-538; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Risk | select field | — | — | — | — | — | — |
| Autonomy | select field | — | — | — | — | — | — |
| AI permissions | select field | — | — | — | — | — | — |
| Data usage | select field | — | — | — | — | — | — |
| Policy | select field | — | — | — | — | — | — |
| Governance decision | select field | — | — | — | — | — | — |
| Important Boundary — Owning Modules | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_CONFIGURE`, `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| but Operations Assistant lacks Pricing approval rights, (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **walk-through**: Step list as on ADM-527 ending in the governance decision and the routed approvers. *(source: contracts/satellite/ai.yaml#simulateAiGovernancePolicy / contracts/satellite/ai.yaml#simulateActionPlan)*

**Data it reads**: `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The human oversight workflow configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the human oversight workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No human oversight workflow configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The plan is executing or finished; simulate a rollback plan instead.; 409 The version is not a draft (already published or superseded). |

#### Consistency with other screens

- Match `ADM-527`: Same step-list component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scenario:
  risk: High
  autonomy: L2 Prepare
  permission: Operations assistant lacks pricing approval rights
  decision: Prepare only - route to Commercial manager
```

#### Permissions

- `simulateAiGovernancePolicy` → `AI_CONFIGURE` (configure) · staff
- `simulateActionPlan` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-538` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-538`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 18: Works in Human Oversight Workflow Simulator & Readiness Center → Allow Soft Labs/TICVAI administrators to test the entire human-in-the-loop workflow before activating it in production.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-538?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, but Operations Assistant lacks Pricing ….
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P09 reference designs** (from `handoff/design-batches/apps/6-ticvai-controller/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P09 TICVAI Web

- Portal access exposes TICVAI pricing, so prospects submit contact details and a trade license as proof of a real venue, reviewed and approved by TICVAI before access is granted. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-827)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

### In P09 · Platform

- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*

**13 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cancelActionPlan": {"method":"POST","path":"/action-plans/{planId}/cancel","contract":"ai","summary":"Cancel a plan","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlan"},
"createAiGovernancePolicyDraft": {"method":"POST","path":"/governance/policy-drafts","contract":"ai","summary":"Draft a governance policy, or a new version of one","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiGovernancePolicyVersion"},
"createApprovalDelegation": {"method":"POST","path":"/delegations","contract":"approvals","summary":"Delegate approval authority","permission":"APPROVAL_DECIDE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalDelegation","responds":"ApprovalDelegation"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"escalateApprovalRequest": {"method":"POST","path":"/approval-requests/{requestId}/escalate","contract":"approvals","summary":"Move it up a level","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequest"},
"evaluateApprovalRequirement": {"method":"POST","path":"/approval-requests/evaluate","contract":"approvals","summary":"Does this need approval, and from whom","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequirement"},
"getActionPlan": {"method":"GET","path":"/action-plans/{planId}","contract":"ai","summary":"A plan with its steps","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiActionPlanDetail"},
"getAiDecisionTrace": {"method":"GET","path":"/decision-records/{decisionRecordId}/trace","contract":"ai","summary":"The full trace of a decision","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"depth","in":"query","required":null}],"requestBody":null,"responds":"AiDecisionTrace"},
"listAiCapabilities": {"method":"GET","path":"/governance/capabilities","contract":"ai","summary":"The capability registry","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"family","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"riskClass","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiGovernancePolicyVersions": {"method":"GET","path":"/governance/policy-versions","contract":"ai","summary":"Governance policies and their versions","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"policyId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiTools": {"method":"GET","path":"/tools","contract":"ai","summary":"The tool registry","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"targetContract","in":"query","required":null},{"name":"effect","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listApprovalDelegations": {"method":"GET","path":"/delegations","contract":"approvals","summary":"Who is standing in for whom","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ApprovalDelegation"},
"listApprovalMatrices": {"method":"GET","path":"/approval-matrices","contract":"approvals","summary":"What requires approval here","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"effective","in":"query","required":null}],"requestBody":null,"responds":"ApprovalMatrix"},
"listOwnPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants/mine","contract":"identity","summary":"The calling platform operator's own grants into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProposedActions": {"method":"GET","path":"/proposed-actions","contract":"ai","summary":"What the assistant has proposed and nobody has decided","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProposedAction"},
"listTenants": {"method":"GET","path":"/tenants","contract":"subscription","summary":"List tenants","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"planId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"overrideAiDecision": {"method":"POST","path":"/decision-records/{decisionRecordId}/override","contract":"ai","summary":"Override an AI decision","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiIntervention"},
"pauseActionPlan": {"method":"POST","path":"/action-plans/{planId}/pause","contract":"ai","summary":"Pause an executing plan","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlan"},
"pauseAiCapability": {"method":"POST","path":"/governance/capabilities/{capabilityKey}/pause","contract":"ai","summary":"Stop a capability now","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiCapabilityRegistration"},
"resumeActionPlan": {"method":"POST","path":"/action-plans/{planId}/resume","contract":"ai","summary":"Resume a paused plan","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlan"},
"resumeAiCapability": {"method":"POST","path":"/governance/capabilities/{capabilityKey}/resume","contract":"ai","summary":"Resume a paused capability","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiCapabilityRegistration"},
"rollbackActionPlan": {"method":"POST","path":"/action-plans/{planId}/rollback","contract":"ai","summary":"Plan a rollback","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"searchAiDecisions": {"method":"GET","path":"/decision-records","contract":"ai","summary":"Find AI decisions","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"capabilityKey","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"traceId","in":"query","required":null},{"name":"policyVersion","in":"query","required":null},{"name":"modelVersion","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"sendAiMessage": {"method":"POST","path":"/conversations/{conversationId}/messages","contract":"ai","summary":"Ask","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiMessage"},
"setApprovalMatrix": {"method":"PUT","path":"/approval-matrices","contract":"approvals","summary":"Configure what requires approval","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalMatrix","responds":"ApprovalMatrix"},
"setApprovalSlaPolicy": {"method":"PUT","path":"/approval-sla-policies","contract":"approvals","summary":"How long a decision may take, and what happens when it does not","permission":"APPROVAL_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalSlaPolicy","responds":"ApprovalSlaPolicy"},
"simulateActionPlan": {"method":"POST","path":"/action-plans/{planId}/simulate","contract":"ai","summary":"Validate and simulate a plan without changing anything","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlanDetail"},
"simulateAiGovernancePolicy": {"method":"POST","path":"/governance/policy-versions/{versionId}/simulate","contract":"ai","summary":"Test a draft policy before it is published","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiPolicySimulation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiActionPlan": {"type":"object","x-ticvai-persistence":"ai.action_plan","description":"**A plan: plan, validate, simulate, approve, execute, with rollback** (design 2.2 D, 3.8; AIC-086..107). Independent of any conversation (AIC-102). Its steps are `ai.action_step`; the change set is hashed so what was approved is what runs (AIC-181).","required":["origin","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"origin":{"type":"string","enum":["configurationSession","generateConfiguration","assistant","riskCase","operationalRequirement","rollback"]},"originRef":{"type":"string","nullable":true},"summary":{"type":"string"},"status":{"type":"string","enum":["draft","validated","simulated","awaitingApproval","approved","executing","paused","completed","partiallyCompleted","failed","compensated","cancelled","rolledBack"],"readOnly":true},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"approvalTier":{"type":"integer","minimum":1,"maximum":2,"description":"The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). Not an autonomy level."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request, where tier 2 or the matrix caught the plan."},"proposedActionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.proposed_action","description":"The `ai.proposed_action` the plan is presented as for a decision."},"changeSetHash":{"type":"string","readOnly":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"readOnly":true},"policyVersionRef":{"type":"string","readOnly":true,"description":"The governance policy version that decided it."},"simulation":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4)."},"partialCompletionAllowed":{"type":"boolean","default":false,"description":"Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134)."},"rollbackOfPlanId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.action_plan"},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiActionPlanDetail": {"type":"object","x-ticvai-persistence":"none — ai.action_plan with its ai.action_step rows","description":"A plan with its steps in DAG order.","required":["plan","steps"],"properties":{"plan":{"$ref":"#/components/schemas/AiActionPlan"},"steps":{"type":"array","items":{"$ref":"#/components/schemas/AiActionStep"}}}},
"AiActionStep": {"type":"object","x-ticvai-persistence":"ai.action_step","description":"One step of a plan: a registered tool against `targetContract.targetOperation` at a contract version (AIC-095), with payload, provenance, compensation and the idempotency key `plan:{id}:step:{n}`. **Scoped through its plan** (`platform.apply_parent_rls`). Each step records its target object's version; drift pauses the plan (AIC-182).","required":["planId","stepNumber","toolKey","targetContract","targetOperation","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"planId":{"type":"string","format":"uuid","x-ticvai-references":"ai.action_plan"},"stepNumber":{"type":"integer","minimum":1},"dependsOn":{"type":"array","items":{"type":"integer","minimum":1},"description":"Step numbers that must succeed first. The plan is a DAG."},"toolKey":{"type":"string"},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"contractVersion":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body of `targetOperation`, validated against it before the plan is approved."},"provenance":{"$ref":"#/components/schemas/AiProvenance"},"idempotencyKey":{"type":"string","readOnly":true},"targetObjectRef":{"type":"string","nullable":true},"targetObjectVersion":{"type":"string","nullable":true,"description":"The version the step was planned against. A different version at execution is drift."},"reversible":{"type":"boolean"},"compensation":{"type":"object","additionalProperties":true,"nullable":true},"status":{"type":"string","enum":["pending","validated","running","succeeded","failed","compensated","skipped","paused"],"readOnly":true},"attempts":{"type":"integer","minimum":0,"maximum":3,"readOnly":true,"description":"Bounded at 3 (AIC-135)."},"lastError":{"type":"string","nullable":true,"readOnly":true},"resultRef":{"type":"string","nullable":true,"readOnly":true,"description":"The owning service's response: success is its answer, not a model's judgement (AIC-097)."},"startedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"AiAutonomyLevel": {"type":"integer","minimum":0,"maximum":4,"description":"**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."},
"AiCapabilityFamily": {"type":"string","enum":["gatewayAndModels","governance","actionPipeline","knowledgeRetrieval","assistants","analyticsInsights","configurationAssistant","forecasting","anomalyDetection","riskIntelligence","recommendations","decisionRecords","operationsEvaluation","residencyPrivacy"],"description":"The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point, action pipeline and human oversight, knowledge and retrieval, assistants, analytics assistant and insights, configuration assistant, forecasting and operational requirements, anomaly detection, fraud and risk intelligence, recommendation and upsell engine, decision records and audit, operations/evaluation/cost, residency/privacy/tenancy. **Every registered capability belongs to exactly one**, which is what `AiPolicy.enabledCapabilities` and the usage report group by."},
"AiCapabilityRegistration": {"type":"object","x-ticvai-persistence":"ai.capability","description":"**An entry in the capability registry** (design 3.1 Registry, AIC-144, AIC-145; ADM-520). Nothing becomes an operational AI capability without a row here: owner, function, risk class, autonomy, data categories and lifecycle per environment. `autonomyCeiling` is the platform ceiling for the tenant; a tenant or venue may lower `autonomyLevel`, never raise it (AIC-151).","required":["capabilityKey","family","riskClass","autonomyLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string","description":"Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`."},"family":{"$ref":"#/components/schemas/AiCapabilityFamily"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal","description":"The accountable business owner (AIC-144)."},"businessFunction":{"type":"string","nullable":true},"riskClass":{"$ref":"#/components/schemas/AiRiskClass"},"autonomyCeiling":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"readOnly":true,"description":"The first-release ceiling for this capability (design 3.8 table). Read-only to a tenant."},"autonomyLevel":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"description":"The level in force at this scope. At most `autonomyCeiling`."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories the capability reads (ADM-524)."},"lifecycle":{"type":"object","description":"Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.","properties":{"development":{"type":"string","enum":["draft","pilot","active","retired"]},"staging":{"type":"string","enum":["draft","pilot","active","retired"]},"production":{"type":"string","enum":["draft","pilot","active","retired"]}}},"degradationMode":{"type":"string","enum":["rulesOnly","searchOnly","humanHandoff","hidden","failOpen","lastPublished"],"description":"What the capability does when its model or the service is unavailable (design 3.7, AIC-241)."},"status":{"type":"string","enum":["active","paused"],"readOnly":true,"description":"Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed."},"pausedReason":{"type":"string","nullable":true,"readOnly":true},"pausedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiDecisionRecord": {"type":"object","x-ticvai-persistence":"ai.decision_record","description":"**The standard record for every governed decision** (design 3.9, C12; AIC-193..209): a recommendation summary, a risk assessment, a forecast publication, a plan step, an assistant answer at significant depth, a governance block, a Help me choose suggestion. **Append-only; corrections are annotations; hash-chained per tenant** so tampering is detectable (AIC-203, AIC-204). **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["traceId","capabilityKey","outcome","recordHash"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"traceId":{"type":"string"},"capabilityKey":{"type":"string"},"task":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true},"subjectRef":{"type":"string","nullable":true},"inputsRef":{"type":"string","nullable":true,"description":"Where the inputs are kept (Blob or `ai.activity`), never the prompt text itself."},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"producer":{"type":"string","nullable":true},"modelVersion":{"type":"string","nullable":true},"promptTemplateVersion":{"type":"string","nullable":true},"featureSetVersion":{"type":"string","nullable":true},"knowledgeVersion":{"type":"string","nullable":true},"ruleVersions":{"type":"object","additionalProperties":true,"nullable":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"nullable":true},"policyVersion":{"type":"string","nullable":true},"approvals":{"type":"object","additionalProperties":true,"nullable":true,"description":"Approval requests and their decisions."},"humanDecision":{"type":"object","additionalProperties":true,"nullable":true,"description":"Override or intervention, where a person changed the outcome."},"executionResult":{"type":"object","additionalProperties":true,"nullable":true},"outcomeRef":{"type":"string","nullable":true,"description":"The business outcome it links to (an order, a published version, a closed case)."},"outcome":{"type":"string","enum":["answered","refused","allowed","blocked","executed","failed","approvedThenFailed","published","suggested"],"description":"`approvedThenFailed` is kept distinct from `executed` (design 1.2 Audit)."},"annotations":{"type":"array","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"byPrincipalId":{"type":"string","format":"uuid"},"note":{"type":"string"}}},"readOnly":true,"description":"Corrections, appended; the original fields are never edited."},"previousHash":{"type":"string","readOnly":true},"recordHash":{"type":"string","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiDecisionTrace": {"type":"object","x-ticvai-persistence":"none — ai.decision_record with the rows it references","description":"**The full trace of one decision** (ADM-540..546): record, evidence, candidates and rules, model and runtime, governance and approvals, execution and business outcome. Depth is gated by permission (AIC-195).","required":["record"],"properties":{"record":{"$ref":"#/components/schemas/AiDecisionRecord"},"depth":{"type":"string","enum":["business","governance","technical"]},"explanation":{"type":"string","description":"Built from structured evidence, never a model's chain of thought (AIC-192)."},"activity":{"type":"array","items":{"$ref":"#/components/schemas/AiInteraction"},"description":"The model calls behind it (`technical` depth)."},"plan":{"allOf":[{"$ref":"#/components/schemas/AiActionPlanDetail"}],"nullable":true},"interventions":{"type":"array","items":{"$ref":"#/components/schemas/AiIntervention"}},"chainVerified":{"type":"boolean","description":"The hash chain around this record verifies."}}},
"AiEvidenceItemList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The evidence of one decision record, stored with it.","items":{"$ref":"#/components/schemas/AiEvidenceItem"}},
"AiGovernanceOutcome": {"type":"string","enum":["allow","allowWithConditions","prepareOnly","approvalRequired","escalate","block"],"description":"What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). `block` is an answer, not an error, and is logged as outcome `refused`."},
"AiGovernancePolicyVersion": {"type":"object","x-ticvai-persistence":"ai.governance_policy_version","description":"One version of a governance policy. **Published versions are never edited**: a change is a new version, and the previous one becomes `superseded` in the same transaction (AIC-165).","required":["policyId","version","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"policyId":{"type":"string","format":"uuid","x-ticvai-references":"ai.governance_policy"},"version":{"type":"integer","minimum":1},"status":{"type":"string","enum":["draft","simulated","published","superseded"]},"rules":{"$ref":"#/components/schemas/AiGovernanceRuleList"},"changeNote":{"type":"string","nullable":true},"simulationSummary":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"The last `simulateAiGovernancePolicy` result: decisions that would change, by outcome."},"draftedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"supersededAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiGovernanceRule": {"type":"object","x-ticvai-persistence":"none — held in the jsonb rules column of ai.governance_policy_version, through AiGovernanceRuleList","description":"One rule of a governance policy version: which actions on which data, under which conditions, get which outcome (AIC-147..160).","required":["effect"],"properties":{"effect":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"capabilityKeys":{"type":"array","items":{"type":"string"},"description":"Registered capabilities it applies to. Empty means every capability the policy names."},"actions":{"type":"array","items":{"type":"string","enum":["read","analyze","recommend","generate","prepare","create","modify","publish","execute","delete"]},"description":"ADM-523: what AI may do, from reading to executing."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories (ADM-524), e.g. `customerContact`, `payment`, `financial`, `operational`."},"purposes":{"type":"array","items":{"type":"string"},"description":"Permitted purposes for those categories (AIC-156, AIR-182)."},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Above this value the effect escalates one step (for example to `approvalRequired`)."},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Roles the rule applies to; empty means every role."},"environments":{"type":"array","items":{"type":"string","enum":["development","sandbox","staging","production"]},"description":"ADM-525. Empty means every environment. **`sandbox`** (18 September minutes, M18-01): the developer sandbox and a tenant's trial environment, governed apart from staging so a rule can allow in sandbox what it blocks in production."},"conditions":{"type":"object","additionalProperties":true,"nullable":true,"description":"Conditions attached to an `allowWithConditions` effect, for example `maskFields` or `requireCitation`."}}},
"AiGovernanceRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The rules of one policy version, stored with the version as one `jsonb` column.","items":{"$ref":"#/components/schemas/AiGovernanceRule"}},
"AiInteraction": {"type":"object","x-ticvai-persistence":"ai.activity","required":["id","principalId","capability","outcome","createdAt"],"properties":{"scrubAudit":{"type":"object","readOnly":true,"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The audit of one call's scrubbing and routing** (3 October 2026, CHG-R1S-016; the legal research `docs/active/research/openai-key-uae-3-october.md`, item 9). Counts of the entities found by type, **never the values**; the residency class, endpoint and region; the scrubber version; whether the call was allowed or blocked; and a hash of the outbound payload. Exportable to the tenant as controller.","properties":{"entityCounts":{"type":"object","additionalProperties":{"type":"integer","minimum":0},"description":"Per entity type, e.g. emiratesId 1 and uaePhone 2. Counts only, never values."},"residencyClass":{"$ref":"../shared/common.yaml#/components/schemas/AiResidencyClass"},"endpointRegion":{"type":"string","description":"Where the call went, e.g. `uaeNorth`, `ae.api.openai.com`, `global`."},"scrubberVersion":{"type":"string"},"decision":{"type":"string","enum":["allowed","blocked"]},"outboundPayloadHash":{"type":"string","description":"SHA-256 of the prompt as sent (after scrubbing), so a dispute can be checked without keeping the text."}}},"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid","nullable":true},"principalId":{"type":"string","format":"uuid"},"audience":{"type":"string","enum":["staff","guest"],"description":"**Billing divides on this.** Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop guests asking questions.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest, where the audience is `guest`. `principalId` is null in that case — **a guest is not a principal**, and attributing their tokens to a staff member would be wrong twice.\n"},"billableToTenantId":{"type":"string","format":"uuid","description":"Resolved from `scopePath` at write time, not derived later. **Billing must not depend on walking a scope tree that has since been reorganised.**\n"},"scopePath":{"type":"string"},"capability":{"type":"string"},"prompt":{"type":"string"},"response":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"outcome":{"type":"string","enum":["answered","refused","applied","rejected","failed"]},"refusalReason":{"type":"string","nullable":true},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"cost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"x-ticvai-column":"cost_amount","description":"What the call cost at the provider. **Money like every other amount** (naming-and-style 5.1) — it replaces an integer `costMinor` that carried no currency or scale, which AED and OMR read differently.\n"},"latencyMs":{"type":"integer"},"maskedFieldCount":{"type":"integer","description":"How many fields were redacted. Zero on a prompt touching guest data is a defect."},"traceId":{"type":"string"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"description":"The `ai.decision_record` this call belongs to, where it was part of a governed decision (AI design 2.3, 3.9). Null for a call audited by this row alone."},"cacheLayer":{"type":"string","nullable":true,"enum":["guardrail","semantic","exact","negative","analytics"],"description":"Which cache answered, where one did (AI design 3.6). Null for a model call."},"createdAt":{"type":"string","format":"date-time"}}},
"AiIntervention": {"type":"object","x-ticvai-persistence":"ai.intervention","description":"**A person stepping in** (AIC-187, ADM-535, ADM-536): an override, pause, resume, stop, retry or rollback, with the original AI decision and the human one side by side.","required":["kind","targetKind","targetRef"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["override","pause","resume","cancel","retry","rollback","capabilityPause","capabilityResume"]},"targetKind":{"type":"string","enum":["plan","step","decision","capability"]},"targetRef":{"type":"string"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true},"originalDecision":{"type":"object","additionalProperties":true,"nullable":true},"humanDecision":{"type":"object","additionalProperties":true,"nullable":true},"reason":{"type":"string","maxLength":2000},"principalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiMessage": {"type":"object","x-ticvai-persistence":"ai.message","required":["id","conversationId","role","content","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid"},"role":{"type":"string","enum":["user","assistant","system"]},"content":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"confidence":{"type":"number","nullable":true,"description":"8.1.5, 8.3.67. **Nullable on purpose** — a provider that does not report confidence must yield null rather than an invented number, and an interface showing 0.9 because the code defaulted it is worse than showing nothing.\n"},"rationale":{"type":"string","nullable":true,"description":"8.3.68, 8.3.69."},"proposedAction":{"allOf":[{"$ref":"#/components/schemas/ProposedAction"}],"nullable":true,"description":"Present where the answer suggests a change. **A draft, never applied here.**"},"traceId":{"type":"string"},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"latencyMs":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"}}},
"AiPolicySimulation": {"type":"object","x-ticvai-persistence":"none — computed; summary kept on ai.governance_policy_version.simulationSummary","description":"What a draft policy version would have decided over recorded decisions and the test cases (ADM-527).","required":["evaluated"],"properties":{"evaluated":{"type":"integer"},"wouldChange":{"type":"integer"},"byOutcome":{"type":"object","additionalProperties":true,"description":"Counts per outcome, current against draft."},"examples":{"type":"array","items":{"type":"object","properties":{"decisionRecordId":{"type":"string","format":"uuid"},"current":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"draft":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"capabilityKey":{"type":"string"}}}}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n**Core42 Compass is reached through `openaiCompatible`** (Chinmay, 2 October: the AI residency decision, amending AI-D02; CHG-CSA-002). Compass is the provider of the `uaeOnly` residency class (common `AiResidencyClass`): Small tier Compass GPT-4.1 mini (or Seraj), Strong tier Compass GPT-5, with OpenAI UAE as the fallback. OpenAI UAE is `openai` with a UAE `endpoint`: OpenAI's UAE-region API project, `ae.api.openai.com` (in-country processing, on OpenAI sales approval), allowed under `uaeOnly` and the only endpoint a `uaeOnly` BYOK OpenAI key may use (CHG-R1S-016). **We host no model** (Chinmay, 3 October, CHG-R1S-002): there is no in-cell open-weights fallback; `localLlm` is used only where a client asks for self-hosting and runs the model on the client's estate (`onPrem`).\n**A kind is a protocol, not a vendor** (Chinmay, 2 October, contract follow-ups: BYOK accepts any provider; CHG-FUP-008). Any vendor is accepted, named in `AiProvider.vendor`: Mistral, Cohere or any other is reached through `openaiCompatible` where its API speaks it, which the compatibility test confirms before activation (`AiProviderCompatibility`). A new native adapter is a new value here, a breaking change for a client built earlier that goes out with an approval (`docs/active/breaking-changes.yaml`); until then a vendor without either protocol is refused `422 provider-protocol-unsupported`.\n"},
"AiRiskClass": {"type":"string","enum":["low","medium","high","critical"],"description":"Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). The governance decision point scores against it."},
"AiSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n","items":{"$ref":"#/components/schemas/AiSource"}},
"AiTool": {"type":"object","x-ticvai-persistence":"ai.tool","description":"**The tool registry** (design 3.1 Registry, 3.8; AIC-088, AIC-089). The executor calls owning modules only for tools registered here: each names its target operation at a contract version, whether it reads, writes or destroys, its risk, the permission it needs, its compensation and timeout. Platform rows, replicated read-only into each tenant database with the tenant root as `scopePath`; written only by `setAiTool` (`PLATFORM_AI_MANAGE`).","x-ticvai-registered-tools-note":"Registrations the release seeds through `setAiTool` for the resources and white-label assistants (29 September, build; 1.2.59, 2.6.50), so a conversational command or a configuration plan can change a resource schedule, a booking, an allocation or the storefront theme, fonts, header, navigation, homepage and pages. Each owner operation accepts `Prefer: validate-only` (added by its owner the same day). `white-label.publishTenantConfig` is deliberately not a tool: the assistant prepares, a person publishes.","x-ticvai-registered-tools":[{"toolKey":"resources.setResourceSchedule","targetContract":"resources","targetOperation":"setResourceSchedule","effect":"write","riskClass":"medium","permission":"RESOURCE_CONFIGURE","reversible":true,"compensationOperation":"setResourceSchedule","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"resources.updateResourceBooking","targetContract":"resources","targetOperation":"updateResourceBooking","effect":"write","riskClass":"medium","permission":"RESOURCE_BOOK","reversible":true,"compensationOperation":"updateResourceBooking","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"resources.allocateResources","targetContract":"resources","targetOperation":"allocateResources","effect":"write","riskClass":"medium","permission":"RESOURCE_BOOK","reversible":true,"compensationOperation":"replaceResourceAllocation","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setTheme","targetContract":"white-label","targetOperation":"setTheme","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setFonts","targetContract":"white-label","targetOperation":"setFonts","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setHeader","targetContract":"white-label","targetOperation":"setHeader","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setNavigation","targetContract":"white-label","targetOperation":"setNavigation","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setHomepageLayout","targetContract":"white-label","targetOperation":"setHomepageLayout","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.createContentPage","targetContract":"white-label","targetOperation":"createContentPage","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"deleteContentPage","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"venue-map.generateVisitPlan","targetContract":"venue-map","targetOperation":"generateVisitPlan","effect":"write","riskClass":"low","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":null,"timeoutMs":3000,"idempotent":true,"validateOnly":false,"agent":"planner.guest"},{"toolKey":"venue-map.getVisitPlan","targetContract":"venue-map","targetOperation":"getVisitPlan","effect":"read","riskClass":"low","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":null,"timeoutMs":2000,"idempotent":true,"validateOnly":false,"agent":"planner.guest"},{"toolKey":"venue-map.listVisitPlanAlternatives","targetContract":"venue-map","targetOperation":"listVisitPlanAlternatives","effect":"read","riskClass":"low","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":null,"timeoutMs":2000,"idempotent":true,"validateOnly":false,"agent":"planner.guest"},{"toolKey":"venue-map.updateVisitPlan","targetContract":"venue-map","targetOperation":"updateVisitPlan","effect":"write","riskClass":"low","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":"updateVisitPlan","timeoutMs":3000,"idempotent":true,"validateOnly":false,"agent":"planner.guest"},{"toolKey":"venue-map.bookVisitPlan","targetContract":"venue-map","targetOperation":"bookVisitPlan","effect":"write","riskClass":"medium","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":"orders.removeCartLine","timeoutMs":5000,"idempotent":true,"validateOnly":false,"agent":"planner.guest","requiresGuestConfirmation":true}],"x-ticvai-registered-tools-planner-note":"**The planner agent's tools** (29 September, MOB-6; the assistant profile `planner.guest`, audience guest, `guestCapabilityScope` `visitPlanning`). The agent refines a rules plan by chat on GST-054 through these five `venue-map` operations, **always called as the guest whose plan it is** (permission null, the guest session's own plan), so every change is a plan version the guest can undo. `bookVisitPlan` needs the guest to press Book in the app; the agent may prepare it and never checks out. AI writes nothing outside `ai.*` (ADR-0020): the plan tables are written by the venue-map service these tools call. **Grounding** (30 September client meeting, MoM 4.7): the agent's candidates are only what these tools return for a day, i.e. the rides, dining and retail points (shops and kiosks) on the published map of that day's venue; it never proposes a point from another venue or from general knowledge, and says so when a preference is not met there (`VisitPlan.unmatchedPreferences`).","required":["toolKey","targetContract","targetOperation","effect"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"toolKey":{"type":"string"},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"contractVersion":{"type":"string"},"effect":{"type":"string","enum":["read","write","destructive"]},"riskClass":{"$ref":"#/components/schemas/AiRiskClass"},"permission":{"type":"string","description":"The permission the requester must hold for the executor to call it on their behalf."},"reversible":{"type":"boolean","description":"Non-reversible steps (a refund, a publish) need the stronger approval tier (AIC-099)."},"compensationOperation":{"type":"string","nullable":true},"timeoutMs":{"type":"integer","minimum":1},"idempotent":{"type":"boolean","default":true},"validateOnly":{"type":"boolean","default":false,"description":"The owner accepts `Prefer: validate-only` on it (design 2.3)."},"status":{"type":"string","enum":["active","disabled"]},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalDelegation": {"type":"object","x-ticvai-persistence":"approvals.delegation","required":["delegatorPrincipalId","delegatePrincipalId","from","to"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"delegatorPrincipalId":{"type":"string","format":"uuid","description":"A principal id (`identity.Principal.id`). This contract stores the id only; the name to show, and the people to pick from, come from `identity.listPrincipals` and `identity.getPrincipal`.\n"},"delegatePrincipalId":{"type":"string","format":"uuid","description":"A principal id, resolved to a name the same way as `delegatorPrincipalId`."},"kinds":{"type":"array","description":"Absent means everything the delegator may approve.","items":{"$ref":"#/components/schemas/ApprovalKind"}},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"A delegate may be given less authority than the delegator, never more."},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time","description":"**Required.** An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it.\n"},"reason":{"type":"string"},"isActive":{"type":"boolean","readOnly":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMatrix": {"type":"object","x-ticvai-persistence":"approvals.matrix","required":["kind","scopeLevel","rules"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string","readOnly":true},"version":{"type":"integer","readOnly":true,"description":"11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"},"rules":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalRule"}},"isActive":{"type":"boolean"}}},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalRequirement": {"type":"object","x-ticvai-persistence":"none — computed","description":"The answer to \"does this need approval\", returned before the action.","required":["isRequired"],"properties":{"isRequired":{"type":"boolean"},"matchedRule":{"allOf":[{"$ref":"#/components/schemas/ApprovalRule"}],"nullable":true},"matrixVersion":{"type":"integer","nullable":true},"approvers":{"type":"array","description":"Resolved, with delegations applied. **Named so the caller can say \"this needs Sara\"** rather than \"this needs approval\".\n","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"level":{"type":"integer"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true}}}},"slaMinutes":{"type":"integer","nullable":true},"noApproverAvailable":{"type":"boolean","description":"**The case that must not fail silently.** A rule requiring a role nobody at this venue holds means the action is blocked forever, and the caller needs to know that now rather than after raising a request nobody can decide.\n"}}},
"ApprovalRule": {"type":"object","x-ticvai-persistence":"approvals.rule","required":["order","approverRoleIds","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"order":{"type":"integer","description":"**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"riskScoreAbove":{"type":"number","nullable":true,"description":"11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"},"condition":{"type":"string","nullable":true,"description":"11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"},"approverRoleIds":{"type":"array","minItems":1,"description":"Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n","items":{"type":"string","format":"uuid"}},"approverScopeLevel":{"type":"string","enum":["venue","department","region","tenant"],"description":"11.1.39. Which organisational level the approver must sit at."},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"levels":{"type":"integer","default":1,"description":"11.1.3. Multi-level chains ask each level in turn."},"requiresMfa":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"slaMinutes":{"type":"integer","nullable":true,"description":"11.1.14. Null means no SLA, which is different from a long one."},"escalateAfterMinutes":{"type":"integer","nullable":true},"escalateToRoleIds":{"type":"array","description":"Role ids from `identity.listRoles`, as `approverRoleIds`.","items":{"type":"string","format":"uuid"}},"expiresAfterMinutes":{"type":"integer","nullable":true,"description":"11.1.53. An unanswered request eventually stops waiting."},"subjectTypes":{"type":"array","description":"**Which subjects of the kind this rule matches** (decided 2 October 2026, Chinmay; CHG-CSP-028, CHG-CSP-036, CHG-CSP-031): the `CreateApprovalRequest.subjectType` values, for example `topologyPublication` or `whiteLabelPublication` under `configurationChange`. Empty matches every subject of the kind. It is how a venue switches an optional review step on for one kind of act without routing every act of the kind.","items":{"type":"string","maxLength":64}},"signatureMethods":{"type":"array","description":"**The signature methods this level accepts, where `requiresSignature` is true** (design-notes correction on ADM-344, Block B: \"Configuring which stages need a signature is a policy write\"; CHG-CSP-045). Values of `ApprovalSignature.method`. Empty accepts any of them. With `requiresSignature` this makes the rule the signature policy: which levels of which kinds need a signature, and how it is given; `signApprovalDecision` refuses a method the level does not accept.","items":{"type":"string","enum":["platformKey","uaePass","externalCertificate","drawnSignature"]}},"externalProviderId":{"type":"string","format":"uuid","nullable":true,"description":"11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"}}},
"ApprovalSlaPolicy": {"type":"object","x-ticvai-persistence":"approvals.sla_policy","description":"Approvals boards 5.5 and 5.6. **A target with no consequence is a number in a table**, so the reminder and breach behaviour are part of the policy.\n","required":["code"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"appliesToRequestKinds":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalKind"}},"targetMinutes":{"type":"integer"},"businessHoursOnly":{"type":"boolean","default":true,"description":"**A four-hour SLA starting at five in the afternoon is breached by nine the next morning with nobody having done anything wrong.**\n"},"calendarId":{"type":"string","format":"uuid","nullable":true},"reminders":{"type":"array","items":{"type":"object","properties":{"atPercentOfTarget":{"type":"integer"},"notify":{"type":"string","enum":["approver","approverManager","requester","escalationGroup"]}}}},"firstReminderAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"**Percent of `targetMinutes` at which the first reminder goes** (decided 29 September, readiness close-out: the reminder steps are percentages of target). A column so the SLA, Escalation, Reminder & Timeout Rules screen reads it rather than unpacking `reminders`; the reminder in `reminders` at this percentage says whom it notifies (data model for the agreed operations, 29 September)."},"secondReminderAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Percent of `targetMinutes` at which the second reminder goes; above `firstReminderAtPercent`"},"escalateAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Percent of `targetMinutes` at which the request or workflow escalates; at or above `secondReminderAtPercent`"},"onBreach":{"type":"string","enum":["notifyOnly","escalate","autoApprove","autoReject"],"default":"escalate"},"autoActionAllowed":{"type":"boolean","default":false,"description":"**Auto-approval on breach is off unless somebody says otherwise, in writing.** A queue that approves itself when nobody looks is not an approval process.\n"},"escalationGroupId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE","CORE_AI_PUBLISH","TICKETING_AI_PUBLISH","ACCESS_AI_PUBLISH","FNB_AI_PUBLISH","RETAIL_AI_PUBLISH","INVENTORY_AI_PUBLISH","SEATING_AI_PUBLISH","MEMBERSHIP_AI_PUBLISH","MARKETING_AI_PUBLISH","RESOURCES_AI_PUBLISH","QUEUE_AI_PUBLISH","TRANSPORT_AI_PUBLISH","GAMES_AI_PUBLISH","MAINTENANCE_AI_PUBLISH","ACCREDITATION_AI_PUBLISH","PARTNER_AI_PUBLISH","ANALYTICS_AI_PUBLISH","BIOMETRIC_IMAGE_VIEW","ACCESS_DIRECTION_SET","REPORT_GOVERNANCE_MANAGE"]},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"SuspensionMode": {"type":"string","description":"Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n","enum":["readOnly","noNewSales","fullLockout"]},
"Tenant": {"x-ticvai-persistence":"control.tenant","type":"object","required":["id","code","name","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"$ref":"#/components/schemas/TenantStatus"},"suspensionMode":{"$ref":"#/components/schemas/SuspensionMode"},"suspensionReason":{"type":"string","nullable":true},"suspensionEffectiveAt":{"type":"string","format":"date-time","nullable":true,"description":"When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."},"suspensionNoticeMessage":{"$ref":"#/components/schemas/LocalisedText","description":"The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."},"terminationScheduledAt":{"type":"string","format":"date-time","nullable":true,"description":"When `terminateTenant` started the retention window. Null when no termination is under way."},"terminationRetentionUntil":{"type":"string","format":"date-time","nullable":true,"description":"`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."},"terminationReason":{"type":"string","maxLength":1000,"nullable":true},"terminationRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"planId":{"type":"string","format":"uuid","nullable":true},"planName":{"type":"string","nullable":true},"cellCount":{"type":"integer"},"venueCount":{"type":"integer"},"regionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500,"nullable":true,"description":"Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."},"accountManagerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantStatus": {"type":"string","enum":["onboarding","active","suspended","terminating","terminated"]}
}
```
