# WS12 — Access Control board 12

**10 screens · 16 operations · 23 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `REPORT_SCHEDULE, REPORT_VIEW_VENUE, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-254` | Access Monitoring & Analytics Command Center | B–D | 0 | 300 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-255` | Live Venue Occupancy & People Counting | B–D | 0 | 0 | 6 | 0 | 4 | 0 | — | notStarted (generated) |
| `BO-256` | Graphical Access Map & Live Gate Performance | B–D | 0 | 2 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-257` | Attendance & Admission Analytics | B–D | 2 | 18 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-258` | Entry, Exit, Re-entry & Crossover Analytics | B–D | 0 | 12 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-259` | Throughput, Queue & Validation Performance Analytics | B–D | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-260` | Validation Outcome & Rejection Analytics | B–D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-261` | Guest Dwell Time, Length of Stay & Attraction Flow | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-262` | Access Reports, Scheduled Reporting & Data Export | B–D | 2 | 0 | 6 | 9 | 0 | 0 | — | notStarted (generated) |
| `BO-263` | AI Access Intelligence, Forecasting & Executive Insights | B–D | 0 | 16 | 6 | 1 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-255, BO-256, BO-258, BO-260, BO-262, BO-263 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-254` Access Monitoring & Analytics Command Center

**Provide a single executive and operational overview of access performance across all TICVAI-controlled venues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-monitoring-analytics-command-center-bo-254` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Total Admissions Today** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Entries** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Exits** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Currently In Venue** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Re-entries** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Crossovers** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Group Admissions** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Fast Pass Uses** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Valid Scans** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Rejected Scans** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Intervention Rate** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Seconds** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Active Gates** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Offline Devices** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Every access monitoring analytics** (data table, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**The selected access monitoring analytics** (detail panel): The pack groups this record's detail under its own headings: “TOTAL ADMISSIONS”, “CURRENTLY IN VENUE”, “Venue Comparison”.

**Data it reads**: `listAccessMonitoring` (onLoad, Access Monitoring & Analytics Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-255` Live Venue Occupancy & People Counting: *Works in Live Venue Occupancy & People Counting*; calls `listAccessMonitoring`
- → `BO-256` Graphical Access Map & Live Gate Performance: *Works in Graphical Access Map & Live Gate Performance*; calls `listAccessMonitoring`
- → `BO-257` Attendance & Admission Analytics: *Works in Attendance & Admission Analytics*; calls `listAccessMonitoring`
- → `BO-258` Entry, Exit, Re-entry & Crossover Analytics: *Works in Entry, Exit, Re-entry & Crossover Analytics*; calls `listAccessMonitoring`
- → `BO-259` Throughput, Queue & Validation Performance Analytics: *Works in Throughput, Queue & Validation Performance Analytics*; calls `listAccessMonitoring`
- → `BO-260` Validation Outcome & Rejection Analytics: *Works in Validation Outcome & Rejection Analytics*; calls `listAccessMonitoring`
- → `BO-261` Guest Dwell Time, Length of Stay & Attraction Flow: *Works in Guest Dwell Time, Length of Stay & Attraction Flow*; calls `listAccessMonitoring`
- → `BO-262` Access Reports, Scheduled Reporting & Data Export: *Works in Access Reports, Scheduled Reporting & Data Export*; calls `listAccessMonitoring`
- → `BO-263` AI Access Intelligence, Forecasting & Executive Insights: *Works in AI Access Intelligence, Forecasting & Executive Insights*; calls `listAccessMonitoring`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access monitoring analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access monitoring analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access monitoring analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access monitoring analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAccessMonitoring` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Fraud assessment view flags suspicious usage patterns or threats; live monitoring shows current attendance, in-park counts and entry/exit/crossover activity per venue in real time. *(client request · MoM 2 Sep 2026, 4.16 Fraud Detection & Live Monitoring · DI-651)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-254` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-254`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 1: Opens Access Monitoring & Analytics Command Center → Provide a single executive and operational overview of access performance across all TICVAI-controlled venues.
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F122 branch at step 1 (expected): when Nothing has been set up on Access Monitoring & Analytics Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F122 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (300 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-254?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-255`, `BO-256`, `BO-257`, `BO-258`, `BO-259`, `BO-260`, `BO-261`, `BO-262`, `BO-263`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-255` Live Venue Occupancy & People Counting

**Provide real-time people counting and occupancy using entry and exit events.**

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
| Route | `/access-venue/live-venue-occupancy-people-counting-bo-255` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listLiveVenueOccupancy` (onLoad, Live Venue Occupancy & People Counting)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listLiveVenueOccupancy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The live venue occupancy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live venue occupancy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live venue occupancy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the live venue occupancy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listLiveVenueOccupancy` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Fraud assessment view flags suspicious usage patterns or threats; live monitoring shows current attendance, in-park counts and entry/exit/crossover activity per venue in real time. *(client request · MoM 2 Sep 2026, 4.16 Fraud Detection & Live Monitoring · DI-651)*
- Access decisions consider who, ticket type, where, when and context; e.g. an otherwise valid unused ticket is denied once the venue's maximum live occupancy is reached, until guests exit. Scanners need a venue-full denial state. *(agreed · MoM 2 Sep 2026, 4.16 Attribute-Based Access Control · DI-650)*
- Two capacity types shown distinctly: sales capacity (tickets sellable per performance) and admission capacity (a real-time, scan-based count of guests inside via entry/exit turnstiles), capping on-site attendance independent of tickets sold. *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-455)*
- Admission Summary dashboard: real-time headcount of guests inside the venue from ticket scans. *(agreed · MoM 7 Aug 2026, 21. Dashboards & Reporting · DI-182)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-255` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-255`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 2: Works in Live Venue Occupancy & People Counting → Provide real-time people counting and occupancy using entry and exit events.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-255?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-256` Graphical Access Map & Live Gate Performance

