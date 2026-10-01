# WS157 — Resource Management Configuration board 3

**10 screens · 30 operations · 30 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `RESOURCE_CONFIGURE, RESOURCE_MANAGE, RESOURCE_VIEW, USER_MANAGE, WORKFORCE_MANAGE, WORKFORCE_VIEW`. A control nobody can use must say so,
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
| `BO-873` | Staff Resource Directory | B–D | 2 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-874` | Staff Resource Profile | B–D | 11 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-875` | Skills & Competency Management | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-876` | Certification & Expiry Management | B–D | 10 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-877` | Qualification & Assignment Rule Engine | A | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-878` | Staff Availability & Working Pattern | B–D | 21 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-879` | Shift Template & Assignment Configuration | B–D | 6 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-880` | Break, Leave & Absence Configuration | B–D | 9 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-881` | Overtime & Working-Hour Rules | B–D | 7 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-882` | Workforce Integration & Synchronization Center | B–D | 0 | 16 | 6 | 9 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-873, BO-875, BO-877 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-873` Staff Resource Directory

**Provide the centralized master directory for all personnel who may be assigned as operational resources within TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `USER_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/staff-resource-directory-bo-873` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search staff resource | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, department, role, staff type, skill, certification and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Scope path | text field | — | — | `listPrincipals` ?scopePath |
| Is active | toggle | — | — | `listPrincipals` ?isActive |

#### Outputs: what the screen shows and produces

**Data it reads**: `listPrincipals` (onLoad, The staff directory)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-874` Staff Resource Profile: *Staff Resource Profile*
- → `BO-875` Skills & Competency Management: *Skills & Competency Management*
- → `BO-876` Certification & Expiry Management: *Certification & Expiry Management*
- → `BO-877` Qualification & Assignment Rule Engine: *Qualification & Assignment Rule Engine*
- → `BO-878` Staff Availability & Working Pattern: *Staff Availability & Working Pattern*
- → `BO-879` Shift Template & Assignment Configuration: *Shift Template & Assignment Configuration*
- → `BO-880` Break, Leave & Absence Configuration: *Break, Leave & Absence Configuration*
- → `BO-881` Overtime & Working-Hour Rules: *Overtime & Working-Hour Rules*
- → `BO-882` Workforce Integration & Synchronization Center: *Workforce Integration & Synchronization Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staff resource list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staff resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staff resource yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the staff resource are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPrincipals` → `USER_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Personnel (cashiers, trainers, drivers, other staff) are a resource type; command-centre view shows total personnel and how many are on duty, available or on leave. A staff profile's operational summary lists associated bookings. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-485)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-873` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-873`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 1: Opens Staff Resource Directory → Provide the centralized master directory for all personnel who may be assigned as operational resources within TICVAI.
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F266 branch at step 1 (expected): when Nothing has been set up on Staff Resource Directory yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F266 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-873?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-874`, `BO-875`, `BO-876`, `BO-877`, `BO-878`, `BO-879`, `BO-880`, `BO-881`, `BO-882`.
- [ ] Every gated control is gated: `USER_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-874` Staff Resource Profile

