# WS106 — Subscription Licensing AI Self Service board 9

**10 screens · 8 operations · 12 schemas · 4 permissions**

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
  `PLATFORM_BILLING_MANAGE, PLATFORM_BILLING_VIEW, PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
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
| `ADM-449` | Usage & License Command Center | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-450` | Entitlement & License Inventory | B | 0 | 0 | 6 | 8 | 1 | 4 | — | notStarted (—) |
| `ADM-451` | Commercial Consumption & Billable Event Metering | B | 0 | 0 | 6 | 7 | 1 | 0 | — | notStarted (—) |
| `ADM-452` | Operational Usage & Threshold Monitor | B | 0 | 0 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `ADM-453` | License Enforcement & Decision Engine | B | 0 | 16 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-454` | Minimum Guarantee & Variable Consumption Monitor | B | 0 | 4 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `ADM-455` | Overage, Capacity & Temporary Exception Management | B | 9 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-456` | Usage Alerts, Reconciliation & Exception Center | B | 5 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-457` | AI Usage Forecast & Commercial Optimization | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-458` | License, Metering & Commercial Synchronization Audit | B | 0 | 18 | 6 | 7 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-449, ADM-450, ADM-451, ADM-452, ADM-453, ADM-454, ADM-457, ADM-458 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-449` Usage & License Command Center

**Provide a real-time consolidated view of technical usage, commercial consumption and license health.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-449 |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/tenants-licensing/usage-license-command-center-adm-449` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Technical usage, commercial consumption and licence health per customer.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Data it reads**: `getEntitlementUsage` (onLoad, Usage against licence)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-450` Entitlement & License Inventory: *Entitlement & License Inventory*
- → `ADM-451` Commercial Consumption & Billable Event Metering: *Commercial Consumption & Billable Event Metering*
- → `ADM-452` Operational Usage & Threshold Monitor: *Operational Usage & Threshold Monitor*
- → `ADM-453` License Enforcement & Decision Engine: *License Enforcement & Decision Engine*
- → `ADM-454` Minimum Guarantee & Variable Consumption Monitor: *Minimum Guarantee & Variable Consumption Monitor*
- → `ADM-455` Overage, Capacity & Temporary Exception Management: *Overage, Capacity & Temporary Exception Management*
- → `ADM-456` Usage Alerts, Reconciliation & Exception Center: *Usage Alerts, Reconciliation & Exception Center*
- → `ADM-457` AI Usage Forecast & Commercial Optimization: *AI Usage Forecast & Commercial Optimization*
- → `ADM-458` License, Metering & Commercial Synchronization Audit: *License, Metering & Commercial Synchronization Audit*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The usage license list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the usage license untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No usage license yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the usage license are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
customer: Marina Leisure Group
posTerminals: 41 of 50
ticketsThisMonth: 412,880 of 500,000
aiTokens: 120%
```

#### Permissions

- `getEntitlementUsage` → `PLATFORM_TENANT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Usage tracking shows tickets sold, licence inventory consumption (e.g. 8 of 10 licensed POS terminals in use) and overage, signalling a possible tier upgrade or extra charges. *(client request · MoM 10 Sep 2026, 4.15 Usage & Commercial Consumption Tracking · DI-836)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-449` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-449`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 9
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 1: Opens Usage & License Command Center → Provide a real-time consolidated view of technical usage, commercial consumption and license health.
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F215 branch at step 1 (expected): when Nothing has been set up on Usage & License Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F215 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-449?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-450`, `ADM-451`, `ADM-452`, `ADM-453`, `ADM-454`, `ADM-455`, `ADM-456`, `ADM-457`, `ADM-458`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-450` Entitlement & License Inventory

**Show exactly what the customer is technically entitled to use independently of the commercial charging model.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-450 |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/tenants-licensing/entitlement-license-inventory-adm-450` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** What a customer is technically entitled to, independent of how they are charged.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Data it reads**: `getTenantLicences` (onLoad, Entitlement inventory)

**Where the user goes next**

- → `ADM-449` Usage & License Command Center: *Back to Usage & License Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The entitlement license inventory list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the entitlement license inventory untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No entitlement license inventory yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the entitlement license inventory are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entitlements:
- module: ticketing
  limit: 500,000 tickets/month
