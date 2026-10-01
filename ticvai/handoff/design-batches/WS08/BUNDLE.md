# WS08 — Access Control board 8

**10 screens · 22 operations · 34 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `ACCESS_POINT_CONFIGURE, MARKETING_VIEW, QUEUE_MANAGE, QUEUE_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-214` | Guest Journey Command Center | B–D | 8 | 220 | 6 | 1 | 1 | 6 | — | notStarted (generated) |
| `BO-215` | Group & B2B Admission Profile Builder | B–D | 7 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-216` | Group Leader & Fast B2B Validation | B–D | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-217` | Group Attendance & Partial Entry Manager | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-218` | Family, Child, POD & Companion Journey | B–D | 13 | 0 | 5 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-219` | Re-entry & Temporary Exit Journey | B–D | 4 | 0 | 5 | 9 | 0 | 6 | — | notStarted (generated) |
| `BO-220` | Multi-Park & Crossover Journey Orchestrator | B–D | 47 | 0 | 6 | 9 | 0 | 6 | — | notStarted (generated) |
| `BO-221` | Fast Pass & Attraction Access Journey | B–D | 27 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-222` | Special Event, Free View & Alternative Admission | A | 13 | 0 | 5 | 1 | 0 | 0 | — | notStarted (generated) |
| `BO-223` | Journey Simulation, Audit & Publication | B–D | 8 | 12 | 6 | 9 | 0 | 6 | — | notStarted (generated) |

## Thin screens in this batch

**BO-216, BO-217, BO-220, BO-222 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-214` Guest Journey Command Center

**Central configuration and monitoring screen for all special and multi-person admission journeys.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/guest-journey-command-center-bo-214` |

#### Inputs: what the user enters or picks

**Form: Save journey profile** (modal, opened by *Save journey profile*; *Save journey profile* calls `setJourneyProfile`, *Cancel* sends nothing)

**Collects what `setJourneyProfile` sends before it is called.** Required: `id`, `scopePath`, `name`, `status`. Optional: `venueId`, `journeyType`, `credentialType`, `steps`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | The journeyProfileId | `setJourneyProfile` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | Null is every park of the tenant | `setJourneyProfile` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setJourneyProfile` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setJourneyProfile` body |
| Journey type `journeyType` | text field | optional | — | max length 60 | — | e.g. | `setJourneyProfile` body |
| Credential type `credentialType` | text field | optional | — | max length 100 | — | e.g. | `setJourneyProfile` body |
| Status `status` | segmented control | required | Active | Active · Inactive | — | — | `setJourneyProfile` body |
| Steps `steps` | repeatable rows | optional | — | — | — | Ordered journey steps, each an accessPointId with a direction (entry or exit) and an optional local time HH:MM, as GuestJourneySimulationInput.steps | `setJourneyProfile` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**Active Journey Profiles** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Group Arrivals Today** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Guests via Group Admission** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Family Journeys** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Re-entry Guests** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Crossovers Today** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Fast Pass Validations** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Special Event Admissions** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**VIP Admissions** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Journey Exceptions** (metric tile, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**Every guest journey** (data table, from `listGuestJourney`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Journey profile | text | Journey profile identifier |
| Journey name | text | Journey, e.g. |
| Journey type | text | Journey type, e.g. |
| Venue | text | Venue or all parks |
| Credential type | text | Credential used, e.g. |
| Status | chip: Active, Inactive | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active journey profiles | 1,234 | Active Journey Profiles |
| Group arrivals today | 1,234 | Group Arrivals Today |
| Guests via group admission | 1,234 | Guests via Group Admission |
| Family journeys | 1,234 | Family Journeys |
| Re entry guests | 1,234 | Re-entry Guests |
| Crossovers today | 1,234 | Crossovers Today |
| Fast pass validations | 1,234 | Fast Pass Validations |
| Special event admissions | 1,234 | Special Event Admissions |
| Vip admissions | 1,234 | VIP Admissions |
| Journey exceptions | 1,234 | Journey Exceptions |

**The selected guest journey** (detail panel): The pack groups this record's detail under its own headings: “Journey Type Venue Credential Status”.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save journey profile (primary button) | `setJourneyProfile` PUT `/journey-profiles` | AccessJourneyProfile | AccessJourneyProfile | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Data it reads**: `listGuestJourney` (onLoad, Guest Journey Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-215` Group & B2B Admission Profile Builder: *Works in Group & B2B Admission Profile Builder*; calls `listGuestJourney`
- → `BO-216` Group Leader & Fast B2B Validation: *Works in Group Leader & Fast B2B Validation*; calls `listGuestJourney`
- → `BO-217` Group Attendance & Partial Entry Manager: *Works in Group Attendance & Partial Entry Manager*; calls `listGuestJourney`
- → `BO-218` Family, Child, POD & Companion Journey: *Works in Family, Child, POD & Companion Journey*; calls `listGuestJourney`
- → `BO-219` Re-entry & Temporary Exit Journey: *Works in Re-entry & Temporary Exit Journey*; calls `listGuestJourney`
- → `BO-220` Multi-Park & Crossover Journey Orchestrator: *Works in Multi-Park & Crossover Journey Orchestrator*; calls `listGuestJourney`
- → `BO-221` Fast Pass & Attraction Access Journey: *Works in Fast Pass & Attraction Access Journey*; calls `listGuestJourney`
- → `BO-222` Special Event, Free View & Alternative Admission: *Works in Special Event, Free View & Alternative Admission*; calls `listGuestJourney`
- → `BO-223` Journey Simulation, Audit & Publication: *Works in Journey Simulation, Audit & Publication*; calls `listGuestJourney`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest journey list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest journey untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest journey yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guest journey are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listGuestJourney` → `SCOPE_VIEW` (read) · staff
- `createAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `setJourneyProfile` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.51 | Admission entitlement management | Ticketing Catalogue | CONTRACTED | `createAdmissionRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-214` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-214`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 1: Opens Guest Journey Command Center → Central configuration and monitoring screen for all special and multi-person admission journeys.
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F118 branch at step 1 (expected): when Nothing has been set up on Guest Journey Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F118 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (220 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-214?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save journey profile.
- [ ] Every transition is wired: `BO-100`, `BO-215`, `BO-216`, `BO-217`, `BO-218`, `BO-219`, `BO-220`, `BO-221`, `BO-222`, `BO-223`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-215` Group & B2B Admission Profile Builder

**Group & B2B Admission Profile Builder**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure admission for) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/group-b2b-admission-profile-builder-bo-215` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Schools | select field | — | — | — | — | — | — |
| Tour Operators | select field | — | — | — | — | — | — |
| Corporate Groups | select field | — | — | — | — | — | — |
| Resellers | select field | — | — | — | — | — | — |
| Travel Groups | select field | — | — | — | — | — | — |
| Camps | select field | — | — | — | — | — | — |
| Families | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `setGroupAdmissionProfile`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group b2b admission configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group b2b admission untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group b2b admission configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGroupAdmissionProfile` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group/B2B admission profile view shows entry statistics by category (general admission, group, re-entry, crossover) and attendance breakdowns for schools and other groups from scanned tickets. *(client request · MoM 2 Sep 2026, 4.15 Guest Journey, Group/B2B Profiles & Live Operations Dashboard · DI-647)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-215` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-215`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 2: Works in Group & B2B Admission Profile Builder → Group & B2B Admission Profile Builder

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-215?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-216` Group Leader & Fast B2B Validation

**Solve the specific matrix requirement for faster entrance flow when large B2B groups have multiple tickets stored on one device.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/group-leader-fast-b2b-validation-bo-216` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every group leader fast** (data table, from `listGroupLeaderFast`)

| Shows | Format | Notes |
|---|---|---|
| Payment | yes / no (icon or chip) | Payment check passed |
| Booking | yes / no (icon or chip) | Booking check passed |
| Group product | yes / no (icon or chip) | Group product check passed |
| Access rules | yes / no (icon or chip) | Access rules check passed |
| Manifest | yes / no (icon or chip) | Manifest check passed |

**The selected group leader fast** (detail panel): The pack groups this record's detail under its own headings: “Booked”, “SCAN LEADER QR”, “Admit All 120”, “Enter Actual Attendance”, “CONFIRM”, “Attendance”.

| Shows | Format | Notes |
|---|---|---|
| Payment | yes / no (icon or chip) | Payment check passed |
| Booking | yes / no (icon or chip) | Booking check passed |
| Group product | yes / no (icon or chip) | Group product check passed |
| Access rules | yes / no (icon or chip) | Access rules check passed |
| Manifest | yes / no (icon or chip) | Manifest check passed |

**Data it reads**: `listGroupLeaderFast` (onLoad, Group Leader & Fast B2B Validation)

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `listGroupLeaderFast`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group leader fast list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group leader fast untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group leader fast yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group leader fast are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGroupLeaderFast` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-216` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-216`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 4: Works in Group Leader & Fast B2B Validation → Solve the specific matrix requirement for faster entrance flow when large B2B groups have multiple tickets stored on one device.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-216?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-217` Group Attendance & Partial Entry Manager

