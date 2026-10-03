# WS121 — AI Governance board 1

**10 screens · 19 operations · 26 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `AI_APPROVE, AI_CONFIGURE, AI_USE, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_VIEW, TENANT_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `ADM-519` | AI Governance Command Center | D | 6 | 10 | 7 | 2 | 0 | 0 | — | notStarted (—) |
| `ADM-520` | AI Capability Registry & Ownership | D | 20 | 21 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-521` | AI Risk Classification & Assessment | D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-522` | AI Autonomy Level Configuration | D | 15 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-523` | AI Action & Permission Policy Builder | A | 23 | 14 | 7 | 1 | 0 | 5 | — | notStarted (—) |
| `ADM-524` | AI Data Access & Usage Policy | D | 6 | 6 | 7 | 2 | 0 | 0 | — | notStarted (—) |
| `ADM-525` | Environment, Tenant & Scope Governance | D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-526` | AI Policy Conflict, Exception & Override Management | D | 13 | 33 | 7 | 1 | 2 | 0 | — | notStarted (—) |
| `ADM-527` | AI Policy Testing & Governance Simulation | A | 9 | 11 | 7 | 1 | 1 | 0 | — | notStarted (—) |
| `ADM-528` | AI Governance Policy Publication & Effective Policy Map | A | 6 | 22 | 7 | 1 | 0 | 0 | — | notStarted (—) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-519` AI Governance Command Center

**Provide management with one centralized view of AI governance across the entire TICVAI platform.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-519 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `capabilityKey` (navigation), `releaseId` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-governance-command-center-adm-519` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listAiCapabilities` (AI_USE), `pauseAiCapability` (AI_CONFIGURE), `promoteAiRelease` (AI_USE), `listAiGovernanceAlerts` (AI_USE), `listAiCapabilityMaturity` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**From the AI & Intelligence process.** The AI governance command centre: capabilities registered, policies in force, governed actions today, actions needing approval or blocked, exceptions, high-risk capabilities, violations, and each capability's maturity - with the "Ready to promote" alerts and the kill switch at hand. The one thing to get right: it is a saved dashboard over the same registry, alerts and maturity data as the detail screens (a command centre is a saved dashboard), and the open question of central vs per-module placement is answered by also offering each tile as a widget for the module dashboards.

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **One central AI governance dashboard, or widgets in each module's dashboard?** → Drawn default accepted: Both - this centre for the governance lead, and the same tiles available as widgets on module command centres (a command centre is a saved dashboard). *(decided by Chinmay, 2026-10-02; DEC-274 / CHG-NOTE-001)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Family | select | — | Gateway and models · Governance · Action pipeline · Knowledge retrieval · Assistants · Analytics insights · Configuration assistant · Forecasting · Anomaly detection · Risk intelligence · Recommendations · Decision records … | `listAiCapabilities` ?family |
| Status | segmented control | — | Active · Paused | `listAiCapabilities` ?status |
| Risk class | radio group | — | Low · Medium · High · Critical | `listAiCapabilities` ?riskClass |
| Kind | select | — | Policy violation · Cross scope attempt · Masking defect · Data usage · Behaviour drift · Input drift · Bias · Override rate shift · Control failed · Spend · Provider breaker · Evaluation regression … | `listAiGovernanceAlerts` ?kind |
| Status | radio group | — | Open · Acknowledged · Dismissed · Resolved · Incident opened | `listAiGovernanceAlerts` ?status |
| Severity | radio group | — | Info · Low · Medium · High · Critical | `listAiGovernanceAlerts` ?severity |
| Stage | radio group | — | Starting · Learning · Established · Learned | `listAiCapabilityMaturity` ?stage |
| Capability key | text field | — | — | `listAiCapabilityMaturity` ?capabilityKey |
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

**AI Capabilities Registered** (metric tile)

**Active Governance Policies** (metric tile)

**Governed AI Actions Today** (metric tile)

**Approval-Required Actions** (metric tile)

**Blocked AI Actions** (metric tile)

**Policy Exceptions** (metric tile)

**High-Risk AI Capabilities** (metric tile)

**Policy Violations** (metric tile)

**AI Autonomy Coverage** (metric tile)

**Governance Warnings** (metric tile)

**AI maturity by question** (data table, from `listAiCapabilityMaturity`): **Starting, learning, established, learned** (AI functions review): where each answer stands, what it is based on and what the next stage needs. A `promotionReady` alert links from the row.