- module: pos
  limit: 50 terminals
```

#### Permissions

- `getTenantLicences` → `PLATFORM_TENANT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Usage tracking shows tickets sold, licence inventory consumption (e.g. 8 of 10 licensed POS terminals in use) and overage, signalling a possible tier upgrade or extra charges. *(client request · MoM 10 Sep 2026, 4.15 Usage & Commercial Consumption Tracking · DI-836)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-450` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-450`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 9
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 2: Works in Entitlement & License Inventory → Show exactly what the customer is technically entitled to use independently of the commercial charging model.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-450?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-449`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-451` Commercial Consumption & Billable Event Metering

**This is the major new Board 9 screen. Meter the events that determine the customer's variable commercial charges.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-451 |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/tenants-licensing/commercial-consumption-billable-event-metering-adm-451` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The billable events that drive variable charges, metered per period.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Period start | date picker | — | — | `getUsageMetering` ?periodStart |
| Period end | date picker | — | — | `getUsageMetering` ?periodEnd |
| Metric | select | — | Venues · Workstations · Active users · Devices · Branded apps · AI tokens · API calls · Storage gb · Transactions · Guest profiles | `getUsageMetering` ?metric |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Data it reads**: `getUsageMetering` (onLoad, Billable event metering)

**Where the user goes next**

- → `ADM-449` Usage & License Command Center: *Back to Usage & License Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial consumption billable list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial consumption billable untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial consumption billable yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial consumption billable are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
billableEvents:
- event: Ticket issued
  september: 412,880
- event: Paid transaction
  september: 96,210
```

#### Permissions

- `getUsageMetering` → `PLATFORM_TENANT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.6.1 | User Usage Monitoring - System shall monitor active user consumption. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.2 | POS Usage Monitoring - System shall monitor POS utilization. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.3 | API Usage Monitoring - System shall monitor API consumption. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.4 | Storage Usage Monitoring - System shall monitor storage consumption. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.5 | Transaction Usage Monitoring - System shall monitor transaction volumes. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.6 | Attendance Usage Monitoring - System shall monitor attendance volumes. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.7 | Usage Dashboards - System shall provide usage dashboards. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Usage tracking shows tickets sold, licence inventory consumption (e.g. 8 of 10 licensed POS terminals in use) and overage, signalling a possible tier upgrade or extra charges. *(client request · MoM 10 Sep 2026, 4.15 Usage & Commercial Consumption Tracking · DI-836)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-451` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-451`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 9
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 4: Works in Commercial Consumption & Billable Event Metering → This is the major new Board 9 screen. Meter the events that determine the customer's variable commercial charges.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-451?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-449`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-452` Operational Usage & Threshold Monitor

**Monitor technical and operational consumption against licensed capacity.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-452 |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/operational-usage-threshold-monitor-adm-452` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Operational consumption against licensed capacity, with approaching, at and over limit states.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Thresholds**: Three states with three responses (warn, require an overage pack, refuse); hard stop off by default. *(source: contracts/satellite/subscription.yaml#getLicenceEnforcement)*

**Data it reads**: `getLicenceEnforcement` (onLoad, Thresholds and position)

**Where the user goes next**

- → `ADM-449` Usage & License Command Center: *Back to Usage & License Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operational usage threshold list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operational usage threshold untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operational usage threshold yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operational usage threshold are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
resource: POS terminals
used: 48
licensed: 50
state: approaching (96%)
```

#### Permissions

