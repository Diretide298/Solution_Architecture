# WS114 — ACCREDITATION board 7

**10 screens · 12 operations · 15 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `ACCREDITATION_CONFIGURE, ACCREDITATION_MANAGE, ACCREDITATION_VIEW, GUEST_MANAGE, MARKETING_SEND, MARKETING_VIEW, REPORT_EXPORT, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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
| `BO-674` | Accreditation Communications Command Center | B–D | 0 | 10 | 6 | 5 | 0 | 6 | — | notStarted (—) |
| `BO-675` | Notification Rule Management | B–D | 9 | 0 | 6 | 5 | 1 | 0 | — | notStarted (—) |
| `BO-676` | Expiry & Renewal Notification Scheduler | B–D | 6 | 0 | 6 | 5 | 0 | 0 | — | notStarted (—) |
| `BO-677` | Communication Template Library | B–D | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `BO-678` | Channel, Language & Branding Configuration | B–D | 10 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-679` | Manual & Bulk Communication Center | B–D | 0 | 0 | 6 | 8 | 0 | 0 | — | notStarted (—) |
| `BO-680` | Accreditation Bulk Import | B–D | 0 | 0 | 6 | 1 | 1 | 6 | — | notStarted (—) |
| `BO-681` | Import Validation & Processing Monitor | B–D | 0 | 20 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-682` | Accreditation Export & Data Extract Center | B–D | 7 | 0 | 6 | 14 | 0 | 6 | — | notStarted (—) |
| `BO-683` | Delivery, Batch & Operational History | B–D | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-674, BO-677, BO-679, BO-680, BO-681, BO-683 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-674` Accreditation Communications Command Center

**Central dashboard for accreditation notifications and operational communications.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Dashboard analytics shall show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-communications-command-center-bo-674` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every accreditation communications** (data table)

| Shows | Format | Notes |
|---|---|---|
| Delivery success rate | text | not in the schema: `Delivery success rate` |
| Notifications by type | text | not in the schema: `Notifications by type` |
| Notifications by channel | text | not in the schema: `Notifications by channel` |
| Failure trends | text | not in the schema: `Failure trends` |
| Upcoming scheduled communications | text | not in the schema: `Upcoming scheduled communications` |

**The selected accreditation communications** (detail panel): The pack groups this record's detail under its own headings: “Scope of Work”, “Key requirements”.

| Shows | Format | Notes |
|---|---|---|
| Delivery success rate | text | not in the schema: `Delivery success rate` |
| Notifications by type | text | not in the schema: `Notifications by type` |
| Notifications by channel | text | not in the schema: `Notifications by channel` |
| Failure trends | text | not in the schema: `Failure trends` |
| Upcoming scheduled communications | text | not in the schema: `Upcoming scheduled communications` |

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-675` Notification Rule Management: *Notification Rule Management*
- → `BO-676` Expiry & Renewal Notification Scheduler: *Expiry & Renewal Notification Scheduler*
- → `BO-677` Communication Template Library: *Communication Template Library*
- → `BO-678` Channel, Language & Branding Configuration: *Channel, Language & Branding Configuration*
- → `BO-679` Manual & Bulk Communication Center: *Manual & Bulk Communication Center*
- → `BO-680` Accreditation Bulk Import: *Accreditation Bulk Import*
- → `BO-681` Import Validation & Processing Monitor: *Import Validation & Processing Monitor*
- → `BO-682` Accreditation Export & Data Extract Center: *Accreditation Export & Data Extract Center*
- → `BO-683` Delivery, Batch & Operational History: *Delivery, Batch & Operational History*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation communications list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation communications untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation communications yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation communications are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setAccreditationNotificationRules` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.36 | Accreditation Expiry Notifications - System shall notify users before accreditation expiration. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.43 | Accreditation Notifications - System shall send accreditation status notifications. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.44 | Approval Notifications - System shall notify applicants of approval decisions. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.45 | Renewal Notifications - System shall notify users of upcoming renewals. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.46 | Expiration Notifications - System shall notify users of upcoming expirations. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-674` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-674`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 1: Opens Accreditation Communications Command Center → Central dashboard for accreditation notifications and operational communications.
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F223 branch at step 1 (expected): when Nothing has been set up on Accreditation Communications Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F223 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-674?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-675`, `BO-676`, `BO-677`, `BO-678`, `BO-679`, `BO-680`, `BO-681`, `BO-682`, `BO-683`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-675` Notification Rule Management

**Configure when accreditation notifications are automatically triggered.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Each rule shall define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/notification-rule-management-bo-675` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Trigger | select field | — | — | — | — | — | — |
| Recipient | select field | — | — | — | — | — | — |
| Communication channel | select field | — | — | — | — | — | — |
| Template | select field | — | — | — | — | — | — |
| Timing | select field | — | — | — | — | — | — |
| Event/program scope | select field | — | — | — | — | — | — |
| Category | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Active/inactive status | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The notification rule configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the notification rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No notification rule configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setAccreditationNotificationRules` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.36 | Accreditation Expiry Notifications - System shall notify users before accreditation expiration. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.43 | Accreditation Notifications - System shall send accreditation status notifications. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.44 | Approval Notifications - System shall notify applicants of approval decisions. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.45 | Renewal Notifications - System shall notify users of upcoming renewals. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.46 | Expiration Notifications - System shall notify users of upcoming expirations. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Lifecycle: activation, expiry, renewal, suspension; if a document (e.g. Emirates ID) expires before the event, a resubmission request is raised and the credential is blocked if unresolved. Applicants are notified at each status change (approved, rejected, needs validation). *(client request · MoM 7 Sep 2026, 4.6 / 4.7 Lifecycle & Notifications · DI-663)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-675` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-675`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 2: Works in Notification Rule Management → Configure when accreditation notifications are automatically triggered.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-675?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-676` Expiry & Renewal Notification Scheduler

