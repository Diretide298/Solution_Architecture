# WS142 — Marketing CRM Configuration Reference v1.0 board 8

**10 screens · 16 operations · 21 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `APPROVAL_CONFIGURE, CASE_MANAGE, CASE_VIEW, ORDER_REFUND`. A control nobody can use must say so,
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
| `BO-804` | Case Command Center | B–D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-805` | Case Queue & Search | B–D | 4 | 13 | 6 | 1 | 0 | 6 | — | notStarted (—) |
| `BO-806` | Case Creation | B–D | 3 | 7 | 6 | 8 | 2 | 0 | — | notStarted (—) |
| `BO-807` | Classification & Workflow | B–D | 8 | 7 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-808` | Assignment & Workload | B–D | 1 | 6 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-809` | SLA Policy Configuration | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-810` | Escalation Rules | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-811` | Case Workspace | B–D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-812` | Service Recovery | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-813` | Case Analytics & Audit | B–D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-804, BO-808, BO-809, BO-810, BO-811, BO-812, BO-813 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-804` Case Command Center

**Provide a role-specific overview of service operations. Show new, open, pending, resolved, overdue and SLA-risk cases with escalations, response time, resolution time and CSAT. Visualize volume, priority, category, channel, venue, owner, aging and trend. Surface major incidents, repeated issues, overloaded queues and high-value guests requiring attention. Provide drill-down to saved queues and allow supervisors to take governed corrective action. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/case-command-center-bo-804` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Open · In progress · Awaiting guest · Escalated · Resolved · Closed | `listCases` ?status |
| Assigned to principal | picker: choose an assigned to principal | — | — | `listCases` ?assignedToPrincipalId |
| Breached sla | toggle | — | — | `listCases` ?breachedSla |
| Priority | radio group | — | Low · Normal · High · Urgent | `listCases` ?priority |
| Membership | picker: choose a membership | — | — | `listCases` ?membershipId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listMyCases` (onLoad, The cases this guest raised); `listCases` (onLoad, List service cases)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-805` Case Queue & Search: *Case Queue & Search*
- → `BO-806` Case Creation: *Case Creation*
- → `BO-807` Classification & Workflow: *Classification & Workflow*
- → `BO-808` Assignment & Workload: *Assignment & Workload*
- → `BO-809` SLA Policy Configuration: *SLA Policy Configuration*
- → `BO-810` Escalation Rules: *Escalation Rules*
- → `BO-811` Case Workspace: *Case Workspace*; carries `caseId`
- → `BO-812` Service Recovery: *Service Recovery*
- → `BO-813` Case Analytics & Audit: *Case Analytics & Audit*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The case list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the case untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No case yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the case are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listMyCases` → no permission · guest
- `listCases` → `CASE_VIEW` (read) · staff, guest, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.2.17 | Case & Support History | Marketing & CRM | CONTRACTED | `listCases` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-804` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-804`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 8
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 1: Opens Case Command Center → Provide a role-specific overview of service operations. Show new, open, pending, resolved, overdue and SLA-risk cases with escalations, response time, resolution time and CSAT. Visualize volume …
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F251 branch at step 1 (expected): when Nothing has been set up on Case Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F251 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-804?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-805`, `BO-806`, `BO-807`, `BO-808`, `BO-809`, `BO-810`, `BO-811`, `BO-812`, `BO-813`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-805` Case Queue & Search