- `getLicenceEnforcement` → `PLATFORM_BILLING_VIEW` (read) · staff
- `getPlanRecommendations` → `PLATFORM_BILLING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.3 | AI Usage Forecasting - System shall forecast future platform consumption. | Subscription & Licensing Management | CONTRACTED | `getLicenceEnforcement` |
| 20.8.4 | AI Upgrade Recommendations - System shall recommend subscription upgrades. | Subscription & Licensing Management | CONTRACTED | `getPlanRecommendations` |
| 20.8.5 | AI Cost Optimization - System shall recommend cost optimization opportunities. | Subscription & Licensing Management | CONTRACTED | `getPlanRecommendations` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A configurable warning threshold (e.g. 80% of an included allowance) notifies both the customer and TICVAI before the client exceeds included usage. *(client request · MoM 10 Sep 2026, 4.3 Subscription Tiers, Allowances & Usage Thresholds · DI-820)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-452` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-452`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 9
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 6: Works in Operational Usage & Threshold Monitor → Monitor technical and operational consumption against licensed capacity.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-452?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-449`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-453` License Enforcement & Decision Engine

**Apply the correct technical enforcement behavior when licensed resources reach or exceed limits.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-453 |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/license-enforcement-decision-engine-adm-453` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** What happens when a limit is reached: per resource the rule, decision, reason, whether an override is allowed and which approval it needs. Refusing service to a paying customer is a commercial decision.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 8 labels bound). (CHG-SBO-005)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Hard stop**: Off by default; turning it on requires a reason and states which customers it would affect now. *(source: contracts/satellite/subscription.yaml#getLicenceEnforcement)*
- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setLicenceEnforcementPolicy: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/subscription.yaml#setLicenceEnforcementPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Every license enforcement decision** (data table)

| Shows | Format | Notes |
|---|---|---|
| Requested action | text | not in the schema: `Requested Action` |
| Current entitlement | text | not in the schema: `Current Entitlement` |
| Current consumption | text | not in the schema: `Current Consumption` |
| Rule | text | not in the schema: `Rule` |
| Decision | text | not in the schema: `Decision` |
| Reason | text | not in the schema: `Reason` |
| Override allowed | text | not in the schema: `Override Allowed` |
| Required approval | text | not in the schema: `Required Approval` |

**The selected license enforcement decision** (detail panel): The pack groups this record's detail under its own headings: “Overage”, “Approval”, “Transactions Soft / Overage”, “Modules Hard”.

| Shows | Format | Notes |
|---|---|---|
| Requested action | text | not in the schema: `Requested Action` |
| Current entitlement | text | not in the schema: `Current Entitlement` |
| Current consumption | text | not in the schema: `Current Consumption` |
| Rule | text | not in the schema: `Rule` |
| Decision | text | not in the schema: `Decision` |
| Reason | text | not in the schema: `Reason` |
| Override allowed | text | not in the schema: `Override Allowed` |
| Required approval | text | not in the schema: `Required Approval` |

**Where the user goes next**

- → `ADM-449` Usage & License Command Center: *Back to Usage & License Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The license enforcement decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the license enforcement decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No license enforcement decision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the license enforcement decision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every license enforcement decision:
- Requested Action: 128
  Current Entitlement: 74
  Current Consumption: 74
  Rule: 19
  Decision: 128
  Reason: 57
  Override Allowed: 128
  Required Approval: 46
- Requested Action: 46
  Current Entitlement: 19
  Current Consumption: 19
  Rule: 233
  Decision: 46
  Reason: 11
  Override Allowed: 46
  Required Approval: 312
- Requested Action: 312
  Current Entitlement: 233
  Current Consumption: 233
  Rule: 57
  Decision: 312
  Reason: 128
  Override Allowed: 312
  Required Approval: 74
```

#### Permissions

- `setLicenceEnforcementPolicy` → `PLATFORM_PLAN_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-453` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-453`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 9
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 8: Works in License Enforcement & Decision Engine → Apply the correct technical enforcement behavior when licensed resources reach or exceed limits.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-453?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-449`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-454` Minimum Guarantee & Variable Consumption Monitor

**Track the commercial consumption position against contractual minimum guarantees. This screen does not issue the invoice. It provides Board 10 with the reconciled consumption basis.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-454 |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Forecast) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/minimum-guarantee-variable-consumption-monitor-adm-454` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Consumption against the contractual minimum guarantee; it feeds billing but issues no invoice.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 2 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Column labels contain values ("Projected month-end billable tickets - 43,800"). (CHG-SBO-015); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every minimum guarantee variable** (data table)

| Shows | Format | Notes |
|---|---|---|
| Projected month end billable tickets | text | not in the schema: `Projected month-end billable tickets` |
| Projected variable billing basis: AED 32,850 | text | not in the schema: `Projected variable billing basis: AED 32,850` |

**The selected minimum guarantee variable** (detail panel): The pack groups this record's detail under its own headings: “Rate”, “Billable Tickets”, “Current Position”, “Automatically calculate”, “Progress Visualization”, “Where applicable show”.

| Shows | Format | Notes |
|---|---|---|
| Projected month end billable tickets | text | not in the schema: `Projected month-end billable tickets` |
| Projected variable billing basis: AED 32,850 | text | not in the schema: `Projected variable billing basis: AED 32,850` |

**Data it reads**: `getLicenceEnforcement` (onLoad, Minimum guarantee and variable consumption)

**Where the user goes next**

- → `ADM-449` Usage & License Command Center: *Back to Usage & License Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The minimum guarantee variable list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the minimum guarantee variable untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No minimum guarantee variable yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the minimum guarantee variable are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every minimum guarantee variable:
- 'Projected month-end billable tickets: 43,800': 19
  'Projected variable billing basis: AED 32,850': AED 12,400.00
- 'Projected month-end billable tickets: 43,800': 233
  'Projected variable billing basis: AED 32,850': AED 482,300.00
- 'Projected month-end billable tickets: 43,800': 57
  'Projected variable billing basis: AED 32,850': AED 96,750.00
```