**Configure proactive reminders before accreditation expiry or renewal.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/expiry-renewal-notification-scheduler-bo-676` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Days before/after event | select field | — | — | — | — | — | — |
| Recipient | select field | — | — | — | — | — | — |
| Template | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Escalation rule | select field | — | — | — | — | — | — |
| Retry policy | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The expiry renewal notification configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the expiry renewal notification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No expiry renewal notification configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setAccreditationNotificationRules` → `ACCREDITATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.36 | Accreditation Expiry Notifications - System shall notify users before accreditation expiration. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.43 | Accreditation Notifications - System shall send accreditation status notifications. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.44 | Approval Notifications - System shall notify applicants of approval decisions. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.45 | Renewal Notifications - System shall notify users of upcoming renewals. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |
| 12.1.46 | Expiration Notifications - System shall notify users of upcoming expirations. | Accreditation & Credential Management | CONTRACTED | `setAccreditationNotificationRules` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-676` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-676`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 4: Works in Expiry & Renewal Notification Scheduler → Configure proactive reminders before accreditation expiry or renewal.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-676?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Every gated control is gated: `ACCREDITATION_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-677` Communication Template Library

**Manage reusable accreditation communication templates.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/communication-template-library-bo-677` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listMessageTemplates` ?channel |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listMessageTemplates` (onLoad, Template library)

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The communication template list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the communication template untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No communication template yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the communication template are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listMessageTemplates` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.3 | The system should support email templates for e-ticket purchase confirmation supporting dynamic parameters. The email templates should be configurable per site, per event | Ticketing Sales | CONTRACTED | `listMessageTemplates` |
| 2.6.26 | It is expected that confirmation email can be generated including the number of tickets, the cost, the order number. | Ticketing Sales | CONTRACTED | `listMessageTemplates` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-677` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-677`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 6: Works in Communication Template Library → Manage reusable accreditation communication templates.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-677?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-678` Channel, Language & Branding Configuration

