# WS118 — AI Configuration Assistant board 3

**10 screens · 23 operations · 29 schemas · 6 permissions**

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
| `ADM-489` | AI Configuration Readiness Center | D | 20 | 14 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-490` | Configuration Validation Results | D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-491` | AI Recommendations & Best-Practice Review | D | 6 | 20 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-492` | Configuration Approval Workflow | D | 6 | 6 | 7 | 2 | 0 | 3 | — | notStarted (—) |
| `ADM-493` | AI Configuration Execution Center | D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-494` | Execution Progress & Dependency Monitor | D | 6 | 48 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-495` | Configuration Results & Object Mapping | D | 6 | 22 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-496` | Configuration Change & Modification Assistant | D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-497` | Configuration History, Versions & Rollback | D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-498` | AI Configuration Audit & Governance | D | 8 | 16 | 7 | 5 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-492 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-489` AI Configuration Readiness Center

**Provide a final readiness assessment before the proposed Configuration Plan can enter approval or execution. This is the first governance gate.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-489 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `planId` (navigation), `venueId` (session), `tenantId` (navigation) |
| Route | `/platform/ai-configuration-readiness-center-adm-489` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getEffectiveAiPolicy` (AI_USE), `getActionPlan` (AI_USE), `getAiVenueSettings` (AI_USE), `setAiVenueSettings` (AI_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**From the AI & Intelligence process.** The first governance gate: is the plan ready to enter approval or execution - objects ready, warnings, blocking issues, approvals needed, modules affected, production impact - plus the venue AI profile captured during setup. The one thing to get right: a blocking issue disables "Send for approval", and the effective governance policy for the configuration assistant (autonomy L3, approval required) is stated.

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

**Form: Save venue AI profile** (modal, opened by *Save venue AI profile*; *Save venue AI profile* calls `setAiVenueSettings`, *Cancel* sends nothing)

**Collects what `setAiVenueSettings` sends before it is called.** Required: `venueId`, `venueType`. Every other figure is optional and defaults to the starting pattern for the venue type, so a venue that knows only its type still gets answers.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setAiVenueSettings` body |
| Venue type `venueType` | select | required | — | Water park · Theme park · Family entertainment centre · Museum · Arena · Zoo aquarium · Other | — | — | `setAiVenueSettings` body |
| Is outdoor `isOutdoor` | toggle | optional | on | — | — | Outdoor venues take the summer-heat and weather effects. | `setAiVenueSettings` body |
| Capacity `capacity` | number field | optional | — | min 1 | — | — | `setAiVenueSettings` body |
| Opening hours `openingHours` | repeatable rows | optional | — | — | — | The usual week. Exceptions come from the venue calendar. | `setAiVenueSettings` body |
| Day of week `openingHours[].dayOfWeek` | stepper or slider | optional | — | min 1; max 7 | — | — | `setAiVenueSettings` body |
| Opens at `openingHours[].opensAt` | text field | optional | — | — | — | — | `setAiVenueSettings` body |
| Closes at `openingHours[].closesAt` | text field | optional | — | — | — | — | `setAiVenueSettings` body |
| Typical weekday attendance `typicalWeekdayAttendance` | number field | optional | — | min 0 | — | — | `setAiVenueSettings` body |
| Typical weekend attendance `typicalWeekendAttendance` | number field | optional | — | min 0 | — | — | `setAiVenueSettings` body |
| Peak months `peakMonths` | list of values (chips) | optional | — | — | — | — | `setAiVenueSettings` body |
| Average spend `averageSpend` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setAiVenueSettings` body |
| Fnb attach rate `fnbAttachRate` | stepper or slider (%) | optional | — | min 0; max 1 | — | — | `setAiVenueSettings` body |
| Staff productivity `staffProductivity` | key and value settings | optional | — | — | — | Per role, units per staff hour, e.g. `{"cashier": 40, "gate": 300}`. | `setAiVenueSettings` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

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

**Configuration Objects** (metric tile)

**Ready** (metric tile)

**Warnings** (metric tile)

**Blocking Issues** (metric tile)

**Approval Requirements** (metric tile)

**AI Recommendations** (metric tile)

**Modules Affected** (metric tile)

**Production Impact** (metric tile)

**Venue AI profile** (detail panel, from `getAiVenueSettings`): **What every AI answer stands on before the venue has history** (29 September, AI functions review). Collected at onboarding, here or by the configuration assistant in conversation.

| Shows | Format | Notes |
|---|---|---|
| Venue type | chip: Water park, Theme park, Family entertainment centre, Museum, Arena, Zoo aquarium… | — |
| Capacity | 1,234 | — |
| Opening hours | list or chips (count when long) | The usual week. Exceptions come from the venue calendar. |
| Typical weekday attendance | 1,234 | — |
| Typical weekend attendance | 1,234 | — |
| Peak months | list or chips (count when long) | — |
| Average spend | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Fnb attach rate | 12.5% | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Save venue AI profile (primary button) | `setAiVenueSettings` PUT `/venues/{venueId}/ai-settings` | AiVenueSettings | AiVenueSettings | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **readiness**: Tiles with counts; blocking issues list first. *(source: contracts/satellite/ai.yaml#getActionPlan)*
- **governance line**: "Configuration assistant: L3 Execute with approval. This plan needs approval from: Commercial manager (pricing), Venue manager." *(source: contracts/satellite/ai.yaml#getEffectiveAiPolicy / ADR-0050)*
- **venue AI profile**: The baseline figures with pattern defaults greyed; saving here is the same as on ANL-071. *(source: contracts/satellite/ai.yaml#setAiVenueSettings / ADR-0051)*

**Data it reads**: `getEffectiveAiPolicy` (onLoad, The policy in force for a capability at a scope); `getActionPlan` (onLoad, A plan with its steps); `getAiVenueSettings` (onLoad, The venue AI profile the baselines use); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-490` Configuration Validation Results: *Configuration Validation Results*; carries `planId`
- → `ADM-491` AI Recommendations & Best-Practice Review: *AI Recommendations & Best-Practice Review*; carries `tenantId`
- → `ADM-492` Configuration Approval Workflow: *Configuration Approval Workflow*; carries `planId`
- → `ADM-493` AI Configuration Execution Center: *AI Configuration Execution Center*; carries `planId`
- → `ADM-494` Execution Progress & Dependency Monitor: *Execution Progress & Dependency Monitor*; carries `planId`, `stepNumber`
- → `ADM-495` Configuration Results & Object Mapping: *Configuration Results & Object Mapping*; carries `planId`
- → `ADM-496` Configuration Change & Modification Assistant: *Configuration Change & Modification Assistant*; carries `tenantId`
- → `ADM-497` Configuration History, Versions & Rollback: *Configuration History, Versions & Rollback*; carries `planId`
- → `ADM-498` AI Configuration Audit & Governance: *AI Configuration Audit & Governance*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The readiness list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the readiness untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No readiness yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the readiness are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `ANL-071`: Same venue AI profile form.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  objects: 46
  ready: 44
  warnings: 2
  blocking: 0
  approvals: 2
  modules: 6
```

#### Permissions

- `getEffectiveAiPolicy` → `AI_USE` (operate) · staff
- `getActionPlan` → `AI_USE` (operate) · staff
- `getAiVenueSettings` → `AI_USE` (operate) · staff
- `setAiVenueSettings` → `AI_CONFIGURE` (configure) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-489` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-489`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 1: Opens AI Configuration Readiness Center → Provide a final readiness assessment before the proposed Configuration Plan can enter approval or execution. This is the first governance gate.
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F227 branch at step 1 (expected): when Nothing has been set up on AI Configuration Readiness Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F227 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-489?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Save venue AI profile.
- [ ] Every transition is wired: `ADM-002`, `ADM-490`, `ADM-491`, `ADM-492`, `ADM-493`, `ADM-494`, `ADM-495`, `ADM-496`, `ADM-497`, `ADM-498`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-490` Configuration Validation Results

**Provide detailed evidence that the proposed configuration has passed all required TICVAI validation layers. Screen 1 provides the summary; Screen 2 provides the technical and business evidence.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-490 |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `planId` (navigation), `tenantId` (navigation) |
| Route | `/platform/configuration-validation-results-adm-490` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getActionPlan` (AI_USE), `simulateActionPlan` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Validation evidence: for each validation layer (schema, module rules, dependencies, governance, simulation) what was checked and the result, per object. The one thing to get right: it is evidence for an approver - each pass is as visible as each failure, with the rule named.

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

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **evidence table**: Layer, object, rule, result, detail; filter to failures. *(source: contracts/satellite/ai.yaml#simulateActionPlan / contracts/satellite/ai.yaml#getActionPlan)*

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The validation results list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the validation results untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No validation results yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the validation results are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The plan is executing or finished; simulate a rollback plan instead. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- layer: Governance
  object: Price Day Pass Sat
  rule: Price change approval tier 1
  result: Approval required
```

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-490` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-490`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 2: Works in Configuration Validation Results → Provide detailed evidence that the proposed configuration has passed all required TICVAI validation layers. Screen 1 provides the summary; Screen 2 provides the technical and business evidence.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-490?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Cancel.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-491` AI Recommendations & Best-Practice Review

**Separate mandatory configuration from AI recommendations so the administrator understands what is required and what is advice.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-491 |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | `decisionKey` (navigation), `sessionId` (session), `tenantId` (navigation) |
| Route | `/platform/ai-recommendations-best-practice-review-adm-491` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getConfigurationBlueprint` (AI_USE), `decideBlueprintRecommendation` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the AI & Intelligence process.** AI recommendations and best practice kept apart from mandatory configuration, so the administrator knows what is required and what is the assistant's advice - with each recommendation's decision recorded (accepted, modified, rejected by whom and why). The one thing to get right: rejecting a recommendation is a normal outcome, recorded with a reason, never nagged again in the same session.

**Fixed on main** (the package already carries these; draw what it says): Columns are a board row ("Family Package", "Rejected", "Administrator"). (CHG-WIR-013).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `getConfigurationBlueprint` ?module |
| Decision class | segmented control | — | Required · Recommended · Optional | `getConfigurationBlueprint` ?decisionClass |
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

**Every recommendations best-practice review** (data table)

| Shows | Format | Notes |
|---|---|---|
| Recommendation | text | not in the schema: `Recommendation` |
| Family package | text | not in the schema: `Family Package` |
| Decision | text | not in the schema: `Decision` |
| Rejected | text | not in the schema: `Rejected` |
| By | text | not in the schema: `By` |
| Administrator | text | not in the schema: `Administrator` |
| Reason | text | not in the schema: `Reason` |

**The selected recommendations best-practice review** (detail panel): The pack groups this record's detail under its own headings: “Where available”.

| Shows | Format | Notes |
|---|---|---|
| Recommendation | text | not in the schema: `Recommendation` |
| Family package | text | not in the schema: `Family Package` |
| Decision | text | not in the schema: `Decision` |
| Rejected | text | not in the schema: `Rejected` |
| By | text | not in the schema: `By` |
| Administrator | text | not in the schema: `Administrator` |
| Reason | text | not in the schema: `Reason` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **recommendation list**: Recommendation, why, decision, by, reason; mandatory items in a separate section. *(source: contracts/satellite/ai.yaml#/components/schemas/AiBlueprintDecision (recommendation, decisionClass))*

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`, `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendations best-practice review list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendations best-practice review untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendations best-practice review yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendations best-practice review are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The session is no longer open for decisions (`session-not-open`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  recommendation: Add a Family Package
  decision: Rejected
  by: Administrator (Omar Haddad)
  reason: Family pricing handled by promotions
```

#### Permissions

- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
- `decideBlueprintRecommendation` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-491` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-491`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 4: Works in AI Recommendations & Best-Practice Review → Separate mandatory configuration from AI recommendations so the administrator understands what This is important for trust and governance.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-491?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-492` Configuration Approval Workflow

**Route the proposed AI configuration through TICVAI's existing RBAC/PBAC and approval governance before execution. The AI Assistant should reuse the central TICVAI approval engine, not create an independent approval system.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-492 |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `actionId` (navigation), `planId` (navigation), `tenantId` (navigation) |
| Route | `/platform/configuration-approval-workflow-adm-492` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getActionPlan` (AI_USE), `listProposedActions` (AI_USE), `decideProposedAction` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-012): The "Approve workflow" button was bound to catalogue approveWorkflow, which designs approval workflows; approving this plan is decideProposedAction (declared) …

**From the AI & Intelligence process.** Approval of the configuration plan through TICVAI's central approval engine and RBAC - not a separate AI approval system. Approvers see each proposed action with current vs proposed, impact and risk, and approve or reject with a reason. The one thing to get right: an AI-prepared change goes to approval even when the requester could make it by hand (autonomy is separate from permission), and proposals expire.

**Known correction pending (do not draw the wrong version)**

- **No AI-generated summary for the approver.** Why: The approval engine requirement asks for an AI-generated summary on approval screens. *(source: TRACKER Actions row 76; AI & Intelligence)*

**Fixed on main** (the package already carries these; draw what it says): "Approve workflow" button bound to catalogue approveWorkflow (PRODUCT_CONFIGURE), which designs approval workflows. (CHG-WIR-012).

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

- **proposals**: Summary, target module and operation, current → proposed, risk, approval tier, status, expires at (proposed: 7 days; approved but not applied: 24 hours). *(source: contracts/satellite/ai.yaml#listProposedActions / contracts/satellite/ai.yaml#/components/schemas/ProposedAction / ADR-0050)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Approve / Reject**: Reject needs a reason; the requester cannot approve their own plan. *(source: contracts/satellite/ai.yaml#decideProposedAction)*

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `listProposedActions` (onLoad, What the assistant has proposed and nobody has decided); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval workflow list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval workflow yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval workflow are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
proposal:
  summary: Create 12 products, 48 prices, 3 bundles for Coastal Aqua
  tier: 2
  approvers:
  - Commercial manager
  - Venue GM
  expires: Thu 8 Oct
```

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `listProposedActions` → `AI_USE` (operate) · staff
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

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-492` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-492`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 6: Works in Configuration Approval Workflow → Route the proposed AI configuration through TICVAI's existing RBAC/PBAC and approval governance before execution. The AI Assistant should reuse the central TICVAI approval engine, not create an …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-492?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-493` AI Configuration Execution Center

**Execute the approved Configuration Plan against the appropriate TICVAI modules in a controlled and traceable sequence. This is where proposed configuration becomes real TICVAI configuration.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-493 |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (3 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `planId` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-configuration-execution-center-adm-493` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getActionPlan` (AI_USE), `pauseActionPlan` (AI_APPROVE), `cancelActionPlan` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Execution of the approved plan against the owning modules in dependency order, traceably. The one thing to get right: a person can pause at any step boundary (nothing half-applies) or cancel; on a partial failure the plan rolls back rather than leaving a product half-configured.

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

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (primary button) | navigation or local | — | — | — | — |
| Cancel action plan (destructive button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **steps**: Ordered steps with tool, target, status; executing step animated; each step's idempotency means a retry never duplicates. *(source: contracts/satellite/ai.yaml#getActionPlan / MoM 21 Sep 4.9)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Pause**: Executor stops at the next step boundary; recorded as an intervention (AI_APPROVE). *(source: contracts/satellite/ai.yaml#pauseActionPlan)*
- **Cancel action plan**: Destructive confirmation naming what has already been applied and what will not run; reason required. *(source: contracts/satellite/ai.yaml#cancelActionPlan)*

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The execution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the execution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No execution yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the execution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_APPROVE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The plan is already finished.; 409 The plan is not executing. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
plan:
  status: executing
  steps:
  - Venue ✓
  - Operating calendar ✓
  - Products ✓
  - Timeslots ✓
  - Capacity …
  - Pricing ○
  - Channels ○
```

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `pauseActionPlan` → `AI_APPROVE` (operate) · staff
- `cancelActionPlan` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-493` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-493`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 8: Works in AI Configuration Execution Center → Execute the approved Configuration Plan against the appropriate TICVAI modules in a controlled and traceable sequence. This is where proposed configuration becomes real TICVAI configuration.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-493?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Cancel action plan, Cancel.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-494` Execution Progress & Dependency Monitor

**Provide a detailed real-time view of execution dependencies, failures, retries, and downstream configuration status.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-494 |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (3 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `planId` (navigation), `stepNumber` (navigation), `tenantId` (navigation) |
| Route | `/platform/execution-progress-dependency-monitor-adm-494` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getActionPlan` (AI_USE), `pauseActionPlan` (AI_APPROVE), `resumeActionPlan` (AI_APPROVE), `retryActionStep` (AI_APPROVE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the AI & Intelligence process.** Live execution and dependency monitor: each step's status (waiting, executing, success, failed), what it waits on, retries and downstream status. The one thing to get right: a failed step shows the owning module's error and the choices - retry the step, pause, or roll back - with what each does.

**Known correction pending (do not draw the wrong version)**

- **Statuses and step names are table columns ("Venue ✓", "Capacity ●", "Waiting").** Why: Steps are rows; status is a column. *(source: screens/P09-platform-admin-console.yaml#ADM-494; AI & Intelligence)*

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

**Every execution progress dependency** (data table)

| Shows | Format | Notes |
|---|---|---|
| Venue ✓ | text | not in the schema: `Venue ✓` |
| ↓ | text | not in the schema: `↓` |
| Operating calendar ✓ | text | not in the schema: `Operating Calendar ✓` |
| Products ✓ | text | not in the schema: `Products ✓` |
| Timeslots ✓ | text | not in the schema: `Timeslots ✓` |
| Capacity ● | text | not in the schema: `Capacity ●` |
| Pricing ○ | text | not in the schema: `Pricing ○` |
| Channels ○ | text | not in the schema: `Channels ○` |
| Media ○ | text | not in the schema: `Media ○` |
| Access ○ | text | not in the schema: `Access ○` |
| Status | text | not in the schema: `Status` |
| Waiting | text | not in the schema: `Waiting` |
| Executing | text | not in the schema: `Executing` |
| Success | text | not in the schema: `Success` |
| Warning | text | not in the schema: `Warning` |
| Failed | text | not in the schema: `Failed` |
| Skipped | text | not in the schema: `Skipped` |
| Rolled back | text | not in the schema: `Rolled Back` |
| Failure example | text | not in the schema: `Failure Example` |
| 🔴 pricing profile creation failed | text | not in the schema: `🔴 Pricing Profile Creation Failed` |
| Weekend adult pricing | text | not in the schema: `Weekend Adult Pricing` |

**The selected execution progress dependency** (detail panel): The pack groups this record's detail under its own headings: “Blocked”, “Retry History”, “Resolution Applied”.

| Shows | Format | Notes |
|---|---|---|
| Venue ✓ | text | not in the schema: `Venue ✓` |
| ↓ | text | not in the schema: `↓` |
| Operating calendar ✓ | text | not in the schema: `Operating Calendar ✓` |
| Products ✓ | text | not in the schema: `Products ✓` |
| Timeslots ✓ | text | not in the schema: `Timeslots ✓` |
| Capacity ● | text | not in the schema: `Capacity ●` |
| Pricing ○ | text | not in the schema: `Pricing ○` |
| Channels ○ | text | not in the schema: `Channels ○` |
| Media ○ | text | not in the schema: `Media ○` |
| Access ○ | text | not in the schema: `Access ○` |
| Status | text | not in the schema: `Status` |
| Waiting | text | not in the schema: `Waiting` |
| Executing | text | not in the schema: `Executing` |
| Success | text | not in the schema: `Success` |
| Warning | text | not in the schema: `Warning` |
| Failed | text | not in the schema: `Failed` |
| Skipped | text | not in the schema: `Skipped` |
| Rolled back | text | not in the schema: `Rolled Back` |
| Failure example | text | not in the schema: `Failure Example` |
| 🔴 pricing profile creation failed | text | not in the schema: `🔴 Pricing Profile Creation Failed` |
| Weekend adult pricing | text | not in the schema: `Weekend Adult Pricing` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **dependency chain**: Steps as a chain with status icons and the blocking dependency highlighted. *(source: contracts/satellite/ai.yaml#getActionPlan)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Retry step / Resume**: Retries the failed step (idempotent); resume revalidates before continuing. *(source: contracts/satellite/ai.yaml#retryActionStep / contracts/satellite/ai.yaml#resumeActionPlan)*

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The execution progress dependency list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the execution progress dependency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No execution progress dependency yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the execution progress dependency are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_APPROVE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Not resumable: the plan is not paused (`plan-not-paused`), or a target object changed since planning (`plan-drifted`).; 409 Not retryable: the step has not failed (`step-not-failed`) or has used its 3 attempts (`retry-limit-reached`).; 409 The plan is not executing. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
failed:
  step: Pricing
  error: 'Catalogue: channel price list ''Resellers'' does not exist'
  attempts: 1
```

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `pauseActionPlan` → `AI_APPROVE` (operate) · staff
- `resumeActionPlan` → `AI_APPROVE` (operate) · staff
- `retryActionStep` → `AI_APPROVE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-494` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-494`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 10: Works in Execution Progress & Dependency Monitor → Provide a detailed real-time view of execution dependencies, failures, retries, and downstream configuration status.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (48 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-494?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-495` Configuration Results & Object Mapping

**Show exactly what TICVAI objects were created or changed after successful execution.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-495 |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (3 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `planId` (navigation), `tenantId` (navigation) |
| Route | `/platform/configuration-results-object-mapping-adm-495` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getActionPlan` (AI_USE), `rollbackActionPlan` (AI_APPROVE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the AI & Intelligence process.** What was actually created or changed: each TICVAI object with its id, module, before and after, linked to the plan step that made it. The one thing to get right: object ids link into the owning screens, and rollback is offered as a planned rollback (with forward-fix preferred where reversing is unsafe).

**Known correction pending (do not draw the wrong version)**

- **Object ids are table columns.** Why: Rows. *(source: screens/P09-platform-admin-console.yaml#ADM-495; AI & Intelligence)*

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

**Every results object mapping** (data table)

| Shows | Format | Notes |
|---|---|---|
| VEN 1028 | text | not in the schema: `VEN-1028` |
| ↓ | text | not in the schema: `↓` |
| TKT 4012 | text | not in the schema: `TKT-4012` |
| SCH 0291 | text | not in the schema: `SCH-0291` |
| CAP 0218 | text | not in the schema: `CAP-0218` |
| PRC 3002 | text | not in the schema: `PRC-3002` |
| MED 0082 | text | not in the schema: `MED-0082` |
| ACC 0142 | text | not in the schema: `ACC-0142` |

**The selected results object mapping** (detail panel): The pack groups this record's detail under its own headings: “Object Mapping”, “Created does not necessarily mean”, “Pending”.

| Shows | Format | Notes |
|---|---|---|
| VEN 1028 | text | not in the schema: `VEN-1028` |
| ↓ | text | not in the schema: `↓` |
| TKT 4012 | text | not in the schema: `TKT-4012` |
| SCH 0291 | text | not in the schema: `SCH-0291` |
| CAP 0218 | text | not in the schema: `CAP-0218` |
| PRC 3002 | text | not in the schema: `PRC-3002` |
| MED 0082 | text | not in the schema: `MED-0082` |
| ACC 0142 | text | not in the schema: `ACC-0142` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **object mapping**: Plan step → object id (e.g. VEN-1028, TKT-4012, SCH-0291, PRC-3002) → module → change; each id a link. *(source: contracts/satellite/ai.yaml#getActionPlan)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Plan a rollback**: Creates a rollback plan (origin rollback) that goes through approval like any plan; reason required; prefer forward fix option. *(source: contracts/satellite/ai.yaml#rollbackActionPlan)*

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The results object mapping list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the results object mapping untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No results object mapping yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the results object mapping are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_APPROVE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Nothing to roll back: the plan has no completed step (`plan-not-applied`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
objects:
- VEN-1028
- TKT-4012
- SCH-0291
- CAP-0218
- PRC-3002
- MED-0082
- ACC-0142
```

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
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

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-495` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-495`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 12: Works in Configuration Results & Object Mapping → Show exactly what TICVAI objects were created or changed after successful execution.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-495?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-496` Configuration Change & Modification Assistant

**Allow administrators to return later and modify existing TICVAI configuration through natural-language AI. This is what transforms the feature from an onboarding wizard into a permanent AI configuration capability.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-496 |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `sessionId` (session), `tenantId` (navigation) |
| Route | `/platform/configuration-change-modification-assistant-adm-496` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `startConfigurationSession` (AI_USE), `answerConfigurationQuestion` (AI_USE), `buildConfigurationPlan` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Prepare Change / Ask More / Cancel. Each needs an operation, or needs removing from the screen; this is the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Change existing configuration in natural language ("raise weekend adult prices by AED 10 from November", "add a sunset session on Fridays"): the assistant asks what it needs, prepares the change as a plan, and it goes through the same validation and approval. The one thing to get right: it shows the before/after and the affected bookings before "Prepare change"; purchased tickets never change retroactively.

**Known correction pending (do not draw the wrong version)**

- **"Prepare Change / Ask More / Cancel" as one button.** Why: Three actions. *(source: screens/P09-platform-admin-console.yaml#ADM-496; AI & Intelligence)*

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
| Prepare Change / Ask More / Cancel (primary button) | navigation or local | — | — | — | — |
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Prepare change**: Builds a plan from the session (intent modify) and opens validation. *(source: contracts/satellite/ai.yaml#buildConfigurationPlan / contracts/satellite/ai.yaml#startConfigurationSession)*

**Data it reads**: `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The change modification assistant list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the change modification assistant untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No change modification assistant yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the change modification assistant are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The blueprint is not ready: a required decision is open or deferred (AIC-115).; 409 The session is no longer discovering (`session-not-open`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
request: Raise weekend adult Day Pass by AED 10 from 1 Nov
preview: 'Day Pass Adult Sat/Sun: AED 140 → AED 150 from 1 Nov; 1,204 existing bookings unaffected'
```

#### Permissions

- `startConfigurationSession` → `AI_USE` (operate) · staff
- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `buildConfigurationPlan` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-496` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-496`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 14: Works in Configuration Change & Modification Assistant → Allow administrators to return later and modify existing TICVAI configuration through natural-language AI. This is what transforms the feature from an onboarding wizard into a permanent AI …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-496?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Prepare Change / Ask More / Cancel, Open access grant, Cancel.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-497` Configuration History, Versions & Rollback

**Maintain complete version history for AI-created and AI-modified configuration and provide governed rollback capability where technically possible.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-497 |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (3 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `planId` (navigation), `tenantId` (navigation) |
| Route | `/platform/configuration-history-versions-rollback-adm-497` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getActionPlan` (AI_USE), `rollbackActionPlan` (AI_APPROVE), `listConfigurationSessions` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** History of AI-created and AI-modified configuration: sessions, plans and their versions, with governed rollback where technically possible. The one thing to get right: each entry shows who asked, what the AI proposed, who approved and when it was published - the client's example is every price change.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Discovering · Blueprint ready · Planned · Executing · Completed · Abandoned | `listConfigurationSessions` ?status |
| Intent | radio group | — | Create · Modify · Extend · Clone | `listConfigurationSessions` ?intent |
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

**Detail panel** (detail panel): One record, read-only.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **history**: Session → plan → executed changes, newest first; who suggested, who approved, when published. *(source: DI-938 / contracts/satellite/ai.yaml#listConfigurationSessions / contracts/satellite/ai.yaml#getActionPlan)*

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `listConfigurationSessions` (onLoad, Configuration-assistant sessions); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The history versions rollback list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the history versions rollback untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No history versions rollback yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the history versions rollback are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_APPROVE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Nothing to roll back: the plan has no completed step (`plan-not-applied`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entry:
  change: Day Pass Adult weekend AED 140 → 150
  suggested: Configuration assistant (requested by Omar Haddad)
  approved: Priya Nair, 2 Oct 11:05
  published: 2 Oct 11:20
```

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `rollbackActionPlan` → `AI_APPROVE` (operate) · staff
- `listConfigurationSessions` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-497` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-497`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 16: Works in Configuration History, Versions & Rollback → Maintain complete version history for AI-created and AI-modified configuration and provide governed rollback capability where technically possible.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-497?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Cancel.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-498` AI Configuration Audit & Governance

**Provide an immutable governance record showing how AI participated in every configuration decision and execution. This is essential for an enterprise AI system.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-498 |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Header KPIs; Show) and a per-row directory (§For each configuration value show) — counts over a population, then the population |
| Offline | online only |
| Opens with | `decisionRecordId` (navigation), `tenantId` (navigation) |
| Route | `/platform/ai-configuration-audit-governance-adm-498` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `searchAiDecisions` (AI_AUDIT_VIEW), `getAiDecisionTrace` (AI_AUDIT_VIEW) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the AI & Intelligence process.** The immutable audit of AI's part in configuration: from user request to AI interpretation, blueprint decision, object, validation, approval and execution, each with actor, time and trace id, searchable by venue, user, session, plan, object and module. The one thing to get right: every value's source is visible - user provided, AI recommended, system derived, existing configuration.

**Known correction pending (do not draw the wrong version)**

- **The trace chain's step names are drawn as metric tiles ("User Request", "↓", "AI Interpretation", "Timestamp", "Actor").** Why: They are the stages of one record's trace, drawn as a chain. *(source: screens/P09-platform-admin-console.yaml#ADM-498; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Search audit governance | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, user, date, session, configuration plan and 13 more — which are present is a decision the pack already made. | — |

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

**AI Configuration Sessions** (metric tile)

**AI Recommendations** (metric tile)

**Accepted** (metric tile)

**Rejected** (metric tile)

**Executed Changes** (metric tile)

**Rollbacks** (metric tile)

**Approval Overrides** (metric tile)

**Failed Executions** (metric tile)

**User Request** (metric tile)

**↓** (metric tile)

**AI Interpretation** (metric tile)

**Blueprint Decision** (metric tile)

**Configuration Object** (metric tile)

**Validation** (metric tile)

**Approval** (metric tile)

**Execution** (metric tile)

**Audit Requirements** (metric tile)

**Original User Intent** (metric tile)

**AI Recommendation** (metric tile)

**User Decision** (metric tile)

**Configuration Plan** (metric tile)

**Before / After** (metric tile)

**Validation Results** (metric tile)

**Failure / Retry** (metric tile)

**Rollback** (metric tile)

**Timestamp** (metric tile)

**Actor** (metric tile)

**Correlation / Trace ID** (metric tile)

**Every audit governance** (data table)

| Shows | Format | Notes |
|---|---|---|
| Source | text | not in the schema: `Source` |
| 👤 user provided | text | not in the schema: `👤 User Provided` |
| 🤖 AI recommended | text | not in the schema: `🤖 AI Recommended` |
| ⚙ system derived | text | not in the schema: `⚙ System Derived` |
| 📋 existing configuration | text | not in the schema: `📋 Existing Configuration` |

**The selected audit governance** (detail panel): The pack groups this record's detail under its own headings: “Objects”, “Timeslots 24 System Derived Operations”, “Critical Execution Architecture”, “The architecture should be”, “Owning TICVAI Modules”, “Execution Dependency Engine”.

| Shows | Format | Notes |
|---|---|---|
| Source | text | not in the schema: `Source` |
| 👤 user provided | text | not in the schema: `👤 User Provided` |
| 🤖 AI recommended | text | not in the schema: `🤖 AI Recommended` |
| ⚙ system derived | text | not in the schema: `⚙ System Derived` |
| 📋 existing configuration | text | not in the schema: `📋 Existing Configuration` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **decision chain**: Request → interpretation → decision → object → validation → approval → execution as a vertical chain with timestamps and actors; before/after; failure/retry; rollback. *(source: contracts/satellite/ai.yaml#getAiDecisionTrace / MoM 18 Sep 4.7)*
- **counts**: Sessions, recommendations, accepted, rejected, executed, rollbacks, approval overrides, failed executions for the period. *(source: contracts/satellite/ai.yaml#searchAiDecisions)*

**Data it reads**: `searchAiDecisions` (onLoad, Find AI decisions); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audit governance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audit governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audit governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the audit governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_AUDIT_VIEW`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
record:
  request: Create a water park setup
  interpretation: Create venue Coastal Aqua, 12 products
  approval: Priya Nair 2 Oct 11:05
  trace: tr-7f3a9c
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

- AI-prepared configuration keeps full version history, e.g. every price change shows who suggested it, who approved it and when it was published. *(client request · MoM 18 Sep 2026, 4.7 AI Configuration Assistant — Approval, Execution & Audit Trail · DI-938)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-498` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-498`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 18: Works in AI Configuration Audit & Governance → Provide an immutable governance record showing how AI participated in every configuration decision and execution. This is essential for an enterprise AI system.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-498?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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
"answerConfigurationQuestion": {"method":"POST","path":"/configuration-sessions/{sessionId}/answers","contract":"ai","summary":"Answer the current question","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiConfigurationTurn"},
"buildConfigurationPlan": {"method":"POST","path":"/configuration-sessions/{sessionId}/plan","contract":"ai","summary":"Compile the blueprint into a plan","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlanDetail"},
"cancelActionPlan": {"method":"POST","path":"/action-plans/{planId}/cancel","contract":"ai","summary":"Cancel a plan","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlan"},
"decideBlueprintRecommendation": {"method":"POST","path":"/configuration-sessions/{sessionId}/decisions/{decisionKey}","contract":"ai","summary":"Accept, modify, reject or defer a blueprint decision","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiBlueprintDecision"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"getActionPlan": {"method":"GET","path":"/action-plans/{planId}","contract":"ai","summary":"A plan with its steps","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiActionPlanDetail"},
"getAiDecisionTrace": {"method":"GET","path":"/decision-records/{decisionRecordId}/trace","contract":"ai","summary":"The full trace of a decision","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"depth","in":"query","required":null}],"requestBody":null,"responds":"AiDecisionTrace"},
"getAiVenueSettings": {"method":"GET","path":"/venues/{venueId}/ai-settings","contract":"ai","summary":"The venue AI profile the baselines stand on","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiVenueSettings"},
"getConfigurationBlueprint": {"method":"GET","path":"/configuration-sessions/{sessionId}/blueprint","contract":"ai","summary":"The blueprint so far","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"module","in":"query","required":null},{"name":"decisionClass","in":"query","required":null}],"requestBody":null,"responds":"AiBlueprintView"},
"getEffectiveAiPolicy": {"method":"GET","path":"/governance/effective-policy","contract":"ai","summary":"The policy in force for a capability at a scope","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"capabilityKey","in":"query","required":true},{"name":"scopePath","in":"query","required":null},{"name":"environment","in":"query","required":null}],"requestBody":null,"responds":"AiEffectivePolicy"},
"listConfigurationSessions": {"method":"GET","path":"/configuration-sessions","contract":"ai","summary":"Configuration-assistant sessions","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"intent","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOwnPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants/mine","contract":"identity","summary":"The calling platform operator's own grants into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProposedActions": {"method":"GET","path":"/proposed-actions","contract":"ai","summary":"What the assistant has proposed and nobody has decided","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProposedAction"},
"listTenants": {"method":"GET","path":"/tenants","contract":"subscription","summary":"List tenants","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"planId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"pauseActionPlan": {"method":"POST","path":"/action-plans/{planId}/pause","contract":"ai","summary":"Pause an executing plan","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlan"},
"resumeActionPlan": {"method":"POST","path":"/action-plans/{planId}/resume","contract":"ai","summary":"Resume a paused plan","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlan"},
"retryActionStep": {"method":"POST","path":"/action-plans/{planId}/steps/{stepNumber}/retry","contract":"ai","summary":"Retry a failed step","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionStep"},
"rollbackActionPlan": {"method":"POST","path":"/action-plans/{planId}/rollback","contract":"ai","summary":"Plan a rollback","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"searchAiDecisions": {"method":"GET","path":"/decision-records","contract":"ai","summary":"Find AI decisions","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"capabilityKey","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"traceId","in":"query","required":null},{"name":"policyVersion","in":"query","required":null},{"name":"modelVersion","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setAiVenueSettings": {"method":"PUT","path":"/venues/{venueId}/ai-settings","contract":"ai","summary":"Set the venue AI profile","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiVenueSettings","responds":"AiVenueSettings"},
"simulateActionPlan": {"method":"POST","path":"/action-plans/{planId}/simulate","contract":"ai","summary":"Validate and simulate a plan without changing anything","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlanDetail"},
"startConfigurationSession": {"method":"POST","path":"/configuration-sessions","contract":"ai","summary":"Start the configuration assistant","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiConfigurationSession"}
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
"AiBlueprintDecision": {"type":"object","x-ticvai-persistence":"ai.blueprint_decision","description":"One decision in a blueprint and what the administrator did with it. **Scoped through its blueprint** (`platform.apply_parent_rls`).","required":["blueprintId","decisionKey","decisionClass","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"blueprintId":{"type":"string","format":"uuid","x-ticvai-references":"ai.blueprint"},"decisionKey":{"type":"string"},"module":{"type":"string"},"decisionClass":{"type":"string","enum":["required","recommended","optional"]},"question":{"type":"string","nullable":true},"value":{"type":"object","additionalProperties":true,"nullable":true},"provenance":{"$ref":"#/components/schemas/AiProvenance"},"sourceId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.config_source","description":"The attached document the value was extracted from (29 September, build; `attachConfigurationSource`)."},"sourceCitation":{"type":"string","nullable":true,"maxLength":200,"description":"Where in it, e.g. `page 4`, `sheet Prices!B7`, `logo region`."},"recommendation":{"type":"object","additionalProperties":true,"nullable":true,"description":"What the assistant recommends and why (ADM-491): mandatory configuration and best practice kept apart."},"status":{"type":"string","enum":["open","accepted","modified","rejected","deferred"]},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"note":{"type":"string","nullable":true}}},
"AiBlueprintView": {"type":"object","x-ticvai-persistence":"none — ai.blueprint with its ai.blueprint_decision rows","description":"A blueprint with its decisions.","required":["blueprint","decisions"],"properties":{"blueprint":{"$ref":"#/components/schemas/AiConfigurationBlueprint"},"decisions":{"type":"array","items":{"$ref":"#/components/schemas/AiBlueprintDecision"}}}},
"AiConfigurationBlueprint": {"type":"object","x-ticvai-persistence":"ai.blueprint","description":"**The blueprint** (design 2.2 D step 2, ADM-478): decisions, severity-graded issues and a dependency map. **Never `ready` while a required decision is deferred** (AIC-115).","required":["sessionId","version","readiness"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"sessionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.config_session"},"version":{"type":"integer","minimum":1},"readiness":{"type":"string","enum":["notReady","readyWithWarnings","ready"],"readOnly":true},"requiredOpen":{"type":"integer","minimum":0,"readOnly":true,"description":"Required decisions not yet accepted or modified."},"issues":{"$ref":"#/components/schemas/AiBlueprintIssueList"},"dependencyMap":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Configuration objects and the order they depend on each other, by module."},"summary":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiConfigurationQuestion": {"type":"object","x-ticvai-persistence":"none — chosen per turn from the configuration knowledge model","description":"**The next question, chosen by the configuration knowledge model, not by the language model** (design 2.2 D, AIC-111). The model only extracts a structured answer against `answerSchema`.","required":["questionKey","text","decisionClass"],"properties":{"questionKey":{"type":"string"},"text":{"type":"string"},"module":{"type":"string","nullable":true},"decisionClass":{"type":"string","enum":["required","recommended","optional"]},"answerType":{"type":"string","enum":["freeText","singleChoice","multiChoice","number","date","confirm"]},"options":{"type":"array","items":{"type":"string"}},"why":{"type":"string","nullable":true,"description":"Why it is asked: which configuration branch it opens or closes."},"answerSchema":{"type":"object","additionalProperties":true,"nullable":true,"description":"JSON Schema the extracted answer must satisfy."}}},
"AiConfigurationSession": {"type":"object","x-ticvai-persistence":"ai.config_session","description":"**A configuration-assistant session** (design 2.2 D steps 1-2, C7; ADM-469..478). Discovery runs from the configuration knowledge model; every value carries provenance.","required":["intent","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"intent":{"type":"string","enum":["create","modify","extend","clone"]},"venueType":{"type":"string","nullable":true,"description":"Museum, theme park, water park, zoo, aquarium, theatre, stadium, festival, conference..."},"sourceScopePath":{"type":"string","nullable":true,"description":"The setup being cloned or extended."},"status":{"type":"string","enum":["discovering","blueprintReady","planned","executing","completed","abandoned"],"readOnly":true},"progressPercent":{"type":"integer","minimum":0,"maximum":100,"readOnly":true},"nextQuestion":{"allOf":[{"$ref":"#/components/schemas/AiConfigurationQuestion"}],"nullable":true,"readOnly":true},"conversationId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.conversation"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan"},"locale":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"startedAt":{"type":"string","format":"date-time","readOnly":true},"lastActivityAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiConfigurationTurn": {"type":"object","x-ticvai-persistence":"none — the answer is written to ai.blueprint_decision and the session","description":"The result of one answer: what was extracted with its provenance, the next question and progress.","required":["session"],"properties":{"session":{"$ref":"#/components/schemas/AiConfigurationSession"},"extracted":{"type":"array","items":{"type":"object","properties":{"decisionKey":{"type":"string"},"value":{"type":"object","additionalProperties":true,"nullable":true},"provenance":{"$ref":"#/components/schemas/AiProvenance"}}}},"nextQuestion":{"allOf":[{"$ref":"#/components/schemas/AiConfigurationQuestion"}],"nullable":true},"clarificationsNeeded":{"type":"array","items":{"type":"string"}}}},
"AiDecisionRecord": {"type":"object","x-ticvai-persistence":"ai.decision_record","description":"**The standard record for every governed decision** (design 3.9, C12; AIC-193..209): a recommendation summary, a risk assessment, a forecast publication, a plan step, an assistant answer at significant depth, a governance block, a Help me choose suggestion. **Append-only; corrections are annotations; hash-chained per tenant** so tampering is detectable (AIC-203, AIC-204). **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["traceId","capabilityKey","outcome","recordHash"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"traceId":{"type":"string"},"capabilityKey":{"type":"string"},"task":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true},"subjectRef":{"type":"string","nullable":true},"inputsRef":{"type":"string","nullable":true,"description":"Where the inputs are kept (Blob or `ai.activity`), never the prompt text itself."},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"producer":{"type":"string","nullable":true},"modelVersion":{"type":"string","nullable":true},"promptTemplateVersion":{"type":"string","nullable":true},"featureSetVersion":{"type":"string","nullable":true},"knowledgeVersion":{"type":"string","nullable":true},"ruleVersions":{"type":"object","additionalProperties":true,"nullable":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"nullable":true},"policyVersion":{"type":"string","nullable":true},"approvals":{"type":"object","additionalProperties":true,"nullable":true,"description":"Approval requests and their decisions."},"humanDecision":{"type":"object","additionalProperties":true,"nullable":true,"description":"Override or intervention, where a person changed the outcome."},"executionResult":{"type":"object","additionalProperties":true,"nullable":true},"outcomeRef":{"type":"string","nullable":true,"description":"The business outcome it links to (an order, a published version, a closed case)."},"outcome":{"type":"string","enum":["answered","refused","allowed","blocked","executed","failed","approvedThenFailed","published","suggested"],"description":"`approvedThenFailed` is kept distinct from `executed` (design 1.2 Audit)."},"annotations":{"type":"array","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"byPrincipalId":{"type":"string","format":"uuid"},"note":{"type":"string"}}},"readOnly":true,"description":"Corrections, appended; the original fields are never edited."},"previousHash":{"type":"string","readOnly":true},"recordHash":{"type":"string","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiDecisionTrace": {"type":"object","x-ticvai-persistence":"none — ai.decision_record with the rows it references","description":"**The full trace of one decision** (ADM-540..546): record, evidence, candidates and rules, model and runtime, governance and approvals, execution and business outcome. Depth is gated by permission (AIC-195).","required":["record"],"properties":{"record":{"$ref":"#/components/schemas/AiDecisionRecord"},"depth":{"type":"string","enum":["business","governance","technical"]},"explanation":{"type":"string","description":"Built from structured evidence, never a model's chain of thought (AIC-192)."},"activity":{"type":"array","items":{"$ref":"#/components/schemas/AiInteraction"},"description":"The model calls behind it (`technical` depth)."},"plan":{"allOf":[{"$ref":"#/components/schemas/AiActionPlanDetail"}],"nullable":true},"interventions":{"type":"array","items":{"$ref":"#/components/schemas/AiIntervention"}},"chainVerified":{"type":"boolean","description":"The hash chain around this record verifies."}}},
"AiEffectivePolicy": {"type":"object","x-ticvai-persistence":"none — resolved from published policy versions, exceptions and ai.policy","description":"**The policy in force for a capability at a scope** (AIC-153, AIC-165; ADM-525, ADM-528): the intersection of the capability, governance policy and the tenant or venue AI policy, with where each part came from.","required":["capabilityKey","autonomyLevel","rules"],"properties":{"capabilityKey":{"type":"string"},"scopePath":{"type":"string"},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"autonomyCeiling":{"$ref":"#/components/schemas/AiAutonomyLevel"},"rules":{"type":"array","items":{"type":"object","properties":{"rule":{"$ref":"#/components/schemas/AiGovernanceRule"},"policyKey":{"type":"string"},"version":{"type":"integer"},"scopePath":{"type":"string"}}}},"exceptions":{"type":"array","items":{"$ref":"#/components/schemas/AiPolicyException"}},"conflicts":{"type":"array","items":{"type":"object","properties":{"description":{"type":"string"},"resolvedTo":{"$ref":"#/components/schemas/AiGovernanceOutcome"}}},"description":"Conflicting rules and the more restrictive result they resolved to (AIC-161)."},"resolvedAt":{"type":"string","format":"date-time"}}},
"AiEvidenceItemList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The evidence of one decision record, stored with it.","items":{"$ref":"#/components/schemas/AiEvidenceItem"}},
"AiGovernanceOutcome": {"type":"string","enum":["allow","allowWithConditions","prepareOnly","approvalRequired","escalate","block"],"description":"What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). `block` is an answer, not an error, and is logged as outcome `refused`."},
"AiGovernanceRule": {"type":"object","x-ticvai-persistence":"none — held in the jsonb rules column of ai.governance_policy_version, through AiGovernanceRuleList","description":"One rule of a governance policy version: which actions on which data, under which conditions, get which outcome (AIC-147..160).","required":["effect"],"properties":{"effect":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"capabilityKeys":{"type":"array","items":{"type":"string"},"description":"Registered capabilities it applies to. Empty means every capability the policy names."},"actions":{"type":"array","items":{"type":"string","enum":["read","analyze","recommend","generate","prepare","create","modify","publish","execute","delete"]},"description":"ADM-523: what AI may do, from reading to executing."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories (ADM-524), e.g. `customerContact`, `payment`, `financial`, `operational`."},"purposes":{"type":"array","items":{"type":"string"},"description":"Permitted purposes for those categories (AIC-156, AIR-182)."},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Above this value the effect escalates one step (for example to `approvalRequired`)."},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Roles the rule applies to; empty means every role."},"environments":{"type":"array","items":{"type":"string","enum":["development","sandbox","staging","production"]},"description":"ADM-525. Empty means every environment. **`sandbox`** (18 September minutes, M18-01): the developer sandbox and a tenant's trial environment, governed apart from staging so a rule can allow in sandbox what it blocks in production."},"conditions":{"type":"object","additionalProperties":true,"nullable":true,"description":"Conditions attached to an `allowWithConditions` effect, for example `maskFields` or `requireCitation`."}}},
"AiInteraction": {"type":"object","x-ticvai-persistence":"ai.activity","required":["id","principalId","capability","outcome","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid","nullable":true},"principalId":{"type":"string","format":"uuid"},"audience":{"type":"string","enum":["staff","guest"],"description":"**Billing divides on this.** Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop guests asking questions.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest, where the audience is `guest`. `principalId` is null in that case — **a guest is not a principal**, and attributing their tokens to a staff member would be wrong twice.\n"},"billableToTenantId":{"type":"string","format":"uuid","description":"Resolved from `scopePath` at write time, not derived later. **Billing must not depend on walking a scope tree that has since been reorganised.**\n"},"scopePath":{"type":"string"},"capability":{"type":"string"},"prompt":{"type":"string"},"response":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"outcome":{"type":"string","enum":["answered","refused","applied","rejected","failed"]},"refusalReason":{"type":"string","nullable":true},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"cost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"x-ticvai-column":"cost_amount","description":"What the call cost at the provider. **Money like every other amount** (naming-and-style 5.1) — it replaces an integer `costMinor` that carried no currency or scale, which AED and OMR read differently.\n"},"latencyMs":{"type":"integer"},"maskedFieldCount":{"type":"integer","description":"How many fields were redacted. Zero on a prompt touching guest data is a defect."},"traceId":{"type":"string"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"description":"The `ai.decision_record` this call belongs to, where it was part of a governed decision (AI design 2.3, 3.9). Null for a call audited by this row alone."},"cacheLayer":{"type":"string","nullable":true,"enum":["guardrail","semantic","exact","negative","analytics"],"description":"Which cache answered, where one did (AI design 3.6). Null for a model call."},"createdAt":{"type":"string","format":"date-time"}}},
"AiIntervention": {"type":"object","x-ticvai-persistence":"ai.intervention","description":"**A person stepping in** (AIC-187, ADM-535, ADM-536): an override, pause, resume, stop, retry or rollback, with the original AI decision and the human one side by side.","required":["kind","targetKind","targetRef"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["override","pause","resume","cancel","retry","rollback","capabilityPause","capabilityResume"]},"targetKind":{"type":"string","enum":["plan","step","decision","capability"]},"targetRef":{"type":"string"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true},"originalDecision":{"type":"object","additionalProperties":true,"nullable":true},"humanDecision":{"type":"object","additionalProperties":true,"nullable":true},"reason":{"type":"string","maxLength":2000},"principalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiPolicyException": {"type":"object","x-ticvai-persistence":"ai.policy_exception","description":"**A temporary, recorded exception to a governance policy** (AIC-162, ADM-526): an expiry, an approver and compensating controls. Governance is never bypassed silently.","required":["policyId","reason","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"policyId":{"type":"string","format":"uuid","x-ticvai-references":"ai.governance_policy"},"capabilityKey":{"type":"string","nullable":true},"reason":{"type":"string","maxLength":2000},"compensatingControls":{"type":"array","items":{"type":"string"}},"startsAt":{"type":"string","format":"date-time","nullable":true},"expiresAt":{"type":"string","format":"date-time","description":"Required. An exception with no end is a policy change, and goes through publication."},"status":{"type":"string","enum":["active","expired","revoked"],"readOnly":true},"approvedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"revokedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"revokedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"revokeReason":{"type":"string","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiProvenance": {"type":"string","enum":["confirmed","aiRecommended","inferred","unknown"],"description":"**Where a configuration value came from** (design 2.2 D, AIC-111): said by the administrator, recommended by the assistant, inferred from other answers, or not known yet. Shown beside every value; no confidence number is shown for configuration (design 5.6)."},
"AiVenueSettings": {"type":"object","x-ticvai-persistence":"ai.venue_settings","description":"**The venue AI profile** (29 September, AI functions review): the figures a venue gives at onboarding so every data-driven answer is useful before it has history. One row per venue; configuration, not history. Defaults come from the starting pattern for `venueType`, which TICVAI writes from published sources and made-up example curves, **never from another tenant's data** (AI-D01, AIP-149).","required":["venueId","venueType"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"venueType":{"type":"string","enum":["waterPark","themePark","familyEntertainmentCentre","museum","arena","zooAquarium","other"]},"isOutdoor":{"type":"boolean","default":true,"description":"Outdoor venues take the summer-heat and weather effects."},"capacity":{"type":"integer","minimum":1,"nullable":true},"openingHours":{"type":"array","description":"The usual week. Exceptions come from the venue calendar.","items":{"type":"object","properties":{"dayOfWeek":{"type":"integer","minimum":1,"maximum":7},"opensAt":{"type":"string"},"closesAt":{"type":"string"}}}},"typicalWeekdayAttendance":{"type":"integer","minimum":0,"nullable":true},"typicalWeekendAttendance":{"type":"integer","minimum":0,"nullable":true},"peakMonths":{"type":"array","items":{"type":"integer","minimum":1,"maximum":12}},"averageSpend":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"fnbAttachRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"staffProductivity":{"type":"object","additionalProperties":{"type":"number"},"description":"Per role, units per staff hour, e.g. `{\"cashier\": 40, \"gate\": 300}`. Defaults from the pattern."},"startingPatternKey":{"type":"string","readOnly":true,"description":"The pattern and version in use, e.g. `waterPark@3`."},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE","CORE_AI_PUBLISH","TICKETING_AI_PUBLISH","ACCESS_AI_PUBLISH","FNB_AI_PUBLISH","RETAIL_AI_PUBLISH","INVENTORY_AI_PUBLISH","SEATING_AI_PUBLISH","MEMBERSHIP_AI_PUBLISH","MARKETING_AI_PUBLISH","RESOURCES_AI_PUBLISH","QUEUE_AI_PUBLISH","TRANSPORT_AI_PUBLISH","GAMES_AI_PUBLISH","MAINTENANCE_AI_PUBLISH","ACCREDITATION_AI_PUBLISH","PARTNER_AI_PUBLISH","ANALYTICS_AI_PUBLISH","BIOMETRIC_IMAGE_VIEW","ACCESS_DIRECTION_SET","REPORT_GOVERNANCE_MANAGE"]},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"SuspensionMode": {"type":"string","description":"Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n","enum":["readOnly","noNewSales","fullLockout"]},
"Tenant": {"x-ticvai-persistence":"control.tenant","type":"object","required":["id","code","name","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"$ref":"#/components/schemas/TenantStatus"},"suspensionMode":{"$ref":"#/components/schemas/SuspensionMode"},"suspensionReason":{"type":"string","nullable":true},"suspensionEffectiveAt":{"type":"string","format":"date-time","nullable":true,"description":"When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."},"suspensionNoticeMessage":{"$ref":"#/components/schemas/LocalisedText","description":"The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."},"terminationScheduledAt":{"type":"string","format":"date-time","nullable":true,"description":"When `terminateTenant` started the retention window. Null when no termination is under way."},"terminationRetentionUntil":{"type":"string","format":"date-time","nullable":true,"description":"`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."},"terminationReason":{"type":"string","maxLength":1000,"nullable":true},"terminationRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"planId":{"type":"string","format":"uuid","nullable":true},"planName":{"type":"string","nullable":true},"cellCount":{"type":"integer"},"venueCount":{"type":"integer"},"regionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500,"nullable":true,"description":"Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."},"accountManagerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantStatus": {"type":"string","enum":["onboarding","active","suspended","terminating","terminated"]}
}
```
