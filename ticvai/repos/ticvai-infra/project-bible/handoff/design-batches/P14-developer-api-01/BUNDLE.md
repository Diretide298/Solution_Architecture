# P14-developer-api-01 — P14 · Developer & API

**8 screens · 28 operations · 18 schemas · 3 permissions**

Platform P14 Developer · ships as **ticvai-control** ·
partner audience · web ·
online only

## Who this is for

**partner on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `DEVELOPER_ADMIN, DEVELOPER_MANAGE, DEVELOPER_VIEW`. A control nobody can use must say so,
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
| `DEV-001` | API Reference | B | 1 | 38 | 6 | 11 | 4 | 0 | — | notStarted (generated) |
| `DEV-002` | Register & Organisation | A | 12 | 0 | 5 | 6 | 0 | 0 | — | notStarted (generated) |
| `DEV-003` | Clients & Credentials | A | 15 | 16 | 6 | 17 | 4 | 0 | — | notStarted (generated) |
| `DEV-004` | Sandbox | B | 14 | 31 | 6 | 20 | 3 | 0 | — | notStarted (generated) |
| `DEV-005` | Webhooks | B | 9 | 21 | 6 | 13 | 0 | 0 | — | notStarted (generated) |
| `DEV-006` | Usage & Limits | B | 0 | 13 | 6 | 5 | 1 | 0 | — | notStarted (generated) |
| `DEV-007` | Marketplace Listing | B | 8 | 17 | 6 | 2 | 1 | 0 | — | notStarted (generated) |
| `DEV-008` | Programme Administration | A | 41 | 24 | 6 | 4 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `DEV-001` API Reference

**Read the contract, and call it without leaving the page.**

| | |
|---|---|
| App · platform | TICVAI Control · P14 Developer (web) |
| Module | Developer & API · wave 2 · needs the `developerApi` module |
| Block | Block B · task APP-DEVPORTAL-DEV-001 |
| Who uses it | partner staff holding `DEVELOPER_VIEW` (1 read); in the flows as partner |
| Device and orientation | This is a developer portal on a desktop browser, 1440 wide, with a docs-style left navigation. · LTR · light, dark theme |
| Pattern | listDetail (compact density): `listApiVersions` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/developer/reference` |

**What the spec says about it.** CF-135. **A portal over artefacts that already exist**, which is why this is frontend scope rather than a contract gap — the twelve domain-13 rows left open after the contract landed are all this screen and its siblings. **The API reference.** A developer arrives at the documentation, not at a sign-up form — registration is what they do after reading. **Declared 20 August** — `isEntryPoint` existed in the schema and five platforms used none, so every screen in them read as unreachable.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The API reference grouped by licensable module then contract, with versions, changelog per version and "Try it" against the developer's sandbox. A link to an operation opens at that operation.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search operations | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | field | — | — | `listApiScopes` ?module |

#### Outputs: what the screen shows and produces

**Shown**

**Every API version** (data table, from `listApiVersions`)

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Preview, Current, Deprecated, Sunset | — |
| Released at | 1 Oct 2026, 14:30 | — |
| Deprecated at | 1 Oct 2026, 14:30 | — |
| Sunset at | 1 Oct 2026, 14:30 | — |
| Minimum notice months | 1,234 | The commitment, not the intention. A deprecation policy without a stated minimum is a policy that shortens under pressure. |
| Migration guide URL | text | — |
| Active client count | 1,234 | — |

**Detail panel** (detail panel): Request, response, scopes and error codes. **The error codes are what a developer comes back for**, and they are the section most documentation buries.

**Code block** (code block): A working example per language. **Copy-paste that runs** — an example with a placeholder token teaches nothing about auth, which is where integrations fail.

**Changelog for the selected version** (data table, from `listApiVersions`): **Every operation added, changed, deprecated or removed, with breaking changes marked** (17 September minutes, M17-14; ADR-0026).

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Preview, Current, Deprecated, Sunset | — |
| Released at | 1 Oct 2026, 14:30 | — |
| Deprecated at | 1 Oct 2026, 14:30 | — |
| Sunset at | 1 Oct 2026, 14:30 | — |
| Minimum notice months | 1,234 | The commitment, not the intention. A deprecation policy without a stated minimum is a policy that shortens under pressure. |
| Migration guide URL | text | — |
| Active client count | 1,234 | — |
| Changes | list or chips (count when long) | The developer changelog for this version (17 September minutes, M17-14): every operation added, changed, deprecated or removed, and whether … |
| Operation | text | — |
| Contract | text | — |
| Kind | chip: Added, Changed, Deprecated, Removed | — |
| Breaking | yes / no (icon or chip) | — |
| Summary | text | — |

**The selected API version** (detail panel, from `listApiVersions`)

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Preview, Current, Deprecated, Sunset | — |
| Released at | 1 Oct 2026, 14:30 | — |
| Deprecated at | 1 Oct 2026, 14:30 | — |
| Sunset at | 1 Oct 2026, 14:30 | — |
| Minimum notice months | 1,234 | The commitment, not the intention. A deprecation policy without a stated minimum is a policy that shortens under pressure. |
| Migration guide URL | text | — |
| Active client count | 1,234 | — |

**Tree nav** (tree nav, from `listApiScopes`): **Grouped by licensable module, then contract** (17 September minutes, M17-05 and M17-12): a developer sees which operations each module brings and which scope opens them, so a CRM partner reads the CRM operations and knows it will be granted nothing else.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Scope | text | e.g. `ticketing.read`. |
| Module | text | — |
| Access | chip: Read, Write | — |
| Description | text | — |
| Operations | list or chips (count when long) | — |
| Contract | text | — |
| Operation | text | — |
| Licensed | yes / no (icon or chip) | Whether the caller's tenant licenses the module (`ApiLicence.licensedModules`). |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Try it (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Versions**: Status (current, deprecated with sunset date, retired), minimum notice months and migration guide; breaking changes marked in the changelog. *(source: contracts/satellite/public-api.yaml#listApiVersions; ADR-0026)*

**Data it reads**: `listApiVersions` (onLoad, Which versions exist and which is current); `listApiScopes` (onLoad, The module scope catalogue the reference is grouped by)

**Where the user goes next**

- → `DEV-002` Register & Organisation: *They register their organisation*; calls `listApiVersions`
- → `DEV-004` Sandbox: *Sandbox*
- → `DEV-008` Programme Administration: *Programme Administration*; carries `version`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operation list; the current version renders first. |
| Error (`?state=error`) | Could not load the reference. **Names which contract failed** — 28 files load independently and one missing does not mean the API is down. |
| Empty, first run (`?state=emptyFirstRun`) | **Never empty in practice** — the contracts are the documentation and they ship with the platform. An empty reference means the artefacts did not load, which is an error rather than a first run. |
| Empty, no results (`?state=emptyNoResults`) | No operation matches this search. **Search covers the summary and the description**, not just the operationId, because a developer looking for *"how do I refund"* does not know it is called `createRefund`. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `DEVELOPER_VIEW`, which `listApiVersions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
versions:
- version: v1
  status: current
  releasedAt: 01/12/2026
```

#### Permissions

- `listApiVersions` → `DEVELOPER_VIEW` (read) · public, partner
- `listApiScopes` → `DEVELOPER_VIEW` (read) · public, staff, partner

**A refused user sees:** Shown when the caller lacks `DEVELOPER_VIEW`, which `listApiVersions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.24 | To provide the ability to enable license for the API only for the specific module. Example. APIs are exposed only for ticketing excluding resource management, Seating Module, etc | Developer & API Management | CONTRACTED | `listApiScopes` |
| 13.1.1 | API Documentation Portal - System shall provide interactive API documentation. | Developer & API Management | CONTRACTED | data `ApiVersion` |
| 13.1.2 | API Endpoint Documentation - System shall document all available API endpoints. | Developer & API Management | CONTRACTED | data `ApiVersion` |
| 13.1.3 | Request & Response Examples - System shall provide request and response examples. | Developer & API Management | CONTRACTED | data `ApiVersion` |
| 13.1.4 | API Schema Documentation - System shall publish API schemas. | Developer & API Management | CONTRACTED | data `ApiVersion` |
| 13.1.5 | OpenAPI Support - System shall support OpenAPI/Swagger documentation. | Developer & API Management | CONTRACTED | data `ApiVersion` |
| 13.1.31 | API Versioning - System shall support API version management. | Developer & API Management | CONTRACTED | data `ApiVersion` |
| 13.1.32 | API Deprecation Management - System shall support API deprecation processes. | Developer & API Management | CONTRACTED | data `ApiVersion` |
| 13.1.33 | API Lifecycle Management - System shall support API lifecycle management. | Developer & API Management | CONTRACTED | data `ApiVersion` |
| 13.1.34 | API Change Notifications - System shall notify developers of API changes. | Developer & API Management | CONTRACTED | data `ApiVersion` |
| 13.1.35 | API Release Notes - System shall publish API release notes. | Developer & API Management | CONTRACTED | data `ApiVersion` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The API reference lists every operation added, changed, deprecated or removed per version, with breaking changes marked. *(agreed · MoM 17 Sep 2026, M17-14 · DI-929)*
- API scopes are picked from a list grouped by module ({module}.read / {module}.write), with unlicensed modules shown disabled rather than hidden; the API reference is grouped by licensable module, then contract. *(agreed · MoM 17 Sep 2026, M17-05, M17-12 · DI-926)*
- The developer portal includes a product/data schema reference (field requirements, min/max lengths), an interactive "try it" API tester showing live request/response, an SDK library with sample code in JavaScript, Python, Java and .NET, a Postman collection and full documentation. *(client request · MoM 17 Sep 2026, 4.9 Developer Portal & API Documentation · DI-913)*
- API documentation must be organised by module (which APIs belong to which module), so a client can see exactly which module's APIs to request, e.g. only CRM-related APIs for a CRM integration. *(agreed · MoM 17 Sep 2026, 4.13 Sandbox Environment & Partner Ecosystem Analytics · DI-912)*