**Control how communications are delivered and branded.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/channel-language-branding-configuration-bo-678` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Sender identity | select field | — | — | — | — | — | — |
| Reply information | select field | — | — | — | — | — | — |
| Default language | select field | — | — | — | — | — | — |
| Alternative languages | select field | — | — | — | — | — | — |
| Tenant logo | select field | — | — | — | — | — | — |
| Event branding | select field | — | — | — | — | — | — |
| Venue branding | select field | — | — | — | — | — | — |
| Header/footer | select field | — | — | — | — | — | — |
| Contact information | select field | — | — | — | — | — | — |
| Key requirement: 12.1.57 | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel language branding configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel language branding untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel language branding configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A language of a published version was changed.; 422 An approval without a human reviewer, or approved by the translator. |

#### Permissions

- `setLocalizationBrandingCustomer` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-678` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-678`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 8: Works in Channel, Language & Branding Configuration → Control how communications are delivered and branded.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-678?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Every gated control is gated: `GUEST_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-679` Manual & Bulk Communication Center

**Allow authorized operators to communicate with selected accreditation populations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_SEND` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/manual-bulk-communication-center-bo-679` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Send transactional message (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The manual bulk communication list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the manual bulk communication untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No manual bulk communication yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the manual bulk communication are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Address suppressed, or the guest has no address for that channel |

#### Permissions

- `sendTransactionalMessage` → `MARKETING_SEND` (operate) · service, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.61 | Reservation Notifications - System shall provide reservation reminders. | Guest Mobile App & Branding | CONTRACTED | `sendTransactionalMessage` |
| 19.2.62 | Ticket Notifications - System shall provide ticket reminders. | Guest Mobile App & Branding | CONTRACTED | `sendTransactionalMessage` |
| 19.2.64 | Operational Notifications - System shall provide operational notifications. | Guest Mobile App & Branding | CONTRACTED | `sendTransactionalMessage` |
| 2.7.21 | It is expected that confirmation email can be generated; the email shall include relevant visit information such as the number of tickets, the cost, the order number. | Ticketing Sales | CONTRACTED | `sendTransactionalMessage` |
| 4.4.8 | The system should be able to reduce the use of paper and send out receipts via phone as SMS or whatsapp or email for all transactions. | Bundles and Promotions | CONTRACTED | `sendTransactionalMessage` |
| 4.6.14 | The system should be able to reduce the use of paper and send out receipts via phone or email for all transactions. | Bundles and Promotions | CONTRACTED | `sendTransactionalMessage` |
| 13.3.15 | APIs shall support email, SMS, push notifications, WhatsApp notifications and notification status retrieval. | Developer & API Management | CONTRACTED | `sendTransactionalMessage` |
| 22.9.2 | Multi-Channel Delivery | Marketing & CRM | CONTRACTED | `sendTransactionalMessage` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-679` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-679`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 10: Works in Manual & Bulk Communication Center → Allow authorized operators to communicate with selected accreditation populations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-679?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Send transactional message, Cancel.
- [ ] Every transition is wired: `BO-674`.
- [ ] Every gated control is gated: `MARKETING_SEND`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-680` Accreditation Bulk Import

**Import accreditation records at scale.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-bulk-import-bo-680` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Import accreditation holders (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation bulk import list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation bulk import untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation bulk import yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation bulk import are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `importAccreditationHolders` → `ACCREDITATION_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.54 | Accreditation Import - System shall support bulk import of accreditation records. | Accreditation & Credential Management | CONTRACTED | `importAccreditationHolders` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Bulk: a company with many members (e.g. 1,000) gets an Excel template to submit all details and documents at once; each imported record still goes through profile, documents and approval. *(client request · MoM 7 Sep 2026, 4.7 Notifications, Bulk Operations & Analytics · DI-664)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-680` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-680`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 12: Works in Accreditation Bulk Import → Import accreditation records at scale.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-680?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Import accreditation holders, Cancel.
- [ ] Every transition is wired: `BO-674`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-681` Import Validation & Processing Monitor

**Govern and monitor bulk accreditation imports.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§The screen shall display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/import-validation-processing-monitor-bo-681` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every import validation processing** (data table)

| Shows | Format | Notes |
|---|---|---|
| Import batch ID | text | not in the schema: `Import batch ID` |
| File name | text | not in the schema: `File name` |
| Uploaded by | text | not in the schema: `Uploaded by` |
| Upload date/time | text | not in the schema: `Upload date/time` |
| Total records | text | not in the schema: `Total records` |
| Valid records | text | not in the schema: `Valid records` |
| Warning records | text | not in the schema: `Warning records` |
| Failed records | text | not in the schema: `Failed records` |
| Duplicate records | text | not in the schema: `Duplicate records` |
| Processing status | text | not in the schema: `Processing status` |

