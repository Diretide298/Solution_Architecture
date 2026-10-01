# P09-infrastructure-resilienc-01 — P09 · Infrastructure & Resilience

**4 screens · 4 operations · 3 schemas · 2 permissions**

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

## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `ADM-014` | Auto-Scaling Configuration | B–D | 0 | 52 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-030` | Infrastructure Sizing & Scaling Policy | B–D | 8 | 52 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-033` | Backup & DR Status | B–D | 0 | 54 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-034` | Archival Job Monitor | B–D | 0 | 54 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-014` Auto-Scaling Configuration

**Change how auto-scaling behaves here, and see which level the current value came from.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Infrastructure & Resilience · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_CELL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getCellCapacity` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/auto-scaling-configuration` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — infrastructure, Terraform not API

#### Inputs: what the user enters or picks

**Form: Decommission cell** (modal, opened by *Decommission cell*; *Decommission cell* calls `decommissionCell`, *Cancel* sends nothing)

**Collects what `decommissionCell` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

`decommissionCell` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Save cell tier** (modal, opened by *Save cell tier*; *Save cell tier* calls `updateCellTier`, *Cancel* sends nothing)

**Collects what `updateCellTier` sends before it is called.** Required: `tier`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.

`updateCellTier` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every cell job** (data table, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellJob.id` |
| Kind | text | not in the schema: `CellJob.kind` |
| Status | text | not in the schema: `CellJob.status` |
| Progress percent | text | not in the schema: `CellJob.progressPercent` |
| Message | text | not in the schema: `CellJob.message` |
| Error | text | not in the schema: `CellJob.error` |
| Scheduled for | text | not in the schema: `CellJob.scheduledFor` |
| Completed at | text | not in the schema: `CellJob.completedAt` |

**The selected cell job** (detail panel, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellJob.id` |
| Kind | text | not in the schema: `CellJob.kind` |
| Status | text | not in the schema: `CellJob.status` |
| Progress percent | text | not in the schema: `CellJob.progressPercent` |
| Message | text | not in the schema: `CellJob.message` |
| Error | text | not in the schema: `CellJob.error` |
| Scheduled for | text | not in the schema: `CellJob.scheduledFor` |
| Completed at | text | not in the schema: `CellJob.completedAt` |

**The cell** (detail panel, from `getCell`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellDetail.id` |
| Name | text | not in the schema: `CellDetail.name` |
| Kind | text | not in the schema: `CellDetail.kind` |
| Cluster ID | text | not in the schema: `CellDetail.clusterId` |
| Is reachable | text | not in the schema: `CellDetail.isReachable` |
| Last contact at | text | not in the schema: `CellDetail.lastContactAt` |
| Licence expires at | text | not in the schema: `CellDetail.licenceExpiresAt` |
| Participates in cross cell | text | not in the schema: `CellDetail.participatesInCrossCell` |
| Region ID | text | not in the schema: `CellDetail.regionId` |
| Region name | text | not in the schema: `CellDetail.regionName` |
| Country code | text | not in the schema: `CellDetail.countryCode` |
| Tier | text | not in the schema: `CellDetail.tier` |
| Status | text | not in the schema: `CellDetail.status` |
| Cloud provider | text | not in the schema: `CellDetail.cloudProvider` |
| Cloud region | text | not in the schema: `CellDetail.cloudRegion` |
| API endpoint | text | not in the schema: `CellDetail.apiEndpoint` |

**The cell health** (detail panel, from `getCellHealth`)

| Shows | Format | Notes |
|---|---|---|
| Is healthy | text | not in the schema: `CellHealth.isHealthy` |
| Is schema behind | text | not in the schema: `CellHealth.isSchemaBehind` |
| Database status | text | not in the schema: `CellHealth.databaseStatus` |
| Replication lag seconds | text | not in the schema: `CellHealth.replicationLagSeconds` |
| Last backup at | text | not in the schema: `CellHealth.lastBackupAt` |
| Last restore drill at | text | not in the schema: `CellHealth.lastRestoreDrillAt` |
| Checked at | text | not in the schema: `CellHealth.checkedAt` |

**The scaling policy** (detail panel, from `getScalingPolicy`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Service | text | — |
| Replica floor | 1,234 | — |
| Replica ceiling | 1,234 | Null means no maximum, which is the correct setting for a burst cell. |
| Target utilisation pct | 1,234 | — |
| Scale step pct | 1,234 | — |

**The cell capacity** (detail panel, from `getCellCapacity`)

| Shows | Format | Notes |
|---|---|---|
| Kind | text | not in the schema: `CellCapacity.kind` |
| Tenant count | text | not in the schema: `CellCapacity.tenantCount` |
| Is constrained | text | not in the schema: `CellCapacity.isConstrained` |
| Constrained dimension | text | not in the schema: `CellCapacity.constrainedDimension` |
| Dimensions | text | not in the schema: `CellCapacity.dimensions` |
| Forecast breach at | text | not in the schema: `CellCapacity.forecastBreachAt` |
| Measured at | text | not in the schema: `CellCapacity.measuredAt` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cancel decommission (destructive button) | `cancelDecommission` (not in any contract) | — | — | — | — |
| Decommission cell (secondary button) | `decommissionCell` (not in any contract) | — | — | — | — |
| Save cell tier (secondary button) | `updateCellTier` (not in any contract) | — | — | — | — |

**Data it reads**: `getCellCapacity` (onLoad, Load against headroom); `getCell` (onLoad, Read a cell); `getCellHealth` (onLoad, Cell health and schema version); `listCellJobs` (onLoad, Provisioning, migration and maintenance jobs); `getScalingPolicy` (onLoad, Floors, ceilings and target utilisation)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

**What opens over it**

- confirmDialog *Cancel decommission*: **Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A auto-scaling this affects should be identified in the dialog, not just counted. **Collects what `cancelDecommission` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The auto-scaling list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the auto-scaling untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No auto-scaling yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellCapacity` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getScalingPolicy` → `PLATFORM_CELL_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellCapacity` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Infrastructure & Resilience, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-014` · status **notStarted** · provenance generated
- Flow F97 *A cell is capacity-checked and a tenant is placed on it*, step 3: Auto-Scaling Configuration. → 7 operations, 7 of them previously unwalked.
- ADR-0035 *A flash sale gets its own environment, and it cannot be deleted until it has been reconciled* (`docs/adr/0035-burst-environments.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (52 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-014?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cancel decommission, Decommission cell, Save cell tier.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `PLATFORM_CELL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-030` Infrastructure Sizing & Scaling Policy

**See infrastructure sizing & scaling policy for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Infrastructure & Resilience · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_CELL_MANAGE`, `PLATFORM_CELL_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getCellCapacity` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/infrastructure-sizing-and-scaling-policy` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — Terraform

#### Inputs: what the user enters or picks

**Form: Decommission cell** (modal, opened by *Decommission cell*; *Decommission cell* calls `decommissionCell`, *Cancel* sends nothing)

**Collects what `decommissionCell` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

`decommissionCell` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Save cell tier** (modal, opened by *Save cell tier*; *Save cell tier* calls `updateCellTier`, *Cancel* sends nothing)

**Collects what `updateCellTier` sends before it is called.** Required: `tier`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.

`updateCellTier` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Save scaling policy** (modal, opened by *Save scaling policy*; *Save scaling policy* calls `setScalingPolicy`, *Cancel* sends nothing)

**Collects what `setScalingPolicy` sends before it is called.** Required: `id`. Optional: `service`, `replicaFloor`, `replicaCeiling`, `targetUtilisationPct`, `scaleStepPct`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setScalingPolicy` body |
| Cell `cellId` | picker: choose a cell | optional | — | — | shows names, sends the id | — | `setScalingPolicy` body |
| Service `service` | text field | optional | — | — | — | — | `setScalingPolicy` body |
| Replica floor `replicaFloor` | number field | optional | — | — | — | — | `setScalingPolicy` body |
| Replica ceiling `replicaCeiling` | number field | optional | — | — | — | Null means no maximum, which is the correct setting for a burst cell. | `setScalingPolicy` body |
| Target utilisation pct `targetUtilisationPct` | number field (%) | optional | — | — | — | — | `setScalingPolicy` body |
| Scale step pct `scaleStepPct` | number field (%) | optional | — | — | — | — | `setScalingPolicy` body |
| Updated at `updatedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setScalingPolicy` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every cell job** (data table, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellJob.id` |
| Kind | text | not in the schema: `CellJob.kind` |
| Status | text | not in the schema: `CellJob.status` |
| Progress percent | text | not in the schema: `CellJob.progressPercent` |
| Message | text | not in the schema: `CellJob.message` |
| Error | text | not in the schema: `CellJob.error` |
| Scheduled for | text | not in the schema: `CellJob.scheduledFor` |
| Completed at | text | not in the schema: `CellJob.completedAt` |

**The selected cell job** (detail panel, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellJob.id` |
| Kind | text | not in the schema: `CellJob.kind` |
| Status | text | not in the schema: `CellJob.status` |
| Progress percent | text | not in the schema: `CellJob.progressPercent` |
| Message | text | not in the schema: `CellJob.message` |
| Error | text | not in the schema: `CellJob.error` |
| Scheduled for | text | not in the schema: `CellJob.scheduledFor` |
| Completed at | text | not in the schema: `CellJob.completedAt` |

**The cell** (detail panel, from `getCell`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellDetail.id` |
| Name | text | not in the schema: `CellDetail.name` |
| Kind | text | not in the schema: `CellDetail.kind` |
| Cluster ID | text | not in the schema: `CellDetail.clusterId` |
| Is reachable | text | not in the schema: `CellDetail.isReachable` |
| Last contact at | text | not in the schema: `CellDetail.lastContactAt` |
| Licence expires at | text | not in the schema: `CellDetail.licenceExpiresAt` |
| Participates in cross cell | text | not in the schema: `CellDetail.participatesInCrossCell` |
| Region ID | text | not in the schema: `CellDetail.regionId` |
| Region name | text | not in the schema: `CellDetail.regionName` |
| Country code | text | not in the schema: `CellDetail.countryCode` |
| Tier | text | not in the schema: `CellDetail.tier` |
| Status | text | not in the schema: `CellDetail.status` |
| Cloud provider | text | not in the schema: `CellDetail.cloudProvider` |
| Cloud region | text | not in the schema: `CellDetail.cloudRegion` |
| API endpoint | text | not in the schema: `CellDetail.apiEndpoint` |

**The cell health** (detail panel, from `getCellHealth`)

| Shows | Format | Notes |
|---|---|---|
| Is healthy | text | not in the schema: `CellHealth.isHealthy` |
| Is schema behind | text | not in the schema: `CellHealth.isSchemaBehind` |
| Database status | text | not in the schema: `CellHealth.databaseStatus` |
| Replication lag seconds | text | not in the schema: `CellHealth.replicationLagSeconds` |
| Last backup at | text | not in the schema: `CellHealth.lastBackupAt` |
| Last restore drill at | text | not in the schema: `CellHealth.lastRestoreDrillAt` |
| Checked at | text | not in the schema: `CellHealth.checkedAt` |

**The scaling policy** (detail panel, from `getScalingPolicy`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Service | text | — |
| Replica floor | 1,234 | — |
| Replica ceiling | 1,234 | Null means no maximum, which is the correct setting for a burst cell. |
| Target utilisation pct | 1,234 | — |
| Scale step pct | 1,234 | — |

**The cell capacity** (detail panel, from `getCellCapacity`)

| Shows | Format | Notes |
|---|---|---|
| Kind | text | not in the schema: `CellCapacity.kind` |
| Tenant count | text | not in the schema: `CellCapacity.tenantCount` |
| Is constrained | text | not in the schema: `CellCapacity.isConstrained` |
| Constrained dimension | text | not in the schema: `CellCapacity.constrainedDimension` |
| Dimensions | text | not in the schema: `CellCapacity.dimensions` |
| Forecast breach at | text | not in the schema: `CellCapacity.forecastBreachAt` |
| Measured at | text | not in the schema: `CellCapacity.measuredAt` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cancel decommission (destructive button) | `cancelDecommission` (not in any contract) | — | — | — | — |
| Decommission cell (secondary button) | `decommissionCell` (not in any contract) | — | — | — | — |
| Save cell tier (secondary button) | `updateCellTier` (not in any contract) | — | — | — | — |
| Save scaling policy (secondary button) | `setScalingPolicy` PUT `/scaling-policies` | ScalingPolicy | ScalingPolicy | — | opens modal first |

**Data it reads**: `getCellCapacity` (onLoad, Load against headroom); `getCell` (onLoad, Read a cell); `getCellHealth` (onLoad, Cell health and schema version); `listCellJobs` (onLoad, Provisioning, migration and maintenance jobs); `getScalingPolicy` (onLoad, The policy as it stands)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

**What opens over it**

- confirmDialog *Cancel decommission*: **Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A infrastructure sizing scaling this affects should be identified in the dialog, not just counted. **Collects what `cancelDecommission` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The infrastructure sizing scaling list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the infrastructure sizing scaling untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No infrastructure sizing scaling yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellCapacity` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getScalingPolicy` → `PLATFORM_CELL_VIEW` (read) · staff
- `setScalingPolicy` → `PLATFORM_CELL_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellCapacity` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Infrastructure & Resilience, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-030` · status **notStarted** · provenance generated
- ADR-0035 *A flash sale gets its own environment, and it cannot be deleted until it has been reconciled* (`docs/adr/0035-burst-environments.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (52 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-030?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cancel decommission, Decommission cell, Save cell tier, Save scaling policy.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`, `PLATFORM_CELL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-033` Backup & DR Status

**See backup & dr status for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Infrastructure & Resilience · wave 2 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_CELL_VIEW` (1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getCellHealth` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/backup-and-dr-status` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

#### Inputs: what the user enters or picks

**Form: Decommission cell** (modal, opened by *Decommission cell*; *Decommission cell* calls `decommissionCell`, *Cancel* sends nothing)

**Collects what `decommissionCell` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

`decommissionCell` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Save cell tier** (modal, opened by *Save cell tier*; *Save cell tier* calls `updateCellTier`, *Cancel* sends nothing)

**Collects what `updateCellTier` sends before it is called.** Required: `tier`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.

`updateCellTier` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every cell job** (data table, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellJob.id` |
| Kind | text | not in the schema: `CellJob.kind` |
| Status | text | not in the schema: `CellJob.status` |
| Progress percent | text | not in the schema: `CellJob.progressPercent` |
| Message | text | not in the schema: `CellJob.message` |
| Error | text | not in the schema: `CellJob.error` |
| Scheduled for | text | not in the schema: `CellJob.scheduledFor` |
| Completed at | text | not in the schema: `CellJob.completedAt` |

**Every backup run** (data table, from `listBackupRuns`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Scope | chip: Cell, Tenant | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| State | chip: Running, Succeeded, Failed | — |
| Size bytes | 1,234 | — |
| Restore tested at | 1 Oct 2026, 14:30 | A backup nobody has restored is a hypothesis. |
| Error | text | — |

**The selected cell job** (detail panel, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellJob.id` |
| Kind | text | not in the schema: `CellJob.kind` |
| Status | text | not in the schema: `CellJob.status` |
| Progress percent | text | not in the schema: `CellJob.progressPercent` |
| Message | text | not in the schema: `CellJob.message` |
| Error | text | not in the schema: `CellJob.error` |
| Scheduled for | text | not in the schema: `CellJob.scheduledFor` |
| Completed at | text | not in the schema: `CellJob.completedAt` |

**The cell** (detail panel, from `getCell`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellDetail.id` |
| Name | text | not in the schema: `CellDetail.name` |
| Kind | text | not in the schema: `CellDetail.kind` |
| Cluster ID | text | not in the schema: `CellDetail.clusterId` |
| Is reachable | text | not in the schema: `CellDetail.isReachable` |
| Last contact at | text | not in the schema: `CellDetail.lastContactAt` |
| Licence expires at | text | not in the schema: `CellDetail.licenceExpiresAt` |
| Participates in cross cell | text | not in the schema: `CellDetail.participatesInCrossCell` |
| Region ID | text | not in the schema: `CellDetail.regionId` |
| Region name | text | not in the schema: `CellDetail.regionName` |
| Country code | text | not in the schema: `CellDetail.countryCode` |
| Tier | text | not in the schema: `CellDetail.tier` |
| Status | text | not in the schema: `CellDetail.status` |
| Cloud provider | text | not in the schema: `CellDetail.cloudProvider` |
| Cloud region | text | not in the schema: `CellDetail.cloudRegion` |
| API endpoint | text | not in the schema: `CellDetail.apiEndpoint` |

**The cell capacity** (detail panel, from `getCellCapacity`)

| Shows | Format | Notes |
|---|---|---|
| Kind | text | not in the schema: `CellCapacity.kind` |
| Tenant count | text | not in the schema: `CellCapacity.tenantCount` |
| Is constrained | text | not in the schema: `CellCapacity.isConstrained` |
| Constrained dimension | text | not in the schema: `CellCapacity.constrainedDimension` |
| Dimensions | text | not in the schema: `CellCapacity.dimensions` |
| Forecast breach at | text | not in the schema: `CellCapacity.forecastBreachAt` |
| Measured at | text | not in the schema: `CellCapacity.measuredAt` |

**The cell health** (detail panel, from `getCellHealth`)

| Shows | Format | Notes |
|---|---|---|
| Is healthy | text | not in the schema: `CellHealth.isHealthy` |
| Is schema behind | text | not in the schema: `CellHealth.isSchemaBehind` |
| Database status | text | not in the schema: `CellHealth.databaseStatus` |
| Replication lag seconds | text | not in the schema: `CellHealth.replicationLagSeconds` |
| Last backup at | text | not in the schema: `CellHealth.lastBackupAt` |
| Last restore drill at | text | not in the schema: `CellHealth.lastRestoreDrillAt` |
| Checked at | text | not in the schema: `CellHealth.checkedAt` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cancel decommission (destructive button) | `cancelDecommission` (not in any contract) | — | — | — | — |
| Decommission cell (secondary button) | `decommissionCell` (not in any contract) | — | — | — | — |
| Save cell tier (secondary button) | `updateCellTier` (not in any contract) | — | — | — | — |

**Data it reads**: `getCellHealth` (onLoad, from page inventory); `getCell` (onLoad, Read a cell); `getCellCapacity` (onLoad, Load against headroom); `listCellJobs` (onLoad, Provisioning, migration and maintenance jobs); `listBackupRuns` (onLoad, Backups taken and how old the newest is)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

**What opens over it**

- confirmDialog *Cancel decommission*: **Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A backup status this affects should be identified in the dialog, not just counted. **Collects what `cancelDecommission` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The backup status list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the backup status untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No backup status yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listBackupRuns` → `PLATFORM_CELL_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Infrastructure & Resilience, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-033` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (54 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-033?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cancel decommission, Decommission cell, Save cell tier.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `PLATFORM_CELL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-034` Archival Job Monitor

**Find archival job monitor for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Infrastructure & Resilience · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_CELL_VIEW` (1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getCell` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/archival-job-monitor` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — retention not specified

#### Inputs: what the user enters or picks

**Form: Decommission cell** (modal, opened by *Decommission cell*; *Decommission cell* calls `decommissionCell`, *Cancel* sends nothing)

**Collects what `decommissionCell` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

`decommissionCell` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Save cell tier** (modal, opened by *Save cell tier*; *Save cell tier* calls `updateCellTier`, *Cancel* sends nothing)

**Collects what `updateCellTier` sends before it is called.** Required: `tier`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.

`updateCellTier` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every cell job** (data table, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellJob.id` |
| Kind | text | not in the schema: `CellJob.kind` |
| Status | text | not in the schema: `CellJob.status` |
| Progress percent | text | not in the schema: `CellJob.progressPercent` |
| Message | text | not in the schema: `CellJob.message` |
| Error | text | not in the schema: `CellJob.error` |
| Scheduled for | text | not in the schema: `CellJob.scheduledFor` |
| Completed at | text | not in the schema: `CellJob.completedAt` |

**Every archival job** (data table, from `listArchivalJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Policy name | text | — |
| Target table | text | — |
| Rows archived | 1,234 | — |
| Rows purged | 1,234 | — |
| State | chip: Scheduled, Running, Succeeded, Failed | — |
| Run at | 1 Oct 2026, 14:30 | — |
| Error | text | — |

**The selected cell job** (detail panel, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellJob.id` |
| Kind | text | not in the schema: `CellJob.kind` |
| Status | text | not in the schema: `CellJob.status` |
| Progress percent | text | not in the schema: `CellJob.progressPercent` |
| Message | text | not in the schema: `CellJob.message` |
| Error | text | not in the schema: `CellJob.error` |
| Scheduled for | text | not in the schema: `CellJob.scheduledFor` |
| Completed at | text | not in the schema: `CellJob.completedAt` |

**The cell capacity** (detail panel, from `getCellCapacity`)

| Shows | Format | Notes |
|---|---|---|
| Kind | text | not in the schema: `CellCapacity.kind` |
| Tenant count | text | not in the schema: `CellCapacity.tenantCount` |
| Is constrained | text | not in the schema: `CellCapacity.isConstrained` |
| Constrained dimension | text | not in the schema: `CellCapacity.constrainedDimension` |
| Dimensions | text | not in the schema: `CellCapacity.dimensions` |
| Forecast breach at | text | not in the schema: `CellCapacity.forecastBreachAt` |
| Measured at | text | not in the schema: `CellCapacity.measuredAt` |

**The cell health** (detail panel, from `getCellHealth`)

| Shows | Format | Notes |
|---|---|---|
| Is healthy | text | not in the schema: `CellHealth.isHealthy` |
| Is schema behind | text | not in the schema: `CellHealth.isSchemaBehind` |
| Database status | text | not in the schema: `CellHealth.databaseStatus` |
| Replication lag seconds | text | not in the schema: `CellHealth.replicationLagSeconds` |
| Last backup at | text | not in the schema: `CellHealth.lastBackupAt` |
| Last restore drill at | text | not in the schema: `CellHealth.lastRestoreDrillAt` |
| Checked at | text | not in the schema: `CellHealth.checkedAt` |

**The cell** (detail panel, from `getCell`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `CellDetail.id` |
| Name | text | not in the schema: `CellDetail.name` |
| Kind | text | not in the schema: `CellDetail.kind` |
| Cluster ID | text | not in the schema: `CellDetail.clusterId` |
| Is reachable | text | not in the schema: `CellDetail.isReachable` |
| Last contact at | text | not in the schema: `CellDetail.lastContactAt` |
| Licence expires at | text | not in the schema: `CellDetail.licenceExpiresAt` |
| Participates in cross cell | text | not in the schema: `CellDetail.participatesInCrossCell` |
| Region ID | text | not in the schema: `CellDetail.regionId` |
| Region name | text | not in the schema: `CellDetail.regionName` |
| Country code | text | not in the schema: `CellDetail.countryCode` |
| Tier | text | not in the schema: `CellDetail.tier` |
| Status | text | not in the schema: `CellDetail.status` |
| Cloud provider | text | not in the schema: `CellDetail.cloudProvider` |
| Cloud region | text | not in the schema: `CellDetail.cloudRegion` |
| API endpoint | text | not in the schema: `CellDetail.apiEndpoint` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cancel decommission (destructive button) | `cancelDecommission` (not in any contract) | — | — | — | — |
| Decommission cell (secondary button) | `decommissionCell` (not in any contract) | — | — | — | — |
| Save cell tier (secondary button) | `updateCellTier` (not in any contract) | — | — | — | — |

**Data it reads**: `listCellJobs` (onLoad, Provisioning, migration and maintenance jobs); `getCell` (onLoad, Read a cell); `getCellCapacity` (onLoad, Load against headroom); `getCellHealth` (onLoad, Cell health and schema version); `listArchivalJobs` (onLoad, Archival and retention jobs)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

**What opens over it**

- confirmDialog *Cancel decommission*: **Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A archival job this affects should be identified in the dialog, not just counted. **Collects what `cancelDecommission` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The archival job list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the archival job untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No archival job yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `listCellJobs` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listArchivalJobs` → `PLATFORM_CELL_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `listCellJobs` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Infrastructure & Resilience, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-034` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (54 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-034?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cancel decommission, Decommission cell, Save cell tier.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `PLATFORM_CELL_VIEW`.
- [ ] The module and platform inputs below are applied.
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

### In P09 · Infrastructure & Resilience

- **Open question.** Open (Chinmay): should server/infrastructure monitoring and management be a dedicated module inside the TICVAI platform, or stay in Softlabs' own tooling (e.g. Terraform) outside the product? Input from Tejesh pending. *(open · MoM 10 Sep 2026, 4.18 Other Discussion · DI-841)*

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getScalingPolicy": {"method":"GET","path":"/scaling-policies","contract":"platform-ops","summary":"The floors, ceilings and target utilisation a cell scales on","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"ScalingPolicy"},
"listArchivalJobs": {"method":"GET","path":"/archival-jobs","contract":"platform-ops","summary":"Archival and retention jobs","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"ArchivalJob"},
"listBackupRuns": {"method":"GET","path":"/backup-runs","contract":"platform-ops","summary":"Backups taken and what they cover","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"BackupRun"},
"setScalingPolicy": {"method":"PUT","path":"/scaling-policies","contract":"platform-ops","summary":"Change the scaling policy","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ScalingPolicy","responds":"ScalingPolicy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ArchivalJob": {"type":"object","x-ticvai-persistence":"control.archival_job","description":"**Drafted 4 September.** One archival or retention run. Retention is a legal obligation, so a stalled job is a compliance failure rather than a housekeeping one.","required":["id"],"properties":{"id":{"type":"string","format":"uuid"},"cellId":{"type":"string","format":"uuid"},"policyName":{"type":"string"},"targetTable":{"type":"string"},"rowsArchived":{"type":"integer"},"rowsPurged":{"type":"integer"},"state":{"type":"string","enum":["scheduled","running","succeeded","failed"]},"runAt":{"type":"string","format":"date-time"},"error":{"type":"string"}}},
"BackupRun": {"type":"object","x-ticvai-persistence":"control.backup_run","description":"**Drafted 4 September.** One backup run. The question this answers is not *did it run* but *how old is the newest restorable copy* - a job that succeeds nightly against an empty database succeeds forever.","required":["id"],"properties":{"id":{"type":"string","format":"uuid"},"cellId":{"type":"string","format":"uuid"},"scope":{"type":"string","enum":["cell","tenant"]},"startedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time"},"state":{"type":"string","enum":["running","succeeded","failed"]},"sizeBytes":{"type":"integer"},"restoreTestedAt":{"type":"string","format":"date-time","description":"**A backup nobody has restored is a hypothesis.**"},"error":{"type":"string"}}},
"ScalingPolicy": {"type":"object","x-ticvai-persistence":"control.scaling_policy","description":"**Drafted 4 September.** What a cell scales on. **A floor and a ceiling are not symmetric** - the floor is the size the environment is stood up at before traffic arrives, and the ceiling is a cap on absorbing a peak nobody predicted (ADR-0035).","required":["id"],"properties":{"id":{"type":"string","format":"uuid"},"cellId":{"type":"string","format":"uuid"},"service":{"type":"string"},"replicaFloor":{"type":"integer"},"replicaCeiling":{"type":"integer","description":"Null means no maximum, which is the correct setting for a burst cell."},"targetUtilisationPct":{"type":"integer"},"scaleStepPct":{"type":"integer"},"updatedAt":{"type":"string","format":"date-time"}}}
}
```