#### Permissions

- `getLicenceEnforcement` → `PLATFORM_BILLING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.3 | AI Usage Forecasting - System shall forecast future platform consumption. | Subscription & Licensing Management | CONTRACTED | `getLicenceEnforcement` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Per-customer billing view shows minimum billable volume (month-to-date) and variable/overage revenue; a customer profile consolidates all commercial and licensing information per client. *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-839)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-454` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-454`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 9
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 10: Works in Minimum Guarantee & Variable Consumption Monitor → Track the commercial consumption position against contractual minimum guarantees. This screen does not issue the invoice. It provides Board 10 with the reconciled consumption basis.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-454?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-449`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-455` Overage, Capacity & Temporary Exception Management

**Manage technical capacity above standard entitlement and temporary operational requirements.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-455 |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Fields) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/overage-capacity-temporary-exception-management-adm-455` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Temporary capacity above entitlement for a venue, with commercial treatment and approval.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Resource | select field | — | — | — | — | — | — |
| Quantity | select field | — | — | — | — | — | — |
| Start | select field | — | — | — | — | — | — |
| Expiry | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Requested By | select field | — | — | — | — | — | — |
| Commercial Treatment | select field | — | — | — | — | — | — |
| Approval | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-449` Usage & License Command Center: *Back to Usage & License Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The overage capacity temporary configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the overage capacity temporary untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No overage capacity temporary configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Resource: 128
  Quantity: 46
  Start: 11
  Expiry: 46
  Venue: AquaCove Dubai
  Reason: 74
  Requested By: Rahul Menon
  Commercial Treatment: 74
  Approval: 128
```

#### Permissions

- `addCapacityPack` → `PLATFORM_BILLING_MANAGE` (configure) · staff, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Usage tracking shows tickets sold, licence inventory consumption (e.g. 8 of 10 licensed POS terminals in use) and overage, signalling a possible tier upgrade or extra charges. *(client request · MoM 10 Sep 2026, 4.15 Usage & Commercial Consumption Tracking · DI-836)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-455` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-455`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 9
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 12: Works in Overage, Capacity & Temporary Exception Management → Manage technical capacity above standard entitlement and temporary operational requirements.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-455?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-449`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-456` Usage Alerts, Reconciliation & Exception Center

**Provide a central operational center for consumption alerts and commercial metering exceptions.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-456 |
| Who uses it | ticvai staff holding `PLATFORM_BILLING_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure recipients) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/usage-alerts-reconciliation-exception-center-adm-456` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Consumption alerts and metering exceptions, routed to the customer admin, commercial, finance, operations or support.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Customer Admin | select field | — | — | — | — | — | — |
| TICVAI Commercial | select field | — | — | — | — | — | — |
| Finance | select field | — | — | — | — | — | — |
| Operations | select field | — | — | — | — | — | — |
| Technical Support | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Period | text field | — | — | `getBillingReconciliation` ?period |

#### Outputs: what the screen shows and produces

**Data it reads**: `getBillingReconciliation` (onLoad, Alerts and reconciliation)