**Manage actual attendance when fewer guests arrive than the quantity purchased. The matrix explicitly requires the scanner to show the exact group size and allow the operator to enter actual attendants so daily attendance is updated correctly.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/group-attendance-partial-entry-manager-bo-217` |

**Known gaps.** **Group Attendance & Partial Entry Manager declares no operation that writes anything** — its only declared call is `listGroupAttendancePartial`, a read. The name promises authoring and the contract … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listGroupAttendancePartial` (onLoad, Group Attendance & Partial Entry Manager)

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `listGroupAttendancePartial`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group attendance partial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group attendance partial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group attendance partial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group attendance partial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGroupAttendancePartial` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group/B2B admission profile view shows entry statistics by category (general admission, group, re-entry, crossover) and attendance breakdowns for schools and other groups from scanned tickets. *(client request · MoM 2 Sep 2026, 4.15 Guest Journey, Group/B2B Profiles & Live Operations Dashboard · DI-647)*
- Group tickets can carry one shared QR code or individual QR codes, with partial check-in tracking; family tickets bundle adult/child pricing. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-137)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-217` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-217`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 6: Works in Group Attendance & Partial Entry Manager → Manage actual attendance when fewer guests arrive than the quantity purchased. The matrix explicitly requires the scanner to show the exact group size and allow the operator to enter actual …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-217?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-218` Family, Child, POD & Companion Journey

**Configure linked-person access journeys. The matrix requires child protection through adult-ticket pairing or biometric validation of the assigned adult. It also requires POD accompanying persons and nannies to be bound to a primary guest and only enter when accompanied by that guest.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/family-child-pod-companion-journey-bo-218` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Parent → Child | select field | — | — | — | — | — | — |
| Guardian → Minor | select field | — | — | — | — | — | — |
| POD → Companion | select field | — | — | — | — | — | — |
| Primary Guest → Nanny | text field | — | — | — | — | — | — |
| Group Leader → Group Member | text field | — | — | — | — | — | — |

**Sent by *Save companion rule*** (`setGuestCompanionEligibility`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rule `ruleId` | picker: choose a rule | optional | — | — | shows names, sends the id | Absent creates a rule | `setGuestCompanionEligibility` body |
| Venue `venueId` | text field | required | — | — | — | — | `setGuestCompanionEligibility` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setGuestCompanionEligibility` body |
| Guest category `guestCategory` | select | required | — | Adult · Child · Junior · Senior · Pod · Pod companion · Nanny · Vip · Member · Staff · Accreditation · Customer segment | — | — | `setGuestCompanionEligibility` body |
| Required companion category `requiredCompanionCategory` | radio group | required | — | Adult · Pod companion · Nanny · Guardian | — | Category of the companion who must be present | `setGuestCompanionEligibility` body |
| Companion verification `companionVerification` | segmented control | optional | Linked ticket | Linked ticket · Companion biometric | — | — | `setGuestCompanionEligibility` body |
| Verify at `verifyAt` | multi-select chips | required | — | Admission · Exit · Attraction; at least 1 | — | Where the companion is checked | `setGuestCompanionEligibility` body |
| Attractions `attractionIds` | list of values (chips) | optional | — | — | — | Where verifyAt includes attraction | `setGuestCompanionEligibility` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save companion rule (primary button) | `setGuestCompanionEligibility` PUT `/guest-companion-eligibility` | GuestCompanionEligibilityRulesInput | GuestCompanionEligibilityRulesView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Data it reads**: `listFamilyChildPod` (onLoad, Family, Child, POD & Companion Journey)

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `listFamilyChildPod`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The family child pod configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the family child pod untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No family child pod configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listFamilyChildPod` → `SCOPE_VIEW` (read) · staff
- `setGuestCompanionEligibility` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-218` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-218`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 8: Works in Family, Child, POD & Companion Journey → Configure linked-person access journeys. The matrix requires child protection through adult-ticket pairing or biometric validation of the assigned adult. It also requires POD accompanying persons and …

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-218?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save companion rule.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-219` Re-entry & Temporary Exit Journey

**Manage guests temporarily leaving and returning to the venue. The source matrix requires configurable re-entry and also describes a journey using a designated re-entry gate with both ticket verification and a UV stamp.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/access-venue/re-entry-temporary-exit-journey-bo-219` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Credential only | select field | — | — | — | — | — | — |
| Credential + UV stamp | text field | — | — | — | — | — | — |
| Credential + Face | select field | — | — | — | — | — | — |
| Credential + operator | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listEntryTemporaryExit` (onLoad, Re-entry & Temporary Exit Journey); `listAdmissionRules` (onLoad, The admission profiles that allow a temporary exit)

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `listEntryTemporaryExit`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The re-entry temporary exit configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the re-entry temporary exit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No re-entry temporary exit configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before validity.from |

#### Permissions

- `listEntryTemporaryExit` → `SCOPE_VIEW` (read) · staff
- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff
- `updateAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |
| 3.2.34 | The access rules can be modified even after the ticket has been issued. | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.62 | It must be possible to change the access control organization process on special dates. Venue is organizing on regular basis free view days where the main gate access control doors are opened letting … | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.71 | The access control can support special requirements for special events such as but not limited to: -definition of a specific product that can capture attendance without physical admission, -special … | Admission and Access | CONTRACTED | `updateAdmissionRules` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-219` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-219`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 10: Works in Re-entry & Temporary Exit Journey → Manage guests temporarily leaving and returning to the venue. The source matrix requires configurable re-entry and also describes a journey using a designated re-entry gate with both ticket …

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-219?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-220` Multi-Park & Crossover Journey Orchestrator

**Operationalize the multi-park rules configured in Board 2. The matrix specifically distinguishes crossover from normal entry and re-entry and requires crossover to be tracked separately.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/access-venue/multi-park-crossover-journey-orchestrator-bo-220` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Sent by *Save admission rules*** (`updateAdmissionRules`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `updateAdmissionRules` body |
| Per product rules `perProductRules` | repeatable rows | optional | — | — | — | BL-059. Transaction rules were per profile and a ticket type could not state its own. | `updateAdmissionRules` body |
| Product `perProductRules[].productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `updateAdmissionRules` body |
| Entries per day `perProductRules[].entriesPerDay` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Minimum gap minutes `perProductRules[].minimumGapMinutes` | number field (minutes) | optional | — | — | — | Anti-passback in minutes rather than a boolean. A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back … | `updateAdmissionRules` body |
| Allowed access points `perProductRules[].allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | — | `updateAdmissionRules` body |
| Biometric policy `perProductRules[].biometricPolicy` | segmented control | optional | — | Disabled · Offered · Preferred | — | BL-105, 3.2.9. The biometric check is a property of the product, not of the venue — memberships checked, day tickets not. | `updateAdmissionRules` body |
| Max passes per biometric identity `perProductRules[].maxPassesPerBiometricIdentity` | number field | optional | — | min 1 | — | BL-096, 2.14.7. The annual-pass quota, keyed to biometric identity. | `updateAdmissionRules` body |
| Name `name` | text field | required | — | max length 200 | — | — | `updateAdmissionRules` body |
| Open minutes before `openMinutesBefore` | number field (minutes) | required | — | — | — | How long before a performance validation opens. | `updateAdmissionRules` body |
| Close minutes after `closeMinutesAfter` | number field (minutes) | required | — | — | — | — | `updateAdmissionRules` body |
| Max duration minutes `maxDurationMinutes` | number field (minutes) | optional | — | — | — | — | `updateAdmissionRules` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Max reentries `maxReentries` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Entry limit `entryLimit` | group | optional | — | — | — | How many times the credential may enter (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). | `updateAdmissionRules` body |
| Mode `entryLimit.mode` | radio group | required | Unlimited | Unlimited · Once · N times · N per day · N per period | — | — | `updateAdmissionRules` body |
| Count `entryLimit.count` | number field | optional | — | min 1 | — | N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it) | `updateAdmissionRules` body |
| Period days `entryLimit.periodDays` | number field (days) | optional | — | min 1 | — | The period for nPerPeriod | `updateAdmissionRules` body |
| Exit scan `exitScan` | segmented control | optional | Optional | Required · Optional · None | — | (decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. | `updateAdmissionRules` body |
| Max exits `maxExits` | number field | optional | — | min 0 | — | Null is unlimited (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Re entry window minutes `reEntryWindowMinutes` | number field (minutes) | optional | — | min 1 | — | Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Same day only `sameDayOnly` | toggle | optional | on | — | — | Re-entry only on the day of the exit (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Designated access points `designatedAccessPointIds` | multi-picker: choose designated access points | optional | — | — | — | Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Validity `validity` | group | optional | — | — | — | When the credential is valid (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). | `updateAdmissionRules` body |
| Anchor `validity.anchor` | radio group | required | — | Fixed range · After sale · After activation · After first use | — | fixedRange uses from and to; the others count days from the event | `updateAdmissionRules` body |
| Days `validity.days` | number field | optional | — | min 1 | — | N days after the anchor; required unless the anchor is fixedRange | `updateAdmissionRules` body |
| From `validity.from` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateAdmissionRules` body |
| To `validity.to` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Inclusive. | `updateAdmissionRules` body |
| End of `validity.endOf` | radio group | optional | — | Day · Week · Month · Year | — | Validity runs to the end of the day, week, month or year the relative period ends in | `updateAdmissionRules` body |
| Days of week `validity.daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | Empty is every day | `updateAdmissionRules` body |
| Day types `validity.dayTypes` | multi-select chips | optional | — | Peak dates · Off peak dates · Holidays · Seasons · Event dates | — | Calendar day types on which access is allowed; empty is every day type | `updateAdmissionRules` body |
| Blackout dates `validity.blackoutDates` | list of values (chips) | optional | — | — | — | Dates on which access is refused whatever else allows it | `updateAdmissionRules` body |
| Crossover `crossover` | group | optional | — | — | — | Crossover between parks (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. | `updateAdmissionRules` body |
| Allowed park org units `crossover.allowedParkOrgUnitIds` | multi-picker: choose allowed park org units | required | — | at least 2 | — | — | `updateAdmissionRules` body |
| Park order `crossover.parkOrder` | multi-picker: choose park order | optional | — | — | — | Required order of parks, if any; empty is any order | `updateAdmissionRules` body |
| Same day only `crossover.sameDayOnly` | toggle | optional | on | — | — | — | `updateAdmissionRules` body |
| Different day access `crossover.differentDayAccess` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Day pattern `crossover.dayPattern` | segmented control | optional | Flexible within validity | Consecutive from first scan · Flexible within validity | — | — | `updateAdmissionRules` body |
| Max park entries `crossover.maxParkEntries` | number field | optional | — | min 1 | — | Null is unlimited | `updateAdmissionRules` body |
| Crossover quantity `crossover.crossoverQuantity` | number field | optional | — | min 1 | — | How many crossovers; null is unlimited | `updateAdmissionRules` body |
| Crossover after time `crossover.crossoverAfterTime` | time picker | optional | — | — | HH:mm, 24-hour | Earliest venue-local time HH:MM a crossover is allowed | `updateAdmissionRules` body |
| Prerequisite park org unit `crossover.prerequisiteParkOrgUnitId` | picker: choose a prerequisite park org unit | optional | — | — | shows names, sends the id | The park that must be entered first | `updateAdmissionRules` body |
| Re entry after crossover `crossover.reEntryAfterCrossover` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Allowed access points `allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Empty means any access point in the venue. | `updateAdmissionRules` body |
| Re entry verification `reEntryVerification` | radio group | optional | Credential only | Credential only · Credential uv stamp · Credential face · Credential operator · Custom | — | What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1). | `updateAdmissionRules` body |
| … 2 more | | | | | | the rest are in `schemas.json` | `updateAdmissionRules` body |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save admission rules (primary button) | `updateAdmissionRules` PUT `/admission-rules/{profileId}` | AdmissionRules | AdmissionRules | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before … | — |

