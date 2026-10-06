# P09-releases-environments-01 — P09 · Releases & Environments

**8 screens · 28 operations · 28 schemas · 8 permissions**

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
  `DEVELOPER_ADMIN, PLATFORM_MIGRATION_APPLY, PLATFORM_MIGRATION_VIEW, PLATFORM_RELEASE_MANAGE, PLATFORM_RELEASE_PROMOTE, PLATFORM_RELEASE_VIEW, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
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
| `ADM-022` | Release & Version Management | B | 17 | 25 | 6 | 1 | 2 | 0 | — | notStarted (generated) |
| `ADM-023` | Staging Promotion & Approval | B | 7 | 23 | 6 | 1 | 2 | 5 | — | notStarted (generated) |
| `ADM-024` | Release Notification Composer | B | 7 | 21 | 6 | 1 | 1 | 0 | — | notStarted (generated) |
| `ADM-025` | Tenant Upgrade Scheduler | B | 8 | 14 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-026` | End-of-Support Notice Management | B | 16 | 16 | 7 | 1 | 1 | 0 | — | notStarted (generated) |
| `ADM-027` | Database Migration Console | B | 14 | 26 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-028` | Environment Registry | B | 8 | 14 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-700` | Configuration Promotion | B | 11 | 13 | 6 | 0 | 0 | 2 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-025, ADM-028 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-022` Release & Version Management

**Cut releases and move them through the environments.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 2 · needs the `core` module |
| Block | Block B · ticket #29217 (APP-CONSOLE-ADM-022) |
| Who uses it | ticvai staff holding `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_PROMOTE`, `PLATFORM_RELEASE_VIEW` (1 configure, 1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listReleases` reads the population and `getRelease` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `releaseId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/release-and-version-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — new scope, 30 Jul

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Releases of the platform: their components, migrations, breaking changes and readiness; create, promote to staging and production, reject or withdraw. Promotion shows readiness first.

**Fixed on main** (the package already carries these; draw what it says): Purpose "for this venue". (CHG-WIR-023); ADM-022 and ADM-023 declare the same seven release operations. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every release' drop id, createdByPrincipalId. (CHG-SBO-004).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Draft · In dev · In staging · In production · Superseded · Withdrawn | — | Sends `?status=` to `listReleases`. | `listReleases` ?status |
| Environment | segmented control | optional | — | Dev · Staging · Production | — | Sends `?environment=` to `listReleases`. | `listReleases` ?environment |

**Form: Create release** (modal, opened by *Create release*; *Create release* calls `createRelease`, *Cancel* sends nothing)

**Collects what `createRelease` sends before it is called.** Required: `components`, `note`. Optional: `requiredMigrations`, `breakingChanges`, `guestReleaseNotes` (the public "what's new" for guests, one short text per locale, naming no person; decided 29 September, rev 3 GAP-B2). Guests read it on the Help screen once the release reaches their cell; `note` stays internal. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Version `version` | text field | required | — | — | — | — | `createRelease` body |
| Components `components` | repeatable rows | required | — | at least 1 | — | — | `createRelease` body |
| Component `components[].component` | radio group | required | — | Backend · Frontend · AI · Infra · Contracts | — | — | `createRelease` body |
| Version `components[].version` | text field | required | — | — | — | — | `createRelease` body |
| Image digest `components[].imageDigest` | text field | optional | — | — | — | — | `createRelease` body |
| Required migrations `requiredMigrations` | list of values (chips) | optional | — | — | — | Migration versions this release depends on. | `createRelease` body |
| Note `note` | text area | required | — | min length 3; max length 2000 | — | Internal. Never shown to guests; `guestReleaseNotes` is. | `createRelease` body |
| Guest release notes `guestReleaseNotes` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | The public, localised "what's new" for guests (decided 29 September, rev 3 GAP-B2), one short text per locale, written for a guest and naming no person. | `createRelease` body |
| Breaking changes `breakingChanges` | list of values (chips) | optional | — | — | — | — | `createRelease` body |

Errors to draw in the form: 400 A required migration is absent, or a component version does not exist in the registry.

**Form: Promote release** (modal, opened by *Promote release*; *Promote release* calls `promoteRelease`, *Cancel* sends nothing)

**Collects what `promoteRelease` sends before it is called.** Required: `targetEnvironment`, `note`. Optional: `approverPrincipalId`, `stepUpToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target environment `targetEnvironment` | segmented control | required | — | Dev · Staging · Production | — | — | `promoteRelease` body |
| Note `note` | text area | required | — | min length 3; max length 1000 | — | — | `promoteRelease` body |
| Approver principal `approverPrincipalId` | picker: choose an approver principal | optional | — | — | shows names, sends the id | Required for production. May not be the requester. | `promoteRelease` body |
| Step up token `stepUpToken` | text field | optional | — | — | — | Required for production. Proves a factor was presented just now. | `promoteRelease` body |

Errors to draw in the form: 403 Approver is the requester, or the step-up token is absent or expired; 409 Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. (PromotionBlockedProblem)