**Where the user goes next**

- → `ADM-449` Usage & License Command Center: *Back to Usage & License Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The usage alerts reconciliation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the usage alerts reconciliation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No usage alerts reconciliation configured yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Customer Admin: Marina Leisure Group
  TICVAI Commercial: 312
  Finance: 46
  Operations: 233
  Technical Support: 233
```

#### Permissions

- `getBillingReconciliation` → `PLATFORM_BILLING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A configurable warning threshold (e.g. 80% of an included allowance) notifies both the customer and TICVAI before the client exceeds included usage. *(client request · MoM 10 Sep 2026, 4.3 Subscription Tiers, Allowances & Usage Thresholds · DI-820)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-456` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-456`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 9
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 14: Works in Usage Alerts, Reconciliation & Exception Center → Provide a central operational center for consumption alerts and commercial metering exceptions.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-456?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-449`.
- [ ] Every gated control is gated: `PLATFORM_BILLING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-457` AI Usage Forecast & Commercial Optimization

**Use AI to forecast operational and commercial consumption and recommend appropriate action.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-457 |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/tenants-licensing/ai-usage-forecast-commercial-optimization-adm-457` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** AI forecast of consumption with recommended actions.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Data it reads**: `getEntitlementUsage` (onLoad, Consumption trend)

**Where the user goes next**

- → `ADM-449` Usage & License Command Center: *Back to Usage & License Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The usage forecast commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the usage forecast commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No usage forecast commercial yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the usage forecast commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
forecast: Tickets exceed allowance on 24/10/2026
recommendation: Offer capacity pack of 100,000 tickets
```

#### Permissions

- `getEntitlementUsage` → `PLATFORM_TENANT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-457` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-457`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 9
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 16: Works in AI Usage Forecast & Commercial Optimization → Use AI to forecast operational and commercial consumption and recommend appropriate action.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-457?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-449`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-458` License, Metering & Commercial Synchronization Audit

**Ensure that the approved contract, subscription, license and actual metering configuration remain synchronized.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-458 |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/tenants-licensing/license-metering-commercial-synchronization-audit-adm-458` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Contract, subscription, licence and metering versions kept in sync, with every change and who approved it.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 9 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Period start | date picker | — | — | `getUsageMetering` ?periodStart |
| Period end | date picker | — | — | `getUsageMetering` ?periodEnd |
| Metric | select | — | Venues · Workstations · Active users · Devices · Branded apps · AI tokens · API calls · Storage gb · Transactions · Guest profiles | `getUsageMetering` ?metric |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every license metering commercial** (data table)

| Shows | Format | Notes |
|---|---|---|
| Contract version | text | not in the schema: `Contract Version` |
| License version | text | not in the schema: `License Version` |
| Metering rule version | text | not in the schema: `Metering Rule Version` |
| Previous value | text | not in the schema: `Previous Value` |
| New value | text | not in the schema: `New Value` |
| Changed by | text | not in the schema: `Changed By` |
| Approved by | text | not in the schema: `Approved By` |
| Timestamp | text | not in the schema: `Timestamp` |
| Effective date | text | not in the schema: `Effective Date` |

**The selected license metering commercial** (detail panel): The pack groups this record's detail under its own headings: “Approved Commercial Package”, “Contract”, “All Tickets Issued”, “Critical Board 9 Data Separation”, “Suppose during September”, “Contract says”.

| Shows | Format | Notes |
|---|---|---|
| Contract version | text | not in the schema: `Contract Version` |
| License version | text | not in the schema: `License Version` |
| Metering rule version | text | not in the schema: `Metering Rule Version` |
| Previous value | text | not in the schema: `Previous Value` |
| New value | text | not in the schema: `New Value` |
| Changed by | text | not in the schema: `Changed By` |
| Approved by | text | not in the schema: `Approved By` |
| Timestamp | text | not in the schema: `Timestamp` |
| Effective date | text | not in the schema: `Effective Date` |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (New Value, Previous Value)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `getUsageMetering` (onLoad, Metering audit)

**Where the user goes next**

- → `ADM-449` Usage & License Command Center: *Back to Usage & License Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The license metering commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the license metering commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No license metering commercial yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the license metering commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every license metering commercial:
- Contract Version: 128
  License Version: 11
  Metering Rule Version: 233
  Previous Value: AED 12,400.00
  New Value: AED 482,300.00
  Changed By: 312
  Approved By: Rahul Menon
  Timestamp: 3 h 20 min
- Contract Version: 46
  License Version: 128
  Metering Rule Version: 57
  Previous Value: AED 482,300.00
  New Value: AED 96,750.00
  Changed By: 74
  Approved By: Fatima Al Mansoori
  Timestamp: 42 min
- Contract Version: 312
  License Version: 46
  Metering Rule Version: 11
  Previous Value: AED 96,750.00
  New Value: AED 12,400.00
  Changed By: 19
  Approved By: Omar Haddad
  Timestamp: 1.8 s
```