Also apply: 3 for all of P14, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P14 Developer.dc.html#dev-001` · status **notStarted** · provenance generated
- Flow F27 *A developer integrates*, step 1: The developer reads the reference and tries an operation. → **Try-it runs against the sandbox, never production**, and the button says so. A try-it that quietly hits production is how somebody refunds a real order while reading the docs.
- ADR-0026 *Public API versioning, scopes and deprecation* (`docs/adr/0026-public-api-versioning.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (38 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#DEV-001?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Try it.
- [ ] Every transition is wired: `DEV-002`, `DEV-004`, `DEV-008`.
- [ ] Every gated control is gated: `DEVELOPER_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `DEV-002` Register & Organisation

**Sign up as an organisation, and manage who at it may do what.**

| | |
|---|---|
| App · platform | TICVAI Control · P14 Developer (web) |
| Module | Developer & API · wave 1 · needs the `developerApi` module |
| Block | Block A · task APP-SETUP-DEV-002 |
| Who uses it | partner staff holding `DEVELOPER_MANAGE`, `DEVELOPER_VIEW` (1 configure, 1 read); in the flows as partner |
| Device and orientation | This is a developer portal on a desktop browser, 1440 wide, with a docs-style left navigation. · LTR · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`registerDeveloper`, `setDeveloperMembers`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `developerId` (deepLink) · cold entry: **A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. … |
| Route | `/developer/organisation` |

**What the spec says about it.** 13.1.6 to 13.1.10. **The organisation administers its own people** — Softlabs maintaining every integrator's staff list is Softlabs doing their HR. **Form rebuilt 2 October 2026 (CHG-SOT-014, design-notes corrections DEV-002).** Registration asks name, email, website and country; the eight raw schema names (id, status, verifiedAt, partnerId among them) are gone from the form. Never `id` or `status`: the id is a client UUIDv7 generated silently and the status is the server's.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** An integrator registers their organisation (not a personal account) and its owner manages who in it may do what: owner, admin, developer, read-only. Registration is pending until TICVAI verifies it; nothing is provisioned before that, because an unverified account with live credentials is an open door.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- registerDeveloper requires DEVELOPER_VIEW with audience public. (CHG-SOT-016)

**Fixed on main** (the package already carries these; draw what it says): Text fields for id, status, verifiedAt and partnerId. (CHG-SOT-014); 8 text fields are raw schema property names, not inputs: id, organisationName, contactEmail, websiteUrl, countryCode, partnerId, status … (CHG-SOT-014).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which door does a developer sign in through? P14 belongs to TICVAI Control, whose doors are ADM-001 (platform staff) and PTR-001 (partners).** → Drawn default accepted: Developers sign in through the partner door with a developer account; draw a "Sign in to the Developer Portal" variant of PTR-001. *(decided by Chinmay, 2026-10-02; DEC-096 / CHG-NOTE-005)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Organisation name | text field | optional | — | — | — | — | `DeveloperAccount.organisationName` |
| Contact email | email field | optional | — | — | name@example.ae | Where the verification email goes. | `DeveloperAccount.contactEmail` |
| Website | text field | optional | — | — | — | — | `DeveloperAccount.websiteUrl` |
| Country | text field | optional | — | — | — | — | `DeveloperAccount.countryCode` |

**Form: Save developer members** (modal, opened by *Save developer members*; *Save developer members* calls `setDeveloperMembers`, *Cancel* sends nothing)

**Collects what `setDeveloperMembers` sends before it is called.** Required: `members`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Members `members` | repeatable rows | required | — | — | — | — | `setDeveloperMembers` body |
| Email `members[].email` | email field | optional | — | — | name@example.ae | — | `setDeveloperMembers` body |
| Role `members[].role` | radio group | optional | — | Owner · Admin · Developer · Read only | — | — | `setDeveloperMembers` body |

**Sent by *Register developer*** (`registerDeveloper`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Organisation name `organisationName` | text field | required | — | — | — | — | `registerDeveloper` body |
| Contact email `contactEmail` | email field | required | — | — | name@example.ae | — | `registerDeveloper` body |
| Website URL `websiteUrl` | text field | optional | — | — | — | — | `registerDeveloper` body |
| Country code `countryCode` | text field | optional | — | — | — | — | `registerDeveloper` body |
| Partner `partnerId` | picker: choose a partner | optional | — | — | shows names, sends the id | Where this developer is also a commercial partner. The link exists and the two are not the same record, which is what CF-135a was about. | `registerDeveloper` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Organisation**: Organisation name, contact email (verified by email), website, country; the person registering becomes owner. *(source: contracts/satellite/public-api.yaml#registerDeveloper; F27 step 2)*
- **Members**: Invite by email with a role (owner, admin, developer, read-only); at least one owner always remains. *(source: contracts/satellite/public-api.yaml#setDeveloperMembers)*

#### Outputs: what the screen shows and produces

**Shown**

**Registration status** (banner): Shown after registering: "Pending: check your email" until the email is verified, then "Verified on <date>" (`DeveloperAccount.status`, `verifiedAt`). The partner link (`partnerId`) is set by TICVAI, never typed.

**Data table** (data table): Role per member — owner, admin, developer, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Invite (primary button) | navigation or local | — | — | — | — |
| Register developer (primary button) | `registerDeveloper` POST `/developers` | DeveloperAccount | DeveloperAccount | — | — |
| Save developer members (secondary button) | `setDeveloperMembers` PUT `/developers/{developerId}/members` | inline | inline | — | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Verification status**: Pending, verified (with date), suspended or closed, and what pending means ("we review within 2 working days; you can explore the docs and sandbox meanwhile"). *(source: contracts/satellite/public-api.yaml#/components/schemas/DeveloperAccount)*

**Where the user goes next**

- → `DEV-003` Clients & Credentials: *They create a sandbox client and take the secret*; calls `registerDeveloper`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The organisation and its members. |
| Error (`?state=error`) | Could not load. Your credentials are unaffected. |
| Empty, first run (`?state=emptyFirstRun`) | **You are the first member and you are the owner.** An integration outlives the engineer who built it, so this is an organisation rather than a personal account — and the invite action is the point of the state. |
| Permission denied (`?state=emptyNoAccess`) | **You are a member and not an owner.** Stated plainly rather than shown as an empty list, because a developer who sees no colleagues assumes the page is broken. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `DEV-003`: Clients are created after verification.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
organisation:
  name: Gulf Kiosk Systems FZ-LLC
  contactEmail: dev@gulfkiosk.ae
  country: AE
  status: pending
members:
- name: Nadia Farouk
  email: nadia@gulfkiosk.ae
  role: owner
- name: Karim Youssef
  email: karim@gulfkiosk.ae
  role: developer
```

#### Permissions

- `registerDeveloper` → `DEVELOPER_VIEW` (read) · public
- `setDeveloperMembers` → `DEVELOPER_MANAGE` (configure) · partner

**A refused user sees:** **You are a member and not an owner.** Stated plainly rather than shown as an empty list, because a developer who sees no colleagues assumes the page is broken.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.1.10 | Developer Role Management - System shall support role-based permissions for developers. | Developer & API Management | CONTRACTED | `setDeveloperMembers` |
| 13.1.6 | Developer Registration - System shall support developer account registration. | Developer & API Management | CONTRACTED | data `DeveloperAccount` |
| 13.1.7 | Developer Authentication - System shall support secure developer authentication. | Developer & API Management | CONTRACTED | data `DeveloperAccount` |
| 13.1.8 | Developer Profiles - System shall maintain developer profiles. | Developer & API Management | CONTRACTED | data `DeveloperAccount` |
| 13.1.9 | Organization Accounts - System shall support organization-based developer accounts. | Developer & API Management | CONTRACTED | data `DeveloperAccount` |
| 13.1.47 | Partner Portal - System shall support partner developer programs. | Developer & API Management | CONTRACTED | data `DeveloperAccount` |

#### Client meeting inputs

None names this screen.

Also apply: 3 for all of P14, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P14 Developer.dc.html#dev-002` · status **notStarted** · provenance generated
- Flow F27 *A developer integrates*, step 2: They register their organisation. → Pending verification. **Nothing is provisioned yet** — an unverified account with live credentials is an open door.
- Flow F27 branch at step 2 (abandonsFlow): when Verification fails., Rejected with a reason they can act on. **Nothing was provisioned, so nothing needs cleaning up** — which is the whole point of verifying before provisioning rather than alongside it.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#DEV-002?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Invite, Register developer, Save developer members.
- [ ] Every transition is wired: `DEV-003`.
- [ ] Every gated control is gated: `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `DEV-003` Clients & Credentials

**Create a client, choose its scopes, and rotate its secret without an outage.**

| | |
|---|---|
| App · platform | TICVAI Control · P14 Developer (web) |
| Module | Developer & API · wave 1 · needs the `developerApi` module |
| Block | Block A · task APP-SETUP-DEV-003 |
| Who uses it | partner staff holding `DEVELOPER_MANAGE`, `DEVELOPER_VIEW` (1 configure, 1 read); in the flows as partner |
| Device and orientation | This is a developer portal on a desktop browser, 1440 wide, with a docs-style left navigation. · LTR · light, dark theme |
| Pattern | listDetail (compact density): `listApiClients` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `clientId` (deepLink) · cold entry: **A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. … |
| Route | `/developer/clients` |

**What the spec says about it.** CF-135a. **The one credential model** — 2.7.52, 7.1.25 and 7.1.30 each asserted their own. **Rotation carries an overlap window and revocation does not**: one is hygiene, the other is what you reach for when a secret has leaked, and a grace period defeats it.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A developer creates sandbox clients, picks scopes by module, takes the secret once, rotates with an overlap window or revokes at once, and requests production access for a certified integration. Production clients are never created here; TICVAI issues them on an approved request.

**Fixed on main** (the package already carries these; draw what it says): formCreateApiClient requires id, status and environment and offers lastUsedAt. (CHG-SOT-014); Tables show every schema field, plumbing included: 'Every API client' drop id, developerId, clientId, allowedTenantIds. (CHG-SOT-014).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scopes, by module | multi select | — | — | — | — | **A scope picker grouped by module** (M17-05): `{module}.read` and `{module}.write`, with unlicensed modules shown and disabled rather than hidden. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | field | — | — | `listApiScopes` ?module |

**Form: Create API client** (modal, opened by *Create API client*; *Create API client* calls `createApiClient`, *Cancel* sends nothing)

**Collects what `createApiClient` sends before it is called.** The person enters `name` and picks `scopes` (by module); `ipAllowList` is optional. **The environment is sandbox here**: a production client is issued by TICVAI after certification (DI-927, F36 step 5), so the form offers no environment choice. `developerId` comes from the session. Never `id` or `status`: the id is a client UUIDv7 generated silently and the status is the server's. `lastUsedAt` is the server's and never asked. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Developer `developerId` | picker: choose a developer | required | — | — | shows names, sends the id | — | `createApiClient` body |
| Name `name` | text field | required | — | — | — | — | `createApiClient` body |
| Environment `environment` | segmented control | required | — | Sandbox · Production | — | Bound to one, stated on the object rather than by naming convention. A key that works in both is a key somebody will use in the wrong one. | `createApiClient` body |
| Scopes `scopes` | list of values (chips) | required | — | — | — | Resolved against the tenant's licence at token issue (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call … | `createApiClient` body |
| Certification listing `certificationListingId` | picker: choose a certification listing | optional | — | — | shows names, sends the id | For a production client, the certified integration it was issued against. | `createApiClient` body |
| Credential ttl days `credentialTtlDays` | number field (days) | optional | — | min 1; max 730 | — | Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry). | `createApiClient` body |
| Allowed tenants `allowedTenantIds` | multi-picker: choose allowed tenants | optional | — | — | — | 13.1.46. Which tenants this client may act for. | `createApiClient` body |
| Ip allow list `ipAllowList` | list of values (chips) | optional | — | — | — | 13.1.38. Required on a production client (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the internet); optional in the sandbox. | `createApiClient` body |

Errors to draw in the form: 409 A `production` client without a current certification, or asked for by a developer rather than issued by TICVAI (`certification-required`, M17-06).; 422 A `production` client with an empty `ipAllowList` (`ip-allow-list-required`, M17-07), or a scope that is not in the scope catalogue (`unknown-scope`, M17-05).

**Form: Rotate API credential** (modal, opened by *Rotate API credential*; *Rotate API credential* calls `rotateApiCredential`, *Cancel* sends nothing)

**Collects what `rotateApiCredential` sends before it is called.** Nothing in the body is required. Optional: `overlapHours`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Overlap hours `overlapHours` | number field (hours) | optional | 72 | — | — | — | `rotateApiCredential` body |

**Form: Request production access** (modal, opened by *Request production access*; *Request production access* calls `requestProductionAccess`, *Cancel* sends nothing)

**Collects what `requestProductionAccess` sends before it is called.** Required: `listingId` (a certified integration), `scopes`, `allowedTenantIds`, `ipAllowList` (at least one address, M17-07). Optional: `note`. The form says that a new production key is issued and the sandbox key stays a sandbox key.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Listing `listingId` | picker: choose a listing | required | — | — | shows names, sends the id | — | `requestProductionAccess` body |
| Scopes `scopes` | list of values (chips) | required | — | at least 1 | — | — | `requestProductionAccess` body |
| Allowed tenants `allowedTenantIds` | multi-picker: choose allowed tenants | required | — | at least 1 | — | — | `requestProductionAccess` body |
| Ip allow list `ipAllowList` | list of values (chips) | required | — | at least 1 | — | — | `requestProductionAccess` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `requestProductionAccess` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The listing is not certified, or its certification has lapsed (`certification-required`); or the client is not a sandbox client, or a request for it is already …; 422 An empty `ipAllowList` (`ip-allow-list-required`) or an unknown scope (`unknown-scope`).

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Create client**: Name and scopes only; environment fixed to sandbox and shown as such; the client id and status are the server's. *(source: contracts/satellite/public-api.yaml#createApiClient; DI-927)*
- **Scopes**: Grouped by module, {module}.read and {module}.write; unlicensed modules shown disabled with "not licensed by any tenant you work for", not hidden. *(source: DI-926; contracts/satellite/public-api.yaml#listApiScopes)*
- **Rotate**: Overlap hours for the old secret (hygiene); Revoke has no overlap (a leak). *(source: contracts/satellite/public-api.yaml#rotateApiCredential)*
- **Request production access**: The certified listing, tenants, scopes and at least one IP allow-list address; the form says a new production key will be issued and the sandbox key stays sandbox. *(source: DI-927; DI-928; F36 step 4)*

#### Outputs: what the screen shows and produces

**Shown**

**Every API client** (data table, from `listApiClients`): Name, environment, scopes, IP allow-list, status and last used. The client id and the developer are in the detail panel, with a copy action; allowed tenants are shown by venue name there (design-notes correction DEV-003).

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Environment | chip: Sandbox, Production | Bound to one, stated on the object rather than by naming convention. A key that works in both is a key somebody will use in the wrong one. |
| Scopes | list or chips (count when long) | Resolved against the tenant's licence at token issue (13.3.24). A scope granted here and not licensed there produces no token — and the … |
| Ip allow list | list or chips (count when long) | 13.1.38. Required on a production client (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the … |
| Status | chip: Active, Suspended, Revoked | — |
| Last used at | 1 Oct 2026, 14:30 | A credential unused for a year is a credential nobody will notice being stolen. |

**Data table** (data table): Environment is a column and not a badge. **A sandbox key and a production key that look alike is how somebody uses the wrong one**, and the difference must survive a glance.

**Banner** (banner): **The secret is shown once.** The banner says so before it is generated, not after — a system that can show you a secret later is a system that stores one. **A production client is never created here** (M17-06): it is issued by TICVAI on an approved production access request, and its first secret is taken once with Rotate.

**The selected API client** (detail panel, from `listApiClients`)

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create client (primary button) | navigation or local | — | — | — | — |
| Create API client (primary button) | `createApiClient` POST `/api-clients` | ApiClient | inline | 409 A `production` client without a current certification, or asked for by a developer rather than issued by TICVAI (`certification-required`, M17-06).; 422 A `production` client with an empty `ipAllowList` … | opens modal first |
| Rotate API credential (secondary button) | `rotateApiCredential` POST `/api-clients/{clientId}/credentials` | inline | inline | — | opens modal first |
| Revoke API credential (destructive button) | `revokeApiCredential` DELETE `/api-clients/{clientId}/credentials` | — | — | — | — |
| Request production access (secondary button) | `requestProductionAccess` POST `/api-clients/{clientId}/production-access` | inline | ProductionAccessRequest | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The listing is not certified, or its certification has lapsed (`certification-required`); or the client is not … | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Environment**: A column in words (Sandbox / Production) with distinct styling; a sandbox and a production key must not look alike. *(source: screens/P14-developer-portal.yaml#DEV-003)*
- **Secret**: Shown once at creation or rotation, with copy; the banner says so before it is generated. *(source: F27 step 3)*
- **Production access status**: Sandbox only, requested (pending), approved, or rejected with the reason. *(source: DI-927)*

**Data it reads**: `listApiClients` (onLoad, Clients with their environment and scopes); `listApiScopes` (onLoad, Scopes to choose from, by module)

**Where the user goes next**

- → `DEV-005` Webhooks: *Webhooks*
- → `DEV-004` Sandbox: *They provision a sandbox and build against it*; carries `clientId`; calls `createApiClient`
- → `DEV-008` Programme Administration: *TICVAI decides the request*; carries `listingId`, `requestId`; calls `requestProductionAccess`

**What opens over it**

- confirmDialog *Revoke API credential*: **Names what `revokeApiCredential` changes and what it leaves alone**, in the consequence rather than the verb. A clients credentials this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Clients, sandbox first. |
| Error (`?state=error`) | Could not load clients. Existing credentials keep working. |
| Empty, first run (`?state=emptyFirstRun`) | **No clients yet. Create a sandbox one** — the action says sandbox because a first client should never be a production client, and defaulting the other way is how a first API call hits a live venue. |
| Empty, no results (`?state=emptyNoResults`) | No client matches this environment or scope. |
| Permission denied (`?state=emptyNoAccess`) | You are a read-only member. Credentials are hidden, not absent. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A `production` client without a current certification, or asked for by a developer rather than issued by TICVAI (`certification-required`, M17-06).; 409 The listing is not certified, or its certification has lapsed (`certification-required`); or the client is not a sandbox client, or a request for it is already …; 422 A `production` client with an empty `ipAllowList` … |

#### Edge cases to draw

- **Can read but not change (holds DEVELOPER_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: DEVELOPER_MANAGE for Create API client, Rotate API credential, Revoke API credential. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/public-api.yaml#createApiClient)*
- **createApiClient answers 409**: Show it as something the person can act on, not a failure: A `production` client without a current certification, or asked for by a developer rather than issued by TICVAI (`certification-required`, M17-06). Use `requestProductionAccess`. *(source: contracts/satellite/public-api.yaml#createApiClient)*
- **createApiClient answers 422**: Show it as something the person can act on, not a failure: A `production` client with an empty `ipAllowList` (`ip-allow-list-required`, M17-07), or a scope that is not in the scope catalogue (`unknown-scope`, M17-05). *(source: contracts/satellite/public-api.yaml#createApiClient)*
- **requestProductionAccess answers 409**: Show it as something the person can act on, not a failure: The listing is not certified, or its certification has lapsed (`certification-required`); or the client is not a sandbox client, or a request for it is already pending (`production-access-pending`). *(source: contracts/satellite/public-api.yaml#requestProductionAccess)*
- **requestProductionAccess answers 422**: Show it as something the person can act on, not a failure: An empty `ipAllowList` (`ip-allow-list-required`) or an unknown scope (`unknown-scope`). *(source: contracts/satellite/public-api.yaml#requestProductionAccess)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
clients:
- name: Kiosk connector (test)
  environment: Sandbox
  scopes:
  - ticketing.read
  - orders.write
  status: active
  lastUsed: 01/10/2026 08:40
  expires: 30/12/2026
- name: Kiosk connector
  environment: Production
  issuedBy: TICVAI
  tenants:
  - Marina Leisure Group
  ipAllowList:
  - 185.53.2.10
  expires: 30/09/2027
```

#### Permissions

- `listApiClients` → `DEVELOPER_VIEW` (read) · staff, partner
- `createApiClient` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `rotateApiCredential` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `revokeApiCredential` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `listApiScopes` → `DEVELOPER_VIEW` (read) · public, staff, partner
- `requestProductionAccess` → `DEVELOPER_MANAGE` (configure) · partner

**A refused user sees:** You are a read-only member. Credentials are hidden, not absent.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.24 | To provide the ability to enable license for the API only for the specific module. Example. APIs are exposed only for ticketing excluding resource management, Seating Module, etc | Developer & API Management | CONTRACTED | `listApiScopes` |
| 13.1.49 | API Certification Program - System shall support certification of integrations. | Developer & API Management | CONTRACTED | `requestProductionAccess` |
| 2.7.52 | System shall allow approved B2B partners to request, generate, manage, rotate, and revoke API credentials. Access shall be restricted by partner permissions, products, quotas, rate limits, IP … | Ticketing Sales | CONTRACTED | data `ApiClient` |
| 7.1.25 | The system shall support dedicated API users, integration users, service accounts, API keys, credential rotation, expiry controls, IP restrictions, and audit logging. | F&B POS | CONTRACTED | data `ApiClient` |
| 13.1.11 | API Key Management - System shall support API key generation and management. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.13 | OAuth Support - System shall support OAuth authentication. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.14 | Token Management - System shall support access token management. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.15 | Credential Revocation - System shall support credential revocation. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.21 | API Explorer - System shall provide interactive API testing tools. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.22 | SDK Availability - System shall provide SDKs for supported platforms. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.23 | Code Samples - System shall provide implementation examples. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.24 | Postman Collections - System shall provide Postman collections. | Developer & API Management | CONTRACTED | data `ApiClient` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Abnormal API volume is flagged, not only throttled (calls above the client's baseline, refusals outside the allow-list, calls to unused operations); a production access request requires at least one IP allow-list address. *(agreed · MoM 17 Sep 2026, M17-07 · DI-928)*
- Production access status is shown: sandbox only, requested (pending), approved, or rejected with the reason. Production keys only after certification; the request form says a new production key is issued and the sandbox key stays sandbox. *(agreed · MoM 17 Sep 2026, M17-06 · DI-927)*
- API scopes are picked from a list grouped by module ({module}.read / {module}.write), with unlicensed modules shown disabled rather than hidden; the API reference is grouped by licensable module, then contract. *(agreed · MoM 17 Sep 2026, M17-05, M17-12 · DI-926)*
- API keys can be partner-generated or TICVAI-generated with configurable expiry; sandbox keys are shown and kept separate from production keys, and production access is granted only after certification. *(agreed · MoM 17 Sep 2026, 4.10 Developer Accounts, API Credentials & Sandbox/Production Separation · DI-914)*

Also apply: 3 for all of P14, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P14 Developer.dc.html#dev-003` · status **notStarted** · provenance generated
- Flow F27 *A developer integrates*, step 3: They create a sandbox client and take the secret. → **`issueApiToken` is not on this screen and should not be** — a token exchange is a call their code makes, not a button somebody presses. The flow named it here and the checker was right to refuse. …
- Flow F36 *A developer goes from sandbox to production*, step 4: They request production access for the certified integration. → **The request names the certified listing, the tenants, the scopes and an IP allow-list** (at least one address, M17-07). The sandbox client stays a sandbox client.
- Flow F36 *A developer goes from sandbox to production*, step 6: They take the production secret once, with Rotate. → **The secret is shown once and never again.** From here their production calls are watched by the anomaly rules (M17-07) and limited by the quota.
- Flow F27 branch at step 3 (requiresStaff): when They request a scope their target tenant has not licensed., **No token is issued, and the refusal happens at issue rather than at call time.** An integrator whose tenant has not licensed the F&B API finds out once, in testing, rather than at 3am against a 403 …
- Flow F36 branch at step 4 (recoverable): when The integration named is not certified, or its certification has lapsed., **Refused 409 `certification-required`.** There is no route to production that skips certification, including creating a production client directly (createApiClient refuses it the same way unless …
- Flow F36 branch at step 4 (recoverable): when The request has no IP allow-list, or asks for a scope that does not exist., Refused 422 (`ip-allow-list-required`, `unknown-scope`) naming the field, before anyone at TICVAI has to look at it. No scope opens a catalogue write (M17-04).
- Flow F36 branch at step 6 (requiresStaff): when The certification lapses or is withdrawn while the production client is live., **The production clients bound to it are suspended**, and the developer and the tenants they serve are told; recertifying restores them. A lapsed certification never leaves a live key running …

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#DEV-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create client, Create API client, Rotate API credential, Revoke API credential, Request production access.
- [ ] Every transition is wired: `DEV-005`, `DEV-004`, `DEV-008`.
- [ ] Every gated control is gated: `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `DEV-004` Sandbox

**Test against synthetic data, and reset to a known state.**

| | |
|---|---|
| App · platform | TICVAI Control · P14 Developer (web) |
| Module | Developer & API · wave 2 · needs the `developerApi` module |
| Block | Block B · task APP-DEVPORTAL-DEV-004 |
| Who uses it | partner staff holding `DEVELOPER_MANAGE`, `DEVELOPER_VIEW` (1 configure, 1 read); in the flows as partner |
| Device and orientation | This is a developer portal on a desktop browser, 1440 wide, with a docs-style left navigation. · LTR · light, dark theme |
| Pattern | listDetail (compact density): `listSandboxes` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `sandboxId` (deepLink), `clientId` (navigation) · cold entry: **A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. … |
| Route | `/developer/sandbox` |

**What the spec says about it.** Decisions D2 and D3. **One shared sandbox, synthetic data only** — which removes the PDPL and DESC exposure entirely. Tenant-specific validation runs on per-customer staging.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A developer's sandboxes with synthetic data: create, reset to a known state, see expiry. Sandboxes never contain production data. Production access is requested from the client, not promoted from a sandbox.

**Fixed on main** (the package already carries these; draw what it says): "Promote to production" on the sandbox. (CHG-SOT-014); Tables show every schema field, plumbing included: 'Every sandbox' drop id, developerId. (CHG-SOT-014).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Pending · Approved · Rejected · Withdrawn | `listProductionAccessRequests` ?status |

**Form: Create sandbox** (modal, opened by *Create sandbox*; *Create sandbox* calls `createSandbox`, *Cancel* sends nothing)

**Collects what `createSandbox` sends before it is called.** Required: `name`, `dataProfile`. Optional: `expiresAfterDays`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | — | — | — | `createSandbox` body |
| Data profile `dataProfile` | group | required | — | — | — | 13.2.5 and 13.2.13. What the synthetic dataset contains, so a developer can test against a shape that resembles a real venue without any of it being real. | `createSandbox` body |
| Venue kind `dataProfile.venueKind` | select | optional | — | Theme park · Water park · Museum · Theatre · Stadium · Arena · Mixed | — | — | `createSandbox` body |
| Product count `dataProfile.productCount` | number field | optional | 200 | — | — | — | `createSandbox` body |
| Guest count `dataProfile.guestCount` | number field | optional | 5000 | — | — | — | `createSandbox` body |
| Seat map included `dataProfile.seatMapIncluded` | toggle | optional | on | — | — | — | `createSandbox` body |
| Historical months `dataProfile.historicalMonths` | number field | optional | 12 | — | — | Backdated synthetic orders, because an integration reading a reporting API against an empty venue tests nothing. | `createSandbox` body |
| Locale `dataProfile.locale` | text field | optional | en-AE | — | — | — | `createSandbox` body |
| Expires after days `expiresAfterDays` | number field (days) | optional | 90 | — | — | — | `createSandbox` body |

**Form: Request production access** (modal, opened by *Request production access*; *Promote to production* calls `requestProductionAccess`, *Cancel* sends nothing)

**Collects what `requestProductionAccess` sends before it is called.** Required: `listingId`, `scopes`, `allowedTenantIds`, `ipAllowList`. Optional: `note`.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Listing `listingId` | picker: choose a listing | required | — | — | shows names, sends the id | — | `requestProductionAccess` body |
| Scopes `scopes` | list of values (chips) | required | — | at least 1 | — | — | `requestProductionAccess` body |
| Allowed tenants `allowedTenantIds` | multi-picker: choose allowed tenants | required | — | at least 1 | — | — | `requestProductionAccess` body |
| Ip allow list `ipAllowList` | list of values (chips) | required | — | at least 1 | — | — | `requestProductionAccess` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `requestProductionAccess` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The listing is not certified, or its certification has lapsed (`certification-required`); or the client is not a sandbox client, or a request for it is already …; 422 An empty `ipAllowList` (`ip-allow-list-required`) or an unknown scope (`unknown-scope`).

#### Outputs: what the screen shows and produces

**Shown**

**Every sandbox** (data table, from `listSandboxes`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Status | chip: Provisioning, Active, Resetting, Expired, Deleted | — |
| Data profile | grouped details | 13.2.5 and 13.2.13. What the synthetic dataset contains, so a developer can test against a shape that resembles a real venue without any of … |
| Contains production data | yes / no (icon or chip) | Always false, and stated rather than assumed (D2). No cloning, no masking. |
| Expires at | 1 Oct 2026, 14:30 | — |
| Last reset at | 1 Oct 2026, 14:30 | — |

**Card list** (card list): Venue kind, record counts, expiry.

**Banner** (banner): **Expiry, counted in days.** A sandbox that vanishes with no warning is a developer who thinks the platform broke.

**The selected sandbox** (detail panel, from `listSandboxes`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Developer | the name it points at, never the id | — |
| Status | chip: Provisioning, Active, Resetting, Expired, Deleted | — |
| Data profile | grouped details | 13.2.5 and 13.2.13. What the synthetic dataset contains, so a developer can test against a shape that resembles a real venue without any of … |
| Contains production data | yes / no (icon or chip) | Always false, and stated rather than assumed (D2). No cloning, no masking. |
| Expires at | 1 Oct 2026, 14:30 | — |
| Last reset at | 1 Oct 2026, 14:30 | — |

**Path to production** (detail panel, from `listProductionAccessRequests`): **Sandbox, certification, production** (17 September minutes, M17-06): where this developer stands, the certification and the production access request with its decision.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Developer | the name it points at, never the id | — |
| Sandbox client | the name it points at, never the id | — |
| Listing | the name it points at, never the id | — |
| Scopes | list or chips (count when long) | — |
| Allowed tenants | list or chips (count when long) | — |
| Ip allow list | list or chips (count when long) | — |
| Note | text | — |
| Status | chip: Pending, Approved, Rejected, Withdrawn | — |
| Decided by principal | the name it points at, never the id | — |
| Decided at | 1 Oct 2026, 14:30 | — |
| Reason | text | — |
| Production client | the name it points at, never the id | — |
| Requested at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Provision sandbox (primary button) | navigation or local | — | — | — | — |
| Reset (secondary button) | navigation or local | — | — | — | — |
| Create sandbox (primary button) | `createSandbox` POST `/sandboxes` | inline | Sandbox | — | opens modal first |
| Reset sandbox (destructive button) | `resetSandbox` POST `/sandboxes/{sandboxId}/reset` | — | Sandbox | — | — |
| Request production access (secondary button) | `requestProductionAccess` POST `/api-clients/{clientId}/production-access` | inline | ProductionAccessRequest | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The listing is not certified, or its certification has lapsed (`certification-required`); or the client is not … | opens modal first |

**Data it reads**: `listSandboxes` (onLoad, Sandboxes and their expiry); `listProductionAccessRequests` (onLoad, The path to production and its state)

**Where the user goes next**

- → `DEV-005` Webhooks: *They subscribe to the events they need and watch the deliveries*
- → `DEV-007` Marketplace Listing: *They submit the integration for certification*; calls `createSandbox`

**What opens over it**

- confirmDialog *Reset sandbox*: **Names what `resetSandbox` changes and what it leaves alone**, in the consequence rather than the verb. A sandbox this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Sandboxes with their data profile. |
| Error (`?state=error`) | Could not load. A running sandbox is unaffected. |
| Empty, first run (`?state=emptyFirstRun`) | **No sandbox yet. Provisioning takes a few minutes and the data is generated, not copied** — no production data is ever cloned or masked into it, which is the decision the whole environment rests on. |
| Empty, no results (`?state=emptyNoResults`) | No sandbox matches. |
| Permission denied (`?state=emptyNoAccess`) | Without `DEVELOPER_VIEW`, which `listSandboxes` requires, the screen does not load and this state names that permission. You do not have `DEVELOPER_MANAGE`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The listing is not certified, or its certification has lapsed (`certification-required`); or the client is not a sandbox client, or a request for it is already …; 422 An empty `ipAllowList` (`ip-allow-list-required`) or an unknown scope (`unknown-scope`). |

#### Edge cases to draw

- **Can read but not change (holds DEVELOPER_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: DEVELOPER_MANAGE for Create sandbox, Reset sandbox, Promote to production. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/public-api.yaml#createSandbox)*
- **requestProductionAccess answers 409**: Show it as something the person can act on, not a failure: The listing is not certified, or its certification has lapsed (`certification-required`); or the client is not a sandbox client, or a request for it is already pending (`production-access-pending`). *(source: contracts/satellite/public-api.yaml#requestProductionAccess)*
- **requestProductionAccess answers 422**: Show it as something the person can act on, not a failure: An empty `ipAllowList` (`ip-allow-list-required`) or an unknown scope (`unknown-scope`). *(source: contracts/satellite/public-api.yaml#requestProductionAccess)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every sandbox:
- name: Kiosk connector (sandbox)
  status: active
  expiresAt: 31/12/2026 23:59
  lastResetAt: 01/10/2026 09:14
- name: OTA availability feed
  status: pending
  expiresAt: 15/10/2026 00:00
  lastResetAt: 30/09/2026 18:02
- name: Wallet sync
  status: suspended
  expiresAt: 01/11/2026 06:00
  lastResetAt: 28/09/2026 11:45
```

#### Permissions

- `listSandboxes` → `DEVELOPER_VIEW` (read) · staff, partner
- `createSandbox` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `resetSandbox` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `listProductionAccessRequests` → `DEVELOPER_VIEW` (read) · staff, partner
- `requestProductionAccess` → `DEVELOPER_MANAGE` (configure) · partner

**A refused user sees:** Without `DEVELOPER_VIEW`, which `listSandboxes` requires, the screen does not load and this state names that permission. You do not have `DEVELOPER_MANAGE`.

#### Requirements it meets

20 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.2.6 | Integration Testing - Developers shall validate integrations without affecting production. | Developer & API Management | CONTRACTED | `createSandbox` |
| 13.2.7 | API Testing - System shall support API testing. | Developer & API Management | CONTRACTED | `createSandbox` |
| 13.2.8 | Webhook Testing - System shall support webhook testing. | Developer & API Management | CONTRACTED | `createSandbox` |
| 13.2.9 | Performance Testing - System shall support performance testing. | Developer & API Management | CONTRACTED | `createSandbox` |
| 13.2.10 | Regression Testing - System shall support regression testing. | Developer & API Management | CONTRACTED | `createSandbox` |
| 13.2.19 | Sandbox API Access - System shall expose APIs within sandbox environments. | Developer & API Management | CONTRACTED | `createSandbox` |
| 13.2.3 | Environment Reset - System shall support sandbox reset functionality. | Developer & API Management | CONTRACTED | `resetSandbox` |
| 13.1.49 | API Certification Program - System shall support certification of integrations. | Developer & API Management | CONTRACTED | `requestProductionAccess` |
| 13.2.1 | Sandbox Environment Provisioning - System shall provide isolated sandbox environments. | Developer & API Management | CONTRACTED | data `Sandbox` |
| 13.2.2 | Multi-Tenant Sandbox Support - System shall support tenant-specific sandboxes. | Developer & API Management | PARKED | data `Sandbox` |
| 13.2.4 | Environment Cloning - System shall support cloning of environments. | Developer & API Management | PARKED | data `Sandbox` |
| 13.2.5 | Test Data Management - System shall support sandbox test data management. | Developer & API Management | CONTRACTED | data `Sandbox` |
| … 8 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Production access status is shown: sandbox only, requested (pending), approved, or rejected with the reason. Production keys only after certification; the request form says a new production key is issued and the sandbox key stays sandbox. *(agreed · MoM 17 Sep 2026, M17-06 · DI-927)*
- API keys can be partner-generated or TICVAI-generated with configurable expiry; sandbox keys are shown and kept separate from production keys, and production access is granted only after certification. *(agreed · MoM 17 Sep 2026, 4.10 Developer Accounts, API Credentials & Sandbox/Production Separation · DI-914)*
- The developer portal includes a product/data schema reference (field requirements, min/max lengths), an interactive "try it" API tester showing live request/response, an SDK library with sample code in JavaScript, Python, Java and .NET, a Postman collection and full documentation. *(client request · MoM 17 Sep 2026, 4.9 Developer Portal & API Documentation · DI-913)*

Also apply: 3 for all of P14, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P14 Developer.dc.html#dev-004` · status **notStarted** · provenance generated
- Flow F27 *A developer integrates*, step 4: They provision a sandbox and build against it. → Synthetic data, generated rather than sampled. **No production data is cloned or masked**, which is what removes the PDPL and DESC exposure entirely — and why this step needs no legal review at all.
- Flow F36 *A developer goes from sandbox to production*, step 1: They build and test against a sandbox with synthetic data. → **Synthetic data only**: nothing here can touch a live venue, so this is where every mistake is cheap. Their sandbox client carries module scopes (M17-05) and nothing else.
- Flow F27 branch at step 4 (recoverable): when The sandbox expires mid-build., **Data goes and the record stays.** A developer whose sandbox vanished entirely cannot tell it from one that never existed, and the expiry was counted in days on the screen before it happened.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (31 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#DEV-004?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Provision sandbox, Reset, Create sandbox, Reset sandbox, Request production access.
- [ ] Every transition is wired: `DEV-005`, `DEV-007`.
- [ ] Every gated control is gated: `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `DEV-005` Webhooks

**Subscribe to events, see every delivery, and replay what was missed.**

| | |
|---|---|
| App · platform | TICVAI Control · P14 Developer (web) |
| Module | Developer & API · wave 2 · needs the `developerApi` module |
| Block | Block B · task APP-DEVPORTAL-DEV-005 |
| Who uses it | partner staff holding `DEVELOPER_MANAGE`, `DEVELOPER_VIEW` (1 configure, 1 read); in the flows as partner |
| Device and orientation | This is a developer portal on a desktop browser, 1440 wide, with a docs-style left navigation. · LTR · light, dark theme |
| Pattern | listDetail (compact density): `listWebhookSubscriptions` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `subscriptionId` (deepLink) · cold entry: **A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. … |
| Route | `/developer/webhooks` |

**What the spec says about it.** 13.1.26 to 13.1.30, 13.3.17 to 13.3.23. **The 29 events already existed and nothing outside could receive one.**

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A developer's webhook subscriptions, every delivery with status and response, and replay of missed events from a point in time. The signing secret is shown once.

**Fixed on main** (the package already carries these; draw what it says): The subscription table shows signingSecret. (CHG-SOT-014); formCreateWebhookSubscription asks the person for status, id. (CHG-SOT-014); Tables show every schema field, plumbing included: 'Every webhook subscription' drop id, clientId; 'Every webhook delivery' drop id … (CHG-SOT-014).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| API client | picker: choose a client (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?clientId=` to `listWebhookSubscriptions`. Empty lists every subscription in the tenant; a client narrows it to that client's subscriptions. A partner sees only its own client's whatever it … | `listWebhookSubscriptions` ?clientId |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Publisher | text field | — | — | `listWebhookEventTypes` ?publisher |

**Form: Create webhook subscription** (modal, opened by *Create webhook subscription*; *Create webhook subscription* calls `createWebhookSubscription`, *Cancel* sends nothing)

**Collects what `createWebhookSubscription` sends before it is called.** The person picks the API client (by name) and enters `endpointUrl`, `eventTypes` and optional `filters`. Never `id` or `status`: the id is a client UUIDv7 generated silently and the status is the server's. `signingSecret`, `consecutiveFailures` and `disabledReason` are the server's: the secret is returned once in the response and shown then. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Client `clientId` | picker: choose a client | required | — | — | shows names, sends the id | — | `createWebhookSubscription` body |
| Endpoint URL `endpointUrl` | text field | required | — | — | — | — | `createWebhookSubscription` body |
| Event types `eventTypes` | multi-select chips | required | — | Access.validated · Accreditation.application decided · Accreditation.credential issued · Accreditation.holder status changed · Accreditation.renewal due · Ai.ceiling approaching · API client.anomaly detected · Approval.escalated · Approval.expired · … | — | Filtered at subscription, not at delivery. A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to. | `createWebhookSubscription` body |
| Filters `filters` | key and value settings | optional | — | — | — | 13.3.22. Tenant, venue, or a business condition on the payload. | `createWebhookSubscription` body |
| Signing secret `signingSecret` | text field | optional | — | — | — | How the receiver knows it was TICVAI. Without a signature an endpoint accepts a ticket-sale event from anybody who learns the URL. | `createWebhookSubscription` body |

Errors to draw in the form: 422 An entry in `eventTypes` is not in the webhook event catalogue.

**Form: Replay events** (modal, opened by *Replay events*; *Replay events* calls `replayEvents`, *Cancel* sends nothing)

**Collects what `replayEvents` sends before it is called.** Required: `from`. Optional: `to`, `eventTypes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| From `from` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `replayEvents` body |
| To `to` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `replayEvents` body |
| Event types `eventTypes` | multi-select chips | optional | — | Access.validated · Accreditation.application decided · Accreditation.credential issued · Accreditation.holder status changed · Accreditation.renewal due · Ai.ceiling approaching · API client.anomaly detected · Approval.escalated · Approval.expired · … | — | — | `replayEvents` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every webhook subscription** (data table, from `listWebhookSubscriptions`)

| Shows | Format | Notes |
|---|---|---|
| Endpoint URL | text | — |
| Event types | list or chips (count when long) | Filtered at subscription, not at delivery. A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to. |
| Filters | grouped details | 13.3.22. Tenant, venue, or a business condition on the payload. |
| Status | chip: Pending verification, Active, Paused, Failing, Disabled | — |
| Consecutive failures | 1,234 | — |
| Disabled reason | text | 13.1.29. An endpoint failing for days is disabled rather than retried forever, and the developer is told — a queue growing against a dead … |

**Every webhook delivery** (data table, from `listWebhookDeliveries`)

| Shows | Format | Notes |
|---|---|---|
| Event type | text | — |
| Status | chip: Pending, Delivered, Failed, Retrying, Abandoned | — |
| Attempt count | 1,234 | — |
| Response code | 1,234 | — |
| Response body excerpt | text | Truncated, and it is what makes the log useful — a 500 with the receiver's own error message in it answers the question without a … |
| Is replay | yes / no (icon or chip) | — |
| Delivered at | 1 Oct 2026, 14:30 | — |

**Data table** (data table): Status, attempts, response code and an excerpt of the receiver's own error. **The excerpt is what makes the log useful** — a 500 with their own message in it answers the question without a support conversation.

**The selected webhook subscription** (detail panel, from `listWebhookSubscriptions`): **The signing secret is shown once, at creation**, in the confirmation, with a copy action; afterwards it is never displayed (a secret in a list is a leak). The API client is shown by name.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Client | the name it points at, never the id | — |
| Endpoint URL | text | — |
| Event types | list or chips (count when long) | Filtered at subscription, not at delivery. A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to. |
| Filters | grouped details | 13.3.22. Tenant, venue, or a business condition on the payload. |
| Status | chip: Pending verification, Active, Paused, Failing, Disabled | — |
| Consecutive failures | 1,234 | — |
| Disabled reason | text | 13.1.29. An endpoint failing for days is disabled rather than retried forever, and the developer is told — a queue growing against a dead … |

**Card list** (card list): Failing subscriptions sort first and carry the consecutive-failure count. **A developer is told before it is disabled, not after.**

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Replay from… (secondary button) | navigation or local | — | — | — | — |
| Create webhook subscription (primary button) | `createWebhookSubscription` POST `/webhook-subscriptions` | WebhookSubscription | WebhookSubscription | 422 An entry in `eventTypes` is not in the webhook event catalogue. | opens modal first |
| Replay events (secondary button) | `replayEvents` POST `/webhook-subscriptions/{subscriptionId}/replay` | inline | inline | — | opens modal first |

**Data it reads**: `listWebhookSubscriptions` (onLoad, The tenant's webhook subscriptions, filterable by API …); `listWebhookEventTypes` (onLoad, Events a subscription can take)

**Where the user goes next**

- → `DEV-006` Usage & Limits: *They go live (production keys only after certification, flow F36), and watch whether it is healthy*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Subscriptions; failing ones first. |
| Error (`?state=error`) | Could not load. Deliveries continue regardless of this screen. |
| Empty, first run (`?state=emptyFirstRun`) | **No subscriptions. Twenty-nine business events are available** — and the state names a few, because a developer who does not know what exists cannot subscribe to it. |
| Empty, no results (`?state=emptyNoResults`) | No delivery matches this window or status. |
| Permission denied (`?state=emptyNoAccess`) | You do not have `DEVELOPER_VIEW`. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVELOPER_MANAGE` for `createWebhookSubscription`, `replayEvents`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 An entry in `eventTypes` is not in the webhook event catalogue. |

#### Edge cases to draw

- **Can read but not change (holds DEVELOPER_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: DEVELOPER_MANAGE for Create webhook subscription, Replay events. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/public-api.yaml#createWebhookSubscription)*
- **createWebhookSubscription answers 422**: Show it as something the person can act on, not a failure: An entry in `eventTypes` is not in the webhook event catalogue. *(source: contracts/satellite/public-api.yaml#createWebhookSubscription)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listWebhookDeliveries (WebhookDelivery):
- status: active
  attemptCount: 12
  responseCode: 12
  isReplay: true
  isTest: true
  deliveredAt: 01/10/2026 09:14
- status: pending
  attemptCount: 3
  responseCode: 3
  isReplay: false
  isTest: false
  deliveredAt: 30/09/2026 18:02
```

#### Permissions

- `listWebhookSubscriptions` → `DEVELOPER_VIEW` (read) · staff, partner
- `createWebhookSubscription` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `listWebhookDeliveries` → `DEVELOPER_VIEW` (read) · staff, partner
- `replayEvents` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `listWebhookEventTypes` → `DEVELOPER_VIEW` (read) · staff, partner

**A refused user sees:** You do not have `DEVELOPER_VIEW`. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVELOPER_MANAGE` for `createWebhookSubscription`, `replayEvents`.

#### Requirements it meets

13 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.19 | System shall support replay of historical events for recovery, synchronization, troubleshooting, and integration reprocessing purposes. | Developer & API Management | CONTRACTED | `replayEvents` |
| 13.3.21 | System shall maintain complete audit history of published events, subscriptions, deliveries, retries, failures, acknowledgements, and processing outcomes. | Developer & API Management | CONTRACTED | data `WebhookDelivery` |
| 13.3.23 | System shall monitor event delivery performance, processing status, failed deliveries, retry attempts, latency metrics, and subscriber health. | Developer & API Management | CONTRACTED | data `WebhookDelivery` |
| 13.1.25 | Webhook Testing Tools - System shall support webhook testing. | Developer & API Management | CONTRACTED | data `WebhookSubscription` |
| 13.1.26 | Webhook Registration - System shall support webhook registration. | Developer & API Management | CONTRACTED | data `WebhookSubscription` |
| 13.1.27 | Webhook Management - System shall support webhook management. | Developer & API Management | CONTRACTED | data `WebhookSubscription` |
| 13.1.28 | Webhook Event Catalog - System shall provide event documentation. | Developer & API Management | CONTRACTED | data `WebhookSubscription` |
| 13.1.29 | Webhook Retry Management - System shall support retry mechanisms. | Developer & API Management | CONTRACTED | data `WebhookSubscription` |
| 13.1.30 | Webhook Delivery Monitoring - System shall monitor webhook delivery status. | Developer & API Management | CONTRACTED | data `WebhookSubscription` |
| 13.3.17 | System shall publish business events such as ticket sales, ticket validation, membership changes, loyalty transactions, wallet transactions, reservations, access events, refunds, upgrades, and … | Developer & API Management | CONTRACTED | data `WebhookSubscription` |
| 13.3.18 | System shall allow authorized internal and external systems to subscribe to business events based on configurable subscription rules and permissions. | Developer & API Management | CONTRACTED | data `WebhookSubscription` |
| 13.3.20 | System shall support configurable retention policies for published events including archival, expiration, and compliance-based retention requirements. | Developer & API Management | CONTRACTED | data `WebhookSubscription` |
| … 1 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 3 for all of P14, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P14 Developer.dc.html#dev-005` · status **notStarted** · provenance generated
- Flow F27 *A developer integrates*, step 5: They subscribe to the events they need and watch the deliveries. → The endpoint is verified before the first delivery. **An unverified endpoint is somebody else's server being sent a venue's ticket sales.**
- Flow F27 branch at step 5 (recoverable): when Their endpoint fails repeatedly., `failing` before `disabled`, so **they are told before it stops rather than after**. And disabling is safe because `replayEvents` is the recovery path — nothing is lost, it is just not being pushed.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (21 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#DEV-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Replay from…, Create webhook subscription, Replay events.
- [ ] Every transition is wired: `DEV-006`.
- [ ] Every gated control is gated: `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `DEV-006` Usage & Limits

**See whether the integration is healthy, and whose fault it is when it is not.**

| | |
|---|---|
| App · platform | TICVAI Control · P14 Developer (web) |
| Module | Developer & API · wave 2 · needs the `developerApi` module |
| Block | Block B · task APP-DEVPORTAL-DEV-006 |
| Who uses it | partner staff holding `DEVELOPER_VIEW` (1 read); in the flows as partner |
| Device and orientation | This is a developer portal on a desktop browser, 1440 wide, with a docs-style left navigation. · LTR · light, dark theme |
| Pattern | statusTracker (compact density): `getApiUsage` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/developer/usage` |

**What the spec says about it.** 13.1.16 to 13.1.20 and 13.1.41 to 13.1.45. **One screen for five requirements, because they are one question asked five ways.**

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Usage against quota and flagged anomalies for the developer's clients, so they can tell whose fault a failure is.

**Fixed on main** (the package already carries these; draw what it says): Tables show every schema field, plumbing included: 'Flagged traffic' drop clientId. (CHG-SOT-014).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApiUsage` ?from |
| To | date picker | — | — | `getApiUsage` ?to |
| Client | picker: choose a client | — | — | `listApiAnomalies` ?clientId |
| From | date and time picker | — | — | `listApiAnomalies` ?from |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

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

**Metric tile** (metric tile): Calls, success rate, p95 latency, quota headroom.

**Chart** (chart): **Client errors and server errors on separate series.** A 4xx is the integrator's problem and a 5xx is ours, and one combined error rate lets both sides blame the other.

**Data table** (data table): Per operation, sorted by error rate rather than by volume.

**Flagged traffic** (data table, from `listApiAnomalies`): **Abnormal volume on your own clients** (17 September minutes, M17-07), so a runaway integration is seen here before a venue calls. The API client is shown by name, not by `clientId` (design-notes correction DEV-006).

| Shows | Format | Notes |
|---|---|---|
| Measure | text | — |
| Observed | 1,234.5 | — |
| Baseline | 1,234.5 | — |
| Action taken | chip: Flag, Throttle, Suspend | — |
| Detected at | 1 Oct 2026, 14:30 | — |

**Data it reads**: `getApiUsage` (onLoad, Calls, errors, latency); `listApiAnomalies` (onLoad, Abnormal traffic flagged on the developer's clients)

**Where the user goes next**

- → `DEV-007` Marketplace Listing: *They submit the integration for certification and listing*; calls `getApiUsage`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Call volume; the current window renders first. |
| Error (`?state=error`) | Could not load usage. Your quota is unaffected. |
| Empty, first run (`?state=emptyFirstRun`) | **No calls yet.** The state links to the reference rather than sitting blank — a developer who has registered and not called anything is a developer who needs a first request. |
| Empty, no results (`?state=emptyNoResults`) | No calls in this window. |
| Permission denied (`?state=emptyNoAccess`) | You do not have DEVELOPER_VIEW. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
getApiUsage (ApiUsageSummary):
- totalCalls: 12
  successRate: 12
  clientErrorRate: 12
  serverErrorRate: 12
  p50LatencyMs: 12
  p95LatencyMs: 12
  p99LatencyMs: 12
  quotaBreaches: 12
- totalCalls: 3
  successRate: 3
  clientErrorRate: 3
  serverErrorRate: 3
  p50LatencyMs: 3
  p95LatencyMs: 3
  p99LatencyMs: 3
  quotaBreaches: 3
```

#### Permissions

- `getApiUsage` → `DEVELOPER_VIEW` (read) · staff, partner
- `listApiAnomalies` → `DEVELOPER_VIEW` (read) · staff, partner

**A refused user sees:** You do not have DEVELOPER_VIEW.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.1.16 | API Usage Dashboard - System shall provide API usage dashboards. | Developer & API Management | CONTRACTED | data `ApiUsageSummary` |
| 13.1.17 | API Consumption Monitoring - System shall monitor API consumption. | Developer & API Management | CONTRACTED | data `ApiUsageSummary` |
| 13.1.18 | API Error Monitoring - System shall monitor API errors. | Developer & API Management | CONTRACTED | data `ApiUsageSummary` |
| 13.1.19 | API Performance Monitoring - System shall monitor API performance. | Developer & API Management | CONTRACTED | data `ApiUsageSummary` |
| 13.1.20 | API Latency Monitoring - System shall monitor API response times. | Developer & API Management | CONTRACTED | data `ApiUsageSummary` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Abnormal API volume is flagged, not only throttled (calls above the client's baseline, refusals outside the allow-list, calls to unused operations); a production access request requires at least one IP allow-list address. *(agreed · MoM 17 Sep 2026, M17-07 · DI-928)*

Also apply: 3 for all of P14, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P14 Developer.dc.html#dev-006` · status **notStarted** · provenance generated
- Flow F27 *A developer integrates*, step 6: They go live (production keys only after certification, flow F36), and watch whether it is healthy. → **Client errors and server errors on separate series.** A 4xx is theirs and a 5xx is ours, and one combined rate lets both sides blame the other.
- Flow F27 branch at step 6 (recoverable): when They exceed their quota., Throttled by default rather than rejected, and the 429 carries `Retry-After`. **A limit with no guidance produces a client that retries immediately and makes it worse.**

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#DEV-006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `DEV-007`.
- [ ] Every gated control is gated: `DEVELOPER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `DEV-007` Marketplace Listing

**Submit an integration for certification, and see where it is in review.**

| | |
|---|---|
| App · platform | TICVAI Control · P14 Developer (web) |
| Module | Developer & API · wave 3 · needs the `developerApi` module |
| Block | Block B · task APP-DEVPORTAL-DEV-007 |
| Who uses it | partner staff holding `DEVELOPER_MANAGE`, `DEVELOPER_VIEW` (1 configure, 1 read); in the flows as partner |
| Device and orientation | This is a developer portal on a desktop browser, 1440 wide, with a docs-style left navigation. · LTR · light, dark theme |
| Pattern | listDetail (compact density): `listIntegrationListings` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/developer/marketplace` |

**What the spec says about it.** 13.1.49 and 13.1.50, decision D1. **A listing, not an installation** — the integration runs on the developer's own infrastructure, and third-party code does not execute inside TICVAI.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The developer's view of support and status for the API.

**Fixed on main** (the package already carries these; draw what it says): formSubmitIntegrationListing asks the person for status, id. (CHG-SOT-014); Tables show every schema field, plumbing included: 'Every integration listing' drop id, developerId. (CHG-SOT-014).

#### Inputs: what the user enters or picks

**Form: Submit integration listing** (modal, opened by *Submit integration listing*; *Submit integration listing* calls `submitIntegrationListing`, *Cancel* sends nothing)

**Collects what `submitIntegrationListing` sends before it is called.** The person enters `name`, `category`, `description`, `integrationUrl` and the `requiredScopes`, and chooses `visibility`. `developerId` comes from the session. Never `id` or `status`: the id is a client UUIDv7 generated silently and the status is the server's. Certification fields (`certifiedUntil`, `certifiedAgainstVersion`) and `listingFeeModel` are set by TICVAI on DEV-008. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Developer `developerId` | picker: choose a developer | required | — | — | shows names, sends the id | — | `submitIntegrationListing` body |
| Name `name` | text field | required | — | — | — | — | `submitIntegrationListing` body |
| Category `category` | select | required | — | Crm · Marketing · Accounting · Hotel · Transport · Analytics · Accessibility · Other | — | — | `submitIntegrationListing` body |
| Description `description` | text area | optional | — | — | — | — | `submitIntegrationListing` body |
| Integration URL `integrationUrl` | text field | optional | — | — | — | — | `submitIntegrationListing` body |
| Required scopes `requiredScopes` | list of values (chips) | optional | — | — | — | — | `submitIntegrationListing` body |
| Listing fee model `listingFeeModel` | segmented control | optional | — | None · Flat · Revenue share | — | — | `submitIntegrationListing` body |
| Visibility `visibility` | segmented control | optional | Public | Public · Private | — | `private`: certified for production access and never shown in the marketplace (17 September minutes, M17-06). | `submitIntegrationListing` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every integration listing** (data table, from `listIntegrationListings`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Category | chip: Crm, Marketing, Accounting, Hotel, Transport, Analytics… | — |
| Description | text | — |
| Status | chip: Draft, Submitted, In review, Certified, Rejected, Revoked… | — |
| Certified until | 1 Oct 2026 | Certification expires. An integration certified against v1 and still listed after v3 is TICVAI vouching for something it has not looked at … |
| Listing fee model | chip: None, Flat, Revenue share | — |

**Banner** (banner): **Certification expires, and the date is shown.** An integration certified against v1 and still listed after v3 is Softlabs vouching for something nobody has looked at in two years. When it lapses, the production clients issued against it are suspended.

**The selected integration listing** (detail panel, from `listIntegrationListings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Developer | the name it points at, never the id | — |
| Name | text | — |
| Category | chip: Crm, Marketing, Accounting, Hotel, Transport, Analytics… | — |
| Description | text | — |
| Integration URL | text | — |
| Required scopes | list or chips (count when long) | — |
| Status | chip: Draft, Submitted, In review, Certified, Rejected, Revoked… | — |
| Certified until | 1 Oct 2026 | Certification expires. An integration certified against v1 and still listed after v3 is TICVAI vouching for something it has not looked at … |
| Certified against version | text | — |
| Listing fee model | chip: None, Flat, Revenue share | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Submit for certification (primary button) | navigation or local | — | — | — | — |
| Submit integration listing (primary button) | `submitIntegrationListing` POST `/listings` | IntegrationListing | IntegrationListing | — | opens modal first |

**Data it reads**: `listIntegrationListings` (onLoad, Published integrations)

**Where the user goes next**

- → `DEV-008` Programme Administration: *TICVAI reviews the integration and certifies it*; carries `listingId`; calls `submitIntegrationListing`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Listings with their certification status. |
| Error (`?state=error`) | Could not load listings. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing submitted. Certification gates production keys and the listing** (17 September minutes, M17-06): build and test in the sandbox, submit here, and once certified request production access. A private integration is certified without appearing in the marketplace. |
| Empty, no results (`?state=emptyNoResults`) | No listing matches this category or status. |
| Permission denied (`?state=emptyNoAccess`) | Without `DEVELOPER_VIEW`, which `listIntegrationListings` requires, the screen does not load and this state names that permission. You do not have `DEVELOPER_MANAGE`. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds DEVELOPER_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: DEVELOPER_MANAGE for Submit integration listing. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/public-api.yaml#submitIntegrationListing)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every integration listing:
- name: Kiosk connector (sandbox)
  description: Guest charged twice at Main Gate Till 3
  status: active
  certifiedUntil: 31/12/2026 23:59
- name: OTA availability feed
  description: Group of 40 from Desert Gate Tours
  status: pending
  certifiedUntil: 15/10/2026 00:00
- name: Wallet sync
  description: Annual pass upgrade for the Al Nuaimi family
  status: suspended
  certifiedUntil: 01/11/2026 06:00
```

#### Permissions

- `listIntegrationListings` → `DEVELOPER_VIEW` (read) · public, staff, partner
- `submitIntegrationListing` → `DEVELOPER_MANAGE` (configure) · partner

**A refused user sees:** Without `DEVELOPER_VIEW`, which `listIntegrationListings` requires, the screen does not load and this state names that permission. You do not have `DEVELOPER_MANAGE`.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.1.50 | API Marketplace - System shall support publishing integrations and extensions. | Developer & API Management | CONTRACTED | data `IntegrationListing` |
| 13.3.16 | APIs shall support installation, activation and management of third-party integrations and marketplace extensions. | Developer & API Management | CONTRACTED | data `IntegrationListing` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Production access status is shown: sandbox only, requested (pending), approved, or rejected with the reason. Production keys only after certification; the request form says a new production key is issued and the sandbox key stays sandbox. *(agreed · MoM 17 Sep 2026, M17-06 · DI-927)*

Also apply: 3 for all of P14, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P14 Developer.dc.html#dev-007` · status **notStarted** · provenance generated
- Flow F27 *A developer integrates*, step 7: They submit the integration for certification and listing. → Submitted for review. **Certification is a Softlabs act on `DEV-008`, not something the developer does** — the flow named both on one screen and the checker refused, correctly. Listed once certified. …
- Flow F36 *A developer goes from sandbox to production*, step 2: They submit the integration for certification. → **Submitted for review, with visibility public or private** (M17-06): a private listing is certified for the tenants it serves and never appears in the marketplace.
- Flow F27 branch at step 7 (recoverable): when Certification is refused., **Sandbox access is unaffected; production stays closed.** Production keys are issued only after certification (17 September minutes M17-06, decided again 29 September): the route is flow F36 …
- Flow F27 branch at step 7 (recoverable): when The API version they built against is deprecated., Twelve months' notice, and **the notification names the operations they actually call**. A generic *"v1 is retiring"* to somebody using three of two hundred endpoints is a message they will ignore.
- Flow F36 branch at step 4 (recoverable): when The integration named is not certified, or its certification has lapsed., **Refused 409 `certification-required`.** There is no route to production that skips certification, including creating a production client directly (createApiClient refuses it the same way unless …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#DEV-007?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Submit for certification, Submit integration listing.
- [ ] Every transition is wired: `DEV-008`.
- [ ] Every gated control is gated: `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `DEV-008` Programme Administration

**Set quotas, certify integrations and configure licensing.**

| | |
|---|---|
| App · platform | TICVAI Control · P14 Developer (web) |
| Module | Developer & API · wave 1 · needs the `developerApi` module |
| Block | Block A · task APP-SETUP-DEV-008 |
| Who uses it | partner staff holding `DEVELOPER_ADMIN`, `DEVELOPER_VIEW` (1 configure, 1 read); in the flows as partner |
| Device and orientation | This is a developer portal on a desktop browser, 1440 wide, with a docs-style left navigation. · LTR · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`setApiQuota`, `certifyIntegration`, `setApiLicensing`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `listingId` (deepLink), `version` (deepLink), `requestId` (navigation) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/developer/admin` |

**What the spec says about it.** **`DEVELOPER_ADMIN` throughout, and never shown to a developer.** Decision D5 makes the commercial model configuration rather than code — this is the surface, and the rates themselves remain CF-135c. **Staff audience on a partner platform, and deliberately.** Every operation here — `setApiQuota`, `certifyIntegration`, `setApiLicensing`, `deprecateApiVersion` — is **Softlabs administering the programme, not a developer self-serving.** A developer who could set their own quota has no quota. **Declared on the screen rather than the platform** because P14 is a partner surface with one staff screen on it, and moving the screen to P09 would separate the console from the catalogue it governs. `check-screens` reads `screen.audience` before the platform’s. **Quota form labelled 2 October 2026 (CHG-SOT-014, design-notes correction DEV-008):** number fields with units and a client picker replace the raw schema names; the quota id is the server's.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** TICVAI's programme administration behind the developer portal: per-client quotas, certification of integrations (with an end date), the production-access queue, anomaly rules, API licensing per tenant and version deprecation. Never shown to a developer; a developer reaching it is told plainly it is a TICVAI screen.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- listProductionAccessRequests allows the partner audience with DEVELOPER_VIEW. (CHG-SOT-016)

**Fixed on main** (the package already carries these; draw what it says): Text fields named id, clientId, sustainedPerMinute, burstPerSecond, dailyCap, perOperationOverrides, onBreach. (CHG-SOT-014).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| API client | picker: choose a client | optional | — | — | shows names, sends the id | A picker of API clients by developer and name, never a typed id. | `ApiQuota.clientId` |
| Sustained calls per minute | number field | optional | — | — | — | — | `ApiQuota.sustainedPerMinute` |
| Burst calls per second | number field | optional | — | — | — | Separate from the sustained rate, because a nightly sync is a legitimate spike and a flat per-second limit either blocks it or permits the flood it was meant to stop. | `ApiQuota.burstPerSecond` |
| Daily cap (calls) | number field | optional | — | — | — | Empty for no daily cap. | `ApiQuota.dailyCap` |
| On breach | segmented control | optional | Throttle | Throttle · Reject · Queue | — | What happens when the quota is exceeded. | `ApiQuota.onBreach` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Pending · Approved · Rejected · Withdrawn | `listProductionAccessRequests` ?status |

**Form: Certify integration** (modal, opened by *Certify integration*; *Certify integration* calls `certifyIntegration`, *Cancel* sends nothing)

**Collects what `certifyIntegration` sends before it is called.** Required: `decision`. Optional: `certifiedUntil`, `notes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | segmented control | required | — | Certify · Reject · Revoke | — | — | `certifyIntegration` body |
| Certified until `certifiedUntil` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `certifyIntegration` body |
| Notes `notes` | text area | optional | — | — | — | — | `certifyIntegration` body |

**Form: Save API licensing** (modal, opened by *Save API licensing*; *Save API licensing* calls `setApiLicensing`, *Cancel* sends nothing)

**Collects what `setApiLicensing` sends before it is called.** Required: `licensedModules`. Optional: `callAllowancePerMonth`, `overageRatePerThousand`, `revenueSharePercent`, `effectiveFrom`, `effectiveTo`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets it (readOnly in the contract): `id` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tenant `tenantId` | picker: choose a tenant | required | — | — | shows names, sends the id | — | `setApiLicensing` body |
| Licensed modules `licensedModules` | list of values (chips) | required | — | — | — | The example in the requirement is the shape: a venue licensing the ticketing API and not the F&B one. | `setApiLicensing` body |
| Call allowance per month `callAllowancePerMonth` | number field | optional | — | — | — | — | `setApiLicensing` body |
| Catalogue write exception `catalogueWriteException` | group | optional | — | — | — | M17-04: the one way a client reaches a catalogue write, set by TICVAI platform staff only (`setApiLicensing` refuses anyone else 403 `platform-staff-only`). | `setApiLicensing` body |
| Client `catalogueWriteException.clientId` | picker: choose a client | required | — | — | shows names, sends the id | — | `setApiLicensing` body |
| Operations `catalogueWriteException.operationIds` | multi-select chips | required | — | Create product · Update product · Set product attributes · Create price list · Update price list · Copy price list · Set prices · Create channel capacity · Update channel capacity · Set channel allocations · Transition product lifecycle · Set alternative … | — | — | `setApiLicensing` body |
| Reason `catalogueWriteException.reason` | text area | required | — | max length 500 | — | — | `setApiLicensing` body |
| Granted until `catalogueWriteException.grantedUntil` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setApiLicensing` body |
| Overage rate per thousand `overageRatePerThousand` | number field | optional | — | — | — | — | `setApiLicensing` body |
| Revenue share percent `revenueSharePercent` | number field | optional | — | — | — | — | `setApiLicensing` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setApiLicensing` body |
| Effective to `effectiveTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setApiLicensing` body |

Errors to draw in the form: 403 `catalogueWriteException` was sent by a principal that is not TICVAI platform staff (`platform-staff-only`, M17-04).

**Form: Deprecate API version** (modal, opened by *Deprecate API version*; *Deprecate API version* calls `deprecateApiVersion`, *Cancel* sends nothing)

**Collects what `deprecateApiVersion` sends before it is called.** Required: `sunsetAt`, `reason`. Optional: `migrationGuideUrl`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sunset at `sunsetAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `deprecateApiVersion` body |
| Reason `reason` | text area | required | — | — | — | — | `deprecateApiVersion` body |
| Migration guide URL `migrationGuideUrl` | text field | optional | — | — | — | — | `deprecateApiVersion` body |

**Form: Decide production access** (modal, opened by *Decide production access*; *Decide production access* calls `decideProductionAccess`, *Cancel* sends nothing)

**Collects what `decideProductionAccess` sends before it is called.** Required: `decision`. Optional: `reason` (required to reject), `scopes` (narrow only), `credentialTtlDays`.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | segmented control | required | — | Approve · Reject | — | — | `decideProductionAccess` body |
| Reason `reason` | text area | optional | — | max length 1000 | — | — | `decideProductionAccess` body |
| Scopes `scopes` | list of values (chips) | optional | — | — | — | Narrow the requested scopes. Never widens them. | `decideProductionAccess` body |
| Credential ttl days `credentialTtlDays` | number field (days) | optional | 365 | min 1; max 730 | — | — | `decideProductionAccess` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already decided (`already-decided`), or the listing's certification lapsed since the request (`certification-required`).; 422 `reject` without a `reason`.

**Form: Save anomaly rule** (modal, opened by *Save anomaly rule*; *Save anomaly rule* calls `setApiAnomalyRule`, *Cancel* sends nothing)

**Collects what `setApiAnomalyRule` sends before it is called.** Required: `ruleKey`, `measure`, `comparison`, `threshold`, `action`.

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

**Sent by *Save API quota*** (`setApiQuota`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Client `clientId` | picker: choose a client | required | — | — | shows names, sends the id | — | `setApiQuota` body |
| Sustained per minute `sustainedPerMinute` | number field | required | — | — | — | — | `setApiQuota` body |
| Burst per second `burstPerSecond` | number field | optional | — | — | — | Separate from the sustained rate, because a nightly sync is a legitimate spike and a flat per-second limit either blocks it or permits the flood it was meant to stop. | `setApiQuota` body |
| Daily cap `dailyCap` | number field | optional | — | — | — | — | `setApiQuota` body |
| Per operation overrides `perOperationOverrides` | key and value settings | optional | — | — | — | Availability checks and order creation deserve different limits — one is cheap and polled, the other is expensive and rare. | `setApiQuota` body |
| On breach `onBreach` | segmented control | optional | Throttle | Throttle · Reject · Queue | — | — | `setApiQuota` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Quota**: Sustained per minute, burst per second, daily cap, per-operation overrides and the action on breach; within the tenant's request budget. *(source: contracts/satellite/public-api.yaml#setApiQuota; ADR-0064)*
- **Decide production access**: Approve issues a new production client bound to the certified listing with its own expiry (default 365 days, 1 to 730); scopes may only be narrowed; reject needs a reason the developer can act on. *(source: contracts/satellite/public-api.yaml#decideProductionAccess; F36 step 5)*
- **Deprecate version**: Sunset date, reason and migration guide; the banner names how many clients call it and which operations they use. *(source: contracts/satellite/public-api.yaml#deprecateApiVersion; ADR-0026)*
- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setApiQuota, setApiLicensing, setApiAnomalyRule: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/public-api.yaml#setApiQuota)*

#### Outputs: what the screen shows and produces

**Shown**

**Per-operation limits** (data table, from `setApiQuota`): An operation and its own per-minute limit, one row each.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Client | the name it points at, never the id | — |
| Sustained per minute | 1,234 | — |
| Burst per second | 1,234 | Separate from the sustained rate, because a nightly sync is a legitimate spike and a flat per-second limit either blocks it or permits the … |
| Daily cap | 1,234 | — |
| Per operation overrides | grouped details | Availability checks and order creation deserve different limits — one is cheap and polled, the other is expensive and rare. |
| On breach | chip: Throttle, Reject, Queue | — |

**Banner** (banner): **Deprecating a version names how many clients call it and which operations they use.** A generic "v1 is retiring" to somebody using three of two hundred endpoints is a message they will ignore.

**Production access requests** (data table, from `listProductionAccessRequests`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Developer | the name it points at, never the id | — |
| Sandbox client | the name it points at, never the id | — |
| Listing | the name it points at, never the id | — |
| Scopes | list or chips (count when long) | — |
| Allowed tenants | list or chips (count when long) | — |
| Ip allow list | list or chips (count when long) | — |
| Note | text | — |
| Status | chip: Pending, Approved, Rejected, Withdrawn | — |
| Decided by principal | the name it points at, never the id | — |
| Decided at | 1 Oct 2026, 14:30 | — |
| Reason | text | — |
| Production client | the name it points at, never the id | — |
| Requested at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Tree nav** (tree nav): Quotas · Certification queue · Production access · Anomaly rules · Licensing · Versions.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |
| Reject (secondary button) | navigation or local | — | — | — | — |
| Save API quota (primary button) | `setApiQuota` PUT `/api-quotas` | ApiQuota | ApiQuota | — | — |
| Certify integration (secondary button) | `certifyIntegration` POST `/listings/{listingId}/certify` | inline | IntegrationListing | — | opens modal first |
| Save API licensing (secondary button) | `setApiLicensing` PUT `/api-licensing` | ApiLicence | ApiLicence | 403 `catalogueWriteException` was sent by a principal that is not TICVAI platform staff (`platform-staff-only`, M17-04). | opens modal first |
| Deprecate API version (secondary button) | `deprecateApiVersion` POST `/api-versions/{version}/deprecate` | inline | ApiVersion | — | opens modal first |
| Decide production access (secondary button) | `decideProductionAccess` POST `/production-access-requests/{requestId}/decide` | inline | ProductionAccessRequest | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already decided (`already-decided`), or the listing's certification lapsed since the request … | opens modal first |
| Save anomaly rule (secondary button) | `setApiAnomalyRule` PUT `/api-anomaly-rules` | ApiAnomalyRule | ApiAnomalyRule | — | opens modal first |

**Data it reads**: `listProductionAccessRequests` (onLoad, The production key queue)

**Where the user goes next**

- → `DEV-003` Clients & Credentials: *They request production access for the certified integration*; carries `clientId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Pending certifications first. |
| Error (`?state=error`) | Could not load. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing awaiting review. |
| Permission denied (`?state=emptyNoAccess`) | **This is a Softlabs screen and you are a developer.** Said plainly — a blank administration page shown to a partner is worse than a refusal, because they will file a support ticket about it. |
| Empty, no results (`?state=emptyNoResults`) | No production access request with this status. Names the filter and offers to clear it. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already decided (`already-decided`), or the listing's certification lapsed since the request (`certification-required`).; 422 `reject` without a `reason`. |

#### Edge cases to draw

- **Can read but not change (holds DEVELOPER_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: DEVELOPER_ADMIN for Save API quota, Certify integration, Save API licensing. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/public-api.yaml#setApiQuota)*
- **setApiLicensing answers 403**: Show it as something the person can act on, not a failure: `catalogueWriteException` was sent by a principal that is not TICVAI platform staff (`platform-staff-only`, M17-04). *(source: contracts/satellite/public-api.yaml#setApiLicensing)*
- **decideProductionAccess answers 409**: Show it as something the person can act on, not a failure: Already decided (`already-decided`), or the listing's certification lapsed since the request (`certification-required`). *(source: contracts/satellite/public-api.yaml#decideProductionAccess)*
- **decideProductionAccess answers 422**: Show it as something the person can act on, not a failure: `reject` without a `reason`. *(source: contracts/satellite/public-api.yaml#decideProductionAccess)*

#### Consistency with other screens

- Match `DEV-003`: The developer's request and status shown there are decided here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
queue:
- developer: Gulf Kiosk Systems FZ-LLC
  listing: AquaCove Kiosk Connector v1.2
  tenants:
  - Marina Leisure Group
  scopes:
  - ticketing.read
  - orders.write
  ip: 185.53.2.10
  requested: 30/09/2026
quota:
  client: Kiosk connector
  sustainedPerMinute: 600
  burstPerSecond: 20
  dailyCap: 200000
  onBreach: throttle
```

#### Permissions

- `setApiQuota` → `DEVELOPER_ADMIN` (configure) · staff
- `certifyIntegration` → `DEVELOPER_ADMIN` (configure) · staff
- `setApiLicensing` → `DEVELOPER_ADMIN` (configure) · staff
- `deprecateApiVersion` → `DEVELOPER_ADMIN` (configure) · staff
- `listProductionAccessRequests` → `DEVELOPER_VIEW` (read) · staff, partner
- `decideProductionAccess` → `DEVELOPER_ADMIN` (configure) · staff
- `setApiAnomalyRule` → `DEVELOPER_ADMIN` (configure) · staff

**A refused user sees:** **This is a Softlabs screen and you are a developer.** Said plainly — a blank administration page shown to a partner is worse than a refusal, because they will file a support ticket about it.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.1.12 | Client Secret Management - System shall support client secret management. | Developer & API Management | CONTRACTED | `decideProductionAccess` |
| 13.1.39 | API Audit Logs - System shall maintain API audit logs. | Developer & API Management | CONTRACTED | `setApiAnomalyRule` |
| 13.1.36 | Rate Limiting - System shall support API rate limiting. | Developer & API Management | CONTRACTED | data `ApiQuota` |
| 13.1.37 | Throttling Rules - System shall support API throttling. | Developer & API Management | CONTRACTED | data `ApiQuota` |

#### Client meeting inputs

None names this screen.

Also apply: 3 for all of P14, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P14 Developer.dc.html#dev-008` · status **notStarted** · provenance generated
- Flow F36 *A developer goes from sandbox to production*, step 3: TICVAI reviews the integration and certifies it. → **Certification is a TICVAI act, not the developer's**, and it has an end date (`certifiedUntil`). The listing moves to `certified`.
- Flow F36 *A developer goes from sandbox to production*, step 5: TICVAI decides the request. → **Approval issues a new production client** (`issuedBy: ticvai`, bound to the certified listing, with its own expiry). Nothing is promoted; the decision and who made it are recorded.
- Flow F36 branch at step 3 (recoverable): when Certification is refused., **Sandbox access is unaffected; production stays closed.** The refusal gives the reason, and the developer resubmits from DEV-007 once it is fixed.
- Flow F36 branch at step 5 (recoverable): when TICVAI rejects the request., The rejection carries the reason. The sandbox client and the certification stand; the developer corrects the request and asks again.

#### Acceptance for the design

- [ ] Every input above is drawn (41), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#DEV-008?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Approve, Reject, Save API quota, Certify integration, Save API licensing, Deprecate API version, Decide production access, Save anomaly rule.
- [ ] Every transition is wired: `DEV-003`.
- [ ] Every gated control is gated: `DEVELOPER_ADMIN`, `DEVELOPER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P14 reference designs** (from `handoff/design-batches/apps/6-ticvai-controller/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for density.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P14 Developer

- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

**13 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"certifyIntegration": {"method":"POST","path":"/listings/{listingId}/certify","contract":"public-api","summary":"Approve, reject or revoke a certification","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"IntegrationListing"},
"createApiClient": {"method":"POST","path":"/api-clients","contract":"public-api","summary":"Create a client with scopes and an environment","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApiClient","responds":null},
"createSandbox": {"method":"POST","path":"/sandboxes","contract":"public-api","summary":"Provision a sandbox with synthetic data","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createWebhookSubscription": {"method":"POST","path":"/webhook-subscriptions","contract":"public-api","summary":"Subscribe to business events","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WebhookSubscription","responds":"WebhookSubscription"},
"decideProductionAccess": {"method":"POST","path":"/production-access-requests/{requestId}/decide","contract":"public-api","summary":"Approve or reject production access","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductionAccessRequest"},
"deprecateApiVersion": {"method":"POST","path":"/api-versions/{version}/deprecate","contract":"public-api","summary":"Announce a sunset date and notify subscribers","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApiVersion"},
"getApiUsage": {"method":"GET","path":"/api-usage","contract":"public-api","summary":"Calls, errors, latency and success rate","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"ApiUsageSummary"},
"listApiAnomalies": {"method":"GET","path":"/api-anomalies","contract":"public-api","summary":"Flagged API traffic","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"clientId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listApiClients": {"method":"GET","path":"/api-clients","contract":"public-api","summary":"Registered clients for this developer","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ApiClient"},
"listApiScopes": {"method":"GET","path":"/api-scopes","contract":"public-api","summary":"The scope catalogue, one read and one write scope per module","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"module","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listApiVersions": {"method":"GET","path":"/api-versions","contract":"public-api","summary":"Versions, their status and their sunset dates","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ApiVersion"},
"listIntegrationListings": {"method":"GET","path":"/listings","contract":"public-api","summary":"Published third-party integrations","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"IntegrationListing"},
"listProductionAccessRequests": {"method":"GET","path":"/production-access-requests","contract":"public-api","summary":"Production access requests, pending first","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSandboxes": {"method":"GET","path":"/sandboxes","contract":"public-api","summary":"Sandbox environments","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"Sandbox"},
"listWebhookDeliveries": {"method":"GET","path":"/webhook-subscriptions/{subscriptionId}/deliveries","contract":"public-api","summary":"What was sent, what failed, and why","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"WebhookDelivery"},
"listWebhookEventTypes": {"method":"GET","path":"/webhook-event-types","contract":"public-api","summary":"The events a webhook may subscribe to","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"publisher","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWebhookSubscriptions": {"method":"GET","path":"/webhook-subscriptions","contract":"public-api","summary":"The tenant's webhook subscriptions, filterable by API client","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"clientId","in":"query","required":false}],"requestBody":null,"responds":"WebhookSubscription"},
"registerDeveloper": {"method":"POST","path":"/developers","contract":"public-api","summary":"Register a developer or organisation","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DeveloperAccount","responds":"DeveloperAccount"},
"replayEvents": {"method":"POST","path":"/webhook-subscriptions/{subscriptionId}/replay","contract":"public-api","summary":"Re-deliver events from a point in time","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"requestProductionAccess": {"method":"POST","path":"/api-clients/{clientId}/production-access","contract":"public-api","summary":"Ask for production keys for a sandbox client that passed certification","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductionAccessRequest"},
"resetSandbox": {"method":"POST","path":"/sandboxes/{sandboxId}/reset","contract":"public-api","summary":"Back to a clean synthetic dataset","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"revokeApiCredential": {"method":"DELETE","path":"/api-clients/{clientId}/credentials","contract":"public-api","summary":"Revoke immediately","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"rotateApiCredential": {"method":"POST","path":"/api-clients/{clientId}/credentials","contract":"public-api","summary":"Issue a new secret, with an overlap window","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setApiAnomalyRule": {"method":"PUT","path":"/api-anomaly-rules","contract":"public-api","summary":"When API traffic is flagged as abnormal","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApiAnomalyRule","responds":"ApiAnomalyRule"},
"setApiLicensing": {"method":"PUT","path":"/api-licensing","contract":"public-api","summary":"Which API modules a tenant has licensed, and on what terms","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApiLicence","responds":"ApiLicence"},
"setApiQuota": {"method":"PUT","path":"/api-quotas","contract":"public-api","summary":"Rate limits and throttling per client","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApiQuota","responds":"ApiQuota"},
"setDeveloperMembers": {"method":"PUT","path":"/developers/{developerId}/members","contract":"public-api","summary":"Who at this organisation may do what","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"submitIntegrationListing": {"method":"POST","path":"/listings","contract":"public-api","summary":"Submit an integration for certification (and, if public, listing)","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"IntegrationListing","responds":"IntegrationListing"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApiAnomaly": {"type":"object","x-ticvai-persistence":"control.api_anomaly","description":"One flagged breach of an anomaly rule (M17-07).","required":["id","ruleKey","clientId","detectedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"ruleKey":{"type":"string"},"clientId":{"type":"string","format":"uuid","x-ticvai-references":"control.api_client"},"measure":{"type":"string"},"observed":{"type":"number"},"baseline":{"type":"number","nullable":true},"actionTaken":{"type":"string","enum":["flag","throttle","suspend"]},"detectedAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"ApiAnomalyRule": {"type":"object","x-ticvai-persistence":"control.api_anomaly_rule","description":"**When API traffic is abnormal** (17 September minutes, M17-07). Platform defaults ship for every tenant; TICVAI tightens them per tenant or per client.\n","required":["ruleKey","measure","comparison","threshold","action"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"ruleKey":{"type":"string"},"clientId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"control.api_client","description":"Null applies to every client of the tenant."},"measure":{"type":"string","enum":["callsPerMinute","clientErrorShare","allowListRefusals","unusualOperations","authFailures"]},"comparison":{"type":"string","enum":["aboveBaselineMultiple","aboveFixed"],"description":"`aboveBaselineMultiple`: above `threshold` x the same hour over the last four weeks."},"threshold":{"type":"number"},"windowMinutes":{"type":"integer","minimum":1,"default":5},"action":{"type":"string","enum":["flag","throttle","suspend"],"default":"flag"},"isActive":{"type":"boolean","default":true}}},
"ApiClient": {"type":"object","x-ticvai-persistence":"control.api_client","description":"CF-135a. **The one credential model.** 2.7.52, 7.1.25 and 7.1.30 each asserted their own, so a partner API key, a POS integration credential and a webstore credential were three unrelated things with three lifecycles.\n","required":["id","developerId","name","environment","scopes","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid"},"name":{"type":"string"},"clientId":{"type":"string","readOnly":true},"environment":{"type":"string","enum":["sandbox","production"],"description":"**Bound to one, stated on the object rather than by naming convention.** A key that works in both is a key somebody will use in the wrong one.\n"},"scopes":{"type":"array","description":"**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing. **Module scopes** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, one of `listApiScopes`.\n","items":{"type":"string","pattern":"^[a-zA-Z]+\\.(read|write)$"}},"issuedBy":{"type":"string","enum":["partner","ticvai"],"readOnly":true,"description":"Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`.\n"},"certificationListingId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"control.integration_listing","description":"For a production client, the certified integration it was issued against."},"credentialTtlDays":{"type":"integer","minimum":1,"maximum":730,"nullable":true,"description":"Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry)."},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the key stops working unless rotated. No token is issued after it."},"allowedTenantIds":{"type":"array","description":"13.1.46. **Which tenants this client may act for.** A developer integrating for one venue must not reach another, and a client with an empty list reaches none.\n","items":{"type":"string","format":"uuid"}},"ipAllowList":{"type":"array","description":"13.1.38. **Required on a production client** (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the internet); optional in the sandbox. CIDR ranges. Checked at token issue and on every call.\n","items":{"type":"string"}},"status":{"type":"string","enum":["active","suspended","revoked"],"readOnly":true},"lastUsedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**A credential unused for a year is a credential nobody will notice being stolen.**\n"}}},
"ApiLicence": {"type":"object","x-ticvai-persistence":"control.api_licence","description":"13.3.24, decision D5. **Configuration, not code** — rates and terms change without a release.\n**The rates themselves are CF-135c and remain open.** This is the surface they will be set through.\n","required":["tenantId","licensedModules"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"tenantId":{"type":"string","format":"uuid"},"licensedModules":{"type":"array","description":"**The example in the requirement is the shape**: a venue licensing the ticketing API and not the F&B one. **The platform module list** (17 September minutes, M17-05), so the licence, the scope catalogue and the modules a tenant buys are one vocabulary.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"}},"callAllowancePerMonth":{"type":"integer","nullable":true},"catalogueWriteException":{"type":"object","nullable":true,"description":"**M17-04: the one way a client reaches a catalogue write**, set by TICVAI platform staff only (`setApiLicensing` refuses anyone else 403 `platform-staff-only`). Null, the default, means no partner or developer client of this tenant can create or change products, price lists, prices, channel capacity, lifecycle or alternative codes.\n","required":["clientId","operationIds","reason","grantedUntil"],"properties":{"clientId":{"type":"string","format":"uuid","x-ticvai-references":"control.api_client"},"operationIds":{"type":"array","minItems":1,"items":{"type":"string","enum":["createProduct","updateProduct","setProductAttributes","createPriceList","updatePriceList","copyPriceList","setPrices","createChannelCapacity","updateChannelCapacity","setChannelAllocations","transitionProductLifecycle","setAlternativeCodes"]}},"reason":{"type":"string","maxLength":500},"grantedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"grantedUntil":{"type":"string","format":"date"}}},"overageRatePerThousand":{"type":"number","nullable":true},"revenueSharePercent":{"type":"number","nullable":true},"effectiveFrom":{"type":"string","format":"date"},"effectiveTo":{"type":"string","format":"date","nullable":true}}},
"ApiQuota": {"type":"object","x-ticvai-persistence":"control.api_limit","description":"13.1.36 and 13.1.37. **A quota protects the venue, not the developer.**\n","required":["clientId","sustainedPerMinute"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"clientId":{"type":"string","format":"uuid"},"sustainedPerMinute":{"type":"integer"},"burstPerSecond":{"type":"integer","description":"**Separate from the sustained rate**, because a nightly sync is a legitimate spike and a flat per-second limit either blocks it or permits the flood it was meant to stop.\n"},"dailyCap":{"type":"integer","nullable":true},"perOperationOverrides":{"type":"object","additionalProperties":{"type":"integer"},"description":"**Availability checks and order creation deserve different limits** — one is cheap and polled, the other is expensive and rare.\n"},"onBreach":{"type":"string","enum":["throttle","reject","queue"],"default":"throttle"}}},
"ApiScope": {"type":"object","x-ticvai-persistence":"none — generated at release from x-ticvai-api-scope on each partner-callable operation","description":"**One module scope** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, and the operations it opens.\n**A write scope never opens a catalogue write** (M17-04): `ticketing.write` opens carts, orders and holds for a partner or developer client, and no product, price list, price, channel capacity, lifecycle or alternative-code write, since those operations are not partner-callable and carry no `x-ticvai-api-scope`. Only a platform-staff `ApiLicence.catalogueWriteException` opens one, for one named client.\n","required":["scope","module","access"],"properties":{"scope":{"type":"string","description":"e.g. `ticketing.read`."},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"access":{"type":"string","enum":["read","write"]},"description":{"type":"string"},"operations":{"type":"array","items":{"type":"object","properties":{"contract":{"type":"string"},"operationId":{"type":"string"}}}},"licensed":{"type":"boolean","description":"Whether the caller's tenant licenses the module (`ApiLicence.licensedModules`)."}}},
"ApiUsageSummary": {"type":"object","description":"13.1.16 to 13.1.20, 13.1.41 to 13.1.45. **One endpoint because they are one question asked five ways.**\n","properties":{"totalCalls":{"type":"integer"},"successRate":{"type":"number"},"clientErrorRate":{"type":"number","description":"**4xx — the integrator's problem.** Separated because a single error rate lets both sides blame the other.\n"},"serverErrorRate":{"type":"number","description":"5xx — TICVAI's problem."},"p50LatencyMs":{"type":"number"},"p95LatencyMs":{"type":"number"},"p99LatencyMs":{"type":"number"},"quotaBreaches":{"type":"integer"},"byOperation":{"type":"array","items":{"type":"object","properties":{"operationId":{"type":"string"},"calls":{"type":"integer"},"errorRate":{"type":"number"}}}}}},
"ApiVersion": {"type":"object","x-ticvai-persistence":"control.api_version","description":"13.1.31 to 13.1.35, ADR-0026. **CF-141 is sharper under D1**: a single supported production version was tenable when only Softlabs called the API, and **with third parties a breaking change with no window breaks somebody else's business.**\n","required":["version","status"],"properties":{"version":{"type":"string"},"status":{"type":"string","enum":["preview","current","deprecated","sunset"]},"releasedAt":{"type":"string","format":"date-time"},"deprecatedAt":{"type":"string","format":"date-time","nullable":true},"sunsetAt":{"type":"string","format":"date-time","nullable":true},"minimumNoticeMonths":{"type":"integer","default":12,"description":"**The commitment, not the intention.** A deprecation policy without a stated minimum is a policy that shortens under pressure.\n"},"migrationGuideUrl":{"type":"string","nullable":true},"activeClientCount":{"type":"integer","readOnly":true},"changes":{"type":"array","description":"**The developer changelog for this version** (17 September minutes, M17-14): every operation added, changed, deprecated or removed, and whether the change is breaking under ADR-0026. Generated at release from the contract diff; shown on DEV-001.\n","items":{"type":"object","required":["operationId","kind"],"properties":{"operationId":{"type":"string"},"contract":{"type":"string"},"kind":{"type":"string","enum":["added","changed","deprecated","removed"]},"breaking":{"type":"boolean","default":false},"summary":{"type":"string"}}}}}},
"DeveloperAccount": {"type":"object","x-ticvai-persistence":"control.developer_account","description":"13.1.6 to 13.1.9. **An organisation, because an integration outlives the engineer who built it.** A credential tied to somebody's personal account dies when they leave.\n**Not a tenant and not a partner.** A partner resells tickets; a developer writes software, and one organisation may be both.\n","required":["id","organisationName","contactEmail","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"organisationName":{"type":"string"},"contactEmail":{"type":"string","format":"email"},"websiteUrl":{"type":"string","nullable":true},"countryCode":{"type":"string"},"partnerId":{"type":"string","format":"uuid","nullable":true,"description":"Where this developer is also a commercial partner. **The link exists and the two are not the same record**, which is what CF-135a was about.\n"},"status":{"type":"string","enum":["pending","verified","suspended","closed"],"readOnly":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"IntegrationListing": {"type":"object","x-ticvai-persistence":"control.integration_listing","description":"13.1.50, decision D1. **A listing, not an installation.** The integration runs on the developer's own infrastructure.\n**Third-party code does not execute inside TICVAI** — stated rather than assumed, because that is a different product with a different threat model.\n","required":["id","developerId","name","category","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid"},"name":{"type":"string"},"category":{"type":"string","enum":["crm","marketing","accounting","hotel","transport","analytics","accessibility","other"]},"description":{"type":"string"},"integrationUrl":{"type":"string"},"requiredScopes":{"type":"array","items":{"type":"string"}},"status":{"type":"string","enum":["draft","submitted","inReview","certified","rejected","revoked","delisted"],"readOnly":true},"certifiedUntil":{"type":"string","format":"date","nullable":true,"readOnly":true,"description":"**Certification expires.** An integration certified against v1 and still listed after v3 is TICVAI vouching for something it has not looked at in two years.\n"},"certifiedAgainstVersion":{"type":"string","nullable":true,"readOnly":true},"listingFeeModel":{"type":"string","enum":["none","flat","revenueShare"],"nullable":true},"visibility":{"type":"string","enum":["public","private"],"default":"public","description":"`private`: certified for production access and never shown in the marketplace (17 September minutes, M17-06). `public`: also listed once certified.\n"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProductionAccessRequest": {"type":"object","x-ticvai-persistence":"control.production_access_request","description":"**A developer's request for production keys** (17 September minutes, M17-06): sandbox, then certification, then production.\n","required":["id","developerId","sandboxClientId","listingId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid","readOnly":true},"sandboxClientId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"control.api_client"},"listingId":{"type":"string","format":"uuid","x-ticvai-references":"control.integration_listing"},"scopes":{"type":"array","items":{"type":"string"}},"allowedTenantIds":{"type":"array","items":{"type":"string","format":"uuid"}},"ipAllowList":{"type":"array","items":{"type":"string"}},"note":{"type":"string","nullable":true},"status":{"type":"string","enum":["pending","approved","rejected","withdrawn"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"reason":{"type":"string","nullable":true,"readOnly":true},"productionClientId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"control.api_client"},"requestedAt":{"type":"string","format":"date-time","readOnly":true}}},
"Sandbox": {"type":"object","x-ticvai-persistence":"control.sandbox","description":"D2 and D3. **One shared TICVAI sandbox, synthetic data only.**\n","required":["id","name","status","dataProfile"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"developerId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["provisioning","active","resetting","expired","deleted"],"readOnly":true},"dataProfile":{"$ref":"#/components/schemas/SyntheticDataProfile"},"containsProductionData":{"type":"boolean","default":false,"readOnly":true,"description":"**Always false, and stated rather than assumed** (D2). No cloning, no masking. It is a field so that a future reversal is a visible change rather than a silent one — and because **the whole PDPL and DESC argument for this contract rests on it.**\n"},"expiresAt":{"type":"string","format":"date-time","readOnly":true},"lastResetAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"SyntheticDataProfile": {"type":"object","description":"13.2.5 and 13.2.13. **What the synthetic dataset contains**, so a developer can test against a shape that resembles a real venue without any of it being real.\n**Generated, not sampled.** Sampling production and calling it synthetic is masking with extra steps.\n","properties":{"venueKind":{"type":"string","enum":["themePark","waterPark","museum","theatre","stadium","arena","mixed"]},"productCount":{"type":"integer","default":200},"guestCount":{"type":"integer","default":5000},"seatMapIncluded":{"type":"boolean","default":true},"historicalMonths":{"type":"integer","default":12,"description":"**Backdated synthetic orders**, because an integration reading a reporting API against an empty venue tests nothing.\n"},"locale":{"type":"string","default":"en-AE"}}},
"WebhookDelivery": {"type":"object","x-ticvai-persistence":"control.webhook_delivery","description":"13.1.30. **The log a developer needs most**, and without it every question becomes a support ticket.\n","required":["id","subscriptionId","eventType","status"],"properties":{"id":{"type":"string","format":"uuid"},"subscriptionId":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"eventType":{"type":"string"},"status":{"type":"string","enum":["pending","delivered","failed","retrying","abandoned"]},"attemptCount":{"type":"integer"},"responseCode":{"type":"integer","nullable":true},"responseBodyExcerpt":{"type":"string","nullable":true,"description":"**Truncated, and it is what makes the log useful** — a 500 with the receiver's own error message in it answers the question without a conversation.\n"},"isReplay":{"type":"boolean","default":false},"isTest":{"type":"boolean","default":false,"description":"Sent by `testWebhookSubscription` (VM close-out, 29 September). Marked in the payload so a receiver never books it, and never counted towards `consecutiveFailures`.\n"},"deliveredAt":{"type":"string","format":"date-time","nullable":true}}},
"WebhookEventCatalogueEntry": {"type":"object","x-ticvai-persistence":"none — read from the event catalogue (events/*.yaml) shipped with the release","description":"One event a webhook may subscribe to, as the event catalogue declares it. What a receiver needs to write a handler: the name, the version in the payload, who publishes it, what it is about and when, and the payload fields.\n","required":["name","version","publisher"],"properties":{"name":{"$ref":"#/components/schemas/WebhookEventType"},"version":{"type":"integer","minimum":1},"publisher":{"type":"string","description":"The one context that publishes it."},"aggregate":{"type":"string","description":"What the event is about. Delivery is ordered within one instance of it."},"description":{"type":"string"},"emittedWhen":{"type":"string","nullable":true},"payload":{"type":"array","items":{"type":"object","required":["field","type"],"properties":{"field":{"type":"string"},"type":{"type":"string"},"required":{"type":"boolean","default":true},"notes":{"type":"string","nullable":true}}}}}},
"WebhookEventType": {"type":"string","description":"**The webhook event catalogue: every event a subscription may name** (29 September, build pass). Each value is the `name` of an event in `events/` — `aggregate.pastTenseFact`, published through `platform.outbox` by exactly one context. A name is added here in the same change that adds its event file, and never before.\n**Added 29 September**, each closing a requirement that had the webhook mechanism and nothing to subscribe to:\n| Events | Publisher | Requirement | |---|---|---| | `device.statusChanged`, `device.tamperDetected`, `device.enrolmentChanged`, `device.firmwareReleased`, `device.firmwareRolloutCompleted` | tenancy | 16.9.56 | | `accreditation.applicationDecided`, `accreditation.holderStatusChanged`, `accreditation.credentialIssued`, `accreditation.renewalDue` | accreditation | 12.1.53 | | `approval.requested`, `approval.escalated`, `approval.stepCompleted`, `approval.expired` | approvals | 11.1.64, 11.1.66 | | `seat.held`, `seat.released`, `seat.blocked`, `seatMap.published` | seating | 21.13.4 | | `consent.deviceConsentRecorded`, `consent.deviceConsentClaimed` | marketing | 2.6.65 | | `order.chargebackRecorded` | orders | 8.3.11 to 8.3.15 (a tenant's own finance or fraud tooling) | | `entitlement.expiringSoon` | access | 5.5.30 (a tenant's own CRM) | | `apiClient.anomalyDetected` | public-api | 17 September minutes M17-07 (added 30 September with its event file) |\n**Deprecated** (1 October, ADR-0067 amendment): `device.enrolmentChanged` is still offered but nothing inside the platform consumes it any more; it is removed at the next major version of this API. Subscribers are told in the release note.\n**Published and deliberately not offered** (29 September, build pass, group G2): `identity.credentialResetRequested` and `identity.loginRecorded` are security signals, and a stream of them to an outside receiver is a map of which accounts are under attack; `storefront.sessionEvent` is high-volume fraud telemetry, not a business fact a receiver acts on.\n","x-ticvai-deprecated-values":["device.enrolmentChanged"],"enum":["access.validated","accreditation.applicationDecided","accreditation.credentialIssued","accreditation.holderStatusChanged","accreditation.renewalDue","ai.ceilingApproaching","apiClient.anomalyDetected","approval.escalated","approval.expired","approval.granted","approval.rejected","approval.requested","approval.stepCompleted","assets.documentIndexed","cart.abandoned","catalogue.productPublished","consent.deviceConsentClaimed","consent.deviceConsentRecorded","conversation.handedOver","device.enrolmentChanged","device.firmwareReleased","device.firmwareRolloutCompleted","device.statusChanged","device.tamperDetected","entitlement.expiringSoon","entitlement.issued","entitlement.statusChanged","fnb.menuPublished","fnb.orderReady","inventory.purchaseOrderReceived","ledger.journalPosted","ledger.periodClosed","maintenance.assetReturnedToService","maintenance.templatePublished","maintenance.workOrderCompleted","marketing.caseClosed","order.chargebackRecorded","order.completed","order.paid","order.refunded","performance.cancelled","reporting.definitionPublished","retail.merchandisePublished","seat.blocked","seat.held","seat.released","seat.sold","seatMap.published","shift.closed","stock.depleted","tenant.suspended","whitelabel.contentPublished"]},
"WebhookSubscription": {"type":"object","x-ticvai-persistence":"control.webhook_subscription","description":"13.1.26, 13.3.18 and 13.3.22. **The 29 events already exist and nothing outside could receive one.**\n","required":["id","clientId","endpointUrl","eventTypes","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"clientId":{"type":"string","format":"uuid"},"endpointUrl":{"type":"string"},"eventTypes":{"type":"array","description":"**Filtered at subscription, not at delivery.** A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to. Each entry is a name from the webhook event catalogue (`WebhookEventType`).\n","items":{"$ref":"#/components/schemas/WebhookEventType"}},"filters":{"type":"object","nullable":true,"description":"13.3.22. Tenant, venue, or a business condition on the payload.","additionalProperties":true},"signingSecret":{"type":"string","format":"password","writeOnly":true,"description":"**How the receiver knows it was TICVAI.** Without a signature an endpoint accepts a ticket-sale event from anybody who learns the URL.\n**Write-only: accepted on create, never returned.** The same rule as `clientSecret` — a system that can show you a secret later is a system that hands it to whoever reads the subscription.\n"},"status":{"type":"string","enum":["pendingVerification","active","paused","failing","disabled"],"readOnly":true},"consecutiveFailures":{"type":"integer","readOnly":true},"disabledReason":{"type":"string","nullable":true,"readOnly":true,"description":"13.1.29. **An endpoint failing for days is disabled rather than retried forever**, and the developer is told — a queue growing against a dead endpoint is a cost the platform carries silently.\n"}}}
}
```
