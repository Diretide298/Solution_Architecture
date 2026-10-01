# P09-tenants-licensing-01 — P09 · Tenants & Licensing

**9 screens · 12 operations · 15 schemas · 6 permissions**

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
  `DEVELOPER_ADMIN, DEVELOPER_VIEW, PLATFORM_TENANT_ACCESS, SCOPE_MANAGE, SCOPE_VIEW, USER_MANAGE`. A control nobody can use must say so,
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
| `ADM-005` | Tenant Directory | A | 21 | 79 | 7 | 17 | 0 | 0 | — | notStarted (generated) |
| `ADM-006` | Tenant Hierarchy Explorer | B–D | 6 | 80 | 6 | 15 | 0 | 0 | — | notStarted (generated) |
| `ADM-007` | Module & Feature Entitlement | B–D | 0 | 81 | 6 | 14 | 0 | 0 | — | notStarted (generated) |
| `ADM-008` | Subscription & Plan Management | A | 0 | 118 | 6 | 46 | 0 | 0 | — | notStarted (generated) |
| `ADM-009` | Tenant Billing & Invoicing | B–D | 1 | 90 | 6 | 11 | 0 | 0 | — | notStarted (generated) |
| `ADM-010` | Usage Metering | B–D | 0 | 75 | 6 | 16 | 0 | 0 | — | notStarted (generated) |
| `ADM-011` | Licence & Seat Management | B–D | 0 | 81 | 6 | 18 | 0 | 6 | — | notStarted (generated) |
| `ADM-012` | Tenant Isolation & Resource Pool | B–D | 0 | 79 | 6 | 9 | 0 | 0 | — | notStarted (generated) |
| `ADM-015` | API Rate Limit & Quota Management | B–D | 18 | 105 | 6 | 33 | 2 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-005` Tenant Directory

**Find the right one quickly, and act on it without opening it.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 1 · needs the `membership` module |
| Block | Block A · ticket #17824 (APP-SETUP-ADM-005) |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_ACCESS`, `USER_MANAGE` (1 operate, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenants` reads the population and `getEntitlementUsage` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (ADM-002) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/tenant-directory` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | text field | — | — | — | — | Sends `?status=` to `listTenants`. | `listTenants` ?status |
| Plan id | text field | — | — | — | — | Sends `?planId=` to `listTenants`. | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client UUIDv7), `permissions` (tenant permissions only — the ones this screen's operations need, preselected), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Add licence add on** (modal, opened by *Add licence add on*; *Add licence add on* calls `addLicenceAddOn`, *Cancel* sends nothing)

**Collects what `addLicenceAddOn` sends before it is called.** Required: `moduleKey`. Optional: `limitOverrides`, `price`, `validFrom`, `validTo`, `note`. Dismissing sends nothing; the screen behind is unchanged.

`addLicenceAddOn` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Create tenant** (modal, opened by *Create tenant*; *Create tenant* calls `createTenant`, *Cancel* sends nothing)

**Collects what `createTenant` sends before it is called.** Required: `code`, `name`, `billingEmail`. Optional: `billingAddress`, `accountManagerPrincipalId`, `planId`. Dismissing sends nothing; the screen behind is unchanged.

`createTenant` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Provision cell** (modal, opened by *Provision cell*; *Provision cell* calls `provisionCell`, *Cancel* sends nothing)

**Collects what `provisionCell` sends before it is called.** Required: `regionId`, `countryCode`, `tier`. Optional: `cloudProvider`, `cloudRegion`, `clientHostedEndpoint`. Dismissing sends nothing; the screen behind is unchanged.

`provisionCell` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Save SSO config** (modal, opened by *Save SSO config*; *Save SSO config* calls `setSsoConfig`, *Cancel* sends nothing)

**Collects what `setSsoConfig` sends before it is called.** Required: `id`, `displayName`, `protocol`, `groupMappings`. Optional: `metadataUrl`, `issuer`, `clientId`, `clientSecretRef`, `autoProvisionPrincipals`, `isEnforced`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setSsoConfig` body |
| Display name `displayName` | text field | required | — | — | — | — | `setSsoConfig` body |
| Protocol `protocol` | segmented control | required | — | Oidc · Saml2 | — | — | `setSsoConfig` body |
| Metadata URL `metadataUrl` | text field | optional | — | — | — | — | `setSsoConfig` body |
| Issuer `issuer` | text field | optional | — | — | — | — | `setSsoConfig` body |
| Client `clientId` | text field | optional | — | — | — | — | `setSsoConfig` body |
| Client secret ref `clientSecretRef` | text field | optional | — | — | — | Key vault reference. The secret itself is never returned. | `setSsoConfig` body |
| Group mappings `groupMappings` | repeatable rows | required | — | at least 1 | — | A group with no mapping grants nothing. No default role, ever — otherwise the identity provider becomes a way to mint access nobody configured. | `setSsoConfig` body |
| External group `groupMappings[].externalGroup` | text field | required | — | — | — | — | `setSsoConfig` body |
| Role `groupMappings[].roleId` | picker: choose a role | required | — | — | shows names, sends the id | — | `setSsoConfig` body |
| Scope path `groupMappings[].scopePath` | text field | optional | — | — | — | Scope the mapped role is granted at. | `setSsoConfig` body |
| Auto provision principals `autoProvisionPrincipals` | toggle | optional | off | — | — | Create a principal on first successful sign-in. | `setSsoConfig` body |
| Is enforced `isEnforced` | toggle | optional | off | — | — | — | `setSsoConfig` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `setSsoConfig` body |

Errors to draw in the form: 400 Metadata unreachable, or no group mappings supplied

**Form: Save tenant** (modal, opened by *Save tenant*; *Save tenant* calls `updateTenant`, *Cancel* sends nothing)

**Collects what `updateTenant` sends before it is called.** Nothing in the body is required. Optional: `name`, `billingEmail`, `billingAddress`, `accountManagerPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.

`updateTenant` is not in any contract: draw the form greyed and list it in FINDINGS.md.

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (detail panel, from `openPlatformStaffGrant`): **Always visible while the screen acts on a tenant** (decided 28 September, audit R098): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Add licence add on (primary button) | `addLicenceAddOn` (not in any contract) | — | — | — | — |
| Create tenant (secondary button) | `createTenant` (not in any contract) | — | — | — | — |
| Provision cell (secondary button) | `provisionCell` (not in any contract) | — | — | — | — |
| Reactivate tenant (secondary button) | `reactivateTenant` (not in any contract) | — | — | — | — |
| Remove licence add on (destructive button) | `removeLicenceAddOn` (not in any contract) | — | — | — | — |
| Save SSO config (secondary button) | `setSsoConfig` PUT `/tenants/sso-config` | SsoProviderConfig | SsoProviderConfig | 400 Metadata unreachable, or no group mappings supplied | opens modal first |
| Suspend tenant (destructive button) | `suspendTenant` (not in any contract) | — | — | — | — |
| Terminate tenant (destructive button) | `terminateTenant` (not in any contract) | — | — | — | — |
| Save tenant (secondary button) | `updateTenant` (not in any contract) | — | — | — | — |

**Data it reads**: `listTenants` (onLoad, from page inventory); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getSsoConfig` (onLoad, Read SSO configuration); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `listTenantCells` (onLoad, List a tenant's cells)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`
- → `ADM-008` Subscription & Plan Management: *Subscription & Plan Management*; carries `planId`, `tenantId`
- → `ADM-012` Tenant Isolation & Resource Pool: *Provisions or assigns a cell*; carries `cellId`, `tenantId`

**What opens over it**

- confirmDialog *Remove licence add on*: **Names what `removeLicenceAddOn` changes and what it leaves alone**, in the consequence rather than the verb. A tenant this affects should be identified in the dialog, not just counted. **Collects what `removeLicenceAddOn` sends before it is called.** Required: `moduleKey`, `reason`.
- confirmDialog *Suspend tenant*: **Names what `suspendTenant` changes and what it leaves alone**, in the consequence rather than the verb. A tenant this affects should be identified in the dialog, not just counted. **Collects what `suspendTenant` sends before it is called.** Required: `mode`, `reason`. Optional: `effectiveAt` …
- confirmDialog *Terminate tenant*: **Names what `terminateTenant` changes and what it leaves alone**, in the consequence rather than the verb. A tenant this affects should be identified in the dialog, not just counted. **Collects what `terminateTenant` sends before it is called.** Required: `reason`, `retentionDays` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tenant list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tenant untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tenant yet. Offers Add licence add on (`addLicenceAddOn`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, planId and the tenant are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Metadata unreachable, or no group mappings supplied; 400 Validation failed |

#### Permissions

- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `getSsoConfig` → `USER_MANAGE` (configure) · staff
- `setSsoConfig` → `USER_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.4.1 | Marketplace Catalog - System shall provide a marketplace of available modules. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.4.2 | Module Discovery - System shall allow customers to browse modules. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.4.3 | Module Installation - System shall support self-service module installation. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.4.4 | Module Activation - System shall support module activation. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.4.5 | Module Deactivation - System shall support module deactivation. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.5.1 | License Generation - System shall generate subscription licenses. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.2 | License Assignment - System shall assign licenses to tenants. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.3 | License Validation - System shall validate licenses automatically. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.4 | License Enforcement - System shall enforce licensing restrictions. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.5 | License Expiration - System shall support license expiration management. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.6 | Grace Period Management - System shall support configurable grace periods. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.7 | License Renewal Management - System shall support license renewals. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-005` · status **notStarted** · provenance generated
- Flow F16 *A venue opens for the first time*, step 1: Creates the tenant → A tenant with no venues yet
- Flow F96 *A tenant is provisioned, licensed and its modules enabled*, step 1: Tenant Directory. → 15 operations, 15 of them previously unwalked.
- Flow F96 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (79 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Add licence add on, Create tenant, Provision cell, Reactivate tenant, Remove licence add on, Save SSO config, Suspend tenant, Terminate tenant, Save tenant.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `ADM-008`, `ADM-012`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_ACCESS`, `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-006` Tenant Hierarchy Explorer

**See tenant hierarchy explorer for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 1 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `SCOPE_MANAGE`, `SCOPE_VIEW`, `USER_MANAGE` (2 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenants` reads the population and `getSsoConfig` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (ADM-002) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/tenant-hierarchy-explorer` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | text field | — | — | — | — | Sends `?status=` to `listTenants`. | `listTenants` ?status |
| Plan id | text field | — | — | — | — | Sends `?planId=` to `listTenants`. | `listTenants` ?planId |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Under | text field | — | — | `listOrgUnits` ?under |
| Level | select | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet · Subject | `listOrgUnits` ?level |
| Include inactive | toggle | off | — | `listOrgUnits` ?includeInactive |

**Form: Save tenant** (modal, opened by *Save tenant*; *Save tenant* calls `updateTenant`, *Cancel* sends nothing)

**Collects what `updateTenant` sends before it is called.** Nothing in the body is required. Optional: `name`, `billingEmail`, `billingAddress`, `accountManagerPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.

`updateTenant` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Create org unit** (modal, opened by *Create org unit*; *Create org unit* calls `createOrgUnit`, *Cancel* sends nothing)

**Collects what `createOrgUnit` sends before it is called.** Required: `level`, `parentId`, `code`, `name`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Level `level` | select | required | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet · Subject | — | The eight organisational levels, plus `subject`. Restored 24 August. | `createOrgUnit` body |
| Parent `parentId` | picker: choose a parent | required | — | — | shows names, sends the id | Required for every level except tenant, which the cell creates at provisioning. | `createOrgUnit` body |
| Code `code` | text field | required | — | max length 64; pattern `^[a-z0-9_]+$` | — | Becomes the final ltree segment. Immutable once created. | `createOrgUnit` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createOrgUnit` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.

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

**Every org unit** (data table, from `listOrgUnits`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Level | chip: Tenant, Brand, Region, Venue, Department, Sub department… | The eight organisational levels, plus `subject`. Restored 24 August. |
| Parent | the name it points at, never the id | — |
| Path | text | Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`. |
| Code | text | — |
| Name | text | — |
| Is active | yes / no (icon or chip) | False causes every permission query at or beneath this node to resolve to DENY. |
| Child count | 1,234 | — |

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

**The entitlement usage** (detail panel, from `getEntitlementUsage`)

| Shows | Format | Notes |
|---|---|---|
| Metrics | text | not in the schema: `EntitlementUsage.metrics` |
| As at | text | not in the schema: `EntitlementUsage.asAt` |

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save tenant (primary button) | `updateTenant` (not in any contract) | — | — | — | — |
| Create org unit (secondary button) | `createOrgUnit` POST `/org-units` | CreateScopeNodeRequest | OrgUnit | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types. | opens modal first |

**Data it reads**: `getSsoConfig` (onLoad, Read SSO configuration); `listTenants` (onLoad, List tenants); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `listTenantCells` (onLoad, List a tenant's cells); `listOrgUnits` (onLoad, List scope nodes visible to the session)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`
- → `ADM-007` Module & Feature Entitlement: *Enables the modules the tenant bought*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tenant hierarchy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tenant hierarchy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tenant hierarchy yet. Offers Create org unit (`createOrgUnit`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, planId and the tenant hierarchy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `USER_MANAGE`, which `getSsoConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types. |

#### Permissions

- `getSsoConfig` → `USER_MANAGE` (configure) · staff
- `listOrgUnits` → `SCOPE_VIEW` (read) · staff
- `createOrgUnit` → `SCOPE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `USER_MANAGE`, which `getSsoConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| 3.3.41 | Venue-Specific Policies - System shall support venue-specific access policies. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 3.3.43 | Policy Inheritance - System shall support inheritance of policies across organizational structures. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 7.1.13 | The system shall support permission assignment at company, department, venue, park, attraction, facility, event, sales channel, POS terminal, and product levels. | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.27 | The system shall support management of companies, business units, departments, parks, venues, attractions, facilities, cost centers, and reporting structures. | F&B POS | CONTRACTED | `listOrgUnits` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-006` · status **notStarted** · provenance generated
- Flow F16 *A venue opens for the first time*, step 3: Builds the scope tree → Region, venue, department. **Venue is the configuration floor** (ADR-0018)
- Flow F16 branch at step 3 (recoverable): when The scope tree is built wrongly, Correctable, but `cascade_scope_path` rewrites every descendant and **RLS starts answering a different question**. The riskiest routine operation in the platform.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (80 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save tenant, Create org unit.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `ADM-007`.
- [ ] Every gated control is gated: `SCOPE_MANAGE`, `SCOPE_VIEW`, `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-007` Module & Feature Entitlement

**See module & feature entitlement for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 1 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `USER_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenantCells` reads the population and `getTenantLicences` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (ADM-002) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/module-and-feature-entitlement` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-platform navigation removed 24 August**: BO-074. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Removed 24 August**: generateInvoice, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: createTenant, provisionCell, reactivateTenant, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.

#### Inputs: what the user enters or picks

**Form: Add licence add on** (modal, opened by *Add licence add on*; *Add licence add on* calls `addLicenceAddOn`, *Cancel* sends nothing)

**Collects what `addLicenceAddOn` sends before it is called.** Required: `moduleKey`. Optional: `limitOverrides`, `price`, `validFrom`, `validTo`, `note`. Dismissing sends nothing; the screen behind is unchanged.

`addLicenceAddOn` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

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

**Every tenant** (data table, from `listTenants`)

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

**The selected cell** (detail panel, from `listTenantCells`)

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
| Status | text | not in the schema: `Cell.status` |
| Cloud provider | text | not in the schema: `Cell.cloudProvider` |
| Cloud region | text | not in the schema: `Cell.cloudRegion` |
| API endpoint | text | not in the schema: `Cell.apiEndpoint` |

**The entitlement usage** (detail panel, from `getEntitlementUsage`)

| Shows | Format | Notes |
|---|---|---|
| Metrics | text | not in the schema: `EntitlementUsage.metrics` |
| As at | text | not in the schema: `EntitlementUsage.asAt` |

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

**The subscription** (detail panel, from `getSubscription`)

| Shows | Format | Notes |
|---|---|---|
| Plan ID | text | not in the schema: `Subscription.planId` |
| Plan name | text | not in the schema: `Subscription.planName` |
| Plan version | text | not in the schema: `Subscription.planVersion` |
| Status | text | not in the schema: `Subscription.status` |
| Starts at | text | not in the schema: `Subscription.startsAt` |
| Renews at | text | not in the schema: `Subscription.renewsAt` |
| Cancelled at | text | not in the schema: `Subscription.cancelledAt` |
| Current price | text | not in the schema: `Subscription.currentPrice` |
| Billing period | text | not in the schema: `Subscription.billingPeriod` |

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Add licence add on (primary button) | `addLicenceAddOn` (not in any contract) | — | — | — | — |
| Remove licence add on (destructive button) | `removeLicenceAddOn` (not in any contract) | — | — | — | — |

**Data it reads**: `getTenantLicences` (onLoad, from page inventory); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getSsoConfig` (onLoad, Read SSO configuration); `getSubscription` (onLoad, Read the current subscription); `getTenant` (onLoad, Read a tenant with cells and subscription); `listTenantCells` (onLoad, List a tenant's cells); `listTenants` (onLoad, List tenants)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`
- → `BO-074` Chart of Accounts: *Finance sets the chart of accounts*; calls `getTenantLicences`
- → `ADM-012` Tenant Isolation & Resource Pool: *Tenant Isolation & Resource Pool*; carries `cellId`, `tenantId`

**What opens over it**

- confirmDialog *Remove licence add on*: **Names what `removeLicenceAddOn` changes and what it leaves alone**, in the consequence rather than the verb. A module feature entitlement this affects should be identified in the dialog, not just counted. **Collects what `removeLicenceAddOn` sends before it is called.** Required: `moduleKey` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The module feature entitlement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the module feature entitlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No module feature entitlement yet. Offers Add licence add on (`addLicenceAddOn`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listTenantCells` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getTenantLicences` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getSsoConfig` → `USER_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getTenantLicences` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| 20.4.1 | Marketplace Catalog - System shall provide a marketplace of available modules. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.4.2 | Module Discovery - System shall allow customers to browse modules. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.4.3 | Module Installation - System shall support self-service module installation. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.4.4 | Module Activation - System shall support module activation. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-007` · status **notStarted** · provenance generated
- Flow F16 *A venue opens for the first time*, step 4: Enables the modules the tenant bought → A venue with no F&B does not get F&B screens
- Flow F96 *A tenant is provisioned, licensed and its modules enabled*, step 4: Module & Feature Entitlement. → 15 operations, 15 of them previously unwalked.
- Flow F16 branch at step 4 (recoverable): when A module is enabled that the tenant did not buy, Licensing catches it at use rather than at configuration. **Degrade, never stop** (CF-61) — a gate refusing entry over a licence is worse than running unlicensed.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (81 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-007?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Add licence add on, Remove licence add on.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `BO-074`, `ADM-012`.
- [ ] Every gated control is gated: `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-008` Subscription & Plan Management

**Find subscription & plan management for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 1 · needs the `membership` module |
| Block | Block A · ticket #18060 (APP-SETUP-ADM-008) |
| Who uses it | ticvai staff holding `USER_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPlans` reads the population and `getEntitlementUsage` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `agreementId` (deepLink), `planId` (deepLink), `tenantId` (ADM-002) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/subscription-and-plan-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.

#### Inputs: what the user enters or picks

**Form: Save subscription** (modal, opened by *Save subscription*; *Save subscription* calls `setSubscription`, *Cancel* sends nothing)

**Collects what `setSubscription` sends before it is called.** Required: `planId`. Optional: `planVersion`, `effectiveFrom`, `prorate`, `note`. Dismissing sends nothing; the screen behind is unchanged.

`setSubscription` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Create plan** (modal, opened by *Create plan*; *Create plan* calls `createPlan`, *Cancel* sends nothing)

**Collects what `createPlan` sends before it is called.** Required: `code`, `name`, `cellTier`, `licensedModules`, `limits`, `basePrice`. Optional: `description`, `billingPeriod`, `includesBrandedApp`, `includedAiTokens`. Dismissing sends nothing; the screen behind is unchanged.

`createPlan` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Create plan version** (modal, opened by *Create plan version*; *Create plan version* calls `createPlanVersion`, *Cancel* sends nothing)

**Collects what `createPlanVersion` sends before it is called.** Required: `code`, `name`, `cellTier`, `licensedModules`, `limits`, `basePrice`. Optional: `description`, `billingPeriod`, `includesBrandedApp`, `includedAiTokens`. Dismissing sends nothing; the screen behind is unchanged.

`createPlanVersion` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Generate invoice** (modal, opened by *Generate invoice*; *Generate invoice* calls `generateInvoice`, *Cancel* sends nothing)

**Collects what `generateInvoice` sends before it is called.** Required: `periodStart`, `periodEnd`. Optional: `dryRun`. Dismissing sends nothing; the screen behind is unchanged.

`generateInvoice` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Preview subscription change** (modal, opened by *Preview subscription change*; *Preview subscription change* calls `previewSubscriptionChange`, *Cancel* sends nothing)

**Collects what `previewSubscriptionChange` sends before it is called.** Required: `planId`. Optional: `planVersion`, `effectiveFrom`, `prorate`, `note`. Dismissing sends nothing; the screen behind is unchanged.

`previewSubscriptionChange` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Create partner agreement** (modal, opened by *Create partner agreement*; *Create partner agreement* calls `createPartnerAgreement`, *Cancel* sends nothing)

**Collects what `createPartnerAgreement` sends before it is called.** Required: `partnerId`, `rateMode`, `validFrom`. Optional: `id`, `partnerName`, `status`, `commissionPercent`, `volumeTiers`, `volumeWindow`, `seasonalRates`, `segmentTier`, `brandingAssetId`, `storefrontSubdomain`, `sponsorship`, `netRates` and 17 more. Dismissing sends nothing; the screen behind is unchanged.

`createPartnerAgreement` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Save partner agreement** (modal, opened by *Save partner agreement*; *Save partner agreement* calls `updatePartnerAgreement`, *Cancel* sends nothing)

**Collects what `updatePartnerAgreement` sends before it is called.** Required: `partnerId`, `rateMode`, `validFrom`. Optional: `id`, `partnerName`, `status`, `commissionPercent`, `volumeTiers`, `volumeWindow`, `seasonalRates`, `segmentTier`, `brandingAssetId`, `storefrontSubdomain`, `sponsorship`, `netRates` and 17 more. Dismissing sends nothing; the screen behind is unchanged.

`updatePartnerAgreement` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every plan** (data table, from `listPlans`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | not in the schema: `Plan.code` |
| Name | text | not in the schema: `Plan.name` |
| Description | text | not in the schema: `Plan.description` |
| Cell tier | text | not in the schema: `Plan.cellTier` |
| Licensed modules | text | not in the schema: `Plan.licensedModules` |
| Limits | text | not in the schema: `Plan.limits` |
| Base price | text | not in the schema: `Plan.basePrice` |
| Billing period | text | not in the schema: `Plan.billingPeriod` |
| Includes branded app | text | not in the schema: `Plan.includesBrandedApp` |
| Included AI tokens | text | not in the schema: `Plan.includedAiTokens` |
| ID | text | not in the schema: `Plan.id` |
| Is active | text | not in the schema: `Plan.isActive` |

**Every subscription invoice** (data table, from `listSubscriptionInvoices`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `SubscriptionInvoice.id` |
| Invoice number | text | not in the schema: `SubscriptionInvoice.invoiceNumber` |
| Period start | text | not in the schema: `SubscriptionInvoice.periodStart` |
| Period end | text | not in the schema: `SubscriptionInvoice.periodEnd` |
| Status | text | not in the schema: `SubscriptionInvoice.status` |
| Lines | text | not in the schema: `SubscriptionInvoice.lines` |
| Subtotal | text | not in the schema: `SubscriptionInvoice.subtotal` |
| Tax amount | text | not in the schema: `SubscriptionInvoice.taxAmount` |
| Total | text | not in the schema: `SubscriptionInvoice.total` |
| Plan version used | text | not in the schema: `SubscriptionInvoice.planVersionUsed` |
| Issued at | text | not in the schema: `SubscriptionInvoice.issuedAt` |
| Due at | text | not in the schema: `SubscriptionInvoice.dueAt` |

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

**Every tenant** (data table, from `listTenants`)

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

**Every partner agreement** (data table, from `listPartnerAgreements`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `PartnerAgreement.id` |
| Partner ID | text | not in the schema: `PartnerAgreement.partnerId` |
| Partner name | text | not in the schema: `PartnerAgreement.partnerName` |
| Status | text | not in the schema: `PartnerAgreement.status` |
| Rate mode | text | not in the schema: `PartnerAgreement.rateMode` |
| Commission percent | text | not in the schema: `PartnerAgreement.commissionPercent` |
| Volume tiers | text | not in the schema: `PartnerAgreement.volumeTiers` |
| Volume window | text | not in the schema: `PartnerAgreement.volumeWindow` |
| Seasonal rates | text | not in the schema: `PartnerAgreement.seasonalRates` |
| Segment tier | text | not in the schema: `PartnerAgreement.segmentTier` |
| Branding asset ID | text | not in the schema: `PartnerAgreement.brandingAssetId` |
| Storefront subdomain | text | not in the schema: `PartnerAgreement.storefrontSubdomain` |

**The selected plan** (detail panel, from `getPlan`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | not in the schema: `Plan.code` |
| Name | text | not in the schema: `Plan.name` |
| Description | text | not in the schema: `Plan.description` |
| Cell tier | text | not in the schema: `Plan.cellTier` |
| Licensed modules | text | not in the schema: `Plan.licensedModules` |
| Limits | text | not in the schema: `Plan.limits` |
| Base price | text | not in the schema: `Plan.basePrice` |
| Billing period | text | not in the schema: `Plan.billingPeriod` |
| Includes branded app | text | not in the schema: `Plan.includesBrandedApp` |
| Included AI tokens | text | not in the schema: `Plan.includedAiTokens` |
| ID | text | not in the schema: `Plan.id` |
| Is active | text | not in the schema: `Plan.isActive` |
| Subscriber count | text | not in the schema: `Plan.subscriberCount` |
| Published at | text | not in the schema: `Plan.publishedAt` |

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

**The subscription** (detail panel, from `getSubscription`)

| Shows | Format | Notes |
|---|---|---|
| Plan ID | text | not in the schema: `Subscription.planId` |
| Plan name | text | not in the schema: `Subscription.planName` |
| Plan version | text | not in the schema: `Subscription.planVersion` |
| Status | text | not in the schema: `Subscription.status` |
| Starts at | text | not in the schema: `Subscription.startsAt` |
| Renews at | text | not in the schema: `Subscription.renewsAt` |
| Cancelled at | text | not in the schema: `Subscription.cancelledAt` |
| Current price | text | not in the schema: `Subscription.currentPrice` |
| Billing period | text | not in the schema: `Subscription.billingPeriod` |

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

**The usage report** (detail panel, from `getUsageMetering`)

| Shows | Format | Notes |
|---|---|---|
| Period start | text | not in the schema: `UsageReport.periodStart` |
| Period end | text | not in the schema: `UsageReport.periodEnd` |
| Metrics | text | not in the schema: `UsageReport.metrics` |

**The entitlement usage** (detail panel, from `getEntitlementUsage`)

| Shows | Format | Notes |
|---|---|---|
| Metrics | text | not in the schema: `EntitlementUsage.metrics` |
| As at | text | not in the schema: `EntitlementUsage.asAt` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save subscription (primary button) | `setSubscription` (not in any contract) | — | — | — | — |
| Create plan (secondary button) | `createPlan` (not in any contract) | — | — | — | — |
| Create plan version (secondary button) | `createPlanVersion` (not in any contract) | — | — | — | — |
| Generate invoice (secondary button) | `generateInvoice` (not in any contract) | — | — | — | — |
| Preview subscription change (secondary button) | `previewSubscriptionChange` (not in any contract) | — | — | — | — |
| Create partner agreement (secondary button) | `createPartnerAgreement` (not in any contract) | — | — | — | — |
| Save partner agreement (secondary button) | `updatePartnerAgreement` (not in any contract) | — | — | — | — |

**Data it reads**: `listPlans` (onLoad, from page inventory); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getSsoConfig` (onLoad, Read SSO configuration); `getSubscription` (onLoad, Read the current subscription); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `getUsageMetering` (onLoad, Metered usage for a period); `listSubscriptionInvoices` (onLoad, List subscription invoices); `listTenantCells` (onLoad, List a tenant's cells); `listTenants` (onLoad, List tenants); `listPartnerAgreements` (onLoad, Commercial agreements with B2B partners)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`
- → `ADM-011` Licence & Seat Management: *Licence & Seat Management*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The subscription plan list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the subscription plan untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No subscription plan yet. Offers Create plan (`createPlan`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listPlans` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listPlans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getSsoConfig` → `USER_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listPlans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

46 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.2.2 | Monthly Billing - System shall support monthly subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |
| 20.2.3 | Annual Billing - System shall support annual subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |
| 20.2.1 | Subscription Plans - System shall support configurable subscription plans. | Subscription & Licensing Management | CONTRACTED | `createPlan` |
| 20.4.8 | Module Pricing - System shall support module-specific pricing. | Subscription & Licensing Management | CONTRACTED | `createPlan` |
| 20.7.1 | Subscription Invoicing - System shall generate subscription invoices. | Subscription & Licensing Management | CONTRACTED | `generateInvoice` |
| 20.7.5 | Billing History - System shall maintain billing history. | Subscription & Licensing Management | CONTRACTED | `generateInvoice` |
| 20.5.1 | License Generation - System shall generate subscription licenses. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.2 | License Assignment - System shall assign licenses to tenants. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.3 | License Validation - System shall validate licenses automatically. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.4 | License Enforcement - System shall enforce licensing restrictions. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.5 | License Expiration - System shall support license expiration management. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.6 | Grace Period Management - System shall support configurable grace periods. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| … 34 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-008` · status **notStarted** · provenance generated
- Flow F96 *A tenant is provisioned, licensed and its modules enabled*, step 2: Subscription & Plan Management. → 22 operations, 22 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (118 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save subscription, Create plan, Create plan version, Generate invoice, Preview subscription change, Create partner agreement, Save partner agreement.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `ADM-011`.
- [ ] Every gated control is gated: `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-009` Tenant Billing & Invoicing

**Find tenant billing & invoicing for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 2 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `USER_MANAGE` (1 configure) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSubscriptionInvoices` reads the population and `getEntitlementUsage` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (ADM-002) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/tenant-billing-and-invoicing` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: getUsageMetering, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | text field | — | — | — | — | Sends `?status=` to `listSubscriptionInvoices`. | `listSubscriptionInvoices` ?status |

**Form: Generate invoice** (modal, opened by *Generate invoice*; *Generate invoice* calls `generateInvoice`, *Cancel* sends nothing)

**Collects what `generateInvoice` sends before it is called.** Required: `periodStart`, `periodEnd`. Optional: `dryRun`. Dismissing sends nothing; the screen behind is unchanged.

`generateInvoice` is not in any contract: draw the form greyed and list it in FINDINGS.md.

#### Outputs: what the screen shows and produces

**Shown**

**Every subscription invoice** (data table, from `listSubscriptionInvoices`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `SubscriptionInvoice.id` |
| Invoice number | text | not in the schema: `SubscriptionInvoice.invoiceNumber` |
| Period start | text | not in the schema: `SubscriptionInvoice.periodStart` |
| Period end | text | not in the schema: `SubscriptionInvoice.periodEnd` |
| Status | text | not in the schema: `SubscriptionInvoice.status` |
| Lines | text | not in the schema: `SubscriptionInvoice.lines` |
| Subtotal | text | not in the schema: `SubscriptionInvoice.subtotal` |
| Tax amount | text | not in the schema: `SubscriptionInvoice.taxAmount` |
| Total | text | not in the schema: `SubscriptionInvoice.total` |
| Plan version used | text | not in the schema: `SubscriptionInvoice.planVersionUsed` |
| Issued at | text | not in the schema: `SubscriptionInvoice.issuedAt` |
| Due at | text | not in the schema: `SubscriptionInvoice.dueAt` |

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

**Every tenant** (data table, from `listTenants`)

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

**The selected subscription invoice** (detail panel, from `listSubscriptionInvoices`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `SubscriptionInvoice.id` |
| Invoice number | text | not in the schema: `SubscriptionInvoice.invoiceNumber` |
| Period start | text | not in the schema: `SubscriptionInvoice.periodStart` |
| Period end | text | not in the schema: `SubscriptionInvoice.periodEnd` |
| Status | text | not in the schema: `SubscriptionInvoice.status` |
| Lines | text | not in the schema: `SubscriptionInvoice.lines` |
| Subtotal | text | not in the schema: `SubscriptionInvoice.subtotal` |
| Tax amount | text | not in the schema: `SubscriptionInvoice.taxAmount` |
| Total | text | not in the schema: `SubscriptionInvoice.total` |
| Plan version used | text | not in the schema: `SubscriptionInvoice.planVersionUsed` |
| Issued at | text | not in the schema: `SubscriptionInvoice.issuedAt` |
| Due at | text | not in the schema: `SubscriptionInvoice.dueAt` |
| Paid at | text | not in the schema: `SubscriptionInvoice.paidAt` |

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

**The subscription** (detail panel, from `getSubscription`)

| Shows | Format | Notes |
|---|---|---|
| Plan ID | text | not in the schema: `Subscription.planId` |
| Plan name | text | not in the schema: `Subscription.planName` |
| Plan version | text | not in the schema: `Subscription.planVersion` |
| Status | text | not in the schema: `Subscription.status` |
| Starts at | text | not in the schema: `Subscription.startsAt` |
| Renews at | text | not in the schema: `Subscription.renewsAt` |
| Cancelled at | text | not in the schema: `Subscription.cancelledAt` |
| Current price | text | not in the schema: `Subscription.currentPrice` |
| Billing period | text | not in the schema: `Subscription.billingPeriod` |

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Generate invoice (primary button) | `generateInvoice` (not in any contract) | — | — | — | — |

**Data it reads**: `listSubscriptionInvoices` (onLoad, from page inventory); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getSsoConfig` (onLoad, Read SSO configuration); `getSubscription` (onLoad, Read the current subscription); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `listTenantCells` (onLoad, List a tenant's cells); `listTenants` (onLoad, List tenants); `listCreditNotes` (onLoad, Credit notes beside the invoices)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tenant billing invoicing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tenant billing invoicing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tenant billing invoicing yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status and the tenant billing invoicing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_BILLING_VIEW`, which `listSubscriptionInvoices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getSsoConfig` → `USER_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_BILLING_VIEW`, which `listSubscriptionInvoices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.7.1 | Subscription Invoicing - System shall generate subscription invoices. | Subscription & Licensing Management | CONTRACTED | `generateInvoice` |
| 20.7.5 | Billing History - System shall maintain billing history. | Subscription & Licensing Management | CONTRACTED | `generateInvoice` |
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-009` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (90 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Generate invoice.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-010` Usage Metering

**See usage metering for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 2 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `USER_MANAGE` (1 configure) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenantCells` reads the population and `getUsageMetering` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (ADM-002) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/usage-metering` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

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

**Every tenant** (data table, from `listTenants`)

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

**The selected cell** (detail panel, from `listTenantCells`)

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
| Status | text | not in the schema: `Cell.status` |
| Cloud provider | text | not in the schema: `Cell.cloudProvider` |
| Cloud region | text | not in the schema: `Cell.cloudRegion` |
| API endpoint | text | not in the schema: `Cell.apiEndpoint` |

**The entitlement usage** (detail panel, from `getEntitlementUsage`)

| Shows | Format | Notes |
|---|---|---|
| Metrics | text | not in the schema: `EntitlementUsage.metrics` |
| As at | text | not in the schema: `EntitlementUsage.asAt` |

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

**The usage report** (detail panel, from `getUsageMetering`)

| Shows | Format | Notes |
|---|---|---|
| Period start | text | not in the schema: `UsageReport.periodStart` |
| Period end | text | not in the schema: `UsageReport.periodEnd` |
| Metrics | text | not in the schema: `UsageReport.metrics` |

**Data it reads**: `getUsageMetering` (onLoad, from page inventory); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getSsoConfig` (onLoad, Read SSO configuration); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `listTenantCells` (onLoad, List a tenant's cells); `listTenants` (onLoad, List tenants)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The usage metering list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the usage metering untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No usage metering yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listTenantCells` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getUsageMetering` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getSsoConfig` → `USER_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getUsageMetering` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.6.1 | User Usage Monitoring - System shall monitor active user consumption. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.2 | POS Usage Monitoring - System shall monitor POS utilization. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.3 | API Usage Monitoring - System shall monitor API consumption. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.4 | Storage Usage Monitoring - System shall monitor storage consumption. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.5 | Transaction Usage Monitoring - System shall monitor transaction volumes. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.6 | Attendance Usage Monitoring - System shall monitor attendance volumes. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.7 | Usage Dashboards - System shall provide usage dashboards. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.5.1 | License Generation - System shall generate subscription licenses. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.2 | License Assignment - System shall assign licenses to tenants. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.3 | License Validation - System shall validate licenses automatically. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.4 | License Enforcement - System shall enforce licensing restrictions. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.5 | License Expiration - System shall support license expiration management. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-010` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (75 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-010?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-011` Licence & Seat Management

**See licence & seat management for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 2 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `USER_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenantCells` reads the population and `getEntitlementUsage` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (ADM-002) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/licence-and-seat-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getUsageMetering, listSubscriptionInvoices. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: createTenant, provisionCell, reactivateTenant, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.

#### Inputs: what the user enters or picks

**Form: Add licence add on** (modal, opened by *Add licence add on*; *Add licence add on* calls `addLicenceAddOn`, *Cancel* sends nothing)

**Collects what `addLicenceAddOn` sends before it is called.** Required: `moduleKey`. Optional: `limitOverrides`, `price`, `validFrom`, `validTo`, `note`. Dismissing sends nothing; the screen behind is unchanged.

`addLicenceAddOn` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Preview subscription change** (modal, opened by *Preview subscription change*; *Preview subscription change* calls `previewSubscriptionChange`, *Cancel* sends nothing)

**Collects what `previewSubscriptionChange` sends before it is called.** Required: `planId`. Optional: `planVersion`, `effectiveFrom`, `prorate`, `note`. Dismissing sends nothing; the screen behind is unchanged.

`previewSubscriptionChange` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Save subscription** (modal, opened by *Save subscription*; *Save subscription* calls `setSubscription`, *Cancel* sends nothing)

**Collects what `setSubscription` sends before it is called.** Required: `planId`. Optional: `planVersion`, `effectiveFrom`, `prorate`, `note`. Dismissing sends nothing; the screen behind is unchanged.

`setSubscription` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

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

**Every tenant** (data table, from `listTenants`)

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

**The selected cell** (detail panel, from `listTenantCells`)

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
| Status | text | not in the schema: `Cell.status` |
| Cloud provider | text | not in the schema: `Cell.cloudProvider` |
| Cloud region | text | not in the schema: `Cell.cloudRegion` |
| API endpoint | text | not in the schema: `Cell.apiEndpoint` |

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

**The subscription** (detail panel, from `getSubscription`)

| Shows | Format | Notes |
|---|---|---|
| Plan ID | text | not in the schema: `Subscription.planId` |
| Plan name | text | not in the schema: `Subscription.planName` |
| Plan version | text | not in the schema: `Subscription.planVersion` |
| Status | text | not in the schema: `Subscription.status` |
| Starts at | text | not in the schema: `Subscription.startsAt` |
| Renews at | text | not in the schema: `Subscription.renewsAt` |
| Cancelled at | text | not in the schema: `Subscription.cancelledAt` |
| Current price | text | not in the schema: `Subscription.currentPrice` |
| Billing period | text | not in the schema: `Subscription.billingPeriod` |

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add licence add on (primary button) | `addLicenceAddOn` (not in any contract) | — | — | — | — |
| Preview subscription change (secondary button) | `previewSubscriptionChange` (not in any contract) | — | — | — | — |
| Remove licence add on (destructive button) | `removeLicenceAddOn` (not in any contract) | — | — | — | — |
| Save subscription (secondary button) | `setSubscription` (not in any contract) | — | — | — | — |

**Data it reads**: `getEntitlementUsage` (onLoad, from page inventory); `getSsoConfig` (onLoad, Read SSO configuration); `getSubscription` (onLoad, Read the current subscription); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `listTenantCells` (onLoad, List a tenant's cells); `listTenants` (onLoad, List tenants)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`
- → `PTR-020` Sub-Agent Management: *Sub-Agent Management*
- → `ADM-007` Module & Feature Entitlement: *Module & Feature Entitlement*; carries `tenantId`

**What opens over it**

- confirmDialog *Remove licence add on*: **Names what `removeLicenceAddOn` changes and what it leaves alone**, in the consequence rather than the verb. A licence seat this affects should be identified in the dialog, not just counted. **Collects what `removeLicenceAddOn` sends before it is called.** Required: `moduleKey`, `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The licence seat list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the licence seat untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No licence seat yet. Offers Add licence add on (`addLicenceAddOn`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listTenantCells` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getEntitlementUsage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getSsoConfig` → `USER_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getEntitlementUsage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.4.1 | Marketplace Catalog - System shall provide a marketplace of available modules. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.4.2 | Module Discovery - System shall allow customers to browse modules. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.4.3 | Module Installation - System shall support self-service module installation. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.4.4 | Module Activation - System shall support module activation. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.4.5 | Module Deactivation - System shall support module deactivation. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.5.1 | License Generation - System shall generate subscription licenses. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.2 | License Assignment - System shall assign licenses to tenants. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.3 | License Validation - System shall validate licenses automatically. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.4 | License Enforcement - System shall enforce licensing restrictions. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.5 | License Expiration - System shall support license expiration management. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.6 | Grace Period Management - System shall support configurable grace periods. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.7 | License Renewal Management - System shall support license renewals. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-011` · status **notStarted** · provenance generated
- Flow F105 *A rate limit is set and a developer hits it*, step 2: Licence & Seat Management. → 15 operations, 15 of them previously unwalked.
- Flow F96 *A tenant is provisioned, licensed and its modules enabled*, step 3: Licence & Seat Management. → 15 operations, 15 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (81 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-011?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add licence add on, Preview subscription change, Remove licence add on, Save subscription.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `PTR-020`, `ADM-007`.
- [ ] Every gated control is gated: `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-012` Tenant Isolation & Resource Pool

**Work with tenant isolation & resource pool for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 1 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `USER_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenantCells` reads the population and `getEntitlementUsage` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink), `tenantId` (ADM-002) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/tenant-isolation-and-resource-pool` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.

#### Inputs: what the user enters or picks

**Form: Provision cell** (modal, opened by *Provision cell*; *Provision cell* calls `provisionCell`, *Cancel* sends nothing)

**Collects what `provisionCell` sends before it is called.** Required: `regionId`, `countryCode`, `tier`. Optional: `cloudProvider`, `cloudRegion`, `clientHostedEndpoint`. Dismissing sends nothing; the screen behind is unchanged.

`provisionCell` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

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

**Every tenant** (data table, from `listTenants`)

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

**The selected cell** (detail panel, from `listTenantCells`)

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
| Status | text | not in the schema: `Cell.status` |
| Cloud provider | text | not in the schema: `Cell.cloudProvider` |
| Cloud region | text | not in the schema: `Cell.cloudRegion` |
| API endpoint | text | not in the schema: `Cell.apiEndpoint` |

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

**The entitlement usage** (detail panel, from `getEntitlementUsage`)

| Shows | Format | Notes |
|---|---|---|
| Metrics | text | not in the schema: `EntitlementUsage.metrics` |
| As at | text | not in the schema: `EntitlementUsage.asAt` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Provision cell (primary button) | `provisionCell` (not in any contract) | — | — | — | — |

**Data it reads**: `getEntitlementUsage` (onLoad, Usage against licensed limits); `getSsoConfig` (onLoad, Read SSO configuration); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `listTenantCells` (onLoad, List a tenant's cells); `listTenants` (onLoad, List tenants); `getCellCapacity` (onLoad, Load against headroom)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`
- → `ADM-006` Tenant Hierarchy Explorer: *Builds the scope tree*; carries `tenantId`
- → `ADM-013` Tenant Performance Monitor: *Tenant Performance Monitor*; carries `cellId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tenant isolation resource list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tenant isolation resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tenant isolation resource yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listTenantCells` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getEntitlementUsage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getSsoConfig` → `USER_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getEntitlementUsage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-012` · status **notStarted** · provenance generated
- Flow F16 *A venue opens for the first time*, step 2: Provisions or assigns a cell → **Region decides the cell** — data residency is not a preference (ADR-0001)
- Flow F96 *A tenant is provisioned, licensed and its modules enabled*, step 5: Tenant Isolation & Resource Pool. → 16 operations, 16 of them previously unwalked.
- Flow F97 *A cell is capacity-checked and a tenant is placed on it*, step 1: Tenant Isolation & Resource Pool. → 16 operations, 16 of them previously unwalked.
- Flow F16 branch at step 2 (requiresStaff): when The region has no cell and residency forbids an existing one, A new cell is provisioned, which takes time and money. **The commercial decision is upstream of the technical one** — a venue in a new jurisdiction is a new cost line.
- Flow F97 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.
- ADR-0001 *Cell architecture — one tenant per jurisdiction* (`docs/adr/0001-cell-architecture-one-tenant-per-jurisdiction.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (79 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-012?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Provision cell.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `ADM-006`, `ADM-013`.
- [ ] Every gated control is gated: `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-015` API Rate Limit & Quota Management

**See api rate limit & quota management for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `DEVELOPER_ADMIN`, `DEVELOPER_VIEW`, `USER_MANAGE` (2 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenantCells` reads the population and `getTenantLicences` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (ADM-002), `requestId` (navigation) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/api-rate-limit-and-quota-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant. **`setApiQuota` wired 24 August.** This screen is named *API Rate Limit & Quota Management* and **declared no quota operation at all** — it carried nine subscription operations and six tenant-lifecycle ones instead. **The screen for the job could not do the job**, and only writing F105 against it surfaced that.

**Known gaps.**  Open: Blocked — Developer & API workshop

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApiUsage` ?from |
| To | date picker | — | — | `getApiUsage` ?to |
| Status | radio group | — | Pending · Approved · Rejected · Withdrawn | `listProductionAccessRequests` ?status |
| Client | picker: choose a client | — | — | `listApiAnomalies` ?clientId |
| From | date and time picker | — | — | `listApiAnomalies` ?from |

**Form: Save API quota** (modal, opened by *Save API quota*; *Save API quota* calls `setApiQuota`, *Cancel* sends nothing)

**Collects what `setApiQuota` sends before it is called.** Required: `clientId`, `sustainedPerMinute`. Optional: `id`, `burstPerSecond`, `dailyCap`, `perOperationOverrides`, `onBreach`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Client `clientId` | picker: choose a client | required | — | — | shows names, sends the id | — | `setApiQuota` body |
| Sustained per minute `sustainedPerMinute` | number field | required | — | — | — | — | `setApiQuota` body |
| Burst per second `burstPerSecond` | number field | optional | — | — | — | Separate from the sustained rate, because a nightly sync is a legitimate spike and a flat per-second limit either blocks it or permits the flood it was meant to stop. | `setApiQuota` body |
| Daily cap `dailyCap` | number field | optional | — | — | — | — | `setApiQuota` body |
| Per operation overrides `perOperationOverrides` | key and value settings | optional | — | — | — | Availability checks and order creation deserve different limits — one is cheap and polled, the other is expensive and rare. | `setApiQuota` body |
| On breach `onBreach` | segmented control | optional | Throttle | Throttle · Reject · Queue | — | — | `setApiQuota` body |

**Form: Decide production access** (modal, opened by *Decide production access*; *Decide production access* calls `decideProductionAccess`, *Cancel* sends nothing)

**Collects what `decideProductionAccess` sends before it is called.** Required: `decision`. Optional: `reason` (required to reject, in words the developer can act on), `scopes` (narrow only), `credentialTtlDays`. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | segmented control | required | — | Approve · Reject | — | — | `decideProductionAccess` body |
| Reason `reason` | text area | optional | — | max length 1000 | — | — | `decideProductionAccess` body |
| Scopes `scopes` | list of values (chips) | optional | — | — | — | Narrow the requested scopes. Never widens them. | `decideProductionAccess` body |
| Credential ttl days `credentialTtlDays` | number field (days) | optional | 365 | min 1; max 730 | — | — | `decideProductionAccess` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already decided (`already-decided`), or the listing's certification lapsed since the request (`certification-required`).; 422 `reject` without a `reason`.

**Form: Save anomaly rule** (modal, opened by *Save anomaly rule*; *Save anomaly rule* calls `setApiAnomalyRule`, *Cancel* sends nothing)

**Collects what `setApiAnomalyRule` sends before it is called.** Required: `ruleKey`, `measure`, `comparison`, `threshold`, `action`. Optional: `clientId`, `windowMinutes`, `isActive`. A `suspend` action is named in the form: it stops the client until someone reactivates it.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rule key `ruleKey` | text field | required | — | — | — | — | `setApiAnomalyRule` body |
| Client `clientId` | picker: choose a client | optional | — | — | shows names, sends the id | Null applies to every client of the tenant. | `setApiAnomalyRule` body |
| Measure `measure` | radio group | required | — | Calls per minute · Client error share · Allow list refusals · Unusual operations · Auth failures | — | — | `setApiAnomalyRule` body |
| Comparison `comparison` | segmented control | required | — | Above baseline multiple · Above fixed | — | `aboveBaselineMultiple`: above `threshold` x the same hour over the last four weeks. | `setApiAnomalyRule` body |
| Threshold `threshold` | number field | required | — | — | — | — | `setApiAnomalyRule` body |
| Window minutes `windowMinutes` | number field (minutes) | optional | 5 | min 1 | — | — | `setApiAnomalyRule` body |
| Action `action` | segmented control | required | Flag | Flag · Throttle · Suspend | — | — | `setApiAnomalyRule` body |
| Is active `isActive` | toggle | optional | on | — | — | — | `setApiAnomalyRule` body |

#### Outputs: what the screen shows and produces

**Shown**

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

**Every tenant** (data table, from `listTenants`)

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

**Every API client** (data table, from `listApiClients`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Developer | the name it points at, never the id | — |
| Name | text | — |
| Client | text | — |
| Environment | chip: Sandbox, Production | Bound to one, stated on the object rather than by naming convention. A key that works in both is a key somebody will use in the wrong one. |
| Scopes | list or chips (count when long) | Resolved against the tenant's licence at token issue (13.3.24). A scope granted here and not licensed there produces no token — and the … |
| Allowed tenants | list or chips (count when long) | 13.1.46. Which tenants this client may act for. |
| Ip allow list | list or chips (count when long) | 13.1.38. Required on a production client (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the … |
| Status | chip: Active, Suspended, Revoked | — |
| Last used at | 1 Oct 2026, 14:30 | A credential unused for a year is a credential nobody will notice being stolen. |

**Production access requests, pending first** (data table, from `listProductionAccessRequests`): **Production keys only after certification** (17 September minutes, M17-06). The queue a TICVAI administrator works: each request names the certified integration, the tenants, the module scopes and the IP allow-list. Approving issues a new production client; the sandbox key is never promoted.

| Shows | Format | Notes |
|---|---|---|
| Developer | the name it points at, never the id | — |
| Listing | the name it points at, never the id | — |
| Scopes | list or chips (count when long) | — |
| Allowed tenants | list or chips (count when long) | — |
| Ip allow list | list or chips (count when long) | — |
| Status | chip: Pending, Approved, Rejected, Withdrawn | — |
| Requested at | 1 Oct 2026, 14:30 | — |

**Flagged API traffic** (data table, from `listApiAnomalies`): **Abnormal volume is flagged, not only throttled** (M17-07): calls above the client's own baseline, refusals from outside the allow-list, calls to operations it never uses.

| Shows | Format | Notes |
|---|---|---|
| Client | the name it points at, never the id | — |
| Rule key | text | — |
| Measure | text | — |
| Observed | 1,234.5 | — |
| Baseline | 1,234.5 | — |
| Action taken | chip: Flag, Throttle, Suspend | — |
| Detected at | 1 Oct 2026, 14:30 | — |

**The selected cell** (detail panel, from `listTenantCells`)

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
| Status | text | not in the schema: `Cell.status` |
| Cloud provider | text | not in the schema: `Cell.cloudProvider` |
| Cloud region | text | not in the schema: `Cell.cloudRegion` |
| API endpoint | text | not in the schema: `Cell.apiEndpoint` |

**The entitlement usage** (detail panel, from `getEntitlementUsage`)

| Shows | Format | Notes |
|---|---|---|
| Metrics | text | not in the schema: `EntitlementUsage.metrics` |
| As at | text | not in the schema: `EntitlementUsage.asAt` |

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

**The API usage** (detail panel, from `getApiUsage`)

| Shows | Format | Notes |
|---|---|---|
| Total calls | 1,234 | — |
| Success rate | 12.5% | — |
| Client error rate | 12.5% | 4xx — the integrator's problem. Separated because a single error rate lets both sides blame the other. |
| Server error rate | 12.5% | 5xx — TICVAI's problem. |
| P50 latency ms | 1,234.5 | — |
| P95 latency ms | 1,234.5 | — |
| P99 latency ms | 1,234.5 | — |
| Quota breaches | 1,234 | — |
| By operation | list or chips (count when long) | — |

**The licence position** (detail panel, from `getTenantLicences`)

| Shows | Format | Notes |
|---|---|---|
| Plan ID | text | not in the schema: `LicencePosition.planId` |
| Licensed modules | text | not in the schema: `LicencePosition.licensedModules` |
| Limits | text | not in the schema: `LicencePosition.limits` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save API quota (primary button) | `setApiQuota` PUT `/api-quotas` | ApiQuota | ApiQuota | — | opens modal first |
| Decide production access (primary button) | `decideProductionAccess` POST `/production-access-requests/{requestId}/decide` | inline | ProductionAccessRequest | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already decided (`already-decided`), or the listing's certification lapsed since the request … | opens modal first |
| Save anomaly rule (secondary button) | `setApiAnomalyRule` PUT `/api-anomaly-rules` | ApiAnomalyRule | ApiAnomalyRule | — | opens modal first |

**Data it reads**: `getTenantLicences` (onLoad, What a tenant is licensed to use); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getSsoConfig` (onLoad, Read SSO configuration); `getTenant` (onLoad, Read a tenant with cells and subscription); `listTenantCells` (onLoad, List a tenant's cells); `listTenants` (onLoad, List tenants); `getApiUsage` (onLoad, Calls, errors, latency and success rate); `listApiClients` (onLoad, Registered clients for this developer); `listProductionAccessRequests` (onLoad, The production key approval queue); `listApiAnomalies` (onLoad, Flagged abnormal API traffic)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`
- → `ADM-011` Licence & Seat Management: *Licence & Seat Management*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The api rate limit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the api rate limit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No api rate limit yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listTenantCells` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getTenantLicences` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already decided (`already-decided`), or the listing's certification lapsed since the request (`certification-required`).; 422 `reject` without a `reason`. |

#### Permissions

- `getSsoConfig` → `USER_MANAGE` (configure) · staff
- `setApiQuota` → `DEVELOPER_ADMIN` (configure) · staff
- `getApiUsage` → `DEVELOPER_VIEW` (read) · staff, partner
- `listApiClients` → `DEVELOPER_VIEW` (read) · staff, partner
- `listProductionAccessRequests` → `DEVELOPER_VIEW` (read) · staff, partner
- `decideProductionAccess` → `DEVELOPER_ADMIN` (configure) · staff
- `listApiAnomalies` → `DEVELOPER_VIEW` (read) · staff, partner
- `setApiAnomalyRule` → `DEVELOPER_ADMIN` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getTenantLicences` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

33 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| 13.1.12 | Client Secret Management - System shall support client secret management. | Developer & API Management | CONTRACTED | `decideProductionAccess` |
| 13.1.39 | API Audit Logs - System shall maintain API audit logs. | Developer & API Management | CONTRACTED | `setApiAnomalyRule` |
| 2.7.52 | System shall allow approved B2B partners to request, generate, manage, rotate, and revoke API credentials. Access shall be restricted by partner permissions, products, quotas, rate limits, IP … | Ticketing Sales | CONTRACTED | data `ApiClient` |
| 7.1.25 | The system shall support dedicated API users, integration users, service accounts, API keys, credential rotation, expiry controls, IP restrictions, and audit logging. | F&B POS | CONTRACTED | data `ApiClient` |
| … 21 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Abnormal API volume is flagged, not only throttled (calls above the client's baseline, refusals outside the allow-list, calls to unused operations); a production access request requires at least one IP allow-list address. *(agreed · MoM 17 Sep 2026, M17-07 · DI-928)*
- Production access status is shown: sandbox only, requested (pending), approved, or rejected with the reason. Production keys only after certification; the request form says a new production key is issued and the sandbox key stays sandbox. *(agreed · MoM 17 Sep 2026, M17-06 · DI-927)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-015` · status **notStarted** · provenance generated
- Flow F105 *A rate limit is set and a developer hits it*, step 1: API Rate Limit & Quota Management. → 15 operations, 15 of them previously unwalked.
- Flow F105 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (105 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save API quota, Decide production access, Save anomaly rule.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `ADM-011`.
- [ ] Every gated control is gated: `DEVELOPER_ADMIN`, `DEVELOPER_VIEW`, `USER_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createOrgUnit": {"method":"POST","path":"/org-units","contract":"tenancy","summary":"Create a scope node","permission":"SCOPE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"brand","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateScopeNodeRequest","responds":"OrgUnit"},
"decideProductionAccess": {"method":"POST","path":"/production-access-requests/{requestId}/decide","contract":"public-api","summary":"Approve or reject production access","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductionAccessRequest"},
"getApiUsage": {"method":"GET","path":"/api-usage","contract":"public-api","summary":"Calls, errors, latency and success rate","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"ApiUsageSummary"},
"getSsoConfig": {"method":"GET","path":"/tenants/sso-config","contract":"identity","summary":"Read SSO configuration","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SsoProviderConfig"},
"listApiAnomalies": {"method":"GET","path":"/api-anomalies","contract":"public-api","summary":"Flagged API traffic","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"clientId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listApiClients": {"method":"GET","path":"/api-clients","contract":"public-api","summary":"Registered clients for this developer","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ApiClient"},
"listOrgUnits": {"method":"GET","path":"/org-units","contract":"tenancy","summary":"List scope nodes visible to the session","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"under","in":"query","required":null},{"name":"level","in":"query","required":null},{"name":"includeInactive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductionAccessRequests": {"method":"GET","path":"/production-access-requests","contract":"public-api","summary":"Production access requests, pending first","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"setApiAnomalyRule": {"method":"PUT","path":"/api-anomaly-rules","contract":"public-api","summary":"When API traffic is flagged as abnormal","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApiAnomalyRule","responds":"ApiAnomalyRule"},
"setApiQuota": {"method":"PUT","path":"/api-quotas","contract":"public-api","summary":"Rate limits and throttling per client","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApiQuota","responds":"ApiQuota"},
"setSsoConfig": {"method":"PUT","path":"/tenants/sso-config","contract":"identity","summary":"Configure an identity provider","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SsoProviderConfig","responds":"SsoProviderConfig"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApiAnomaly": {"type":"object","x-ticvai-persistence":"control.api_anomaly","description":"One flagged breach of an anomaly rule (M17-07).","required":["id","ruleKey","clientId","detectedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"ruleKey":{"type":"string"},"clientId":{"type":"string","format":"uuid","x-ticvai-references":"control.api_client"},"measure":{"type":"string"},"observed":{"type":"number"},"baseline":{"type":"number","nullable":true},"actionTaken":{"type":"string","enum":["flag","throttle","suspend"]},"detectedAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"ApiAnomalyRule": {"type":"object","x-ticvai-persistence":"control.api_anomaly_rule","description":"**When API traffic is abnormal** (17 September minutes, M17-07). Platform defaults ship for every tenant; TICVAI tightens them per tenant or per client.\n","required":["ruleKey","measure","comparison","threshold","action"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"ruleKey":{"type":"string"},"clientId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"control.api_client","description":"Null applies to every client of the tenant."},"measure":{"type":"string","enum":["callsPerMinute","clientErrorShare","allowListRefusals","unusualOperations","authFailures"]},"comparison":{"type":"string","enum":["aboveBaselineMultiple","aboveFixed"],"description":"`aboveBaselineMultiple`: above `threshold` x the same hour over the last four weeks."},"threshold":{"type":"number"},"windowMinutes":{"type":"integer","minimum":1,"default":5},"action":{"type":"string","enum":["flag","throttle","suspend"],"default":"flag"},"isActive":{"type":"boolean","default":true}}},
"ApiClient": {"type":"object","x-ticvai-persistence":"control.api_client","description":"CF-135a. **The one credential model.** 2.7.52, 7.1.25 and 7.1.30 each asserted their own, so a partner API key, a POS integration credential and a webstore credential were three unrelated things with three lifecycles.\n","required":["id","developerId","name","environment","scopes","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid"},"name":{"type":"string"},"clientId":{"type":"string","readOnly":true},"environment":{"type":"string","enum":["sandbox","production"],"description":"**Bound to one, stated on the object rather than by naming convention.** A key that works in both is a key somebody will use in the wrong one.\n"},"scopes":{"type":"array","description":"**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing. **Module scopes** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, one of `listApiScopes`.\n","items":{"type":"string","pattern":"^[a-zA-Z]+\\.(read|write)$"}},"issuedBy":{"type":"string","enum":["partner","ticvai"],"readOnly":true,"description":"Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`.\n"},"certificationListingId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"control.integration_listing","description":"For a production client, the certified integration it was issued against."},"credentialTtlDays":{"type":"integer","minimum":1,"maximum":730,"nullable":true,"description":"Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry)."},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the key stops working unless rotated. No token is issued after it."},"allowedTenantIds":{"type":"array","description":"13.1.46. **Which tenants this client may act for.** A developer integrating for one venue must not reach another, and a client with an empty list reaches none.\n","items":{"type":"string","format":"uuid"}},"ipAllowList":{"type":"array","description":"13.1.38. **Required on a production client** (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the internet); optional in the sandbox. CIDR ranges. Checked at token issue and on every call.\n","items":{"type":"string"}},"status":{"type":"string","enum":["active","suspended","revoked"],"readOnly":true},"lastUsedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**A credential unused for a year is a credential nobody will notice being stolen.**\n"}}},
"ApiQuota": {"type":"object","x-ticvai-persistence":"control.api_limit","description":"13.1.36 and 13.1.37. **A quota protects the venue, not the developer.**\n","required":["clientId","sustainedPerMinute"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"clientId":{"type":"string","format":"uuid"},"sustainedPerMinute":{"type":"integer"},"burstPerSecond":{"type":"integer","description":"**Separate from the sustained rate**, because a nightly sync is a legitimate spike and a flat per-second limit either blocks it or permits the flood it was meant to stop.\n"},"dailyCap":{"type":"integer","nullable":true},"perOperationOverrides":{"type":"object","additionalProperties":{"type":"integer"},"description":"**Availability checks and order creation deserve different limits** — one is cheap and polled, the other is expensive and rare.\n"},"onBreach":{"type":"string","enum":["throttle","reject","queue"],"default":"throttle"}}},
"ApiUsageSummary": {"type":"object","description":"13.1.16 to 13.1.20, 13.1.41 to 13.1.45. **One endpoint because they are one question asked five ways.**\n","properties":{"totalCalls":{"type":"integer"},"successRate":{"type":"number"},"clientErrorRate":{"type":"number","description":"**4xx — the integrator's problem.** Separated because a single error rate lets both sides blame the other.\n"},"serverErrorRate":{"type":"number","description":"5xx — TICVAI's problem."},"p50LatencyMs":{"type":"number"},"p95LatencyMs":{"type":"number"},"p99LatencyMs":{"type":"number"},"quotaBreaches":{"type":"integer"},"byOperation":{"type":"array","items":{"type":"object","properties":{"operationId":{"type":"string"},"calls":{"type":"integer"},"errorRate":{"type":"number"}}}}}},
"CreateScopeNodeRequest": {"type":"object","required":["level","parentId","code","name"],"properties":{"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","description":"Required for every level except tenant, which the cell creates at provisioning."},"code":{"type":"string","maxLength":64,"pattern":"^[a-z0-9_]+$","description":"Becomes the final ltree segment. Immutable once created."},"name":{"type":"string","maxLength":200}}},
"OrgUnit": {"x-ticvai-persistence":"platform.scope","type":"object","required":["id","level","path","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","nullable":true},"path":{"type":"string","description":"Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"isActive":{"type":"boolean","description":"False causes every permission query at or beneath this node to resolve to DENY.\n"},"childCount":{"type":"integer","minimum":0}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE"]},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"ProductionAccessRequest": {"type":"object","x-ticvai-persistence":"control.production_access_request","description":"**A developer's request for production keys** (17 September minutes, M17-06): sandbox, then certification, then production.\n","required":["id","developerId","sandboxClientId","listingId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid","readOnly":true},"sandboxClientId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"control.api_client"},"listingId":{"type":"string","format":"uuid","x-ticvai-references":"control.integration_listing"},"scopes":{"type":"array","items":{"type":"string"}},"allowedTenantIds":{"type":"array","items":{"type":"string","format":"uuid"}},"ipAllowList":{"type":"array","items":{"type":"string"}},"note":{"type":"string","nullable":true},"status":{"type":"string","enum":["pending","approved","rejected","withdrawn"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"reason":{"type":"string","nullable":true,"readOnly":true},"productionClientId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"control.api_client"},"requestedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ScopeLevel": {"type":"string","description":"**The eight organisational levels, plus `subject`.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition of the eight levels and this mirrors them so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n\n**`subject` is the one value tenancy does not have, and it is not a level.** It is here because `check-package` reads this enum as the closed vocabulary for `x-ticvai-scope-level`, and some operations act on one guest's own resources, which sit in no node of the venue hierarchy. So `subject` is valid as an operation's scope level and never as a `ScopeRef.level`: every `ScopeRef` is a row of `platform.scope`, and those carry one of the eight.\n","enum":["tenant","brand","region","venue","department","subDepartment","workstation","outlet","subject"]},
"SsoGroupMapping": {"x-ticvai-persistence":"identity.sso_group_mapping","type":"object","required":["externalGroup","roleId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — the response returned the external group, the role and the scope, which is everything a caller needs and not the row own identity.\n**(provider, external_group) is unique and would serve**, but a mapping is edited and revoked by an administrator, and **a row addressed by the values it holds cannot be corrected** — changing the group means deleting a mapping and creating another, which loses who granted it and when.\n"},"externalGroup":{"type":"string"},"roleId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"Scope the mapped role is granted at."}}},
"SsoProtocol": {"type":"string","enum":["oidc","saml2"]},
"SsoProviderConfig": {"x-ticvai-persistence":"identity.sso_provider","type":"object","required":["id","displayName","protocol","groupMappings"],"properties":{"id":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"protocol":{"$ref":"#/components/schemas/SsoProtocol"},"metadataUrl":{"type":"string","nullable":true},"issuer":{"type":"string","nullable":true},"clientId":{"type":"string","nullable":true},"clientSecretRef":{"type":"string","nullable":true,"description":"Key vault reference. The secret itself is never returned."},"groupMappings":{"type":"array","minItems":1,"description":"**A group with no mapping grants nothing.** No default role, ever — otherwise the identity provider becomes a way to mint access nobody configured.\n","items":{"$ref":"#/components/schemas/SsoGroupMapping"}},"autoProvisionPrincipals":{"type":"boolean","default":false,"description":"Create a principal on first successful sign-in."},"isEnforced":{"type":"boolean","default":false},"isActive":{"type":"boolean"}}}
}
```