#### Permissions

- `getUsageMetering` → `PLATFORM_TENANT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.6.1 | User Usage Monitoring - System shall monitor active user consumption. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.2 | POS Usage Monitoring - System shall monitor POS utilization. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.3 | API Usage Monitoring - System shall monitor API consumption. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.4 | Storage Usage Monitoring - System shall monitor storage consumption. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.5 | Transaction Usage Monitoring - System shall monitor transaction volumes. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.6 | Attendance Usage Monitoring - System shall monitor attendance volumes. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |
| 20.6.7 | Usage Dashboards - System shall provide usage dashboards. | Subscription & Licensing Management | CONTRACTED | `getUsageMetering` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-458` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS161 Subscription Licensing AI Self Service Board 9.dc.html#adm-458`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 9
- Flow F215 *Subscription Licensing AI Self Service board 9: Usage & License Command Center*, step 18: Works in License, Metering & Commercial Synchronization Audit → Ensure that the approved contract, subscription, license and actual metering configuration remain synchronized.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-458?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-449`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
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
"addCapacityPack": {"method":"POST","path":"/capacity-packs","contract":"subscription","summary":"Buy headroom without changing tier","permission":"PLATFORM_BILLING_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CapacityPack","responds":"CapacityPack"},
"getBillingReconciliation": {"method":"GET","path":"/billing-reconciliation","contract":"subscription","summary":"Metered consumption against what was invoiced","permission":"PLATFORM_BILLING_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":"tenantId","in":"query","required":true},{"name":"period","in":"query","required":true}],"requestBody":null,"responds":"BillingReconciliation"},
"getEntitlementUsage": {"method":"GET","path":"/tenants/{tenantId}/entitlement-usage","contract":"subscription","summary":"Usage against licensed limits","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"EntitlementUsage"},
"getLicenceEnforcement": {"method":"GET","path":"/licence-enforcement","contract":"subscription","summary":"Where a tenant stands against its entitlements, and what happens next","permission":"PLATFORM_BILLING_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":"tenantId","in":"query","required":true}],"requestBody":null,"responds":"LicenceEnforcement"},
"getPlanRecommendations": {"method":"GET","path":"/plan-recommendations","contract":"subscription","summary":"Which plan, module or pack would fit this tenant better, and what it would cost or save","permission":"PLATFORM_BILLING_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":"tenantId","in":"query","required":true},{"name":"horizonMonths","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getTenantLicences": {"method":"GET","path":"/tenants/{tenantId}/licences","contract":"subscription","summary":"What a tenant is licensed to use","permission":"PLATFORM_TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"LicencePosition"},
"getUsageMetering": {"method":"GET","path":"/tenants/{tenantId}/usage","contract":"subscription","summary":"Metered usage for a period","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"periodStart","in":"query","required":true},{"name":"periodEnd","in":"query","required":true},{"name":"metric","in":"query","required":null}],"requestBody":null,"responds":"UsageReport"},
"setLicenceEnforcementPolicy": {"method":"PUT","path":"/licence-enforcement","contract":"subscription","summary":"What happens at each threshold","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LicenceEnforcementPolicy","responds":"LicenceEnforcementPolicy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"BillingReconciliation": {"type":"object","description":"Boards 10.2 and 10.3. **The first invoice sets the tone for the relationship.**","properties":{"tenantId":{"type":"string","format":"uuid"},"period":{"type":"string"},"lines":{"type":"array","items":{"type":"object","properties":{"unit":{"type":"string"},"meteredQuantity":{"type":"integer"},"billedQuantity":{"type":"integer"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"type":"integer"}}}},"meteredNotBilled":{"type":"integer"},"billedNotMetered":{"type":"integer"},"invoiceId":{"type":"string","format":"uuid","nullable":true},"approvedBy":{"type":"string","format":"uuid","nullable":true}}},
"CapacityPack": {"type":"object","x-ticvai-persistence":"subscription.capacity_pack","description":"Board 3.8. **A good season should not require renegotiating a contract in August.**\n","required":["tenantId","unit","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"unit":{"type":"string"},"quantity":{"type":"integer"},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"validFrom":{"type":"string","format":"date"},"validTo":{"type":"string","format":"date","nullable":true},"temporary":{"type":"boolean","default":true},"approvedBy":{"type":"string","format":"uuid","nullable":true},"invoiceId":{"type":"string","format":"uuid","nullable":true}}},
"EntitlementLimit": {"type":"object","required":["metric","limit"],"properties":{"metric":{"$ref":"#/components/schemas/UsageMetric"},"limit":{"type":"integer","nullable":true,"x-ticvai-column":"limit_value","description":"Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure `limit_value`."},"overageAllowed":{"type":"boolean","default":false},"overageUnitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"EntitlementUsage": {"x-ticvai-persistence":"none — aggregated from usage_record","type":"object","required":["tenantId","metrics"],"properties":{"tenantId":{"type":"string","format":"uuid"},"metrics":{"type":"array","items":{"type":"object","required":["metric","current","isNearLimit"],"properties":{"metric":{"$ref":"#/components/schemas/UsageMetric"},"current":{"type":"integer"},"limit":{"type":"integer","nullable":true},"percentUsed":{"type":"number","nullable":true},"isNearLimit":{"type":"boolean","description":"Approaching a limit is an account conversation. Hitting one silently at a gate is an incident.\n"},"isExceeded":{"type":"boolean"}}}},"asAt":{"type":"string","format":"date-time"}}},
"LicenceEnforcement": {"type":"object","description":"Board 9.5. **Three states, three responses.**","properties":{"tenantId":{"type":"string","format":"uuid"},"period":{"type":"string"},"units":{"type":"array","items":{"type":"object","properties":{"unit":{"type":"string"},"allowance":{"type":"integer"},"consumed":{"type":"integer"},"percentUsed":{"type":"number"},"projectedAtPeriodEnd":{"type":"integer","nullable":true},"state":{"type":"string","enum":["withinAllowance","approaching","atLimit","overage"]},"nextAction":{"type":"string","nullable":true},"overageCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"minimumGuaranteeMet":{"type":"boolean"},"alertsRaised":{"type":"integer"}}},
"LicenceEnforcementPolicy": {"type":"object","x-ticvai-persistence":"subscription.enforcement_policy","description":"Board 9.5. **Refusing service to a paying customer mid-season is a commercial decision.**\n","properties":{"id":{"type":"string","format":"uuid"},"thresholds":{"type":"array","items":{"type":"object","properties":{"atPercentOfAllowance":{"type":"integer"},"action":{"type":"string","enum":["notify","notifyAccountManager","requireCapacityPack","autoAddCapacityPack","restrictNewConfiguration","hardStop"]},"notifyRoles":{"type":"array","items":{"type":"string"}}}}},"hardStopAllowed":{"type":"boolean","default":false,"description":"**Off by default, and every enforcement action is alerted.**"},"graceDays":{"type":"integer","default":7}}},
"LicencePosition": {"x-ticvai-persistence":"none — union of the tenant's plan (control.tenant.plan_id -> subscription.plan_module, subscription.plan_limit) and its add-ons (control.licence_add_on, control.licence_add_on_limit by tenant_id)","type":"object","required":["tenantId","licensedModules","limits"],"properties":{"poweredByRemovable":{"type":"boolean","readOnly":true,"default":false,"description":"**Whether the tenant's licence lets it switch \"Powered by TICVAI\" off** (Chinmay, 2 October, workbook Q160 and the pre-apply round; CHG-CSA-036). False by default; true where TICVAI sold the tenant the add-on keyed `poweredByRemoval` (`addLicenceAddOn`). White label's `setBrandIdentity` refuses `showPoweredBy` false while this is false."},"tenantId":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid","nullable":true},"licensedModules":{"type":"array","description":"Union of plan modules and add-ons. The White Label Builder reads this and cannot enable anything absent from it.\n","items":{"type":"object","required":["moduleKey","source"],"properties":{"moduleKey":{"type":"string"},"displayName":{"type":"string"},"source":{"type":"string","enum":["plan","addOn"]},"validTo":{"type":"string","format":"date","nullable":true}}}},"limits":{"type":"array","items":{"$ref":"#/components/schemas/EntitlementLimit"}}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"SubscriptionPlanRecommendation": {"type":"object","x-ticvai-persistence":"none — computed from control.usage_record, the plan, tier and add-on limits and capacity packs, priced as simulateCommercialPackage prices","description":"One plan-fit move for a tenant, priced against staying as it is (20.8.4, 20.8.5; decided 29 September, build pass, group G2).","required":["kind","reason","projectedMonthlyCost"],"properties":{"kind":{"type":"string","enum":["upgrade","downgrade","addModule","removeModule","removeAddOn","capacityPack"]},"targetPlanId":{"type":"string","format":"uuid","nullable":true,"description":"The tier to move to, for `upgrade` and `downgrade`."},"moduleCode":{"type":"string","nullable":true,"description":"For `addModule` and `removeModule`."},"addOnCode":{"type":"string","nullable":true,"description":"For `removeAddOn`."},"billableUnit":{"type":"string","nullable":true,"description":"The unit that drives it (for `upgrade`, `downgrade` and `capacityPack`), as `getLicenceEnforcement` names it."},"capacityPackSize":{"type":"integer","nullable":true,"description":"For `capacityPack`, the pack size that covers the projected overage."},"projectedMonthlyCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"projectedSaving":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Against staying as it is over the horizon, monthly. Set where the move saves money."},"projectedAddedCost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Where the move costs more than today but less than the alternative named in `comparedWith`."},"comparedWith":{"type":"string","enum":["currentPackage","projectedOverage","nextTier","capacityPack"],"description":"What the move is cheaper than. An `upgrade` is compared with paying the projected overage; a `capacityPack` with the next tier."},"reason":{"type":"string","maxLength":500,"description":"One sentence a person can repeat to the customer."},"basis":{"type":"object","description":"The numbers it rests on.","properties":{"usageWindowDays":{"type":"integer"},"usedAverage":{"type":"number","nullable":true},"usedPeak":{"type":"number","nullable":true},"projectedPeak":{"type":"number","nullable":true},"currentLimit":{"type":"number","nullable":true},"targetLimit":{"type":"number","nullable":true},"lastUsedAt":{"type":"string","format":"date-time","nullable":true,"description":"For `removeModule` and `removeAddOn`, the last metered use; null for never."}}},"applyWith":{"type":"string","enum":["setSubscription","addCapacityPack"],"description":"The operation a person uses to carry it out (after `previewSubscriptionChange` for `setSubscription`)."}}},
"UsageMetric": {"type":"string","enum":["venues","workstations","activeUsers","devices","brandedApps","aiTokens","apiCalls","storageGb","transactions","guestProfiles"]},
"UsageReport": {"x-ticvai-persistence":"none — aggregated","type":"object","required":["tenantId","periodStart","periodEnd","metrics"],"properties":{"tenantId":{"type":"string","format":"uuid"},"periodStart":{"type":"string","format":"date"},"periodEnd":{"type":"string","format":"date"},"metrics":{"type":"array","items":{"type":"object","properties":{"metric":{"$ref":"#/components/schemas/UsageMetric"},"total":{"type":"number"},"included":{"type":"number","nullable":true},"overage":{"type":"number"},"byVenue":{"type":"array","items":{"type":"object","properties":{"venueId":{"type":"string","format":"uuid"},"quantity":{"type":"number"}}}},"byCapability":{"type":"array","description":"AI tokens only.","items":{"type":"object","properties":{"capability":{"type":"string"},"quantity":{"type":"number"}}}}}}}}}
}
```