**Turn the graphical access topology created in Board 1 into a live operational analytics map.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/graphical-access-map-live-gate-performance-bo-256` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listGraphicalAccessMap` ?venue |
| Park | text field | — | — | `listGraphicalAccessMap` ?park |
| Zone | text field | — | — | `listGraphicalAccessMap` ?zone |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every graphical access map** (data table, from `listGraphicalAccessMap`)

| Shows | Format | Notes |
|---|---|---|
| Point type | chip: Gate, Turnstile, Entry point, Exit point, Re entry gate, Group gate… | — |

**The selected graphical access map** (detail panel): The pack groups this record's detail under its own headings: “Guests”, “Throughput”, “Success”, “Reject”, “Yellow”.

| Shows | Format | Notes |
|---|---|---|
| Point type | chip: Gate, Turnstile, Entry point, Exit point, Re entry gate, Group gate… | — |

**Data it reads**: `listGraphicalAccessMap` (onLoad, Graphical Access Map & Live Gate Performance)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listGraphicalAccessMap`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The graphical access map list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the graphical access map untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No graphical access map yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the graphical access map are still there. The pack's own statuses are 🟢 Healthy — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGraphicalAccessMap` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Venue-wide attendance overview (open/closed gates, offline/maintenance status, graphed) and a visual map of all access-control locations across venues/tenants, including entry and exit turnstile layouts that vary by venue. *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-623)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-256` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-256`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 4: Works in Graphical Access Map & Live Gate Performance → Turn the graphical access topology created in Board 1 into a live operational analytics map.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-256?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-257` Attendance & Admission Analytics

**Provide detailed reporting of who actually attended compared with tickets sold/reserved. This is particularly important because group admission may differ from purchased quantity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/attendance-admission-analytics-bo-257` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search attendance admission analytics | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by ticket type, product, event, timeslot, membership, channel and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | text field | — | — | `listAttendanceAdmission` ?product |
| Timeslot | text field | — | — | `listAttendanceAdmission` ?timeslot |
| Membership | text field | — | — | `listAttendanceAdmission` ?membership |
| B2B partner | text field | — | — | `listAttendanceAdmission` ?b2bPartner |
| Reseller | text field | — | — | `listAttendanceAdmission` ?reseller |
| Guest category | text field | — | — | `listAttendanceAdmission` ?guestCategory |
| Venue | text field | — | — | `listAttendanceAdmission` ?venue |
| Ticket type | text field | — | — | `listAttendanceAdmission` ?ticketType |
| Event | text field | — | — | `listAttendanceAdmission` ?event |
| Channel | text field | — | — | `listAttendanceAdmission` ?channel |
| Customer segment | text field | — | — | `listAttendanceAdmission` ?customerSegment |
| Date | text field | — | — | `listAttendanceAdmission` ?date |

#### Outputs: what the screen shows and produces

**Shown**

**Every attendance admission analytics** (data table, from `listAttendanceAdmission`)

| Shows | Format | Notes |
|---|---|---|
| Tickets sold | 1,234 | Tickets Sold |
| Tickets eligible today | 1,234 | Tickets Eligible Today |
| Tickets scanned | 1,234 | Tickets Scanned |
| Unique guests | 1,234 | Unique Guests |
| No shows | 1,234 | No-Shows |
| Group attendance | 1,234 | Group Attendance |
| Membership attendance | 1,234 | Membership Attendance |
| Repeat entry | 1,234 | Repeat Entry |
| No show rate | 12.5% | no-show rate |

**The selected attendance admission analytics** (detail panel): The pack groups this record's detail under its own headings: “Sold”, “Eligible”, “Attended”, “ATTENDANCE RATE”, “Purchased”, “Actual Attendance”.

