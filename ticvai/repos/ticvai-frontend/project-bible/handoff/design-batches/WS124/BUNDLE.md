# WS124 — AI Governance board 4

**10 screens · 22 operations · 21 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `AI_APPROVE, AI_AUDIT_VIEW, AI_CONFIGURE, AI_USE, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
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
| `ADM-549` | AI Governance Monitoring Command Center | D | 8 | 33 | 7 | 4 | 1 | 0 | — | notStarted (—) |
| `ADM-550` | AI Risk Register & Risk Exposure Management | D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-551` | AI Governance Control Library & Control Effectiveness | D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-552` | AI Policy Compliance & Violation Monitoring | D | 6 | 20 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-553` | AI Data, Privacy & Usage Compliance Monitoring | D | 6 | 40 | 7 | 1 | 0 | 4 | — | notStarted (—) |
| `ADM-554` | AI Quality, Behavior & Governance Drift Monitoring | A | 15 | 25 | 7 | 2 | 0 | 0 | — | notStarted (—) |
| `ADM-555` | AI Governance Alert & Detection Center | D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-556` | AI Incident & Remediation Management | A | 25 | 19 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-557` | AI Compliance, Assurance & Governance Reporting | D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-558` | AI Governance Review, Action Plan & Continuous Improvement | D | 7 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-549` AI Governance Monitoring Command Center

**Provide executives, governance teams and authorized administrators with one centralized real-time view of AI governance health across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-549 |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 read, 2 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/platform/ai-governance-monitoring-command-center-adm-549` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listAiGovernanceAlerts` (AI_USE), `listAiIncidents` (AI_USE), `listAiCapabilityHealth` (AI_USE), `getAiUsage` (AI_AUDIT_VIEW) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-012): catalogue listGovernanceRiskMonitoring (PRODUCT_VIEW) is a product-governance read attached by name resemblance; AI governance health comes from the ai …

**From the AI & Intelligence process.** Governance monitoring: AI health in production per capability (availability, latency, errors, breaker, degraded, data freshness), spend by agent with the month-end projection labelled a forecast, open alerts and incidents. The one thing to get right: degraded capabilities say what they are doing instead (their degradation mode).

**Fixed on main** (the package already carries these; draw what it says): Declares catalogue listGovernanceRiskMonitoring (PRODUCT_VIEW). (CHG-WIR-012).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Search governance monitoring | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, capability, module, environment, risk and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Policy violation · Cross scope attempt · Masking defect · Data usage · Behaviour drift · Input drift · Bias · Override rate shift · Control failed · Spend · Provider breaker · Evaluation regression … | `listAiGovernanceAlerts` ?kind |
| Status | radio group | — | Open · Acknowledged · Dismissed · Resolved · Incident opened | `listAiGovernanceAlerts` ?status |
| Severity | radio group | — | Info · Low · Medium · High · Critical | `listAiGovernanceAlerts` ?severity |
| Status | radio group | — | Open · Contained · Investigating · Remediating · Closed | `listAiIncidents` ?status |
| Severity | radio group | — | Low · Medium · High · Critical | `listAiIncidents` ?severity |
| Breaker state | segmented control | — | Closed · Half open · Open | `listAiCapabilityHealth` ?breakerState |
| From | date picker | — | — | `getAiUsage` ?from |
| Group by | select | — | Tenant · Venue · Principal · Provider · Capability · Day · Agent · Model · Task | `getAiUsage` ?groupBy |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_AUDIT_VIEW`, `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

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

**Capability health** (data table, from `listAiCapabilityHealth`): **Overall AI health in production** (21 September minutes, M21-13).

| Shows | Format | Notes |
|---|---|---|
| Capability key | text | — |
| Availability | 1,234.5 | — |
| P95 latency ms | 1,234 | — |
| Error rate | 12.5% | — |
| Breaker state | chip: Closed, Half open, Open | — |
| Degraded | yes / no (icon or chip) | Answering from its degradation mode (rules only, search only, a person). |
| Data freshness | text | e.g. index lag, the last forecast published. |

**Spend by agent** (chart, from `getAiUsage`): `getAiUsage` grouped by `agent`, with the month-end projection labelled a forecast: which agents consume the most, and for what (M21-13).

| Shows | Format | Notes |
|---|---|---|
| Currency | text | The tenant's selected currency, by default its billing currency (AED for a UAE tenant), not USD (CHG-RUL-017; Chinmay, 2 October, workbook … |
| Ceiling | grouped details | The spend ceiling in force (`getAiSpendCeiling`), with the tokens it equals at the current blended rate and what is used so far … |
| Spend | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tokens | 1,234 | — |
| Used spend | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Used tokens | 1,234 | — |
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | text | — |
| Rows | list or chips (count when long) | — |
| Key | text | — |
| Interactions | 1,234 | — |
| Prompt tokens | 1,234 | — |
| Completion tokens | 1,234 | — |
| Cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| P95 latency ms | 1,234 | — |
| Refusal rate | 12.5% | — |
| Rejection rate | 12.5% | Proposals a person refused. The number that says whether the assistant is worth having, and the one nobody thinks to measure. |
| Forecast | grouped details | A month-end projection, labelled a forecast (AI design 2.3, 4.5). Present where `to` is inside the current month. |
| Label | chip: Forecast | — |

**Active AI Capabilities** (metric tile)

**AI Decisions Today** (metric tile)

**Governance Compliance Rate** (metric tile)

**Policy Violations** (metric tile)

**High-Risk Events** (metric tile)

**Critical AI Events** (metric tile)

**Open AI Incidents** (metric tile)

**Active Exceptions** (metric tile)

**Controls Passing** (metric tile)

**Controls Failing** (metric tile)

**AI Capabilities Under Review** (metric tile)

