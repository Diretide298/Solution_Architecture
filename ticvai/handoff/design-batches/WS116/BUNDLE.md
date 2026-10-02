# WS116 — AI Configuration Assistant board 1

**10 screens · 12 operations · 19 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AI_CONFIGURE, AI_USE, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
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
| `ADM-469` | AI Configuration Home & Start | B–D | 6 | 36 | 7 | 3 | 1 | 0 | — | notStarted (—) |
| `ADM-470` | Setup Type & Business Intent Discovery | B–D | 21 | 6 | 7 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-471` | Venue & Business Model Discovery | B–D | 50 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-472` | Guided Question & Answer Workspace | B–D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-473` | Product & Admission Model Discovery | B–D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-474` | Operational Requirement Discovery | B–D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-475` | Commercial Requirement Discovery | B–D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-476` | Required, Recommended & Optional Decisions | B–D | 10 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-477` | Missing Information & Clarification Center | B–D | 6 | 6 | 7 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-478` | Configuration Blueprint & Dependency Map | B–D | 6 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-469` AI Configuration Home & Start

**Provide one intelligent starting point for creating or modifying TICVAI configuration through AI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show intelligent cards such as; Show) and no metric row |
| Offline | online only |
| Opens with | `sessionId` (session), `tenantId` (navigation) |
| Route | `/platform/ai-configuration-home-start-adm-469` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `startConfigurationSession` (AI_USE), `listConfigurationSessions` (AI_USE), `attachConfigurationSource` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Create New Configuration, Modify Existing Configuration, Extend Existing Configuration, Clone & Adapt … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the AI & Intelligence process.** The configuration assistant's start: create, modify, extend or clone a setup by describing it, optionally seeded from documents (a brief, brochure, price list, spreadsheet), and resume earlier sessions. It needs no history and works fully from day one; it was the client's first AI priority. The one thing to get right: the promise on the page - "Describe what you want; the assistant asks what is missing and nothing is applied until you approve it."

**Known correction pending (do not draw the wrong version)**

- **Venue types are table columns and the four intents are unbound buttons.** Why: Venue types are choices for startConfigurationSession.venueType; the intents map to intent create/modify/extend/clone. *(source: contracts/satellite/ai.yaml#startConfigurationSession / screens/P09-platform-admin-console.yaml#ADM-469; AI & Intelligence)*
- **The configuration assistant screens sit on P09 (TICVAI console) though the client wants venue admins and newly onboarded clients to use it.** Why: Either the tenant's administrators use them through the console with a grant, or BO-597/BO-598 are the tenant's entry; say which (see ADM-520). *(source: MoM 18 Sep 4.5 / screens/P08-venue-back-office.yaml#BO-597; AI & Intelligence)*

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

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **intent / venue type / description**: Four intent cards (Create new, Modify, Extend, Clone and adapt); venue type tiles (museum, theme park, water park, zoo, aquarium, theatre, stadium, indoor attraction, family entertainment centre, festival, conference, temporary event, start from scratch); a free description box. Clone and extend ask for the source setup. *(source: contracts/satellite/ai.yaml#startConfigurationSession / DI-279)*
- **documents**: Upload a brief, brochure, catalogue, price list, spreadsheet or brand asset; values extracted later cite the page or cell. *(source: contracts/satellite/ai.yaml#attachConfigurationSource / TRACKER Actions row 125)*

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

**Every home start** (data table)

| Shows | Format | Notes |
|---|---|---|
| Museum | text | not in the schema: `Museum` |
| Theme park | text | not in the schema: `Theme Park` |
| Water park | text | not in the schema: `Water Park` |
| Zoo | text | not in the schema: `Zoo` |
| Aquarium | text | not in the schema: `Aquarium` |
| Theatre | text | not in the schema: `Theatre` |
| Stadium | text | not in the schema: `Stadium` |
| Indoor attraction | text | not in the schema: `Indoor Attraction` |
| Family entertainment center | text | not in the schema: `Family Entertainment Center` |
| Festival | text | not in the schema: `Festival` |
| Conference | text | not in the schema: `Conference` |
| Temporary event | text | not in the schema: `Temporary Event` |
| Start from scratch | text | not in the schema: `Start from Scratch` |
| Session type progress last activity status | text | not in the schema: `Session Type Progress Last Activity Status` |
| Summer festival event 100% yesterday blueprint ready | text | not in the schema: `Summer Festival Event 100% Yesterday Blueprint Ready` |

**The selected home start** (detail panel): The pack groups this record's detail under its own headings: “The screen should immediately answer”, “Subtitle”, “Large conversational input”.

| Shows | Format | Notes |
|---|---|---|
| Museum | text | not in the schema: `Museum` |
| Theme park | text | not in the schema: `Theme Park` |
| Water park | text | not in the schema: `Water Park` |
| Zoo | text | not in the schema: `Zoo` |
| Aquarium | text | not in the schema: `Aquarium` |
| Theatre | text | not in the schema: `Theatre` |
| Stadium | text | not in the schema: `Stadium` |
| Indoor attraction | text | not in the schema: `Indoor Attraction` |
| Family entertainment center | text | not in the schema: `Family Entertainment Center` |
| Festival | text | not in the schema: `Festival` |
| Conference | text | not in the schema: `Conference` |
| Temporary event | text | not in the schema: `Temporary Event` |
| Start from scratch | text | not in the schema: `Start from Scratch` |
| Session type progress last activity status | text | not in the schema: `Session Type Progress Last Activity Status` |
| Summer festival event 100% yesterday blueprint ready | text | not in the schema: `Summer Festival Event 100% Yesterday Blueprint Ready` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Create New Configuration (primary button) | navigation or local | — | — | — | — |
| Modify Existing Configuration (secondary button) | navigation or local | — | — | — | — |
| Extend Existing Configuration (secondary button) | navigation or local | — | — | — | — |
| Clone & Adapt Existing Setup (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **sessions**: Earlier sessions with intent, venue type, progress %, status (discovering, blueprint ready, planned, executing, completed, abandoned), last activity; resume opens where it stopped. *(source: contracts/satellite/ai.yaml#listConfigurationSessions)*

**Data it reads**: `listConfigurationSessions` (onLoad, Configuration-assistant sessions); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-470` Setup Type & Business Intent Discovery: *Setup Type & Business Intent Discovery*; carries `tenantId`
- → `ADM-471` Venue & Business Model Discovery: *Venue & Business Model Discovery*; carries `tenantId`
- → `ADM-472` Guided Question & Answer Workspace: *Guided Question & Answer Workspace*; carries `tenantId`
- → `ADM-473` Product & Admission Model Discovery: *Product & Admission Model Discovery*; carries `tenantId`
- → `ADM-474` Operational Requirement Discovery: *Operational Requirement Discovery*; carries `tenantId`
- → `ADM-475` Commercial Requirement Discovery: *Commercial Requirement Discovery*; carries `tenantId`
- → `ADM-476` Required, Recommended & Optional Decisions: *Required, Recommended & Optional Decisions*; carries `tenantId`
- → `ADM-477` Missing Information & Clarification Center: *Missing Information & Clarification Center*; carries `tenantId`
- → `ADM-478` Configuration Blueprint & Dependency Map: *Configuration Blueprint & Dependency Map*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The home start list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the home start untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No home start yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the home start are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The session is no longer discovering (`session-not-open`), or the governance data policy refuses the document (`governance-blocked`).; 422 The asset is not a readable document or image (`unreadable-source`), for example a scan with no text layer the extractor could read. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
session:
  intent: create
  venueType: Water park
  description: New water park in Dubai, day passes and cabanas, family bundles, open 10-18, closed Mondays in summer
  progress: 35%
  status: discovering
