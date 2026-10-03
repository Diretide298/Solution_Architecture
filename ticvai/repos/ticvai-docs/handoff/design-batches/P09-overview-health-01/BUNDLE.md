# P09-overview-health-01 — P09 · Overview & Health

**5 screens · 22 operations · 34 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `AI_AUDIT_VIEW, AUDIT_VIEW, PLATFORM_CELL_MANAGE, PLATFORM_CELL_VIEW, PLATFORM_RELEASE_PROMOTE, PLATFORM_RELEASE_VIEW, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
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
| `ADM-002` | Platform Dashboard | B | 2 | 33 | 6 | 9 | 0 | 0 | — | notStarted (generated) |
| `ADM-003` | Cross-Tenant Health Dashboard | A | 4 | 37 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-004` | Platform Audit Log | D | 9 | 30 | 7 | 4 | 0 | 0 | — | notStarted (generated) |
| `ADM-013` | Tenant Performance Monitor | B | 0 | 37 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-029` | Deployment Monitor | B | 5 | 53 | 7 | 0 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-002` Platform Dashboard

**The screen this app sits on. Everything else is entered from here and returns to it.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Overview & Health · wave 1 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-002 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_VIEW` (2 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenants` reads the population and `getEntitlementUsage` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/platform-dashboard` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant. **Drawn 26 August** — `Dashboards Board` frame `adm-002`. **One board draws five dashboards across five platforms** — platform admin, partner, support, guest web and cross-tenant health. A dashboard is a shape rather than a domain, and the pack recognised that before the package did. **Exits to the moved workshop-pack screens dropped 2 October 2026** (CHG-SBO-023; DEC-100, CHG-MOV-001): ADM-048, ADM-058, ADM-078, ADM-088, ADM-098, ADM-108, ADM-118, ADM-128, ADM-138, ADM-148, ADM-158, ADM-168, ADM-178, ADM-188, ADM-198, ADM-208, ADM-218, ADM-228, ADM-238, ADM-248, ADM-258, ADM-268, ADM-278, ADM-288, ADM-298, ADM-308, ADM-559, ADM-569, ADM-579, ADM-589, ADM-599, ADM-609, ADM-629, ADM-639 …

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): getSsoConfig (USER_MANAGE) on the platform home; tenant SSO is not platform-home content and needs a tenant grant (R098; design-notes correction …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The Console's home for a platform operator: tenants by status, cells by health, licence pressure, open alerts and the operator's own open grants, each opening the screen that acts on it. Read-only; nothing is changed from here.

**Fixed on main** (the package already carries these; draw what it says): getSsoConfig (USER_MANAGE) on the platform home. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every tenant' drop id, planId, accountManagerPrincipalId; 'Every cell' drop id … (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | radio group | optional | — | Onboarding · Active · Suspended · Terminating · Terminated | — | Sends `?status=` to `listTenants`. | `listTenants` ?status |
| Plan id | picker: choose a plan (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?planId=` to `listTenants`. | `listTenants` ?planId |

#### Outputs: what the screen shows and produces

**Shown**

