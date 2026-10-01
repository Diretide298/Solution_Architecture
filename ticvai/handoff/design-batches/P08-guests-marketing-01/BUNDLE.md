# P08-guests-marketing-01 — P08 · Guests & Marketing

**4 screens · 18 operations · 32 schemas · 11 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `AI_AUDIT_VIEW, AI_CONFIGURE, AI_USE, AUDIT_VIEW, CASE_MANAGE, CASE_VIEW, MARKETING_MANAGE, MARKETING_VIEW, PERMISSION_VIEW, REPORT_VIEW_VENUE, TENANT_VIEW`. A control nobody can use must say so,
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
| `BO-068` | Audit Log | B–D | 12 | 15 | 6 | 4 | 1 | 0 | — | notStarted (generated) |
| `BO-073` | Lost & Found Register | B–D | 4 | 26 | 6 | 1 | 1 | 0 | — | notStarted (generated) |
| `BO-091` | AI Policy & Spend | A | 42 | 34 | 6 | 37 | 1 | 0 | — | notStarted (generated) |
| `BO-107` | Guests & Marketing | B–D | 42 | 43 | 6 | 25 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-073 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-068` Audit Log

**See who changed what at this venue.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Guests & Marketing · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AUDIT_VIEW`, `PERMISSION_VIEW` (2 read); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAuditRecords` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/audit-log` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried `listAiInteractions` alone** — an audit log showing only AI prompts. The platform audit record is `identity.audit_event`. **Rewired 20 August.** **`listAuditRecords` wired 24 August.** This screen declared zero operations — an audit log with nothing behind it — and `platform.audit_record` was written by nothing and read by nothing. **Found by mapping the POS pack**, where four separate frames wanted an audit view. **Retail board operations wired 24 August.** **Platform-staff access shown 28 September (audit R098)** — `listPlatformStaffGrants` lists every grant a TICVAI operator opened into this tenant, and the `platformStaffGrantId` filter of `listAuditRecords` shows what was done under each.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Org unit id | picker: choose an org unit (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?orgUnitId=` to `listAuditRecords`. | `listAuditRecords` ?orgUnitId |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listAuditRecords`. | `listAuditRecords` ?principalId |
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listAuditRecords`. | `listAuditRecords` ?workstationId |
| Action | text field | optional | — | — | — | Sends `?action=` to `listAuditRecords`. | `listAuditRecords` ?action |
| Subject ref | text field | optional | — | — | — | Sends `?subjectRef=` to `listAuditRecords`. | `listAuditRecords` ?subjectRef |
| From | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?from=` to `listAuditRecords`. | `listAuditRecords` ?from |
| To | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?to=` to `listAuditRecords`. | `listAuditRecords` ?to |
| Platform-staff grant id | picker: choose a platform staff grant (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?platformStaffGrantId=` to `listAuditRecords`, so the log shows only what a platform operator did under that grant. Choosing a row in **Platform-staff grants** fills it (decided 28 September … | `listAuditRecords` ?platformStaffGrantId |
| Open grants only | toggle | — | — | — | — | Sends `?activeOnly=true` to `listPlatformStaffGrants`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Active only | toggle | off | — | `listPlatformStaffGrants` ?activeOnly |

**Form: Resolve permissions** (modal, opened by *Resolve permissions*; *Resolve permissions* calls `resolvePermissions`, *Cancel* sends nothing)

**Collects what `resolvePermissions` sends before it is called.** Required: `principalId`, `roleId`. Optional: `atScopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Principal `principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `resolvePermissions` body |
| Role `roleId` | picker: choose a role | required | — | — | shows names, sends the id | — | `resolvePermissions` body |
| At scope path `atScopePath` | text field | optional | — | — | — | Optional. When supplied, the response also carries `decisionsAtScope`: PERMIT or DENY per permission at that node. | `resolvePermissions` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every audit** (data table, from `listAuditRecords`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | Who acted. |
| Org unit | the name it points at, never the id | The scope node the action happened in. |
| Workstation | the name it points at, never the id | The workstation it was done from, where there was one. |
| Action | text | What was done, as the writing operation names it. |
| Subject ref | text | The thing acted on — a profile, a shift, an order. The same value the `subjectRef` filter matches. |
| Occurred at | 1 Oct 2026, 14:30 | When. The list is ordered by this, most recent first. |
| Platform staff grant | the name it points at, never the id | Set when a TICVAI platform operator acted, naming the grant they acted under (`identity.openPlatformStaffGrant`; decided 28 September … |

**Platform-staff grants** (data table, from `listPlatformStaffGrants`): **Every platform-staff grant into this tenant is visible here** — open, expired and ended, most recent first. Choosing a grant filters the audit log on `platformStaffGrantId` to show what was done under it (decided 28 September, audit R098).

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Operator principal | the name it points at, never the id | The platform operator, from the Control Plane token. Set by the server. |
| Reason | text | — |
| Ticket ref | text | — |
| Permissions | list or chips (count when long) | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Resolve permissions (primary button) | `resolvePermissions` POST `/permissions/resolve` | inline | inline | — | opens modal first |

**Data it reads**: `listAuditRecords` (onLoad, Who did what, where, and when); `listPlatformStaffGrants` (onLoad, Every platform-staff grant into this tenant, so the tenant …)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audit log list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audit log untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audit log yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on orgUnitId, principalId, workstationId, action, subjectRef, from and platformStaffGrantId; the audit log is still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AUDIT_VIEW`, which `listAuditRecords` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAuditRecords` → `AUDIT_VIEW` (read) · staff
- `listPlatformStaffGrants` → `AUDIT_VIEW` (read) · staff
- `resolvePermissions` → `PERMISSION_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `AUDIT_VIEW`, which `listAuditRecords` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.27 | Real-Time Authorization - System shall evaluate access decisions in real time. | Admission and Access | CONTRACTED | `resolvePermissions` |
| 7.1.15 | The system shall support inheritance of permissions from parent roles, groups, departments, venues, or business structures while allowing controlled overrides. | F&B POS | CONTRACTED | `resolvePermissions` |
| 7.1.31 | The system shall restrict access to guest profiles, CRM data, financial data, wallet data, loyalty data, membership data, inventory costs, and marketing data based on permissions. | F&B POS | CONTRACTED | `resolvePermissions` |
| 7.1.51 | Evaluate authorization decisions in real time for every protected transaction, screen, API call or business action. | F&B POS | CONTRACTED | `resolvePermissions` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Audit history shows logins, shift start/end and every change made (old value vs new value) on every screen and transaction; logging can be switched on/off and archived. *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-158)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-068` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 6.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 6.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 6.dc.html#ret-6j`
- Flow F106 *A security dashboard surfaces something and it is investigated*, step 3: Audit Log. → 2 operations, 0 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-068?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Resolve permissions.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `AUDIT_VIEW`, `PERMISSION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-073` Lost & Found Register

**Match what was lost to what was handed in.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Guests & Marketing · wave 2 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listLostItems` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `itemId` (deepLink) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/venue-operations/lost-found-register` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried `listCases` and `createCase`.** `LostItem` exists — CL-07 built it as one entity in two directions, lost and found — and a service case is a different thing. **Rewired 20 August.**

#### Inputs: what the user enters or picks

**Form: Find matches for lost item** (modal, opened by *Find matches for lost item*; *Find matches for lost item* calls `matchLostItem`, *Cancel* sends nothing)

**Collects what `matchLostItem` sends before it is called.** Required: `action`. Optional: `otherItemId`, `claimantSubjectId`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | radio group | required | — | Match · Unmatch · Claim · Return · Dispose | — | — | `matchLostItem` body |
| Other item `otherItemId` | picker: choose an other item | optional | — | — | shows names, sends the id | — | `matchLostItem` body |
| Claimant subject `claimantSubjectId` | picker: choose a claimant subject | optional | — | — | shows names, sends the id | — | `matchLostItem` body |
| Note `note` | text area | optional | — | — | — | — | `matchLostItem` body |

Errors to draw in the form: 409 The item's `status` does not allow the action (`states/lost-item.yaml`) — `match` and `return` need `open`, `unmatch` and `claim` need `matched`, `dispose` … (StateTransitionProblem)

#### Outputs: what the screen shows and produces

**Shown**

**Every lost** (data table, from `listLostItems`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Found or lost | chip: Lost, Found | One entity, two directions. A guest reports a loss and a steward reports a find, and modelling them separately means matching across two … |
| Kind | chip: Bag, Phone, Wallet, Keys, Clothing, Jewellery… | — |
| Description | text | — |
| Colour | text | — |
| Brand | text | — |
| Venue | the name it points at, never the id | — |
| Last seen point | the name it points at, never the id | A point on the venue map. Where a guest thinks they lost it is the strongest signal for a match, and it is also the thing they are least … |
| Reported at | 1 Oct 2026, 14:30 | Device time — `recordLostItem` is offline-capable, so this is when the loss was reported or the find handed in, not when the device synced. |
| Reported by subject | the name it points at, never the id | — |
| Storage location | text | — |
| Status | chip: Open, Matched, Claimed, Disposed, Returned | — |

**The selected lost** (detail panel, from `listLostItems`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Found or lost | chip: Lost, Found | One entity, two directions. A guest reports a loss and a steward reports a find, and modelling them separately means matching across two … |
| Kind | chip: Bag, Phone, Wallet, Keys, Clothing, Jewellery… | — |
| Description | text | — |
| Colour | text | — |
| Brand | text | — |
| Venue | the name it points at, never the id | — |
| Last seen point | the name it points at, never the id | A point on the venue map. Where a guest thinks they lost it is the strongest signal for a match, and it is also the thing they are least … |
| Reported at | 1 Oct 2026, 14:30 | Device time — `recordLostItem` is offline-capable, so this is when the loss was reported or the find handed in, not when the device synced. |
| Reported by subject | the name it points at, never the id | — |
| Storage location | text | — |
| Status | chip: Open, Matched, Claimed, Disposed, Returned | — |
| Photo assets | list or chips (count when long) | — |
| Dispose after | 1 Oct 2026 | A retention date, because unclaimed property has one. A storeroom with no disposal date is a storeroom that fills, and the date is a venue … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Find matches for lost item (primary button) | `matchLostItem` POST `/lost-items/{itemId}/match` | inline | LostItem | 409 The item's `status` does not allow the action (`states/lost-item.yaml`) — `match` and `return` need `open`, `unmatch` and `claim` need `matched`, `dispose` … (StateTransitionProblem) | opens modal first |

**Data it reads**: `listLostItems` (onLoad, Reported and found, with suggested matches)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The lost found register list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the lost found register untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No lost found register yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listLostItems` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `CASE_VIEW`, which `listLostItems` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The item's `status` does not allow the action (`states/lost-item.yaml`) — `match` and `return` need `open`, `unmatch` and `claim` need `matched`, `dispose` … (StateTransitionProblem) |

#### Permissions

- `listLostItems` → `CASE_VIEW` (read) · staff, guest
- `matchLostItem` → `CASE_MANAGE` (configure) · staff
- `recordLostItem` → `CASE_MANAGE` (configure) · staff, guest

**A refused user sees:** Shown when the caller lacks `CASE_VIEW`, which `listLostItems` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.69 | Lost & Found - System shall support lost and found requests. | Guest Mobile App & Branding | CONTRACTED | data `LostItem` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Lost & Found: guests log lost items in the app; back-office staff match and mark items found for collection, with full tracking. *(client request · MoM 10 Aug 2026, 4.6 AI Functions, Lost & Found, Reviews, Loyalty · DI-208)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-073` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-073?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Find matches for lost item.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-091` AI Policy & Spend

**What the assistant may do here, what it has cost, and what happens at the ceiling.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Guests & Marketing · wave 1 · needs the `ai` module |
| Block | Block A · ticket #18095 (APP-SETUP-BO-091) |
| Who uses it | venue staff holding `AI_AUDIT_VIEW`, `AI_CONFIGURE`, `AI_USE` (1 read, 1 configure, 1 operate); in the flows as platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listIndexFailures` reads the population and `getAiPolicy` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `profileKey` (navigation) |
| Route | `/ai/policy` |

**What the spec says about it.** Added 17 August. **Staff and guest spend shown separately** — a venue can manage the first and cannot stop guests asking questions. At the ceiling the manager decides whether to continue; the assistant does not stop on its own (CF-14). **Index failures sit beside spend on purpose** - both answer the same two questions, is the assistant working and what is it costing, and a failure rate is the cheaper half of that answer.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Job id | picker: choose a job (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?jobId=` to `listIndexFailures`. | `listIndexFailures` ?jobId |
| Stage | radio group | optional | — | Fetch · Parse · Chunk · Embed · Upsert | — | Sends `?stage=` to `listIndexFailures`. | `listIndexFailures` ?stage |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Scope path | text field | — | — | `getAiPolicy` ?scopePath |
| From | date picker | — | — | `getAiUsage` ?from |
| Group by | select | — | Tenant · Venue · Principal · Provider · Capability · Day · Agent · Model · Task | `getAiUsage` ?groupBy |
| Family | select | — | Gateway and models · Governance · Action pipeline · Knowledge retrieval · Assistants · Analytics insights · Configuration assistant · Forecasting · Anomaly detection · Risk intelligence · Recommendations · Decision records … | `listAiCapabilities` ?family |
| Status | segmented control | — | Active · Paused | `listAiCapabilities` ?status |
| Risk class | radio group | — | Low · Medium · High · Critical | `listAiCapabilities` ?riskClass |
| Capability key | text field | — | — | `getEffectiveAiPolicy` ?capabilityKey |
| Scope path | text field | — | — | `getEffectiveAiPolicy` ?scopePath |
| Environment | radio group | — | Development · Sandbox · Staging · Production | `getEffectiveAiPolicy` ?environment |
| Audience | segmented control | — | Staff · Guest · Support | `listAssistantProfiles` ?audience |

**Form: Save AI policy** (modal, opened by *Save AI policy*; *Save AI policy* calls `setAiPolicy`, *Cancel* sends nothing)

**Collects what `setAiPolicy` sends before it is called.** Required: `scopeLevel`, `scopePath`, `enabledCapabilities`. Optional: `id`, `allowedRoleIds`, `maskedFields`, `requiresApprovalFor`, `monthlyTokenCeiling`, `ceilingBehaviour`, `ceilingWarningPercent`, `guestCapabilityScope`, `retrieveTopK`, `rerankTopK`, `cacheAnswers`, `cacheTtlMinutes` and 12 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope level `scopeLevel` | segmented control | required | — | Tenant · Venue | — | Tenant sets the default; a venue may narrow it and never widen it. | `setAiPolicy` body |
| Scope path `scopePath` | text field | required | — | — | — | The node this row belongs to, and the key it is written under — the tenant's node where `scopeLevel` is `tenant`, a venue's where it is `venue`. | `setAiPolicy` body |
| Enabled capabilities `enabledCapabilities` | multi-select chips | required | — | Assist · Search · Generate configuration · Generate layout · Summarise · Explain · Gateway and models · Governance · Action pipeline · Knowledge retrieval · Assistants · Analytics insights …; `governance`, `decisionRecords` and `residencyPrivacy` cannot be … | — | Extended on 29 September to the fourteen capabilities of the AI design (section 1.1, `AiCapabilityFamily`). | `setAiPolicy` body |
| Allowed roles `allowedRoleIds` | multi-picker: choose allowed roles | optional | — | — | — | — | `setAiPolicy` body |
| Masked fields `maskedFields` | list of values (chips) | optional | — | An entry naming no column is refused at save rather than silently masking nothing. | — | Redacted before a prompt leaves the platform (8.3.73). Defaults to every field in the pii schema — a masking list nobody filled in should send nothing rather than everything. | `setAiPolicy` body |
| Requires approval for `requiresApprovalFor` | multi-select chips | optional | — | Pricing · Promotion · Operational · Financial · Configuration | — | 8.3.61–8.3.64. Nothing in this list executes without a decision. | `setAiPolicy` body |
| Monthly token ceiling `monthlyTokenCeiling` | number field | optional | — | — | — | — | `setAiPolicy` body |
| Ceiling behaviour `ceilingBehaviour` | segmented control | optional | Warn | Warn · Warn then disable · Block | — | Decided 17 August: warn, and let the venue manager choose. A cap that stops the assistant mid-visit turns a cost control into a guest-facing outage, and the venue has no warning … | `setAiPolicy` body |
| Ceiling behaviour by capability `ceilingBehaviourByCapability` | repeatable rows | optional | — | — | — | Ceiling behaviour per capability (AI design 5.9, AIC-227), so a budget never silently disables fraud scoring, which spends no tokens, or a critical capability. | `setAiPolicy` body |
| Capability `ceilingBehaviourByCapability[].capability` | text field | required | — | — | — | An `AiCapabilityFamily` value, or a registered capability key. | `setAiPolicy` body |
| Behaviour `ceilingBehaviourByCapability[].behaviour` | radio group | required | — | Warn · Warn then disable · Block · Never restrict | — | — | `setAiPolicy` body |
| Autonomy overrides `autonomyOverrides` | repeatable rows | optional | — | — | — | Tighten only (AI design 3.8, AIC-151). A level per capability at or below the capability's ceiling, and on a venue row at or below the tenant row's. | `setAiPolicy` body |
| Capability key `autonomyOverrides[].capabilityKey` | text field | required | — | — | — | — | `setAiPolicy` body |
| Autonomy level `autonomyOverrides[].autonomyLevel` | stepper or slider | required | — | min 0; max 4; 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after … | — | One autonomy scale for every capability (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). | `setAiPolicy` body |
| Ceiling warning percent `ceilingWarningPercent` | number field | optional | 80 | — | — | Warn before the ceiling, not at it. A manager told at 100% has already spent it; one told at 80% can decide with a week left. | `setAiPolicy` body |
| Guest capability scope `guestCapabilityScope` | multi-select chips | optional | — | Ticket selection · Promotions · FAQ · Recommendations · Checkout · Wait times · Wayfinding · Visit planning | — | What a guest-facing assistant may help with, and nothing else (2.1.28). Bounding the capability is what makes the cost predictable and the safety posture tractable — an assistant … | `setAiPolicy` body |
| Retrieve top k `retrieveTopK` | number field | optional | 30 | — | — | How many chunks retrieval returns before reranking. | `setAiPolicy` body |
| Rerank top k `rerankTopK` | number field | optional | 5 | — | — | How many survive the rerank and reach the model. Reranking reduces cost as well as improving quality, which is unusual — retrieval is cheap and the tokens sent to the model are … | `setAiPolicy` body |
| Cache answers `cacheAnswers` | toggle | optional | on | — | — | The largest cost lever available at a kiosk. Guest questions are extraordinarily repetitive — forty questions, thousands of times a day — where staff questions are diverse. | `setAiPolicy` body |
| Cache ttl minutes `cacheTtlMinutes` | number field (minutes) | optional | 60 | — | — | An upper bound on top of event invalidation, not instead of it. The key carries `scope_path` — a cache keyed on the question alone is a cross-venue leak wearing a performance hat. | `setAiPolicy` body |
| Retain interactions days `retainInteractionsDays` | number field (days) | optional | — | — | — | How long prompts and responses are kept. Deprecated 29 September (decision 5): AI data retention is one tenant configuration with a period per data class, 90 days by default, kept … | `setAiPolicy` body |
| Semantic cache threshold `semanticCacheThreshold` | stepper or slider | optional | 0.95 | min 0; max 1 | — | Similarity above which a cached answer serves a new question. `cache:answer` is exact-match on question, scope and locale — *what time do you close* and *when do you shut* are two … | `setAiPolicy` body |
| Negative cache ttl seconds `negativeCacheTtlSeconds` | number field (seconds) | optional | 300 | — | — | How long *no answer found* is remembered. A miss costs a full retrieval and a completion. | `setAiPolicy` body |
| Cascade `cascade` | group | optional | — | — | — | A small model answers and escalates only below a confidence threshold. `ai.suggestion.confidence` exists and nothing routes on it. | `setAiPolicy` body |
| Small model `cascade.smallModel` | text field | optional | — | — | — | — | `setAiPolicy` body |
| Large model `cascade.largeModel` | text field | optional | — | — | — | — | `setAiPolicy` body |
| Escalate below `cascade.escalateBelow` | number field | optional | 0.7 | — | — | — | `setAiPolicy` body |
| Chunking `chunking` | group | optional | — | — | — | The single biggest lever on retrieval quality, and currently nowhere. A venue FAQ and a maintenance manual do not chunk the same way. | `setAiPolicy` body |
| Size tokens `chunking.sizeTokens` | number field | optional | 512 | — | — | — | `setAiPolicy` body |
| Overlap tokens `chunking.overlapTokens` | number field | optional | 64 | — | — | — | `setAiPolicy` body |
| Strategy `chunking.strategy` | segmented control | optional | Sentence | Fixed · Sentence · Semantic | — | — | `setAiPolicy` body |
| Quantisation `quantisation` | segmented control | optional | None | None · Scalar · Binary | — | A decision, never a default. `scalar` int8 is roughly four times smaller — 49 GB becomes 12 — and it costs recall. | `setAiPolicy` body |
| Hnsw `hnsw` | group | optional | — | — | — | Defaults are tuned for neither our recall nor our latency. A collection built with the wrong ones needs a rebuild, which is why this is a creation decision like the sparse index. | `setAiPolicy` body |
| M `hnsw.m` | number field | optional | 16 | — | — | — | `setAiPolicy` body |
| Ef construct `hnsw.efConstruct` | number field | optional | 128 | — | — | — | `setAiPolicy` body |
| Ef search `hnsw.efSearch` | number field | optional | 64 | — | — | — | `setAiPolicy` body |
| Per request token ceiling `perRequestTokenCeiling` | number field | optional | — | — | — | One runaway conversation can spend a tenant's month. `monthlyTokenCeiling` discovers that after it has happened. | `setAiPolicy` body |
| Streams by capability `streamsByCapability` | list of values (chips) | optional | — | — | — | Time to first token and total latency are separate targets. A concierge that starts answering in 300 ms and finishes in 4 seconds is better than one silent for 2. | `setAiPolicy` body |
| Fallback provider `fallbackProviderId` | picker: choose a fallback provider | optional | — | — | shows names, sends the id | BL-151: a provider outage with no fallback is every AI surface going dark at once. | `setAiPolicy` body |
| Guardrail short circuit `guardrailShortCircuit` | toggle | optional | on | — | — | A refusal a rule can decide never reaches a model. Cheaper, faster and more consistent than asking a model to refuse. | `setAiPolicy` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every index failure** (data table, from `listIndexFailures`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Job | the name it points at, never the id | — |
| Source | the name it points at, never the id | — |
| Document ref | text | What would not index. |
| Stage | chip: Fetch, Parse, Chunk, Embed, Upsert | Where it failed decides who fixes it. A parse failure is a document problem; an embed failure is a provider one. |
| Error | text | — |
| Attempts | 1,234 | — |

**The selected index failure** (detail panel, from `listIndexFailures`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Job | the name it points at, never the id | — |
| Source | the name it points at, never the id | — |
| Document ref | text | What would not index. |
| Stage | chip: Fetch, Parse, Chunk, Embed, Upsert | Where it failed decides who fixes it. A parse failure is a document problem; an embed failure is a provider one. |
| Error | text | — |
| Attempts | 1,234 | — |

**The AI usage report** (detail panel, from `getAiUsage`)

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | text | — |
| Rows | list or chips (count when long) | — |

**The AI policy** (detail panel, from `getAiPolicy`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Scope level | chip: Tenant, Venue | Tenant sets the default; a venue may narrow it and never widen it. |
| Scope path | text | The node this row belongs to, and the key it is written under — the tenant's node where `scopeLevel` is `tenant`, a venue's where it is … |
| Enabled capabilities | list or chips (count when long) | Extended on 29 September to the fourteen capabilities of the AI design (section 1.1, `AiCapabilityFamily`). |
| Allowed roles | list or chips (count when long) | — |
| Masked fields | list or chips (count when long) | Redacted before a prompt leaves the platform (8.3.73). Defaults to every field in the pii schema — a masking list nobody filled in should … |
| Requires approval for | list or chips (count when long) | 8.3.61–8.3.64. Nothing in this list executes without a decision. |
| Monthly token ceiling | 1,234 | — |
| Ceiling behaviour | chip: Warn, Warn then disable, Block | Decided 17 August: warn, and let the venue manager choose. A cap that stops the assistant mid-visit turns a cost control into a … |
| Ceiling warning percent | 1,234 | Warn before the ceiling, not at it. A manager told at 100% has already spent it; one told at 80% can decide with a week left. |
| Guest capability scope | list or chips (count when long) | What a guest-facing assistant may help with, and nothing else (2.1.28). Bounding the capability is what makes the cost predictable and the … |
| Retrieve top k | 1,234 | How many chunks retrieval returns before reranking. |
| Rerank top k | 1,234 | How many survive the rerank and reach the model. Reranking reduces cost as well as improving quality, which is unusual — retrieval is cheap … |
| Cache answers | yes / no (icon or chip) | The largest cost lever available at a kiosk. Guest questions are extraordinarily repetitive — forty questions, thousands of times a day — … |
| Cache ttl minutes | 1,234 | An upper bound on top of event invalidation, not instead of it. The key carries `scope_path` — a cache keyed on the question alone is a … |
| Retain interactions days | 1,234 | How long prompts and responses are kept. Deprecated 29 September (decision 5): AI data retention is one tenant configuration with a period … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save AI policy (primary button) | `setAiPolicy` PUT `/policy` | AiPolicy | AiPolicy | — | opens modal first |

**Data it reads**: `getAiPolicy` (onLoad, What the assistant may do here); `getAiUsage` (onLoad, Usage, cost and performance); `listIndexFailures` (onLoad, Records an index could not embed, and at which stage); `listAiCapabilities` (onLoad, The capability registry); `getEffectiveAiPolicy` (onLoad, The policy in force for a capability at a scope); `listAssistantProfiles` (onLoad, Assistant profiles)

**Where the user goes next**

- → `ADM-004` Platform Audit Log: *Platform Audit Log*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The policy spend list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the policy spend untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No policy spend yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on jobId, stage and the policy spend are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_CONFIGURE`, which `getAiPolicy` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getAiPolicy` → `AI_CONFIGURE` (configure) · staff
- `setAiPolicy` → `AI_CONFIGURE` (configure) · staff
- `getAiUsage` → `AI_AUDIT_VIEW` (read) · staff
- `listIndexFailures` → `AI_CONFIGURE` (configure) · staff
- `listAiCapabilities` → `AI_USE` (operate) · staff
- `getEffectiveAiPolicy` → `AI_USE` (operate) · staff
- `configureAssistantProfile` → `AI_CONFIGURE` (configure) · staff
- `listAssistantProfiles` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `AI_CONFIGURE`, which `getAiPolicy` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

37 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.1 | Provides control, transparency and accountability over AI-generated outputs. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.55 | System shall log all AI prompts. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.56 | System shall log all AI responses. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.57 | System shall log all AI actions. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.58 | System shall maintain AI audit trails. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.59 | System shall maintain AI decision history. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.60 | System shall maintain AI execution history. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.61 | System shall require approval before AI-driven pricing changes. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.62 | System shall require approval before AI-driven promotions. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.63 | System shall require approval before AI-driven operational changes. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.64 | System shall require approval before AI-driven financial actions. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| 8.3.65 | System shall support multi-level AI approvals. | Unified Operations Dashboard | CONTRACTED | `getAiPolicy` |
| … 25 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI operations monitoring shows health, cost/budget tracking and which AI agents consume the most resources and for what purpose, so the business can manage AI spend. *(client request · MoM 21 Sep 2026, 4.11 Core AI Platform — Operations & Consumption Monitoring · DI-968)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-091` · status **notStarted** · provenance generated
- Flow F100 *An AI provider is configured, budgeted and audited*, step 2: AI Policy & Spend. → 3 operations, 3 of them previously unwalked.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)
- ADR-0033 *Every asynchronous handoff has an outbox and a place to fail* (`docs/adr/0033-outbox-and-dead-letters.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (42), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-091?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save AI policy.
- [ ] Every transition is wired: `ADM-004`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `AI_CONFIGURE`, `AI_USE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-107` Guests & Marketing

**Everything in guests & marketing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Guests & Marketing · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW`, `REPORT_VIEW_VENUE`, `TENANT_VIEW` (1 configure, 2 read, 1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCampaigns` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more … |
| Route | `/guests-marketing` |

**What the spec says about it.** Section landing. **3 screens reach the entry point through here** — before 20 August they reached it through nothing.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Draft · Scheduled · Sending · Paused · Completed · Stopped · Failed | — | Sends `?status=` to `listCampaigns`. | `listCampaigns` ?status |
| Search guests & marketing | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |

**Form: Create campaign** (modal, opened by *Create campaign*; *Create campaign* calls `createCampaign`, *Cancel* sends nothing)

**Collects what `createCampaign` sends before it is called.** Required: `name`, `kind`, `channel`, `segmentId`, `content`. Optional: `venueId`, `trigger`, `scheduledFor`, `consentPurpose`, `sendWindow`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createCampaign` body |
| Kind `kind` | radio group | required | — | One off · Scheduled · Triggered · Recurring | — | — | `createCampaign` body |
| Channel `channel` | select | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `createCampaign` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCampaign` body |
| Segment `segmentId` | picker: choose a segment | required | — | — | shows names, sends the id | — | `createCampaign` body |
| Content `content` | group | required | — | — | — | — | `createCampaign` body |
| Template `content.templateId` | picker: choose a template | required | — | — | shows names, sends the id | — | `createCampaign` body |
| Subject override `content.subjectOverride` | key and value settings | optional | — | — | — | — | `createCampaign` body |
| Merge defaults `content.mergeDefaults` | key and value settings | optional | — | — | — | Fallback values for the template's `mergeFields`, by name, used where a guest has no value. | `createCampaign` body |
| Promotion `content.promotionId` | picker: choose a promotion | optional | — | — | shows names, sends the id | Offer carried by the campaign. Coupon codes are issued from it. | `createCampaign` body |
| Trigger `trigger` | group | optional | — | — | — | — | `createCampaign` body |
| Event `trigger.event` | select | optional | — | Booking confirmed · Visit completed · Membership expiring · Birthday · Abandoned cart · First visit · Inactivity · Entitlement expiring | — | `entitlementExpiring` (29 September, build pass, group G2; 5.5.30) fires on `entitlement.expiringSoon`: a ticket or pass the guest still holds comes within its template's … | `createCampaign` body |
| Delay hours `trigger.delayHours` | number field (hours) | optional | — | — | — | — | `createCampaign` body |
| Conditions `trigger.conditions` | repeatable rows | optional | — | — | — | — | `createCampaign` body |
| Attribute `trigger.conditions[].attribute` | text field | required | — | — | — | Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language. | `createCampaign` body |
| Operator `trigger.conditions[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Exists · Not exists · Within days | — | — | `createCampaign` body |
| Value `trigger.conditions[].value` | field | optional | — | — | — | — | `createCampaign` body |
| Values `trigger.conditions[].values` | list of values (chips) | optional | — | — | — | — | `createCampaign` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCampaign` body |
| Consent purpose `consentPurpose` | select | optional | Marketing | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | — | — | `createCampaign` body |
| Send window `sendWindow` | group | optional | — | — | — | Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen. | `createCampaign` body |
| Start time `sendWindow.startTime` | text field | optional | — | — | — | — | `createCampaign` body |
| End time `sendWindow.endTime` | text field | optional | — | — | — | — | `createCampaign` body |
| Time zone `sendWindow.timeZone` | text field | optional | — | — | — | — | `createCampaign` body |
| Send time mode `sendTimeMode` | segmented control | optional | Fixed | Fixed · Optimised | — | `optimised` sends each recipient at the hour `ai.requestSuggestion` (kind `sendTime`) gives for them, inside `sendWindow` (29 September, build pass, group G2; 22.3.19). | `createCampaign` body |
| Optimise channel `optimiseChannel` | toggle | optional | off | — | — | With `sendTimeMode` `optimised`, route each recipient to the channel the suggestion names, among the channels they consented to (22.9.16). | `createCampaign` body |
| Variants `variants` | repeatable rows | optional | — | at most 5 | — | A/B (or up to five-way) content and subject variants (29 September, build pass, group G2; 22.1.17, BO-772). | `createCampaign` body |
| Label `variants[].label` | text field | required | — | max length 20 | — | A, B, C... | `createCampaign` body |
| Subject override `variants[].subjectOverride` | key and value settings | optional | — | — | — | Subject line by locale. | `createCampaign` body |
| Template `variants[].templateId` | picker: choose a template | optional | — | — | shows names, sends the id | A different template for this variant; null uses the campaign's `content.templateId`. | `createCampaign` body |
| Split percent `variants[].splitPercent` | stepper or slider | optional | — | min 1; max 100 | — | Share of the test group; null splits evenly. | `createCampaign` body |
| Source `variants[].source` | segmented control | optional | Manual | Manual · AI draft | — | — | `createCampaign` body |
| AI decision record `variants[].aiDecisionRecordId` | text field | optional | — | — | — | The decision record of the `ai.proposeMarketingContent` draft it came from, for `aiDraft`. | `createCampaign` body |
| Ab test `abTest` | group | optional | — | Required when `variants` has two or more. | — | How the variants are tested. Required when `variants` has two or more. | `createCampaign` body |
| Test percent `abTest.testPercent` | stepper or slider | optional | 20 | min 5; max 100 | — | Share of the audience the variants are tested on; 100 splits everyone and picks no winner. | `createCampaign` body |
| Success metric `abTest.successMetric` | radio group | optional | Click rate | Open rate · Click rate · Conversion rate · Attributed revenue | — | — | `createCampaign` body |
| Decide after hours `abTest.decideAfterHours` | number field (hours) | optional | 4 | min 1; max 168 | — | — | `createCampaign` body |
| Winner rule `abTest.winnerRule` | segmented control | optional | Automatic | Automatic · Manual | — | — | `createCampaign` body |
| Minimum sample per variant `abTest.minimumSamplePerVariant` | number field | optional | 500 | min 1 | — | Below this many sends per variant no winner is declared automatically; a person picks. | `createCampaign` body |
| Winning variant `abTest.winningVariantId` | picker: choose a winning variant | optional | — | — | shows names, sends the id | Set by the automatic rule, or by a person through `updateCampaign`. | `createCampaign` body |

Errors to draw in the form: 400 Validation failed

#### Outputs: what the screen shows and produces

**Shown**

**Every campaign** (data table, from `listCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: One off, Scheduled, Triggered, Recurring | — |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Venue | the name it points at, never the id | — |
| Segment | the name it points at, never the id | — |
| Content | grouped details | — |
| Trigger | grouped details | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Consent purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |
| Send window | grouped details | Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen. |
| ID | the name it points at, never the id | — |
| Budget cap | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Takings and admissions today** (metric tile, from `getKpiValues`): **Takings and admissions**, from `getKpiValues?kpiCodes=takings,admissions`; with no `period` the period is today in the venue's time zone (decided 28 September, audit R283).

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Period | text | — |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Card list** (card list): 3 screens. **No attention counts** until a summary operation exists to supply them (decided 28 September, audit R283).

**The selected campaign** (detail panel, from `listCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: One off, Scheduled, Triggered, Recurring | — |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Venue | the name it points at, never the id | — |
| Segment | the name it points at, never the id | — |
| Content | grouped details | — |
| Trigger | grouped details | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Consent purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |
| Send window | grouped details | Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen. |
| ID | the name it points at, never the id | — |
| Budget cap | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Budget spent | AED 1,234.50 | BL-169. A campaign could spend without limit — following the promotions `budgetCap` precedent. |
| Status | chip: Draft, Scheduled, Sending, Paused, Completed, Stopped… | — |
| Is paused | yes / no (icon or chip) | — |
| Created by principal | the name it points at, never the id | — |

**The venue settings** (detail panel, from `getVenueSettings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | From the path of `setVenueSettings`. |
| Currency code | text | `readOnly` is the freeze. `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the … |
| Currency scale | 1,234 | Scale travels with currency (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency … |
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| Biometrics | grouped details | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. |
| Segregated access | grouped details | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a … |
| Alerting | grouped details | CF-134. On-platform notification, marked as read. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create campaign (primary button) | `createCampaign` POST `/campaigns` | CreateCampaignRequest | Campaign | 400 Validation failed | opens modal first |

**Data it reads**: `getKpiValues` (onLoad, Today's takings and admissions tiles — …); `getVenueSettings` (onLoad, What is enabled here); `listCampaigns` (onLoad, Campaigns and their reach)

**Where the user goes next**

- → `BO-073` Lost & Found Register: *Lost & Found Register*
- → `BO-091` AI Policy & Spend: *AI Policy & Spend*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list, with counts. |
| Error (`?state=error`) | Could not load. Venue Home is still reachable. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing configured in guests & marketing yet.** The action is the first thing to set up, not a blank list. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter. |
| Permission denied (`?state=emptyNoAccess`) | You do not have permission for guests & marketing. **Said plainly** — an empty section reads as broken. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `listCampaigns` → `MARKETING_VIEW` (read) · staff
- `createCampaign` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** You do not have permission for guests & marketing. **Said plainly** — an empty section reads as broken.

#### Requirements it meets

25 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.1.1 | Campaign Creation | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.4 | Campaign Scheduling | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.12 | Ticketing Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.13 | Membership Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.14 | Loyalty Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.4.8 | Product & Event Integration | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.9.14 | Marketing Notifications | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.8 | Campaign Budget Management | Marketing & CRM | CONTRACTED | data `Campaign` |
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| 3.2.46 | Face Pass shouldt restrict male guests attempting to enter during Friday Ladies Night, which needs to be validated with rule-based facial recognition validation. | Admission and Access | CONTRACTED | data `VenueSettings` |
| 8.9.3 | System shall display queue lengths, estimated wait times, queue utilization, queue alerts, and queue prediction metrics. | Unified Operations Dashboard | CONTRACTED | data `VenueSettings` |
| 11.1.15 | Approval Breach Alerts - System shall notify users when approval SLA thresholds are exceeded. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| … 13 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-107` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (42), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (43 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-107?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create campaign.
- [ ] Every transition is wired: `BO-073`, `BO-091`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`, `REPORT_VIEW_VENUE`, `TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P08 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-030, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-043, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051, DI-052 (each is in the design inputs below).

**Workshop tracker rows about P08 as a whole** (1: 1 open, 0 closed). Open first; a closed row says where it went on 30 September.

- **S8** Venue Management back-end configuration wireframes *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*

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

### Across P08 Venue Management

- Qossai: configuration screens should consolidate related functionality, potentially merging 3-4 previously separate screens into one, rather than the repetitive one-screen-per-concept pattern of the AI-built reference system. *(agreed · MoM 24 Sep 2026, 4.5 Screen Consolidation Philosophy · DI-987)*
- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- **Open question.** Allam: a user's visibility must be restrictable to specific outlets (an F&B manager of one outlet should not see other outlets' items); also relevant for ticketing/event-specific access. Implementation approach still open. *(open · MoM 18 Aug 2026, 4.6 Role-Based & Outlet-Level Access Control — Open Item · DI-331)*
- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Built-in help menu with step-by-step tutorials with screenshots for common tasks (e.g. how to sell a ticket at the POS). *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-160)*
- Custom data-capture fields ("data mask") at account, event, extended-ticket and product level: field types text, dropdown, radio, true/false; multi-language labels; validation (min/max length, required/optional); reusable value lists (e.g. country list). Standard fields come out of the box. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-155)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Allam: queue management is built into the system (not third-party) so traffic entering the site can be throttled from the back office itself. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-060)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Documentation deliverable includes user guides and help content; the preview shows a TICVAI Help Center with categories (Getting Started, Events, Tickets, Orders, Payments, Memberships, Access Control, Reports, Integrations), a "Welcome to TICVAI" getting-started article and Quick Links (Create an Event, Set Pricing, Manage Access, View Reports). *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - What We Deliver / Key Deliverables Preview · DI-052)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Back-office shell: collapsible left sidebar with Overview, Events, Tickets, Orders, Customers, Memberships, Access Control, POS, Reports, Analytics, AI Assistant, Settings, and the signed-in user (name, role) at the bottom; top bar with global search (Cmd+K), current time and date, Notifications with unread dot, and user menu. *(agreed · Design Vision Book 29 Jul 2026, 04 Dashboard Vision (p4) - navigation shell · DI-030)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*
- Back-office controls for the waiting room: configurable maximum active users and admission intervals, set per customer and venue. *(agreed · MoM 28 Jul 2026, 19. Auto-scaling and Virtual Waiting Room · DI-017)*

**3 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"configureAssistantProfile": {"method":"PUT","path":"/assistant-profiles/{profileKey}","contract":"ai","summary":"Define an assistant profile","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiAssistantProfile","responds":"AiAssistantProfile"},
"createCampaign": {"method":"POST","path":"/campaigns","contract":"marketing-crm","summary":"Create a campaign","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCampaignRequest","responds":"Campaign"},
"getAiPolicy": {"method":"GET","path":"/policy","contract":"ai","summary":"What the assistant may do here","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopePath","in":"query","required":false}],"requestBody":null,"responds":"AiPolicy"},
"getAiUsage": {"method":"GET","path":"/usage","contract":"ai","summary":"Usage, cost and performance","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"AiUsageReport"},
"getEffectiveAiPolicy": {"method":"GET","path":"/governance/effective-policy","contract":"ai","summary":"The policy in force for a capability at a scope","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"capabilityKey","in":"query","required":true},{"name":"scopePath","in":"query","required":null},{"name":"environment","in":"query","required":null}],"requestBody":null,"responds":"AiEffectivePolicy"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getVenueSettings": {"method":"GET","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Operational settings for this venue","permission":"TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"listAiCapabilities": {"method":"GET","path":"/governance/capabilities","contract":"ai","summary":"The capability registry","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"family","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"riskClass","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAssistantProfiles": {"method":"GET","path":"/assistant-profiles","contract":"ai","summary":"Assistant profiles","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"audience","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAuditRecords": {"method":"GET","path":"/audit-records","contract":"tenancy","summary":"Who did what, where, and when","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"orgUnitId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"action","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"platformStaffGrantId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCampaigns": {"method":"GET","path":"/campaigns","contract":"marketing-crm","summary":"List campaigns","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listIndexFailures": {"method":"GET","path":"/index-failures","contract":"ai","summary":"Records an index could not embed","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"jobId","in":"query","required":null},{"name":"stage","in":"query","required":null}],"requestBody":null,"responds":"IndexFailure"},
"listLostItems": {"method":"GET","path":"/lost-items","contract":"marketing-crm","summary":"Reported and found items","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants","contract":"identity","summary":"Which platform staff have acted in this tenant, and under what grant","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"matchLostItem": {"method":"POST","path":"/lost-items/{itemId}/match","contract":"marketing-crm","summary":"Tie a report to a found item, or hand it back","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LostItem"},
"recordLostItem": {"method":"POST","path":"/lost-items","contract":"marketing-crm","summary":"Report something lost, or hand something in","permission":"CASE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LostItem","responds":"LostItem"},
"resolvePermissions": {"method":"POST","path":"/permissions/resolve","contract":"identity","summary":"Simulate a principal's effective permissions","permission":"PERMISSION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setAiPolicy": {"method":"PUT","path":"/policy","contract":"ai","summary":"Set the policy","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiPolicy","responds":"AiPolicy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAssistantProfile": {"type":"object","x-ticvai-persistence":"ai.assistant_profile","description":"**One assistant runtime, many profiles** (design 5.10, C5; AIC-069..080). The profile decides the audience, roles, knowledge sources, tools, model task and guest scope: guest concierge, support chatbot and staff assistants by role.","required":["profileKey","audience"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"profileKey":{"type":"string"},"name":{"type":"string"},"audience":{"type":"string","enum":["staff","guest","support"]},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"module":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"}],"nullable":true},"collectionIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Knowledge collections it retrieves from."},"toolKeys":{"type":"array","items":{"type":"string"},"description":"Registered tools it may propose (an assistant only reads; a change request goes to the configuration assistant, AIC-078)."},"modelTask":{"type":"string","description":"The gateway task, e.g. `assistant.staff.answer`. The visit planner agent (29 September, MOB-6) is profile `planner.guest` with task `planner.guest.refine` and the five `venue-map` visit-plan tools. The app publishing guide (M24-08) is profile `guide.appPublishing` with task `assistant.staff.answer`, grounded on the platform's store-publishing collection only."},"guestCapabilityScope":{"type":"array","items":{"type":"string"},"description":"For a guest profile: the same values as `AiPolicy.guestCapabilityScope`, narrowed."},"locales":{"type":"array","items":{"type":"string"}},"handoverTarget":{"type":"string","nullable":true,"description":"Where \"ask a person\" goes: a support queue or a staff role."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiAutonomyLevel": {"type":"integer","minimum":0,"maximum":4,"description":"**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."},
"AiCapabilityFamily": {"type":"string","enum":["gatewayAndModels","governance","actionPipeline","knowledgeRetrieval","assistants","analyticsInsights","configurationAssistant","forecasting","anomalyDetection","riskIntelligence","recommendations","decisionRecords","operationsEvaluation","residencyPrivacy"],"description":"The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point, action pipeline and human oversight, knowledge and retrieval, assistants, analytics assistant and insights, configuration assistant, forecasting and operational requirements, anomaly detection, fraud and risk intelligence, recommendation and upsell engine, decision records and audit, operations/evaluation/cost, residency/privacy/tenancy. **Every registered capability belongs to exactly one**, which is what `AiPolicy.enabledCapabilities` and the usage report group by."},
"AiCapabilityRegistration": {"type":"object","x-ticvai-persistence":"ai.capability","description":"**An entry in the capability registry** (design 3.1 Registry, AIC-144, AIC-145; ADM-520). Nothing becomes an operational AI capability without a row here: owner, function, risk class, autonomy, data categories and lifecycle per environment. `autonomyCeiling` is the platform ceiling for the tenant; a tenant or venue may lower `autonomyLevel`, never raise it (AIC-151).","required":["capabilityKey","family","riskClass","autonomyLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string","description":"Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`."},"family":{"$ref":"#/components/schemas/AiCapabilityFamily"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal","description":"The accountable business owner (AIC-144)."},"businessFunction":{"type":"string","nullable":true},"riskClass":{"$ref":"#/components/schemas/AiRiskClass"},"autonomyCeiling":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"readOnly":true,"description":"The first-release ceiling for this capability (design 3.8 table). Read-only to a tenant."},"autonomyLevel":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"description":"The level in force at this scope. At most `autonomyCeiling`."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories the capability reads (ADM-524)."},"lifecycle":{"type":"object","description":"Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.","properties":{"development":{"type":"string","enum":["draft","pilot","active","retired"]},"staging":{"type":"string","enum":["draft","pilot","active","retired"]},"production":{"type":"string","enum":["draft","pilot","active","retired"]}}},"degradationMode":{"type":"string","enum":["rulesOnly","searchOnly","humanHandoff","hidden","failOpen","lastPublished"],"description":"What the capability does when its model or the service is unavailable (design 3.7, AIC-241)."},"status":{"type":"string","enum":["active","paused"],"readOnly":true,"description":"Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed."},"pausedReason":{"type":"string","nullable":true,"readOnly":true},"pausedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiEffectivePolicy": {"type":"object","x-ticvai-persistence":"none — resolved from published policy versions, exceptions and ai.policy","description":"**The policy in force for a capability at a scope** (AIC-153, AIC-165; ADM-525, ADM-528): the intersection of the capability, governance policy and the tenant or venue AI policy, with where each part came from.","required":["capabilityKey","autonomyLevel","rules"],"properties":{"capabilityKey":{"type":"string"},"scopePath":{"type":"string"},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"autonomyCeiling":{"$ref":"#/components/schemas/AiAutonomyLevel"},"rules":{"type":"array","items":{"type":"object","properties":{"rule":{"$ref":"#/components/schemas/AiGovernanceRule"},"policyKey":{"type":"string"},"version":{"type":"integer"},"scopePath":{"type":"string"}}}},"exceptions":{"type":"array","items":{"$ref":"#/components/schemas/AiPolicyException"}},"conflicts":{"type":"array","items":{"type":"object","properties":{"description":{"type":"string"},"resolvedTo":{"$ref":"#/components/schemas/AiGovernanceOutcome"}}},"description":"Conflicting rules and the more restrictive result they resolved to (AIC-161)."},"resolvedAt":{"type":"string","format":"date-time"}}},
"AiGovernanceOutcome": {"type":"string","enum":["allow","allowWithConditions","prepareOnly","approvalRequired","escalate","block"],"description":"What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). `block` is an answer, not an error, and is logged as outcome `refused`."},
"AiGovernanceRule": {"type":"object","x-ticvai-persistence":"none — held in the jsonb rules column of ai.governance_policy_version, through AiGovernanceRuleList","description":"One rule of a governance policy version: which actions on which data, under which conditions, get which outcome (AIC-147..160).","required":["effect"],"properties":{"effect":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"capabilityKeys":{"type":"array","items":{"type":"string"},"description":"Registered capabilities it applies to. Empty means every capability the policy names."},"actions":{"type":"array","items":{"type":"string","enum":["read","analyze","recommend","generate","prepare","create","modify","publish","execute","delete"]},"description":"ADM-523: what AI may do, from reading to executing."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories (ADM-524), e.g. `customerContact`, `payment`, `financial`, `operational`."},"purposes":{"type":"array","items":{"type":"string"},"description":"Permitted purposes for those categories (AIC-156, AIR-182)."},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Above this value the effect escalates one step (for example to `approvalRequired`)."},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Roles the rule applies to; empty means every role."},"environments":{"type":"array","items":{"type":"string","enum":["development","sandbox","staging","production"]},"description":"ADM-525. Empty means every environment. **`sandbox`** (18 September minutes, M18-01): the developer sandbox and a tenant's trial environment, governed apart from staging so a rule can allow in sandbox what it blocks in production."},"conditions":{"type":"object","additionalProperties":true,"nullable":true,"description":"Conditions attached to an `allowWithConditions` effect, for example `maskFields` or `requireCitation`."}}},
"AiPolicy": {"type":"object","x-ticvai-persistence":"ai.policy","required":["scopeLevel","scopePath","enabledCapabilities"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"scopeLevel":{"type":"string","enum":["tenant","venue"],"description":"Tenant sets the default; a venue may narrow it and never widen it."},"scopePath":{"type":"string","description":"**The node this row belongs to, and the key it is written under** — the tenant's node where `scopeLevel` is `tenant`, a venue's where it is `venue`. One row per `scopePath`; `setAiPolicy` writes the row it names and `getAiPolicy` resolves nearest ancestor first (ADR-0018).\n"},"enabledCapabilities":{"type":"array","description":"**Extended on 29 September to the fourteen capabilities of the AI design** (section 1.1, `AiCapabilityFamily`). The six earlier values stay: they are finer switches inside `assistants`, `knowledgeRetrieval` and `configurationAssistant`, and a tenant that set them keeps them. `governance`, `decisionRecords` and `residencyPrivacy` cannot be switched off; listing them is accepted and changes nothing.\n","items":{"type":"string","enum":["assist","search","generateConfiguration","generateLayout","summarise","explain","gatewayAndModels","governance","actionPipeline","knowledgeRetrieval","assistants","analyticsInsights","configurationAssistant","forecasting","anomalyDetection","riskIntelligence","recommendations","decisionRecords","operationsEvaluation","residencyPrivacy"]}},"allowedRoleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"maskedFields":{"type":"array","description":"Redacted before a prompt leaves the platform (8.3.73). **Defaults to every field in the pii schema** — a masking list nobody filled in should send nothing rather than everything.\nEach entry is a column named `schema.table.column`, as the DDL names it — `pii.subject_contact.email`. **Omitted, null and an empty array all take the default**, because each of them is a list nobody filled in. An entry naming no column is refused at save rather than silently masking nothing.\n","items":{"type":"string","pattern":"^[a-z][a-z0-9_]*\\.[a-z][a-z0-9_]*\\.[a-z][a-z0-9_]*$"}},"requiresApprovalFor":{"type":"array","description":"8.3.61–8.3.64. Nothing in this list executes without a decision.","items":{"type":"string","enum":["pricing","promotion","operational","financial","configuration"]}},"monthlyTokenCeiling":{"type":"integer","nullable":true},"ceilingBehaviour":{"type":"string","enum":["warn","warnThenDisable","block"],"default":"warn","description":"**Decided 17 August: warn, and let the venue manager choose.** A cap that stops the assistant mid-visit turns a cost control into a guest-facing outage, and the venue has no warning it is about to happen.\nAt the ceiling a notification reaches the venue manager with the spend and the remaining period, and **the assistant keeps answering until somebody decides otherwise**. `warnThenDisable` and `block` exist for a tenant who asks for a hard limit; neither is the default.\n**Now the default for capabilities without their own entry** in `ceilingBehaviourByCapability` (AI design 5.9).\n"},"ceilingBehaviourByCapability":{"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**Ceiling behaviour per capability** (AI design 5.9, AIC-227), so a budget never silently disables fraud scoring, which spends no tokens, or a critical capability. A capability not listed takes `ceilingBehaviour`. The guest concierge defaults to `warn` (decided 17 August).\n","items":{"type":"object","required":["capability","behaviour"],"properties":{"capability":{"type":"string","description":"An `AiCapabilityFamily` value, or a registered capability key."},"behaviour":{"type":"string","enum":["warn","warnThenDisable","block","neverRestrict"]}}}},"autonomyOverrides":{"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**Tighten only** (AI design 3.8, AIC-151). A level per capability at or below the capability's ceiling, and on a venue row at or below the tenant row's. Autonomy is separate from user permission (AIC-154).\n","items":{"type":"object","required":["capabilityKey","autonomyLevel"],"properties":{"capabilityKey":{"type":"string"},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"}}}},"ceilingWarningPercent":{"type":"integer","default":80,"description":"**Warn before the ceiling, not at it.** A manager told at 100% has already spent it; one told at 80% can decide with a week left.\n"},"guestCapabilityScope":{"type":"array","description":"**What a guest-facing assistant may help with, and nothing else** (2.1.28). Bounding the capability is what makes the cost predictable and the safety posture tractable — an assistant that answers anything is one that can be asked anything.\n","items":{"type":"string","enum":["ticketSelection","promotions","faq","recommendations","checkout","waitTimes","wayfinding","visitPlanning"]}},"retrieveTopK":{"type":"integer","default":30,"description":"How many chunks retrieval returns before reranking."},"rerankTopK":{"type":"integer","nullable":true,"default":5,"description":"How many survive the rerank and reach the model. **Reranking reduces cost as well as improving quality**, which is unusual — retrieval is cheap and the tokens sent to the model are not.\nNull disables reranking, and a venue with no rerank provider configured runs without it rather than failing.\n"},"cacheAnswers":{"type":"boolean","default":true,"description":"**The largest cost lever available at a kiosk.** Guest questions are extraordinarily repetitive — forty questions, thousands of times a day — where staff questions are diverse.\n**Invalidation runs on the same events that invalidate the index.** A cached answer that outlives a price change has misled a guest on the venue's behalf, which is worse than a slow one.\n"},"cacheTtlMinutes":{"type":"integer","default":60,"description":"An upper bound on top of event invalidation, not instead of it. **The key carries `scope_path`** — a cache keyed on the question alone is a cross-venue leak wearing a performance hat.\n"},"retainInteractionsDays":{"type":"integer","deprecated":true,"description":"How long prompts and responses are kept. **Deprecated 29 September (decision 5):** AI data retention is one tenant configuration with a period per data class, 90 days by default, kept with the tenant's other data-retention settings in `tenancy`, not here. Read for one release and ignored once the tenant setting exists.\n"},"semanticCacheThreshold":{"type":"number","minimum":0,"maximum":1,"default":0.95,"description":"**Similarity above which a cached answer serves a new question.** `cache:answer` is exact-match on question, scope and locale — *what time do you close* and *when do you shut* are two misses and two provider calls.\n\n**Per capability, not global.** A factual venue question tolerates 0.95; a recommendation tolerates nothing. **A tenant who finds it wrong can move it**, which is why it is policy rather than a constant."},"negativeCacheTtlSeconds":{"type":"integer","default":300,"description":"**How long *no answer found* is remembered.** A miss costs a full retrieval and a completion.\n\n**Shorter than a hit deliberately** — the answer may exist tomorrow because somebody indexed it."},"cascade":{"type":"object","nullable":true,"description":"**A small model answers and escalates only below a confidence threshold.** `ai.suggestion.confidence` exists and nothing routes on it.","properties":{"smallModel":{"type":"string"},"largeModel":{"type":"string"},"escalateBelow":{"type":"number","default":0.7}}},"chunking":{"type":"object","description":"**The single biggest lever on retrieval quality**, and currently nowhere. **A venue FAQ and a maintenance manual do not chunk the same way.** Per collection, not global.","properties":{"sizeTokens":{"type":"integer","default":512},"overlapTokens":{"type":"integer","default":64},"strategy":{"type":"string","enum":["fixed","sentence","semantic"],"default":"sentence"}}},"quantisation":{"type":"string","enum":["none","scalar","binary"],"default":"none","description":"**A decision, never a default.** `scalar` int8 is roughly four times smaller — 49 GB becomes 12 — **and it costs recall**. `binary` is smaller again and needs rescoring against full vectors to be usable.\n\n**A creation decision**: changing it means a rebuild, which is what `shadow_collection` is for. **A tenant whose search quality drops after an infrastructure change should be able to find the line that did it.**"},"hnsw":{"type":"object","nullable":true,"description":"**Defaults are tuned for neither our recall nor our latency.** A collection built with the wrong ones needs a rebuild, which is why this is a creation decision like the sparse index.","properties":{"m":{"type":"integer","default":16},"efConstruct":{"type":"integer","default":128},"efSearch":{"type":"integer","default":64}}},"perRequestTokenCeiling":{"type":"integer","nullable":true,"description":"**One runaway conversation can spend a tenant's month.** `monthlyTokenCeiling` discovers that after it has happened."},"streamsByCapability":{"type":"array","items":{"type":"string"},"description":"**Time to first token and total latency are separate targets.** A concierge that starts answering in 300 ms and finishes in 4 seconds is better than one silent for 2.\n\n**`chat` streams; `generateConfiguration` does not** — nobody watches a config draft assemble."},"fallbackProviderId":{"type":"string","format":"uuid","nullable":true,"description":"BL-151: **a provider outage with no fallback is every AI surface going dark at once.**\n\n**`residencyRefused` is never failed over.** It is a correct answer, and moving the call elsewhere would defeat the refusal."},"guardrailShortCircuit":{"type":"boolean","default":true,"description":"**A refusal a rule can decide never reaches a model.** Cheaper, faster and more consistent than asking a model to refuse."},"suggestionProviders":{"allOf":[{"$ref":"#/components/schemas/SuggestionProviderAssignments"}],"readOnly":true,"description":"**Which producer answers each `SuggestionKind`**, and what `requestSuggestion` routes by. Written only by `setSuggestionProvider`; `setAiPolicy` leaves it as it was. Held on the tenant row — a venue row does not carry its own.\n"}}},
"AiPolicyException": {"type":"object","x-ticvai-persistence":"ai.policy_exception","description":"**A temporary, recorded exception to a governance policy** (AIC-162, ADM-526): an expiry, an approver and compensating controls. Governance is never bypassed silently.","required":["policyId","reason","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"policyId":{"type":"string","format":"uuid","x-ticvai-references":"ai.governance_policy"},"capabilityKey":{"type":"string","nullable":true},"reason":{"type":"string","maxLength":2000},"compensatingControls":{"type":"array","items":{"type":"string"}},"startsAt":{"type":"string","format":"date-time","nullable":true},"expiresAt":{"type":"string","format":"date-time","description":"Required. An exception with no end is a policy change, and goes through publication."},"status":{"type":"string","enum":["active","expired","revoked"],"readOnly":true},"approvedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"revokedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"revokedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"revokeReason":{"type":"string","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRiskClass": {"type":"string","enum":["low","medium","high","critical"],"description":"Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). The governance decision point scores against it."},
"AiUsageReport": {"type":"object","x-ticvai-persistence":"none — aggregated from ai.activity","properties":{"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"groupBy":{"type":"string"},"rows":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"interactions":{"type":"integer"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"p95LatencyMs":{"type":"integer"},"refusalRate":{"type":"number"},"rejectionRate":{"type":"number","description":"Proposals a person refused. **The number that says whether the assistant is worth having**, and the one nobody thinks to measure.\n"}}}},"forecast":{"type":"object","nullable":true,"description":"**A month-end projection, labelled a forecast** (AI design 2.3, 4.5). Present where `to` is inside the current month. Never added into `rows`.\n","properties":{"label":{"type":"string","enum":["forecast"]},"periodEnd":{"type":"string","format":"date"},"projectedTokens":{"type":"integer"},"projectedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"basis":{"type":"string","description":"How it was projected, e.g. the run rate of the last 7 days."}}}}},
"AuditRecord": {"x-ticvai-append-only":"occurredAt","type":"object","x-ticvai-persistence":"platform.audit_record","description":"26 September, pull audit R198. **One row of the platform audit trail, as `listAuditRecords` returns it.** It was a free-form object, so nothing said what an audit row carries. These are the fields the operation already filters on — who, where, on which workstation, what action, on what, and when — and nothing more. Written by the operations that audit themselves; never edited and never deleted.\n","required":["id","action","occurredAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid","description":"Who acted."},"orgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The scope node the action happened in."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation it was done from, where there was one."},"action":{"type":"string","description":"What was done, as the writing operation names it."},"subjectRef":{"type":"string","nullable":true,"description":"**The thing acted on** — a profile, a shift, an order. The same value the `subjectRef` filter matches.\n"},"occurredAt":{"type":"string","format":"date-time","description":"When. The list is ordered by this, most recent first."},"platformStaffGrantId":{"type":"string","format":"uuid","nullable":true,"description":"**Set when a TICVAI platform operator acted, naming the grant they acted under** (`identity.openPlatformStaffGrant`; decided 28 September, audit R098). Null for the tenant's own staff. Every platform action in a tenant carries one, so the tenant can see all of them.\n"}}},
"Campaign": {"x-ticvai-persistence":"marketing.campaign","allOf":[{"$ref":"#/components/schemas/CreateCampaignRequest"},{"type":"object","required":["id","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"budgetCap":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"budgetSpent":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"BL-169. **A campaign could spend without limit** — following the promotions `budgetCap` precedent. **Sending stops at the cap rather than overspending and reporting it**, because a marketing budget discovered after it was exceeded is a budget nobody set.\n"},"status":{"$ref":"#/components/schemas/CampaignStatus"},"isPaused":{"type":"boolean"},"createdByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"launchedAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true},"sentCount":{"type":"integer","readOnly":true,"x-ticvai-persisted":false,"description":"**How many messages went out**, counted from `marketing.message_dispatch` at read time rather than kept as a counter on the campaign row, so it cannot drift from the dispatch records it summarises. Test sends are not dispatches of the campaign and are not counted.\n"}}}]},
"CampaignContent": {"x-ticvai-persistence":"none — embedded in campaign","type":"object","required":["templateId"],"properties":{"templateId":{"type":"string","format":"uuid"},"subjectOverride":{"type":"object","additionalProperties":{"type":"string"}},"mergeDefaults":{"type":"object","description":"Fallback values for the template's `mergeFields`, by name, used where a guest has no value.","additionalProperties":{"type":"string"}},"promotionId":{"type":"string","format":"uuid","nullable":true,"description":"Offer carried by the campaign. Coupon codes are issued from it."}}},
"CampaignKind": {"type":"string","enum":["oneOff","scheduled","triggered","recurring"]},
"CampaignStatus": {"type":"string","enum":["draft","scheduled","sending","paused","completed","stopped","failed"]},
"CampaignTrigger": {"x-ticvai-persistence":"none — embedded in campaign","type":"object","properties":{"event":{"type":"string","enum":["bookingConfirmed","visitCompleted","membershipExpiring","birthday","abandonedCart","firstVisit","inactivity","entitlementExpiring"],"description":"`entitlementExpiring` (29 September, build pass, group G2; 5.5.30) fires on `entitlement.expiringSoon`: a ticket or pass the guest still holds comes within its template's `expiryNoticeDays` of `validTo`. The notice period is set on the template, so `delayHours` shifts the send within it rather than setting it. An entitlement belonging to a membership is left to `membershipExpiring`, so a member is not told twice."},"delayHours":{"type":"integer"},"conditions":{"type":"array","items":{"$ref":"#/components/schemas/SegmentCriterion"}}}},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"CreateCampaignRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","kind","channel","segmentId","content"],"properties":{"name":{"type":"string","maxLength":200},"kind":{"$ref":"#/components/schemas/CampaignKind"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"venueId":{"type":"string","format":"uuid"},"segmentId":{"type":"string","format":"uuid"},"content":{"$ref":"#/components/schemas/CampaignContent"},"trigger":{"$ref":"#/components/schemas/CampaignTrigger"},"scheduledFor":{"type":"string","format":"date-time"},"consentPurpose":{"allOf":[{"$ref":"#/components/schemas/ConsentPurpose"}],"default":"marketing"},"sendWindow":{"type":"object","description":"Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen.\n","properties":{"startTime":{"type":"string"},"endTime":{"type":"string"},"timeZone":{"type":"string"}}},"sendTimeMode":{"type":"string","enum":["fixed","optimised"],"default":"fixed","description":"`optimised` sends each recipient at the hour `ai.requestSuggestion` (kind `sendTime`) gives for them, inside `sendWindow` (29 September, build pass, group G2; 22.3.19). `fixed` is the behaviour before. Falls back to `scheduledFor` per recipient where there is no suggestion or AI is off."},"optimiseChannel":{"type":"boolean","default":false,"description":"With `sendTimeMode` `optimised`, route each recipient to the channel the suggestion names, among the channels they consented to (22.9.16). Off keeps `channel`."},"variants":{"type":"array","maxItems":5,"nullable":true,"description":"**A/B (or up to five-way) content and subject variants** (29 September, build pass, group G2; 22.1.17, BO-772). Each is a subject override and optionally a different template, written by a person or taken from an AI draft (`ai.proposeMarketingContent`, `source` `aiDraft`). Held as rows of `marketing.campaign_variant`. Null or empty is a single-content campaign.","items":{"$ref":"#/components/schemas/MarketingCampaignVariant"}},"abTest":{"type":"object","nullable":true,"description":"How the variants are tested. Required when `variants` has two or more.","properties":{"testPercent":{"type":"integer","minimum":5,"maximum":100,"default":20,"description":"Share of the audience the variants are tested on; 100 splits everyone and picks no winner."},"successMetric":{"type":"string","enum":["openRate","clickRate","conversionRate","attributedRevenue"],"default":"clickRate"},"decideAfterHours":{"type":"integer","minimum":1,"maximum":168,"default":4},"winnerRule":{"type":"string","enum":["automatic","manual"],"default":"automatic"},"minimumSamplePerVariant":{"type":"integer","minimum":1,"default":500,"description":"Below this many sends per variant no winner is declared automatically; a person picks."},"winningVariantId":{"type":"string","format":"uuid","nullable":true,"description":"Set by the automatic rule, or by a person through `updateCampaign`."}}}}},
"IndexFailure": {"type":"object","x-ticvai-persistence":"ai.index_failure","description":"ADR-0033. **Failure is a row somebody works, not a log line.**\n\n`ai.index_job` already counts `records_failed` and holds a `failure_sample`; **this is where the other 4,999 go.**","required":["id"],"properties":{"id":{"type":"string","format":"uuid"},"jobId":{"type":"string","format":"uuid"},"sourceId":{"type":"string","format":"uuid"},"documentRef":{"type":"string","description":"What would not index."},"stage":{"type":"string","enum":["fetch","parse","chunk","embed","upsert"],"description":"**Where it failed decides who fixes it.** A parse failure is a document problem; an embed failure is a provider one."},"error":{"type":"string"},"attempts":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.index_failure` had no scope column and no declared owner, so no policy. The indexed source's scope, copied when the failure is written.\n"}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"LostItem": {"type":"object","x-ticvai-persistence":"marketing.lost_item","description":"BL-021. **Screens existed on three platforms and `lostAndFound` is a `ModuleKey`, and there was no item, no claim and no match between them** — which is the whole capability.\nGeneric case management holds a conversation about a lost bag. **It cannot tell you that the bag somebody handed in on Tuesday is the one somebody asked about on Monday**, and that match is the only thing the module is for.\n","required":["id","kind","foundOrLost","venueId","reportedAt"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"foundOrLost":{"type":"string","enum":["lost","found"],"description":"**One entity, two directions.** A guest reports a loss and a steward reports a find, and modelling them separately means matching across two tables that drift.\n"},"kind":{"type":"string","enum":["bag","phone","wallet","keys","clothing","jewellery","documents","toy","buggy","other"]},"description":{"type":"string"},"colour":{"type":"string","nullable":true},"brand":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid"},"lastSeenPointId":{"type":"string","format":"uuid","nullable":true,"description":"A point on the venue map. **Where a guest thinks they lost it is the strongest signal for a match**, and it is also the thing they are least sure about.\n"},"reportedAt":{"type":"string","format":"date-time","description":"**Device time** — `recordLostItem` is offline-capable, so this is when the loss was reported or the find handed in, not when the device synced. The `recorded_at` of naming-and-style 5.2 for this row.\n"},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the record arrived. Equal to `reportedAt` for one recorded online."},"reportedBySubjectId":{"type":"string","format":"uuid","nullable":true},"storageLocation":{"type":"string","nullable":true},"status":{"readOnly":true,"type":"string","enum":["open","matched","claimed","disposed","returned"]},"photoAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"matchedItemId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The other side of the match — set by `matchLostItem` `match` (to `otherItemId`) and cleared by `unmatch`, on both items."},"caseId":{"type":"string","format":"uuid","nullable":true,"description":"The case the guest raised about it (`raiseMyCase` with `kind` `lostProperty`), where there is one."},"disposeAfter":{"type":"string","format":"date","nullable":true,"description":"**A retention date, because unclaimed property has one.** A storeroom with no disposal date is a storeroom that fills, and the date is a venue policy rather than a default.\n"}}},
"MarketingCampaignVariant": {"type":"object","x-ticvai-persistence":"marketing.campaign_variant","description":"One content or subject variant of a campaign, for an A/B test (22.1.17; 29 September, build pass, group G2, from group G1's handoff). Written with its campaign by `createCampaign` and `updateCampaign`.","required":["label"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"campaignId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"marketing.campaign"},"label":{"type":"string","maxLength":20,"description":"A, B, C..."},"subjectOverride":{"type":"object","nullable":true,"description":"Subject line by locale.","additionalProperties":{"type":"string"}},"templateId":{"type":"string","format":"uuid","nullable":true,"description":"A different template for this variant; null uses the campaign's `content.templateId`."},"splitPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Share of the test group; null splits evenly."},"source":{"type":"string","enum":["manual","aiDraft"],"default":"manual"},"aiDecisionRecordId":{"type":"string","nullable":true,"description":"The decision record of the `ai.proposeMarketingContent` draft it came from, for `aiDraft`."},"isWinner":{"type":"boolean","default":false,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005), the campaign's."}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE"]},
"PermissionSet": {"type":"array","items":{"$ref":"#/components/schemas/Permission"},"uniqueItems":true},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"ScopedPermissions": {"type":"object","description":"Permissions effective at a given scope path, after deny resolution. Clients filter navigation on this and never compute permissions themselves.\n","required":["scopePath","permissions"],"properties":{"scopePath":{"type":"string","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"permissions":{"$ref":"#/components/schemas/PermissionSet"}}},
"SuggestionProviderAssignments": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The routing table for `requestSuggestion`, held on the tenant's `ai.policy` row** as one `jsonb` column (`suggestion_providers`). At most one entry per `kind`.\n","items":{"$ref":"#/components/schemas/SuggestionProviderAssignment"}},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}}
}
```
