# P09-overview-health-01 — P09 · Overview & Health

**5 screens · 13 operations · 20 schemas · 7 permissions**

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
  `AI_AUDIT_VIEW, ORDER_VIEW, PLATFORM_RELEASE_PROMOTE, PLATFORM_RELEASE_VIEW, REGION_CONFIGURE, TICKET_LOOKUP, USER_MANAGE`. A control nobody can use must say so,
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

## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `ADM-002` | Platform Dashboard | B–D | 2 | 72 | 6 | 9 | 0 | 0 | — | notStarted (generated) |
| `ADM-003` | Cross-Tenant Health Dashboard | B–D | 15 | 62 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-004` | Platform Audit Log | B–D | 3 | 28 | 6 | 3 | 0 | 0 | — | notStarted (generated) |
| `ADM-013` | Tenant Performance Monitor | B–D | 0 | 46 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-029` | Deployment Monitor | B–D | 5 | 71 | 7 | 0 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-002` Platform Dashboard

**The screen this app sits on. Everything else is entered from here and returns to it.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Overview & Health · wave 1 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `USER_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenants` reads the population and `getEntitlementUsage` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/platform-dashboard` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant. **Drawn 26 August** — `Dashboards Board` frame `adm-002`. **One board draws five dashboards across five platforms** — platform admin, partner, support, guest web and cross-tenant health. A dashboard is a shape rather than a domain, and the pack recognised that before the package did.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | text field | — | — | — | — | Sends `?status=` to `listTenants`. | `listTenants` ?status |
| Plan id | text field | — | — | — | — | Sends `?planId=` to `listTenants`. | `listTenants` ?planId |

#### Outputs: what the screen shows and produces

**Shown**

