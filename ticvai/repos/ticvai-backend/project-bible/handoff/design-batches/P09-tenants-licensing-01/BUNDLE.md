# P09-tenants-licensing-01 — P09 · Tenants & Licensing

**9 screens · 38 operations · 44 schemas · 14 permissions**

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

- **Every control that can be refused must be gated.** 14 permissions apply here:
  `DEVELOPER_ADMIN, DEVELOPER_VIEW, PLATFORM_BILLING_MANAGE, PLATFORM_BILLING_VIEW, PLATFORM_CELL_MANAGE, PLATFORM_CELL_VIEW, PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_MANAGE, PLATFORM_TENANT_TERMINATE, PLATFORM_TENANT_VIEW, SCOPE_MANAGE`…. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `ADM-005` | Tenant Directory | A | 57 | 48 | 7 | 17 | 0 | 0 | — | notStarted (generated) |
| `ADM-006` | Tenant Hierarchy Explorer | B | 16 | 45 | 7 | 15 | 0 | 0 | — | notStarted (generated) |
| `ADM-007` | Module & Feature Entitlement | B | 12 | 42 | 6 | 14 | 0 | 0 | — | notStarted (generated) |
| `ADM-008` | Subscription & Plan Management | A | 83 | 57 | 6 | 24 | 0 | 0 | — | notStarted (generated) |
| `ADM-009` | Tenant Billing & Invoicing | B | 4 | 42 | 6 | 11 | 0 | 0 | — | notStarted (generated) |
| `ADM-010` | Usage Metering | B | 0 | 36 | 6 | 16 | 0 | 0 | — | notStarted (generated) |
| `ADM-011` | Licence & Seat Management | B | 17 | 42 | 6 | 16 | 0 | 6 | — | notStarted (generated) |
| `ADM-012` | Tenant Isolation & Resource Pool | B | 6 | 40 | 6 | 9 | 0 | 0 | — | notStarted (generated) |
| `ADM-015` | API Rate Limit & Quota Management | B | 24 | 50 | 7 | 33 | 2 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-005` Tenant Directory

**Find any tenant and act on its account, status, licences and cells.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 1 · needs the `core` module |
| Block | Block A · task APP-SETUP-ADM-005 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_MANAGE`, `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_TERMINATE`, `PLATFORM_TENANT_VIEW`… (3 configure, 2 read, 2 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenants` reads the population and `getEntitlementUsage` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (ADM-002) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/tenant-directory` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The platform operator's tenant list: find a tenant, see its plan, cells, venues, status and licence position, and act on it (create, amend, suspend, reactivate, terminate, license an add-on, provision a cell, configure its SSO) without opening a separate page. Actions on the tenant record itself are control-plane acts; configuring the tenant's SSO happens inside the tenant and needs a platform-staff grant.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun offers Add licence add on as the create action. (CHG-SBO-011); requiresModule is 'membership'. (CHG-SBO-003); formSetSsoConfig asks the person for id. (CHG-SBO-004); Tables show every schema field, plumbing included: 'Every tenant' drop id, planId, accountManagerPrincipalId; 'Every cell' drop id … (CHG-SBO-004).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is opening a grant needed for getSsoConfig/setSsoConfig only, or does TICVAI configure tenant SSO at all (versus the tenant's own admin in Venue Management)?** → Drawn default accepted: Draw SSO configuration behind the grant on this screen, and the same card on the tenant's identity settings. *(decided by Chinmay, 2026-10-02; DEC-094 / CHG-NOTE-005)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Status | radio group | optional | — | Onboarding · Active · Suspended · Terminating · Terminated | — | Sends `?status=` to `listTenants`. | `listTenants` ?status |
| Plan id | picker: choose a plan (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?planId=` to `listTenants`. | `listTenants` ?planId |

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

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Module key `moduleKey` | text field | required | — | — | — | — | `addLicenceAddOn` body |
| Limit overrides `limitOverrides` | repeatable rows | optional | — | — | — | — | `addLicenceAddOn` body |
| Metric `limitOverrides[].metric` | select | required | — | Venues · Workstations · Active users · Devices · Branded apps · AI tokens · API calls · Storage gb · Transactions · Guest profiles | — | — | `addLicenceAddOn` body |
| Limit `limitOverrides[].limit` | number field | required | — | — | — | Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure `limit_value`. | `addLicenceAddOn` body |
| Overage allowed `limitOverrides[].overageAllowed` | toggle | optional | off | — | — | — | `addLicenceAddOn` body |
| Overage unit price `limitOverrides[].overageUnitPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `addLicenceAddOn` body |
| Price `price` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `addLicenceAddOn` body |
| Valid from `validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `addLicenceAddOn` body |
| Valid to `validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `addLicenceAddOn` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `addLicenceAddOn` body |

**Form: Create tenant** (modal, opened by *Create tenant*; *Create tenant* calls `createTenant`, *Cancel* sends nothing)

**Collects what `createTenant` sends before it is called.** Required: `code`, `name`, `billingEmail`. Optional: `billingAddress`, `accountManagerPrincipalId`, `planId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; pattern `^[a-z0-9-]+$` | — | — | `createTenant` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createTenant` body |
| Billing email `billingEmail` | text field | required | — | — | — | — | `createTenant` body |
| Billing address `billingAddress` | text area | optional | — | max length 500 | — | — | `createTenant` body |
| Account manager principal `accountManagerPrincipalId` | picker: choose an account manager principal | optional | — | — | shows names, sends the id | — | `createTenant` body |
| Plan `planId` | picker: choose a plan | optional | — | — | shows names, sends the id | — | `createTenant` body |

Errors to draw in the form: 409 Code already in use

**Form: Provision cell** (modal, opened by *Provision cell*; *Provision cell* calls `provisionCell`, *Cancel* sends nothing)

**Collects what `provisionCell` sends before it is called.** Required: `regionId`, `countryCode`, `tier`. Optional: `cloudProvider`, `cloudRegion`, `clientHostedEndpoint`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Region `regionId` | picker: choose a region | required | — | — | shows names, sends the id | — | `provisionCell` body |
| Country code `countryCode` | text field | required | — | pattern `^[A-Z]{2}$` | — | Determines the jurisdiction. Placement must be within it — this is enforced, not trusted. | `provisionCell` body |
| Tier `tier` | radio group | required | — | Shared · Dedicated · Isolated · Client hosted | — | — | `provisionCell` body |
| Cloud provider `cloudProvider` | text field | optional | — | — | — | — | `provisionCell` body |
| Cloud region `cloudRegion` | text field | optional | — | — | — | — | `provisionCell` body |
| Client hosted endpoint `clientHostedEndpoint` | text field | optional | — | — | — | Required for `clientHosted`, where no in-region cloud exists. | `provisionCell` body |

Errors to draw in the form: 400 Placement is outside the region's jurisdiction, or the target cloud has no region in that country.; 409 A cell already exists for this region

**Form: Save SSO config** (modal, opened by *Save SSO config*; *Save SSO config* calls `setSsoConfig`, *Cancel* sends nothing)

**Collects what `setSsoConfig` sends before it is called.** Required: `displayName`, `protocol`, `groupMappings`. Optional: `metadataUrl`, `issuer`, `clientId`, `clientSecretRef`, `autoProvisionPrincipals`, `isEnforced`, `isActive`. **Not asked:** `id` is a client UUIDv7 generated silently (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged.

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

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateTenant` body |
| Billing email `billingEmail` | text field | optional | — | — | — | — | `updateTenant` body |
| Billing address `billingAddress` | text area | optional | — | max length 500 | — | — | `updateTenant` body |
| Account manager principal `accountManagerPrincipalId` | picker: choose an account manager principal | optional | — | — | shows names, sends the id | — | `updateTenant` body |

Errors to draw in the form: 409 The tenant is terminated (`tenant-terminated`, audit R214 (3)).

**Sent by *Remove licence add on*** (`removeLicenceAddOn`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Module key `moduleKey` | text field | required | — | — | — | — | `removeLicenceAddOn` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `removeLicenceAddOn` body |

**Sent by *Suspend tenant*** (`suspendTenant`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Mode `mode` | segmented control | required | — | Read only · No new sales · Full lockout | — | Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets. | `suspendTenant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `suspendTenant` body |
| Effective at `effectiveAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `suspendTenant` body |
| Notice message `noticeMessage` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `suspendTenant` body |

**Sent by *Terminate tenant*** (`terminateTenant`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `terminateTenant` body |
| Retention days `retentionDays` | number field (days) | required | — | min 30; max 2555 | — | — | `terminateTenant` body |
| Confirm tenant code `confirmTenantCode` | text field | required | — | — | — | Must match the tenant's code. Guards against the wrong tenant. | `terminateTenant` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Create tenant**: Code (unique), legal name, billing email required; billing address, account manager and plan optional. A new tenant has no venues yet. *(source: contracts/satellite/subscription.yaml#createTenant; F16 step 1)*
- **Suspend**: Mode and reason required; optional effective time and a notice message the tenant's staff will see. Suspended tenants may still be amended; terminated tenants may not. *(source: contracts/satellite/subscription.yaml#suspendTenant; R214)*
- **Terminate**: Reason, retention days and a typed confirmation of the tenant code; the confirmation states the retention date and that it cannot be undone after it. *(source: contracts/satellite/subscription.yaml#terminateTenant; ADR-0047)*
- **Open access grant (permissions, reason, expiry)**: Permissions preselected to exactly what this screen's tenant calls need (USER_MANAGE), never PLATFORM_* (those ride on the platform token); reason required and shown to the tenant; expiry at most 8 hours ahead (proposed). The tenant must be picked first. *(source: R098; contracts/spine/identity.yaml#openPlatformStaffGrant)*
- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setSsoConfig: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/identity.yaml#setSsoConfig)*

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (detail panel, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (decided 28 September, audit R098): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log.

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

**The SSO provider config** (detail panel, from `getSsoConfig`)

| Shows | Format | Notes |
|---|---|---|
| Display name | text | — |
| Protocol | chip: Oidc, Saml2 | — |
| Metadata URL | text | — |
| Issuer | text | — |
| Client secret ref | text | Key vault reference. The secret itself is never returned. |
| Group mappings | list or chips (count when long) | A group with no mapping grants nothing. No default role, ever — otherwise the identity provider becomes a way to mint access nobody … |
| Auto provision principals | yes / no (icon or chip) | Create a principal on first successful sign-in. |
| Is enforced | yes / no (icon or chip) | — |

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Add licence add on (primary button) | `addLicenceAddOn` POST `/tenants/{tenantId}/licences/add-ons` | LicenceAddOn | LicencePosition | — | opens modal first |
| Create tenant (secondary button) | `createTenant` POST `/tenants` | CreateTenantRequest | Tenant | 409 Code already in use | opens modal first |
| Provision cell (secondary button) | `provisionCell` POST `/tenants/{tenantId}/cells` | ProvisionCellRequest | Cell | 400 Placement is outside the region's jurisdiction, or the target cloud has no region in that country.; 409 A cell already exists for this region | opens modal first |
| Reactivate tenant (secondary button) | `reactivateTenant` POST `/tenants/{tenantId}/reactivate` | — | Tenant | 409 Tenant is terminated, not suspended. | — |
| Remove licence add on (destructive button) | `removeLicenceAddOn` DELETE `/tenants/{tenantId}/licences/add-ons` | inline | LicencePosition | 409 Module is currently enabled by the tenant. (DowngradeConflictProblem) | — |
| Save SSO config (secondary button) | `setSsoConfig` PUT `/tenants/sso-config` | SsoProviderConfig | SsoProviderConfig | 400 Metadata unreachable, or no group mappings supplied | opens modal first |
| Suspend tenant (destructive button) | `suspendTenant` POST `/tenants/{tenantId}/suspend` | inline | Tenant | — | — |
| Terminate tenant (destructive button) | `terminateTenant` POST `/tenants/{tenantId}/terminate` | inline | TerminationSchedule | 400 Confirmation code does not match; 409 Unsettled ledger balances exist | — |
| Save tenant (secondary button) | `updateTenant` PATCH `/tenants/{tenantId}` | inline | Tenant | 409 The tenant is terminated (`tenant-terminated`, audit R214 (3)). | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Tenant rows**: Name and code, plan, status chip (active, suspended with mode, terminating with date), cells, venues, billing email, account manager by name. *(source: contracts/satellite/subscription.yaml#listTenants)*
- **Licence position**: Licensed modules and limits with usage against each (usage/limit, percent), add-ons marked separately from the plan. *(source: contracts/satellite/subscription.yaml#getTenantLicences; contracts/satellite/subscription.yaml#getEntitlementUsage)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Terminate tenant**: Requires PLATFORM_TENANT_TERMINATE (distinct from manage) and the step-up; the tenant's staff are notified with the retention date. *(source: contracts/satellite/subscription.yaml#terminateTenant; contracts/spine/identity.yaml#createMfaChallenge)*
- **Open access grant**: Confirmation names the consequence first, then asks for the authentication code (authenticator app, or an emailed code as fallback); only a verified challenge sends openPlatformStaffGrant with its single-use stepUpToken. Wrong code: the action is not sent and nothing changes; five wrong codes lock step-up for the policy's lockout minutes and the screen says when it lifts. Why the control exists: Opens a platform operator's access into a tenant's data. *(source: contracts/spine/identity.yaml#openPlatformStaffGrant; R126; contracts/spine/identity.yaml#createMfaChallenge)*

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
| Empty, first run (`?state=emptyFirstRun`) | No tenants yet. Offers Create tenant, the first act of onboarding; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, planId and the tenant are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_CELL_VIEW`, `USER_MANAGE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_CELL_MANAGE` for `provisionCell` … |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Confirmation code does not match; 400 Metadata unreachable, or no group mappings supplied; 400 Placement is outside the region's jurisdiction, or the target cloud has no region in that country.; 400 Validation failed |

#### Edge cases to draw

- **Configuring SSO without an open grant into the tenant**: The SSO card shows grantRequired with Open access grant; tenant-record actions (suspend, add-on) stay available because they are control-plane. *(source: R098; contracts/spine/identity.yaml#setSsoConfig)*
- **The platform-staff grant expires while the operator is mid-edit**: Every tenant action disables at once, the grantRequired state returns with Open access grant, and anything typed is kept so it can be sent after a new grant; the countdown in the grant panel warns before expiry. *(source: R098; screens/P09-platform-admin-console.yaml#ADM-412)*
- **Can read but not change (holds PLATFORM_CELL_VIEW, PLATFORM_TENANT_VIEW, USER_MANAGE only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_TENANT_ACCESS for Open access grant; PLATFORM_TENANT_MANAGE for Add licence add on, Create tenant, Reactivate tenant; PLATFORM_CELL_MANAGE for Provision cell; PLATFORM_TENANT_TERMINATE for Terminate tenant. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/identity.yaml#openPlatformStaffGrant)*
- **provisionCell answers 409**: Show it as something the person can act on, not a failure: A cell already exists for this region *(source: contracts/satellite/subscription.yaml#provisionCell)*
- **reactivateTenant answers 409**: Show it as something the person can act on, not a failure: Tenant is terminated, not suspended. Termination is not reversible here *(source: contracts/satellite/subscription.yaml#reactivateTenant)*
- **removeLicenceAddOn answers 409**: Show it as something the person can act on, not a failure: Module is currently enabled by the tenant. Disable it there first *(source: contracts/satellite/subscription.yaml#removeLicenceAddOn)*
- **terminateTenant answers 409**: Show it as something the person can act on, not a failure: Unsettled ledger balances exist *(source: contracts/satellite/subscription.yaml#terminateTenant)*

#### Consistency with other screens

- Match `ADM-008`: Plan and subscription changes live there; the tenant row links to it.
- Match `ADM-003`: Cells link to cell health.
- Match `ADM-412`: Same tenant picker, grant panel and grantRequired state on every P09 screen that acts in a tenant (R098).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tenants:
- name: Marina Leisure Group
  code: MLG
  plan: Enterprise
  status: active
  cells: 2
  venues: 3
  billingEmail: finance@marinaleisure.ae
  accountManager: Sara Khalil
- name: Gulf Fun Parks LLC
  code: GFP
  plan: Growth
  status: suspended (read-only) since 20/09/2026
  cells: 1
  venues: 1
```

#### Permissions

- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `addLicenceAddOn` → `PLATFORM_TENANT_MANAGE` (configure) · staff
- `createTenant` → `PLATFORM_TENANT_MANAGE` (configure) · staff
- `getEntitlementUsage` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getSsoConfig` → `USER_MANAGE` (configure) · staff
- `getTenant` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenantLicences` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listTenantCells` → `PLATFORM_CELL_VIEW` (read) · staff
- `provisionCell` → `PLATFORM_CELL_MANAGE` (configure) · staff
- `reactivateTenant` → `PLATFORM_TENANT_MANAGE` (configure) · staff
- `removeLicenceAddOn` → `PLATFORM_TENANT_MANAGE` (configure) · staff
- `setSsoConfig` → `USER_MANAGE` (configure) · staff
- `suspendTenant` → `PLATFORM_TENANT_MANAGE` (configure) · staff
- `terminateTenant` → `PLATFORM_TENANT_TERMINATE` (operate) · staff
- `updateTenant` → `PLATFORM_TENANT_MANAGE` (configure) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_CELL_VIEW`, `USER_MANAGE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_CELL_MANAGE` for `provisionCell` …

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
- ADR-0014 *Cell Per Region* (`docs/adr/0014-cell-per-region.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (57), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (48 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Add licence add on, Create tenant, Provision cell, Reactivate tenant, Remove licence add on, Save SSO config, Suspend tenant, Terminate tenant, Save tenant.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `ADM-008`, `ADM-012`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`, `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_TERMINATE`, `PLATFORM_TENANT_VIEW`, `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 7 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-006` Tenant Hierarchy Explorer

**Explore a tenant's organisation tree and add to it.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 1 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-006 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW`, `SCOPE_MANAGE`, `SCOPE_VIEW` (3 read, 1 operate, 2 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenants` reads the population and `getSsoConfig` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (ADM-002) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/tenant-hierarchy-explorer` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant. **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listOrgUnits` (SCOPE_VIEW), `createOrgUnit` (SCOPE_MANAGE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): getSsoConfig was bulk-attached to every tenant screen of the Console; tenant SSO is configured on the Tenant Directory (ADM-005, setSsoConfig) and is not part of …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A tenant's hierarchy as a tree (brands, regions, venues, departments, outlets) with cells per region; amend the structure under a grant.

**Fixed on main** (the package already carries these; draw what it says): Purpose "for this venue". (CHG-WIR-023); Calls tenant-permission operations with no tenant picker and no platform-staff grant: getSsoConfig (USER_MANAGE), listOrgUnits … (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every tenant' drop id, planId, accountManagerPrincipalId; 'Every cell' drop id … (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Status | radio group | optional | — | Onboarding · Active · Suspended · Terminating · Terminated | — | Sends `?status=` to `listTenants`. | `listTenants` ?status |
| Plan id | picker: choose a plan (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?planId=` to `listTenants`. | `listTenants` ?planId |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Under | text field | — | — | `listOrgUnits` ?under |
| Level | select | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet · Subject | `listOrgUnits` ?level |
| Include inactive | toggle | off | — | `listOrgUnits` ?includeInactive |

**Form: Save tenant** (modal, opened by *Save tenant*; *Save tenant* calls `updateTenant`, *Cancel* sends nothing)

**Collects what `updateTenant` sends before it is called.** Nothing in the body is required. Optional: `name`, `billingEmail`, `billingAddress`, `accountManagerPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateTenant` body |
| Billing email `billingEmail` | text field | optional | — | — | — | — | `updateTenant` body |
| Billing address `billingAddress` | text area | optional | — | max length 500 | — | — | `updateTenant` body |
| Account manager principal `accountManagerPrincipalId` | picker: choose an account manager principal | optional | — | — | shows names, sends the id | — | `updateTenant` body |

Errors to draw in the form: 409 The tenant is terminated (`tenant-terminated`, audit R214 (3)).

**Form: Create org unit** (modal, opened by *Create org unit*; *Create org unit* calls `createOrgUnit`, *Cancel* sends nothing)

**Collects what `createOrgUnit` sends before it is called.** Required: `level`, `parentId`, `code`, `name`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Level `level` | select | required | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet · Subject | — | The eight organisational levels, plus `subject`. Restored 24 August. | `createOrgUnit` body |
| Parent `parentId` | picker: choose a parent | required | — | — | shows names, sends the id | Required for every level except tenant, which the cell creates at provisioning. | `createOrgUnit` body |
| Code `code` | text field | required | — | max length 64; pattern `^[a-z0-9_]+$` | — | Becomes the final ltree segment. Immutable once created. | `createOrgUnit` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createOrgUnit` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `SCOPE_MANAGE`, `SCOPE_VIEW` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

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

**Every org unit** (data table, from `listOrgUnits`)

| Shows | Format | Notes |
|---|---|---|
| Level | chip: Tenant, Brand, Region, Venue, Department, Sub department… | The eight organisational levels, plus `subject`. Restored 24 August. |
| Path | text | Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`. |
| Code | text | — |
| Name | text | — |
| Is active | yes / no (icon or chip) | False causes every permission query at or beneath this node to resolve to DENY. |
| Child count | 1,234 | — |

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

**The entitlement usage** (detail panel, from `getEntitlementUsage`)

| Shows | Format | Notes |
|---|---|---|
| Metrics | list or chips (count when long) | — |
| As at | 1 Oct 2026, 14:30 | — |

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Save tenant (primary button) | `updateTenant` PATCH `/tenants/{tenantId}` | inline | Tenant | 409 The tenant is terminated (`tenant-terminated`, audit R214 (3)). | opens modal first |
| Create org unit (secondary button) | `createOrgUnit` POST `/org-units` | CreateScopeNodeRequest | OrgUnit | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types. | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Tree**: Seven binding levels in order with outlet beside department; each node shows code and status; region nodes show currency, time zone and cell. *(source: ADR-0011; ADR-0018)*

**Data it reads**: `listTenants` (onLoad, List tenants); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `listTenantCells` (onLoad, List a tenant's cells); `listOrgUnits` (onLoad, List scope nodes visible to the session)

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_CELL_VIEW`, `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_ACCESS` for … |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `SCOPE_MANAGE`, `SCOPE_VIEW`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.; 409 The tenant is terminated (`tenant-terminated`, audit R214 (3)). |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_CELL_VIEW, PLATFORM_TENANT_VIEW, SCOPE_VIEW, USER_MANAGE only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_TENANT_MANAGE for Save tenant; SCOPE_MANAGE for Create org unit. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#updateTenant)*
- **updateTenant answers 409**: Show it as something the person can act on, not a failure: The tenant is terminated (`tenant-terminated`, audit R214 (3)). *(source: contracts/satellite/subscription.yaml#updateTenant)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every tenant:
- code: AQC-AUH
  name: Growth plan
  status: active
  planName: Growth
  cellCount: 12
  venueCount: 12
- code: AQC-DXB
  name: AquaCove Annual Pass Gold
  status: pending
  planName: Enterprise
  cellCount: 3
  venueCount: 3
- code: AQC-MCT
  name: Enterprise plan
  status: suspended
  planName: Starter
  cellCount: 0
  venueCount: 0
```

#### Permissions

- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getEntitlementUsage` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenant` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenantLicences` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listTenantCells` → `PLATFORM_CELL_VIEW` (read) · staff
- `updateTenant` → `PLATFORM_TENANT_MANAGE` (configure) · staff
- `listOrgUnits` → `SCOPE_VIEW` (read) · staff
- `createOrgUnit` → `SCOPE_MANAGE` (configure) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_CELL_VIEW`, `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_ACCESS` for …

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
- ADR-0014 *Cell Per Region* (`docs/adr/0014-cell-per-region.md`)
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (45 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Save tenant, Create org unit.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `ADM-007`.
- [ ] Every gated control is gated: `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW`, `SCOPE_MANAGE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-007` Module & Feature Entitlement

**See and change which modules and features a tenant is entitled to.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 1 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-007 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW` (2 read, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenantCells` reads the population and `getTenantLicences` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (ADM-002) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/module-and-feature-entitlement` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-platform navigation removed 24 August**: BO-074. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Removed 24 August**: generateInvoice, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: createTenant, provisionCell, reactivateTenant, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): getSsoConfig was bulk-attached to every tenant screen of the Console; module entitlement does not read SSO (R098; design-notes corrections platform-foundation …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A tenant's licensed modules and features, plan versus add-ons, with usage against limits; add or remove an add-on.

**Fixed on main** (the package already carries these; draw what it says): Purpose "for this venue". (CHG-WIR-023); Calls tenant-permission operations with no tenant picker and no platform-staff grant: getSsoConfig (USER_MANAGE). (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every cell' drop id, clusterId, regionId; 'Every tenant' drop id … (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Add licence add on** (modal, opened by *Add licence add on*; *Add licence add on* calls `addLicenceAddOn`, *Cancel* sends nothing)

**Collects what `addLicenceAddOn` sends before it is called.** Required: `moduleKey`. Optional: `limitOverrides`, `price`, `validFrom`, `validTo`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Module key `moduleKey` | text field | required | — | — | — | — | `addLicenceAddOn` body |
| Limit overrides `limitOverrides` | repeatable rows | optional | — | — | — | — | `addLicenceAddOn` body |
| Metric `limitOverrides[].metric` | select | required | — | Venues · Workstations · Active users · Devices · Branded apps · AI tokens · API calls · Storage gb · Transactions · Guest profiles | — | — | `addLicenceAddOn` body |
| Limit `limitOverrides[].limit` | number field | required | — | — | — | Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure `limit_value`. | `addLicenceAddOn` body |
| Overage allowed `limitOverrides[].overageAllowed` | toggle | optional | off | — | — | — | `addLicenceAddOn` body |
| Overage unit price `limitOverrides[].overageUnitPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `addLicenceAddOn` body |
| Price `price` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `addLicenceAddOn` body |
| Valid from `validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `addLicenceAddOn` body |
| Valid to `validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `addLicenceAddOn` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `addLicenceAddOn` body |

**Sent by *Remove licence add on*** (`removeLicenceAddOn`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Module key `moduleKey` | text field | required | — | — | — | — | `removeLicenceAddOn` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `removeLicenceAddOn` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every cell** (data table, from `listTenantCells`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Last contact at | 1 Oct 2026, 14:30 | When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first. |
| Licence expires at | 1 Oct 2026, 14:30 | On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. |
| Region name | text | — |
| Country code | text | — |

**Every tenant** (data table, from `listTenants`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Status | chip: Onboarding, Active, Suspended, Terminating, Terminated | — |
| Suspension effective at | 1 Oct 2026, 14:30 | When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. A future value is a pending suspension: the tenant stays `active` … |
| Termination scheduled at | 1 Oct 2026, 14:30 | When `terminateTenant` started the retention window. Null when no termination is under way. |
| Termination retention until | 1 Oct 2026, 14:30 | `terminationScheduledAt` plus the request's `retentionDays`. Stored, not recomputed — the day count is client-supplied and exists nowhere … |

**The selected cell** (detail panel, from `listTenantCells`)

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

**The entitlement usage** (detail panel, from `getEntitlementUsage`)

| Shows | Format | Notes |
|---|---|---|
| Metrics | list or chips (count when long) | — |
| As at | 1 Oct 2026, 14:30 | — |

**The subscription** (detail panel, from `getSubscription`)

| Shows | Format | Notes |
|---|---|---|
| Plan | the name it points at, never the id | — |
| Plan name | text | — |
| Plan version | text | — |
| Status | chip: Trial, Active, Past due, Cancelled, Expired | — |
| Starts at | 1 Oct 2026 | — |
| Renews at | 1 Oct 2026 | — |
| Cancelled at | 1 Oct 2026 | — |
| Current price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Billing period | text | — |

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Add licence add on (primary button) | `addLicenceAddOn` POST `/tenants/{tenantId}/licences/add-ons` | LicenceAddOn | LicencePosition | — | opens modal first |
| Remove licence add on (destructive button) | `removeLicenceAddOn` DELETE `/tenants/{tenantId}/licences/add-ons` | inline | LicencePosition | 409 Module is currently enabled by the tenant. (DowngradeConflictProblem) | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (currentPrice)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Remove licence add-on**: Confirmation names the module and what stops for the tenant's users (screens of that module leave navigation); reason required. *(source: contracts/satellite/subscription.yaml#removeLicenceAddOn; screens/_schema.yaml#requiresModule)*

**Data it reads**: `getTenantLicences` (onLoad, from page inventory); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getSubscription` (onLoad, Read the current subscription); `getTenant` (onLoad, Read a tenant with cells and subscription); `listTenantCells` (onLoad, List a tenant's cells); `listTenants` (onLoad, List tenants)

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getTenantLicences` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_CELL_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_MANAGE` for `addLicenceAddOn` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Module is currently enabled by the tenant. (DowngradeConflictProblem) |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_CELL_VIEW, PLATFORM_TENANT_VIEW, USER_MANAGE only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_TENANT_MANAGE for Add licence add on, Remove licence add on. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#addLicenceAddOn)*
- **removeLicenceAddOn answers 409**: Show it as something the person can act on, not a failure: Module is currently enabled by the tenant. Disable it there first *(source: contracts/satellite/subscription.yaml#removeLicenceAddOn)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every cell:
- name: Growth plan
  kind: standard
  isReachable: true
  lastContactAt: 01/10/2026 09:14
  licenceExpiresAt: 01/10/2026 09:14
  regionName: UAE
  countryCode: AE
- name: AquaCove Annual Pass Gold
  kind: standard
  isReachable: true
  lastContactAt: 30/09/2026 18:02
  licenceExpiresAt: 30/09/2026 18:02
  regionName: UAE
  countryCode: AE
- name: Enterprise plan
  kind: override
  isReachable: false
  lastContactAt: 28/09/2026 11:45
  licenceExpiresAt: 28/09/2026 11:45
  regionName: Oman
  countryCode: OM
```

#### Permissions

- `getTenantLicences` → `PLATFORM_TENANT_VIEW` (read) · staff
- `addLicenceAddOn` → `PLATFORM_TENANT_MANAGE` (configure) · staff
- `getEntitlementUsage` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getSubscription` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenant` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listTenantCells` → `PLATFORM_CELL_VIEW` (read) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `removeLicenceAddOn` → `PLATFORM_TENANT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getTenantLicences` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_CELL_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_MANAGE` for `addLicenceAddOn` …

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
- ADR-0014 *Cell Per Region* (`docs/adr/0014-cell-per-region.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-007?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Add licence add on, Remove licence add on.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `BO-074`, `ADM-012`.
- [ ] Every gated control is gated: `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-008` Subscription & Plan Management

**Manage the plan catalogue and each tenant's subscription.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 1 · needs the `core` module |
| Block | Block A · task APP-SETUP-ADM-008 |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_MANAGE`, `PLATFORM_BILLING_VIEW`, `PLATFORM_CELL_VIEW`, `PLATFORM_PLAN_MANAGE`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW` (3 configure, 3 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPlans` reads the population and `getEntitlementUsage` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `planId` (deepLink), `tenantId` (ADM-002) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/subscription-and-plan-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Partner agreements (list, create, update, PARTNER_MANAGE) are the tenant's B2B commercial terms and the tenant SSO config is tenant identity; neither belongs to … Removed 2 October 2026 (CHG-WIR-021): Partner agreements (list, create, update, PARTNER_MANAGE) are the tenant's B2B commercial terms and the tenant SSO config is tenant identity; neither belongs to … Removed 2 October 2026 (CHG-WIR-021): Partner agreements (list, create, update, PARTNER_MANAGE) are the tenant's B2B commercial terms and the tenant SSO config is tenant identity; neither belongs to …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Plans and subscriptions for TICVAI's own commercial offer: the plan catalogue (modules, limits, base price, cell tier, AI tokens, branded app), new plan versions, a tenant's subscription with a preview before any change, usage and invoices. The rule: upgrades take effect now with proration, downgrades at the next renewal, and the preview shows the money before the change is made.

**Fixed on main** (the package already carries these; draw what it says): Partner agreements (list, create, update) and the tenant SSO config are on plan management. (CHG-WIR-021); Purpose reads "Find subscription & plan management for this venue". (CHG-WIR-023); requiresModule is 'membership'. (CHG-SBO-003); Calls tenant-permission operations with no tenant picker and no platform-staff grant: getSsoConfig (USER_MANAGE), listPartnerAgreements … (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every plan' drop id; 'Every subscription invoice' drop id, lines, planVersionUsed … (CHG-SBO-004).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Offered to tenant | picker: choose an offered to tenant | — | — | `listPlans` ?offeredToTenantId |
| Package kind | segmented control | — | Standard · Custom | `listPlans` ?packageKind |
| Period start | date picker | — | — | `getUsageMetering` ?periodStart |
| Period end | date picker | — | — | `getUsageMetering` ?periodEnd |
| Metric | select | — | Venues · Workstations · Active users · Devices · Branded apps · AI tokens · API calls · Storage gb · Transactions · Guest profiles | `getUsageMetering` ?metric |
| Status | select | — | Draft · Issued · Paid · Overdue · Disputed · Cancelled | `listSubscriptionInvoices` ?status |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Save subscription** (modal, opened by *Save subscription*; *Save subscription* calls `setSubscription`, *Cancel* sends nothing)

**Collects what `setSubscription` sends before it is called.** Required: `planId`. Optional: `planVersion`, `effectiveFrom`, `prorate`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Plan `planId` | picker: choose a plan | required | — | — | shows names, sends the id | — | `setSubscription` body |
| Plan version `planVersion` | text field | optional | — | — | — | Defaults to the current version. | `setSubscription` body |
| Effective from `effectiveFrom` | date picker | optional | — | Today for an upgrade, `renewsAt` for a downgrade; any other date is refused (audit R214 (1)). | 1 Oct 2026 (dd MMM yyyy) | Optional, and set by the server if omitted. Today for an upgrade, `renewsAt` for a downgrade; any other date is refused (audit R214 (1)). | `setSubscription` body |
| Prorate `prorate` | toggle | optional | on | — | — | An upgrade is always prorated and a downgrade, which starts at renewal, never is (audit R214 (1)). | `setSubscription` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `setSubscription` body |

Errors to draw in the form: 409 Downgrade conflicts with current usage. The response names every module and limit that would be violated. (DowngradeConflictProblem); 422 `effectiveFrom` was sent and is not the date the change must take effect: today for an upgrade, the next renewal for a downgrade (`effective-date-not-allowed` …

**Form: Create plan** (modal, opened by *Create plan*; *Create plan* calls `createPlan`, *Cancel* sends nothing)

**Collects what `createPlan` sends before it is called.** Required: `code`, `name`, `cellTier`, `licensedModules`, `limits`, `basePrice`. Optional: `description`, `billingPeriod`, `includesBrandedApp`, `includedAiTokens`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createPlan` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createPlan` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createPlan` body |
| Cell tier `cellTier` | radio group | required | — | Shared · Dedicated · Isolated · Client hosted | — | — | `createPlan` body |
| Licensed modules `licensedModules` | list of values (chips) | required | — | at least 1 | — | A closed set as of 24 August. `moduleKey` was a free string, so nothing could join a licence to a screen — a tenant without an F&B licence was still served every F&B screen … | `createPlan` body |
| Limits `limits` | repeatable rows | required | — | — | — | — | `createPlan` body |
| Metric `limits[].metric` | select | required | — | Venues · Workstations · Active users · Devices · Branded apps · AI tokens · API calls · Storage gb · Transactions · Guest profiles | — | — | `createPlan` body |
| Limit `limits[].limit` | number field | required | — | — | — | Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure `limit_value`. | `createPlan` body |
| Overage allowed `limits[].overageAllowed` | toggle | optional | off | — | — | — | `createPlan` body |
| Overage unit price `limits[].overageUnitPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createPlan` body |
| Base price `basePrice` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createPlan` body |
| Billing period `billingPeriod` | segmented control | optional | — | Monthly · Quarterly · Annual | — | — | `createPlan` body |
| Includes branded app `includesBrandedApp` | toggle | optional | — | — | — | Branded native publishing carries per-tenant operational cost and is priced, not absorbed. | `createPlan` body |
| Included AI tokens `includedAiTokens` | number field | optional | — | — | — | AI tokens the package includes per billing period. Usage beyond it is a `metered` invoice line at the AI module's price (decided 29 September). | `createPlan` body |
| Request limits `requestLimits` | group | optional | — | Over budget, the call is refused `429` with `Retry-After` and the `RateLimit-*` headers (every operation declares it). | — | The limits section of a plan: every tenant has a request budget (ADR-0064, accepted 1 October; it decides the per-tenant limit ADR-0032 deferred). | `createPlan` body |
| Guest `requestLimits.guest` | group | optional | — | — | — | One audience's bucket (ADR-0064). `guest` covers `public` and `anonymous` callers too; shedding order stays ADR-0032's, `guest` first and `staff` and `service` last. | `createPlan` body |
| Sustained per second `requestLimits.guest.sustainedPerSecond` | number field | required | — | min 1 | — | Requests per second the bucket refills at. | `createPlan` body |
| Burst multiplier `requestLimits.guest.burstMultiplier` | number field | optional | 2 | min 1 | — | How far above the sustained rate a burst may go (2 is twice the rate). | `createPlan` body |
| Burst seconds `requestLimits.guest.burstSeconds` | number field (seconds) | optional | 10 | min 1 | — | How long a burst may last. | `createPlan` body |
| Staff `requestLimits.staff` | group | optional | — | — | — | One audience's bucket (ADR-0064). `guest` covers `public` and `anonymous` callers too; shedding order stays ADR-0032's, `guest` first and `staff` and `service` last. | `createPlan` body |
| Sustained per second `requestLimits.staff.sustainedPerSecond` | number field | required | — | min 1 | — | Requests per second the bucket refills at. | `createPlan` body |
| Burst multiplier `requestLimits.staff.burstMultiplier` | number field | optional | 2 | min 1 | — | How far above the sustained rate a burst may go (2 is twice the rate). | `createPlan` body |
| Burst seconds `requestLimits.staff.burstSeconds` | number field (seconds) | optional | 10 | min 1 | — | How long a burst may last. | `createPlan` body |
| Service `requestLimits.service` | group | optional | — | — | — | One audience's bucket (ADR-0064). `guest` covers `public` and `anonymous` callers too; shedding order stays ADR-0032's, `guest` first and `staff` and `service` last. | `createPlan` body |
| Sustained per second `requestLimits.service.sustainedPerSecond` | number field | required | — | min 1 | — | Requests per second the bucket refills at. | `createPlan` body |
| Burst multiplier `requestLimits.service.burstMultiplier` | number field | optional | 2 | min 1 | — | How far above the sustained rate a burst may go (2 is twice the rate). | `createPlan` body |
| Burst seconds `requestLimits.service.burstSeconds` | number field (seconds) | optional | 10 | min 1 | — | How long a burst may last. | `createPlan` body |
| Partner `requestLimits.partner` | group | optional | — | — | — | One audience's bucket (ADR-0064). `guest` covers `public` and `anonymous` callers too; shedding order stays ADR-0032's, `guest` first and `staff` and `service` last. | `createPlan` body |
| Sustained per second `requestLimits.partner.sustainedPerSecond` | number field | required | — | min 1 | — | Requests per second the bucket refills at. | `createPlan` body |
| Burst multiplier `requestLimits.partner.burstMultiplier` | number field | optional | 2 | min 1 | — | How far above the sustained rate a burst may go (2 is twice the rate). | `createPlan` body |
| Burst seconds `requestLimits.partner.burstSeconds` | number field (seconds) | optional | 10 | min 1 | — | How long a burst may last. | `createPlan` body |
| Replica share percent `requestLimits.replicaSharePercent` | stepper or slider | optional | 25 | min 1; max 100 | — | The most of one replica's request slots one tenant may hold while the share is enforced. | `createPlan` body |
| Share enforced above percent `requestLimits.shareEnforcedAbovePercent` | stepper or slider | optional | 70 | min 1; max 100 | — | The replica load, as a percent of its limit, above which the share is enforced. | `createPlan` body |
| Package kind `packageKind` | segmented control | optional | Standard | Standard · Custom | — | Three standard packages, and custom ones allowed (decided 29 September, Chinmay). | `createPlan` body |
| Offered to tenant `offeredToTenantId` | picker: choose an offered to tenant | optional | — | — | shows names, sends the id | Private to one tenant (decided 29 September, Chinmay): a custom package offered only to this tenant; `listPlans` shows it to no other tenant and `setSubscription` refuses it for … | `createPlan` body |

Errors to draw in the form: 422 `offeredToTenantId` on a standard package, or a tenant that does not exist

**Form: Create plan version** (modal, opened by *Create plan version*; *Create plan version* calls `createPlanVersion`, *Cancel* sends nothing)

**Collects what `createPlanVersion` sends before it is called.** Required: `code`, `name`, `cellTier`, `licensedModules`, `limits`, `basePrice`. Optional: `description`, `billingPeriod`, `includesBrandedApp`, `includedAiTokens`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createPlanVersion` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createPlanVersion` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createPlanVersion` body |
| Cell tier `cellTier` | radio group | required | — | Shared · Dedicated · Isolated · Client hosted | — | — | `createPlanVersion` body |
| Licensed modules `licensedModules` | list of values (chips) | required | — | at least 1 | — | A closed set as of 24 August. `moduleKey` was a free string, so nothing could join a licence to a screen — a tenant without an F&B licence was still served every F&B screen … | `createPlanVersion` body |
| Limits `limits` | repeatable rows | required | — | — | — | — | `createPlanVersion` body |
| Metric `limits[].metric` | select | required | — | Venues · Workstations · Active users · Devices · Branded apps · AI tokens · API calls · Storage gb · Transactions · Guest profiles | — | — | `createPlanVersion` body |
| Limit `limits[].limit` | number field | required | — | — | — | Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure `limit_value`. | `createPlanVersion` body |
| Overage allowed `limits[].overageAllowed` | toggle | optional | off | — | — | — | `createPlanVersion` body |
| Overage unit price `limits[].overageUnitPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createPlanVersion` body |
| Base price `basePrice` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createPlanVersion` body |
| Billing period `billingPeriod` | segmented control | optional | — | Monthly · Quarterly · Annual | — | — | `createPlanVersion` body |
| Includes branded app `includesBrandedApp` | toggle | optional | — | — | — | Branded native publishing carries per-tenant operational cost and is priced, not absorbed. | `createPlanVersion` body |
| Included AI tokens `includedAiTokens` | number field | optional | — | — | — | AI tokens the package includes per billing period. Usage beyond it is a `metered` invoice line at the AI module's price (decided 29 September). | `createPlanVersion` body |
| Request limits `requestLimits` | group | optional | — | Over budget, the call is refused `429` with `Retry-After` and the `RateLimit-*` headers (every operation declares it). | — | The limits section of a plan: every tenant has a request budget (ADR-0064, accepted 1 October; it decides the per-tenant limit ADR-0032 deferred). | `createPlanVersion` body |
| Guest `requestLimits.guest` | group | optional | — | — | — | One audience's bucket (ADR-0064). `guest` covers `public` and `anonymous` callers too; shedding order stays ADR-0032's, `guest` first and `staff` and `service` last. | `createPlanVersion` body |
| Sustained per second `requestLimits.guest.sustainedPerSecond` | number field | required | — | min 1 | — | Requests per second the bucket refills at. | `createPlanVersion` body |
| Burst multiplier `requestLimits.guest.burstMultiplier` | number field | optional | 2 | min 1 | — | How far above the sustained rate a burst may go (2 is twice the rate). | `createPlanVersion` body |
| Burst seconds `requestLimits.guest.burstSeconds` | number field (seconds) | optional | 10 | min 1 | — | How long a burst may last. | `createPlanVersion` body |
| Staff `requestLimits.staff` | group | optional | — | — | — | One audience's bucket (ADR-0064). `guest` covers `public` and `anonymous` callers too; shedding order stays ADR-0032's, `guest` first and `staff` and `service` last. | `createPlanVersion` body |
| Sustained per second `requestLimits.staff.sustainedPerSecond` | number field | required | — | min 1 | — | Requests per second the bucket refills at. | `createPlanVersion` body |
| Burst multiplier `requestLimits.staff.burstMultiplier` | number field | optional | 2 | min 1 | — | How far above the sustained rate a burst may go (2 is twice the rate). | `createPlanVersion` body |
| Burst seconds `requestLimits.staff.burstSeconds` | number field (seconds) | optional | 10 | min 1 | — | How long a burst may last. | `createPlanVersion` body |
| Service `requestLimits.service` | group | optional | — | — | — | One audience's bucket (ADR-0064). `guest` covers `public` and `anonymous` callers too; shedding order stays ADR-0032's, `guest` first and `staff` and `service` last. | `createPlanVersion` body |
| Sustained per second `requestLimits.service.sustainedPerSecond` | number field | required | — | min 1 | — | Requests per second the bucket refills at. | `createPlanVersion` body |
| Burst multiplier `requestLimits.service.burstMultiplier` | number field | optional | 2 | min 1 | — | How far above the sustained rate a burst may go (2 is twice the rate). | `createPlanVersion` body |
| Burst seconds `requestLimits.service.burstSeconds` | number field (seconds) | optional | 10 | min 1 | — | How long a burst may last. | `createPlanVersion` body |
| Partner `requestLimits.partner` | group | optional | — | — | — | One audience's bucket (ADR-0064). `guest` covers `public` and `anonymous` callers too; shedding order stays ADR-0032's, `guest` first and `staff` and `service` last. | `createPlanVersion` body |
| Sustained per second `requestLimits.partner.sustainedPerSecond` | number field | required | — | min 1 | — | Requests per second the bucket refills at. | `createPlanVersion` body |
| Burst multiplier `requestLimits.partner.burstMultiplier` | number field | optional | 2 | min 1 | — | How far above the sustained rate a burst may go (2 is twice the rate). | `createPlanVersion` body |
| Burst seconds `requestLimits.partner.burstSeconds` | number field (seconds) | optional | 10 | min 1 | — | How long a burst may last. | `createPlanVersion` body |
| Replica share percent `requestLimits.replicaSharePercent` | stepper or slider | optional | 25 | min 1; max 100 | — | The most of one replica's request slots one tenant may hold while the share is enforced. | `createPlanVersion` body |
| Share enforced above percent `requestLimits.shareEnforcedAbovePercent` | stepper or slider | optional | 70 | min 1; max 100 | — | The replica load, as a percent of its limit, above which the share is enforced. | `createPlanVersion` body |
| Package kind `packageKind` | segmented control | optional | Standard | Standard · Custom | — | Three standard packages, and custom ones allowed (decided 29 September, Chinmay). | `createPlanVersion` body |
| Offered to tenant `offeredToTenantId` | picker: choose an offered to tenant | optional | — | — | shows names, sends the id | Private to one tenant (decided 29 September, Chinmay): a custom package offered only to this tenant; `listPlans` shows it to no other tenant and `setSubscription` refuses it for … | `createPlanVersion` body |

Errors to draw in the form: 422 `offeredToTenantId` on a standard package, or a tenant that does not exist

**Form: Generate invoice** (modal, opened by *Generate invoice*; *Generate invoice* calls `generateInvoice`, *Cancel* sends nothing)

**Collects what `generateInvoice` sends before it is called.** Required: `periodStart`, `periodEnd`. Optional: `dryRun`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Period start `periodStart` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `generateInvoice` body |
| Period end `periodEnd` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `generateInvoice` body |
| Dry run `dryRun` | toggle | optional | off | — | — | — | `generateInvoice` body |

Errors to draw in the form: 409 An invoice already exists for this period

**Form: Preview subscription change** (modal, opened by *Preview subscription change*; *Preview subscription change* calls `previewSubscriptionChange`, *Cancel* sends nothing)

**Collects what `previewSubscriptionChange` sends before it is called.** Required: `planId`. Optional: `planVersion`, `effectiveFrom`, `prorate`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Plan `planId` | picker: choose a plan | required | — | — | shows names, sends the id | — | `previewSubscriptionChange` body |
| Plan version `planVersion` | text field | optional | — | — | — | Defaults to the current version. | `previewSubscriptionChange` body |
| Effective from `effectiveFrom` | date picker | optional | — | Today for an upgrade, `renewsAt` for a downgrade; any other date is refused (audit R214 (1)). | 1 Oct 2026 (dd MMM yyyy) | Optional, and set by the server if omitted. Today for an upgrade, `renewsAt` for a downgrade; any other date is refused (audit R214 (1)). | `previewSubscriptionChange` body |
| Prorate `prorate` | toggle | optional | on | — | — | An upgrade is always prorated and a downgrade, which starts at renewal, never is (audit R214 (1)). | `previewSubscriptionChange` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `previewSubscriptionChange` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Change subscription**: Plan (and version), effective from and prorate; the form always calls the preview first and shows the prorated amount and the new renewal date; a downgrade's effective date is fixed to the renewal and the field says so. *(source: contracts/satellite/subscription.yaml#previewSubscriptionChange; R214)*
- **Plan**: Code unique, modules from the module list, limits per metric, base price with currency and billing period. Editing a published plan creates a new version; subscribers stay on theirs until changed. *(source: contracts/satellite/subscription.yaml#createPlanVersion)*

#### Outputs: what the screen shows and produces

**Shown**

**Every plan** (data table, from `listPlans`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Cell tier | chip: Shared, Dedicated, Isolated, Client hosted | — |
| Base price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Billing period | chip: Monthly, Quarterly, Annual | — |

**Every subscription invoice** (data table, from `listSubscriptionInvoices`)

| Shows | Format | Notes |
|---|---|---|
| Invoice number | text | A tax invoice number, so gapless, per legal entity (decided 28 September, audit R152): one unbroken sequence for the TICVAI legal entity … |
| Status | chip: Draft, Issued, Paid, Overdue, Disputed, Cancelled | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Issued at | 1 Oct 2026, 14:30 | — |
| Due at | 1 Oct 2026 | — |

**Every cell** (data table, from `listTenantCells`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Last contact at | 1 Oct 2026, 14:30 | When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first. |
| Licence expires at | 1 Oct 2026, 14:30 | On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. |
| Region name | text | — |
| Country code | text | — |

**Every tenant** (data table, from `listTenants`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Status | chip: Onboarding, Active, Suspended, Terminating, Terminated | — |
| Suspension effective at | 1 Oct 2026, 14:30 | When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. A future value is a pending suspension: the tenant stays `active` … |
| Termination scheduled at | 1 Oct 2026, 14:30 | When `terminateTenant` started the retention window. Null when no termination is under way. |
| Termination retention until | 1 Oct 2026, 14:30 | `terminationScheduledAt` plus the request's `retentionDays`. Stored, not recomputed — the day count is client-supplied and exists nowhere … |

**The selected plan** (detail panel, from `getPlan`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Cell tier | chip: Shared, Dedicated, Isolated, Client hosted | — |
| Licensed modules | list or chips (count when long) | A closed set as of 24 August. `moduleKey` was a free string, so nothing could join a licence to a screen — a tenant without an F&B licence … |
| Base price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Subscriber count | 1,234 | — |
| Published at | 1 Oct 2026, 14:30 | — |

**The subscription** (detail panel, from `getSubscription`)

| Shows | Format | Notes |
|---|---|---|
| Plan | the name it points at, never the id | — |
| Plan name | text | — |
| Plan version | text | — |
| Status | chip: Trial, Active, Past due, Cancelled, Expired | — |
| Starts at | 1 Oct 2026 | — |
| Renews at | 1 Oct 2026 | — |
| Cancelled at | 1 Oct 2026 | — |
| Current price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Billing period | text | — |

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

**The usage report** (detail panel, from `getUsageMetering`)

| Shows | Format | Notes |
|---|---|---|
| Period start | 1 Oct 2026 | — |
| Period end | 1 Oct 2026 | — |
| Metrics | list or chips (count when long) | — |

**The entitlement usage** (detail panel, from `getEntitlementUsage`)

| Shows | Format | Notes |
|---|---|---|
| Metrics | list or chips (count when long) | — |
| As at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save subscription (primary button) | `setSubscription` PUT `/tenants/{tenantId}/subscription` | SetSubscriptionRequest | Subscription | 409 Downgrade conflicts with current usage. The response names every module and limit that would be violated. (DowngradeConflictProblem); 422 `effectiveFrom` was sent and is not the date the change must take effect … | opens modal first |
| Create plan (secondary button) | `createPlan` POST `/plans` | CreatePlanRequest | Plan | 422 `offeredToTenantId` on a standard package, or a tenant that does not exist | opens modal first |
| Create plan version (secondary button) | `createPlanVersion` POST `/plans/{planId}` | CreatePlanRequest | Plan | 422 `offeredToTenantId` on a standard package, or a tenant that does not exist | opens modal first |
| Generate invoice (secondary button) | `generateInvoice` POST `/tenants/{tenantId}/invoices` | inline | SubscriptionInvoice | 409 An invoice already exists for this period | opens modal first |
| Preview subscription change (secondary button) | `previewSubscriptionChange` POST `/tenants/{tenantId}/subscription/preview` | SetSubscriptionRequest | SubscriptionPreview | — | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Invoices**: Number, period, status, subtotal, tax and total with currency, and the plan version used. *(source: contracts/satellite/subscription.yaml#listSubscriptionInvoices)*
- **Money columns (basePrice, currentPrice, subtotal, taxAmount, total)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Generate invoice**: Period start and end, with a dry run first that shows the lines; issuing is a separate confirm. *(source: contracts/satellite/subscription.yaml#generateInvoice)*

**Data it reads**: `listPlans` (onLoad, from page inventory); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getSubscription` (onLoad, Read the current subscription); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `getUsageMetering` (onLoad, Metered usage for a period); `listSubscriptionInvoices` (onLoad, List subscription invoices); `listTenantCells` (onLoad, List a tenant's cells); `listTenants` (onLoad, List tenants)

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listPlans` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_BILLING_VIEW`, `PLATFORM_CELL_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_BILLING_MANAGE` for … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 An invoice already exists for this period; 409 Downgrade conflicts with current usage. The response names every module and limit that would be violated. (DowngradeConflictProblem); 422 `effectiveFrom` was sent and is not the date the change must take effect: today for an upgrade, the next renewal for a downgrade (`effective-date-not-allowed` …; 422 `offeredToTenantId` on a standard package … |

#### Edge cases to draw

- **Can read but not change (holds PARTNER_MANAGE, PLATFORM_BILLING_VIEW, PLATFORM_CELL_VIEW, PLATFORM_TENANT_VIEW …**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_TENANT_MANAGE for Save subscription; PLATFORM_PLAN_MANAGE for Create plan, Create plan version; PLATFORM_BILLING_MANAGE for Generate invoice. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#setSubscription)*
- **setSubscription answers 409**: Show it as something the person can act on, not a failure: Downgrade conflicts with current usage. The response names every module and limit that would be violated. Or the subscription is `expired` and cannot be reactivated (`subscription-expired`, audit STATE-SUBSCRIPTION); start a new one. *(source: contracts/satellite/subscription.yaml#setSubscription)*
- **setSubscription answers 422**: Show it as something the person can act on, not a failure: `effectiveFrom` was sent and is not the date the change must take effect: today for an upgrade, the next renewal for a downgrade (`effective-date-not-allowed`, audit R214 (1)). Or the plan is a custom package private to another tenant (`plan-not-offered`, decided 29 September). *(source: contracts/satellite/subscription.yaml#setSubscription)*
- **createPlan answers 422**: Show it as something the person can act on, not a failure: `offeredToTenantId` on a standard package, or a tenant that does not exist *(source: contracts/satellite/subscription.yaml#createPlan)*
- **createPlanVersion answers 422**: Show it as something the person can act on, not a failure: `offeredToTenantId` on a standard package, or a tenant that does not exist *(source: contracts/satellite/subscription.yaml#createPlanVersion)*

#### Consistency with other screens

- Match `ADM-005`: Opened from a tenant row with that tenant selected.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
plans:
- code: GROWTH
  name: Growth
  modules:
  - ticketing
  - fnb
  - retail
  - marketing
  basePrice: AED 18,000.00 / month
  cellTier: shared
  includedAiTokens: 2,000,000
- code: ENTERPRISE
  name: Enterprise
  modules: all
  basePrice: AED 55,000.00 / month
  cellTier: dedicated
  includesBrandedApp: true
preview:
  from: Growth v3
  to: Enterprise v1
  effective: 01/10/2026
  prorated: AED 23,870.97
  renewsAt: 01/01/2027
```

#### Permissions

- `listPlans` → `PLATFORM_TENANT_VIEW` (read) · staff, prospect
- `setSubscription` → `PLATFORM_TENANT_MANAGE` (configure) · staff, prospect
- `createPlan` → `PLATFORM_PLAN_MANAGE` (configure) · staff
- `createPlanVersion` → `PLATFORM_PLAN_MANAGE` (configure) · staff
- `generateInvoice` → `PLATFORM_BILLING_MANAGE` (configure) · staff
- `getEntitlementUsage` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getPlan` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getSubscription` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenant` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenantLicences` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getUsageMetering` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listSubscriptionInvoices` → `PLATFORM_BILLING_VIEW` (read) · staff
- `listTenantCells` → `PLATFORM_CELL_VIEW` (read) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `previewSubscriptionChange` → `PLATFORM_TENANT_VIEW` (read) · staff, prospect

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listPlans` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_BILLING_VIEW`, `PLATFORM_CELL_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_BILLING_MANAGE` for …

#### Requirements it meets

24 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 12 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-008` · status **notStarted** · provenance generated
- Flow F96 *A tenant is provisioned, licensed and its modules enabled*, step 2: Subscription & Plan Management. → 22 operations, 22 of them previously unwalked.
- ADR-0014 *Cell Per Region* (`docs/adr/0014-cell-per-region.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (83), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (57 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save subscription, Create plan, Create plan version, Generate invoice, Preview subscription change.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `ADM-011`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_MANAGE`, `PLATFORM_BILLING_VIEW`, `PLATFORM_CELL_VIEW`, `PLATFORM_PLAN_MANAGE`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-009` Tenant Billing & Invoicing

**Bill each tenant for its subscription and track invoices and credit notes.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 2 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-009 |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_MANAGE`, `PLATFORM_BILLING_VIEW`, `PLATFORM_TENANT_VIEW` (1 configure, 2 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSubscriptionInvoices` reads the population and `getEntitlementUsage` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (ADM-002) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/tenant-billing-and-invoicing` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: getUsageMetering, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Cells and SSO were repeated from the tenant directory; tenant billing needs invoices, credit notes and the subscription only (design-notes correction … Removed 2 October 2026 (CHG-WIR-021): Cells and SSO were repeated from the tenant directory; tenant billing needs invoices, credit notes and the subscription only (design-notes correction …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A tenant's subscription invoices and generating one for a period (dry run first).

**Fixed on main** (the package already carries these; draw what it says): Purpose "for this venue"; cells and SSO tables repeated from the tenant directory. (CHG-WIR-023); Calls tenant-permission operations with no tenant picker and no platform-staff grant: getSsoConfig (USER_MANAGE). (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every subscription invoice' drop id, lines, planVersionUsed; 'Every cell' drop id … (CHG-WIR-021); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Draft · Issued · Paid · Overdue · Disputed · Cancelled | — | Sends `?status=` to `listSubscriptionInvoices`. | `listSubscriptionInvoices` ?status |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |
| Invoice | text field | — | — | `listCreditNotes` ?invoiceId |

**Form: Generate invoice** (modal, opened by *Generate invoice*; *Generate invoice* calls `generateInvoice`, *Cancel* sends nothing)

**Collects what `generateInvoice` sends before it is called.** Required: `periodStart`, `periodEnd`. Optional: `dryRun`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Period start `periodStart` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `generateInvoice` body |
| Period end `periodEnd` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `generateInvoice` body |
| Dry run `dryRun` | toggle | optional | off | — | — | — | `generateInvoice` body |

Errors to draw in the form: 409 An invoice already exists for this period

#### Outputs: what the screen shows and produces

**Shown**

**Every subscription invoice** (data table, from `listSubscriptionInvoices`)

| Shows | Format | Notes |
|---|---|---|
| Invoice number | text | A tax invoice number, so gapless, per legal entity (decided 28 September, audit R152): one unbroken sequence for the TICVAI legal entity … |
| Status | chip: Draft, Issued, Paid, Overdue, Disputed, Cancelled | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Issued at | 1 Oct 2026, 14:30 | — |
| Due at | 1 Oct 2026 | — |

**Every tenant** (data table, from `listTenants`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Status | chip: Onboarding, Active, Suspended, Terminating, Terminated | — |
| Suspension effective at | 1 Oct 2026, 14:30 | When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. A future value is a pending suspension: the tenant stays `active` … |
| Termination scheduled at | 1 Oct 2026, 14:30 | When `terminateTenant` started the retention window. Null when no termination is under way. |
| Termination retention until | 1 Oct 2026, 14:30 | `terminationScheduledAt` plus the request's `retentionDays`. Stored, not recomputed — the day count is client-supplied and exists nowhere … |

**The selected subscription invoice** (detail panel, from `listSubscriptionInvoices`)

| Shows | Format | Notes |
|---|---|---|
| Invoice number | text | A tax invoice number, so gapless, per legal entity (decided 28 September, audit R152): one unbroken sequence for the TICVAI legal entity … |
| Status | chip: Draft, Issued, Paid, Overdue, Disputed, Cancelled | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Issued at | 1 Oct 2026, 14:30 | — |
| Due at | 1 Oct 2026 | — |
| Paid at | 1 Oct 2026, 14:30 | — |

**The subscription** (detail panel, from `getSubscription`)

| Shows | Format | Notes |
|---|---|---|
| Plan | the name it points at, never the id | — |
| Plan name | text | — |
| Plan version | text | — |
| Status | chip: Trial, Active, Past due, Cancelled, Expired | — |
| Starts at | 1 Oct 2026 | — |
| Renews at | 1 Oct 2026 | — |
| Cancelled at | 1 Oct 2026 | — |
| Current price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Billing period | text | — |

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Generate invoice (primary button) | `generateInvoice` POST `/tenants/{tenantId}/invoices` | inline | SubscriptionInvoice | 409 An invoice already exists for this period | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (currentPrice, subtotal, taxAmount, total)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listSubscriptionInvoices` (onLoad, from page inventory); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getSubscription` (onLoad, Read the current subscription); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `listTenants` (onLoad, List tenants); `listCreditNotes` (onLoad, Credit notes beside the invoices)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tenant billing invoicing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tenant billing invoicing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tenant billing invoicing yet. Offers Generate invoice (`generateInvoice`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status and the tenant billing invoicing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_BILLING_VIEW`, which `listSubscriptionInvoices` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_BILLING_MANAGE` for … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 An invoice already exists for this period |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_BILLING_VIEW, PLATFORM_CELL_VIEW, PLATFORM_TENANT_VIEW, USER_MANAGE only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_BILLING_MANAGE for Generate invoice. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#generateInvoice)*
- **generateInvoice answers 409**: Show it as something the person can act on, not a failure: An invoice already exists for this period *(source: contracts/satellite/subscription.yaml#generateInvoice)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every subscription invoice:
- status: active
  subtotal: AED 1,250.00
  taxAmount: AED 1,250.00
  total: AED 1,250.00
  issuedAt: 01/10/2026 09:14
- status: pending
  subtotal: AED 48,000.00
  taxAmount: AED 48,000.00
  total: AED 48,000.00
  issuedAt: 30/09/2026 18:02
- status: suspended
  subtotal: OMR 48.500
  taxAmount: OMR 48.500
  total: OMR 48.500
  issuedAt: 28/09/2026 11:45
```

#### Permissions

- `listSubscriptionInvoices` → `PLATFORM_BILLING_VIEW` (read) · staff
- `generateInvoice` → `PLATFORM_BILLING_MANAGE` (configure) · staff
- `getEntitlementUsage` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getSubscription` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenant` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenantLicences` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listCreditNotes` → `PLATFORM_BILLING_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_BILLING_VIEW`, which `listSubscriptionInvoices` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_BILLING_MANAGE` for …

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

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Generate invoice.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_MANAGE`, `PLATFORM_BILLING_VIEW`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-010` Usage Metering

**See each tenant's metered usage for a period, against what it is licensed for.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 2 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-010 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_VIEW` (2 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenantCells` reads the population and `getUsageMetering` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (ADM-002) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/usage-metering` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): getSsoConfig was bulk-attached to every tenant screen of the Console; usage metering does not read SSO (R098; design-notes corrections platform-foundation …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Metered usage per tenant and period against what the plan includes.

**Fixed on main** (the package already carries these; draw what it says): Purpose "for this venue". (CHG-WIR-023); Calls tenant-permission operations with no tenant picker and no platform-staff grant: getSsoConfig (USER_MANAGE). (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every cell' drop id, clusterId, regionId; 'Every tenant' drop id … (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Period start | date picker | — | — | `getUsageMetering` ?periodStart |
| Period end | date picker | — | — | `getUsageMetering` ?periodEnd |
| Metric | select | — | Venues · Workstations · Active users · Devices · Branded apps · AI tokens · API calls · Storage gb · Transactions · Guest profiles | `getUsageMetering` ?metric |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every cell** (data table, from `listTenantCells`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Last contact at | 1 Oct 2026, 14:30 | When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first. |
| Licence expires at | 1 Oct 2026, 14:30 | On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. |
| Region name | text | — |
| Country code | text | — |

**Every tenant** (data table, from `listTenants`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Status | chip: Onboarding, Active, Suspended, Terminating, Terminated | — |
| Suspension effective at | 1 Oct 2026, 14:30 | When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. A future value is a pending suspension: the tenant stays `active` … |
| Termination scheduled at | 1 Oct 2026, 14:30 | When `terminateTenant` started the retention window. Null when no termination is under way. |
| Termination retention until | 1 Oct 2026, 14:30 | `terminationScheduledAt` plus the request's `retentionDays`. Stored, not recomputed — the day count is client-supplied and exists nowhere … |

**The selected cell** (detail panel, from `listTenantCells`)

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

**The entitlement usage** (detail panel, from `getEntitlementUsage`)

| Shows | Format | Notes |
|---|---|---|
| Metrics | list or chips (count when long) | — |
| As at | 1 Oct 2026, 14:30 | — |

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

**The usage report** (detail panel, from `getUsageMetering`)

| Shows | Format | Notes |
|---|---|---|
| Period start | 1 Oct 2026 | — |
| Period end | 1 Oct 2026 | — |
| Metrics | list or chips (count when long) | — |

**Data it reads**: `getUsageMetering` (onLoad, from page inventory); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `listTenantCells` (onLoad, List a tenant's cells); `listTenants` (onLoad, List tenants)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The usage metering list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the usage metering untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No usage metering yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listTenantCells` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getUsageMetering` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
usage:
- metric: Tickets issued
  used: 412,880
  included: 500,000
  period: September 2026
- metric: AI tokens
  used: 2,410,000
  included: 2,000,000
  overage: 410,000
```

#### Permissions

- `getUsageMetering` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getEntitlementUsage` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenant` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenantLicences` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listTenantCells` → `PLATFORM_CELL_VIEW` (read) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff

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
- ADR-0014 *Cell Per Region* (`docs/adr/0014-cell-per-region.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-010?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-011` Licence & Seat Management

**Manage a tenant's licences, add-ons and seats against its subscription.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 2 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-011 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW` (2 read, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenantCells` reads the population and `getEntitlementUsage` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (ADM-002) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/licence-and-seat-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getUsageMetering, listSubscriptionInvoices. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: createTenant, provisionCell, reactivateTenant, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant. **Division (2 October 2026, CHG-SBO-015):** ADM-007 shows module entitlement, ADM-008 changes the subscription (Save subscription), ADM-011 holds the licence position, seats and add-ons and previews what a plan change would do to them (F96, F105).

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): getSsoConfig was bulk-attached to every tenant screen of the Console; licences and seats do not read SSO (R098; design-notes corrections platform-foundation … Changing the subscription is ADM-008's; this screen is the licence position, seats and add-ons (design-note correction platform-foundation ADM-011, CHG-SBO-015).

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Licences and seats per tenant, with add-ons and plan changes previewed before saving.

**Fixed on main** (the package already carries these; draw what it says): Duplicates ADM-007 and ADM-008 operations (add-ons, subscription change). (CHG-SBO-015); Calls tenant-permission operations with no tenant picker and no platform-staff grant: getSsoConfig (USER_MANAGE). (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every cell' drop id, clusterId, regionId; 'Every tenant' drop id … (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Add licence add on** (modal, opened by *Add licence add on*; *Add licence add on* calls `addLicenceAddOn`, *Cancel* sends nothing)

**Collects what `addLicenceAddOn` sends before it is called.** Required: `moduleKey`. Optional: `limitOverrides`, `price`, `validFrom`, `validTo`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Module key `moduleKey` | text field | required | — | — | — | — | `addLicenceAddOn` body |
| Limit overrides `limitOverrides` | repeatable rows | optional | — | — | — | — | `addLicenceAddOn` body |
| Metric `limitOverrides[].metric` | select | required | — | Venues · Workstations · Active users · Devices · Branded apps · AI tokens · API calls · Storage gb · Transactions · Guest profiles | — | — | `addLicenceAddOn` body |
| Limit `limitOverrides[].limit` | number field | required | — | — | — | Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure `limit_value`. | `addLicenceAddOn` body |
| Overage allowed `limitOverrides[].overageAllowed` | toggle | optional | off | — | — | — | `addLicenceAddOn` body |
| Overage unit price `limitOverrides[].overageUnitPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `addLicenceAddOn` body |
| Price `price` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `addLicenceAddOn` body |
| Valid from `validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `addLicenceAddOn` body |
| Valid to `validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `addLicenceAddOn` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `addLicenceAddOn` body |

**Form: Preview subscription change** (modal, opened by *Preview subscription change*; *Preview subscription change* calls `previewSubscriptionChange`, *Cancel* sends nothing)

**Collects what `previewSubscriptionChange` sends before it is called.** Required: `planId`. Optional: `planVersion`, `effectiveFrom`, `prorate`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Plan `planId` | picker: choose a plan | required | — | — | shows names, sends the id | — | `previewSubscriptionChange` body |
| Plan version `planVersion` | text field | optional | — | — | — | Defaults to the current version. | `previewSubscriptionChange` body |
| Effective from `effectiveFrom` | date picker | optional | — | Today for an upgrade, `renewsAt` for a downgrade; any other date is refused (audit R214 (1)). | 1 Oct 2026 (dd MMM yyyy) | Optional, and set by the server if omitted. Today for an upgrade, `renewsAt` for a downgrade; any other date is refused (audit R214 (1)). | `previewSubscriptionChange` body |
| Prorate `prorate` | toggle | optional | on | — | — | An upgrade is always prorated and a downgrade, which starts at renewal, never is (audit R214 (1)). | `previewSubscriptionChange` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `previewSubscriptionChange` body |

**Sent by *Remove licence add on*** (`removeLicenceAddOn`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Module key `moduleKey` | text field | required | — | — | — | — | `removeLicenceAddOn` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `removeLicenceAddOn` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every cell** (data table, from `listTenantCells`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Last contact at | 1 Oct 2026, 14:30 | When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first. |
| Licence expires at | 1 Oct 2026, 14:30 | On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. |
| Region name | text | — |
| Country code | text | — |

**Every tenant** (data table, from `listTenants`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Status | chip: Onboarding, Active, Suspended, Terminating, Terminated | — |
| Suspension effective at | 1 Oct 2026, 14:30 | When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. A future value is a pending suspension: the tenant stays `active` … |
| Termination scheduled at | 1 Oct 2026, 14:30 | When `terminateTenant` started the retention window. Null when no termination is under way. |
| Termination retention until | 1 Oct 2026, 14:30 | `terminationScheduledAt` plus the request's `retentionDays`. Stored, not recomputed — the day count is client-supplied and exists nowhere … |

**The selected cell** (detail panel, from `listTenantCells`)

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

**The subscription** (detail panel, from `getSubscription`)

| Shows | Format | Notes |
|---|---|---|
| Plan | the name it points at, never the id | — |
| Plan name | text | — |
| Plan version | text | — |
| Status | chip: Trial, Active, Past due, Cancelled, Expired | — |
| Starts at | 1 Oct 2026 | — |
| Renews at | 1 Oct 2026 | — |
| Cancelled at | 1 Oct 2026 | — |
| Current price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Billing period | text | — |

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add licence add on (primary button) | `addLicenceAddOn` POST `/tenants/{tenantId}/licences/add-ons` | LicenceAddOn | LicencePosition | — | opens modal first |
| Preview subscription change (secondary button) | `previewSubscriptionChange` POST `/tenants/{tenantId}/subscription/preview` | SetSubscriptionRequest | SubscriptionPreview | — | opens modal first |
| Remove licence add on (destructive button) | `removeLicenceAddOn` DELETE `/tenants/{tenantId}/licences/add-ons` | inline | LicencePosition | 409 Module is currently enabled by the tenant. (DowngradeConflictProblem) | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (currentPrice)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `getEntitlementUsage` (onLoad, from page inventory); `getSubscription` (onLoad, Read the current subscription); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `listTenantCells` (onLoad, List a tenant's cells); `listTenants` (onLoad, List tenants)

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getEntitlementUsage` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_CELL_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_MANAGE` for `addLicenceAddOn` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Module is currently enabled by the tenant. (DowngradeConflictProblem) |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_CELL_VIEW, PLATFORM_TENANT_VIEW, USER_MANAGE only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_TENANT_MANAGE for Add licence add on, Remove licence add on, Save subscription. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#addLicenceAddOn)*
- **removeLicenceAddOn answers 409**: Show it as something the person can act on, not a failure: Module is currently enabled by the tenant. Disable it there first *(source: contracts/satellite/subscription.yaml#removeLicenceAddOn)*
- **setSubscription answers 409**: Show it as something the person can act on, not a failure: Downgrade conflicts with current usage. The response names every module and limit that would be violated. Or the subscription is `expired` and cannot be reactivated (`subscription-expired`, audit STATE-SUBSCRIPTION); start a new one. *(source: contracts/satellite/subscription.yaml#setSubscription)*
- **setSubscription answers 422**: Show it as something the person can act on, not a failure: `effectiveFrom` was sent and is not the date the change must take effect: today for an upgrade, the next renewal for a downgrade (`effective-date-not-allowed`, audit R214 (1)). Or the plan is a custom package private to another tenant (`plan-not-offered`, decided 29 September). *(source: contracts/satellite/subscription.yaml#setSubscription)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every cell:
- name: Growth plan
  kind: standard
  isReachable: true
  lastContactAt: 01/10/2026 09:14
  licenceExpiresAt: 01/10/2026 09:14
  regionName: UAE
  countryCode: AE
- name: AquaCove Annual Pass Gold
  kind: standard
  isReachable: true
  lastContactAt: 30/09/2026 18:02
  licenceExpiresAt: 30/09/2026 18:02
  regionName: UAE
  countryCode: AE
- name: Enterprise plan
  kind: override
  isReachable: false
  lastContactAt: 28/09/2026 11:45
  licenceExpiresAt: 28/09/2026 11:45
  regionName: Oman
  countryCode: OM
```

#### Permissions

- `getEntitlementUsage` → `PLATFORM_TENANT_VIEW` (read) · staff
- `addLicenceAddOn` → `PLATFORM_TENANT_MANAGE` (configure) · staff
- `getSubscription` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenant` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenantLicences` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listTenantCells` → `PLATFORM_CELL_VIEW` (read) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `previewSubscriptionChange` → `PLATFORM_TENANT_VIEW` (read) · staff, prospect
- `removeLicenceAddOn` → `PLATFORM_TENANT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getEntitlementUsage` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_CELL_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_MANAGE` for `addLicenceAddOn` …

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 4 more | | | | `traceability.json` |

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
- ADR-0014 *Cell Per Region* (`docs/adr/0014-cell-per-region.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-011?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add licence add on, Preview subscription change, Remove licence add on.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `PTR-020`, `ADM-007`.
- [ ] Every gated control is gated: `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-012` Tenant Isolation & Resource Pool

**Place each tenant in its cells, one per region, and watch the capacity of the pool.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 1 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-012 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_MANAGE`, `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_VIEW` (1 configure, 2 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenantCells` reads the population and `getEntitlementUsage` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink), `tenantId` (ADM-002) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/tenant-isolation-and-resource-pool` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): getSsoConfig was bulk-attached to every tenant screen of the Console; cell placement does not read SSO (R098; design-notes corrections platform-foundation …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A tenant's cells and placement (shared or dedicated), and provisioning a cell in a new region.

**Fixed on main** (the package already carries these; draw what it says): Purpose "for this venue". (CHG-WIR-023); Calls tenant-permission operations with no tenant picker and no platform-staff grant: getSsoConfig (USER_MANAGE). (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every cell' drop id, clusterId, regionId; 'Every tenant' drop id … (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |
| Window | radio group | Day | Hour · Day · Week · Month | `getCellCapacity` ?window |

**Form: Provision cell** (modal, opened by *Provision cell*; *Provision cell* calls `provisionCell`, *Cancel* sends nothing)

**Collects what `provisionCell` sends before it is called.** Required: `regionId`, `countryCode`, `tier`. Optional: `cloudProvider`, `cloudRegion`, `clientHostedEndpoint`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Region `regionId` | picker: choose a region | required | — | — | shows names, sends the id | — | `provisionCell` body |
| Country code `countryCode` | text field | required | — | pattern `^[A-Z]{2}$` | — | Determines the jurisdiction. Placement must be within it — this is enforced, not trusted. | `provisionCell` body |
| Tier `tier` | radio group | required | — | Shared · Dedicated · Isolated · Client hosted | — | — | `provisionCell` body |
| Cloud provider `cloudProvider` | text field | optional | — | — | — | — | `provisionCell` body |
| Cloud region `cloudRegion` | text field | optional | — | — | — | — | `provisionCell` body |
| Client hosted endpoint `clientHostedEndpoint` | text field | optional | — | — | — | Required for `clientHosted`, where no in-region cloud exists. | `provisionCell` body |

Errors to draw in the form: 400 Placement is outside the region's jurisdiction, or the target cloud has no region in that country.; 409 A cell already exists for this region

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Provision cell**: Region and country required; tier; cloud provider and region, or a client-hosted endpoint for on-premise. *(source: contracts/satellite/subscription.yaml#provisionCell; ADR-0046)*

#### Outputs: what the screen shows and produces

**Shown**

**Every cell** (data table, from `listTenantCells`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Last contact at | 1 Oct 2026, 14:30 | When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first. |
| Licence expires at | 1 Oct 2026, 14:30 | On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. |
| Region name | text | — |
| Country code | text | — |

**Every tenant** (data table, from `listTenants`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Status | chip: Onboarding, Active, Suspended, Terminating, Terminated | — |
| Suspension effective at | 1 Oct 2026, 14:30 | When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. A future value is a pending suspension: the tenant stays `active` … |
| Termination scheduled at | 1 Oct 2026, 14:30 | When `terminateTenant` started the retention window. Null when no termination is under way. |
| Termination retention until | 1 Oct 2026, 14:30 | `terminationScheduledAt` plus the request's `retentionDays`. Stored, not recomputed — the day count is client-supplied and exists nowhere … |

**The selected cell** (detail panel, from `listTenantCells`)

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

**The entitlement usage** (detail panel, from `getEntitlementUsage`)

| Shows | Format | Notes |
|---|---|---|
| Metrics | list or chips (count when long) | — |
| As at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Provision cell (primary button) | `provisionCell` POST `/tenants/{tenantId}/cells` | ProvisionCellRequest | Cell | 400 Placement is outside the region's jurisdiction, or the target cloud has no region in that country.; 409 A cell already exists for this region | opens modal first |

**Data it reads**: `getEntitlementUsage` (onLoad, Usage against licensed limits); `getTenant` (onLoad, Read a tenant with cells and subscription); `getTenantLicences` (onLoad, What a tenant is licensed to use); `listTenantCells` (onLoad, List a tenant's cells); `listTenants` (onLoad, List tenants); `getCellCapacity` (onLoad, Load against headroom)

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getEntitlementUsage` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_CELL_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_CELL_MANAGE` for `provisionCell`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Placement is outside the region's jurisdiction, or the target cloud has no region in that country.; 409 A cell already exists for this region |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_CELL_VIEW, PLATFORM_TENANT_VIEW, USER_MANAGE only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_CELL_MANAGE for Provision cell. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#provisionCell)*
- **provisionCell answers 409**: Show it as something the person can act on, not a failure: A cell already exists for this region *(source: contracts/satellite/subscription.yaml#provisionCell)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every cell:
- name: Growth plan
  kind: standard
  isReachable: true
  lastContactAt: 01/10/2026 09:14
  licenceExpiresAt: 01/10/2026 09:14
  regionName: UAE
  countryCode: AE
- name: AquaCove Annual Pass Gold
  kind: standard
  isReachable: true
  lastContactAt: 30/09/2026 18:02
  licenceExpiresAt: 30/09/2026 18:02
  regionName: UAE
  countryCode: AE
- name: Enterprise plan
  kind: override
  isReachable: false
  lastContactAt: 28/09/2026 11:45
  licenceExpiresAt: 28/09/2026 11:45
  regionName: Oman
  countryCode: OM
```

#### Permissions

- `provisionCell` → `PLATFORM_CELL_MANAGE` (configure) · staff
- `getEntitlementUsage` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenant` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenantLicences` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listTenantCells` → `PLATFORM_CELL_VIEW` (read) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getCellCapacity` → `PLATFORM_CELL_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getEntitlementUsage` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_CELL_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_CELL_MANAGE` for `provisionCell`.

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
- ADR-0014 *Cell Per Region* (`docs/adr/0014-cell-per-region.md`)
- ADR-0001 *Cell architecture — one tenant per jurisdiction* (`docs/adr/0001-cell-architecture-one-tenant-per-jurisdiction.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-012?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Provision cell.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `ADM-006`, `ADM-013`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`, `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-015` API Rate Limit & Quota Management

**Set the rate limits and quotas of each API client within its tenant's budget.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-015 |
| Who uses it | ticvai staff holding `DEVELOPER_ADMIN`, `DEVELOPER_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listTenantCells` reads the population and `getTenantLicences` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `tenantId` (ADM-002), `requestId` (navigation) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/api-rate-limit-and-quota-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant. **`setApiQuota` wired 24 August.** This screen is named *API Rate Limit & Quota Management* and **declared no quota operation at all** — it carried nine subscription operations and six tenant-lifecycle ones instead. **The screen for the job could not do the job**, and only writing F105 against it surfaced that. **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `setApiQuota` (DEVELOPER_ADMIN), `getApiUsage` (DEVELOPER_VIEW), `listApiClients` (DEVELOPER_VIEW), `listProductionAccessRequests` (DEVELOPER_VIEW) …

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Cells and SSO tables were copied from the tenant directory; quotas are per API client within a tenant's budget (ADR-0064; design-notes correction … Removed 2 October 2026 (CHG-WIR-021): Cells and SSO tables were copied from the tenant directory; quotas are per API client within a tenant's budget (ADR-0064; design-notes correction … Open: Blocked — Developer & API workshop

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** API rate limits and quotas per client within a tenant's request budget, production-access decisions and anomaly rules; TICVAI's administration of the public API.

**Fixed on main** (the package already carries these; draw what it says): Purpose "for this venue"; tenant, cells and SSO tables copied from the tenant directory. (CHG-WIR-023); Calls tenant-permission operations with no tenant picker and no platform-staff grant: getSsoConfig (USER_MANAGE), getApiUsage … (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every cell' drop id, clusterId, regionId; 'Every tenant' drop id … (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003).

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
| From | date picker | — | — | `getApiUsage` ?from |
| To | date picker | — | — | `getApiUsage` ?to |
| Status | radio group | — | Pending · Approved · Rejected · Withdrawn | `listProductionAccessRequests` ?status |
| Client | picker: choose a client | — | — | `listApiAnomalies` ?clientId |
| From | date and time picker | — | — | `listApiAnomalies` ?from |

**Form: Save API quota** (modal, opened by *Save API quota*; *Save API quota* calls `setApiQuota`, *Cancel* sends nothing)

**Collects what `setApiQuota` sends before it is called.** Required: `clientId`, `sustainedPerMinute`. Optional: `burstPerSecond`, `dailyCap`, `perOperationOverrides`, `onBreach`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets it (readOnly in the contract): `id` (3 October 2026, CHG-SPF-001).

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

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `DEVELOPER_ADMIN`, `DEVELOPER_VIEW` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setApiQuota, setApiAnomalyRule: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/public-api.yaml#setApiQuota)*

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

**Every tenant** (data table, from `listTenants`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Status | chip: Onboarding, Active, Suspended, Terminating, Terminated | — |
| Suspension effective at | 1 Oct 2026, 14:30 | When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. A future value is a pending suspension: the tenant stays `active` … |
| Termination scheduled at | 1 Oct 2026, 14:30 | When `terminateTenant` started the retention window. Null when no termination is under way. |
| Termination retention until | 1 Oct 2026, 14:30 | `terminationScheduledAt` plus the request's `retentionDays`. Stored, not recomputed — the day count is client-supplied and exists nowhere … |

**Every API client** (data table, from `listApiClients`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Environment | chip: Sandbox, Production | Bound to one, stated on the object rather than by naming convention. A key that works in both is a key somebody will use in the wrong one. |
| Scopes | list or chips (count when long) | Resolved against the tenant's licence at token issue (13.3.24). A scope granted here and not licensed there produces no token — and the … |
| Ip allow list | list or chips (count when long) | 13.1.38. Required on a production client (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the … |
| Status | chip: Active, Suspended, Revoked | — |
| Last used at | 1 Oct 2026, 14:30 | A credential unused for a year is a credential nobody will notice being stolen. |

**Production access requests, pending first** (data table, from `listProductionAccessRequests`): **Production keys only after certification** (17 September minutes, M17-06). The queue a TICVAI administrator works: each request names the certified integration, the tenants, the module scopes and the IP allow-list. Approving issues a new production client; the sandbox key is never promoted.

| Shows | Format | Notes |
|---|---|---|
| Scopes | list or chips (count when long) | — |
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

**The entitlement usage** (detail panel, from `getEntitlementUsage`)

| Shows | Format | Notes |
|---|---|---|
| Metrics | list or chips (count when long) | — |
| As at | 1 Oct 2026, 14:30 | — |

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

**The licence position** (detail panel, from `getTenantLicences`)

| Shows | Format | Notes |
|---|---|---|
| Plan | the name it points at, never the id | — |
| Licensed modules | list or chips (count when long) | Union of plan modules and add-ons. The White Label Builder reads this and cannot enable anything absent from it. |
| Limits | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Save API quota (primary button) | `setApiQuota` PUT `/api-quotas` | ApiQuota | ApiQuota | — | opens modal first |
| Decide production access (primary button) | `decideProductionAccess` POST `/production-access-requests/{requestId}/decide` | inline | ProductionAccessRequest | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already decided (`already-decided`), or the listing's certification lapsed since the request … | opens modal first |
| Save anomaly rule (secondary button) | `setApiAnomalyRule` PUT `/api-anomaly-rules` | ApiAnomalyRule | ApiAnomalyRule | — | opens modal first |

**Data it reads**: `getTenantLicences` (onLoad, What a tenant is licensed to use); `getEntitlementUsage` (onLoad, Usage against licensed limits); `getTenant` (onLoad, Read a tenant with cells and subscription); `listTenants` (onLoad, List tenants); `getApiUsage` (onLoad, Calls, errors, latency and success rate); `listApiClients` (onLoad, Registered clients for this developer); `listProductionAccessRequests` (onLoad, The production key approval queue); `listApiAnomalies` (onLoad, Flagged abnormal API traffic)

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
| Empty, no results (`?state=emptyNoResults`) | Never shown: nothing on this screen filters its list, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getTenantLicences` requires to show this screen, and names that permission (the screen's other reads need `DEVELOPER_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVELOPER_ADMIN` for `setApiQuota` … |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `DEVELOPER_ADMIN`, `DEVELOPER_VIEW`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Already decided (`already-decided`), or the listing's certification lapsed since the request (`certification-required`).; 422 `reject` without a `reason`. |

#### Edge cases to draw

- **Can read but not change (holds DEVELOPER_VIEW, PLATFORM_CELL_VIEW, PLATFORM_TENANT_VIEW, USER_MANAGE only)**: Everything reads; the actions needing another permission are not offered as live buttons: DEVELOPER_ADMIN for Save API quota, Decide production access, Save anomaly rule. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/public-api.yaml#setApiQuota)*
- **decideProductionAccess answers 409**: Show it as something the person can act on, not a failure: Already decided (`already-decided`), or the listing's certification lapsed since the request (`certification-required`). *(source: contracts/satellite/public-api.yaml#decideProductionAccess)*
- **decideProductionAccess answers 422**: Show it as something the person can act on, not a failure: `reject` without a `reason`. *(source: contracts/satellite/public-api.yaml#decideProductionAccess)*

#### Consistency with other screens

- Match `DEV-008`: The same quota, production-access and anomaly operations; one administration screen.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every cell:
- name: Kiosk connector (sandbox)
  kind: standard
  isReachable: true
  lastContactAt: 01/10/2026 09:14
  licenceExpiresAt: 01/10/2026 09:14
  regionName: UAE
  countryCode: AE
- name: OTA availability feed
  kind: standard
  isReachable: true
  lastContactAt: 30/09/2026 18:02
  licenceExpiresAt: 30/09/2026 18:02
  regionName: UAE
  countryCode: AE
- name: Wallet sync
  kind: override
  isReachable: false
  lastContactAt: 28/09/2026 11:45
  licenceExpiresAt: 28/09/2026 11:45
  regionName: Oman
  countryCode: OM
```

#### Permissions

- `getTenantLicences` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getEntitlementUsage` → `PLATFORM_TENANT_VIEW` (read) · staff
- `getTenant` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `setApiQuota` → `DEVELOPER_ADMIN` (configure) · staff
- `getApiUsage` → `DEVELOPER_VIEW` (read) · staff, partner
- `listApiClients` → `DEVELOPER_VIEW` (read) · staff, partner
- `listProductionAccessRequests` → `DEVELOPER_VIEW` (read) · staff, partner
- `decideProductionAccess` → `DEVELOPER_ADMIN` (configure) · staff
- `listApiAnomalies` → `DEVELOPER_VIEW` (read) · staff, partner
- `setApiAnomalyRule` → `DEVELOPER_ADMIN` (configure) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `getTenantLicences` requires to show this screen, and names that permission (the screen's other reads need `DEVELOPER_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVELOPER_ADMIN` for `setApiQuota` …

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
- ADR-0064 *Every tenant has a request budget, and a busy tenant cannot starve the others* (`docs/adr/0064-per-tenant-limits.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (50 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Save API quota, Decide production access, Save anomaly rule.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`, `ADM-011`.
- [ ] Every gated control is gated: `DEVELOPER_ADMIN`, `DEVELOPER_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
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
"addLicenceAddOn": {"method":"POST","path":"/tenants/{tenantId}/licences/add-ons","contract":"subscription","summary":"License a module outside the plan","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LicenceAddOn","responds":"LicencePosition"},
"createOrgUnit": {"method":"POST","path":"/org-units","contract":"tenancy","summary":"Create a scope node","permission":"SCOPE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"brand","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateScopeNodeRequest","responds":"OrgUnit"},
"createPlan": {"method":"POST","path":"/plans","contract":"subscription","summary":"Create a subscription plan","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePlanRequest","responds":"Plan"},
"createPlanVersion": {"method":"POST","path":"/plans/{planId}","contract":"subscription","summary":"Publish a new version of a plan","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePlanRequest","responds":"Plan"},
"createTenant": {"method":"POST","path":"/tenants","contract":"subscription","summary":"Create a tenant","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateTenantRequest","responds":"Tenant"},
"decideProductionAccess": {"method":"POST","path":"/production-access-requests/{requestId}/decide","contract":"public-api","summary":"Approve or reject production access","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductionAccessRequest"},
"generateInvoice": {"method":"POST","path":"/tenants/{tenantId}/invoices","contract":"subscription","summary":"Generate an invoice for a period","permission":"PLATFORM_BILLING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SubscriptionInvoice"},
"getApiUsage": {"method":"GET","path":"/api-usage","contract":"public-api","summary":"Calls, errors, latency and success rate","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"ApiUsageSummary"},
"getCellCapacity": {"method":"GET","path":"/cells/{cellId}/capacity","contract":"subscription","summary":"Load against headroom","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"window","in":"query","required":null}],"requestBody":null,"responds":"CellCapacity"},
"getEntitlementUsage": {"method":"GET","path":"/tenants/{tenantId}/entitlement-usage","contract":"subscription","summary":"Usage against licensed limits","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"EntitlementUsage"},
"getPlan": {"method":"GET","path":"/plans/{planId}","contract":"subscription","summary":"Read a plan","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"Plan"},
"getSsoConfig": {"method":"GET","path":"/tenants/sso-config","contract":"identity","summary":"Read SSO configuration","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SsoProviderConfig"},
"getSubscription": {"method":"GET","path":"/tenants/{tenantId}/subscription","contract":"subscription","summary":"Read the current subscription","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"Subscription"},
"getTenant": {"method":"GET","path":"/tenants/{tenantId}","contract":"subscription","summary":"Read a tenant with cells and subscription","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantDetail"},
"getTenantLicences": {"method":"GET","path":"/tenants/{tenantId}/licences","contract":"subscription","summary":"What a tenant is licensed to use","permission":"PLATFORM_TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"LicencePosition"},
"getUsageMetering": {"method":"GET","path":"/tenants/{tenantId}/usage","contract":"subscription","summary":"Metered usage for a period","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"periodStart","in":"query","required":true},{"name":"periodEnd","in":"query","required":true},{"name":"metric","in":"query","required":null}],"requestBody":null,"responds":"UsageReport"},
"listApiAnomalies": {"method":"GET","path":"/api-anomalies","contract":"public-api","summary":"Flagged API traffic","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"clientId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listApiClients": {"method":"GET","path":"/api-clients","contract":"public-api","summary":"Registered clients for this developer","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ApiClient"},
"listCreditNotes": {"method":"GET","path":"/tenants/{tenantId}/credit-notes","contract":"subscription","summary":"List a tenant's credit notes","permission":"PLATFORM_BILLING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"invoiceId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrgUnits": {"method":"GET","path":"/org-units","contract":"tenancy","summary":"List scope nodes visible to the session","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"under","in":"query","required":null},{"name":"level","in":"query","required":null},{"name":"includeInactive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOwnPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants/mine","contract":"identity","summary":"The calling platform operator's own grants into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPlans": {"method":"GET","path":"/plans","contract":"subscription","summary":"List subscription plans","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"offeredToTenantId","in":"query","required":false},{"name":"packageKind","in":"query","required":false}],"requestBody":null,"responds":"Plan"},
"listProductionAccessRequests": {"method":"GET","path":"/production-access-requests","contract":"public-api","summary":"Production access requests, pending first","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSubscriptionInvoices": {"method":"GET","path":"/tenants/{tenantId}/invoices","contract":"subscription","summary":"List subscription invoices","permission":"PLATFORM_BILLING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTenantCells": {"method":"GET","path":"/tenants/{tenantId}/cells","contract":"subscription","summary":"List a tenant's cells","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"Cell"},
"listTenants": {"method":"GET","path":"/tenants","contract":"subscription","summary":"List tenants","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"planId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"previewSubscriptionChange": {"method":"POST","path":"/tenants/{tenantId}/subscription/preview","contract":"subscription","summary":"Preview the effect of a plan change","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetSubscriptionRequest","responds":"SubscriptionPreview"},
"provisionCell": {"method":"POST","path":"/tenants/{tenantId}/cells","contract":"subscription","summary":"Provision a cell for a region","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProvisionCellRequest","responds":null},
"reactivateTenant": {"method":"POST","path":"/tenants/{tenantId}/reactivate","contract":"subscription","summary":"Lift a suspension","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Tenant"},
"removeLicenceAddOn": {"method":"DELETE","path":"/tenants/{tenantId}/licences/add-ons","contract":"subscription","summary":"Remove an add-on","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LicencePosition"},
"setApiAnomalyRule": {"method":"PUT","path":"/api-anomaly-rules","contract":"public-api","summary":"When API traffic is flagged as abnormal","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApiAnomalyRule","responds":"ApiAnomalyRule"},
"setApiQuota": {"method":"PUT","path":"/api-quotas","contract":"public-api","summary":"Rate limits and throttling per client","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApiQuota","responds":"ApiQuota"},
"setSsoConfig": {"method":"PUT","path":"/tenants/sso-config","contract":"identity","summary":"Configure an identity provider","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SsoProviderConfig","responds":"SsoProviderConfig"},
"setSubscription": {"method":"PUT","path":"/tenants/{tenantId}/subscription","contract":"subscription","summary":"Assign or change a subscription","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetSubscriptionRequest","responds":"Subscription"},
"suspendTenant": {"method":"POST","path":"/tenants/{tenantId}/suspend","contract":"subscription","summary":"Suspend a tenant","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Tenant"},
"terminateTenant": {"method":"POST","path":"/tenants/{tenantId}/terminate","contract":"subscription","summary":"Begin termination","permission":"PLATFORM_TENANT_TERMINATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"updateTenant": {"method":"PATCH","path":"/tenants/{tenantId}","contract":"subscription","summary":"Amend tenant details","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Tenant"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApiAnomaly": {"type":"object","x-ticvai-persistence":"control.api_anomaly","description":"One flagged breach of an anomaly rule (M17-07).","required":["id","ruleKey","clientId","detectedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"ruleKey":{"type":"string"},"clientId":{"type":"string","format":"uuid","x-ticvai-references":"control.api_client"},"measure":{"type":"string"},"observed":{"type":"number"},"baseline":{"type":"number","nullable":true},"actionTaken":{"type":"string","enum":["flag","throttle","suspend"]},"detectedAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"ApiAnomalyRule": {"type":"object","x-ticvai-persistence":"control.api_anomaly_rule","description":"**When API traffic is abnormal** (17 September minutes, M17-07). Platform defaults ship for every tenant; TICVAI tightens them per tenant or per client.\n","required":["ruleKey","measure","comparison","threshold","action"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"ruleKey":{"type":"string"},"clientId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"control.api_client","description":"Null applies to every client of the tenant."},"measure":{"type":"string","enum":["callsPerMinute","clientErrorShare","allowListRefusals","unusualOperations","authFailures"]},"comparison":{"type":"string","enum":["aboveBaselineMultiple","aboveFixed"],"description":"`aboveBaselineMultiple`: above `threshold` x the same hour over the last four weeks."},"threshold":{"type":"number"},"windowMinutes":{"type":"integer","minimum":1,"default":5},"action":{"type":"string","enum":["flag","throttle","suspend"],"default":"flag"},"isActive":{"type":"boolean","default":true},"tenantId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The tenant a rule belongs to** (4 October 2026, CHG-FXC-003). Null for a platform default, which every tenant reads; `listApiAnomalyRules` returns the platform defaults and the caller tenant's own rules."},"scopePath":{"type":"string","nullable":true,"readOnly":true,"description":"The tenant's root scope path for a tenant rule (scope row-level security); null for a platform default."}}},
"ApiClient": {"type":"object","x-ticvai-persistence":"control.api_client","description":"CF-135a. **The one credential model.** 2.7.52, 7.1.25 and 7.1.30 each asserted their own, so a partner API key, a POS integration credential and a webstore credential were three unrelated things with three lifecycles.\n","required":["id","developerId","name","environment","scopes","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid"},"name":{"type":"string"},"clientId":{"type":"string","readOnly":true},"environment":{"type":"string","enum":["sandbox","production"],"description":"**Bound to one, stated on the object rather than by naming convention.** A key that works in both is a key somebody will use in the wrong one.\n"},"scopes":{"type":"array","description":"**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing. **Module scopes** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, one of `listApiScopes`.\n","items":{"type":"string","pattern":"^[a-zA-Z]+\\.(read|write)$"}},"issuedBy":{"type":"string","enum":["partner","ticvai"],"readOnly":true,"description":"Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`.\n"},"certificationListingId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"control.integration_listing","description":"For a production client, the certified integration it was issued against."},"credentialTtlDays":{"type":"integer","minimum":1,"maximum":730,"nullable":true,"description":"Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry)."},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the key stops working unless rotated. No token is issued after it."},"allowedTenantIds":{"type":"array","description":"13.1.46. **Which tenants this client may act for.** A developer integrating for one venue must not reach another, and a client with an empty list reaches none.\n","items":{"type":"string","format":"uuid"}},"ipAllowList":{"type":"array","description":"13.1.38. **Required on a production client** (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the internet); optional in the sandbox. CIDR ranges. Checked at token issue and on every call.\n","items":{"type":"string"}},"status":{"type":"string","enum":["active","suspended","revoked"],"readOnly":true},"lastUsedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**A credential unused for a year is a credential nobody will notice being stolen.**\n"}}},
"ApiQuota": {"type":"object","x-ticvai-persistence":"control.api_limit","description":"13.1.36 and 13.1.37. **A quota protects the venue, not the developer.**\n","required":["clientId","sustainedPerMinute"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"clientId":{"type":"string","format":"uuid"},"sustainedPerMinute":{"type":"integer"},"burstPerSecond":{"type":"integer","description":"**Separate from the sustained rate**, because a nightly sync is a legitimate spike and a flat per-second limit either blocks it or permits the flood it was meant to stop.\n"},"dailyCap":{"type":"integer","nullable":true},"perOperationOverrides":{"type":"object","additionalProperties":{"type":"integer"},"description":"**Availability checks and order creation deserve different limits** — one is cheap and polled, the other is expensive and rare.\n"},"onBreach":{"type":"string","enum":["throttle","reject","queue"],"default":"throttle"}}},
"ApiUsageSummary": {"type":"object","description":"13.1.16 to 13.1.20, 13.1.41 to 13.1.45. **One endpoint because they are one question asked five ways.**\n","properties":{"totalCalls":{"type":"integer"},"successRate":{"type":"number"},"clientErrorRate":{"type":"number","description":"**4xx — the integrator's problem.** Separated because a single error rate lets both sides blame the other.\n"},"serverErrorRate":{"type":"number","description":"5xx — TICVAI's problem."},"p50LatencyMs":{"type":"number"},"p95LatencyMs":{"type":"number"},"p99LatencyMs":{"type":"number"},"quotaBreaches":{"type":"integer"},"byOperation":{"type":"array","items":{"type":"object","properties":{"operationId":{"type":"string"},"calls":{"type":"integer"},"errorRate":{"type":"number"}}}}}},
"Cell": {"x-ticvai-persistence":"control.cell","x-ticvai-retired-columns":["tenant_id"],"type":"object","required":["id","name","regionId","countryCode","tier","status"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/CellKind"},"clusterId":{"type":"string","format":"uuid","nullable":true},"isReachable":{"type":"boolean","default":true,"description":"False for `onPremiseIsolated`, true for `onPremiseConnected` (ADR-0046). When false, the Control Plane holds the record for licensing and support and **cannot reach the installation** — it may sit behind a firewall with no inbound route. Every operation assuming reachability must handle absence rather than timing out, and a cell that has not called home for a month is not necessarily broken.\n"},"lastContactAt":{"type":"string","format":"date-time","nullable":true,"description":"When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first.\n"},"licenceExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. **An expired licence degrades rather than stops** — a venue whose gates refuse entry because a licence lapsed over a weekend is worse than one running unlicensed until Monday.\n"},"participatesInCrossCell":{"type":"boolean","default":true,"description":"False by default for `onPremiseIsolated`, available for `onPremiseConnected` (ADR-0046). Redeeming a pass issued elsewhere requires reaching the issuing cell at that moment, and an on-premise site may not be able to. Exclusion is the honest default; local-then-reconcile carries a double-redemption risk that needs a decision rather than an assumption.\n"},"regionId":{"type":"string","format":"uuid"},"regionName":{"type":"string"},"countryCode":{"type":"string"},"tier":{"$ref":"#/components/schemas/CellTier"},"status":{"$ref":"#/components/schemas/CellStatus"},"cloudProvider":{"type":"string","nullable":true},"cloudRegion":{"type":"string","nullable":true},"apiEndpoint":{"type":"string","nullable":true},"venueCount":{"type":"integer"},"provisionedAt":{"type":"string","format":"date-time","nullable":true},"deploymentRef":{"type":"string","nullable":true,"description":"**A pointer to where this cell runs, not a description of it.** A Kubernetes namespace, an ECS cluster ARN, a stack name — whatever the orchestrator calls the thing.\n\n**The platform does not model instances, nodes or shards** (31 August). Kubernetes already holds instance counts and they change by the second; a table copying them drifts within minutes and the copy would win.\n\n**The line is: routing decisions belong to the platform, provisioning facts belong to the orchestrator.** Qdrant is the proof — ADR-0021 makes the tenant *the* shard key, so nine operations route without a lookup and **a stored shard assignment would be a second copy of something derivable.**\n\n**CF-161 needed a table after all, and this said it did not.** The claim here was that one database per cell or one per service is a build-time decision and the DDL is identical either way. **ADR-0038 answered it per tenant**, which drops `Cell.tenantId`, adds `CellTenant`, `RolloutTenant` and a per-tenant migration row, and takes `control` out of the tenant template. `tools/derive-ddl.py` carried the same claim in its docstring.\n\n**A claim that a question cannot affect your artefact is the one most likely to be left standing after it does**, which is why the correction is recorded here rather than the sentence simply deleted."}}},
"CellCapacity": {"type":"object","x-ticvai-persistence":"none — measured, not stored","required":["cellId","isConstrained","dimensions","measuredAt"],"properties":{"cellId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/CellKind"},"tenantCount":{"type":"integer","description":"Reported, and **deliberately not the sizing signal.** Forty quiet tenants may load a cell less than three busy ones.\n"},"isConstrained":{"type":"boolean"},"constrainedDimension":{"type":"string","nullable":true},"dimensions":{"type":"array","description":"Per dimension, because the response differs. Short of connections and long on storage is a different problem from short of both.\n","items":{"type":"object","required":["dimension","used","headroom"],"properties":{"dimension":{"type":"string","enum":["concurrentUsers","transactionsPerSecond","scansPerSecond","databaseConnections","storageGb","replicationLag","cpu"]},"used":{"type":"number"},"limit":{"type":"number"},"headroom":{"type":"number","description":"Fraction remaining. Negative means already over."},"peakAt":{"type":"string","format":"date-time","nullable":true}}}},"forecastBreachAt":{"type":"string","format":"date-time","nullable":true,"description":"When the constrained dimension is projected to run out at the current trend. Null where there is no trend to project — an honest null beats an invented date.\n"},"measuredAt":{"type":"string","format":"date-time"}}},
"CellKind": {"type":"string","description":"Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law requires it.\n\n**On-premise is two configurations, not one (ADR-0046).** `onPremiseIsolated` keeps no channel to TICVAI — updates are pull-initiated or physically delivered, licensing is a signed file, support is blind. `onPremiseConnected` keeps an outbound control channel and is reachable, updatable and licensable in the ordinary way. The channel carries control traffic only and no natural person (ADR-0043); **AI inference is data, not control**, so connectivity alone does not grant the assistant.\n\nThere is no `hybrid`. The RFP's third model is answered by `onPremiseConnected`; a genuine split workload has never been asked for and would be a new decision.\n\n\n**`burst` added 31 August.** An environment stood up for one on-sale and torn down after (CF-162 scenario c). **It is not a jurisdiction and it is not permanent** — it holds a catalogue snapshot, three services of sixteen, and 17 tables of 380.\n\n**The other four are places data lives. This one is a place data passes through**, which is why it has its own lifecycle and a reconciliation obligation the others do not.","enum":["shared","dedicated","onPremiseIsolated","onPremiseConnected","controlPlane","burst"]},
"CellStatus": {"type":"string","enum":["provisioning","active","migrating","suspended","decommissioning","failed"]},
"CellTier": {"type":"string","enum":["shared","dedicated","isolated","clientHosted"]},
"CreatePlanRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","cellTier","licensedModules","limits","basePrice"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"cellTier":{"$ref":"#/components/schemas/CellTier"},"licensedModules":{"type":"array","minItems":1,"description":"**A closed set as of 24 August.** `moduleKey` was a free string, so nothing could join a licence to a screen — **a tenant without an F&B licence was still served every F&B screen**, because no screen said which module it belonged to in a form the licence could match.\n**The key is the join.** `screen.requiresModule` names one of these, and navigation is built from the intersection of what a tenant licensed and what their role permits.\n","items":{"$ref":"#/components/schemas/ModuleKey"}},"limits":{"type":"array","items":{"$ref":"#/components/schemas/EntitlementLimit"}},"basePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"billingPeriod":{"type":"string","enum":["monthly","quarterly","annual"]},"includesBrandedApp":{"type":"boolean","description":"Branded native publishing carries per-tenant operational cost and is priced, not absorbed.\n"},"includedAiTokens":{"type":"integer","nullable":true,"description":"AI tokens the package includes per billing period. Usage beyond it is a `metered` invoice line at the AI module's price (decided 29 September)."},"requestLimits":{"$ref":"#/components/schemas/PlanRequestLimits"},"packageKind":{"type":"string","enum":["standard","custom"],"default":"standard","description":"**Three standard packages, and custom ones allowed** (decided 29 September, Chinmay)."},"offeredToTenantId":{"type":"string","format":"uuid","nullable":true,"description":"**Private to one tenant** (decided 29 September, Chinmay): a custom package offered only to this tenant; `listPlans` shows it to no other tenant and `setSubscription` refuses it for any other (422 `plan-not-offered`). Null for a package any tenant may buy. Custom packages only."}}},
"CreateScopeNodeRequest": {"type":"object","required":["level","parentId","code","name"],"properties":{"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","description":"Required for every level except tenant, which the cell creates at provisioning."},"code":{"type":"string","maxLength":64,"pattern":"^[a-z0-9_]+$","description":"Becomes the final ltree segment. Immutable once created."},"name":{"type":"string","maxLength":200}}},
"CreateTenantRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","billingEmail"],"properties":{"code":{"type":"string","maxLength":64,"pattern":"^[a-z0-9-]+$"},"name":{"type":"string","maxLength":200},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500},"accountManagerPrincipalId":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid"}}},
"DowngradeConflictProblem": {"x-ticvai-persistence":"none — error shape","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Problem"},{"type":"object","properties":{"modulesInUse":{"type":"array","description":"Enabled by the tenant but not licensed by the target plan.","items":{"type":"object","properties":{"moduleKey":{"type":"string"},"displayName":{"type":"string"},"isEnabled":{"type":"boolean"}}}},"limitsExceeded":{"type":"array","items":{"type":"object","properties":{"metric":{"$ref":"#/components/schemas/UsageMetric"},"currentUsage":{"type":"integer"},"targetLimit":{"type":"integer"}}}}}}]},
"EntitlementLimit": {"type":"object","required":["metric","limit"],"properties":{"metric":{"$ref":"#/components/schemas/UsageMetric"},"limit":{"type":"integer","nullable":true,"x-ticvai-column":"limit_value","description":"Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure `limit_value`."},"overageAllowed":{"type":"boolean","default":false},"overageUnitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"EntitlementUsage": {"x-ticvai-persistence":"none — aggregated from usage_record","type":"object","required":["tenantId","metrics"],"properties":{"tenantId":{"type":"string","format":"uuid"},"metrics":{"type":"array","items":{"type":"object","required":["metric","current","isNearLimit"],"properties":{"metric":{"$ref":"#/components/schemas/UsageMetric"},"current":{"type":"integer"},"limit":{"type":"integer","nullable":true},"percentUsed":{"type":"number","nullable":true},"isNearLimit":{"type":"boolean","description":"Approaching a limit is an account conversation. Hitting one silently at a gate is an incident.\n"},"isExceeded":{"type":"boolean"}}}},"asAt":{"type":"string","format":"date-time"}}},
"InvoiceStatus": {"type":"string","enum":["draft","issued","paid","overdue","disputed","cancelled"]},
"LicenceAddOn": {"x-ticvai-persistence":"control.licence_add_on + control.licence_add_on_limit","x-ticvai-retired-columns":["plan_id"],"description":"**Belongs to the tenant, not the plan.** Add-ons survive a plan change unless explicitly removed (`addLicenceAddOn`), so a row keyed on `plan_id` would be lost, or silently re-applied to every tenant on that plan, at the first plan change. The tenant comes from the path. `limitOverrides` are child rows in `control.licence_add_on_limit`.","type":"object","required":["moduleKey"],"properties":{"tenantId":{"type":"string","format":"uuid","readOnly":true,"description":"The tenant the add-on was sold to — the `tenantId` in the path, never the body."},"moduleKey":{"type":"string"},"limitOverrides":{"type":"array","items":{"$ref":"#/components/schemas/EntitlementLimit"}},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"validFrom":{"type":"string","format":"date"},"validTo":{"type":"string","format":"date","nullable":true},"note":{"type":"string","maxLength":500}}},
"LicencePosition": {"x-ticvai-persistence":"none — union of the tenant's plan (control.tenant.plan_id -> subscription.plan_module, subscription.plan_limit) and its add-ons (control.licence_add_on, control.licence_add_on_limit by tenant_id)","type":"object","required":["tenantId","licensedModules","limits"],"properties":{"poweredByRemovable":{"type":"boolean","readOnly":true,"default":false,"description":"**Whether the tenant's licence lets it switch \"Powered by TICVAI\" off** (Chinmay, 2 October, workbook Q160 and the pre-apply round; CHG-CSA-036). False by default; true where TICVAI sold the tenant the add-on keyed `poweredByRemoval` (`addLicenceAddOn`). White label's `setBrandIdentity` refuses `showPoweredBy` false while this is false."},"tenantId":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid","nullable":true},"licensedModules":{"type":"array","description":"Union of plan modules and add-ons. The White Label Builder reads this and cannot enable anything absent from it.\n\n**`moduleKey` values are `ModuleKey`s** (4 October 2026, CHG-FXC-010; ADM-424), the vocabulary of\n`white-label.ModuleEnablement.moduleKey`.","items":{"type":"object","required":["moduleKey","source"],"properties":{"moduleKey":{"type":"string"},"displayName":{"type":"string"},"source":{"type":"string","enum":["plan","addOn"]},"validTo":{"type":"string","format":"date","nullable":true}}}},"limits":{"type":"array","items":{"$ref":"#/components/schemas/EntitlementLimit"}}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"ModuleKey": {"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},
"OrgUnit": {"x-ticvai-persistence":"platform.scope","type":"object","required":["id","level","path","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","nullable":true},"path":{"type":"string","description":"Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"isActive":{"type":"boolean","description":"False causes every permission query at or beneath this node to resolve to DENY.\n"},"childCount":{"type":"integer","minimum":0}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE","CORE_AI_PUBLISH","TICKETING_AI_PUBLISH","ACCESS_AI_PUBLISH","FNB_AI_PUBLISH","RETAIL_AI_PUBLISH","INVENTORY_AI_PUBLISH","SEATING_AI_PUBLISH","MEMBERSHIP_AI_PUBLISH","MARKETING_AI_PUBLISH","RESOURCES_AI_PUBLISH","QUEUE_AI_PUBLISH","TRANSPORT_AI_PUBLISH","GAMES_AI_PUBLISH","MAINTENANCE_AI_PUBLISH","ACCREDITATION_AI_PUBLISH","PARTNER_AI_PUBLISH","ANALYTICS_AI_PUBLISH","BIOMETRIC_IMAGE_VIEW","ACCESS_DIRECTION_SET","REPORT_GOVERNANCE_MANAGE"]},
"Plan": {"x-ticvai-persistence":"subscription.plan + subscription.plan_module + subscription.plan_limit","description":"**A plan's modules and limits are rows, keyed on `plan_id`.** `licensedModules` and `limits` are required on every plan, and `subscription.plan` alone had no column for either — so the licence position, the downgrade check and every module gate had nothing to read. `plan_module` holds one row per licensed `ModuleKey`; `plan_limit` one row per `EntitlementLimit`. Both belong to the plan version the row is, so a subscriber on an earlier version keeps the modules and limits they were sold.","allOf":[{"$ref":"#/components/schemas/CreatePlanRequest"},{"type":"object","required":["id","version","isActive","subscriberCount"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string","description":"Existing subscribers stay on the version they were sold. A price change never applies retroactively.\n"},"isActive":{"type":"boolean"},"subscriberCount":{"type":"integer"},"publishedAt":{"type":"string","format":"date-time"}}}]},
"PlanRequestLimits": {"type":"object","nullable":true,"x-ticvai-persistence":"none — embedded in subscription.plan as its request_limits jsonb column","description":"**The limits section of a plan: every tenant has a request budget** (ADR-0064, accepted 1 October; it decides the per-tenant limit ADR-0032 deferred). A token bucket per tenant and audience in the kernel middleware of `commerce`, `access` and `operations`, counted in Azure Managed Redis so every replica agrees; a guest browse never spends a till's budget. Over budget, the call is refused `429` with `Retry-After` and the `RateLimit-*` headers (every operation declares it).\n\n**Null takes the platform default**, which starts at twice the tenant's expected peak from its sizing tier (`handoff/sizing.json` venue tiers) and is recalibrated after the benchmark and after four weeks of production. **A tenant may use the whole platform when others are quiet**: the per-replica share (`replicaSharePercent`) is enforced only above `shareEnforcedAbovePercent` of the replica's limit. If Redis is unavailable each replica falls back to its own buckets (the limit divided by the replica count); the request path never fails because the limiter's store did.","properties":{"guest":{"$ref":"#/components/schemas/RequestBudget"},"staff":{"$ref":"#/components/schemas/RequestBudget"},"service":{"$ref":"#/components/schemas/RequestBudget"},"partner":{"$ref":"#/components/schemas/RequestBudget"},"replicaSharePercent":{"type":"integer","minimum":1,"maximum":100,"default":25,"description":"The most of one replica's request slots one tenant may hold while the share is enforced."},"shareEnforcedAbovePercent":{"type":"integer","minimum":1,"maximum":100,"default":70,"description":"The replica load, as a percent of its limit, above which the share is enforced."}}},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"ProductionAccessRequest": {"type":"object","x-ticvai-persistence":"control.production_access_request","description":"**A developer's request for production keys** (17 September minutes, M17-06): sandbox, then certification, then production.\n","required":["id","developerId","sandboxClientId","listingId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid","readOnly":true},"sandboxClientId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"control.api_client"},"listingId":{"type":"string","format":"uuid","x-ticvai-references":"control.integration_listing"},"scopes":{"type":"array","items":{"type":"string"}},"allowedTenantIds":{"type":"array","items":{"type":"string","format":"uuid"}},"ipAllowList":{"type":"array","items":{"type":"string"}},"note":{"type":"string","nullable":true},"status":{"type":"string","enum":["pending","approved","rejected","withdrawn"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"reason":{"type":"string","nullable":true,"readOnly":true},"productionClientId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"control.api_client"},"requestedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ProvisionCellRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["regionId","countryCode","tier"],"properties":{"regionId":{"type":"string","format":"uuid"},"countryCode":{"type":"string","pattern":"^[A-Z]{2}$","description":"Determines the jurisdiction. Placement must be within it — this is enforced, not trusted.\n"},"tier":{"$ref":"#/components/schemas/CellTier"},"cloudProvider":{"type":"string"},"cloudRegion":{"type":"string"},"clientHostedEndpoint":{"type":"string","nullable":true,"description":"Required for `clientHosted`, where no in-region cloud exists."}}},
"ScopeLevel": {"type":"string","description":"**The eight organisational levels, plus `subject`.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition of the eight levels and this mirrors them so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n\n**`subject` is the one value tenancy does not have, and it is not a level.** It is here because `check-package` reads this enum as the closed vocabulary for `x-ticvai-scope-level`, and some operations act on one guest's own resources, which sit in no node of the venue hierarchy. So `subject` is valid as an operation's scope level and never as a `ScopeRef.level`: every `ScopeRef` is a row of `platform.scope`, and those carry one of the eight.\n","enum":["tenant","brand","region","venue","department","subDepartment","workstation","outlet","subject"]},
"SetSubscriptionRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["planId"],"properties":{"planId":{"type":"string","format":"uuid"},"planVersion":{"type":"string","description":"Defaults to the current version."},"effectiveFrom":{"type":"string","format":"date","description":"Optional, and set by the server if omitted. Today for an upgrade, `renewsAt` for a downgrade; any other date is refused (audit R214 (1))."},"prorate":{"type":"boolean","default":true,"description":"An upgrade is always prorated and a downgrade, which starts at renewal, never is (audit R214 (1)). Kept so a preview can show the unprorated figure; `setSubscription` applies the rule whatever is sent."},"note":{"type":"string","maxLength":500}}},
"SsoGroupMapping": {"x-ticvai-persistence":"identity.sso_group_mapping","type":"object","required":["externalGroup","roleId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — the response returned the external group, the role and the scope, which is everything a caller needs and not the row own identity.\n**(provider, external_group) is unique and would serve**, but a mapping is edited and revoked by an administrator, and **a row addressed by the values it holds cannot be corrected** — changing the group means deleting a mapping and creating another, which loses who granted it and when.\n"},"externalGroup":{"type":"string"},"roleId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"Scope the mapped role is granted at."}}},
"SsoProtocol": {"type":"string","enum":["oidc","saml2"]},
"SsoProviderConfig": {"x-ticvai-persistence":"identity.sso_provider","type":"object","required":["id","displayName","protocol","groupMappings"],"properties":{"id":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"protocol":{"$ref":"#/components/schemas/SsoProtocol"},"metadataUrl":{"type":"string","nullable":true},"issuer":{"type":"string","nullable":true},"clientId":{"type":"string","nullable":true},"clientSecretRef":{"type":"string","nullable":true,"description":"Key vault reference. The secret itself is never returned."},"groupMappings":{"type":"array","minItems":1,"description":"**A group with no mapping grants nothing.** No default role, ever — otherwise the identity provider becomes a way to mint access nobody configured.\n","items":{"$ref":"#/components/schemas/SsoGroupMapping"}},"autoProvisionPrincipals":{"type":"boolean","default":false,"description":"Create a principal on first successful sign-in."},"isEnforced":{"type":"boolean","default":false},"isActive":{"type":"boolean"}}},
"Subscription": {"x-ticvai-persistence":"subscription.contract","type":"object","required":["tenantId","planId","planVersion","status","startsAt"],"properties":{"tenantId":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid"},"planName":{"type":"string"},"planVersion":{"type":"string"},"status":{"type":"string","enum":["trial","active","pastDue","cancelled","expired"]},"startsAt":{"type":"string","format":"date"},"renewsAt":{"type":"string","format":"date","nullable":true},"cancelledAt":{"type":"string","format":"date","nullable":true},"scheduledChange":{"type":"object","nullable":true,"readOnly":true,"description":"A downgrade waiting for the next renewal (decided 28 September, audit R214 (1)). Null when none is scheduled.","properties":{"planId":{"type":"string","format":"uuid"},"planVersion":{"type":"string"},"effectiveFrom":{"type":"string","format":"date","description":"Always the `renewsAt` it was scheduled against."}}},"currentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"billingPeriod":{"type":"string"}}},
"SubscriptionCreditNote": {"type":"object","x-ticvai-persistence":"control.credit_note + control.credit_note_line","description":"**A credit note against one tenant invoice** (20.7.7, 29 September build): its own number, lines, tax and total. The invoice it credits is never edited.","required":["id","creditNoteNumber","invoiceId","tenantId","reasonCode","settlement","total","issuedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"creditNoteNumber":{"type":"string","readOnly":true,"description":"**Gapless, per issuing legal entity, in its own sequence** (the R152 rule for invoices, decided 28 September, applied to credit notes): assigned at issue, never reused."},"invoiceId":{"type":"string","description":"The invoice credited."},"tenantId":{"type":"string","format":"uuid"},"reasonCode":{"type":"string","enum":["billingError","serviceCredit","disputeResolution","goodwill","other"]},"reason":{"type":"string","maxLength":500,"nullable":true},"settlement":{"type":"string","enum":["offsetNextInvoice","refund"]},"settlementStatus":{"type":"string","enum":["pending","offset","refunded"],"readOnly":true,"description":"`offset` once a later invoice has taken it; `refunded` once the refund is recorded."},"lines":{"type":"array","items":{"type":"object","properties":{"invoiceLineIndex":{"type":"integer"},"description":{"type":"string"},"quantity":{"type":"number","nullable":true},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"issuedAt":{"type":"string","format":"date-time","readOnly":true},"issuedByPrincipalId":{"type":"string","format":"uuid","readOnly":true}}},
"SubscriptionInvoice": {"x-ticvai-persistence":"control.invoice + control.invoice_line","type":"object","required":["id","invoiceNumber","tenantId","periodStart","periodEnd","status","total"],"properties":{"id":{"type":"string","format":"uuid"},"invoiceNumber":{"type":"string","readOnly":true,"description":"A tax invoice number, so **gapless, per legal entity** (decided 28 September, audit R152): one unbroken sequence for the TICVAI legal entity that issues it, assigned when the invoice is issued, never reused. A cancelled invoice keeps its number.\n"},"tenantId":{"type":"string","format":"uuid"},"periodStart":{"type":"string","format":"date"},"periodEnd":{"type":"string","format":"date"},"status":{"$ref":"#/components/schemas/InvoiceStatus"},"lines":{"type":"array","items":{"type":"object","properties":{"description":{"type":"string"},"kind":{"type":"string","enum":["basePlan","module","addOn","overage","metered","oneOff","credit"],"description":"`module`, one per licensed module at its platform price, and `metered`, usage such as AI tokens (decided 29 September)."},"moduleCode":{"type":"string","nullable":true,"description":"The module a `module` or `metered` line charges for."},"audience":{"type":"string","enum":["staff","guest"],"nullable":true,"description":"For an AI `metered` line, whose usage it is."},"metric":{"$ref":"#/components/schemas/UsageMetric"},"quantity":{"type":"number"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"planVersionUsed":{"type":"string","description":"Priced against the version the tenant is subscribed to, not the latest."},"creditedTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"The sum of the credit notes issued against this invoice (`issueCreditNote`); the invoice itself is never edited. Null with none."},"issuedAt":{"type":"string","format":"date-time","nullable":true},"dueAt":{"type":"string","format":"date","nullable":true},"paidAt":{"type":"string","format":"date-time","nullable":true}}},
"SubscriptionPreview": {"x-ticvai-persistence":"none — computed","type":"object","required":["canApply","priceChange"],"properties":{"canApply":{"type":"boolean"},"priceChange":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"proratedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"modulesGained":{"type":"array","items":{"type":"string"}},"modulesLost":{"type":"array","items":{"type":"string"}},"conflicts":{"$ref":"#/components/schemas/DowngradeConflictProblem"},"cellTierChange":{"type":"object","nullable":true,"properties":{"from":{"$ref":"#/components/schemas/CellTier"},"to":{"$ref":"#/components/schemas/CellTier"},"requiresMigration":{"type":"boolean"}}}}},
"SuspensionMode": {"type":"string","description":"Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n","enum":["readOnly","noNewSales","fullLockout"]},
"Tenant": {"x-ticvai-persistence":"control.tenant","type":"object","required":["id","code","name","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"$ref":"#/components/schemas/TenantStatus"},"suspensionMode":{"$ref":"#/components/schemas/SuspensionMode"},"suspensionReason":{"type":"string","nullable":true},"suspensionEffectiveAt":{"type":"string","format":"date-time","nullable":true,"description":"When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."},"suspensionNoticeMessage":{"$ref":"#/components/schemas/LocalisedText","description":"The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."},"terminationScheduledAt":{"type":"string","format":"date-time","nullable":true,"description":"When `terminateTenant` started the retention window. Null when no termination is under way."},"terminationRetentionUntil":{"type":"string","format":"date-time","nullable":true,"description":"`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."},"terminationReason":{"type":"string","maxLength":1000,"nullable":true},"terminationRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"planId":{"type":"string","format":"uuid","nullable":true},"planName":{"type":"string","nullable":true},"cellCount":{"type":"integer"},"venueCount":{"type":"integer"},"regionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500,"nullable":true,"description":"Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."},"accountManagerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantDetail": {"x-ticvai-persistence":"control.tenant","allOf":[{"$ref":"#/components/schemas/Tenant"},{"type":"object","properties":{"subscription":{"$ref":"#/components/schemas/Subscription"},"cells":{"type":"array","items":{"$ref":"#/components/schemas/Cell"}},"licences":{"$ref":"#/components/schemas/LicencePosition"}}}]},
"TenantStatus": {"type":"string","enum":["onboarding","active","suspended","terminating","terminated"]},
"UsageMetric": {"type":"string","enum":["venues","workstations","activeUsers","devices","brandedApps","aiTokens","apiCalls","storageGb","transactions","guestProfiles"]},
"UsageReport": {"x-ticvai-persistence":"none — aggregated","type":"object","required":["tenantId","periodStart","periodEnd","metrics"],"properties":{"tenantId":{"type":"string","format":"uuid"},"periodStart":{"type":"string","format":"date"},"periodEnd":{"type":"string","format":"date"},"metrics":{"type":"array","items":{"type":"object","properties":{"metric":{"$ref":"#/components/schemas/UsageMetric"},"total":{"type":"number"},"included":{"type":"number","nullable":true},"overage":{"type":"number"},"byVenue":{"type":"array","items":{"type":"object","properties":{"venueId":{"type":"string","format":"uuid"},"quantity":{"type":"number"}}}},"byCapability":{"type":"array","description":"AI tokens only.","items":{"type":"object","properties":{"capability":{"type":"string"},"quantity":{"type":"number"}}}}}}}}}
}
```