| Shows | Format | Notes |
|---|---|---|
| Tickets sold | 1,234 | Tickets Sold |
| Tickets eligible today | 1,234 | Tickets Eligible Today |
| Tickets scanned | 1,234 | Tickets Scanned |
| Unique guests | 1,234 | Unique Guests |
| No shows | 1,234 | No-Shows |
| Group attendance | 1,234 | Group Attendance |
| Membership attendance | 1,234 | Membership Attendance |
| Repeat entry | 1,234 | Repeat Entry |
| No show rate | 12.5% | no-show rate |

**Data it reads**: `listAttendanceAdmission` (onLoad, Attendance & Admission Analytics)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listAttendanceAdmission`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attendance admission analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attendance admission analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attendance admission analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the attendance admission analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAttendanceAdmission` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-257` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-257`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 6: Works in Attendance & Admission Analytics → Provide detailed reporting of who actually attended compared with tickets sold/reserved. This is particularly important because group admission may differ from purchased quantity.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-257?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-258` Entry, Exit, Re-entry & Crossover Analytics

**Analyze complete guest movement across the access journey.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Measure) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/entry-exit-re-entry-crossover-analytics-bo-258` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every entry exit re-entry** (data table, from `listEntryExitCrossover`)

| Shows | Format | Notes |
|---|---|---|
| Re entry rate | 12.5% | Re-entry rate |
| Average time outside | 1,234 | Minutes |
| Most used re entry gates | list or chips (count when long) | most-used re-entry gates |
| Rejected re entry | 1,234 | rejected re-entry |
| Crossover time | 1,234 | Average minutes between leaving one park and entering the next |
| Crossover product | list or chips (count when long) | Products used for crossover, with counts |

**The selected entry exit re-entry** (detail panel): The pack groups this record's detail under its own headings: “Adventure Park”, “Water Park”.

| Shows | Format | Notes |
|---|---|---|
| Re entry rate | 12.5% | Re-entry rate |
| Average time outside | 1,234 | Minutes |
| Most used re entry gates | list or chips (count when long) | most-used re-entry gates |
| Rejected re entry | 1,234 | rejected re-entry |
| Crossover time | 1,234 | Average minutes between leaving one park and entering the next |
| Crossover product | list or chips (count when long) | Products used for crossover, with counts |

**Data it reads**: `listEntryExitCrossover` (onLoad, Entry, Exit, Re-entry & Crossover Analytics)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listEntryExitCrossover`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The entry exit re-entry list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the entry exit re-entry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No entry exit re-entry yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the entry exit re-entry are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listEntryExitCrossover` → `REPORT_VIEW_VENUE` (operate) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-258` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-258`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 8: Works in Entry, Exit, Re-entry & Crossover Analytics → Analyze complete guest movement across the access journey.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-258?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-259` Throughput, Queue & Validation Performance Analytics

**Measure the operational efficiency of gates and validation devices.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/throughput-queue-validation-performance-analytics-bo-259` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Guests per Minute** (metric tile)

**Guests per Hour** (metric tile)

**Average Scan Time** (metric tile)

**Average Gate Cycle** (metric tile)

**Success Rate** (metric tile)

**Yellow Rate** (metric tile)

**Reject Rate** (metric tile)

**Manual Intervention Rate** (metric tile)

**Data it reads**: `listThroughputQueueValidation` (onLoad, Throughput, Queue & Validation Performance Analytics)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listThroughputQueueValidation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The throughput queue validation list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the throughput queue validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No throughput queue validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the throughput queue validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listThroughputQueueValidation` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-259` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-259`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 10: Works in Throughput, Queue & Validation Performance Analytics → Measure the operational efficiency of gates and validation devices.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-259?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-260` Validation Outcome & Rejection Analytics

**Analyze why guests are denied or require manual intervention.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/validation-outcome-rejection-analytics-bo-260` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search validation outcome rejection | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, gate, product, ticket type, channel, reseller and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listValidationOutcomeRejection` ?venue |
| Gate | text field | — | — | `listValidationOutcomeRejection` ?gate |
| Product | text field | — | — | `listValidationOutcomeRejection` ?product |
| Ticket type | text field | — | — | `listValidationOutcomeRejection` ?ticketType |
| Channel | text field | — | — | `listValidationOutcomeRejection` ?channel |
| Reseller | text field | — | — | `listValidationOutcomeRejection` ?reseller |
| Operator | text field | — | — | `listValidationOutcomeRejection` ?operator |
| Device | text field | — | — | `listValidationOutcomeRejection` ?device |
| Credential type | text field | — | — | `listValidationOutcomeRejection` ?credentialType |
| Time | text field | — | — | `listValidationOutcomeRejection` ?time |

#### Outputs: what the screen shows and produces