**Data it reads**: `listMultiParkCrossover2` (onLoad, Multi-Park & Crossover Journey Orchestrator); `listMultiParkCrossover` (onLoad, Multi-Park & Crossover Rules); `listAdmissionRules` (onLoad, The admission profiles that carry crossover rules)

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `listMultiParkCrossover2`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-park crossover journey list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-park crossover journey untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-park crossover journey yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multi-park crossover journey are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before validity.from |

#### Permissions

- `listMultiParkCrossover2` → `SCOPE_VIEW` (read) · staff
- `listMultiParkCrossover` → `SCOPE_VIEW` (read) · staff
- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff
- `updateAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |
| 3.2.34 | The access rules can be modified even after the ticket has been issued. | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.62 | It must be possible to change the access control organization process on special dates. Venue is organizing on regular basis free view days where the main gate access control doors are opened letting … | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.71 | The access control can support special requirements for special events such as but not limited to: -definition of a specific product that can capture attendance without physical admission, -special … | Admission and Access | CONTRACTED | `updateAdmissionRules` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-220` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-220`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 12: Works in Multi-Park & Crossover Journey Orchestrator → Operationalize the multi-park rules configured in Board 2. The matrix specifically distinguishes crossover from normal entry and re-entry and requires crossover to be tracked separately.

#### Acceptance for the design

- [ ] Every input above is drawn (47), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-220?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save admission rules.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-221` Fast Pass & Attraction Access Journey

**Configure the operational experience for limited and unlimited priority-access entitlements. The matrix requires Silver Fast Pass to support three accesses and Gold to support unlimited access with an optional one-access-per-ride restriction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `QUEUE_MANAGE`, `QUEUE_VIEW`, `SCOPE_VIEW` (2 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select eligible) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `queueId` (navigation) |
| Route | `/access-venue/fast-pass-attraction-access-journey-bo-221` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Roller Coaster | select field | — | — | — | — | — | — |
| Drop Tower | select field | — | — | — | — | — | — |
| Water Ride | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Open only | toggle | off | — | `listQueues` ?openOnly |

**Form: Save fast pass profile** (modal, opened by *Save fast pass profile*; *Save fast pass profile* calls `setFastPassProfile`, *Cancel* sends nothing)

**Collects what `setFastPassProfile` sends before it is called.** Required: `id`, `scopePath`, `name`, `unlimited`. Optional: `venueId`, `totalUses`, `consumptionPerValidation`, `onePerRide`, `eligibleAttractionCategories`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | The profileId the list shows | `setFastPassProfile` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setFastPassProfile` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setFastPassProfile` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setFastPassProfile` body |
| Unlimited `unlimited` | toggle | required | off | — | — | — | `setFastPassProfile` body |
| Total uses `totalUses` | number field | optional | — | min 1 | — | Null when unlimited | `setFastPassProfile` body |
| Consumption per validation `consumptionPerValidation` | number field | optional | 1 | min 1 | — | — | `setFastPassProfile` body |
| One per ride `onePerRide` | toggle | optional | off | — | — | — | `setFastPassProfile` body |
| Eligible attraction categories `eligibleAttractionCategories` | list of values (chips) | optional | — | — | — | The list's eligibleType, e.g. | `setFastPassProfile` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `totalUses` missing on a limited profile.

**Sent by *Save Fast Pass settings*** (`updateQueue`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | The same locale-to-text map `createQueue` takes and `Queue` returns, so an edit form round-trips the name. | `updateQueue` body |
| Capacity per cycle `capacityPerCycle` | number field | optional | — | min 1 | — | — | `updateQueue` body |
| Cycle minutes `cycleMinutes` | number field (minutes) | optional | — | min 0 | — | — | `updateQueue` body |
| Max party size `maxPartySize` | number field | optional | — | min 1 | — | — | `updateQueue` body |
| Return window minutes `returnWindowMinutes` | number field (minutes) | optional | — | min 1 | — | — | `updateQueue` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `updateQueue` body |
| Fast pass allocation percent `fastPassAllocationPercent` | stepper or slider | optional | — | min 0; max 100 | — | — | `updateQueue` body |
| Fast pass `fastPass` | group | optional | — | — | — | The lane's Fast Pass block (decided 29 September, VM close-out). Replaces the whole block; null removes it. | `updateQueue` body |
| Entitlement products `fastPass.entitlementProductIds` | multi-picker: choose entitlement products | required | — | — | — | Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need. | `updateQueue` body |
| Loyalty tiers `fastPass.loyaltyTierIds` | multi-picker: choose loyalty tiers | optional | — | — | — | 5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. | `updateQueue` body |
| Promotions `fastPass.promotionIds` | multi-picker: choose promotions | optional | — | — | — | 5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. | `updateQueue` body |
| Accessibility priority `fastPass.accessibilityPriority` | toggle | optional | off | — | — | 5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. | `updateQueue` body |
| Return window minutes `fastPass.returnWindowMinutes` | number field (minutes) | optional | 60 | min 1; max 240 | — | How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan. | `updateQueue` body |
| Max per guest per day `fastPass.maxPerGuestPerDay` | number field | optional | — | min 1 | — | Fast Pass redemptions one guest may make on this lane per day; null is no cap. | `updateQueue` body |
| Allowed access points `fastPass.allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Access points that redeem Fast Pass for this lane; empty is the queue's own. | `updateQueue` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save Fast Pass settings (primary button) | `updateQueue` PATCH `/queues/{queueId}` | inline | Queue | — | — |
| Save fast pass profile (secondary button) | `setFastPassProfile` PUT `/fast-pass-profiles` | AccessFastPassProfile | AccessFastPassProfile | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Data it reads**: `listFastPassAttraction` (onLoad, Fast Pass & Attraction Access Journey); `listQueues` (onLoad, The attraction lanes a Fast Pass is configured on)

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `listFastPassAttraction`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fast pass attraction configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fast pass attraction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fast pass attraction configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 `totalUses` missing on a limited profile. |

#### Permissions

- `listFastPassAttraction` → `SCOPE_VIEW` (read) · staff
- `listQueues` → `QUEUE_VIEW` (read) · staff, guest
- `updateQueue` → `QUEUE_MANAGE` (configure) · staff
- `setFastPassProfile` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Qossai: walk-in, virtual-queue and VIP guests must be distinguished at the ride; VQ guests are never merged into the VIP line (would erode paid value); VQ arrivals need their own handling, e.g. a separate line or a QR scan within the arrival window. *(agreed · MoM 7 Sep 2026, 4.15 Virtual Queue - Three-Tier Guest Model · DI-678)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-221` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-221`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 14: Works in Fast Pass & Attraction Access Journey → Configure the operational experience for limited and unlimited priority-access entitlements. The matrix requires Silver Fast Pass to support three accesses and Gold to support unlimited access with …

#### Acceptance for the design

- [ ] Every input above is drawn (27), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-221?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save Fast Pass settings, Save fast pass profile.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `QUEUE_MANAGE`, `QUEUE_VIEW`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-222` Special Event, Free View & Alternative Admission

**Configure temporary/special admission processes that differ from normal venue access. The matrix requires special-event products capable of capturing attendance without physical admission, N- person attendance entered through a turnstile/tablet/handheld, and Free View days where main gates are open while attraction gates continue validating tickets.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #20680 (APP-SETUP-BO-222) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/special-event-free-view-alternative-admission-bo-222` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| 15 Sep 2026 | select field | — | — | — | — | — | — |
| 08:00–18:00 | select field | — | — | — | — | — | — |

**Form: Save operating calendar entry** (modal, opened by *Save operating calendar entry*; *Save operating calendar entry* calls `setOperatingCalendarEntry`, *Cancel* sends nothing)

