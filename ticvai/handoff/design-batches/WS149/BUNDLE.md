# WS149 — Payment Payment Orchestration board 3

**10 screens · 14 operations · 18 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `DEVICE_MANAGE, DEVICE_VIEW, PAYMENT_CONFIGURE, PAYMENT_PROVIDER_MANAGE, PAYMENT_VIEW, WORK_ORDER_MANAGE`. A control nobody can use must say so,
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
| `ADM-579` | Terminal & Card-Present Command Center\t48 | B–D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-580` | Payment Terminal & Device Inventory\t49 | B–D | 0 | 0 | 6 | 8 | 0 | 4 | — | notStarted (—) |
| `ADM-581` | Terminal Provisioning & Device Configuration\t51 | B–D | 9 | 0 | 6 | 6 | 0 | 0 | — | notStarted (—) |
| `ADM-582` | POS, Kiosk & Terminal Assignment Manager\t52 | B–D | 0 | 0 | 6 | 4 | 0 | 0 | — | notStarted (—) |
| `ADM-583` | EMV & Card-Present Processing Configuration\t53 | B–D | 8 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `ADM-584` | Payment Server & Terminal Connectivity Manager\t54 | B–D | 0 | 8 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `ADM-585` | Card-Present Transaction Monitor & Operations\t55 | B–D | 2 | 26 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-586` | Degraded, Offline & Store-and-Forward Manager\t56 | B–D | 0 | 14 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `ADM-587` | Terminal Health, Maintenance & Incident Center\t57 | B–D | 0 | 0 | 6 | 14 | 0 | 2 | — | notStarted (—) |
| `ADM-588` | Terminal Simulator, Certification & AI Operations Advisor\t59 | B–D | 16 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-582, ADM-584, ADM-586, ADM-587 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-579` Terminal & Card-Present Command Center\t48

**Provide real-time operational visibility over all card-present payment infrastructure.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/terminal-card-present-command-center-t48-adm-579` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search terminal card-present \t48 | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, location, terminal, pos, acquirer, payment method and 2 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Total Terminals** (metric tile)

**Online Terminals** (metric tile)

**Offline Terminals** (metric tile)

**Degraded Terminals** (metric tile)

**Active POS Assignments** (metric tile)

**Card-Present Transactions** (metric tile)

**Authorization Rate** (metric tile)

**Card-Present Value** (metric tile)

**Failed Transactions** (metric tile)

**Average Processing Time** (metric tile)

**Terminal Alerts** (metric tile)

**Offline/Pending Transactions** (metric tile)

**Data it reads**: `listPaymentTerminals` (onLoad, Terminals across venues)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-580` Payment Terminal & Device Inventory\t49: *Payment Terminal & Device Inventory\t49*
- → `ADM-581` Terminal Provisioning & Device Configuration\t51: *Terminal Provisioning & Device Configuration\t51*
- → `ADM-582` POS, Kiosk & Terminal Assignment Manager\t52: *POS, Kiosk & Terminal Assignment Manager\t52*
- → `ADM-583` EMV & Card-Present Processing Configuration\t53: *EMV & Card-Present Processing Configuration\t53*
- → `ADM-584` Payment Server & Terminal Connectivity Manager\t54: *Payment Server & Terminal Connectivity Manager\t54*
- → `ADM-585` Card-Present Transaction Monitor & Operations\t55: *Card-Present Transaction Monitor & Operations\t55*
- → `ADM-586` Degraded, Offline & Store-and-Forward Manager\t56: *Degraded, Offline & Store-and-Forward Manager\t56*
- → `ADM-587` Terminal Health, Maintenance & Incident Center\t57: *Terminal Health, Maintenance & Incident Center\t57*
- → `ADM-588` Terminal Simulator, Certification & AI Operations Advisor\t59: *Terminal Simulator, Certification & AI Operations Advisor\t59*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The terminal card-present \t48 list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the terminal card-present \t48 untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No terminal card-present \t48 yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the terminal card-present \t48 are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPaymentTerminals` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-579` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-579`
- Workshop pack: Payment_Payment_Orchestration.pdf board 3
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 1: Opens Terminal & Card-Present Command Center\t48 → Provide real-time operational visibility over all card-present payment infrastructure.
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F258 branch at step 1 (expected): when Nothing has been set up on Terminal & Card-Present Command Center\t48 yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F258 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-579?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-580`, `ADM-581`, `ADM-582`, `ADM-583`, `ADM-584`, `ADM-585`, `ADM-586`, `ADM-587`, `ADM-588`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-580` Payment Terminal & Device Inventory\t49