**Governance Health Score** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **capability health**: Rows with availability, p95 latency, error rate, breaker (closed/open), degraded and data freshness. *(source: contracts/satellite/ai.yaml#listAiCapabilityHealth)*
- **spend by agent**: Bars per agent; projection dashed and labelled forecast. *(source: DI-973 / contracts/satellite/ai.yaml#getAiUsage)*

**Data it reads**: `listAiGovernanceAlerts` (onLoad, Governance alerts); `listAiIncidents` (onLoad, AI incidents); `listAiCapabilityHealth` (onLoad, Health per capability); `getAiUsage` (onLoad, Consumption by agent); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-550` AI Risk Register & Risk Exposure Management: *AI Risk Register & Risk Exposure Management*; carries `tenantId`
- → `ADM-551` AI Governance Control Library & Control Effectiveness: *AI Governance Control Library & Control Effectiveness*; carries `tenantId`
- → `ADM-552` AI Policy Compliance & Violation Monitoring: *AI Policy Compliance & Violation Monitoring*; carries `tenantId`
- → `ADM-553` AI Data, Privacy & Usage Compliance Monitoring: *AI Data, Privacy & Usage Compliance Monitoring*; carries `tenantId`
- → `ADM-554` AI Quality, Behavior & Governance Drift Monitoring: *AI Quality, Behavior & Governance Drift Monitoring*; carries `releaseId`
- → `ADM-555` AI Governance Alert & Detection Center: *AI Governance Alert & Detection Center*; carries `tenantId`
- → `ADM-556` AI Incident & Remediation Management: *AI Incident & Remediation Management*; carries `capabilityKey`, `incidentId`, `releaseId`
- → `ADM-557` AI Compliance, Assurance & Governance Reporting: *AI Compliance, Assurance & Governance Reporting*; carries `tenantId`
- → `ADM-558` AI Governance Review, Action Plan & Continuous Improvement: *AI Governance Review, Action Plan & Continuous Improvement*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance monitoring list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance monitoring untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance monitoring yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance monitoring are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_AUDIT_VIEW`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
health:
- capability: assistant.guest
  availability: 99.9%
  p95: 2.1 s
  errors: 0.3%
  breaker: closed
- capability: recommend.checkout
  degraded: true
  mode: rules only
```

#### Permissions

- `listAiGovernanceAlerts` → `AI_USE` (operate) · staff
- `listAiIncidents` → `AI_USE` (operate) · staff
- `listAiCapabilityHealth` → `AI_USE` (operate) · staff
- `getAiUsage` → `AI_AUDIT_VIEW` (read) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.7 | AI Usage Analytics System shall provide reporting on AI usage and outcomes. | Unified Operations Dashboard | CONTRACTED | `getAiUsage` |
| 8.4.27 | System shall support AI usage monitoring. | Unified Operations Dashboard | CONTRACTED | `getAiUsage` |
| 8.7.10 | System shall provide AI analytics dashboards. | Unified Operations Dashboard | CONTRACTED | `getAiUsage` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI governance shows overall AI health in production and spend by agent, with the month-end projection labelled a forecast. *(agreed · MoM 21 Sep 2026, M21-13 · DI-973)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-549` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-549`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 1: Opens AI Governance Monitoring Command Center → Provide executives, governance teams and authorized administrators with one centralized real-time view of AI governance health across TICVAI.
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F233 branch at step 1 (expected): when Nothing has been set up on AI Governance Monitoring Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F233 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (33 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-549?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-002`, `ADM-550`, `ADM-551`, `ADM-552`, `ADM-553`, `ADM-554`, `ADM-555`, `ADM-556`, `ADM-557`, `ADM-558`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-550` AI Risk Register & Risk Exposure Management

**Maintain the enterprise risk register specifically for TICVAI AI capabilities. Board 1 classifies individual capabilities/actions. Board 4 manages the ongoing risk exposure after those capabilities are operational.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-550 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `entryId` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-risk-register-risk-exposure-management-adm-550` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listAiRiskRegister` (AI_USE), `setAiRiskRegisterEntry` (AI_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack names 21 actions on this screen and the screen declares 0 operations.** Unserved: Customer, Commercial, Financial, Operational, Security, Model / AI Quality, Risk Matrix, Critical …. Each … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** The AI risk register: risks across customer, commercial, financial, operational, security, model quality, privacy and compliance, each with likelihood, impact, controls, residual rating, treatment and owner. The one thing to get right: a likelihood × impact matrix with each risk placed, and residual rating after controls.

**Known correction pending (do not draw the wrong version)**

- **Categories and "Risk Matrix" drawn as buttons.** Why: Category filter chips and a matrix view. *(source: screens/P09-platform-admin-console.yaml#ADM-550; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | select | — | Customer · Commercial · Financial · Operational · Security · Model quality · Privacy · Compliance | `listAiRiskRegister` ?category |
| Status | radio group | — | Open · Mitigating · Accepted · Closed | `listAiRiskRegister` ?status |
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

- **entry**: Title, category, capabilities, likelihood and impact (1-5), controls, residual rating, treatment (accept, mitigate, transfer, avoid), owner, status. *(source: contracts/satellite/ai.yaml#setAiRiskRegisterEntry)*

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
| Customer (primary button) | navigation or local | — | — | — | — |
| Commercial (secondary button) | navigation or local | — | — | — | — |
| Financial (secondary button) | navigation or local | — | — | — | — |
| Operational (secondary button) | navigation or local | — | — | — | — |
| Security (secondary button) | navigation or local | — | — | — | — |
| Model / AI Quality (secondary button) | navigation or local | — | — | — | — |
| Risk Matrix (secondary button) | navigation or local | — | — | — | — |
| Critical (secondary button) | navigation or local | — | — | — | — |
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Data it reads**: `listAiRiskRegister` (onLoad, The AI risk register); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The risk register risk list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the risk register risk untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No risk register risk yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the risk register risk are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entry:
  title: Upsell offers a sold-out add-on
  category: customer
  likelihood: 3
  impact: 2
  controls:
  - Availability check before display
  residual: low
  treatment: mitigate
  owner: Fatima Al Mansoori
```

#### Permissions

- `listAiRiskRegister` → `AI_USE` (operate) · staff
- `setAiRiskRegisterEntry` → `AI_CONFIGURE` (configure) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-550` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-550`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 2: Works in AI Risk Register & Risk Exposure Management → Maintain the enterprise risk register specifically for TICVAI AI capabilities. Board 1 classifies individual capabilities/actions. Board 4 manages the ongoing risk exposure after those capabilities …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-550?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Customer, Commercial, Financial, Operational, Security, Model / AI Quality, Risk Matrix, Critical, Open access grant.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-551` AI Governance Control Library & Control Effectiveness

**Define and continuously test whether the controls designed to govern AI are actually working. A policy existing on paper does not mean the control is effective.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-551 |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 read, 2 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `controlKey` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-governance-control-library-control-effectiveness-adm-551` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listAiControls` (AI_USE), `runAiControlTest` (AI_AUDIT_VIEW) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Control library and effectiveness: the controls that govern AI (masking, isolation, approval gates, autonomy ceilings, budget limits) and whether each actually works, tested automatically or by hand with evidence. The one thing to get right: a control that has never been tested shows as "untested", not effective.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Effectiveness | radio group | — | Effective · Partially effective · Ineffective · Untested | `listAiControls` ?effectiveness |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_AUDIT_VIEW`, `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

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

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **controls**: Control, kind (automatic/manual), last test, result, evidence, next due. *(source: contracts/satellite/ai.yaml#listAiControls / contracts/satellite/ai.yaml#runAiControlTest)*

**Data it reads**: `listAiControls` (onLoad, Governance controls); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance effectiveness list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance effectiveness untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance effectiveness yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance effectiveness are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_AUDIT_VIEW`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
control:
  key: masking.pii
  name: Personal data masked before a prompt leaves
  lastTest: 1 Oct
  result: pass
```

#### Permissions

- `listAiControls` → `AI_USE` (operate) · staff
- `runAiControlTest` → `AI_AUDIT_VIEW` (read) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-551` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-551`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 4: Works in AI Governance Control Library & Control Effectiveness → Define and continuously test whether the controls designed to govern AI are actually working. A policy existing on paper does not mean the control is effective.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-551?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Cancel.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-552` AI Policy Compliance & Violation Monitoring

**Continuously detect AI activity that violates or attempts to violate Board 1 governance policies.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-552 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Compliance KPIs) and a per-row directory (§Show) — counts over a population, then the population |
| Offline | online only |
| Opens with | `alertId` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-policy-compliance-violation-monitoring-adm-552` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listAiGovernanceAlerts` (AI_USE), `decideAiGovernanceAlert` (AI_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the AI & Intelligence process.** Policy violations: AI activity that broke or tried to break governance (e.g. a price change beyond the maximum), the path from request to block to alert, and repeated attempts. The one thing to get right: a violation attempt that was blocked is shown as working governance, with repeated attempts flagged.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Policy violation · Cross scope attempt · Masking defect · Data usage · Behaviour drift · Input drift · Bias · Override rate shift · Control failed · Spend · Provider breaker · Evaluation regression … | `listAiGovernanceAlerts` ?kind |
| Status | radio group | — | Open · Acknowledged · Dismissed · Resolved · Incident opened | `listAiGovernanceAlerts` ?status |
| Severity | radio group | — | Info · Low · Medium · High · Critical | `listAiGovernanceAlerts` ?severity |
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

**Evaluated Actions** (metric tile)

**Compliant** (metric tile)

**Blocked by Policy** (metric tile)

**Policy Violations** (metric tile)

**Attempted Violations** (metric tile)

**Exception-Based Actions** (metric tile)

**Unknown / Unclassified Actions** (metric tile)

**Every policy compliance violation** (data table)

| Shows | Format | Notes |
|---|---|---|
| Request | text | not in the schema: `Request` |
| → governance evaluation | text | not in the schema: `→ Governance Evaluation` |
| → violation detected | text | not in the schema: `→ Violation Detected` |
| → execution blocked | text | not in the schema: `→ Execution Blocked` |
| → alert created | text | not in the schema: `→ Alert Created` |
| Repeated violation detection | text | not in the schema: `Repeated Violation Detection` |
| 14 times in 24 hours | text | not in the schema: `14 times in 24 hours` |

**The selected policy compliance violation** (detail panel): The pack groups this record's detail under its own headings: “Actor”.

| Shows | Format | Notes |
|---|---|---|
| Request | text | not in the schema: `Request` |
| → governance evaluation | text | not in the schema: `→ Governance Evaluation` |
| → violation detected | text | not in the schema: `→ Violation Detected` |
| → execution blocked | text | not in the schema: `→ Execution Blocked` |
| → alert created | text | not in the schema: `→ Alert Created` |
| Repeated violation detection | text | not in the schema: `Repeated Violation Detection` |
| 14 times in 24 hours | text | not in the schema: `14 times in 24 hours` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **violation path**: Request → governance evaluation → violation → execution blocked → alert, with count ("14 times in 24 hours"). *(source: contracts/satellite/ai.yaml#listAiGovernanceAlerts (policyViolation, crossScopeAttempt) / MoM 18 Sep 4.4)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Acknowledge / Dismiss / Resolve / Open incident**: Records the decision on the alert. *(source: contracts/satellite/ai.yaml#decideAiGovernanceAlert)*

**Data it reads**: `listAiGovernanceAlerts` (onLoad, Governance alerts); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The policy compliance violation list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the policy compliance violation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No policy compliance violation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the policy compliance violation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The alert is already closed (`alert-not-open`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
violation:
  capability: config.assistant
  request: Raise Adult price +22%
  rule: Max price change +15%
  result: Blocked
  repeated: 3 times today
```

#### Permissions

- `listAiGovernanceAlerts` → `AI_USE` (operate) · staff
- `decideAiGovernanceAlert` → `AI_CONFIGURE` (configure) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-552` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-552`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 6: Works in AI Policy Compliance & Violation Monitoring → Continuously detect AI activity that violates or attempts to violate Board 1 governance policies.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-552?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-553` AI Data, Privacy & Usage Compliance Monitoring

**Monitor whether AI capabilities are actually using data according to the policies configured in Board 1. This screen is monitoring—not the configuration of the data policies themselves.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-553 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Data Usage KPIs) and a per-row directory (§Show) — counts over a population, then the population |
| Offline | online only |
| Opens with | `alertId` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-data-privacy-usage-compliance-monitoring-adm-553` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listAiGovernanceAlerts` (AI_USE), `decideAiGovernanceAlert` (AI_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the AI & Intelligence process.** Data and privacy monitoring: whether AI actually uses data as policy allows - which data categories were sent to which provider, prohibited data detected, data minimisation (requested vs actually sent). The one thing to get right: what left the platform is shown as categories and counts, never the content itself.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Policy violation · Cross scope attempt · Masking defect · Data usage · Behaviour drift · Input drift · Bias · Override rate shift · Control failed · Spend · Provider breaker · Evaluation regression … | `listAiGovernanceAlerts` ?kind |
| Status | radio group | — | Open · Acknowledged · Dismissed · Resolved · Incident opened | `listAiGovernanceAlerts` ?status |
| Severity | radio group | — | Info · Low · Medium · High · Critical | `listAiGovernanceAlerts` ?severity |
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

**AI Data Requests** (metric tile)

**Allowed** (metric tile)

**Conditionally Allowed** (metric tile)

**Blocked** (metric tile)

**External Transfers** (metric tile)

**Masked / Redacted** (metric tile)

**Data Policy Violations** (metric tile)

**Unknown Data Categories** (metric tile)

**Every data privacy usage** (data table)

| Shows | Format | Notes |
|---|---|---|
| Provider | text | not in the schema: `Provider` |
| Approved provider a | text | not in the schema: `Approved Provider A` |
| Data categories sent | text | not in the schema: `Data Categories Sent` |
| Product | text | not in the schema: `Product` |
| Basket context | text | not in the schema: `Basket Context` |
| Venue | text | not in the schema: `Venue` |
| Prohibited data | text | not in the schema: `Prohibited Data` |
| Full payment details | text | not in the schema: `Full Payment Details` |
| Restricted PII | text | not in the schema: `Restricted PII` |
| Data minimization monitoring | text | not in the schema: `Data Minimization Monitoring` |
| Requested data | text | not in the schema: `Requested Data` |
| Actually sent | text | not in the schema: `Actually Sent` |
| 24 available fields | text | not in the schema: `24 available fields` |
| ↓ | text | not in the schema: `↓` |
| 8 required fields | text | not in the schema: `8 required fields` |
| 6 sent after masking | text | not in the schema: `6 sent after masking` |
| Sensitive data alert | text | not in the schema: `Sensitive Data Alert` |

**The selected data privacy usage** (detail panel): The pack groups this record's detail under its own headings: “Data Usage Matrix”, “HIGH”, “Response”.

| Shows | Format | Notes |
|---|---|---|
| Provider | text | not in the schema: `Provider` |
| Approved provider a | text | not in the schema: `Approved Provider A` |
| Data categories sent | text | not in the schema: `Data Categories Sent` |
| Product | text | not in the schema: `Product` |
| Basket context | text | not in the schema: `Basket Context` |
| Venue | text | not in the schema: `Venue` |
| Prohibited data | text | not in the schema: `Prohibited Data` |
| Full payment details | text | not in the schema: `Full Payment Details` |
| Restricted PII | text | not in the schema: `Restricted PII` |
| Data minimization monitoring | text | not in the schema: `Data Minimization Monitoring` |
| Requested data | text | not in the schema: `Requested Data` |
| Actually sent | text | not in the schema: `Actually Sent` |
| 24 available fields | text | not in the schema: `24 available fields` |
| ↓ | text | not in the schema: `↓` |
| 8 required fields | text | not in the schema: `8 required fields` |
| 6 sent after masking | text | not in the schema: `6 sent after masking` |
| Sensitive data alert | text | not in the schema: `Sensitive Data Alert` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **data sent by provider**: Provider, data categories sent, prohibited categories detected (e.g. full payment details - should be zero), fields requested vs sent. *(source: contracts/satellite/ai.yaml#listAiGovernanceAlerts (maskingDefect, dataUsage) / ADR-0020)*

**Data it reads**: `listAiGovernanceAlerts` (onLoad, Governance alerts); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data privacy usage list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data privacy usage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data privacy usage yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data privacy usage are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The alert is already closed (`alert-not-open`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  provider: Azure OpenAI (UAE North)
  categories:
  - Product
  - Basket context
  - Venue
  prohibited: 0
  minimisation: 6 of 24 available fields sent
```

#### Permissions

- `listAiGovernanceAlerts` → `AI_USE` (operate) · staff
- `decideAiGovernanceAlert` → `AI_CONFIGURE` (configure) · staff
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

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-553` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-553`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 8: Works in AI Data, Privacy & Usage Compliance Monitoring → Monitor whether AI capabilities are actually using data according to the policies configured in Board 1. This screen is monitoring—not the configuration of the data policies themselves.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-553?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-554` AI Quality, Behavior & Governance Drift Monitoring

**Detect meaningful changes in AI behavior that may increase governance risk. This is not the full model monitoring platform. Board 4 focuses specifically on governance-relevant behavioral changes.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 1 · needs the `core` module |
| Block | Block A · ticket #28977 (APP-SETUP-ADM-554) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (3 operate, 1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `releaseId` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-quality-behavior-governance-drift-monitoring-adm-554` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `runAiEvaluation` (AI_CONFIGURE), `listAiEvaluations` (AI_USE), `promoteAiRelease` (AI_USE), `rollbackAiRelease` (AI_APPROVE), `listAiGovernanceAlerts` (AI_USE), `listAiTrainingRuns` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it. **The generator's 'needs a person' gap removed 4 October 2026: the screen's content is defined (tables, panels and actions bound to its operations)** (CHG-FXS-005)

**From the AI & Intelligence process.** Behaviour drift, training runs and model promotion: where a governance lead sees whether AI behaviour has shifted in a way that matters, how each per-tenant training and backtest run did, and where a model that has passed its gate in the background is promoted - by a person, one stage at a time - or rolled back. The one thing to get right: "Ready to promote" is a recommendation with its evidence (the gate figures against the baseline); nothing switches by itself, and the empty state is normal for months.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- In Block A only promoteAiRelease, rollbackAiRelease and runAiEvaluation are in the slice; listAiGovernanceAlerts, listAiEvaluations and listAiTrainingRuns are not. (CHG-SBO-006)

**Fixed on main** (the package already carries these; draw what it says): Layout has an unbound table, an unlabelled primary button and a publishGate with no operation. (CHG-SBO-007).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is promotion a tenant decision (tenant admin with AI_APPROVE) or TICVAI's?** → Role builder: roles are preset permission configurations (All, Viewer, Mid-level and the like), not fixed default roles. Picking a preset fills the per-module permission checklist, which stays editable, and the role can be renamed. Each module carries its own "Publish AI model" permission; AI release promotion goes to whoever holds it (Pre-apply round, 2 October). *(decided by Chinmay, 2026-10-02; DEC-007 / CHG-NOTE-001)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Release | picker: choose a release | — | — | `listAiEvaluations` ?releaseId |
| Capability key | text field | — | — | `listAiEvaluations` ?capabilityKey |
| Status | radio group | — | Queued · Running · Passed · Failed · Error | `listAiEvaluations` ?status |
| Kind | select | — | Policy violation · Cross scope attempt · Masking defect · Data usage · Behaviour drift · Input drift · Bias · Override rate shift · Control failed · Spend · Provider breaker · Evaluation regression … | `listAiGovernanceAlerts` ?kind |
| Status | radio group | — | Open · Acknowledged · Dismissed · Resolved · Incident opened | `listAiGovernanceAlerts` ?status |
| Severity | radio group | — | Info · Low · Medium · High · Critical | `listAiGovernanceAlerts` ?severity |
| Capability key | text field | — | — | `listAiTrainingRuns` ?capabilityKey |
| Status | select | — | Queued · Training · Backtesting · Shadow · Gate passed · Gate failed · Failed | `listAiTrainingRuns` ?status |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Run evaluation** (modal, opened by *Run evaluation*; *Run evaluation* calls `runAiEvaluation`, *Cancel* sends nothing)

**Collects what `runAiEvaluation` sends before it is called.** Required: `suiteId`, `candidateRef`, `kind`. Optional: `releaseId`, `baselineRef`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Suite `suiteId` | picker: choose a suite | required | — | — | shows names, sends the id | — | `runAiEvaluation` body |
| Release `releaseId` | picker: choose a release | optional | — | — | shows names, sends the id | — | `runAiEvaluation` body |
| Candidate ref `candidateRef` | text field | required | — | — | — | — | `runAiEvaluation` body |
| Baseline ref `baselineRef` | text field | optional | — | — | — | — | `runAiEvaluation` body |
| Kind `kind` | segmented control | required | — | Offline · Backtest · Shadow | — | — | `runAiEvaluation` body |

**Form: Promote release** (modal, opened by *Promote release*; *Promote release* calls `promoteAiRelease`, *Cancel* sends nothing)

**Collects what `promoteAiRelease` sends before it is called.** Nothing in the body is required. Optional: `toStage`, `canaryScope`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To stage `toStage` | segmented control | optional | — | Canary · Production | — | — | `promoteAiRelease` body |
| Canary scope `canaryScope` | key and value settings | optional | — | — | — | — | `promoteAiRelease` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `promoteAiRelease` body |

Errors to draw in the form: 403 A tenant release, and the caller does not hold the AI publish permission of its module (`module-ai-publish-required`, CHG-FUP-004); or a platform release, and …; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not promotable: the gate has not passed (`gate-not-passed`), an isolation case failed (`isolation-cases-failed`), the stage cannot follow the current one …

**Form: Roll back release** (modal, opened by *Roll back release*; *Roll back release* calls `rollbackAiRelease`, *Cancel* sends nothing)

**Collects what `rollbackAiRelease` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `rollbackAiRelease` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Nothing to roll back to (`no-previous-release`).

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **promote (toStage, canaryScope, note)**: Next stage only (shadow → canary → production); canary scope e.g. one venue or a share of traffic; note optional. *(source: contracts/satellite/ai.yaml#promoteAiRelease)*
- **rollback reason**: Required; the confirmation says what production returns to (the previous artefact or the rule). *(source: contracts/satellite/ai.yaml#rollbackAiRelease)*
- **run evaluation**: Suite, candidate, baseline, kind (offline golden set, backtest, shadow comparison). *(source: contracts/satellite/ai.yaml#runAiEvaluation)*

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

**Training and backtest runs** (data table, from `listAiTrainingRuns`): **Per tenant, own data only** (AIP-149). A run that passes its shadow gate raises `promotionReady`; the admin promotes it here with `promoteAiRelease`. Nothing switches by itself (AI-D16).

| Shows | Format | Notes |
|---|---|---|
| Capability key | text | — |
| Training window from | 1 Oct 2026 | — |
| Training window to | 1 Oct 2026 | — |
| Includes imported history | yes / no (icon or chip) | — |
| Status | chip: Queued, Training, Backtesting, Shadow, Gate passed, Gate failed… | — |
| Metrics | grouped details | — |
| Release | the name it points at, never the id | — |

**Evaluation runs** (data table, from `listAiEvaluations`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Offline, Backtest, Shadow | — |
| Candidate ref | text | — |
| Baseline ref | text | — |
| Status | chip: Queued, Running, Passed, Failed, Error | — |
| Metrics | grouped details | — |
| Gate | grouped details | The promotion gate thresholds (design 3.5 table) and whether each passed. |
| Completed at | 1 Oct 2026, 14:30 | — |

**Governance alerts** (data table, from `listAiGovernanceAlerts`): A `promotionReady` alert is what makes Promote available.

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Policy violation, Cross scope attempt, Masking defect, Data usage, Behaviour drift … | — |
| Severity | chip: Info, Low, Medium, High, Critical | — |
| Capability key | text | — |
| Status | chip: Open, Acknowledged, Dismissed, Resolved, Incident opened | — |
| Raised at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (publish gate) | navigation or local | — | — | — | — |
| Run evaluation (secondary button) | `runAiEvaluation` POST `/evaluations` | inline | AiEvaluationRun | — | opens modal first |
| Promote release (primary button) | `promoteAiRelease` POST `/releases/{releaseId}/promote` | inline | AiRelease | 403 A tenant release, and the caller does not hold the AI publish permission of its module (`module-ai-publish-required`, CHG-FUP-004); or a platform release, and …; 404 The resource does not exist, or is outside the … | opens modal first |
| Roll back release (destructive button) | `rollbackAiRelease` POST `/releases/{releaseId}/rollback` | inline | AiRelease | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Nothing to roll back to (`no-previous-release`). | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **release pipeline per capability**: Stage track draft → offline eval → background (shadow) → canary → production → monitored, with the current stage highlighted and the live producer named (rule or model version). *(source: contracts/satellite/ai.yaml#/components/schemas/AiRelease (stage))*
- **gate evidence**: Against the baseline: forecasts - WAPE at 7 days (needs 10% better), bias (within ±3%), range coverage (70-90%); fraud - recall (at least equal) and precision (20% better at the same review rate); recommendations - the controlled experiment result. Each figure with its pass/fail and the shadow period (at least 6 weeks). *(source: ADR-0051 Promotion / ADR-0051 (AI functions review 30 Sep §2))*
- **drift alerts**: Behaviour drift, input drift, bias, override-rate shift and evaluation regression alerts with severity; isolation and permission cases must pass 100% - one failure fails the run. *(source: contracts/satellite/ai.yaml#/components/schemas/AiGovernanceAlert / contracts/satellite/ai.yaml#runAiEvaluation)*
- **training runs**: Capability, window, whether imported history was included, status, metrics, release. *(source: contracts/satellite/ai.yaml#listAiTrainingRuns)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Promote**: Moves one stage and resolves the promotionReady alert; the holder of that module's "Publish AI model" permission for a tenant release (chosen on the per-module checklist; roles are preset, editable permission configurations) or PLATFORM_AI_MANAGE for a platform release; refused to service callers. *(source: contracts/satellite/ai.yaml#promoteAiRelease / ADR-0051 (AI-D16) / decided 2 October 2026 by Chinmay (CHG-NOTE-001))*
- **Roll back**: Pointer switch back; immediate; recorded. *(source: contracts/satellite/ai.yaml#rollbackAiRelease)*

**Data it reads**: `listAiEvaluations` (onLoad, Evaluation runs); `listAiGovernanceAlerts` (onLoad, Governance alerts); `listAiTrainingRuns` (onLoad, The per-tenant training and backtest runs); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The quality behavior governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the quality behavior governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No quality behavior governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the quality behavior governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Not promotable: the gate has not passed (`gate-not-passed`), an isolation case failed (`isolation-cases-failed`), the stage cannot follow the current one …; 409 Nothing to roll back to (`no-previous-release`). |

#### Edge cases to draw

- **No model ready (the normal case before a season of data)**: "No model is ready to promote. Your AI answers from <stage> and is learning your venue." with each capability's stage and what the next stage needs; not an empty table. *(source: ADR-0051 Consequences / ADR-0051 (AI functions review 30 Sep §7))*
- **Promotion attempted out of order**: 409 stage-out-of-order shown as "Promote to canary first". *(source: contracts/satellite/ai.yaml#promoteAiRelease)*

#### Consistency with other screens

- Match `ANL-071`: The venue-facing maturity page shows the same stage and the same "Ready to promote" state, without the controls.
- Match `ADM-508`: Forecast accuracy figures are the same numbers the gate reads.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
release:
  capability: forecast.attendance
  candidate: gbm-attendance v1.3 (trained on 14 months incl. imported history)
  stage: shadow
  shadowFor: 7 weeks
gate:
  WAPE7d: 12.4% vs rule 15.9% (22% better ✓)
  bias: -1.2% ✓
  coverage: 84% ✓
alert: Ready to promote - Attendance forecast (Coastal Aqua)
```

#### Permissions

- `runAiEvaluation` → `AI_CONFIGURE` (configure) · staff
- `listAiEvaluations` → `AI_USE` (operate) · staff
- `promoteAiRelease` → `AI_USE` (operate) · staff
- `rollbackAiRelease` → `AI_APPROVE` (operate) · staff
- `listAiGovernanceAlerts` → `AI_USE` (operate) · staff
- `listAiTrainingRuns` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-554` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-554`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 10: Works in AI Quality, Behavior & Governance Drift Monitoring → Detect meaningful changes in AI behavior that may increase governance risk. This is not the full model monitoring platform. Board 4 focuses specifically on governance-relevant behavioral changes.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-554?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Run evaluation, Promote release, Roll back release.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-555` AI Governance Alert & Detection Center

**Centralize governance-related alerts generated from policy, control, data, behavior and operational monitoring.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-555 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `alertId` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-governance-alert-detection-center-adm-555` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listAiGovernanceAlerts` (AI_USE), `decideAiGovernanceAlert` (AI_CONFIGURE), `openAiIncident` (AI_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** All governance alerts in one place - policy, control, data, behaviour, spend, provider breaker, evaluation regression, forecast not published, index lag and Ready to promote - with acknowledge, dismiss, resolve or open an incident. The one thing to get right: Ready to promote is an alert like the others but its action is "Review", leading to the promotion screen; it is never auto-resolved by switching.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Policy violation · Cross scope attempt · Masking defect · Data usage · Behaviour drift · Input drift · Bias · Override rate shift · Control failed · Spend · Provider breaker · Evaluation regression … | `listAiGovernanceAlerts` ?kind |
| Status | radio group | — | Open · Acknowledged · Dismissed · Resolved · Incident opened | `listAiGovernanceAlerts` ?status |
| Severity | radio group | — | Info · Low · Medium · High · Critical | `listAiGovernanceAlerts` ?severity |
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

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **alerts**: Kind, severity, capability, raised at, status; one situation → one alert. *(source: contracts/satellite/ai.yaml#listAiGovernanceAlerts / contracts/satellite/ai.yaml#/components/schemas/AiGovernanceAlert)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Open incident**: Opens ADM-556 pre-filled from the selected alerts. *(source: contracts/satellite/ai.yaml#openAiIncident)*

**Data it reads**: `listAiGovernanceAlerts` (onLoad, Governance alerts); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance alert detection list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance alert detection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance alert detection yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance alert detection are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The alert is already closed (`alert-not-open`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
alerts:
- kind: promotionReady
  capability: forecast.attendance
  severity: info
- kind: spend
  capability: assistant.guest
  severity: medium
  detail: 80% of monthly budget
```

#### Permissions

- `listAiGovernanceAlerts` → `AI_USE` (operate) · staff
- `decideAiGovernanceAlert` → `AI_CONFIGURE` (configure) · staff
- `openAiIncident` → `AI_CONFIGURE` (configure) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-555` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-555`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 12: Works in AI Governance Alert & Detection Center → Centralize governance-related alerts generated from policy, control, data, behavior and operational monitoring.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-555?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Cancel.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-556` AI Incident & Remediation Management

**Manage significant AI governance failures from detection through containment, investigation, remediation and closure.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 1 · needs the `core` module |
| Block | Block A · ticket #28978 (APP-SETUP-ADM-556) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (3 operate, 1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `capabilityKey` (navigation), `incidentId` (navigation), `releaseId` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-incident-remediation-management-adm-556` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `pauseAiCapability` (AI_CONFIGURE), `rollbackAiRelease` (AI_APPROVE), `listAiIncidents` (AI_USE), `openAiIncident` (AI_CONFIGURE), `containAiIncident` (AI_APPROVE), `closeAiIncident` (AI_APPROVE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Revalidate thresholds Fraud Team 15 Sep Pending, Run control test Governance 15 Sep Pending. Each needs an … Contract gap recorded 2 October 2026 (CHG-WIR-014): closeAiIncident lacks impact, control failure and lessons learned.

**From the AI & Intelligence process.** AI incidents from detection to closure: open an incident from governance alerts or by hand, contain it (pause a capability, roll back a release, revoke an exception, disable a tool), investigate, remediate and close with a root cause. The one thing to get right: containment actions are the real operations, recorded on the incident - the screen must show what was done, by whom, and what the AI is doing meanwhile.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- In Block A only containAiIncident is in the slice; openAiIncident, listAiIncidents and closeAiIncident are not. (CHG-SBO-006)
- The post-incident fields (impact, control failure, lessons learned) are selectFields bound to nothing, and closeAiIncident takes only rootCause and remediation. (CHG-WIR-014)

**Fixed on main** (the package already carries these; draw what it says): Buttons labelled "Revalidate thresholds Fraud Team 15 Sep Pending" and "Run control test Governance 15 Sep Pending". (CHG-SBO-007).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Open · Contained · Investigating · Remediating · Closed | `listAiIncidents` ?status |
| Severity | radio group | — | Low · Medium · High · Critical | `listAiIncidents` ?severity |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Open incident** (modal, opened by *Open incident*; *Open incident* calls `openAiIncident`, *Cancel* sends nothing)

**Collects what `openAiIncident` sends before it is called.** Required: `title`, `severity`. Optional: `kind`, `capabilityKeys`, `alertIds`, `operationalIncidentRef`, `ownerPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text field | required | — | — | — | — | `openAiIncident` body |
| Kind `kind` | segmented control | optional | Governance | Governance · Operational · Both | — | — | `openAiIncident` body |
| Severity `severity` | radio group | required | — | Low · Medium · High · Critical | — | — | `openAiIncident` body |
| Capability keys `capabilityKeys` | list of values (chips) | optional | — | — | — | — | `openAiIncident` body |
| Alerts `alertIds` | multi-picker: choose alerts | optional | — | — | — | — | `openAiIncident` body |
| Operational incident ref `operationalIncidentRef` | text field | optional | — | — | — | — | `openAiIncident` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `openAiIncident` body |

**Form: Contain incident** (modal, opened by *Contain incident*; *Contain incident* calls `containAiIncident`, *Cancel* sends nothing)

**Collects what `containAiIncident` sends before it is called.** Required: `actions`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Actions `actions` | repeatable rows | required | — | at least 1 | — | — | `containAiIncident` body |
| Action `actions[].action` | radio group | required | — | Pause capability · Rollback release · Revoke exception · Disable tool | — | — | `containAiIncident` body |
| Target ref `actions[].targetRef` | text field | required | — | — | — | — | `containAiIncident` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `containAiIncident` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The incident is closed (`incident-closed`).

**Form: Close incident** (modal, opened by *Close incident*; *Close incident* calls `closeAiIncident`, *Cancel* sends nothing)

**Collects what `closeAiIncident` sends before it is called.** Required: `rootCause`, `remediation`. Optional: `impact`, `controlFailure`, `lessonsLearned`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Root cause `rootCause` | text area | required | — | max length 4000 | — | — | `closeAiIncident` body |
| Remediation `remediation` | text area | required | — | max length 4000 | — | — | `closeAiIncident` body |
| Impact `impact` | text area | optional | — | max length 4000 | — | Who and what was affected (contract gap CHG-WIR-014, ADM-556; CHG-CSA-045). | `closeAiIncident` body |
| Control failure `controlFailure` | text area | optional | — | max length 4000 | — | Which control failed or was missing. | `closeAiIncident` body |
| Lessons learned `lessonsLearned` | text area | optional | — | max length 4000 | — | — | `closeAiIncident` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already closed (`incident-closed`), or never contained (`incident-not-contained`).

**Form: Pause capability** (modal, opened by *Pause capability*; *Pause capability* calls `pauseAiCapability`, *Cancel* sends nothing)

**Collects what `pauseAiCapability` sends before it is called.** Required: `reason`. Optional: `incidentId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `pauseAiCapability` body |
| Incident `incidentId` | picker: choose an incident | optional | — | — | shows names, sends the id | — | `pauseAiCapability` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already paused.

**Form: Roll back release** (modal, opened by *Roll back release*; *Roll back release* calls `rollbackAiRelease`, *Cancel* sends nothing)

**Collects what `rollbackAiRelease` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `rollbackAiRelease` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Nothing to roll back to (`no-previous-release`).

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **open (title, kind, severity, capabilities, alerts, owner)**: From selected alerts the fields pre-fill; kind governance, operational or both (with the operational incident reference). *(source: contracts/satellite/ai.yaml#openAiIncident)*
- **containment actions**: Checklist of pause capability / roll back release / revoke exception / disable tool, each naming its target; a note. *(source: contracts/satellite/ai.yaml#containAiIncident)*
- **close (rootCause, remediation)**: Both required. *(source: contracts/satellite/ai.yaml#closeAiIncident)*
- **post-incident review (impact, customers/transactions affected, control failure, corrective and preventive actions …**: Free text and lists on the incident; corrective actions as rows with owner team, due date and status. *(source: screens/P09-platform-admin-console.yaml#ADM-556 (board fields))*

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

**AI incidents** (data table, from `listAiIncidents`)

| Shows | Format | Notes |
|---|---|---|
| Reference | text | — |
| Title | text | — |
| Kind | chip: Governance, Operational, Both | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Status | chip: Open, Contained, Investigating, Remediating, Closed | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Contained at | 1 Oct 2026, 14:30 | — |

**Investigation and remediation** (detail panel, from `listAiIncidents`): The board's "Revalidate thresholds - Fraud Team - 15 Sep - Pending" rows are corrective actions (action, owner, due, status) recorded in `remediation` and `containment`, not buttons.

| Shows | Format | Notes |
|---|---|---|
| Containment | list or chips (count when long) | — |
| Root cause | text | — |
| Impact | text | The post-incident review's impact (`closeAiIncident`, CHG-CSA-045). |
| Control failure | text | — |
| Remediation | text | — |
| Lessons learned | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Open incident (primary button) | `openAiIncident` POST `/incidents` | inline | AiIncident | — | opens modal first |
| Contain incident (secondary button) | `containAiIncident` POST `/incidents/{incidentId}/contain` | inline | AiIncident | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The incident is closed (`incident-closed`). | opens modal first |
| Close incident (secondary button) | `closeAiIncident` POST `/incidents/{incidentId}/close` | inline | AiIncident | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already closed (`incident-closed`), or never contained (`incident-not-contained`). | opens modal first |
| Pause capability (destructive button) | `pauseAiCapability` POST `/governance/capabilities/{capabilityKey}/pause` | inline | AiCapabilityRegistration | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already paused. | opens modal first |
| Roll back release (destructive button) | `rollbackAiRelease` POST `/releases/{releaseId}/rollback` | inline | AiRelease | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Nothing to roll back to (`no-previous-release`). | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **incident timeline**: Opened → contained → investigating → remediating → closed, each step with person and time; containment actions listed with their effect. *(source: contracts/satellite/ai.yaml#/components/schemas/AiIncident (status, containment))*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Contain**: Performs each action (same as its own operation) and records it; AI_APPROVE. *(source: contracts/satellite/ai.yaml#containAiIncident)*
- **Close**: Needs root cause and remediation; 409 if containment is still open. *(source: contracts/satellite/ai.yaml#closeAiIncident)*

**Data it reads**: `listAiIncidents` (onLoad, AI incidents); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The incident remediation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the incident remediation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **No AI incident**, which is the good outcome. Offers Open incident (`openAiIncident`); distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Already closed (`incident-closed`), or never contained (`incident-not-contained`).; 409 Already paused.; 409 Nothing to roll back to (`no-previous-release`). |

#### Edge cases to draw

- **The incident touches guests (e.g. wrong prices offered at checkout)**: Kind both, linked to the operational incident; the guest-facing capability's degradation mode is stated after containment. *(source: contracts/satellite/ai.yaml#openAiIncident)*

#### Consistency with other screens

- Match `ADM-536`: Pausing from here and from the override centre is the same action with the same confirmation.
- Match `ADM-555`: Alerts selected there open an incident here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
incident:
  ref: AI-INC-0007
  title: Fraud holds on 112 legitimate wallet top-ups
  kind: both
  severity: high
  capability: risk.transaction
  status: contained
containment:
- Rolled back risk rule set v8 → v7 (Priya Nair, 1 Oct 15:10)
correctiveActions:
- action: Revalidate thresholds
  owner: Fraud team
  due: 15 Oct
  status: Pending
- action: Run control test
  owner: Governance
  due: 15 Oct
  status: Pending
```

#### Permissions

- `pauseAiCapability` → `AI_CONFIGURE` (configure) · staff
- `rollbackAiRelease` → `AI_APPROVE` (operate) · staff
- `listAiIncidents` → `AI_USE` (operate) · staff
- `openAiIncident` → `AI_CONFIGURE` (configure) · staff
- `containAiIncident` → `AI_APPROVE` (operate) · staff
- `closeAiIncident` → `AI_APPROVE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-556` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-556`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 14: Works in AI Incident & Remediation Management → Manage significant AI governance failures from detection through containment, investigation, remediation and closure.

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (19 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-556?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Open incident, Contain incident, Close incident, Pause capability, Roll back release.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-557` AI Compliance, Assurance & Governance Reporting

**Provide structured governance evidence and management reporting without duplicating TICVAI's generic BI platform.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-557 |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 read, 2 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/platform/ai-compliance-assurance-governance-reporting-adm-557` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `exportAiEvidencePackage` (AI_AUDIT_VIEW), `listAiRiskRegister` (AI_USE), `listAiControls` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack names 9 actions on this screen and the screen declares 0 operations.** Unserved: AI Capability Inventory, AI Risk Register, AI Policy Compliance, AI Approval Compliance, AI Data Usage, AI … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Governance reporting and assurance: standard reports - capability inventory, risk register, policy and approval compliance, data usage, exceptions, control effectiveness, model and provider governance - exported as evidence packages. The one thing to get right: reports are generated from the governance records, not the BI layer, and each carries its period and generation time.

**Known correction pending (do not draw the wrong version)**

- **Report types drawn as buttons.** Why: A report list. *(source: screens/P09-platform-admin-console.yaml#ADM-557; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | select | — | Customer · Commercial · Financial · Operational · Security · Model quality · Privacy · Compliance | `listAiRiskRegister` ?category |
| Status | radio group | — | Open · Mitigating · Accepted · Closed | `listAiRiskRegister` ?status |
| Effectiveness | radio group | — | Effective · Partially effective · Ineffective · Untested | `listAiControls` ?effectiveness |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_AUDIT_VIEW`, `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

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
| AI Capability Inventory (primary button) | navigation or local | — | — | — | — |
| AI Risk Register (secondary button) | navigation or local | — | — | — | — |
| AI Policy Compliance (secondary button) | navigation or local | — | — | — | — |
| AI Approval Compliance (secondary button) | navigation or local | — | — | — | — |
| AI Data Usage (secondary button) | navigation or local | — | — | — | — |
| AI Exceptions (secondary button) | navigation or local | — | — | — | — |
| Control Effectiveness (secondary button) | navigation or local | — | — | — | — |
| Model / Provider Governance (secondary button) | navigation or local | — | — | — | — |
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **report list**: Report, period, last generated, export (PDF/CSV/JSON). *(source: contracts/satellite/ai.yaml#exportAiEvidencePackage)*

**Data it reads**: `listAiRiskRegister` (onLoad, The AI risk register); `listAiControls` (onLoad, Governance controls); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The compliance assurance governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the compliance assurance governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No compliance assurance governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the compliance assurance governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_AUDIT_VIEW`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
report:
  name: AI policy compliance - Q4 2026
  generated: 1 Jan 2027 06:00
```

#### Permissions

- `exportAiEvidencePackage` → `AI_AUDIT_VIEW` (read) · staff
- `listAiRiskRegister` → `AI_USE` (operate) · staff
- `listAiControls` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-557` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-557`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 16: Works in AI Compliance, Assurance & Governance Reporting → Provide structured governance evidence and management reporting without duplicating TICVAI's generic BI platform.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-557?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: AI Capability Inventory, AI Risk Register, AI Policy Compliance, AI Approval Compliance, AI Data Usage, AI Exceptions, Control Effectiveness, Model / Provider Governance, Open access grant.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-558` AI Governance Review, Action Plan & Continuous Improvement

**Bring all governance monitoring together into a structured periodic review and improvement cycle. This is the final screen of the entire AI Governance module.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-558 |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Another option) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/platform/ai-governance-review-action-plan-continuous-improvement-adm-558` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listAiGovernanceAlerts` (AI_USE), `listAiRiskRegister` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Critical Continuous Monitoring Architecture. Each needs an operation, or needs removing from the screen … Contract gap recorded 2 October 2026 (CHG-WIR-014): No governance review record.

**From the AI & Intelligence process.** Periodic governance review: alerts, incidents, risk register changes and control results brought together into a review with an action plan (owner, due, status) and decisions such as pausing a specific model. The one thing to get right: actions taken from the review are the real operations (pause, rollback), recorded against the review.

**Known correction pending (do not draw the wrong version)**

- **No operation stores a review or its action plan; "Pause Specific Model" is a select.** Why: Either add a governance review record or drop the form; pausing is pauseAiCapability / rollbackAiRelease. *(source: contracts/satellite/ai.yaml#pauseAiCapability; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Pause Specific Model | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Policy violation · Cross scope attempt · Masking defect · Data usage · Behaviour drift · Input drift · Bias · Override rate shift · Control failed · Spend · Provider breaker · Evaluation regression … | `listAiGovernanceAlerts` ?kind |
| Status | radio group | — | Open · Acknowledged · Dismissed · Resolved · Incident opened | `listAiGovernanceAlerts` ?status |
| Severity | radio group | — | Info · Low · Medium · High · Critical | `listAiGovernanceAlerts` ?severity |
| Category | select | — | Customer · Commercial · Financial · Operational · Security · Model quality · Privacy · Compliance | `listAiRiskRegister` ?category |
| Status | radio group | — | Open · Mitigating · Accepted · Closed | `listAiRiskRegister` ?status |
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
| Critical Continuous Monitoring Architecture (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **review**: Period summary, findings, action plan rows; actions link to pause/rollback. *(source: contracts/satellite/ai.yaml#listAiGovernanceAlerts / contracts/satellite/ai.yaml#listAiRiskRegister)*

**Data it reads**: `listAiGovernanceAlerts` (onLoad, Governance alerts); `listAiRiskRegister` (onLoad, The AI risk register); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance review action configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance review action untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance review action configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
action:
  action: Re-baseline refund anomaly thresholds
  owner: Fraud team
  due: 15 Oct
  status: open
```

#### Permissions

- `listAiGovernanceAlerts` → `AI_USE` (operate) · staff
- `listAiRiskRegister` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-558` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-558`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 18: Works in AI Governance Review, Action Plan & Continuous Improvement → Bring all governance monitoring together into a structured periodic review and improvement cycle. This is the final screen of the entire AI Governance module.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-558?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Critical Continuous Monitoring ….
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"closeAiIncident": {"method":"POST","path":"/incidents/{incidentId}/close","contract":"ai","summary":"Close an incident","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiIncident"},
"containAiIncident": {"method":"POST","path":"/incidents/{incidentId}/contain","contract":"ai","summary":"Contain an incident","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiIncident"},
"decideAiGovernanceAlert": {"method":"POST","path":"/governance-alerts/{alertId}/decide","contract":"ai","summary":"Acknowledge, dismiss, resolve, or open an incident","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiGovernanceAlert"},
"exportAiEvidencePackage": {"method":"POST","path":"/evidence-packages","contract":"ai","summary":"Export an evidence package","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getAiUsage": {"method":"GET","path":"/usage","contract":"ai","summary":"Usage, cost and performance","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"AiUsageReport"},
"listAiCapabilityHealth": {"method":"GET","path":"/governance/capability-health","contract":"ai","summary":"How each AI capability is running now","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"breakerState","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiControls": {"method":"GET","path":"/controls","contract":"ai","summary":"Governance controls","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"effectiveness","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiEvaluations": {"method":"GET","path":"/evaluations","contract":"ai","summary":"Evaluation runs","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"releaseId","in":"query","required":null},{"name":"capabilityKey","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiGovernanceAlerts": {"method":"GET","path":"/governance-alerts","contract":"ai","summary":"Governance alerts","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiIncidents": {"method":"GET","path":"/incidents","contract":"ai","summary":"AI incidents","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiRiskRegister": {"method":"GET","path":"/risk-register","contract":"ai","summary":"The AI risk register","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"category","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiTrainingRuns": {"method":"GET","path":"/training-runs","contract":"ai","summary":"The per-tenant training and backtest runs","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"capabilityKey","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOwnPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants/mine","contract":"identity","summary":"The calling platform operator's own grants into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTenants": {"method":"GET","path":"/tenants","contract":"subscription","summary":"List tenants","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"planId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"openAiIncident": {"method":"POST","path":"/incidents","contract":"ai","summary":"Open an AI incident","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiIncident"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"pauseAiCapability": {"method":"POST","path":"/governance/capabilities/{capabilityKey}/pause","contract":"ai","summary":"Stop a capability now","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiCapabilityRegistration"},
"promoteAiRelease": {"method":"POST","path":"/releases/{releaseId}/promote","contract":"ai","summary":"Promote a release to its next stage (a person)","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRelease"},
"rollbackAiRelease": {"method":"POST","path":"/releases/{releaseId}/rollback","contract":"ai","summary":"Roll a release back","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRelease"},
"runAiControlTest": {"method":"POST","path":"/controls/{controlKey}/tests","contract":"ai","summary":"Test a control now","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiControlTest"},
"runAiEvaluation": {"method":"POST","path":"/evaluations","contract":"ai","summary":"Evaluate a candidate","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setAiRiskRegisterEntry": {"method":"PUT","path":"/risk-register/{entryId}","contract":"ai","summary":"Record or update a risk register entry","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiRiskRegisterEntry","responds":"AiRiskRegisterEntry"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAutonomyLevel": {"type":"integer","minimum":0,"maximum":4,"description":"**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."},
"AiCapabilityFamily": {"type":"string","enum":["gatewayAndModels","governance","actionPipeline","knowledgeRetrieval","assistants","analyticsInsights","configurationAssistant","forecasting","anomalyDetection","riskIntelligence","recommendations","decisionRecords","operationsEvaluation","residencyPrivacy"],"description":"The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point, action pipeline and human oversight, knowledge and retrieval, assistants, analytics assistant and insights, configuration assistant, forecasting and operational requirements, anomaly detection, fraud and risk intelligence, recommendation and upsell engine, decision records and audit, operations/evaluation/cost, residency/privacy/tenancy. **Every registered capability belongs to exactly one**, which is what `AiPolicy.enabledCapabilities` and the usage report group by."},
"AiCapabilityHealth": {"type":"object","x-ticvai-persistence":"none — computed from gateway telemetry, ai.activity and the breaker state in cache","description":"How one capability is running over the last hour (21 September minutes, M21-13).","required":["capabilityKey"],"properties":{"capabilityKey":{"type":"string"},"availability":{"type":"number","minimum":0,"maximum":1},"p95LatencyMs":{"type":"integer"},"latencyBudgetMs":{"type":"integer","nullable":true},"errorRate":{"type":"number","minimum":0,"maximum":1},"breakerState":{"type":"string","enum":["closed","halfOpen","open"]},"degraded":{"type":"boolean","description":"Answering from its degradation mode (rules only, search only, a person)."},"dataFreshness":{"type":"string","nullable":true,"description":"e.g. index lag, the last forecast published."},"requests":{"type":"integer"},"measuredAt":{"type":"string","format":"date-time"}}},
"AiCapabilityRegistration": {"type":"object","x-ticvai-persistence":"ai.capability","description":"**An entry in the capability registry** (design 3.1 Registry, AIC-144, AIC-145; ADM-520). Nothing becomes an operational AI capability without a row here: owner, function, risk class, autonomy, data categories and lifecycle per environment. `autonomyCeiling` is the platform ceiling for the tenant; a tenant or venue may lower `autonomyLevel`, never raise it (AIC-151).","required":["capabilityKey","family","riskClass","autonomyLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string","description":"Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`."},"family":{"$ref":"#/components/schemas/AiCapabilityFamily"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal","description":"The accountable business owner (AIC-144)."},"businessFunction":{"type":"string","nullable":true},"riskClass":{"$ref":"#/components/schemas/AiRiskClass"},"autonomyCeiling":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"readOnly":true,"description":"The first-release ceiling for this capability (design 3.8 table). Read-only to a tenant."},"autonomyLevel":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"description":"The level in force at this scope. At most `autonomyCeiling`."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories the capability reads (ADM-524)."},"lifecycle":{"type":"object","description":"Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.","properties":{"development":{"type":"string","enum":["draft","pilot","active","retired"]},"staging":{"type":"string","enum":["draft","pilot","active","retired"]},"production":{"type":"string","enum":["draft","pilot","active","retired"]}}},"degradationMode":{"type":"string","enum":["rulesOnly","searchOnly","humanHandoff","hidden","failOpen","lastPublished"],"description":"What the capability does when its model or the service is unavailable (design 3.7, AIC-241)."},"status":{"type":"string","enum":["active","paused"],"readOnly":true,"description":"Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed."},"pausedReason":{"type":"string","nullable":true,"readOnly":true},"pausedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiControl": {"type":"object","x-ticvai-persistence":"ai.control","description":"**A governance control** (AIC-219, ADM-551). Deterministic controls run nightly as SQL over system records (design 4.4): every applied tier-2 action has an approver other than the requester; no L3+ action executed without approval; no card field in any prompt.","required":["controlKey","name","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"controlKey":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"kind":{"type":"string","enum":["deterministic","manual"]},"checkRef":{"type":"string","nullable":true,"description":"The registered check a deterministic control runs. Not free SQL from a request."},"frequency":{"type":"string","enum":["nightly","weekly","monthly","onDemand"]},"capabilityKeys":{"type":"array","items":{"type":"string"}},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal"},"effectiveness":{"type":"string","enum":["effective","partiallyEffective","ineffective","untested"],"readOnly":true},"lastTestedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiControlTest": {"type":"object","x-ticvai-persistence":"ai.control_test","description":"One run of a control and what it found. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["controlId","result"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"controlId":{"type":"string","format":"uuid","x-ticvai-references":"ai.control"},"result":{"type":"string","enum":["pass","fail","error"]},"exceptionsFound":{"type":"integer","minimum":0},"evidence":{"type":"object","additionalProperties":true,"nullable":true},"runByPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal","description":"Null where the nightly job ran it."},"runAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiEvaluationRun": {"type":"object","x-ticvai-persistence":"ai.eval_run","description":"One evaluation of a candidate against its baseline: offline golden set, backtest or shadow comparison. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["suiteId","kind","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"suiteId":{"type":"string","format":"uuid","x-ticvai-references":"ai.eval_suite"},"releaseId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.release"},"kind":{"type":"string","enum":["offline","backtest","shadow"]},"candidateRef":{"type":"string"},"baselineRef":{"type":"string","nullable":true},"status":{"type":"string","enum":["queued","running","passed","failed","error"],"readOnly":true},"metrics":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true},"gate":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"The promotion gate thresholds (design 3.5 table) and whether each passed."},"isolationCasesPassed":{"type":"boolean","readOnly":true,"description":"False blocks release, whatever the other metrics say."},"requestedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"startedAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiGovernanceAlert": {"type":"object","x-ticvai-persistence":"ai.governance_alert","description":"**A governance alert** (design 4.4, AIC-210..223; ADM-549..555). Kept separate from operational incidents and linked where both apply (AIC-250). **`promotionReady`** (design 3.12, decided 29 September): a shadow model passed its promotion gate; the alert names the release and waits for a person to call `promoteAiRelease`. Monitoring never switches a model (AIC-252).","required":["kind","severity","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["policyViolation","crossScopeAttempt","maskingDefect","dataUsage","behaviourDrift","inputDrift","bias","overrideRateShift","controlFailed","spend","providerBreaker","evaluationRegression","forecastNotPublished","indexLag","promotionReady"]},"severity":{"type":"string","enum":["info","low","medium","high","critical"]},"capabilityKey":{"type":"string","nullable":true},"releaseId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.release","description":"For `promotionReady` and `evaluationRegression`: the release concerned."},"subjectRef":{"type":"string","nullable":true},"evidence":{"type":"object","additionalProperties":true,"nullable":true},"status":{"type":"string","enum":["open","acknowledged","dismissed","resolved","incidentOpened"],"readOnly":true},"incidentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.incident"},"raisedAt":{"type":"string","format":"date-time","readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"note":{"type":"string","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiIncident": {"type":"object","x-ticvai-persistence":"ai.incident","description":"**An AI governance incident** (ADM-556): detection, containment, investigation, remediation and closure.","required":["reference","title","severity","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"reference":{"type":"string","readOnly":true},"title":{"type":"string"},"kind":{"type":"string","enum":["governance","operational","both"]},"severity":{"type":"string","enum":["low","medium","high","critical"]},"status":{"type":"string","enum":["open","contained","investigating","remediating","closed"],"readOnly":true},"capabilityKeys":{"type":"array","items":{"type":"string"}},"alertIds":{"type":"array","items":{"type":"string","format":"uuid"}},"operationalIncidentRef":{"type":"string","nullable":true,"description":"The linked operational incident, where both apply (AIC-250)."},"containment":{"type":"array","items":{"type":"object","properties":{"action":{"type":"string"},"targetRef":{"type":"string"},"at":{"type":"string","format":"date-time"},"byPrincipalId":{"type":"string","format":"uuid"}}},"readOnly":true},"rootCause":{"type":"string","nullable":true},"remediation":{"type":"string","nullable":true},"impact":{"type":"string","nullable":true,"description":"The post-incident review's impact (`closeAiIncident`, CHG-CSA-045)."},"controlFailure":{"type":"string","nullable":true},"lessonsLearned":{"type":"string","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal"},"openedAt":{"type":"string","format":"date-time","readOnly":true},"containedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"closedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRelease": {"type":"object","x-ticvai-persistence":"ai.release","description":"**The release pointer per capability and tenant** (design 3.5): draft, offline evaluation, shadow, canary, production, monitored. Rollback is a pointer switch. **A model goes live only when a person promotes it** (design 3.12, decided 29 September).","required":["capabilityKey","artefactKind","candidateRef","layer","stage"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string"},"artefactKind":{"type":"string","enum":["model","prompt","routing","embedding","retrieval","rule"]},"candidateRef":{"type":"string"},"currentRef":{"type":"string","nullable":true,"description":"What production runs now: the rule, or the previously promoted artefact."},"previousRef":{"type":"string","nullable":true,"readOnly":true},"layer":{"type":"string","enum":["platform","tenant"]},"module":{"allOf":[{"$ref":"#/components/schemas/common::ModuleKey"}],"nullable":true,"description":"**Whose AI this release is, and so who promotes it** (Chinmay, 2 October, workbook Q7: \"AI release promotion goes to whoever holds it\"; CHG-FUP-004). For a tenant release, `promoteAiRelease` requires the permission `contracts/shared/permissions.yaml` `x-ticvai-module-ai-publish` names for this module; a tenant release with no module cannot be promoted (`409 module-required`). Set when the release is registered, from the capability's module. Null on a platform release, which `PLATFORM_AI_MANAGE` promotes."},"suggestionKind":{"allOf":[{"$ref":"#/components/schemas/SuggestionKind"}],"nullable":true,"description":"Where the capability answers a `requestSuggestion` kind: promotion rewrites that kind's assignment in `AiPolicy.suggestionProviders`."},"stage":{"type":"string","enum":["draft","offlineEval","shadow","canary","production","monitored","rolledBack","rejected"],"readOnly":true},"shadowStartedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"gatePassedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the shadow run passed its gate and `promotionReady` was raised."},"canaryScope":{"type":"object","additionalProperties":true,"nullable":true,"description":"Venues or share of traffic in canary."},"promotedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"promotedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"rolledBackByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"rolledBackAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRiskClass": {"type":"string","enum":["low","medium","high","critical"],"description":"Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). The governance decision point scores against it."},
"AiRiskRegisterEntry": {"type":"object","x-ticvai-persistence":"ai.risk_register","description":"**The AI risk register** (ADM-550): ongoing risks of AI capabilities with likelihood, impact, controls and residual rating. Board 1 classifies capabilities; this manages the risks over time.","required":["title","category","likelihood","impact"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"title":{"type":"string"},"category":{"type":"string","enum":["customer","commercial","financial","operational","security","modelQuality","privacy","compliance"]},"capabilityKeys":{"type":"array","items":{"type":"string"}},"likelihood":{"type":"integer","minimum":1,"maximum":5},"impact":{"type":"integer","minimum":1,"maximum":5},"inherentRating":{"type":"string","enum":["low","medium","high","critical"],"readOnly":true},"controlKeys":{"type":"array","items":{"type":"string"}},"residualRating":{"type":"string","enum":["low","medium","high","critical"]},"treatment":{"type":"string","enum":["accept","mitigate","transfer","avoid"]},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal"},"status":{"type":"string","enum":["open","mitigating","accepted","closed"]},"reviewDueAt":{"type":"string","format":"date-time","nullable":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiTrainingRun": {"type":"object","x-ticvai-persistence":"ai.training_run","description":"**One per-tenant training run** (29 September, AI functions review; design 3.5): trained on the tenant's own data only, backtested, then run in shadow. When its shadow period passes the gate, the release moves to `gatePassedAt` and a `promotionReady` alert goes to the admin (AI-D16).","required":["capabilityKey","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string"},"suggestionKind":{"allOf":[{"$ref":"#/components/schemas/SuggestionKind"}],"nullable":true},"forecastDefinitionKey":{"type":"string","nullable":true},"trainingWindowFrom":{"type":"string","format":"date"},"trainingWindowTo":{"type":"string","format":"date"},"dataCutoffAt":{"type":"string","format":"date-time"},"includesImportedHistory":{"type":"boolean","default":false},"featureSetVersion":{"type":"string"},"artefactRef":{"type":"string","nullable":true,"description":"The model file in the tenant's Blob container."},"backtestRunId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.eval_run"},"releaseId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.release"},"status":{"type":"string","enum":["queued","training","backtesting","shadow","gatePassed","gateFailed","failed"]},"metrics":{"type":"object","additionalProperties":true,"nullable":true},"startedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiUsageReport": {"type":"object","x-ticvai-persistence":"none — aggregated from ai.activity","properties":{"currency":{"type":"string","minLength":3,"maxLength":3,"readOnly":true,"description":"**The tenant's selected currency, by default its billing currency (AED for a UAE tenant), not USD** (CHG-RUL-017; Chinmay, 2 October, workbook Q8; CHG-CSA-004). Every `cost` here is in it; token counts sit beside each cost."},"ceiling":{"type":"object","nullable":true,"readOnly":true,"description":"The spend ceiling in force (`getAiSpendCeiling`), with the tokens it equals at the current blended rate and what is used so far (CHG-CSA-004).","properties":{"spend":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tokens":{"type":"integer","nullable":true},"usedSpend":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"usedTokens":{"type":"integer"}}},"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"groupBy":{"type":"string"},"rows":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"interactions":{"type":"integer"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"p95LatencyMs":{"type":"integer"},"refusalRate":{"type":"number"},"rejectionRate":{"type":"number","description":"Proposals a person refused. **The number that says whether the assistant is worth having**, and the one nobody thinks to measure.\n"}}}},"forecast":{"type":"object","nullable":true,"description":"**A month-end projection, labelled a forecast** (AI design 2.3, 4.5). Present where `to` is inside the current month. Never added into `rows`.\n","properties":{"label":{"type":"string","enum":["forecast"]},"periodEnd":{"type":"string","format":"date"},"projectedTokens":{"type":"integer"},"projectedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"basis":{"type":"string","description":"How it was projected, e.g. the run rate of the last 7 days."}}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE","CORE_AI_PUBLISH","TICKETING_AI_PUBLISH","ACCESS_AI_PUBLISH","FNB_AI_PUBLISH","RETAIL_AI_PUBLISH","INVENTORY_AI_PUBLISH","SEATING_AI_PUBLISH","MEMBERSHIP_AI_PUBLISH","MARKETING_AI_PUBLISH","RESOURCES_AI_PUBLISH","QUEUE_AI_PUBLISH","TRANSPORT_AI_PUBLISH","GAMES_AI_PUBLISH","MAINTENANCE_AI_PUBLISH","ACCREDITATION_AI_PUBLISH","PARTNER_AI_PUBLISH","ANALYTICS_AI_PUBLISH","BIOMETRIC_IMAGE_VIEW","ACCESS_DIRECTION_SET","REPORT_GOVERNANCE_MANAGE"]},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]},
"SuspensionMode": {"type":"string","description":"Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n","enum":["readOnly","noNewSales","fullLockout"]},
"Tenant": {"x-ticvai-persistence":"control.tenant","type":"object","required":["id","code","name","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"$ref":"#/components/schemas/TenantStatus"},"suspensionMode":{"$ref":"#/components/schemas/SuspensionMode"},"suspensionReason":{"type":"string","nullable":true},"suspensionEffectiveAt":{"type":"string","format":"date-time","nullable":true,"description":"When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."},"suspensionNoticeMessage":{"$ref":"#/components/schemas/subscription::LocalisedText","description":"The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."},"terminationScheduledAt":{"type":"string","format":"date-time","nullable":true,"description":"When `terminateTenant` started the retention window. Null when no termination is under way."},"terminationRetentionUntil":{"type":"string","format":"date-time","nullable":true,"description":"`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."},"terminationReason":{"type":"string","maxLength":1000,"nullable":true},"terminationRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"planId":{"type":"string","format":"uuid","nullable":true},"planName":{"type":"string","nullable":true},"cellCount":{"type":"integer"},"venueCount":{"type":"integer"},"regionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500,"nullable":true,"description":"Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."},"accountManagerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantStatus": {"type":"string","enum":["onboarding","active","suspended","terminating","terminated"]}
}
```