| Shows | Format | Notes |
|---|---|---|
| Capability key | text | — |
| Stage | chip: Starting, Learning, Established, Learned | — |
| Maturity | grouped details | Where an answer stands, on every answer (29 September, AI functions review; baseline then learn). |
| Since | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **tiles**: Counts that link to their screens; "Ready to promote" as its own tile from promotionReady alerts; blocked actions shown as refused decisions, not errors. *(source: contracts/satellite/ai.yaml#listAiGovernanceAlerts / contracts/satellite/ai.yaml#/components/schemas/AiGovernanceOutcome / ADR-0041)*
- **maturity by question**: Stage badge per capability question with "since"; the same component as ANL-071. *(source: contracts/satellite/ai.yaml#listAiCapabilityMaturity / ADR-0051)*
- **autonomy coverage**: Capabilities per level L0-L4 against ceilings, as a stacked bar. *(source: ADR-0050 / contracts/satellite/ai.yaml#listAiCapabilities)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Pause capability**: Kill switch with the degradation mode stated (as ADM-536). *(source: contracts/satellite/ai.yaml#pauseAiCapability)*

**Data it reads**: `listAiCapabilities` (onLoad, The capability registry); `listAiGovernanceAlerts` (onLoad, Governance alerts); `listAiCapabilityMaturity` (onLoad, Where each AI answer stands on the way to learned); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-520` AI Capability Registry & Ownership: *AI Capability Registry & Ownership*; carries `capabilityKey`
- → `ADM-521` AI Risk Classification & Assessment: *AI Risk Classification & Assessment*; carries `capabilityKey`
- → `ADM-522` AI Autonomy Level Configuration: *AI Autonomy Level Configuration*; carries `capabilityKey`
- → `ADM-523` AI Action & Permission Policy Builder: *AI Action & Permission Policy Builder*; carries `tenantId`
- → `ADM-524` AI Data Access & Usage Policy: *AI Data Access & Usage Policy*; carries `tenantId`
- → `ADM-525` Environment, Tenant & Scope Governance: *Environment, Tenant & Scope Governance*; carries `tenantId`
- → `ADM-526` AI Policy Conflict, Exception & Override Management: *AI Policy Conflict, Exception & Override Management*; carries `tenantId`
- → `ADM-527` AI Policy Testing & Governance Simulation: *AI Policy Testing & Governance Simulation*; carries `tenantId`
- → `ADM-528` AI Governance Policy Publication & Effective Policy Map: *AI Governance Policy Publication & Effective Policy Map*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Already paused.; 409 Not promotable: the gate has not passed (`gate-not-passed`), an isolation case failed (`isolation-cases-failed`), the stage cannot follow the current one … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  registered: 14
  policies: 9
  governedToday: 12480
  approvalRequired: 37
  blocked: 6
  exceptions: 1
  highRisk: 3
  violations: 0
  readyToPromote: 0
```

#### Permissions

- `listAiCapabilities` → `AI_USE` (operate) · staff
- `pauseAiCapability` → `AI_CONFIGURE` (configure) · staff
- `promoteAiRelease` → `AI_USE` (operate) · staff
- `listAiGovernanceAlerts` → `AI_USE` (operate) · staff
- `listAiCapabilityMaturity` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.2.52 | System shall continuously retrain forecasting models. | Unified Operations Dashboard | CONTRACTED | `promoteAiRelease` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-519` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS14 AI Governance Board 1.dc.html#adm-519`
- Workshop pack: AI_Governance_Reference.pdf board 1
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 1: Opens AI Governance Command Center → Provide management with one centralized view of AI governance across the entire TICVAI platform.
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F230 branch at step 1 (expected): when Nothing has been set up on AI Governance Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F230 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-519?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, .
- [ ] Every transition is wired: `ADM-002`, `ADM-520`, `ADM-521`, `ADM-522`, `ADM-523`, `ADM-524`, `ADM-525`, `ADM-526`, `ADM-527`, `ADM-528`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-520` AI Capability Registry & Ownership

**Maintain a controlled registry of every AI capability operating within TICVAI. Nothing should become an operational AI capability without being identifiable and governed.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-SETUP-ADM-520 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `capabilityKey` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-capability-registry-ownership-adm-520` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listAiCapabilities` (AI_USE), `configureAiCapability` (AI_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** The AI capability registry: every AI capability operating in a tenant, with its accountable owner, risk class, the autonomy level in force against its first-release ceiling, the data it reads, its lifecycle per environment and what it does when it is unavailable. Nothing becomes an operational AI capability without an entry here. The one thing to get right: autonomy is chosen on the one L0-L4 scale and can never exceed the ceiling.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The layout is an unbound dataTable with unlabelled buttons; in Block A only configureAiCapability is in the slice. (CHG-SBO-006)

**Fixed on main** (the package already carries these; draw what it says): The P09 governance screens (ADM-519..558) act on one tenant's registry and policies but, unlike ADM-037, declare no tenant picker and no … (CHG-SBO-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Who runs the governance boards day to day - TICVAI staff on the console, or the tenant's own AI governance lead?** → Drawn default stands (answer: "Default / recommended accepted"): TICVAI staff through a grant for the first release; the open item on central versus per-module placement (MoM 18 Sep §6) stays with Chinmay's team. *(decided by Chinmay, 2026-10-02; DEC-004 / CHG-NOTE-001)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Family | select | — | Gateway and models · Governance · Action pipeline · Knowledge retrieval · Assistants · Analytics insights · Configuration assistant · Forecasting · Anomaly detection · Risk intelligence · Recommendations · Decision records … | `listAiCapabilities` ?family |
| Status | segmented control | — | Active · Paused | `listAiCapabilities` ?status |
| Risk class | radio group | — | Low · Medium · High · Critical | `listAiCapabilities` ?riskClass |
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

**Form: Save capability** (modal, opened by *Save capability*; *Save capability* calls `configureAiCapability`, *Cancel* sends nothing)

**Collects what `configureAiCapability` sends before it is called.** Required: `capabilityKey`, `family`, `riskClass`, `autonomyLevel`. Optional: `name`, `description`, `ownerPrincipalId`, `businessFunction`, `dataCategories`, `lifecycle`, `degradationMode`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Capability key `capabilityKey` | text field | required | — | — | — | Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`. | `configureAiCapability` body |
| Family `family` | select | required | — | Gateway and models · Governance · Action pipeline · Knowledge retrieval · Assistants · Analytics insights · Configuration assistant · Forecasting · Anomaly detection · Risk intelligence · Recommendations · Decision records … | — | The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point, action pipeline and human oversight … | `configureAiCapability` body |
| Name `name` | text field | optional | — | — | — | — | `configureAiCapability` body |
| Description `description` | text area | optional | — | — | — | — | `configureAiCapability` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | The accountable business owner (AIC-144). | `configureAiCapability` body |
| Business function `businessFunction` | text field | optional | — | — | — | — | `configureAiCapability` body |
| Risk class `riskClass` | radio group | required | — | Low · Medium · High · Critical | — | Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). | `configureAiCapability` body |
| Autonomy level `autonomyLevel` | stepper or slider | required | — | min 0; max 4; At most `autonomyCeiling`. | — | The level in force at this scope. At most `autonomyCeiling`. | `configureAiCapability` body |
| Data categories `dataCategories` | list of values (chips) | optional | — | — | — | Data categories the capability reads (ADM-524). | `configureAiCapability` body |
| Lifecycle `lifecycle` | group | optional | — | — | — | Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production. | `configureAiCapability` body |
| Development `lifecycle.development` | radio group | optional | — | Draft · Pilot · Active · Retired | — | — | `configureAiCapability` body |
| Staging `lifecycle.staging` | radio group | optional | — | Draft · Pilot · Active · Retired | — | — | `configureAiCapability` body |
| Production `lifecycle.production` | radio group | optional | — | Draft · Pilot · Active · Retired | — | — | `configureAiCapability` body |
| Degradation mode `degradationMode` | select | optional | — | Rules only · Search only · Human handoff · Hidden · Fail open · Last published | — | What the capability does when its model or the service is unavailable (design 3.7, AIC-241). | `configureAiCapability` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The requested `autonomyLevel` is above the capability's `autonomyCeiling` (AIC-151).

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **autonomyLevel**: A five-step selector "L0 Disabled ... L4 Controlled auto" with the capability's ceiling marked; levels above the ceiling are drawn disabled with the reason (e.g. "Fraud restrictive actions: ceiling L1 Advisory in the first release"). 409 autonomy-above-ceiling if the platform ceiling changed meanwhile. *(source: ADR-0050 / contracts/satellite/ai.yaml#configureAiCapability)*
- **ownerPrincipalId**: Required in practice - an unowned capability shows as a warning in the list. Picker of tenant users. *(source: MoM 18 Sep 4.1 (capability registration and ownership) / contracts/satellite/ai.yaml#/components/schemas/AiCapabilityRegistration)*
- **riskClass**: Low / Medium / High / Critical with the client's examples inline (explaining a sales report - low; suggesting a price change - high). *(source: MoM 18 Sep 4.1 / MoM 18 Sep §5)*
- **degradationMode**: Explained choices: rules only, search only, hand over to a person, hidden, fail open, last published. Defaults per family (recommendations leave the slot empty, fraud falls back to owners' rules, concierge offers a person). *(source: contracts/satellite/ai.yaml#/components/schemas/AiCapabilityRegistration / contracts/satellite/ai.yaml#pauseAiCapability)*

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
| Business function | text | — |
| Risk class | chip: Low, Medium, High, Critical | Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). |
| Autonomy level | 1,234 | The level in force at this scope. At most `autonomyCeiling`. |
| Autonomy ceiling | 1,234 | The first-release ceiling for this capability (design 3.8 table). Read-only to a tenant. |
| Lifecycle | grouped details | Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production. |
| Status | chip: Active, Paused | Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed. |

**The selected capability** (detail panel, from `listAiCapabilities`)

| Shows | Format | Notes |
|---|---|---|
| Capability key | text | Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`. |
| Description | text | — |
| Owner principal | the name it points at, never the id | The accountable business owner (AIC-144). |
| Data categories | list or chips (count when long) | Data categories the capability reads (ADM-524). |
| Degradation mode | chip: Rules only, Search only, Human handoff, Hidden, Fail open, Last published | What the capability does when its model or the service is unavailable (design 3.7, AIC-241). |
| Paused reason | text | — |
| Updated at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Save capability (primary button) | `configureAiCapability` PUT `/governance/capabilities/{capabilityKey}` | AiCapabilityRegistration | AiCapabilityRegistration | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The requested `autonomyLevel` is above the capability's `autonomyCeiling` (AIC-151). | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **registry rows**: Key (e.g. assistant.guest, forecast.attendance, risk.transaction, config.assistant, recommend.checkout), name, family, owner, risk class, "L2 Prepare - ceiling L3", status (Active / Paused with reason and time), lifecycle per environment (e.g. Production: live, Staging: live). The capability's maturity stage is shown beside it where it is data-driven. *(source: contracts/satellite/ai.yaml#listAiCapabilities / contracts/satellite/ai.yaml#listAiCapabilityMaturity)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Register / change capability**: Writes one entry; the list updates. A venue-scope change that would raise the tenant's level is refused on the field. *(source: contracts/satellite/ai.yaml#configureAiCapability)*

**Data it reads**: `listAiCapabilities` (onLoad, The capability registry); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-519` AI Governance Command Center: *Back to AI Governance Command Center*; carries `capabilityKey`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The capability registry ownership list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the capability registry ownership untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No capability registry ownership yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the capability registry ownership are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The requested `autonomyLevel` is above the capability's `autonomyCeiling` (AIC-151). |

#### Edge cases to draw

- **Capability paused**: Row shows Paused, the reason, who and when, and what it does meanwhile (its degradation mode); Resume links to ADM-536. *(source: contracts/satellite/ai.yaml#/components/schemas/AiCapabilityRegistration (status, pausedReason))*

#### Consistency with other screens

- Match `ADM-522`: The autonomy screen edits the same field with the same selector.
- Match `ANL-060`: Reads this registry first; same labels.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- key: assistant.guest
  name: Guest concierge (Sahli)
  family: assistants
  owner: Fatima Al Mansoori (Guest Experience)
  risk: Low
  autonomy: L1 Advisory - ceiling L2
  status: Active
- key: config.assistant
  name: Configuration assistant
  family: configurationAssistant
  owner: Omar Haddad (Operations)
  risk: High
  autonomy: L3 Execute with approval - ceiling L3
  status: Active
- key: risk.transaction
  name: Transaction risk scoring
  family: riskIntelligence
  owner: Priya Nair (Finance)
  risk: Critical
  autonomy: L1 Advisory - ceiling L1
  status: Active
- key: forecast.attendance
  name: Attendance forecast
  family: forecasting
  owner: Omar Haddad
  risk: Medium
  autonomy: L4 Controlled auto (auto-publish) - ceiling L4
  status: Active
  stage: Learning
```

#### Permissions

- `listAiCapabilities` → `AI_USE` (operate) · staff
- `configureAiCapability` → `AI_CONFIGURE` (configure) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-520` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS14 AI Governance Board 1.dc.html#adm-520`
- Workshop pack: AI_Governance_Reference.pdf board 1
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 2: Works in AI Capability Registry & Ownership → Maintain a controlled registry of every AI capability operating within TICVAI. Nothing should become an operational AI capability without being identifiable and governed.

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (21 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-520?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Save capability.
- [ ] Every transition is wired: `ADM-519`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-521` AI Risk Classification & Assessment

**Classify AI capabilities and individual AI action types according to their potential business, customer, financial, operational, security and compliance impact. Risk should not be based only on which AI model is being used.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-521 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `capabilityKey` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-risk-classification-assessment-adm-521` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listAiCapabilities` (AI_USE), `configureAiCapability` (AI_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Risk classification of capabilities and action types by business, customer, financial, operational, security and compliance impact - not by which model is used. The one thing to get right: the client's examples anchor the scale - explaining a sales report is low risk and needs no approval; an AI-suggested price change is high risk and needs a person.

**Known correction pending (do not draw the wrong version)**

- **Risk is on the capability only; action types (price change vs explanation within one capability) have no risk field.** Why: The purpose asks for action-type risk; it lives in governance rules (effect per action) - say so on the screen or add a per-tool risk (AiTool.riskClass exists). *(source: contracts/satellite/ai.yaml#setAiTool (riskClass); AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Family | select | — | Gateway and models · Governance · Action pipeline · Knowledge retrieval · Assistants · Analytics insights · Configuration assistant · Forecasting · Anomaly detection · Risk intelligence · Recommendations · Decision records … | `listAiCapabilities` ?family |
| Status | segmented control | — | Active · Paused | `listAiCapabilities` ?status |
| Risk class | radio group | — | Low · Medium · High · Critical | `listAiCapabilities` ?riskClass |
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

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **riskClass per capability / action type**: Low, medium, high, critical with the impact dimensions as checkboxes and the consequence shown ("High - approval required before publishing"). *(source: contracts/satellite/ai.yaml#configureAiCapability / MoM 18 Sep 4.1 / MoM 18 Sep §5)*

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

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAiCapabilities` (onLoad, The capability registry); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-519` AI Governance Command Center: *Back to AI Governance Command Center*; carries `capabilityKey`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The risk classification assessment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the risk classification assessment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No risk classification assessment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the risk classification assessment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The requested `autonomyLevel` is above the capability's `autonomyCeiling` (AIC-151). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- capability: Report explanation
  risk: Low
  approval: None
- capability: Price change suggestion
  risk: High
  approval: Commercial manager
- capability: Fraud hold
  risk: Critical
  autonomy: L1 Advisory
```

#### Permissions

- `listAiCapabilities` → `AI_USE` (operate) · staff
- `configureAiCapability` → `AI_CONFIGURE` (configure) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-521` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS14 AI Governance Board 1.dc.html#adm-521`
- Workshop pack: AI_Governance_Reference.pdf board 1
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 4: Works in AI Risk Classification & Assessment → Classify AI capabilities and individual AI action types according to their potential business, customer, financial, operational, security and compliance impact. Risk should not be based only on which …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-521?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Cancel.
- [ ] Every transition is wired: `ADM-519`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-522` AI Autonomy Level Configuration

**Define exactly how independently AI is permitted to operate. This is one of the most important screens in the governance module. I recommend four controlled levels plus a disabled state. Level 0 — Disabled AI capability cannot operate. Level 1 — Advisory**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-522 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure by) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `capabilityKey` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-autonomy-level-configuration-adm-522` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listAiCapabilities` (AI_USE), `configureAiCapability` (AI_CONFIGURE), `getEffectiveAiPolicy` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**From the AI & Intelligence process.** Autonomy levels per capability on the one L0-L4 scale with the first-release ceilings, tightened per venue, environment or role but never raised. The one thing to get right: the board's own scale ("four controlled levels plus disabled") must be relabelled to L0 Disabled, L1 Advisory, L2 Prepare, L3 Execute with approval, L4 Controlled auto - and autonomy is separate from the user's permission.

**Known correction pending (do not draw the wrong version)**

- **Filters Tenant, Module, Action Type, User Role, Business Unit as selectFields with no operation.** Why: Autonomy is per capability (configureAiCapability) with tighten-only overrides per scope (setAiPolicy.autonomyOverrides); there is no per-role autonomy - autonomy is separate from permission. *(source: ADR-0050 / contracts/satellite/ai.yaml#configureAiCapability; AI & Intelligence)*
- **purpose carries the board's own level descriptions.** Why: Relabel to ADR-0050's scale. *(source: ADR-0050; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| AI Capability | select field | — | — | — | — | — | — |
| Module | select field | — | — | — | — | — | — |
| Action Type | select field | — | — | — | — | — | — |
| User Role | select field | — | — | — | — | — | — |
| Environment | select field | — | — | — | — | — | — |
| Risk Level | select field | — | — | — | — | — | — |
| Business Unit | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Family | select | — | Gateway and models · Governance · Action pipeline · Knowledge retrieval · Assistants · Analytics insights · Configuration assistant · Forecasting · Anomaly detection · Risk intelligence · Recommendations · Decision records … | `listAiCapabilities` ?family |
| Status | segmented control | — | Active · Paused | `listAiCapabilities` ?status |
| Risk class | radio group | — | Low · Medium · High · Critical | `listAiCapabilities` ?riskClass |
| Capability key | text field | — | — | `getEffectiveAiPolicy` ?capabilityKey |
| Scope path | text field | — | — | `getEffectiveAiPolicy` ?scopePath |
| Environment | radio group | — | Development · Sandbox · Staging · Production | `getEffectiveAiPolicy` ?environment |
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

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **autonomy level**: Selector with the ceiling marked and higher levels disabled with the reason; venue and environment overrides tighten only. *(source: ADR-0050 / contracts/satellite/ai.yaml#/components/schemas/AiPolicy (autonomyOverrides))*

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

- **ceiling table**: First-release ceilings - L1 fraud restrictive actions, access-security changes, finance actions; L2 operational requirements, pricing inputs, campaigns, Help me choose; L3 configuration assistant, forecast publication; L4 only forecast auto-publish, ranking inside a published strategy, fraud hold mapping if turned on. *(source: ADR-0050)*
- **note**: "A manager who may change a price by hand still gets an AI-prepared change routed for approval." *(source: ADR-0050)*

**Data it reads**: `listAiCapabilities` (onLoad, The capability registry); `getEffectiveAiPolicy` (onLoad, The policy in force for a capability at a scope); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-519` AI Governance Command Center: *Back to AI Governance Command Center*; carries `capabilityKey`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The autonomy level configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the autonomy level untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No autonomy level configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The requested `autonomyLevel` is above the capability's `autonomyCeiling` (AIC-151). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- capability: Configuration assistant
  level: L3 Execute with approval
  ceiling: L3
- capability: Help me choose
  level: L2 Prepare
  ceiling: L2
- capability: Fraud hold
  level: L1 Advisory
  ceiling: L1 (L4 hold mapping off)
```

#### Permissions

- `listAiCapabilities` → `AI_USE` (operate) · staff
- `configureAiCapability` → `AI_CONFIGURE` (configure) · staff
- `getEffectiveAiPolicy` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-522` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS14 AI Governance Board 1.dc.html#adm-522`
- Workshop pack: AI_Governance_Reference.pdf board 1
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 6: Works in AI Autonomy Level Configuration → Define exactly how independently AI is permitted to operate. This is one of the most important screens in the governance module. I recommend four controlled levels plus a disabled state. Level 0 — …

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-522?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-519`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-523` AI Action & Permission Policy Builder

**Define granular rules controlling what AI is allowed to read, recommend, prepare, modify or execute. This should work alongside TICVAI's existing RBAC/PBAC, not replace it.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 1 · needs the `core` module |
| Block | Block A · task APP-SETUP-ADM-523 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/platform/ai-action-permission-policy-builder-adm-523` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `createAiGovernancePolicyDraft` (AI_CONFIGURE), `listAiGovernancePolicyVersions` (AI_USE), `listAiTools` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-012): setAiTool (PLATFORM_AI_MANAGE) was declared on a tenant policy screen; tools are platform facts replicated read-only into tenants, so the tenant board only reads …

**From the AI & Intelligence process.** The action and permission policy builder: rules that say which AI capabilities may read, analyse, recommend, generate, prepare, create, modify, publish, execute or delete - on which data, in which environment, for which roles and up to what amount - and with what outcome (allow, allow with conditions, prepare only, approval required, escalate, block). It works alongside RBAC, not instead of it: autonomy is separate from a person's permission. Rules are saved as a draft; testing and publication happen on ADM-527 and ADM-528. The one thing to get right: the verbs are a matrix in each rule, not buttons on the screen.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- In Block A only createAiGovernancePolicyDraft is in the slice. (CHG-SBO-006)

**Fixed on main** (the package already carries these; draw what it says): The actionBar has buttons Analyze, Recommend, Generate, Prepare, Create, Modify, Delete, Publish, all unbound. (CHG-SBO-007); setAiTool (PLATFORM_AI_MANAGE) is declared on a tenant policy screen. (CHG-WIR-012).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are the action verbs the client's ten, or the five the minutes name (read, recommend, prepare, modify, execute)?** → Drawn default stands (answer: "Default / recommended accepted"): The contract's ten, grouped into the minutes' five headings. *(decided by Chinmay, 2026-10-02; DEC-005 / CHG-NOTE-001)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Actions the rule covers | repeatable rows | optional | — | — | — | Per rule, the verbs it governs (`AiGovernanceRule.actions`: read, analyze, recommend, generate, prepare, create, modify, publish, execute, delete). The board's Analyze ... Publish buttons were these … | `AiGovernancePolicyVersion.rules` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Policy | picker: choose a policy | — | — | `listAiGovernancePolicyVersions` ?policyId |
| Status | radio group | — | Draft · Simulated · Published · Superseded | `listAiGovernancePolicyVersions` ?status |
| Kind | select | — | Action · Data · Scope · Autonomy · Approval · Environment | `listAiGovernancePolicyVersions` ?kind |
| Target contract | text field | — | — | `listAiTools` ?targetContract |
| Effect | segmented control | — | Read · Write · Destructive | `listAiTools` ?effect |
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

**Form: Save draft** (modal, opened by *Save draft*; *Save draft* calls `createAiGovernancePolicyDraft`, *Cancel* sends nothing)

**Collects what `createAiGovernancePolicyDraft` sends before it is called.** Required: `rules`. Optional: `policyId`, `policyKey`, `name`, `kind`, `capabilityKeys`, `changeNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Policy `policyId` | picker: choose a policy | optional | — | — | shows names, sends the id | An existing policy to draft the next version of. | `createAiGovernancePolicyDraft` body |
| Policy key `policyKey` | text field | optional | — | — | — | Required for a new policy. | `createAiGovernancePolicyDraft` body |
| Name `name` | text field | optional | — | — | — | — | `createAiGovernancePolicyDraft` body |
| Kind `kind` | select | optional | — | Action · Data · Scope · Autonomy · Approval · Environment | — | — | `createAiGovernancePolicyDraft` body |
| Capability keys `capabilityKeys` | list of values (chips) | optional | — | — | — | — | `createAiGovernancePolicyDraft` body |
| Rules `rules` | repeatable rows | required | — | at least 1 | — | — | `createAiGovernancePolicyDraft` body |
| Effect `rules[].effect` | select | required | — | Allow · Allow with conditions · Prepare only · Approval required · Escalate · Block | — | What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). | `createAiGovernancePolicyDraft` body |
| Capability keys `rules[].capabilityKeys` | list of values (chips) | optional | — | — | — | Registered capabilities it applies to. Empty means every capability the policy names. | `createAiGovernancePolicyDraft` body |
| Actions `rules[].actions` | multi-select chips | optional | — | Read · Analyze · Recommend · Generate · Prepare · Create · Modify · Publish · Execute · Delete | — | ADM-523: what AI may do, from reading to executing. | `createAiGovernancePolicyDraft` body |
| Data categories `rules[].dataCategories` | list of values (chips) | optional | — | — | — | Data categories (ADM-524), e.g. `customerContact`, `payment`, `financial`, `operational`. | `createAiGovernancePolicyDraft` body |
| Purposes `rules[].purposes` | list of values (chips) | optional | — | — | — | Permitted purposes for those categories (AIC-156, AIR-182). | `createAiGovernancePolicyDraft` body |
| Max amount `rules[].maxAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Above this value the effect escalates one step (for example to `approvalRequired`). | `createAiGovernancePolicyDraft` body |
| Roles `rules[].roleIds` | multi-picker: choose roles | optional | — | — | — | Roles the rule applies to; empty means every role. | `createAiGovernancePolicyDraft` body |
| Environments `rules[].environments` | multi-select chips | optional | — | Development · Sandbox · Staging · Production | — | ADM-525. Empty means every environment. | `createAiGovernancePolicyDraft` body |
| Conditions `rules[].conditions` | key and value settings | optional | — | — | — | Conditions attached to an `allowWithConditions` effect, for example `maskFields` or `requireCitation`. | `createAiGovernancePolicyDraft` body |
| Change note `changeNote` | text field | optional | — | — | — | — | `createAiGovernancePolicyDraft` body |

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **rule.actions**: Multi-select chips read, analyse, recommend, generate, prepare, create, modify, publish, execute, delete; grouped visually as read-only (read, analyse), advisory (recommend, generate), and changing (prepare ... delete). *(source: contracts/satellite/ai.yaml#/components/schemas/AiGovernanceRule / MoM 18 Sep 4.1)*
- **rule.effect**: One of allow, allow with conditions, prepare only, approval required, escalate, block, each with a one-line meaning. Block is an answer, logged as refused, not an error. *(source: contracts/satellite/ai.yaml#/components/schemas/AiGovernanceOutcome)*
- **rule.environments / dataCategories / roleIds / maxAmount / conditions**: Environments as chips (development, sandbox, staging, production) - e.g. "price testing allowed in sandbox, not production"; maxAmount in AED for money-moving actions; conditions as readable sentences, not JSON. *(source: contracts/satellite/ai.yaml#/components/schemas/AiGovernanceRule / MoM 18 Sep 4.1)*
- **kind / name / changeNote**: Kind action for this screen (data, scope, autonomy, approval, environment have their own boards); a change note is required for a new version. *(source: contracts/satellite/ai.yaml#createAiGovernancePolicyDraft)*

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

**Policies and versions** (data table, from `listAiGovernancePolicyVersions`)

| Shows | Format | Notes |
|---|---|---|
| Policy | the name it points at, never the id | — |
| Version | 1,234 | — |
| Status | chip: Draft, Simulated, Published, Superseded | — |
| Change note | text | — |
| Published at | 1 Oct 2026, 14:30 | — |

**Tools the rules may allow** (data table, from `listAiTools`): Read-only: tools are platform facts replicated into the tenant.

| Shows | Format | Notes |
|---|---|---|
| Target contract | text | — |
| Effect | chip: Read, Write, Destructive | — |
| Status | chip: Active, Disabled | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save draft (primary button) | `createAiGovernancePolicyDraft` POST `/governance/policy-drafts` | inline | AiGovernancePolicyVersion | — | opens modal first |
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **tool registry (read-only)**: What the executor may call - target operation, effect (read/write/destructive), risk, permission, reversible, compensation - as reference beside the rules; tenants do not edit it. *(source: contracts/satellite/ai.yaml#listAiTools / contracts/satellite/ai.yaml#setAiTool ("platform layer only"))*
- **draft state**: After save the version shows Draft with "Test before publishing" linking to ADM-527; a draft decides nothing. *(source: contracts/satellite/ai.yaml#createAiGovernancePolicyDraft)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Save draft**: Writes a draft version (new policy at version 1, or the next version of an existing one). *(source: contracts/satellite/ai.yaml#createAiGovernancePolicyDraft)*

**Data it reads**: `listAiGovernancePolicyVersions` (onLoad, Governance policies and their versions); `listAiTools` (onLoad, The tool registry); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-519` AI Governance Command Center: *Back to AI Governance Command Center*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The action permission policy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the action permission policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No action permission policy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the action permission policy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **A rule would let AI do something its capability's autonomy ceiling forbids (e.g. execute a fraud restriction)**: The rule saves (it is a draft) but carries a warning that the ceiling wins; simulation shows the effective, more restrictive result. *(source: ADR-0050 / contracts/satellite/ai.yaml#getEffectiveAiPolicy)*

#### Consistency with other screens

- Match `ADM-527`: Simulation reads exactly these rules; labels must match.
- Match `ADM-530`: Approval-routing rules are drafted with the same component (kind approval).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy: Pricing actions - Coastal Leisure Group
rules:
- capability: config.assistant
  actions:
  - prepare
  data:
  - catalogue
  - pricing
  environments:
  - production
  effect: approval required
  maxAmount: AED 50.00 per ticket change
- capability: config.assistant
  actions:
  - create
  - modify
  - publish
  environments:
  - sandbox
  - staging
  effect: allow
- capability: assistant.staff
  actions:
  - read
  data:
  - purchase history
  effect: allow
- capability: assistant.staff
  actions:
  - read
  data:
  - card details
  effect: block
```

#### Permissions

- `createAiGovernancePolicyDraft` → `AI_CONFIGURE` (configure) · staff
- `listAiGovernancePolicyVersions` → `AI_USE` (operate) · staff
- `listAiTools` → `AI_USE` (operate) · staff
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

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-523` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS14 AI Governance Board 1.dc.html#adm-523`
- Workshop pack: AI_Governance_Reference.pdf board 1
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 8: Works in AI Action & Permission Policy Builder → Define granular rules controlling what AI is allowed to read, recommend, prepare, modify or execute. This should work alongside TICVAI's existing RBAC/PBAC, not replace it.

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-523?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Save draft, Open access grant.
- [ ] Every transition is wired: `ADM-519`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-524` AI Data Access & Usage Policy

**Control which data categories each AI capability is permitted to access and for what purpose. This complements privacy/consent controls but does not replace TICVAI's core privacy governance.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-524 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW` (2 configure, 2 operate, 2 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `dataClass` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-data-access-usage-policy-adm-524` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `createAiGovernancePolicyDraft` (AI_CONFIGURE), `listAiGovernancePolicyVersions` (AI_USE), `listDataRetentionSettings` (TENANT_VIEW), `setDataRetentionSetting` (TENANT_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** What data each AI capability may read, for what purpose, and what may be shared with an external provider - e.g. the staff assistant may read a guest's purchase history but never card details. It complements, not replaces, privacy governance; retention of AI data per class is set here too. The one thing to get right: masked fields fail closed, and prompts are the only thing that leaves the platform.

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
| Data class | select | — | Guest profile · Payment record · Financial record · Audit record · Approval record · Compliance inspection · Face tag biometric · Face pass biometric · AI prompts · AI conversations · AI decision records · AI metadata index | `listDataRetentionSettings` ?dataClass |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_CONFIGURE`, `AI_USE`, `TENANT_CONFIGURE`, `TENANT_VIEW` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **data rule**: Capability × data category × purpose → allow / block, drafted as a data policy (kind data). *(source: contracts/satellite/ai.yaml#createAiGovernancePolicyDraft / MoM 18 Sep 4.1)*
- **AI retention**: Per data class (prompts and responses, conversations, decision records, approvals) - prompts 90 days by default; decision records follow the audit period; legal floors cannot be undercut. *(source: contracts/spine/tenancy.yaml#setDataRetentionSetting / ADR-0020 (AI-D05 retention per tenant))*

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

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Create (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAiGovernancePolicyVersions` (onLoad, Governance policies and their versions); `listDataRetentionSettings` (onLoad, AI data retention (prompts, conversations, decision …); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-519` AI Governance Command Center: *Back to AI Governance Command Center*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data access usage list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data access usage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data access usage yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data access usage are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, `TENANT_CONFIGURE`, `TENANT_VIEW`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A period below the class's legal minimum or above its legal maximum, a period sent for `aiMetadataIndex`, or a `followsDataClass` chain that loops |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- capability: Staff assistant
  data: Purchase history
  purpose: Answer staff questions
  effect: allow
- capability: Staff assistant
  data: Card details
  effect: block
retention:
- dataClass: AI prompts and responses
  keep: 90 days
  onExpiry: delete
- dataClass: AI decision records
  follows: Audit records
```

#### Permissions

- `createAiGovernancePolicyDraft` → `AI_CONFIGURE` (configure) · staff
- `listAiGovernancePolicyVersions` → `AI_USE` (operate) · staff
- `listDataRetentionSettings` → `TENANT_VIEW` (read) · staff
- `setDataRetentionSetting` → `TENANT_CONFIGURE` (configure) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.4 | The system should support payment servers that provide the following functions: - Record transactions below the authorization threshold - Procure authorizations over the automatic authorization … | Bundles and Promotions | CONTRACTED | `setDataRetentionSetting` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-524` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS14 AI Governance Board 1.dc.html#adm-524`
- Workshop pack: AI_Governance_Reference.pdf board 1
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 10: Works in AI Data Access & Usage Policy → Control which data categories each AI capability is permitted to access and for what purpose. This complements privacy/consent controls but does not replace TICVAI's core privacy governance.
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-524?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Create, Cancel.
- [ ] Every transition is wired: `ADM-519`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-525` Environment, Tenant & Scope Governance

**Allow different AI governance rules across TICVAI's multi-tenant and multi-environment architecture. A rule suitable for a development sandbox may not be acceptable in production.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-525 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/platform/environment-tenant-scope-governance-adm-525` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getEffectiveAiPolicy` (AI_USE), `createAiGovernancePolicyDraft` (AI_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Generate Configuration Allow Allow Allow Allow, Prepare Change Allow Allow Allow Allow, Customer Data Use … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Governance by environment, tenant and scope: what AI may do in development, sandbox, staging and production - e.g. price testing allowed in sandbox, not production; customer data synthetic in development, restricted in staging, governed in production. The one thing to get right: an environment × action matrix with the effect in each cell, read from the effective policy.

**Known correction pending (do not draw the wrong version)**

- **Matrix rows drawn as buttons ("Generate Configuration Allow Allow Allow Allow").** Why: Table rows. *(source: screens/P09-platform-admin-console.yaml#ADM-525; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Capability key | text field | — | — | `getEffectiveAiPolicy` ?capabilityKey |
| Scope path | text field | — | — | `getEffectiveAiPolicy` ?scopePath |
| Environment | radio group | — | Development · Sandbox · Staging · Production | `getEffectiveAiPolicy` ?environment |
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
| Generate Configuration Allow Allow Allow Allow (primary button) | navigation or local | — | — | — | — |
| Prepare Change Allow Allow Allow Allow (secondary button) | navigation or local | — | — | — | — |
| Customer Data Use Synthetic Restricted Restricted Governed (secondary button) | navigation or local | — | — | — | — |
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **matrix**: Rows are actions (generate configuration, prepare change, customer data use...), columns environments, cells the effect (Allow, Restricted, Synthetic only, Governed). *(source: contracts/satellite/ai.yaml#getEffectiveAiPolicy (environment) / MoM 18 Sep 4.1)*

**Data it reads**: `getEffectiveAiPolicy` (onLoad, The policy in force for a capability at a scope); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-519` AI Governance Command Center: *Back to AI Governance Command Center*; carries `capabilityKey`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The environment tenant scope list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the environment tenant scope untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No environment tenant scope yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the environment tenant scope are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
matrix:
- action: Generate configuration
  dev: Allow
  sandbox: Allow
  staging: Allow
  prod: Allow
- action: Customer data use
  dev: Synthetic
  sandbox: Restricted
  staging: Restricted
  prod: Governed
```

#### Permissions

- `getEffectiveAiPolicy` → `AI_USE` (operate) · staff
- `createAiGovernancePolicyDraft` → `AI_CONFIGURE` (configure) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-525` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS14 AI Governance Board 1.dc.html#adm-525`
- Workshop pack: AI_Governance_Reference.pdf board 1
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 12: Works in Environment, Tenant & Scope Governance → Allow different AI governance rules across TICVAI's multi-tenant and multi-environment architecture. A rule suitable for a development sandbox may not be acceptable in production.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-525?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Generate Configuration Allow Allow …, Prepare Change Allow Allow Allow Allow, Customer Data Use Synthetic Restricted …, Open access grant.
- [ ] Every transition is wired: `ADM-519`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-526` AI Policy Conflict, Exception & Override Management

**Identify conflicting governance rules and manage legitimate temporary exceptions without bypassing governance silently.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-SETUP-ADM-526 |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (3 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `exceptionId` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-policy-conflict-exception-override-management-adm-526` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getEffectiveAiPolicy` (AI_USE), `listAiGovernancePolicyVersions` (AI_USE), `createAiPolicyException` (AI_APPROVE), `revokeAiPolicyException` (AI_APPROVE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Policy conflicts and exceptions: where governance rules contradict each other (shown with the more restrictive result they resolved to), and the legitimate, time-boxed exceptions that let a capability do something a policy otherwise forbids - recorded with a reason, compensating controls, an expiry and the approver, never a silent bypass. The one thing to get right: every exception ends - an expiry is required - and revoking one makes the stricter policy apply at once.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- In Block A only createAiPolicyException is in the slice; getEffectiveAiPolicy, listAiGovernancePolicyVersions and revokeAiPolicyException are not. (CHG-SBO-006)

**Fixed on main** (the package already carries these; draw what it says): Two dataTables, one unlabelled, both bound to getEffectiveAiPolicy with no columns; no exceptions list operation. (CHG-SBO-007).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Maximum length of an exception?** → Drawn default stands (answer: "Default / recommended accepted"): No cap in the contract; the form suggests 30 days and warns beyond 90. *(decided by Chinmay, 2026-10-02; DEC-006 / CHG-NOTE-001)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Capability key | text field | — | — | `getEffectiveAiPolicy` ?capabilityKey |
| Scope path | text field | — | — | `getEffectiveAiPolicy` ?scopePath |
| Environment | radio group | — | Development · Sandbox · Staging · Production | `getEffectiveAiPolicy` ?environment |
| Policy | picker: choose a policy | — | — | `listAiGovernancePolicyVersions` ?policyId |
| Status | radio group | — | Draft · Simulated · Published · Superseded | `listAiGovernancePolicyVersions` ?status |
| Kind | select | — | Action · Data · Scope · Autonomy · Approval · Environment | `listAiGovernancePolicyVersions` ?kind |
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

**Form: Create AI policy exception** (modal, opened by *Create AI policy exception*; *Create AI policy exception* calls `createAiPolicyException`, *Cancel* sends nothing)

**Collects what `createAiPolicyException` sends before it is called.** Required: `policyId`, `reason`, `expiresAt`. Optional: `capabilityKey`, `compensatingControls`, `startsAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Policy `policyId` | picker: choose a policy | required | — | — | shows names, sends the id | — | `createAiPolicyException` body |
| Capability key `capabilityKey` | text field | optional | — | — | — | — | `createAiPolicyException` body |
| Reason `reason` | text area | required | — | max length 2000 | — | — | `createAiPolicyException` body |
| Compensating controls `compensatingControls` | list of values (chips) | optional | — | — | — | — | `createAiPolicyException` body |
| Starts at `startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createAiPolicyException` body |
| Expires at `expiresAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Required. An exception with no end is a policy change, and goes through publication. | `createAiPolicyException` body |

**Form: Revoke AI policy exception** (modal, opened by *Revoke AI policy exception*; *Revoke AI policy exception* calls `revokeAiPolicyException`, *Cancel* sends nothing)

**Collects what `revokeAiPolicyException` sends before it is called.** Required: `reason`. Names the exception and what the capability falls back to: the stricter policy applies at once to every scope the exception covered. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `revokeAiPolicyException` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is not active.

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **exception (createAiPolicyException)**: Policy and capability, reason (required), compensating controls (list of short sentences), starts at (default now), expires at (required; no open-ended option). The approver is the person granting it (AI_APPROVE), shown, not chosen. *(source: contracts/satellite/ai.yaml#createAiPolicyException / MoM 18 Sep 4.1)*
- **revoke reason**: Required; the confirmation names the exception and what the capability falls back to. *(source: contracts/satellite/ai.yaml#revokeAiPolicyException / screens/P09-platform-admin-console.yaml#ADM-526 (overlays.confirmRevokeAiPolicyException))*

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

**Policy conflicts** (data table, from `getEffectiveAiPolicy`): The conflicts `getEffectiveAiPolicy` resolved for the capability and scope, and which rule won.

| Shows | Format | Notes |
|---|---|---|
| Capability key | text | — |
| Autonomy level | 1,234 | One autonomy scale for every capability (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). |
| Autonomy ceiling | 1,234 | One autonomy scale for every capability (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). |
| Rules | list or chips (count when long) | — |
| Rule | grouped details | One rule of a governance policy version: which actions on which data, under which conditions, get which outcome (AIC-147..160). |
| Effect | chip: Allow, Allow with conditions, Prepare only, Approval required, Escalate, Block | What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). |
| Capability keys | list or chips (count when long) | Registered capabilities it applies to. Empty means every capability the policy names. |
| Actions | list or chips (count when long) | ADM-523: what AI may do, from reading to executing. |
| Data categories | list or chips (count when long) | Data categories (ADM-524), e.g. `customerContact`, `payment`, `financial`, `operational`. |
| Purposes | list or chips (count when long) | Permitted purposes for those categories (AIC-156, AIR-182). |
| Max amount | AED 1,234.50 | Above this value the effect escalates one step (for example to `approvalRequired`). |
| Roles | list or chips (count when long) | Roles the rule applies to; empty means every role. |
| Environments | list or chips (count when long) | ADM-525. Empty means every environment. |
| Conditions | grouped details | Conditions attached to an `allowWithConditions` effect, for example `maskFields` or `requireCitation`. |
| Policy key | text | — |
| Exceptions | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Policy | the name it points at, never the id | — |
| Capability key | text | — |
| Reason | text | — |

**Exceptions in force** (data table, from `getEffectiveAiPolicy`): Drawn from `getEffectiveAiPolicy.exceptions` per capability (there is no separate exceptions list): every exception, its expiry and who approved it, so none is a silent bypass.

| Shows | Format | Notes |
|---|---|---|
| Capability key | text | — |
| Reason | text | — |
| Compensating controls | list or chips (count when long) | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | Required. An exception with no end is a policy change, and goes through publication. |
| Status | chip: Active, Expired, Revoked | — |
| Approved by principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Create AI policy exception (primary button) | `createAiPolicyException` POST `/governance/policy-exceptions` | AiPolicyException | AiPolicyException | — | opens modal first |
| Revoke AI policy exception (destructive button) | `revokeAiPolicyException` POST `/governance/policy-exceptions/{exceptionId}/revoke` | inline | AiPolicyException | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is not active. | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **conflicts**: Each conflict as "Rule A says X; Rule B says Y; in force: Y (more restrictive)", with the capability and scope, e.g. an AI price increase above the configured maximum shown as blocked, never applied. A plan step failing a module limit is shown as governance-blocked. *(source: DI-955 / DI-935 / contracts/satellite/ai.yaml#getEffectiveAiPolicy)*
- **exceptions**: Active first with time left ("expires in 3 days"), then expired and revoked; each with approver, reason and controls. *(source: contracts/satellite/ai.yaml#/components/schemas/AiPolicyException)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Grant exception**: Active immediately (or at startsAt); the effective policy shows it while active. *(source: contracts/satellite/ai.yaml#createAiPolicyException)*
- **Revoke**: Status revoked; the stricter policy applies at once to every scope the exception covered. *(source: contracts/satellite/ai.yaml#revokeAiPolicyException)*

**Data it reads**: `getEffectiveAiPolicy` (onLoad, The policy in force for a capability at a scope); `listAiGovernancePolicyVersions` (onLoad, Governance policies and their versions); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-519` AI Governance Command Center: *Back to AI Governance Command Center*; carries `capabilityKey`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The policy conflict exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the policy conflict exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No policy conflict exception yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the policy conflict exception are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_APPROVE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The exception is not active. |

#### Edge cases to draw

- **Exception reaches its expiry**: Moves to Expired by itself; the list and the effective map update; the owner is notified (designer default). *(source: contracts/satellite/ai.yaml#/components/schemas/AiPolicyException (status expired))*

#### Consistency with other screens

- Match `ADM-528`: The effective policy map shows the same exceptions and conflicts.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
conflict:
  capability: config.assistant
  ruleA: 'Pricing v3: prepare price changes up to +15%'
  ruleB: 'Venue Coastal Aqua: max price change +10%'
  inForce: +10% (more restrictive)
exception:
  policy: Pricing v3
  capability: config.assistant
  reason: Eid Al Adha bulk price load for 46 products
  controls:
  - Second approver on every change
  - Changes limited to Eid dates
  expires: Sun 18 Oct 2026 23:59
  approver: Priya Nair
```

#### Permissions

- `getEffectiveAiPolicy` → `AI_USE` (operate) · staff
- `listAiGovernancePolicyVersions` → `AI_USE` (operate) · staff
- `createAiPolicyException` → `AI_APPROVE` (operate) · staff
- `revokeAiPolicyException` → `AI_APPROVE` (operate) · staff
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

- The AI policy screen shows each conflict and the more restrictive result it resolved to; a plan step failing a module limit is shown as governance-blocked and never applied. *(agreed · MoM 18 Sep 2026, M18-01 · DI-955)*
- AI policy testing lets administrators preview what would be allowed or blocked before a governance policy is published; policy conflicts (e.g. an AI price increase above a configured maximum) are flagged, never applied silently. *(client request · MoM 18 Sep 2026, 4.1 AI Governance — Capability Registration, Risk & Autonomy Configuration · DI-935)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-526` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS14 AI Governance Board 1.dc.html#adm-526`
- Workshop pack: AI_Governance_Reference.pdf board 1
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 14: Works in AI Policy Conflict, Exception & Override Management → Identify conflicting governance rules and manage legitimate temporary exceptions without bypassing governance silently.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (33 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-526?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Create AI policy exception, Revoke AI policy exception.
- [ ] Every transition is wired: `ADM-519`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-527` AI Policy Testing & Governance Simulation

**Test governance policies before activating them, so a policy mistake neither gives AI too much authority nor blocks legitimate operations.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 1 · needs the `core` module |
| Block | Block A · task APP-SETUP-ADM-527 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `versionId` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-policy-testing-governance-simulation-adm-527` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `simulateAiGovernancePolicy` (AI_CONFIGURE), `listAiGovernancePolicyVersions` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Test a draft governance policy before publishing it: replay it over recorded decisions in a time window and over the capability's test cases, and see what would be allowed, prepared, routed for approval or blocked - and what would change against today. A policy mistake either gives AI too much authority or stops legitimate work, so a version cannot be published until it has been simulated. Nothing runs. The one thing to get right: show the step-by-step evaluation for an example, the way the client's board does.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- In Block A only simulateAiGovernancePolicy is in the slice. (CHG-SBO-006)

**Fixed on main** (the package already carries these; draw what it says): The board's example (user, capability, request, steps, final decision) is pasted into purpose; layout is an unbound table and buttons. (CHG-WIR-013).

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

**Form: Simulate policy** (modal, opened by *Simulate policy*; *Simulate policy* calls `simulateAiGovernancePolicy`, *Cancel* sends nothing)

**Collects what `simulateAiGovernancePolicy` sends before it is called.** Nothing in the body is required. Optional: `from`, `to`, `capabilityKeys`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| From `from` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `simulateAiGovernancePolicy` body |
| To `to` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `simulateAiGovernancePolicy` body |
| Capability keys `capabilityKeys` | list of values (chips) | optional | — | — | — | — | `simulateAiGovernancePolicy` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The version is not a draft (already published or superseded).

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **version / window / capabilities**: A draft version (from the list), a from-to window (default last 30 days), and optionally a subset of capabilities. *(source: contracts/satellite/ai.yaml#simulateAiGovernancePolicy)*

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

**Draft versions** (data table, from `listAiGovernancePolicyVersions`)

| Shows | Format | Notes |
|---|---|---|
| Policy | the name it points at, never the id | — |
| Version | 1,234 | — |
| Status | chip: Draft, Simulated, Published, Superseded | — |
| Change note | text | — |
| Simulation summary | grouped details | The last `simulateAiGovernancePolicy` result: decisions that would change, by outcome. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Simulate policy (primary button) | `simulateAiGovernancePolicy` POST `/governance/policy-versions/{versionId}/simulate` | inline | AiPolicySimulation | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The version is not a draft (already published or superseded). | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **summary**: Decisions evaluated, how many would change, counts by outcome (allow, allow with conditions, prepare only, approval required, escalate, block) today vs with the draft. *(source: contracts/satellite/ai.yaml#/components/schemas/AiPolicySimulation (evaluated, wouldChange, byOutcome))*
- **example trace**: For each example: user permission, AI capability permission, autonomy level, environment policy, risk policy, final decision and execution - as a vertical step list with ticks and a final verdict, e.g. "ALLOW PREPARATION - execution blocked until approval". *(source: screens/P09-platform-admin-console.yaml#ADM-527 (purpose, board example) / contracts/satellite/ai.yaml#/components/schemas/AiPolicySimulation (examples))*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Run simulation**: Version moves to Simulated (required for publication); results shown; "Publish" links to ADM-528. 409 if the version is not a draft. *(source: contracts/satellite/ai.yaml#simulateAiGovernancePolicy)*

**Data it reads**: `listAiGovernancePolicyVersions` (onLoad, Governance policies and their versions); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-519` AI Governance Command Center: *Back to AI Governance Command Center*; carries `capabilityKey`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The policy testing governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the policy testing governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No policy testing governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the policy testing governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The version is not a draft (already published or superseded). |

#### Edge cases to draw

- **No recorded decisions in the window (new tenant)**: Runs on the capability's test cases only and says so. *(source: contracts/satellite/ai.yaml#simulateAiGovernancePolicy)*
- **The draft would block something that is allowed today**: Listed first, in red, as "Would now be blocked". *(source: MoM 18 Sep 4.1 (block legitimate operations) / designer default)*

#### Consistency with other screens

- Match `ADM-538`: The oversight workflow simulator uses the same step-list component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
example:
  user: Venue Administrator, Coastal Aqua
  capability: AI Configuration Assistant
  request: Increase Adult Ticket Price
  module: Pricing
  environment: Production
  risk: High
  steps:
  - User permission ✓ can modify pricing
  - AI capability ✓ can prepare pricing change
  - Autonomy L2 Prepare
  - 'Production policy: approval required'
  - 'Risk policy: commercial owner approval'
  decision: ALLOW PREPARATION
  execution: BLOCKED UNTIL APPROVAL
summary:
  evaluated: 1284
  wouldChange: 37
  nowBlocked: 4
```

#### Permissions

- `simulateAiGovernancePolicy` → `AI_CONFIGURE` (configure) · staff
- `listAiGovernancePolicyVersions` → `AI_USE` (operate) · staff
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

- AI policy testing lets administrators preview what would be allowed or blocked before a governance policy is published; policy conflicts (e.g. an AI price increase above a configured maximum) are flagged, never applied silently. *(client request · MoM 18 Sep 2026, 4.1 AI Governance — Capability Registration, Risk & Autonomy Configuration · DI-935)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-527` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS14 AI Governance Board 1.dc.html#adm-527`
- Workshop pack: AI_Governance_Reference.pdf board 1
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 16: Works in AI Policy Testing & Governance Simulation → Allow administrators to test governance policies before activating them. This is extremely important because a policy mistake could either: Allow AI too much authority, or Block legitimate TICVAI …

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-527?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Simulate policy.
- [ ] Every transition is wired: `ADM-519`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-528` AI Governance Policy Publication & Effective Policy Map

**Provide the final review, approval, versioning and publication layer for AI governance policies. No material governance policy should become active without a controlled lifecycle.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 1 · needs the `core` module |
| Block | Block A · task APP-SETUP-ADM-528 |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (3 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `versionId` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-governance-policy-publication-effective-policy-map-adm-528` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getEffectiveAiPolicy` (AI_USE), `publishAiGovernancePolicy` (AI_APPROVE), `listAiGovernancePolicyVersions` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Publication and the effective policy map: the final review where a simulated policy version is published by someone other than its author, and a map of what is actually in force for each capability at each scope - autonomy against ceiling, rules, active exceptions and resolved conflicts. The one thing to get right: the map answers "what would the decision point do here, and why", with the more restrictive rule winning visibly.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- In Block A only publishAiGovernancePolicy is in the slice. (CHG-SBO-006)

**Fixed on main** (the package already carries these; draw what it says): The "Publish AI governance policy" button is bound to no operation (op None) though publishAiGovernancePolicy is declared. (CHG-SBO-007).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Capability key | text field | — | — | `getEffectiveAiPolicy` ?capabilityKey |
| Scope path | text field | — | — | `getEffectiveAiPolicy` ?scopePath |
| Environment | radio group | — | Development · Sandbox · Staging · Production | `getEffectiveAiPolicy` ?environment |
| Policy | picker: choose a policy | — | — | `listAiGovernancePolicyVersions` ?policyId |
| Status | radio group | — | Draft · Simulated · Published · Superseded | `listAiGovernancePolicyVersions` ?status |
| Kind | select | — | Action · Data · Scope · Autonomy · Approval · Environment | `listAiGovernancePolicyVersions` ?kind |
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

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **version to publish**: Only simulated versions are publishable; the publisher must not be the drafter (the button is disabled for the author, with the reason). *(source: contracts/satellite/ai.yaml#publishAiGovernancePolicy)*
- **map filters**: Capability, scope (tenant, venue), environment. *(source: contracts/satellite/ai.yaml#getEffectiveAiPolicy)*

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

**Simulated versions** (data table, from `listAiGovernancePolicyVersions`)

| Shows | Format | Notes |
|---|---|---|
| Policy | the name it points at, never the id | — |
| Version | 1,234 | — |
| Status | chip: Draft, Simulated, Published, Superseded | — |
| Simulation summary | grouped details | The last `simulateAiGovernancePolicy` result: decisions that would change, by outcome. |
| Change note | text | — |

**Effective policy map** (detail panel, from `getEffectiveAiPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Capability key | text | — |
| Autonomy level | 1,234 | One autonomy scale for every capability (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). |
| Autonomy ceiling | 1,234 | One autonomy scale for every capability (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). |
| Rules | list or chips (count when long) | — |
| Exceptions | list or chips (count when long) | — |
| Conflicts | list or chips (count when long) | Conflicting rules and the more restrictive result they resolved to (AIC-161). |
| Resolved at | 1 Oct 2026, 14:30 | — |

**The selected version** (detail panel, from `listAiGovernancePolicyVersions`)

| Shows | Format | Notes |
|---|---|---|
| Rules | list or chips (count when long) | The rules of one policy version, stored with the version as one `jsonb` column. |
| Drafted by principal | the name it points at, never the id | — |
| Published by principal | the name it points at, never the id | — |
| Superseded at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (publish gate) | navigation or local | — | — | — | — |
| Publish AI governance policy (primary button) | `publishAiGovernancePolicy` POST `/governance/policy-versions/{versionId}/publish` | — | AiGovernancePolicyVersion | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not publishable: the version has not been simulated (`policy-not-simulated`), or the caller drafted it … | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **diff before publishing**: Rules added, removed and changed against the published version, plus the simulation summary (would change N decisions). *(source: contracts/satellite/ai.yaml#/components/schemas/AiGovernancePolicyVersion (simulationSummary))*
- **effective policy map**: Per capability and scope - autonomy "L2 Prepare (ceiling L3)", the rules in force with their source policy and version, active exceptions with expiry, conflicts with the result. *(source: contracts/satellite/ai.yaml#/components/schemas/AiEffectivePolicy)*
- **history**: Every version newest first with drafted by, published by, published at, superseded at. *(source: contracts/satellite/ai.yaml#listAiGovernancePolicyVersions)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Publish AI governance policy**: The version becomes Published and the previous one Superseded in the same step; cached decisions are invalidated. 409 policy-not-simulated or approver-is-requester shown as a sentence. *(source: contracts/satellite/ai.yaml#publishAiGovernancePolicy)*

**Data it reads**: `getEffectiveAiPolicy` (onLoad, The policy in force for a capability at a scope); `listAiGovernancePolicyVersions` (onLoad, Governance policies and their versions); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-519` AI Governance Command Center: *Back to AI Governance Command Center*; carries `capabilityKey`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance policy publication list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance policy publication untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance policy publication yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance policy publication are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_APPROVE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Not publishable: the version has not been simulated (`policy-not-simulated`), or the caller drafted it (`approver-is-requester`). |

#### Edge cases to draw

- **Two people edit and simulate the same policy**: Only the newest simulated version is publishable; older drafts show "Superseded by draft v5". *(source: designer default)*

#### Consistency with other screens

- Match `ADM-526`: Same conflict and exception rendering.
- Match `ADM-525`: Environment and scope governance feeds the same map.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
publish:
  policy: Pricing actions
  version: 4
  draftedBy: Omar Haddad
  publisher: Priya Nair
  simulation: 1,284 evaluated, 37 would change
map:
- capability: config.assistant
  scope: Coastal Aqua
  autonomy: L3 Execute with approval (ceiling L3)
  rules: Pricing actions v4; Venue max price change +10%
  exceptions: Eid bulk load until 18 Oct
```

#### Permissions

- `getEffectiveAiPolicy` → `AI_USE` (operate) · staff
- `publishAiGovernancePolicy` → `AI_APPROVE` (operate) · staff
- `listAiGovernancePolicyVersions` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-528` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS14 AI Governance Board 1.dc.html#adm-528`
- Workshop pack: AI_Governance_Reference.pdf board 1
- Flow F230 *AI Governance board 1: AI Governance Command Center*, step 18: Works in AI Governance Policy Publication & Effective Policy Map → Provide the final review, approval, versioning and publication layer for AI governance policies. No material governance policy should become active without a controlled lifecycle.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-528?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Publish AI governance policy.
- [ ] Every transition is wired: `ADM-519`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
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

**3 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"configureAiCapability": {"method":"PUT","path":"/governance/capabilities/{capabilityKey}","contract":"ai","summary":"Register a capability, or change its owner, risk class or autonomy","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiCapabilityRegistration","responds":"AiCapabilityRegistration"},
"createAiGovernancePolicyDraft": {"method":"POST","path":"/governance/policy-drafts","contract":"ai","summary":"Draft a governance policy, or a new version of one","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiGovernancePolicyVersion"},
"createAiPolicyException": {"method":"POST","path":"/governance/policy-exceptions","contract":"ai","summary":"Grant a temporary exception to a governance policy","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiPolicyException","responds":"AiPolicyException"},
"getEffectiveAiPolicy": {"method":"GET","path":"/governance/effective-policy","contract":"ai","summary":"The policy in force for a capability at a scope","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"capabilityKey","in":"query","required":true},{"name":"scopePath","in":"query","required":null},{"name":"environment","in":"query","required":null}],"requestBody":null,"responds":"AiEffectivePolicy"},
"listAiCapabilities": {"method":"GET","path":"/governance/capabilities","contract":"ai","summary":"The capability registry","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"family","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"riskClass","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiCapabilityMaturity": {"method":"GET","path":"/capability-maturity","contract":"ai","summary":"Where each AI answer stands on the way from baseline to learned","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"stage","in":"query","required":null},{"name":"capabilityKey","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiGovernanceAlerts": {"method":"GET","path":"/governance-alerts","contract":"ai","summary":"Governance alerts","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiGovernancePolicyVersions": {"method":"GET","path":"/governance/policy-versions","contract":"ai","summary":"Governance policies and their versions","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"policyId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiTools": {"method":"GET","path":"/tools","contract":"ai","summary":"The tool registry","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"targetContract","in":"query","required":null},{"name":"effect","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDataRetentionSettings": {"method":"GET","path":"/data-retention-settings","contract":"tenancy","summary":"How long the tenant keeps each class of data","permission":"TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"dataClass","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOwnPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants/mine","contract":"identity","summary":"The calling platform operator's own grants into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTenants": {"method":"GET","path":"/tenants","contract":"subscription","summary":"List tenants","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"planId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"pauseAiCapability": {"method":"POST","path":"/governance/capabilities/{capabilityKey}/pause","contract":"ai","summary":"Stop a capability now","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiCapabilityRegistration"},
"promoteAiRelease": {"method":"POST","path":"/releases/{releaseId}/promote","contract":"ai","summary":"Promote a release to its next stage (a person)","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRelease"},
"publishAiGovernancePolicy": {"method":"POST","path":"/governance/policy-versions/{versionId}/publish","contract":"ai","summary":"Publish a simulated policy version","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiGovernancePolicyVersion"},
"revokeAiPolicyException": {"method":"POST","path":"/governance/policy-exceptions/{exceptionId}/revoke","contract":"ai","summary":"End an exception before it expires","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiPolicyException"},
"setDataRetentionSetting": {"method":"PUT","path":"/data-retention-settings/{dataClass}","contract":"tenancy","summary":"Set how long the tenant keeps one class of data","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TenantDataRetentionSetting","responds":"TenantDataRetentionSetting"},
"simulateAiGovernancePolicy": {"method":"POST","path":"/governance/policy-versions/{versionId}/simulate","contract":"ai","summary":"Test a draft policy before it is published","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiPolicySimulation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAutonomyLevel": {"type":"integer","minimum":0,"maximum":4,"description":"**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."},
"AiCapabilityFamily": {"type":"string","enum":["gatewayAndModels","governance","actionPipeline","knowledgeRetrieval","assistants","analyticsInsights","configurationAssistant","forecasting","anomalyDetection","riskIntelligence","recommendations","decisionRecords","operationsEvaluation","residencyPrivacy"],"description":"The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point, action pipeline and human oversight, knowledge and retrieval, assistants, analytics assistant and insights, configuration assistant, forecasting and operational requirements, anomaly detection, fraud and risk intelligence, recommendation and upsell engine, decision records and audit, operations/evaluation/cost, residency/privacy/tenancy. **Every registered capability belongs to exactly one**, which is what `AiPolicy.enabledCapabilities` and the usage report group by."},
"AiCapabilityMaturity": {"type":"object","x-ticvai-persistence":"ai.capability_maturity","description":"**The stage of each question the venue's AI answers** (29 September, AI functions review). Written by the nightly re-estimate; a stage change is a new row, so the page can show when each answer moved.","required":["capabilityKey","stage"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string"},"suggestionKind":{"allOf":[{"$ref":"#/components/schemas/SuggestionKind"}],"nullable":true},"forecastDefinitionKey":{"type":"string","nullable":true},"stage":{"type":"string","enum":["starting","learning","established","learned"]},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producerRef":{"type":"string","description":"The producer and version answering now."},"since":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiCapabilityRegistration": {"type":"object","x-ticvai-persistence":"ai.capability","description":"**An entry in the capability registry** (design 3.1 Registry, AIC-144, AIC-145; ADM-520). Nothing becomes an operational AI capability without a row here: owner, function, risk class, autonomy, data categories and lifecycle per environment. `autonomyCeiling` is the platform ceiling for the tenant; a tenant or venue may lower `autonomyLevel`, never raise it (AIC-151).","required":["capabilityKey","family","riskClass","autonomyLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string","description":"Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`."},"family":{"$ref":"#/components/schemas/AiCapabilityFamily"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal","description":"The accountable business owner (AIC-144)."},"businessFunction":{"type":"string","nullable":true},"riskClass":{"$ref":"#/components/schemas/AiRiskClass"},"autonomyCeiling":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"readOnly":true,"description":"The first-release ceiling for this capability (design 3.8 table). Read-only to a tenant."},"autonomyLevel":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"description":"The level in force at this scope. At most `autonomyCeiling`."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories the capability reads (ADM-524)."},"lifecycle":{"type":"object","description":"Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.","properties":{"development":{"type":"string","enum":["draft","pilot","active","retired"]},"staging":{"type":"string","enum":["draft","pilot","active","retired"]},"production":{"type":"string","enum":["draft","pilot","active","retired"]}}},"degradationMode":{"type":"string","enum":["rulesOnly","searchOnly","humanHandoff","hidden","failOpen","lastPublished"],"description":"What the capability does when its model or the service is unavailable (design 3.7, AIC-241)."},"status":{"type":"string","enum":["active","paused"],"readOnly":true,"description":"Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed."},"pausedReason":{"type":"string","nullable":true,"readOnly":true},"pausedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiEffectivePolicy": {"type":"object","x-ticvai-persistence":"none — resolved from published policy versions, exceptions and ai.policy","description":"**The policy in force for a capability at a scope** (AIC-153, AIC-165; ADM-525, ADM-528): the intersection of the capability, governance policy and the tenant or venue AI policy, with where each part came from.","required":["capabilityKey","autonomyLevel","rules"],"properties":{"capabilityKey":{"type":"string"},"scopePath":{"type":"string"},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"autonomyCeiling":{"$ref":"#/components/schemas/AiAutonomyLevel"},"rules":{"type":"array","items":{"type":"object","properties":{"rule":{"$ref":"#/components/schemas/AiGovernanceRule"},"policyKey":{"type":"string"},"version":{"type":"integer"},"scopePath":{"type":"string"}}}},"exceptions":{"type":"array","items":{"$ref":"#/components/schemas/AiPolicyException"}},"conflicts":{"type":"array","items":{"type":"object","properties":{"description":{"type":"string"},"resolvedTo":{"$ref":"#/components/schemas/AiGovernanceOutcome"}}},"description":"Conflicting rules and the more restrictive result they resolved to (AIC-161)."},"resolvedAt":{"type":"string","format":"date-time"}}},
"AiGovernanceAlert": {"type":"object","x-ticvai-persistence":"ai.governance_alert","description":"**A governance alert** (design 4.4, AIC-210..223; ADM-549..555). Kept separate from operational incidents and linked where both apply (AIC-250). **`promotionReady`** (design 3.12, decided 29 September): a shadow model passed its promotion gate; the alert names the release and waits for a person to call `promoteAiRelease`. Monitoring never switches a model (AIC-252).","required":["kind","severity","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["policyViolation","crossScopeAttempt","maskingDefect","dataUsage","behaviourDrift","inputDrift","bias","overrideRateShift","controlFailed","spend","providerBreaker","evaluationRegression","forecastNotPublished","indexLag","promotionReady"]},"severity":{"type":"string","enum":["info","low","medium","high","critical"]},"capabilityKey":{"type":"string","nullable":true},"releaseId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.release","description":"For `promotionReady` and `evaluationRegression`: the release concerned."},"subjectRef":{"type":"string","nullable":true},"evidence":{"type":"object","additionalProperties":true,"nullable":true},"status":{"type":"string","enum":["open","acknowledged","dismissed","resolved","incidentOpened"],"readOnly":true},"incidentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.incident"},"raisedAt":{"type":"string","format":"date-time","readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"note":{"type":"string","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiGovernanceOutcome": {"type":"string","enum":["allow","allowWithConditions","prepareOnly","approvalRequired","escalate","block"],"description":"What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). `block` is an answer, not an error, and is logged as outcome `refused`."},
"AiGovernancePolicyVersion": {"type":"object","x-ticvai-persistence":"ai.governance_policy_version","description":"One version of a governance policy. **Published versions are never edited**: a change is a new version, and the previous one becomes `superseded` in the same transaction (AIC-165).","required":["policyId","version","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"policyId":{"type":"string","format":"uuid","x-ticvai-references":"ai.governance_policy"},"version":{"type":"integer","minimum":1},"status":{"type":"string","enum":["draft","simulated","published","superseded"]},"rules":{"$ref":"#/components/schemas/AiGovernanceRuleList"},"changeNote":{"type":"string","nullable":true},"simulationSummary":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"The last `simulateAiGovernancePolicy` result: decisions that would change, by outcome."},"draftedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"supersededAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiGovernanceRule": {"type":"object","x-ticvai-persistence":"none — held in the jsonb rules column of ai.governance_policy_version, through AiGovernanceRuleList","description":"One rule of a governance policy version: which actions on which data, under which conditions, get which outcome (AIC-147..160).","required":["effect"],"properties":{"effect":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"capabilityKeys":{"type":"array","items":{"type":"string"},"description":"Registered capabilities it applies to. Empty means every capability the policy names."},"actions":{"type":"array","items":{"type":"string","enum":["read","analyze","recommend","generate","prepare","create","modify","publish","execute","delete"]},"description":"ADM-523: what AI may do, from reading to executing."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories (ADM-524), e.g. `customerContact`, `payment`, `financial`, `operational`."},"purposes":{"type":"array","items":{"type":"string"},"description":"Permitted purposes for those categories (AIC-156, AIR-182)."},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Above this value the effect escalates one step (for example to `approvalRequired`)."},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Roles the rule applies to; empty means every role."},"environments":{"type":"array","items":{"type":"string","enum":["development","sandbox","staging","production"]},"description":"ADM-525. Empty means every environment. **`sandbox`** (18 September minutes, M18-01): the developer sandbox and a tenant's trial environment, governed apart from staging so a rule can allow in sandbox what it blocks in production."},"conditions":{"type":"object","additionalProperties":true,"nullable":true,"description":"Conditions attached to an `allowWithConditions` effect, for example `maskFields` or `requireCitation`."}}},
"AiGovernanceRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The rules of one policy version, stored with the version as one `jsonb` column.","items":{"$ref":"#/components/schemas/AiGovernanceRule"}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"AiPolicyException": {"type":"object","x-ticvai-persistence":"ai.policy_exception","description":"**A temporary, recorded exception to a governance policy** (AIC-162, ADM-526): an expiry, an approver and compensating controls. Governance is never bypassed silently.","required":["policyId","reason","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"policyId":{"type":"string","format":"uuid","x-ticvai-references":"ai.governance_policy"},"capabilityKey":{"type":"string","nullable":true},"reason":{"type":"string","maxLength":2000},"compensatingControls":{"type":"array","items":{"type":"string"}},"startsAt":{"type":"string","format":"date-time","nullable":true},"expiresAt":{"type":"string","format":"date-time","description":"Required. An exception with no end is a policy change, and goes through publication."},"status":{"type":"string","enum":["active","expired","revoked"],"readOnly":true},"approvedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"revokedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"revokedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"revokeReason":{"type":"string","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiPolicySimulation": {"type":"object","x-ticvai-persistence":"none — computed; summary kept on ai.governance_policy_version.simulationSummary","description":"What a draft policy version would have decided over recorded decisions and the test cases (ADM-527).","required":["evaluated"],"properties":{"evaluated":{"type":"integer"},"wouldChange":{"type":"integer"},"byOutcome":{"type":"object","additionalProperties":true,"description":"Counts per outcome, current against draft."},"examples":{"type":"array","items":{"type":"object","properties":{"decisionRecordId":{"type":"string","format":"uuid"},"current":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"draft":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"capabilityKey":{"type":"string"}}}}}},
"AiRelease": {"type":"object","x-ticvai-persistence":"ai.release","description":"**The release pointer per capability and tenant** (design 3.5): draft, offline evaluation, shadow, canary, production, monitored. Rollback is a pointer switch. **A model goes live only when a person promotes it** (design 3.12, decided 29 September).","required":["capabilityKey","artefactKind","candidateRef","layer","stage"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string"},"artefactKind":{"type":"string","enum":["model","prompt","routing","embedding","retrieval","rule"]},"candidateRef":{"type":"string"},"currentRef":{"type":"string","nullable":true,"description":"What production runs now: the rule, or the previously promoted artefact."},"previousRef":{"type":"string","nullable":true,"readOnly":true},"layer":{"type":"string","enum":["platform","tenant"]},"module":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"}],"nullable":true,"description":"**Whose AI this release is, and so who promotes it** (Chinmay, 2 October, workbook Q7: \"AI release promotion goes to whoever holds it\"; CHG-FUP-004). For a tenant release, `promoteAiRelease` requires the permission `contracts/shared/permissions.yaml` `x-ticvai-module-ai-publish` names for this module; a tenant release with no module cannot be promoted (`409 module-required`). Set when the release is registered, from the capability's module. Null on a platform release, which `PLATFORM_AI_MANAGE` promotes."},"suggestionKind":{"allOf":[{"$ref":"#/components/schemas/SuggestionKind"}],"nullable":true,"description":"Where the capability answers a `requestSuggestion` kind: promotion rewrites that kind's assignment in `AiPolicy.suggestionProviders`."},"stage":{"type":"string","enum":["draft","offlineEval","shadow","canary","production","monitored","rolledBack","rejected"],"readOnly":true},"shadowStartedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"gatePassedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the shadow run passed its gate and `promotionReady` was raised."},"canaryScope":{"type":"object","additionalProperties":true,"nullable":true,"description":"Venues or share of traffic in canary."},"promotedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"promotedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"rolledBackByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"rolledBackAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRiskClass": {"type":"string","enum":["low","medium","high","critical"],"description":"Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). The governance decision point scores against it."},
"AiTool": {"type":"object","x-ticvai-persistence":"ai.tool","description":"**The tool registry** (design 3.1 Registry, 3.8; AIC-088, AIC-089). The executor calls owning modules only for tools registered here: each names its target operation at a contract version, whether it reads, writes or destroys, its risk, the permission it needs, its compensation and timeout. Platform rows, replicated read-only into each tenant database with the tenant root as `scopePath`; written only by `setAiTool` (`PLATFORM_AI_MANAGE`).","x-ticvai-registered-tools-note":"Registrations the release seeds through `setAiTool` for the resources and white-label assistants (29 September, build; 1.2.59, 2.6.50), so a conversational command or a configuration plan can change a resource schedule, a booking, an allocation or the storefront theme, fonts, header, navigation, homepage and pages. Each owner operation accepts `Prefer: validate-only` (added by its owner the same day). `white-label.publishTenantConfig` is deliberately not a tool: the assistant prepares, a person publishes.","x-ticvai-registered-tools":[{"toolKey":"resources.setResourceSchedule","targetContract":"resources","targetOperation":"setResourceSchedule","effect":"write","riskClass":"medium","permission":"RESOURCE_CONFIGURE","reversible":true,"compensationOperation":"setResourceSchedule","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"resources.updateResourceBooking","targetContract":"resources","targetOperation":"updateResourceBooking","effect":"write","riskClass":"medium","permission":"RESOURCE_BOOK","reversible":true,"compensationOperation":"updateResourceBooking","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"resources.allocateResources","targetContract":"resources","targetOperation":"allocateResources","effect":"write","riskClass":"medium","permission":"RESOURCE_BOOK","reversible":true,"compensationOperation":"replaceResourceAllocation","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setTheme","targetContract":"white-label","targetOperation":"setTheme","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setFonts","targetContract":"white-label","targetOperation":"setFonts","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setHeader","targetContract":"white-label","targetOperation":"setHeader","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setNavigation","targetContract":"white-label","targetOperation":"setNavigation","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setHomepageLayout","targetContract":"white-label","targetOperation":"setHomepageLayout","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.createContentPage","targetContract":"white-label","targetOperation":"createContentPage","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"deleteContentPage","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"venue-map.generateVisitPlan","targetContract":"venue-map","targetOperation":"generateVisitPlan","effect":"write","riskClass":"low","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":null,"timeoutMs":3000,"idempotent":true,"validateOnly":false,"agent":"planner.guest"},{"toolKey":"venue-map.getVisitPlan","targetContract":"venue-map","targetOperation":"getVisitPlan","effect":"read","riskClass":"low","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":null,"timeoutMs":2000,"idempotent":true,"validateOnly":false,"agent":"planner.guest"},{"toolKey":"venue-map.listVisitPlanAlternatives","targetContract":"venue-map","targetOperation":"listVisitPlanAlternatives","effect":"read","riskClass":"low","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":null,"timeoutMs":2000,"idempotent":true,"validateOnly":false,"agent":"planner.guest"},{"toolKey":"venue-map.updateVisitPlan","targetContract":"venue-map","targetOperation":"updateVisitPlan","effect":"write","riskClass":"low","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":"updateVisitPlan","timeoutMs":3000,"idempotent":true,"validateOnly":false,"agent":"planner.guest"},{"toolKey":"venue-map.bookVisitPlan","targetContract":"venue-map","targetOperation":"bookVisitPlan","effect":"write","riskClass":"medium","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":"orders.removeCartLine","timeoutMs":5000,"idempotent":true,"validateOnly":false,"agent":"planner.guest","requiresGuestConfirmation":true}],"x-ticvai-registered-tools-planner-note":"**The planner agent's tools** (29 September, MOB-6; the assistant profile `planner.guest`, audience guest, `guestCapabilityScope` `visitPlanning`). The agent refines a rules plan by chat on GST-054 through these five `venue-map` operations, **always called as the guest whose plan it is** (permission null, the guest session's own plan), so every change is a plan version the guest can undo. `bookVisitPlan` needs the guest to press Book in the app; the agent may prepare it and never checks out. AI writes nothing outside `ai.*` (ADR-0020): the plan tables are written by the venue-map service these tools call. **Grounding** (30 September client meeting, MoM 4.7): the agent's candidates are only what these tools return for a day, i.e. the rides, dining and retail points (shops and kiosks) on the published map of that day's venue; it never proposes a point from another venue or from general knowledge, and says so when a preference is not met there (`VisitPlan.unmatchedPreferences`).","required":["toolKey","targetContract","targetOperation","effect"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"toolKey":{"type":"string"},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"contractVersion":{"type":"string"},"effect":{"type":"string","enum":["read","write","destructive"]},"riskClass":{"$ref":"#/components/schemas/AiRiskClass"},"permission":{"type":"string","description":"The permission the requester must hold for the executor to call it on their behalf."},"reversible":{"type":"boolean","description":"Non-reversible steps (a refund, a publish) need the stronger approval tier (AIC-099)."},"compensationOperation":{"type":"string","nullable":true},"timeoutMs":{"type":"integer","minimum":1},"idempotent":{"type":"boolean","default":true},"validateOnly":{"type":"boolean","default":false,"description":"The owner accepts `Prefer: validate-only` on it (design 2.3)."},"status":{"type":"string","enum":["active","disabled"]},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE","CORE_AI_PUBLISH","TICKETING_AI_PUBLISH","ACCESS_AI_PUBLISH","FNB_AI_PUBLISH","RETAIL_AI_PUBLISH","INVENTORY_AI_PUBLISH","SEATING_AI_PUBLISH","MEMBERSHIP_AI_PUBLISH","MARKETING_AI_PUBLISH","RESOURCES_AI_PUBLISH","QUEUE_AI_PUBLISH","TRANSPORT_AI_PUBLISH","GAMES_AI_PUBLISH","MAINTENANCE_AI_PUBLISH","ACCREDITATION_AI_PUBLISH","PARTNER_AI_PUBLISH","ANALYTICS_AI_PUBLISH","BIOMETRIC_IMAGE_VIEW","ACCESS_DIRECTION_SET","REPORT_GOVERNANCE_MANAGE"]},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]},
"SuspensionMode": {"type":"string","description":"Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n","enum":["readOnly","noNewSales","fullLockout"]},
"Tenant": {"x-ticvai-persistence":"control.tenant","type":"object","required":["id","code","name","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"$ref":"#/components/schemas/TenantStatus"},"suspensionMode":{"$ref":"#/components/schemas/SuspensionMode"},"suspensionReason":{"type":"string","nullable":true},"suspensionEffectiveAt":{"type":"string","format":"date-time","nullable":true,"description":"When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."},"suspensionNoticeMessage":{"$ref":"#/components/schemas/LocalisedText","description":"The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."},"terminationScheduledAt":{"type":"string","format":"date-time","nullable":true,"description":"When `terminateTenant` started the retention window. Null when no termination is under way."},"terminationRetentionUntil":{"type":"string","format":"date-time","nullable":true,"description":"`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."},"terminationReason":{"type":"string","maxLength":1000,"nullable":true},"terminationRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"planId":{"type":"string","format":"uuid","nullable":true},"planName":{"type":"string","nullable":true},"cellCount":{"type":"integer"},"venueCount":{"type":"integer"},"regionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500,"nullable":true,"description":"Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."},"accountManagerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantDataRetentionClass": {"type":"string","description":"**The data classes a tenant sets a retention period for** (decided 29 September, Chinmay: all data retention is tenant configuration, one setting per class). Defaults are ADR-0047's and the AI system design's (section 8, decision 5); a legal limit is the only thing the platform enforces.\n| Class | Default | Counted from | Legal limit (refused) | |---|---|---|---| | `guestProfile` | 5 years | last activity | none | | `paymentRecord` | 10 years | created | at least 10 years (4.3.4) | | `financialRecord` | 7 years | created | at least 7 years (6.1.78) | | `auditRecord` | 2 years (authorisation and device audit) | created | none | | `approvalRecord` | 7 years (approvals board 6.7) | decided | none | | `complianceInspection` | 7 years | created | none | | `faceTagBiometric` | 7 days | ticket expiry | make-or-break | | `facePassBiometric` | follows `guestProfile` | last activity | make-or-break | | `aiPrompts` | 90 days (prompts and responses) | created | none | | `aiConversations` | 90 days | last activity | none | | `aiDecisionRecords` | follows `auditRecord` (decision records and the approvals of AI actions) | decided | none | | `aiMetadataIndex` | always follows `aiDecisionRecords` (summaries, entities, embeddings) | created | none |\n**ADR-0047's floors and ceilings that are not law are defaults now, not refusals** (the audit floor of one year, the proposed seven-year guest-profile ceiling, the Face Tag thirty-day ceiling). Platform-owned copies — the burst environment copy, a decommissioned cell — are not tenant data classes and are not here.\n","enum":["guestProfile","paymentRecord","financialRecord","auditRecord","approvalRecord","complianceInspection","faceTagBiometric","facePassBiometric","aiPrompts","aiConversations","aiDecisionRecords","aiMetadataIndex"]},
"TenantDataRetentionSetting": {"type":"object","x-ticvai-persistence":"tenancy.data_retention_setting","description":"**One tenant's retention period for one data class** (decided 29 September, Chinmay). One row per tenant and class, written by `setDataRetentionSetting`; a class with no row takes the platform default. The limit and default fields are the platform's catalogue, computed for the response and not stored on the row.\n","required":["dataClass"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"dataClass":{"allOf":[{"$ref":"#/components/schemas/TenantDataRetentionClass"}],"x-ticvai-unique":"tenant","description":"One row per class per tenant. On a write it comes from the path; a body value is ignored."},"retainAmount":{"type":"integer","nullable":true,"minimum":0,"description":"The tenant's period. Null with no `followsDataClass` means the platform default applies. Zero means the data is not kept past the transaction that produced it.\n"},"retainUnit":{"type":"string","nullable":true,"enum":["days","months","years"],"description":"Required with `retainAmount`."},"followsDataClass":{"allOf":[{"$ref":"#/components/schemas/TenantDataRetentionClass"}],"nullable":true,"description":"Keep this class for as long as another class is kept. Set by default for `aiDecisionRecords` (follows `auditRecord`), `facePassBiometric` (follows `guestProfile`) and `aiMetadataIndex` (follows `aiDecisionRecords`, and cannot be changed).\n"},"onExpiry":{"type":"string","enum":["archive","anonymise","delete"],"default":"archive","description":"ADR-0047's stages. `archive` moves the data to the archive instance, from where it is erased on the class's own schedule; derived stores (the AI index, search) purge at archive, not later.\n"},"anchor":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"enum":["createdAt","lastActivity","decidedAt","ticketExpiry"],"description":"What the period is counted from. Fixed per class by the platform."},"effectiveAmount":{"type":"integer","readOnly":true,"x-ticvai-persisted":false,"description":"The period actually applied, after follows and defaults are resolved."},"effectiveUnit":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"isDefault":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"True when the tenant has not set this class and the platform default applies."},"defaultAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false},"defaultUnit":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"legalMinimumAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"A floor the law sets. A shorter period is refused (`422`)."},"legalMaximumAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"A maximum the law sets. A longer period is refused (`422`). Null for every class until the biometric make-or-break is answered."},"legalLimitUnit":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"legalBasis":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"The law or requirement the limit comes from, e.g. `4.3.4`."},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"updatedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The tenant. Retention is set at tenant scope only."}}},
"TenantStatus": {"type":"string","enum":["onboarding","active","suspended","terminating","terminated"]}
}
```