**Collects what `setOperatingCalendarEntry` sends before it is called.** Required: `id`, `venueId`, `dayType`, `startsAt`, `endsAt`, `scopePath`. Optional: `name`, `ticketValidationRequired`, `admissionType`, `attractionValidation`, `manualAttendanceRequired`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setOperatingCalendarEntry` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setOperatingCalendarEntry` body |
| Day type `dayType` | select | required | — | Normal operating day · Weekend · Holiday · Seasonal schedule · Private event · Free entry day · Maintenance period · Special event · Ladies only session · School group session · After hours event | — | Kind of calendar entry | `setOperatingCalendarEntry` body |
| Name `name` | text field | optional | — | — | — | — | `setOperatingCalendarEntry` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setOperatingCalendarEntry` body |
| Ends at `endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setOperatingCalendarEntry` body |
| Ticket validation required `ticketValidationRequired` | toggle | optional | on | — | — | False on free-entry days | `setOperatingCalendarEntry` body |
| Admission type `admissionType` | segmented control | optional | — | Free view day · Special event | — | Set on special admission windows only | `setOperatingCalendarEntry` body |
| Attraction validation `attractionValidation` | toggle | optional | — | — | — | Special windows: attraction gates keep validating tickets | `setOperatingCalendarEntry` body |
| Manual attendance required `manualAttendanceRequired` | toggle | optional | — | — | — | Special windows: operator enters attendance count | `setOperatingCalendarEntry` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setOperatingCalendarEntry` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `endsAt` is not after `startsAt`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save operating calendar entry (primary button) | `setOperatingCalendarEntry` PUT `/operating-calendar-entries` | AccessOperatingCalendarEntry | AccessOperatingCalendarEntry | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Data it reads**: `listSpecialEventFree` (onLoad, Special Event, Free View & Alternative Admission)

**Where the user goes next**

- → `BO-214` Guest Journey Command Center: *Returns to the board's landing screen*; calls `listSpecialEventFree`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The special event free configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the special event free untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No special event free configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 `endsAt` is not after `startsAt`. |

#### Permissions

- `listSpecialEventFree` → `SCOPE_VIEW` (read) · staff
- `createAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `setContextTimeEvent` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `setOperatingCalendarEntry` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.51 | Admission entitlement management | Ticketing Catalogue | CONTRACTED | `createAdmissionRules` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-222` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-222`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 16: Works in Special Event, Free View & Alternative Admission → Configure temporary/special admission processes that differ from normal venue access. The matrix requires special-event products capable of capturing attendance without physical admission, N- person …

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-222?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save operating calendar entry.
- [ ] Every transition is wired: `BO-214`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-223` Journey Simulation, Audit & Publication

**Test an entire guest journey—not merely an individual scan—before deploying it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/journey-simulation-audit-publication-bo-223` |

#### Inputs: what the user enters or picks

**Sent by *Run journey simulation*** (`simulateGuestJourney`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Journey profile `journeyProfileId` | text field | required | — | — | — | The access journey (`GuestJourneyCommandCenterView.journeyProfileId`) | `simulateGuestJourney` body |
| Scenario `scenario` | radio group | required | — | Standard day · Free view day · Special event · Peak day | — | — | `simulateGuestJourney` body |
| Simulated date `simulatedDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Date the calendar rules are evaluated for; empty is today | `simulateGuestJourney` body |
| Entitlements `entitlementIds` | list of values (chips) | optional | — | — | — | Entitlements the simulated guest holds | `simulateGuestJourney` body |
| Steps `steps` | repeatable rows | optional | — | at least 1; at most 50 | — | The scans, in order | `simulateGuestJourney` body |
| Access point `steps[].accessPointId` | text field | required | — | — | — | — | `simulateGuestJourney` body |
| Direction `steps[].direction` | segmented control | optional | Entry | Entry · Exit | — | — | `simulateGuestJourney` body |
| At `steps[].at` | time picker | optional | — | — | HH:mm, 24-hour | Local time HH:MM | `simulateGuestJourney` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every journey simulation audit** (data table, from `listJourneys`)

| Shows | Format | Notes |
|---|---|---|
| Impossible journey sequences | text | not in the schema: `impossible journey sequences` |
| Missing gates | text | not in the schema: `missing gates` |
| Incompatible hardware | text | not in the schema: `incompatible hardware` |
| Missing companion relationship | text | not in the schema: `missing companion relationship` |
| Conflicting quantities | text | not in the schema: `conflicting quantities` |
| Duplicate attendance | text | not in the schema: `duplicate attendance` |

**The selected journey simulation audit** (detail panel): The pack groups this record's detail under its own headings: “Purchased”, “Arrive”, “Simulation Trace”, “Attendance”, “Remaining”, “Journey Audit”.

