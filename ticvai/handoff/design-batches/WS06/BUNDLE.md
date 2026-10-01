# WS06 — Access Control board 6

**10 screens · 18 operations · 32 schemas · 5 permissions**

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
  `ACCESS_POINT_CONFIGURE, DEVICE_CONFIGURE, DEVICE_VIEW, SCOPE_VIEW, TURNSTILE_MODE_SET`. A control nobody can use must say so,
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
| `BO-194` | Device & Gate Command Center | B–D | 21 | 294 | 6 | 44 | 6 | 0 | — | notStarted (generated) |
| `BO-195` | Device Type & Hardware Library | B–D | 15 | 0 | 6 | 0 | 3 | 0 | — | notStarted (generated) |
| `BO-196` | Physical Device Registration & Provisioning | B–D | 67 | 0 | 5 | 41 | 5 | 0 | — | notStarted (generated) |
| `BO-197` | Turnstile & Lane Behavior Configuration | B–D | 14 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-198` | Validation Outcome & Guest Feedback Designer | B–D | 11 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-199` | Reader, Scanner & Peripheral Configuration | B–D | 1 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-200` | Handheld & Mobile Access Device Configuration | B–D | 8 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-201` | Gate Modes, Free Spin & Emergency Controls | A | 16 | 0 | 5 | 0 | 1 | 2 | — | notStarted (generated) |
| `BO-202` | Device Software, Content & Remote Configuration | B–D | 6 | 0 | 5 | 0 | 4 | 0 | — | notStarted (generated) |
| `BO-203` | Hardware Compatibility, Health, Testing & Deployment | B–D | 8 | 0 | 6 | 0 | 8 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-195, BO-199 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-194` Device & Gate Command Center

**Provide the central operational/configuration view of the complete access-control hardware estate.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE`, `DEVICE_VIEW`, `SCOPE_VIEW`, `TURNSTILE_MODE_SET` (1 configure, 2 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | `accessPointId` (navigation), `deviceId` (navigation), `placementId` (navigation) |
| Route | `/access-venue/device-gate-command-center-bo-194` |

#### Inputs: what the user enters or picks

**Form: Save access device** (modal, opened by *Save access device*; *Save access device* calls `updateAccessDevicePlacement`, *Cancel* sends nothing)

**Collects what `updateAccessDevicePlacement` sends before it is called.** Required: `id`, `venueId`, `deviceId`, `role`, `isActive`, `scopePath`. Optional: `accessAreaId`, `accessPointId`, `gateLaneId`, `name`, `deviceGroupId`, `controllerReference`, `proximityThresholdMeters`, `installationDate`. The device itself (serial, hardware model, versions) is registered in `platform.device` first, with tenancy `registerDevice` (ADR-0067). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order, and minted by the service with the … | `updateAccessDevicePlacement` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `updateAccessDevicePlacement` body |
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | The registered device placed here (`platform.device`, tenancy `registerDevice`). | `updateAccessDevicePlacement` body |
| Access area `accessAreaId` | picker: choose an access area | optional | — | — | shows names, sends the id | Most specific park, zone or attraction the device sits in (access.access_area) | `updateAccessDevicePlacement` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | Access point (gate) the device serves | `updateAccessDevicePlacement` body |
| Gate lane `gateLaneId` | picker: choose a gate lane | optional | — | — | shows names, sends the id | Lane the device is mounted on (access.gate_lane) | `updateAccessDevicePlacement` body |
| Role `role` | select | required | Entry and exit | Entry · Exit · Entry and exit · Validation only · Proximity · Monitoring | — | What the device does at this place. `proximity` is a beacon; `monitoring` a camera controller that decides nothing. | `updateAccessDevicePlacement` body |
| Name `name` | text field | optional | — | — | — | Label at this place, e.g. | `updateAccessDevicePlacement` body |
| Device group `deviceGroupId` | text field | optional | — | — | — | Device group the placement belongs to, as targeted by hardware deployments and device configurations | `updateAccessDevicePlacement` body |
| Controller reference `controllerReference` | text field | optional | — | — | — | — | `updateAccessDevicePlacement` body |
| Proximity threshold meters `proximityThresholdMeters` | number field | optional | — | min 0 | — | Beacons only: activation distance in metres | `updateAccessDevicePlacement` body |
| Installation date `installationDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateAccessDevicePlacement` body |
| Provisioning checklist `provisioningChecklist` | group | optional | — | — | — | Access's provisioning stages, as a checklist on the placement (ADR-0067). Each item is the time the step was confirmed, null until it is. | `updateAccessDevicePlacement` body |
| Hardware profile assigned at `provisioningChecklist.hardwareProfileAssignedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Location assigned at `provisioningChecklist.locationAssignedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Authenticated at `provisioningChecklist.authenticatedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Configuration downloaded at `provisioningChecklist.configurationDownloadedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Security package downloaded at `provisioningChecklist.securityPackageDownloadedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Connectivity tested at `provisioningChecklist.connectivityTestedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Is active `isActive` | toggle | required | on | A device that is `retired` or `deactivated` in the register is refused at the gate whatever this says. | — | Whether this placement is in use (beacons: activeInactive). A device that is `retired` or `deactivated` in the register is refused at the gate whatever this says. | `updateAccessDevicePlacement` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `updateAccessDevicePlacement` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `device-not-registered`: `deviceId` names no device in `platform.device`, or one that is `deactivated` or `retired` there (ADR-0067).

#### Outputs: what the screen shows and produces

**Shown**

**Total Devices** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Online** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Offline** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Degraded** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Turnstiles** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Handhelds** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Biometric Readers** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**RFID/NFC Readers** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Gates Open** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Gates Closed** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Devices Requiring Sync** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Firmware/Software Exceptions** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Hardware Alerts** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Ai** (metric tile, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |
| Camera health where applicable | text | camera health where applicable |
| Device | text | — |
| Device type | text | e.g. |
| Access point | text | — |
| Mode | text | Current operating mode |
| Status | chip: Healthy, Active, Degraded, Offline, Local mode | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total devices | 1,234 | Total Devices |
| Online | 1,234 | Online |
| Offline | 1,234 | Offline |

**Every device gate** (data table, from `listDeviceGate`)

| Shows | Format | Notes |
|---|---|---|
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |

**The selected device gate** (detail panel): The pack groups this record's detail under its own headings: “Device Directory”.

| Shows | Format | Notes |
|---|---|---|
| Connectivity | text | connectivity |
| Last heartbeat | 1 Oct 2026, 14:30 | last heartbeat |
| Configuration version | text | configuration version |
| Local rule version | text | local rule version |
| Credential security package version | text | credential/security package version |
| Scanner health | text | scanner health |
| Controller health | text | controller health |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save access device (primary button) | `updateAccessDevicePlacement` PUT `/device-placements/{placementId}` | AccessDevicePlacement | AccessDevicePlacement | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `DEVICE_CONFIGURE`; opens modal first |

**Data it reads**: `listDeviceGate` (onLoad, Device & Gate Command Center); `listAccessPoints` (onLoad, The gates and turnstiles whose mode is set)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-195` Device Type & Hardware Library: *Works in Device Type & Hardware Library*; calls `listDeviceGate`
- → `BO-196` Physical Device Registration & Provisioning: *Works in Physical Device Registration & Provisioning*; carries `placementId`; calls `listDeviceGate`
- → `BO-197` Turnstile & Lane Behavior Configuration: *Works in Turnstile & Lane Behavior Configuration*; calls `listDeviceGate`
- → `BO-198` Validation Outcome & Guest Feedback Designer: *Works in Validation Outcome & Guest Feedback Designer*; calls `listDeviceGate`
- → `BO-199` Reader, Scanner & Peripheral Configuration: *Works in Reader, Scanner & Peripheral Configuration*; calls `listDeviceGate`
- → `BO-200` Handheld & Mobile Access Device Configuration: *Works in Handheld & Mobile Access Device Configuration*; calls `listDeviceGate`
- → `BO-201` Gate Modes, Free Spin & Emergency Controls: *Works in Gate Modes, Free Spin & Emergency Controls*; calls `listDeviceGate`
- → `BO-202` Device Software, Content & Remote Configuration: *Works in Device Software, Content & Remote Configuration*; calls `listDeviceGate`
- → `BO-203` Hardware Compatibility, Health, Testing & Deployment: *Works in Hardware Compatibility, Health, Testing & Deployment*; calls `listDeviceGate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The device gate list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the device gate untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No device gate yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the device gate are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here from access with the …; 422 `device-not-registered`: `deviceId` names no device in `platform.device`, or one that is `deactivated` or `retired` there (ADR-0067).; 422 `workstationId` missing for a kind other than `mobileHandset`, or given … |

#### Permissions

- `listDeviceGate` → `DEVICE_VIEW` (read) · staff
- `registerDevice` → `DEVICE_CONFIGURE` (configure) · staff
- `setTurnstileMode` → `TURNSTILE_MODE_SET` (operate) · staff
- `listAccessPoints` → `SCOPE_VIEW` (read) · staff
- `updateAccessDevicePlacement` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

44 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.14 | The system should be able to identify each ticketing kiosk individually by an ID, locate it geographically and administer it remotely. The kiosks should include a supervision interface and alert … | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.6 | It is expected that front gate sales can be performed by the operators using a POS having a touch screen. | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.7 | The POS can be connected to a keyboard for which the function touches can be setup by the system administrator. | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.8 | The POS can be connected to a cash drawer | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.9 | The POS can be connected to a BOCA printer (it is expected to have the list of ticket printing hardware compatible) | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.10 | The POS can be connected to a ZEBRA printer or datamax printer or Evolis, for annual pass (it is expected to have the list of plastic card pass printing hardware compatible) | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.11 | The POS can be connected to a Receipt printer | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.12 | The POS can be connected to a 2D scanner | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.13 | The POS can be connected to a RFID reader/writer | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.14 | The POS can be connected to a Customer display including a double screen allowing the video display | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.15 | The POS can be connected to a camera | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.16 | The POS can be connected to a credit card machine | Ticketing Sales | CONTRACTED | `registerDevice` |
| … 32 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Device incidents get automatic severity (e.g. main-entrance controller outage = critical); adding a device goes through an approval workflow; webhooks notify external systems when a critical device goes offline. *(client request · MoM 15 Sep 2026, 4.9 Device Integration & Operation Analytics · DI-906)*
- Device analytics: total/active/inactive devices across venues (multi-tenant) with location breakdown; health, availability, fault rate and top failure reasons (communication timeout, device offline, invalid response, power issue, firmware error); SLA tracking for devices in extended maintenance. *(client request · MoM 15 Sep 2026, 4.9 Device Integration & Operation Analytics · DI-905)*
- One screen shows live online/offline status of every workstation and device (printers, turnstiles, handheld scanners); a 360 health view shows connectivity, CPU/memory, storage and temperature. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-899)*
- Inventory counts by status (assigned, under maintenance, in stock) - e.g. 15 receipt printers broken down by ticketing, retail, F&B and in store. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-894)*
- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Real-time health view of device connectivity. Device-pushed events (anti-passback attempts, power loss, network loss) are surfaced as alerts and reports, e.g. notifying the operations team when a turnstile goes offline. *(agreed · MoM 2 Sep 2026, 4.1 / 4.2 Health Monitoring & Alerts · DI-625)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-194` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-194`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 1: Opens Device & Gate Command Center → Provide the central operational/configuration view of the complete access-control hardware estate.
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F116 branch at step 1 (expected): when Nothing has been set up on Device & Gate Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F116 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …
- ADR-0067 *One device register; Access keeps only where a device is placed* (`docs/adr/0067-one-device-register.md`)
- ADR-0015 *Standards-First Device Drivers* (`docs/adr/0015-standards-first-device-drivers.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (294 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-194?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save access device.
- [ ] Every transition is wired: `BO-100`, `BO-195`, `BO-196`, `BO-197`, `BO-198`, `BO-199`, `BO-200`, `BO-201`, `BO-202`, `BO-203`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`, `DEVICE_VIEW`, `SCOPE_VIEW`, `TURNSTILE_MODE_SET`.
- [ ] The 6 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-195` Device Type & Hardware Library

**Create reusable hardware definitions independently from physical deployed devices.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE`, `DEVICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/device-type-hardware-library-bo-195` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Form: Save hardware model** (modal, opened by *Save hardware model*; *Save hardware model* calls `setHardwareModel`, *Cancel* sends nothing)

**Collects what `setHardwareModel` sends before it is called.** Required: `id`, `manufacturer`, `model`, `deviceCategory`, `hardwareType`, `scopePath`. Optional: `supportedTechnologies`, `connectivity`, `offlineCapability`, `screenCapability`, `soundCapability`, `lightCapability`, `relayControllerSupport`, `paymentCapability`, `firmwareSoftwareInformation`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setHardwareModel` body |
| Manufacturer `manufacturer` | text field | required | — | — | — | — | `setHardwareModel` body |
| Model `model` | text field | required | — | — | — | — | `setHardwareModel` body |
| Device category `deviceCategory` | radio group | required | — | Turnstile · Special gate · Mobile · Reader · Other | — | — | `setHardwareModel` body |
| Hardware type `hardwareType` | select | required | — | Standard turnstile · Full height turnstile · Tripod turnstile · Speed gate · Wide lane · Accessible pod gate · Buggy gate · Vip gate · Staff gate · Android handheld · Ios device · Tablet … | — | The specific hardware under a device's `kind` (ADR-0067, accepted 1 October: one device register). | `setHardwareModel` body |
| Supported technologies `supportedTechnologies` | list of values (chips) | optional | — | — | — | — | `setHardwareModel` body |
| Connectivity `connectivity` | list of values (chips) | optional | — | — | — | — | `setHardwareModel` body |
| Offline capability `offlineCapability` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Screen capability `screenCapability` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Sound capability `soundCapability` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Light capability `lightCapability` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Relay controller support `relayControllerSupport` | toggle | optional | off | — | — | — | `setHardwareModel` body |
| Payment capability `paymentCapability` | toggle | optional | off | — | — | Payment capability where available | `setHardwareModel` body |
| Firmware software information `firmwareSoftwareInformation` | text field | optional | — | — | — | — | `setHardwareModel` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setHardwareModel` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save hardware model (primary button) | `setHardwareModel` PUT `/hardware-models` | AccessHardwareModel | AccessHardwareModel | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `DEVICE_CONFIGURE`; opens modal first |

**Data it reads**: `listDeviceTypeHardware` (onLoad, Device Type & Hardware Library)

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; calls `listDeviceTypeHardware`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The device type hardware list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the device type hardware untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No device type hardware yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the device type hardware are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listDeviceTypeHardware` → `DEVICE_VIEW` (read) · staff
- `setHardwareModel` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- No driver is ever installed on the workstation OS: drivers are built into the TICVAI app; staff only connect the device and test print/scan from within the app; new models are supported by a back-end driver update, not a code release. *(agreed · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-897)*
- Configuration template library: a template per model (e.g. a specific Epson receipt printer) auto-attaches the right drivers when a device of that type is added. Template attribute list pending from Allam. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-896)*
- Gate & zone management shows gates per location (e.g. three at a main entry plaza, two at a main entry zone); device inventory lists turnstiles and handhelds assignable per gate; a device is added by choosing an integrated turnstile model and entering connection details (IP address). *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-624)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-195` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-195`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 2: Works in Device Type & Hardware Library → Create reusable hardware definitions independently from physical deployed devices.
- ADR-0067 *One device register; Access keeps only where a device is placed* (`docs/adr/0067-one-device-register.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-195?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save hardware model.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`, `DEVICE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-196` Physical Device Registration & Provisioning

**Register actual deployed hardware and connect it to the Board 1 topology.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE`, `DEVICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `deviceId` (session), `placementId` (navigation) |
| Route | `/access-venue/physical-device-registration-provisioning-bo-196` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Device ID | select field | — | — | — | — | — | — |
| Serial Number | select field | — | — | — | — | — | — |
| Hardware Model | select field | — | — | — | — | — | — |
| Manufacturer | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Park | select field | — | — | — | — | — | — |
| Zone | select field | — | — | — | — | — | — |
| Access Point | select field | — | — | — | — | — | — |
| Gate/Lane | select field | — | — | — | — | — | — |
| IP/network reference | select field | — | — | — | — | — | — |
| controller reference | select field | — | — | — | — | — | — |

**Form: Register device** (modal, opened by *Register device*; *Register device* calls `registerDevice`, *Cancel* sends nothing)

**Collects what `registerDevice` sends before it is called** (tenancy, the one device register, ADR-0067). Required: `kind`, `driver`. Optional: `hardwareType`, `hardwareModelId`, `serialNumber`, `model`, `identifier`, `ipNetworkReference`. An access-control device binds to no workstation. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Receipt printer · Ticket printer · Label printer · Cash drawer · Barcode scanner · RFID reader · NFC reader · Card reader · ID reader · Biometric reader · Access reader · Payment terminal … | — | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation. | `registerDevice` body |
| Driver `driver` | text field | required | — | — | — | Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015). | `registerDevice` body |
| Identifier `identifier` | text field | optional | — | — | — | — | `registerDevice` body |
| Workstation `workstationId` | picker: choose a workstation | optional | — | — | shows names, sends the id | Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control device (one with a `hardwareType`), which is … | `registerDevice` body |
| Model `model` | text field | optional | — | — | — | — | `registerDevice` body |
| Hardware type `hardwareType` | select | optional | — | Standard turnstile · Full height turnstile · Tripod turnstile · Speed gate · Wide lane · Accessible pod gate · Buggy gate · Vip gate · Staff gate · Android handheld · Ios device · Tablet … | — | The specific hardware under `kind` (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into the one register. | `registerDevice` body |
| Hardware model `hardwareModelId` | picker: choose a hardware model | optional | — | — | shows names, sends the id | The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it. | `registerDevice` body |
| Serial number `serialNumber` | text field | optional | — | max length 100; A serial already registered in the tenant is refused `409` by `registerDevice`. | — | The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). | `registerDevice` body |
| Ip network reference `ipNetworkReference` | text field | optional | — | — | — | Network address or reference the device is reached at (ADR-0067). | `registerDevice` body |
| Push token `pushToken` | text field | optional | — | Guest devices register for push and staff devices did not — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has … | — | BL-163. Guest devices register for push and staff devices did not — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told … | `registerDevice` body |
| Push platform `pushPlatform` | radio group | optional | — | Ios · Android · Web · Windows | — | — | `registerDevice` body |
| Offline scope `offlineScope` | radio group | optional | — | None · Read only · Sell and scan · Full venue | — | BL-163. What this device may do with no connection, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled. | `registerDevice` body |
| Is required `isRequired` | toggle | optional | — | — | — | True blocks shift open when the device is unreachable. | `registerDevice` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here from access with the …; 422 `workstationId` missing for a kind other than `mobileHandset`, or given for a `mobileHandset` (18.1.5).

**Form: Register access device** (modal, opened by *Register access device*; *Register access device* calls `placeAccessDevice`, *Cancel* sends nothing)

**Collects what `placeAccessDevice` sends before it is called.** Required: `id`, `venueId`, `deviceId`, `role`, `isActive`, `scopePath`. Optional: `accessAreaId`, `accessPointId`, `gateLaneId`, `name`, `deviceGroupId`, `controllerReference`, `proximityThresholdMeters`, `installationDate`. The device itself (serial, hardware model, versions) is registered in `platform.device` first, with tenancy `registerDevice` (ADR-0067). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order, and minted by the service with the … | `placeAccessDevice` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `placeAccessDevice` body |
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | The registered device placed here (`platform.device`, tenancy `registerDevice`). | `placeAccessDevice` body |
| Access area `accessAreaId` | picker: choose an access area | optional | — | — | shows names, sends the id | Most specific park, zone or attraction the device sits in (access.access_area) | `placeAccessDevice` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | Access point (gate) the device serves | `placeAccessDevice` body |
| Gate lane `gateLaneId` | picker: choose a gate lane | optional | — | — | shows names, sends the id | Lane the device is mounted on (access.gate_lane) | `placeAccessDevice` body |
| Role `role` | select | required | Entry and exit | Entry · Exit · Entry and exit · Validation only · Proximity · Monitoring | — | What the device does at this place. `proximity` is a beacon; `monitoring` a camera controller that decides nothing. | `placeAccessDevice` body |
| Name `name` | text field | optional | — | — | — | Label at this place, e.g. | `placeAccessDevice` body |
| Device group `deviceGroupId` | text field | optional | — | — | — | Device group the placement belongs to, as targeted by hardware deployments and device configurations | `placeAccessDevice` body |
| Controller reference `controllerReference` | text field | optional | — | — | — | — | `placeAccessDevice` body |
| Proximity threshold meters `proximityThresholdMeters` | number field | optional | — | min 0 | — | Beacons only: activation distance in metres | `placeAccessDevice` body |
| Installation date `installationDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `placeAccessDevice` body |
| Provisioning checklist `provisioningChecklist` | group | optional | — | — | — | Access's provisioning stages, as a checklist on the placement (ADR-0067). Each item is the time the step was confirmed, null until it is. | `placeAccessDevice` body |
| Hardware profile assigned at `provisioningChecklist.hardwareProfileAssignedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `placeAccessDevice` body |
| Location assigned at `provisioningChecklist.locationAssignedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `placeAccessDevice` body |
| Authenticated at `provisioningChecklist.authenticatedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `placeAccessDevice` body |
| Configuration downloaded at `provisioningChecklist.configurationDownloadedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `placeAccessDevice` body |
| Security package downloaded at `provisioningChecklist.securityPackageDownloadedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `placeAccessDevice` body |
| Connectivity tested at `provisioningChecklist.connectivityTestedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `placeAccessDevice` body |
| Is active `isActive` | toggle | required | on | A device that is `retired` or `deactivated` in the register is refused at the gate whatever this says. | — | Whether this placement is in use (beacons: activeInactive). A device that is `retired` or `deactivated` in the register is refused at the gate whatever this says. | `placeAccessDevice` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `placeAccessDevice` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 `device-already-placed`: the device already has an active placement. Move it with `updateAccessDevicePlacement`, or set that placement `isActive: false` first.; 422 `device-not-registered`: `deviceId` names no device in `platform.device`, or one that is `deactivated` or `retired` there (ADR-0067).

**Form: Save access device** (modal, opened by *Save access device*; *Save access device* calls `updateAccessDevicePlacement`, *Cancel* sends nothing)

**Collects what `updateAccessDevicePlacement` sends before it is called.** Required: `id`, `venueId`, `deviceId`, `role`, `isActive`, `scopePath`. Optional: `accessAreaId`, `accessPointId`, `gateLaneId`, `name`, `deviceGroupId`, `controllerReference`, `proximityThresholdMeters`, `installationDate`. The device itself (serial, hardware model, versions) is registered in `platform.device` first, with tenancy `registerDevice` (ADR-0067). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Every id is a uuid, and every new one is a UUIDv7 (ADR-0056, 30 September): time-ordered, so a key in an index stays in insertion order, and minted by the service with the … | `updateAccessDevicePlacement` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `updateAccessDevicePlacement` body |
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | The registered device placed here (`platform.device`, tenancy `registerDevice`). | `updateAccessDevicePlacement` body |
| Access area `accessAreaId` | picker: choose an access area | optional | — | — | shows names, sends the id | Most specific park, zone or attraction the device sits in (access.access_area) | `updateAccessDevicePlacement` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | Access point (gate) the device serves | `updateAccessDevicePlacement` body |
| Gate lane `gateLaneId` | picker: choose a gate lane | optional | — | — | shows names, sends the id | Lane the device is mounted on (access.gate_lane) | `updateAccessDevicePlacement` body |
| Role `role` | select | required | Entry and exit | Entry · Exit · Entry and exit · Validation only · Proximity · Monitoring | — | What the device does at this place. `proximity` is a beacon; `monitoring` a camera controller that decides nothing. | `updateAccessDevicePlacement` body |
| Name `name` | text field | optional | — | — | — | Label at this place, e.g. | `updateAccessDevicePlacement` body |
| Device group `deviceGroupId` | text field | optional | — | — | — | Device group the placement belongs to, as targeted by hardware deployments and device configurations | `updateAccessDevicePlacement` body |
| Controller reference `controllerReference` | text field | optional | — | — | — | — | `updateAccessDevicePlacement` body |
| Proximity threshold meters `proximityThresholdMeters` | number field | optional | — | min 0 | — | Beacons only: activation distance in metres | `updateAccessDevicePlacement` body |
| Installation date `installationDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateAccessDevicePlacement` body |
| Provisioning checklist `provisioningChecklist` | group | optional | — | — | — | Access's provisioning stages, as a checklist on the placement (ADR-0067). Each item is the time the step was confirmed, null until it is. | `updateAccessDevicePlacement` body |
| Hardware profile assigned at `provisioningChecklist.hardwareProfileAssignedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Location assigned at `provisioningChecklist.locationAssignedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Authenticated at `provisioningChecklist.authenticatedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Configuration downloaded at `provisioningChecklist.configurationDownloadedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Security package downloaded at `provisioningChecklist.securityPackageDownloadedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Connectivity tested at `provisioningChecklist.connectivityTestedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessDevicePlacement` body |
| Is active `isActive` | toggle | required | on | A device that is `retired` or `deactivated` in the register is refused at the gate whatever this says. | — | Whether this placement is in use (beacons: activeInactive). A device that is `retired` or `deactivated` in the register is refused at the gate whatever this says. | `updateAccessDevicePlacement` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `updateAccessDevicePlacement` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `device-not-registered`: `deviceId` names no device in `platform.device`, or one that is `deactivated` or `retired` there (ADR-0067).

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Register device (secondary button) | `registerDevice` POST `/devices` | RegisteredDevice | RegisteredDevice | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here … | gated `DEVICE_CONFIGURE`; opens modal first |
| Register access device (primary button) | `placeAccessDevice` POST `/device-placements` | AccessDevicePlacement | AccessDevicePlacement | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 `device-already-placed`: the device already has an active placement. Move it with `updateAccessDevicePlacement`, or set that … | gated `DEVICE_CONFIGURE`; opens modal first |
| Save access device (secondary button) | `updateAccessDevicePlacement` PUT `/device-placements/{placementId}` | AccessDevicePlacement | AccessDevicePlacement | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `DEVICE_CONFIGURE`; opens modal first |

**Data it reads**: `listPhysicalDeviceRegistration` (onLoad, Physical Device Registration & Provisioning)

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; carries `accessPointId`, `deviceId`, `placementId`; calls `listPhysicalDeviceRegistration`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The physical device registration configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the physical device registration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No physical device registration configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here from access with the …; 409 `device-already-placed`: the device already has an active placement. Move it with `updateAccessDevicePlacement`, or set that placement `isActive: false` first.; 422 `device-not-registered`: `deviceId` names no … |

#### Permissions

- `listPhysicalDeviceRegistration` → `DEVICE_VIEW` (read) · staff
- `registerDevice` → `DEVICE_CONFIGURE` (configure) · staff
- `placeAccessDevice` → `DEVICE_CONFIGURE` (configure) · staff
- `updateAccessDevicePlacement` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

41 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.14 | The system should be able to identify each ticketing kiosk individually by an ID, locate it geographically and administer it remotely. The kiosks should include a supervision interface and alert … | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.6 | It is expected that front gate sales can be performed by the operators using a POS having a touch screen. | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.7 | The POS can be connected to a keyboard for which the function touches can be setup by the system administrator. | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.8 | The POS can be connected to a cash drawer | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.9 | The POS can be connected to a BOCA printer (it is expected to have the list of ticket printing hardware compatible) | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.10 | The POS can be connected to a ZEBRA printer or datamax printer or Evolis, for annual pass (it is expected to have the list of plastic card pass printing hardware compatible) | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.11 | The POS can be connected to a Receipt printer | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.12 | The POS can be connected to a 2D scanner | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.13 | The POS can be connected to a RFID reader/writer | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.14 | The POS can be connected to a Customer display including a double screen allowing the video display | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.15 | The POS can be connected to a camera | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.16 | The POS can be connected to a credit card machine | Ticketing Sales | CONTRACTED | `registerDevice` |
| … 29 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Device incidents get automatic severity (e.g. main-entrance controller outage = critical); adding a device goes through an approval workflow; webhooks notify external systems when a critical device goes offline. *(client request · MoM 15 Sep 2026, 4.9 Device Integration & Operation Analytics · DI-906)*
- Asset record: purchase date, warranty status/expiry, supplier, serial, manufacturer; ownership and responsibility shown separately (venue owns, operations responsible); a visual map shows installation location. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-895)*
- 360 device view shows status and workstation; reassign to another workstation or deactivate with a logged reason; lifecycle view tracks registration -> enrolment -> assignment -> reassignment. *(client request · MoM 15 Sep 2026, 4.3 Device Management - Registration, Enrollment & Workstation Assignment · DI-893)*
- Device directory: search and add devices (printers, scanners, customer displays, cash drawers, turnstiles, handhelds, mobile POS) capturing serial number, type and model; adding generates a secure enrolment code; devices are assigned to workstations (e.g. A has ticket printer, receipt printer and cash drawer). *(client request · MoM 15 Sep 2026, 4.3 Device Management - Registration, Enrollment & Workstation Assignment · DI-892)*
- Gate & zone management shows gates per location (e.g. three at a main entry plaza, two at a main entry zone); device inventory lists turnstiles and handhelds assignable per gate; a device is added by choosing an integrated turnstile model and entering connection details (IP address). *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-624)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-196` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-196`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 4: Works in Physical Device Registration & Provisioning → Register actual deployed hardware and connect it to the Board 1 topology.
- ADR-0067 *One device register; Access keeps only where a device is placed* (`docs/adr/0067-one-device-register.md`)
- ADR-0015 *Standards-First Device Drivers* (`docs/adr/0015-standards-first-device-drivers.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (67), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-196?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Register device, Register access device, Save access device.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`, `DEVICE_VIEW`.
- [ ] The 5 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-197` Turnstile & Lane Behavior Configuration

**Configure how each turnstile or lane behaves. The matrix specifically requires software on turnstiles to behave differently according to card/ticket type and supports different operating modes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/turnstile-lane-behavior-configuration-bo-197` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Entry | select field | — | — | — | — | — | — |
| Exit | select field | — | — | — | — | — | — |
| Entry/Exit | select field | — | — | — | — | — | — |
| Re-entry | select field | — | — | — | — | — | — |
| Crossover | select field | — | — | — | — | — | — |
| Fast Pass | select field | — | — | — | — | — | — |
| Attraction | select field | — | — | — | — | — | — |
| Group | select field | — | — | — | — | — | — |
| Count Only | select field | — | — | — | — | — | — |
| Free Spin | select field | — | — | — | — | — | — |
| Closed | select field | — | — | — | — | — | — |
| Unlock duration | select field | — | — | — | — | — | — |
| pass-through timeout | select field | — | — | — | — | — | — |
| relock behavior | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; carries `accessPointId`; calls `setTurnstileLaneBehavior`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The turnstile lane behavior configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the turnstile lane behavior untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No turnstile lane behavior configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setTurnstileLaneBehavior` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Turnstile light/sound feedback is configurable: e.g. green light for an adult ticket, orange for a child ticket as a quick visual fraud check; some models play audio, including celebratory sounds (e.g. birthday visit). *(client request · MoM 2 Sep 2026, 4.13 Turnstile Hardware & Handheld Scanner Configuration · DI-644)*
- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-197` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-197`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 6: Works in Turnstile & Lane Behavior Configuration → Configure how each turnstile or lane behaves. The matrix specifically requires software on turnstiles to behave differently according to card/ticket type and supports different operating modes.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-197?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-198` Validation Outcome & Guest Feedback Designer

**Configure what the physical access device does and displays after validation. The matrix explicitly requires valid/non-valid messages, lights, pictograms and sounds, including green/yellow/red behavior.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/validation-outcome-guest-feedback-designer-bo-198` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Green light | select field | — | — | — | — | — | — |
| Gate open | select field | — | — | — | — | — | — |
| Success tone | select field | — | — | — | — | — | — |
| ✓ pictogram | select field | — | — | — | — | — | — |
| Custom message | select field | — | — | — | — | — | — |
| Yellow light | select field | — | — | — | — | — | — |
| Alert sound | select field | — | — | — | — | — | — |
| Gate remains controlled | select field | — | — | — | — | — | — |
| Red light | select field | — | — | — | — | — | — |
| Denial sound | select field | — | — | — | — | — | — |
| Gate remains locked | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; calls `setValidationOutcomeGuest`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The validation outcome guest configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the validation outcome guest untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No validation outcome guest configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setValidationOutcomeGuest` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A custom welcome message and the venue's branding/logo show on the reader on a successful scan. *(client request · MoM 2 Sep 2026, 4.13 Turnstile Hardware & Handheld Scanner Configuration · DI-645)*
- Turnstile light/sound feedback is configurable: e.g. green light for an adult ticket, orange for a child ticket as a quick visual fraud check; some models play audio, including celebratory sounds (e.g. birthday visit). *(client request · MoM 2 Sep 2026, 4.13 Turnstile Hardware & Handheld Scanner Configuration · DI-644)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-198` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-198`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 8: Works in Validation Outcome & Guest Feedback Designer → Configure what the physical access device does and displays after validation. The matrix explicitly requires valid/non-valid messages, lights, pictograms and sounds, including green/yellow/red …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-198?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-199` Reader, Scanner & Peripheral Configuration

**Configure the technologies attached to a gate/device.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/reader-scanner-peripheral-configuration-bo-199` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
|  | scan target | — | — | — | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; carries `accessPointId`; calls `setReaderScannerPeripheral`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader scanner peripheral list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader scanner peripheral untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader scanner peripheral yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader scanner peripheral are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setReaderScannerPeripheral` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- No driver is ever installed on the workstation OS: drivers are built into the TICVAI app; staff only connect the device and test print/scan from within the app; new models are supported by a back-end driver update, not a code release. *(agreed · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-897)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-199` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-199`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 10: Works in Reader, Scanner & Peripheral Configuration → Configure the technologies attached to a gate/device.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-199?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-200` Handheld & Mobile Access Device Configuration

**Configure mobile access-control devices used by staff. The matrix explicitly requires handheld devices and Android/iOS dedicated mobile applications.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/handheld-mobile-access-device-configuration-bo-200` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Device type | select field | — | — | — | — | — | — |
| Android/iOS | select field | — | — | — | — | — | — |
| assigned venue | select field | — | — | — | — | — | — |
| assigned zone | select field | — | — | — | — | — | — |
| assigned operator group | select field | — | — | — | — | — | — |
| permitted operating modes | select field | — | — | — | — | — | — |
| offline capability | select field | — | — | — | — | — | — |
| scanner source | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Scan Ticket (primary button) | navigation or local | — | — | — | — |
| Search Ticket (secondary button) | navigation or local | — | — | — | — |
| Entry (secondary button) | navigation or local | — | — | — | — |
| Manual Attendance (secondary button) | navigation or local | — | — | — | — |
| Override (destructive button) | navigation or local | — | — | — | — |
| View History (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; calls `setHandheldMobileAccess`

**What opens over it**

- confirmDialog *Override*: **Override on a handheld mobile access is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The handheld mobile access configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the handheld mobile access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No handheld mobile access configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setHandheldMobileAccess` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Handheld scanners read QR, RFID or other supported media. Offline, devices validate locally from data embedded in the credential, queue the transactions and auto-sync when connectivity returns. *(agreed · MoM 2 Sep 2026, 4.13 / 4.14 Handheld Scanners & Offline Mode · DI-646)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-200` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-200`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 12: Works in Handheld & Mobile Access Device Configuration → Configure mobile access-control devices used by staff. The matrix explicitly requires handheld devices and Android/iOS dedicated mobile applications.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-200?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Scan Ticket, Search Ticket, Entry, Manual Attendance, Override, View History.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-201` Gate Modes, Free Spin & Emergency Controls

**Manage non-standard operational modes. The source specifically requires Free Spin and Drop Arm/Emergency behavior.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #20679 (APP-SETUP-BO-201) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/gate-modes-free-spin-emergency-controls-bo-201` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Who can activate | select field | — | — | — | — | — | — |
| Venue scope | select field | — | — | — | — | — | — |
| Gate group | select field | — | — | — | — | — | — |
| reason | select field | — | — | — | — | — | — |
| emergency code | select field | — | — | — | — | — | — |
| automatic notification | select field | — | — | — | — | — | — |

**Form: Save gate mode policy** (modal, opened by *Save gate mode policy*; *Save gate mode policy* calls `setGateModePolicy`, *Cancel* sends nothing)

**Collects what `setGateModePolicy` sends before it is called.** Required: `id`, `venueId`, `mode`, `scopePath`. Optional: `whoCanActivate`, `accessPointGroupId`, `reasonRequired`, `emergencyCode`, `automaticNotification`, `createsIncident`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setGateModePolicy` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setGateModePolicy` body |
| Mode `mode` | segmented control | required | — | Free flow · Drop arm | — | Non-standard operating mode governed (R221 vocabulary) | `setGateModePolicy` body |
| Who can activate `whoCanActivate` | list of values (chips) | optional | — | — | — | Roles allowed to activate this mode | `setGateModePolicy` body |
| Access point group `accessPointGroupId` | picker: choose an access point group | optional | — | — | shows names, sends the id | Gate group the policy applies to (access.access_point_group); null for the whole venue | `setGateModePolicy` body |
| Reason required `reasonRequired` | toggle | optional | on | — | — | — | `setGateModePolicy` body |
| Emergency code `emergencyCode` | text field | optional | — | — | — | — | `setGateModePolicy` body |
| Automatic notification `automaticNotification` | toggle | optional | off | — | — | — | `setGateModePolicy` body |
| Creates incident `createsIncident` | toggle | optional | off | — | — | Activation creates an incident record | `setGateModePolicy` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setGateModePolicy` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save gate mode policy (primary button) | `setGateModePolicy` PUT `/gate-mode-policies` | AccessGateModePolicy | AccessGateModePolicy | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Data it reads**: `listGateModeFree` (onLoad, Gate Modes, Free Spin & Emergency Controls)

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; calls `listGateModeFree`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gate modes free configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gate modes free untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gate modes free configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listGateModeFree` → `SCOPE_VIEW` (read) · staff
- `setGateModePolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A69** Implement duplicate-account detection and profile-merge functionality (consolidating two profiles into one, carrying over the combined transaction history) *(Softlabs Backend Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Aug 2026 · workshop tracker · keyword 'duplicate-account')*
- **A90** Implement consent-gated duplicate merge (fuzzy name / exact mobile / exact email matching, customer confirmation required, admin review queue, login-of-record rule) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'duplicate merge')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-201` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-201`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 14: Works in Gate Modes, Free Spin & Emergency Controls → Manage non-standard operational modes. The source specifically requires Free Spin and Drop Arm/Emergency behavior.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-201?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save gate mode policy.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-202` Device Software, Content & Remote Configuration

**Centrally control access-control device software and guest-facing configuration. The source requires the ability to configure/manage software on turnstiles, add external webpages on supported screens, and enable payment technologies where available.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/device-software-content-remote-configuration-bo-202` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Welcome page | select field | — | — | — | — | — | — |
| Instructions | select field | — | — | — | — | — | — |
| Ticket status | select field | — | — | — | — | — | — |
| Reason message | select field | — | — | — | — | — | — |
| Promotional information | select field | — | — | — | — | — | — |
| External approved webpage | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Returns to the board's landing screen*; calls `setDeviceSoftwareContent`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The device software content configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the device software content untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No device software content configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setDeviceSoftwareContent` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Firmware: package library per device; compatibility rules limit deployment to compatible models; update wizard with phased/scheduled rollout; live monitor flags failures (e.g. device offline at deployment); rollback and update history. *(client request · MoM 15 Sep 2026, 4.7 Firmware & Software Management · DI-903)*
- Remote configuration deploys a device type's settings (e.g. receipt printers) to many workstations in one action; configuration versions can be compared and rolled back. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-898)*
- No driver is ever installed on the workstation OS: drivers are built into the TICVAI app; staff only connect the device and test print/scan from within the app; new models are supported by a back-end driver update, not a code release. *(agreed · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-897)*
- A custom welcome message and the venue's branding/logo show on the reader on a successful scan. *(client request · MoM 2 Sep 2026, 4.13 Turnstile Hardware & Handheld Scanner Configuration · DI-645)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-202` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-202`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 16: Works in Device Software, Content & Remote Configuration → Centrally control access-control device software and guest-facing configuration. The source requires the ability to configure/manage software on turnstiles, add external webpages on supported …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-202?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-203` Hardware Compatibility, Health, Testing & Deployment

**Provide the final testing and governance layer before hardware is used in production. The matrix says venues may select their hardware, while the provider must expose hardware limitations and recommendations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `DEVICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/hardware-compatibility-health-testing-deployment-bo-203` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Sent by *Deploy configuration version*** (`publishHardwareDeployment`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated deployment id | `publishHardwareDeployment` body |
| Configuration version `configurationVersion` | text field | required | — | — | — | The access configuration version being deployed | `publishHardwareDeployment` body |
| Target scope `targetScope` | radio group | required | — | Pilot · Selected gates · Device group · Venue | — | — | `publishHardwareDeployment` body |
| Venue `venueId` | text field | required | — | — | — | — | `publishHardwareDeployment` body |
| Gates `gateIds` | list of values (chips) | optional | — | — | — | Required for pilot and selectedGates | `publishHardwareDeployment` body |
| Device group `deviceGroupId` | text field | optional | — | — | — | Required for deviceGroup | `publishHardwareDeployment` body |
| Run compatibility test first `runCompatibilityTestFirst` | toggle | optional | on | — | — | Devices that fail the compatibility test are skipped and named in the result | `publishHardwareDeployment` body |
| Scheduled at `scheduledAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Empty deploys now | `publishHardwareDeployment` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Selected gates (primary button) | navigation or local | — | — | — | — |
| device group (secondary button) | navigation or local | — | — | — | — |
| venue (secondary button) | navigation or local | — | — | — | — |
| Deploy configuration version (publish gate) | `publishHardwareDeployment` POST `/hardware-deployments` | HardwareDeploymentInput | HardwareDeploymentView | 409 A deployment to an overlapping target set is still queued or in progress; 422 gateIds or deviceGroupId missing for the chosen targetScope | — |

**Data it reads**: `listHardwareCompatibilityHealth` (onLoad, Hardware Compatibility, Health, Testing & Deployment)

**Where the user goes next**

- → `BO-194` Device & Gate Command Center: *Device & Gate Command Center*; carries `deviceId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The hardware compatibility health list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the hardware compatibility health untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No hardware compatibility health yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the hardware compatibility health are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A deployment to an overlapping target set is still queued or in progress; 422 gateIds or deviceGroupId missing for the chosen targetScope |

#### Permissions

- `listHardwareCompatibilityHealth` → `DEVICE_VIEW` (read) · staff
- `publishHardwareDeployment` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Device analytics: total/active/inactive devices across venues (multi-tenant) with location breakdown; health, availability, fault rate and top failure reasons (communication timeout, device offline, invalid response, power issue, firmware error); SLA tracking for devices in extended maintenance. *(client request · MoM 15 Sep 2026, 4.9 Device Integration & Operation Analytics · DI-905)*
- **Open question.** Open (Allam): physical tamper detection - lock out communication if a device is opened, as bank payment terminals do - worth evaluating per device type; not a requirement for every device. *(open · MoM 15 Sep 2026, 4.8 Device Security & Governance · DI-904)*
- Device maintenance: preventive cycles (quarterly, half-yearly, seasonal) on a calendar by device type; staff log faulty devices which raise work orders; diagnostic workspace for the engineer; warranty and maintenance history; return to service. *(client request · MoM 15 Sep 2026, 4.6 Device Maintenance & Lifecycle Servicing · DI-902)*
- Performance monitoring shows successful vs failed validations and scan response time; configurable alert rules (e.g. low battery, device offline) with escalation for unresolved alerts. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-901)*
- **Open question.** Open: can health metrics such as handheld battery be read via the manufacturer's SDK in-app rather than by physical inspection? Depends on each vendor SDK; to confirm during integration. *(open · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-900)*
- One screen shows live online/offline status of every workstation and device (printers, turnstiles, handheld scanners); a 360 health view shows connectivity, CPU/memory, storage and temperature. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-899)*
- Media compatibility testing validates that each supported media type works at each gate/device before go-live. *(client request · MoM 2 Sep 2026, 4.9 Media & Credential Configuration · DI-639)*
- Real-time health view of device connectivity. Device-pushed events (anti-passback attempts, power loss, network loss) are surfaced as alerts and reports, e.g. notifying the operations team when a turnstile goes offline. *(agreed · MoM 2 Sep 2026, 4.1 / 4.2 Health Monitoring & Alerts · DI-625)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-203` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS23 Access Control Board 6.dc.html#bo-203`
- Workshop pack: Access Control Module_Reference.pdf board 6
- Flow F116 *Access Control board 6: Device & Gate Command Center*, step 18: Works in Hardware Compatibility, Health, Testing & Deployment → Provide the final testing and governance layer before hardware is used in production. The matrix says venues may select their hardware, while the provider must expose hardware limitations and …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-203?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Selected gates, device group, venue, Deploy configuration version.
- [ ] Every transition is wired: `BO-194`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `DEVICE_VIEW`.
- [ ] The 8 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**33 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listAccessPoints": {"method":"GET","path":"/access-points","contract":"access","summary":"List access points","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDeviceGate": {"method":"GET","path":"/device-gate","contract":"access","summary":"Device & Gate Command Center","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDeviceTypeHardware": {"method":"GET","path":"/device-type-hardware","contract":"access","summary":"Device Type & Hardware Library","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DeviceTypeHardwareLibraryView"},
"listGateModeFree": {"method":"GET","path":"/gate-mode-free","contract":"access","summary":"Gate Modes, Free Spin & Emergency Controls","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GateModesFreeSpinEmergencyControlsView"},
"listHardwareCompatibilityHealth": {"method":"GET","path":"/hardware-compatibility-health","contract":"access","summary":"Hardware Compatibility, Health, Testing & Deployment","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPhysicalDeviceRegistration": {"method":"GET","path":"/physical-device-registration","contract":"access","summary":"Physical Device Registration & Provisioning","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"placeAccessDevice": {"method":"POST","path":"/device-placements","contract":"access","summary":"Place a registered device in the gate topology","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessDevicePlacement","responds":"AccessDevicePlacement"},
"publishHardwareDeployment": {"method":"POST","path":"/hardware-deployments","contract":"access","summary":"Deploy a gate configuration version","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"HardwareDeploymentInput","responds":"HardwareDeploymentView"},
"registerDevice": {"method":"POST","path":"/devices","contract":"tenancy","summary":"Register a device","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RegisteredDevice","responds":"RegisteredDevice"},
"setDeviceSoftwareContent": {"method":"PUT","path":"/device-software-content","contract":"access","summary":"Device Software, Content & Remote Configuration","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DeviceSoftwareContentRemoteConfigurationInput","responds":"DeviceSoftwareContentRemoteConfigurationView"},
"setGateModePolicy": {"method":"PUT","path":"/gate-mode-policies","contract":"access","summary":"Set a policy for a non-standard gate mode","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessGateModePolicy","responds":"AccessGateModePolicy"},
"setHandheldMobileAccess": {"method":"PUT","path":"/handheld-mobile-access","contract":"access","summary":"Handheld & Mobile Access Device Configuration","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"HandheldMobileAccessDeviceConfigurationInput","responds":"HandheldMobileAccessDeviceConfigurationView"},
"setHardwareModel": {"method":"PUT","path":"/hardware-models","contract":"access","summary":"Create or replace a hardware model in the library","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessHardwareModel","responds":"AccessHardwareModel"},
"setReaderScannerPeripheral": {"method":"PUT","path":"/reader-scanner-peripheral","contract":"access","summary":"Reader, Scanner & Peripheral Configuration","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ReaderScannerPeripheralConfigurationInput","responds":"ReaderScannerPeripheralConfigurationView"},
"setTurnstileLaneBehavior": {"method":"PUT","path":"/turnstile-lane-behavior","contract":"access","summary":"Turnstile & Lane Behavior Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TurnstileLaneBehaviorConfigurationInput","responds":"TurnstileLaneBehaviorConfigurationView"},
"setTurnstileMode": {"method":"PUT","path":"/access-points/{accessPointId}/mode","contract":"access","summary":"Set the operating mode of an access point","permission":"TURNSTILE_MODE_SET","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessPoint"},
"setValidationOutcomeGuest": {"method":"PUT","path":"/validation-outcome-guest","contract":"access","summary":"Validation Outcome & Guest Feedback Designer","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ValidationOutcomeGuestFeedbackDesignerInput","responds":"ValidationOutcomeGuestFeedbackDesignerView"},
"updateAccessDevicePlacement": {"method":"PUT","path":"/device-placements/{placementId}","contract":"access","summary":"Replace a device's placement","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessDevicePlacement","responds":"AccessDevicePlacement"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessDevicePlacement": {"type":"object","x-ticvai-persistence":"access.device_placement","description":"**Where one registered device is placed in the gate topology, and nothing else about it** (ADR-0067, accepted 1 October). The device itself (kind and hardware type, hardware model, serial, every version, health, heartbeat and its one lifecycle) is `platform.device`, the only device register, owned and migrated by Tenancy and registered with tenancy `registerDevice`. This row names that device (`deviceId`) and says which access area, access point and lane it serves, in what role, at what proximity threshold for a beacon, and through which controller. Access reads device facts only through what Tenancy publishes (`getDevice`, `listDevices`), never with its own SQL.\n\n**Access's provisioning stages are a checklist on the placement, not a second lifecycle** (`provisioningChecklist`). Placed with `placeAccessDevice` and changed with `updateAccessDevicePlacement`. Was `access.access_device` (renamed 1 October, ADR-0067), which repeated the register's serial, versions, health and lifecycle; `device.enrolmentChanged` no longer keeps two registers in step. Not `access.device_binding`, which binds a guest's phone to an entitlement. `deviceGroupId` is a free deployment label, not a key (decided 29 September, writers pass).","required":["id","venueId","deviceId","role","isActive","scopePath"],"properties":{"id":{"$ref":"../shared/common.yaml#/components/schemas/Id"},"venueId":{"type":"string","format":"uuid"},"deviceId":{"type":"string","format":"uuid","x-ticvai-references":"platform.device","description":"The registered device placed here (`platform.device`, tenancy `registerDevice`). One active placement per device; replacing a failed unit gives its placement the new `deviceId`."},"accessAreaId":{"type":"string","format":"uuid","nullable":true,"description":"Most specific park, zone or attraction the device sits in (access.access_area)"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Access point (gate) the device serves"},"gateLaneId":{"type":"string","format":"uuid","nullable":true,"description":"Lane the device is mounted on (access.gate_lane)"},"role":{"type":"string","enum":["entry","exit","entryAndExit","validationOnly","proximity","monitoring"],"default":"entryAndExit","description":"What the device does at this place. `proximity` is a beacon; `monitoring` a camera controller that decides nothing."},"name":{"type":"string","nullable":true,"description":"Label at this place, e.g. Gate A, HH-01"},"deviceGroupId":{"type":"string","nullable":true,"description":"Device group the placement belongs to, as targeted by hardware deployments and device configurations"},"controllerReference":{"type":"string","nullable":true},"proximityThresholdMeters":{"type":"integer","minimum":0,"nullable":true,"description":"Beacons only: activation distance in metres"},"installationDate":{"type":"string","format":"date","nullable":true},"provisioningChecklist":{"type":"object","description":"**Access's provisioning stages, as a checklist on the placement** (ADR-0067). Each item is the time the step was confirmed, null until it is. The device's lifecycle (registered, enrolled, provisioned, active, deactivated, retired) is `platform.device.enrolment_state`, not this.","properties":{"hardwareProfileAssignedAt":{"type":"string","format":"date-time","nullable":true},"locationAssignedAt":{"type":"string","format":"date-time","nullable":true},"authenticatedAt":{"type":"string","format":"date-time","nullable":true},"configurationDownloadedAt":{"type":"string","format":"date-time","nullable":true},"securityPackageDownloadedAt":{"type":"string","format":"date-time","nullable":true},"connectivityTestedAt":{"type":"string","format":"date-time","nullable":true}}},"isActive":{"type":"boolean","default":true,"description":"Whether this placement is in use (beacons: activeInactive). A device that is `retired` or `deactivated` in the register is refused at the gate whatever this says."},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessGateModePolicy": {"type":"object","x-ticvai-persistence":"access.gate_mode_policy","description":"One policy for a non-standard gate mode (free spin or count only as freeFlow, emergency as dropArm): who may activate it, on which gate group, whether a reason is required, emergency code, notification and incident creation (declared 29 September, data-model close-out DM1)","required":["id","venueId","mode","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"mode":{"type":"string","enum":["freeFlow","dropArm"],"description":"Non-standard operating mode governed (R221 vocabulary)"},"whoCanActivate":{"type":"array","items":{"type":"string"},"description":"Roles allowed to activate this mode"},"accessPointGroupId":{"type":"string","format":"uuid","nullable":true,"description":"Gate group the policy applies to (access.access_point_group); null for the whole venue"},"reasonRequired":{"type":"boolean","default":true},"emergencyCode":{"type":"string","nullable":true},"automaticNotification":{"type":"boolean","default":false},"createsIncident":{"type":"boolean","default":false,"description":"Activation creates an incident record"},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessHardwareModel": {"type":"object","x-ticvai-persistence":"access.hardware_model","description":"One hardware model in the reusable library, independent of deployed devices: manufacturer, model, category and type, supported technologies, connectivity, capability flags and firmware information (declared 29 September, data-model close-out DM1)","required":["id","manufacturer","model","deviceCategory","hardwareType","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"manufacturer":{"type":"string"},"model":{"type":"string"},"deviceCategory":{"type":"string","enum":["turnstile","specialGate","mobile","reader","other"]},"hardwareType":{"$ref":"../shared/common.yaml#/components/schemas/DeviceHardwareType"},"supportedTechnologies":{"type":"array","items":{"type":"string"}},"connectivity":{"type":"array","items":{"type":"string"}},"offlineCapability":{"type":"boolean","default":false},"screenCapability":{"type":"boolean","default":false},"soundCapability":{"type":"boolean","default":false},"lightCapability":{"type":"boolean","default":false},"relayControllerSupport":{"type":"boolean","default":false},"paymentCapability":{"type":"boolean","default":false,"description":"Payment capability where available"},"firmwareSoftwareInformation":{"type":"string","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessPoint": {"x-ticvai-persistence":"access.access_point","type":"object","required":["id","code","name","venueId","operatingMode","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"externalCredentialSources":{"allOf":[{"$ref":"#/components/schemas/ExternalCredentialSourceList"}],"description":"BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"},"scanAnomalyRules":{"allOf":[{"$ref":"#/components/schemas/ScanAnomalyRuleList"}],"description":"BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"},"operatingMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"default":"normal","description":"**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"},"vehicleLocationCapture":{"type":"boolean","default":false,"description":"BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"},"mode":{"allOf":[{"$ref":"#/components/schemas/TurnstileMode"}],"nullable":true,"description":"Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"},"direction":{"allOf":[{"$ref":"#/components/schemas/Direction"}],"description":"**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n"},"antiPassbackEnabled":{"type":"boolean"},"requiresExitBeforeReentry":{"type":"boolean","default":false,"description":"Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."},"driver":{"type":"string","nullable":true,"description":"Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"},"geofence":{"allOf":[{"$ref":"#/components/schemas/AccessPointGeofence"}],"nullable":true,"description":"Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"},"isActive":{"type":"boolean"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true}}},
"AccessPointGeofence": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n","required":["enforcement"],"properties":{"latitude":{"type":"number"},"longitude":{"type":"number"},"radiusMetres":{"type":"integer","minimum":5,"maximum":5000},"enforcement":{"type":"string","enum":["off","warn","deny"],"description":"`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"},"allowProximityBeacon":{"type":"boolean","description":"Accept a BLE proximity assertion in place of GPS. Better indoors."}}},
"AccessPointOperatingMode": {"type":"string","description":"BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"]},
"DeviceCapability": {"type":"string","description":"BL-179. **Something a driver reports, not something the platform provides.** The list grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a driver plus configuration rather than a core change.\n**`genderClassification` is here because `VenueSettings.segregatedAccess. genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch with no driver behind it. Where a venue's access hardware performs the check and the venue chooses to use it, the result is **advisory to the steward and never decisive at the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package deviates deliberately and CF-130 records why.\n**Access's capabilities merged in** (ADR-0067, 1 October): `dynamicQr`, `rfid`, `nfc`, `facePass`, `offline` and `heightCheck` were the access register's own list, from the compatibility matrix.\n","enum":["genderClassification","dynamicQr","rfid","nfc","facePass","offline","heightCheck"]},
"DeviceGateCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Device & Gate Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"connectivity":{"type":"string","description":"connectivity"},"lastHeartbeat":{"type":"string","format":"date-time","description":"last heartbeat"},"configurationVersion":{"type":"string","description":"configuration version"},"localRuleVersion":{"type":"string","description":"local rule version"},"credentialSecurityPackageVersion":{"type":"string","description":"credential/security package version"},"scannerHealth":{"type":"string","description":"scanner health"},"controllerHealth":{"type":"string","description":"controller health"},"cameraHealthWhereApplicable":{"type":"string","description":"camera health where applicable"},"deviceId":{"type":"string"},"deviceType":{"type":"string","description":"e.g. Turnstile, VIP Gate, Handheld, Reader"},"accessPointId":{"type":"string"},"mode":{"type":"string","description":"Current operating mode"},"status":{"type":"string","enum":["healthy","active","degraded","offline","localMode"]}}},
"DeviceGateCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"totalDevices":{"type":"integer","description":"Total Devices"},"online":{"type":"integer","description":"Online"},"offline":{"type":"integer","description":"Offline"},"degraded":{"type":"integer","description":"Degraded"},"turnstiles":{"type":"integer","description":"Turnstiles"},"handhelds":{"type":"integer","description":"Handhelds"},"biometricReaders":{"type":"integer","description":"Biometric Readers"},"rfidNfcReaders":{"type":"integer","description":"RFID/NFC Readers"},"gatesOpen":{"type":"integer","description":"Gates Open"},"gatesClosed":{"type":"integer","description":"Gates Closed"},"devicesRequiringSync":{"type":"integer","description":"Devices Requiring Sync"},"firmwareSoftwareExceptions":{"type":"integer","description":"Firmware/Software Exceptions"},"hardwareAlerts":{"type":"integer","description":"Hardware Alerts"},"ai":{"type":"array","items":{"type":"string"},"description":"Advisory AI findings, e.g. a gate with a high scan-failure rate. Read-only."}}},
"DeviceKind": {"type":"string","enum":["receiptPrinter","ticketPrinter","labelPrinter","cashDrawer","barcodeScanner","rfidReader","nfcReader","cardReader","idReader","biometricReader","accessReader","paymentTerminal","customerDisplay","signageDisplay","kitchenDisplay","turnstileController","wristbandEncoder","signaturePad","scale","camera","mobileHandset","handheldScanner","accessPodium","bleBeacon"],"description":"`mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation.\n**One kind vocabulary for every device** (ADR-0067, 1 October). `handheldScanner`, `accessPodium` and `bleBeacon` came from Access's register; the finer hardware type (a speed gate under `turnstileController`, a tablet under `handheldScanner`) is `RegisteredDevice.hardwareType` (common `DeviceHardwareType`).\n"},
"DeviceSoftwareContentRemoteConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Device Software, Content & Remote Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"deviceGroupId":{"type":"string","description":"Target device group"},"venueId":{"type":"string"},"configurationId":{"type":"string"},"deviceSettings":{"type":"string","description":"Device settings"},"gateMode":{"type":"string","description":"Gate mode"},"readerSettings":{"type":"string","description":"Reader settings"},"mediaProfiles":{"type":"array","items":{"type":"string"},"description":"Media profiles"},"outcomeProfiles":{"type":"array","items":{"type":"string"},"description":"Outcome profiles"},"language":{"type":"string","description":"Language"},"uiContent":{"type":"string","description":"UI content"},"localRules":{"type":"string","description":"Local rules"},"offlineSecurityConfiguration":{"type":"string","description":"Offline security package reference"},"welcomePage":{"type":"string","description":"Welcome page"},"instructions":{"type":"string","description":"Instructions"},"ticketStatus":{"type":"string","description":"Ticket status"},"reasonMessage":{"type":"string","description":"Reason message"},"promotionalInformation":{"type":"string","description":"Promotional information"},"externalApprovedWebpage":{"type":"string","description":"External approved webpage"},"emergencyInformation":{"type":"string","description":"Emergency information"},"version":{"type":"string","description":"Configuration version, for rollback"},"deploymentStage":{"type":"string","enum":["draft","testDevice","deviceGroup","venueRollout"]}},"required":["configurationId","venueId","deviceGroupId"]},
"DeviceSoftwareContentRemoteConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Device Software, Content & Remote Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"deviceGroupId":{"type":"string","description":"Target device group"},"venueId":{"type":"string"},"configurationId":{"type":"string"},"deviceSettings":{"type":"string","description":"Device settings"},"gateMode":{"type":"string","description":"Gate mode"},"readerSettings":{"type":"string","description":"Reader settings"},"mediaProfiles":{"type":"array","items":{"type":"string"},"description":"Media profiles"},"outcomeProfiles":{"type":"array","items":{"type":"string"},"description":"Outcome profiles"},"language":{"type":"string","description":"Language"},"uiContent":{"type":"string","description":"UI content"},"localRules":{"type":"string","description":"Local rules"},"offlineSecurityConfiguration":{"type":"string","description":"Offline security package reference"},"welcomePage":{"type":"string","description":"Welcome page"},"instructions":{"type":"string","description":"Instructions"},"ticketStatus":{"type":"string","description":"Ticket status"},"reasonMessage":{"type":"string","description":"Reason message"},"promotionalInformation":{"type":"string","description":"Promotional information"},"externalApprovedWebpage":{"type":"string","description":"External approved webpage"},"emergencyInformation":{"type":"string","description":"Emergency information"},"version":{"type":"string","description":"Configuration version, for rollback"},"deploymentStage":{"type":"string","enum":["draft","testDevice","deviceGroup","venueRollout"]}},"required":["configurationId","venueId","deviceGroupId"]},
"DeviceTypeHardwareLibraryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Device Type & Hardware Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"hardwareType":{"type":"string","enum":["standardTurnstile","fullHeightTurnstile","tripodTurnstile","speedGate","wideLane","accessiblePodGate","buggyGate","vipGate","staffGate","androidHandheld","iosDevice","tablet","qrBarcodeReader","rfidReader","nfcReader","multiTechnologyReader","biometricReader","podium","counter","beacon","cameraController","externalAccessDevice"],"description":"Specific hardware type within the device category"},"manufacturer":{"type":"string","description":"Manufacturer"},"model":{"type":"string","description":"Model"},"deviceCategory":{"type":"string","enum":["turnstile","specialGate","mobile","reader","other"],"description":"Device Category"},"supportedTechnologies":{"type":"array","items":{"type":"string"},"description":"Supported technologies"},"connectivity":{"type":"array","items":{"type":"string"},"description":"Connectivity"},"offlineCapability":{"type":"boolean","description":"Offline capability"},"screenCapability":{"type":"boolean","description":"Screen capability"},"soundCapability":{"type":"boolean","description":"Sound capability"},"lightCapability":{"type":"boolean","description":"Light capability"},"relayControllerSupport":{"type":"boolean","description":"Relay/controller support"},"paymentCapabilityWhereAvailable":{"type":"boolean","description":"payment capability where available"},"firmwareSoftwareInformation":{"type":"string","description":"firmware/software information"},"hardwareModelId":{"type":"string"}}},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"ExternalCredentialSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["hotelRoomCard","corporateBadge","cityPass","transitCard","partnerToken"]},"providerName":{"type":"string"},"endpoint":{"type":"string"},"credentialRef":{"type":"string"},"grantsProductId":{"type":"string","format":"uuid"}}}},
"GateModesFreeSpinEmergencyControlsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Gate Modes, Free Spin & Emergency Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"whoCanActivate":{"type":"array","items":{"type":"string"},"description":"Roles allowed to activate this mode"},"venueScope":{"type":"string","description":"Venue scope"},"gateGroup":{"type":"string","description":"Gate group"},"reasonRequired":{"type":"string","description":"reason"},"emergencyCode":{"type":"string","description":"emergency code"},"automaticNotification":{"type":"boolean","description":"automatic notification"},"incidentRecord":{"type":"boolean","description":"Activation creates an incident record"},"policyId":{"type":"string"},"mode":{"type":"string","enum":["freeFlow","dropArm"],"description":"Non-standard operating mode this policy governs (R221 vocabulary): freeFlow covers free spin and count only, dropArm is the emergency mode"}}},
"HandheldMobileAccessDeviceConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Handheld & Mobile Access Device Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"name":{"type":"string","description":"e.g. Standard Attendant, Supervisor"},"profileId":{"type":"string","description":"Handheld configuration profile identifier"},"deviceType":{"type":"string","description":"Device type"},"platform":{"type":"string","enum":["android","ios"],"description":"Android/iOS"},"assignedVenue":{"type":"string","description":"assigned venue"},"assignedZone":{"type":"string","description":"assigned zone"},"assignedOperatorGroup":{"type":"string","description":"assigned operator group"},"permittedOperatingModes":{"type":"array","items":{"type":"string"},"description":"permitted operating modes"},"offlineCapability":{"type":"boolean","description":"offline capability"},"scannerSource":{"type":"string","description":"scanner source"},"biometricCapabilityWhereSupported":{"type":"boolean","description":"biometric capability where supported"},"enabledFunctions":{"type":"array","items":{"type":"string","enum":["scanTicket","searchTicket","entry","exit","reEntry","crossover","groupAdmission","manualAttendance","override","viewHistory","changeDeviceMode"]},"description":"Functions enabled for this device role"}},"required":["profileId","name"]},
"HandheldMobileAccessDeviceConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Handheld & Mobile Access Device Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string","description":"e.g. Standard Attendant, Supervisor"},"profileId":{"type":"string","description":"Handheld configuration profile identifier"},"deviceType":{"type":"string","description":"Device type"},"platform":{"type":"string","enum":["android","ios"],"description":"Android/iOS"},"assignedVenue":{"type":"string","description":"assigned venue"},"assignedZone":{"type":"string","description":"assigned zone"},"assignedOperatorGroup":{"type":"string","description":"assigned operator group"},"permittedOperatingModes":{"type":"array","items":{"type":"string"},"description":"permitted operating modes"},"offlineCapability":{"type":"boolean","description":"offline capability"},"scannerSource":{"type":"string","description":"scanner source"},"biometricCapabilityWhereSupported":{"type":"boolean","description":"biometric capability where supported"},"enabledFunctions":{"type":"array","items":{"type":"string","enum":["scanTicket","searchTicket","entry","exit","reEntry","crossover","groupAdmission","manualAttendance","override","viewHistory","changeDeviceMode"]},"description":"Functions enabled for this device role"}},"required":["profileId","name"]},
"HardwareCompatibilityHealthTestingDeploymentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Hardware Compatibility, Health, Testing & Deployment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"deviceId":{"type":"string","description":"Device identifier"},"capabilities":{"type":"array","items":{"type":"string","enum":["dynamicQr","rfid","nfc","facePass","offline","heightCheck"]},"description":"Capabilities this device supports, from the compatibility matrix"},"rolloutScope":{"type":"string","enum":["pilot","selectedGates","deviceGroup","venue"],"description":"How far the production rollout of this device reaches"},"deviceName":{"type":"string","description":"Device or gate name, e.g. Gate A, HH-01"},"lifecycleStatus":{"type":"string","enum":["registered","configured","tested","approved","production"],"description":"Certification stage; no device enters production until validated"}},"required":["deviceId"]},
"HardwareDeploymentInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"Deploy one gate configuration version to a target set (decided 29 September, VM close-out).","required":["id","configurationVersion","targetScope","venueId"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated deployment id"},"configurationVersion":{"type":"string","description":"The access configuration version being deployed"},"targetScope":{"type":"string","enum":["pilot","selectedGates","deviceGroup","venue"]},"venueId":{"type":"string"},"gateIds":{"type":"array","items":{"type":"string"},"description":"Required for pilot and selectedGates"},"deviceGroupId":{"type":"string","description":"Required for deviceGroup"},"runCompatibilityTestFirst":{"type":"boolean","default":true,"description":"Devices that fail the compatibility test are skipped and named in the result"},"scheduledAt":{"type":"string","format":"date-time","description":"Empty deploys now"}}},
"HardwareDeploymentView": {"type":"object","x-ticvai-persistence":"access.hardware_deployment","description":"**One rollout of one gate configuration version to one target set** (decided 29 September, VM close-out). The lifecycle is the one `tenancy.ProfileDeployment` uses for configuration profiles, so a partial failure is visible and retried or rolled back, never an end state.","required":["id","configurationVersion","targetScope","status"],"properties":{"id":{"type":"string","format":"uuid"},"configurationVersion":{"type":"string"},"targetScope":{"type":"string","enum":["pilot","selectedGates","deviceGroup","venue"]},"venueId":{"type":"string"},"gateIds":{"type":"array","items":{"type":"string"}},"deviceGroupId":{"type":"string"},"status":{"type":"string","enum":["queued","inProgress","completed","partiallyFailed","rolledBack"]},"devicesTargeted":{"type":"integer"},"devicesAcknowledged":{"type":"integer"},"failedDeviceIds":{"type":"array","items":{"type":"string"},"description":"Devices that failed the compatibility test or did not acknowledge"},"requestedByPrincipalId":{"type":"string"},"requestedAt":{"type":"string","format":"date-time"},"scheduledAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"The partition key (ADR-0005). Written at venue scope"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PhysicalDeviceRegistrationProvisioningView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Physical Device Registration & Provisioning displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"deviceId":{"type":"string","description":"Device ID"},"serialNumber":{"type":"string","description":"Serial Number"},"hardwareModel":{"type":"string","description":"Hardware Model"},"manufacturer":{"type":"string","description":"Manufacturer"},"tenantId":{"type":"string","description":"Tenant"},"venueId":{"type":"string","description":"Venue"},"parkId":{"type":"string","description":"Park"},"zoneId":{"type":"string","description":"Zone"},"accessPointId":{"type":"string","description":"Access Point"},"gateLane":{"type":"string","description":"Gate/Lane"},"ipNetworkReference":{"type":"string","description":"IP/network reference"},"controllerReference":{"type":"string","description":"controller reference"},"installationDate":{"type":"string","format":"date","description":"installation date"},"provisioningStage":{"type":"string","enum":["registered","hardwareProfileAssigned","locationAssigned","authenticated","configurationDownloaded","securityPackageDownloaded","connectivityTested","active"]}}},
"ReaderScannerPeripheralConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Reader, Scanner & Peripheral Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"accessPointId":{"type":"string","description":"Gate or device the peripherals attach to"},"readers":{"type":"array","items":{"type":"string"},"description":"Attached readers, e.g. qrBarcode, rfid, nfc, biometricCamera, paymentReader, heightSensor"},"verificationPriority":{"type":"array","items":{"type":"string"},"description":"Order methods are tried, e.g. facePass, dynamicQr, rfid, nfc"},"rfidRange":{"type":"string","enum":["near","medium","far"]},"heightVerificationEnabled":{"type":"boolean","description":"Height check for junior tickets; without a supported sensor the result is yellow for operator verification"},"capabilityWarnings":{"type":"array","items":{"type":"string"},"description":"Configured checks the attached hardware cannot perform"}},"required":["accessPointId"]},
"ReaderScannerPeripheralConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Reader, Scanner & Peripheral Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"accessPointId":{"type":"string","description":"Gate or device the peripherals attach to"},"readers":{"type":"array","items":{"type":"string"},"description":"Attached readers, e.g. qrBarcode, rfid, nfc, biometricCamera, paymentReader, heightSensor"},"verificationPriority":{"type":"array","items":{"type":"string"},"description":"Order methods are tried, e.g. facePass, dynamicQr, rfid, nfc"},"rfidRange":{"type":"string","enum":["near","medium","far"]},"heightVerificationEnabled":{"type":"boolean","description":"Height check for junior tickets; without a supported sensor the result is yellow for operator verification"},"capabilityWarnings":{"type":"array","items":{"type":"string"},"description":"Configured checks the attached hardware cannot perform"}},"required":["accessPointId"]},
"RegisteredDevice": {"x-ticvai-persistence":"platform.device","type":"object","description":"**The only device register** (ADR-0067, accepted 1 October; the register of record since 29 September). Identity (kind, hardware type, model, serial), every version (firmware, configuration, rule package, credential package), health, heartbeat and one lifecycle (`enrolmentState`: registered, enrolled, provisioned, active, deactivated, retired) for every device in the estate live on this row. The access-control device row, which repeated serial, versions, health and lifecycle, is now `access.device_placement` and holds only where an access-control device is placed. Tenancy owns and migrates this table; Access reads it only through this contract.\n","required":["id","kind","driver"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015).\n"},"identifier":{"type":"string","nullable":true},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control device (one with a `hardwareType`), which is placed in the gate topology by access `placeAccessDevice` rather than bound to a workstation (ADR-0067); `registerDevice` refuses either mistake with `422`.\n"},"model":{"type":"string","nullable":true},"hardwareType":{"$ref":"../shared/common.yaml#/components/schemas/DeviceHardwareType","nullable":true,"description":"**The specific hardware under `kind`** (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into the one register. Null for a device with no finer type than its kind.\n"},"hardwareModelId":{"type":"string","format":"uuid","nullable":true,"description":"The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it.\n"},"serialNumber":{"type":"string","nullable":true,"maxLength":100,"description":"The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). A serial already registered in the tenant is refused `409` by `registerDevice`.\n"},"ipNetworkReference":{"type":"string","nullable":true,"description":"Network address or reference the device is reached at (ADR-0067)."},"configurationVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Access configuration version the device reports running (ADR-0067)."},"localRuleVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Admission rule package the device reports running (ADR-0067)."},"credentialSecurityPackageVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Credential security package the device reports running (ADR-0067)."},"scannerHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Component health as the device or vendor reports it on its heartbeat (ADR-0067)."},"controllerHealth":{"type":"string","nullable":true,"readOnly":true},"cameraHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Where the device has a camera."},"connectivity":{"type":"string","nullable":true,"readOnly":true,"description":"Reported connectivity."},"pushToken":{"type":"string","format":"password","nullable":true,"writeOnly":true,"description":"BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only, and marked `writeOnly`: accepted by `registerDevice` and never returned by `listDevices` or `getDevice`. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"},"pushPlatform":{"type":"string","nullable":true,"enum":["ios","android","web","windows"]},"pushFailureCount":{"type":"integer","default":0,"readOnly":true,"description":"**Consecutive failures.** A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a notification queue fills with nothing.\n"},"offlineScope":{"type":"string","nullable":true,"enum":["none","readOnly","sellAndScan","fullVenue"],"description":"BL-163. **What this device may do with no connection**, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled.\n**`fullVenue` on a personal handset is a decision, not a default** — a device that can do everything offline is a device that carries the whole venue's data in somebody's pocket.\n"},"firmwareVersion":{"type":"string","nullable":true,"readOnly":true,"description":"As the device last reported it on its heartbeat."},"isRequired":{"type":"boolean","description":"True blocks shift open when the device is unreachable."},"status":{"type":"string","readOnly":true,"enum":["online","offline","error","consumableLow","needsAttention","localMode","unknown"],"description":"What the device last said on its heartbeat; `unknown` until it has. `localMode` is an access-control device validating from its offline package with its link down (ADR-0067).\n"},"batteryPercent":{"type":"integer","nullable":true,"readOnly":true,"minimum":0,"maximum":100,"description":"Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"},"lastCheckedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Distinct from `lastHeartbeatAt`.** A heartbeat is the workstation saying the device is attached; a check is the device answering. **A printer with no paper heartbeats perfectly**, which is why the client's board shows both columns.\n"},"health":{"type":"string","enum":["healthy","warning","degraded","offline","unknown"],"default":"unknown","readOnly":true,"description":"**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"capabilities":{"type":"array","readOnly":true,"items":{"$ref":"#/components/schemas/DeviceCapability"},"description":"BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is standards-first — the device does what the device does — and until now a venue could switch on a feature that depended on hardware without anything being able to say whether the hardware was there.\n**A capability absent is a capability unavailable**, not a capability assumed. A venue setting that requires one is refused where no device in scope reports it, rather than silently doing nothing at the gate.\n"},"enrolmentState":{"type":"string","enum":["registered","enrolled","provisioned","active","deactivated","retired"],"default":"registered","readOnly":true,"description":"BL-160. **Where the device is in its life, which is not the same question as whether it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled, provisioned, active, deactivated, retired — since 16.1.2, and until now there was no column for it to land in, so the operation read this table and wrote nothing.\n**Distinct from `status` and from `health`.** `status` is what the device last said and `health` is what we computed from it; a decommissioned turnstile still sitting on the network is `online` and `retired` at once, and neither column contradicts the other. **A device that is `retired` is refused at the gate whatever its status says.**\nThe transition itself — who moved it, from what, and why — is a `tenancy.device_audit` record. It is not repeated here, because the latest transition stored in two places is one place to go stale.\n"},"retiredAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from `tenancy.device_audit`, and kept as a column for the same reason `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit log is a date nobody filters a fleet by.\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The profile this device was provisioned with.** `enrolDevice` has accepted one since 16.1.3 and there was nowhere to keep it, so the answer to *\"what is this reader configured as\"* lived only in the request that set it.\n"}}},
"ScanAnomalyRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n","items":{"type":"object","properties":{"rule":{"type":"string","enum":["simultaneousEntry","impossibleTravelTime","rapidReentry","sharedDevice","velocityBreach"]},"action":{"type":"string","enum":["log","flag","requireSupervisor","deny"]},"thresholdSeconds":{"type":"integer","nullable":true}}}},
"TurnstileLaneBehaviorConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Turnstile & Lane Behavior Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"accessPointId":{"type":"string","description":"Turnstile or lane being configured"},"mode":{"type":"string","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"],"description":"Default operating mode of the lane (AccessPointOperatingMode, R221). Direction is fixed per access point; re-entry, crossover, fast pass and group are admission rules, not lane modes"},"passThroughTimeout":{"type":"integer","description":"Seconds"},"relockBehavior":{"type":"string","description":"relock behavior"},"incompletePassageBehavior":{"type":"string","description":"incomplete passage behavior"},"unlockDuration":{"type":"integer","description":"Seconds"}},"required":["accessPointId","mode"]},
"TurnstileLaneBehaviorConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Turnstile & Lane Behavior Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"accessPointId":{"type":"string","description":"Turnstile or lane being configured"},"mode":{"type":"string","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"],"description":"Default operating mode of the lane (AccessPointOperatingMode, R221). Direction is fixed per access point; re-entry, crossover, fast pass and group are admission rules, not lane modes"},"passThroughTimeout":{"type":"integer","description":"Seconds"},"relockBehavior":{"type":"string","description":"relock behavior"},"incompletePassageBehavior":{"type":"string","description":"incomplete passage behavior"},"unlockDuration":{"type":"integer","description":"Seconds"}},"required":["accessPointId","mode"]},
"TurnstileMode": {"type":"string","description":"**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n","enum":["freeRotation","closed"]},
"ValidationOutcomeGuestFeedbackDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Validation Outcome & Guest Feedback Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"appliesTo":{"type":"string","enum":["adult","child","vip","pod","membership","invalidCredential","wrongVerificationMethod","biometricReview","reEntryException"],"description":"Guest type or case this response is for"},"outcome":{"type":"string","enum":["granted","operatorAction","denied"]},"venueId":{"type":"string"},"outcomeProfileId":{"type":"string"},"lightColour":{"type":"string","enum":["green","yellow","red"],"description":"Light shown"},"gateAction":{"type":"string","enum":["open","remainsControlled","remainsLocked"],"description":"What the gate does"},"sound":{"type":"string","enum":["successTone","alertSound","denialSound"],"description":"Sound played"},"pictogram":{"type":"string","description":"✓ pictogram"},"customMessage":{"type":"string","description":"Custom message"},"operatorPrompt":{"type":"string","description":"operator prompt"},"reasonCode":{"type":"string","description":"reason code"},"language":{"type":"string","description":"Message language, e.g. ar, en"}},"required":["outcomeProfileId","venueId","outcome","appliesTo"]},
"ValidationOutcomeGuestFeedbackDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Validation Outcome & Guest Feedback Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"appliesTo":{"type":"string","enum":["adult","child","vip","pod","membership","invalidCredential","wrongVerificationMethod","biometricReview","reEntryException"],"description":"Guest type or case this response is for"},"outcome":{"type":"string","enum":["granted","operatorAction","denied"]},"venueId":{"type":"string"},"outcomeProfileId":{"type":"string"},"lightColour":{"type":"string","enum":["green","yellow","red"],"description":"Light shown"},"gateAction":{"type":"string","enum":["open","remainsControlled","remainsLocked"],"description":"What the gate does"},"sound":{"type":"string","enum":["successTone","alertSound","denialSound"],"description":"Sound played"},"pictogram":{"type":"string","description":"✓ pictogram"},"customMessage":{"type":"string","description":"Custom message"},"operatorPrompt":{"type":"string","description":"operator prompt"},"reasonCode":{"type":"string","description":"reason code"},"language":{"type":"string","description":"Message language, e.g. ar, en"}},"required":["outcomeProfileId","venueId","outcome","appliesTo"]}
}
```