**Data it reads**: `listValidationOutcomeRejection` (onLoad, Validation Outcome & Rejection Analytics)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listValidationOutcomeRejection`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The validation outcome rejection list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the validation outcome rejection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No validation outcome rejection yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the validation outcome rejection are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listValidationOutcomeRejection` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-260` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-260`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 12: Works in Validation Outcome & Rejection Analytics → Analyze why guests are denied or require manual intervention.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-260?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-261` Guest Dwell Time, Length of Stay & Attraction Flow

**Use access events to understand how guests move through and use the venue.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/guest-dwell-time-length-of-stay-attraction-flow-bo-261` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Average Length of Stay** (metric tile)

**Median Stay** (metric tile)

**Peak Arrival** (metric tile)

**Peak Departure** (metric tile)

**Zone Dwell Time** (metric tile)

**Attraction Visits** (metric tile)

**Fast Pass Usage** (metric tile)

**Data it reads**: `listGuestDwellTime` (onLoad, Guest Dwell Time, Length of Stay & Attraction Flow)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listGuestDwellTime`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest dwell time list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest dwell time untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest dwell time yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guest dwell time are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGuestDwellTime` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-261` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-261`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 14: Works in Guest Dwell Time, Length of Stay & Attraction Flow → Use access events to understand how guests move through and use the venue.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-261?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-262` Access Reports, Scheduled Reporting & Data Export

**Provide configurable operational and management reports.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `reportId` (navigation), `scheduleId` (navigation) |
| Route | `/access-venue/access-reports-scheduled-reporting-data-export-bo-262` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search access reports scheduled | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, park, zone, event, date and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listAccessReportScheduled` ?venue |
| Park | text field | — | — | `listAccessReportScheduled` ?park |
| Zone | text field | — | — | `listAccessReportScheduled` ?zone |
| Event | text field | — | — | `listAccessReportScheduled` ?event |
| Date | text field | — | — | `listAccessReportScheduled` ?date |
| Ticket type | text field | — | — | `listAccessReportScheduled` ?ticketType |
| Product | text field | — | — | `listAccessReportScheduled` ?product |
| Gate | text field | — | — | `listAccessReportScheduled` ?gate |
| Device | text field | — | — | `listAccessReportScheduled` ?device |
| Channel | text field | — | — | `listAccessReportScheduled` ?channel |
| Partner | text field | — | — | `listAccessReportScheduled` ?partner |
| Category | select | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | `listReports` ?category |
| Search | text field | — | — | `listReports` ?search |

#### Outputs: what the screen shows and produces

**Data it reads**: `listAccessReportScheduled` (onLoad, Access Reports, Scheduled Reporting & Data Export); `listReportSchedules` (onLoad, The scheduled access reports); `listReports` (onLoad, The access reports to run or schedule)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listAccessReportScheduled`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access reports scheduled list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access reports scheduled untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access reports scheduled yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access reports scheduled are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Invalid cadence (a field its frequency needs is missing, or one it does not take is sent, audit R158), or no recipients; 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158) |

#### Permissions

- `listAccessReportScheduled` → `REPORT_VIEW_VENUE` (operate) · staff
- `listReportSchedules` → `REPORT_VIEW_VENUE` (operate) · staff
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `createReportSchedule` → `REPORT_SCHEDULE` (operate) · staff
- `updateReportSchedule` → `REPORT_SCHEDULE` (operate) · staff
- `deleteReportSchedule` → `REPORT_SCHEDULE` (operate) · staff
- `listReports` → `REPORT_VIEW_VENUE` (operate) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |
| 6.1.14 | The system should have scheduling of report generation and delivery to web address location or list of email addresses. | Retail POS | CONTRACTED | `createReportSchedule` |
| 8.7.15 | System shall support report scheduling. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |
| 8.7.16 | System shall support report subscriptions. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |
| 8.7.17 | System shall support report sharing. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-262` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-262`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 16: Works in Access Reports, Scheduled Reporting & Data Export → Provide configurable operational and management reports.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-262?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-263` AI Access Intelligence, Forecasting & Executive Insights