**Sent by *Reject release*** (`rejectRelease`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `rejectRelease` body |

**Sent by *Withdraw release*** (`withdrawRelease`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `withdrawRelease` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **stepUpToken**: Never a visible field. It is what verifyMfaChallenge returns after the in-place challenge, short-lived and single-purpose; the form shows the challenge step, not a token box. *(source: contracts/spine/identity.yaml#verifyMfaChallenge)*

#### Outputs: what the screen shows and produces

**Shown**

**Every release** (data table, from `listReleases`)

| Shows | Format | Notes |
|---|---|---|
| Components | list or chips (count when long) | — |
| Required migrations | list or chips (count when long) | Migration versions this release depends on. |
| Note | text | Internal. Never shown to guests; `guestReleaseNotes` is. |
| Guest release notes | in the reader's language | The public, localised "what's new" for guests (decided 29 September, rev 3 GAP-B2), one short text per locale, written for a guest and … |
| Breaking changes | list or chips (count when long) | — |
| Status | chip: Draft, In dev, In staging, In production, Superseded, Withdrawn | — |
| Promoted to staging at | 1 Oct 2026, 14:30 | — |
| Promoted to production at | 1 Oct 2026, 14:30 | — |

**The selected release** (detail panel, from `listReleases`)

| Shows | Format | Notes |
|---|---|---|
| Components | list or chips (count when long) | — |
| Required migrations | list or chips (count when long) | Migration versions this release depends on. |
| Note | text | Internal. Never shown to guests; `guestReleaseNotes` is. |
| Guest release notes | in the reader's language | The public, localised "what's new" for guests (decided 29 September, rev 3 GAP-B2), one short text per locale, written for a guest and … |
| Breaking changes | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Status | chip: Draft, In dev, In staging, In production, Superseded, Withdrawn | — |
| Created by principal | the name it points at, never the id | — |
| Promoted to staging at | 1 Oct 2026, 14:30 | — |
| Promoted to production at | 1 Oct 2026, 14:30 | — |

**The release readiness** (detail panel, from `getReleaseReadiness`)

| Shows | Format | Notes |
|---|---|---|
| Release | the name it points at, never the id | — |
| Can promote | yes / no (icon or chip) | — |
| Target environment | chip: Dev, Staging, Production | — |
| Gates | list or chips (count when long) | — |

**The release** (detail panel, from `getRelease`)

| Shows | Format | Notes |
|---|---|---|
| Rollouts | list or chips (count when long) | — |
| Cells on this version | 1,234 | — |
| Cells total | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Create release (primary button) | `createRelease` POST `/releases` | CreateReleaseRequest | Release | 400 A required migration is absent, or a component version does not exist in the registry. | opens modal first |
| Promote release (secondary button) | `promoteRelease` POST `/releases/{releaseId}/promote` | inline | Rollout | 403 Approver is the requester, or the step-up token is absent or expired; 409 Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. (PromotionBlockedProblem) | opens modal first |
| Reject release (destructive button) | `rejectRelease` POST `/releases/{releaseId}/reject` | inline | no body | 409 Not in a state that permits this | — |
| Withdraw release (destructive button) | `withdrawRelease` POST `/releases/{releaseId}/withdraw` | inline | no body | 409 Not in a state that permits this | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (cellsTotal)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Promote release**: Shows readiness checks; blocked names what fails; production promotion needs the promote permission. *(source: contracts/satellite/platform-ops.yaml#promoteRelease)*
- **Promote release**: Separate from Save. The publish gate names what goes live, where and from when before it happens; blocked names what is wrong and how to fix it; an override past a warning is recorded with who authorised it. *(source: screens/_components.yaml#publishGate; contracts/satellite/platform-ops.yaml#promoteRelease)*

**Data it reads**: `listReleases` (onLoad, Release list)

**Where the user goes next**

- → `ADM-027` Database Migration Console: *Plans the migrations the release requires*
- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

**What opens over it**

- confirmDialog *Reject release*: **Names what `rejectRelease` changes and what it leaves alone**, in the consequence rather than the verb. A release version this affects should be identified in the dialog, not just counted. **Collects what `rejectRelease` sends before it is called.** Required: `reason`.
- confirmDialog *Withdraw release*: **Names what `withdrawRelease` changes and what it leaves alone**, in the consequence rather than the verb. A release version this affects should be identified in the dialog, not just counted. **Collects what `withdrawRelease` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The release version list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the release version untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No release version yet. Offers Create release (`createRelease`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, environment and the release version are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listReleases` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_MANAGE` for `createRelease`, `withdrawRelease`; `PLATFORM_RELEASE_PROMOTE` for `promoteRelease`, `rejectRelease`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A required migration is absent, or a component version does not exist in the registry.; 409 Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. (PromotionBlockedProblem); 409 Not in a state that permits this |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_RELEASE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_RELEASE_MANAGE for Create release, Withdraw release; PLATFORM_RELEASE_PROMOTE for Promote release, Reject release. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/platform-ops.yaml#createRelease)*
- **promoteRelease answers 403**: Show it as something the person can act on, not a failure: Approver is the requester, or the step-up token is absent or expired *(source: contracts/satellite/platform-ops.yaml#promoteRelease)*
- **promoteRelease answers 409**: Show it as something the person can act on, not a failure: Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. *(source: contracts/satellite/platform-ops.yaml#promoteRelease)*
- **rejectRelease answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/platform-ops.yaml#rejectRelease)*
- **withdrawRelease answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/platform-ops.yaml#withdrawRelease)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
releases:
- version: 2026.10.1
  status: staging
  breakingChanges: 0
  migrations: 3
  promotedToStaging: 30/09/2026 22:00
- version: 2026.09.4
  status: production
  promotedToProduction: 22/09/2026 02:00
```

#### Permissions

- `listReleases` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `getRelease` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `getReleaseReadiness` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `createRelease` → `PLATFORM_RELEASE_MANAGE` (configure) · staff
- `promoteRelease` → `PLATFORM_RELEASE_PROMOTE` (operate) · staff
- `rejectRelease` → `PLATFORM_RELEASE_PROMOTE` (operate) · staff
- `withdrawRelease` → `PLATFORM_RELEASE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listReleases` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_MANAGE` for `createRelease`, `withdrawRelease`; `PLATFORM_RELEASE_PROMOTE` for `promoteRelease`, `rejectRelease`.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.1 | All business functionality available through the TAIS user interface shall be exposed through documented APIs unless restricted by security, compliance or operational considerations. | Developer & API Management | CONTRACTED | `listReleases` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Minor releases are notified but optional and customers can postpone them. Major releases carry advance notice, a defined support lifecycle, end-of-support announcements for old versions and a mandatory upgrade (e.g. Version 3 -> End of Support Notice -> Version 4). *(agreed · MoM 30 Jul 2026, 6. Global Versioning Strategy · DI-054)*
- Releases go to staging first; customers are notified of each new version with new features, bug fixes and release notes, test in staging, and approve before promotion to production. *(agreed · MoM 30 Jul 2026, 4. Deployment Workflow Discussion · DI-053)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-022` · status **notStarted** · provenance generated
- Flow F04 *Platform admin ships a release*, step 1: Reviews the release and its readiness → Sees which gates pass and which block, before attempting anything

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-022?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Create release, Promote release, Reject release, Withdraw release, What publishing changes.
- [ ] Every transition is wired: `ADM-027`, `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_PROMOTE`, `PLATFORM_RELEASE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-023` Staging Promotion & Approval

**Approve or reject a release's promotion out of staging.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 2 · needs the `core` module |
| Block | Block B · ticket #29218 (APP-CONSOLE-ADM-023) |
| Who uses it | ticvai staff holding `PLATFORM_RELEASE_PROMOTE`, `PLATFORM_RELEASE_VIEW` (1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listReleases` reads the population and `getReleaseReadiness` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `releaseId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/staging-promotion-and-approval` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): ADM-022 and ADM-023 declared the same seven release operations; ADM-023 is the staging approval step only, so cutting and withdrawing a release stay on ADM-022 … Removed 2 October 2026 (CHG-WIR-021): ADM-022 and ADM-023 declared the same seven release operations; ADM-023 is the staging approval step only, so cutting and withdrawing a release stay on ADM-022 … Open: No contract — new scope, 30 Jul

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The approval step between staging and production for a release: soak time, readiness, approve or reject with reason.

**Fixed on main** (the package already carries these; draw what it says): Purpose "for this venue"; same operations as ADM-022. (CHG-WIR-023); Tables show every schema field, plumbing included: 'Every release' drop id, createdByPrincipalId. (CHG-SBO-004).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Draft · In dev · In staging · In production · Superseded · Withdrawn | — | Sends `?status=` to `listReleases`. | `listReleases` ?status |
| Environment | segmented control | optional | — | Dev · Staging · Production | — | Sends `?environment=` to `listReleases`. | `listReleases` ?environment |

**Form: Promote release** (modal, opened by *Promote release*; *Promote release* calls `promoteRelease`, *Cancel* sends nothing)

**Collects what `promoteRelease` sends before it is called.** Required: `targetEnvironment`, `note`. Optional: `approverPrincipalId`, `stepUpToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target environment `targetEnvironment` | segmented control | required | — | Dev · Staging · Production | — | — | `promoteRelease` body |
| Note `note` | text area | required | — | min length 3; max length 1000 | — | — | `promoteRelease` body |
| Approver principal `approverPrincipalId` | picker: choose an approver principal | optional | — | — | shows names, sends the id | Required for production. May not be the requester. | `promoteRelease` body |
| Step up token `stepUpToken` | text field | optional | — | — | — | Required for production. Proves a factor was presented just now. | `promoteRelease` body |

Errors to draw in the form: 403 Approver is the requester, or the step-up token is absent or expired; 409 Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. (PromotionBlockedProblem)

**Sent by *Reject release*** (`rejectRelease`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `rejectRelease` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **stepUpToken**: Never a visible field. It is what verifyMfaChallenge returns after the in-place challenge, short-lived and single-purpose; the form shows the challenge step, not a token box. *(source: contracts/spine/identity.yaml#verifyMfaChallenge)*

#### Outputs: what the screen shows and produces

**Shown**

**Every release** (data table, from `listReleases`)

| Shows | Format | Notes |
|---|---|---|
| Components | list or chips (count when long) | — |
| Required migrations | list or chips (count when long) | Migration versions this release depends on. |
| Note | text | Internal. Never shown to guests; `guestReleaseNotes` is. |
| Breaking changes | list or chips (count when long) | — |
| Status | chip: Draft, In dev, In staging, In production, Superseded, Withdrawn | — |
| Promoted to staging at | 1 Oct 2026, 14:30 | — |
| Promoted to production at | 1 Oct 2026, 14:30 | — |

**The selected release** (detail panel, from `listReleases`)

| Shows | Format | Notes |
|---|---|---|
| Components | list or chips (count when long) | — |
| Required migrations | list or chips (count when long) | Migration versions this release depends on. |
| Note | text | Internal. Never shown to guests; `guestReleaseNotes` is. |
| Breaking changes | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Status | chip: Draft, In dev, In staging, In production, Superseded, Withdrawn | — |
| Created by principal | the name it points at, never the id | — |
| Promoted to staging at | 1 Oct 2026, 14:30 | — |
| Promoted to production at | 1 Oct 2026, 14:30 | — |

**The release** (detail panel, from `getRelease`)

| Shows | Format | Notes |
|---|---|---|
| Rollouts | list or chips (count when long) | — |
| Cells on this version | 1,234 | — |
| Cells total | 1,234 | — |

**The release readiness** (detail panel, from `getReleaseReadiness`)

| Shows | Format | Notes |
|---|---|---|
| Release | the name it points at, never the id | — |
| Can promote | yes / no (icon or chip) | — |
| Target environment | chip: Dev, Staging, Production | — |
| Gates | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Promote release (primary button) | `promoteRelease` POST `/releases/{releaseId}/promote` | inline | Rollout | 403 Approver is the requester, or the step-up token is absent or expired; 409 Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. (PromotionBlockedProblem) | opens modal first |
| Reject release (destructive button) | `rejectRelease` POST `/releases/{releaseId}/reject` | inline | no body | 409 Not in a state that permits this | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (cellsTotal)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Promote release**: Separate from Save. The publish gate names what goes live, where and from when before it happens; blocked names what is wrong and how to fix it; an override past a warning is recorded with who authorised it. *(source: screens/_components.yaml#publishGate; contracts/satellite/platform-ops.yaml#promoteRelease)*

**Data it reads**: `listReleases` (onLoad, List releases)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-029` Deployment Monitor: *Watches the rollout per cell*; carries `rolloutId`; calls `promoteRelease`

**What opens over it**

- confirmDialog *Reject release*: **Names what `rejectRelease` changes and what it leaves alone**, in the consequence rather than the verb. A staging promotion approval this affects should be identified in the dialog, not just counted. **Collects what `rejectRelease` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staging promotion approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staging promotion approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staging promotion approval yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, environment and the staging promotion approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listReleases` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_PROMOTE` for `promoteRelease`, `rejectRelease`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. (PromotionBlockedProblem); 409 Not in a state that permits this |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_RELEASE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_RELEASE_PROMOTE for Promote release, Reject release; PLATFORM_RELEASE_MANAGE for Create release, Withdraw release. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/platform-ops.yaml#promoteRelease)*
- **promoteRelease answers 403**: Show it as something the person can act on, not a failure: Approver is the requester, or the step-up token is absent or expired *(source: contracts/satellite/platform-ops.yaml#promoteRelease)*
- **promoteRelease answers 409**: Show it as something the person can act on, not a failure: Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. *(source: contracts/satellite/platform-ops.yaml#promoteRelease)*
- **rejectRelease answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/platform-ops.yaml#rejectRelease)*
- **withdrawRelease answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/platform-ops.yaml#withdrawRelease)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every release:
- note: Guest charged twice at Main Gate Till 3
  status: active
  promotedToStagingAt: 01/10/2026 09:14
  promotedToProductionAt: 01/10/2026 09:14
- note: Group of 40 from Desert Gate Tours
  status: pending
  promotedToStagingAt: 30/09/2026 18:02
  promotedToProductionAt: 30/09/2026 18:02
- note: Annual pass upgrade for the Al Nuaimi family
  status: suspended
  promotedToStagingAt: 28/09/2026 11:45
  promotedToProductionAt: 28/09/2026 11:45
```

#### Permissions

- `promoteRelease` → `PLATFORM_RELEASE_PROMOTE` (operate) · staff
- `getReleaseReadiness` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `getRelease` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `listReleases` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `rejectRelease` → `PLATFORM_RELEASE_PROMOTE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listReleases` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_PROMOTE` for `promoteRelease`, `rejectRelease`.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.1 | All business functionality available through the TAIS user interface shall be exposed through documented APIs unless restricted by security, compliance or operational considerations. | Developer & API Management | CONTRACTED | `listReleases` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Post-go-live, only configuration changes tested in staging (e.g. a new product or package) should be promoted to production, never transactional data; feasibility pending the CI/CD engineer. *(open · MoM 10 Sep 2026, 4.13 Pre-Production to Production Configuration Promotion · DI-834)*
- Releases go to staging first; customers are notified of each new version with new features, bug fixes and release notes, test in staging, and approve before promotion to production. *(agreed · MoM 30 Jul 2026, 4. Deployment Workflow Discussion · DI-053)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-023` · status **notStarted** · provenance generated
- Flow F04 *Platform admin ships a release*, step 3: Requests promotion with an approver → Approval recorded against the release. The approver may not be the requester
- Flow F04 branch at step 3 (recoverable): when The plan has gone stale, Apply is refused. Cell state changed since the plan was computed, and applying it would run against a different world than the one reviewed.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (23 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-023?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Promote release, Reject release, What publishing changes.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-029`.
- [ ] Every gated control is gated: `PLATFORM_RELEASE_PROMOTE`, `PLATFORM_RELEASE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-024` Release Notification Composer

**Tell tenants about a release before and after it ships.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 3 · needs the `core` module |
| Block | Block B · ticket #29222 (APP-CONSOLE-ADM-024) |
| Who uses it | ticvai staff holding `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSupportNotices` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/general/release-notification-composer` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — new scope, 30 Jul

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Compose and publish the notice tenants see about a release (what changes, when, guest release notes).

**Fixed on main** (the package already carries these; draw what it says): Purpose "Push live ... for this venue". (CHG-WIR-023); formPublishSupportNotice asks the person for publishedAt, id. (CHG-SBO-004); Tables show every schema field, plumbing included: 'Every support notice' drop id, affectedTenantIds, publishedByPrincipalId, scopePath … (CHG-SBO-004); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Draft · In dev · In staging · In production · Superseded · Withdrawn | `listReleases` ?status |
| Environment | segmented control | — | Dev · Staging · Production | `listReleases` ?environment |

**Form: Publish support notice** (modal, opened by *Publish support notice*; *Publish support notice* calls `publishSupportNotice`, *Cancel* sends nothing)

**Collects what `publishSupportNotice` sends before it is called.** Required: `supportEndsAt`. Optional: `message`, `publishedByPrincipalId`, `scopePath`. **Not asked:** `id` is a client UUIDv7 generated silently; `publishedAt` is set by the server (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets it (readOnly in the contract): `affectedTenantIds` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `publishSupportNotice` body |
| Version `version` | text field | required | — | — | — | — | `publishSupportNotice` body |
| Support ends at `supportEndsAt` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `publishSupportNotice` body |
| Message `message` | key and value settings | optional | — | — | — | — | `publishSupportNotice` body |
| Published by principal `publishedByPrincipalId` | picker: choose a published by principal | optional | — | — | shows names, sends the id | — | `publishSupportNotice` body |
| Published at `publishedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishSupportNotice` body |
| Scope path `scopePath` | text field | optional | — | — | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row … | `publishSupportNotice` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every support notice** (data table, from `listSupportNotices`)

| Shows | Format | Notes |
|---|---|---|
| Support ends at | 1 Oct 2026 | — |
| Message | grouped details | — |
| Published at | 1 Oct 2026, 14:30 | — |

**Every release** (data table, from `listReleases`)

| Shows | Format | Notes |
|---|---|---|
| Components | list or chips (count when long) | — |
| Required migrations | list or chips (count when long) | Migration versions this release depends on. |
| Note | text | Internal. Never shown to guests; `guestReleaseNotes` is. |
| Guest release notes | in the reader's language | The public, localised "what's new" for guests (decided 29 September, rev 3 GAP-B2), one short text per locale, written for a guest and … |
| Breaking changes | list or chips (count when long) | — |
| Status | chip: Draft, In dev, In staging, In production, Superseded, Withdrawn | — |
| Promoted to staging at | 1 Oct 2026, 14:30 | — |
| Promoted to production at | 1 Oct 2026, 14:30 | — |

**The selected support notice** (detail panel, from `listSupportNotices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Support ends at | 1 Oct 2026 | — |
| Message | grouped details | — |
| Affected tenants | list or chips (count when long) | Computed from cell versions, never typed. A notice to the wrong list is worse than none. |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**What's new for guests** (detail panel, from `listReleases`): **The public, localised release notes a guest reads on the Help screen** (decided 29 September, rev 3 GAP-B2; WEB-025, WEB-045, GST-040 through `getTenantAppStatus.whatsNew`, the ten newest). Written with the release on ADM-022 (`createRelease.guestReleaseNotes`); shown here beside the staff notice so the two are composed together and say the same thing. Distinct from the staff-only recent …

| Shows | Format | Notes |
|---|---|---|
| Version | text | — |
| Guest release notes | in the reader's language | The public, localised "what's new" for guests (decided 29 September, rev 3 GAP-B2), one short text per locale, written for a guest and … |
| Promoted to production at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Publish support notice (primary button) | `publishSupportNotice` POST `/support-notices` | SupportNotice | SupportNotice | — | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Publish support notice**: Separate from Save. The publish gate names what goes live, where and from when before it happens; blocked names what is wrong and how to fix it; an override past a warning is recorded with who authorised it. *(source: screens/_components.yaml#publishGate; contracts/satellite/platform-ops.yaml#publishSupportNotice)*

**Data it reads**: `listSupportNotices` (onLoad, End-of-support notices); `listReleases` (onLoad, Releases and their readiness)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The release notification composer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the release notification composer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No release notification composer yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listSupportNotices` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_MANAGE` for `publishSupportNotice`. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_RELEASE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_RELEASE_MANAGE for Publish support notice. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/platform-ops.yaml#publishSupportNotice)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every support notice:
- supportEndsAt: 01/10/2026 09:14
  publishedAt: 01/10/2026 09:14
- supportEndsAt: 30/09/2026 18:02
  publishedAt: 30/09/2026 18:02
- supportEndsAt: 28/09/2026 11:45
  publishedAt: 28/09/2026 11:45
```

#### Permissions

- `publishSupportNotice` → `PLATFORM_RELEASE_MANAGE` (configure) · staff
- `listSupportNotices` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `listReleases` → `PLATFORM_RELEASE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_MANAGE` for `publishSupportNotice`.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.1 | All business functionality available through the TAIS user interface shall be exposed through documented APIs unless restricted by security, compliance or operational considerations. | Developer & API Management | CONTRACTED | `listReleases` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Releases go to staging first; customers are notified of each new version with new features, bug fixes and release notes, test in staging, and approve before promotion to production. *(agreed · MoM 30 Jul 2026, 4. Deployment Workflow Discussion · DI-053)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-024` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (21 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-024?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Publish support notice, What publishing changes.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-025` Tenant Upgrade Scheduler

**Schedule or defer each tenant's upgrade.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 2 · needs the `core` module |
| Block | Block B · ticket #29211 (APP-CONSOLE-ADM-025) |
| Who uses it | ticvai staff holding `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listUpgradeSchedules` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/general/tenant-upgrade-scheduler` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — new scope, 30 Jul

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Schedule each tenant's upgrade to a release, within the deferral a tenant may take; deferred upgrades show the reason and the latest date.

**Fixed on main** (the package already carries these; draw what it says): Purpose "for this venue". (CHG-WIR-023); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Form: Schedule tenant upgrade** (modal, opened by *Schedule tenant upgrade*; *Schedule tenant upgrade* calls `scheduleTenantUpgrade`, *Cancel* sends nothing)

**Collects what `scheduleTenantUpgrade` sends before it is called.** Required: `releaseVersion`, `scheduledFor`. Optional: `tenantName`, `deferredByTenant`, `deferralReason`, `maxDeferralUntil`, `notifiedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tenant `tenantId` | picker: choose a tenant | required | — | — | shows names, sends the id | — | `scheduleTenantUpgrade` body |
| Tenant name `tenantName` | text field | optional | — | — | — | — | `scheduleTenantUpgrade` body |
| Release version `releaseVersion` | text field | required | — | — | — | — | `scheduleTenantUpgrade` body |
| Scheduled for `scheduledFor` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `scheduleTenantUpgrade` body |
| Deferred by tenant `deferredByTenant` | toggle | optional | — | — | — | — | `scheduleTenantUpgrade` body |
| Deferral reason `deferralReason` | text field | optional | — | — | — | — | `scheduleTenantUpgrade` body |
| Max deferral until `maxDeferralUntil` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Beyond this the platform proceeds. An indefinitely deferred tenant becomes a version nobody supports. | `scheduleTenantUpgrade` body |
| Notified at `notifiedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `scheduleTenantUpgrade` body |

Errors to draw in the form: 400 Deferral exceeds the maximum permitted window

#### Outputs: what the screen shows and produces

**Shown**

**Every upgrade schedule** (data table, from `listUpgradeSchedules`)

| Shows | Format | Notes |
|---|---|---|
| Tenant name | text | — |
| Release version | text | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Deferred by tenant | yes / no (icon or chip) | — |
| Deferral reason | text | — |
| Max deferral until | 1 Oct 2026, 14:30 | Beyond this the platform proceeds. An indefinitely deferred tenant becomes a version nobody supports. |
| Notified at | 1 Oct 2026, 14:30 | — |

**The selected upgrade schedule** (detail panel, from `listUpgradeSchedules`)

| Shows | Format | Notes |
|---|---|---|
| Tenant name | text | — |
| Release version | text | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Deferred by tenant | yes / no (icon or chip) | — |
| Deferral reason | text | — |
| Max deferral until | 1 Oct 2026, 14:30 | Beyond this the platform proceeds. An indefinitely deferred tenant becomes a version nobody supports. |
| Notified at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Schedule tenant upgrade (primary button) | `scheduleTenantUpgrade` POST `/upgrade-schedules` | UpgradeSchedule | UpgradeSchedule | 400 Deferral exceeds the maximum permitted window | opens modal first |

**Data it reads**: `listUpgradeSchedules` (onLoad, Scheduled tenant upgrades)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tenant upgrade scheduler list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tenant upgrade scheduler untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tenant upgrade scheduler yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listUpgradeSchedules` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listUpgradeSchedules` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_MANAGE` for `scheduleTenantUpgrade`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Deferral exceeds the maximum permitted window |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_RELEASE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_RELEASE_MANAGE for Schedule tenant upgrade. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/platform-ops.yaml#scheduleTenantUpgrade)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
schedules:
- tenant: Marina Leisure Group
  release: 2026.10.1
  scheduledFor: 12/10/2026 03:00
  deferred: false
- tenant: Gulf Fun Parks LLC
  release: 2026.10.1
  deferred: true
  reason: Peak weekend
  maxDeferralUntil: 26/10/2026
```

#### Permissions

- `listUpgradeSchedules` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `scheduleTenantUpgrade` → `PLATFORM_RELEASE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listUpgradeSchedules` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_MANAGE` for `scheduleTenantUpgrade`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Minor releases are notified but optional and customers can postpone them. Major releases carry advance notice, a defined support lifecycle, end-of-support announcements for old versions and a mandatory upgrade (e.g. Version 3 -> End of Support Notice -> Version 4). *(agreed · MoM 30 Jul 2026, 6. Global Versioning Strategy · DI-054)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-025` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-025?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Schedule tenant upgrade.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-026` End-of-Support Notice Management

**Announce when a version or an API version reaches end of support.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 3 · needs the `core` module |
| Block | Block B · ticket #29225 (APP-CONSOLE-ADM-026) |
| Who uses it | ticvai staff holding `DEVELOPER_ADMIN`, `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 configure, 2 read, 1 operate) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSupportNotices` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `version` (navigation), `tenantId` (navigation) · cold entry: **Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one the screen says what is missing and offers that … |
| Route | `/general/end-of-support-notice-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `deprecateApiVersion` (DEVELOPER_ADMIN) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.**  Open: No contract — new scope, 30 Jul

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** End-of-support notices for versions, and API version deprecation, with the tenants affected.

**Fixed on main** (the package already carries these; draw what it says): Purpose "Answer a question without needing a person". (CHG-WIR-023); formPublishSupportNotice asks the person for publishedAt, id. (CHG-SBO-004); Tables show every schema field, plumbing included: 'Every support notice' drop id, affectedTenantIds, publishedByPrincipalId, scopePath. (CHG-SBO-004); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

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

**Form: Publish support notice** (modal, opened by *Publish support notice*; *Publish support notice* calls `publishSupportNotice`, *Cancel* sends nothing)

**Collects what `publishSupportNotice` sends before it is called.** Required: `supportEndsAt`. Optional: `message`, `publishedByPrincipalId`, `scopePath`. **Not asked:** `id` is a client UUIDv7 generated silently; `publishedAt` is set by the server (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets it (readOnly in the contract): `affectedTenantIds` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `publishSupportNotice` body |
| Version `version` | text field | required | — | — | — | — | `publishSupportNotice` body |
| Support ends at `supportEndsAt` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `publishSupportNotice` body |
| Message `message` | key and value settings | optional | — | — | — | — | `publishSupportNotice` body |
| Published by principal `publishedByPrincipalId` | picker: choose a published by principal | optional | — | — | shows names, sends the id | — | `publishSupportNotice` body |
| Published at `publishedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishSupportNotice` body |
| Scope path `scopePath` | text field | optional | — | — | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row … | `publishSupportNotice` body |

**Form: Deprecate API version** (modal, opened by *Deprecate API version*; *Deprecate API version* calls `deprecateApiVersion`, *Cancel* sends nothing)

**Collects what `deprecateApiVersion` sends before it is called.** Required: `sunsetAt`, `reason`. Optional: `migrationGuideUrl`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sunset at `sunsetAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `deprecateApiVersion` body |
| Reason `reason` | text area | required | — | — | — | — | `deprecateApiVersion` body |
| Migration guide URL `migrationGuideUrl` | text field | optional | — | — | — | — | `deprecateApiVersion` body |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `DEVELOPER_ADMIN` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

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

**Every support notice** (data table, from `listSupportNotices`)

| Shows | Format | Notes |
|---|---|---|
| Support ends at | 1 Oct 2026 | — |
| Message | grouped details | — |
| Published at | 1 Oct 2026, 14:30 | — |

**The selected support notice** (detail panel, from `listSupportNotices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Support ends at | 1 Oct 2026 | — |
| Message | grouped details | — |
| Affected tenants | list or chips (count when long) | Computed from cell versions, never typed. A notice to the wrong list is worse than none. |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (publish gate) | navigation or local | — | — | — | — |
| Publish support notice (primary button) | `publishSupportNotice` POST `/support-notices` | SupportNotice | SupportNotice | — | opens modal first |
| Deprecate API version (secondary button) | `deprecateApiVersion` POST `/api-versions/{version}/deprecate` | inline | ApiVersion | — | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Publish support notice**: Separate from Save. The publish gate names what goes live, where and from when before it happens; blocked names what is wrong and how to fix it; an override past a warning is recorded with who authorised it. *(source: screens/_components.yaml#publishGate; contracts/satellite/platform-ops.yaml#publishSupportNotice)*

**Data it reads**: `listSupportNotices` (onLoad, End-of-support notices); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The end-of-support notice list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the end-of-support notice untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No end-of-support notice yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listSupportNotices` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVELOPER_ADMIN` for `deprecateApiVersion` … |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `DEVELOPER_ADMIN`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_RELEASE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_RELEASE_MANAGE for Publish support notice; DEVELOPER_ADMIN for Deprecate API version. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/platform-ops.yaml#publishSupportNotice)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every support notice:
- supportEndsAt: 01/10/2026 09:14
  publishedAt: 01/10/2026 09:14
- supportEndsAt: 30/09/2026 18:02
  publishedAt: 30/09/2026 18:02
- supportEndsAt: 28/09/2026 11:45
  publishedAt: 28/09/2026 11:45
```

#### Permissions

- `listSupportNotices` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `publishSupportNotice` → `PLATFORM_RELEASE_MANAGE` (configure) · staff
- `deprecateApiVersion` → `DEVELOPER_ADMIN` (configure) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVELOPER_ADMIN` for `deprecateApiVersion` …

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Minor releases are notified but optional and customers can postpone them. Major releases carry advance notice, a defined support lifecycle, end-of-support announcements for old versions and a mandatory upgrade (e.g. Version 3 -> End of Support Notice -> Version 4). *(agreed · MoM 30 Jul 2026, 6. Global Versioning Strategy · DI-054)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-026` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-026?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Publish support notice, Deprecate API version, What publishing changes.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `DEVELOPER_ADMIN`, `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-027` Database Migration Console

**Plan, apply and roll back database migrations across the cells.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 1 · needs the `core` module |
| Block | Block B · ticket #29209 (APP-CONSOLE-ADM-027) |
| Who uses it | ticvai staff holding `PLATFORM_MIGRATION_APPLY`, `PLATFORM_MIGRATION_VIEW` (1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listMigrations` reads the population and `getVersionSkew` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `runId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/database-migration-console` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — the unowned orchestrator

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Plan and apply database migrations across cells, see version skew and roll back a run. Applying shows estimated lock time and whether a partitioned table is touched before it runs.

**Fixed on main** (the package already carries these; draw what it says): Purpose "for this venue". (CHG-WIR-023); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Applied to | picker: choose an applied to (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?appliedTo=` to `listMigrations`. | `listMigrations` ?appliedTo |
| Pending only | toggle | optional | off | — | — | Sends `?pendingOnly=` to `listMigrations`. | `listMigrations` ?pendingOnly |

**Form: Plan migration** (modal, opened by *Plan migration*; *Plan migration* calls `planMigration`, *Cancel* sends nothing)

**Collects what `planMigration` sends before it is called.** Required: `targetVersion`. Optional: `cellIds`, `environment`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target version `targetVersion` | text field | required | — | — | — | — | `planMigration` body |
| Cells `cellIds` | multi-picker: choose cells | optional | — | — | — | Omit to plan across every cell in scope. | `planMigration` body |
| Environment `environment` | segmented control | optional | — | Dev · Staging · Production | — | — | `planMigration` body |

Errors to draw in the form: 400 Target version unknown, or the path between versions is not contiguous

**Form: Apply migration** (modal, opened by *Apply migration*; *Apply migration* calls `applyMigration`, *Cancel* sends nothing)

**Collects what `applyMigration` sends before it is called.** Required: `planId`, `stepUpToken`. Optional: `canaryCellId`, `haltOnFirstFailure`, `maintenanceWindow`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Plan `planId` | picker: choose a plan | required | — | — | shows names, sends the id | — | `applyMigration` body |
| Step up token `stepUpToken` | text field | required | — | — | — | — | `applyMigration` body |
| Canary cell `canaryCellId` | picker: choose a canary cell | optional | — | — | shows names, sends the id | Applied alone and verified before the rest proceed. Defaults to the smallest cell in the plan. | `applyMigration` body |
| Halt on first failure `haltOnFirstFailure` | toggle | optional | on | — | — | — | `applyMigration` body |
| Maintenance window `maintenanceWindow` | group | optional | — | — | — | — | `applyMigration` body |
| Starts at `maintenanceWindow.startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `applyMigration` body |
| Ends at `maintenanceWindow.endsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `applyMigration` body |

Errors to draw in the form: 409 The plan is stale — cell state changed since it was computed. Re-plan and review before applying.

**Form: Rollback migration run** (modal, opened by *Rollback migration run*; *Rollback migration run* calls `rollbackMigrationRun`, *Cancel* sends nothing)

**Collects what `rollbackMigrationRun` sends before it is called.** Required: `reason`, `stepUpToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `rollbackMigrationRun` body |
| Step up token `stepUpToken` | text field | required | — | — | — | — | `rollbackMigrationRun` body |

Errors to draw in the form: 409 A migration in this run is irreversible (IrreversibleProblem)

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **stepUpToken**: Never a visible field. It is what verifyMfaChallenge returns after the in-place challenge, short-lived and single-purpose; the form shows the challenge step, not a token box. *(source: contracts/spine/identity.yaml#verifyMfaChallenge)*

#### Outputs: what the screen shows and produces

**Shown**

**Every migration** (data table, from `listMigrations`)

| Shows | Format | Notes |
|---|---|---|
| Module | text | — |
| Description | text | — |
| Rollback tested at | 1 Oct 2026, 14:30 | — |
| Checksum | text | Compared on apply. A migration edited after it was applied somewhere is a defect the register catches, not a mystery to debug later. |
| Applied cell count | 1,234 | — |
| Pending cell count | 1,234 | — |

**The selected migration** (detail panel, from `listMigrations`)

| Shows | Format | Notes |
|---|---|---|
| Module | text | — |
| Description | text | — |
| Is reversible | yes / no (icon or chip) | A rollback section exists and CI has executed it against a restored snapshot. A rollback nobody has run is a comment, not a rollback. |
| Rollback tested at | 1 Oct 2026, 14:30 | — |
| Checksum | text | Compared on apply. A migration edited after it was applied somewhere is a defect the register catches, not a mystery to debug later. |
| Estimated lock ms | 1,234 | — |
| Touches partitioned table | yes / no (icon or chip) | — |
| Applied cell count | 1,234 | — |
| Pending cell count | 1,234 | — |

**The migration run** (detail panel, from `getMigrationRun`)

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Queued, Canary, Running, Paused, Complete, Failed… | — |
| Tenants total | 1,234 | — |
| Tenants complete | 1,234 | — |
| Tenants failed | 1,234 | — |
| Cells total | 1,234 | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Cells | list or chips (count when long) | — |

**The version skew report** (detail panel, from `getVersionSkew`)

| Shows | Format | Notes |
|---|---|---|
| As at | 1 Oct 2026, 14:30 | — |
| Has unexplained skew | yes / no (icon or chip) | Skew during a rollout is expected. Skew outside one is a defect, and separating the two is the entire value of this report. |
| Cells | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Plan migration (primary button) | `planMigration` POST `/migrations/plan` | inline | MigrationPlan | 400 Target version unknown, or the path between versions is not contiguous | opens modal first |
| Apply migration (secondary button) | `applyMigration` POST `/migrations/apply` | inline | MigrationRun | 409 The plan is stale — cell state changed since it was computed. Re-plan and review before applying. | opens modal first |
| Rollback migration run (secondary button) | `rollbackMigrationRun` POST `/migrations/runs/{runId}/rollback` | inline | MigrationRun | 409 A migration in this run is irreversible (IrreversibleProblem) | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (cellsTotal, tenantsTotal)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listMigrations` (onLoad, The migration register); `getVersionSkew` (onLoad, Schema and application version per cell); `getMigrationRun` (onLoad, Migration run progress per cell)

**Where the user goes next**

- → `ADM-023` Staging Promotion & Approval: *Requests promotion with an approver*; calls `planMigration`
- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The database migration console list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the database migration console untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No database migration console yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on appliedTo, pendingOnly and the database migration console are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_MIGRATION_VIEW`, which `listMigrations` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_MIGRATION_APPLY` for `applyMigration`, `rollbackMigrationRun`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Target version unknown, or the path between versions is not contiguous; 409 A migration in this run is irreversible (IrreversibleProblem); 409 The plan is stale — cell state changed since it was computed. Re-plan and review before applying. |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_MIGRATION_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_MIGRATION_APPLY for Apply migration, Rollback migration run. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/platform-ops.yaml#applyMigration)*
- **applyMigration answers 409**: Show it as something the person can act on, not a failure: The plan is stale — cell state changed since it was computed. Re-plan and review before applying. *(source: contracts/satellite/platform-ops.yaml#applyMigration)*
- **rollbackMigrationRun answers 409**: Show it as something the person can act on, not a failure: A migration in this run is irreversible *(source: contracts/satellite/platform-ops.yaml#rollbackMigrationRun)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
migrations:
- module: identity
  description: Add credential history
  reversible: true
  estimatedLockMs: 120
  appliedCells: 14
  pendingCells: 3
```

#### Permissions

- `listMigrations` → `PLATFORM_MIGRATION_VIEW` (read) · staff
- `planMigration` → `PLATFORM_MIGRATION_VIEW` (read) · staff
- `applyMigration` → `PLATFORM_MIGRATION_APPLY` (operate) · staff
- `getVersionSkew` → `PLATFORM_MIGRATION_VIEW` (read) · staff
- `getMigrationRun` → `PLATFORM_MIGRATION_VIEW` (read) · staff
- `rollbackMigrationRun` → `PLATFORM_MIGRATION_APPLY` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_MIGRATION_VIEW`, which `listMigrations` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_MIGRATION_APPLY` for `applyMigration`, `rollbackMigrationRun`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-027` · status **notStarted** · provenance generated
- Flow F04 *Platform admin ships a release*, step 2: Plans the migrations the release requires → Sees per-cell migrations, estimated lock duration, and whether every one is reversible
- Flow F04 branch at step 2 (requiresStaff): when A migration in the release is irreversible, Named in the plan, not merely counted. A one-way door should be identified before it is walked through — promotion may still proceed, but knowingly.
- Flow F04 branch at step 2 (recoverable): when The plan predicts a long lock on a partitioned table, Surfaced as a warning with the affected cells. This is the output the plan step exists to produce.
- ADR-0014 *Cell Per Region* (`docs/adr/0014-cell-per-region.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-027?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Plan migration, Apply migration, Rollback migration run.
- [ ] Every transition is wired: `ADM-023`, `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_MIGRATION_APPLY`, `PLATFORM_MIGRATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-028` Environment Registry

**Keep the register of platform environments and the cells in each.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 2 · needs the `core` module |
| Block | Block B · ticket #29204 (APP-CONSOLE-ADM-028) |
| Who uses it | ticvai staff holding `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listEnvironments` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/general/environment-registry` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — not specified

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The environments (dev, test, staging, production) with their cells, soak hours and whether promotion needs approval.

**Fixed on main** (the package already carries these; draw what it says): Purpose "for this venue". (CHG-WIR-023); formRegisterEnvironment asks the person for id. (CHG-SBO-004); Tables show every schema field, plumbing included: 'Every environment' drop id, cellIds. (CHG-SBO-004).

#### Inputs: what the user enters or picks

**Form: Register environment** (modal, opened by *Register environment*; *Register environment* calls `registerEnvironment`, *Cancel* sends nothing)

**Collects what `registerEnvironment` sends before it is called.** Required: `kind`, `name`. Optional: `cellIds`, `requiresApprovalToPromote`, `soakHours`, `currentReleaseVersion`, `isActive`. **Not asked:** `id` is a client UUIDv7 generated silently (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `registerEnvironment` body |
| Kind `kind` | segmented control | required | — | Dev · Staging · Production | — | — | `registerEnvironment` body |
| Name `name` | text field | required | — | — | — | — | `registerEnvironment` body |
| Cells `cellIds` | multi-picker: choose cells | optional | — | — | — | — | `registerEnvironment` body |
| Requires approval to promote `requiresApprovalToPromote` | toggle | optional | — | — | — | — | `registerEnvironment` body |
| Soak hours `soakHours` | number field (hours) | optional | — | — | — | How long a release must sit here before it may be promoted. Zero for dev; a real number for staging, or staging is a formality. | `registerEnvironment` body |
| Current release version `currentReleaseVersion` | text field | optional | — | — | — | — | `registerEnvironment` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `registerEnvironment` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every environment** (data table, from `listEnvironments`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Dev, Staging, Production | — |
| Name | text | — |
| Requires approval to promote | yes / no (icon or chip) | — |
| Soak hours | 1,234 | How long a release must sit here before it may be promoted. Zero for dev; a real number for staging, or staging is a formality. |
| Current release version | text | — |
| Is active | yes / no (icon or chip) | — |

**The selected environment** (detail panel, from `listEnvironments`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Dev, Staging, Production | — |
| Name | text | — |
| Cells | list or chips (count when long) | — |
| Requires approval to promote | yes / no (icon or chip) | — |
| Soak hours | 1,234 | How long a release must sit here before it may be promoted. Zero for dev; a real number for staging, or staging is a formality. |
| Current release version | text | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Register environment (primary button) | `registerEnvironment` POST `/environments` | Environment | Environment | — | opens modal first |

**Data it reads**: `listEnvironments` (onLoad, Environment registry)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-700` Configuration Promotion: *Configuration Promotion*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The environment registry list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the environment registry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No environment registry yet. Offers Register environment (`registerEnvironment`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listEnvironments` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listEnvironments` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_MANAGE` for `registerEnvironment`. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_RELEASE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_RELEASE_MANAGE for Register environment. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/platform-ops.yaml#registerEnvironment)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every environment:
- kind: standard
  name: AquaCove Abu Dhabi
  isActive: true
- kind: standard
  name: Main Gate Till 3
  isActive: true
- kind: override
  name: Lagoon Grill
  isActive: false
```

#### Permissions

- `listEnvironments` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `registerEnvironment` → `PLATFORM_RELEASE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listEnvironments` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_MANAGE` for `registerEnvironment`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-028` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-028?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Register environment.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-700`.
- [ ] Every gated control is gated: `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-700` Configuration Promotion

**Move a tenant's configuration from one environment to another as a versioned package: export it, see the diff against the target, and apply it once approved.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 2 · needs the `core` module |
| Block | Block B · ticket #29206 (APP-CONSOLE-ADM-700) |
| Who uses it | ticvai staff holding `PLATFORM_MIGRATION_APPLY`, `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW` (1 operate, 1 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): One package moving through export, diff, approval and apply; each step shows its result before the next. |
| Offline | online only |
| Opens with | `packageId` (navigation), `challengeId` (navigation) · cold entry: Opened cold, it starts at Export package; with a package id it opens that package. |
| Route | `/releases-environments/configuration-promotion` |

**What the spec says about it.** **Added 2 October 2026** (Chinmay, DEC-168, ADR-0070; the lead's call on CHG-MOV-010; CHG-SBO-024). Configuration moves between environments as a versioned package exported with stable keys, diffed against the target, approved, applied as an idempotent upsert by key and audited; rollback re-applies the previous package; secrets and environment settings never travel in it. Production databases are never merged or reverse-migrated: schema goes forward through versioned migrations. **Platform permissions only** (PLATFORM_RELEASE_MANAGE, PLATFORM_RELEASE_VIEW, PLATFORM_MIGRATION_APPLY), so no tenant grant is opened here; ADM-122 stays in Venue Management for product import and export.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Source environment | picker: choose an id | optional | — | — | shows names, sends the id | Pick lists of the environment registry (ADM-028), never typed. | `Environment.id` |

**Form: Export package** (modal, opened by *Export package*; *Export package* calls `exportConfigPackage`, *Cancel* sends nothing)

**Collects what `exportConfigPackage` sends before it is called.** Required: `sourceEnvironment`. Optional: `kinds`. `kinds` narrows the package; secrets and environment settings never travel in it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Source environment `sourceEnvironment` | segmented control | required | — | Dev · Staging · Production | — | — | `exportConfigPackage` body |
| Kinds `kinds` | list of values (chips) | optional | — | — | — | The configuration kinds to include (e.g. products, price lists, access profiles, templates); all where absent. | `exportConfigPackage` body |

**Form: Compare with target** (modal, opened by *Compare with target*; *Compare with target* calls `diffConfigPackage`, *Cancel* sends nothing)

**Collects what `diffConfigPackage` sends before it is called.** Required: `targetEnvironment`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target environment `targetEnvironment` | segmented control | required | — | Dev · Staging · Production | — | — | `diffConfigPackage` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The package was exported for a different tenant than the target (`package-tenant-mismatch`).

**Form: Apply package** (modal, opened by *Apply package*; *Apply package* calls `applyConfigPackage`, *Cancel* sends nothing)

**Collects what `applyConfigPackage` sends before it is called.** Required: `diffId`, `stepUpToken`. Optional: `approvalRequestId`. `stepUpToken` comes from the authentication code asked in this dialog (`createMfaChallenge`, `verifyMfaChallenge`); `approvalRequestId` names the approval it rests on. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Diff `diffId` | picker: choose a diff | required | — | — | shows names, sends the id | — | `applyConfigPackage` body |
| Approval request `approvalRequestId` | picker: choose an approval request | optional | — | — | shows names, sends the id | The approved request for this diff. | `applyConfigPackage` body |
| Step up token `stepUpToken` | text field | required | — | — | — | — | `applyConfigPackage` body |

Errors to draw in the form: 409 The diff is stale (`diff-stale`), or not approved (`diff-not-approved`).

**Form: Apply package** (confirmDialog, opened by *Apply package*; *Send the code* calls `createMfaChallenge`, *Cancel* sends nothing)

Asks for the authentication code before the package is applied.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | text field | required | — | — | — | What the step-up is for. Recorded in the audit trail. | `createMfaChallenge` body |
| Method `methodId` | picker: choose a method | optional | — | — | shows names, sends the id | — | `createMfaChallenge` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | For a guest, the venue whose `VenueSettings.identity.guestTwoStep` applies (sign-in venue, or the venue of the booking being acted on). | `createMfaChallenge` body |

**Form: Verify** (confirmDialog, opened by *Verify*; *Verify* calls `verifyMfaChallenge`, *Cancel* sends nothing)

Verifies the code and returns the step-up token the apply needs.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `verifyMfaChallenge` body |

Errors to draw in the form: 410 The challenge has expired or was voided (by a fifth wrong code, or a newer challenge for the same purpose).; 422 A wrong code, attempts one to four (CHG-R1S-025; the r1 gate found only the fifth failure specified).

#### Outputs: what the screen shows and produces

**Shown**

**Package** (detail panel, from `exportConfigPackage`): What the package holds, by kind, and what it left out on purpose (secrets, environment settings).

| Shows | Format | Notes |
|---|---|---|
| Version | 1,234 | — |
| Source environment | chip: Dev, Staging, Production | — |
| Checksum | text | — |
| Record counts | grouped details | Records per configuration kind. |
| Excluded kinds | list or chips (count when long) | What never travels in a package (secrets, credentials, endpoints, environment settings). |
| Created at | 1 Oct 2026, 14:30 | — |

**Changes against the target** (data table, from `diffConfigPackage`): Every record to add, change or leave, by stable key; nothing applies that is not shown here.

| Shows | Format | Notes |
|---|---|---|
| Target environment | chip: Dev, Staging, Production | — |
| Computed at | 1 Oct 2026, 14:30 | — |
| Changes | list or chips (count when long) | — |

**Application** (detail panel, from `applyConfigPackage`): Rollback is re-applying `previousPackageId`.

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Applying, Applied, Failed | — |
| Applied count | 1,234 | — |
| Previous package | the name it points at, never the id | What a rollback re-applies. |
| Started at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What applying changes (publish gate) | navigation or local | — | — | — | — |
| Export package (primary button) | `exportConfigPackage` POST `/config-packages` | inline | ConfigPackage | — | opens modal first |
| Compare with target (secondary button) | `diffConfigPackage` POST `/config-packages/{packageId}/diff` | inline | ConfigPackageDiff | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The package was exported for a different tenant than the target (`package-tenant-mismatch`). | opens modal first |
| Apply package (secondary button) | `applyConfigPackage` POST `/config-packages/{packageId}/apply` | inline | ConfigPackageApplication | 409 The diff is stale (`diff-stale`), or not approved (`diff-not-approved`). | opens modal first |

**Data it reads**: `listEnvironments` (onLoad, The environments to move between)

**Where the user goes next**

- → `ADM-028` Environment Registry: *Environment Registry*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The package and its diff. |
| Error (`?state=error`) | Could not export, compare or apply; names which step failed and leaves the earlier results. |
| Empty, first run (`?state=emptyFirstRun`) | No package yet. Offers Export package (`exportConfigPackage`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: nothing on this screen filters. |
| Permission denied (`?state=emptyNoAccess`) | You don't have access to promote configuration — it needs TICVAI's release permissions. Named in words, never an empty table. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The diff is stale (`diff-stale`), or not approved (`diff-not-approved`).; 409 The package was exported for a different tenant than the target (`package-tenant-mismatch`).; 422 A wrong code, attempts one to four (CHG-R1S-025; the r1 gate found only the fifth failure specified). |

#### Permissions

- `listEnvironments` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `exportConfigPackage` → `PLATFORM_RELEASE_MANAGE` (configure) · staff
- `diffConfigPackage` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `applyConfigPackage` → `PLATFORM_MIGRATION_APPLY` (operate) · staff
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest

**A refused user sees:** You don't have access to promote configuration — it needs TICVAI's release permissions. Named in words, never an empty table.

Screen guard: `PLATFORM_RELEASE_VIEW`

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-700` · status **notStarted** · provenance generated
- ADR-0070 *Configuration moves to production as a versioned package; the schema only moves forward* (`docs/adr/0070-configuration-moves-as-a-versioned-package.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404, 409, 410, 422).
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-700?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What applying changes, Export package, Compare with target, Apply package.
- [ ] Every transition is wired: `ADM-028`.
- [ ] Every gated control is gated: `PLATFORM_MIGRATION_APPLY`, `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW`.
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

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"applyConfigPackage": {"method":"POST","path":"/config-packages/{packageId}/apply","contract":"platform-ops","summary":"Apply an approved package to the target environment","permission":"PLATFORM_MIGRATION_APPLY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"applyMigration": {"method":"POST","path":"/migrations/apply","contract":"platform-ops","summary":"Apply a planned migration run","permission":"PLATFORM_MIGRATION_APPLY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createRelease": {"method":"POST","path":"/releases","contract":"platform-ops","summary":"Cut a release","permission":"PLATFORM_RELEASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReleaseRequest","responds":"Release"},
"deprecateApiVersion": {"method":"POST","path":"/api-versions/{version}/deprecate","contract":"public-api","summary":"Announce a sunset date and notify subscribers","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApiVersion"},
"diffConfigPackage": {"method":"POST","path":"/config-packages/{packageId}/diff","contract":"platform-ops","summary":"Compare a package with the target environment","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConfigPackageDiff"},
"exportConfigPackage": {"method":"POST","path":"/config-packages","contract":"platform-ops","summary":"Export a tenant's configuration as a versioned package","permission":"PLATFORM_RELEASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConfigPackage"},
"getMigrationRun": {"method":"GET","path":"/migrations/runs/{runId}","contract":"platform-ops","summary":"Migration run progress per cell","permission":"PLATFORM_MIGRATION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MigrationRun"},
"getRelease": {"method":"GET","path":"/releases/{releaseId}","contract":"platform-ops","summary":"Read a release with its rollout state","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ReleaseDetail"},
"getReleaseReadiness": {"method":"GET","path":"/releases/{releaseId}/readiness","contract":"platform-ops","summary":"Whether a release can be promoted, and what blocks it","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ReleaseReadiness"},
"getVersionSkew": {"method":"GET","path":"/migrations/version-skew","contract":"platform-ops","summary":"Schema and application version across every cell","permission":"PLATFORM_MIGRATION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"VersionSkewReport"},
"listEnvironments": {"method":"GET","path":"/environments","contract":"platform-ops","summary":"The environment registry","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"Environment"},
"listMigrations": {"method":"GET","path":"/migrations","contract":"platform-ops","summary":"The migration register","permission":"PLATFORM_MIGRATION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"appliedTo","in":"query","required":null},{"name":"pendingOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOwnPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants/mine","contract":"identity","summary":"The calling platform operator's own grants into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReleases": {"method":"GET","path":"/releases","contract":"platform-ops","summary":"List releases","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"environment","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSupportNotices": {"method":"GET","path":"/support-notices","contract":"platform-ops","summary":"End-of-support notices","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SupportNotice"},
"listTenants": {"method":"GET","path":"/tenants","contract":"subscription","summary":"List tenants","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"planId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listUpgradeSchedules": {"method":"GET","path":"/upgrade-schedules","contract":"platform-ops","summary":"Scheduled tenant upgrades","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"UpgradeSchedule"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"planMigration": {"method":"POST","path":"/migrations/plan","contract":"platform-ops","summary":"Plan a migration run without applying it","permission":"PLATFORM_MIGRATION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MigrationPlan"},
"promoteRelease": {"method":"POST","path":"/releases/{releaseId}/promote","contract":"platform-ops","summary":"Promote a release to the next environment","permission":"PLATFORM_RELEASE_PROMOTE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"publishSupportNotice": {"method":"POST","path":"/support-notices","contract":"platform-ops","summary":"Publish an end-of-support notice","permission":"PLATFORM_RELEASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SupportNotice","responds":"SupportNotice"},
"registerEnvironment": {"method":"POST","path":"/environments","contract":"platform-ops","summary":"Register an environment","permission":"PLATFORM_RELEASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Environment","responds":"Environment"},
"rejectRelease": {"method":"POST","path":"/releases/{releaseId}/reject","contract":"platform-ops","summary":"Reject a release back a stage","permission":"PLATFORM_RELEASE_PROMOTE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"rollbackMigrationRun": {"method":"POST","path":"/migrations/runs/{runId}/rollback","contract":"platform-ops","summary":"Roll a migration run back","permission":"PLATFORM_MIGRATION_APPLY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"scheduleTenantUpgrade": {"method":"POST","path":"/upgrade-schedules","contract":"platform-ops","summary":"Schedule or defer a tenant upgrade","permission":"PLATFORM_RELEASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"UpgradeSchedule","responds":"UpgradeSchedule"},
"verifyMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge/{challengeId}/verify","contract":"identity","summary":"Complete a sign-in or step-up challenge","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"withdrawRelease": {"method":"POST","path":"/releases/{releaseId}/withdraw","contract":"platform-ops","summary":"Withdraw a release","permission":"PLATFORM_RELEASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApiVersion": {"type":"object","x-ticvai-persistence":"control.api_version","description":"13.1.31 to 13.1.35, ADR-0026. **CF-141 is sharper under D1**: a single supported production version was tenable when only Softlabs called the API, and **with third parties a breaking change with no window breaks somebody else's business.**\n","required":["version","status"],"properties":{"version":{"type":"string"},"status":{"type":"string","enum":["preview","current","deprecated","sunset"]},"releasedAt":{"type":"string","format":"date-time"},"deprecatedAt":{"type":"string","format":"date-time","nullable":true},"sunsetAt":{"type":"string","format":"date-time","nullable":true},"minimumNoticeMonths":{"type":"integer","default":12,"description":"**The commitment, not the intention.** A deprecation policy without a stated minimum is a policy that shortens under pressure.\n"},"migrationGuideUrl":{"type":"string","nullable":true},"activeClientCount":{"type":"integer","readOnly":true},"changes":{"type":"array","description":"**The developer changelog for this version** (17 September minutes, M17-14): every operation added, changed, deprecated or removed, and whether the change is breaking under ADR-0026. Generated at release from the contract diff; shown on DEV-001.\n","items":{"type":"object","required":["operationId","kind"],"properties":{"operationId":{"type":"string"},"contract":{"type":"string"},"kind":{"type":"string","enum":["added","changed","deprecated","removed"]},"breaking":{"type":"boolean","default":false},"summary":{"type":"string"}}}}}},
"ComponentVersion": {"type":"object","required":["component","version"],"properties":{"component":{"type":"string","enum":["backend","frontend","ai","infra","contracts"]},"version":{"type":"string"},"imageDigest":{"type":"string","nullable":true}}},
"ConfigPackage": {"type":"object","x-ticvai-persistence":"control.config_package","description":"A tenant's configuration exported with stable keys (`exportConfigPackage`, CHG-CSA-034). Immutable.","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"tenantId":{"type":"string","format":"uuid"},"sourceEnvironment":{"$ref":"#/components/schemas/EnvironmentKind"},"version":{"type":"integer","readOnly":true},"checksum":{"type":"string","readOnly":true},"recordCounts":{"type":"object","additionalProperties":{"type":"integer"},"description":"Records per configuration kind."},"excludedKinds":{"type":"array","description":"What never travels in a package (secrets, credentials, endpoints, environment settings).","items":{"type":"string"}},"createdAt":{"type":"string","format":"date-time","readOnly":true}}},
"ConfigPackageDiff": {"type":"object","x-ticvai-persistence":"control.config_package_diff","description":"What applying a package would change in a target environment, by stable key (CHG-CSA-034).","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"packageId":{"type":"string","format":"uuid"},"targetEnvironment":{"$ref":"#/components/schemas/EnvironmentKind"},"computedAt":{"type":"string","format":"date-time"},"changes":{"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","type":"array","items":{"type":"object","properties":{"kind":{"type":"string"},"stableKey":{"type":"string"},"change":{"type":"string","enum":["add","update","unchanged"]},"fields":{"type":"array","items":{"type":"string"}}}}}}},
"CreateReleaseRequest": {"type":"object","required":["version","components","note"],"properties":{"version":{"type":"string"},"components":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ComponentVersion"}},"requiredMigrations":{"type":"array","description":"Migration versions this release depends on.","items":{"type":"string"}},"note":{"type":"string","minLength":3,"maxLength":2000,"description":"Internal. Never shown to guests; `guestReleaseNotes` is."},"guestReleaseNotes":{"allOf":[{"$ref":"#/components/schemas/platform-ops::LocalisedText"}],"nullable":true,"description":"**The public, localised \"what's new\" for guests** (decided 29 September, rev 3 GAP-B2), one short text per locale, written for a guest and naming no person. Public once the release reaches the tenant's cell; read by the guest Help screen (WEB-025, WEB-045, GST-040) through `white-label.getTenantAppStatus`. Distinct from the staff-only `TenantAppStatus.recentChanges`, which names the principal behind each change and stays staff only.\n"},"breakingChanges":{"type":"array","items":{"type":"string"}}}},
"Environment": {"type":"object","x-ticvai-persistence":"control.environment","required":["id","kind","name"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/EnvironmentKind"},"name":{"type":"string"},"cellIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requiresApprovalToPromote":{"type":"boolean"},"soakHours":{"type":"integer","description":"How long a release must sit here before it may be promoted. Zero for dev; a real number for staging, or staging is a formality.\n"},"currentReleaseVersion":{"type":"string","nullable":true},"isActive":{"type":"boolean"}}},
"EnvironmentKind": {"type":"string","enum":["dev","staging","production"]},
"Migration": {"type":"object","x-ticvai-persistence":"control.migration","required":["version","module","isReversible","checksum"],"properties":{"version":{"type":"string"},"module":{"type":"string"},"description":{"type":"string"},"isReversible":{"type":"boolean","description":"A rollback section exists and CI has executed it against a restored snapshot. A rollback nobody has run is a comment, not a rollback.\n"},"rollbackTestedAt":{"type":"string","format":"date-time","nullable":true},"checksum":{"type":"string","description":"Compared on apply. A migration edited after it was applied somewhere is a defect the register catches, not a mystery to debug later.\n"},"estimatedLockMs":{"type":"integer","nullable":true},"touchesPartitionedTable":{"type":"boolean"},"appliedCellCount":{"type":"integer"},"pendingCellCount":{"type":"integer"}}},
"MigrationPlan": {"type":"object","x-ticvai-persistence":"control.migration_plan","required":["id","targetVersion","computedAt","cells","allReversible"],"properties":{"id":{"type":"string","format":"uuid"},"targetVersion":{"type":"string"},"computedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","description":"A plan is computed against cell state at a moment. Beyond this it is stale and apply refuses it rather than applying to a different world than it was made for.\n"},"allReversible":{"type":"boolean"},"irreversible":{"type":"array","items":{"type":"string"}},"totalEstimatedLockMs":{"type":"integer"},"cells":{"type":"array","items":{"type":"object","properties":{"cellId":{"type":"string","format":"uuid"},"cellName":{"type":"string"},"tenantSelection":{"type":"string","description":"Which of the cell's tenant databases the plan targets. **A plan that can only say \"this region\" cannot express the rollout ADR-0038 makes normal** — a cell is a region holding many tenants, and a wave may be a subset of one.","enum":["all","named"]},"tenantIds":{"type":"array","description":"Present only where `tenantSelection` is `named`. **Named rather than counted**, for the reason `migration_run_cell` gives about partial failure: a set recorded as a number cannot be checked against what actually ran.","items":{"type":"string","format":"uuid"}},"currentVersion":{"type":"string"},"migrationsToApply":{"type":"array","items":{"type":"string"}},"estimatedLockMs":{"type":"integer"},"warnings":{"type":"array","description":"A long lock on a partitioned table during trading hours is the output this endpoint exists to produce.\n","items":{"type":"string"}}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"MigrationRun": {"type":"object","x-ticvai-persistence":"control.migration_run + control.migration_run_cell + control.migration_run_tenant","description":"One run, its per-region rollup, and its per-tenant outcomes. **The third table exists because ADR-0038 made a cell a region holding many tenants**, and `migration_run_cell`'s own note says it is there so *\"a partial failure is named rather than counted\"* — which is exactly what it stopped doing. A run that fails for twenty of two hundred tenants had one row saying `failed`.\n\nThe rollup stays. *\"How is the UAE doing\"* is a real question and computing it from two hundred rows on every read is not.\n","required":["id","planId","status","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["queued","canary","running","paused","complete","failed","rolledBack"]},"canaryCellId":{"type":"string","format":"uuid","nullable":true,"description":"Which region the canary tenant is in. **The canary itself is a tenant** — a first cell holding two hundred databases is not a cheap failure, and cheap failure is the only thing a canary is for."},"canaryTenantId":{"type":"string","format":"uuid","nullable":true},"tenantsTotal":{"type":"integer"},"tenantsComplete":{"type":"integer"},"tenantsFailed":{"type":"integer"},"cellsTotal":{"type":"integer"},"cellsComplete":{"type":"integer"},"cellsFailed":{"type":"integer"},"startedByPrincipalId":{"type":"string","format":"uuid"},"startedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"cells":{"type":"array","items":{"$ref":"#/components/schemas/MigrationRunCell"}},"tenants":{"type":"array","items":{"$ref":"#/components/schemas/RolloutTenant"}}}},
"MigrationRunCell": {"type":"object","x-ticvai-persistence":"none — rows of control.migration_run_cell, stored through MigrationRun","description":"One cell's rollup within one migration run. **The fields of `RolloutCell` without its `rolloutId`**: a migration run is not a rollout, and its parent key `migration_run_id` comes from `MigrationRun.cells`.\n","required":["cellId","status"],"properties":{"cellId":{"type":"string","format":"uuid"},"cellName":{"type":"string"},"regionName":{"type":"string"},"countryCode":{"type":"string"},"isCanary":{"type":"boolean"},"wave":{"type":"integer"},"status":{"type":"string","enum":["pending","running","complete","failed","skipped","rolledBack"]},"fromVersion":{"type":"string","nullable":true},"toVersion":{"type":"string","nullable":true},"error":{"type":"string","nullable":true},"startedAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE","CORE_AI_PUBLISH","TICKETING_AI_PUBLISH","ACCESS_AI_PUBLISH","FNB_AI_PUBLISH","RETAIL_AI_PUBLISH","INVENTORY_AI_PUBLISH","SEATING_AI_PUBLISH","MEMBERSHIP_AI_PUBLISH","MARKETING_AI_PUBLISH","RESOURCES_AI_PUBLISH","QUEUE_AI_PUBLISH","TRANSPORT_AI_PUBLISH","GAMES_AI_PUBLISH","MAINTENANCE_AI_PUBLISH","ACCREDITATION_AI_PUBLISH","PARTNER_AI_PUBLISH","ANALYTICS_AI_PUBLISH","BIOMETRIC_IMAGE_VIEW","ACCESS_DIRECTION_SET","REPORT_GOVERNANCE_MANAGE"]},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"Release": {"allOf":[{"$ref":"#/components/schemas/CreateReleaseRequest"},{"type":"object","required":["id","status","createdAt"],"x-ticvai-persistence":"control.release + control.release_component","properties":{"id":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/ReleaseStatus"},"createdByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"promotedToStagingAt":{"type":"string","format":"date-time","nullable":true},"promotedToProductionAt":{"type":"string","format":"date-time","nullable":true}}}]},
"ReleaseDetail": {"allOf":[{"$ref":"#/components/schemas/Release"},{"type":"object","x-ticvai-persistence":"none — projection","properties":{"rollouts":{"type":"array","items":{"$ref":"#/components/schemas/Rollout"}},"cellsOnThisVersion":{"type":"integer"},"cellsTotal":{"type":"integer"}}}]},
"ReleaseReadiness": {"type":"object","x-ticvai-persistence":"none — computed","required":["releaseId","canPromote","gates"],"properties":{"releaseId":{"type":"string","format":"uuid"},"canPromote":{"type":"boolean"},"targetEnvironment":{"$ref":"#/components/schemas/EnvironmentKind"},"gates":{"type":"array","items":{"type":"object","required":["gate","passed"],"properties":{"gate":{"type":"string","enum":["priorEnvironmentHealthy","soakPeriodElapsed","migrationsReversible","noOpenIncidents","approvalRecorded","contractsCompatible"]},"passed":{"type":"boolean"},"detail":{"type":"string"}}}}}},
"ReleaseStatus": {"type":"string","enum":["draft","inDev","inStaging","inProduction","superseded","withdrawn"]},
"Rollout": {"type":"object","x-ticvai-persistence":"control.rollout","required":["id","releaseId","environment","status","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"releaseId":{"type":"string","format":"uuid"},"environment":{"$ref":"#/components/schemas/EnvironmentKind"},"status":{"$ref":"#/components/schemas/RolloutStatus"},"cellsTotal":{"type":"integer"},"cellsComplete":{"type":"integer"},"cellsFailed":{"type":"integer"},"startedByPrincipalId":{"type":"string","format":"uuid"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"pausedReason":{"type":"string","nullable":true},"startedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"RolloutTenant": {"type":"object","x-ticvai-persistence":"control.rollout_tenant","description":"What happened to one tenant database during one run. **The same shape as `RolloutCell` one level down**, and it serves the per-tenant rows of both a rollout and a migration run — the arrangement `RolloutCell` had with `rollout_cell` and `migration_run_cell` until `rollout_cell` needed its `rolloutId` parent key and the migration run's cells moved to `MigrationRunCell`.\n\n**`databaseName` is denormalised on purpose.** After a drop the run record still has to say what it touched, and a join to a row that no longer exists says nothing.\n","required":["tenantId","cellId","status"],"properties":{"tenantId":{"type":"string","format":"uuid"},"cellId":{"type":"string","format":"uuid"},"databaseName":{"type":"string"},"isCanary":{"type":"boolean"},"wave":{"type":"integer","description":"A wave is now a set of tenants and may be a subset of one cell."},"status":{"type":"string","enum":["pending","running","complete","failed","skipped","rolledBack"]},"fromVersion":{"type":"string","nullable":true},"toVersion":{"type":"string","nullable":true},"error":{"type":"string","nullable":true},"startedAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n\n**Optional since 2 October 2026: only a till session carries it** (Chinmay, door follow-ups; CHG-CSP-002; breaking change against r1 approved as BC-001 to BC-005 in `docs/active/breaking-changes.yaml`). A browser door (ADM-001, SUP-001, PTR-001) and a staff handheld (EMP-001) sign in with no workstation since CHG-DOOR-001, so they have no board to land on and the field is absent. On a till it is the workstation's effective board: the outlet's board unless the till overrides it (`tenancy.Workstation.saleBoardSource`; CHG-CSP-006). A client reads its landing from this field when present and from its own platform otherwise.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"SupportNotice": {"type":"object","x-ticvai-persistence":"control.support_notice","required":["id","version","supportEndsAt","publishedAt"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string"},"supportEndsAt":{"type":"string","format":"date"},"message":{"type":"object","additionalProperties":{"type":"string"}},"affectedTenantIds":{"type":"array","readOnly":true,"description":"Computed from cell versions, never typed. A notice to the wrong list is worse than none.","items":{"type":"string","format":"uuid"}},"publishedByPrincipalId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"SuspensionMode": {"type":"string","description":"Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n","enum":["readOnly","noNewSales","fullLockout"]},
"Tenant": {"x-ticvai-persistence":"control.tenant","type":"object","required":["id","code","name","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"$ref":"#/components/schemas/TenantStatus"},"suspensionMode":{"$ref":"#/components/schemas/SuspensionMode"},"suspensionReason":{"type":"string","nullable":true},"suspensionEffectiveAt":{"type":"string","format":"date-time","nullable":true,"description":"When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."},"suspensionNoticeMessage":{"$ref":"#/components/schemas/subscription::LocalisedText","description":"The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."},"terminationScheduledAt":{"type":"string","format":"date-time","nullable":true,"description":"When `terminateTenant` started the retention window. Null when no termination is under way."},"terminationRetentionUntil":{"type":"string","format":"date-time","nullable":true,"description":"`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."},"terminationReason":{"type":"string","maxLength":1000,"nullable":true},"terminationRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"planId":{"type":"string","format":"uuid","nullable":true},"planName":{"type":"string","nullable":true},"cellCount":{"type":"integer"},"venueCount":{"type":"integer"},"regionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500,"nullable":true,"description":"Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."},"accountManagerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantStatus": {"type":"string","enum":["onboarding","active","suspended","terminating","terminated"]},
"UpgradeSchedule": {"type":"object","x-ticvai-persistence":"control.upgrade_schedule","required":["tenantId","releaseVersion","scheduledFor"],"properties":{"tenantId":{"type":"string","format":"uuid"},"tenantName":{"type":"string"},"releaseVersion":{"type":"string"},"scheduledFor":{"type":"string","format":"date-time"},"deferredByTenant":{"type":"boolean"},"deferralReason":{"type":"string","nullable":true},"maxDeferralUntil":{"type":"string","format":"date-time","description":"Beyond this the platform proceeds. An indefinitely deferred tenant becomes a version nobody supports.\n"},"notifiedAt":{"type":"string","format":"date-time","nullable":true}}},
"VersionSkewReport": {"type":"object","x-ticvai-persistence":"none — computed from cell state","required":["asAt","cells","hasUnexplainedSkew"],"properties":{"asAt":{"type":"string","format":"date-time"},"hasUnexplainedSkew":{"type":"boolean","description":"Skew during a rollout is expected. Skew outside one is a defect, and separating the two is the entire value of this report.\n**An on-premise cell is a third case: legitimately behind, indefinitely**, because the client has not scheduled the window and TICVAI cannot push. It is not counted here and must not appear as a defect (ADR-0017).\n"},"cells":{"type":"array","items":{"type":"object","properties":{"cellId":{"type":"string","format":"uuid"},"cellName":{"type":"string"},"schemaVersion":{"type":"string"},"applicationVersion":{"type":"string"},"isBehind":{"type":"boolean"},"versionsBehind":{"type":"integer"},"reason":{"type":"string","nullable":true,"enum":["midRollout","rolloutPaused","rolloutFailed","tenantDeferred","onPremiseNotScheduled","unexplained"]}}}}}},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
