# P09-platform-ops-01 — P09 · Platform Ops

**1 screens · 6 operations · 4 schemas · 2 permissions**

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
  `PLATFORM_CELL_MANAGE, PLATFORM_CELL_VIEW`. A control nobody can use must say so,
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
| `ADM-318` | Dead Letters | B–D | 9 | 39 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-318` Dead Letters

**Every event the platform gave up on, and the act that puts it back. A dead letter is work the platform accepted and did not do.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform Ops · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_CELL_MANAGE`, `PLATFORM_CELL_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listDeadLetters` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `deadLetterId` (deepLink), `republishId` (navigation) · cold entry: **The ordinary path is a row on this screen**, and `replayDeadLetter` takes the id from the row the operator chose. A deep link is how an alert reaches one … |
| Route | `/platform/dead-letters` |

**What the spec says about it.** Added 4 September. **47 consumers declare `retryThenDeadLetter` and all 47 are marked `isCritical`, and until this screen existed nothing in the package read the table they land in.** Deliberately not DEV-005 Webhooks: `replayEvents` is partner-facing redelivery of a customer's own integration, and handling a platform failure as a customer integration question is how it stays unfixed.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Events the platform gave up on (dead letters) and the act that puts them back: replay one, or republish from the outbox by tenant and time range. Replaying shows attempts and the last error first.

**Fixed on main** (the package already carries these; draw what it says): Tables show every schema field, plumbing included: 'Every dead letter' drop id, outboxId, scopePath; 'Outbox republishes, newest first' … (CHG-SBO-004); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Consumer | text field | optional | — | — | — | Sends `?consumer=` to `listDeadLetters`. | `listDeadLetters` ?consumer |
| Since | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?since=` to `listDeadLetters`. | `listDeadLetters` ?since |
| Republish status | radio group | optional | — | Queued · Running · Completed · Failed · Cancelled | — | Sends `?status=` to `listOutboxRepublishes`. | `listOutboxRepublishes` ?status |
| Tenant | picker: choose a tenant (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?tenantId=` to `listOutboxRepublishes`. | `listOutboxRepublishes` ?tenantId |

**Form: Republish from the outbox** (modal, opened by *Republish from the outbox*; *Republish* calls `republishOutbox`, *Cancel* sends nothing)

**Collects what `republishOutbox` sends before it is called.** Required: `tenantId`, `from`, `to` (`from` before `to`, `to` no later than now) and `reason` (up to 500 characters). Optional: `eventNames`, catalogue names; empty means every event. **Says how to choose `from`**: when the oldest message the lost broker still held was published; if unknown, the time of the loss minus one hour, or the start of any consumer halt then in progress, whichever is earlier. Too early costs duplicates the inboxes skip; too late loses events. A `409` names the republish the tenant already has; a `422` names the oldest `from` the hot outbox still holds. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tenant `tenantId` | picker: choose a tenant | required | — | — | shows names, sends the id | The tenant whose database's outbox is read (`control.tenant`). | `republishOutbox` body |
| From `from` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Inclusive. Early enough: when the oldest message still held by the lost broker was published; when unknown, the time of the loss minus one hour, or the start of any consumer halt … | `republishOutbox` body |
| To `to` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Exclusive. No later than now; after a DR failover, the time of the request. | `republishOutbox` body |
| Event names `eventNames` | list of values (chips) | optional | — | — | — | Catalogue event names (`events/`) to republish; absent means every event. An unknown name is the shared `400` `validation`. | `republishOutbox` body |
| Reason `reason` | text area | required | — | max length 500 | — | Why, for the audit trail (e.g. "broker rebuilt after DR failover to the secondary region"). | `republishOutbox` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 The tenant already has a republish `queued` or `running` (`republish-in-progress`; `detail` names it), or the `Idempotency-Key` was used for a different …; 422 `from` is older than the oldest hot outbox partition: that part of the range is archived to Blob and republishing from the archive is not built …

**Form: Cancel republish** (confirmDialog, opened by *Cancel republish*; *Cancel republish* calls `cancelOutboxRepublish`, *Cancel* sends nothing)

**Names the tenant, the range and how far it has got** (`cursorAt`, `rowsPublished`). The relay stops after the batch in flight and keeps the cursor, so a new request can start where this one stopped. A republish that has already finished is refused `409` `republish-finished`.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The republish has already `completed`, `failed` or been `cancelled` (`republish-finished`), or the `Idempotency-Key` was used for a different request …

#### Outputs: what the screen shows and produces

**Shown**

**Every dead letter** (data table, from `listDeadLetters`)