| Shows | Format | Notes |
|---|---|---|
| Impossible journey sequences | text | not in the schema: `impossible journey sequences` |
| Missing gates | text | not in the schema: `missing gates` |
| Incompatible hardware | text | not in the schema: `incompatible hardware` |
| Missing companion relationship | text | not in the schema: `missing companion relationship` |
| Conflicting quantities | text | not in the schema: `conflicting quantities` |
| Duplicate attendance | text | not in the schema: `duplicate attendance` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Free View Day (primary button) | navigation or local | — | — | — | — |
| Run journey simulation (primary button) | `simulateGuestJourney` POST `/guest-journey/simulate` | GuestJourneySimulationInput | GuestJourneySimulationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Data it reads**: `listJourneys` (onLoad, Automated journeys)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The journey simulation audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the journey simulation audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No journey simulation audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the journey simulation audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listJourneys` → `MARKETING_VIEW` (read) · staff
- `simulateGuestJourney` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.3.1 | Visual Journey Builder | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.6 | Abandoned Cart Recovery Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.7 | Membership Lifecycle Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.8 | Loyalty Lifecycle Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.9 | Wallet Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.10 | Birthday & Anniversary Campaigns | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.14 | Cross-Sell & Upsell Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.21 | Automation Analytics Dashboard | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.22 | Automation Audit Trail | Marketing & CRM | CONTRACTED | data `Journey` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-223` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS25 Access Control Board 8.dc.html#bo-223`
- Workshop pack: Access Control Module_Reference.pdf board 8
- Flow F118 *Access Control board 8: Guest Journey Command Center*, step 18: Works in Journey Simulation, Audit & Publication → Test an entire guest journey—not merely an individual scan—before deploying it.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-223?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Free View Day, Run journey simulation.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `MARKETING_VIEW`.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createAdmissionRules": {"method":"POST","path":"/admission-rules","contract":"access","summary":"Create an admission profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AdmissionRules","responds":"AdmissionRules"},
"listAdmissionRules": {"method":"GET","path":"/admission-rules","contract":"access","summary":"List admission profiles","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEntryTemporaryExit": {"method":"GET","path":"/entry-temporary-exit","contract":"access","summary":"Re-entry & Temporary Exit Journey","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReEntryTemporaryExitJourneyView"},
"listFamilyChildPod": {"method":"GET","path":"/family-child-pod","contract":"access","summary":"Family, Child, POD & Companion Journey","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FamilyChildPodCompanionJourneyView"},
"listFastPassAttraction": {"method":"GET","path":"/fast-pass-attraction","contract":"access","summary":"Fast Pass & Attraction Access Journey","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FastPassAttractionAccessJourneyView"},
"listGroupAttendancePartial": {"method":"GET","path":"/group-attendance-partial","contract":"access","summary":"Group Attendance & Partial Entry Manager","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGroupLeaderFast": {"method":"GET","path":"/group-leader-fast","contract":"access","summary":"Group Leader & Fast B2B Validation","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGuestJourney": {"method":"GET","path":"/guest-journey","contract":"access","summary":"Guest Journey Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listJourneys": {"method":"GET","path":"/journeys","contract":"marketing-crm","summary":"Automated journeys","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMultiParkCrossover": {"method":"GET","path":"/multi-park-crossover","contract":"access","summary":"Multi-Park & Crossover Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MultiParkCrossoverRulesView"},
"listMultiParkCrossover2": {"method":"GET","path":"/multi-park-crossover-2","contract":"access","summary":"Multi-Park & Crossover Journey Orchestrator","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listQueues": {"method":"GET","path":"/queues","contract":"queue","summary":"List queues","permission":"QUEUE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"openOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSpecialEventFree": {"method":"GET","path":"/special-event-free","contract":"access","summary":"Special Event, Free View & Alternative Admission","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SpecialEventFreeViewAlternativeAdmissionView"},
"setContextTimeEvent": {"method":"PUT","path":"/context-time-event","contract":"access","summary":"Context, Time, Event & Capacity Policy Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ContextTimeEventCapacityPolicyBuilderInput","responds":"ContextTimeEventCapacityPolicyBuilderView"},
"setFastPassProfile": {"method":"PUT","path":"/fast-pass-profiles","contract":"access","summary":"Create or replace a Fast Pass profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessFastPassProfile","responds":"AccessFastPassProfile"},
"setGroupAdmissionProfile": {"method":"PUT","path":"/group-admission-profile","contract":"access","summary":"Group & B2B Admission Profile Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GroupB2bAdmissionProfileBuilderInput","responds":"GroupB2bAdmissionProfileBuilderView"},
"setGuestCompanionEligibility": {"method":"PUT","path":"/guest-companion-eligibility","contract":"access","summary":"Save a companion eligibility rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestCompanionEligibilityRulesInput","responds":"GuestCompanionEligibilityRulesView"},
"setJourneyProfile": {"method":"PUT","path":"/journey-profiles","contract":"access","summary":"Create or replace a guest journey profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessJourneyProfile","responds":"AccessJourneyProfile"},
"setOperatingCalendarEntry": {"method":"PUT","path":"/operating-calendar-entries","contract":"access","summary":"Create or replace an operating calendar entry","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessOperatingCalendarEntry","responds":"AccessOperatingCalendarEntry"},
"simulateGuestJourney": {"method":"POST","path":"/guest-journey/simulate","contract":"access","summary":"Simulate an access journey","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestJourneySimulationInput","responds":"GuestJourneySimulationView"},
"updateAdmissionRules": {"method":"PUT","path":"/admission-rules/{profileId}","contract":"access","summary":"Update an admission profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AdmissionRules","responds":"AdmissionRules"},
"updateQueue": {"method":"PATCH","path":"/queues/{queueId}","contract":"queue","summary":"Amend queue configuration","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Queue"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessFastPassProfile": {"type":"object","x-ticvai-persistence":"access.fast_pass_profile","description":"One Fast Pass profile (e.g. Silver, Gold) - total uses or unlimited, uses consumed per validation, the one-access-per-ride restriction and the eligible attraction categories (declared 29 September, data-model close-out DM1).","required":["id","scopePath","name","unlimited"],"properties":{"id":{"type":"string","format":"uuid","description":"The profileId the list shows"},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"name":{"type":"string","maxLength":200},"unlimited":{"type":"boolean","default":false},"totalUses":{"type":"integer","minimum":1,"nullable":true,"description":"Null when unlimited"},"consumptionPerValidation":{"type":"integer","minimum":1,"default":1},"onePerRide":{"type":"boolean","default":false},"eligibleAttractionCategories":{"type":"array","items":{"type":"string"},"description":"The list's eligibleType, e.g. rollerCoaster, dropTower, waterRide, adventureRide"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessJourneyProfile": {"type":"object","x-ticvai-persistence":"access.journey_profile","description":"One guest access journey profile (e.g. School Group Entry) - type, venue, credential used, status and the ordered steps a simulation walks (declared 29 September, data-model close-out DM1).","required":["id","scopePath","name","status"],"properties":{"id":{"type":"string","format":"uuid","description":"The journeyProfileId"},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Null is every park of the tenant"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"name":{"type":"string","maxLength":200},"journeyType":{"type":"string","maxLength":60,"nullable":true,"description":"e.g. B2B group, family"},"credentialType":{"type":"string","maxLength":100,"nullable":true,"description":"e.g. group QR, mixed"},"status":{"type":"string","enum":["active","inactive"],"default":"active"},"steps":{"allOf":[{"$ref":"#/components/schemas/AccessJsonList"}],"description":"Ordered journey steps, each an accessPointId with a direction (entry or exit) and an optional local time HH:MM, as GuestJourneySimulationInput.steps"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessJsonList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the row that holds it.** A short list of structured entries read with its row and never queried on its own (thresholds, per-language messages, field mappings, steps), so a child table would add a join for nothing. The property that uses it says what an entry holds (declared 29 September, data-model close-out DM1).","items":{"type":"object"}},
"AccessOperatingCalendarEntry": {"type":"object","x-ticvai-persistence":"access.operating_calendar_entry","description":"One dated entry in a venue operating calendar (normal day, holiday, private event, free-entry day, special event and so on), with whether tickets must be validated. Merges access.special_admission_window, whose free-view and special-event windows are entries carrying an admission type (declared 29 September, data-model close-out DM1)","required":["id","venueId","dayType","startsAt","endsAt","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"dayType":{"type":"string","enum":["normalOperatingDay","weekend","holiday","seasonalSchedule","privateEvent","freeEntryDay","maintenancePeriod","specialEvent","ladiesOnlySession","schoolGroupSession","afterHoursEvent"],"description":"Kind of calendar entry"},"name":{"type":"string","nullable":true},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"ticketValidationRequired":{"type":"boolean","default":true,"description":"False on free-entry days"},"admissionType":{"type":"string","enum":["freeViewDay","specialEvent"],"nullable":true,"description":"Set on special admission windows only"},"attractionValidation":{"type":"boolean","nullable":true,"description":"Special windows: attraction gates keep validating tickets"},"manualAttendanceRequired":{"type":"boolean","nullable":true,"description":"Special windows: operator enters attendance count"},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AdmissionRule": {"type":"object","x-ticvai-persistence":"none — embedded as the jsonb column condition_rule of access.dynamic_policy, and in each access.dynamic_policy_version definition","description":"**One rule format that runs on both sides** (ADR-0068, accepted 1 October). A guest-admission condition was free text (`conditionExpression`, \"AND, OR, NOT, IN and BETWEEN\"), which a .NET server and a TypeScript gate cannot be relied on to read the same way. This is a closed JSON format instead: every condition is drawn from the `policyType` and `contextType` enums already on `AccessDynamicPolicy`, with a fixed set of comparators, so `validateAccess` online and the gate offline evaluate the same active version to the same answer. **One evaluator in .NET and one in TypeScript, proven equal by a shared set of test vectors in CI** (ACC-RULE-EVAL, B1 with the scanner).\n\n`match` combines `conditions` and `groups` (`all` is AND, `any` is OR); each group is its own `all` or `any` over its conditions and counts as one condition of the rule; `negate` is NOT. **Two levels and no more**: every rule the Access Control pack shows fits in them, and a deeper tree is refused `400` rather than approximated. A rule that needs more than the closed set extends the set; free text does not come back (ADR-0068, Revisit).","required":["match","conditions"],"properties":{"formatVersion":{"type":"integer","enum":[1],"default":1,"description":"The rule format's version. An evaluator refuses a version it does not know rather than guess."},"match":{"type":"string","enum":["all","any"]},"conditions":{"type":"array","minItems":1,"maxItems":50,"items":{"$ref":"#/components/schemas/AdmissionCondition"}},"groups":{"type":"array","maxItems":10,"items":{"type":"object","required":["match","conditions"],"properties":{"match":{"type":"string","enum":["all","any"]},"negate":{"type":"boolean","default":false},"conditions":{"type":"array","minItems":1,"maxItems":50,"items":{"$ref":"#/components/schemas/AdmissionCondition"}}}}}}},
"AdmissionRules": {"x-ticvai-persistence":"access.admission_rules","type":"object","required":["id","code","name","openMinutesBefore","closeMinutesAfter"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Server-assigned.** Ignored in a `createAdmissionRules` or `updateAdmissionRules` body; on update the profile is the one the path names.\n"},"code":{"type":"string","maxLength":64},"perProductRules":{"allOf":[{"$ref":"#/components/schemas/PerProductRuleList"}],"description":"BL-059. **Transaction rules were per profile and a ticket type could not state its own.** An annual pass allowing one entry per day and a single ticket allowing one entry ever are different rules, and forcing a profile per product multiplies profiles instead.\n"},"name":{"type":"string","maxLength":200},"openMinutesBefore":{"type":"integer","description":"How long before a performance validation opens."},"closeMinutesAfter":{"type":"integer"},"maxDurationMinutes":{"type":"integer","nullable":true},"requiresExitBeforeReentry":{"type":"boolean","default":false},"maxReentries":{"type":"integer","nullable":true},"entryLimit":{"type":"object","description":"**How many times the credential may enter** (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). Absent means `unlimited`.","required":["mode"],"properties":{"mode":{"type":"string","enum":["unlimited","once","nTimes","nPerDay","nPerPeriod"],"default":"unlimited"},"count":{"type":"integer","minimum":1,"description":"N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it)"},"periodDays":{"type":"integer","minimum":1,"description":"The period for nPerPeriod"}}},"exitScan":{"type":"string","enum":["required","optional","none"],"default":"optional","description":"(decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. `optional`: exits run in free rotation and headcount is inferred. `none`: the exit has no reader."},"maxExits":{"type":"integer","minimum":0,"nullable":true,"description":"Null is unlimited (decided 29 September, VM close-out)"},"reEntryWindowMinutes":{"type":"integer","minimum":1,"nullable":true,"description":"Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out)"},"sameDayOnly":{"type":"boolean","default":true,"description":"Re-entry only on the day of the exit (decided 29 September, VM close-out)"},"designatedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out)"},"validity":{"type":"object","description":"**When the credential is valid** (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). The admission window above still applies inside it.","required":["anchor"],"properties":{"anchor":{"type":"string","enum":["fixedRange","afterSale","afterActivation","afterFirstUse"],"description":"fixedRange uses from and to; the others count days from the event"},"days":{"type":"integer","minimum":1,"description":"N days after the anchor; required unless the anchor is fixedRange"},"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date","description":"Inclusive. Must not be before from (`422`)"},"endOf":{"type":"string","enum":["day","week","month","year"],"nullable":true,"description":"Validity runs to the end of the day, week, month or year the relative period ends in"},"daysOfWeek":{"type":"array","items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"description":"Empty is every day"},"dayTypes":{"type":"array","items":{"type":"string","enum":["peakDates","offPeakDates","holidays","seasons","eventDates"]},"description":"Calendar day types on which access is allowed; empty is every day type"},"blackoutDates":{"type":"array","items":{"type":"string","format":"date"},"description":"Dates on which access is refused whatever else allows it"}}},"crossover":{"type":"object","nullable":true,"description":"**Crossover between parks** (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. Null means the profile admits to one park only.","required":["allowedParkOrgUnitIds"],"properties":{"allowedParkOrgUnitIds":{"type":"array","minItems":2,"items":{"type":"string","format":"uuid"}},"parkOrder":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Required order of parks, if any; empty is any order"},"sameDayOnly":{"type":"boolean","default":true},"differentDayAccess":{"type":"boolean","default":false},"dayPattern":{"type":"string","enum":["consecutiveFromFirstScan","flexibleWithinValidity"],"default":"flexibleWithinValidity"},"maxParkEntries":{"type":"integer","minimum":1,"nullable":true,"description":"Null is unlimited"},"crossoverQuantity":{"type":"integer","minimum":1,"nullable":true,"description":"How many crossovers; null is unlimited"},"crossoverAfterTime":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Earliest venue-local time HH:MM a crossover is allowed"},"prerequisiteParkOrgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The park that must be entered first"},"reEntryAfterCrossover":{"type":"boolean","default":false}}},"allowedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Empty means any access point in the venue."},"reEntryVerification":{"type":"string","enum":["credentialOnly","credentialUvStamp","credentialFace","credentialOperator","custom"],"default":"credentialOnly","description":"What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1)."},"ruleConditions":{"type":"object","nullable":true,"description":"The visual rule builder body `setVisualAccessRule` writes: `appliesTo` (products or credential types), `conditions`, `logic` (AND / OR / NOT over the conditions), `decision` (allow, deny, referToOperator, overrideEligible) and `consequences`. **One `jsonb` column on the rule row**, read with the rule and never queried on its own; the locations stay in `access.entry_rule_point` (added 29 September, data-model close-out DM1)."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ContextTimeEventCapacityPolicyBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Context, Time, Event & Capacity Policy Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"result":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"]},"conditionRule":{"$ref":"#/components/schemas/AdmissionRule","description":"The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`). For example: Zone Occupancy >= 90% AND Day = Friday AND Time BETWEEN 18:00 AND 23:59."},"name":{"type":"string"},"policyId":{"type":"string"},"contextType":{"type":"string","enum":["date","day","time","season","event","performance","specialEvent","holiday","operatingCalendar","occupancy","attractionStatus"],"description":"Kind of venue condition the policy reacts to"},"monitorThresholdPercent":{"type":"integer","description":"Occupancy percent at which the band becomes Monitor"},"restrictThresholdPercent":{"type":"integer","description":"Occupancy percent at which the band becomes Restrict"},"status":{"type":"string","enum":["active","inactive"],"default":"active","description":"`inactive` switches the policy off at once; `active` on a new or inactive policy submits it for approval (`pendingApproval`) (decided 29 September, writers pass)"},"validFrom":{"type":"string","format":"date-time","nullable":true,"description":"Start of validity; null for at once (decided 29 September, writers pass)"},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"End of validity: after it a timer moves the policy to `expired` (decided 29 September, writers pass)"}},"required":["policyId","name","contextType","conditionRule","result"]},
"ContextTimeEventCapacityPolicyBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Context, Time, Event & Capacity Policy Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"result":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"]},"conditionRule":{"$ref":"#/components/schemas/AdmissionRule","description":"The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`). For example: Zone Occupancy >= 90% AND Day = Friday AND Time BETWEEN 18:00 AND 23:59."},"name":{"type":"string"},"policyId":{"type":"string"},"contextType":{"type":"string","enum":["date","day","time","season","event","performance","specialEvent","holiday","operatingCalendar","occupancy","attractionStatus"],"description":"Kind of venue condition the policy reacts to"},"monitorThresholdPercent":{"type":"integer","description":"Occupancy percent at which the band becomes Monitor"},"restrictThresholdPercent":{"type":"integer","description":"Occupancy percent at which the band becomes Restrict"}},"required":["policyId","name","contextType","conditionRule","result"]},
"CreateQueueRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","capacityPerCycle","cycleMinutes"],"properties":{"code":{"type":"string","maxLength":64},"name":{"$ref":"#/components/schemas/LocalisedText"},"venueId":{"type":"string","format":"uuid"},"attractionProductId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["standby","singleRider","fastPass","virtual","accessible","groupOnly","staffOnly"],"default":"standby","description":"5.6.x. **A ride has several queues and the model had one.** A single-rider line and a standby line at the same attraction draw from one capacity and fill at different rates, and modelling them as one queue makes both wait estimates wrong.\n**`accessible` is not a courtesy lane.** It has its own capacity because a guest who cannot stand in a switchback needs a place to wait, not priority.\n"},"operatingWindows":{"type":"array","description":"**When the queue runs, which is not when the venue is open.** A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen.\nStored one row per window in `queue.queue_operating_window` (see `Queue`), not as a column on the queue.\n","items":{"type":"object","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, when the queue starts running."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, when the queue stops running."},"lastEntryMinutesBefore":{"type":"integer","default":0,"description":"**When the queue stops accepting, which is before it stops running.** A guest joining two minutes before close waits twenty and is turned away at the front.\n"}}}},"parentQueueId":{"type":"string","format":"uuid","nullable":true,"description":"Where several queues share one capacity. **The standby and single-rider lines at one ride draw from the same cycles**, and a parent is how that is expressed without either queue owning the other.\n"},"loadBalanceWithQueueIds":{"type":"array","description":"BL-137. **Two rides with the same theme and different waits**, and nothing directed a guest to the shorter one. Load balancing is an offer, not an assignment — **a guest sent to a ride they did not choose is a guest who feels managed.**\n","items":{"type":"string","format":"uuid"}},"inQueueOfferEnabled":{"type":"boolean","default":false,"description":"**A guest with twenty minutes to wait is a guest with twenty minutes to buy something.** Offers surface in the wait screen and are the only reason a virtual queue earns its infrastructure.\n"},"notifyBeforeCallMinutes":{"type":"integer","default":5,"description":"BL-017, 19.2.61. **A guest was not told their turn was approaching**, which makes a virtual queue worse than a physical one — at least a line is visible.\n"},"capacityPerCycle":{"type":"integer","minimum":1},"cycleMinutes":{"type":"number","minimum":0},"maxPartySize":{"type":"integer","default":6},"returnWindowMinutes":{"type":"integer","default":15,"description":"How long a called party has to arrive before the entry expires."},"heightRequirementCm":{"type":"integer","nullable":true},"fastPassAllocationPercent":{"type":"number","minimum":0,"maximum":100,"default":0,"description":"Share of each cycle reserved for Fast Pass holders."},"zone":{"type":"string","nullable":true},"fastPass":{"allOf":[{"$ref":"#/components/schemas/QueueFastPass"}],"nullable":true,"description":"The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass.\n"}}},
"FamilyChildPodCompanionJourneyView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Family, Child, POD & Companion Journey displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string","description":"Companion rule identifier"},"relationshipType":{"type":"string","enum":["parentChild","guardianMinor","podCompanion","primaryGuestNanny","groupLeaderGroupMember","other"],"description":"Linked-person relationship this rule governs"},"verificationMethod":{"type":"string","enum":["pairedAdultCredential","assignedAdultBiometric"],"description":"How the accompanying adult is verified"},"assignedAdultRequiredForExit":{"type":"boolean","description":"The assigned adult must be present for the dependent to exit"}},"required":["ruleId"]},
"FastPassAttractionAccessJourneyView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Fast Pass & Attraction Access Journey displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"profileId":{"type":"string","description":"Fast Pass profile identifier"},"totalUses":{"type":"integer","description":"Total Uses (the pack shows 3)"},"eligibleType":{"type":"array","items":{"type":"string"},"description":"Eligible attraction categories: rollerCoaster, dropTower, waterRide, adventureRide"},"name":{"type":"string","description":"Profile name, e.g. Silver, Gold"},"unlimited":{"type":"boolean","description":"Unlimited uses"},"consumptionPerValidation":{"type":"integer","description":"Uses consumed per validation"},"onePerRide":{"type":"boolean","description":"Restrict to one access per ride"}},"required":["profileId"]},
"GroupAttendancePartialEntryManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Group Attendance & Partial Entry Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"waveId":{"type":"string","description":"Admission wave identifier"},"remaining":{"type":"integer","description":"Guests still to arrive after this wave"},"totalEntered":{"type":"integer","description":"Total Entered (the pack shows 48)"},"group":{"type":"string","description":"Group"},"leader":{"type":"string","description":"Leader"},"gate":{"type":"string","description":"Gate"},"operator":{"type":"string","description":"Operator"},"quantity":{"type":"integer","description":"Quantity"},"time":{"type":"string","format":"date-time","description":"Time"},"device":{"type":"string","description":"Device"},"purchased":{"type":"integer","description":"Guests purchased on the group booking"}},"required":["waveId"]},
"GroupB2bAdmissionProfileBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Group & B2B Admission Profile Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"name":{"type":"string","description":"Profile name"},"venueId":{"type":"string","description":"Venue"},"profileId":{"type":"string","description":"The rule row's key (access.group_admission_rule.id); absent creates one (decided 29 September, writers pass)","format":"uuid"},"groupSegments":{"type":"array","items":{"type":"string","enum":["schools","tourOperators","corporateGroups","resellers","travelGroups","camps","families","events"]},"description":"Group segments this profile applies to"},"credentialMode":{"type":"string","enum":["singleGroupQr","groupBarcode","groupRfid","groupLeaderCredential","individualCredentials","hybrid"],"description":"How the group presents its credentials"},"admissionMethod":{"type":"string","enum":["entireGroup","partialGroup","multipleWaves","individualScan","leaderQuantity","manifestBased"],"description":"How the group is admitted at the gate"}},"required":["profileId","venueId","name"]},
"GroupB2bAdmissionProfileBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Group & B2B Admission Profile Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string","description":"Profile name"},"venueId":{"type":"string","description":"Venue"},"profileId":{"type":"string","description":"Group admission profile identifier"},"groupSegments":{"type":"array","items":{"type":"string","enum":["schools","tourOperators","corporateGroups","resellers","travelGroups","camps","families","events"]},"description":"Group segments this profile applies to"},"credentialMode":{"type":"string","enum":["singleGroupQr","groupBarcode","groupRfid","groupLeaderCredential","individualCredentials","hybrid"],"description":"How the group presents its credentials"},"admissionMethod":{"type":"string","enum":["entireGroup","partialGroup","multipleWaves","individualScan","leaderQuantity","manifestBased"],"description":"How the group is admitted at the gate"}},"required":["profileId","venueId","name"]},
"GroupLeaderFastB2bValidationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Group Leader & Fast B2B Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"groupBookingId":{"type":"string","description":"Group booking"},"attendance":{"type":"integer","description":"Attendance (the pack shows +112)"},"remaining":{"type":"integer","description":"Guests not yet admitted"},"payment":{"type":"boolean","description":"Payment check passed"},"booking":{"type":"boolean","description":"Booking check passed"},"groupProduct":{"type":"boolean","description":"Group product check passed"},"accessRules":{"type":"boolean","description":"Access rules check passed"},"manifest":{"type":"boolean","description":"Manifest check passed"},"bookedGuests":{"type":"integer","description":"Guests booked"},"visitDateValid":{"type":"boolean","description":"Visit date check passed"}},"required":["groupBookingId"]},
"GuestCompanionEligibilityRulesInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Guest, Companion & Eligibility Rules submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["venueId","name","guestCategory","requiredCompanionCategory","verifyAt"],"properties":{"ruleId":{"type":"string","format":"uuid","description":"Absent creates a rule"},"venueId":{"type":"string"},"name":{"type":"string","maxLength":200},"guestCategory":{"type":"string","enum":["adult","child","junior","senior","pod","podCompanion","nanny","vip","member","staff","accreditation","customerSegment"]},"requiredCompanionCategory":{"type":"string","enum":["adult","podCompanion","nanny","guardian"],"description":"Category of the companion who must be present"},"companionVerification":{"type":"string","enum":["linkedTicket","companionBiometric"],"default":"linkedTicket"},"verifyAt":{"type":"array","items":{"type":"string","enum":["admission","exit","attraction"]},"minItems":1,"description":"Where the companion is checked"},"attractionIds":{"type":"array","items":{"type":"string"},"description":"Where verifyAt includes attraction"}}},
"GuestCompanionEligibilityRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Guest, Companion & Eligibility Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"guestCategory":{"type":"string","enum":["adult","child","junior","senior","pod","podCompanion","nanny","vip","member","staff","accreditation","customerSegment"]},"name":{"type":"string"},"requiredCompanionCategory":{"type":"string","description":"Category of the qualifying companion, e.g. adult"},"companionVerification":{"type":"string","enum":["linkedTicket","companionBiometric"]},"verifyAt":{"type":"array","items":{"type":"string","enum":["admission","exit","attraction"]},"description":"Where the companion is checked (decided 29 September, VM close-out)"},"attractionIds":{"type":"array","items":{"type":"string"}}},"required":["ruleId","guestCategory"]},
"GuestJourneyCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Guest Journey Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"journeyProfileId":{"type":"string","description":"Journey profile identifier"},"journeyName":{"type":"string","description":"Journey, e.g. School Group Entry"},"journeyType":{"type":"string","description":"Journey type, e.g. B2B group, family"},"venueId":{"type":"string","description":"Venue or all parks"},"credentialType":{"type":"string","description":"Credential used, e.g. group QR, mixed"},"status":{"type":"string","enum":["active","inactive"],"description":"Status"}},"required":["journeyProfileId"]},
"GuestJourneyCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"activeJourneyProfiles":{"type":"integer","description":"Active Journey Profiles"},"groupArrivalsToday":{"type":"integer","description":"Group Arrivals Today"},"guestsViaGroupAdmission":{"type":"integer","description":"Guests via Group Admission"},"familyJourneys":{"type":"integer","description":"Family Journeys"},"reEntryGuests":{"type":"integer","description":"Re-entry Guests"},"crossoversToday":{"type":"integer","description":"Crossovers Today"},"fastPassValidations":{"type":"integer","description":"Fast Pass Validations"},"specialEventAdmissions":{"type":"integer","description":"Special Event Admissions"},"vipAdmissions":{"type":"integer","description":"VIP Admissions"},"journeyExceptions":{"type":"integer","description":"Journey Exceptions"}}},
"GuestJourneySimulationInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"A journey to simulate against the access rules, before it is published (decided 29 September, VM close-out).","required":["journeyProfileId","scenario"],"properties":{"journeyProfileId":{"type":"string","description":"The access journey (`GuestJourneyCommandCenterView.journeyProfileId`)"},"scenario":{"type":"string","enum":["standardDay","freeViewDay","specialEvent","peakDay"]},"simulatedDate":{"type":"string","format":"date","description":"Date the calendar rules are evaluated for; empty is today"},"entitlementIds":{"type":"array","items":{"type":"string"},"description":"Entitlements the simulated guest holds"},"steps":{"type":"array","items":{"type":"object","required":["accessPointId"],"properties":{"accessPointId":{"type":"string"},"direction":{"type":"string","enum":["entry","exit"],"default":"entry"},"at":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time HH:MM"}}},"minItems":1,"maxItems":50,"description":"The scans, in order"}}},
"GuestJourneySimulationView": {"type":"object","x-ticvai-persistence":"none — computed; nothing is admitted or consumed (decided 29 September, VM close-out)","description":"What each step of a simulated journey would decide (decided 29 September, VM close-out).","required":["journeyProfileId","scenario","steps"],"properties":{"journeyProfileId":{"type":"string"},"scenario":{"type":"string","enum":["standardDay","freeViewDay","specialEvent","peakDay"]},"passed":{"type":"boolean","description":"Every step produced the expected decision"},"steps":{"type":"array","items":{"type":"object","properties":{"accessPointId":{"type":"string"},"decision":{"type":"string","enum":["allowed","denied","review"]},"reasonCode":{"type":"string"},"entitlementConsumed":{"type":"string","nullable":true},"decisionTrace":{"type":"array","items":{"type":"string"}}}}}}},
"Journey": {"type":"object","x-ticvai-persistence":"marketing.journey + marketing.journey_step","description":"22.3.1b to 22.3.10b, CF-137. **A journey is a sequence with branches; a `MessageTrigger` is one step of it.** The trigger already handles *\"send this when that happens\"* — a journey is what you need when the next message depends on what the guest did about the last one.\nFive of the ten requirements are named lifecycles — abandoned cart, membership, loyalty, wallet, birthday. **They are not five features.** Each is a journey with a different entry event and a different set of steps, which is why this is one entity and a template library rather than five contracts.\n**Consent is checked at every send, not at entry.** A guest who opts out mid-journey stops receiving, and the journey does not need to know — the same rule `MessageTrigger` follows and the one PDPL Article 17(1) makes unconditional.\n","required":["id","name","entryEvent","status","steps"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"name":{"type":"string"},"templateKind":{"type":"string","nullable":true,"enum":["abandonedCart","membershipLifecycle","loyaltyLifecycle","walletLifecycle","birthday","onboarding","winBack","custom"],"description":"Which named lifecycle this implements. **Set for reporting and for the library**, not for behaviour — the steps decide what happens.\n"},"entryEvent":{"type":"string","description":"22.3.2b. From the event catalogue, so a journey cannot enter on something nothing publishes.\n"},"entryConditions":{"type":"object","nullable":true,"description":"Narrows entry — a segment, a tier, a venue. **Evaluated once at entry**, unlike step conditions.\n"},"steps":{"type":"array","description":"22.3.1b. What the builder produces. **The visual builder is a frontend over this** — the contract holds the graph and the canvas is a rendering of it.\n","items":{"$ref":"#/components/schemas/JourneyStep"}},"status":{"readOnly":true,"type":"string","enum":["draft","active","paused","archived"]},"maxDurationDays":{"type":"integer","default":30,"description":"**A journey with no end is a guest who never leaves it.** After this, entrants exit wherever they are.\n"},"reentryPolicy":{"type":"string","enum":["never","afterCompletion","always"],"default":"afterCompletion","description":"22.3.6b. **Abandoned cart is the case that needs this.** A guest who abandons three carts in an hour should not get three recovery sequences, and `never` is wrong too — they may genuinely abandon one next month.\n"},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"JourneyStep": {"type":"object","description":"One node. **A step either sends, waits, or branches** — three kinds rather than a general graph, because a marketing user drawing an arbitrary graph draws a loop.\n","required":["id","kind"],"properties":{"id":{"type":"string"},"kind":{"type":"string","x-ticvai-column":"type","enum":["send","wait","branch","exit","goal"]},"templateId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-column":"message_template_id","description":"For `send`. Channel is resolved from the guest's preference at the moment of sending."},"sendTimeMode":{"type":"string","enum":["fixed","optimised"],"default":"fixed","description":"For `send` (29 September, build pass, group G2; 22.3.19). `optimised` delays the send, after the step is reached, to the recipient's suggested hour from `ai.requestSuggestion` (kind `sendTime`) within the next 24 hours and inside `waitUntil`; no suggestion or AI off sends at once, as `fixed`."},"channelMode":{"type":"string","enum":["preference","optimised"],"default":"preference","description":"For `send`. `optimised` tries first the consented channel the send-time suggestion names, then `channelPreference` in order (22.9.16)."},"channelPreference":{"type":"array","nullable":true,"description":"22.3.3b. Ordered fallback — email, then SMS, then push. **A guest with no email address does not get an email step**, and the step does not fail, it moves down the list.\n","items":{"type":"string","enum":["email","sms","whatsapp","push","inApp"]}},"waitMinutes":{"type":"integer","nullable":true},"waitUntil":{"type":"object","nullable":true,"description":"22.3.5b. **Business hours, time zone and blackout windows** — a wallet low-balance alert at 3am is a complaint, and the venue's quiet hours are venue configuration rather than a property of this step.\n","properties":{"businessHoursOnly":{"type":"boolean","default":false},"timezone":{"type":"string","nullable":true},"respectQuietHours":{"type":"boolean","default":true},"notBefore":{"type":"string","nullable":true}}},"condition":{"type":"object","nullable":true,"description":"22.3.4b. IF/THEN over guest profile, behaviour and prior steps. **The most common condition is whether the previous message worked** — a recovery sequence must stop when the guest buys.\n","properties":{"field":{"type":"string"},"operator":{"type":"string","enum":["eq","neq","gt","lt","contains","exists","notExists"]},"value":{"type":"string","nullable":true}}},"onTrue":{"type":"string","nullable":true,"description":"Next step id."},"onFalse":{"type":"string","nullable":true},"next":{"type":"string","nullable":true,"x-ticvai-column":"next_journey_step_id"},"goalEvent":{"type":"string","nullable":true,"description":"For `goal`. **The event that means this journey worked and the guest should leave it** — a purchase for abandoned cart, a renewal for membership. **Reaching a goal exits immediately**, which is what stops a recovered cart from being chased.\n"}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MultiParkCrossoverJourneyOrchestratorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Multi-Park & Crossover Journey Orchestrator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"eventId":{"type":"string","description":"Journey event identifier"},"eventType":{"type":"string","enum":["normalEntry","reEntry","crossover"],"description":"Kind of admission, tracked separately"},"credentialId":{"type":"string","description":"Credential"},"fromParkId":{"type":"string","description":"Park the guest left"},"toParkId":{"type":"string","description":"Park entered"},"occurredAt":{"type":"string","format":"date-time","description":"When it happened"}},"required":["eventId"]},
"MultiParkCrossoverRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Multi-Park & Crossover Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"allowedParks":{"type":"array","items":{"type":"string"},"description":"allowed parks"},"parkOrder":{"type":"array","items":{"type":"string"},"description":"Required park order, if any"},"sameDayCrossover":{"type":"boolean","description":"same-day crossover"},"differentDayAccess":{"type":"boolean","description":"different-day access"},"numberOfParkEntries":{"type":"integer","description":"number of park entries"},"crossoverQuantity":{"type":"integer","description":"crossover quantity"},"crossoverTime":{"type":"string","description":"Earliest local time HH:MM a crossover is allowed"},"prerequisitePark":{"type":"string","description":"prerequisite park"},"reEntryAfterCrossover":{"type":"boolean","description":"re-entry after crossover"},"name":{"type":"string"},"dayPattern":{"type":"string","enum":["consecutiveFromFirstScan","flexibleWithinValidity"]}},"required":["ruleId","allowedParks"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PerProductRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the profile row** (`access.admission_rules.per_product_rules`). The rules are read with the profile and a rule is never queried on its own, so a child table would add a join for nothing.\n","items":{"type":"object","properties":{"productId":{"type":"string","format":"uuid"},"entriesPerDay":{"type":"integer","nullable":true},"minimumGapMinutes":{"type":"integer","nullable":true,"description":"**Anti-passback in minutes rather than a boolean.** A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back over a fence.\n"},"allowedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"biometricPolicy":{"allOf":[{"$ref":"#/components/schemas/BiometricPolicy"}],"description":"BL-105, 3.2.9. **The biometric check is a property of the product, not of the venue** — memberships checked, day tickets not. It sits here rather than on the profile because `perProductRules` is already where a ticket type states its own terms, and a profile per product would multiply profiles to carry one flag.\n**Absent means `disabled`**, and `disabled` is the answer for every product until somebody chooses otherwise. **Inert while `VenueSettings.biometrics.isEnabled` is false**, so a rules profile copied to another venue cannot begin capturing faces there.\n"},"maxPassesPerBiometricIdentity":{"type":"integer","nullable":true,"minimum":1,"description":"BL-096, 2.14.7. **The annual-pass quota, keyed to biometric identity.** `enrolFacePass` already answers 409 where a face is on another annual pass; the constant behind that refusal was one and was invisible. **Null means unlimited** and is the answer for every product that is not an annual pass — a quota applied where nobody asked for one turns a family sharing a day ticket into a fraud alert.\n"}}}},
"Queue": {"x-ticvai-persistence":"queue.queue + queue.queue_operating_window","allOf":[{"$ref":"#/components/schemas/CreateQueueRequest"},{"type":"object","required":["id","status","waitingPartyCount"],"properties":{"id":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/QueueStatus"},"statusReason":{"type":"string","nullable":true},"waitingPartyCount":{"type":"integer"},"waitingGuestCount":{"type":"integer"},"currentWaitMinutes":{"type":"integer","nullable":true},"waitTimeSource":{"$ref":"#/components/schemas/WaitTimeSource"},"waitTimeAsOf":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When `currentWaitMinutes` was last set, by whichever source set it. `WaitTime.asOf` reads this.\n"},"manualWaitExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Set by `setWaitTime` as now plus `expiresInMinutes`. Past it, the manual figure is dropped and the queue reverts to its sensor or throughput estimate. Null when the current figure is not manual.\n"},"manualWaitNote":{"type":"string","maxLength":200,"nullable":true,"readOnly":true,"description":"The `note` given with the current manual figure. Cleared when it expires."},"expectedReopenAt":{"type":"string","format":"date-time","nullable":true}}}]},
"QueueFastPass": {"x-ticvai-persistence":"queue.queue","type":"object","description":"**Which Fast Pass entitlements this lane accepts, and how** (decided 29 September, VM close-out; pack 'Access Control Module' p.109, BO-221 Fast Pass & Attraction Access Journey). Fast Pass stays an entitlement owned by Product & Entitlement; this block is the lane's side of it: which products it honours, the return window, a per-guest daily cap and the access points that redeem it. Stored on the queue row. Only meaningful where `kind` is `fastPass` or `fastPassAllocationPercent` is above 0.\n**Four ways into priority, not one** (decided 29 September, build pass; 5.6.7 and 5.6.34). A guest joins this lane as priority when they hold an entitlement from `entitlementProductIds` (VIP, annual pass, premium package), are a member of a tier in `loyaltyTierIds`, qualify for a live promotion in `promotionIds`, or declare an accessibility need where `accessibilityPriority` is on. The first criterion met is recorded on the entry as `WaitingGuest.priorityBasis`. Every criterion is resolved by the server at join time; nothing the request asserts about a tier or a promotion is trusted. All four draw on the same reserved `fastPassAllocationPercent`, so widening who qualifies never widens the share of the ride they take.\n","required":["entitlementProductIds"],"properties":{"entitlementProductIds":{"type":"array","description":"Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need.\n","items":{"type":"string","format":"uuid"}},"loyaltyTierIds":{"type":"array","description":"5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. Read from the guest's own loyalty position at join time, never from the request, so a guest cannot claim a tier they do not hold. Empty: tier grants nothing on this lane.\n","items":{"type":"string","format":"uuid"}},"promotionIds":{"type":"array","description":"5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. A guest qualifies when the promotion's conditions hold for them at join (the evaluation `promotions` already makes for a price), or by presenting its code in `JoinQueueRequest.promotionCode`. A paused or expired promotion grants nothing.\n","items":{"type":"string","format":"uuid"}},"accessibilityPriority":{"type":"boolean","default":false,"description":"5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. **Taken on trust**, because asking for proof at a ride entrance is worse than the occasional abuse; the declaration is on the entry, so the operator at the front sees it (`listQueueEntries`). A venue that wants proof sells or issues an accessibility pass and lists it in `entitlementProductIds` instead. **Not the `accessible` lane**: that is where a guest who cannot stand in a switchback waits; this moves them ahead in the lane they chose.\n"},"returnWindowMinutes":{"type":"integer","minimum":1,"maximum":240,"default":60,"description":"How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan.\n"},"maxPerGuestPerDay":{"type":"integer","minimum":1,"nullable":true,"description":"Fast Pass redemptions one guest may make on this lane per day; null is no cap."},"allowedAccessPointIds":{"type":"array","description":"Access points that redeem Fast Pass for this lane; empty is the queue's own.","items":{"type":"string","format":"uuid"}}}},
"QueueStatus": {"type":"string","enum":["open","paused","closed","atCapacity"]},
"ReEntryTemporaryExitJourneyView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Re-entry & Temporary Exit Journey displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string","description":"Re-entry rule identifier"},"reEntryVerification":{"type":"string","enum":["credentialOnly","credentialUvStamp","credentialFace","credentialOperator","custom"],"description":"Verification required at re-entry"},"maximum":{"type":"integer","description":"Maximum re-entries allowed"},"name":{"type":"string","description":"Rule name"}},"required":["ruleId"]},
"SpecialEventFreeViewAlternativeAdmissionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Special Event, Free View & Alternative Admission displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"configId":{"type":"string","description":"Special admission configuration identifier"},"attendance":{"type":"integer","description":"Attendance (the pack shows +85)"},"admissionType":{"type":"string","enum":["freeViewDay","specialEvent"],"description":"Kind of special admission"},"startsAt":{"type":"string","format":"date-time","description":"Start"},"endsAt":{"type":"string","format":"date-time","description":"End"},"attractionValidation":{"type":"boolean","description":"Attraction gates keep validating tickets"},"manualAttendanceRequired":{"type":"boolean","description":"Operator enters attendance count"}},"required":["configId"]},
"WaitTimeSource": {"type":"string","description":"Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n","enum":["sensor","throughput","manual","unavailable"]}
}
```