**Every tenant** (data table, from `listTenants`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Status | chip: Onboarding, Active, Suspended, Terminating, Terminated | — |
| Plan name | text | — |
| Cell count | 1,234 | — |
| Venue count | 1,234 | — |

**Every cell** (data table, from `listTenantCells`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Last contact at | 1 Oct 2026, 14:30 | When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first. |
| Licence expires at | 1 Oct 2026, 14:30 | On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. |
| Region name | text | — |
| Country code | text | — |

**The selected tenant** (detail panel, from `listTenants`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Status | chip: Onboarding, Active, Suspended, Terminating, Terminated | — |
| Suspension mode | chip: Read only, No new sales, Full lockout | Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets. |
| Suspension effective at | 1 Oct 2026, 14:30 | When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. A future value is a pending suspension: the tenant stays `active` … |
| Plan name | text | — |
| Cell count | 1,234 | — |
| Venue count | 1,234 | — |

**The tenant** (detail panel, from `getTenant`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Status | chip: Onboarding, Active, Suspended, Terminating, Terminated | — |
| Suspension mode | chip: Read only, No new sales, Full lockout | Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets. |
| Suspension effective at | 1 Oct 2026, 14:30 | When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. A future value is a pending suspension: the tenant stays `active` … |
| Plan name | text | — |
| Cell count | 1,234 | — |
| Venue count | 1,234 | — |

**The licence position** (detail panel, from `getTenantLicences`)

| Shows | Format | Notes |
|---|---|---|
| Plan | the name it points at, never the id | — |
| Licensed modules | list or chips (count when long) | Union of plan modules and add-ons. The White Label Builder reads this and cannot enable anything absent from it. |
| Limits | list or chips (count when long) | — |

**The entitlement usage** (detail panel, from `getEntitlementUsage`)

| Shows | Format | Notes |
|---|---|---|
| Metrics | list or chips (count when long) | — |
| As at | 1 Oct 2026, 14:30 | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Tenants needing attention**: Suspended, terminating, over licence limits and cells unreachable first; counts link to filtered lists. *(source: contracts/satellite/subscription.yaml#listTenants; contracts/satellite/subscription.yaml#getEntitlementUsage)*
- **My open grants**: The operator's own platform-staff grants into tenants with time left. *(source: contracts/spine/identity.yaml#listOwnPlatformStaffGrants; R098)*

**Data it reads**: `listTenants` (onLoad, from page inventory); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `listTenantCells` (onLoad, List a tenant's cells)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`
- → `ADM-004` Platform Audit Log: *Platform Audit Log*; carries `tenantId`
- → `ADM-005` Tenant Directory: *Tenant Directory*; carries `tenantId`
- → `ADM-006` Tenant Hierarchy Explorer: *Tenant Hierarchy Explorer*; carries `tenantId`
- → `ADM-007` Module & Feature Entitlement: *Module & Feature Entitlement*; carries `tenantId`
- → `ADM-008` Subscription & Plan Management: *Subscription & Plan Management*; carries `planId`, `tenantId`
- → `ADM-012` Tenant Isolation & Resource Pool: *Tenant Isolation & Resource Pool*; carries `cellId`, `tenantId`
- → `ADM-369` Commercial Command Center: *Commercial Command Center*
- → `ADM-459` Billing & Commercial Command Center: *Billing & Commercial Command Center*
- → `ADM-379` Welcome & Start Your TICVAI Journey: *Welcome & Start Your TICVAI Journey*
- → `ADM-389` Commercial Rules Engine Overview: *Commercial Rules Engine Overview*
- → `ADM-399` Recommended Package Overview: *Recommended Package Overview*
- → `ADM-409` Purchase / Trial Journey Selection: *Purchase / Trial Journey Selection*
- → `ADM-419` Provisioning Command Center: *Provisioning Command Center*; carries `cellId`
- → `ADM-449` Usage & License Command Center: *Usage & License Command Center*
- → `ADM-469` AI Configuration Home & Start: *AI Configuration Home & Start*; carries `tenantId`
- → `ADM-479` AI Configuration Build Command Center: *AI Configuration Build Command Center*; carries `planId`, `tenantId`
- → `ADM-489` AI Configuration Readiness Center: *AI Configuration Readiness Center*; carries `planId`, `tenantId`
- → `ADM-499` Forecasting Command Center: *Forecasting Command Center*; carries `tenantId`
- → `ADM-509` Operational Forecasting Command Center: *Operational Forecasting Command Center*; carries `tenantId`
- → `ADM-519` AI Governance Command Center: *AI Governance Command Center*; carries `tenantId`
- → `ADM-529` AI Human Oversight Command Center: *AI Human Oversight Command Center*; carries `planId`, `tenantId`
- → `ADM-539` AI Explainability & Audit Command Center: *AI Explainability & Audit Command Center*; carries `tenantId`
- → `ADM-549` AI Governance Monitoring Command Center: *AI Governance Monitoring Command Center*; carries `tenantId`
- → `ADM-619` Reconciliation & Settlement Command Center: *Reconciliation & Settlement Command Center\t139*; carries `tenantId`
- → `ADM-009` Tenant Billing & Invoicing: *Tenant Billing & Invoicing*; carries `tenantId`
- → `ADM-010` Usage Metering: *Usage Metering*; carries `tenantId`
- → `ADM-011` Licence & Seat Management: *Licence & Seat Management*; carries `tenantId`
- → `ADM-013` Tenant Performance Monitor: *Tenant Performance Monitor*; carries `cellId`
- → `ADM-014` Auto-Scaling Configuration: *Auto-Scaling Configuration*; carries `cellId`
- → `ADM-015` API Rate Limit & Quota Management: *API Rate Limit & Quota Management*; carries `tenantId`
- → `ADM-016` White-Label Branding Management: *White-Label Branding Management*; carries `tenantId`
- → `ADM-017` Domain & Certificate Management: *Domain & Certificate Management*; carries `tenantId`
- → `ADM-018` Interface Languages: *Localisation & Language Pack*; carries `tenantId`
- → `ADM-019` Global Configuration & Defaults: *Global Configuration & Defaults*; carries `tenantId`
- → `ADM-022` Release & Version Management: *Release & Version Management*
- → `ADM-023` Staging Promotion & Approval: *Staging Promotion & Approval*
- → `ADM-026` End-of-Support Notice Management: *End-of-Support Notice Management*; carries `tenantId`
- → `ADM-027` Database Migration Console: *Database Migration Console*
- → `ADM-029` Deployment Monitor: *Deployment Monitor*; carries `cellId`
- → `ADM-030` Infrastructure Sizing & Scaling Policy: *Infrastructure Sizing & Scaling Policy*; carries `cellId`
- → `ADM-031` Security & Compliance Dashboard: *Security & Compliance Dashboard*; carries `tenantId`
- → `ADM-032` WAF & Security Policy View: *WAF & Security Policy View*
- → `ADM-033` Backup & DR Status: *Backup & DR Status*; carries `cellId`
- → `ADM-034` Archival Job Monitor: *Archival Job Monitor*
- → `ADM-037` AI Provider & Credentials: *AI Provider & Credentials*; carries `regionId`
- → `ADM-318` Dead Letters: *Dead Letters*
- → `ADM-024` Release Notification Composer: *Release Notification Composer*
- → `ADM-025` Tenant Upgrade Scheduler: *Tenant Upgrade Scheduler*
- → `ADM-028` Environment Registry: *Environment Registry*
- → `ADM-035` Support & Escalation Console: *Support & Escalation Console*
- → `ADM-036` Platform Notification Broadcast: *Platform Notification Broadcast*
- → `ADM-068` Tax, Fee & Calculation Command Center: *Tax, Fee & Calculation Command Center*; carries `tenantId`
- → `ADM-699` My Account & Security: *My account & security*
- → `ADM-020` Platform User Directory: *Creates the first principal and grants it the role*; carries `tenantId`; calls `listTenants`
- → `ADM-021` Platform Role Management: *Defines the role the first administrator will hold*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The platform list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the platform untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No platform yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, planId and the platform are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  activeTenants: 38
  suspended: 2
  cellsUnreachable: 1
  overLicence: 3
  myOpenGrants: 1
```

#### Permissions

- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getEntitlementUsage` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenant` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenantLicences` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listTenantCells` → `PLATFORM_CELL_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.5.1 | License Generation - System shall generate subscription licenses. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.2 | License Assignment - System shall assign licenses to tenants. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.3 | License Validation - System shall validate licenses automatically. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.4 | License Enforcement - System shall enforce licensing restrictions. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.5 | License Expiration - System shall support license expiration management. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.6 | Grace Period Management - System shall support configurable grace periods. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.7 | License Renewal Management - System shall support license renewals. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.8 | License Audit Logs - System shall maintain license audit logs. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-002` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Dashboards Board.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Dashboards Board.dc.html`
- Client design-board frames: `Dashboards Board.dc.html#adm-002`
- Flow F109 *A tenant gets its first administrator*, step 2: Opens the console and picks the tenant → The tenant exists, is licensed, and has no principals
- Flow F109 *A tenant gets its first administrator*, step 4: Returns to the console → Role defined, no one holding it
- ADR-0014 *Cell Per Region* (`docs/adr/0014-cell-per-region.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (33 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-001`, `ADM-003`, `ADM-004`, `ADM-005`, `ADM-006`, `ADM-007`, `ADM-008`, `ADM-012`, `ADM-369`, `ADM-459`, `ADM-379`, `ADM-389`, `ADM-399`, `ADM-409`, `ADM-419`, `ADM-449`, `ADM-469`, `ADM-479`, `ADM-489`, `ADM-499`, `ADM-509`, `ADM-519`, `ADM-529`, `ADM-539`, `ADM-549`, `ADM-619`, `ADM-009`, `ADM-010`, `ADM-011`, `ADM-013`, `ADM-014`, `ADM-015`, `ADM-016`, `ADM-017`, `ADM-018`, `ADM-019`, `ADM-022`, `ADM-023`, `ADM-026`, `ADM-027`, `ADM-029`, `ADM-030`, `ADM-031`, `ADM-032`, `ADM-033`, `ADM-034`, `ADM-037`, `ADM-318`, `ADM-024`, `ADM-025`, `ADM-028`, `ADM-035`, `ADM-036`, `ADM-068`, `ADM-699`, `ADM-020`, `ADM-021`.
- [ ] Every gated control is gated: `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-003` Cross-Tenant Health Dashboard

**See the health of every cell across tenants, and act on a failing one.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Overview & Health · wave 1 · needs the `core` module |
| Block | Block A · task APP-CONSOLE-ADM-003 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_MANAGE`, `PLATFORM_CELL_VIEW` (1 configure, 1 read); in the flows as guest |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getCellHealth` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/cross-tenant-health-dashboard` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-platform navigation removed 24 August**: SCN-003. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Drawn 26 August** — `Dashboards Board` frame `adm-003`. **One board draws five dashboards across five platforms** — platform admin, partner, support, guest web and cross-tenant health. A dashboard is a shape rather than a domain, and the pack recognised that before the package did.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): propagateCrossRegionEntitlement and reconcileRedemptions are service-audience calls between cells (F19) that no operator makes, and getCrossRegionEntitlement … Removed 2 October 2026 (CHG-WIR-021): propagateCrossRegionEntitlement and reconcileRedemptions are service-audience calls between cells (F19) that no operator makes, and getCrossRegionEntitlement … Removed 2 October 2026 (CHG-WIR-021): propagateCrossRegionEntitlement and reconcileRedemptions are service-audience calls between cells (F19) that no operator makes, and getCrossRegionEntitlement …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** For a TICVAI platform operator: the health of every cell (one tenant in one jurisdiction) — reachability, schema lag, replication lag, backups and restore drills, capacity against headroom — with the jobs running in each, and the tier and decommission controls. The rule: health is per cell, so a tenant in two regions appears twice.

**Fixed on main** (the package already carries these; draw what it says): Purpose says "The screen this app sits on. Everything else is entered from here". (CHG-WIR-023); Propagate cross region entitlement and Reconcile redemptions are buttons with forms. (CHG-WIR-021); getCrossRegionEntitlement, getWalletAllocation and setWalletAllocationPolicy (tenant permissions TICKET_LOOKUP, ORDER_VIEW … (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every cell job' drop id. (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Window | radio group | Day | Hour · Day · Week · Month | `getCellCapacity` ?window |

**Form: Decommission cell** (modal, opened by *Decommission cell*; *Decommission cell* calls `decommissionCell`, *Cancel* sends nothing)

**Collects what `decommissionCell` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `decommissionCell` body |

Errors to draw in the form: 409 Not in a state that permits this

**Form: Save cell tier** (modal, opened by *Save cell tier*; *Save cell tier* calls `updateCellTier`, *Cancel* sends nothing)

**Collects what `updateCellTier` sends before it is called.** Required: `tier`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tier `tier` | radio group | required | — | Shared · Dedicated · Isolated · Client hosted | — | — | `updateCellTier` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateCellTier` body |

Errors to draw in the form: 400 Target tier is unavailable in this jurisdiction

**Sent by *Cancel decommission*** (`cancelDecommission`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `cancelDecommission` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setWalletAllocationPolicy: set per region (money, tax, ledger); venues inherit and cannot override. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/cross-region.yaml#setWalletAllocationPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Every cell job** (data table, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Provision, Tier migration, Schema migration, Backup, Restore, Decommission | — |
| Status | chip: Queued, Running, Completed, Failed, Rolled back | — |
| Progress percent | 1,234 | — |
| Message | text | — |
| Error | text | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**The selected cell job** (detail panel, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Provision, Tier migration, Schema migration, Backup, Restore, Decommission | — |
| Status | chip: Queued, Running, Completed, Failed, Rolled back | — |
| Progress percent | 1,234 | — |
| Message | text | — |
| Error | text | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**The cell** (detail panel, from `getCell`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Last contact at | 1 Oct 2026, 14:30 | When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first. |
| Licence expires at | 1 Oct 2026, 14:30 | On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. |
| Region name | text | — |
| Country code | text | — |
| Tier | chip: Shared, Dedicated, Isolated, Client hosted | — |
| Status | chip: Provisioning, Active, Migrating, Suspended, Decommissioning, Failed | — |

**The cell capacity** (detail panel, from `getCellCapacity`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Tenant count | 1,234 | Reported, and deliberately not the sizing signal. Forty quiet tenants may load a cell less than three busy ones. |
| Is constrained | yes / no (icon or chip) | — |
| Constrained dimension | text | — |
| Dimensions | list or chips (count when long) | Per dimension, because the response differs. Short of connections and long on storage is a different problem from short of both. |
| Forecast breach at | 1 Oct 2026, 14:30 | When the constrained dimension is projected to run out at the current trend. Null where there is no trend to project — an honest null beats … |
| Measured at | 1 Oct 2026, 14:30 | — |

**The cell health** (detail panel, from `getCellHealth`)

| Shows | Format | Notes |
|---|---|---|
| Is healthy | yes / no (icon or chip) | — |
| Is schema behind | yes / no (icon or chip) | — |
| Database status | text | — |
| Replication lag seconds | 1,234.5 | — |
| Last backup at | 1 Oct 2026, 14:30 | — |
| Last restore drill at | 1 Oct 2026, 14:30 | — |
| Checked at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cancel decommission (destructive button) | `cancelDecommission` POST `/cells/{cellId}/cancel-decommission` | inline | no body | 409 Not in a state that permits this | — |
| Decommission cell (secondary button) | `decommissionCell` POST `/cells/{cellId}/decommission` | inline | no body | 409 Not in a state that permits this | opens modal first |
| Save cell tier (secondary button) | `updateCellTier` PATCH `/cells/{cellId}` | inline | CellJob | 400 Target tier is unavailable in this jurisdiction | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Cell list**: Tenant name, region and country, tier, status, reachable or last contact, schema behind (yes/no), replication lag in seconds, last backup and last restore drill (older than 30 days amber), constrained dimension and forecast breach date. Times in the operator's time zone with the zone named. *(source: contracts/satellite/subscription.yaml#getCellHealth; contracts/satellite/subscription.yaml#getCellCapacity; ADR-0060)*
- **Jobs**: Provisioning, migration and maintenance jobs with progress percent, message and error, newest first. *(source: contracts/satellite/subscription.yaml#listCellJobs)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Decommission cell**: Confirmation names the tenant, region and what stops ("Marina Leisure Group's Oman cell stops serving AquaCove Muscat"); requires a reason; Cancel decommission halts it while it runs. *(source: contracts/satellite/subscription.yaml#decommissionCell; contracts/satellite/subscription.yaml#cancelDecommission)*
- **Change tier**: Tier with an optional scheduled time; the change is a job, shown in the jobs list. *(source: contracts/satellite/subscription.yaml#updateCellTier)*

**Data it reads**: `getCellHealth` (onLoad, from page inventory); `getCell` (onLoad, Read a cell); `getCellCapacity` (onLoad, Load against headroom); `listCellJobs` (onLoad, Provisioning, migration and maintenance jobs)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-004` Platform Audit Log: *Platform Audit Log*
- → `SCN-003` Ready to scan: *Guest scans at the other venue*

**What opens over it**

- confirmDialog *Cancel decommission*: **Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A cross-tenant health this affects should be identified in the dialog, not just counted. **Collects what `cancelDecommission` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cross-tenant health list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cross-tenant health untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cross-tenant health yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellHealth` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_CELL_MANAGE` for `cancelDecommission`, `decommissionCell`, `updateCellTier`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Target tier is unavailable in this jurisdiction; 409 Not in a state that permits this |

#### Edge cases to draw

- **Can read but not change (holds ORDER_VIEW, PLATFORM_CELL_VIEW, TICKET_LOOKUP only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_CELL_MANAGE for Cancel decommission, Decommission cell, Save cell tier; REGION_CONFIGURE for setWalletAllocationPolicy. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **cancelDecommission answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **decommissionCell answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#decommissionCell)*
- **propagateCrossRegionEntitlement answers 409**: Show it as something the person can act on, not a failure: Right already propagated. Idempotent — returns the existing right. *(source: contracts/spine/cross-region.yaml#propagateCrossRegionEntitlement)*

#### Consistency with other screens

- Match `ADM-002`: The Platform Dashboard is the home; this is the cell health drill-down from it.
- Match `ADM-005`: The tenant's cells shown there link here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cells:
- tenant: Marina Leisure Group
  region: UAE
  tier: dedicated
  reachable: true
  schemaBehind: false
  replicationLag: 0.4 s
  lastBackup: 01/10/2026 03:00
  lastRestoreDrill: 14/09/2026
- tenant: Marina Leisure Group
  region: Oman
  tier: shared
  reachable: false
  lastContact: 01/10/2026 08:51
  schemaBehind: true
```

#### Permissions

- `getCellHealth` → `PLATFORM_CELL_VIEW` (read) · staff
- `cancelDecommission` → `PLATFORM_CELL_MANAGE` (configure) · staff
- `decommissionCell` → `PLATFORM_CELL_MANAGE` (configure) · staff
- `getCell` → `PLATFORM_CELL_VIEW` (read) · staff
- `getCellCapacity` → `PLATFORM_CELL_VIEW` (read) · staff
- `listCellJobs` → `PLATFORM_CELL_VIEW` (read) · staff
- `updateCellTier` → `PLATFORM_CELL_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellHealth` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_CELL_MANAGE` for `cancelDecommission`, `decommissionCell`, `updateCellTier`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-003` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Dashboards Board.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Dashboards Board.dc.html`
- Client design-board frames: `Dashboards Board.dc.html#adm-003`
- Flow F19 *A membership works in another country*, step 2: The right is propagated to the other cell → A copy of the entitlement to redeem against, not the entitlement itself
- Flow F19 *A membership works in another country*, step 5: Reconciliation confirms it → Or names the difference
- Flow F19 branch at step 2 (recoverable): when The target cell is unreachable when the right is propagated, Queued and retried. **The guest may arrive before it lands**, which is why propagation happens at purchase rather than at travel.
- Flow F19 branch at step 5 (requiresStaff): when The two cells disagree on the remaining entitlement, **The owning cell wins.** The pass was sold somewhere, and that cell holds the truth — a copy that drifts is reconciled to the original, never the other way.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (37 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cancel decommission, Decommission cell, Save cell tier.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-004`, `SCN-003`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`, `PLATFORM_CELL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-004` Platform Audit Log

**Find platform audit log for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Overview & Health · wave 2 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-004 |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW`, `AUDIT_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (3 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAiInteractions` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `decisionRecordId` (navigation), `tenantId` (navigation) |
| Route | `/general/platform-audit-log` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listAiInteractions` (AI_AUDIT_VIEW), `getAiDecisionTrace` (AI_AUDIT_VIEW), `listAuditRecords` (AUDIT_VIEW) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.**  Open: No contract — Control Plane audit not specified

**From the AI & Intelligence process.** The AI interaction log: every prompt, response and action, who asked, for which tenant it was billed, which capability, the outcome and any refusal reason. The one thing to get right: prompt and response text are personal data - shown only to AI_AUDIT_VIEW holders, with masked fields shown as masked, and the screen states the retention period for prompts (90 days by default).

**Fixed on main** (the package already carries these; draw what it says): purpose "Find platform audit log for this venue" and name "Platform Audit Log", while the screen lists AI interactions only. (CHG-WIR-012).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listAiInteractions`. | `listAiInteractions` ?principalId |
| Outcome | radio group | optional | — | Answered · Refused · Applied · Rejected · Failed | — | Sends `?outcome=` to `listAiInteractions`. | `listAiInteractions` ?outcome |
| From | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?from=` to `listAiInteractions`. | `listAiInteractions` ?from |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Org unit | picker: choose an org unit | — | — | `listAuditRecords` ?orgUnitId |
| Principal | picker: choose a principal | — | — | `listAuditRecords` ?principalId |
| Workstation | picker: choose a workstation | — | — | `listAuditRecords` ?workstationId |
| Action | text field | — | — | `listAuditRecords` ?action |
| Subject ref | text field | — | — | `listAuditRecords` ?subjectRef |
| Platform staff grant | picker: choose a platform staff grant | — | — | `listAuditRecords` ?platformStaffGrantId |
| From | date and time picker | — | — | `listAuditRecords` ?from |
| To | date and time picker | — | — | `listAuditRecords` ?to |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_AUDIT_VIEW`, `AUDIT_VIEW` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

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

**Every AI interaction** (data table, from `listAiInteractions`)

| Shows | Format | Notes |
|---|---|---|
| Audience | chip: Staff, Guest | Billing divides on this. Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop … |
| Capability | text | — |
| Prompt | text | — |
| Response | text | — |
| Outcome | chip: Answered, Refused, Applied, Rejected, Failed | — |

**Platform audit log** (data table, from `listAuditRecords`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | Who acted. |
| Org unit | the name it points at, never the id | The scope node the action happened in. |
| Workstation | the name it points at, never the id | The workstation it was done from, where there was one. |
| Action | text | What was done, as the writing operation names it. |
| Subject ref | text | The thing acted on — a profile, a shift, an order. The same value the `subjectRef` filter matches. |
| Occurred at | 1 Oct 2026, 14:30 | When. The list is ordered by this, most recent first. |
| Platform staff grant | the name it points at, never the id | Set when a TICVAI platform operator acted, naming the grant they acted under (`identity.openPlatformStaffGrant`; decided 28 September … |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**The selected AI interaction** (detail panel, from `listAiInteractions`)

| Shows | Format | Notes |
|---|---|---|
| Audience | chip: Staff, Guest | Billing divides on this. Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop … |
| Capability | text | — |
| Prompt | text | — |
| Response | text | — |
| Sources | list or chips (count when long) | The sources an answer was grounded in, stored with the answer (8.3.70). One `jsonb` column on the row that carries it — … |
| Outcome | chip: Answered, Refused, Applied, Rejected, Failed | — |
| Refusal reason | text | — |
| Provider | chip: Openai, Gemini, Anthropic, Azure openai, Local llm, Openai compatible | `openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **interaction rows**: Time, principal, audience (staff/guest), capability, outcome, provider and model, tokens and cost; prompt and response in the detail panel only. *(source: contracts/satellite/ai.yaml#listAiInteractions / ADR-0020)*
- **retention line**: "Prompts are kept for 90 days (your setting), then deleted." *(source: contracts/spine/tenancy.yaml#setDataRetentionSetting / ADR-0020 (AI-D05))*

**Data it reads**: `listAiInteractions` (onLoad, Every prompt, response and action); `listAuditRecords` (onLoad, Who did what, where, and when); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*
- → `BO-068` Audit Log: *Audit Log*; calls `listAiInteractions`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The platform audit log list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the platform audit log untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No platform audit log yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on principalId, outcome, from and the platform audit log are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_AUDIT_VIEW`, which `listAiInteractions` requires to show this screen, and names that permission (the screen's other reads need `AUDIT_VIEW`, `PLATFORM_TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_ACCESS` for … |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_AUDIT_VIEW`, `AUDIT_VIEW`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  when: 1 Oct 14:02
  principal: guest (anonymous)
  capability: assistant.guest
  outcome: answered
  model: gpt-4o-mini
  tokens: 812
  cost: AED 0.004
```

#### Permissions

- `listAiInteractions` → `AI_AUDIT_VIEW` (read) · staff
- `getAiDecisionTrace` → `AI_AUDIT_VIEW` (read) · staff
- `listAuditRecords` → `AUDIT_VIEW` (read) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Shown when the caller lacks `AI_AUDIT_VIEW`, which `listAiInteractions` requires to show this screen, and names that permission (the screen's other reads need `AUDIT_VIEW`, `PLATFORM_TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_ACCESS` for …

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.2 | Prompt Logging System shall store prompts submitted to AI services. | Unified Operations Dashboard | CONTRACTED | `listAiInteractions` |
| 8.1.3 | Response Logging System shall store AI-generated responses. | Unified Operations Dashboard | CONTRACTED | `listAiInteractions` |
| 8.1.6 | AI Audit Trail System shall maintain a history of AI-generated actions and user decisions. | Unified Operations Dashboard | CONTRACTED | `listAiInteractions` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-004` · status **notStarted** · provenance generated
- Flow F100 *An AI provider is configured, budgeted and audited*, step 3: Platform Audit Log. → 1 operations, 1 of them previously unwalked.
- Flow F106 *A security dashboard surfaces something and it is investigated*, step 2: Platform Audit Log. → 1 operations, 1 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-004?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `BO-068`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `AUDIT_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-013` Tenant Performance Monitor

**Watch how each tenant's cells perform against their capacity.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Overview & Health · wave 2 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-013 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getCellHealth` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/tenant-performance-monitor` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Six screens offered Decommission cell, six places to make the worst mistake; decommission stays on ADM-003 only, and a performance monitor does not change a … Removed 2 October 2026 (CHG-WIR-021): Six screens offered Decommission cell, six places to make the worst mistake; decommission stays on ADM-003 only, and a performance monitor does not change a … Removed 2 October 2026 (CHG-WIR-021): Six screens offered Decommission cell, six places to make the worst mistake; decommission stays on ADM-003 only, and a performance monitor does not change a …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Performance of a tenant's cells: health, capacity, jobs.

**Fixed on main** (the package already carries these; draw what it says): Carries the same seven cell operations as ADM-014, ADM-030, ADM-032, ADM-033, ADM-034 and ADM-003, including Decommission cell. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every cell job' drop id. (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Window | radio group | Day | Hour · Day · Week · Month | `getCellCapacity` ?window |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every cell job** (data table, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Provision, Tier migration, Schema migration, Backup, Restore, Decommission | — |
| Status | chip: Queued, Running, Completed, Failed, Rolled back | — |
| Progress percent | 1,234 | — |
| Message | text | — |
| Error | text | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**The selected cell job** (detail panel, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Provision, Tier migration, Schema migration, Backup, Restore, Decommission | — |
| Status | chip: Queued, Running, Completed, Failed, Rolled back | — |
| Progress percent | 1,234 | — |
| Message | text | — |
| Error | text | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**The cell** (detail panel, from `getCell`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Last contact at | 1 Oct 2026, 14:30 | When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first. |
| Licence expires at | 1 Oct 2026, 14:30 | On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. |
| Region name | text | — |
| Country code | text | — |
| Tier | chip: Shared, Dedicated, Isolated, Client hosted | — |
| Status | chip: Provisioning, Active, Migrating, Suspended, Decommissioning, Failed | — |

**The cell capacity** (detail panel, from `getCellCapacity`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Tenant count | 1,234 | Reported, and deliberately not the sizing signal. Forty quiet tenants may load a cell less than three busy ones. |
| Is constrained | yes / no (icon or chip) | — |
| Constrained dimension | text | — |
| Dimensions | list or chips (count when long) | Per dimension, because the response differs. Short of connections and long on storage is a different problem from short of both. |
| Forecast breach at | 1 Oct 2026, 14:30 | When the constrained dimension is projected to run out at the current trend. Null where there is no trend to project — an honest null beats … |
| Measured at | 1 Oct 2026, 14:30 | — |

**The cell health** (detail panel, from `getCellHealth`)

| Shows | Format | Notes |
|---|---|---|
| Is healthy | yes / no (icon or chip) | — |
| Is schema behind | yes / no (icon or chip) | — |
| Database status | text | — |
| Replication lag seconds | 1,234.5 | — |
| Last backup at | 1 Oct 2026, 14:30 | — |
| Last restore drill at | 1 Oct 2026, 14:30 | — |
| Checked at | 1 Oct 2026, 14:30 | — |

**Data it reads**: `getCellHealth` (onLoad, from page inventory); `getCell` (onLoad, Read a cell); `getCellCapacity` (onLoad, Load against headroom); `listCellJobs` (onLoad, Provisioning, migration and maintenance jobs)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`
- → `ADM-014` Auto-Scaling Configuration: *Auto-Scaling Configuration*; carries `cellId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tenant performance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tenant performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tenant performance yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_CELL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_CELL_MANAGE for Cancel decommission, Decommission cell, Save cell tier. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **cancelDecommission answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **decommissionCell answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#decommissionCell)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every cell job:
- kind: standard
  status: active
  progressPercent: 12.5
  scheduledFor: 31/12/2026 23:59
  completedAt: 01/10/2026 09:14
- kind: standard
  status: pending
  progressPercent: 8.0
  scheduledFor: 15/10/2026 00:00
  completedAt: 30/09/2026 18:02
- kind: override
  status: suspended
  progressPercent: 15.0
  scheduledFor: 01/11/2026 06:00
  completedAt: 28/09/2026 11:45
```

#### Permissions

- `getCellHealth` → `PLATFORM_CELL_VIEW` (read) · staff
- `getCell` → `PLATFORM_CELL_VIEW` (read) · staff
- `getCellCapacity` → `PLATFORM_CELL_VIEW` (read) · staff
- `listCellJobs` → `PLATFORM_CELL_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-013` · status **notStarted** · provenance generated
- Flow F97 *A cell is capacity-checked and a tenant is placed on it*, step 2: Tenant Performance Monitor. → 7 operations, 7 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (37 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-013?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `ADM-014`.
- [ ] Every gated control is gated: `PLATFORM_CELL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-029` Deployment Monitor

**Watch each rollout cell by cell, and pause or roll it back.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Overview & Health · wave 2 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-029 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_VIEW`, `PLATFORM_RELEASE_PROMOTE`, `PLATFORM_RELEASE_VIEW` (2 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getRollout` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink), `rolloutId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/deployment-monitor` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Decommission cell and Save cell tier on a deployment monitor were copied cell actions; decommission stays on ADM-003 only (design-notes corrections … Removed 2 October 2026 (CHG-WIR-021): Decommission cell and Save cell tier on a deployment monitor were copied cell actions; decommission stays on ADM-003 only (design-notes corrections … Removed 2 October 2026 (CHG-WIR-021): Decommission cell and Save cell tier on a deployment monitor were copied cell actions; decommission stays on ADM-003 only (design-notes corrections …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Release rollouts across cells: progress, failed cells, pause and rollback.

**Fixed on main** (the package already carries these; draw what it says): Decommission cell and Save cell tier on a deployment monitor. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every cell job' drop id; 'Every rollout' drop id, releaseId, startedByPrincipalId … (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Queued · Canary · Rolling · Paused · Complete · Failed · Rolled back | `listRollouts` ?status |
| Window | radio group | Day | Hour · Day · Week · Month | `getCellCapacity` ?window |

**Form: Pause rollout** (modal, opened by *Pause rollout*; *Pause rollout* calls `pauseRollout`, *Cancel* sends nothing)

**Collects what `pauseRollout` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `pauseRollout` body |

**Form: Rollback rollout** (modal, opened by *Rollback rollout*; *Rollback rollout* calls `rollbackRollout`, *Cancel* sends nothing)

**Collects what `rollbackRollout` sends before it is called.** Required: `reason`, `stepUpToken`. Optional: `cellIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `rollbackRollout` body |
| Step up token `stepUpToken` | text field | required | — | — | — | — | `rollbackRollout` body |
| Cells `cellIds` | multi-picker: choose cells | optional | — | — | — | Omit to roll back every cell in the rollout. | `rollbackRollout` body |

Errors to draw in the form: 409 A migration in this release is irreversible. The response names it — a one-way door should be identified, not discovered. (IrreversibleProblem)

**Form: Start rollout** (modal, opened by *Start rollout*; *Start rollout* calls `startRollout`, *Cancel* sends nothing)

**Collects what `startRollout` sends before it is called.** Required: `stage`. **Sending it asks for approval, it does not promote** (decided 28 September, audit R144): the answer is 202 with a pending `releasePromotion` request, routed to a holder of `PLATFORM_RELEASE_PROMOTE` other than the requester — nobody approves their own promotion. The rollout moves to the stage when that request is approved. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Stage `stage` | segmented control | required | — | Canary · Partial · Full | — | The stage to take the rollout to (decided 28 September, audit R096). `canary` is the first cell only; `partial` is a wave of the remaining cells, and may be sent again to continue … | `startRollout` body |

Errors to draw in the form: 409 Not in a state that permits this

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **stepUpToken**: Never a visible field. It is what verifyMfaChallenge returns after the in-place challenge, short-lived and single-purpose; the form shows the challenge step, not a token box. *(source: contracts/spine/identity.yaml#verifyMfaChallenge)*

#### Outputs: what the screen shows and produces

**Shown**

**Every cell job** (data table, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Provision, Tier migration, Schema migration, Backup, Restore, Decommission | — |
| Status | chip: Queued, Running, Completed, Failed, Rolled back | — |
| Progress percent | 1,234 | — |
| Message | text | — |
| Error | text | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**Every rollout** (data table, from `listRollouts`)

| Shows | Format | Notes |
|---|---|---|
| Environment | chip: Dev, Staging, Production | — |
| Status | chip: Queued, Canary, Rolling, Paused, Complete, Failed… | — |
| Cells total | 1,234 | — |
| Cells complete | 1,234 | — |
| Cells failed | 1,234 | — |
| Paused reason | text | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**The selected cell job** (detail panel, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Provision, Tier migration, Schema migration, Backup, Restore, Decommission | — |
| Status | chip: Queued, Running, Completed, Failed, Rolled back | — |
| Progress percent | 1,234 | — |
| Message | text | — |
| Error | text | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**The cell** (detail panel, from `getCell`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Last contact at | 1 Oct 2026, 14:30 | When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first. |
| Licence expires at | 1 Oct 2026, 14:30 | On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. |
| Region name | text | — |
| Country code | text | — |
| Tier | chip: Shared, Dedicated, Isolated, Client hosted | — |
| Status | chip: Provisioning, Active, Migrating, Suspended, Decommissioning, Failed | — |

**The cell capacity** (detail panel, from `getCellCapacity`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Tenant count | 1,234 | Reported, and deliberately not the sizing signal. Forty quiet tenants may load a cell less than three busy ones. |
| Is constrained | yes / no (icon or chip) | — |
| Constrained dimension | text | — |
| Dimensions | list or chips (count when long) | Per dimension, because the response differs. Short of connections and long on storage is a different problem from short of both. |
| Forecast breach at | 1 Oct 2026, 14:30 | When the constrained dimension is projected to run out at the current trend. Null where there is no trend to project — an honest null beats … |
| Measured at | 1 Oct 2026, 14:30 | — |

**The cell health** (detail panel, from `getCellHealth`)

| Shows | Format | Notes |
|---|---|---|
| Is healthy | yes / no (icon or chip) | — |
| Is schema behind | yes / no (icon or chip) | — |
| Database status | text | — |
| Replication lag seconds | 1,234.5 | — |
| Last backup at | 1 Oct 2026, 14:30 | — |
| Last restore drill at | 1 Oct 2026, 14:30 | — |
| Checked at | 1 Oct 2026, 14:30 | — |

**The rollout** (detail panel, from `getRollout`)

| Shows | Format | Notes |
|---|---|---|
| Environment | chip: Dev, Staging, Production | — |
| Status | chip: Queued, Canary, Rolling, Paused, Complete, Failed… | — |
| Cells total | 1,234 | — |
| Cells complete | 1,234 | — |
| Cells failed | 1,234 | — |
| Paused reason | text | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Pause rollout (primary button) | `pauseRollout` POST `/rollouts/{rolloutId}/pause` | inline | RolloutDetail | — | opens modal first |
| Rollback rollout (secondary button) | `rollbackRollout` POST `/rollouts/{rolloutId}/rollback` | inline | RolloutDetail | 409 A migration in this release is irreversible. The response names it — a one-way door should be identified, not discovered. (IrreversibleProblem) | opens modal first |
| Start rollout (secondary button) | `startRollout` POST `/rollouts/{rolloutId}/start` | inline | no body | 409 Not in a state that permits this | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (cellsTotal)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Rollback rollout**: Confirmation names the release and the cells it reverts; reason required. *(source: contracts/satellite/platform-ops.yaml#rollbackRollout)*

**Data it reads**: `listCellJobs` (onLoad, from page inventory); `listRollouts` (onLoad, Rollouts in flight); `getCell` (onLoad, Read a cell); `getCellCapacity` (onLoad, Load against headroom); `getCellHealth` (onLoad, Cell health and schema version)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The deployment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deployment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No deployment yet. Offers Start rollout (`startRollout`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `listCellJobs` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_RELEASE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_PROMOTE` for `pauseRollout` … |
| Rollout pending approval (`?state=rolloutPendingApproval`) | **Requested, not moved.** `startRollout` answered 202: the rollout shows the stage it has reached, the stage requested and that a `releasePromotion` approval is pending with the platform release manager. The requester sees no approve action for their own request (decided 28 September, audit R144). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A migration in this release is irreversible. The response names it — a one-way door should be identified, not discovered. (IrreversibleProblem); 409 Not in a state that permits this |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_CELL_VIEW, PLATFORM_RELEASE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_RELEASE_PROMOTE for Pause rollout, Rollback rollout, Start rollout; PLATFORM_CELL_MANAGE for Cancel decommission, Decommission cell, Save cell tier. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/platform-ops.yaml#pauseRollout)*
- **rollbackRollout answers 409**: Show it as something the person can act on, not a failure: A migration in this release is irreversible. The response names it — a one-way door should be identified, not discovered. *(source: contracts/satellite/platform-ops.yaml#rollbackRollout)*
- **cancelDecommission answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **decommissionCell answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#decommissionCell)*
- **startRollout answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/platform-ops.yaml#startRollout)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every cell job:
- kind: standard
  status: active
  progressPercent: 12.5
  scheduledFor: 31/12/2026 23:59
  completedAt: 01/10/2026 09:14
- kind: standard
  status: pending
  progressPercent: 8.0
  scheduledFor: 15/10/2026 00:00
  completedAt: 30/09/2026 18:02
- kind: override
  status: suspended
  progressPercent: 15.0
  scheduledFor: 01/11/2026 06:00
  completedAt: 28/09/2026 11:45
```

#### Permissions

- `listCellJobs` → `PLATFORM_CELL_VIEW` (read) · staff
- `listRollouts` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `getRollout` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `pauseRollout` → `PLATFORM_RELEASE_PROMOTE` (operate) · staff
- `rollbackRollout` → `PLATFORM_RELEASE_PROMOTE` (operate) · staff
- `getCell` → `PLATFORM_CELL_VIEW` (read) · staff
- `getCellCapacity` → `PLATFORM_CELL_VIEW` (read) · staff
- `getCellHealth` → `PLATFORM_CELL_VIEW` (read) · staff
- `startRollout` → `PLATFORM_RELEASE_PROMOTE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `listCellJobs` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_RELEASE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_PROMOTE` for `pauseRollout` …

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-029` · status **notStarted** · provenance generated
- Flow F04 *Platform admin ships a release*, step 4: Watches the rollout per cell → Canary first, then waves. Per-cell state, because a percentage says nothing useful
- Flow F04 branch at step 4 (requiresStaff): when The canary cell fails, The wave halts rather than continuing into it. Cells already updated stay updated — pause is not rollback, and the console keeps the distinction visible.
- ADR-0001 *Cell architecture — one tenant per jurisdiction* (`docs/adr/0001-cell-architecture-one-tenant-per-jurisdiction.md`)
- ADR-0014 *Cell Per Region* (`docs/adr/0014-cell-per-region.md`)
- ADR-0017 *— Deployment models* (`docs/adr/0017-deployment-models.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (53 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-029?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, rolloutPendingApproval, offline.
- [ ] Every action is wired with its success and its failure: Pause rollout, Rollback rollout, Start rollout.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `PLATFORM_CELL_VIEW`, `PLATFORM_RELEASE_PROMOTE`, `PLATFORM_RELEASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 5 edge case(s) from the process notes are drawn.
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

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cancelDecommission": {"method":"POST","path":"/cells/{cellId}/cancel-decommission","contract":"subscription","summary":"Halt a decommission","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"decommissionCell": {"method":"POST","path":"/cells/{cellId}/decommission","contract":"subscription","summary":"Begin decommissioning a cell","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getAiDecisionTrace": {"method":"GET","path":"/decision-records/{decisionRecordId}/trace","contract":"ai","summary":"The full trace of a decision","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"depth","in":"query","required":null}],"requestBody":null,"responds":"AiDecisionTrace"},
"getCell": {"method":"GET","path":"/cells/{cellId}","contract":"subscription","summary":"Read a cell","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"CellDetail"},
"getCellCapacity": {"method":"GET","path":"/cells/{cellId}/capacity","contract":"subscription","summary":"Load against headroom","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"window","in":"query","required":null}],"requestBody":null,"responds":"CellCapacity"},
"getCellHealth": {"method":"GET","path":"/cells/{cellId}/health","contract":"subscription","summary":"Cell health and schema version","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"CellHealth"},
"getEntitlementUsage": {"method":"GET","path":"/tenants/{tenantId}/entitlement-usage","contract":"subscription","summary":"Usage against licensed limits","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"EntitlementUsage"},
"getRollout": {"method":"GET","path":"/rollouts/{rolloutId}","contract":"platform-ops","summary":"Rollout progress per cell","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"RolloutDetail"},
"getTenant": {"method":"GET","path":"/tenants/{tenantId}","contract":"subscription","summary":"Read a tenant with cells and subscription","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantDetail"},
"getTenantLicences": {"method":"GET","path":"/tenants/{tenantId}/licences","contract":"subscription","summary":"What a tenant is licensed to use","permission":"PLATFORM_TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"LicencePosition"},
"listAiInteractions": {"method":"GET","path":"/interactions","contract":"ai","summary":"Every prompt, response and action","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"principalId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAuditRecords": {"method":"GET","path":"/audit-records","contract":"tenancy","summary":"Who did what, where, and when","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"orgUnitId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"action","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"platformStaffGrantId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCellJobs": {"method":"GET","path":"/cells/{cellId}/jobs","contract":"subscription","summary":"Provisioning, migration and maintenance jobs","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOwnPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants/mine","contract":"identity","summary":"The calling platform operator's own grants into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRollouts": {"method":"GET","path":"/rollouts","contract":"platform-ops","summary":"List rollouts","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTenantCells": {"method":"GET","path":"/tenants/{tenantId}/cells","contract":"subscription","summary":"List a tenant's cells","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"Cell"},
"listTenants": {"method":"GET","path":"/tenants","contract":"subscription","summary":"List tenants","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"planId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"pauseRollout": {"method":"POST","path":"/rollouts/{rolloutId}/pause","contract":"platform-ops","summary":"Halt a rollout in progress","permission":"PLATFORM_RELEASE_PROMOTE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RolloutDetail"},
"rollbackRollout": {"method":"POST","path":"/rollouts/{rolloutId}/rollback","contract":"platform-ops","summary":"Roll a rollout back","permission":"PLATFORM_RELEASE_PROMOTE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"startRollout": {"method":"POST","path":"/rollouts/{rolloutId}/start","contract":"platform-ops","summary":"Start or continue a rollout","permission":"PLATFORM_RELEASE_PROMOTE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"updateCellTier": {"method":"PATCH","path":"/cells/{cellId}","contract":"subscription","summary":"Change a cell's tier","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiActionPlanDetail": {"type":"object","x-ticvai-persistence":"none — ai.action_plan with its ai.action_step rows","description":"A plan with its steps in DAG order.","required":["plan","steps"],"properties":{"plan":{"$ref":"#/components/schemas/AiActionPlan"},"steps":{"type":"array","items":{"$ref":"#/components/schemas/AiActionStep"}}}},
"AiDecisionRecord": {"type":"object","x-ticvai-persistence":"ai.decision_record","description":"**The standard record for every governed decision** (design 3.9, C12; AIC-193..209): a recommendation summary, a risk assessment, a forecast publication, a plan step, an assistant answer at significant depth, a governance block, a Help me choose suggestion. **Append-only; corrections are annotations; hash-chained per tenant** so tampering is detectable (AIC-203, AIC-204). **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["traceId","capabilityKey","outcome","recordHash"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"traceId":{"type":"string"},"capabilityKey":{"type":"string"},"task":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true},"subjectRef":{"type":"string","nullable":true},"inputsRef":{"type":"string","nullable":true,"description":"Where the inputs are kept (Blob or `ai.activity`), never the prompt text itself."},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"producer":{"type":"string","nullable":true},"modelVersion":{"type":"string","nullable":true},"promptTemplateVersion":{"type":"string","nullable":true},"featureSetVersion":{"type":"string","nullable":true},"knowledgeVersion":{"type":"string","nullable":true},"ruleVersions":{"type":"object","additionalProperties":true,"nullable":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"nullable":true},"policyVersion":{"type":"string","nullable":true},"approvals":{"type":"object","additionalProperties":true,"nullable":true,"description":"Approval requests and their decisions."},"humanDecision":{"type":"object","additionalProperties":true,"nullable":true,"description":"Override or intervention, where a person changed the outcome."},"executionResult":{"type":"object","additionalProperties":true,"nullable":true},"outcomeRef":{"type":"string","nullable":true,"description":"The business outcome it links to (an order, a published version, a closed case)."},"outcome":{"type":"string","enum":["answered","refused","allowed","blocked","executed","failed","approvedThenFailed","published","suggested"],"description":"`approvedThenFailed` is kept distinct from `executed` (design 1.2 Audit)."},"annotations":{"type":"array","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"byPrincipalId":{"type":"string","format":"uuid"},"note":{"type":"string"}}},"readOnly":true,"description":"Corrections, appended; the original fields are never edited."},"previousHash":{"type":"string","readOnly":true},"recordHash":{"type":"string","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiDecisionTrace": {"type":"object","x-ticvai-persistence":"none — ai.decision_record with the rows it references","description":"**The full trace of one decision** (ADM-540..546): record, evidence, candidates and rules, model and runtime, governance and approvals, execution and business outcome. Depth is gated by permission (AIC-195).","required":["record"],"properties":{"record":{"$ref":"#/components/schemas/AiDecisionRecord"},"depth":{"type":"string","enum":["business","governance","technical"]},"explanation":{"type":"string","description":"Built from structured evidence, never a model's chain of thought (AIC-192)."},"activity":{"type":"array","items":{"$ref":"#/components/schemas/AiInteraction"},"description":"The model calls behind it (`technical` depth)."},"plan":{"allOf":[{"$ref":"#/components/schemas/AiActionPlanDetail"}],"nullable":true},"interventions":{"type":"array","items":{"$ref":"#/components/schemas/AiIntervention"}},"chainVerified":{"type":"boolean","description":"The hash chain around this record verifies."}}},
"AiInteraction": {"type":"object","x-ticvai-persistence":"ai.activity","required":["id","principalId","capability","outcome","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid","nullable":true},"principalId":{"type":"string","format":"uuid"},"audience":{"type":"string","enum":["staff","guest"],"description":"**Billing divides on this.** Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop guests asking questions.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest, where the audience is `guest`. `principalId` is null in that case — **a guest is not a principal**, and attributing their tokens to a staff member would be wrong twice.\n"},"billableToTenantId":{"type":"string","format":"uuid","description":"Resolved from `scopePath` at write time, not derived later. **Billing must not depend on walking a scope tree that has since been reorganised.**\n"},"scopePath":{"type":"string"},"capability":{"type":"string"},"prompt":{"type":"string"},"response":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"outcome":{"type":"string","enum":["answered","refused","applied","rejected","failed"]},"refusalReason":{"type":"string","nullable":true},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"cost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"x-ticvai-column":"cost_amount","description":"What the call cost at the provider. **Money like every other amount** (naming-and-style 5.1) — it replaces an integer `costMinor` that carried no currency or scale, which AED and OMR read differently.\n"},"latencyMs":{"type":"integer"},"maskedFieldCount":{"type":"integer","description":"How many fields were redacted. Zero on a prompt touching guest data is a defect."},"traceId":{"type":"string"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"description":"The `ai.decision_record` this call belongs to, where it was part of a governed decision (AI design 2.3, 3.9). Null for a call audited by this row alone."},"cacheLayer":{"type":"string","nullable":true,"enum":["guardrail","semantic","exact","negative","analytics"],"description":"Which cache answered, where one did (AI design 3.6). Null for a model call."},"createdAt":{"type":"string","format":"date-time"}}},
"AiIntervention": {"type":"object","x-ticvai-persistence":"ai.intervention","description":"**A person stepping in** (AIC-187, ADM-535, ADM-536): an override, pause, resume, stop, retry or rollback, with the original AI decision and the human one side by side.","required":["kind","targetKind","targetRef"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["override","pause","resume","cancel","retry","rollback","capabilityPause","capabilityResume"]},"targetKind":{"type":"string","enum":["plan","step","decision","capability"]},"targetRef":{"type":"string"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true},"originalDecision":{"type":"object","additionalProperties":true,"nullable":true},"humanDecision":{"type":"object","additionalProperties":true,"nullable":true},"reason":{"type":"string","maxLength":2000},"principalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n**Core42 Compass is reached through `openaiCompatible`** (Chinmay, 2 October: the AI residency decision, amending AI-D02; CHG-CSA-002). Compass is the provider of the `uaeOnly` residency class (common `AiResidencyClass`): Small tier Compass GPT-4.1 mini (or Seraj), Strong tier Compass GPT-5, with OpenAI UAE and then the in-cell open-weights model as the fallback chain. OpenAI UAE is `openai` with a UAE `endpoint`; the in-cell model is `localLlm`.\n**A kind is a protocol, not a vendor** (Chinmay, 2 October, contract follow-ups: BYOK accepts any provider; CHG-FUP-008). Any vendor is accepted, named in `AiProvider.vendor`: Mistral, Cohere or any other is reached through `openaiCompatible` where its API speaks it, which the compatibility test confirms before activation (`AiProviderCompatibility`). A new native adapter is a new value here, a breaking change for a client built earlier that goes out with an approval (`docs/active/breaking-changes.yaml`); until then a vendor without either protocol is refused `422 provider-protocol-unsupported`.\n"},
"AiSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n","items":{"$ref":"#/components/schemas/AiSource"}},
"AuditRecord": {"x-ticvai-append-only":"occurredAt","type":"object","x-ticvai-persistence":"platform.audit_record","description":"26 September, pull audit R198. **One row of the platform audit trail, as `listAuditRecords` returns it.** It was a free-form object, so nothing said what an audit row carries. These are the fields the operation already filters on — who, where, on which workstation, what action, on what, and when — and nothing more. Written by the operations that audit themselves; never edited and never deleted.\n","required":["id","action","occurredAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid","description":"Who acted."},"orgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The scope node the action happened in."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation it was done from, where there was one."},"action":{"type":"string","description":"What was done, as the writing operation names it."},"subjectRef":{"type":"string","nullable":true,"description":"**The thing acted on** — a profile, a shift, an order. The same value the `subjectRef` filter matches.\n"},"occurredAt":{"type":"string","format":"date-time","description":"When. The list is ordered by this, most recent first."},"platformStaffGrantId":{"type":"string","format":"uuid","nullable":true,"description":"**Set when a TICVAI platform operator acted, naming the grant they acted under** (`identity.openPlatformStaffGrant`; decided 28 September, audit R098). Null for the tenant's own staff. Every platform action in a tenant carries one, so the tenant can see all of them.\n"}}},
"Cell": {"x-ticvai-persistence":"control.cell","x-ticvai-retired-columns":["tenant_id"],"type":"object","required":["id","name","regionId","countryCode","tier","status"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/CellKind"},"clusterId":{"type":"string","format":"uuid","nullable":true},"isReachable":{"type":"boolean","default":true,"description":"False for `onPremiseIsolated`, true for `onPremiseConnected` (ADR-0046). When false, the Control Plane holds the record for licensing and support and **cannot reach the installation** — it may sit behind a firewall with no inbound route. Every operation assuming reachability must handle absence rather than timing out, and a cell that has not called home for a month is not necessarily broken.\n"},"lastContactAt":{"type":"string","format":"date-time","nullable":true,"description":"When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first.\n"},"licenceExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. **An expired licence degrades rather than stops** — a venue whose gates refuse entry because a licence lapsed over a weekend is worse than one running unlicensed until Monday.\n"},"participatesInCrossCell":{"type":"boolean","default":true,"description":"False by default for `onPremiseIsolated`, available for `onPremiseConnected` (ADR-0046). Redeeming a pass issued elsewhere requires reaching the issuing cell at that moment, and an on-premise site may not be able to. Exclusion is the honest default; local-then-reconcile carries a double-redemption risk that needs a decision rather than an assumption.\n"},"regionId":{"type":"string","format":"uuid"},"regionName":{"type":"string"},"countryCode":{"type":"string"},"tier":{"$ref":"#/components/schemas/CellTier"},"status":{"$ref":"#/components/schemas/CellStatus"},"cloudProvider":{"type":"string","nullable":true},"cloudRegion":{"type":"string","nullable":true},"apiEndpoint":{"type":"string","nullable":true},"venueCount":{"type":"integer"},"provisionedAt":{"type":"string","format":"date-time","nullable":true},"deploymentRef":{"type":"string","nullable":true,"description":"**A pointer to where this cell runs, not a description of it.** A Kubernetes namespace, an ECS cluster ARN, a stack name — whatever the orchestrator calls the thing.\n\n**The platform does not model instances, nodes or shards** (31 August). Kubernetes already holds instance counts and they change by the second; a table copying them drifts within minutes and the copy would win.\n\n**The line is: routing decisions belong to the platform, provisioning facts belong to the orchestrator.** Qdrant is the proof — ADR-0021 makes the tenant *the* shard key, so nine operations route without a lookup and **a stored shard assignment would be a second copy of something derivable.**\n\n**CF-161 needed a table after all, and this said it did not.** The claim here was that one database per cell or one per service is a build-time decision and the DDL is identical either way. **ADR-0038 answered it per tenant**, which drops `Cell.tenantId`, adds `CellTenant`, `RolloutTenant` and a per-tenant migration row, and takes `control` out of the tenant template. `tools/derive-ddl.py` carried the same claim in its docstring.\n\n**A claim that a question cannot affect your artefact is the one most likely to be left standing after it does**, which is why the correction is recorded here rather than the sentence simply deleted."}}},
"CellCapacity": {"type":"object","x-ticvai-persistence":"none — measured, not stored","required":["cellId","isConstrained","dimensions","measuredAt"],"properties":{"cellId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/CellKind"},"tenantCount":{"type":"integer","description":"Reported, and **deliberately not the sizing signal.** Forty quiet tenants may load a cell less than three busy ones.\n"},"isConstrained":{"type":"boolean"},"constrainedDimension":{"type":"string","nullable":true},"dimensions":{"type":"array","description":"Per dimension, because the response differs. Short of connections and long on storage is a different problem from short of both.\n","items":{"type":"object","required":["dimension","used","headroom"],"properties":{"dimension":{"type":"string","enum":["concurrentUsers","transactionsPerSecond","scansPerSecond","databaseConnections","storageGb","replicationLag","cpu"]},"used":{"type":"number"},"limit":{"type":"number"},"headroom":{"type":"number","description":"Fraction remaining. Negative means already over."},"peakAt":{"type":"string","format":"date-time","nullable":true}}}},"forecastBreachAt":{"type":"string","format":"date-time","nullable":true,"description":"When the constrained dimension is projected to run out at the current trend. Null where there is no trend to project — an honest null beats an invented date.\n"},"measuredAt":{"type":"string","format":"date-time"}}},
"CellDetail": {"x-ticvai-persistence":"control.cell","allOf":[{"$ref":"#/components/schemas/Cell"},{"type":"object","properties":{"health":{"$ref":"#/components/schemas/CellHealth"},"activeJobs":{"type":"array","items":{"$ref":"#/components/schemas/CellJob"}}}}]},
"CellHealth": {"x-ticvai-persistence":"none — polled, not stored","type":"object","required":["cellId","isHealthy","schemaVersion","checkedAt"],"properties":{"cellId":{"type":"string","format":"uuid"},"isHealthy":{"type":"boolean"},"schemaVersion":{"type":"string","description":"From the cell's version register. Skew across a tenant's cells is expected during rollout; unexplained skew is a defect.\n"},"isSchemaBehind":{"type":"boolean"},"databaseStatus":{"type":"string"},"replicationLagSeconds":{"type":"number","nullable":true},"lastBackupAt":{"type":"string","format":"date-time","nullable":true},"lastRestoreDrillAt":{"type":"string","format":"date-time","nullable":true},"checkedAt":{"type":"string","format":"date-time"}}},
"CellJob": {"x-ticvai-persistence":"control.cell_job","type":"object","required":["id","cellId","kind","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"cellId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["provision","tierMigration","schemaMigration","backup","restore","decommission"]},"status":{"type":"string","enum":["queued","running","completed","failed","rolledBack"]},"progressPercent":{"type":"integer","minimum":0,"maximum":100},"message":{"type":"string","nullable":true},"error":{"type":"string","nullable":true},"scheduledFor":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"CellKind": {"type":"string","description":"Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law requires it.\n\n**On-premise is two configurations, not one (ADR-0046).** `onPremiseIsolated` keeps no channel to TICVAI — updates are pull-initiated or physically delivered, licensing is a signed file, support is blind. `onPremiseConnected` keeps an outbound control channel and is reachable, updatable and licensable in the ordinary way. The channel carries control traffic only and no natural person (ADR-0043); **AI inference is data, not control**, so connectivity alone does not grant the assistant.\n\nThere is no `hybrid`. The RFP's third model is answered by `onPremiseConnected`; a genuine split workload has never been asked for and would be a new decision.\n\n\n**`burst` added 31 August.** An environment stood up for one on-sale and torn down after (CF-162 scenario c). **It is not a jurisdiction and it is not permanent** — it holds a catalogue snapshot, three services of sixteen, and 17 tables of 380.\n\n**The other four are places data lives. This one is a place data passes through**, which is why it has its own lifecycle and a reconciliation obligation the others do not.","enum":["shared","dedicated","onPremiseIsolated","onPremiseConnected","controlPlane","burst"]},
"CellStatus": {"type":"string","enum":["provisioning","active","migrating","suspended","decommissioning","failed"]},
"CellTier": {"type":"string","enum":["shared","dedicated","isolated","clientHosted"]},
"EntitlementLimit": {"type":"object","required":["metric","limit"],"properties":{"metric":{"$ref":"#/components/schemas/UsageMetric"},"limit":{"type":"integer","nullable":true,"x-ticvai-column":"limit_value","description":"Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure `limit_value`."},"overageAllowed":{"type":"boolean","default":false},"overageUnitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"EntitlementUsage": {"x-ticvai-persistence":"none — aggregated from usage_record","type":"object","required":["tenantId","metrics"],"properties":{"tenantId":{"type":"string","format":"uuid"},"metrics":{"type":"array","items":{"type":"object","required":["metric","current","isNearLimit"],"properties":{"metric":{"$ref":"#/components/schemas/UsageMetric"},"current":{"type":"integer"},"limit":{"type":"integer","nullable":true},"percentUsed":{"type":"number","nullable":true},"isNearLimit":{"type":"boolean","description":"Approaching a limit is an account conversation. Hitting one silently at a gate is an incident.\n"},"isExceeded":{"type":"boolean"}}}},"asAt":{"type":"string","format":"date-time"}}},
"EnvironmentKind": {"type":"string","enum":["dev","staging","production"]},
"LicencePosition": {"x-ticvai-persistence":"none — union of the tenant's plan (control.tenant.plan_id -> subscription.plan_module, subscription.plan_limit) and its add-ons (control.licence_add_on, control.licence_add_on_limit by tenant_id)","type":"object","required":["tenantId","licensedModules","limits"],"properties":{"poweredByRemovable":{"type":"boolean","readOnly":true,"default":false,"description":"**Whether the tenant's licence lets it switch \"Powered by TICVAI\" off** (Chinmay, 2 October, workbook Q160 and the pre-apply round; CHG-CSA-036). False by default; true where TICVAI sold the tenant the add-on keyed `poweredByRemoval` (`addLicenceAddOn`). White label's `setBrandIdentity` refuses `showPoweredBy` false while this is false."},"tenantId":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid","nullable":true},"licensedModules":{"type":"array","description":"Union of plan modules and add-ons. The White Label Builder reads this and cannot enable anything absent from it.\n","items":{"type":"object","required":["moduleKey","source"],"properties":{"moduleKey":{"type":"string"},"displayName":{"type":"string"},"source":{"type":"string","enum":["plan","addOn"]},"validTo":{"type":"string","format":"date","nullable":true}}}},"limits":{"type":"array","items":{"$ref":"#/components/schemas/EntitlementLimit"}}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE","CORE_AI_PUBLISH","TICKETING_AI_PUBLISH","ACCESS_AI_PUBLISH","FNB_AI_PUBLISH","RETAIL_AI_PUBLISH","INVENTORY_AI_PUBLISH","SEATING_AI_PUBLISH","MEMBERSHIP_AI_PUBLISH","MARKETING_AI_PUBLISH","RESOURCES_AI_PUBLISH","QUEUE_AI_PUBLISH","TRANSPORT_AI_PUBLISH","GAMES_AI_PUBLISH","MAINTENANCE_AI_PUBLISH","ACCREDITATION_AI_PUBLISH","PARTNER_AI_PUBLISH","ANALYTICS_AI_PUBLISH","BIOMETRIC_IMAGE_VIEW","ACCESS_DIRECTION_SET","REPORT_GOVERNANCE_MANAGE"]},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"Rollout": {"type":"object","x-ticvai-persistence":"control.rollout","required":["id","releaseId","environment","status","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"releaseId":{"type":"string","format":"uuid"},"environment":{"$ref":"#/components/schemas/EnvironmentKind"},"status":{"$ref":"#/components/schemas/RolloutStatus"},"cellsTotal":{"type":"integer"},"cellsComplete":{"type":"integer"},"cellsFailed":{"type":"integer"},"startedByPrincipalId":{"type":"string","format":"uuid"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"pausedReason":{"type":"string","nullable":true},"startedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"RolloutCell": {"type":"object","x-ticvai-persistence":"control.rollout_cell","description":"One cell's state within one rollout. **`rolloutId` is the row's parent**: a cell takes part in many rollouts over its life, and `skipRolloutCell` addresses `/rollouts/{rolloutId}/cells/{cellId}`, so a row keyed on the cell alone cannot say which run it belongs to or be found by that path.\n\nA migration run's per-cell rows are the same fields under a different parent, and use `MigrationRunCell`.\n","required":["rolloutId","cellId","status"],"properties":{"rolloutId":{"type":"string","format":"uuid","description":"The rollout this row belongs to (`control.rollout`)."},"cellId":{"type":"string","format":"uuid"},"cellName":{"type":"string"},"regionName":{"type":"string"},"countryCode":{"type":"string"},"isCanary":{"type":"boolean"},"wave":{"type":"integer"},"status":{"type":"string","enum":["pending","running","complete","failed","skipped","rolledBack"]},"fromVersion":{"type":"string","nullable":true},"toVersion":{"type":"string","nullable":true},"error":{"type":"string","nullable":true},"startedAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"RolloutDetail": {"allOf":[{"$ref":"#/components/schemas/Rollout"},{"type":"object","x-ticvai-persistence":"none — projection over rollout and cell state","properties":{"cells":{"type":"array","description":"Per-cell state. \"60% complete\" says nothing about whether the failing 40% is one region or forty venues.\n","items":{"$ref":"#/components/schemas/RolloutCell"}}}}]},
"RolloutStatus": {"type":"string","enum":["queued","canary","rolling","paused","complete","failed","rolledBack"]},
"Subscription": {"x-ticvai-persistence":"subscription.contract","type":"object","required":["tenantId","planId","planVersion","status","startsAt"],"properties":{"tenantId":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid"},"planName":{"type":"string"},"planVersion":{"type":"string"},"status":{"type":"string","enum":["trial","active","pastDue","cancelled","expired"]},"startsAt":{"type":"string","format":"date"},"renewsAt":{"type":"string","format":"date","nullable":true},"cancelledAt":{"type":"string","format":"date","nullable":true},"scheduledChange":{"type":"object","nullable":true,"readOnly":true,"description":"A downgrade waiting for the next renewal (decided 28 September, audit R214 (1)). Null when none is scheduled.","properties":{"planId":{"type":"string","format":"uuid"},"planVersion":{"type":"string"},"effectiveFrom":{"type":"string","format":"date","description":"Always the `renewsAt` it was scheduled against."}}},"currentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"billingPeriod":{"type":"string"}}},
"SuspensionMode": {"type":"string","description":"Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n","enum":["readOnly","noNewSales","fullLockout"]},
"Tenant": {"x-ticvai-persistence":"control.tenant","type":"object","required":["id","code","name","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"$ref":"#/components/schemas/TenantStatus"},"suspensionMode":{"$ref":"#/components/schemas/SuspensionMode"},"suspensionReason":{"type":"string","nullable":true},"suspensionEffectiveAt":{"type":"string","format":"date-time","nullable":true,"description":"When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."},"suspensionNoticeMessage":{"$ref":"#/components/schemas/LocalisedText","description":"The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."},"terminationScheduledAt":{"type":"string","format":"date-time","nullable":true,"description":"When `terminateTenant` started the retention window. Null when no termination is under way."},"terminationRetentionUntil":{"type":"string","format":"date-time","nullable":true,"description":"`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."},"terminationReason":{"type":"string","maxLength":1000,"nullable":true},"terminationRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"planId":{"type":"string","format":"uuid","nullable":true},"planName":{"type":"string","nullable":true},"cellCount":{"type":"integer"},"venueCount":{"type":"integer"},"regionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500,"nullable":true,"description":"Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."},"accountManagerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantDetail": {"x-ticvai-persistence":"control.tenant","allOf":[{"$ref":"#/components/schemas/Tenant"},{"type":"object","properties":{"subscription":{"$ref":"#/components/schemas/Subscription"},"cells":{"type":"array","items":{"$ref":"#/components/schemas/Cell"}},"licences":{"$ref":"#/components/schemas/LicencePosition"}}}]},
"TenantStatus": {"type":"string","enum":["onboarding","active","suspended","terminating","terminated"]},
"UsageMetric": {"type":"string","enum":["venues","workstations","activeUsers","devices","brandedApps","aiTokens","apiCalls","storageGb","transactions","guestProfiles"]}
}
```