| Shows | Format | Notes |
|---|---|---|
| Event name | text | — |
| Consumer | text | Which consumer failed. A dead letter you cannot attribute is a log entry with a table’s overhead. |
| Payload | grouped details | The event as it was written. Replay needs the payload, not a reference to a row that may have moved on. |
| Attempts | 1,234 | Five, exponential from one second, jittered (ADR-0033). Jitter because a thousand failures at the same instant retry at the same instant. |
| Last error | text | — |
| Last attempt at | 1 Oct 2026, 14:30 | — |
| Replay count | 1,234 | A replay is a new attempt, not a reset. An operator retrying the same poison message forty times should be able to see that they did. |

**The selected dead letter** (detail panel, from `listDeadLetters`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Outbox | the name it points at, never the id | The row that would not deliver. |
| Event name | text | — |
| Consumer | text | Which consumer failed. A dead letter you cannot attribute is a log entry with a table’s overhead. |
| Payload | grouped details | The event as it was written. Replay needs the payload, not a reference to a row that may have moved on. |
| Attempts | 1,234 | Five, exponential from one second, jittered (ADR-0033). Jitter because a thousand failures at the same instant retry at the same instant. |
| Last error | text | — |
| Last attempt at | 1 Oct 2026, 14:30 | — |
| Replay count | 1,234 | A replay is a new attempt, not a reset. An operator retrying the same poison message forty times should be able to see that they did. |
| Scope path | text | — |

**Outbox republishes, newest first** (data table, from `listOutboxRepublishes`)

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026, 14:30 | Inclusive start of the outbox `created_at` range. |
| To | 1 Oct 2026, 14:30 | Exclusive end of the outbox `created_at` range. |
| Event names | list or chips (count when long) | The event names asked for; null means every event. |
| Status | chip: Queued, Running, Completed, Failed, Cancelled | `queued` until the lease holder picks it up; `completed` when the cursor reaches `to`; `failed` with `lastError` after the relay's retry … |
| Cursor at | 1 Oct 2026, 14:30 | How far it has got, the `created_at` of the last row published (with the row id as the keyset tiebreak, held by the relay). |
| Rows published | 1,234 | — |
| Requested by | the name it points at, never the id | The staff principal who asked. |
| Requested at | 1 Oct 2026, 14:30 | — |

**The selected republish and its progress** (detail panel, from `getOutboxRepublish`): Refetched while the republish is `queued` or `running`, so `cursorAt` and `rowsPublished` move.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Tenant | the name it points at, never the id | The tenant whose database's outbox is republished. |
| From | 1 Oct 2026, 14:30 | Inclusive start of the outbox `created_at` range. |
| To | 1 Oct 2026, 14:30 | Exclusive end of the outbox `created_at` range. |
| Event names | list or chips (count when long) | The event names asked for; null means every event. |
| Reason | text | — |
| Status | chip: Queued, Running, Completed, Failed, Cancelled | `queued` until the lease holder picks it up; `completed` when the cursor reaches `to`; `failed` with `lastError` after the relay's retry … |
| Cursor at | 1 Oct 2026, 14:30 | How far it has got, the `created_at` of the last row published (with the row id as the keyset tiebreak, held by the relay). |
| Rows published | 1,234 | — |
| Last error | text | — |
| Requested by | the name it points at, never the id | The staff principal who asked. |
| Requested at | 1 Oct 2026, 14:30 | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Finished at | 1 Oct 2026, 14:30 | Set on `completed`, `failed` or `cancelled`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Replay dead letter (primary button) | `replayDeadLetter` POST `/dead-letters/{deadLetterId}/replay` | — | DeadLetter | — | — |
| Republish from the outbox (primary button) | `republishOutbox` POST `/outbox-republishes` | OutboxRepublishRequest | OutboxRepublish | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 The tenant already has a republish `queued` or `running` (`republish-in-progress`; `detail` names it), or the `Idempotency-Key` was … | gated `PLATFORM_CELL_MANAGE`; opens modal first |
| Cancel republish (destructive button) | `cancelOutboxRepublish` POST `/outbox-republishes/{republishId}/cancel` | — | OutboxRepublish | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The republish has already `completed`, `failed` or … | gated `PLATFORM_CELL_MANAGE`; opens confirmDialog first |

**Data it reads**: `listDeadLetters` (onLoad, Events the retry path gave up on); `listOutboxRepublishes` (onLoad, Every outbox republish asked for, newest first, with how …)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dead letters list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dead letters untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dead letters yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on consumer, since and the dead letters are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `listDeadLetters` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The republish has already `completed`, `failed` or been `cancelled` (`republish-finished`), or the `Idempotency-Key` was used for a different request …; 409 The tenant already has a republish `queued` or `running` (`republish-in-progress`; `detail` names it), or the `Idempotency-Key` was used for a different …; 422 `from` is older than the oldest hot outbox partition … |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_CELL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_CELL_MANAGE for Replay dead letter, Republish from the outbox, Cancel republish. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/platform-ops.yaml#replayDeadLetter)*
- **republishOutbox answers 409**: Show it as something the person can act on, not a failure: The tenant already has a republish `queued` or `running` (`republish-in-progress`; `detail` names it), or the `Idempotency-Key` was used for a different request (`idempotency-conflict`). *(source: contracts/satellite/platform-ops.yaml#republishOutbox)*
- **republishOutbox answers 422**: Show it as something the person can act on, not a failure: `from` is older than the oldest hot outbox partition: that part of the range is archived to Blob and republishing from the archive is not built (`outbox-range-archived`; `detail` names the oldest `from` that would be accepted). *(source: contracts/satellite/platform-ops.yaml#republishOutbox)*
- **cancelOutboxRepublish answers 409**: Show it as something the person can act on, not a failure: The republish has already `completed`, `failed` or been `cancelled` (`republish-finished`), or the `Idempotency-Key` was used for a different request (`idempotency-conflict`). *(source: contracts/satellite/platform-ops.yaml#cancelOutboxRepublish)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
deadLetters:
- event: orders.orderPaid
  consumer: loyalty-accrual
  attempts: 8
  lastError: timeout
  lastAttempt: 01/10/2026 04:12
republish:
  tenant: Marina Leisure Group
  from: 30/09/2026 22:00
  to: 01/10/2026 02:00
  status: running
  rowsPublished: 1840
```

#### Permissions

- `listDeadLetters` → `PLATFORM_CELL_VIEW` (read) · staff
- `replayDeadLetter` → `PLATFORM_CELL_MANAGE` (configure) · staff
- `listOutboxRepublishes` → `PLATFORM_CELL_VIEW` (read) · staff
- `getOutboxRepublish` → `PLATFORM_CELL_VIEW` (read) · staff
- `republishOutbox` → `PLATFORM_CELL_MANAGE` (configure) · staff
- `cancelOutboxRepublish` → `PLATFORM_CELL_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `listDeadLetters` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-318` · status **notStarted** · provenance generated
- ADR-0058 *One relay per region reads every tenant's outbox, and every consumer has an inbox* (`docs/adr/0058-one-relay-per-region-and-an-inbox-per-tenant-database.md`)
- ADR-0033 *Every asynchronous handoff has an outbox and a place to fail* (`docs/adr/0033-outbox-and-dead-letters.md`)
- ADR-0060 *Availability targets per tier, and how they are met* (`docs/adr/0060-availability-targets-high-availability-and-disaster-recovery.md`)
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)
- ADR-0056 *One id type, and time partitioning first, fixed before the first migration* (`docs/adr/0056-one-id-type-and-time-partitioning-before-the-first-migration.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (39 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-318?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Replay dead letter, Republish from the outbox, Cancel republish.
- [ ] Every transition is wired: `ADM-001`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`, `PLATFORM_CELL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 edge case(s) from the process notes are drawn.
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
"cancelOutboxRepublish": {"method":"POST","path":"/outbox-republishes/{republishId}/cancel","contract":"platform-ops","summary":"Stop a republish after its current batch","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OutboxRepublish"},
"getOutboxRepublish": {"method":"GET","path":"/outbox-republishes/{republishId}","contract":"platform-ops","summary":"One republish and its progress","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"platform","parameters":[],"requestBody":null,"responds":"OutboxRepublish"},
"listDeadLetters": {"method":"GET","path":"/dead-letters","contract":"platform-ops","summary":"Undeliverable events","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":"consumer","in":"query","required":null},{"name":"since","in":"query","required":null}],"requestBody":null,"responds":"DeadLetter"},
"listOutboxRepublishes": {"method":"GET","path":"/outbox-republishes","contract":"platform-ops","summary":"Outbox republishes, newest first","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"platform","parameters":[{"name":"tenantId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"replayDeadLetter": {"method":"POST","path":"/dead-letters/{deadLetterId}/replay","contract":"platform-ops","summary":"Re-enter the delivery path","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"platform","parameters":[{"name":"deadLetterId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DeadLetter"},
"republishOutbox": {"method":"POST","path":"/outbox-republishes","contract":"platform-ops","summary":"Republish one tenant database's outbox rows for a time range","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OutboxRepublishRequest","responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"DeadLetter": {"x-ticvai-append-only":"createdAt","type":"object","x-ticvai-persistence":"platform.dead_letter","description":"ADR-0033. **An outbox row whose delivery failed after its retry budget.**\n\n**A financial posting is never dead-lettered** — `ledger.journal_entry` is append-only and a failed posting is an incident. **Nor is a DSAR**: `platform.dsar_request` carries a legal clock, and a dead-lettered erasure nobody works is a regulatory failure with a timestamp on it. Both halt and alert.","required":["id"],"properties":{"id":{"type":"string","format":"uuid"},"outboxId":{"type":"string","format":"uuid","description":"The row that would not deliver."},"eventName":{"type":"string"},"consumer":{"type":"string","description":"Which consumer failed. **A dead letter you cannot attribute is a log entry with a table’s overhead.**"},"payload":{"type":"object","description":"The event as it was written. **Replay needs the payload, not a reference to a row that may have moved on.**"},"attempts":{"type":"integer","description":"**Five, exponential from one second, jittered** (ADR-0033). Jitter because a thousand failures at the same instant retry at the same instant."},"lastError":{"type":"string"},"lastAttemptAt":{"type":"string","format":"date-time"},"replayCount":{"type":"integer","default":0,"description":"**A replay is a new attempt, not a reset.** An operator retrying the same poison message forty times should be able to see that they did."},"scopePath":{"type":"string"},"createdAt":{"type":"string","format":"date-time"}}},
"OutboxRepublish": {"type":"object","x-ticvai-persistence":"control.outbox_republish","description":"**One republish of a tenant database's outbox** (ADR-0058, amended 1 October). A job row in the regional control database beside the relay lease table `control.outbox_relay`. The relay loop holding the tenant's lease carries it out, alternating one republish batch with each live batch, and moves `cursorAt` as it goes. **At most one `queued` or `running` per tenant.** A cancelled or failed job keeps its cursor, so a new request can start where it stopped. The rows republished keep their `published_at`.","required":["id","tenantId","from","to","reason","status","rowsPublished","requestedBy","requestedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"tenantId":{"type":"string","format":"uuid","x-ticvai-references":"control.tenant","description":"The tenant whose database's outbox is republished."},"from":{"type":"string","format":"date-time","x-ticvai-column":"range_starts_at","description":"Inclusive start of the outbox `created_at` range."},"to":{"type":"string","format":"date-time","x-ticvai-column":"range_ends_at","description":"Exclusive end of the outbox `created_at` range."},"eventNames":{"type":"array","nullable":true,"description":"The event names asked for; null means every event.","items":{"type":"string"}},"reason":{"type":"string","maxLength":500},"status":{"type":"string","readOnly":true,"enum":["queued","running","completed","failed","cancelled"],"description":"`queued` until the lease holder picks it up; `completed` when the cursor reaches `to`; `failed` with `lastError` after the relay's retry budget; `cancelled` by `cancelOutboxRepublish`."},"cursorAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"How far it has got, the `created_at` of the last row published (with the row id as the keyset tiebreak, held by the relay). Null until the first batch."},"rowsPublished":{"type":"integer","minimum":0,"default":0,"readOnly":true},"lastError":{"type":"string","nullable":true,"readOnly":true},"requestedBy":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-column":"requested_by_principal_id","description":"The staff principal who asked."},"requestedAt":{"type":"string","format":"date-time","readOnly":true},"startedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"finishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Set on `completed`, `failed` or `cancelled`."}}},
"OutboxRepublishRequest": {"type":"object","x-ticvai-persistence":"none — request body","description":"**What a person asks to republish** (ADR-0058, amended 1 October). One tenant database, a half-open range of `created_at`, optionally some event names, and why.","required":["tenantId","from","to","reason"],"properties":{"tenantId":{"type":"string","format":"uuid","description":"The tenant whose database's outbox is read (`control.tenant`)."},"from":{"type":"string","format":"date-time","description":"Inclusive. **Early enough**: when the oldest message still held by the lost broker was published; when unknown, the time of the loss minus one hour, or the start of any consumer halt then in progress, whichever is earlier. Must be before `to`."},"to":{"type":"string","format":"date-time","description":"Exclusive. No later than now; after a DR failover, the time of the request."},"eventNames":{"type":"array","description":"Catalogue event names (`events/`) to republish; absent means every event. An unknown name is the shared `400` `validation`.","items":{"type":"string"}},"reason":{"type":"string","maxLength":500,"description":"Why, for the audit trail (e.g. \"broker rebuilt after DR failover to the secondary region\")."}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