**Turn access-control data into proactive operational intelligence. This should be the final intelligence screen of the entire Access Control module.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Forecast) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/ai-access-intelligence-forecasting-executive-insights-bo-263` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every access intelligence forecasting** (data table, from `listAccessExecutiveInsight`)

| Shows | Format | Notes |
|---|---|---|
| Tomorrow s attendance | 1,234 | Tomorrow's Attendance |
| Peak arrival time | text | Forecast time window, e.g. |
| Peak exit time | text | Forecast time window |
| Venue occupancy | 1,234 | Venue Occupancy |
| Zone occupancy | 1,234 | Zone Occupancy |
| Gate demand | 1,234 | Forecast guests per hour at peak across gates |
| Group arrival pressure | text | Group Arrival Pressure |
| Re entry demand | text | Re-entry Demand |

**The selected access intelligence forecasting** (detail panel): The pack groups this record's detail under its own headings: “Expected Attendance”, “Peak Arrival”, “Current Planned”, “Board 12 Key Workflow”, “Final Access Control Architecture”, “Board Area”.

| Shows | Format | Notes |
|---|---|---|
| Tomorrow s attendance | 1,234 | Tomorrow's Attendance |
| Peak arrival time | text | Forecast time window, e.g. |
| Peak exit time | text | Forecast time window |
| Venue occupancy | 1,234 | Venue Occupancy |
| Zone occupancy | 1,234 | Zone Occupancy |
| Gate demand | 1,234 | Forecast guests per hour at peak across gates |
| Group arrival pressure | text | Group Arrival Pressure |
| Re entry demand | text | Re-entry Demand |

**Data it reads**: `listAccessExecutiveInsight` (onLoad, AI Access Intelligence, Forecasting & Executive Insights)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access intelligence forecasting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access intelligence forecasting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access intelligence forecasting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access intelligence forecasting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAccessExecutiveInsight` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.46 | AI Policy Recommendations - System shall provide AI-assisted policy recommendations. | Admission and Access | CONTRACTED_PARTIAL | `listAccessExecutiveInsight` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-263` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-263`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 18: Works in AI Access Intelligence, Forecasting & Executive Insights → Turn access-control data into proactive operational intelligence. This should be the final intelligence screen of the entire Access Control module.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-263?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
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

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createReportSchedule": {"method":"POST","path":"/report-schedules","contract":"reporting","summary":"Schedule a report","permission":"REPORT_SCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportScheduleRequest","responds":"ReportSchedule"},
"deleteReportSchedule": {"method":"DELETE","path":"/report-schedules/{scheduleId}","contract":"reporting","summary":"Delete a schedule","permission":"REPORT_SCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listAccessExecutiveInsight": {"method":"GET","path":"/access-executive-insight","contract":"access","summary":"AI Access Intelligence, Forecasting & Executive Insights","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiAccessIntelligenceForecastingExecutiveInsightsView"},
"listAccessMonitoring": {"method":"GET","path":"/access-monitoring","contract":"access","summary":"Access Monitoring & Analytics Command Center","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAccessReportScheduled": {"method":"GET","path":"/access-report-scheduled","contract":"access","summary":"Access Reports, Scheduled Reporting & Data Export","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"park","in":"query","required":false},{"name":"zone","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"ticketType","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"gate","in":"query","required":false},{"name":"device","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"partner","in":"query","required":false}],"requestBody":null,"responds":"AccessReportsScheduledReportingDataExportView"},
"listAttendanceAdmission": {"method":"GET","path":"/attendance-admission","contract":"access","summary":"Attendance & Admission Analytics","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"product","in":"query","required":false},{"name":"timeslot","in":"query","required":false},{"name":"membership","in":"query","required":false},{"name":"b2bPartner","in":"query","required":false},{"name":"reseller","in":"query","required":false},{"name":"guestCategory","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"ticketType","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"date","in":"query","required":false}],"requestBody":null,"responds":"AttendanceAdmissionAnalyticsView"},
"listEntryExitCrossover": {"method":"GET","path":"/entry-exit-crossover","contract":"access","summary":"Entry, Exit, Re-entry & Crossover Analytics","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"EntryExitReEntryCrossoverAnalyticsView"},
"listGraphicalAccessMap": {"method":"GET","path":"/graphical-access-map","contract":"access","summary":"Graphical Access Map & Live Gate Performance","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venue","in":"query","required":false},{"name":"park","in":"query","required":false},{"name":"zone","in":"query","required":false}],"requestBody":null,"responds":"GraphicalAccessMapLiveGatePerformanceView"},
"listGuestDwellTime": {"method":"GET","path":"/guest-dwell-time","contract":"access","summary":"Guest Dwell Time, Length of Stay & Attraction Flow","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestDwellTimeLengthOfStayAttractionFlowView"},
"listLiveVenueOccupancy": {"method":"GET","path":"/live-venue-occupancy","contract":"access","summary":"Live Venue Occupancy & People Counting","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LiveVenueOccupancyPeopleCountingView"},
"listReportSchedules": {"method":"GET","path":"/report-schedules","contract":"reporting","summary":"List scheduled reports","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReports": {"method":"GET","path":"/reports","contract":"reporting","summary":"List available report definitions","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"category","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listThroughputQueueValidation": {"method":"GET","path":"/throughput-queue-validation","contract":"access","summary":"Throughput, Queue & Validation Performance Analytics","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ThroughputQueueValidationPerformanceAnalyticsView"},
"listValidationOutcomeRejection": {"method":"GET","path":"/validation-outcome-rejection","contract":"access","summary":"Validation Outcome & Rejection Analytics","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venue","in":"query","required":false},{"name":"gate","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"ticketType","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"reseller","in":"query","required":false},{"name":"operator","in":"query","required":false},{"name":"device","in":"query","required":false},{"name":"credentialType","in":"query","required":false},{"name":"time","in":"query","required":false}],"requestBody":null,"responds":"ValidationOutcomeRejectionAnalyticsView"},
"runReport": {"method":"POST","path":"/reports/{reportId}/run","contract":"reporting","summary":"Run a report","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RunReportRequest","responds":"ReportResult"},
"updateReportSchedule": {"method":"PATCH","path":"/report-schedules/{scheduleId}","contract":"reporting","summary":"Amend, pause or resume a schedule","permission":"REPORT_SCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReportSchedule"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessMonitoringAnalyticsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Monitoring & Analytics Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string"},"venueName":{"type":"string"},"venueEntries":{"type":"integer"},"venueInVenue":{"type":"integer"},"venueRejectedRate":{"type":"number","description":"Percent"},"venueThroughputPerMinute":{"type":"number"}},"required":["venueId"]},
"AccessMonitoringAnalyticsCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"totalAdmissionsToday":{"type":"integer","description":"Total Admissions Today"},"entries":{"type":"integer","description":"Entries"},"exits":{"type":"integer","description":"Exits"},"currentlyInVenue":{"type":"integer","description":"Currently In Venue"},"reEntries":{"type":"integer","description":"Re-entries"},"crossovers":{"type":"integer","description":"Crossovers"},"groupAdmissions":{"type":"integer","description":"Group Admissions"},"fastPassUses":{"type":"integer","description":"Fast Pass Uses"},"validScans":{"type":"integer","description":"Valid Scans"},"rejectedScans":{"type":"integer","description":"Rejected Scans"},"interventionRate":{"type":"number","description":"Intervention Rate"},"averageValidationTime":{"type":"number","description":"Seconds"},"activeGates":{"type":"integer","description":"Active Gates"},"offlineDevices":{"type":"integer","description":"Offline Devices"},"validationSuccessRate":{"type":"number","description":"Percent"}}},
"AccessReportsScheduledReportingDataExportView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Reports, Scheduled Reporting & Data Export displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string"},"reportId":{"type":"string"},"formats":{"type":"array","items":{"type":"string","enum":["dashboard","csv","xlsx","pdf","apiDataFeed","biIntegration"]}},"filterCriteria":{"type":"array","items":{"type":"string"},"description":"Saved filters, e.g. venue=..., gate=..."},"scheduleTime":{"type":"string","description":"Local time of day, e.g. 07:00"},"recipients":{"type":"array","items":{"type":"string"},"description":"Authorized recipients or reporting destinations"}},"required":["reportId","name"]},
"AiAccessIntelligenceForecastingExecutiveInsightsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What AI Access Intelligence, Forecasting & Executive Insights displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"tomorrowSAttendance":{"type":"integer","description":"Tomorrow's Attendance"},"peakArrivalTime":{"type":"string","description":"Forecast time window, e.g. 09:40-10:30"},"peakExitTime":{"type":"string","description":"Forecast time window"},"venueOccupancy":{"type":"integer","description":"Venue Occupancy"},"zoneOccupancy":{"type":"integer","description":"Zone Occupancy"},"gateDemand":{"type":"integer","description":"Forecast guests per hour at peak across gates"},"groupArrivalPressure":{"type":"string","description":"Group Arrival Pressure"},"reEntryDemand":{"type":"string","description":"Re-entry Demand"},"deviceCapacity":{"type":"integer","description":"Device Capacity"},"currentPlanned":{"type":"integer","description":"Entry lanes currently planned"},"recommendedEntryLanes":{"type":"integer"},"aiRecommendation":{"type":"string","description":"Advisory text only; any operational change goes through the normal permission and approval controls"}}},
"AttendanceAdmissionAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Attendance & Admission Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ticketsSold":{"type":"integer","description":"Tickets Sold"},"ticketsEligibleToday":{"type":"integer","description":"Tickets Eligible Today"},"ticketsScanned":{"type":"integer","description":"Tickets Scanned"},"uniqueGuests":{"type":"integer","description":"Unique Guests"},"noShows":{"type":"integer","description":"No-Shows"},"groupAttendance":{"type":"integer","description":"Group Attendance"},"membershipAttendance":{"type":"integer","description":"Membership Attendance"},"repeatEntry":{"type":"integer","description":"Repeat Entry"},"attendanceRate":{"type":"number","description":"Percent"},"noShowRate":{"type":"number","description":"no-show rate"}}},
"Cadence": {"x-ticvai-persistence":"none — embedded in schedule","type":"object","description":"**What each frequency needs (decided 28 September, audit R158).** `daily`: `timeOfDay`. `weekly`: `dayOfWeek` and `timeOfDay`. `monthly`: `dayOfMonth` and `timeOfDay`, a day past the month's end running on its last day. `quarterly`: `dayOfMonth` and `timeOfDay`, in the first month of each quarter. `onShiftClose` and `onPeriodClose`: nothing else, they run on the event. A field a frequency needs and does not have, or one it does not take, is the 400 on `createReportSchedule`. **Times are in the venue's time zone.**\n","required":["frequency"],"properties":{"frequency":{"type":"string","enum":["daily","weekly","monthly","quarterly","onShiftClose","onPeriodClose"]},"dayOfWeek":{"type":"integer","minimum":0,"maximum":6},"dayOfMonth":{"type":"integer","minimum":1,"maximum":31},"timeOfDay":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"timeZone":{"type":"string","readOnly":true,"description":"Always the venue's time zone (decided 28 September, audit R158), returned so a reader knows which. Not taken on a write."}}},
"CreateReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","category","dataSource","columns","requiredPermission"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"category":{"$ref":"#/components/schemas/ReportCategory"},"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"parameters":{"type":"array","items":{"$ref":"#/components/schemas/ReportParameter"}},"requiredPermission":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission","description":"Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"},"maxDateRangeDays":{"type":"integer","nullable":true,"minimum":1,"default":366,"description":"Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."}}},
"CreateReportScheduleRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["reportId","cadence","recipients","format"],"properties":{"reportId":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"cadence":{"$ref":"#/components/schemas/Cadence"},"parameters":{"type":"object","additionalProperties":true,"description":"As `RunReportRequest.parameters` — keyed by the report's `ReportParameter.key`, applied to every run."},"recipients":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/Recipient"}},"format":{"$ref":"#/components/schemas/ExportFormat"},"includePersonalData":{"type":"boolean","default":false},"skipIfEmpty":{"type":"boolean","default":true,"description":"An empty report every morning trains people to ignore the report."}}},
"EntryExitReEntryCrossoverAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Entry, Exit, Re-entry & Crossover Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"reEntryRate":{"type":"number","description":"Re-entry rate"},"averageTimeOutside":{"type":"integer","description":"Minutes"},"mostUsedReEntryGates":{"type":"array","items":{"type":"string"},"description":"most-used re-entry gates"},"rejectedReEntry":{"type":"integer","description":"rejected re-entry"},"reEntryByProduct":{"type":"array","items":{"type":"string"},"description":"Product and re-entry count pairs"},"crossoverTime":{"type":"integer","description":"Average minutes between leaving one park and entering the next"},"crossoverProduct":{"type":"array","items":{"type":"string"},"description":"Products used for crossover, with counts"},"crossoverUtilization":{"type":"number","description":"crossover utilization"},"firstEntries":{"type":"integer"},"temporaryExits":{"type":"integer"},"reEntries":{"type":"integer"},"crossovers":{"type":"integer"},"finalExits":{"type":"integer"},"crossoverFlows":{"type":"array","items":{"type":"string"},"description":"From park, to park and count, e.g. Park A to Park B"}}},
"ExecutionStatus": {"type":"string","enum":["queued","running","completed","failed","cancelled","expired"]},
"ExportFormat": {"type":"string","enum":["csv","xlsx","pdf","json"]},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"GraphicalAccessMapLiveGatePerformanceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Graphical Access Map & Live Gate Performance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"accessPointId":{"type":"string"},"pointType":{"type":"string","enum":["gate","turnstile","entryPoint","exitPoint","reEntryGate","groupGate","vipGate","attractionAccess","crossoverPoint"]},"status":{"type":"string","enum":["healthy","warning","critical","offline"]},"guests":{"type":"integer","description":"Guests (the pack shows 4,821)"},"success":{"type":"number","description":"Success rate, percent"},"reject":{"type":"number","description":"Reject rate, percent"},"yellow":{"type":"number","description":"Operator-review rate, percent"},"name":{"type":"string"},"parentId":{"type":"string","description":"Zone or park the point sits in"},"throughputPerMinute":{"type":"number"},"averageValidationSeconds":{"type":"number"}},"required":["accessPointId","pointType","status"]},
"GuestDwellTimeLengthOfStayAttractionFlowView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Guest Dwell Time, Length of Stay & Attraction Flow displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"averageLengthOfStay":{"type":"integer","description":"Minutes, where entry and exit data exist"},"medianStay":{"type":"integer","description":"Minutes"},"peakArrival":{"type":"string","description":"Time window, e.g. 09:40-10:30"},"peakDeparture":{"type":"string","description":"Time window"},"zoneDwellTime":{"type":"integer","description":"Average minutes in the selected zone"},"attractionVisits":{"type":"integer","description":"Attraction Visits"},"fastPassUsage":{"type":"integer","description":"Fast Pass Usage"},"reEntryBehavior":{"type":"string","description":"Re-entry behavior"},"uniqueGuests":{"type":"integer","description":"Unique Guests (the pack shows 5,842)"},"totalValidations":{"type":"integer","description":"Total Validations (the pack shows 6,211)"},"repeatVisits":{"type":"integer","description":"Repeat Visits (the pack shows 369)"}}},
"LiveVenueOccupancyPeopleCountingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Live Venue Occupancy & People Counting displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"areaLevel":{"type":"string","enum":["venue","park","zone","attraction","controlledArea"]},"areaId":{"type":"string"},"exits":{"type":"integer","description":"Exits (the pack shows ±)"},"operationalAdjustments":{"type":"integer","description":"Operational Adjustments (the pack shows =)"},"current":{"type":"integer","description":"Current (the pack shows 8,214)"},"capacity":{"type":"integer","description":"Capacity (the pack shows 12,000)"},"occupancy":{"type":"number","description":"Percent of capacity"},"areaName":{"type":"string"},"parentAreaId":{"type":"string"},"entries":{"type":"integer"},"status":{"type":"string","enum":["normal","warning","high","critical"],"description":"Band from the configured occupancy thresholds"}},"required":["areaId","areaLevel"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Recipient": {"x-ticvai-persistence":"reporting.schedule_recipient","type":"object","description":"One recipient of a schedule. **A row of `reporting.schedule_recipient`, a child of `reporting.schedule`** — `ReportSchedule` declares the pair, which is what gives the table its `schedule_id`. Pull audit 26 September: declared on its own, the table had no column tying a recipient to its schedule.\n","required":["kind","address"],"properties":{"kind":{"type":"string","enum":["principal","email","sftp","webhook"]},"address":{"type":"string"},"principalId":{"type":"string","format":"uuid"}}},
"ReportDefinition": {"x-ticvai-persistence":"reporting.report_definition + reporting.report_column + reporting.report_filter","allOf":[{"$ref":"#/components/schemas/CreateReportRequest"},{"type":"object","required":["id","version","isSystem","isRetired","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."},"isSystem":{"type":"boolean","description":"Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"},"isRetired":{"type":"boolean"},"estimatedCost":{"type":"string","enum":["low","medium","high"],"description":"Informs whether it may run inline or must be queued."},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}}]},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportSchedule": {"x-ticvai-persistence":"reporting.schedule + reporting.schedule_recipient","allOf":[{"$ref":"#/components/schemas/CreateReportScheduleRequest"},{"type":"object","required":["id","ownerPrincipalId","isPaused","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid","description":"The schedule runs under this principal's permissions, not the recipients'. A standing grant of whatever the owner can see.\n"},"isPaused":{"type":"boolean"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"lastRunStatus":{"$ref":"#/components/schemas/ExecutionStatus"},"nextRunAt":{"type":"string","format":"date-time","nullable":true},"consecutiveFailures":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"}}}]},
"RunReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","properties":{"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"},"venueId":{"type":"string","format":"uuid","description":"Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"},"dateFrom":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."},"dateTo":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (audit R158)."},"forceAsync":{"type":"boolean","default":false,"description":"Queue regardless of size, for a result to be collected later."}}},
"ThroughputQueueValidationPerformanceAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Throughput, Queue & Validation Performance Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"gateId":{"type":"string"},"guestsPerMinute":{"type":"number","description":"Guests per Minute"},"guestsPerHour":{"type":"integer","description":"Guests per Hour"},"averageScanTime":{"type":"number","description":"Seconds"},"averageGateCycle":{"type":"number","description":"Seconds"},"successRate":{"type":"number","description":"Success Rate"},"yellowRate":{"type":"number","description":"Yellow Rate"},"manualInterventionRate":{"type":"number","description":"Manual Intervention Rate"},"downtime":{"type":"integer","description":"Minutes"},"bottleneckReason":{"type":"string","enum":["qrReadFailures","excessiveManualVerification","hardwareLatency","policyComplexity","wrongGuestRouting"],"description":"Vocabulary listed under Potential reasons."},"gateName":{"type":"string"},"rejectRate":{"type":"number","description":"Percent"},"underperforming":{"type":"boolean"}},"required":["gateId"]},
"ValidationOutcomeRejectionAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Validation Outcome & Rejection Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"rejected":{"type":"integer","description":"Rejected (the pack shows 482)"},"overrides":{"type":"integer","description":"Overrides (the pack shows 281)"},"allowedRate":{"type":"number","description":"Percent"},"operatorReviewRate":{"type":"number","description":"Percent"},"deniedRate":{"type":"number","description":"Percent"},"overrideRate":{"type":"number","description":"Overrides as a percent of rejections"},"rejectionReasons":{"type":"array","items":{"type":"string"},"description":"Reason, count and share, e.g. Wrong Visit Date"}}}
}
```
