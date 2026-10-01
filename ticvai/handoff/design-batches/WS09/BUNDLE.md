# WS09 — Access Control board 9

**10 screens · 19 operations · 28 schemas · 8 permissions**

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
  `ACCESS_OVERRIDE, ACCESS_POINT_CONFIGURE, AUDIT_VIEW, DEVICE_CONFIGURE, INCIDENT_MANAGE, SCOPE_VIEW, TICKET_LOOKUP, TURNSTILE_MODE_SET`. A control nobody can use must say so,
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
| `BO-224` | Live Access Operations Command Center | B–D | 0 | 260 | 6 | 0 | 3 | 0 | — | notStarted (generated) |
| `BO-225` | Podium Operations Console | B–D | 9 | 7 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-226` | Ticket & Credential Investigation Console | B–D | 2 | 0 | 6 | 0 | 3 | 0 | — | notStarted (generated) |
| `BO-227` | Validation Exception & Reason Code Manager | B–D | 9 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-228` | Manual Override & Supervisor Approval | B–D | 11 | 0 | 5 | 0 | 1 | 3 | — | notStarted (generated) |
| `BO-229` | Credential Disable, Blacklist & Whitelist Operations | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-230` | Live Gate Mode & Lane Control | B–D | 1 | 8 | 6 | 3 | 1 | 0 | — | notStarted (generated) |
| `BO-231` | Queue, Throughput & Lane Optimization | B–D | 0 | 2 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-232` | Operational Incident & Exception Workspace | B–D | 7 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-233` | Operations Audit, Shift Handover & Control Summary | B–D | 1 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |

## Thin screens in this batch

**BO-226, BO-227, BO-229, BO-230, BO-231, BO-232, BO-233 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-224` Live Access Operations Command Center

