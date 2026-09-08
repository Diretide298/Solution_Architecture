# ADR-0041: A command centre is a saved dashboard, not a screen

**Status:** Accepted
**Date:** 8 September 2026
**Amends:** [ADR-0028](0028-service-decomposition.md) — no schema moves; 57 screens become rows in `reporting.dashboard`
**Raises:** **CF-169** — the authoring screens this decision needs, and a dashboard that cannot be deleted

---

## Context

**Fifty-seven screens across five platforms are named "Command Center", and fifty-seven of them
are the same screen.** Every one uses the layout `dashboard` with `dataTable` and `metricTile`,
and nothing else:

| Platform | Command centres |
|---|---:|
| P09 platform admin console | 26 |
| P08 venue back office | 22 |
| P13 white label CMS | 4 |
| P10 partner reseller portal | 3 |
| P12 support agent console | 2 |

**The ids give away where they came from.** On P08 the gap between consecutive command centres is
**exactly ten, every time** — `BO-144`, `BO-154`, `BO-164`, `BO-174`, `BO-184`, `BO-194` — and on
P09 it is ten or twenty. A generator emitted a block of ten screens per sub-domain and headed each
block with a dashboard. **Nobody decided that a venue needs twenty-two access dashboards.**

**Four other screens carry the name and are not this**, and they stay as they are:
`EMP-051` and `EMP-061` are `list`, `KIT-001` is `board`, `ANL-001` is a genuine single dashboard.

### The model this decision needs already exists

**Nothing here is new work in the schema or the contract.** Measured on 8 September:

| | |
|---|---|
| `reporting.dashboard` | 8 columns — *"an arrangement of tiles, each resolving its own source"* |
| `reporting.dashboard_tile` | 8 columns — *"one panel, and the query behind it"* |
| Operations | `listDashboards`, `createDashboard`, `getDashboard`, `updateDashboard` |
| `CreateDashboardRequest.tiles` | array, `minItems: 1`, `maxItems: 24` |
| Screens that author a dashboard | **0** |

Searching all 1,091 screen names for `widget`, `saved view`, `drag`, `layout editor`,
`add a tile` returns **nothing**. **Somebody modelled user-configured dashboards, gave them an
API, and no screen was ever written.**

---

## Decision

**A command centre is a row in `reporting.dashboard` with tiles in `reporting.dashboard_tile`.
The 57 screens are deleted from `screens/` and seeded as data.**

A tile already carries what a command centre needs: `title`, `report_id`, `visualisation`,
`parameters`, `refresh_seconds` and a jsonb `position`. A dashboard carries `name`, `venue_id`,
`is_shared` and `owner_principal_id` — so the same mechanism serves a seeded platform dashboard
and one a venue manager builds on a Tuesday.

### Three sections replace fifty-seven screens

**1. Command Centre — one screen, scoped by entitlement.** Every screen in the package already
carries `requiresModule`; the 57 resolve to `ticketing` 19, `access` 15, `marketing` 12, `core` 6,
`partner` 3, `membership` 2. **A tenant holding F&B, Retail and Ticketing already resolves to their
subset without anything being built** — the entitlement is not new, only its use here is.

**2. Reporting and AI analytics — already built.** `BO-058 Reporting Home`, `BO-029 Report
Builder`, `BO-059 Sales Reports`, `BO-061 Scheduled Reports`, and eleven AI analytics screens.
Behind them `report_definition`, `report_column`, `report_filter`, `report_parameter`, `schedule`,
`schedule_recipient`, `execution`, `export`. `report_definition`'s own note states the boundary
this decision relies on: ***"A saved question, not its answer."***

**3. Board customisation — the part that must be built.** Add a tile, bind it to a saved report,
choose a visualisation, set parameters and a refresh, place it. **Three or four screens**, listed
in CF-169.

---

## Consequences

**The screen estate shrinks by 57.** P08 goes 363 → **341**, P09 318 → **292**. Those two
platforms are the whole of the board gap, so this is the cheapest 57 screens anyone will remove.

**It removes most of the largest drawing job.** `BP-003` in the board plan — `dashboard` with
`dataTable` and `metricTile`, 115 screens — is mostly these. Drawing one configurable dashboard
replaces drawing it 57 times, and the remainder of BP-003 is genuine.

**🔴 The cost columns are a warning nobody has acted on.** `reporting.dashboard.aggregate_cost` and
`reporting.report_definition.estimated_cost` exist because somebody foresaw a user assembling an
expensive board. **The editor has to surface both**, or the first shared dashboard with twenty-four
tiles on a five-second refresh is a performance incident with a person's name on it. `maxItems: 24`
is a bound on tiles, not on cost.

**🔴 A dashboard cannot be deleted.** There is `list`, `create`, `get` and `update` and no
`deleteDashboard`. A screen that lets people create things and never remove them accumulates until
somebody asks for a migration. Raised in CF-169 rather than added by inference, because a soft
delete and a hard delete are different answers where `is_shared` is true.

**Seeding is a migration, and it is the honest cost of this decision.** Fifty-seven dashboards,
each with its tiles bound to real `report_definition` rows. **Where a command centre's tiles have
no saved report behind them, this decision exposes that rather than causes it** — the screen was
asserting a dashboard that nothing could populate either way.

**Two of the 57 already have boards drawn.** Retiring them loses that design, which is a small
real cost against 55 that were never drawn.

**A generator that emits one dashboard per ten screens is still running.** Nothing here stops it.
Unless the generator is changed, the next pack reintroduces the pattern — which is the argument for
the CI check in the board plan that fails an unauthored layout rather than defaulting it.

---

## When this is reopened

**A command centre that cannot be expressed as tiles over saved reports.** If one needs a bespoke
visualisation the tile model has no room for, that is a real screen and should be written as one —
the test is whether `visualisation` and `parameters` can carry it.

**A tenant who wants a dashboard nobody may edit.** `is_shared` and `owner_principal_id` express
ownership, not immutability. A locked corporate dashboard is a permission this model does not have.

---

## Alternatives considered

**Draw all 57.** Rejected. It is 57 boards for one layout, and it leaves the configurable dashboard
the schema already describes still unbuilt — so the same work returns the first time a venue asks
for a view nobody anticipated.

**Delete them and offer nothing.** Rejected. The navigation would lose its entry points and the
seeded dashboards are what makes the deletion invisible to a user.

**Keep them as screens and add customisation beside them.** Rejected as the most expensive option:
two mechanisms for one thing, and a guaranteed disagreement between a hand-specified command centre
and the configurable one that shows the same numbers.

**Generate the 57 from the tile model at build time.** Rejected. It keeps the screen count and the
maintenance while adding a generator — the count is the thing worth removing.