**Every tenant** (data table, from `listTenants`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `Tenant.id` |
| Code | text | not in the schema: `Tenant.code` |
| Name | text | not in the schema: `Tenant.name` |
| Status | text | not in the schema: `Tenant.status` |
| Suspension mode | text | not in the schema: `Tenant.suspensionMode` |
| Suspension reason | text | not in the schema: `Tenant.suspensionReason` |
| Plan ID | text | not in the schema: `Tenant.planId` |
| Plan name | text | not in the schema: `Tenant.planName` |
| Cell count | text | not in the schema: `Tenant.cellCount` |
| Venue count | text | not in the schema: `Tenant.venueCount` |
| Billing email | text | not in the schema: `Tenant.billingEmail` |
| Account manager principal ID | text | not in the schema: `Tenant.accountManagerPrincipalId` |

**Every cell** (data table, from `listTenantCells`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `Cell.id` |
| Name | text | not in the schema: `Cell.name` |
| Kind | text | not in the schema: `Cell.kind` |
| Cluster ID | text | not in the schema: `Cell.clusterId` |
| Is reachable | text | not in the schema: `Cell.isReachable` |
| Last contact at | text | not in the schema: `Cell.lastContactAt` |
| Licence expires at | text | not in the schema: `Cell.licenceExpiresAt` |
| Participates in cross cell | text | not in the schema: `Cell.participatesInCrossCell` |
| Region ID | text | not in the schema: `Cell.regionId` |
| Region name | text | not in the schema: `Cell.regionName` |
| Country code | text | not in the schema: `Cell.countryCode` |
| Tier | text | not in the schema: `Cell.tier` |

**The selected tenant** (detail panel, from `listTenants`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `Tenant.id` |
| Code | text | not in the schema: `Tenant.code` |
| Name | text | not in the schema: `Tenant.name` |
| Status | text | not in the schema: `Tenant.status` |
| Suspension mode | text | not in the schema: `Tenant.suspensionMode` |
| Suspension reason | text | not in the schema: `Tenant.suspensionReason` |
| Suspension effective at | text | not in the schema: `Tenant.suspensionEffectiveAt` |
| Suspension notice message | text | not in the schema: `Tenant.suspensionNoticeMessage` |
| Termination scheduled at | text | not in the schema: `Tenant.terminationScheduledAt` |
| Termination retention until | text | not in the schema: `Tenant.terminationRetentionUntil` |
| Termination reason | text | not in the schema: `Tenant.terminationReason` |
| Termination requested by principal ID | text | not in the schema: `Tenant.terminationRequestedByPrincipalId` |
| Plan ID | text | not in the schema: `Tenant.planId` |
| Plan name | text | not in the schema: `Tenant.planName` |
| Cell count | text | not in the schema: `Tenant.cellCount` |
| Venue count | text | not in the schema: `Tenant.venueCount` |

**The SSO provider config** (detail panel, from `getSsoConfig`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Display name | text | — |
| Protocol | chip: Oidc, Saml2 | — |
| Metadata URL | text | — |
| Issuer | text | — |
| Client | text | — |
| Client secret ref | text | Key vault reference. The secret itself is never returned. |
| Group mappings | list or chips (count when long) | A group with no mapping grants nothing. No default role, ever — otherwise the identity provider becomes a way to mint access nobody … |
| Auto provision principals | yes / no (icon or chip) | Create a principal on first successful sign-in. |
| Is enforced | yes / no (icon or chip) | — |
| Is active | yes / no (icon or chip) | — |

**The tenant** (detail panel, from `getTenant`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `TenantDetail.id` |
| Code | text | not in the schema: `TenantDetail.code` |
| Name | text | not in the schema: `TenantDetail.name` |
| Status | text | not in the schema: `TenantDetail.status` |
| Suspension mode | text | not in the schema: `TenantDetail.suspensionMode` |
| Suspension reason | text | not in the schema: `TenantDetail.suspensionReason` |
| Suspension effective at | text | not in the schema: `TenantDetail.suspensionEffectiveAt` |
| Suspension notice message | text | not in the schema: `TenantDetail.suspensionNoticeMessage` |
| Termination scheduled at | text | not in the schema: `TenantDetail.terminationScheduledAt` |
| Termination retention until | text | not in the schema: `TenantDetail.terminationRetentionUntil` |
| Termination reason | text | not in the schema: `TenantDetail.terminationReason` |
| Termination requested by principal ID | text | not in the schema: `TenantDetail.terminationRequestedByPrincipalId` |
| Plan ID | text | not in the schema: `TenantDetail.planId` |
| Plan name | text | not in the schema: `TenantDetail.planName` |
| Cell count | text | not in the schema: `TenantDetail.cellCount` |
| Venue count | text | not in the schema: `TenantDetail.venueCount` |

**The licence position** (detail panel, from `getTenantLicences`)

| Shows | Format | Notes |
|---|---|---|
| Plan ID | text | not in the schema: `LicencePosition.planId` |
| Licensed modules | text | not in the schema: `LicencePosition.licensedModules` |
| Limits | text | not in the schema: `LicencePosition.limits` |

**The entitlement usage** (detail panel, from `getEntitlementUsage`)

| Shows | Format | Notes |
|---|---|---|
| Metrics | text | not in the schema: `EntitlementUsage.metrics` |
| As at | text | not in the schema: `EntitlementUsage.asAt` |

**Data it reads**: `listTenants` (onLoad, from page inventory); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getSsoConfig` (onLoad, Read SSO configuration); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `listTenantCells` (onLoad, List a tenant's cells)

**Where the user goes next**

- → `ADM-319` Approval Workflow Library: *Approval Workflow Library*
- → `ADM-329` Approval Matrix Command Center: *Approval Matrix Command Center*
- → `ADM-339` Governance & Compliance Command Center: *Governance & Compliance Command Center*
- → `ADM-349` Approval Integration Command Center: *Approval Integration Command Center*
- → `ADM-359` Approval Executive KPI Dashboard: *Approval Executive KPI Dashboard*
- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`
- → `ADM-004` Platform Audit Log: *Platform Audit Log*
- → `ADM-005` Tenant Directory: *Tenant Directory*; carries `tenantId`
- → `ADM-006` Tenant Hierarchy Explorer: *Tenant Hierarchy Explorer*; carries `tenantId`
- → `ADM-007` Module & Feature Entitlement: *Module & Feature Entitlement*; carries `tenantId`
- → `ADM-008` Subscription & Plan Management: *Subscription & Plan Management*; carries `planId`, `tenantId`
- → `ADM-012` Tenant Isolation & Resource Pool: *Tenant Isolation & Resource Pool*; carries `cellId`, `tenantId`
- → `ADM-020` Platform User Directory: *Creates the first principal and grants it the role*; calls `listTenants`
- → `ADM-021` Platform Role Management: *Defines the role the first administrator will hold*
- → `ADM-369` Commercial Command Center: *Commercial Command Center*
- → `ADM-459` Billing & Commercial Command Center: *Billing & Commercial Command Center*
- → `ADM-379` Welcome & Start Your TICVAI Journey: *Welcome & Start Your TICVAI Journey*
- → `ADM-389` Commercial Rules Engine Overview: *Commercial Rules Engine Overview*
- → `ADM-399` Recommended Package Overview: *Recommended Package Overview*
- → `ADM-409` Purchase / Trial Journey Selection: *Purchase / Trial Journey Selection*
- → `ADM-419` Provisioning Command Center: *Provisioning Command Center*
- → `ADM-449` Usage & License Command Center: *Usage & License Command Center*
- → `ADM-469` AI Configuration Home & Start: *AI Configuration Home & Start*
- → `ADM-479` AI Configuration Build Command Center: *AI Configuration Build Command Center*
- → `ADM-489` AI Configuration Readiness Center: *AI Configuration Readiness Center*
- → `ADM-499` Forecasting Command Center: *Forecasting Command Center*
- → `ADM-509` Operational Forecasting Command Center: *Operational Forecasting Command Center*
- → `ADM-519` AI Governance Command Center: *AI Governance Command Center*
- → `ADM-529` AI Human Oversight Command Center: *AI Human Oversight Command Center*
- → `ADM-539` AI Explainability & Audit Command Center: *AI Explainability & Audit Command Center*
- → `ADM-549` AI Governance Monitoring Command Center: *AI Governance Monitoring Command Center*
- → `ADM-559` Payment Command Center\t7: *Payment Command Center\t7*
- → `ADM-569` Payment Orchestration Command Center\t27: *Payment Orchestration Command Center\t27*
- → `ADM-579` Terminal & Card-Present Command Center\t48: *Terminal & Card-Present Command Center\t48*
- → `ADM-589` Digital Payments Command Center\t71: *Digital Payments Command Center\t71*
- → `ADM-599` Mixed Tender & Credit Command Center\t93: *Mixed Tender & Credit Command Center\t93*
- → `ADM-609` Refund & Payment Adjustment Command Center\t116: *Refund & Payment Adjustment Command Center\t116*
- → `ADM-619` Reconciliation & Settlement Command Center\t139: *Reconciliation & Settlement Command Center\t139*
- → `ADM-629` Payment Risk & Fraud Command Center\t166: *Payment Risk & Fraud Command Center\t166*
- → `ADM-639` Recommendation Command Center: *Recommendation Command Center*
- → `ADM-649` Upsell & Upgrade Command Center: *Upsell & Upgrade Command Center*
- → `ADM-659` Cross-Sell Command Center: *Cross-Sell Command Center*
- → `ADM-669` Journey & Context Command Center: *Journey & Context Command Center*
- → `ADM-679` Personalization & NBO Command Center: *Personalization & NBO Command Center*
- → `ADM-689` Recommendation Performance Command Center: *Recommendation Performance Command Center*
- → `ADM-009` Tenant Billing & Invoicing: *Tenant Billing & Invoicing*; carries `tenantId`
- → `ADM-010` Usage Metering: *Usage Metering*; carries `tenantId`
- → `ADM-011` Licence & Seat Management: *Licence & Seat Management*; carries `tenantId`
- → `ADM-013` Tenant Performance Monitor: *Tenant Performance Monitor*; carries `cellId`
- → `ADM-014` Auto-Scaling Configuration: *Auto-Scaling Configuration*; carries `cellId`
- → `ADM-015` API Rate Limit & Quota Management: *API Rate Limit & Quota Management*; carries `tenantId`
- → `ADM-016` White-Label Branding Management: *White-Label Branding Management*
- → `ADM-017` Domain & Certificate Management: *Domain & Certificate Management*
- → `ADM-018` Localisation & Language Pack: *Localisation & Language Pack*
- → `ADM-019` Global Configuration & Defaults: *Global Configuration & Defaults*; carries `planId`
- → `ADM-022` Release & Version Management: *Release & Version Management*
- → `ADM-023` Staging Promotion & Approval: *Staging Promotion & Approval*
- → `ADM-026` End-of-Support Notice Management: *End-of-Support Notice Management*
- → `ADM-027` Database Migration Console: *Database Migration Console*
- → `ADM-029` Deployment Monitor: *Deployment Monitor*; carries `cellId`
- → `ADM-030` Infrastructure Sizing & Scaling Policy: *Infrastructure Sizing & Scaling Policy*; carries `cellId`
- → `ADM-031` Security & Compliance Dashboard: *Security & Compliance Dashboard*
- → `ADM-032` WAF & Security Policy View: *WAF & Security Policy View*; carries `cellId`
- → `ADM-033` Backup & DR Status: *Backup & DR Status*; carries `cellId`
- → `ADM-034` Archival Job Monitor: *Archival Job Monitor*; carries `cellId`
- → `ADM-037` AI Provider & Credentials: *AI Provider & Credentials*; carries `regionId`
- → `ADM-138` Promotion Command Center Dashboard: *Promotion Command Center Dashboard*
- → `ADM-158` Coupon & Promo Code Command Center: *Coupon & Promo Code Command Center*
- → `ADM-318` Dead Letters: *Dead Letters*
- → `ADM-024` Release Notification Composer: *Release Notification Composer*
- → `ADM-025` Tenant Upgrade Scheduler: *Tenant Upgrade Scheduler*
- → `ADM-028` Environment Registry: *Environment Registry*
- → `ADM-035` Support & Escalation Console: *Support & Escalation Console*
- → `ADM-036` Platform Notification Broadcast: *Platform Notification Broadcast*
- → `ADM-038` Communication Service Command Center: *Communication Service Command Center*
- → `ADM-048` Commercial Pricing Command Center: *Commercial Pricing Command Center*
- → `ADM-058` Pricing Rule Command Center: *Pricing Rule Command Center*
- → `ADM-068` Tax, Fee & Calculation Command Center: *Tax, Fee & Calculation Command Center*
- → `ADM-078` Pricing Governance Command Center: *Pricing Governance Command Center*
- → `ADM-088` Dynamic Pricing Strategy Command Center: *Dynamic Pricing Strategy Command Center*
- → `ADM-098` AI Pricing Intelligence Command Center: *AI Pricing Intelligence Command Center*
- → `ADM-108` Revenue Optimization Command Center: *Revenue Optimization Command Center*
- → `ADM-118` Product Lifecycle Command Center: *Product Lifecycle Command Center*
- → `ADM-128` Product Governance Command Center: *Product Governance Command Center*
- → `ADM-148` Promotion Rule Builder: *Promotion Rule Builder*
- → `ADM-168` Advanced Offer Command Center: *Advanced Offer Command Center*
- → `ADM-178` Bundle & Combo Command Center: *Bundle & Combo Command Center*
- → `ADM-188` Dynamic Bundle Operations Command Center: *Dynamic Bundle Operations Command Center*
- → `ADM-198` Targeting & Eligibility Command Center: *Targeting & Eligibility Command Center*
- → `ADM-208` Stacking & Conflict Command Center: *Stacking & Conflict Command Center*
- → `ADM-218` Campaign Governance & Budget Command Center: *Campaign Governance & Budget Command Center*
- → `ADM-228` Promotion Performance Command Center: *Promotion Performance Command Center*
- → `ADM-238` Rules & Workflow Command Center: *Rules & Workflow Command Center*
- → `ADM-248` Workflow Operations Command Center: *Workflow Operations Command Center*
- → `ADM-258` Sales Channel Command Center: *Sales Channel Command Center*
- → `ADM-268` Channel Operations Command Center: *Channel Operations Command Center*
- → `ADM-278` Resale Marketplace Command Center: *Resale Marketplace Command Center*
- → `ADM-288` Resale Operations Command Center: *Resale Operations Command Center*
- → `ADM-298` My Tickets & Resale Marketplace Entry: *My Tickets & Resale Marketplace Entry*
- → `ADM-308` Upgrade & Conversion Command Center: *Upgrade & Conversion Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The platform list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the platform untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No platform yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, planId and the platform are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getSsoConfig` → `USER_MANAGE` (configure) · staff

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

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (72 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-319`, `ADM-329`, `ADM-339`, `ADM-349`, `ADM-359`, `ADM-001`, `ADM-003`, `ADM-004`, `ADM-005`, `ADM-006`, `ADM-007`, `ADM-008`, `ADM-012`, `ADM-020`, `ADM-021`, `ADM-369`, `ADM-459`, `ADM-379`, `ADM-389`, `ADM-399`, `ADM-409`, `ADM-419`, `ADM-449`, `ADM-469`, `ADM-479`, `ADM-489`, `ADM-499`, `ADM-509`, `ADM-519`, `ADM-529`, `ADM-539`, `ADM-549`, `ADM-559`, `ADM-569`, `ADM-579`, `ADM-589`, `ADM-599`, `ADM-609`, `ADM-619`, `ADM-629`, `ADM-639`, `ADM-649`, `ADM-659`, `ADM-669`, `ADM-679`, `ADM-689`, `ADM-009`, `ADM-010`, `ADM-011`, `ADM-013`, `ADM-014`, `ADM-015`, `ADM-016`, `ADM-017`, `ADM-018`, `ADM-019`, `ADM-022`, `ADM-023`, `ADM-026`, `ADM-027`, `ADM-029`, `ADM-030`, `ADM-031`, `ADM-032`, `ADM-033`, `ADM-034`, `ADM-037`, `ADM-138`, `ADM-158`, `ADM-318`, `ADM-024`, `ADM-025`, `ADM-028`, `ADM-035`, `ADM-036`, `ADM-038`, `ADM-048`, `ADM-058`, `ADM-068`, `ADM-078`, `ADM-088`, `ADM-098`, `ADM-108`, `ADM-118`, `ADM-128`, `ADM-148`, `ADM-168`, `ADM-178`, `ADM-188`, `ADM-198`, `ADM-208`, `ADM-218`, `ADM-228`, `ADM-238`, `ADM-248`, `ADM-258`, `ADM-268`, `ADM-278`, `ADM-288`, `ADM-298`, `ADM-308`.
- [ ] Every gated control is gated: `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-003` Cross-Tenant Health Dashboard

**The screen this app sits on. Everything else is entered from here and returns to it.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Overview & Health · wave 2 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW`, `REGION_CONFIGURE`, `TICKET_LOOKUP` (1 read, 1 configure, 1 operate); in the flows as guest |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getCellHealth` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink), `rightId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/cross-tenant-health-dashboard` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-platform navigation removed 24 August**: SCN-003. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Drawn 26 August** — `Dashboards Board` frame `adm-003`. **One board draws five dashboards across five platforms** — platform admin, partner, support, guest web and cross-tenant health. A dashboard is a shape rather than a domain, and the pack recognised that before the package did.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Guest link | text field | — | — | `getWalletAllocation` ?guestLinkId |

**Form: Decommission cell** (modal, opened by *Decommission cell*; *Decommission cell* calls `decommissionCell`, *Cancel* sends nothing)

**Collects what `decommissionCell` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

`decommissionCell` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Save cell tier** (modal, opened by *Save cell tier*; *Save cell tier* calls `updateCellTier`, *Cancel* sends nothing)

**Collects what `updateCellTier` sends before it is called.** Required: `tier`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.

`updateCellTier` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Propagate cross region entitlement** (modal, opened by *Propagate cross region entitlement*; *Propagate cross region entitlement* calls `propagateCrossRegionEntitlement`, *Cancel* sends nothing)

**Collects what `propagateCrossRegionEntitlement` sends before it is called.** Required: `rightId`, `ticketId`, `issuingCellName`, `validFrom`, `validTo`, `admissionRulesId`, `entriesAllowed`. Optional: `guestLinkId`, `mediaCodes`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Right `rightId` | picker: choose a right | required | — | — | shows names, sends the id | — | `propagateCrossRegionEntitlement` body |
| Ticket `ticketId` | text field | required | — | — | — | — | `propagateCrossRegionEntitlement` body |
| Guest link `guestLinkId` | text field | optional | — | — | — | — | `propagateCrossRegionEntitlement` body |
| Issuing cell name `issuingCellName` | text field | required | — | — | — | — | `propagateCrossRegionEntitlement` body |
| Media codes `mediaCodes` | list of values (chips) | optional | — | — | — | — | `propagateCrossRegionEntitlement` body |
| Valid from `validFrom` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `propagateCrossRegionEntitlement` body |
| Valid to `validTo` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `propagateCrossRegionEntitlement` body |
| Admission rules `admissionRulesId` | picker: choose an admission rules | required | — | — | shows names, sends the id | — | `propagateCrossRegionEntitlement` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `propagateCrossRegionEntitlement` body |
| Entries allowed `entriesAllowed` | number field | required | — | — | — | — | `propagateCrossRegionEntitlement` body |

Errors to draw in the form: 400 Validation failed; 409 Right already propagated. Idempotent — returns the existing right. (CrossRegionEntitlement)

**Form: Reconcile redemptions** (modal, opened by *Reconcile redemptions*; *Reconcile redemptions* calls `reconcileRedemptions`, *Cancel* sends nothing)

**Collects what `reconcileRedemptions` sends before it is called.** Required: `consumingCellName`, `consumptions`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Consuming cell name `consumingCellName` | text field | required | — | — | — | — | `reconcileRedemptions` body |
| Consumptions `consumptions` | repeatable rows | required | — | at most 500 | — | — | `reconcileRedemptions` body |
| Right `consumptions[].rightId` | text field | required | — | — | — | — | `reconcileRedemptions` body |
| Total consumed `consumptions[].totalConsumed` | number field | required | — | — | — | — | `reconcileRedemptions` body |
| Last consumed at `consumptions[].lastConsumedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reconcileRedemptions` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every cell job** (data table, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellJob.id` |
| Kind | text | not in the schema: `CellJob.kind` |
| Status | text | not in the schema: `CellJob.status` |
| Progress percent | text | not in the schema: `CellJob.progressPercent` |
| Message | text | not in the schema: `CellJob.message` |
| Error | text | not in the schema: `CellJob.error` |
| Scheduled for | text | not in the schema: `CellJob.scheduledFor` |
| Completed at | text | not in the schema: `CellJob.completedAt` |

**The selected cell job** (detail panel, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellJob.id` |
| Kind | text | not in the schema: `CellJob.kind` |
| Status | text | not in the schema: `CellJob.status` |
| Progress percent | text | not in the schema: `CellJob.progressPercent` |
| Message | text | not in the schema: `CellJob.message` |
| Error | text | not in the schema: `CellJob.error` |
| Scheduled for | text | not in the schema: `CellJob.scheduledFor` |
| Completed at | text | not in the schema: `CellJob.completedAt` |

**The cell** (detail panel, from `getCell`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellDetail.id` |
| Name | text | not in the schema: `CellDetail.name` |
| Kind | text | not in the schema: `CellDetail.kind` |
| Cluster ID | text | not in the schema: `CellDetail.clusterId` |
| Is reachable | text | not in the schema: `CellDetail.isReachable` |
| Last contact at | text | not in the schema: `CellDetail.lastContactAt` |
| Licence expires at | text | not in the schema: `CellDetail.licenceExpiresAt` |
| Participates in cross cell | text | not in the schema: `CellDetail.participatesInCrossCell` |
| Region ID | text | not in the schema: `CellDetail.regionId` |
| Region name | text | not in the schema: `CellDetail.regionName` |
| Country code | text | not in the schema: `CellDetail.countryCode` |
| Tier | text | not in the schema: `CellDetail.tier` |
| Status | text | not in the schema: `CellDetail.status` |
| Cloud provider | text | not in the schema: `CellDetail.cloudProvider` |
| Cloud region | text | not in the schema: `CellDetail.cloudRegion` |
| API endpoint | text | not in the schema: `CellDetail.apiEndpoint` |

**The cell capacity** (detail panel, from `getCellCapacity`)

| Shows | Format | Notes |
|---|---|---|
| Kind | text | not in the schema: `CellCapacity.kind` |
| Tenant count | text | not in the schema: `CellCapacity.tenantCount` |
| Is constrained | text | not in the schema: `CellCapacity.isConstrained` |
| Constrained dimension | text | not in the schema: `CellCapacity.constrainedDimension` |
| Dimensions | text | not in the schema: `CellCapacity.dimensions` |
| Forecast breach at | text | not in the schema: `CellCapacity.forecastBreachAt` |
| Measured at | text | not in the schema: `CellCapacity.measuredAt` |

**The cross region entitlement** (detail panel, from `getCrossRegionEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Right | the name it points at, never the id | — |
| Ticket | text | — |
| Guest link | text | — |
| Issuing cell name | text | — |
| Consuming cell name | text | — |
| Media codes | list or chips (count when long) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Admission rules | the name it points at, never the id | — |
| Venue | the name it points at, never the id | Null where the right is valid at any venue in the consuming cell. |
| Entries allowed | 1,234 | Null means unlimited. |
| Entries consumed | 1,234 | — |
| Status | chip: Active, Exhausted, Revoked, Expired | — |
| Last consumed at | 1 Oct 2026, 14:30 | — |
| Last reconciled at | 1 Oct 2026, 14:30 | — |

**The cell health** (detail panel, from `getCellHealth`)

| Shows | Format | Notes |
|---|---|---|
| Is healthy | text | not in the schema: `CellHealth.isHealthy` |
| Is schema behind | text | not in the schema: `CellHealth.isSchemaBehind` |
| Database status | text | not in the schema: `CellHealth.databaseStatus` |
| Replication lag seconds | text | not in the schema: `CellHealth.replicationLagSeconds` |
| Last backup at | text | not in the schema: `CellHealth.lastBackupAt` |
| Last restore drill at | text | not in the schema: `CellHealth.lastRestoreDrillAt` |
| Checked at | text | not in the schema: `CellHealth.checkedAt` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cancel decommission (destructive button) | `cancelDecommission` (not in any contract) | — | — | — | — |
| Decommission cell (secondary button) | `decommissionCell` (not in any contract) | — | — | — | — |
| Save cell tier (secondary button) | `updateCellTier` (not in any contract) | — | — | — | — |
| Propagate cross region entitlement (secondary button) | `propagateCrossRegionEntitlement` POST `/cross-region-entitlements` | PropagateRightRequest | CrossRegionEntitlement | 400 Validation failed; 409 Right already propagated. Idempotent — returns the existing right. (CrossRegionEntitlement) | opens modal first |
| Reconcile redemptions (secondary button) | `reconcileRedemptions` POST `/cross-region-entitlements/reconcile` | inline | inline | — | opens modal first |

**Data it reads**: `getCellHealth` (onLoad, from page inventory); `getCell` (onLoad, Read a cell); `getCellCapacity` (onLoad, Load against headroom); `listCellJobs` (onLoad, Provisioning, migration and maintenance jobs); `getCrossRegionEntitlement` (onLoad, Read a redemption right); `getWalletAllocation` (onLoad, How wallet funds are allocated across regions)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-004` Platform Audit Log: *Platform Audit Log*
- → `SCN-003` Ready to scan: *Guest scans at the other venue*; carries `rightId`

**What opens over it**

- confirmDialog *Cancel decommission*: **Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A cross-tenant health this affects should be identified in the dialog, not just counted. **Collects what `cancelDecommission` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cross-tenant health list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cross-tenant health untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cross-tenant health yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Right already propagated. Idempotent — returns the existing right. (CrossRegionEntitlement) |

#### Permissions

- `propagateCrossRegionEntitlement` → no permission · service
- `getCrossRegionEntitlement` → `TICKET_LOOKUP` (operate) · staff
- `reconcileRedemptions` → no permission · service
- `getWalletAllocation` → `ORDER_VIEW` (read) · staff
- `setWalletAllocationPolicy` → `REGION_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

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

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (62 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cancel decommission, Decommission cell, Save cell tier, Propagate cross region entitlement, Reconcile redemptions.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-004`, `SCN-003`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `REGION_CONFIGURE`, `TICKET_LOOKUP`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-004` Platform Audit Log

**Find platform audit log for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Overview & Health · wave 2 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAiInteractions` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `decisionRecordId` (navigation) |
| Route | `/general/platform-audit-log` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — Control Plane audit not specified

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listAiInteractions`. | `listAiInteractions` ?principalId |
| Outcome | radio group | optional | — | Answered · Refused · Applied · Rejected · Failed | — | Sends `?outcome=` to `listAiInteractions`. | `listAiInteractions` ?outcome |
| From | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?from=` to `listAiInteractions`. | `listAiInteractions` ?from |

#### Outputs: what the screen shows and produces

**Shown**

**Every AI interaction** (data table, from `listAiInteractions`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Conversation | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Audience | chip: Staff, Guest | Billing divides on this. Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop … |
| Subject | the name it points at, never the id | The guest, where the audience is `guest`. `principalId` is null in that case — a guest is not a principal, and attributing their tokens to … |
| Billable to tenant | the name it points at, never the id | Resolved from `scopePath` at write time, not derived later. Billing must not depend on walking a scope tree that has since been reorganised. |
| Scope path | text | — |
| Capability | text | — |
| Prompt | text | — |
| Response | text | — |
| Sources | list or chips (count when long) | The sources an answer was grounded in, stored with the answer (8.3.70). One `jsonb` column on the row that carries it — … |
| Outcome | chip: Answered, Refused, Applied, Rejected, Failed | — |

**The selected AI interaction** (detail panel, from `listAiInteractions`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Conversation | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Audience | chip: Staff, Guest | Billing divides on this. Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop … |
| Subject | the name it points at, never the id | The guest, where the audience is `guest`. `principalId` is null in that case — a guest is not a principal, and attributing their tokens to … |
| Billable to tenant | the name it points at, never the id | Resolved from `scopePath` at write time, not derived later. Billing must not depend on walking a scope tree that has since been reorganised. |
| Scope path | text | — |
| Capability | text | — |
| Prompt | text | — |
| Response | text | — |
| Sources | list or chips (count when long) | The sources an answer was grounded in, stored with the answer (8.3.70). One `jsonb` column on the row that carries it — … |
| Outcome | chip: Answered, Refused, Applied, Rejected, Failed | — |
| Refusal reason | text | — |
| Provider | chip: Openai, Gemini, Anthropic, Azure openai, Local llm, Openai compatible | `openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development … |
| Model | text | — |
| Prompt tokens | 1,234 | — |

**Data it reads**: `listAiInteractions` (onLoad, Every prompt, response and action)

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_AUDIT_VIEW`, which `listAiInteractions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAiInteractions` → `AI_AUDIT_VIEW` (read) · staff
- `getAiDecisionTrace` → `AI_AUDIT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `AI_AUDIT_VIEW`, which `listAiInteractions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.2 | Prompt Logging System shall store prompts submitted to AI services. | Unified Operations Dashboard | CONTRACTED | `listAiInteractions` |
| 8.1.3 | Response Logging System shall store AI-generated responses. | Unified Operations Dashboard | CONTRACTED | `listAiInteractions` |
| 8.1.6 | AI Audit Trail System shall maintain a history of AI-generated actions and user decisions. | Unified Operations Dashboard | CONTRACTED | `listAiInteractions` |

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

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-004?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `BO-068`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-013` Tenant Performance Monitor

**See tenant performance monitor for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Overview & Health · wave 2 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getCellHealth` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/tenant-performance-monitor` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

#### Inputs: what the user enters or picks

**Form: Decommission cell** (modal, opened by *Decommission cell*; *Decommission cell* calls `decommissionCell`, *Cancel* sends nothing)

**Collects what `decommissionCell` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

`decommissionCell` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Save cell tier** (modal, opened by *Save cell tier*; *Save cell tier* calls `updateCellTier`, *Cancel* sends nothing)

**Collects what `updateCellTier` sends before it is called.** Required: `tier`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.

`updateCellTier` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every cell job** (data table, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellJob.id` |
| Kind | text | not in the schema: `CellJob.kind` |
| Status | text | not in the schema: `CellJob.status` |
| Progress percent | text | not in the schema: `CellJob.progressPercent` |
| Message | text | not in the schema: `CellJob.message` |
| Error | text | not in the schema: `CellJob.error` |
| Scheduled for | text | not in the schema: `CellJob.scheduledFor` |
| Completed at | text | not in the schema: `CellJob.completedAt` |

**The selected cell job** (detail panel, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellJob.id` |
| Kind | text | not in the schema: `CellJob.kind` |
| Status | text | not in the schema: `CellJob.status` |
| Progress percent | text | not in the schema: `CellJob.progressPercent` |
| Message | text | not in the schema: `CellJob.message` |
| Error | text | not in the schema: `CellJob.error` |
| Scheduled for | text | not in the schema: `CellJob.scheduledFor` |
| Completed at | text | not in the schema: `CellJob.completedAt` |

**The cell** (detail panel, from `getCell`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellDetail.id` |
| Name | text | not in the schema: `CellDetail.name` |
| Kind | text | not in the schema: `CellDetail.kind` |
| Cluster ID | text | not in the schema: `CellDetail.clusterId` |
| Is reachable | text | not in the schema: `CellDetail.isReachable` |
| Last contact at | text | not in the schema: `CellDetail.lastContactAt` |
| Licence expires at | text | not in the schema: `CellDetail.licenceExpiresAt` |
| Participates in cross cell | text | not in the schema: `CellDetail.participatesInCrossCell` |
| Region ID | text | not in the schema: `CellDetail.regionId` |
| Region name | text | not in the schema: `CellDetail.regionName` |
| Country code | text | not in the schema: `CellDetail.countryCode` |
| Tier | text | not in the schema: `CellDetail.tier` |
| Status | text | not in the schema: `CellDetail.status` |
| Cloud provider | text | not in the schema: `CellDetail.cloudProvider` |
| Cloud region | text | not in the schema: `CellDetail.cloudRegion` |
| API endpoint | text | not in the schema: `CellDetail.apiEndpoint` |

**The cell capacity** (detail panel, from `getCellCapacity`)

| Shows | Format | Notes |
|---|---|---|
| Kind | text | not in the schema: `CellCapacity.kind` |
| Tenant count | text | not in the schema: `CellCapacity.tenantCount` |
| Is constrained | text | not in the schema: `CellCapacity.isConstrained` |
| Constrained dimension | text | not in the schema: `CellCapacity.constrainedDimension` |
| Dimensions | text | not in the schema: `CellCapacity.dimensions` |
| Forecast breach at | text | not in the schema: `CellCapacity.forecastBreachAt` |
| Measured at | text | not in the schema: `CellCapacity.measuredAt` |

**The cell health** (detail panel, from `getCellHealth`)

| Shows | Format | Notes |
|---|---|---|
| Is healthy | text | not in the schema: `CellHealth.isHealthy` |
| Is schema behind | text | not in the schema: `CellHealth.isSchemaBehind` |
| Database status | text | not in the schema: `CellHealth.databaseStatus` |
| Replication lag seconds | text | not in the schema: `CellHealth.replicationLagSeconds` |
| Last backup at | text | not in the schema: `CellHealth.lastBackupAt` |
| Last restore drill at | text | not in the schema: `CellHealth.lastRestoreDrillAt` |
| Checked at | text | not in the schema: `CellHealth.checkedAt` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cancel decommission (destructive button) | `cancelDecommission` (not in any contract) | — | — | — | — |
| Decommission cell (secondary button) | `decommissionCell` (not in any contract) | — | — | — | — |
| Save cell tier (secondary button) | `updateCellTier` (not in any contract) | — | — | — | — |

**Data it reads**: `getCellHealth` (onLoad, from page inventory); `getCell` (onLoad, Read a cell); `getCellCapacity` (onLoad, Load against headroom); `listCellJobs` (onLoad, Provisioning, migration and maintenance jobs)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`
- → `ADM-014` Auto-Scaling Configuration: *Auto-Scaling Configuration*; carries `cellId`

**What opens over it**

- confirmDialog *Cancel decommission*: **Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A tenant performance this affects should be identified in the dialog, not just counted. **Collects what `cancelDecommission` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tenant performance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tenant performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tenant performance yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

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

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (46 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-013?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cancel decommission, Decommission cell, Save cell tier.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `ADM-014`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-029` Deployment Monitor

**Find deployment monitor for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Overview & Health · wave 2 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_RELEASE_PROMOTE`, `PLATFORM_RELEASE_VIEW` (1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getRollout` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink), `rolloutId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/deployment-monitor` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Queued · Canary · Rolling · Paused · Complete · Failed · Rolled back | `listRollouts` ?status |

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

**Form: Decommission cell** (modal, opened by *Decommission cell*; *Decommission cell* calls `decommissionCell`, *Cancel* sends nothing)

**Collects what `decommissionCell` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

`decommissionCell` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Start rollout** (modal, opened by *Start rollout*; *Start rollout* calls `startRollout`, *Cancel* sends nothing)

**Collects what `startRollout` sends before it is called.** Required: `stage`. **Sending it asks for approval, it does not promote** (decided 28 September, audit R144): the answer is 202 with a pending `releasePromotion` request, routed to a holder of `PLATFORM_RELEASE_PROMOTE` other than the requester — nobody approves their own promotion. The rollout moves to the stage when that request is approved. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Stage `stage` | segmented control | required | — | Canary · Partial · Full | — | The stage to take the rollout to (decided 28 September, audit R096). `canary` is the first cell only; `partial` is a wave of the remaining cells, and may be sent again to continue … | `startRollout` body |

Errors to draw in the form: 409 Not in a state that permits this

**Form: Save cell tier** (modal, opened by *Save cell tier*; *Save cell tier* calls `updateCellTier`, *Cancel* sends nothing)

**Collects what `updateCellTier` sends before it is called.** Required: `tier`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.

`updateCellTier` is not in any contract: draw the form greyed and list it in FINDINGS.md.

#### Outputs: what the screen shows and produces

**Shown**

**Every cell job** (data table, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellJob.id` |
| Kind | text | not in the schema: `CellJob.kind` |
| Status | text | not in the schema: `CellJob.status` |
| Progress percent | text | not in the schema: `CellJob.progressPercent` |
| Message | text | not in the schema: `CellJob.message` |
| Error | text | not in the schema: `CellJob.error` |
| Scheduled for | text | not in the schema: `CellJob.scheduledFor` |
| Completed at | text | not in the schema: `CellJob.completedAt` |

**Every rollout** (data table, from `listRollouts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Release | the name it points at, never the id | — |
| Environment | chip: Dev, Staging, Production | — |
| Status | chip: Queued, Canary, Rolling, Paused, Complete, Failed… | — |
| Cells total | 1,234 | — |
| Cells complete | 1,234 | — |
| Cells failed | 1,234 | — |
| Started by principal | the name it points at, never the id | — |
| Approved by principal | the name it points at, never the id | — |
| Paused reason | text | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**The selected cell job** (detail panel, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellJob.id` |
| Kind | text | not in the schema: `CellJob.kind` |
| Status | text | not in the schema: `CellJob.status` |
| Progress percent | text | not in the schema: `CellJob.progressPercent` |
| Message | text | not in the schema: `CellJob.message` |
| Error | text | not in the schema: `CellJob.error` |
| Scheduled for | text | not in the schema: `CellJob.scheduledFor` |
| Completed at | text | not in the schema: `CellJob.completedAt` |

**The cell** (detail panel, from `getCell`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellDetail.id` |
| Name | text | not in the schema: `CellDetail.name` |
| Kind | text | not in the schema: `CellDetail.kind` |
| Cluster ID | text | not in the schema: `CellDetail.clusterId` |
| Is reachable | text | not in the schema: `CellDetail.isReachable` |
| Last contact at | text | not in the schema: `CellDetail.lastContactAt` |
| Licence expires at | text | not in the schema: `CellDetail.licenceExpiresAt` |
| Participates in cross cell | text | not in the schema: `CellDetail.participatesInCrossCell` |
| Region ID | text | not in the schema: `CellDetail.regionId` |
| Region name | text | not in the schema: `CellDetail.regionName` |
| Country code | text | not in the schema: `CellDetail.countryCode` |
| Tier | text | not in the schema: `CellDetail.tier` |
| Status | text | not in the schema: `CellDetail.status` |
| Cloud provider | text | not in the schema: `CellDetail.cloudProvider` |
| Cloud region | text | not in the schema: `CellDetail.cloudRegion` |
| API endpoint | text | not in the schema: `CellDetail.apiEndpoint` |

**The cell capacity** (detail panel, from `getCellCapacity`)

| Shows | Format | Notes |
|---|---|---|
| Kind | text | not in the schema: `CellCapacity.kind` |
| Tenant count | text | not in the schema: `CellCapacity.tenantCount` |
| Is constrained | text | not in the schema: `CellCapacity.isConstrained` |
| Constrained dimension | text | not in the schema: `CellCapacity.constrainedDimension` |
| Dimensions | text | not in the schema: `CellCapacity.dimensions` |
| Forecast breach at | text | not in the schema: `CellCapacity.forecastBreachAt` |
| Measured at | text | not in the schema: `CellCapacity.measuredAt` |

**The cell health** (detail panel, from `getCellHealth`)

| Shows | Format | Notes |
|---|---|---|
| Is healthy | text | not in the schema: `CellHealth.isHealthy` |
| Is schema behind | text | not in the schema: `CellHealth.isSchemaBehind` |
| Database status | text | not in the schema: `CellHealth.databaseStatus` |
| Replication lag seconds | text | not in the schema: `CellHealth.replicationLagSeconds` |
| Last backup at | text | not in the schema: `CellHealth.lastBackupAt` |
| Last restore drill at | text | not in the schema: `CellHealth.lastRestoreDrillAt` |
| Checked at | text | not in the schema: `CellHealth.checkedAt` |

**The rollout** (detail panel, from `getRollout`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Release | the name it points at, never the id | — |
| Environment | chip: Dev, Staging, Production | — |
| Status | chip: Queued, Canary, Rolling, Paused, Complete, Failed… | — |
| Cells total | 1,234 | — |
| Cells complete | 1,234 | — |
| Cells failed | 1,234 | — |
| Started by principal | the name it points at, never the id | — |
| Approved by principal | the name it points at, never the id | — |
| Paused reason | text | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Cells | list or chips (count when long) | Per-cell state. "60% complete" says nothing about whether the failing 40% is one region or forty venues. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Pause rollout (primary button) | `pauseRollout` POST `/rollouts/{rolloutId}/pause` | inline | RolloutDetail | — | opens modal first |
| Rollback rollout (secondary button) | `rollbackRollout` POST `/rollouts/{rolloutId}/rollback` | inline | RolloutDetail | 409 A migration in this release is irreversible. The response names it — a one-way door should be identified, not discovered. (IrreversibleProblem) | opens modal first |
| Cancel decommission (destructive button) | `cancelDecommission` (not in any contract) | — | — | — | — |
| Decommission cell (secondary button) | `decommissionCell` (not in any contract) | — | — | — | — |
| Start rollout (secondary button) | `startRollout` POST `/rollouts/{rolloutId}/start` | inline | no body | 409 Not in a state that permits this | opens modal first |
| Save cell tier (secondary button) | `updateCellTier` (not in any contract) | — | — | — | — |

**Data it reads**: `listCellJobs` (onLoad, from page inventory); `listRollouts` (onLoad, Rollouts in flight); `getCell` (onLoad, Read a cell); `getCellCapacity` (onLoad, Load against headroom); `getCellHealth` (onLoad, Cell health and schema version)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

**What opens over it**

- confirmDialog *Cancel decommission*: **Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A deployment this affects should be identified in the dialog, not just counted. **Collects what `cancelDecommission` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The deployment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deployment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No deployment yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `listCellJobs` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Rollout pending approval (`?state=rolloutPendingApproval`) | **Requested, not moved.** `startRollout` answered 202: the rollout shows the stage it has reached, the stage requested and that a `releasePromotion` approval is pending with the platform release manager. The requester sees no approve action for their own request (decided 28 September, audit R144). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A migration in this release is irreversible. The response names it — a one-way door should be identified, not discovered. (IrreversibleProblem); 409 Not in a state that permits this |

#### Permissions

- `listRollouts` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `getRollout` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `pauseRollout` → `PLATFORM_RELEASE_PROMOTE` (operate) · staff
- `rollbackRollout` → `PLATFORM_RELEASE_PROMOTE` (operate) · staff
- `startRollout` → `PLATFORM_RELEASE_PROMOTE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `listCellJobs` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

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
- [ ] Every output is drawn (71 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-029?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, rolloutPendingApproval, offline.
- [ ] Every action is wired with its success and its failure: Pause rollout, Rollback rollout, Cancel decommission, Decommission cell, Start rollout, Save cell tier.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `PLATFORM_RELEASE_PROMOTE`, `PLATFORM_RELEASE_VIEW`.
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

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getAiDecisionTrace": {"method":"GET","path":"/decision-records/{decisionRecordId}/trace","contract":"ai","summary":"The full trace of a decision","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"depth","in":"query","required":null}],"requestBody":null,"responds":"AiDecisionTrace"},
"getCrossRegionEntitlement": {"method":"GET","path":"/cross-region-entitlements/{rightId}","contract":"cross-region","summary":"Read a redemption right","permission":"TICKET_LOOKUP","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CrossRegionEntitlement"},
"getRollout": {"method":"GET","path":"/rollouts/{rolloutId}","contract":"platform-ops","summary":"Rollout progress per cell","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"RolloutDetail"},
"getSsoConfig": {"method":"GET","path":"/tenants/sso-config","contract":"identity","summary":"Read SSO configuration","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SsoProviderConfig"},
"getWalletAllocation": {"method":"GET","path":"/wallet-allocations","contract":"cross-region","summary":"The consuming cell's bounded offline allocation","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"guestLinkId","in":"query","required":true}],"requestBody":null,"responds":"WalletAllocation"},
"listAiInteractions": {"method":"GET","path":"/interactions","contract":"ai","summary":"Every prompt, response and action","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"principalId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRollouts": {"method":"GET","path":"/rollouts","contract":"platform-ops","summary":"List rollouts","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"pauseRollout": {"method":"POST","path":"/rollouts/{rolloutId}/pause","contract":"platform-ops","summary":"Halt a rollout in progress","permission":"PLATFORM_RELEASE_PROMOTE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RolloutDetail"},
"propagateCrossRegionEntitlement": {"method":"POST","path":"/cross-region-entitlements","contract":"cross-region","summary":"Propagate a right from the issuing cell to a consuming cell","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PropagateRightRequest","responds":"CrossRegionEntitlement"},
"reconcileRedemptions": {"method":"POST","path":"/cross-region-entitlements/reconcile","contract":"cross-region","summary":"Report consumption back to the issuing cell","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"rollbackRollout": {"method":"POST","path":"/rollouts/{rolloutId}/rollback","contract":"platform-ops","summary":"Roll a rollout back","permission":"PLATFORM_RELEASE_PROMOTE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setWalletAllocationPolicy": {"method":"PUT","path":"/wallet-allocations","contract":"cross-region","summary":"Set the allocation cap policy","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletAllocation"},
"startRollout": {"method":"POST","path":"/rollouts/{rolloutId}/start","contract":"platform-ops","summary":"Start or continue a rollout","permission":"PLATFORM_RELEASE_PROMOTE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
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
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"},
"AiSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n","items":{"$ref":"#/components/schemas/AiSource"}},
"CrossRegionEntitlement": {"x-ticvai-persistence":"platform.cross_region_entitlement","type":"object","required":["rightId","ticketId","issuingCellName","consumingCellName","validFrom","validTo","entriesAllowed","entriesConsumed","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"rightId":{"type":"string","format":"uuid"},"ticketId":{"type":"string"},"guestLinkId":{"type":"string","nullable":true},"issuingCellName":{"type":"string"},"consumingCellName":{"type":"string"},"mediaCodes":{"type":"array","items":{"type":"string"}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"admissionRulesId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Null where the right is valid at any venue in the consuming cell."},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited."},"entriesConsumed":{"type":"integer"},"status":{"type":"string","enum":["active","exhausted","revoked","expired"]},"lastConsumedAt":{"type":"string","format":"date-time","nullable":true},"lastReconciledAt":{"type":"string","format":"date-time","nullable":true}}},
"EnvironmentKind": {"type":"string","enum":["dev","staging","production"]},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PropagateRightRequest": {"type":"object","required":["rightId","ticketId","issuingCellName","validFrom","validTo","admissionRulesId","entriesAllowed"],"properties":{"rightId":{"type":"string","format":"uuid"},"ticketId":{"type":"string"},"guestLinkId":{"type":"string"},"issuingCellName":{"type":"string"},"mediaCodes":{"type":"array","items":{"type":"string"}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"admissionRulesId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"entriesAllowed":{"type":"integer","nullable":true}}},
"Rollout": {"type":"object","x-ticvai-persistence":"control.rollout","required":["id","releaseId","environment","status","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"releaseId":{"type":"string","format":"uuid"},"environment":{"$ref":"#/components/schemas/EnvironmentKind"},"status":{"$ref":"#/components/schemas/RolloutStatus"},"cellsTotal":{"type":"integer"},"cellsComplete":{"type":"integer"},"cellsFailed":{"type":"integer"},"startedByPrincipalId":{"type":"string","format":"uuid"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"pausedReason":{"type":"string","nullable":true},"startedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"RolloutCell": {"type":"object","x-ticvai-persistence":"control.rollout_cell","description":"One cell's state within one rollout. **`rolloutId` is the row's parent**: a cell takes part in many rollouts over its life, and `skipRolloutCell` addresses `/rollouts/{rolloutId}/cells/{cellId}`, so a row keyed on the cell alone cannot say which run it belongs to or be found by that path.\n\nA migration run's per-cell rows are the same fields under a different parent, and use `MigrationRunCell`.\n","required":["rolloutId","cellId","status"],"properties":{"rolloutId":{"type":"string","format":"uuid","description":"The rollout this row belongs to (`control.rollout`)."},"cellId":{"type":"string","format":"uuid"},"cellName":{"type":"string"},"regionName":{"type":"string"},"countryCode":{"type":"string"},"isCanary":{"type":"boolean"},"wave":{"type":"integer"},"status":{"type":"string","enum":["pending","running","complete","failed","skipped","rolledBack"]},"fromVersion":{"type":"string","nullable":true},"toVersion":{"type":"string","nullable":true},"error":{"type":"string","nullable":true},"startedAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"RolloutDetail": {"allOf":[{"$ref":"#/components/schemas/Rollout"},{"type":"object","x-ticvai-persistence":"none — projection over rollout and cell state","properties":{"cells":{"type":"array","description":"Per-cell state. \"60% complete\" says nothing about whether the failing 40% is one region or forty venues.\n","items":{"$ref":"#/components/schemas/RolloutCell"}}}}]},
"RolloutStatus": {"type":"string","enum":["queued","canary","rolling","paused","complete","failed","rolledBack"]},
"SsoGroupMapping": {"x-ticvai-persistence":"identity.sso_group_mapping","type":"object","required":["externalGroup","roleId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — the response returned the external group, the role and the scope, which is everything a caller needs and not the row own identity.\n**(provider, external_group) is unique and would serve**, but a mapping is edited and revoked by an administrator, and **a row addressed by the values it holds cannot be corrected** — changing the group means deleting a mapping and creating another, which loses who granted it and when.\n"},"externalGroup":{"type":"string"},"roleId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"Scope the mapped role is granted at."}}},
"SsoProtocol": {"type":"string","enum":["oidc","saml2"]},
"SsoProviderConfig": {"x-ticvai-persistence":"identity.sso_provider","type":"object","required":["id","displayName","protocol","groupMappings"],"properties":{"id":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"protocol":{"$ref":"#/components/schemas/SsoProtocol"},"metadataUrl":{"type":"string","nullable":true},"issuer":{"type":"string","nullable":true},"clientId":{"type":"string","nullable":true},"clientSecretRef":{"type":"string","nullable":true,"description":"Key vault reference. The secret itself is never returned."},"groupMappings":{"type":"array","minItems":1,"description":"**A group with no mapping grants nothing.** No default role, ever — otherwise the identity provider becomes a way to mint access nobody configured.\n","items":{"$ref":"#/components/schemas/SsoGroupMapping"}},"autoProvisionPrincipals":{"type":"boolean","default":false,"description":"Create a principal on first successful sign-in."},"isEnforced":{"type":"boolean","default":false},"isActive":{"type":"boolean"}}},
"WalletAllocation": {"x-ticvai-persistence":"platform.wallet_authorisation","type":"object","required":["guestLinkId","mode","availableAmount"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"guestLinkId":{"type":"string"},"mode":{"type":"string","enum":["none","fixed","percentageOfBalance"]},"allocatedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"drawnAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"availableAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lastToppedUpAt":{"type":"string","format":"date-time","nullable":true},"allocationCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"**The allocation is denominated in the home currency.** A ceiling set in AED does not become a different ceiling because the guest walked into a Saudi venue — converting the limit as well as the spend is how a policy silently loosens when a rate moves."}}}
}
```