**Maintain the centralized inventory of all payment terminals connected to TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `DEVICE_VIEW`, `PAYMENT_PROVIDER_MANAGE`, `PAYMENT_VIEW` (2 read, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `modelCode` (navigation) |
| Route | `/commercial/payment-terminal-device-inventory-t49-adm-580` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Fixed POS terminal, SoftPOS where supported, Device owner, Last service, Replacement date. Each needs an … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listDevices` ?workstationId |
| Kind | select | — | Receipt printer · Ticket printer · Label printer · Cash drawer · Barcode scanner · RFID reader · NFC reader · Card reader · ID reader · Biometric reader · Access reader · Payment terminal … | `listDevices` ?kind |
| Model code | text field | — | — | `listPaymentTerminalCertifications` ?modelCode |
| Expiring before | date picker | — | — | `listPaymentTerminalCertifications` ?expiringBefore |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Fixed POS terminal (primary button) | navigation or local | — | — | — | — |
| SoftPOS where supported (secondary button) | navigation or local | — | — | — | — |
| Device owner (secondary button) | navigation or local | — | — | — | — |
| Last service (secondary button) | navigation or local | — | — | — | — |
| Replacement date (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPaymentTerminals` (onLoad, The inventory); `listDevices` (onLoad, The device register behind it); `listPaymentTerminalCertifications` (onLoad, Terminal model certifications)

**Where the user goes next**

- → `ADM-579` Terminal & Card-Present Command Center\t48: *Back to Terminal & Card-Present Command Center\t48*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment terminal device list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment terminal device untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment terminal device yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment terminal device are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 An expiry before the approval date, or a Level 3 entry for an acquirer connection that does not exist. |

#### Permissions

- `listPaymentTerminals` → `PAYMENT_VIEW` (read) · staff
- `listDevices` → `DEVICE_VIEW` (read) · staff
- `listPaymentTerminalCertifications` → `PAYMENT_VIEW` (read) · staff
- `recordPaymentTerminalCertification` → `PAYMENT_PROVIDER_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.18 | POS and kiosk devices shall be linked to the Device Management module so administrators can monitor device status, location, software version, connectivity, errors, paper levels, and assigned … | Ticketing Sales | CONTRACTED | `listDevices` |
| 2.1.26 | System shall provide centralized monitoring of kiosk health including online status, stock levels, payment devices, printers, connectivity, and alerts. | Ticketing Sales | CONTRACTED | `listDevices` |
| 8.9.6 | System shall monitor scanners, POS devices, kiosks, handhelds, printers, gates, network connectivity, and infrastructure health. | Unified Operations Dashboard | CONTRACTED | `listDevices` |
| 16.2.7 | Device Inventory Management - System shall maintain device inventories. | Device Management | CONTRACTED | `listDevices` |
| 16.2.8 | Device Classification - System shall support device categorization. | Device Management | CONTRACTED | `listDevices` |
| 16.2.12 | Device Asset Tracking - System shall maintain device asset records. | Device Management | CONTRACTED | `listDevices` |
| 16.9.55 | Device APIs - System shall expose device management APIs. | Device Management | CONTRACTED | `listDevices` |
| 4.3.1 | The system should be EMV (Euro pay, MasterCard and Visa) certified for offline and online payments. | Bundles and Promotions | CONTRACTED | `recordPaymentTerminalCertification` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-580` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-580`
- Workshop pack: Payment_Payment_Orchestration.pdf board 3
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 2: Works in Payment Terminal & Device Inventory\t49 → Maintain the centralized inventory of all payment terminals connected to TICVAI.
- ADR-0067 *One device register; Access keeps only where a device is placed* (`docs/adr/0067-one-device-register.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-580?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Fixed POS terminal, SoftPOS where supported, Device owner, Last service, Replacement date.
- [ ] Every transition is wired: `ADM-579`.
- [ ] Every gated control is gated: `DEVICE_VIEW`, `PAYMENT_PROVIDER_MANAGE`, `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-581` Terminal Provisioning & Device Configuration\t51

**Configure and activate a physical terminal for TICVAI use.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `DEVICE_MANAGE`, `PAYMENT_CONFIGURE` (2 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `deviceId` (session) |
| Route | `/commercial/terminal-provisioning-device-configuration-t51-adm-581` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Device reference, Receipt configuration, Connection profile. Each needs an operation, or needs removing …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | select field | — | — | — | — | — | — |
| Legal Entity | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Location | select field | — | — | — | — | — | — |
| POS | select field | — | — | — | — | — | — |
| Provider | select field | — | — | — | — | — | — |
| Acquirer | select field | — | — | — | — | — | — |
| Merchant Account | select field | — | — | — | — | — | — |
| Terminal Profile | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Device reference (primary button) | navigation or local | — | — | — | — |
| Receipt configuration (secondary button) | navigation or local | — | — | — | — |
| Connection profile (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-579` Terminal & Card-Present Command Center\t48: *Back to Terminal & Card-Present Command Center\t48*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The terminal provisioning device configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the terminal provisioning device untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No terminal provisioning device configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The transition is not allowed from the current state; 422 Status `active` for a terminal whose model has no current Level 3 certification for its acquirer (`recordPaymentTerminalCertification`), or `dccEnabled` with … |

#### Permissions

- `enrolDevice` → `DEVICE_MANAGE` (configure) · staff
- `setPaymentTerminalConfiguration` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.1.2 | Device Enrollment - System shall support device enrollment workflows. | Device Management | CONTRACTED | `enrolDevice` |
| 16.1.3 | Device Provisioning - System shall support device provisioning. | Device Management | CONTRACTED | `enrolDevice` |
| 16.1.6 | Device Retirement - System shall support device retirement. | Device Management | CONTRACTED | `enrolDevice` |
| 16.5.29 | Device Lifecycle Tracking - System shall track device lifecycle status. | Device Management | CONTRACTED | `enrolDevice` |
| 4.3.2 | The system should support payment terminals (PDQ) that: - Accept all the credit and debit cards considered - Enter the code by Pin - Accept swipe payment - Accept contactless payment - Handle … | Bundles and Promotions | CONTRACTED | `setPaymentTerminalConfiguration` |
| 4.3.3 | The system should support payment terminals that are connected to an internal or external payment server and are not linked directly to the bank. | Bundles and Promotions | CONTRACTED | `setPaymentTerminalConfiguration` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-581` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-581`
- Workshop pack: Payment_Payment_Orchestration.pdf board 3
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 4: Works in Terminal Provisioning & Device Configuration\t51 → Configure and activate a physical terminal for TICVAI use.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (404, 409, 412, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-581?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Device reference, Receipt configuration, Connection profile.
- [ ] Every transition is wired: `ADM-579`.
- [ ] Every gated control is gated: `DEVICE_MANAGE`, `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-582` POS, Kiosk & Terminal Assignment Manager\t52

**Control which terminal is connected or assigned to each TICVAI selling device.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `DEVICE_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `deviceId` (session) |
| Route | `/commercial/pos-kiosk-terminal-assignment-manager-t52-adm-582` |

**Known gaps.** **POS, Kiosk & Terminal Assignment Manager\t52 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save device assignment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-579` Terminal & Card-Present Command Center\t48: *Back to Terminal & Card-Present Command Center\t48*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pos kiosk terminal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pos kiosk terminal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pos kiosk terminal yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pos kiosk terminal are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setDeviceAssignment` → `DEVICE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.2.9 | Device Ownership - System shall maintain ownership records. | Device Management | CONTRACTED | `setDeviceAssignment` |
| 16.2.10 | Device Assignment - System shall support assignment of devices to users and locations. | Device Management | CONTRACTED | `setDeviceAssignment` |
| 16.2.11 | Device Location Tracking - System shall maintain device location records. | Device Management | CONTRACTED | `setDeviceAssignment` |
| 16.5.28 | Warranty Tracking - System shall track device warranties. | Device Management | CONTRACTED | `setDeviceAssignment` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-582` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-582`
- Workshop pack: Payment_Payment_Orchestration.pdf board 3
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 6: Works in POS, Kiosk & Terminal Assignment Manager\t52 → Control which terminal is connected or assigned to each TICVAI selling device.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-582?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save device assignment, Cancel.
- [ ] Every transition is wired: `ADM-579`.
- [ ] Every gated control is gated: `DEVICE_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-583` EMV & Card-Present Processing Configuration\t53

**Configure card-present transaction capabilities without exposing sensitive cardholder data.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/emv-card-present-processing-configuration-t53-adm-583` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Sale | select field | — | — | — | — | — | — |
| Authorization | select field | — | — | — | — | — | — |
| Capture | select field | — | — | — | — | — | — |
| Void | select field | — | — | — | — | — | — |
| Refund | select field | — | — | — | — | — | — |
| Reversal | select field | — | — | — | — | — | — |
| Preauthorization where supported | select field | — | — | — | — | — | — |
| Completion where supported | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-579` Terminal & Card-Present Command Center\t48: *Back to Terminal & Card-Present Command Center\t48*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The emv card-present processing configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the emv card-present processing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No emv card-present processing configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 Status `active` for a terminal whose model has no current Level 3 certification for its acquirer (`recordPaymentTerminalCertification`), or `dccEnabled` with … |

#### Permissions

- `setPaymentTerminalConfiguration` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.2 | The system should support payment terminals (PDQ) that: - Accept all the credit and debit cards considered - Enter the code by Pin - Accept swipe payment - Accept contactless payment - Handle … | Bundles and Promotions | CONTRACTED | `setPaymentTerminalConfiguration` |
| 4.3.3 | The system should support payment terminals that are connected to an internal or external payment server and are not linked directly to the bank. | Bundles and Promotions | CONTRACTED | `setPaymentTerminalConfiguration` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-583` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-583`
- Workshop pack: Payment_Payment_Orchestration.pdf board 3
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 8: Works in EMV & Card-Present Processing Configuration\t53 → Configure card-present transaction capabilities without exposing sensitive cardholder data.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (412, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-583?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-579`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-584` Payment Server & Terminal Connectivity Manager\t54

**Monitor and configure the communication path between TICVAI POS, payment terminal, payment server and payment provider.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `DEVICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `deviceId` (session) |
| Route | `/commercial/payment-server-terminal-connectivity-manager-t54-adm-584` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … **Payment Server & Terminal Connectivity Manager\t54 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getDeviceTelemetry` ?from |
| To | date and time picker | — | — | `getDeviceTelemetry` ?to |
| Metric | text field | — | — | `getDeviceTelemetry` ?metric |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every payment server terminal** (data table)

| Shows | Format | Notes |
|---|---|---|
| POS ↔ terminal | text | not in the schema: `POS ↔ Terminal` |
| Terminal ↔ payment server | text | not in the schema: `Terminal ↔ Payment Server` |
| Payment server ↔ provider | text | not in the schema: `Payment Server ↔ Provider` |
| Provider ↔ acquirer | text | not in the schema: `Provider ↔ Acquirer` |

**The selected payment server terminal** (detail panel): The pack groups this record's detail under its own headings: “Architecture Example”, “Terminal Integration Layer”, “Payment Terminal”, “Payment Server / Provider”, “Depending on integration”, “Health Indicators”.

| Shows | Format | Notes |
|---|---|---|
| POS ↔ terminal | text | not in the schema: `POS ↔ Terminal` |
| Terminal ↔ payment server | text | not in the schema: `Terminal ↔ Payment Server` |
| Payment server ↔ provider | text | not in the schema: `Payment Server ↔ Provider` |
| Provider ↔ acquirer | text | not in the schema: `Provider ↔ Acquirer` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Connectivity test, Terminal ping/health test where supported, Provider reachability, Merchant validation, Configuration validation. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `getDeviceTelemetry` (onLoad, Connectivity over time)

**Where the user goes next**

- → `ADM-579` Terminal & Card-Present Command Center\t48: *Back to Terminal & Card-Present Command Center\t48*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment server terminal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment server terminal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment server terminal yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment server terminal are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getDeviceTelemetry` → `DEVICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.4.21 | Battery Monitoring - System shall monitor battery levels where applicable. | Device Management | CONTRACTED | `getDeviceTelemetry` |
| 16.4.22 | Device Performance Monitoring - System shall monitor device performance. | Device Management | CONTRACTED | `getDeviceTelemetry` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-584` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-584`
- Workshop pack: Payment_Payment_Orchestration.pdf board 3
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 10: Works in Payment Server & Terminal Connectivity Manager\t54 → Monitor and configure the communication path between TICVAI POS, payment terminal, payment server and payment provider.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-584?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-579`.
- [ ] Every gated control is gated: `DEVICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-585` Card-Present Transaction Monitor & Operations\t55

**Provide operations teams with real-time visibility into card-present payment attempts.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/card-present-transaction-monitor-operations-t55-adm-585` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search card-present transaction operations\t55 | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by ticvai payment id, order, pos, terminal, venue, provider and 6 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Every card-present transaction operations\t55** (data table)

| Shows | Format | Notes |
|---|---|---|
| Payment ID | text | not in the schema: `Payment ID` |
| Order ID | text | not in the schema: `Order ID` |
| Terminal | text | not in the schema: `Terminal` |
| POS | text | not in the schema: `POS` |
| Amount | text | not in the schema: `Amount` |
| Currency | text | not in the schema: `Currency` |
| Provider | text | not in the schema: `Provider` |
| Merchant account | text | not in the schema: `Merchant account` |
| Card scheme | text | not in the schema: `Card scheme` |
| Entry method | text | not in the schema: `Entry method` |
| Authorization result | text | not in the schema: `Authorization result` |
| Processing duration | text | not in the schema: `Processing duration` |
| Status | text | not in the schema: `Status` |

**The selected card-present transaction operations\t55** (detail panel): The pack groups this record's detail under its own headings: “Important”.

| Shows | Format | Notes |
|---|---|---|
| Payment ID | text | not in the schema: `Payment ID` |
| Order ID | text | not in the schema: `Order ID` |
| Terminal | text | not in the schema: `Terminal` |
| POS | text | not in the schema: `POS` |
| Amount | text | not in the schema: `Amount` |
| Currency | text | not in the schema: `Currency` |
| Provider | text | not in the schema: `Provider` |
| Merchant account | text | not in the schema: `Merchant account` |
| Card scheme | text | not in the schema: `Card scheme` |
| Entry method | text | not in the schema: `Entry method` |
| Authorization result | text | not in the schema: `Authorization result` |
| Processing duration | text | not in the schema: `Processing duration` |
| Status | text | not in the schema: `Status` |

**Data it reads**: `listPaymentTerminals` (onLoad, Live card-present operations)

**Where the user goes next**

- → `ADM-579` Terminal & Card-Present Command Center\t48: *Back to Terminal & Card-Present Command Center\t48*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card-present transaction operations\t55 list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card-present transaction operations\t55 untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card-present transaction operations\t55 yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the card-present transaction operations\t55 are still there. The pack's own statuses are Initiated — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPaymentTerminals` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-585` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-585`
- Workshop pack: Payment_Payment_Orchestration.pdf board 3
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 12: Works in Card-Present Transaction Monitor & Operations\t55 → Provide operations teams with real-time visibility into card-present payment attempts.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-585?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-579`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-586` Degraded, Offline & Store-and-Forward Manager\t56

**Manage card-present operations when normal connectivity is unavailable. This directly addresses the degraded-mode requirement in the payment matrix.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE`, `PAYMENT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `terminalId` (session) |
| Route | `/commercial/degraded-offline-store-and-forward-manager-t56-adm-586` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … **Degraded, Offline & Store-and-Forward Manager\t56 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every degraded offline store-and-forward** (data table)

| Shows | Format | Notes |
|---|---|---|
| Terminal | text | not in the schema: `Terminal` |
| Transaction | text | not in the schema: `Transaction` |
| Amount | text | not in the schema: `Amount` |
| Timestamp | text | not in the schema: `Timestamp` |
| Offline reason | text | not in the schema: `Offline reason` |
| Retry status | text | not in the schema: `Retry status` |
| Synchronization state | text | not in the schema: `Synchronization state` |

**The selected degraded offline store-and-forward** (detail panel): The pack groups this record's detail under its own headings: “Important Principle”, “Synchronization”.

| Shows | Format | Notes |
|---|---|---|
| Terminal | text | not in the schema: `Terminal` |
| Transaction | text | not in the schema: `Transaction` |
| Amount | text | not in the schema: `Amount` |
| Timestamp | text | not in the schema: `Timestamp` |
| Offline reason | text | not in the schema: `Offline reason` |
| Retry status | text | not in the schema: `Retry status` |
| Synchronization state | text | not in the schema: `Synchronization state` |

**Data it reads**: `listStoredForwardTransactions` (onLoad, What is held offline)

**Where the user goes next**

- → `ADM-579` Terminal & Card-Present Command Center\t48: *Back to Terminal & Card-Present Command Center\t48*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The degraded offline store-and-forward list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the degraded offline store-and-forward untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No degraded offline store-and-forward yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the degraded offline store-and-forward are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 Status `active` for a terminal whose model has no current Level 3 certification for its acquirer (`recordPaymentTerminalCertification`), or `dccEnabled` with … |

#### Permissions

- `listStoredForwardTransactions` → `PAYMENT_VIEW` (read) · staff
- `setPaymentTerminalConfiguration` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.2 | The system should support payment terminals (PDQ) that: - Accept all the credit and debit cards considered - Enter the code by Pin - Accept swipe payment - Accept contactless payment - Handle … | Bundles and Promotions | CONTRACTED | `setPaymentTerminalConfiguration` |
| 4.3.3 | The system should support payment terminals that are connected to an internal or external payment server and are not linked directly to the bank. | Bundles and Promotions | CONTRACTED | `setPaymentTerminalConfiguration` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-586` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-586`
- Workshop pack: Payment_Payment_Orchestration.pdf board 3
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 14: Works in Degraded, Offline & Store-and-Forward Manager\t56 → Manage card-present operations when normal connectivity is unavailable. This directly addresses the degraded-mode requirement in the payment matrix.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412, 422).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-586?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-579`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`, `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-587` Terminal Health, Maintenance & Incident Center\t57

**Provide centralized lifecycle monitoring and operational maintenance of terminal hardware.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `DEVICE_MANAGE`, `DEVICE_VIEW`, `WORK_ORDER_MANAGE` (2 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `deviceId` (session), `firmwareId` (navigation) |
| Route | `/commercial/terminal-health-maintenance-incident-center-t57-adm-587` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Device replacement, Certification update. Each needs an operation, or needs removing from the screen; this … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getDeviceTelemetry` ?from |
| To | date and time picker | — | — | `getDeviceTelemetry` ?to |
| Metric | text field | — | — | `getDeviceTelemetry` ?metric |
| Device kind | text field | — | — | `listDeviceFirmware` ?deviceKind |
| Version | text field | — | — | `listDeviceFirmware` ?version |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Device replacement (primary button) | navigation or local | — | — | — | — |
| Certification update (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getDeviceTelemetry` (onLoad, Terminal health); `listDeviceFirmware` (onLoad, Terminal firmware versions across the fleet)

**Where the user goes next**

- → `ADM-579` Terminal & Card-Present Command Center\t48: *Back to Terminal & Card-Present Command Center\t48*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The terminal health maintenance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the terminal health maintenance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No terminal health maintenance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the terminal health maintenance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A release with this `deviceKind` and `version` already exists |

#### Permissions

- `getDeviceTelemetry` → `DEVICE_VIEW` (read) · staff
- `createWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `listDeviceFirmware` → `DEVICE_VIEW` (read) · staff
- `getDeviceFirmware` → `DEVICE_VIEW` (read) · staff
- `createDeviceFirmware` → `DEVICE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.4.21 | Battery Monitoring - System shall monitor battery levels where applicable. | Device Management | CONTRACTED | `getDeviceTelemetry` |
| 16.4.22 | Device Performance Monitoring - System shall monitor device performance. | Device Management | CONTRACTED | `getDeviceTelemetry` |
| 16.5.25 | Corrective Maintenance - System shall support corrective maintenance tracking. | Device Management | CONTRACTED | `createWorkOrder` |
| 16.5.26 | Maintenance Work Orders - System shall support device maintenance work orders. | Device Management | CONTRACTED | `createWorkOrder` |
| 17.3.1 | Maintenance Requests - System shall support maintenance requests. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.3.2 | Breakdown Management - System shall support equipment breakdown management. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.3.3 | Emergency Maintenance - System shall support emergency maintenance requests. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.1 | Work Order Creation - System shall support work order creation. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.2 | Work Order Assignment - System shall support work order assignment. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.3 | Work Order Prioritization - System shall support work order prioritization. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.4 | Work Order Status Management - System shall support work order lifecycle management. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 16.6.32 | Software Version Tracking - System shall maintain software version records. | Device Management | CONTRACTED | `listDeviceFirmware` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-587` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-587`
- Workshop pack: Payment_Payment_Orchestration.pdf board 3
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 16: Works in Terminal Health, Maintenance & Incident Center\t57 → Provide centralized lifecycle monitoring and operational maintenance of terminal hardware.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-587?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Device replacement, Certification update.
- [ ] Every transition is wired: `ADM-579`.
- [ ] Every gated control is gated: `DEVICE_MANAGE`, `DEVICE_VIEW`, `WORK_ORDER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-588` Terminal Simulator, Certification & AI Operations Advisor\t59

**Provide a controlled environment to validate terminal configuration and payment flows before production activation.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_PROVIDER_MANAGE`, `PAYMENT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select; Terminal Receipt Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `connectionId` (navigation), `modelCode` (navigation) |
| Route | `/commercial/terminal-simulator-certification-ai-operations-advisor-t-adm-588` |

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 0 operations.** Unserved: Successful payment, Card decline, Lost connection, Reversal, Duplicate request, Temporary assignment …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| POS | select field | — | — | — | — | — | — |
| Terminal | select field | — | — | — | — | — | — |
| Provider | select field | — | — | — | — | — | — |
| Merchant account | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Transaction amount | select field | — | — | — | — | — | — |
| Transaction type | select field | — | — | — | — | — | — |
| Connectivity state | select field | — | — | — | — | — | — |
| Merchant receipt | select field | — | — | — | — | — | — |
| Customer receipt | select field | — | — | — | — | — | — |
| Printed | select field | — | — | — | — | — | — |
| Digital | select field | — | — | — | — | — | — |
| Combined TICVAI receipt | select field | — | — | — | — | — | — |
| Terminal-only receipt | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Model code | text field | — | — | `listPaymentTerminalCertifications` ?modelCode |
| Expiring before | date picker | — | — | `listPaymentTerminalCertifications` ?expiringBefore |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Successful payment (primary button) | navigation or local | — | — | — | — |
| Card decline (secondary button) | navigation or local | — | — | — | — |
| Lost connection (secondary button) | navigation or local | — | — | — | — |
| Reversal (secondary button) | navigation or local | — | — | — | — |
| Duplicate request (secondary button) | navigation or local | — | — | — | — |
| Temporary assignment (secondary button) | navigation or local | — | — | — | — |
| Venue (secondary button) | navigation or local | — | — | — | — |
| Assignment history (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPaymentTerminalCertifications` (onLoad, Terminal model certifications)

**Where the user goes next**

- → `ADM-579` Terminal & Card-Present Command Center\t48: *Back to Terminal & Card-Present Command Center\t48*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The terminal simulator certification configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the terminal simulator certification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No terminal simulator certification configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 An expiry before the approval date, or a Level 3 entry for an acquirer connection that does not exist. |

#### Permissions

- `testPaymentProviderConnection` → `PAYMENT_PROVIDER_MANAGE` (configure) · staff
- `listPaymentTerminalCertifications` → `PAYMENT_VIEW` (read) · staff
- `recordPaymentTerminalCertification` → `PAYMENT_PROVIDER_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.1 | The system should be EMV (Euro pay, MasterCard and Visa) certified for offline and online payments. | Bundles and Promotions | CONTRACTED | `recordPaymentTerminalCertification` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-588` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS89 Payment Payment Orchestration Board 3.dc.html#adm-588`
- Workshop pack: Payment_Payment_Orchestration.pdf board 3
- Flow F258 *Payment Payment Orchestration board 3: Terminal & Card-Present Command …*, step 18: Works in Terminal Simulator, Certification & AI Operations Advisor\t59 → Provide a controlled environment to validate terminal configuration and payment flows before production activation.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (412, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-588?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Successful payment, Card decline, Lost connection, Reversal, Duplicate request, Temporary assignment, Venue, Assignment history.
- [ ] Every transition is wired: `ADM-579`.
- [ ] Every gated control is gated: `PAYMENT_PROVIDER_MANAGE`, `PAYMENT_VIEW`.
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

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createDeviceFirmware": {"method":"POST","path":"/device-firmware","contract":"tenancy","summary":"Register a firmware or software release before it is deployed","permission":"DEVICE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DeviceFirmware","responds":"DeviceFirmware"},
"createWorkOrder": {"method":"POST","path":"/work-orders","contract":"maintenance","summary":"Raise a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateWorkOrderRequest","responds":"WorkOrder"},
"enrolDevice": {"method":"POST","path":"/devices/{deviceId}/enrolment","contract":"tenancy","summary":"Take a registered device through enrolment to activation","permission":"DEVICE_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DeviceEnrolment","responds":"RegisteredDevice"},
"getDeviceFirmware": {"method":"GET","path":"/device-firmware/{firmwareId}","contract":"tenancy","summary":"Read one firmware release, and how much of the fleet is on it","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"DeviceFirmware"},
"getDeviceTelemetry": {"method":"GET","path":"/devices/{deviceId}/telemetry","contract":"tenancy","summary":"Battery, performance and consumables over time","permission":"DEVICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"metric","in":"query","required":null}],"requestBody":null,"responds":"DeviceTelemetryPoint"},
"listDeviceFirmware": {"method":"GET","path":"/device-firmware","contract":"tenancy","summary":"Firmware and software versions, and what is running where","permission":"DEVICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"deviceKind","in":"query","required":null},{"name":"version","in":"query","required":null}],"requestBody":null,"responds":"DeviceFirmware"},
"listDevices": {"method":"GET","path":"/devices","contract":"tenancy","summary":"List registered devices","permission":"DEVICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPaymentTerminalCertifications": {"method":"GET","path":"/payment-terminal-certifications","contract":"payments","summary":"EMV and PCI certification of each terminal model and kernel","permission":"PAYMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"modelCode","in":"query","required":null},{"name":"expiringBefore","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPaymentTerminals": {"method":"GET","path":"/payment-terminals","contract":"payments","summary":"Terminals, and the payment configuration on each","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null}],"requestBody":null,"responds":"PaymentTerminal"},
"listStoredForwardTransactions": {"method":"GET","path":"/payment-terminals/{terminalId}/forwarded","contract":"payments","summary":"What a terminal took offline and has not yet sent","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"StoredForwardTransaction"},
"recordPaymentTerminalCertification": {"method":"PUT","path":"/payment-terminal-certifications/{modelCode}","contract":"payments","summary":"Record a terminal model's EMV and PCI certification","permission":"PAYMENT_PROVIDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"PayTerminalCertification","responds":"PayTerminalCertification"},
"setDeviceAssignment": {"method":"PUT","path":"/devices/{deviceId}/assignment","contract":"tenancy","summary":"Who owns it, who holds it, and where it is","permission":"DEVICE_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DeviceAssignment","responds":"DeviceAssignment"},
"setPaymentTerminalConfiguration": {"method":"PUT","path":"/payment-terminals","contract":"payments","summary":"Merchant account, acquirer, EMV and offline behaviour","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"PaymentTerminal","responds":"PaymentTerminal"},
"testPaymentProviderConnection": {"method":"POST","path":"/payment-providers/{connectionId}/test","contract":"payments","summary":"Prove the connection works before anybody pays through it","permission":"PAYMENT_PROVIDER_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProviderTestResult"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CreateWorkOrderRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","title","venueId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"title":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":5000},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"kind":{"allOf":[{"$ref":"#/components/schemas/WorkOrderKind"}],"default":"corrective"},"priority":{"allOf":[{"$ref":"#/components/schemas/WorkOrderPriority"}],"description":"**Optional since 29 September** (M17-01). Sent, it is `manual` and wins. Absent, the asset's `priorityOverride` applies, and failing that the venue's `WorkOrderPriorityPolicy` scores the fault.\n"},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","maxItems":10,"items":{"type":"string"},"description":"Skills the job needs, as qualification codes; `suggestWorkOrderAssignee` ranks by them (M17-13)."},"categoryId":{"type":"string","format":"uuid"},"assignedToPrincipalId":{"type":"string","format":"uuid"},"dueAt":{"type":"string","format":"date-time"},"attachmentRefs":{"type":"array","description":"Photo-first. Expected at creation, not added later from memory.","items":{"type":"string"}},"takeAssetOutOfService":{"type":"boolean","default":false,"description":"Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"DeviceAssignment": {"type":"object","x-ticvai-persistence":"tenancy.device_assignment","description":"16.2.9 to 16.2.11. **Ownership, custody and location are three facts, not one.**","properties":{"deviceId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setDeviceAssignment`."},"ownerOrgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"Who the device belongs to — the cost centre that replaces it when it breaks."},"custodianPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**Who is holding it right now.** The fact a loss investigation needs."},"assignedWorkstationId":{"type":"string","format":"uuid","nullable":true},"locationScopePath":{"type":"string","nullable":true},"lastSeenLocation":{"type":"string","nullable":true,"readOnly":true,"description":"Reported by the heartbeat; distinct from where it is supposed to be."},"assetTag":{"type":"string","nullable":true},"acquiredAt":{"type":"string","format":"date","nullable":true,"description":"A calendar date in the region's time zone."},"warrantyExpiresAt":{"type":"string","format":"date","nullable":true,"description":"A calendar date in the region's time zone."},"assignedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true}}},
"DeviceCapability": {"type":"string","description":"BL-179. **Something a driver reports, not something the platform provides.** The list grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a driver plus configuration rather than a core change.\n**`genderClassification` is here because `VenueSettings.segregatedAccess. genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch with no driver behind it. Where a venue's access hardware performs the check and the venue chooses to use it, the result is **advisory to the steward and never decisive at the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package deviates deliberately and CF-130 records why.\n**Access's capabilities merged in** (ADR-0067, 1 October): `dynamicQr`, `rfid`, `nfc`, `facePass`, `offline` and `heightCheck` were the access register's own list, from the compatibility matrix.\n","enum":["genderClassification","dynamicQr","rfid","nfc","facePass","offline","heightCheck"]},
"DeviceEnrolment": {"x-ticvai-persistence":"platform.device","type":"object","description":"BL-160. **The body `enrolDevice` accepts, named so that it writes.**\nIt was an anonymous inline object, and `derive-lineage` reads writes from the schema an operation accepts — so the one operation that moves a device through its whole lifecycle recorded no writes at all, and `platform.device` looked like a table only `registerDevice` touched.\n**Provisioning is inside enrolment rather than beside it**, which is why `configurationProfileId` is here: a device that is enrolled but unprovisioned is a device that will fail at the gate on its first morning.\n","required":["state"],"properties":{"state":{"type":"string","enum":["enrolled","provisioned","active","deactivated","retired"],"description":"**The target state, not the current one.** `registered` is absent because `registerDevice` is what produces it and nothing transitions back to it.\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","nullable":true,"description":"**Recorded on the `tenancy.device_audit` row, not on the device.** Required in practice for `deactivated` and `retired`, where an investigation six months later needs to know why a gate stopped working.\n"}}},
"DeviceFirmware": {"type":"object","x-ticvai-persistence":"tenancy.device_firmware","description":"16.6.30 and 16.6.32. **A release, and how much of the fleet is on it.** Written by `createDeviceFirmware` and moved through its life by `setDeviceFirmwareStatus` (29 September, build pass); `startDeviceFirmwareRollout` deploys only a `released` one.\n","required":["deviceKind","version"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"deviceKind":{"type":"string"},"version":{"type":"string"},"vendor":{"type":"string","nullable":true,"description":"Who built the image, as the device's driver names its maker."},"checksumAlgorithm":{"type":"string","enum":["sha256","sha512"],"default":"sha256"},"releaseNotes":{"type":"string","nullable":true},"artefactAssetId":{"type":"string","format":"uuid","nullable":true},"checksum":{"type":"string","nullable":true},"minimumPreviousVersion":{"type":"string","nullable":true,"description":"**Some updates cannot be applied from any starting point.** Naming the floor is how a two-step upgrade stays possible instead of bricking the devices that skipped one.\n"},"releasedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Set when `setDeviceFirmwareStatus` first makes the release `released`."},"installedCount":{"type":"integer","readOnly":true},"status":{"type":"string","readOnly":true,"default":"draft","enum":["draft","released","deprecated","withdrawn"]},"statusReason":{"type":"string","nullable":true,"readOnly":true,"description":"The `reason` given when the release was deprecated or withdrawn."},"scopePath":{"type":"string","readOnly":true,"description":"The tenant the release belongs to. Releases are tenant-wide; rollouts narrow them."}}},
"DeviceKind": {"type":"string","enum":["receiptPrinter","ticketPrinter","labelPrinter","cashDrawer","barcodeScanner","rfidReader","nfcReader","cardReader","idReader","biometricReader","accessReader","paymentTerminal","customerDisplay","signageDisplay","kitchenDisplay","turnstileController","wristbandEncoder","signaturePad","scale","camera","mobileHandset","handheldScanner","accessPodium","bleBeacon"],"description":"`mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation.\n**One kind vocabulary for every device** (ADR-0067, 1 October). `handheldScanner`, `accessPodium` and `bleBeacon` came from Access's register; the finer hardware type (a speed gate under `turnstileController`, a tablet under `handheldScanner`) is `RegisteredDevice.hardwareType` (common `DeviceHardwareType`).\n"},
"DeviceTelemetryPoint": {"type":"object","x-ticvai-persistence":"tenancy.device_telemetry","description":"16.4.21 and 16.4.22. **A series, because degradation is not visible in a point-in-time reading.**\n","properties":{"deviceId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"batteryPercent":{"type":"integer","nullable":true},"batteryHealthPercent":{"type":"integer","nullable":true},"charging":{"type":"boolean","nullable":true},"signalStrength":{"type":"integer","nullable":true},"cpuPercent":{"type":"number","nullable":true},"memoryPercent":{"type":"number","nullable":true},"storageFreeMb":{"type":"integer","nullable":true},"consumables":{"type":"object","additionalProperties":true,"description":"Paper, ribbon, wristband stock — whatever the device kind reports."},"uptimeSeconds":{"type":"integer","nullable":true},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PayTerminalCertification": {"type":"object","x-ticvai-persistence":"payments.terminal_certification + payments.terminal_certification_level3","description":"4.3.1. Also the `recordPaymentTerminalCertification` body. **One per terminal model**; a terminal names its model in `PaymentTerminal.terminalModelCode`.","required":["modelCode","manufacturer"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"modelCode":{"type":"string","maxLength":100},"manufacturer":{"type":"string","maxLength":200},"emvLevel1ApprovalReference":{"type":"string","nullable":true},"emvLevel1ExpiresAt":{"type":"string","format":"date","nullable":true},"emvLevel2KernelVersions":{"type":"array","description":"Contact and contactless kernels with their EMVCo approval, e.g. `EMV Contact 4.3 / ref`.","items":{"type":"string"}},"emvLevel2ExpiresAt":{"type":"string","format":"date","nullable":true},"level3Certifications":{"type":"array","description":"Per acquirer and card scheme; a terminal is activated only against an acquirer listed here and not expired.","items":{"type":"object","properties":{"acquirerConnectionId":{"type":"string","format":"uuid"},"cardScheme":{"type":"string"},"reference":{"type":"string"},"certifiedAt":{"type":"string","format":"date"},"expiresAt":{"type":"string","format":"date","nullable":true}}}},"pciPtsApprovalNumber":{"type":"string","nullable":true},"pciPtsExpiresAt":{"type":"string","format":"date","nullable":true},"documentAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `tenant` scope."}}},
"PaymentTerminal": {"type":"object","x-ticvai-persistence":"payments.terminal","description":"Board 3. **The payment layer on a `tenancy` device**, not a second device register.","required":["deviceId"],"properties":{"deviceId":{"type":"string","format":"uuid","description":"The `tenancy.RegisteredDevice`. **Enrolment, credentials, firmware and tamper state live there.**"},"merchantAccountId":{"type":"string","format":"uuid","nullable":true},"acquirerConnectionId":{"type":"string","format":"uuid","nullable":true},"terminalIdentifier":{"type":"string","nullable":true},"emvConfigurationVersion":{"type":"string","nullable":true},"terminalModelCode":{"type":"string","nullable":true,"description":"4.3.1. The model whose EMV and PCI certification applies (`listPaymentTerminalCertifications`)."},"entryModes":{"type":"array","description":"4.3.2. The card entry modes this terminal accepts. **`magstripe` (swipe) is off unless listed**, since a swiped card carries no chip cryptogram; it stays available as a fallback where the acquirer allows it.","items":{"type":"string","enum":["chip","contactless","magstripe","manualEntry","mobileWallet"]}},"dccEnabled":{"type":"boolean","default":false,"description":"4.3.2. Offer Dynamic Currency Conversion on a foreign card at this terminal. The rate is the provider's and is recorded on the payment (`fxRateSource` `cardScheme`); the ledger still holds the base currency."},"dccProviderConnectionId":{"type":"string","format":"uuid","nullable":true},"contactlessLimit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"pinBypassAllowed":{"type":"boolean","default":false},"storeAndForward":{"type":"object","description":"**A risk decision, not a technical one.**","properties":{"enabled":{"type":"boolean","default":false},"floorLimit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumHeldTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumAgeMinutes":{"type":"integer","nullable":true}}},"status":{"type":"string","enum":["unconfigured","active","offline","suspended"]},"scopePath":{"type":"string"}}},
"ProviderTestResult": {"type":"object","description":"Board 3.10. **A provider configured and never tested fails on the first real transaction.**\n","properties":{"connectionId":{"type":"string","format":"uuid"},"testedAt":{"type":"string","format":"date-time"},"checks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["credentials","authorise","capture","refund","void","tokenise","webhook"]},"passed":{"type":"boolean"},"latencyMs":{"type":"integer","nullable":true},"detail":{"type":"string","nullable":true}}}},"overall":{"type":"string","enum":["pass","partial","fail"]}}},
"RegisteredDevice": {"x-ticvai-persistence":"platform.device","type":"object","description":"**The only device register** (ADR-0067, accepted 1 October; the register of record since 29 September). Identity (kind, hardware type, model, serial), every version (firmware, configuration, rule package, credential package), health, heartbeat and one lifecycle (`enrolmentState`: registered, enrolled, provisioned, active, deactivated, retired) for every device in the estate live on this row. The access-control device row, which repeated serial, versions, health and lifecycle, is now `access.device_placement` and holds only where an access-control device is placed. Tenancy owns and migrates this table; Access reads it only through this contract.\n","required":["id","kind","driver"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015).\n"},"identifier":{"type":"string","nullable":true},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control device (one with a `hardwareType`), which is placed in the gate topology by access `placeAccessDevice` rather than bound to a workstation (ADR-0067); `registerDevice` refuses either mistake with `422`.\n"},"model":{"type":"string","nullable":true},"hardwareType":{"$ref":"../shared/common.yaml#/components/schemas/DeviceHardwareType","nullable":true,"description":"**The specific hardware under `kind`** (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into the one register. Null for a device with no finer type than its kind.\n"},"hardwareModelId":{"type":"string","format":"uuid","nullable":true,"description":"The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it.\n"},"serialNumber":{"type":"string","nullable":true,"maxLength":100,"description":"The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). A serial already registered in the tenant is refused `409` by `registerDevice`.\n"},"ipNetworkReference":{"type":"string","nullable":true,"description":"Network address or reference the device is reached at (ADR-0067)."},"configurationVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Access configuration version the device reports running (ADR-0067)."},"localRuleVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Admission rule package the device reports running (ADR-0067)."},"credentialSecurityPackageVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Credential security package the device reports running (ADR-0067)."},"scannerHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Component health as the device or vendor reports it on its heartbeat (ADR-0067)."},"controllerHealth":{"type":"string","nullable":true,"readOnly":true},"cameraHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Where the device has a camera."},"connectivity":{"type":"string","nullable":true,"readOnly":true,"description":"Reported connectivity."},"pushToken":{"type":"string","format":"password","nullable":true,"writeOnly":true,"description":"BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only, and marked `writeOnly`: accepted by `registerDevice` and never returned by `listDevices` or `getDevice`. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"},"pushPlatform":{"type":"string","nullable":true,"enum":["ios","android","web","windows"]},"pushFailureCount":{"type":"integer","default":0,"readOnly":true,"description":"**Consecutive failures.** A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a notification queue fills with nothing.\n"},"offlineScope":{"type":"string","nullable":true,"enum":["none","readOnly","sellAndScan","fullVenue"],"description":"BL-163. **What this device may do with no connection**, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled.\n**`fullVenue` on a personal handset is a decision, not a default** — a device that can do everything offline is a device that carries the whole venue's data in somebody's pocket.\n"},"firmwareVersion":{"type":"string","nullable":true,"readOnly":true,"description":"As the device last reported it on its heartbeat."},"isRequired":{"type":"boolean","description":"True blocks shift open when the device is unreachable."},"status":{"type":"string","readOnly":true,"enum":["online","offline","error","consumableLow","needsAttention","localMode","unknown"],"description":"What the device last said on its heartbeat; `unknown` until it has. `localMode` is an access-control device validating from its offline package with its link down (ADR-0067).\n"},"batteryPercent":{"type":"integer","nullable":true,"readOnly":true,"minimum":0,"maximum":100,"description":"Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"},"lastCheckedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Distinct from `lastHeartbeatAt`.** A heartbeat is the workstation saying the device is attached; a check is the device answering. **A printer with no paper heartbeats perfectly**, which is why the client's board shows both columns.\n"},"health":{"type":"string","enum":["healthy","warning","degraded","offline","unknown"],"default":"unknown","readOnly":true,"description":"**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"capabilities":{"type":"array","readOnly":true,"items":{"$ref":"#/components/schemas/DeviceCapability"},"description":"BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is standards-first — the device does what the device does — and until now a venue could switch on a feature that depended on hardware without anything being able to say whether the hardware was there.\n**A capability absent is a capability unavailable**, not a capability assumed. A venue setting that requires one is refused where no device in scope reports it, rather than silently doing nothing at the gate.\n"},"enrolmentState":{"type":"string","enum":["registered","enrolled","provisioned","active","deactivated","retired"],"default":"registered","readOnly":true,"description":"BL-160. **Where the device is in its life, which is not the same question as whether it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled, provisioned, active, deactivated, retired — since 16.1.2, and until now there was no column for it to land in, so the operation read this table and wrote nothing.\n**Distinct from `status` and from `health`.** `status` is what the device last said and `health` is what we computed from it; a decommissioned turnstile still sitting on the network is `online` and `retired` at once, and neither column contradicts the other. **A device that is `retired` is refused at the gate whatever its status says.**\nThe transition itself — who moved it, from what, and why — is a `tenancy.device_audit` record. It is not repeated here, because the latest transition stored in two places is one place to go stale.\n"},"retiredAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from `tenancy.device_audit`, and kept as a column for the same reason `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit log is a date nobody filters a fleet by.\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The profile this device was provisioned with.** `enrolDevice` has accepted one since 16.1.3 and there was nowhere to keep it, so the answer to *\"what is this reader configured as\"* lived only in the request that set it.\n"}}},
"StoredForwardTransaction": {"type":"object","x-ticvai-persistence":"payments.stored_forward","description":"Board 3.8. **Money taken that the platform does not yet know about.**","properties":{"id":{"type":"string","format":"uuid"},"deviceId":{"type":"string","format":"uuid"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"takenAt":{"type":"string","format":"date-time"},"maskedPan":{"type":"string","nullable":true},"status":{"type":"string","enum":["held","forwarding","accepted","rejected","expired"]},"attempts":{"type":"integer","default":0},"rejectionReason":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"WorkOrder": {"x-ticvai-persistence":"maintenance.work_order","x-ticvai-retired-columns":["is_overdue"],"type":"object","required":["id","workOrderNumber","title","venueId","status","priority","kind","createdAt"],"properties":{"downtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"},"rootCause":{"type":"string","nullable":true,"enum":["wearAndTear","operatorError","guestDamage","manufacturingDefect","environmental","softwareFault","powerFailure","deferredMaintenance","unknown"],"description":"**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"},"rootCauseNote":{"type":"string","nullable":true},"escalatedAt":{"type":"string","format":"date-time","nullable":true},"escalationLevel":{"type":"integer","default":0,"description":"**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"},"id":{"type":"string","format":"uuid"},"workOrderNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"title":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"assetName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"},"status":{"$ref":"#/components/schemas/WorkOrderStatus"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."},"prioritySource":{"type":"string","enum":["scored","assetOverride","manual"],"readOnly":true,"description":"Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","items":{"type":"string"},"description":"Skills the job needs (M17-13)."},"kind":{"$ref":"#/components/schemas/WorkOrderKind"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"},"locationDescription":{"type":"string","maxLength":500,"nullable":true,"description":"Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"},"elapsedMinutes":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"},"isTimerRunning":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"},"dueAt":{"type":"string","format":"date-time","nullable":true},"isOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"},"requiresVerification":{"type":"boolean"},"sourcePlanId":{"type":"string","format":"uuid","nullable":true},"sourceInspectionId":{"type":"string","format":"uuid","nullable":true},"sourceIncidentId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderFaultAssessment": {"x-ticvai-persistence":"none — columns on maintenance.work_order","type":"object","description":"What the person raising a fault says about it, which the priority score reads (M17-01).","properties":{"safetyRisk":{"type":"boolean","default":false},"guestImpact":{"type":"string","enum":["none","degraded","closed"],"default":"none"}}},
"WorkOrderKind": {"type":"string","enum":["corrective","planned","inspectionFollowUp","incidentCorrective","improvement"]},
"WorkOrderPriority": {"type":"string","enum":["low","normal","high","urgent","emergency"]},
"WorkOrderStatus": {"type":"string","enum":["open","assigned","inProgress","paused","awaitingParts","completed","verified","closed","cancelled"]}
}
```