```

#### Permissions

- `startConfigurationSession` → `AI_USE` (operate) · staff
- `listConfigurationSessions` → `AI_USE` (operate) · staff
- `attachConfigurationSource` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.31 | System shall allow administrators to upload event briefs, brochures, schedules, PDFs or spreadsheets and use AI to automatically generate event configurations, sessions, ticket types, capacities … | Ticketing Catalogue | CONTRACTED | `attachConfigurationSource` |
| 1.4.21 | System shall allow administrators to upload spreadsheets, brochures, PDFs or existing catalogues and automatically generate products, pricing structures, rules, entitlements and configurations using … | Ticketing Catalogue | CONTRACTED | `attachConfigurationSource` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Phase-one AI priority is a conversational configuration assistant: the admin says e.g. "I want to configure a new product" and it asks the product type (admission, time slot, etc.) and walks through product/promotion setup. *(agreed · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-279)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-469` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-469`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 1: Opens AI Configuration Home & Start → Provide one intelligent starting point for creating or modifying TICVAI configuration through AI.
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F225 branch at step 1 (expected): when Nothing has been set up on AI Configuration Home & Start yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F225 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-469?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Create New Configuration, Modify Existing Configuration, Extend Existing Configuration, Clone & Adapt Existing Setup.
- [ ] Every transition is wired: `ADM-002`, `ADM-470`, `ADM-471`, `ADM-472`, `ADM-473`, `ADM-474`, `ADM-475`, `ADM-476`, `ADM-477`, `ADM-478`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-470` Setup Type & Business Intent Discovery

**Understand what the administrator is actually trying to accomplish before asking detailed configuration questions. This is the first AI interview screen.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Detected Setup; Likely Configuration Areas) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `sessionId` (session), `tenantId` (navigation) |
| Route | `/platform/setup-type-business-intent-discovery-adm-470` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `startConfigurationSession` (AI_USE), `answerConfigurationQuestion` (AI_USE), `attachConfigurationSource` (AI_USE), `listConfigurationSources` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **Setup Type & Business Intent Discovery declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either …

**From the AI & Intelligence process.** The first interview step: what is the administrator actually trying to do - create a venue, add products, change prices - for which organisation and location, and which configuration areas it will touch. The assistant restates its understanding for confirmation before asking details. The one thing to get right: the understanding is shown as editable chips (action, object, venue type, organisation, location, operation type, areas), each marked as said by the user or inferred - not as a confidence percentage.

**Known correction pending (do not draw the wrong version)**

