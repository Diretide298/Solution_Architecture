# P09-support-communications-01 — P09 · Support & Communications

**2 screens · 2 operations · 1 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `PLATFORM_RELEASE_MANAGE, PLATFORM_RELEASE_VIEW`. A control nobody can use must say so,
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
| `ADM-035` | Support & Escalation Console | B | 7 | 10 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-036` | Platform Notification Broadcast | B | 7 | 14 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-035` Support & Escalation Console

**Work the support escalations that reach TICVAI, and tell tenants what is known.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Support & Communications · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-035 |
| Who uses it | ticvai staff holding `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSupportNotices` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/general/support-and-escalation-console` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-024): No operation lists or works the support escalations that reach TICVAI. Open: No contract — overlaps P12

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** TICVAI support: notices and escalations raised to platform support.

**Fixed on main** (the package already carries these; draw what it says): Purpose "Answer a question without needing a person"; operations are support notices only. (CHG-WIR-023); formPublishSupportNotice asks the person for publishedAt, id. (CHG-SBO-004); Tables show every schema field, plumbing included: 'Every support notice' drop id, affectedTenantIds, publishedByPrincipalId, scopePath. (CHG-SBO-004); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

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
|  (publish gate) | navigation or local | — | — | — | — |
| Publish support notice (primary button) | `publishSupportNotice` POST `/support-notices` | SupportNotice | SupportNotice | — | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Publish support notice**: Separate from Save. The publish gate names what goes live, where and from when before it happens; blocked names what is wrong and how to fix it; an override past a warning is recorded with who authorised it. *(source: screens/_components.yaml#publishGate; contracts/satellite/platform-ops.yaml#publishSupportNotice)*

**Data it reads**: `listSupportNotices` (onLoad, End-of-support notices)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The support escalation console list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the support escalation console untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No support escalation console yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
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

- `listSupportNotices` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `publishSupportNotice` → `PLATFORM_RELEASE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_MANAGE` for `publishSupportNotice`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-035` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-035?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Publish support notice, What publishing changes.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-036` Platform Notification Broadcast

**Broadcast a notice to every tenant, or to some of them.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Support & Communications · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-036 |
| Who uses it | ticvai staff holding `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSupportNotices` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/general/platform-notification-broadcast` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): listAnnouncements and publishAnnouncement are the tenant's staff announcements (WORKFORCE_VIEW, ANNOUNCEMENT_PUBLISH); a platform broadcast is a support notice … Removed 2 October 2026 (CHG-WIR-021): listAnnouncements and publishAnnouncement are the tenant's staff announcements (WORKFORCE_VIEW, ANNOUNCEMENT_PUBLISH); a platform broadcast is a support notice … Open: No contract — not specified

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Broadcast a platform notice to tenants (maintenance, incidents) and see what was sent.

**Fixed on main** (the package already carries these; draw what it says): listAnnouncements and publishAnnouncement (tenant staff announcements, WORKFORCE_VIEW, ANNOUNCEMENT_PUBLISH). (CHG-WIR-021); formPublishSupportNotice asks the person for publishedAt, id. (CHG-SBO-004); formPublishAnnouncement asks the person for publishedAt. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every support notice' drop id, affectedTenantIds, publishedByPrincipalId, scopePath … (CHG-WIR-021); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

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
| ID | the name it points at, never the id | — |
| Support ends at | 1 Oct 2026 | — |
| Message | grouped details | — |
| Affected tenants | list or chips (count when long) | Computed from cell versions, never typed. A notice to the wrong list is worse than none. |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

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
|  (publish gate) | navigation or local | — | — | — | — |
| Publish support notice (primary button) | `publishSupportNotice` POST `/support-notices` | SupportNotice | SupportNotice | — | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Publish support notice**: Separate from Save. The publish gate names what goes live, where and from when before it happens; blocked names what is wrong and how to fix it; an override past a warning is recorded with who authorised it. *(source: screens/_components.yaml#publishGate; contracts/satellite/platform-ops.yaml#publishSupportNotice)*

**Data it reads**: `listSupportNotices` (onLoad, End-of-support notices)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The platform notification broadcast list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the platform notification broadcast untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No platform notification broadcast yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listSupportNotices` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_MANAGE` for `publishSupportNotice`. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_RELEASE_VIEW, WORKFORCE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_RELEASE_MANAGE for Publish support notice; ANNOUNCEMENT_PUBLISH for Publish announcement. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/platform-ops.yaml#publishSupportNotice)*
- **publishAnnouncement answers 403**: Show it as something the person can act on, not a failure: The caller lacks `ANNOUNCEMENT_PUBLISH` at the target scope, or sent `kind` `emergency` without `ANNOUNCEMENT_EMERGENCY` (problem type `emergency-permission-required`, audit R091 (1)). *(source: contracts/satellite/workforce.yaml#publishAnnouncement)*

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

**A refused user sees:** Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_RELEASE_MANAGE` for `publishSupportNotice`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-036` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-036?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Publish support notice, What publishing changes.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
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
"listSupportNotices": {"method":"GET","path":"/support-notices","contract":"platform-ops","summary":"End-of-support notices","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SupportNotice"},
"publishSupportNotice": {"method":"POST","path":"/support-notices","contract":"platform-ops","summary":"Publish an end-of-support notice","permission":"PLATFORM_RELEASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SupportNotice","responds":"SupportNotice"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"SupportNotice": {"type":"object","x-ticvai-persistence":"control.support_notice","required":["id","version","supportEndsAt","publishedAt"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string"},"supportEndsAt":{"type":"string","format":"date"},"message":{"type":"object","additionalProperties":{"type":"string"}},"affectedTenantIds":{"type":"array","readOnly":true,"description":"Computed from cell versions, never typed. A notice to the wrong list is worse than none.","items":{"type":"string","format":"uuid"}},"publishedByPrincipalId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}}
}
```
