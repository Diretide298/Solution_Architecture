# P06-operations-05 — P06 · Operations (5 of 5)

**6 screens · 15 operations · 26 schemas · 9 permissions**

Platform P06 Venue Staff App · ships as **venue-staff-mobile** ·
staff audience · mobileApp ·
offline-capable

## Who this is for

**staff on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `ACCESS_VALIDATE, ANNOUNCEMENT_PUBLISH, INCIDENT_MANAGE, INCIDENT_VIEW, INSPECTION_MANAGE, INSPECTION_SUBMIT, INSPECTION_VIEW, REPORT_VIEW_VENUE, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **5 of these operations work offline**: acknowledgeAnnouncement, listAnnouncements, listInspectionTemplates, logout, submitInspection
  — and the rest do not. A surface that looks the same online and off is lying.
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
| `EMP-048` | Opening checklist | A | 31 | 30 | 6 | 4 | 0 | 0 | — | notStarted (generated) |
| `EMP-047` | Emergency mode | B–D | 12 | 29 | 6 | 4 | 0 | 2 | — | notStarted (generated) |
| `EMP-050` | Post-incident restore | B–D | 16 | 44 | 6 | 1 | 0 | 0 | — | notStarted (generated) |
| `EMP-045` | Arabic / RTL | B–D | 0 | 0 | 4 | 0 | 0 | 0 | — | notStarted (generated) |
| `EMP-046` | Sign out | B–D | 0 | 0 | 4 | 0 | 0 | 0 | — | notStarted (generated) |
| `EMP-049` | Hand over the journal | B–D | 20 | 27 | 6 | 8 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**EMP-045, EMP-046 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `EMP-048` Opening checklist

**Confirm a gate is fit to open before the first guest reaches it.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `maintenance` module |
| Block | Block A · ticket #20693 (APP-SETUP-EMP-048) |
| Who uses it | venue staff holding `INSPECTION_MANAGE`, `INSPECTION_SUBMIT`, `INSPECTION_VIEW` (1 configure, 1 operate, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listInspectionTemplates` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | Works from the cached template. Completions queue |
| Opens with | nothing: it opens on its own |
| Route | `/operations/opening-checklist` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Template | picker: choose a template | — | — | `listInspections` ?templateId |
| Asset | upload, or pick from the media library | — | — | `listInspections` ?assetId |
| Outcome | segmented control | — | Passed · Passed with observations · Failed | `listInspections` ?outcome |
| Performed from | date picker | — | — | `listInspections` ?performedFrom |
| Performed to | date picker | — | — | `listInspections` ?performedTo |

**Form: Submit inspection** (modal, opened by *Submit inspection*; *Submit inspection* calls `submitInspection`, *Cancel* sends nothing)

**Collects what `submitInspection` sends before it is called.** Required: `id`, `templateId`, `venueId`, `responses`, `recordedAt`. Optional: `assetId`, `signatureRef`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `submitInspection` body |
| Template `templateId` | picker: choose a template | required | — | — | shows names, sends the id | — | `submitInspection` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `submitInspection` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `submitInspection` body |
| Responses `responses` | repeatable rows | required | — | at least 1 | — | — | `submitInspection` body |
| Key `responses[].key` | text field | required | — | — | — | — | `submitInspection` body |
| Value `responses[].value` | field | required | — | — | — | — | `submitInspection` body |
| Passed `responses[].passed` | toggle | optional | — | — | — | — | `submitInspection` body |
| Note `responses[].note` | text area | optional | — | max length 1000 | — | — | `submitInspection` body |
| Attachment refs `responses[].attachmentRefs` | list of values (chips) | optional | — | — | — | — | `submitInspection` body |
| Signature ref `signatureRef` | text field | optional | — | — | — | — | `submitInspection` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `submitInspection` body |

Errors to draw in the form: 400 A required item was not answered

**Form: Create inspection template** (modal, opened by *Create inspection template*; *Create inspection template* calls `createInspectionTemplate`, *Cancel* sends nothing)