**Provide a complete, searchable work queue for service cases. Search by case, guest, contact, transaction, ticket, booking, keyword or external reference. Filter by category, subcategory, priority, channel, venue, status, owner, SLA, date and guest tier. Support saved views, configurable columns, controlled bulk assignment/status actions and export. Display live SLA clocks and role-based action availability without exposing restricted guest data. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/case-queue-search-bo-805` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Parent category id | picker: choose a parent category (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?parentCategoryId=` to `listCaseCategories`. | `listCaseCategories` ?parentCategoryId |
| Top level only | toggle | optional | off | — | — | Sends `?topLevelOnly=` to `listCaseCategories`. | `listCaseCategories` ?topLevelOnly |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listCaseCategories`. | `listCaseCategories` ?isActive |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listServiceQueues`. | `listServiceQueues` ?isActive |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Open · In progress · Awaiting guest · Escalated · Resolved · Closed | `listCases` ?status |
| Assigned to principal | picker: choose an assigned to principal | — | — | `listCases` ?assignedToPrincipalId |
| Breached sla | toggle | — | — | `listCases` ?breachedSla |
| Priority | radio group | — | Low · Normal · High · Urgent | `listCases` ?priority |
| Membership | picker: choose a membership | — | — | `listCases` ?membershipId |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Every case category** (data table, from `listCaseCategories`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Parent category | the name it points at, never the id | Set on a subcategory; null on a top-level category. |
| Default priority | chip: Low, Normal, High, Urgent | The priority a case in this category starts at before routing factors apply. |
| Is active | yes / no (icon or chip) | — |
| Scope path | text | The partition key (ADR-0005). |

**Every service queue** (data table, from `listServiceQueues`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Overflow wait seconds | 1,234 | The queue's overflow threshold; a case waiting longer marks the queue `critical`. |
| Is active | yes / no (icon or chip) | — |
| Scope path | text | The partition key (ADR-0005). |

**Data it reads**: `listCases` (onLoad, The queue); `listCaseCategories` (onLoad, List case categories and subcategories); `listServiceQueues` (onLoad, List customer-service queues)

**Where the user goes next**

- → `BO-804` Case Command Center: *Back to Case Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The case queue search list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the case queue search untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No case queue search yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the case queue search are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCases` → `CASE_VIEW` (read) · staff, guest, partner
- `listCaseCategories` → `CASE_VIEW` (read) · staff
- `listServiceQueues` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.2.17 | Case & Support History | Marketing & CRM | CONTRACTED | `listCases` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-805` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-805`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 8
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 2: Works in Case Queue & Search → Provide a complete, searchable work queue for service cases. Search by case, guest, contact, transaction, ticket, booking, keyword or external reference. Filter by category, subcategory, priority …

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-805?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-804`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-806` Case Creation

**Create a complete case from any service touchpoint. Create manually or from chatbot, conversation, survey, review, transaction, incident or API event. Capture guest, category, priority, channel, venue, subject, details, attachments and linked records. Apply defaults, mandatory fields, duplicate detection, suggested classification and SLA preview. Allow draft and submit workflows and record source, creator, timestamp and initial evidence. Configuration Scope of Work / Version 1.0 41 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/case-creation-bo-806` |

**Known gaps.** **Case Creation declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Parent category id | picker: choose a parent category (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?parentCategoryId=` to `listCaseCategories`. | `listCaseCategories` ?parentCategoryId |
| Top level only | toggle | optional | off | — | — | Sends `?topLevelOnly=` to `listCaseCategories`. | `listCaseCategories` ?topLevelOnly |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listCaseCategories`. | `listCaseCategories` ?isActive |

#### Outputs: what the screen shows and produces

**Shown**

**Every case category** (data table, from `listCaseCategories`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Parent category | the name it points at, never the id | Set on a subcategory; null on a top-level category. |
| Default priority | chip: Low, Normal, High, Urgent | The priority a case in this category starts at before routing factors apply. |
| Is active | yes / no (icon or chip) | — |
| Scope path | text | The partition key (ADR-0005). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create case (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listCaseCategories` (onLoad, List case categories and subcategories)

**Where the user goes next**

- → `BO-804` Case Command Center: *Back to Case Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The case creation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the case creation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No case creation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the case creation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `createCase` → `CASE_MANAGE` (configure) · staff, guest, partner
- `listCaseCategories` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.66 | Guest Support - System shall provide guest support channels. | Guest Mobile App & Branding | CONTRACTED | `createCase` |
| 19.2.70 | Complaint Management - System shall support guest complaints. | Guest Mobile App & Branding | CONTRACTED | `createCase` |
| 2.8.12 | System shall allow agents to create, assign, escalate, track, and resolve guest cases including complaints, refund requests, service requests, incidents, and operational issues. Cases shall be linked … | Ticketing Sales | CONTRACTED | `createCase` |
| 5.3.34 | Link guest profiles with customer service cases, complaints, incidents, refunds, investigations, and follow-up activities. | F&B & Guest Management | CONTRACTED | `createCase` |
| 22.3.1 | Case Creation | Marketing & CRM | CONTRACTED | `createCase` |
| 22.3.2 | Case Classification | Marketing & CRM | CONTRACTED | `createCase` |
| 22.3.3 | Case Assignment | Marketing & CRM | CONTRACTED | `createCase` |
| 22.8.12 | Case Creation & Escalation | Marketing & CRM | CONTRACTED | `createCase` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Case creation captures logging channel/source, category and subcategory (e.g. ticket issue > reschedule) and supports screenshot attachments; investigation tracks all activity and actions on the case. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-541)*
- Cases can be logged from the customer app/website and from the call-centre/admin side, with category, priority, channel and SLA-based escalation rules. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-390)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-806` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-806`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 8
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 4: Works in Case Creation → Create a complete case from any service touchpoint. Create manually or from chatbot, conversation, survey, review, transaction, incident or API event. Capture guest, category, priority, channel …

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-806?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create case, Cancel.
- [ ] Every transition is wired: `BO-804`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-807` Classification & Workflow

**Configure case taxonomies and lifecycle states. Maintain categories, subcategories, reason codes, outcomes, severity, priority and applicable business units. Configure status model, stage transitions, mandatory fields, validation and conditional steps. Use a visual workflow for assignment, work, approval, escalation, resolution and closure. Version and approve configurations and show affected open cases before activating changes. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/classification-workflow-bo-807` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Parent category id | picker: choose a parent category (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?parentCategoryId=` to `listCaseCategories`. | `listCaseCategories` ?parentCategoryId |
| Top level only | toggle | optional | off | — | — | Sends `?topLevelOnly=` to `listCaseCategories`. | `listCaseCategories` ?topLevelOnly |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listCaseCategories`. | `listCaseCategories` ?isActive |

**Form: Save case category definition** (modal, opened by *Save case category definition*; *Save case category definition* calls `setCaseCategoryDefinition`, *Cancel* sends nothing)

**Collects what `setCaseCategoryDefinition` sends before it is called.** Required: `id`, `code`, `name`, `isActive`. Optional: `parentCategoryId`, `defaultPriority`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 60 | — | — | `setCaseCategoryDefinition` body |
| Name `name` | text field | required | — | max length 150 | — | — | `setCaseCategoryDefinition` body |
| Parent category `parentCategoryId` | picker: choose a parent category | optional | — | — | shows names, sends the id | Set on a subcategory; null on a top-level category. | `setCaseCategoryDefinition` body |
| Default priority `defaultPriority` | radio group | optional | — | Low · Normal · High · Urgent | — | The priority a case in this category starts at before routing factors apply. | `setCaseCategoryDefinition` body |
| Is active `isActive` | toggle | required | on | — | — | — | `setCaseCategoryDefinition` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Retiring a category that still has active subcategories.; 422 The parent is not a top-level category of this venue, or the row names itself as its parent.

#### Outputs: what the screen shows and produces

**Shown**

**Every case category** (data table, from `listCaseCategories`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Parent category | the name it points at, never the id | Set on a subcategory; null on a top-level category. |
| Default priority | chip: Low, Normal, High, Urgent | The priority a case in this category starts at before routing factors apply. |
| Is active | yes / no (icon or chip) | — |
| Scope path | text | The partition key (ADR-0005). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Save case category definition (primary button) | `setCaseCategoryDefinition` PUT `/case-categories` | CaseCategory | CaseCategory | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Retiring a category that still has active subcategories. | gated `CASE_MANAGE`; opens modal first |

**Data it reads**: `listCaseCategories` (onLoad, List case categories and subcategories)

**Where the user goes next**

- → `BO-804` Case Command Center: *Back to Case Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The classification workflow list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the classification workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No classification workflow yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the classification workflow are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Retiring a category that still has active subcategories.; 422 The parent is not a top-level category of this venue, or the row names itself as its parent.; 422 The referenced record does not exist or is outside the caller's scope. |

#### Permissions

- `setCaseInvestigationResolution` → `CASE_MANAGE` (configure) · staff
- `listCaseCategories` → `CASE_VIEW` (read) · staff
- `setCaseCategoryDefinition` → `CASE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-807` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-807`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 8
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 6: Works in Classification & Workflow → Configure case taxonomies and lifecycle states. Maintain categories, subcategories, reason codes, outcomes, severity, priority and applicable business units. Configure status model, stage …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-807?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel, Save case category definition.
- [ ] Every transition is wired: `BO-804`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-808` Assignment & Workload

**Assign cases to the best available team or agent. Route by skill, department, venue, language, category, guest tier, priority and operating hours. Configure round robin, least load, ownership continuity, named team and manual assignment methods. Display capacity, utilization, open workload, absence and assignment recommendation. Require approval for restricted reassignment and retain assignment reason and history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/assignment-workload-bo-808` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listServiceQueues`. | `listServiceQueues` ?isActive |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Queue | picker: choose a queue | — | — | `listAgentWorkloadAvailability` ?queueId |
| Team | text field | — | max length 100 | `listAgentWorkloadAvailability` ?team |
| Status | select | — | Available · Busy · On call · Chatting · After call work · Break · Training · Offline | `listAgentWorkloadAvailability` ?status |
| Skill | text field | — | max length 60 | `listAgentWorkloadAvailability` ?skill |
| Language | text field | — | max length 10 | `listAgentWorkloadAvailability` ?language |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Every service queue** (data table, from `listServiceQueues`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Overflow wait seconds | 1,234 | The queue's overflow threshold; a case waiting longer marks the queue `critical`. |
| Is active | yes / no (icon or chip) | — |
| Scope path | text | The partition key (ADR-0005). |

**Data it reads**: `listAgentWorkloadAvailability` (onLoad, Assignment and workload); `listServiceQueues` (onLoad, List customer-service queues)

**Where the user goes next**

- → `BO-804` Case Command Center: *Back to Case Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workload list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workload untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workload yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workload are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAgentWorkloadAvailability` → `CASE_VIEW` (read) · staff
- `listServiceQueues` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-808` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-808`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 8
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 8: Works in Assignment & Workload → Assign cases to the best available team or agent. Route by skill, department, venue, language, category, guest tier, priority and operating hours. Configure round robin, least load, ownership …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-808?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-804`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-809` SLA Policy Configuration

**Define measurable service commitments and pause rules. Configure first-response and resolution targets by case type, priority, venue, channel and guest tier. Apply operating calendars, holidays, 24/7 rules, pause conditions, dependency states and warning thresholds. Define target hierarchy, precedence, exceptions and behavior when multiple SLAs apply. Simulate policies before activation and version, approve and audit every change. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `CASE_MANAGE`, `CASE_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/sla-policy-configuration-bo-809` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Sla policy | picker: choose a sla policy | — | — | `listSlaPolicyService` ?slaPolicyId |
| Priority | radio group | — | Low · Normal · High · Urgent | `listSlaPolicyService` ?priority |
| Kind | select | — | Lost property · Complaint · Question · Accessibility · Refund request · Other; Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.; A case raised as `other` must carry a non-empty `detail` … | `listSlaPolicyService` ?kind |
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listSlaPolicyService` ?channel |
| Queue | picker: choose a queue | — | — | `listSlaPolicyService` ?queueId |
| From | date and time picker | — | — | `listSlaPolicyService` ?from |
| To | date and time picker | — | — | `listSlaPolicyService` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save approval SLA policy (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listSlaPolicyService` (onLoad, SLA policies)

**Where the user goes next**

- → `BO-804` Case Command Center: *Back to Case Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sla policy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sla policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sla policy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the sla policy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listSlaPolicyService` → `CASE_VIEW` (read) · staff
- `setApprovalSlaPolicy` → `APPROVAL_CONFIGURE` (configure) · staff
- `setSlaPolicy` → `CASE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Cases can be logged from the customer app/website and from the call-centre/admin side, with category, priority, channel and SLA-based escalation rules. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-390)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-809` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-809`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 8
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 10: Works in SLA Policy Configuration → Define measurable service commitments and pause rules. Configure first-response and resolution targets by case type, priority, venue, channel and guest tier. Apply operating calendars, holidays, 24/7 …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-809?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save approval SLA policy, Cancel.
- [ ] Every transition is wired: `BO-804`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-810` Escalation Rules

**Automate tiered escalation before or after service risk materializes. Create time-based and condition-based triggers for response, resolution, priority, sentiment, repeat contact and compliance risk. Define escalation level, recipients, notification channel, required action, approval and acknowledgement deadline. Configure supervisor, manager, specialist and executive paths, compensation limits and override controls. Prevent escalation loops and record trigger, evaluated conditions, recipients, actions and closure. Configuration Scope of Work / Version 1.0 42 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/escalation-rules-bo-810` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Escalation type | select | — | Vip · Financial · Event day · Management · Technical · Other | `listEscalationCriticalCase` ?escalationType |
| Priority | radio group | — | Low · Normal · High · Urgent | `listEscalationCriticalCase` ?priority |
| Event | picker: choose an event | — | — | `listEscalationCriticalCase` ?eventId |
| Breached only | toggle | — | — | `listEscalationCriticalCase` ?breachedOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listEscalationCriticalCase` (onLoad, Escalation rules in force)

**Where the user goes next**

- → `BO-804` Case Command Center: *Back to Case Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The escalation rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the escalation rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No escalation rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the escalation rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listEscalationCriticalCase` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Cases can be logged from the customer app/website and from the call-centre/admin side, with category, priority, channel and SLA-based escalation rules. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-390)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-810` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-810`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 8
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 12: Works in Escalation Rules → Automate tiered escalation before or after service risk materializes. Create time-based and condition-based triggers for response, resolution, priority, sentiment, repeat contact and compliance risk. …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-810?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-804`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-811` Case Workspace

**Provide one place to investigate, communicate and resolve a case. Display guest 360, case details, SLA, timeline, messages, notes, tasks, attachments and linked transactions. Support email, SMS, WhatsApp and chat responses using approved templates and complete history. Allow assignment, status, priority, task, approval, related-case and resolution actions by authority. Require reason and evidence for sensitive changes and preserve immutable history after closure. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `caseId` (navigation) |
| Route | `/engagement-support/case-workspace-bo-811` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add case message (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-804` Case Command Center: *Back to Case Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The case list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the case untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No case yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the case are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Resolving without a resolution note |

#### Permissions

- `getCase` → `CASE_VIEW` (read) · staff, partner
- `addCaseMessage` → `CASE_MANAGE` (configure) · staff, partner
- `updateCase` → `CASE_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.3.10 | Case Audit Trail | Marketing & CRM | CONTRACTED | `getCase` |
| 22.3.7 | Agent Notes & Attachments | Marketing & CRM | CONTRACTED | `addCaseMessage` |
| 22.3.4 | Case Workflow Management | Marketing & CRM | CONTRACTED | `updateCase` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-811` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-811`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 8
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 14: Works in Case Workspace → Provide one place to investigate, communicate and resolve a case. Display guest 360, case details, SLA, timeline, messages, notes, tasks, attachments and linked transactions. Support email, SMS …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-811?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add case message, Cancel.
- [ ] Every transition is wired: `BO-804`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-812` Service Recovery

**Configure and approve fair, consistent recovery actions. Maintain compensation matrices by issue, severity, guest tier, value and business unit. Support refund, voucher, loyalty points, wallet credit, upgrade, replacement and follow-up journey actions. Apply auto-approval and manager-approval thresholds, budget limits, fraud checks and segregation of duties. Track recovery cost, delivery, redemption, guest response and effect on satisfaction and retention. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_REFUND` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/service-recovery-bo-812` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-804` Case Command Center: *Back to Case Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The service recovery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the service recovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No service recovery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the service recovery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The request is no longer a draft, or the amount exceeds what remains refundable (`exceedsRefundable`). |

#### Permissions

- `setRefundCompensationService` → `ORDER_REFUND` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-812` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-812`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 8
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 16: Works in Service Recovery → Configure and approve fair, consistent recovery actions. Maintain compensation matrices by issue, severity, guest tier, value and business unit. Support refund, voucher, loyalty points, wallet …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-812?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-804`.
- [ ] Every gated control is gated: `ORDER_REFUND`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-813` Case Analytics & Audit

**Measure service quality, root causes and operational accountability. Report case volume, SLA achievement, aging, backlog, escalation, resolution, CSAT and recovery cost. Analyze category, root cause, channel, venue, product, guest tier, team and agent performance. Track repeat cases, lost revenue, compensation, recovery effectiveness and systemic improvement actions. Provide complete audit, secured export and traceability from reported issue to final resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 43 Board 9 - Surveys, Reviews & Voice of Customer Figure 9. High-definition configuration board with all 10 screens. Configuration Scope of Work / Version 1.0 44**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/case-analytics-audit-bo-813` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Open · In progress · Awaiting guest · Escalated · Resolved · Closed | `listCases` ?status |
| Assigned to principal | picker: choose an assigned to principal | — | — | `listCases` ?assignedToPrincipalId |
| Breached sla | toggle | — | — | `listCases` ?breachedSla |
| Priority | radio group | — | Low · Normal · High · Urgent | `listCases` ?priority |
| Membership | picker: choose a membership | — | — | `listCases` ?membershipId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listMyCases` (onLoad, The cases this guest raised); `listCases` (onLoad, List service cases)

**Where the user goes next**

- → `BO-804` Case Command Center: *Back to Case Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The case analytics audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the case analytics audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No case analytics audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the case analytics audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listMyCases` → no permission · guest
- `listCases` → `CASE_VIEW` (read) · staff, guest, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.2.17 | Case & Support History | Marketing & CRM | CONTRACTED | `listCases` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-813` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS77 Marketing CRM Configuration Reference v1.0 Board 8.dc.html#bo-813`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 8
- Flow F251 *Marketing CRM Configuration Reference v1.0 board 8: Case Command Center*, step 18: Works in Case Analytics & Audit → Measure service quality, root causes and operational accountability. Report case volume, SLA achievement, aging, backlog, escalation, resolution, CSAT and recovery cost. Analyze category, root cause …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-813?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-804`.
- [ ] Every gated control is gated: `CASE_VIEW`.
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

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addCaseMessage": {"method":"POST","path":"/cases/{caseId}/messages","contract":"marketing-crm","summary":"Add a message or internal note","permission":"CASE_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CaseMessage"},
"createCase": {"method":"POST","path":"/cases","contract":"marketing-crm","summary":"Raise a service case","permission":"CASE_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCaseRequest","responds":"Case"},
"getCase": {"method":"GET","path":"/cases/{caseId}","contract":"marketing-crm","summary":"Read a case with its thread","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CaseDetail"},
"listAgentWorkloadAvailability": {"method":"GET","path":"/agent-workload-availability","contract":"marketing-crm","summary":"Agent Workload, Availability & Workforce Control","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":"queueId","in":"query","required":false},{"name":"team","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"skill","in":"query","required":false},{"name":"language","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCaseCategories": {"method":"GET","path":"/case-categories","contract":"marketing-crm","summary":"List case categories and subcategories","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"parentCategoryId","in":"query","required":false},{"name":"topLevelOnly","in":"query","required":false},{"name":"isActive","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCases": {"method":"GET","path":"/cases","contract":"marketing-crm","summary":"List service cases","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"assignedToPrincipalId","in":"query","required":null},{"name":"breachedSla","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"membershipId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEscalationCriticalCase": {"method":"GET","path":"/escalation-critical-case","contract":"marketing-crm","summary":"Escalation & Critical Case Monitor","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":"escalationType","in":"query","required":false},{"name":"priority","in":"query","required":false},{"name":"eventId","in":"query","required":false},{"name":"breachedOnly","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMyCases": {"method":"GET","path":"/my/cases","contract":"marketing-crm","summary":"The cases this guest raised","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listServiceQueues": {"method":"GET","path":"/service-queues","contract":"marketing-crm","summary":"List customer-service queues","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"isActive","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSlaPolicyService": {"method":"GET","path":"/sla-policy-service","contract":"marketing-crm","summary":"SLA Policy & Service-Level Management","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venueId","in":"query","required":false},{"name":"slaPolicyId","in":"query","required":false},{"name":"priority","in":"query","required":false},{"name":"kind","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"queueId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false}],"requestBody":null,"responds":"SlaPolicyServiceLevelManagementView"},
"setApprovalSlaPolicy": {"method":"PUT","path":"/approval-sla-policies","contract":"approvals","summary":"How long a decision may take, and what happens when it does not","permission":"APPROVAL_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalSlaPolicy","responds":"ApprovalSlaPolicy"},
"setCaseCategoryDefinition": {"method":"PUT","path":"/case-categories","contract":"marketing-crm","summary":"Create or change a case category or subcategory","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CaseCategory","responds":"CaseCategory"},
"setCaseInvestigationResolution": {"method":"PUT","path":"/case-investigation-resolution","contract":"marketing-crm","summary":"Link a record to a case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CaseInvestigationResolutionWorkspaceInput","responds":"CaseInvestigationResolutionWorkspaceView"},
"setRefundCompensationService": {"method":"PUT","path":"/refund-compensation-service","contract":"marketing-crm","summary":"Raise or change a refund, compensation or policy-exception request on a case","permission":"ORDER_REFUND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RefundCompensationServiceExceptionWorkspaceInput","responds":"RefundCompensationServiceExceptionWorkspaceView"},
"setSlaPolicy": {"method":"PUT","path":"/sla-policies","contract":"marketing-crm","summary":"Define an SLA policy","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MarketingSlaPolicy","responds":"MarketingSlaPolicy"},
"updateCase": {"method":"PATCH","path":"/cases/{caseId}","contract":"marketing-crm","summary":"Assign, reprioritise or resolve a case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Case"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AgentWorkloadAvailabilityWorkforceControlView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.agent_service_profile (new), marketing.agent_availability, marketing.case, marketing.conversation, marketing.service_queue (new) and workforce.shift","description":"One agent's live status and workload. Rates are over the period since the agent's current shift started, or the venue's current day when no shift is rostered.","required":["principalId","agentName","status","activeCases"],"properties":{"principalId":{"type":"string","format":"uuid"},"agentName":{"type":"string","description":"The agent's display name."},"team":{"type":"string","nullable":true},"skills":{"type":"array","items":{"type":"string"}},"languages":{"type":"array","items":{"type":"string"}},"status":{"type":"string","enum":["available","busy","onCall","chatting","afterCallWork","break","training","offline"]},"activeCases":{"type":"integer","minimum":0},"chats":{"type":"integer","minimum":0,"description":"Conversations the agent holds now."},"calls":{"type":"integer","minimum":0,"description":"Voice conversations in progress (0 or 1)."},"queues":{"type":"array","items":{"type":"object","required":["queueId","queueName"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"type":"string"}}}},"slaRiskCases":{"type":"integer","minimum":0,"description":"The agent's open cases at risk or breached."},"averageHandleSeconds":{"type":"integer","minimum":0,"nullable":true},"resolutionRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Cases resolved over cases handled."},"utilization":{"type":"number","minimum":0,"description":"Active cases and conversations over `maxConcurrentCases`; above 1 means overloaded."},"workloadBand":{"type":"string","enum":["available","normal","overloaded"],"description":"`overloaded` at utilization 0.9 or above, `available` below 0.5."},"availabilityExpiresAt":{"type":"string","format":"date-time","nullable":true}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalSlaPolicy": {"type":"object","x-ticvai-persistence":"approvals.sla_policy","description":"Approvals boards 5.5 and 5.6. **A target with no consequence is a number in a table**, so the reminder and breach behaviour are part of the policy.\n","required":["code"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"appliesToRequestKinds":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalKind"}},"targetMinutes":{"type":"integer"},"businessHoursOnly":{"type":"boolean","default":true,"description":"**A four-hour SLA starting at five in the afternoon is breached by nine the next morning with nobody having done anything wrong.**\n"},"calendarId":{"type":"string","format":"uuid","nullable":true},"reminders":{"type":"array","items":{"type":"object","properties":{"atPercentOfTarget":{"type":"integer"},"notify":{"type":"string","enum":["approver","approverManager","requester","escalationGroup"]}}}},"firstReminderAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"**Percent of `targetMinutes` at which the first reminder goes** (decided 29 September, readiness close-out: the reminder steps are percentages of target). A column so the SLA, Escalation, Reminder & Timeout Rules screen reads it rather than unpacking `reminders`; the reminder in `reminders` at this percentage says whom it notifies (data model for the agreed operations, 29 September)."},"secondReminderAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Percent of `targetMinutes` at which the second reminder goes; above `firstReminderAtPercent`"},"escalateAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Percent of `targetMinutes` at which the request or workflow escalates; at or above `secondReminderAtPercent`"},"onBreach":{"type":"string","enum":["notifyOnly","escalate","autoApprove","autoReject"],"default":"escalate"},"autoActionAllowed":{"type":"boolean","default":false,"description":"**Auto-approval on breach is off unless somebody says otherwise, in writing.** A queue that approves itself when nobody looks is not an approval process.\n"},"escalationGroupId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"Case": {"x-ticvai-persistence":"marketing.case","x-ticvai-retired-columns":["guest_name","subject","is_sla_breached"],"type":"object","required":["id","caseNumber","subject","status","priority","createdAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."},"caseNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"},"subject":{"type":"string","x-ticvai-column":"title","description":"**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"},"kind":{"allOf":[{"$ref":"#/components/schemas/CaseKind"}],"nullable":true,"description":"What the guest said it was about, where the guest raised it."},"channel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"description":"How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised — the start of the SLA clock."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the case arrived. Equal to `recordedAt` for a case raised online."},"categoryId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"},"status":{"$ref":"#/components/schemas/CaseStatus"},"priority":{"$ref":"#/components/schemas/CasePriority"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"relatedOrderId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"isSlaBreached":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"},"slaPausedSeconds":{"type":"integer","description":"Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"},"escalationCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"CaseCategory": {"type":"object","x-ticvai-persistence":"marketing.case_category","description":"**The venue's case taxonomy**: categories and, under them, subcategories (`parentCategoryId`). `Case.categoryId` and the routing rules' `match.categoryIds` point here; `createCaseClassificationIntelligent` recommends one. Maintained by `setCaseCategoryDefinition`, read by `listCaseCategories` (decided 29 September, writers pass). (decided 29 September, data model for the agreed operations)\n","required":["id","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":60},"name":{"type":"string","maxLength":150},"parentCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Set on a subcategory; null on a top-level category."},"defaultPriority":{"allOf":[{"$ref":"#/components/schemas/CasePriority"}],"nullable":true,"description":"The priority a case in this category starts at before routing factors apply."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CaseDetail": {"x-ticvai-persistence":"marketing.case","allOf":[{"$ref":"#/components/schemas/Case"},{"type":"object","properties":{"description":{"type":"string"},"resolutionNote":{"type":"string","nullable":true},"messages":{"type":"array","items":{"$ref":"#/components/schemas/CaseMessage"}}}}]},
"CaseInvestigationResolutionWorkspaceInput": {"type":"object","x-ticvai-persistence":"marketing.case_linked_record","x-ticvai-record-definition":"Related Records (agents can attach)","description":"One link between a case and a record another contract owns. The reference is a pointer, never a copy.","required":["caseId","kind","referenceId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"caseId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["order","ticket","payment","refund","membership","walletTransaction","groupBooking","accessEvent"]},"referenceId":{"type":"string","maxLength":64,"description":"The record's id in its owning contract (orders, payments, access, wallet)."},"note":{"type":"string","maxLength":500,"nullable":true},"isActive":{"type":"boolean","default":true,"description":"False unlinks; the row stays for the audit trail."},"linkedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CaseInvestigationResolutionWorkspaceView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.case, marketing.case_message, marketing.case_linked_record (new), marketing.sla_policy and ai.suggestion","description":"The case workspace (pack 10.1.5). Recommended actions and the summary keep verified data, policy and AI recommendation apart.","required":["caseId","caseNumber","subject","priority","status","created","lastUpdated","linkedRecords","recommendedActions"],"properties":{"caseId":{"type":"string","format":"uuid"},"caseNumber":{"type":"string"},"subjectId":{"type":"string","format":"uuid","nullable":true},"customer":{"type":"string","nullable":true,"description":"The guest's name, as `Case.guestName`; null unless the caller holds GUEST_VIEW_PII."},"subject":{"type":"string"},"categoryId":{"type":"string","format":"uuid","nullable":true},"category":{"type":"string","nullable":true,"description":"The category's display name."},"priority":{"$ref":"#/components/schemas/CasePriority"},"status":{"$ref":"#/components/schemas/CaseStatus"},"sla":{"type":"object","properties":{"policyCode":{"type":"string","nullable":true},"dueAt":{"type":"string","format":"date-time","nullable":true},"remainingSeconds":{"type":"integer","nullable":true,"description":"Negative once breached."},"isBreached":{"type":"boolean"},"isPaused":{"type":"boolean","description":"True while `awaitingGuest`."}}},"owner":{"type":"string","format":"uuid","nullable":true,"description":"The assigned agent's principal id (`Case.assignedToPrincipalId`)."},"queue":{"type":"string","nullable":true},"created":{"type":"string","format":"date-time","description":"`Case.createdAt`."},"lastUpdated":{"type":"string","format":"date-time"},"linkedRecords":{"type":"array","description":"Active links, newest first.","items":{"$ref":"#/components/schemas/CaseInvestigationResolutionWorkspaceInput"}},"recommendedActions":{"type":"array","maxItems":10,"items":{"type":"object","required":["action","basis"],"properties":{"action":{"type":"string","enum":["reply","call","reschedule","exchange","reissue","requestRefund","requestCompensation","raiseInternalRequest","escalate","resolve"]},"basis":{"type":"string","enum":["verifiedData","policy","aiRecommendation"]},"reason":{"type":"string","maxLength":500},"policyReference":{"type":"string","nullable":true,"description":"The policy the action rests on; an AI recommendation never invents one."}}}},"aiSummary":{"type":"object","nullable":true,"description":"Where the AI policy enables `summarise`; AI-derived and labelled as such.","properties":{"issue":{"type":"string"},"policy":{"type":"string","nullable":true},"currentStatus":{"type":"string","nullable":true},"commercialImpact":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"recommendedAction":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"}}}}},
"CaseKind": {"type":"string","description":"**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n","enum":["lostProperty","complaint","question","accessibility","refundRequest","other"]},
"CaseMessage": {"x-ticvai-persistence":"marketing.case_message","type":"object","required":["id","body","isInternal","authorKind","recordedAt"],"properties":{"resolution":{"type":"string","description":"**What was actually done about it.** Indexed for retrieval: an agent facing a complaint benefits more from how the last one was resolved than from a policy. Without this column `marketing.case` can only embed its subject line.\n"},"id":{"type":"string"},"body":{"type":"string"},"isInternal":{"type":"boolean"},"authorKind":{"type":"string","enum":["agent","guest","system","ai"]},"authorPrincipalId":{"type":"string","format":"uuid","nullable":true},"channel":{"$ref":"#/components/schemas/MessageChannel"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time","description":"Device time — `addCaseMessage` is offline-capable."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the message arrived."}}},
"CasePriority": {"type":"string","enum":["low","normal","high","urgent"]},
"CaseStatus": {"type":"string","enum":["open","inProgress","awaitingGuest","escalated","resolved","closed"]},
"CreateCaseRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","subject","description","channel","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"subject":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":10000},"categoryId":{"type":"string","format":"uuid"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. Must belong to `subjectId` when both are given (422). (decided 29 September, coordinator decision DM4, writers pass)"},"priority":{"allOf":[{"$ref":"#/components/schemas/CasePriority"}],"default":"normal"},"kind":{"$ref":"#/components/schemas/CaseKind"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"venueId":{"type":"string","format":"uuid"},"relatedOrderId":{"type":"string"},"attachmentRefs":{"type":"array","description":"Stored on the opening `CaseMessage`, not on the case.","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised. The server stamps `Case.syncedAt` on arrival."}}},
"EscalationCriticalCaseMonitorView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.case, marketing.case_escalation (new, one row per escalateCase call) and the related order in orders","description":"One open escalated case, as of its latest escalation.","required":["caseId","caseNumber","reason","escalationType","priority","escalatedAt","status"],"properties":{"caseId":{"type":"string","format":"uuid"},"caseNumber":{"type":"string"},"subjectId":{"type":"string","format":"uuid","nullable":true},"customerName":{"type":"string","nullable":true,"description":"Resolved from `pii.subject`; null unless the caller holds `GUEST_VIEW_PII`."},"reason":{"type":"string","description":"The reason given to `escalateCase`, or `SLA breached` for an automatic escalation."},"reasonCategory":{"type":"string","nullable":true,"enum":["slaRisk","customerComplaint","repeatedContact","highValue","refundException","operationalFailure","systemFailure","legalCompliance","vipCustomer","supervisorRequested","other"]},"escalationType":{"type":"string","enum":["vip","financial","eventDay","management","technical","other"],"description":"`vip` for a VIP-tier customer, `financial` for a refund or high-value order, `eventDay` when the case's event is today, `management` when escalated to a manager, `technical` for a technical category; the first that applies, in that order."},"priority":{"$ref":"#/components/schemas/CasePriority"},"transactionValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"The related order's total, when the case has one."},"eventId":{"type":"string","format":"uuid","nullable":true},"eventName":{"type":"string","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"escalatedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"escalatedAt":{"type":"string","format":"date-time"},"escalationCount":{"type":"integer","minimum":1},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"isSlaBreached":{"type":"boolean"},"status":{"$ref":"#/components/schemas/CaseStatus"}}},
"MarketingSlaPolicy": {"type":"object","x-ticvai-persistence":"marketing.sla_policy","description":"**Taken from the backend workbook, 20 September.** Defines service-level response and resolution targets used by support cases.","required":["code","name","businessHoursOnly","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"scopePath":{"type":"string","nullable":true},"code":{"type":"string","maxLength":100},"name":{"type":"string","maxLength":150},"priority":{"type":"string","maxLength":20,"nullable":true},"firstResponseMinutes":{"type":"integer","nullable":true},"resolutionMinutes":{"type":"integer","nullable":true},"escalationMinutes":{"type":"integer","nullable":true},"businessHoursOnly":{"type":"boolean"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RefundCompensationServiceExceptionWorkspaceInput": {"type":"object","x-ticvai-persistence":"marketing.case_compensation_request","x-ticvai-record-definition":"Request Types","description":"One refund, compensation or policy-exception request raised from a case. The order, refund and approval are references, never copies.","required":["id","caseId","requestType","value","reason"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7; equals the `Idempotency-Key` header."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"caseId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"Required for `fullRefund`, `partialRefund`, `feeWaiver`, `upgrade` and `discount`."},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requestType":{"type":"string","enum":["fullRefund","partialRefund","serviceCredit","walletCredit","voucher","complimentaryTicket","feeWaiver","upgrade","discount","policyException"]},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"The money value requested; for a complimentary ticket or upgrade, its face value. This is what the approval thresholds are compared with."},"reason":{"type":"string","minLength":3,"maxLength":1000},"isPolicyException":{"type":"boolean","default":false,"description":"True when the standard policy would not allow it; always needs approval."},"exceptionReason":{"type":"string","maxLength":1000,"nullable":true,"description":"Required when `isPolicyException` is true."},"submit":{"type":"boolean","default":false,"description":"False saves a draft; true routes it.","writeOnly":true},"status":{"type":"string","readOnly":true,"enum":["draft","pendingApproval","approved","declined","fulfilled","failed","withdrawn"]},"approvalRequestId":{"type":"string","readOnly":true,"nullable":true},"fulfilmentOperation":{"type":"string","readOnly":true,"nullable":true,"description":"e.g. `createRefund`, `topUpWallet`."},"fulfilmentReference":{"type":"string","readOnly":true,"nullable":true,"description":"The refund, wallet transaction or voucher it produced."},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"RefundCompensationServiceExceptionWorkspaceView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.case_compensation_request (new), orders.sales_order, orders.refund, orders.order_fee, orders.refund_policy and approvals.request","description":"The request, the order's financial context, the policy evaluation and who must approve.","required":["request","approvalLevel"],"properties":{"request":{"$ref":"#/components/schemas/RefundCompensationServiceExceptionWorkspaceInput"},"originalTransaction":{"type":"string","nullable":true,"description":"The order number."},"amountPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amountUsed":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Value of tickets already scanned or consumed."},"refundableAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the refund policy's time bands allow now, less previous refunds."},"previousRefund":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"fees":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"proposedRefund":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"proposedCompensation":{"type":"object","nullable":true,"properties":{"requestType":{"type":"string"},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"policyEvaluation":{"type":"object","properties":{"standardPolicy":{"type":"string","description":"The rule that applies, as the venue's refund policy states it."},"isWithinPolicy":{"type":"boolean"},"policyReference":{"type":"string","nullable":true}}},"approvalLevel":{"type":"string","enum":["agent","secondUser","approver"],"description":"From the venue's `selfAuthoriseLimit`, `requiresSecondUserAbove` and `requiresApprovalAbove`; a policy exception is always `approver`."},"aiExplanation":{"type":"string","nullable":true,"maxLength":1000,"description":"AI-derived and labelled as such; cites a recorded policy or says none applies."}}},
"ServiceQueue": {"type":"object","x-ticvai-persistence":"marketing.service_queue","description":"**A customer-service queue** (e.g. `eventDaySupport`). Cases (`Case.queueId`), routing rules (`queueId`, `fallbackQueueId`) and agents (`AgentAvailability.queueIds`) name it; `listContact` and `listAgentWorkloadAvailability` report per queue. Maintained by `setServiceQueueDefinition`, read by `listServiceQueues` (decided 29 September, writers pass). (decided 29 September, data model for the agreed operations)\n","required":["id","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":60},"name":{"type":"string","maxLength":150},"overflowWaitSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"The queue's overflow threshold; a case waiting longer marks the queue `critical`."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"SlaPolicyServiceLevelManagementView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.case and marketing.sla_policy","description":"SLA performance for the filters given. Counts are of open cases for the state counts and of cases in the period for the averages and the compliance rate.","required":["withinSla","atRisk","breached","byPolicy"],"properties":{"withinSla":{"type":"integer","minimum":0},"atRisk":{"type":"integer","minimum":0},"breached":{"type":"integer","minimum":0},"averageResponseSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"Mean time to first response, less paused time."},"averageResolutionSeconds":{"type":"integer","minimum":0,"nullable":true},"slaComplianceRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Cases resolved in the period within target, over cases resolved in the period."},"byPolicy":{"type":"array","description":"One row per SLA policy that timed a case in the period, worst compliance first.","items":{"type":"object","required":["slaPolicyId","code","name","withinSla","atRisk","breached"],"properties":{"slaPolicyId":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"firstResponseMinutes":{"type":"integer","nullable":true},"resolutionMinutes":{"type":"integer","nullable":true},"withinSla":{"type":"integer","minimum":0},"atRisk":{"type":"integer","minimum":0},"breached":{"type":"integer","minimum":0},"slaComplianceRate":{"type":"number","minimum":0,"maximum":1,"nullable":true}}}},"forecastBreaches":{"type":"array","maxItems":50,"description":"AI forecast of open cases likely to breach before the static thresholds fire, soonest first. Advisory; empty when AI is disabled for the tenant.","items":{"type":"object","required":["caseCount","horizonMinutes"],"properties":{"queueId":{"type":"string","format":"uuid","nullable":true},"queueName":{"type":"string","nullable":true},"slaPolicyId":{"type":"string","format":"uuid","nullable":true},"caseCount":{"type":"integer","minimum":0},"horizonMinutes":{"type":"integer","minimum":1},"confidence":{"type":"number","minimum":0,"maximum":1}}}}}}
}
```