**The selected import validation processing** (detail panel): The pack groups this record's detail under its own headings: “Processing statuses shall include”.

| Shows | Format | Notes |
|---|---|---|
| Import batch ID | text | not in the schema: `Import batch ID` |
| File name | text | not in the schema: `File name` |
| Uploaded by | text | not in the schema: `Uploaded by` |
| Upload date/time | text | not in the schema: `Upload date/time` |
| Total records | text | not in the schema: `Total records` |
| Valid records | text | not in the schema: `Valid records` |
| Warning records | text | not in the schema: `Warning records` |
| Failed records | text | not in the schema: `Failed records` |
| Duplicate records | text | not in the schema: `Duplicate records` |
| Processing status | text | not in the schema: `Processing status` |

**Data it reads**: `importAccreditationHolders` (onLoad, Validation and processing)

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The import validation processing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the import validation processing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No import validation processing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the import validation processing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `importAccreditationHolders` → `ACCREDITATION_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.54 | Accreditation Import - System shall support bulk import of accreditation records. | Accreditation & Credential Management | CONTRACTED | `importAccreditationHolders` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-681` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-681`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 14: Works in Import Validation & Processing Monitor → Govern and monitor bulk accreditation imports.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-681?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-682` Accreditation Export & Data Extract Center

**Export authorized accreditation data for operational or reporting purposes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_MANAGE`, `ACCREDITATION_VIEW`, `REPORT_EXPORT`, `REPORT_VIEW_VENUE` (1 configure, 2 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§The system shall capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `executionId` (navigation), `exportId` (navigation), `reportId` (navigation) |
| Route | `/access-venue/accreditation-export-data-extract-center-bo-682` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Requested by | select field | — | — | — | — | — | — |
| Export date/time | select field | — | — | — | — | — | — |
| Filters | select field | — | — | — | — | — | — |
| Fields exported | select field | — | — | — | — | — | — |
| Number of records | select field | — | — | — | — | — | — |
| Export status | select field | — | — | — | — | — | — |
| Key requirement: 12.1.55 | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listAccreditationHolders` ?programmeId |
| Organisation | picker: choose an organisation | — | — | `listAccreditationHolders` ?organisationId |
| Status | text field | — | — | `listAccreditationHolders` ?status |
| Expiring within days | number field (days) | — | — | `listAccreditationHolders` ?expiringWithinDays |
| Status | text field | — | — | `listAccreditationExports` ?status |

#### Outputs: what the screen shows and produces

**Data it reads**: `listAccreditationHolders` (onLoad, Export); `listAccreditationExports` (onLoad, Export history: requested by, date, filters, fields …)

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation export data configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation export data untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation export data configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 422 Personal data requested without a purpose |

#### Permissions