**Collects what `createInspectionTemplate` sends before it is called.** Required: `id`, `code`, `name`, `items`. Optional: `instructions`, `venueId`, `appliesToAssetCategoryId`, `frequency`, `retentionYears`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Instructions `instructions` | text field | optional | — | — | — | The procedure itself. A technician asking how to isolate a chiller is asking a safety question, and the answer has to come from the template rather than from its title. | `createInspectionTemplate` body |
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createInspectionTemplate` body |
| Code `code` | text field | required | — | max length 64 | — | — | `createInspectionTemplate` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createInspectionTemplate` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createInspectionTemplate` body |
| Applies to asset category `appliesToAssetCategoryId` | picker: choose an applies to asset category | optional | — | — | shows names, sends the id | — | `createInspectionTemplate` body |
| Frequency `frequency` | select | optional | — | Pre opening · Post closing · Daily · Weekly · Monthly · Annual · Ad hoc | — | — | `createInspectionTemplate` body |
| Items `items` | repeatable rows | required | — | at least 1 | — | — | `createInspectionTemplate` body |
| Key `items[].key` | text field | required | — | — | — | — | `createInspectionTemplate` body |
| Label `items[].label` | text field | required | — | — | — | — | `createInspectionTemplate` body |
| Kind `items[].kind` | select | required | — | Pass fail · Yes no · Numeric · Text · Photo · Signature | — | — | `createInspectionTemplate` body |
| Is required `items[].isRequired` | toggle | required | — | — | — | — | `createInspectionTemplate` body |
| Is safety critical `items[].isSafetyCritical` | toggle | optional | off | A failed safety-critical item blocks the inspection from passing and cannot be overridden by completing the rest. | — | A failed safety-critical item blocks the inspection from passing and cannot be overridden by completing the rest. | `createInspectionTemplate` body |
| Requires photo on fail `items[].requiresPhotoOnFail` | toggle | optional | on | — | — | — | `createInspectionTemplate` body |
| Min value `items[].minValue` | number field | optional | — | — | — | — | `createInspectionTemplate` body |
| Max value `items[].maxValue` | number field | optional | — | — | — | — | `createInspectionTemplate` body |
| Guidance `items[].guidance` | text field | optional | — | — | — | — | `createInspectionTemplate` body |
| Retention years `retentionYears` | number field | optional | 7 | — | — | Compliance inspections are retained alongside the financial trail. | `createInspectionTemplate` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createInspectionTemplate` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every inspection template** (data table, from `listInspectionTemplates`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Applies to asset category | the name it points at, never the id | — |
| Frequency | chip: Pre opening, Post closing, Daily, Weekly, Monthly, Annual… | — |
| Items | list or chips (count when long) | — |
| Retention years | 1,234 | Compliance inspections are retained alongside the financial trail. |
| Is active | yes / no (icon or chip) | — |

**Every inspection** (data table, from `listInspections`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Template | the name it points at, never the id | — |
| Template name | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Outcome | chip: Passed, Passed with observations, Failed | — |
| Failed item count | 1,234 | — |
| Failed safety critical count | 1,234 | — |
| Performed by principal | the name it points at, never the id | An inspection nobody signed is not an inspection. |
| Performed at | 1 Oct 2026, 14:30 | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | — |

**The selected inspection template** (detail panel, from `listInspectionTemplates`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Applies to asset category | the name it points at, never the id | — |
| Frequency | chip: Pre opening, Post closing, Daily, Weekly, Monthly, Annual… | — |
| Items | list or chips (count when long) | — |
| Retention years | 1,234 | Compliance inspections are retained alongside the financial trail. |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Submit inspection (primary button) | `submitInspection` POST `/inspections` | SubmitInspectionRequest | InspectionResult | 400 A required item was not answered | works offline; opens modal first |
| Create inspection template (secondary button) | `createInspectionTemplate` POST `/inspection-templates` | InspectionTemplate | InspectionTemplate | — | opens modal first |

**Data it reads**: `listInspectionTemplates` (onLoad, List inspection templates); `listInspections` (onLoad, List completed inspections)

**Where the user goes next**

- → `EMP-003` Home — on duty: *Sees the home screen on duty*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The opening checklist list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the opening checklist untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No opening checklist yet. Offers Submit inspection (`submitInspection`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listInspectionTemplates` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `INSPECTION_VIEW`, which `listInspectionTemplates` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Works from the cached template. Completions queue |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A required item was not answered |

#### Permissions

- `listInspectionTemplates` → `INSPECTION_VIEW` (read) · staff
- `submitInspection` → `INSPECTION_SUBMIT` (operate) · staff
- `createInspectionTemplate` → `INSPECTION_MANAGE` (configure) · staff
- `listInspections` → `INSPECTION_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `INSPECTION_VIEW`, which `listInspectionTemplates` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.5.7 | Safety Audits - System shall support safety audits. | Maintenance & Safety Management | CONTRACTED | `submitInspection` |
| 17.5.1 | Safety Inspections - System shall support safety inspections. | Maintenance & Safety Management | CONTRACTED | `createInspectionTemplate` |
| 17.5.2 | Safety Checklists - System shall support configurable safety checklists. | Maintenance & Safety Management | CONTRACTED | `createInspectionTemplate` |
| 17.5.9 | Safety Compliance Tracking - System shall support safety compliance tracking. | Maintenance & Safety Management | CONTRACTED | `listInspections` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-048` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 3: Works the opening checklist → What must be true before the venue opens
- Flow F64 *A steward signs in and takes a venue and a role*, step 3: The opening checklist is worked. → **Tasks, not a paper list.** A checklist nobody records is a checklist nobody did.
- Flow F08 branch at step 3 (recoverable): when A gate needs covering mid-shift, EMP-010 through EMP-015 — the app scans too. Lower throughput than a handheld, and enough for a relief.

#### Acceptance for the design

- [ ] Every input above is drawn (31), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-048?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Submit inspection, Create inspection template.
- [ ] Every transition is wired: `EMP-003`, `EMP-001`, `EMP-002`.
- [ ] Every gated control is gated: `INSPECTION_MANAGE`, `INSPECTION_SUBMIT`, `INSPECTION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-047` Emergency mode

**Evacuate, and stop pretending to be a ticketing app.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ANNOUNCEMENT_PUBLISH`, `WORKFORCE_VIEW` (1 configure, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAnnouncements` reads the population and `getAnnouncementReach` reads one of them — list, select, act |
| Offline | Fully offline by design |
| Opens with | `announcementId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/emergency-mode` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Unacknowledged only | toggle | optional | — | — | — | Sends `?unacknowledgedOnly=` to `listAnnouncements`. | `listAnnouncements` ?unacknowledgedOnly |

**Form: Publish announcement** (modal, opened by *Publish announcement*; *Publish announcement* calls `publishAnnouncement`, *Cancel* sends nothing)

**Collects what `publishAnnouncement` sends before it is called.** Required: `title`, `body`, `kind`, `publishedAt`. Optional: `id`, `venueIds`, `departmentIds`, `roleIds`, `requiresAcknowledgement`, `expiresAt`, `publishedByPrincipalId`, `locale`. **An `emergency` kind requires ANNOUNCEMENT_EMERGENCY** (audit R091 (1)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text field | required | — | max length 140 | — | — | `publishAnnouncement` body |
| Body `body` | text area | required | — | max length 4000 | — | — | `publishAnnouncement` body |
| Kind `kind` | radio group | required | — | Operational · Safety · Emergency · Hr · Celebration | — | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission. | `publishAnnouncement` body |
| Venues `venueIds` | multi-picker: choose venues | optional | — | — | — | — | `publishAnnouncement` body |
| Departments `departmentIds` | multi-picker: choose departments | optional | — | — | — | — | `publishAnnouncement` body |
| Roles `roleIds` | multi-picker: choose roles | optional | — | — | — | — | `publishAnnouncement` body |
| Requires acknowledgement `requiresAcknowledgement` | toggle | optional | — | — | — | — | `publishAnnouncement` body |
| Delivery channels `deliveryChannels` | multi-select chips | optional | In app, Push | In app · Push | — | How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). | `publishAnnouncement` body |
| Expires at `expiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishAnnouncement` body |
| Published at `publishedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishAnnouncement` body |
| Locale `locale` | text field | optional | — | — | — | — | `publishAnnouncement` body |

Errors to draw in the form: 403 The caller lacks `ANNOUNCEMENT_PUBLISH` at the target scope, or sent `kind` `emergency` without `ANNOUNCEMENT_EMERGENCY` (problem type …

#### Outputs: what the screen shows and produces

**Shown**

**Every announcement** (data table, from `listAnnouncements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Title | text | — |
| Body | text | — |
| Kind | chip: Operational, Safety, Emergency, Hr, Celebration | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a … |
| Venues | list or chips (count when long) | — |
| Departments | list or chips (count when long) | — |
| Roles | list or chips (count when long) | — |
| Requires acknowledgement | yes / no (icon or chip) | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Locale | text | — |

**The selected announcement** (detail panel, from `listAnnouncements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Title | text | — |
| Body | text | — |
| Kind | chip: Operational, Safety, Emergency, Hr, Celebration | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a … |
| Venues | list or chips (count when long) | — |
| Departments | list or chips (count when long) | — |
| Roles | list or chips (count when long) | — |
| Requires acknowledgement | yes / no (icon or chip) | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Locale | text | — |

**The announcement reach** (detail panel, from `getAnnouncementReach`)

| Shows | Format | Notes |
|---|---|---|
| Announcement | the name it points at, never the id | — |
| Targeted | 1,234 | — |
| Delivered | 1,234 | — |
| Acknowledged | 1,234 | — |
| Outstanding | list or chips (count when long) | The list that matters. For an operational notice it measures whether anyone read it; during an emergency it is the roll call. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Acknowledge announcement (primary button) | `acknowledgeAnnouncement` POST `/announcements/{announcementId}/acknowledge` | — | — | — | works offline |
| Publish announcement (secondary button) | `publishAnnouncement` POST `/announcements` | Announcement | Announcement | 403 The caller lacks `ANNOUNCEMENT_PUBLISH` at the target scope, or sent `kind` `emergency` without `ANNOUNCEMENT_EMERGENCY` (problem type … | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listAnnouncements` (onLoad, What staff have been told)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-050` Post-incident restore: *Post-incident restore*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The emergency mode list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the emergency mode untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No emergency mode yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on unacknowledgedOnly and the emergency mode are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Fully offline by design |

#### Permissions

- `listAnnouncements` → `WORKFORCE_VIEW` (read) · staff
- `acknowledgeAnnouncement` → `WORKFORCE_VIEW` (read) · staff
- `getAnnouncementReach` → `WORKFORCE_VIEW` (read) · staff
- `publishAnnouncement` → `ANNOUNCEMENT_PUBLISH` (configure) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.66 | System shall send assignment and schedule notifications. | Ticketing Catalogue | CONTRACTED | `publishAnnouncement` |
| 18.1.5 | Push Notifications - System shall support push notifications. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |
| 18.9.3 | Announcements - Users shall receive announcements. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |
| 18.9.4 | Emergency Alerts - Users shall receive emergency notifications. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A69** Implement duplicate-account detection and profile-merge functionality (consolidating two profiles into one, carrying over the combined transaction history) *(Softlabs Backend Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Aug 2026 · workshop tracker · keyword 'duplicate-account')*
- **A90** Implement consent-gated duplicate merge (fuzzy name / exact mobile / exact email matching, customer confirmation required, admin review queue, login-of-record rule) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'duplicate merge')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-047` · status **notStarted** · provenance generated
- Flow F69 *An incident is reported, escalated and closed*, step 4: If it is a venue-wide event, an announcement goes out. → **Reach is measured.** An evacuation announcement nobody acknowledged is an evacuation nobody heard.
- Flow F69 branch at step 4 (high): when Staff do not acknowledge the announcement., **Escalated by name, not re-broadcast.** A second identical message to everybody is a message everybody ignores.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (29 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-047?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Acknowledge announcement, Publish announcement, What publishing changes.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-050`.
- [ ] Every gated control is gated: `ANNOUNCEMENT_PUBLISH`, `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-050` Post-incident restore

**Put the venue back to how it was.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `maintenance` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `INCIDENT_MANAGE`, `INCIDENT_VIEW` (1 configure, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listIncidents` reads the population and `getIncident` reads one of them — list, select, act |
| Offline | **Works offline by design.** Post-incident restore is exactly when the network is worst |
| Opens with | `incidentId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/post-incident-restore` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: reportIncident. **Bulk-attach residue.** A device-settings screen does not merge guest profiles, a rota view does not author the rota, a shift summary does not open a shift, and **authority notification belongs where the incident is raised, not where it is read.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Severity | radio group | optional | — | Near miss · Minor · Moderate · Major · Critical | — | Sends `?severity=` to `listIncidents`. | `listIncidents` ?severity |
| Status | radio group | optional | — | Reported · Under investigation · Action required · Closed | — | Sends `?status=` to `listIncidents`. | `listIncidents` ?status |
| Is reportable | toggle | optional | — | — | — | Sends `?isReportable=` to `listIncidents`. | `listIncidents` ?isReportable |

**Form: Record authority notification** (modal, opened by *Record authority notification*; *Record authority notification* calls `recordAuthorityNotification`, *Cancel* sends nothing)

**Collects what `recordAuthorityNotification` sends before it is called.** Required: `authority`, `notifiedAt`. Optional: `reference`, `notifiedByPrincipalId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Authority `authority` | text field | required | — | max length 200 | — | — | `recordAuthorityNotification` body |
| Reference `reference` | text field | optional | — | max length 128 | — | — | `recordAuthorityNotification` body |
| Notified at `notifiedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordAuthorityNotification` body |
| Notified by principal `notifiedByPrincipalId` | picker: choose a notified by principal | optional | — | — | shows names, sends the id | — | `recordAuthorityNotification` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `recordAuthorityNotification` body |

Errors to draw in the form: 409 The incident is not reportable (`isReportable` false, audit R106 (6)).

**Form: Save incident** (modal, opened by *Save incident*; *Save incident* calls `updateIncident`, *Cancel* sends nothing)

**Collects what `updateIncident` sends before it is called.** Nothing in the body is required. Optional: `status`, `severity`, `assignedToPrincipalId`, `investigationNote`, `rootCause`, `correctiveActions`, `correctiveWorkOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | optional | — | Reported · Under investigation · Action required · Closed | — | — | `updateIncident` body |
| Severity `severity` | radio group | optional | — | Near miss · Minor · Moderate · Major · Critical | — | — | `updateIncident` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `updateIncident` body |
| Investigation note `investigationNote` | text area | optional | — | max length 10000 | — | Appended as a new entry of `IncidentDetail.investigationNotes`, never overwriting the last (audit R106 (5)). | `updateIncident` body |
| Root cause `rootCause` | text area | optional | — | max length 2000 | — | — | `updateIncident` body |
| Corrective actions `correctiveActions` | text area | optional | — | max length 5000 | — | — | `updateIncident` body |
| Corrective work order `correctiveWorkOrderId` | picker: choose a corrective work order | optional | — | — | shows names, sends the id | — | `updateIncident` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `updateIncident` body |

Errors to draw in the form: 400 Closure attempted without findings or a corrective action

#### Outputs: what the screen shows and produces

**Shown**

**Every incident** (data table, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Location description | text | — |
| Is reportable | yes / no (icon or chip) | Requires notification to an external authority within a statutory window. |
| Notification due at | 1 Oct 2026, 14:30 | — |
| Notified at | 1 Oct 2026, 14:30 | The earliest `notifiedAt` among this incident's authority notifications. Maintained on write by `recordAuthorityNotification`; each … |
| Assigned to principal | the name it points at, never the id | — |

**The selected incident** (detail panel, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Location description | text | — |
| Is reportable | yes / no (icon or chip) | Requires notification to an external authority within a statutory window. |
| Notification due at | 1 Oct 2026, 14:30 | — |
| Notified at | 1 Oct 2026, 14:30 | The earliest `notifiedAt` among this incident's authority notifications. Maintained on write by `recordAuthorityNotification`; each … |
| Assigned to principal | the name it points at, never the id | — |
| Reported by principal | the name it points at, never the id | — |
| Corrective work order | the name it points at, never the id | — |
| Occurred at | 1 Oct 2026, 14:30 | — |
| Recorded at | 1 Oct 2026, 14:30 | — |

**The incident** (detail panel, from `getIncident`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Location description | text | — |
| Is reportable | yes / no (icon or chip) | Requires notification to an external authority within a statutory window. |
| Notification due at | 1 Oct 2026, 14:30 | — |
| Notified at | 1 Oct 2026, 14:30 | The earliest `notifiedAt` among this incident's authority notifications. Maintained on write by `recordAuthorityNotification`; each … |
| Assigned to principal | the name it points at, never the id | — |
| Reported by principal | the name it points at, never the id | — |
| Corrective work order | the name it points at, never the id | — |
| Occurred at | 1 Oct 2026, 14:30 | — |
| Recorded at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Record authority notification (primary button) | `recordAuthorityNotification` POST `/incidents/{incidentId}/notify-authority` | inline | Incident | 409 The incident is not reportable (`isReportable` false, audit R106 (6)). | opens modal first |
| Save incident (secondary button) | `updateIncident` PATCH `/incidents/{incidentId}` | inline | Incident | 400 Closure attempted without findings or a corrective action | opens modal first |

**Data it reads**: `listIncidents` (onLoad, List incidents)

**Where the user goes next**

- → `EMP-047` Emergency mode: *If it is a venue-wide event, an announcement goes out*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*; carries `incidentId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The post-incident restore list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the post-incident restore untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No post-incident restore yet. Offers Record authority notification (`recordAuthorityNotification`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on severity, status, isReportable and the post-incident restore are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `INCIDENT_VIEW`, which `listIncidents` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Works offline by design.** Post-incident restore is exactly when the network is worst |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Closure attempted without findings or a corrective action; 409 The incident is not reportable (`isReportable` false, audit R106 (6)). |

#### Permissions

- `listIncidents` → `INCIDENT_VIEW` (read) · staff
- `getIncident` → `INCIDENT_VIEW` (read) · staff
- `recordAuthorityNotification` → `INCIDENT_MANAGE` (configure) · staff
- `updateIncident` → `INCIDENT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `INCIDENT_VIEW`, which `listIncidents` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.9.5 | System shall provide real-time visibility of incidents, hazards, complaints, emergencies, and operational disruptions. | Unified Operations Dashboard | CONTRACTED | `listIncidents` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-050` · status **notStarted** · provenance generated
- Flow F69 *An incident is reported, escalated and closed*, step 3: Where required, the authorities are notified. → **The notification is itself a record.** *We told the police* with no time and no name is not evidence.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-050?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Record authority notification, Save incident.
- [ ] Every transition is wired: `EMP-047`, `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `INCIDENT_MANAGE`, `INCIDENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-045` Arabic / RTL

**Render the staff app right to left.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **the screen's operations choose no pattern** — no list, no get, no write that groups. It falls to the default, and the fallback is recorded rather than passed off as a decision |
| Offline | **Fully offline.** Direction is a device setting, not a server one |
| Opens with | nothing: it opens on its own |
| Route | `/operations/arabic-rtl` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** **This screen declares no operation the contracts recognise.** Nothing fills it, nothing it does is committed anywhere, and its shape below is a default rather than a reading.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | — |
| Error (`?state=error`) | — |
| Empty, first run (`?state=emptyFirstRun`) | — |
| Offline (`?state=offline`) | **Fully offline.** Direction is a device setting, not a server one |

#### Permissions

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-045` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-045?state=<state>`: loading, error, emptyFirstRun, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-046` Sign out

**Leave the shared device safe for the next person.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`logout`) and no read of a population — it is settings, not a list |
| Offline | Signs out locally and the journal stays on the device for the next steward |
| Opens with | nothing: it opens on its own |
| Route | `/operations/sign-out` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** **`logout` declares no request body shape**, so nothing says what this editor edits. The fields cannot be derived and the screen needs the contract before it needs a designer.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Logout (primary button) | `logout` POST `/auth/logout` | — | — | — | works offline |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Closing the session |
| Error (`?state=error`) | **Sign-out with a pending journal warns rather than blocks.** A steward handing over a device must not be trapped by a failed sync |
| Empty, first run (`?state=emptyFirstRun`) | — |
| Offline (`?state=offline`) | Signs out locally and the journal stays on the device for the next steward |

#### Permissions

- `logout` → no permission · staff

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-046` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-046?state=<state>`: loading, error, emptyFirstRun, offline.
- [ ] Every action is wired with its success and its failure: Logout, Cancel.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-049` Hand over the journal

**Move an unsynced journal off a device that is going flat.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as technician |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The point of the screen.** It exists because the journal outlives the shift |
| Opens with | nothing: it opens on its own |
| Route | `/operations/hand-over-the-journal` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Access point id | picker: choose an access point (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?accessPointId=` to `listScans`. | `listScans` ?accessPointId |
| Ticket id | picker: choose a ticket (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ticketId=` to `listScans`. | `listScans` ?ticketId |
| Outcome | segmented control | optional | — | Admitted · Denied · Overridden | — | Sends `?outcome=` to `listScans`. | `listScans` ?outcome |
| Recorded from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedFrom=` to `listScans`. | `listScans` ?recordedFrom |
| Recorded to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedTo=` to `listScans`. | `listScans` ?recordedTo |
|  | scan target | — | — | — | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | — |

**Form: Sync scans** (modal, opened by *Sync scans*; *Sync scans* calls `syncScans`, *Cancel* sends nothing)

**Collects what `syncScans` sends before it is called.** Required: `deviceId`, `scans`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | Sequence numbers are monotonic per device, not globally. | `syncScans` body |
| Scans `scans` | repeatable rows | required | — | at least 1; at most 500 | — | — | `syncScans` body |
| ID `scans[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `syncScans` body |
| Media code `scans[].mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `syncScans` body |
| Media kind `scans[].mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive | — | — | `syncScans` body |
| Direction `scans[].direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `syncScans` body |
| Group size `scans[].groupSize` | number field | optional | — | min 1 | — | For group media admitting several holders on one read. | `syncScans` body |
| Proximity token `scans[].proximityToken` | text field | optional | — | — | — | BLE proximity assertion where the venue requires the operator to be physically at the gate. | `syncScans` body |
| Recorded at `scans[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the read. Authoritative for ordering, not for validity. | `syncScans` body |
| Sequence `scans[].sequence` | number field | required | — | min 1 | — | Monotonic per device. The server processes in this order. | `syncScans` body |
| Local outcome `scans[].localOutcome` | segmented control | required | — | Admitted · Denied · Overridden | — | What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded. | `syncScans` body |
| Local deny reason `scans[].localDenyReason` | select | optional | — | Not found · Not yet valid · Expired · Already used · Reentry limit reached · Exit required before reentry · Wrong access point · Wrong performance · Outside admission window · Entitlement suspended · Blacklisted · Capacity reached … | — | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean. | `syncScans` body |
| Overridden by principal `scans[].overriddenByPrincipalId` | picker: choose an overridden by principal | optional | — | — | shows names, sends the id | — | `syncScans` body |
| Override reason `scans[].overrideReason` | text field | optional | — | — | — | — | `syncScans` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Every scan event** (data table, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The scan's client-generated UUIDv7, the key offline replay deduplicates on. |
| Access point | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Ticket | the name it points at, never the id | The `Entitlement.id` scanned; null where the media resolved to nothing. |
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |
| Deny reason | chip: Not found, Not yet valid, Expired, Already used, Reentry limit reached, Exit … | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a … |
| Direction | chip: Entry, Exit, Reentry, Crossover | — |
| Operator principal | the name it points at, never the id | — |
| Device | the name it points at, never the id | — |
| Overrides scan | the name it points at, never the id | Set only on an override row, naming the denied scan it admits against (decided 28 September, audit R228). |

**The selected scan event** (detail panel, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The scan's client-generated UUIDv7, the key offline replay deduplicates on. |
| Access point | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Ticket | the name it points at, never the id | The `Entitlement.id` scanned; null where the media resolved to nothing. |
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |
| Deny reason | chip: Not found, Not yet valid, Expired, Already used, Reentry limit reached, Exit … | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a … |
| Direction | chip: Entry, Exit, Reentry, Crossover | — |
| Operator principal | the name it points at, never the id | — |
| Device | the name it points at, never the id | — |
| Overrides scan | the name it points at, never the id | Set only on an override row, naming the denied scan it admits against (decided 28 September, audit R228). |
| Override reason | text | The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`. |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | Null while pending. Differs from recordedAt for offline scans. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sync scans (primary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |

**Data it reads**: `listScans` (onLoad, List scan events)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The hand over the list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the hand over the untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No hand over the yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the hand over the are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **The point of the screen.** It exists because the journal outlives the shift |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `syncScans` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.55 | All Guests are invited use the turnstiles when leaving the park. It is expected that the system counts the number of exits. Scan can be required at exit. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.58 | In park attendance figure per ticket time is calculated in real time. | Admission and Access | CONTRACTED | `listScans` |
| 5.3.28 | Maintain detailed access validation history including gate entries, exits, attraction validations, RFID scans, QR scans, and turnstile events. | F&B & Guest Management | CONTRACTED | `listScans` |
| 18.1.4 | Synchronization - System shall synchronize data when connectivity is restored. | Employee Mobile App & AI Assistant | CONTRACTED | `syncScans` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-049` · status **notStarted** · provenance generated
- Flow F71 *A device is prepared, used and handed over*, step 3: At the end of the session the journal is handed over. → **Handed over, not just synced.** A device passed to the next shift with an unsynced journal carries somebody else’s scans.
- Flow F71 branch at step 3 (medium): when The journal will not sync., **A technician job, not a supervisor one.** Connectivity is IT; deciding whether a scan stands is not — CF-159 settled that split.

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-049?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sync scans.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P06 reference designs** (from `handoff/design-batches/apps/4-staff-app/README.md`)

- `sources/designs/TICVAI_Employee_App_UI_Reference_1.pdf`: the client's employee app reference: dark theme, Home, Tasks, Scan, AI, More.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P06 as a whole** (3: 0 open, 3 closed). Open first; a closed row says where it went on 30 September.

- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A49** Confirm scope: deliver a lightweight standalone ticket-validation app for dedicated scanner devices, in addition to the scan/validate function embedded in the full Staff Operations App *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A71** Design an offline-first, native ticket-scanning/access-control capability (local scan storage with sync-on-reconnect) for both the dedicated scanner app and the scanning function embedded in the Employee App *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 10 Aug 2026 · workshop tracker)*

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

### Across P06 Venue Staff App

- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- Approval screens offer Approve, Reject, Return and Request More Information, show an AI-generated approval summary beside the request, and a visible trail of who approved at each stage (e.g. IT → Ops Manager → Finance → CEO → IT publishes). *(client request · MoM 10 Aug 2026, 5.5 Multi-Stage Approval Workflow · DI-235)*
- Two separate apps: an access-control app (handhelds or fixed terminals) scoped purely to entry validation/scanning, and an employee app (approvals, alerts/messages, matrix features) that may include a basic ticket-validity lookup but not full scanning. *(agreed · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-128)*
- Offline state must be clearly visible in the UI, e.g. a visible mode indicator or greyed-out unavailable functions; exact visual treatment to be settled in the UI/UX session. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-072)*
- Allam: the app detects loss of connectivity and switches to offline mode automatically, without cashier action, then restores online mode and syncs pending transactions automatically. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-071)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Allam: the platform is device-agnostic (Android, iOS and web) so sales can continue on any available device. *(agreed · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-068)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

### In P06 · Operations

- Employee app navigation: Work Orders, Task & Assets, Inventory/Safety/Inspections, Attendance, Approvals/Requests, Incidents, Communications, Venue Map; plus employee ID/profile and preferences. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-228)*

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acknowledgeAnnouncement": {"method":"POST","path":"/announcements/{announcementId}/acknowledge","contract":"workforce","summary":"Confirm you have read it","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createInspectionTemplate": {"method":"POST","path":"/inspection-templates","contract":"maintenance","summary":"Create an inspection template","permission":"INSPECTION_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"InspectionTemplate","responds":"InspectionTemplate"},
"getAnnouncementReach": {"method":"GET","path":"/announcements/{announcementId}/reach","contract":"workforce","summary":"Who has acknowledged, and who has not","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AnnouncementReach"},
"getIncident": {"method":"GET","path":"/incidents/{incidentId}","contract":"maintenance","summary":"Read an incident","permission":"INCIDENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"IncidentDetail"},
"listAnnouncements": {"method":"GET","path":"/announcements","contract":"workforce","summary":"What staff have been told","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"unacknowledgedOnly","in":"query","required":null}],"requestBody":null,"responds":"Announcement"},
"listIncidents": {"method":"GET","path":"/incidents","contract":"maintenance","summary":"List incidents","permission":"INCIDENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"isReportable","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listInspectionTemplates": {"method":"GET","path":"/inspection-templates","contract":"maintenance","summary":"List inspection templates","permission":"INSPECTION_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"InspectionTemplate"},
"listInspections": {"method":"GET","path":"/inspections","contract":"maintenance","summary":"List completed inspections","permission":"INSPECTION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"templateId","in":"query","required":null},{"name":"assetId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"performedFrom","in":"query","required":null},{"name":"performedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listScans": {"method":"GET","path":"/access/scans","contract":"access","summary":"List scan events","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"accessPointId","in":"query","required":null},{"name":"ticketId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"recordedFrom","in":"query","required":null},{"name":"recordedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"logout": {"method":"POST","path":"/auth/logout","contract":"identity","summary":"Close the current session","permission":null,"offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"publishAnnouncement": {"method":"POST","path":"/announcements","contract":"workforce","summary":"Tell staff something","permission":"ANNOUNCEMENT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Announcement","responds":"Announcement"},
"recordAuthorityNotification": {"method":"POST","path":"/incidents/{incidentId}/notify-authority","contract":"maintenance","summary":"Record notification to an external authority","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Incident"},
"submitInspection": {"method":"POST","path":"/inspections","contract":"maintenance","summary":"Submit a completed inspection","permission":"INSPECTION_SUBMIT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SubmitInspectionRequest","responds":"InspectionResult"},
"syncScans": {"method":"POST","path":"/access/scans","contract":"access","summary":"Replay scans recorded offline","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ScanSyncResult"},
"updateIncident": {"method":"PATCH","path":"/incidents/{incidentId}","contract":"maintenance","summary":"Investigate, escalate or close an incident","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Incident"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Announcement": {"type":"object","x-ticvai-persistence":"workforce.announcement","required":["title","body","kind","publishedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"title":{"type":"string","maxLength":140},"body":{"type":"string","maxLength":4000},"kind":{"$ref":"#/components/schemas/AnnouncementKind"},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"departmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requiresAcknowledgement":{"type":"boolean"},"deliveryChannels":{"type":"array","description":"How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). `emergency` is sent by both whatever is set here.\n","items":{"type":"string","enum":["inApp","push"]},"default":["inApp","push"]},"expiresAt":{"type":"string","format":"date-time","nullable":true},"publishedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"publishedAt":{"type":"string","format":"date-time"},"locale":{"type":"string","nullable":true}}},
"AnnouncementKind": {"type":"string","description":"`emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission.\n","enum":["operational","safety","emergency","hr","celebration"]},
"AnnouncementReach": {"type":"object","x-ticvai-persistence":"none — computed from workforce.announcement_receipt","properties":{"announcementId":{"type":"string","format":"uuid"},"targeted":{"type":"integer"},"delivered":{"type":"integer"},"acknowledged":{"type":"integer"},"outstanding":{"type":"array","description":"**The list that matters.** For an operational notice it measures whether anyone read it; during an emergency it is the roll call.\n","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"onShift":{"type":"boolean"}}}}}},
"DenyReason": {"type":"string","description":"Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n","enum":["notFound","notYetValid","expired","alreadyUsed","reentryLimitReached","exitRequiredBeforeReentry","wrongAccessPoint","wrongPerformance","outsideAdmissionWindow","entitlementSuspended","blacklisted","capacityReached","waiverRequired","accompanimentRequired","mediaDeactivated","unpaid","delegatedRightExhausted","delegatedRightRevoked","journeyNotCovered"]},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"Incident": {"x-ticvai-persistence":"maintenance.incident","type":"object","required":["id","incidentNumber","kind","severity","status","venueId","occurredAt","reportedByPrincipalId"],"properties":{"id":{"type":"string","format":"uuid"},"incidentNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"kind":{"$ref":"#/components/schemas/IncidentKind"},"severity":{"$ref":"#/components/schemas/IncidentSeverity"},"status":{"$ref":"#/components/schemas/IncidentStatus"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"locationDescription":{"type":"string","nullable":true},"isReportable":{"type":"boolean","description":"Requires notification to an external authority within a statutory window."},"notificationDueAt":{"type":"string","format":"date-time","nullable":true},"notifiedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `notifiedAt` among this incident's authority notifications. **Maintained on write** by `recordAuthorityNotification`; each notification itself is a row of `maintenance.incident_authority_notification`.\n"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"reportedByPrincipalId":{"type":"string","format":"uuid"},"correctiveWorkOrderId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"IncidentAuthorityNotification": {"x-ticvai-persistence":"maintenance.incident_authority_notification","type":"object","description":"**One notification to an external authority, appended by `recordAuthorityNotification`.** An incident may be reported to more than one authority, or to the same one twice, and each is the evidence that an obligation was met — so each is a row, not an overwrite of `maintenance.incident.notified_at`.\n","required":["id","incidentId","authority","notifiedAt"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"authority":{"type":"string","maxLength":200},"reference":{"type":"string","maxLength":128,"nullable":true},"notifiedAt":{"type":"string","format":"date-time"},"notifiedByPrincipalId":{"type":"string","format":"uuid"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time"}}},
"IncidentDetail": {"x-ticvai-persistence":"maintenance.incident","allOf":[{"$ref":"#/components/schemas/Incident"},{"type":"object","properties":{"description":{"type":"string","description":"The original report. Never edited — investigation adds to the record."},"investigationNote":{"type":"string","nullable":true,"readOnly":true,"description":"The latest entry of `investigationNotes`, kept for readers that show one line."},"investigationNotes":{"type":"array","readOnly":true,"description":"**Every investigation note, oldest first** (decided 28 September, audit R106 (5)). Read from `maintenance.incident_investigation_note`; appended by `updateIncident`.\n","items":{"$ref":"#/components/schemas/IncidentInvestigationNote"}},"rootCause":{"type":"string","nullable":true},"correctiveActions":{"type":"string","nullable":true},"firstAidGiven":{"type":"boolean"},"emergencyServicesCalled":{"type":"boolean"},"witnessCount":{"type":"integer"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"involvedParties":{"type":"array","description":"Who was involved, as given in `ReportIncidentRequest.involvedSubjectIds` and `involvedStaffPrincipalIds`. Read from `maintenance.incident_involved_party`.\n","items":{"$ref":"#/components/schemas/IncidentInvolvedParty"}},"authorityNotifications":{"type":"array","description":"Read from `maintenance.incident_authority_notification`, oldest first.","items":{"$ref":"#/components/schemas/IncidentAuthorityNotification"}}}}]},
"IncidentInvestigationNote": {"x-ticvai-persistence":"maintenance.incident_investigation_note","type":"object","description":"**One investigation note, appended by `updateIncident`** (decided 28 September, audit R106 (5)). A history rather than a field, so what an investigator thought on Tuesday survives what they found on Thursday.\n","required":["id","incidentId","note","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"note":{"type":"string","maxLength":10000},"writtenByPrincipalId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"}}},
"IncidentInvolvedParty": {"x-ticvai-persistence":"maintenance.incident_involved_party","type":"object","description":"**One person involved in an incident, by opaque reference.** A guest or member of the public is a `pii.subject` id — personal details live there, the erasable store of ADR-0023, so the incident record survives an erasure request intact. A member of staff is a principal id. Exactly one of the two is set, as `kind` says.\n","required":["id","incidentId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["subject","staff"]},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"A `pii.subject` id where `kind` is `subject`."},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"The staff principal where `kind` is `staff`."}}},
"IncidentKind": {"type":"string","enum":["guestInjury","staffInjury","nearMiss","propertyDamage","equipmentFailure","securityIncident","fireOrEvacuation","foodSafety","environmental","other"]},
"IncidentSeverity": {"type":"string","enum":["nearMiss","minor","moderate","major","critical"]},
"IncidentStatus": {"type":"string","enum":["reported","underInvestigation","actionRequired","closed"]},
"Inspection": {"x-ticvai-persistence":"maintenance.inspection","type":"object","required":["id","templateId","venueId","outcome","performedByPrincipalId","performedAt"],"properties":{"id":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid"},"templateName":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"outcome":{"$ref":"#/components/schemas/InspectionOutcome"},"failedItemCount":{"type":"integer"},"failedSafetyCriticalCount":{"type":"integer"},"performedByPrincipalId":{"type":"string","format":"uuid","description":"An inspection nobody signed is not an inspection."},"performedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true},"retainUntil":{"type":"string","format":"date","nullable":true}}},
"InspectionItem": {"x-ticvai-persistence":"maintenance.inspection_item","type":"object","description":"**One answer to one question, which the API has always accepted and never stored.** `SubmitInspectionRequest.responses[]` takes a key, a value, a pass flag, a note and attachments; the only persistence ever claimed for them was `maintenance.inspection_response`, a table that does not exist.\nSo `maintenance.inspection_template_item` held the questions, `maintenance.inspection` held `failedItemCount` and `failedSafetyCriticalCount`, and **which check failed was accepted over the wire and dropped** — on a record that takes an asset out of service.\nReturned on `InspectionResult`, not on `Inspection`: `listInspections` returns the latter in a list, and twenty item rows per inspection on a list screen is the wrong trade. The counts stay for exactly that reason.\n","required":["id","inspectionId","itemKey"],"properties":{"id":{"type":"string","format":"uuid"},"inspectionId":{"type":"string","format":"uuid"},"templateItemId":{"type":"string","format":"uuid","nullable":true,"description":"**Nullable because a template changes and an inspection does not.** An answer recorded against an item that was later removed still has to be readable, so the key below is the durable record and this is the live link.\n"},"itemKey":{"type":"string","maxLength":120,"description":"The template item's `key`, copied at submission and never updated."},"label":{"type":"string","nullable":true,"description":"The question as it was asked, copied at submission. **A template reworded next season must not silently reword last season's inspection.**\n"},"value":{"nullable":true,"description":"Whatever the item's `kind` calls for — a boolean, a number, a string."},"passed":{"type":"boolean","nullable":true,"description":"Null where the item is informational rather than pass or fail."},"isSafetyCritical":{"type":"boolean","default":false,"description":"Copied from the template item at submission, for the same reason as `label`: it is what makes `failedSafetyCriticalCount` reproducible, and the template can change.\n"},"note":{"type":"string","maxLength":1000,"nullable":true},"attachmentAssetIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"**A deliberate array, and the same exception as `workforce.sync_conflict.affectedAssignmentIds`**: evidence attached to this answer at the moment it was recorded. It is never queried from the other end — nobody asks which inspection items reference a photograph — and it must not change when an asset library is reorganised.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"InspectionItemKind": {"type":"string","enum":["passFail","yesNo","numeric","text","photo","signature"]},
"InspectionOutcome": {"type":"string","enum":["passed","passedWithObservations","failed"]},
"InspectionResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["inspection","consequences"],"properties":{"inspection":{"$ref":"#/components/schemas/Inspection"},"items":{"type":"array","description":"**The answers, which had nowhere to live until 20 September.** A failed safety-critical item takes an asset out of service and `consequences` below says it happened; this says which check caused it.\n","items":{"$ref":"#/components/schemas/InspectionItem"}},"consequences":{"type":"object","description":"What the submission triggered. A failed safety-critical item takes the asset out of service without waiting for anyone to decide.\n","properties":{"assetTakenOutOfService":{"type":"boolean"},"workOrdersRaised":{"type":"array","items":{"type":"string","format":"uuid"}},"productsSuspended":{"type":"array","items":{"type":"string","format":"uuid"}},"escalatedToPrincipalId":{"type":"string","format":"uuid","nullable":true}}}}},
"InspectionTemplate": {"x-ticvai-persistence":"maintenance.inspection_template + maintenance.inspection_template_item","type":"object","required":["id","code","name","items"],"properties":{"instructions":{"type":"string","description":"**The procedure itself.** A technician asking how to isolate a chiller is asking a safety question, and the answer has to come from the template rather than from its title.\n"},"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid","nullable":true},"appliesToAssetCategoryId":{"type":"string","format":"uuid","nullable":true},"frequency":{"type":"string","enum":["preOpening","postClosing","daily","weekly","monthly","annual","adHoc"]},"items":{"type":"array","minItems":1,"items":{"type":"object","required":["key","label","kind","isRequired"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"kind":{"$ref":"#/components/schemas/InspectionItemKind"},"isRequired":{"type":"boolean"},"isSafetyCritical":{"type":"boolean","default":false,"description":"A failed safety-critical item **blocks the inspection from passing** and cannot be overridden by completing the rest.\n"},"requiresPhotoOnFail":{"type":"boolean","default":true},"minValue":{"type":"number","nullable":true},"maxValue":{"type":"number","nullable":true},"guidance":{"type":"string","nullable":true}}}},"retentionYears":{"type":"integer","default":7,"description":"Compliance inspections are retained alongside the financial trail."},"isActive":{"type":"boolean"}}},
"OfflineScan": {"x-ticvai-persistence":"none — client-side journal","allOf":[{"$ref":"#/components/schemas/ValidateRequest"},{"type":"object","required":["sequence","localOutcome"],"properties":{"sequence":{"type":"integer","minimum":1,"description":"Monotonic per device. The server processes in this order."},"localOutcome":{"allOf":[{"$ref":"#/components/schemas/ScanOutcome"}],"description":"What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded.\n"},"localDenyReason":{"$ref":"#/components/schemas/DenyReason"},"overriddenByPrincipalId":{"type":"string","format":"uuid","nullable":true},"overrideReason":{"type":"string","nullable":true}}}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ScanEvent": {"x-ticvai-append-only":"recordedAt","x-ticvai-persistence":"access.scan_event","type":"object","required":["id","accessPointId","venueId","outcome","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The scan's client-generated UUIDv7, the key offline replay deduplicates on."},"accessPointId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"ticketId":{"type":"string","format":"uuid","nullable":true,"description":"The `Entitlement.id` scanned; null where the media resolved to nothing."},"mediaCode":{"type":"string","nullable":true},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"direction":{"$ref":"#/components/schemas/Direction"},"operatorPrincipalId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","format":"uuid","nullable":true},"overridesScanId":{"type":"string","format":"uuid","nullable":true,"description":"**Set only on an override row**, naming the denied scan it admits against (decided 28 September, audit R228). The denied scan itself is never updated: the denial and the override are two rows, and at most one override row names any scan. Null on every other scan.\n"},"overrideReason":{"type":"string","nullable":true,"description":"The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`."},"dynamicPolicyId":{"type":"string","format":"uuid","nullable":true,"description":"The dynamic access policy (`access.dynamic_policy`) whose result decided this scan; null when no dynamic policy matched and the entitlement alone decided (added 29 September, build pass, 3.3.48). `listDynamicPolicyEffectiveness` counts from it."},"dynamicPolicyVersion":{"type":"integer","minimum":1,"nullable":true,"description":"The version of that policy in force at the scan, so a report spanning a change counts each version apart."},"dynamicPolicyResult":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"],"nullable":true,"description":"What the policy decided, which for a step-up is not the same as the scan's outcome."},"quantity":{"type":"integer","minimum":1,"default":1,"description":"Admissions this scan counted. More than one only for a group wave (`validateGroupAccess`) or a quantity entitlement consumed in one pass (added 29 September, data-model close-out DM1)."},"localSequence":{"type":"integer","nullable":true,"description":"The device-local sequence number of a scan recorded offline; null for an online scan (added 29 September, data-model close-out DM1)."},"policySetVersion":{"type":"string","nullable":true,"description":"The admission policy set the scan was decided under (`OfflinePackage.policySetVersion`, or the same fingerprint computed online by `validateAccess`), beside the one policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`). ADR-0068, 1 October."},"packageVersion":{"type":"string","nullable":true,"description":"The offline package (`access.edge_package`) the device validated against; null for an online scan (added 29 September, data-model close-out DM1)."},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while pending. Differs from recordedAt for offline scans."}}},
"ScanOutcome": {"type":"string","enum":["admitted","denied","overridden"]},
"ScanSyncResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["accepted","results"],"properties":{"accepted":{"type":"integer","description":"Entries processed before any stop."},"stoppedAtSequence":{"type":"integer","nullable":true,"description":"Sequence of the first entry that could not be processed. Null when the whole batch succeeded. The client retries from here — never past it.\n"},"results":{"type":"array","items":{"type":"object","required":["id","sequence","status"],"properties":{"id":{"type":"string"},"sequence":{"type":"integer"},"status":{"type":"string","enum":["accepted","duplicate","reconciled","rejected"]},"serverOutcome":{"$ref":"#/components/schemas/ScanOutcome"},"divergence":{"type":"string","nullable":true,"description":"Present when `reconciled` — the device admitted and the server would have denied, or vice versa. Surfaced to the operator, not swallowed.\n"},"error":{"$ref":"../shared/common.yaml#/components/schemas/Problem"}}}}}},
"SubmitInspectionRequest": {"x-ticvai-persistence":"maintenance.inspection + maintenance.inspection_item","type":"object","required":["id","templateId","venueId","responses","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"responses":{"type":"array","minItems":1,"items":{"type":"object","required":["key","value"],"properties":{"key":{"type":"string"},"value":{},"passed":{"type":"boolean","nullable":true},"note":{"type":"string","maxLength":1000},"attachmentRefs":{"type":"array","items":{"type":"string"}}}}},"signatureRef":{"type":"string","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"ValidateRequest": {"type":"object","required":["id","mediaCode","mediaKind","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key and dedupe key."},"mediaCode":{"type":"string","maxLength":256,"description":"What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life.\n"},"mediaKind":{"$ref":"#/components/schemas/MediaKind"},"direction":{"$ref":"#/components/schemas/Direction"},"groupSize":{"type":"integer","minimum":1,"description":"For group media admitting several holders on one read."},"proximityToken":{"type":"string","description":"BLE proximity assertion where the venue requires the operator to be physically at the gate. Absent where not configured.\n"},"recordedAt":{"type":"string","format":"date-time","description":"Device time of the read. Authoritative for ordering, not for validity."}}}
}
```