**Maintain the operational resource profile for an individual employee or contractor. This profile shall complement the organization's HR employee record rather than unnecessarily duplicate an HR system.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_VIEW`, `USER_MANAGE`, `WORKFORCE_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `principalId` (session), `employeeId` (BO-873) · cold entry: Opened from BO-873 with the employee picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says … |
| Route | `/rentals/staff-resource-profile-bo-874` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Resource priority | select field | — | — | — | — | — | — |
| Customer selectable yes/no | select field | — | — | — | — | — | — |
| Individual selection allowed yes/no | text field | — | — | — | — | — | — |
| Bookable yes/no | select field | — | — | — | — | — | — |
| Scheduling enabled yes/no | select field | — | — | — | — | — | — |
| Maximum concurrent assignment | select field | — | — | — | — | — | — |
| Default assignment duration | select field | — | — | — | — | — | — |
| Preferred operating area | select field | — | — | — | — | — | — |
| Languages | select field | — | — | — | — | — | — |
| Tags | select field | — | — | — | — | — | — |
| Employment Classification | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Cabana · Lounger · Locker · Wheelchair · Stroller · Equipment · Room · Auditorium · Vehicle · Instructor · Staff · Table … | `listResources` ?kind |
| Available from | date and time picker | — | — | `listResources` ?availableFrom |
| Available to | date and time picker | — | — | `listResources` ?availableTo |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| External agency (primary button) | navigation or local | — | — | — | — |
| External employee ID (secondary button) | navigation or local | — | — | — | — |
| Source system (secondary button) | navigation or local | — | — | — | — |
| Synchronization status (secondary button) | navigation or local | — | — | — | — |
| Last synchronization (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getPrincipal` (onLoad, One person); `listResources` (onLoad, Them as a bookable resource)

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staff resource profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staff resource profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staff resource profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getPrincipal` → `USER_MANAGE` (configure) · staff, partner
- `listResources` → `RESOURCE_VIEW` (read) · staff
- `getEmployee` → `WORKFORCE_VIEW` (read) · staff
- `listIntegrationSources` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Personnel (cashiers, trainers, drivers, other staff) are a resource type; command-centre view shows total personnel and how many are on duty, available or on leave. A staff profile's operational summary lists associated bookings. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-485)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-874` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-874`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 2: Works in Staff Resource Profile → Maintain the operational resource profile for an individual employee or contractor. This profile shall complement the organization's HR employee record rather than unnecessarily duplicate an HR …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-874?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: External agency, External employee ID, Source system, Synchronization status, Last synchronization.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`, `USER_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-875` Skills & Competency Management

**Define what each staff resource is capable of performing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/skills-competency-management-bo-875` |

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

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The skills competency list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the skills competency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No skills competency yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the skills competency are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setResourceQualifications` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Skills & competency define qualifications required for a role (e.g. level 1/2/3 ski-instructor certification for an advanced trainer); certification expiry tracking flags when recertification is due (e.g. annual renewal). *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-486)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-875` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-875`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 4: Works in Skills & Competency Management → Define what each staff resource is capable of performing.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-875?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-876` Certification & Expiry Management

**Manage certifications, licenses and credentials required for staff assignments.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `WORKFORCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/certification-expiry-management-bo-876` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Certification code | select field | — | — | — | — | — | — |
| Certification name | select field | — | — | — | — | — | — |
| Issuing authority | select field | — | — | — | — | — | — |
| Applicable roles | select field | — | — | — | — | — | — |
| Applicable resource types | select field | — | — | — | — | — | — |
| Applicable venues | select field | — | — | — | — | — | — |
| Validity period | select field | — | — | — | — | — | — |
| Renewal requirements | select field | — | — | — | — | — | — |
| Mandatory/optional | select field | — | — | — | — | — | — |
| Warning period | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `validateWorkforceCompliance` ?from |
| To | date picker | — | — | `validateWorkforceCompliance` ?to |

#### Outputs: what the screen shows and produces

**Data it reads**: `validateWorkforceCompliance` (onLoad, What has lapsed)

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The certification expiry configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the certification expiry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No certification expiry configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setResourceQualifications` → `RESOURCE_MANAGE` (configure) · staff
- `validateWorkforceCompliance` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Skills & competency define qualifications required for a role (e.g. level 1/2/3 ski-instructor certification for an advanced trainer); certification expiry tracking flags when recertification is due (e.g. annual renewal). *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-486)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-876` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-876`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 6: Works in Certification & Expiry Management → Manage certifications, licenses and credentials required for staff assignments.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-876?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-877` Qualification & Assignment Rule Engine

**Convert skills, certifications and operational policies into machine-enforceable assignment rules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block A · ticket #20731 (APP-SETUP-BO-877) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_MANAGE`, `RESOURCE_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `resourceId` (navigation), `experienceId` (navigation) · cold entry: Opened from BO-873 with the experience picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and … |
| Route | `/rentals/qualification-assignment-rule-engine-bo-877` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Resource type | picker: choose a resource type | — | — | `suggestResources` ?resourceTypeId |
| From | date and time picker | — | — | `suggestResources` ?from |
| To | date and time picker | — | — | `suggestResources` ?to |
| Attributes | text field | — | — | `suggestResources` ?attributes |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Minimum requirement (primary button) | navigation or local | — | — | — | — |
| Preferred requirement (secondary button) | navigation or local | — | — | — | — |
| Mandatory requirement (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `suggestResources` (onLoad, Who qualifies)

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The qualification rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the qualification rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No qualification rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the qualification rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setResourceQualifications` → `RESOURCE_MANAGE` (configure) · staff
- `suggestResources` → `RESOURCE_VIEW` (read) · staff
- `setExperienceResourceRequirements` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.53 | AI shall recommend optimal resources. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.54 | AI shall recommend suitable staff based on skills and availability. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.56 | AI shall propose alternatives for scheduling conflicts. | Ticketing Catalogue | CONTRACTED | `suggestResources` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-877` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-877`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 8: Works in Qualification & Assignment Rule Engine → Convert skills, certifications and operational policies into machine-enforceable assignment rules.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-877?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Minimum requirement, Preferred requirement, Mandatory requirement.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-878` Staff Availability & Working Pattern

**Define when an individual staff resource is normally available to work.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (2 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Users shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `resourceId` (navigation), `sourceId` (navigation) |
| Route | `/rentals/staff-availability-working-pattern-bo-878` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Working days | select field | — | — | — | — | — | — |
| Start time | select field | — | — | — | — | — | — |
| End time | select field | — | — | — | — | — | — |
| Time zone | select field | — | — | — | — | — | — |
| Effective period | select field | — | — | — | — | — | — |
| Weekly hours | select field | — | — | — | — | — | — |
| Availability type | select field | — | — | — | — | — | — |
| Seasonal pattern | select field | — | — | — | — | — | — |
| Availability Types | select field | — | — | — | — | — | — |
| Additional availability | select field | — | — | — | — | — | — |
| Temporary unavailability | select field | — | — | — | — | — | — |
| Special working day | select field | — | — | — | — | — | — |
| Venue reassignment | select field | — | — | — | — | — | — |
| Restricted hours | select field | — | — | — | — | — | — |
| Calendar Preview | select field | — | — | — | — | — | — |
| Available | select field | — | — | — | — | — | — |
| Working | select field | — | — | — | — | — | — |
| Unavailable | select field | — | — | — | — | — | — |
| Leave | select field | — | — | — | — | — | — |
| Break | select field | — | — | — | — | — | — |
| Existing assignment | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| External schedule (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staff availability working configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staff availability working untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staff availability working configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getResourceSchedule` → `RESOURCE_VIEW` (read) · staff
- `setResourceSchedule` → `RESOURCE_CONFIGURE` (configure) · staff
- `setFieldOwnership` → `WORKFORCE_MANAGE` (configure) · staff
- `listIntegrationSources` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.59 | Users shall manage resources through conversational AI commands. | Ticketing Catalogue | CONTRACTED | `setResourceSchedule` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-878` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-878`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 10: Works in Staff Availability & Working Pattern → Define when an individual staff resource is normally available to work.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-878?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: External schedule.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-879` Shift Template & Assignment Configuration

**Configure reusable workforce shift structures that can later be used by the operational roster engine.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/shift-template-assignment-configuration-bo-879` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Maximum shifts per day | text field | — | — | — | — | — | — |
| Maximum consecutive days | select field | — | — | — | — | — | — |
| Minimum rest between shifts | text field | — | — | — | — | — | — |
| Allowed roles | select field | — | — | — | — | — | — |
| Venue restrictions | select field | — | — | — | — | — | — |
| Skill requirements | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listShiftTemplates` (onLoad, Shift templates); `listShiftPatterns` (onLoad, Shift patterns)

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shift template configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shift template untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No shift template configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listShiftTemplates` → `WORKFORCE_VIEW` (read) · staff
- `setShiftTemplate` → `WORKFORCE_MANAGE` (configure) · staff
- `listShiftPatterns` → `WORKFORCE_VIEW` (read) · staff
- `setShiftPattern` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Shift templates (morning/afternoon/evening) define working patterns; the system recognises which shift a staff member has logged into from the configured shift timings. Leave/absence types and quotas work as a lightweight HR module, optionally integrated with an external HR/time-and-attendance system. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-487)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-879` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-879`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 12: Works in Shift Template & Assignment Configuration → Configure reusable workforce shift structures that can later be used by the operational roster engine.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-879?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-880` Break, Leave & Absence Configuration

**Ensure employee availability reflects breaks, approved leave, absences and other workforce exceptions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/break-leave-absence-configuration-bo-880` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Break type | select field | — | — | — | — | — | — |
| Minimum shift duration | select field | — | — | — | — | — | — |
| Break duration | select field | — | — | — | — | — | — |
| Paid/unpaid | select field | — | — | — | — | — | — |
| Mandatory/optional | select field | — | — | — | — | — | — |
| Earliest break | select field | — | — | — | — | — | — |
| Latest break | select field | — | — | — | — | — | — |
| Number of breaks | select field | — | — | — | — | — | — |
| Leave Types | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listLeaveRequests` ?status |
| Employee | picker: choose an employee | — | — | `listLeaveBalances` ?employeeId |
| Leave type | picker: choose a leave type | — | — | `listLeaveBalances` ?leaveTypeId |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Administrative block (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listLeaveRequests` (onLoad, Leave and absence); `listLeaveTypes` (onLoad, Leave types); `listLeaveBalances` (onLoad, Leave balances)

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The break leave absence configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the break leave absence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No break leave absence configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Bookings already exist in the window. They are listed, because blocking over a booked resource is sometimes right and must never be silent. (ResourceConflictProblem) |

#### Permissions

- `listLeaveRequests` → `WORKFORCE_VIEW` (read) · staff
- `requestLeave` → `WORKFORCE_VIEW` (read) · staff
- `listLeaveTypes` → `WORKFORCE_VIEW` (read) · staff
- `setLeaveType` → `WORKFORCE_MANAGE` (configure) · staff
- `listLeaveBalances` → `WORKFORCE_VIEW` (read) · staff
- `createResourceBlock` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Shift templates (morning/afternoon/evening) define working patterns; the system recognises which shift a staff member has logged into from the configured shift timings. Leave/absence types and quotas work as a lightweight HR module, optionally integrated with an external HR/time-and-attendance system. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-487)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-880` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-880`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 14: Works in Break, Leave & Absence Configuration → Ensure employee availability reflects breaks, approved leave, absences and other workforce exceptions.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-880?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Administrative block.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-881` Overtime & Working-Hour Rules

**Configure workforce rules controlling employee working hours and overtime eligibility before operational rostering occurs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/overtime-working-hour-rules-bo-881` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Standard daily hours | select field | — | — | — | — | — | — |
| Standard weekly hours | select field | — | — | — | — | — | — |
| Maximum daily hours | select field | — | — | — | — | — | — |
| Maximum weekly hours | select field | — | — | — | — | — | — |
| Minimum rest period | select field | — | — | — | — | — | — |
| Maximum consecutive working days | text field | — | — | — | — | — | — |
| Overtime threshold | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approval required (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The overtime working-hour rules configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the overtime working-hour rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No overtime working-hour rules configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setStaffingRules` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-881` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-881`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 16: Works in Overtime & Working-Hour Rules → Configure workforce rules controlling employee working hours and overtime eligibility before operational rostering occurs.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-881?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Approval required.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-882` Workforce Integration & Synchronization Center

**Connect TICVAI Resource Management with external HR, workforce management, payroll, identity, and employee systems where applicable. Provide TICVAI with a centralized, intelligent Workforce Operations & Rostering Engine that converts staff profiles, availability, skills, certifications, working-hour rules, and demand forecasts into executable operational rosters. Board 4 shall enable managers to: Build operational rosters Assign employees to attractions, venues, events, and activities Define minimum staffing requirements Validate role and skill coverage Identify staffing shortages Manage shift swaps, transfers, pickups, and releases Monitor planned versus actual attendance Capture check-in/check-out and attendance exceptions Validate workforce compliance before assignments Calculate and forecast labor costs Use AI to optimize staffing**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `sourceId` (navigation) |
| Route | `/rentals/workforce-integration-synchronization-center-bo-882` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `listRotaAssignments` ?from |
| To | date picker | — | — | `listRotaAssignments` ?to |
| Principal | picker: choose a principal | — | — | `listRotaAssignments` ?principalId |
| Department | picker: choose a department | — | — | `listRotaAssignments` ?departmentId |
| Source | picker: choose a source | — | — | `listSyncRuns` ?sourceId |
| Status | text field | — | — | `listSyncRuns` ?status |
| Source | picker: choose a source | — | — | `listSyncConflicts` ?sourceId |
| Status | text field | — | — | `listSyncConflicts` ?status |
| Kind | text field | — | — | `listSyncConflicts` ?kind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every workforce integration synchronization** (data table)

| Shows | Format | Notes |
|---|---|---|
| Connected systems | text | not in the schema: `Connected systems` |
| Last synchronization | text | not in the schema: `Last synchronization` |
| Successful records | text | not in the schema: `Successful records` |
| Failed records | text | not in the schema: `Failed records` |
| Warnings | text | not in the schema: `Warnings` |
| Mapping errors | text | not in the schema: `Mapping errors` |
| Authentication status | text | not in the schema: `Authentication status` |
| Conflict handling | text | not in the schema: `Conflict Handling` |

**The selected workforce integration synchronization** (detail panel): The pack groups this record's detail under its own headings: “Integration Sources”, “External System Master”, “For example”, “Board 3 Shared Governance”, “Board 3 End-to-End Outcome”, “The platform understands”.

| Shows | Format | Notes |
|---|---|---|
| Connected systems | text | not in the schema: `Connected systems` |
| Last synchronization | text | not in the schema: `Last synchronization` |
| Successful records | text | not in the schema: `Successful records` |
| Failed records | text | not in the schema: `Failed records` |
| Warnings | text | not in the schema: `Warnings` |
| Mapping errors | text | not in the schema: `Mapping errors` |
| Authentication status | text | not in the schema: `Authentication status` |
| Conflict handling | text | not in the schema: `Conflict Handling` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| API (primary button) | navigation or local | — | — | — | — |
| Webhooks/event-driven integration (secondary button) | navigation or local | — | — | — | — |
| Scheduled synchronization (secondary button) | navigation or local | — | — | — | — |
| Manual synchronization (secondary button) | navigation or local | — | — | — | — |
| File import where required (secondary button) | navigation or local | — | — | — | — |
| Integration Monitoring (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listRotaAssignments` (onLoad, Rota synchronisation); `listIntegrationSources` (onLoad, Connected workforce systems); `getFieldOwnership` (onLoad, Which system masters each field); `listSyncRuns` (onLoad, Synchronisation runs); `listSyncConflicts` (onLoad, Disagreements between systems)

**Where the user goes next**

- → `BO-873` Staff Resource Directory: *Back to Staff Resource Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workforce integration synchronization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workforce integration synchronization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workforce integration synchronization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workforce integration synchronization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A run is already in progress for this source; 409 Already resolved, or the resolution is not available for this kind |

#### Permissions

- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff
- `listIntegrationSources` → `WORKFORCE_VIEW` (read) · staff
- `setIntegrationSource` → `WORKFORCE_MANAGE` (configure) · staff
- `getFieldOwnership` → `WORKFORCE_VIEW` (read) · staff
- `setFieldOwnership` → `WORKFORCE_MANAGE` (configure) · staff
- `listSyncRuns` → `WORKFORCE_VIEW` (read) · staff
- `startSync` → `WORKFORCE_MANAGE` (configure) · staff
- `listSyncConflicts` → `WORKFORCE_VIEW` (read) · staff
- `resolveSyncConflict` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Shift templates (morning/afternoon/evening) define working patterns; the system recognises which shift a staff member has logged into from the configured shift timings. Leave/absence types and quotas work as a lightweight HR module, optionally integrated with an external HR/time-and-attendance system. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-487)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-882` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS128 Resource Management Configuration Board 3.dc.html#bo-882`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 3
- Flow F266 *Resource Management Configuration board 3: Staff Resource Directory*, step 18: Works in Workforce Integration & Synchronization Center → Connect TICVAI Resource Management with external HR, workforce management, payroll, identity, and employee systems where applicable.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-882?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: API, Webhooks/event-driven integration, Scheduled synchronization, Manual synchronization, File import where required, Integration Monitoring.
- [ ] Every transition is wired: `BO-873`.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createResourceBlock": {"method":"POST","path":"/resource-blocks","contract":"resources","summary":"Take a resource out of service for a window, with a reason","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceBlock","responds":"ResourceBlock"},
"getEmployee": {"method":"GET","path":"/employees/{employeeId}","contract":"workforce","summary":"One person, with their employment, postings and leave balances","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"employeeId","in":"path","required":true}],"requestBody":null,"responds":"WorkforceEmployeeProfile"},
"getFieldOwnership": {"method":"GET","path":"/integration-sources/{sourceId}/field-ownership","contract":"workforce","summary":"Which fields this source masters","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"sourceId","in":"path","required":true}],"requestBody":null,"responds":"WorkforceFieldOwnership"},
"getPrincipal": {"method":"GET","path":"/principals/{principalId}","contract":"identity","summary":"Read a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Principal"},
"getResourceSchedule": {"method":"GET","path":"/resources/{resourceId}/schedule","contract":"resources","summary":"The pattern of when it is normally available","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceSchedule"},
"listIntegrationSources": {"method":"GET","path":"/integration-sources","contract":"workforce","summary":"External systems that master workforce data, and their health","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"WorkforceIntegrationSource"},
"listLeaveBalances": {"method":"GET","path":"/leave-balances","contract":"workforce","summary":"What each person has left, by leave type","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"employeeId","in":"query","required":null},{"name":"leaveTypeId","in":"query","required":null}],"requestBody":null,"responds":"WorkforceLeaveBalance"},
"listLeaveRequests": {"method":"GET","path":"/leave-requests","contract":"workforce","summary":"Leave, absence and their effect on cover","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"LeaveRequest"},
"listLeaveTypes": {"method":"GET","path":"/leave-types","contract":"workforce","summary":"Leave types and how each accrues","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkforceLeaveType"},
"listPrincipals": {"method":"GET","path":"/principals","contract":"identity","summary":"List principals","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopePath","in":"query","required":null},{"name":"isActive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listResources": {"method":"GET","path":"/resources","contract":"resources","summary":"Resources at this venue","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"availableFrom","in":"query","required":null},{"name":"availableTo","in":"query","required":null}],"requestBody":null,"responds":"Resource"},
"listRotaAssignments": {"method":"GET","path":"/rota-assignments","contract":"workforce","summary":"The rota","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"departmentId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listShiftPatterns": {"method":"GET","path":"/shift-patterns","contract":"workforce","summary":"Named shift patterns","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkforceShift"},
"listShiftTemplates": {"method":"GET","path":"/shift-templates","contract":"workforce","summary":"Named shift patterns a rota is built from","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ShiftTemplate"},
"listSyncConflicts": {"method":"GET","path":"/sync-conflicts","contract":"workforce","summary":"Disagreements a person has to settle","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"sourceId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSyncRuns": {"method":"GET","path":"/sync-runs","contract":"workforce","summary":"Synchronisation history, with counts","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"sourceId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"requestLeave": {"method":"POST","path":"/leave-requests","contract":"workforce","summary":"Ask for time off, against the cover it would cost","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LeaveRequest","responds":"LeaveRequest"},
"resolveSyncConflict": {"method":"POST","path":"/sync-conflicts","contract":"workforce","summary":"Settle a disagreement","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResolveSyncConflictRequest","responds":"WorkforceSyncConflict"},
"setExperienceResourceRequirements": {"method":"PUT","path":"/experiences/{experienceId}/resource-requirements","contract":"resources","summary":"Bind resource requirements to an experience","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceRequirement"},
"setFieldOwnership": {"method":"PUT","path":"/integration-sources/{sourceId}/field-ownership","contract":"workforce","summary":"Declare who masters each field","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"sourceId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"WorkforceFieldOwnership","responds":"WorkforceFieldOwnership"},
"setIntegrationSource": {"method":"PUT","path":"/integration-sources","contract":"workforce","summary":"Connect or reconfigure an external workforce system","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkforceIntegrationSource","responds":"WorkforceIntegrationSource"},
"setLeaveType": {"method":"PUT","path":"/leave-types","contract":"workforce","summary":"Define a leave type","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkforceLeaveType","responds":"WorkforceLeaveType"},
"setResourceQualifications": {"method":"PUT","path":"/resources/{resourceId}/qualifications","contract":"resources","summary":"What a person resource is certified to do, and until when","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Qualification"},
"setResourceSchedule": {"method":"PUT","path":"/resources/{resourceId}/schedule","contract":"resources","summary":"Operating hours, working pattern and bookable slots","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ResourceSchedule","responds":"ResourceSchedule"},
"setShiftPattern": {"method":"PUT","path":"/shift-patterns","contract":"workforce","summary":"Define a shift pattern and its break","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkforceShift","responds":"WorkforceShift"},
"setShiftTemplate": {"method":"PUT","path":"/shift-templates","contract":"workforce","summary":"Define a shift pattern, its breaks and its qualifications","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ShiftTemplate","responds":"ShiftTemplate"},
"setStaffingRules": {"method":"PUT","path":"/staffing-rules","contract":"workforce","summary":"Minimum cover, working-hour limits and overtime","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"StaffingRules","responds":"StaffingRules"},
"startSync": {"method":"POST","path":"/sync-runs","contract":"workforce","summary":"Run a synchronisation now","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"suggestResources": {"method":"GET","path":"/resource-suggestions","contract":"resources","summary":"Resources matching a requirement, by attribute","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"resourceTypeId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"attributes","in":"query","required":null}],"requestBody":null,"responds":"Resource"},
"validateWorkforceCompliance": {"method":"GET","path":"/workforce-compliance","contract":"workforce","summary":"Where the rota breaks a rule","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"WorkforceComplianceFinding"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"LeaveRequest": {"type":"object","x-ticvai-persistence":"workforce.leave_request","description":"Resource board 3.8. **Approving leave without seeing the gap is how four supervisors book the same week.**\n","required":["principalId","from","to","kind"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["annual","sick","unpaid","parental","compassionate","training","timeOffInLieu"]},"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"halfDay":{"type":"boolean","default":false},"reason":{"type":"string","nullable":true},"status":{"type":"string","enum":["requested","approved","rejected","cancelled","taken"]},"coverageImpact":{"type":"array","readOnly":true,"items":{"$ref":"#/components/schemas/StaffingCoverage"}},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Principal": {"x-ticvai-persistence":"identity.principal","type":"object","required":["id","username","displayName","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"username":{"type":"string"},"displayName":{"type":"string"},"isActive":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"Past this, resolution returns DENY regardless of grants."},"primaryRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Determines the landing screen when the principal holds several roles and picks one at login.\n"},"roles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"lastLoginAt":{"type":"string","format":"date-time","nullable":true}}},
"Qualification": {"type":"object","x-ticvai-persistence":"resources.qualification","description":"1.2.36. **A role is not a skill**, and the check happens before assignment rather than after.\n","required":["code","name"],"properties":{"resourceId":{"type":"string","format":"uuid","readOnly":true,"description":"**The resource that holds this qualification.** Set from the path of `setResourceQualifications`; without it a stored qualification belongs to nobody and the check before assignment has nothing to check against. One row per resource and `code`.\n"},"code":{"type":"string"},"name":{"type":"string"},"issuedAt":{"type":"string","format":"date","nullable":true},"expiresAt":{"type":"string","format":"date","nullable":true,"description":"**The field that makes this worth having.** A certification with no expiry is one nobody renews, and a lifeguard certificate that lapsed last month is a safety failure rather than a data-quality one.\n"},"issuer":{"type":"string","nullable":true},"documentAssetId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ResolveSyncConflictRequest": {"type":"object","x-ticvai-persistence":"none — writes sync_conflict","required":["conflictId","resolution"],"properties":{"conflictId":{"type":"string","format":"uuid"},"resolution":{"type":"string","enum":["acceptExternal","keepTicvai","retry","ignore","escalate"]},"note":{"type":"string","maxLength":1000,"nullable":true},"releaseAffectedAssignments":{"type":"boolean","default":false,"description":"**For a termination conflict, what happens to the shifts already rostered.** Board 3 requires the downstream consequence to be acted on rather than reported: releasing them puts the shifts back on the marketplace, and leaving them means a manager has decided to cover them another way.\n"}}},
"Resource": {"type":"object","x-ticvai-persistence":"resources.resource","description":"**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n","required":["id","code","name","kind","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/ResourceKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentResourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"},"attributes":{"type":"object","additionalProperties":true,"description":"Configurable per kind — capacity, size, shade, power, poolside."},"setupMinutes":{"type":"integer","default":0,"description":"**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"},"teardownMinutes":{"type":"integer","default":0,"description":"After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"},"cleaningPolicy":{"allOf":[{"$ref":"#/components/schemas/ResourceCleaningPolicy"}],"nullable":true,"description":"How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."},"requiresQualification":{"type":"array","items":{"type":"string"},"description":"Qualification codes a person must hold to be assigned to this."},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["available","booked","checkedOut","maintenance","retired"]},"isActive":{"type":"boolean","default":true}}},
"ResourceBlock": {"type":"object","x-ticvai-persistence":"resources.resource_block","description":"Board 2.07. **A block is not a booking**, and the reason travels with it so an operator knows whether to wait or to look elsewhere.\n","required":["resourceId","from","to","reason"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string","enum":["setup","teardown","maintenance","blackout","closed","operational","training"]},"note":{"type":"string","nullable":true},"createdBy":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"ResourceCleaningPolicy": {"x-ticvai-persistence":"none — columns on resources.resource","type":"object","description":"**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n","required":["mode","bufferMinutes"],"properties":{"mode":{"type":"string","enum":["afterEveryBooking","timesPerDay"]},"bufferMinutes":{"type":"integer","minimum":5,"maximum":240,"description":"Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."},"cleaningsPerDay":{"type":"integer","minimum":1,"maximum":24,"nullable":true,"description":"Required for `timesPerDay`; ignored for `afterEveryBooking`."},"windowStart":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window opens. Null means the resource's opening time."},"windowEnd":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window closes. Null means the resource's closing time."}}},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"ResourceRequirement": {"type":"object","x-ticvai-persistence":"resources.resource_requirement","description":"**A type and a quantity, never a named resource.** This is what makes the 26 August rule enforceable — the product states what it needs and the platform decides which one.\nFor resources placed on a published venue map the rule is superseded (decided 29 September, rev 3 REV3-15): the guest names the resource through a `ResourceHold`, and no requirement is needed.\n","required":["quantity"],"properties":{"id":{"type":"string","format":"uuid"},"resourceTypeId":{"type":"string","format":"uuid","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A fixed component, and the exception rather than the rule.** Meeting Room A really is Meeting Room A; the technician is not.\n"},"quantity":{"type":"integer","default":1},"mandatory":{"type":"boolean","default":true},"requiredQualifications":{"type":"array","items":{"type":"string"}},"requiredAttributes":{"type":"object","additionalProperties":true},"substituteResourceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"scopePath":{"type":"string"}}},
"ResourceSchedule": {"type":"object","x-ticvai-persistence":"resources.resource_schedule","description":"Boards 2.03 and 2.04. **A recurring pattern with exceptions, not a list of dates.** A schedule written as concrete dates silently expires.\n","properties":{"resourceId":{"type":"string","format":"uuid"},"availabilityMode":{"type":"string","enum":["alwaysAvailable","scheduled","onRequest"]},"windows":{"type":"array","items":{"type":"object","properties":{"daysOfWeek":{"type":"array","items":{"type":"string"}},"from":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Local time of day, HH:MM."},"to":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Local time of day, HH:MM."},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true}}}},"slotMinutes":{"type":"integer","nullable":true,"description":"**How finely this resource's time can be cut**, which is a property of the resource and not of the product sold against it.\n"},"minimumBookingMinutes":{"type":"integer","nullable":true},"maximumBookingMinutes":{"type":"integer","nullable":true},"advanceBookingDays":{"type":"integer","nullable":true},"exceptions":{"type":"array","items":{"type":"object","properties":{"date":{"type":"string","format":"date"},"closed":{"type":"boolean"},"from":{"type":"string","nullable":true,"pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Local time of day, HH:MM."},"to":{"type":"string","nullable":true,"pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Local time of day, HH:MM."}}}},"scopePath":{"type":"string"}}},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"RotaAssignment": {"type":"object","x-ticvai-persistence":"workforce.rota_assignment","required":["principalId","venueId","startsAt","endsAt","position"],"properties":{"overtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"description":"BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"},"restPeriodBefore":{"type":"integer","nullable":true,"description":"Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"},"breachesWorkingHourLimit":{"type":"boolean","default":false,"readOnly":true,"description":"**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"},"labourCost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"},"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"position":{"type":"string","description":"What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"},"requiredRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/RotaStatus"},"breakMinutes":{"type":"integer","nullable":true},"note":{"type":"string","nullable":true}}},
"RotaStatus": {"type":"string","enum":["planned","published","confirmed","swapPending","cancelled","completed","noShow"]},
"ShiftTemplate": {"type":"object","x-ticvai-persistence":"workforce.shift_template","description":"Resource board 3.7. **The unit a manager actually thinks in.**","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"type":"string","enum":["early","late","middle","split","double","night","onCall","overtime"]},"startsAt":{"type":"string"},"endsAt":{"type":"string"},"breaks":{"type":"array","items":{"type":"object","properties":{"afterMinutes":{"type":"integer"},"minutes":{"type":"integer"},"paid":{"type":"boolean","default":false}}}},"requiredQualifications":{"type":"array","items":{"type":"string"}},"roleCode":{"type":"string","nullable":true},"costCentre":{"type":"string","nullable":true},"hourlyRate":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scopePath":{"type":"string"}}},
"StaffingCoverage": {"type":"object","description":"Resource board 4.4. **The gap is the product.**","properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid"},"positionCode":{"type":"string"},"label":{"type":"string"},"from":{"type":"string"},"to":{"type":"string"},"required":{"type":"integer"},"rostered":{"type":"integer"},"qualified":{"type":"integer","description":"**A position filled by somebody not qualified for it is still a gap.**"},"gap":{"type":"integer"},"severity":{"type":"string","enum":["covered","tight","short","blocking"]},"openShiftIds":{"type":"array","items":{"type":"string","format":"uuid"}},"basisApplied":{"type":"string","enum":["minimum","forecastRequirement"],"description":"Which figure `required` is for this row. With `higherOfBoth`, the larger; with `forecastRequirement` and no handed-over requirement for the period, `minimum`."},"minimumRequired":{"type":"integer","nullable":true,"description":"The configured minimum for the position and window."},"forecastRequired":{"type":"number","nullable":true,"description":"The forecast staff requirement (p50) for the position and window, from `workforce.forecast_requirement`. Null where none was handed over."},"forecastRequiredP90":{"type":"number","nullable":true,"description":"The busy-case requirement, for planning to the busy case."},"forecastVersionId":{"type":"string","format":"uuid","nullable":true,"description":"The AI forecast version the requirement is bound to (AIP-067), so a manager can open the forecast behind it."}}},
"StaffingRules": {"type":"object","x-ticvai-persistence":"workforce.staffing_rules + workforce.position_requirement","description":"Resource board 4.3. **A safety rule before it is a cost rule.**","properties":{"minimumCover":{"type":"array","description":"**Minimum staffing per position, venue and time window, with the qualifications it requires**: the rows of `workforce.position_requirement` (data model for the agreed operations, 29 September). `getStaffingCoverage` measures the rota against them; before this they were an array with no table, so no minimum was stored.","items":{"type":"object","required":["id","positionCode","minimumHeadcount"],"properties":{"id":{"type":"string","format":"uuid"},"positionCode":{"type":"string"},"label":{"type":"string"},"venueId":{"type":"string","format":"uuid","nullable":true},"attractionId":{"type":"string","format":"uuid","nullable":true},"minimumHeadcount":{"type":"integer","minimum":0},"daysOfWeek":{"type":"array","nullable":true,"description":"Days the minimum applies; absent means every day the venue is open","items":{"type":"string","enum":["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]}},"startsAt":{"type":"string","nullable":true,"description":"Start of the time window, local time (HH:MM) as `ShiftTemplate.startsAt`; absent means opening"},"endsAt":{"type":"string","nullable":true,"description":"End of the time window, local time (HH:MM); absent means closing"},"requiredQualifications":{"type":"array","items":{"type":"string"}},"appliesWhenOpen":{"type":"boolean","default":true},"blocksOperation":{"type":"boolean","default":true,"description":"**A ride requiring two operators cannot run with one.** Where this is true the attraction closes rather than running short.\n"}}}},"maximumHoursPerDay":{"type":"integer","nullable":true},"maximumHoursPerWeek":{"type":"integer","nullable":true},"minimumRestHours":{"type":"integer","nullable":true},"maximumConsecutiveDays":{"type":"integer","nullable":true},"overtime":{"type":"object","properties":{"allowed":{"type":"boolean","default":true},"afterHoursPerWeek":{"type":"integer","nullable":true},"rateMultiplier":{"type":"number","nullable":true},"requiresApproval":{"type":"boolean","default":true}}},"minimumAgeForNightShift":{"type":"integer","nullable":true},"defaultIncentiveRateMultiplier":{"type":"number","nullable":true,"minimum":1,"description":"**What an open shift pays above base when it is released.** Added 22 September: `workforce.open_shift.incentive_rate_multiplier` was set per shift with nothing behind it, so two identical shifts could price differently and record no reason. The shift still carries its own value — **as the snapshot**, the rule-and-record split `payments.fee_rule` and `orders.order_fee` use — and this is where it comes from.\n**Top-level rather than beside `overtime`** so the value is its own column. Nested in an object it would be a key inside a JSON blob, which nothing can index, constrain or pair to the shift that uses it.\n"},"maximumIncentiveRateMultiplier":{"type":"number","nullable":true,"minimum":1,"description":"**The ceiling on an incentive.** A shift nobody claims is the moment somebody raises the multiplier in a hurry — the same reason `maximumDailyCharge` bounds a late fee."},"incentiveApprovalAbove":{"type":"number","nullable":true,"minimum":1,"description":"**Above this multiplier a second person approves the release.** Routed as an approval, not a boolean — `overtime.requiresApproval` beside it is one of 26 approval flags across the contracts that no approval kind, matrix row or SLA reaches."},"scopePath":{"type":"string"}}},
"WorkforceComplianceFinding": {"type":"object","description":"Resource board 4.8. **Checked before the rota is published, not in an inspection.**","properties":{"code":{"type":"string","enum":["expiredQualification","missingQualification","exceededDailyHours","exceededWeeklyHours","insufficientRest","missedBreak","consecutiveDaysExceeded","underAgeNightShift","belowMinimumCover"]},"severity":{"type":"string","enum":["breach","warning"]},"principalId":{"type":"string","format":"uuid","nullable":true},"principalName":{"type":"string","nullable":true},"date":{"type":"string","format":"date","nullable":true},"detail":{"type":"string"},"rotaAssignmentIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"WorkforceEmployee": {"type":"object","x-ticvai-persistence":"workforce.employee","description":"**Taken from the backend workbook, 20 September.** Stores the main employee/staff master record.","required":["tenantId","code","firstName","lastName","dateOfJoining","employmentType","employmentStatus","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid","nullable":true},"code":{"type":"string","maxLength":50},"firstName":{"type":"string","maxLength":100},"lastName":{"type":"string","maxLength":100},"email":{"type":"string","maxLength":254,"nullable":true},"mobile":{"type":"string","maxLength":30,"nullable":true},"dateOfJoining":{"type":"string","format":"date"},"dateOfBirth":{"type":"string","format":"date","nullable":true,"description":"**What the under-age check needs** (data model for the agreed operations, 29 September): `validateWorkforceCompliance` reports `underAgeNightShift` against `StaffingRules.minimumAgeForNightShift`, and that rule has nothing to compare with unless the employee's age is on file. **An employee with no date of birth is reported as a warning**, not assumed to be of age."},"employmentType":{"type":"string","maxLength":30},"employmentStatus":{"type":"string","maxLength":30},"managerEmployeeId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkforceEmployeeProfile": {"type":"object","x-ticvai-persistence":"none — composed from employee and four related tables","description":"**One person and everything a profile screen asks about them.** The employment record, the postings and the leave balances are separate tables and one question, so fanning out across four endpoints is four round trips and four chances to render a half-loaded person.\n","required":["employee"],"properties":{"employee":{"$ref":"#/components/schemas/WorkforceEmployee"},"employments":{"type":"array","description":"Most recent first. **More than one is normal** — a seasonal worker rehired each summer has several, and collapsing them to the current one loses the service history that leave accrual is calculated from.\n","items":{"$ref":"#/components/schemas/WorkforceEmployment"}},"assignments":{"type":"array","items":{"$ref":"#/components/schemas/WorkforceWorkAssignment"}},"leaveBalances":{"type":"array","items":{"$ref":"#/components/schemas/WorkforceLeaveBalance"}},"jobTitles":{"type":"array","description":"The titles the postings name, so a client does not have to resolve them one by one.\n","items":{"$ref":"#/components/schemas/WorkforceJobTitle"}},"externallyMasteredFields":{"type":"array","description":"**Which fields on this record the venue may not edit**, resolved from `field_ownership` for whichever source masters this employee. A screen that shows an editable input over a field the HRMS owns has promised something it cannot keep.\n","items":{"type":"string"}}}},
"WorkforceEmployment": {"type":"object","x-ticvai-persistence":"workforce.employment","description":"**Taken from the backend workbook, 20 September.** Stores employment terms and contract validity.","required":["employeeId","contractType","startDate","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"employeeId":{"type":"string","format":"uuid"},"contractType":{"type":"string","maxLength":30},"startDate":{"type":"string","format":"date"},"endDate":{"type":"string","format":"date","nullable":true},"standardHoursPerWeek":{"type":"number","nullable":true},"probationEndDate":{"type":"string","format":"date","nullable":true},"status":{"type":"string","maxLength":30},"createdAt":{"type":"string","format":"date-time"}}},
"WorkforceFieldOwnership": {"type":"object","x-ticvai-persistence":"workforce.field_ownership","description":"**Which system owns a field, which is what prevents conflicting updates.** Board 3: *\"For every field, administrators shall determine ... External System Master.\"* Without this, an employee record mastered in HRMS and edited here disagrees with its source and nothing can say which answer is right.\nOne row per table and column. Absent means ours, so nothing has to be enumerated before it is decided.\n","required":["tableName","columnName","master"],"properties":{"id":{"type":"string","format":"uuid"},"tableName":{"type":"string","maxLength":120},"columnName":{"type":"string","maxLength":120},"master":{"type":"string","enum":["ticvai","external"]},"sourceId":{"type":"string","format":"uuid","nullable":true,"description":"The integration source that masters it, when `master` is `external`."},"onConflict":{"type":"string","enum":["externalWins","ticvaiWins","flagForReview"]},"scopePath":{"type":"string","nullable":true}}},
"WorkforceIntegrationSource": {"type":"object","x-ticvai-persistence":"workforce.integration_source","description":"**An external system that masters some of our workforce data.** Board 3 names HRMS, Workforce Management, Payroll, Time & Attendance, Identity Management and external staffing agencies. The six-state display Board 10 asks for lives on this row: what is connected, when it last synchronised, and whether its credentials still work.\n","required":["code","name","kind","transport","status"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":60},"name":{"type":"string","maxLength":150},"kind":{"type":"string","enum":["hrms","workforceManagement","payroll","timeAndAttendance","identity","staffingAgency"]},"transport":{"type":"string","enum":["api","webhook","scheduled","manual","fileImport"],"description":"Board 3, Support. **`manual` and `fileImport` are in the list on purpose** — a staffing agency that sends a spreadsheet is still a system of record, and modelling only the API cases would leave the messiest source unmanaged.\n"},"authenticationStatus":{"type":"string","enum":["healthy","expiring","expired","failed","notConfigured"]},"lastSynchronisedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["active","degraded","suspended"]},"scopePath":{"type":"string","nullable":true}}},
"WorkforceJobTitle": {"type":"object","x-ticvai-persistence":"workforce.job_title","description":"**Taken from the backend workbook, 20 September.** Stores job/designation definitions such as Cashier, Manager, Chef or Technician.","required":["tenantId","code","name","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":50},"name":{"type":"string","maxLength":150},"description":{"type":"string","maxLength":500,"nullable":true},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkforceLeaveBalance": {"type":"object","x-ticvai-persistence":"workforce.leave_balance","description":"**Taken from the backend workbook, 20 September.** Stores leave entitlement, used amount and remaining balance per employee/period.","required":["employeeId","typeId","periodYear","entitledDays","usedDays","pendingDays","availableDays","updatedAt"],"properties":{"id":{"type":"string","format":"uuid"},"employeeId":{"type":"string","format":"uuid"},"typeId":{"type":"string","format":"uuid"},"periodYear":{"type":"integer"},"entitledDays":{"type":"number"},"usedDays":{"type":"number"},"pendingDays":{"type":"number"},"availableDays":{"type":"number"},"updatedAt":{"type":"string","format":"date-time"}}},
"WorkforceLeaveType": {"type":"object","x-ticvai-persistence":"workforce.leave_type","description":"**Taken from the backend workbook, 20 September.** Defines leave categories and basic leave behavior.","required":["tenantId","code","name","isPaid","requiresApproval","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":50},"name":{"type":"string","maxLength":100},"isPaid":{"type":"boolean"},"requiresApproval":{"type":"boolean"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"}}},
"WorkforceShift": {"type":"object","x-ticvai-persistence":"workforce.shift","description":"**Taken from the backend workbook, 20 September.** Defines reusable shifts such as Morning, Evening or Night.","required":["tenantId","code","name","startTime","endTime","breakMinutes","crossesMidnight","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":50},"name":{"type":"string","maxLength":100},"startTime":{"type":"string","maxLength":0},"endTime":{"type":"string","maxLength":0},"breakMinutes":{"type":"integer"},"crossesMidnight":{"type":"boolean"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"}}},
"WorkforceSyncConflict": {"type":"object","x-ticvai-persistence":"workforce.sync_conflict","description":"**A disagreement a person has to settle, and the assignments it puts at risk.** Board 3 lists the cases by name: an employee in HR and not here, a venue changed externally, a certification expired, and *\"employee terminated externally but has future TICVAI assignments\"* — where *\"the system shall flag affected downstream assignments\"*.\n`affectedAssignmentIds` is deliberately an array and deliberately an exception: it is a snapshot of what was at risk when the conflict was raised, not a live relationship, and it must not change when a roster does.\n","required":["sourceId","kind","status","raisedAt"],"properties":{"id":{"type":"string","format":"uuid"},"sourceId":{"type":"string","format":"uuid"},"syncRunId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["missingInTicvai","missingExternally","venueChangedExternally","certificationExpired","terminatedExternally","fieldDisagreement"]},"employeeId":{"type":"string","format":"uuid","nullable":true},"externalReference":{"type":"string","maxLength":200,"nullable":true},"detail":{"type":"string","maxLength":1000,"nullable":true},"affectedAssignmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"status":{"type":"string","enum":["open","retried","reprocessed","escalated","resolved","ignored"]},"raisedAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","nullable":true}}},
"WorkforceSyncRun": {"type":"object","x-ticvai-persistence":"workforce.sync_run","description":"**One synchronisation, and what it did.** Board 10 asks the page to show successful records, failed records, warnings and mapping errors rather than *\"integration failed\"* — and to say the operational consequence: *\"12 employee availability updates could not be synchronised. Four employees have assignments within the next 24 hours.\"* That sentence needs counts on a row, not a log line.\n","required":["sourceId","startedAt","status"],"properties":{"id":{"type":"string","format":"uuid"},"sourceId":{"type":"string","format":"uuid"},"startedAt":{"type":"string","format":"date-time"},"finishedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["running","succeeded","partial","failed"]},"recordsRead":{"type":"integer"},"recordsApplied":{"type":"integer"},"recordsFailed":{"type":"integer"},"warningCount":{"type":"integer"},"mappingErrorCount":{"type":"integer"},"trigger":{"type":"string","enum":["scheduled","manual","webhook","fileImport"]},"scopePath":{"type":"string","nullable":true}}},
"WorkforceWorkAssignment": {"type":"object","x-ticvai-persistence":"workforce.work_assignment","description":"**Taken from the backend workbook, 20 September.** Assigns an employee to a job and operational location/scope for an effective period.","required":["employeeId","jobTitleId","effectiveFrom","isPrimary","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"employeeId":{"type":"string","format":"uuid"},"jobTitleId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"departmentId":{"type":"string","format":"uuid","nullable":true},"outletId":{"type":"string","format":"uuid","nullable":true},"effectiveFrom":{"type":"string","format":"date"},"effectiveTo":{"type":"string","format":"date","nullable":true},"isPrimary":{"type":"boolean"},"status":{"type":"string","maxLength":30},"createdAt":{"type":"string","format":"date-time"}}}
}
```