**Provide the venue control room with a real-time view of access operations across all gates, parks, zones, and attractions.**

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
| Route | `/access-venue/live-access-operations-command-center-bo-224` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Guests Entered Today** (metric tile, from `listLiveAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Access point | text | Gate |
| Name | text | Gate name |
| Mode | text | Current gate mode |
| Status | chip: Online, Offline, Degraded | Gate status |
| Queue level | chip: Low, Moderate, High | Queue level |
| Throughput per minute | 1,234.5 | Guests per minute at this gate |
| Last scan at | 1 Oct 2026, 14:30 | Last scan |
| Valid percent | 1,234.5 | Valid scans percentage |
| Yellow percent | 1,234.5 | Intervention scans percentage |
| Rejected percent | 1,234.5 | Rejected scans percentage |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Guests entered today | 1,234 | Guests Entered Today |
| Guests exited | 1,234 | Guests Exited |
| Guests currently in park | 1,234 | Guests Currently In Park |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |
| Yellow intervention scans | 1,234 | Yellow / Intervention Scans |

**Guests Exited** (metric tile, from `listLiveAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Access point | text | Gate |
| Name | text | Gate name |
| Mode | text | Current gate mode |
| Status | chip: Online, Offline, Degraded | Gate status |
| Queue level | chip: Low, Moderate, High | Queue level |
| Throughput per minute | 1,234.5 | Guests per minute at this gate |
| Last scan at | 1 Oct 2026, 14:30 | Last scan |
| Valid percent | 1,234.5 | Valid scans percentage |
| Yellow percent | 1,234.5 | Intervention scans percentage |
| Rejected percent | 1,234.5 | Rejected scans percentage |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Guests entered today | 1,234 | Guests Entered Today |
| Guests exited | 1,234 | Guests Exited |
| Guests currently in park | 1,234 | Guests Currently In Park |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |
| Yellow intervention scans | 1,234 | Yellow / Intervention Scans |

**Guests Currently In Park** (metric tile, from `listLiveAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Access point | text | Gate |
| Name | text | Gate name |
| Mode | text | Current gate mode |
| Status | chip: Online, Offline, Degraded | Gate status |
| Queue level | chip: Low, Moderate, High | Queue level |
| Throughput per minute | 1,234.5 | Guests per minute at this gate |
| Last scan at | 1 Oct 2026, 14:30 | Last scan |
| Valid percent | 1,234.5 | Valid scans percentage |
| Yellow percent | 1,234.5 | Intervention scans percentage |
| Rejected percent | 1,234.5 | Rejected scans percentage |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Guests entered today | 1,234 | Guests Entered Today |
| Guests exited | 1,234 | Guests Exited |
| Guests currently in park | 1,234 | Guests Currently In Park |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |
| Yellow intervention scans | 1,234 | Yellow / Intervention Scans |

**Valid Scans** (metric tile, from `listLiveAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Access point | text | Gate |
| Name | text | Gate name |
| Mode | text | Current gate mode |
| Status | chip: Online, Offline, Degraded | Gate status |
| Queue level | chip: Low, Moderate, High | Queue level |
| Throughput per minute | 1,234.5 | Guests per minute at this gate |
| Last scan at | 1 Oct 2026, 14:30 | Last scan |
| Valid percent | 1,234.5 | Valid scans percentage |
| Yellow percent | 1,234.5 | Intervention scans percentage |
| Rejected percent | 1,234.5 | Rejected scans percentage |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Guests entered today | 1,234 | Guests Entered Today |
| Guests exited | 1,234 | Guests Exited |
| Guests currently in park | 1,234 | Guests Currently In Park |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |
| Yellow intervention scans | 1,234 | Yellow / Intervention Scans |

**Rejected Scans** (metric tile, from `listLiveAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Access point | text | Gate |
| Name | text | Gate name |
| Mode | text | Current gate mode |
| Status | chip: Online, Offline, Degraded | Gate status |
| Queue level | chip: Low, Moderate, High | Queue level |
| Throughput per minute | 1,234.5 | Guests per minute at this gate |
| Last scan at | 1 Oct 2026, 14:30 | Last scan |
| Valid percent | 1,234.5 | Valid scans percentage |
| Yellow percent | 1,234.5 | Intervention scans percentage |
| Rejected percent | 1,234.5 | Rejected scans percentage |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Guests entered today | 1,234 | Guests Entered Today |
| Guests exited | 1,234 | Guests Exited |
| Guests currently in park | 1,234 | Guests Currently In Park |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |
| Yellow intervention scans | 1,234 | Yellow / Intervention Scans |

**Yellow / Intervention Scans** (metric tile, from `listLiveAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Access point | text | Gate |
| Name | text | Gate name |
| Mode | text | Current gate mode |
| Status | chip: Online, Offline, Degraded | Gate status |
| Queue level | chip: Low, Moderate, High | Queue level |
| Throughput per minute | 1,234.5 | Guests per minute at this gate |
| Last scan at | 1 Oct 2026, 14:30 | Last scan |
| Valid percent | 1,234.5 | Valid scans percentage |
| Yellow percent | 1,234.5 | Intervention scans percentage |
| Rejected percent | 1,234.5 | Rejected scans percentage |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Guests entered today | 1,234 | Guests Entered Today |
| Guests exited | 1,234 | Guests Exited |
| Guests currently in park | 1,234 | Guests Currently In Park |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |
| Yellow intervention scans | 1,234 | Yellow / Intervention Scans |

**Overrides** (metric tile, from `listLiveAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Access point | text | Gate |
| Name | text | Gate name |
| Mode | text | Current gate mode |
| Status | chip: Online, Offline, Degraded | Gate status |
| Queue level | chip: Low, Moderate, High | Queue level |
| Throughput per minute | 1,234.5 | Guests per minute at this gate |
| Last scan at | 1 Oct 2026, 14:30 | Last scan |
| Valid percent | 1,234.5 | Valid scans percentage |
| Yellow percent | 1,234.5 | Intervention scans percentage |
| Rejected percent | 1,234.5 | Rejected scans percentage |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Guests entered today | 1,234 | Guests Entered Today |
| Guests exited | 1,234 | Guests Exited |
| Guests currently in park | 1,234 | Guests Currently In Park |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |
| Yellow intervention scans | 1,234 | Yellow / Intervention Scans |

**Active Gates** (metric tile, from `listLiveAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Access point | text | Gate |
| Name | text | Gate name |
| Mode | text | Current gate mode |
| Status | chip: Online, Offline, Degraded | Gate status |
| Queue level | chip: Low, Moderate, High | Queue level |
| Throughput per minute | 1,234.5 | Guests per minute at this gate |
| Last scan at | 1 Oct 2026, 14:30 | Last scan |
| Valid percent | 1,234.5 | Valid scans percentage |
| Yellow percent | 1,234.5 | Intervention scans percentage |
| Rejected percent | 1,234.5 | Rejected scans percentage |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Guests entered today | 1,234 | Guests Entered Today |
| Guests exited | 1,234 | Guests Exited |
| Guests currently in park | 1,234 | Guests Currently In Park |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |
| Yellow intervention scans | 1,234 | Yellow / Intervention Scans |

**Offline Gates** (metric tile, from `listLiveAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Access point | text | Gate |
| Name | text | Gate name |
| Mode | text | Current gate mode |
| Status | chip: Online, Offline, Degraded | Gate status |
| Queue level | chip: Low, Moderate, High | Queue level |
| Throughput per minute | 1,234.5 | Guests per minute at this gate |
| Last scan at | 1 Oct 2026, 14:30 | Last scan |
| Valid percent | 1,234.5 | Valid scans percentage |
| Yellow percent | 1,234.5 | Intervention scans percentage |
| Rejected percent | 1,234.5 | Rejected scans percentage |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Guests entered today | 1,234 | Guests Entered Today |
| Guests exited | 1,234 | Guests Exited |
| Guests currently in park | 1,234 | Guests Currently In Park |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |
| Yellow intervention scans | 1,234 | Yellow / Intervention Scans |

**Average validation time in seconds** (metric tile, from `listLiveAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Access point | text | Gate |
| Name | text | Gate name |
| Mode | text | Current gate mode |
| Status | chip: Online, Offline, Degraded | Gate status |
| Queue level | chip: Low, Moderate, High | Queue level |
| Throughput per minute | 1,234.5 | Guests per minute at this gate |
| Last scan at | 1 Oct 2026, 14:30 | Last scan |
| Valid percent | 1,234.5 | Valid scans percentage |
| Yellow percent | 1,234.5 | Intervention scans percentage |
| Rejected percent | 1,234.5 | Rejected scans percentage |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Guests entered today | 1,234 | Guests Entered Today |
| Guests exited | 1,234 | Guests Exited |
| Guests currently in park | 1,234 | Guests Currently In Park |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |
| Yellow intervention scans | 1,234 | Yellow / Intervention Scans |

**Guests per minute** (metric tile, from `listLiveAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Access point | text | Gate |
| Name | text | Gate name |
| Mode | text | Current gate mode |
| Status | chip: Online, Offline, Degraded | Gate status |
| Queue level | chip: Low, Moderate, High | Queue level |
| Throughput per minute | 1,234.5 | Guests per minute at this gate |
| Last scan at | 1 Oct 2026, 14:30 | Last scan |
| Valid percent | 1,234.5 | Valid scans percentage |
| Yellow percent | 1,234.5 | Intervention scans percentage |
| Rejected percent | 1,234.5 | Rejected scans percentage |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Guests entered today | 1,234 | Guests Entered Today |
| Guests exited | 1,234 | Guests Exited |
| Guests currently in park | 1,234 | Guests Currently In Park |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |
| Yellow intervention scans | 1,234 | Yellow / Intervention Scans |

**Active Operational Alerts** (metric tile, from `listLiveAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Access point | text | Gate |
| Name | text | Gate name |
| Mode | text | Current gate mode |
| Status | chip: Online, Offline, Degraded | Gate status |
| Queue level | chip: Low, Moderate, High | Queue level |
| Throughput per minute | 1,234.5 | Guests per minute at this gate |
| Last scan at | 1 Oct 2026, 14:30 | Last scan |
| Valid percent | 1,234.5 | Valid scans percentage |
| Yellow percent | 1,234.5 | Intervention scans percentage |
| Rejected percent | 1,234.5 | Rejected scans percentage |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Guests entered today | 1,234 | Guests Entered Today |
| Guests exited | 1,234 | Guests Exited |
| Guests currently in park | 1,234 | Guests Currently In Park |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |
| Yellow intervention scans | 1,234 | Yellow / Intervention Scans |

**Every live access operations** (data table, from `listLiveAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Access point | text | Gate |
| Name | text | Gate name |
| Mode | text | Current gate mode |
| Status | chip: Online, Offline, Degraded | Gate status |
| Queue level | chip: Low, Moderate, High | Queue level |
| Throughput per minute | 1,234.5 | Guests per minute at this gate |
| Last scan at | 1 Oct 2026, 14:30 | Last scan |
| Valid percent | 1,234.5 | Valid scans percentage |
| Yellow percent | 1,234.5 | Intervention scans percentage |
| Rejected percent | 1,234.5 | Rejected scans percentage |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Guests entered today | 1,234 | Guests Entered Today |
| Guests exited | 1,234 | Guests Exited |
| Guests currently in park | 1,234 | Guests Currently In Park |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |
| Yellow intervention scans | 1,234 | Yellow / Intervention Scans |

**The selected live access operations** (detail panel): The pack groups this record's detail under its own headings: “Live Venue Map”, “Adventure Park”, “MAIN GATE 03”, “QUEUE WARNING”, “REJECTION SPIKE”, “DEVICE WARNING”.

**Data it reads**: `listLiveAccess` (onLoad, Live Access Operations Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-225` Podium Operations Console: *Works in Podium Operations Console*; calls `listLiveAccess`
- → `BO-226` Ticket & Credential Investigation Console: *Works in Ticket & Credential Investigation Console*; calls `listLiveAccess`
- → `BO-227` Validation Exception & Reason Code Manager: *Works in Validation Exception & Reason Code Manager*; calls `listLiveAccess`
- → `BO-228` Manual Override & Supervisor Approval: *Works in Manual Override & Supervisor Approval*; calls `listLiveAccess`
- → `BO-229` Credential Disable, Blacklist & Whitelist Operations: *Works in Credential Disable, Blacklist & Whitelist Operations*; calls `listLiveAccess`
- → `BO-231` Queue, Throughput & Lane Optimization: *Works in Queue, Throughput & Lane Optimization*; calls `listLiveAccess`
- → `BO-232` Operational Incident & Exception Workspace: *Works in Operational Incident & Exception Workspace*; calls `listLiveAccess`
- → `BO-233` Operations Audit, Shift Handover & Control Summary: *Works in Operations Audit, Shift Handover & Control Summary*; calls `listLiveAccess`
- → `BO-230` Live Gate Mode & Lane Control: *Works in Live Gate Mode & Lane Control*; carries `accessPointId`; calls `listLiveAccess`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The live access operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live access operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live access operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the live access operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listLiveAccess` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Live operations dashboard: real-time attendance by venue and gate with each gate's online/offline status and entry count. Turnstile mode can be switched through the day (more entry gates in the morning, more exit in the evening). *(client request · MoM 2 Sep 2026, 4.15 Live Operations Dashboard · DI-648)*
- Real-time health view of device connectivity. Device-pushed events (anti-passback attempts, power loss, network loss) are surfaced as alerts and reports, e.g. notifying the operations team when a turnstile goes offline. *(agreed · MoM 2 Sep 2026, 4.1 / 4.2 Health Monitoring & Alerts · DI-625)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-224` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS26 Access Control Board 9.dc.html#bo-224`
- Workshop pack: Access Control Module_Reference.pdf board 9
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 1: Opens Live Access Operations Command Center → Provide the venue control room with a real-time view of access operations across all gates, parks, zones, and attractions.
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F119 branch at step 1 (expected): when Nothing has been set up on Live Access Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F119 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (260 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-224?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-225`, `BO-226`, `BO-227`, `BO-228`, `BO-229`, `BO-231`, `BO-232`, `BO-233`, `BO-230`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-225` Podium Operations Console

**Provide the operational interface described in the matrix for attendants controlling one or more turnstiles.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE`, `SCOPE_VIEW`, `TURNSTILE_MODE_SET` (1 configure, 1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `shiftId` (navigation), `podiumId` (navigation) |
| Route | `/access-venue/podium-operations-console-bo-225` |

#### Inputs: what the user enters or picks

**Form: Save podium** (modal, opened by *Save podium*; *Save podium* calls `setPodium`, *Cancel* sends nothing)

**Collects what `setPodium` sends before it is called.** Required: `id`, `venueId`, `podiumType`, `name`, `scopePath`. Optional: `accessPointIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setPodium` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setPodium` body |
| Podium type `podiumType` | radio group | required | — | Physical control panel · Tablet · Workstation · Handheld · Other | — | — | `setPodium` body |
| Name `name` | text field | required | — | — | — | e.g. | `setPodium` body |
| Access points `accessPointIds` | multi-picker: choose access points | optional | — | — | — | Gates this podium controls | `setPodium` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setPodium` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 An access point is not in the podium's venue.

**Form: Start podium shift** (modal, opened by *Start podium shift*; *Start podium shift* calls `startPodiumShift`, *Cancel* sends nothing)

**Collects what `startPodiumShift` sends before it is called.** Nothing in the body is required. Optional: `role`, `accessDeviceId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Role `role` | text field | optional | — | max length 64 | — | Role the operator acts in on this podium | `startPodiumShift` body |
| Access device `accessDeviceId` | picker: choose an access device | optional | — | — | shows names, sends the id | The handheld or unit the operator signs in on, where it is not the podium itself | `startPodiumShift` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: End podium shift** (modal, opened by *End podium shift*; *End podium shift* calls `endPodiumShift`, *Cancel* sends nothing)

**Collects what `endPodiumShift` sends before it is called.** Nothing in the body is required. Optional: `handoverNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Handover note `handoverNote` | text area | optional | — | max length 1000 | — | — | `endPodiumShift` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `shift-ended`: the shift is already ended.

#### Outputs: what the screen shows and produces

**Shown**

**Every podium operations console** (data table, from `listPodiumConsole`)

| Shows | Format | Notes |
|---|---|---|
| Podium | text | Podium identifier |
| Podium type | chip: Physical control panel, Tablet, Workstation, Handheld, Other | Kind of podium interface |
| Name | text | Podium name, e.g. |
| Access points | list or chips (count when long) | Gates this podium controls |
| Operator | text | Operator on shift |
| Shift start | 1 Oct 2026, 14:30 | Shift start |
| Shift end | 1 Oct 2026, 14:30 | Shift end |

**The selected podium operations console** (detail panel): The pack groups this record's detail under its own headings: “The podium may be”, “Controls”, “Operator”, “Shift”, “Authorized actions”, “Important”.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save podium (primary button) | `setPodium` PUT `/podiums` | AccessPodium | AccessPodium | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `DEVICE_CONFIGURE`; opens modal first |
| Delete podium (destructive button) | `deletePodium` DELETE `/podiums/{podiumId}` | — | — | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `DEVICE_CONFIGURE` |
| Start podium shift (secondary button) | `startPodiumShift` POST `/podiums/{podiumId}/shifts` | inline | AccessPodiumShift | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `TURNSTILE_MODE_SET`; opens modal first |
| End podium shift (secondary button) | `endPodiumShift` POST `/podium-shifts/{shiftId}/end` | inline | AccessPodiumShift | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `TURNSTILE_MODE_SET`; opens modal first |

**Data it reads**: `listPodiumConsole` (onLoad, Podium Operations Console)

**Where the user goes next**

- → `BO-224` Live Access Operations Command Center: *Returns to the board's landing screen*; calls `listPodiumConsole`

**What opens over it**

- confirmDialog *Delete podium*: **Names what `deletePodium` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The podium operations console list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the podium operations console untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No podium operations console yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the podium operations console are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `shift-ended`: the shift is already ended.; 409 `shift-open`: an operator is signed in to this podium.; 422 An access point is not in the podium's venue. |

#### Permissions

- `listPodiumConsole` → `SCOPE_VIEW` (read) · staff
- `setPodium` → `DEVICE_CONFIGURE` (configure) · staff
- `deletePodium` → `DEVICE_CONFIGURE` (configure) · staff
- `startPodiumShift` → `TURNSTILE_MODE_SET` (operate) · staff
- `endPodiumShift` → `TURNSTILE_MODE_SET` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-225` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS26 Access Control Board 9.dc.html#bo-225`
- Workshop pack: Access Control Module_Reference.pdf board 9
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 2: Works in Podium Operations Console → Provide the operational interface described in the matrix for attendants controlling one or more turnstiles.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-225?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save podium, Delete podium, Start podium shift, End podium shift.
- [ ] Every transition is wired: `BO-224`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`, `SCOPE_VIEW`, `TURNSTILE_MODE_SET`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-226` Ticket & Credential Investigation Console

**Allow operators to quickly investigate why a guest cannot enter.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `TICKET_LOOKUP` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/ticket-credential-investigation-console-bo-226` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search ticket credential investigation | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by ticket id, qr, barcode, rfid, nfc, virtual credential id and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Ticket | text field | — | — | `listTicketCredentialInvestigation` ?ticketId |
| QR | text field | — | — | `listTicketCredentialInvestigation` ?qr |
| Barcode | text field | — | — | `listTicketCredentialInvestigation` ?barcode |
| RFID | text field | — | — | `listTicketCredentialInvestigation` ?rfid |
| NFC | text field | — | — | `listTicketCredentialInvestigation` ?nfc |
| Virtual credential | text field | — | — | `listTicketCredentialInvestigation` ?virtualCredentialId |
| Order number | text field | — | — | `listTicketCredentialInvestigation` ?orderNumber |
| Membership | text field | — | — | `listTicketCredentialInvestigation` ?membership |
| Guest name | text field | — | — | `listTicketCredentialInvestigation` ?guestName |
| Email | text field | — | — | `listTicketCredentialInvestigation` ?email |
| Mobile | phone field | — | — | `listTicketCredentialInvestigation` ?mobile |
| External partner reference | text field | — | — | `listTicketCredentialInvestigation` ?externalPartnerReference |

#### Outputs: what the screen shows and produces

**Data it reads**: `listTicketCredentialInvestigation` (onLoad, Ticket & Credential Investigation Console)

**Where the user goes next**

- → `BO-224` Live Access Operations Command Center: *Returns to the board's landing screen*; calls `listTicketCredentialInvestigation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticket credential investigation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticket credential investigation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticket credential investigation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the ticket credential investigation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listTicketCredentialInvestigation` → `TICKET_LOOKUP` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Ticket lookup shows the complete scan history: purchaser, gate and timestamp for every attempt. Security can manually override to admit a guest despite a scan issue; every override is logged against the visitor's record. *(client request · MoM 2 Sep 2026, 4.16 Ticket Lookup & Manual Override · DI-649)*
- A successful scan marks the ticket used even if the guest did not pass (stroller, turnstile re-locked). Genuine cases are resolved manually by security from the ticket's scan-history log, so scanner lookup must show it. *(agreed · MoM 2 Sep 2026, 4.3 Decision (scan without physical passage) · DI-627)*
- Ticket look-up shows the ticket's full consumption history: transaction date/time, number of scans, expiry, and (if applicable) wallet balance and F&B/retail spend against that ticket. *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-462)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-226` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS26 Access Control Board 9.dc.html#bo-226`
- Workshop pack: Access Control Module_Reference.pdf board 9
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 4: Works in Ticket & Credential Investigation Console → Allow operators to quickly investigate why a guest cannot enter.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-226?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-224`.
- [ ] Every gated control is gated: `TICKET_LOOKUP`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-227` Validation Exception & Reason Code Manager

**Standardize what happens when access is not automatically granted. The matrix requires the scanner to display a reason code when a ticket is invalid.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `reasonCodeId` (navigation) |
| Route | `/access-venue/validation-exception-reason-code-manager-bo-227` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Form: Save reason code** (modal, opened by *Save reason code*; *Save reason code* calls `setReasonCode`, *Cancel* sends nothing)

**Collects what `setReasonCode` sends before it is called.** Required: `id`, `code`, `name`, `operationalResponse`, `scopePath`. Optional: `venueId`, `guestMessage`, `operatorMessage`, `followUpAction`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setReasonCode` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | Null for a tenant-wide code | `setReasonCode` body |
| Code `code` | text field | required | — | max length 32 | — | e.g. | `setReasonCode` body |
| Name `name` | text field | required | — | — | — | e.g. | `setReasonCode` body |
| Guest message `guestMessage` | text field | optional | — | — | — | — | `setReasonCode` body |
| Operator message `operatorMessage` | text field | optional | — | — | — | — | `setReasonCode` body |
| Operational response `operationalResponse` | radio group | required | — | Deny · Operator review · Supervisor required · Allow with warning | — | — | `setReasonCode` body |
| Follow up action `followUpAction` | text field | optional | — | — | — | — | `setReasonCode` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setReasonCode` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save reason code (primary button) | `setReasonCode` PUT `/reason-codes` | AccessReasonCode | AccessReasonCode | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |
| Delete reason code (destructive button) | `deleteReasonCode` DELETE `/reason-codes/{reasonCodeId}` | — | — | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE` |

**Data it reads**: `listValidationExceptionReason` (onLoad, Validation Exception & Reason Code Manager)

**Where the user goes next**

- → `BO-224` Live Access Operations Command Center: *Returns to the board's landing screen*; calls `listValidationExceptionReason`

**What opens over it**

- confirmDialog *Delete reason code*: **Names what `deleteReasonCode` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The validation exception reason list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the validation exception reason untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No validation exception reason yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the validation exception reason are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 `reason-code-in-use`: a scan event carries this code. |

#### Permissions

- `listValidationExceptionReason` → `SCOPE_VIEW` (read) · staff
- `setReasonCode` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `deleteReasonCode` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-227` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS26 Access Control Board 9.dc.html#bo-227`
- Workshop pack: Access Control Module_Reference.pdf board 9
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 6: Works in Validation Exception & Reason Code Manager → Standardize what happens when access is not automatically granted. The matrix requires the scanner to display a reason code when a ticket is invalid.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-227?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save reason code, Delete reason code.
- [ ] Every transition is wired: `BO-224`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-228` Manual Override & Supervisor Approval

**Allow authorized staff to bypass selected access restrictions when operationally justified. The matrix explicitly requires Allow Override and operator-based ticket override.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_OVERRIDE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configured Date; Select) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/manual-override-supervisor-approval-bo-228` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| 02 Sep | select field | — | — | — | — | — | — |
| Guest Service | select field | — | — | — | — | — | — |
| Ticketing Error | select field | — | — | — | — | — | — |
| Operational Exception | select field | — | — | — | — | — | — |
| Management Authorization | select field | — | — | — | — | — | — |
| Technical Failure | select field | — | — | — | — | — | — |
| Event Exception | select field | — | — | — | — | — | — |

**Sent by *Approve*** (`overrideAccess`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `overrideAccess` body |
| Scan `scanId` | picker: choose a scan | required | — | — | shows names, sends the id | The denied scan being overridden. | `overrideAccess` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `overrideAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `overrideAccess` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | gated `ACCESS_OVERRIDE` |

**Where the user goes next**

- → `BO-224` Live Access Operations Command Center: *Returns to the board's landing screen*; calls `overrideAccess`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The manual override supervisor configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the manual override supervisor untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No manual override supervisor configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission, **ACCESS_OVERRIDE** (was ACCESS_POINT_CONFIGURE until 29 September, K1: recording an admission against a failed validation is an override, not gate configuration). Never an empty table. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The scan was not a denial, or has already been overridden |

#### Permissions

- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff

**A refused user sees:** Names the missing permission, **ACCESS_OVERRIDE** (was ACCESS_POINT_CONFIGURE until 29 September, K1: recording an admission against a failed validation is an override, not gate configuration). Never an empty table.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Ticket lookup shows the complete scan history: purchaser, gate and timestamp for every attempt. Security can manually override to admit a guest despite a scan issue; every override is logged against the visitor's record. *(client request · MoM 2 Sep 2026, 4.16 Ticket Lookup & Manual Override · DI-649)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-228` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS26 Access Control Board 9.dc.html#bo-228`
- Workshop pack: Access Control Module_Reference.pdf board 9
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 8: Works in Manual Override & Supervisor Approval → Allow authorized staff to bypass selected access restrictions when operationally justified. The matrix explicitly requires Allow Override and operator-based ticket override.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-228?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve.
- [ ] Every transition is wired: `BO-224`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-229` Credential Disable, Blacklist & Whitelist Operations

**Provide immediate operational security control over individual credentials.**

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
| Route | `/access-venue/credential-disable-blacklist-whitelist-operations-bo-229` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listCredentialDisableBlacklist` (onLoad, Credential Disable, Blacklist & Whitelist Operations)

**Where the user goes next**

- → `BO-224` Live Access Operations Command Center: *Returns to the board's landing screen*; calls `listCredentialDisableBlacklist`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential disable blacklist list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential disable blacklist untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential disable blacklist yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential disable blacklist are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCredentialDisableBlacklist` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-229` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS26 Access Control Board 9.dc.html#bo-229`
- Workshop pack: Access Control Module_Reference.pdf board 9
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 10: Works in Credential Disable, Blacklist & Whitelist Operations → Provide immediate operational security control over individual credentials.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-229?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-224`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-230` Live Gate Mode & Lane Control

**Allow operations to change access-point modes during live operations without entering the Board 6 engineering configuration. Board 6 defines which modes a device can support. Board 9 controls which permitted mode it is currently running.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW`, `TURNSTILE_MODE_SET` (1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `accessPointId` (navigation), `changeId` (navigation) |
| Route | `/access-venue/live-gate-mode-lane-control-bo-230` |

#### Inputs: what the user enters or picks

**Sent by *Cancel gate mode change*** (`cancelGateModeChange`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 200 | — | — | `cancelGateModeChange` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every live gate mode** (data table, from `listLiveGateMode`)

| Shows | Format | Notes |
|---|---|---|
| Current mode | chip: Normal, Free flow, Drop arm, Closed, Podium, Maintenance | current mode |
| Target mode | chip: Normal, Free flow, Drop arm, Closed, Podium, Maintenance | Target mode of the pending `access.gate_mode_change`, if any; with operator, reason and effective time from the same row (decided 29 … |
| Operator | text | operator |
| Reason | text | reason |

**The selected live gate mode** (detail panel): The pack groups this record's detail under its own headings: “ENTRY”, “Available”, “Bulk Command”, “Optional”, “Emergency”.

| Shows | Format | Notes |
|---|---|---|
| Current mode | chip: Normal, Free flow, Drop arm, Closed, Podium, Maintenance | current mode |
| Target mode | chip: Normal, Free flow, Drop arm, Closed, Podium, Maintenance | Target mode of the pending `access.gate_mode_change`, if any; with operator, reason and effective time from the same row (decided 29 … |
| Operator | text | operator |
| Reason | text | reason |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cancel gate mode change (destructive button) | `cancelGateModeChange` POST `/gate-mode-changes/{changeId}/cancel` | inline | AccessGateModeChange | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `TURNSTILE_MODE_SET` |

**Data it reads**: `listLiveGateMode` (onLoad, Live Gate Mode & Lane Control); `listAccessPoints` (onLoad, The gates and lanes whose mode is set)

**Where the user goes next**

- → `BO-224` Live Access Operations Command Center: *Returns to the board's landing screen*; calls `listLiveGateMode`

**What opens over it**

- confirmDialog *Cancel gate mode change*: **Names what `cancelGateModeChange` changes and what it leaves alone**, in the consequence rather than the verb. A access gate mode change this affects should be identified in the dialog, not just counted. **Collects what `cancelGateModeChange` sends before it is called.** Nothing in the body is …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The live gate mode list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live gate mode untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live gate mode yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the live gate mode are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `not-pending`: the change is already applied or cancelled. |

#### Permissions

- `listLiveGateMode` → `SCOPE_VIEW` (read) · staff
- `setTurnstileMode` → `TURNSTILE_MODE_SET` (operate) · staff
- `listAccessPoints` → `SCOPE_VIEW` (read) · staff
- `cancelGateModeChange` → `TURNSTILE_MODE_SET` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.27 | The system should have the ability to customize / configure / manage software on turnstiles and making it behave differently depending on type of card used. There should be the possibility to add … | Admission and Access | CONTRACTED | `setTurnstileMode` |
| 3.2.28 | The system should support turnstiles of multiple sizes. For example, larger turnstiles for buggies. | Admission and Access | CONTRACTED | `setTurnstileMode` |
| 3.2.56 | It is expected to have the possibility to set the access control on Free spin mode, meaning that no ticket is read at access control point, still the turnstile shall be able to count how many times … | Admission and Access | CONTRACTED | `setTurnstileMode` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live operations dashboard: real-time attendance by venue and gate with each gate's online/offline status and entry count. Turnstile mode can be switched through the day (more entry gates in the morning, more exit in the evening). *(client request · MoM 2 Sep 2026, 4.15 Live Operations Dashboard · DI-648)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-230` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS26 Access Control Board 9.dc.html#bo-230`
- Workshop pack: Access Control Module_Reference.pdf board 9
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 12: Works in Live Gate Mode & Lane Control → Allow operations to change access-point modes during live operations without entering the Board 6 engineering configuration. Board 6 defines which modes a device can support. Board 9 controls which …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-230?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cancel gate mode change.
- [ ] Every transition is wired: `BO-224`.
- [ ] Every gated control is gated: `SCOPE_VIEW`, `TURNSTILE_MODE_SET`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-231` Queue, Throughput & Lane Optimization

**Manage entrance flow in real time. This addresses the matrix requirement to improve entrance flow and queuing, particularly for large B2B groups.**

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
| Route | `/access-venue/queue-throughput-lane-optimization-bo-231` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every queue throughput lane** (data table, from `listQueueThroughputLane`)

| Shows | Format | Notes |
|---|---|---|
| Lane type | chip: Standard, Family, Group B2B, Vip, Pod accessible, Re entry… | Lane type |

**The selected queue throughput lane** (detail panel): The pack groups this record's detail under its own headings: “Guests Waiting”, “Active Lanes”, “Current Throughput”, “Estimated Wait”, “Lane Performance”, “Reason”.

| Shows | Format | Notes |
|---|---|---|
| Lane type | chip: Standard, Family, Group B2B, Vip, Pod accessible, Re entry… | Lane type |

**Data it reads**: `listQueueThroughputLane` (onLoad, Queue, Throughput & Lane Optimization)

**Where the user goes next**

- → `BO-224` Live Access Operations Command Center: *Returns to the board's landing screen*; calls `listQueueThroughputLane`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The queue throughput lane list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the queue throughput lane untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No queue throughput lane yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the queue throughput lane are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listQueueThroughputLane` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Per-ride hourly capacity (e.g. 600/hour) split across express/fast-lane, virtual queue and walk-in (illustrative 75% general split walk-in/VQ, 25%/150 express); allocation adjusts dynamically if one lane is disproportionately busy. *(client request · MoM 7 Sep 2026, 4.12 Virtual Queue - Concept & Lane/Allocation Model · DI-674)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-231` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS26 Access Control Board 9.dc.html#bo-231`
- Workshop pack: Access Control Module_Reference.pdf board 9
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 14: Works in Queue, Throughput & Lane Optimization → Manage entrance flow in real time. This addresses the matrix requirement to improve entrance flow and queuing, particularly for large B2B groups.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-231?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-224`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-232` Operational Incident & Exception Workspace

**Manage access incidents that require more than a simple override.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `INCIDENT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/operational-incident-exception-workspace-bo-232` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Sent by *Save changes*** (`setOperationalIncidentException`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | text field | required | — | — | — | Venue | `setOperationalIncidentException` body |
| Incident `incidentId` | text field | required | — | — | — | Incident identifier | `setOperationalIncidentException` body |
| Types type `typesType` | select | required | — | Credential fraud · Duplicate use · Biometric mismatch · Lost wristband · Gate failure · Guest dispute · Child guardian issue · Group admission issue · Security event · Offline conflict · Partner ticket failure · Emergency access event | — | Vocabulary listed under Incident Types. | `setOperationalIncidentException` body |
| Assigned to `assignedTo` | radio group | optional | — | Access supervisor · Guest services · Security · Ticketing · Technical support | — | Team the incident is assigned to | `setOperationalIncidentException` body |
| Ticket `ticketId` | text field | optional | — | — | — | Ticket or credential concerned | `setOperationalIncidentException` body |
| Description `description` | text area | optional | — | — | — | What happened | `setOperationalIncidentException` body |
| Status `status` | radio group | optional | — | Open · Investigating · Resolved · Closed | — | Incident status | `setOperationalIncidentException` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | `setOperationalIncidentException` PUT `/operational-incident-exception` | OperationalIncidentExceptionWorkspaceInput | OperationalIncidentExceptionWorkspaceView | — | gated `INCIDENT_MANAGE` |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-224` Live Access Operations Command Center: *Returns to the board's landing screen*; calls `setOperationalIncidentException`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operational incident exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operational incident exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operational incident exception yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operational incident exception are still there. The pack's own statuses are Open → Investigating → Resolved → Closed — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission, **INCIDENT_MANAGE** (was ACCESS_POINT_CONFIGURE until 29 September, K1: investigating, assigning and closing an incident is incident management, as for F&B and maintenance incidents). Never an empty table. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setOperationalIncidentException` → `INCIDENT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission, **INCIDENT_MANAGE** (was ACCESS_POINT_CONFIGURE until 29 September, K1: investigating, assigning and closing an incident is incident management, as for F&B and maintenance incidents). Never an empty table.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-232` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS26 Access Control Board 9.dc.html#bo-232`
- Workshop pack: Access Control Module_Reference.pdf board 9
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 16: Works in Operational Incident & Exception Workspace → Manage access incidents that require more than a simple override.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-232?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-224`.
- [ ] Every gated control is gated: `INCIDENT_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-233` Operations Audit, Shift Handover & Control Summary

**Provide full accountability for everything operators and supervisors changed during live access operations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AUDIT_VIEW`, `TURNSTILE_MODE_SET` (1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `shiftId` (navigation) |
| Route | `/access-venue/operations-audit-shift-handover-control-summary-bo-233` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Form: End podium shift** (modal, opened by *End podium shift*; *End podium shift* calls `endPodiumShift`, *Cancel* sends nothing)

**Collects what `endPodiumShift` sends before it is called.** Nothing in the body is required. Optional: `handoverNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Handover note `handoverNote` | text area | optional | — | max length 1000 | — | — | `endPodiumShift` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `shift-ended`: the shift is already ended.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Operations Audit, Shift Handover & Control (primary button) | navigation or local | — | — | — | — |
| End podium shift (secondary button) | `endPodiumShift` POST `/podium-shifts/{shiftId}/end` | inline | AccessPodiumShift | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `TURNSTILE_MODE_SET`; opens modal first |

**Data it reads**: `listShiftHandoverSummary` (onLoad, Operations Audit, Shift Handover & Control Summary)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operations audit shift list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operations audit shift untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operations audit shift yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operations audit shift are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `shift-ended`: the shift is already ended. |

#### Permissions

- `listShiftHandoverSummary` → `AUDIT_VIEW` (read) · staff
- `endPodiumShift` → `TURNSTILE_MODE_SET` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-233` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS26 Access Control Board 9.dc.html#bo-233`
- Workshop pack: Access Control Module_Reference.pdf board 9
- Flow F119 *Access Control board 9: Live Access Operations Command Center*, step 18: Works in Operations Audit, Shift Handover & Control Summary → Provide full accountability for everything operators and supervisors changed during live access operations.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-233?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Operations Audit, Shift Handover & …, End podium shift.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `AUDIT_VIEW`, `TURNSTILE_MODE_SET`.
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

**9 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cancelGateModeChange": {"method":"POST","path":"/gate-mode-changes/{changeId}/cancel","contract":"access","summary":"Cancel a scheduled gate mode change","permission":"TURNSTILE_MODE_SET","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessGateModeChange"},
"deletePodium": {"method":"DELETE","path":"/podiums/{podiumId}","contract":"access","summary":"Delete a podium","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"deleteReasonCode": {"method":"DELETE","path":"/reason-codes/{reasonCodeId}","contract":"access","summary":"Delete a validation reason code","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"endPodiumShift": {"method":"POST","path":"/podium-shifts/{shiftId}/end","contract":"access","summary":"End an operator shift on a podium","permission":"TURNSTILE_MODE_SET","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessPodiumShift"},
"listAccessPoints": {"method":"GET","path":"/access-points","contract":"access","summary":"List access points","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialDisableBlacklist": {"method":"GET","path":"/credential-disable-blacklist","contract":"access","summary":"Credential Disable, Blacklist & Whitelist Operations","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listLiveAccess": {"method":"GET","path":"/live-access","contract":"access","summary":"Live Access Operations Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listLiveGateMode": {"method":"GET","path":"/live-gate-mode","contract":"access","summary":"Live Gate Mode & Lane Control","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPodiumConsole": {"method":"GET","path":"/podium-console","contract":"access","summary":"Podium Operations Console","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PodiumOperationsConsoleView"},
"listQueueThroughputLane": {"method":"GET","path":"/queue-throughput-lane","contract":"access","summary":"Queue, Throughput & Lane Optimization","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listShiftHandoverSummary": {"method":"GET","path":"/shift-handover-summary","contract":"access","summary":"Operations Audit, Shift Handover & Control Summary","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTicketCredentialInvestigation": {"method":"GET","path":"/ticket-credential-investigation","contract":"access","summary":"Ticket & Credential Investigation Console","permission":"TICKET_LOOKUP","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"ticketId","in":"query","required":false},{"name":"qr","in":"query","required":false},{"name":"barcode","in":"query","required":false},{"name":"rfid","in":"query","required":false},{"name":"nfc","in":"query","required":false},{"name":"virtualCredentialId","in":"query","required":false},{"name":"orderNumber","in":"query","required":false},{"name":"membership","in":"query","required":false},{"name":"guestName","in":"query","required":false},{"name":"email","in":"query","required":false},{"name":"mobile","in":"query","required":false},{"name":"externalPartnerReference","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listValidationExceptionReason": {"method":"GET","path":"/validation-exception-reason","contract":"access","summary":"Validation Exception & Reason Code Manager","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationExceptionReasonCodeManagerView"},
"overrideAccess": {"method":"POST","path":"/access/override","contract":"access","summary":"Admit against a failed validation","permission":"ACCESS_OVERRIDE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationResult"},
"setOperationalIncidentException": {"method":"PUT","path":"/operational-incident-exception","contract":"access","summary":"Operational Incident & Exception Workspace","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OperationalIncidentExceptionWorkspaceInput","responds":"OperationalIncidentExceptionWorkspaceView"},
"setPodium": {"method":"PUT","path":"/podiums","contract":"access","summary":"Create or replace a podium","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessPodium","responds":"AccessPodium"},
"setReasonCode": {"method":"PUT","path":"/reason-codes","contract":"access","summary":"Create or replace a validation reason code","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessReasonCode","responds":"AccessReasonCode"},
"setTurnstileMode": {"method":"PUT","path":"/access-points/{accessPointId}/mode","contract":"access","summary":"Set the operating mode of an access point","permission":"TURNSTILE_MODE_SET","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessPoint"},
"startPodiumShift": {"method":"POST","path":"/podiums/{podiumId}/shifts","contract":"access","summary":"Start an operator shift on a podium","permission":"TURNSTILE_MODE_SET","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessPodiumShift"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessGateModeChange": {"type":"object","x-ticvai-persistence":"access.gate_mode_change","description":"One gate mode change on an access point, pending or applied: from and target mode, operator, reason and effective time. Append-only history (declared 29 September, data-model close-out DM1) Written by setTurnstileMode (applied at once, or pending until a future effectiveAt) and cancelGateModeChange; a timer applies a pending change at its effective time (decided 29 September, writers pass).","required":["id","venueId","accessPointId","targetMode","status","changedByPrincipalId","changedAt","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid"},"fromMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"nullable":true},"targetMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}]},"status":{"type":"string","enum":["pending","applied","cancelled"]},"reason":{"type":"string","maxLength":500,"nullable":true},"effectiveAt":{"type":"string","format":"date-time","nullable":true},"changedByPrincipalId":{"type":"string","format":"uuid","description":"Operator"},"changedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"}}},
"AccessPodium": {"type":"object","x-ticvai-persistence":"access.podium","description":"One podium: an attendant interface in a venue that controls one or more access points (declared 29 September, data-model close-out DM1)","required":["id","venueId","podiumType","name","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"podiumType":{"type":"string","enum":["physicalControlPanel","tablet","workstation","handheld","other"]},"name":{"type":"string","description":"e.g. Main Entrance A"},"accessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Gates this podium controls"},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessPodiumShift": {"type":"object","x-ticvai-persistence":"access.podium_shift","description":"One operator session on a podium or device: who, in what role, where, and login and logout times. Logout is null while the shift is open (declared 29 September, data-model close-out DM1) Written by startPodiumShift and endPodiumShift; an identity sign-out ends the open shift (decided 29 September, writers pass).","required":["id","venueId","operatorPrincipalId","loginAt","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid"},"role":{"type":"string","nullable":true},"podiumId":{"type":"string","format":"uuid","nullable":true},"accessDeviceId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"platform.device","description":"Device used, from the one device register (platform.device, ADR-0067)"},"loginAt":{"type":"string","format":"date-time"},"logoutAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"}}},
"AccessPoint": {"x-ticvai-persistence":"access.access_point","type":"object","required":["id","code","name","venueId","operatingMode","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"externalCredentialSources":{"allOf":[{"$ref":"#/components/schemas/ExternalCredentialSourceList"}],"description":"BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"},"scanAnomalyRules":{"allOf":[{"$ref":"#/components/schemas/ScanAnomalyRuleList"}],"description":"BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"},"operatingMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"default":"normal","description":"**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"},"vehicleLocationCapture":{"type":"boolean","default":false,"description":"BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"},"mode":{"allOf":[{"$ref":"#/components/schemas/TurnstileMode"}],"nullable":true,"description":"Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"},"direction":{"allOf":[{"$ref":"#/components/schemas/Direction"}],"description":"**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n"},"antiPassbackEnabled":{"type":"boolean"},"requiresExitBeforeReentry":{"type":"boolean","default":false,"description":"Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."},"driver":{"type":"string","nullable":true,"description":"Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"},"geofence":{"allOf":[{"$ref":"#/components/schemas/AccessPointGeofence"}],"nullable":true,"description":"Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"},"isActive":{"type":"boolean"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true}}},
"AccessPointGeofence": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n","required":["enforcement"],"properties":{"latitude":{"type":"number"},"longitude":{"type":"number"},"radiusMetres":{"type":"integer","minimum":5,"maximum":5000},"enforcement":{"type":"string","enum":["off","warn","deny"],"description":"`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"},"allowProximityBeacon":{"type":"boolean","description":"Accept a BLE proximity assertion in place of GPS. Better indoors."}}},
"AccessPointOperatingMode": {"type":"string","description":"BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"]},
"AccessReasonCode": {"type":"object","x-ticvai-persistence":"access.reason_code","description":"One validation reason code in the catalogue: its name, guest and operator messages, the configured operational response and a follow-up hint (declared 29 September, data-model close-out DM1)","required":["id","code","name","operationalResponse","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Null for a tenant-wide code"},"code":{"type":"string","maxLength":32,"description":"e.g. AC-002"},"name":{"type":"string","description":"e.g. Wrong Visit Date"},"guestMessage":{"type":"string","nullable":true},"operatorMessage":{"type":"string","nullable":true},"operationalResponse":{"type":"string","enum":["deny","operatorReview","supervisorRequired","allowWithWarning"]},"followUpAction":{"type":"string","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CredentialDisableBlacklistWhitelistOperationsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Disable, Blacklist & Whitelist Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"entryId":{"type":"string","description":"List entry identifier"},"reason":{"type":"string","enum":["lostTicket","stolenCredential","fraudSuspected","guestRemoval","securityIncident","duplicateCredential","managementInstruction","other"],"description":"Reason"},"disableScope":{"type":"string","enum":["entireCredential","venueAccess","attractionAccess","reEntry","fastPass","specificEntitlement"],"description":"What is disabled"},"durationType":{"type":"string","enum":["permanent","untilEndOfDay","untilDateTime","untilManuallyRestored"],"description":"How long the restriction lasts"},"distributedTo":{"type":"array","items":{"type":"string","enum":["centralPlatform","venueEdge","onlineGates","offlineRevocationPackage"]},"description":"Where the restriction has been distributed"},"credentialId":{"type":"string","description":"Credential"},"listType":{"type":"string","enum":["blacklist","whitelist"],"description":"Blacklist or approved whitelist exception"},"until":{"type":"string","format":"date-time","description":"End of restriction when durationType is untilDateTime"},"createdBy":{"type":"string","description":"Who applied it"},"createdAt":{"type":"string","format":"date-time","description":"When it was applied"}},"required":["entryId"]},
"DenyReason": {"type":"string","description":"Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n","enum":["notFound","notYetValid","expired","alreadyUsed","reentryLimitReached","exitRequiredBeforeReentry","wrongAccessPoint","wrongPerformance","outsideAdmissionWindow","entitlementSuspended","blacklisted","capacityReached","waiverRequired","accompanimentRequired","mediaDeactivated","unpaid","delegatedRightExhausted","delegatedRightRevoked","journeyNotCovered"]},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"ExternalCredentialSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["hotelRoomCard","corporateBadge","cityPass","transitCard","partnerToken"]},"providerName":{"type":"string"},"endpoint":{"type":"string"},"credentialRef":{"type":"string"},"grantsProductId":{"type":"string","format":"uuid"}}}},
"LiveAccessOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Live Access Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"accessPointId":{"type":"string","description":"Gate"},"name":{"type":"string","description":"Gate name"},"mode":{"type":"string","description":"Current gate mode"},"status":{"type":"string","enum":["online","offline","degraded"],"description":"Gate status"},"queueLevel":{"type":"string","enum":["low","moderate","high"],"description":"Queue level"},"throughputPerMinute":{"type":"number","description":"Guests per minute at this gate"},"lastScanAt":{"type":"string","format":"date-time","description":"Last scan"},"validPercent":{"type":"number","description":"Valid scans percentage"},"yellowPercent":{"type":"number","description":"Intervention scans percentage"},"rejectedPercent":{"type":"number","description":"Rejected scans percentage"}},"required":["accessPointId"]},
"LiveAccessOperationsCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"guestsEnteredToday":{"type":"integer","description":"Guests Entered Today"},"guestsExited":{"type":"integer","description":"Guests Exited"},"guestsCurrentlyInPark":{"type":"integer","description":"Guests Currently In Park"},"validScans":{"type":"integer","description":"Valid Scans"},"rejectedScans":{"type":"integer","description":"Rejected Scans"},"yellowInterventionScans":{"type":"integer","description":"Yellow / Intervention Scans"},"overrides":{"type":"integer","description":"Overrides"},"activeGates":{"type":"integer","description":"Active Gates"},"offlineGates":{"type":"integer","description":"Offline Gates"},"averageValidationTime":{"type":"number","description":"Average validation time in seconds"},"guestsMinute":{"type":"number","description":"Guests per minute"},"activeOperationalAlerts":{"type":"integer","description":"Active Operational Alerts"}}},
"LiveGateModeLaneControlView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Live Gate Mode & Lane Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"accessPointId":{"type":"string","description":"Gate"},"availableModes":{"type":"array","items":{"type":"string","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"]},"description":"Operating modes this gate permits, in the AccessPointOperatingMode vocabulary (R221): derived at read time from `access.device_configuration.permittedOperatingModes` of the devices at the gate, the modes every one of them permits (decided 29 September, writers pass)"},"currentMode":{"type":"string","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"],"description":"current mode"},"targetMode":{"type":"string","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"],"description":"Target mode of the pending `access.gate_mode_change`, if any; with operator, reason and effective time from the same row (decided 29 September, writers pass)"},"operator":{"type":"string","description":"operator"},"reason":{"type":"string","description":"reason"},"effectiveTime":{"type":"string","format":"date-time","description":"effective time"}},"required":["accessPointId"]},
"OperationalIncidentExceptionWorkspaceInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Operational Incident & Exception Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"venueId":{"type":"string","description":"Venue"},"incidentId":{"type":"string","description":"Incident identifier"},"typesType":{"type":"string","enum":["credentialFraud","duplicateUse","biometricMismatch","lostWristband","gateFailure","guestDispute","childGuardianIssue","groupAdmissionIssue","securityEvent","offlineConflict","partnerTicketFailure","emergencyAccessEvent"],"description":"Vocabulary listed under Incident Types."},"assignedTo":{"type":"string","enum":["accessSupervisor","guestServices","security","ticketing","technicalSupport"],"description":"Team the incident is assigned to"},"ticketId":{"type":"string","description":"Ticket or credential concerned"},"description":{"type":"string","description":"What happened"},"status":{"type":"string","enum":["open","investigating","resolved","closed"],"description":"Incident status"}},"required":["incidentId","venueId","typesType"]},
"OperationalIncidentExceptionWorkspaceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Operational Incident & Exception Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string","description":"Venue"},"incidentId":{"type":"string","description":"Incident identifier"},"typesType":{"type":"string","enum":["credentialFraud","duplicateUse","biometricMismatch","lostWristband","gateFailure","guestDispute","childGuardianIssue","groupAdmissionIssue","securityEvent","offlineConflict","partnerTicketFailure","emergencyAccessEvent"],"description":"Vocabulary listed under Incident Types."},"assignedTo":{"type":"string","enum":["accessSupervisor","guestServices","security","ticketing","technicalSupport"],"description":"Team the incident is assigned to"},"ticketId":{"type":"string","description":"Ticket or credential concerned"},"description":{"type":"string","description":"What happened"},"status":{"type":"string","enum":["open","investigating","resolved","closed"],"description":"Incident status"}},"required":["incidentId","venueId","typesType"]},
"OperationsAuditShiftHandoverControlSummaryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Operations Audit, Shift Handover & Control Summary displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"shiftId":{"type":"string","description":"Shift identifier"},"operator":{"type":"string","description":"Operator"},"role":{"type":"string","description":"Role"},"podium":{"type":"string","description":"Podium"},"device":{"type":"string","description":"Device"},"login":{"type":"string","format":"date-time","description":"Login"},"logout":{"type":"string","format":"date-time","description":"Logout"},"ticketLookups":{"type":"integer","description":"Ticket lookups"},"overrides":{"type":"integer","description":"Overrides"},"manualOpenings":{"type":"integer","description":"Manual openings"},"modeChanges":{"type":"integer","description":"Mode changes"},"credentialDisables":{"type":"integer","description":"Credential disables"},"blacklistChanges":{"type":"integer","description":"Blacklist changes"},"groupAdjustments":{"type":"integer","description":"Group adjustments"},"incidents":{"type":"integer","description":"incidents"}},"required":["shiftId","operator"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PodiumOperationsConsoleView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Podium Operations Console displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"podiumId":{"type":"string","description":"Podium identifier"},"podiumType":{"type":"string","enum":["physicalControlPanel","tablet","workstation","handheld","other"],"description":"Kind of podium interface"},"name":{"type":"string","description":"Podium name, e.g. Main Entrance A"},"accessPointIds":{"type":"array","items":{"type":"string"},"description":"Gates this podium controls"},"operatorId":{"type":"string","description":"Operator on shift"},"shiftStart":{"type":"string","format":"date-time","description":"Shift start"},"shiftEnd":{"type":"string","format":"date-time","description":"Shift end"}},"required":["podiumId"]},
"QueueThroughputLaneOptimizationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Queue, Throughput & Lane Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"accessPointId":{"type":"string","description":"Lane / gate"},"laneType":{"type":"string","enum":["standard","family","groupB2b","vip","podAccessible","reEntry","fastPass"],"description":"Lane type"},"guestsPerMinute":{"type":"number","description":"Guests per minute"},"rejectPercent":{"type":"number","description":"Reject percentage"},"status":{"type":"string","enum":["healthy","investigate"],"description":"Lane status"}},"required":["accessPointId"]},
"QueueThroughputLaneOptimizationViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"guestsWaiting":{"type":"integer","description":"Guests Waiting (the pack shows 486)"},"activeLanes":{"type":"integer","description":"Active Lanes (the pack shows 12 / 16)"},"lanesTotal":{"type":"integer","description":"Total lanes"},"throughputPer10Min":{"type":"integer","description":"Guests admitted in the last 10 minutes"},"estimatedWaitMinutes":{"type":"integer","description":"Estimated wait"}}},
"ScanAnomalyRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n","items":{"type":"object","properties":{"rule":{"type":"string","enum":["simultaneousEntry","impossibleTravelTime","rapidReentry","sharedDevice","velocityBreach"]},"action":{"type":"string","enum":["log","flag","requireSupervisor","deny"]},"thresholdSeconds":{"type":"integer","nullable":true}}}},
"ScanOutcome": {"type":"string","enum":["admitted","denied","overridden"]},
"TicketCredentialInvestigationConsoleView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Ticket & Credential Investigation Console displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ticketId":{"type":"string","description":"Ticket"},"transactionTime":{"type":"string","format":"date-time","description":"Transaction time"},"salesChannel":{"type":"string","description":"Sales channel"},"pos":{"type":"string","description":"POS"},"clerk":{"type":"string","description":"Clerk"},"paymentReference":{"type":"string","description":"Payment reference"},"paymentMethod":{"type":"string","description":"Payment method"},"guestName":{"type":"string","description":"Guest"},"visitDate":{"type":"string","format":"date","description":"Visit date"},"firstEntryAt":{"type":"string","format":"date-time","description":"First entry"},"reEntriesRemaining":{"type":"integer","description":"Re-entries remaining"},"verificationMethod":{"type":"string","description":"Verification method, e.g. dynamic QR locked"}},"required":["ticketId"]},
"TicketStatus": {"x-ticvai-persistence":"none — computed from entitlement and scans","description":"**A validation result, not a lifecycle**, despite the name. Computed at scan time from the entitlement and its scan history — `isValid`, `entriesUsed`, `isInsideVenue`.\n**The name misled a state model into anchoring on it** (`states/entitlement.yaml`, removed 18 August): six lifecycle states were checked against an object with no values, and `check-states` warned about it for a day before anyone read the schema.\nThe entitlement's lifecycle is `orders.EntitlementStatus`. **This is what a gate learns when it scans**, which is a different question with a similar name.\n","type":"object","required":["ticketId","isValid"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"Stable for the life of the ticket, independent of the media carrying it."},"mediaCode":{"type":"string","nullable":true},"productName":{"type":"string"},"holderName":{"type":"string","nullable":true,"description":"Present only where the entitlement is name-bound. Identity and entitlement are separate concerns; most entitlements carry no holder.\n"},"isValid":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited."},"reentryAllowed":{"type":"boolean"},"isInsideVenue":{"type":"boolean","description":"Derived from the last scan. Drives anti-passback evaluation."},"issuingCellId":{"type":"string","nullable":true,"description":"Present when this entitlement was issued in a different cell and is being redeemed here as a delegated right (ADR-0010). Null for locally issued tickets.\n"},"guestLinkId":{"type":"string","nullable":true,"description":"Pseudonymous cross-region guest reference. Present only on delegated rights. Carries no personal data.\n"},"admissionRulesId":{"type":"string","format":"uuid"},"denyReason":{"$ref":"#/components/schemas/DenyReason"}}},
"TurnstileMode": {"type":"string","description":"**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n","enum":["freeRotation","closed"]},
"ValidationExceptionReasonCodeManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Validation Exception & Reason Code Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"reasonCode":{"type":"string","description":"Reason code, e.g. AC-002"},"operationalResponse":{"type":"string","enum":["deny","operatorReview","supervisorRequired","allowWithWarning"],"description":"Configured response when this reason occurs"},"name":{"type":"string","description":"Reason, e.g. Wrong Visit Date"},"guestMessage":{"type":"string","description":"Message shown to the guest"},"operatorMessage":{"type":"string","description":"Message shown to the operator"},"followUpAction":{"type":"string","description":"Suggested operator follow-up, e.g. check reschedule eligibility"}},"required":["reasonCode"]},
"ValidationResult": {"x-ticvai-persistence":"none — computed, persisted as scan_event","type":"object","required":["scanId","outcome","accessPointId","recordedAt"],"properties":{"scanId":{"type":"string","format":"uuid"},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"denyDetail":{"type":"string","description":"Human-readable, localised. For operator display, never for logic."},"accessPointId":{"type":"string","format":"uuid"},"ticket":{"$ref":"#/components/schemas/TicketStatus"},"admittedCount":{"type":"integer","description":"Holders admitted on this read. Differs from groupSize on partial admission."},"recordedAt":{"type":"string","format":"date-time"},"serverEvaluatedAt":{"type":"string","format":"date-time"},"advisory":{"type":"object","nullable":true,"description":"BL-179, CF-130. **What a device observed, for the steward, never for the gate.** Present only where an access point's device reports the matching `DeviceCapability` and the venue has turned the corresponding setting on.\n**Never persisted.** This schema is computed and stored as `access.scan_event`, and the advisory is deliberately not part of what is stored: an inferred classification kept against a guest is sensitive personal data with no consent behind it. **A guest agreed to be admitted, not to be classified** — Face Pass and Face Tag carry `consent_purpose_id` and `consent_given_at` because somebody enrolled, and nobody enrols in being looked at by a turnstile. `scan_event` records that an override happened and never what the device thought, which keeps `overrideRateAlertThreshold` working without building a register nobody agreed to.\n**It cannot reach `outcome` or `denyReason`.** Those are decisive and `entitlementGated` is `true` and read-only: the gate admits on the entitlement, and everything here sits on top of that without replacing any of it.\n","properties":{"genderClassification":{"type":"string","enum":["women","men","undetermined"],"description":"**`undetermined` is a real answer and the most common one to design for.** A classifier that never returns it is one that has been tuned to look confident.\n"},"confidence":{"type":"number","minimum":0,"maximum":1,"description":"**Required reading for the steward, not decoration.** An advisory with no confidence is read as a fact, and `overrideRateAlertThreshold` exists to catch exactly the failure that produces — *an override rate near zero means the steward has stopped deciding.* That number only means anything if the steward could see how sure the device was.\n"},"reportedByDeviceId":{"type":"string","format":"uuid","description":"**Which device said it.** A classifier that degrades is one camera, not a venue, and an advisory nobody can trace to hardware cannot be investigated or switched off alone.\n"}}}}}
}
```