- `listAccreditationHolders` → `ACCREDITATION_VIEW` (read) · staff
- `listAccreditationExports` → `ACCREDITATION_MANAGE` (configure) · staff
- `exportAccreditationData` → `ACCREDITATION_MANAGE` (configure) · staff
- `getAccreditationExport` → `ACCREDITATION_MANAGE` (configure) · staff
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `exportReportResult` → `REPORT_EXPORT` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.7 | Accreditation Reporting System shall provide reports on active, expired and revoked accreditations. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.47 | Accreditation Dashboard - System shall provide accreditation dashboards. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.52 | Accreditation API - System shall expose accreditation functionality through APIs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.55 | Accreditation Export - System shall support export of accreditation data. | Accreditation & Credential Management | CONTRACTED | `exportAccreditationData` |
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |
| 6.1.20 | The system should be able to all reporting functions should have export option to multiple file formats; minimum of PDF, Excel, delimited text, and XML. | Retail POS | CONTRACTED | `exportReportResult` |
| 6.1.26 | The system should be able to view/export (as CSV) user data. | Retail POS | CONTRACTED | `exportReportResult` |
| 8.7.18 | System shall support report exports to Excel. | Unified Operations Dashboard | CONTRACTED | `exportReportResult` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-682` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-682`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 16: Works in Accreditation Export & Data Extract Center → Export authorized accreditation data for operational or reporting purposes.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-682?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Every gated control is gated: `ACCREDITATION_MANAGE`, `ACCREDITATION_VIEW`, `REPORT_EXPORT`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-683` Delivery, Batch & Operational History

**Provide a consolidated history of notifications, communications, imports and exports.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/delivery-batch-operational-history-bo-683` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Holder | picker: choose a holder | — | — | `listAccreditationAudit` ?holderId |
| From | date and time picker | — | — | `listAccreditationAudit` ?from |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listAccreditationAudit` (onLoad, Import and export audit)

**Where the user goes next**

- → `BO-674` Accreditation Communications Command Center: *Back to Accreditation Communications Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The delivery batch operational list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the delivery batch operational untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No delivery batch operational yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the delivery batch operational are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAccreditationAudit` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.51 | Accreditation Audit Reporting - System shall provide accreditation audit reports. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |
| 12.1.58 | Accreditation Audit Logs - System shall maintain immutable accreditation audit logs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-683` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS07 ACCREDITATION Board 7.dc.html#bo-683`
- Workshop pack: ACCREDITATION.pdf board 7
- Flow F223 *ACCREDITATION board 7: Accreditation Communications Command Center*, step 18: Works in Delivery, Batch & Operational History → Provide a consolidated history of notifications, communications, imports and exports.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-683?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-674`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"exportAccreditationData": {"method":"POST","path":"/accreditation-exports","contract":"accreditation","summary":"Export holders, applications, credentials or access assignments","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationDataExport","responds":null},
"exportReportResult": {"method":"POST","path":"/report-executions/{executionId}/export","contract":"reporting","summary":"Export a completed result","permission":"REPORT_EXPORT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getAccreditationExport": {"method":"GET","path":"/accreditation-exports/{exportId}","contract":"accreditation","summary":"One export, and its download link once ready","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AccreditationDataExport"},
"importAccreditationHolders": {"method":"POST","path":"/accreditation-imports","contract":"accreditation","summary":"Load a roster supplied by an organisation","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccreditationImportResult"},
"listAccreditationAudit": {"method":"GET","path":"/accreditation-audit","contract":"accreditation","summary":"The immutable record of who granted what to whom","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"holderId","in":"query","required":null},{"name":"from","in":"query","required":null}],"requestBody":null,"responds":"AccreditationAuditRecord"},
"listAccreditationExports": {"method":"GET","path":"/accreditation-exports","contract":"accreditation","summary":"Exports taken, by whom, of what","permission":"ACCREDITATION_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAccreditationHolders": {"method":"GET","path":"/accreditation-holders","contract":"accreditation","summary":"Everybody accredited, and what state they are in","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":null},{"name":"organisationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"expiringWithinDays","in":"query","required":null}],"requestBody":null,"responds":"AccreditationHolder"},
"listMessageTemplates": {"method":"GET","path":"/message-templates","contract":"marketing-crm","summary":"List message templates","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"runReport": {"method":"POST","path":"/reports/{reportId}/run","contract":"reporting","summary":"Run a report","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RunReportRequest","responds":"ReportResult"},
"sendTransactionalMessage": {"method":"POST","path":"/messages","contract":"marketing-crm","summary":"Send a transactional message","permission":"MARKETING_SEND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setAccreditationNotificationRules": {"method":"PUT","path":"/accreditation-notifications","contract":"accreditation","summary":"Who is told what, and when","permission":"ACCREDITATION_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccreditationNotificationRules","responds":"AccreditationNotificationRules"},
"setLocalizationBrandingCustomer": {"method":"PUT","path":"/localization-branding-customer","contract":"marketing-crm","summary":"Set a waiver version's languages, branding and channels","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LocalizationBrandingCustomerExperienceConfigurationInput","responds":"LocalizationBrandingCustomerExperienceConfigurationView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccreditationAuditRecord": {"type":"object","x-ticvai-persistence":"accreditation.audit","description":"Board 8.7. **Who gave this person access to that place, when, and on whose authority.**\n","properties":{"id":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"holderId":{"type":"string","format":"uuid","nullable":true},"action":{"type":"string"},"actorPrincipalId":{"type":"string","format":"uuid","nullable":true},"previousValue":{"nullable":true},"newValue":{"nullable":true},"reason":{"type":"string","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"previousRecordHash":{"type":"string","nullable":true},"recordHash":{"type":"string"},"integrity":{"type":"string","readOnly":true,"enum":["intact","broken","unverifiable"]},"scopePath":{"type":"string"}}},
"AccreditationDataExport": {"type":"object","x-ticvai-persistence":"accreditation.data_export","description":"12.1.55. **A spreadsheet of accredited people leaving the platform is an event someone should own.** Requested by `exportAccreditationData`, listed for BO-682, and fetched once `ready`.\n","required":["dataset","format"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"dataset":{"type":"string","enum":["holders","applications","credentials","accessAssignments","documents"]},"format":{"type":"string","enum":["csv","xlsx"]},"programmeId":{"type":"string","format":"uuid","nullable":true},"statusFilter":{"type":"string","nullable":true},"organisationId":{"type":"string","format":"uuid","nullable":true},"categoryCode":{"type":"string","nullable":true},"validOn":{"type":"string","format":"date","nullable":true,"description":"Only accreditations valid on this date — the register for one performance"},"fields":{"type":"array","description":"The columns wanted. Omitted means the dataset's standard set","items":{"type":"string"}},"includePersonalData":{"type":"boolean","default":false,"description":"Contact details, date of birth, nationality and document references. Requires REPORT_EXPORT_PII and a purpose; recorded in the accreditation audit trail"},"purpose":{"type":"string","maxLength":500,"nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"requestedAt":{"type":"string","format":"date-time","readOnly":true},"recordCount":{"type":"integer","nullable":true,"readOnly":true},"status":{"type":"string","readOnly":true,"enum":["queued","running","ready","failed","expired"]},"downloadUrl":{"type":"string","nullable":true,"readOnly":true,"description":"Signed and expiring"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string"}}},
"AccreditationHolder": {"type":"object","x-ticvai-persistence":"accreditation.holder","description":"**A subject who may never sign in to anything.** `identity` owns principals; this owns accredited people.\n","required":["id","fullName"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"accreditationNumber":{"type":"string"},"fullName":{"type":"string"},"photoAssetId":{"type":"string","format":"uuid","nullable":true},"dateOfBirth":{"type":"string","format":"date","nullable":true},"nationality":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true,"description":"12.1.16. The holder's own address — where a mobile credential and renewal notices go"},"phone":{"type":"string","nullable":true,"description":"12.1.16. E.164"},"identityDocumentVerified":{"type":"boolean","default":false},"organisationId":{"type":"string","format":"uuid","nullable":true},"affiliationRole":{"type":"string","nullable":true},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"status":{"type":"string","enum":["active","suspended","revoked","expired","archived"]},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"completenessPercent":{"type":"integer","readOnly":true},"scopePath":{"type":"string"}}},
"AccreditationImportResult": {"type":"object","description":"Board 7.8. **A bulk import is exactly where the same person gets accredited twice.**\n","properties":{"rowsRead":{"type":"integer"},"created":{"type":"integer"},"updated":{"type":"integer"},"rejected":{"type":"integer"},"identityConflicts":{"type":"integer"},"rows":{"type":"array","items":{"type":"object","properties":{"row":{"type":"integer"},"name":{"type":"string"},"outcome":{"type":"string"},"detail":{"type":"string","nullable":true}}}},"committed":{"type":"boolean"}}},
"AccreditationNotificationRules": {"type":"object","x-ticvai-persistence":"accreditation.notification_rules","description":"Board 7.2. **Notices go to the organisation as well as the holder.**","properties":{"programmeId":{"type":"string","format":"uuid"},"rules":{"type":"array","items":{"type":"object","properties":{"event":{"type":"string","enum":["applicationReceived","informationRequested","approved","rejected","credentialReady","expiringSoon","renewalWindowOpen","expired","suspended","revoked"]},"daysBefore":{"type":"integer","nullable":true},"recipients":{"type":"array","items":{"type":"string","enum":["holder","organisation","sponsor","accreditationTeam"]}},"channels":{"type":"array","items":{"type":"string"}},"templateId":{"type":"string","format":"uuid","nullable":true}}}},"scopePath":{"type":"string"}}},
"ExportFormat": {"type":"string","enum":["csv","xlsx","pdf","json"]},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"LocalizationBrandingCustomerExperienceConfigurationInput": {"description":"The request body of `setLocalizationBrandingCustomer`, the record itself; read-only properties are ignored.","allOf":[{"$ref":"#/components/schemas/LocalizationBrandingCustomerExperienceConfigurationView"}]},
"LocalizationBrandingCustomerExperienceConfigurationView": {"type":"object","x-ticvai-persistence":"marketing.waiver_localisation","description":"Languages, branding and channels of one waiver version (pack 11.1.9), keyed on `formId` + `formVersion`.","required":["formId","formVersion","sourceLanguage","languages"],"properties":{"formId":{"type":"string","format":"uuid"},"formVersion":{"type":"integer","minimum":1},"sourceLanguage":{"type":"string","maxLength":10,"description":"The language the legal text is written and reviewed in."},"languages":{"type":"array","minItems":1,"description":"Every language the version is offered in, the source language included. Arabic renders right to left.","items":{"type":"object","required":["language","required","translationStatus","approvalStatus"],"properties":{"language":{"type":"string","maxLength":10},"required":{"type":"boolean","description":"Publication waits for this language's approval."},"translationStatus":{"type":"string","enum":["notStarted","aiDrafted","inTranslation","inReview","complete"]},"translatorUserId":{"type":"string","format":"uuid","nullable":true},"reviewerUserId":{"type":"string","format":"uuid","nullable":true},"approvalStatus":{"type":"string","enum":["pending","approved","rejected"]},"lastUpdated":{"type":"string","format":"date-time","readOnly":true}}}},"branding":{"type":"object","properties":{"brandLogoAssetId":{"type":"string","format":"uuid","nullable":true},"venueLogoAssetId":{"type":"string","format":"uuid","nullable":true},"themeId":{"type":"string","nullable":true,"description":"The white-label theme it takes colours and typography from."},"header":{"$ref":"#/components/schemas/LocalisedText"},"footer":{"$ref":"#/components/schemas/LocalisedText"},"customerInstructions":{"$ref":"#/components/schemas/LocalisedText"},"confirmationMessage":{"$ref":"#/components/schemas/LocalisedText"},"supportEmail":{"type":"string","format":"email","nullable":true},"supportPhone":{"type":"string","maxLength":30,"nullable":true}}},"channels":{"type":"array","items":{"type":"string","enum":["b2cWeb","mobileApp","emailLink","qrLink","kiosk","posFrontDesk","groupPortal"]},"description":"Where the waiver is offered; every channel renders the same version and rules."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MessageTemplate": {"x-ticvai-persistence":"marketing.message_template","type":"object","required":["id","code","name","channel","bodies"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"channel":{"$ref":"#/components/schemas/MessageChannel"},"subjects":{"type":"object","description":"Per language. Email only.","additionalProperties":{"type":"string"}},"bodies":{"type":"object","description":"Per language, keyed by ISO 639-1 code.","additionalProperties":{"type":"string"}},"mergeFields":{"type":"array","items":{"type":"string"}},"missingLanguages":{"type":"array","readOnly":true,"description":"Enabled languages without a body. Flagged rather than silently falling back — a guest receiving English when they chose Arabic is a defect.\n","items":{"type":"string"}},"providerTemplateId":{"type":"string","nullable":true,"description":"Required for WhatsApp, where templates are pre-approved by the provider."},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand whose identity the template carries; null for the tenant default."},"ownership":{"type":"string","enum":["platform","crm"],"default":"crm","description":"`platform` = a transactional template owned by the communication service; `crm` = a marketing template owned by CRM (`listSystemTransactionalTemplate`). Content by language and version is in `MessageTemplateVersion`. (decided 29 September, data model for the agreed operations)"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"RunReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","properties":{"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"},"venueId":{"type":"string","format":"uuid","description":"Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"},"dateFrom":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."},"dateTo":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (audit R158)."},"forceAsync":{"type":"boolean","default":false,"description":"Queue regardless of size, for a result to be collected later."}}}
}
```