- **"Confidence: 96%" field.** Why: The assistant's understanding carries provenance (confirmed, AI recommended, inferred), not a percentage (ranges or bands, never a bare percentage). *(source: contracts/satellite/ai.yaml#/components/schemas/AiProvenance / ADR-0051; AI & Intelligence)*
- **Understanding values drawn as selectFields with the value in the label ("Action: Create").** Why: Label and value separate; values come from the extracted answers. *(source: screens/P09-platform-admin-console.yaml#ADM-470; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Action: Create | select field | — | — | — | — | — | — |
| Object: Venue | select field | — | — | — | — | — | — |
| Venue Type: Museum | select field | — | — | — | — | — | — |
| Organization: Existing | select field | — | — | — | — | — | — |
| Location: Dubai | select field | — | — | — | — | — | — |
| Operation Type: Permanent | select field | — | — | — | — | — | — |
| Confidence: 96% | select field | — | — | — | — | — | — |
| ✓ Venue | select field | — | — | — | — | — | — |
| ✓ Products | select field | — | — | — | — | — | — |
| ✓ Schedule | select field | — | — | — | — | — | — |
| ✓ Capacity | select field | — | — | — | — | — | — |
| ✓ Pricing | select field | — | — | — | — | — | — |
| ✓ Sales Channels | select field | — | — | — | — | — | — |
| ✓ Ticket Media | select field | — | — | — | — | — | — |
| ✓ Access | select field | — | — | — | — | — | — |

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

- **understanding**: Chips like "Create · Venue · Museum · Existing organisation · Dubai · Permanent"; inferred ones dashed with "Confirm"; areas to configure as a checklist (venue, products, schedule, capacity, pricing, channels, ticket media, access). *(source: contracts/satellite/ai.yaml#answerConfigurationQuestion (extracted.provenance) / contracts/satellite/ai.yaml#/components/schemas/AiProvenance)*

**Data it reads**: `listConfigurationSources` (onLoad, Attached documents with extraction status and what they …); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The type business intent configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the type business intent untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No type business intent configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The session is no longer discovering (`session-not-open`), or the governance data policy refuses the document (`governance-blocked`).; 409 The session is no longer discovering (`session-not-open`).; 422 The asset is not a readable document or image (`unreadable-source`), for example a scan with no text layer the extractor could read. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
understanding:
  action: Create
  object: Venue
  venueType: Museum
  organisation: Existing - Tidewater Heritage
  location: Dubai
  operation: Permanent
  areas:
  - Venue
  - Products
  - Schedule
  - Capacity
  - Pricing
  - Sales channels
  - Ticket media
  - Access
```

#### Permissions

- `startConfigurationSession` → `AI_USE` (operate) · staff
- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `attachConfigurationSource` → `AI_USE` (operate) · staff
- `listConfigurationSources` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.31 | System shall allow administrators to upload event briefs, brochures, schedules, PDFs or spreadsheets and use AI to automatically generate event configurations, sessions, ticket types, capacities … | Ticketing Catalogue | CONTRACTED | `attachConfigurationSource` |
| 1.4.21 | System shall allow administrators to upload spreadsheets, brochures, PDFs or existing catalogues and automatically generate products, pricing structures, rules, entitlements and configurations using … | Ticketing Catalogue | CONTRACTED | `attachConfigurationSource` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-470` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-470`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 2: Works in Setup Type & Business Intent Discovery → Understand what the administrator is actually trying to accomplish before asking detailed configuration questions. This is the first AI interview screen.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-470?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-471` Venue & Business Model Discovery

**Understand how the business operates so TICVAI can determine which configuration branches are relevant.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture as relevant) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `sessionId` (session), `venueId` (navigation), `tenantId` (navigation) |
| Route | `/platform/venue-business-model-discovery-adm-471` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `answerConfigurationQuestion` (AI_USE), `getConfigurationBlueprint` (AI_USE), `setAiVenueSettings` (AI_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Confirm / Edit Understanding / Continue. Each needs an operation, or needs removing from the screen; this …

**From the AI & Intelligence process.** Venue and business model discovery: name, type, location, time zone, currency, permanent/seasonal/temporary, indoor/outdoor, locations and attractions, and which admission models apply (general, dated, open-dated, timeslot, assigned seating, multi-day, membership, pass, ride-based). Conditional branches follow (a theatre brings performances, seat map, sections, price categories). This is also where the venue AI profile is collected for the baselines. The one thing to get right: only the branches the answers make relevant are shown.

**Known correction pending (do not draw the wrong version)**

- **Admission models and the theatre branch are separate selectFields; the branch logic is drawn as fields ("Conditional Logic", "Venue = Theatre").** Why: Branches are questions the assistant asks; the screen shows only relevant ones. *(source: screens/P09-platform-admin-console.yaml#ADM-471; AI & Intelligence)*

**Fixed on main** (the package already carries these; draw what it says): setAiVenueSettings is not declared though this is where the profile is collected. (CHG-WIR-012).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Venue Name | select field | — | — | — | — | — | — |
| Venue Type | select field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| City | select field | — | — | — | — | — | — |
| Time Zone | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Operating Model | select field | — | — | — | — | — | — |
| Permanent / Seasonal / Temporary | text field | — | — | — | — | — | — |
| Indoor / Outdoor / Mixed | text field | — | — | — | — | — | — |
| Number of Locations | select field | — | — | — | — | — | — |
| Number of Attractions / Experiences | text field | — | — | — | — | — | — |
| Business Model Discovery | select field | — | — | — | — | — | — |
| General Admission | select field | — | — | — | — | — | — |
| Dated Admission | select field | — | — | — | — | — | — |
| Open-Dated Admission | select field | — | — | — | — | — | — |
| Timeslot Admission | select field | — | — | — | — | — | — |
| Assigned Seating | select field | — | — | — | — | — | — |
| Multi-Day Admission | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Subscription | select field | — | — | — | — | — | — |
| Pass | select field | — | — | — | — | — | — |
| Attraction / Ride-Based | select field | — | — | — | — | — | — |
| Mixed Model | select field | — | — | — | — | — | — |
| Conditional Logic | select field | — | — | — | — | — | — |
| Venue = Theatre | select field | — | — | — | — | — | — |
| Performances | select field | — | — | — | — | — | — |
| Seat Map | select field | — | — | — | — | — | — |
| Sections | select field | — | — | — | — | — | — |
| Price Categories | select field | — | — | — | — | — | — |
| Show Schedule | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `getConfigurationBlueprint` ?module |
| Decision class | segmented control | — | Required · Recommended · Optional | `getConfigurationBlueprint` ?decisionClass |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Save venue AI profile** (modal, opened by *Save venue AI profile*; *Save venue AI profile* calls `setAiVenueSettings`, *Cancel* sends nothing)

**Collects what `setAiVenueSettings` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

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

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **admission models**: Multi-select with one-line examples; each selected model opens its branch of questions; unselected branches are not asked. *(source: contracts/satellite/ai.yaml#answerConfigurationQuestion / MoM 18 Sep 4.5)*
- **venue AI profile**: Capacity, typical weekday/weekend attendance, peak months, average spend, F&B attach rate - asked in conversation, saved to the venue AI settings so every forecast and suggestion starts from them. *(source: contracts/satellite/ai.yaml#setAiVenueSettings / ADR-0051 (venue AI profile captured at onboarding))*

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
| Confirm / Edit Understanding / Continue (primary button) | navigation or local | — | — | — | — |
| Save venue AI profile (secondary button) | `setAiVenueSettings` PUT `/venues/{venueId}/ai-settings` | AiVenueSettings | AiVenueSettings | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue business model configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue business model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue business model configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The session is no longer discovering (`session-not-open`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue:
  name: Coastal Aqua / كوستال أكوا
  type: Water park
  city: Dubai
  timeZone: Asia/Dubai
  currency: AED
  operation: Seasonal
  setting: Outdoor
  attractions: 18
  models:
  - Dated admission
  - Membership
  - Timeslot (cabanas)
```

#### Permissions

- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-471` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-471`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 4: Works in Venue & Business Model Discovery → Understand how the business operates so TICVAI can determine which configuration branches are relevant.

#### Acceptance for the design

- [ ] Every input above is drawn (50), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-471?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Confirm / Edit Understanding / Continue, Save venue AI profile.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-472` Guided Question & Answer Workspace

**Provide the main adaptive AI interview workspace. This is the core screen of Board 1. It should feel conversational but remain structured and controlled.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `sessionId` (session), `tenantId` (navigation) |
| Route | `/platform/guided-question-answer-workspace-adm-472` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `answerConfigurationQuestion` (AI_USE), `getConfigurationBlueprint` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** The core interview workspace: one question at a time on the left, the growing blueprint on the right. Answers can be typed in words or picked; each extracted value appears in the blueprint with where it came from. The one thing to get right: conversational but controlled - the assistant asks for anything required that is missing (e.g. capacity) rather than proceeding, and every value is visibly confirmed, recommended or inferred.

**Known correction pending (do not draw the wrong version)**

- **Layout is an unlabelled button, a detail panel and Cancel.** Why: Two-pane conversation + blueprint, bound to answerConfigurationQuestion and getConfigurationBlueprint. *(source: screens/P09-platform-admin-console.yaml#ADM-472; AI & Intelligence)*

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

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **answer**: Free text (up to 4,000 characters) or the structured control the question offers (date, number, choice); not streamed - a 10-second wait shows "Thinking" with the question kept on screen. *(source: contracts/satellite/ai.yaml#answerConfigurationQuestion)*

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

- **blueprint side panel**: Values grouped by module, each with a provenance chip (You said / AI recommended / Inferred - confirm) and, where extracted from a document, its citation ("Price list p.4"). *(source: contracts/satellite/ai.yaml#getConfigurationBlueprint / contracts/satellite/ai.yaml#/components/schemas/AiProvenance)*
- **progress**: Progress % and required items still open. *(source: contracts/satellite/ai.yaml#/components/schemas/AiConfigurationSession (progressPercent))*

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guided question answer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guided question answer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guided question answer yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guided question answer are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The session is no longer discovering (`session-not-open`). |

#### Edge cases to draw

- **Required information missing**: The assistant asks for it; the blueprint cannot reach Ready while a required decision is open. *(source: MoM 18 Sep 4.5 / MoM 18 Sep §5 / contracts/satellite/ai.yaml#/components/schemas/AiConfigurationBlueprint (requiredOpen))*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
turn:
  question: What is the maximum number of guests in the park at once?
  answer: About 6,000, but 4,500 in summer
  extracted:
  - key: capacity
    value: 6000
    provenance: confirmed
  - key: summerCapacity
    value: 4500
    provenance: confirmed
```

#### Permissions

- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-472` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-472`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 6: Works in Guided Question & Answer Workspace → Provide the main adaptive AI interview workspace. This is the core screen of Board 1. It should feel conversational but remain structured and controlled.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-472?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Cancel.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-473` Product & Admission Model Discovery

**Determine what the venue sells and how each product provides admission or entitlement.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `sessionId` (session), `tenantId` (navigation) |
| Route | `/platform/product-admission-model-discovery-adm-473` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `answerConfigurationQuestion` (AI_USE), `getConfigurationBlueprint` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Product and admission discovery: what the venue sells and how each product grants entry or an entitlement (ticket types, validity, date/time rules, guest categories, bundles, add-ons, memberships). The one thing to get right: products are proposed in the existing ticketing model's terms, not a separate AI product model.

**Known correction pending (do not draw the wrong version)**

- **Unbound button/panel layout.** Why: Same conversation + blueprint pattern as ADM-472, filtered to products. *(source: screens/P09-platform-admin-console.yaml#ADM-473; AI & Intelligence)*

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

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **proposed product list**: Product, type, validity, guest categories, date/time rule, entitlement - each with provenance. *(source: contracts/satellite/ai.yaml#getConfigurationBlueprint / MoM 18 Sep 4.5)*

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product admission model list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product admission model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product admission model yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product admission model are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The session is no longer discovering (`session-not-open`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
products:
- name: Day Pass Adult
  type: dated
  validity: Selected date
  categories:
  - Adult
- name: Family Day Pass (2+2)
  type: bundle
- name: Annual Pass
  type: membership
  validity: 12 months
```

#### Permissions

- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-473` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-473`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 8: Works in Product & Admission Model Discovery → Determine what the venue sells and how each product provides admission or entitlement.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-473?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Cancel.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-474` Operational Requirement Discovery

**Understand the operational rules needed to deliver the configured products.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `sessionId` (session), `tenantId` (navigation) |
| Route | `/platform/operational-requirement-discovery-adm-474` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `answerConfigurationQuestion` (AI_USE), `getConfigurationBlueprint` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Confirm Operations / Add Requirement / Continue. Each needs an operation, or needs removing from the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Operational requirement discovery: opening hours, closures, capacity by area, timeslot lengths, access rules, staffing assumptions - the rules needed to deliver the products. The one thing to get right: operational answers that also feed the venue AI profile (hours, capacity, productivity) are marked as such.

**Known correction pending (do not draw the wrong version)**

- **"Confirm Operations / Add Requirement / Continue" is one button label.** Why: Three actions. *(source: screens/P09-platform-admin-console.yaml#ADM-474; AI & Intelligence)*

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

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm Operations / Add Requirement / Continue (primary button) | navigation or local | — | — | — | — |
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **operations summary**: Hours, closures, capacities, slot rules as confirmable rows; "Add requirement" for anything the assistant did not ask. *(source: contracts/satellite/ai.yaml#getConfigurationBlueprint)*

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operational requirement discovery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operational requirement discovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operational requirement discovery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operational requirement discovery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The session is no longer discovering (`session-not-open`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
operations:
  hours: 10:00-18:00, Fri 10:00-20:00
  closures: Mondays Jun-Aug
  cabanaSlots: Full day only
```

#### Permissions

- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-474` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-474`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 10: Works in Operational Requirement Discovery → Understand the operational rules needed to deliver the configured products.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-474?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Confirm Operations / Add Requirement / …, Open access grant, Cancel.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-475` Commercial Requirement Discovery

**Understand how the venue intends to sell and commercially manage its products without actually configuring pricing yet.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `sessionId` (session), `tenantId` (navigation) |
| Route | `/platform/commercial-requirement-discovery-adm-475` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `answerConfigurationQuestion` (AI_USE), `getConfigurationBlueprint` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Commercial requirement discovery: how the venue intends to sell (channels, B2B and resellers, promotions, memberships, dynamic pricing appetite) without configuring prices yet. The one thing to get right: it records intent; prices and rules are proposed later and approved by a person.

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

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **commercial intent**: Channels, partner selling, promotion types, pricing approach (fixed, seasonal, dynamic within bands) as confirmable rows with provenance. *(source: contracts/satellite/ai.yaml#getConfigurationBlueprint)*

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial requirement discovery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial requirement discovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial requirement discovery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial requirement discovery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The session is no longer discovering (`session-not-open`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
intent:
  channels:
  - Website
  - App
  - POS
  - Kiosk
  - Resellers
  pricing: Seasonal with weekend uplift; dynamic within ±15% later
  promotions:
  - Family bundle
  - Early bird
```

#### Permissions

- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-475` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-475`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 12: Works in Commercial Requirement Discovery → Understand how the venue intends to sell and commercially manage its products without actually configuring pricing yet.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-475?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Cancel.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-476` Required, Recommended & Optional Decisions

**Prevent the administrator from forgetting important configuration while also preventing unnecessary questions from blocking setup. This screen is fundamental to making the AI genuinely useful.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `decisionKey` (navigation), `sessionId` (session), `tenantId` (navigation) |
| Route | `/platform/required-recommended-optional-decisions-adm-476` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getConfigurationBlueprint` (AI_USE), `decideBlueprintRecommendation` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**From the AI & Intelligence process.** Required, recommended and optional decisions: what must be decided now, what the assistant recommends with a default policy, and what can wait - so nothing important is forgotten and nothing unnecessary blocks setup. The one thing to get right: required decisions cannot be deferred; recommended ones can be accepted with the assistant's value in one click; optional ones can be decided later.

**Known correction pending (do not draw the wrong version)**

- **Decision choices drawn as selectFields ("Configure Now", "Use Recommended Policy", "Decide Later", "Required Rule").** Why: They are the decision buttons on each item, mapped to accept/modify/reject/defer. *(source: contracts/satellite/ai.yaml#decideBlueprintRecommendation; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Configure Now | select field | — | — | — | — | — | — |
| Use Recommended Policy | select field | — | — | — | — | — | — |
| Decide Later | select field | — | — | — | — | — | — |
| Required Rule | select field | — | — | — | — | — | — |

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

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **decision per item**: Required - accept or modify (no defer); Recommended - accept, modify, reject; Optional - accept, modify, reject, decide later. Modify takes a value; a note is optional. *(source: contracts/satellite/ai.yaml#decideBlueprintRecommendation / contracts/satellite/ai.yaml#/components/schemas/AiBlueprintDecision (decisionClass))*

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

- **three columns**: Required / Recommended / Optional with counts; each item shows the question, the proposed value, why (recommendation), and provenance. *(source: contracts/satellite/ai.yaml#getConfigurationBlueprint (decisionClass))*

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The required recommended optional configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the required recommended optional untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No required recommended optional configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The session is no longer open for decisions (`session-not-open`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
required:
- Refund policy for day passes
recommended:
- item: Child age limit
  value: 3-11 years
  why: Most UAE water parks use 3-11
optional:
- Birthday party packages
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-476` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-476`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 14: Works in Required, Recommended & Optional Decisions → Prevent the administrator from forgetting important configuration while also preventing unnecessary questions from blocking setup. This screen is fundamental to making the AI genuinely useful.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-476?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-477` Missing Information & Clarification Center

**Allow AI to identify incomplete, contradictory, ambiguous, or logically inconsistent requirements before producing the final blueprint.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `decisionKey` (navigation), `sessionId` (session), `tenantId` (navigation) |
| Route | `/platform/missing-information-clarification-center-adm-477` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `answerConfigurationQuestion` (AI_USE), `getConfigurationBlueprint` (AI_USE), `decideBlueprintRecommendation` (AI_USE), `attachConfigurationSource` (AI_USE), `listConfigurationSources` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**From the AI & Intelligence process.** Missing information and clarification centre: everything incomplete, contradictory, ambiguous or inconsistent before the blueprint is final - required missing, clarifications, conflicts, warnings - each with the question that resolves it. The one thing to get right: each item can be answered in place, and a conflict names both contradicting values and where each came from.

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

**Required Missing** (metric tile)

**Clarifications Needed** (metric tile)

**Conflicts** (metric tile)

**Warnings** (metric tile)

**Recommendations** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **issue list**: Type (required missing, clarification, conflict, warning, recommendation), the question, the values involved with their sources (a document page, the user's answer). *(source: contracts/satellite/ai.yaml#getConfigurationBlueprint (issues) / contracts/satellite/ai.yaml#/components/schemas/AiBlueprintDecision (sourceCitation))*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Answer**: Resolves the item via the next question; counts update. *(source: contracts/satellite/ai.yaml#answerConfigurationQuestion)*

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far); `listConfigurationSources` (onLoad, Attached documents with extraction status and what they …); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The missing information clarification list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the missing information clarification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No missing information clarification yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the missing information clarification are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The session is no longer discovering (`session-not-open`), or the governance data policy refuses the document (`governance-blocked`).; 409 The session is no longer discovering (`session-not-open`).; 409 The session is no longer open for decisions (`session-not-open`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
conflict: 'Capacity: you said 6,000; the brochure (p.2) says 5,500. Which is right?'
missing: No refund policy given for cabanas
```

#### Permissions

- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
- `decideBlueprintRecommendation` → `AI_USE` (operate) · staff
- `attachConfigurationSource` → `AI_USE` (operate) · staff
- `listConfigurationSources` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.31 | System shall allow administrators to upload event briefs, brochures, schedules, PDFs or spreadsheets and use AI to automatically generate event configurations, sessions, ticket types, capacities … | Ticketing Catalogue | CONTRACTED | `attachConfigurationSource` |
| 1.4.21 | System shall allow administrators to upload spreadsheets, brochures, PDFs or existing catalogues and automatically generate products, pricing structures, rules, entitlements and configurations using … | Ticketing Catalogue | CONTRACTED | `attachConfigurationSource` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-477` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-477`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 16: Works in Missing Information & Clarification Center → Allow AI to identify incomplete, contradictory, ambiguous, or logically inconsistent requirements before producing the final blueprint.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-477?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-478` Configuration Blueprint & Dependency Map

**Convert the entire AI conversation into a structured configuration blueprint that can be reviewed before moving to Board 2. This is the final output of Board 1. Nothing should yet be created in production.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `sessionId` (session), `tenantId` (navigation) |
| Route | `/platform/configuration-blueprint-dependency-map-adm-478` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getConfigurationBlueprint` (AI_USE), `buildConfigurationPlan` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** The blueprint and dependency map: the whole conversation turned into a structured configuration blueprint - objects by module and the order they depend on each other - reviewed before anything is built. Nothing is created in production here. The one thing to get right: readiness (not ready, ready with warnings, ready) is explicit, and compiling the plan is disabled while required decisions are open.

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

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **dependency map**: Module lanes (venue, products, schedule, pricing, channels, access) with objects as nodes and arrows for dependencies (e.g. pricing for a channel before publishing a product to it). *(source: contracts/satellite/ai.yaml#/components/schemas/AiConfigurationBlueprint (dependencyMap) / MoM 18 Sep 4.6)*
- **readiness**: Badge with required-open count and issues; version number. *(source: contracts/satellite/ai.yaml#/components/schemas/AiConfigurationBlueprint (readiness, requiredOpen))*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Build plan**: Compiles the blueprint into an action plan (draft) and moves to the build command centre; nothing executes. *(source: contracts/satellite/ai.yaml#buildConfigurationPlan)*

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The blueprint dependency map list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the blueprint dependency map untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No blueprint dependency map yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the blueprint dependency map are still there. The pack's own statuses are Blueprint Ready — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The blueprint is not ready: a required decision is open or deferred (AIC-115). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
blueprint:
  version: 3
  readiness: readyWithWarnings
  requiredOpen: 0
  objects: 46
  warnings:
  - No B2B rate for resellers yet
```

#### Permissions

- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-478` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-478`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 18: Works in Configuration Blueprint & Dependency Map → Convert the entire AI conversation into a structured configuration blueprint that can be reviewed before moving to Board 2. This is the final output of Board 1. Nothing should yet be created in …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-478?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Cancel.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
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
"attachConfigurationSource": {"method":"POST","path":"/configuration-sessions/{sessionId}/sources","contract":"ai","summary":"Seed a configuration session from an uploaded document","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"buildConfigurationPlan": {"method":"POST","path":"/configuration-sessions/{sessionId}/plan","contract":"ai","summary":"Compile the blueprint into a plan","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlanDetail"},
"decideBlueprintRecommendation": {"method":"POST","path":"/configuration-sessions/{sessionId}/decisions/{decisionKey}","contract":"ai","summary":"Accept, modify, reject or defer a blueprint decision","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiBlueprintDecision"},
"getConfigurationBlueprint": {"method":"GET","path":"/configuration-sessions/{sessionId}/blueprint","contract":"ai","summary":"The blueprint so far","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"module","in":"query","required":null},{"name":"decisionClass","in":"query","required":null}],"requestBody":null,"responds":"AiBlueprintView"},
"listConfigurationSessions": {"method":"GET","path":"/configuration-sessions","contract":"ai","summary":"Configuration-assistant sessions","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"intent","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConfigurationSources": {"method":"GET","path":"/configuration-sessions/{sessionId}/sources","contract":"ai","summary":"Documents attached to a configuration session","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOwnPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants/mine","contract":"identity","summary":"The calling platform operator's own grants into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTenants": {"method":"GET","path":"/tenants","contract":"subscription","summary":"List tenants","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"planId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"setAiVenueSettings": {"method":"PUT","path":"/venues/{venueId}/ai-settings","contract":"ai","summary":"Set the venue AI profile","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiVenueSettings","responds":"AiVenueSettings"},
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
"AiBlueprintDecision": {"type":"object","x-ticvai-persistence":"ai.blueprint_decision","description":"One decision in a blueprint and what the administrator did with it. **Scoped through its blueprint** (`platform.apply_parent_rls`).","required":["blueprintId","decisionKey","decisionClass","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"blueprintId":{"type":"string","format":"uuid","x-ticvai-references":"ai.blueprint"},"decisionKey":{"type":"string"},"module":{"type":"string"},"decisionClass":{"type":"string","enum":["required","recommended","optional"]},"question":{"type":"string","nullable":true},"value":{"type":"object","additionalProperties":true,"nullable":true},"provenance":{"$ref":"#/components/schemas/AiProvenance"},"sourceId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.config_source","description":"The attached document the value was extracted from (29 September, build; `attachConfigurationSource`)."},"sourceCitation":{"type":"string","nullable":true,"maxLength":200,"description":"Where in it, e.g. `page 4`, `sheet Prices!B7`, `logo region`."},"recommendation":{"type":"object","additionalProperties":true,"nullable":true,"description":"What the assistant recommends and why (ADM-491): mandatory configuration and best practice kept apart."},"status":{"type":"string","enum":["open","accepted","modified","rejected","deferred"]},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"note":{"type":"string","nullable":true}}},
"AiBlueprintView": {"type":"object","x-ticvai-persistence":"none — ai.blueprint with its ai.blueprint_decision rows","description":"A blueprint with its decisions.","required":["blueprint","decisions"],"properties":{"blueprint":{"$ref":"#/components/schemas/AiConfigurationBlueprint"},"decisions":{"type":"array","items":{"$ref":"#/components/schemas/AiBlueprintDecision"}}}},
"AiConfigurationBlueprint": {"type":"object","x-ticvai-persistence":"ai.blueprint","description":"**The blueprint** (design 2.2 D step 2, ADM-478): decisions, severity-graded issues and a dependency map. **Never `ready` while a required decision is deferred** (AIC-115).","required":["sessionId","version","readiness"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"sessionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.config_session"},"version":{"type":"integer","minimum":1},"readiness":{"type":"string","enum":["notReady","readyWithWarnings","ready"],"readOnly":true},"requiredOpen":{"type":"integer","minimum":0,"readOnly":true,"description":"Required decisions not yet accepted or modified."},"issues":{"$ref":"#/components/schemas/AiBlueprintIssueList"},"dependencyMap":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Configuration objects and the order they depend on each other, by module."},"summary":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiConfigurationQuestion": {"type":"object","x-ticvai-persistence":"none — chosen per turn from the configuration knowledge model","description":"**The next question, chosen by the configuration knowledge model, not by the language model** (design 2.2 D, AIC-111). The model only extracts a structured answer against `answerSchema`.","required":["questionKey","text","decisionClass"],"properties":{"questionKey":{"type":"string"},"text":{"type":"string"},"module":{"type":"string","nullable":true},"decisionClass":{"type":"string","enum":["required","recommended","optional"]},"answerType":{"type":"string","enum":["freeText","singleChoice","multiChoice","number","date","confirm"]},"options":{"type":"array","items":{"type":"string"}},"why":{"type":"string","nullable":true,"description":"Why it is asked: which configuration branch it opens or closes."},"answerSchema":{"type":"object","additionalProperties":true,"nullable":true,"description":"JSON Schema the extracted answer must satisfy."}}},
"AiConfigurationSession": {"type":"object","x-ticvai-persistence":"ai.config_session","description":"**A configuration-assistant session** (design 2.2 D steps 1-2, C7; ADM-469..478). Discovery runs from the configuration knowledge model; every value carries provenance.","required":["intent","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"intent":{"type":"string","enum":["create","modify","extend","clone"]},"venueType":{"type":"string","nullable":true,"description":"Museum, theme park, water park, zoo, aquarium, theatre, stadium, festival, conference..."},"sourceScopePath":{"type":"string","nullable":true,"description":"The setup being cloned or extended."},"status":{"type":"string","enum":["discovering","blueprintReady","planned","executing","completed","abandoned"],"readOnly":true},"progressPercent":{"type":"integer","minimum":0,"maximum":100,"readOnly":true},"nextQuestion":{"allOf":[{"$ref":"#/components/schemas/AiConfigurationQuestion"}],"nullable":true,"readOnly":true},"conversationId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.conversation"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan"},"locale":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"startedAt":{"type":"string","format":"date-time","readOnly":true},"lastActivityAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiConfigurationSource": {"type":"object","x-ticvai-persistence":"ai.config_source","description":"**A document attached to a configuration session** (1.3.31, 1.4.21, 2.6.50): the uploaded asset, what kind of source it is, and how its extraction went. The values it yields are blueprint decisions with provenance `inferred` and a citation back here. **Scoped through its session** (`platform.apply_parent_rls`).","required":["sessionId","assetId","sourceKind","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"sessionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.config_session"},"assetId":{"type":"string","format":"uuid","x-ticvai-references":"assets.MediaAsset"},"sourceKind":{"type":"string","enum":["brief","brochure","catalogue","priceList","spreadsheet","brandAsset"]},"note":{"type":"string","nullable":true},"status":{"type":"string","enum":["extracting","extracted","partial","failed"],"readOnly":true},"pageCount":{"type":"integer","nullable":true,"readOnly":true},"valuesExtracted":{"type":"integer","readOnly":true,"description":"Questions it pre-answered."},"unreadRegions":{"type":"array","items":{"type":"string"},"readOnly":true,"description":"Pages or regions it could not read, named so a person can answer by hand."},"attachedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"attachedAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"AiConfigurationTurn": {"type":"object","x-ticvai-persistence":"none — the answer is written to ai.blueprint_decision and the session","description":"The result of one answer: what was extracted with its provenance, the next question and progress.","required":["session"],"properties":{"session":{"$ref":"#/components/schemas/AiConfigurationSession"},"extracted":{"type":"array","items":{"type":"object","properties":{"decisionKey":{"type":"string"},"value":{"type":"object","additionalProperties":true,"nullable":true},"provenance":{"$ref":"#/components/schemas/AiProvenance"}}}},"nextQuestion":{"allOf":[{"$ref":"#/components/schemas/AiConfigurationQuestion"}],"nullable":true},"clarificationsNeeded":{"type":"array","items":{"type":"string"}}}},
"AiProvenance": {"type":"string","enum":["confirmed","aiRecommended","inferred","unknown"],"description":"**Where a configuration value came from** (design 2.2 D, AIC-111): said by the administrator, recommended by the assistant, inferred from other answers, or not known yet. Shown beside every value; no confidence number is shown for configuration (design 5.6)."},
"AiVenueSettings": {"type":"object","x-ticvai-persistence":"ai.venue_settings","description":"**The venue AI profile** (29 September, AI functions review): the figures a venue gives at onboarding so every data-driven answer is useful before it has history. One row per venue; configuration, not history. Defaults come from the starting pattern for `venueType`, which TICVAI writes from published sources and made-up example curves, **never from another tenant's data** (AI-D01, AIP-149).","required":["venueId","venueType"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"venueType":{"type":"string","enum":["waterPark","themePark","familyEntertainmentCentre","museum","arena","zooAquarium","other"]},"isOutdoor":{"type":"boolean","default":true,"description":"Outdoor venues take the summer-heat and weather effects."},"capacity":{"type":"integer","minimum":1,"nullable":true},"openingHours":{"type":"array","description":"The usual week. Exceptions come from the venue calendar.","items":{"type":"object","properties":{"dayOfWeek":{"type":"integer","minimum":1,"maximum":7},"opensAt":{"type":"string"},"closesAt":{"type":"string"}}}},"typicalWeekdayAttendance":{"type":"integer","minimum":0,"nullable":true},"typicalWeekendAttendance":{"type":"integer","minimum":0,"nullable":true},"peakMonths":{"type":"array","items":{"type":"integer","minimum":1,"maximum":12}},"averageSpend":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"fnbAttachRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"staffProductivity":{"type":"object","additionalProperties":{"type":"number"},"description":"Per role, units per staff hour, e.g. `{\"cashier\": 40, \"gate\": 300}`. Defaults from the pattern."},"startingPatternKey":{"type":"string","readOnly":true,"description":"The pattern and version in use, e.g. `waterPark@3`."},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE","CORE_AI_PUBLISH","TICKETING_AI_PUBLISH","ACCESS_AI_PUBLISH","FNB_AI_PUBLISH","RETAIL_AI_PUBLISH","INVENTORY_AI_PUBLISH","SEATING_AI_PUBLISH","MEMBERSHIP_AI_PUBLISH","MARKETING_AI_PUBLISH","RESOURCES_AI_PUBLISH","QUEUE_AI_PUBLISH","TRANSPORT_AI_PUBLISH","GAMES_AI_PUBLISH","MAINTENANCE_AI_PUBLISH","ACCREDITATION_AI_PUBLISH","PARTNER_AI_PUBLISH","ANALYTICS_AI_PUBLISH","BIOMETRIC_IMAGE_VIEW","ACCESS_DIRECTION_SET","REPORT_GOVERNANCE_MANAGE"]},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"SuspensionMode": {"type":"string","description":"Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n","enum":["readOnly","noNewSales","fullLockout"]},
"Tenant": {"x-ticvai-persistence":"control.tenant","type":"object","required":["id","code","name","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"$ref":"#/components/schemas/TenantStatus"},"suspensionMode":{"$ref":"#/components/schemas/SuspensionMode"},"suspensionReason":{"type":"string","nullable":true},"suspensionEffectiveAt":{"type":"string","format":"date-time","nullable":true,"description":"When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."},"suspensionNoticeMessage":{"$ref":"#/components/schemas/LocalisedText","description":"The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."},"terminationScheduledAt":{"type":"string","format":"date-time","nullable":true,"description":"When `terminateTenant` started the retention window. Null when no termination is under way."},"terminationRetentionUntil":{"type":"string","format":"date-time","nullable":true,"description":"`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."},"terminationReason":{"type":"string","maxLength":1000,"nullable":true},"terminationRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"planId":{"type":"string","format":"uuid","nullable":true},"planName":{"type":"string","nullable":true},"cellCount":{"type":"integer"},"venueCount":{"type":"integer"},"regionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500,"nullable":true,"description":"Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."},"accountManagerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantStatus": {"type":"string","enum":["onboarding","active","suspended","terminating","terminated"]}
}
```
