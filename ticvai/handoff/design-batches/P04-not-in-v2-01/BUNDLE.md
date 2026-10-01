# P04-not-in-v2-01 — P04 · Screens the v2 build does not draw

**7 screens · 33 operations · 61 schemas · 23 permissions**

Platform P04 Venue POS · ships as **venue-pos** ·
staff audience · posTerminal ·
offline-capable

## Why this batch is drawn

No view in the POS v2 build or the approved build. The frames on disk were drawn in Claude Design on 29 September in the approved build's style; draw them again in v2's look (handoff/design-batches/apps/2-pos/README.md). POS-009 and POS-015 build on v2's shift panel, without 'Expected in drawer' (POS v2 decision POSV2-3). The look to match is `sources/designs/TICVAI_POS_Terminal_v2.html` (its shift panel: `wireframes/incoming/P04-pos-v2/img/v2-shift.jpg`), not the approved build below.

## Who this is for

**staff on posTerminal.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 23 permissions apply here:
  `ASSET_LIBRARY_VIEW, ATTENDANCE_RECORD, CASH_LIFT, CASH_NO_SALE, ORDER_CREATE, ORDER_EXCHANGE, ORDER_VIEW, OVERSHORT_ACCEPT, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE, REPORT_VIEW_WORKSTATION`…. A control nobody can use must say so,
  not sit enabled and fail.
- **16 of these operations work offline**: createCashMovement, getCurrentShift, getMediaAsset, getMediaEntitlements, getShift, getVenueSettings, listCashMovements, listDepositBoxes
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
| `POS-009` | Staff Roster | A | 62 | 92 | 6 | 23 | 1 | 0 | — | notStarted (designed) |
| `POS-010` | Add to Existing Ticket | A | 37 | 39 | 5 | 44 | 3 | 0 | — | notStarted (designed) |
| `POS-015` | Cash Operations Dashboard | A | 0 | 34 | 6 | 0 | 2 | 6 | — | notStarted (designed) |
| `POS-017` | Cash In / Cash Out Operations | A | 25 | 0 | 5 | 0 | 2 | 6 | — | notStarted (designed) |
| `POS-018` | Safe Drop & Cash Transfer Management | A | 39 | 30 | 6 | 15 | 1 | 6 | — | notStarted (designed) |
| `POS-019` | Shift Templates & Policies | A | 76 | 37 | 6 | 18 | 1 | 6 | — | notStarted (designed) |
| `POS-024` | Outlet Setup | A | 22 | 29 | 6 | 5 | 0 | 0 | — | notStarted (designed) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `POS-009` Staff Roster

**See who is on duty and on which terminal.**

| | |
|---|---|
| App · platform | TICVAI POS · P04 Venue POS (terminal) |
| Module | Shift · wave 2 · needs the `core` module |
| Block | Block A · ticket #18136 (APP-POS-POS-009) |
| Who uses it | venue staff holding `ATTENDANCE_RECORD`, `CASH_NO_SALE`, `OVERSHORT_ACCEPT`, `REPORT_VIEW_VENUE`, `REPORT_VIEW_WORKSTATION`, `SCOPE_VIEW`… (10 operate, 2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (touchLarge density): `approveShiftOpen` decides items that `listShifts` queues — every row is waiting for a person, so the empty state is success |
| Offline | Last known roster, with its age shown |
| Opens with | `shiftId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/sell/staff-roster` |

**What the spec says about it.** Close counts each foreign currency separately (`foreignHoldings`). **A variance collapsed into a base-currency total cannot be attributed to the currency that caused it.** **createCashMovement removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class). **Improved 20 August against the client design board**, answering 2 board screen(s): Shift & Operator Dashboard; Operator & Workstation Assignment. **Owns POS board frame(s) POS-3A** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listShifts`. | `listShifts` ?workstationId |
| Status | select | optional | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | — | Sends `?status=` to `listShifts`. | `listShifts` ?status |
| Opened from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedFrom=` to `listShifts`. | `listShifts` ?openedFrom |
| Opened to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedTo=` to `listShifts`. | `listShifts` ?openedTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `listRotaAssignments` ?from |
| To | date picker | — | — | `listRotaAssignments` ?to |
| Principal | picker: choose a principal | — | — | `listRotaAssignments` ?principalId |
| Department | picker: choose a department | — | — | `listRotaAssignments` ?departmentId |
| Sale board kind | radio group | — | Ticketing · Fnb · Retail · Mixed | `listWorkstations` ?saleBoardKind |
| Status | radio group | — | Raised · Acknowledged · Resolved · Expired | `listAlerts` ?status |
| Severity | segmented control | — | Info · Warning · Critical | `listAlerts` ?severity |
| Workstation | picker: choose a workstation | — | — | `listAlerts` ?workstationId |
| Shift | picker: choose a shift | — | — | `listAlerts` ?shiftId |
| Item | picker: choose an item | — | — | `listAlerts` ?itemId |

**Form: Clock in, clock out, start or end a break** (modal, opened by *Clock in, clock out, start or end a break*; *Record* calls `recordAttendance`, *Cancel* sends nothing)

**Collects what `recordAttendance` sends before it is called.** Required: `kind` (clockIn, clockOut, breakStart, breakEnd) and `occurredAt`, the device time. Optional: `assignmentId`, `accessPointId`. An out-of-sequence clock (a clock-out with no clock-in) is refused 409 and reported, never corrected. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Clock in · Clock out · Break start · Break end | — | — | `recordAttendance` body |
| Occurred at `occurredAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time. The server records both this and when it arrived. | `recordAttendance` body |
| Assignment `assignmentId` | picker: choose an assignment | optional | — | — | shows names, sends the id | — | `recordAttendance` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | — | `recordAttendance` body |
| Latitude `latitude` | number field | optional | — | — | — | — | `recordAttendance` body |
| Longitude `longitude` | number field | optional | — | — | — | — | `recordAttendance` body |

Errors to draw in the form: 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected.

**Form: Close shift** (confirmDialog, opened by *Close shift*; *Close the shift* calls `closeShift`, *Not yet* sends nothing)

**Names what `closeShift` changes and what it leaves alone**, in the consequence rather than the verb. A staff roster this affects should be identified in the dialog, not just counted. **Collects what `closeShift` sends before it is called.** Required: `countedCash`, `recordedAt`. Optional: `nonCashDeclared`, `notes`, `releaseHeldLeases`.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Counted cash `countedCash` | repeatable rows | required | — | at least 1; A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`. | — | The cashier's blind count, one line per denomination counted (decided 29 September, readiness close-out; our build plan). | `closeShift` body |
| Denomination `countedCash[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there. | `closeShift` body |
| Count `countedCash[].count` | number field | required | — | min 0; max 100000 | — | How many of this note or coin were counted. Zero is a line, not an omission: a denomination counted and found empty. | `closeShift` body |
| Total `countedCash[].total` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | `count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent. | `closeShift` body |
| Non cash declared `nonCashDeclared` | repeatable rows | optional | — | — | — | Declared totals per non-cash tender, for reconciliation against captured payments. | `closeShift` body |
| Tender `nonCashDeclared[].tender` | text field | required | — | — | — | — | `closeShift` body |
| Amount `nonCashDeclared[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `closeShift` body |
| Notes `notes` | text area | optional | — | max length 1000 | — | — | `closeShift` body |
| Release held leases `releaseHeldLeases` | toggle | optional | on | — | — | Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak. | `closeShift` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `closeShift` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not `open` or `suspended` — already closing or closed (problem type `shift-not-open`) — or open orders remain (`open-orders-remain`); 422 A counted line names an unknown or inactive denomination (`unknown-denomination`), repeats one (`duplicate-denomination`), or sends a `total` that disagrees …

**Form: Suspend shift** (confirmDialog, opened by *Suspend shift*; *Suspend* calls `suspendShift`, *Cancel* sends nothing)

**Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A staff roster this affects should be identified in the dialog, not just counted. **Collects what `suspendShift` sends before it is called.** Required: `recordedAt`. Optional: `reason`.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 200 | — | — | `suspendShift` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `suspendShift` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 Shift is not `open` (problem type `shift-not-open`)

**Form: Accept shift variance** (modal, opened by *Accept shift variance*; *Accept shift variance* calls `acceptShiftVariance`, *Cancel* sends nothing)

**Collects what `acceptShiftVariance` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | Retained for audit. The accepting principal is recorded. | `acceptShiftVariance` body |

Errors to draw in the form: 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (problem type `approver-is-cashier`) — a cashier signing off their own …; 409 Shift is not `pendingVariance` (problem type `shift-not-pending-variance`) — within tolerance, still open, or already accepted.

**Form: Approve shift open** (modal, opened by *Approve shift open*; *Approve shift open* calls `approveShiftOpen`, *Cancel* sends nothing)

**Collects what `approveShiftOpen` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 300 | — | — | `approveShiftOpen` body |

Errors to draw in the form: 409 Shift is not `pendingApproval` (problem type `shift-not-awaiting-approval`)

**Form: Open shift** (modal, opened by *Open shift*; *Open shift* calls `openShift`, *Cancel* sends nothing)

**Collects what `openShift` sends before it is called.** Required: `workstationId`, `openingFloat`. Optional: `depositBoxCode`, `bagNumber`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Workstation `workstationId` | picker: choose a workstation | required | — | — | shows names, sends the id | — | `openShift` body |
| Opening float `openingFloat` | repeatable rows | required | — | at least 1 | — | A count is a list of lines and the line is the row. Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — … | `openShift` body |
| ID `openingFloat[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `openShift` body |
| Shift `openingFloat[].shiftId` | picker: choose a shift | required | — | — | shows names, sends the id | A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are. | `openShift` body |
| Deposit box `openingFloat[].depositBoxId` | picker: choose a deposit box | optional | — | — | shows names, sends the id | — | `openShift` body |
| Count kind `openingFloat[].countKind` | segmented control | optional | — | Opening float · Close · Movement | — | Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). | `openShift` body |
| Cash movement `openingFloat[].cashMovementId` | picker: choose a cash movement | optional | — | — | shows names, sends the id | The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`. | `openShift` body |
| Denomination `openingFloat[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` — face value, kind and sort order live there. | `openShift` body |
| Counted quantity `openingFloat[].countedQuantity` | number field | required | — | min 0 | — | How many of this note or coin were in the drawer. | `openShift` body |
| Counted value `openingFloat[].countedValue` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Quantity times face value, stored. Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count. | `openShift` body |
| Counted by `openingFloat[].countedBy` | picker: choose a counted by | optional | — | — | shows names, sends the id | — | `openShift` body |
| Counted at `openingFloat[].countedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `openShift` body |
| Recount of `openingFloat[].recountOf` | picker: choose a recount of | optional | — | — | shows names, sends the id | A recount points at what it replaces rather than overwriting it. `requestRecount` exists because a variance is a question before it is a fact. | `openShift` body |
| Deposit box code `depositBoxCode` | text field | optional | — | max length 64 | — | Physical container assigned to this shift. Required where the venue configures deposit box allocation. | `openShift` body |
| Bag number `bagNumber` | text field | optional | — | max length 64 | — | Required where the venue configures bag numbers as mandatory. | `openShift` body |
| Recorded at `recordedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the device recorded it. `openShift` is online-only (F32), so this differs from server receipt time only by transit; it is kept because the shift's other device writes are … | `openShift` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A shift is already open on this workstation (problem type `shift-already-open`), or a required device is absent (`required-device-absent`).

**Form: Record no sale** (modal, opened by *Record no sale*; *Record no sale* calls `recordNoSale`, *Cancel* sends nothing)

**Collects what `recordNoSale` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `recordNoSale` body |
| Reason `reason` | radio group | required | — | Change for guest · Correct float · Retrieve dropped cash · Till check · Other | — | — | `recordNoSale` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `recordNoSale` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordNoSale` body |

Errors to draw in the form: 409 Shift is not open (problem type `shift-not-open`)

**Form: Reopen shift** (modal, opened by *Reopen shift*; *Reopen shift* calls `reopenShift`, *Cancel* sends nothing)

**Collects what `reopenShift` sends before it is called.** Required: `reason`, `supervisorStepUp` {`principalId`, `credential`}: the supervisor enters their staff PIN on this device, and may not be the principal who closed the shift. Refused 403 `approver-is-closer` or `supervisor-step-up-refused` (decided 28 September, audit R144). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `reopenShift` body |
| Supervisor step up `supervisorStepUp` | group | required | — | — | — | The supervisor signing the reopen on this device (audit R144). Replaces the bare `approverPrincipalId`, which named an approver without proving they were there. | `reopenShift` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `reopenShift` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `reopenShift` body |

Errors to draw in the form: 403 The supervisor is the closing principal (problem type `approver-is-closer`), or the step-up failed: the PIN did not verify, or the principal does not hold …; 409 Shift is not closed (problem type `shift-not-closed`), or the fiscal period has closed over it (`fiscal-period-closed`)

**Form: Resume shift** (modal, opened by *Resume shift*; *Resume shift* calls `resumeShift`, *Cancel* sends nothing)

**Collects what `resumeShift` sends before it is called.** Required: `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `resumeShift` body |

Errors to draw in the form: 403 Not the principal who suspended it, and the caller does not hold SHIFT_CLOSE_OTHER (problem type `not-shift-holder`).; 409 Another shift is now open on this workstation (problem type `shift-already-open`), or this shift is not `suspended` (`shift-not-suspended`)

**Form: Create rota assignment** (modal, opened by *Create rota assignment*; *Create rota assignment* calls `createRotaAssignment`, *Cancel* sends nothing)

**Collects what `createRotaAssignment` sends before it is called.** Required: `principalId`, `venueId`, `position`, `startsAt`, `endsAt`. Optional: `overtimeMinutes`, `restPeriodBefore`, `breachesWorkingHourLimit`, `labourCost`, `id`, `displayName`, `departmentId`, `requiredRoleId`, `workstationId`, `status`, `breakMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rest period before `restPeriodBefore` | number field | optional | — | — | — | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and unsafe in all of them. | `createRotaAssignment` body |
| Labour cost `labourCost` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. | `createRotaAssignment` body |
| Principal `principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `createRotaAssignment` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createRotaAssignment` body |
| Department `departmentId` | picker: choose a department | optional | — | — | shows names, sends the id | — | `createRotaAssignment` body |
| Position `position` | text field | required | — | — | — | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota assignment is not a shift. | `createRotaAssignment` body |
| Required role `requiredRoleId` | picker: choose a required role | optional | — | — | shows names, sends the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. | `createRotaAssignment` body |
| Workstation `workstationId` | picker: choose a workstation | optional | — | — | shows names, sends the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. | `createRotaAssignment` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRotaAssignment` body |
| Ends at `endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRotaAssignment` body |
| Status `status` | select | optional | — | Planned · Published · Confirmed · Swap pending · Cancelled · Completed · No show | — | — | `createRotaAssignment` body |
| Break minutes `breakMinutes` | number field (minutes) | optional | — | — | — | — | `createRotaAssignment` body |
| Note `note` | text area | optional | — | — | — | — | `createRotaAssignment` body |

Errors to draw in the form: 409 Overlaps an existing assignment, or the person lacks the required role

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |

**Every cash movement** (data table, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. |
| Kind | chip: Opening float, Lift, Add | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Denominations | list or chips (count when long) | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. |
| Reference | text | Safe drop reference or bag number. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Shift | the name it points at, never the id | — |
| Deposit box | the name it points at, never the id | The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099). |
| Witness principal | the name it points at, never the id | The cashier who countersigned a withdrawal. Null on other movements. |
| Withdrawal reason | chip: Banking, Safe drop, Change order, Other | Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records. |
| Authorised by principal | the name it points at, never the id | The principal who authorised the movement, recorded for audit. |

**Every rota assignment** (data table, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Breaches working hour limit | yes / no (icon or chip) | Flagged at assignment, not discovered at payroll. A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Display name | text | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Position | text | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota … |
| Required role | the name it points at, never the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. |
| Workstation | the name it points at, never the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. |

**Every workstation** (data table, from `listWorkstations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Region | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Scope path | text | — |
| Sale board | grouped details | Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. |
| Access point | the name it points at, never the id | Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point. |
| Devices | list or chips (count when long) | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |

**Every alert** (data table, from `listAlerts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Rule | the name it points at, never the id | — |
| Rule name | text | `AlertRule.name` as it stood when the alert was raised. The line a person reads — a list of rule ids is not an alert panel, and a screen … |
| Metric | chip: Occupancy, Capacity utilisation, Admission rate, No show rate, Conversion, Sales by … | The rule's metric, carried so the alert says what went out of range. |
| Raised at | 1 Oct 2026, 14:30 | — |
| Severity | chip: Info, Warning, Critical | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. |
| Status | chip: Raised, Acknowledged, Resolved, Expired | Where a raised alert is. Shared by `Alert` and the `listAlerts` filter. |
| Observed value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Threshold | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Scope path | text | — |
| Workstation | the name it points at, never the id | The workstation the reading was taken for, where the metric is measured per workstation (`salesByWorkstation`). |
| Shift | the name it points at, never the id | The till shift (`orders.pos_shift`) the reading belongs to, where it was taken for a workstation with a shift open. |

**Data table** (data table): Staff, role and terminal, shift, sales, status — the columns in the design

**The selected shift** (detail panel, from `getCurrentShift`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sales total | AED 1,234.50 | What the till took in sales, as the guest paid it — tax included. |
| Refunds total | AED 1,234.50 | What the till paid back, as the guest was refunded it — tax included. |
| Lifts total | AED 1,234.50 | Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net. |

**The shift** (detail panel, from `getShift`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sales total | AED 1,234.50 | What the till took in sales, as the guest paid it — tax included. |
| Refunds total | AED 1,234.50 | What the till paid back, as the guest was refunded it — tax included. |
| Lifts total | AED 1,234.50 | Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Accept shift variance (primary button) | `acceptShiftVariance` POST `/shifts/{shiftId}/accept-variance` | inline | Shift | 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (problem type `approver-is-cashier`) — a cashier signing off their own …; 409 Shift is not `pendingVariance` (problem type … | step-up: pin (A supervisor signs off a cashier's over/short at the till, in front of the drawer (audit R080 (e)).); opens modal first |
| Approve shift open (secondary button) | `approveShiftOpen` POST `/shifts/{shiftId}/approve-open` | inline | Shift | 409 Shift is not `pendingApproval` (problem type `shift-not-awaiting-approval`) | opens modal first |
| Close shift (destructive button) | `closeShift` POST `/shifts/{shiftId}/close` | CloseShiftRequest | ShiftCloseResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not `open` or `suspended` — already closing or closed (problem type `shift-not-open`) — or open orders remain … | opens confirmDialog first |
| Open shift (secondary button) | `openShift` POST `/shifts` | OpenShiftRequest | Shift | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A shift is already open on this workstation (problem type `shift-already-open`), or a required device is absent … | opens modal first |
| Record no sale (secondary button) | `recordNoSale` POST `/shifts/{shiftId}/no-sale` | inline | NoSaleEvent | 409 Shift is not open (problem type `shift-not-open`) | works offline; opens modal first |
| Reopen shift (secondary button) | `reopenShift` POST `/shifts/{shiftId}/reopen` | inline | Shift | 403 The supervisor is the closing principal (problem type `approver-is-closer`), or the step-up failed: the PIN did not verify, or the principal does not hold …; 409 Shift is not closed (problem type … | step-up: pin (Reopening a counted shift is a reversal; a supervisor signs it in place (audit R144).); opens modal first |
| Resume shift (secondary button) | `resumeShift` POST `/shifts/{shiftId}/resume` | inline | Shift | 403 Not the principal who suspended it, and the caller does not hold SHIFT_CLOSE_OTHER (problem type `not-shift-holder`).; 409 Another shift is now open on this workstation (problem type `shift-already-open`), or this … | works offline; opens modal first |
| Suspend shift (destructive button) | `suspendShift` POST `/shifts/{shiftId}/suspend` | inline | Shift | 403 Authenticated but not permitted at the requested scope; 409 Shift is not `open` (problem type `shift-not-open`) | works offline; opens confirmDialog first |
| Create rota assignment (secondary button) | `createRotaAssignment` POST `/rota-assignments` | RotaAssignment | RotaAssignment | 409 Overlaps an existing assignment, or the person lacks the required role | opens modal first |
| Clock in, clock out, start or end a break (secondary button) | `recordAttendance` POST `/attendance/clock` | inline | AttendanceRecord | 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected. | works offline; gated `ATTENDANCE_RECORD`; opens modal first |
| Export roster (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listShifts` (onLoad, Open shifts at this venue); `getCurrentShift` (onLoad, The open or suspended shift on the session's workstation); `getShift` (onLoad, Read a shift); `listCashMovements` (onLoad, Lifts, adds and the opening float); `listRotaAssignments` (onLoad, The rota); `listWorkstations` (onLoad, List workstations); `listAlerts` (onLoad, What is currently raised)

**Where the user goes next**

- → `POS-001` Begin Shift: *Begin Shift*; carries `shiftId`
- → `POS-007` Close Shift: *Close Shift*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staff roster list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staff roster untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, status, openedFrom, openedTo and the staff roster are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Last known roster, with its age shown |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A shift is already open on this workstation (problem type `shift-already-open`), or a required device is absent (`required-device-absent`).; 409 Another shift is now open on this workstation (problem type `shift-already-open`), or this shift is not `suspended` (`shift-not-suspended`); 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported … |

#### Permissions

- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `acceptShiftVariance` → `OVERSHORT_ACCEPT` (operate) · staff · step-up pin
- `approveShiftOpen` → `SHIFT_APPROVE_OPEN` (operate) · staff
- `closeShift` → `SHIFT_CLOSE` (operate) · staff
- `getCurrentShift` → `SHIFT_OPEN` (operate) · staff
- `getShift` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listCashMovements` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `openShift` → `SHIFT_OPEN` (operate) · staff
- `recordNoSale` → `CASH_NO_SALE` (operate) · staff
- `reopenShift` → `SHIFT_REOPEN` (operate) · staff · step-up pin
- `resumeShift` → `SHIFT_OPEN` (operate) · staff
- `suspendShift` → `SHIFT_SUSPEND` (operate) · staff
- `createRotaAssignment` → `WORKFORCE_MANAGE` (configure) · staff
- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff
- `listWorkstations` → `SCOPE_VIEW` (read) · staff
- `listAlerts` → `REPORT_VIEW_VENUE` (operate) · staff
- `recordAttendance` → `ATTENDANCE_RECORD` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

23 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.9.8 | The system should allow the option of configuring the requirement of a supervisor's approval for opening and closing a cashier's session. For example, to open a cashier’s session, the cashier details … | F&B & Guest Management | CONTRACTED | `approveShiftOpen` |
| 5.8.3 | The system should allow the cashier to enter a total amount counted, or to count by denomination. For denomination counts, the cashier counts and enters each denomination separately and each count is … | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.1 | The system should be able to manage end of day shift closing and provide the ability to close out each cash register. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.2 | The system should have the ability to do a "blind" cashier close-out. Over-shorts should be captured and recorded. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.5 | The system should allow automatic closing of a cashier's session after a configurable time period. The supervisor should be notified on closing of the session. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| … 11 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Shift management: assignment and scheduling by cashier/department, templates and policies, opening/closing, exceptions/alerts. Allam: explore merging shift-closing and till-closing screens to reduce dashboard count. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-309)*

Also apply: 41 for all of P04, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P04 Venue POS.dc.html#pos-009` · status **notStarted** · provenance designed · **Drawn by Claude Design on `POS Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Prototype (TICVAI OS 4.2.1, build 2026.08.14, verified —, match none): `sources/designs/TICVAI_POS_Terminal_client_approved.html`, view **
- Derived from `wireframes/reference/POS Board 3.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 3.dc.html#pos-3a`
- Flow F74 *A shift closes and the day is reported*, step 3: Staffing against takings is read. → **Takings per staffed hour is the number a venue manager actually wants**, and it needs both sides.

#### Acceptance for the design

- [ ] Every input above is drawn (62), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (92 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#POS-009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Accept shift variance, Approve shift open, Close shift, Open shift, Record no sale, Reopen shift, Resume shift, Suspend shift, Create rota assignment, Clock in, clock out, start or end a …, Export roster.
- [ ] Every transition is wired: `POS-001`, `POS-007`.
- [ ] Every gated control is gated: `ATTENDANCE_RECORD`, `CASH_NO_SALE`, `OVERSHORT_ACCEPT`, `REPORT_VIEW_VENUE`, `REPORT_VIEW_WORKSTATION`, `SCOPE_VIEW`, `SHIFT_APPROVE_OPEN`, `SHIFT_CLOSE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `POS-010` Add to Existing Ticket

**Sell something onto media the guest is already carrying.**

| | |
|---|---|
| App · platform | TICVAI POS · P04 Venue POS (terminal) |
| Module | Sell · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #18001 (APP-POS-POS-010) |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW`, `ORDER_CREATE`, `ORDER_EXCHANGE`, `ORDER_VIEW` (2 read, 2 operate); in the flows as cashier |
| Device and orientation | This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (touchLarge density): `getMediaEntitlements` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Not available.** The entitlement set must be read live; appending to a stale picture double-sells a locker |
| Opens with | `mediaCode` (deepLink), `mediaId` (deepLink), `cartId` (session), `orderId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/sell/add-to-existing-ticket` |

**What the spec says about it.** CF-58, from the 14 August MoM. Not in the delivered mockups. **9 assets operations removed 18 August (CF-114).** The whole media contract was attached to this screen. **A till adding an item to a ticket does not manage a media library** — it reads the asset it needs and nothing else. Same shape as CF-87, one level up: that attached sibling operations, this attached a whole contract. **Wired 24 August from review**: getCart, exchangeOrderLines. **The operations existed and this screen could not call them** — reviewers reported them as missing APIs, which is what an unreachable operation looks like from a wireframe.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
|  | scan target | — | — | — | — | Scan the guest QR, wristband or card first. The media is the join, not the order | — |

**Form: Append entitlement to media** (modal, opened by *Append entitlement to media*; *Append entitlement to media* calls `appendEntitlementToMedia`, *Cancel* sends nothing)

**Collects what `appendEntitlementToMedia` sends before it is called.** Required: `id`, `lines`, `recordedAt`. Optional: `paymentMethod`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the new order this creates, and its idempotency key — it must equal the `Idempotency-Key` header. | `appendEntitlementToMedia` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `appendEntitlementToMedia` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `appendEntitlementToMedia` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `appendEntitlementToMedia` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `appendEntitlementToMedia` body |
| Payment method `paymentMethod` | radio group | optional | — | Card · Cash · Wallet · Gift card · Charge to account | — | — | `appendEntitlementToMedia` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `appendEntitlementToMedia` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `appendEntitlementToMedia` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or the entitlement cannot share media … (AppendRefusedProblem)

**Form: Exchange order lines** (modal, opened by *Exchange order lines*; *Exchange order lines* calls `exchangeOrderLines`, *Cancel* sends nothing)

**Collects what `exchangeOrderLines` sends before it is called.** Required: `id`, `outgoingLineIds`, `incomingLines`, `recordedAt`. Optional: `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header. | `exchangeOrderLines` body |
| Outgoing lines `outgoingLineIds` | multi-picker: choose outgoing lines | required | — | at least 1 | — | — | `exchangeOrderLines` body |
| Incoming lines `incomingLines` | repeatable rows | required | — | at least 1 | — | — | `exchangeOrderLines` body |
| ID `incomingLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `exchangeOrderLines` body |
| Variant `incomingLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `exchangeOrderLines` body |
| Recommendation `incomingLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `exchangeOrderLines` body |
| Performance `incomingLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `exchangeOrderLines` body |
| Booked window `incomingLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `exchangeOrderLines` body |
| Starts at `incomingLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exchangeOrderLines` body |
| Ends at `incomingLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `exchangeOrderLines` body |
| Inventory hold `incomingLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `exchangeOrderLines` body |
| Seats `incomingLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `exchangeOrderLines` body |
| Resource hold `incomingLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `exchangeOrderLines` body |
| Attributes `incomingLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `exchangeOrderLines` body |
| Transport `incomingLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `exchangeOrderLines` body |
| Quantity `incomingLines[].quantity` | number field | required | — | min 1 | — | — | `exchangeOrderLines` body |
| Eligibility declaration `incomingLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `exchangeOrderLines` body |
| Age band `incomingLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `exchangeOrderLines` body |
| Age years `incomingLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `exchangeOrderLines` body |
| Height band index `incomingLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `exchangeOrderLines` body |
| Confident swimmer `incomingLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `exchangeOrderLines` body |
| Guardian signed `incomingLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `exchangeOrderLines` body |
| Quoted unit price `incomingLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `exchangeOrderLines` body |
| Holder name `incomingLines[].holderName` | text field | optional | — | — | — | — | `exchangeOrderLines` body |
| Data mask values `incomingLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `exchangeOrderLines` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `exchangeOrderLines` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `exchangeOrderLines` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exchangeOrderLines` body |

Errors to draw in the form: 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem)

#### Outputs: what the screen shows and produces

**Shown**

**The media entitlements** (detail panel, from `getMediaEntitlements`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Media kind | chip: QR, Wristband, Card, NFC, Mobile pass | — |
| Subject | the name it points at, never the id | — |
| Is valid | yes / no (icon or chip) | — |
| Invalid reason | text | — |
| Can accept more | yes / no (icon or chip) | False where the media has been surrendered, expired or blocked. A cashier should know before taking money, not after. |
| Entitlements | list or chips (count when long) | — |

**The media asset** (detail panel, from `getMediaAsset`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Image, Video, Audio, Document, Vector, Font… | — |
| Status | chip: Processing, Ready, Quarantined, Failed, Archived | — |
| Filename | text | — |
| Content type | text | — |
| Size bytes | 1,234 | — |
| Title | in the reader's language | — |
| Description | in the reader's language | Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored. |
| Alt text | in the reader's language | Required before use in a guest-facing surface. WCAG 2.2 AA. |
| Width | 1,234 | — |
| Height | 1,234 | — |
| Duration seconds | 1,234.5 | — |
| Custom metadata | grouped details | BL-178. `assets` is a strong contract and its metadata was fixed — kind, title, alt text, dimensions, rights. |
| Shared with tenants | list or chips (count when long) | BL-178. Cross-tenant sharing, and it is refused by default for a reason. |
| Tags | list or chips (count when long) | — |
| Venue | the name it points at, never the id | — |

**The cart** (detail panel, from `getCart`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Token | text | How an anonymous guest returns to their cart, including from a recovery email. Rotated on claim, so a link shared before signing in does … |
| Venue | the name it points at, never the id | — |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing … |
| Subject | the name it points at, never the id | Null while anonymous. Set by `claimCart`. |
| Status | chip: Active, Expiring, Expired, Abandoned, Checked out | — |
| Lines | list or chips (count when long) | — |
| Conflicts | list or chips (count when long) | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discount total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied promotions | list or chips (count when long) | Re-evaluated on every read. A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became … |
| Expires at | 1 Oct 2026, 14:30 | The earliest lease expiry in the cart, or the cart's own window where it holds none. |
| Extensions used | 1,234 | — |
| Max extensions | 1,234 | — |

**Detail panel** (detail panel): What they already hold — so a cashier does not sell a locker to someone who has one

**Banner** (banner): Surrendered, expired or blocked media is refused before money is taken, not after

**Sale board** (sale board): Only variants whose template allows canShareMedia

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Append entitlement to media (primary button) | `appendEntitlementToMedia` POST `/media/{mediaCode}/entitlements` | AppendEntitlementRequest | AppendEntitlementResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or … | opens modal first; produces a document or message: Add something to a ticket the guest already holds |
| Exchange order lines (secondary button) | `exchangeOrderLines` POST `/orders/{orderId}/exchanges` | ExchangeOrderRequest | OrderExchangeResult | 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem) | opens modal first |
| Add and pay (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `getMediaAsset` (onLoad, Read an asset with derivatives and usage); `getCart` (onLoad, The cart, priced and checked, right now)

**Where the user goes next**

- → `POS-002` Sell — Ticket Catalogue: *Sell — Ticket Catalogue*; carries `orderId`, `promotionId`
- → `POS-003` Sell — Timed Entry: *Sell — Timed Entry*
- → `POS-004` Sell — Seat Map: *Sell — Seat Map*; carries `performanceId`
- → `POS-005` Payment: *Payment*; carries `paymentId`
- → `POS-011` Returns, Refunds & Exchanges: *They change their mind about the locker*; carries `orderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The add existing ticket, read by `getMediaEntitlements`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the add existing ticket untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No add existing ticket yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Not available.** The entitlement set must be read live; appending to a stale picture double-sells a locker |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or the entitlement cannot share media … (AppendRefusedProblem); 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem) |

#### Permissions

- `getMediaEntitlements` → `ORDER_VIEW` (read) · staff
- `appendEntitlementToMedia` → `ORDER_CREATE` (operate) · staff
- `getMediaAsset` → `ASSET_LIBRARY_VIEW` (read) · staff
- `getCart` → no permission · guest, partner, staff
- `exchangeOrderLines` → `ORDER_EXCHANGE` (operate) · staff, partner

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

44 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.11 | Ticket Storage - System shall store digital tickets. | Guest Mobile App & Branding | CONTRACTED | `getMediaEntitlements` |
| 2.6.18 | - Dynamic QR code | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.7.24 | The BtoB Customer can also receive simple QR Codes, vouchers or packaged PLUs. | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.13.3 | Tickets can be issued and sent either by email (PDF or M-ticket, E-ticket). | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.14.16 | Generate digital cards with QR/NFC/barcode. | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.16.2 | The system should support multiple media types for a ticket. Expected formats: - Paper/thermal tickets with QR, Barcode, RFID - Print at home tickets with QR, Barcode - Smartphones: NFC (near-field … | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.16.17 | The system shall allow multiple media types to be linked to the same guest account and entitlement simultaneously, including QR tickets, RFID wristbands, membership cards, and mobile wallets. | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 3.1.1 | Dynamic QR Code Supports: 1. Registration: Customers select "Digital Ticket" via the confirmation page, email, or ticket PDF to begin the enrollment process. 2.Activation: After registration, the … | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 3.1.2 | Unique Code per Ticket: Generate a unique QR code for every issued ticket or pass. | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 3.1.7 | Dynamic QR technology shall support memberships, annual passes, loyalty accounts, wallets, and other digital credentials in addition to standard tickets. | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 3.2.63 | It is expected that the access code created by the system is unique and randomized to improve fraud prevention. | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 5.4.18 | Provide digital loyalty card in app. | F&B & Guest Management | CONTRACTED | `getMediaEntitlements` |
| … 32 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Upgrade eligibility checks validity/usage. Cases: seated ticket to a better section same day, paying the difference at the counter; general admission to season pass with the amount paid credited. Windows: before use, after use within a window, or until a cutoff (event ticket until the guest exits). *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-603)*
- The till can add an item to an existing ticket (e.g. a locker) after the sale; not in the delivered mockups. *(agreed · MoM 14 Aug 2026, (cited as CF-58 in POS-010 notes) · DI-314)*
- Add-on entitlements (e.g. a locker) are linked to the existing ticket QR by scanning it, not issued as a new QR. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-295)*

Also apply: 5 for P04 · Sell, 41 for all of P04, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P04 Venue POS.dc.html#pos-010` · status **notStarted** · provenance designed
- Prototype (TICVAI OS 4.2.1, build 2026.08.14, verified —, match none): `sources/designs/TICVAI_POS_Terminal_client_approved.html`, view **
- Flow F58 *A ticket is sold at a till, added to, and refunded*, step 7: The guest asks to add a locker to the ticket they just bought. → **Appended to the existing media rather than issued as a second ticket.** A guest carrying two cards for one visit is a guest who will present the wrong one at a gate.

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state (404, 409, 410).
- [ ] Every output is drawn (39 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#POS-010?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Append entitlement to media, Exchange order lines, Add and pay.
- [ ] Every transition is wired: `POS-002`, `POS-003`, `POS-004`, `POS-005`, `POS-011`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`, `ORDER_CREATE`, `ORDER_EXCHANGE`, `ORDER_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `POS-015` Cash Operations Dashboard

**Cash Operations Dashboard — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI POS · P04 Venue POS (terminal) |
| Module | Sell · wave 1 · needs the `core` module |
| Block | Block A · ticket #17886 (APP-POS-POS-015) |
| Who uses it | venue staff holding `REPORT_VIEW_WORKSTATION`, `SHIFT_OPEN` (2 operate); in the flows as venue manager |
| Device and orientation | This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. · LTR and RTL · light, dark theme |
| Pattern | listDetail (touchLarge density): `listCashMovements` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |
| Opens with | `workstationId` (session), `shiftId` (deepLink) · cold entry: **Resolves from the session, which carries the workstation** — a till is signed into, not navigated to. |
| Route | `/sell/cash-operations-dashboard` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Open only | toggle | — | — | `listDepositBoxes` ?openOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every cash movement** (data table, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. |
| Kind | chip: Opening float, Lift, Add | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Denominations | list or chips (count when long) | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. |
| Reference | text | Safe drop reference or bag number. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Shift | the name it points at, never the id | — |
| Authorised by principal | the name it points at, never the id | The principal who authorised the movement, recorded for audit. |
| Sequence | 1,234 | Monotonic within the shift. Preserves order across an offline batch. |
| Synced at | 1 Oct 2026, 14:30 | — |

**Every deposit box** (data table, from `listDepositBoxes`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Cashier principal | the name it points at, never the id | — |
| Cashier name | text | — |
| Venue | the name it points at, never the id | — |
| Workstation | the name it points at, never the id | Where it is being used now. Changes during a shift; the box does not. |
| Shift | the name it points at, never the id | The shift trading from this box. A UUIDv7, as `Shift.id` is. |
| Status | chip: Allocated, Open, Suspended, Closing, Closed, Reconciled | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Opening denominations | list or chips (count when long) | 5.8.3. Either this or a total — a supervisor handing over a counted bag should not have to re-count it into fields. |
| Withdrawn total | AED 1,234.50 | Reduces the expected close figure. Cash skimmed for banking is not a shortfall, and a system that treats it as one makes every busy cashier … |
| Foreign holdings | list or chips (count when long) | 4.6.11 and 6.1.10. Foreign cash accepted at this till, counted separately by currency. |
| Expected total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**The selected cash movement** (detail panel, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. |
| Kind | chip: Opening float, Lift, Add | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Denominations | list or chips (count when long) | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. |
| Reference | text | Safe drop reference or bag number. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Shift | the name it points at, never the id | — |
| Authorised by principal | the name it points at, never the id | The principal who authorised the movement, recorded for audit. |
| Sequence | 1,234 | Monotonic within the shift. Preserves order across an offline batch. |
| Synced at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listCashMovements` (onLoad, Lifts, adds and the opening float); `listDepositBoxes` (onLoad, Cash boxes and who holds them)

**Where the user goes next**

- → `POS-001` Begin Shift: *Begin Shift*; carries `shiftId`
- → `POS-018` Safe Drop & Cash Transfer Management: *Safe drop destinations are allocated*; carries `shiftId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cash operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cash operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cash operations yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCashMovements` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listCashMovements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |

#### Permissions

- `listCashMovements` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listDepositBoxes` → `SHIFT_OPEN` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listCashMovements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Till/cash management shows total cash and card transactions and variance tracking, and supports cash-in/cash-out for mid-shift cash pickups. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-308)*
- Shift/session view shows open and closed sessions per workstation with expected cash and card totals; a live till monitor shows real-time cash status per workstation and open/close codes. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-273)*

Also apply: 5 for P04 · Sell, 41 for all of P04, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P04 Venue POS.dc.html#pos-015` · status **notStarted** · provenance designed
- Prototype (TICVAI OS 4.2.1, build 2026.08.14, verified —, match none): `sources/designs/TICVAI_POS_Terminal_client_approved.html`, view **
- Flow F73 *A till is configured and its cash rules set*, step 3: Cash limits and the drawer ceiling are set. → **A ceiling on the drawer is a security control.** F32 step 4 is the safe drop it forces.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#POS-015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm.
- [ ] Every transition is wired: `POS-001`, `POS-018`.
- [ ] Every gated control is gated: `REPORT_VIEW_WORKSTATION`, `SHIFT_OPEN`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `POS-017` Cash In / Cash Out Operations

**Cash In / Cash Out Operations — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI POS · P04 Venue POS (terminal) |
| Module | Sell · wave 1 · needs the `core` module |
| Block | Block A · ticket #17888 (APP-POS-POS-017) |
| Who uses it | venue staff holding `CASH_LIFT` (1 operate) |
| Device and orientation | This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. · LTR and RTL · light, dark theme |
| Pattern | configEditor (touchLarge density): the screen declares only writes (`createCashMovement`) and no read of a population — it is settings, not a list |
| Offline | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |
| Opens with | `workstationId` (session), `shiftId` (deepLink) · cold entry: **Resolves from the session, which carries the workstation** — a till is signed into, not navigated to. |
| Route | `/sell/cash-in-cash-out-operations` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Drawn 31 August** — `POS Frontline Board 2.dc.html` frame `pos-2d`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Cash In / Cash Out Operations* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| id | picker: choose an id (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Client-generated UUIDv7. | `CreateCashMovementRequest.id` |
| kind | segmented control | optional | — | Opening float · Lift · Add | — | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`. | `CreateCashMovementRequest.kind` |
| amount | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `CreateCashMovementRequest.amount` |
| denominations | repeatable rows | optional | — | at least 1 | — | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. | `CreateCashMovementRequest.denominations` |
| reference | text field | optional | — | max length 64 | — | Safe drop reference or bag number. | `CreateCashMovementRequest.reference` |
| reason | text area | optional | — | max length 500 | — | — | `CreateCashMovementRequest.reason` |
| recordedAt | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `CreateCashMovementRequest.recordedAt` |

**Sent by *Create cash movement*** (`createCashMovement`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. | `createCashMovement` body |
| Kind `kind` | segmented control | required | — | Opening float · Lift · Add | — | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`. | `createCashMovement` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createCashMovement` body |
| Denominations `denominations` | repeatable rows | optional | — | at least 1 | — | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. | `createCashMovement` body |
| ID `denominations[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Shift `denominations[].shiftId` | picker: choose a shift | required | — | — | shows names, sends the id | A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are. | `createCashMovement` body |
| Deposit box `denominations[].depositBoxId` | picker: choose a deposit box | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Count kind `denominations[].countKind` | segmented control | optional | — | Opening float · Close · Movement | — | Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). | `createCashMovement` body |
| Cash movement `denominations[].cashMovementId` | picker: choose a cash movement | optional | — | — | shows names, sends the id | The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`. | `createCashMovement` body |
| Denomination `denominations[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` — face value, kind and sort order live there. | `createCashMovement` body |
| Counted quantity `denominations[].countedQuantity` | number field | required | — | min 0 | — | How many of this note or coin were in the drawer. | `createCashMovement` body |
| Counted value `denominations[].countedValue` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Quantity times face value, stored. Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count. | `createCashMovement` body |
| Counted by `denominations[].countedBy` | picker: choose a counted by | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Counted at `denominations[].countedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCashMovement` body |
| Recount of `denominations[].recountOf` | picker: choose a recount of | optional | — | — | shows names, sends the id | A recount points at what it replaces rather than overwriting it. `requestRecount` exists because a variance is a question before it is a fact. | `createCashMovement` body |
| Reference `reference` | text field | optional | — | max length 64 | — | Safe drop reference or bag number. | `createCashMovement` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `createCashMovement` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCashMovement` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Create cash movement (primary button) | `createCashMovement` POST `/shifts/{shiftId}/cash-movements` | CreateCashMovementRequest | CashMovement | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since … | works offline |

**Where the user goes next**

- → `POS-001` Begin Shift: *Begin Shift*; carries `shiftId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved cash cash out. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cash cash out untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cash cash out configured. The form opens empty and `createCashMovement` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `CASH_LIFT`, which `createCashMovement` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since (`lift-exceeds-float`, audit R123 … |

#### Permissions

- `createCashMovement` → `CASH_LIFT` (operate) · staff

**A refused user sees:** Shown when the caller lacks `CASH_LIFT`, which `createCashMovement` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Till/cash management shows total cash and card transactions and variance tracking, and supports cash-in/cash-out for mid-shift cash pickups. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-308)*
- Configurable cash-drawer limit: on a busy day the cashier unloads excess cash mid-shift; the unloaded amount is held separately (partial hold) and reconciled at final close. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-274)*

Also apply: 5 for P04 · Sell, 41 for all of P04, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P04 Venue POS.dc.html#pos-017` · status **notStarted** · provenance designed · **Drawn by Claude Design on `POS Frontline Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been …
- Prototype (TICVAI OS 4.2.1, build 2026.08.14, verified —, match none): `sources/designs/TICVAI_POS_Terminal_client_approved.html`, view **
- Derived from `wireframes/reference/POS Frontline Board 2.dc.html`
- Client design-board frames: `POS Frontline Board 2.dc.html#pos-2d`

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#POS-017?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create cash movement.
- [ ] Every transition is wired: `POS-001`.
- [ ] Every gated control is gated: `CASH_LIFT`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `POS-018` Safe Drop & Cash Transfer Management

**Safe Drop & Cash Transfer Management — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI POS · P04 Venue POS (terminal) |
| Module | Sell · wave 1 · needs the `core` module |
| Block | Block A · ticket #17889 (APP-POS-POS-018) |
| Who uses it | venue staff holding `CASH_LIFT`, `USER_MANAGE`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (1 operate, 2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. · LTR and RTL · light, dark theme |
| Pattern | listDetail (touchLarge density): `listPrincipals` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |
| Opens with | `workstationId` (session), `boxId` (deepLink), `shiftId` (deepLink) · cold entry: **Resolves from the session, which carries the workstation** — a till is signed into, not navigated to. |
| Route | `/sell/safe-drop-cash-transfer-management` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Owns POS board frame(s) POS-3B** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scope path | text field | optional | — | — | — | Sends `?scopePath=` to `listPrincipals`. | `listPrincipals` ?scopePath |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listPrincipals`. | `listPrincipals` ?isActive |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `listRotaAssignments` ?from |
| To | date picker | — | — | `listRotaAssignments` ?to |
| Principal | picker: choose a principal | — | — | `listRotaAssignments` ?principalId |
| Department | picker: choose a department | — | — | `listRotaAssignments` ?departmentId |

**Form: Withdraw from deposit box** (confirmDialog, opened by *Withdraw from deposit box*; *Withdraw* calls `withdrawFromDepositBox`, *Cancel* sends nothing)

**Names what `withdrawFromDepositBox` changes and what it leaves alone**, in the consequence rather than the verb. A safe drop cash this affects should be identified in the dialog, not just counted. **Collects what `withdrawFromDepositBox` sends before it is called.** Required: `id`, `amount`, `witnessPrincipalId`, `recordedAt`. Optional: `reason`, `note`.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the `CashMovement` this records. | `withdrawFromDepositBox` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `withdrawFromDepositBox` body |
| Witness principal `witnessPrincipalId` | picker: choose a witness principal | required | — | — | shows names, sends the id | The cashier the cash came from. Kept as `CashMovement.witnessPrincipalId`. | `withdrawFromDepositBox` body |
| Reason `reason` | radio group | optional | — | Banking · Safe drop · Change order · Other | — | Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records. | `withdrawFromDepositBox` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `withdrawFromDepositBox` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `withdrawFromDepositBox` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 The box is being counted or has been counted — `closing`, `closed` or `reconciled` (problem type `deposit-box-not-open`).

**Form: Create cash movement** (modal, opened by *Create cash movement*; *Create cash movement* calls `createCashMovement`, *Cancel* sends nothing)

**Collects what `createCashMovement` sends before it is called.** Required: `id`, `kind`, `amount`, `recordedAt`. Optional: `denominations`, `reference`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. | `createCashMovement` body |
| Kind `kind` | segmented control | required | — | Opening float · Lift · Add | — | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`. | `createCashMovement` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createCashMovement` body |
| Denominations `denominations` | repeatable rows | optional | — | at least 1 | — | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. | `createCashMovement` body |
| ID `denominations[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Shift `denominations[].shiftId` | picker: choose a shift | required | — | — | shows names, sends the id | A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are. | `createCashMovement` body |
| Deposit box `denominations[].depositBoxId` | picker: choose a deposit box | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Count kind `denominations[].countKind` | segmented control | optional | — | Opening float · Close · Movement | — | Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). | `createCashMovement` body |
| Cash movement `denominations[].cashMovementId` | picker: choose a cash movement | optional | — | — | shows names, sends the id | The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`. | `createCashMovement` body |
| Denomination `denominations[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` — face value, kind and sort order live there. | `createCashMovement` body |
| Counted quantity `denominations[].countedQuantity` | number field | required | — | min 0 | — | How many of this note or coin were in the drawer. | `createCashMovement` body |
| Counted value `denominations[].countedValue` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Quantity times face value, stored. Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count. | `createCashMovement` body |
| Counted by `denominations[].countedBy` | picker: choose a counted by | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Counted at `denominations[].countedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCashMovement` body |
| Recount of `denominations[].recountOf` | picker: choose a recount of | optional | — | — | shows names, sends the id | A recount points at what it replaces rather than overwriting it. `requestRecount` exists because a variance is a question before it is a fact. | `createCashMovement` body |
| Reference `reference` | text field | optional | — | max length 64 | — | Safe drop reference or bag number. | `createCashMovement` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `createCashMovement` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCashMovement` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since (`lift-exceeds-float`, audit R123 …

**Form: Create rota assignment** (modal, opened by *Create rota assignment*; *Create rota assignment* calls `createRotaAssignment`, *Cancel* sends nothing)

**Collects what `createRotaAssignment` sends before it is called.** Required: `principalId`, `venueId`, `position`, `startsAt`, `endsAt`. Optional: `overtimeMinutes`, `restPeriodBefore`, `breachesWorkingHourLimit`, `labourCost`, `id`, `displayName`, `departmentId`, `requiredRoleId`, `workstationId`, `status`, `breakMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rest period before `restPeriodBefore` | number field | optional | — | — | — | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and unsafe in all of them. | `createRotaAssignment` body |
| Labour cost `labourCost` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. | `createRotaAssignment` body |
| Principal `principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `createRotaAssignment` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createRotaAssignment` body |
| Department `departmentId` | picker: choose a department | optional | — | — | shows names, sends the id | — | `createRotaAssignment` body |
| Position `position` | text field | required | — | — | — | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota assignment is not a shift. | `createRotaAssignment` body |
| Required role `requiredRoleId` | picker: choose a required role | optional | — | — | shows names, sends the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. | `createRotaAssignment` body |
| Workstation `workstationId` | picker: choose a workstation | optional | — | — | shows names, sends the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. | `createRotaAssignment` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRotaAssignment` body |
| Ends at `endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRotaAssignment` body |
| Status `status` | select | optional | — | Planned · Published · Confirmed · Swap pending · Cancelled · Completed · No show | — | — | `createRotaAssignment` body |
| Break minutes `breakMinutes` | number field (minutes) | optional | — | — | — | — | `createRotaAssignment` body |
| Note `note` | text area | optional | — | — | — | — | `createRotaAssignment` body |

Errors to draw in the form: 409 Overlaps an existing assignment, or the person lacks the required role

#### Outputs: what the screen shows and produces

**Shown**

**Every principal** (data table, from `listPrincipals`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Username | text | — |
| Display name | text | — |
| Is active | yes / no (icon or chip) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Past this, resolution returns DENY regardless of grants. |
| Primary role | the name it points at, never the id | Determines the landing screen when the principal holds several roles and picks one at login. |
| Roles | list or chips (count when long) | — |
| Last login at | 1 Oct 2026, 14:30 | — |

**Every rota assignment** (data table, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Breaches working hour limit | yes / no (icon or chip) | Flagged at assignment, not discovered at payroll. A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Display name | text | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Position | text | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota … |
| Required role | the name it points at, never the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. |
| Workstation | the name it points at, never the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. |

**The selected principal** (detail panel, from `listPrincipals`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Username | text | — |
| Display name | text | — |
| Is active | yes / no (icon or chip) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Past this, resolution returns DENY regardless of grants. |
| Primary role | the name it points at, never the id | Determines the landing screen when the principal holds several roles and picks one at login. |
| Roles | list or chips (count when long) | — |
| Last login at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Create cash movement (primary button) | `createCashMovement` POST `/shifts/{shiftId}/cash-movements` | CreateCashMovementRequest | CashMovement | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since … | works offline; opens modal first |
| Withdraw from deposit box (destructive button) | `withdrawFromDepositBox` POST `/deposit-boxes/{boxId}/withdraw` | inline | DepositBox | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 The box is being counted or has been counted — `closing`, `closed` or `reconciled` (problem type `deposit-box-not-open`). | works offline; opens confirmDialog first |
| Create rota assignment (secondary button) | `createRotaAssignment` POST `/rota-assignments` | RotaAssignment | RotaAssignment | 409 Overlaps an existing assignment, or the person lacks the required role | opens modal first |

**Data it reads**: `listPrincipals` (onLoad, List principals); `listRotaAssignments` (onLoad, The rota)

**Where the user goes next**

- → `POS-001` Begin Shift: *Begin Shift*; carries `shiftId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The safe drop cash list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the safe drop cash untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No safe drop cash yet. Offers Create cash movement (`createCashMovement`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on scopePath, isActive and the safe drop cash are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Overlaps an existing assignment, or the person lacks the required role; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since (`lift-exceeds-float`, audit R123 …; 409 The box is being counted or has been counted — `closing`, `closed` or `reconciled` (problem type `deposit-box-not-open`). |

#### Permissions

- `createCashMovement` → `CASH_LIFT` (operate) · staff
- `withdrawFromDepositBox` → `CASH_LIFT` (operate) · staff
- `createRotaAssignment` → `WORKFORCE_MANAGE` (configure) · staff
- `listPrincipals` → `USER_MANAGE` (configure) · staff, partner
- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.8.8 | The system should allow the supervisor to withdraw some cash during the day from an cashier’s cash float and trace it in the system. | F&B & Guest Management | CONTRACTED | `withdrawFromDepositBox` |
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 1.2.37 | System shall integrate approved leave requests. | Ticketing Catalogue | CONTRACTED | data `RotaAssignment` |
| 1.2.38 | System shall manage overtime allocation and monitoring. | Ticketing Catalogue | CONTRACTED | data `RotaAssignment` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Configurable cash-drawer limit: on a busy day the cashier unloads excess cash mid-shift; the unloaded amount is held separately (partial hold) and reconciled at final close. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-274)*

Also apply: 5 for P04 · Sell, 41 for all of P04, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P04 Venue POS.dc.html#pos-018` · status **notStarted** · provenance designed · **Drawn by Claude Design on `POS Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Prototype (TICVAI OS 4.2.1, build 2026.08.14, verified —, match none): `sources/designs/TICVAI_POS_Terminal_client_approved.html`, view **
- Derived from `wireframes/reference/POS Board 3.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 3.dc.html#pos-3b`
- Flow F73 *A till is configured and its cash rules set*, step 4: Safe drop destinations are allocated. → **A box per till per shift.** Two tills sharing a box is two cashiers answering for one variance.

#### Acceptance for the design

- [ ] Every input above is drawn (39), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#POS-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create cash movement, Withdraw from deposit box, Create rota assignment.
- [ ] Every transition is wired: `POS-001`.
- [ ] Every gated control is gated: `CASH_LIFT`, `USER_MANAGE`, `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `POS-019` Shift Templates & Policies

**Shift Templates & Policies — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI POS · P04 Venue POS (terminal) |
| Module | Sell · wave 1 · needs the `core` module |
| Block | Block A · ticket #17915 (APP-POS-POS-019) |
| Who uses it | venue staff holding `REPORT_VIEW_WORKSTATION`, `TENANT_CONFIGURE`, `TENANT_VIEW` (1 operate, 1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. · LTR and RTL · light, dark theme |
| Pattern | listDetail (touchLarge density): `listShifts` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |
| Opens with | `workstationId` (session), `venueId` (deepLink) · cold entry: **Resolves from the session, which carries the workstation** — a till is signed into, not navigated to. |
| Route | `/sell/shift-templates-policies` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it.** **Owns POS board frame(s) POS-3C** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listShifts`. | `listShifts` ?workstationId |
| Status | select | optional | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | — | Sends `?status=` to `listShifts`. | `listShifts` ?status |
| Opened from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedFrom=` to `listShifts`. | `listShifts` ?openedFrom |
| Opened to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedTo=` to `listShifts`. | `listShifts` ?openedTo |

**Form: Save venue settings** (modal, opened by *Save venue settings*; *Save venue settings* calls `setVenueSettings`, *Cancel* sends nothing)

**Collects what `setVenueSettings` sends before it is called.** Nothing in the body is required. Optional: `id`, `venueId`, `currencyCode`, `currencyScale`, `supportHours`, `quietHours`, `biometrics`, `segregatedAccess`, `alerting`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Calendar day start hour `calendarDayStartHour` | stepper or slider | optional | 6 | min 0; max 23 | — | Where the venue's calendar day starts (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in … | `setVenueSettings` body |
| Support hours `supportHours` | group | optional | — | — | — | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. | `setVenueSettings` body |
| Mode `supportHours.mode` | radio group | optional | — | Always on · Business hours · Custom · None | — | — | `setVenueSettings` body |
| Timezone `supportHours.timezone` | text field | optional | — | — | — | IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract. | `setVenueSettings` body |
| Windows `supportHours.windows` | repeatable rows | optional | — | — | — | — | `setVenueSettings` body |
| Day `supportHours.windows[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettings` body |
| From `supportHours.windows[].from` | text field | optional | — | — | — | Wall-clock time the desk opens. | `setVenueSettings` body |
| To `supportHours.windows[].to` | text field | optional | — | — | — | Wall-clock time the desk closes. | `setVenueSettings` body |
| Out of hours message `supportHours.outOfHoursMessage` | text field | optional | — | — | — | — | `setVenueSettings` body |
| Quiet hours `quietHours` | group | optional | — | — | — | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. | `setVenueSettings` body |
| From `quietHours.from` | text field | optional | — | — | — | Wall-clock time sending stops | `setVenueSettings` body |
| To `quietHours.to` | text field | optional | — | — | — | Wall-clock time sending resumes | `setVenueSettings` body |
| Biometrics `biometrics` | group | optional | — | — | — | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. | `setVenueSettings` body |
| Is enabled `biometrics.isEnabled` | toggle | optional | off | Off by default, and turning it on is refused without the two fields below. | — | Off by default, and turning it on is refused without the two fields below. `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — a DPIA nobody can … | `setVenueSettings` body |
| Dpia reference `biometrics.dpiaReference` | text field | optional | — | max length 200 | — | The venue's own reference for its Article 21 assessment. The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is … | `setVenueSettings` body |
| Consent notice acknowledged at `biometrics.consentNoticeAcknowledgedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When somebody confirmed the consent forms are in place at the point of capture. A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice … | `setVenueSettings` body |
| Face tag purge minutes after close `biometrics.faceTagPurgeMinutesAfterClose` | number field (minutes) | optional | 0 | — | — | BL-106. How long a same-visit Face Tag survives past the close of the operating day, and zero is the default because that is what 3.2.44 describes. | `setVenueSettings` body |
| Segregated access `segregatedAccess` | group | optional | — | — | — | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a prayer-time closure. | `setVenueSettings` body |
| Is enabled `segregatedAccess.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettings` body |
| Applies to access points `segregatedAccess.appliesToAccessPointIds` | multi-picker: choose applies to access points | optional | — | — | — | — | `setVenueSettings` body |
| Schedule `segregatedAccess.schedule` | repeatable rows | optional | — | — | — | — | `setVenueSettings` body |
| Day `segregatedAccess.schedule[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettings` body |
| From `segregatedAccess.schedule[].from` | text field | optional | — | — | — | Wall-clock time | `setVenueSettings` body |
| To `segregatedAccess.schedule[].to` | text field | optional | — | — | — | Wall-clock time | `setVenueSettings` body |
| Admits `segregatedAccess.schedule[].admits` | radio group | optional | — | All · Women · Women and children · Families · Members | — | — | `setVenueSettings` body |
| Gender verification `segregatedAccess.genderVerification` | segmented control | optional | Off | Off · Staff assisted · Device assisted; Available only where the driver reports the capability, and the result is advisory to the steward rather than decisive at the turnstile (3. | — | `off` — the entitlement decides and a steward handles exceptions. The default, and what is contracted. | `setVenueSettings` body |
| Override rate alert threshold `segregatedAccess.overrideRateAlertThreshold` | number field | optional | — | — | — | Where `deviceAssisted` is on. An override rate near zero means the steward has stopped deciding, and that is the number that says whether the human safeguard is working or … | `setVenueSettings` body |
| Alerting `alerting` | group | optional | — | The panel is the default and email or WhatsApp only where the matrix names them — an operational alert that arrives by email is an alert nobody sees in time. | — | CF-134. On-platform notification, marked as read. | `setVenueSettings` body |
| Channel `alerting.channel` | segmented control | optional | Dashboard panel | Dashboard panel · Dashboard and email · Dashboard and whatsapp | — | — | `setVenueSettings` body |
| Acknowledgement required `alerting.acknowledgementRequired` | toggle | optional | on | — | — | — | `setVenueSettings` body |
| Escalate after minutes `alerting.escalateAfterMinutes` | number field (minutes) | optional | — | — | — | — | `setVenueSettings` body |
| Display currencies `displayCurrencies` | list of values (chips) | optional | — | A code the region has no rate for is refused `400`. | — | Which currencies this venue shows guests (decided 28 September, audit R120 (a)). | `setVenueSettings` body |
| Cart lease seconds `cartLeaseSeconds` | number field (seconds) | optional | 900 | min 30; max 3600 | — | How long a cart holds capacity (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. | `setVenueSettings` body |
| Cart hold extension minutes `cartHoldExtensionMinutes` | stepper or slider (minutes) | optional | 5 | min 1; max 30 | — | How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094). | `setVenueSettings` body |
| Cart max extensions `cartMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). | `setVenueSettings` body |
| Resale cutoff hours `resaleCutoffHours` | number field (hours) | optional | 24 | min 0; max 168 | — | Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). | `setVenueSettings` body |
| Exchange cutoff hours `exchangeCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). | `setVenueSettings` body |
| Reschedule cutoff hours `rescheduleCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). | `setVenueSettings` body |
| Reservation max extensions `reservationMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094). | `setVenueSettings` body |
| Shift variance threshold `shiftVarianceThreshold` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. | `setVenueSettings` body |
| Catalogue `catalogue` | group | optional | — | — | — | — | `setVenueSettings` body |
| Max variants per product `catalogue.maxVariantsPerProduct` | number field | optional | 200 | min 1; max 2000 | — | Variants one product may generate from its attributes (`setProductAttributes` refuses above it). | `setVenueSettings` body |
| Waitlist offer hold minutes `catalogue.waitlistOfferHoldMinutes` | number field (minutes) | optional | 30 | min 1; max 1440 | — | How long a waitlist offer holds the released capacity for the guest it was offered to. | `setVenueSettings` body |
| Bulk price change escalation percent `catalogue.bulkPriceChangeEscalationPercent` | stepper or slider | optional | 10 | min 0; max 100; A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). | — | A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). | `setVenueSettings` body |
| Bulk price change escalation count `catalogue.bulkPriceChangeEscalationCount` | number field | optional | 50 | min 1; A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). | — | A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). | `setVenueSettings` body |
| … 27 more | | | | | | the rest are in `schemas.json` | `setVenueSettings` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 An enable the venue cannot evidence. Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender …

#### Outputs: what the screen shows and produces

**Shown**

**Every shift** (data table, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |

**The selected shift** (detail panel, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sales total | AED 1,234.50 | What the till took in sales, as the guest paid it — tax included. |
| Refunds total | AED 1,234.50 | What the till paid back, as the guest was refunded it — tax included. |
| Lifts total | AED 1,234.50 | Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net. |

**The venue settings** (detail panel, from `getVenueSettings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | From the path of `setVenueSettings`. |
| Currency code | text | `readOnly` is the freeze. `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the … |
| Currency scale | 1,234 | Scale travels with currency (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency … |
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| Biometrics | grouped details | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. |
| Segregated access | grouped details | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a … |
| Alerting | grouped details | CF-134. On-platform notification, marked as read. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Save venue settings (primary button) | `setVenueSettings` PUT `/venues/{venueId}/settings` | VenueSettings | VenueSettings | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Data it reads**: `listShifts` (onLoad, List shifts); `getVenueSettings` (onLoad, Operational settings for this venue)

**Where the user goes next**

- → `POS-001` Begin Shift: *Begin Shift*; carries `shiftId`
- → `POS-015` Cash Operations Dashboard: *Cash limits and the drawer ceiling are set*; carries `shiftId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shift templates policies list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shift templates policies untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No shift templates policies yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, status, openedFrom, openedTo and the shift templates policies are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 An enable the venue cannot evidence. Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender … |

#### Permissions

- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `setVenueSettings` → `TENANT_CONFIGURE` (configure) · staff
- `getVenueSettings` → `TENANT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.44 | Incident & Exception Logging | Ticketing Sales | CONTRACTED | data `Shift` |
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| 3.2.46 | Face Pass shouldt restrict male guests attempting to enter during Friday Ladies Night, which needs to be validated with rule-based facial recognition validation. | Admission and Access | CONTRACTED | data `VenueSettings` |
| 8.9.3 | System shall display queue lengths, estimated wait times, queue utilization, queue alerts, and queue prediction metrics. | Unified Operations Dashboard | CONTRACTED | data `VenueSettings` |
| 11.1.15 | Approval Breach Alerts - System shall notify users when approval SLA thresholds are exceeded. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.17 | Approval Notifications - System shall notify approvers when new approval requests are assigned. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.18 | Approval Reminder Notifications - System shall send reminder notifications for pending approvals. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.19 | Approval Outcome Notifications - System shall notify requestors when approvals are approved, rejected or escalated. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 15.1.32 | Overstock Alerts - System shall generate overstock alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.33 | Stock Shortage Alerts - System shall generate stock shortage alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.34 | Expiry Alerts - System shall generate expiry alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 16.4.23 | Device Alerts - System shall generate device alerts. | Device Management | CONTRACTED | data `VenueSettings` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Shift management: assignment and scheduling by cashier/department, templates and policies, opening/closing, exceptions/alerts. Allam: explore merging shift-closing and till-closing screens to reduce dashboard count. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-309)*

Also apply: 5 for P04 · Sell, 41 for all of P04, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P04 Venue POS.dc.html#pos-019` · status **notStarted** · provenance designed · **Drawn by Claude Design on `POS Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Prototype (TICVAI OS 4.2.1, build 2026.08.14, verified —, match none): `sources/designs/TICVAI_POS_Terminal_client_approved.html`, view **
- Derived from `wireframes/reference/POS Board 3.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 3.dc.html#pos-3c`
- Flow F73 *A till is configured and its cash rules set*, step 2: Shift policy is set. → **Venue scope, not workstation.** Every till in a venue closes to the same rules or the variance report compares nothing.
- Flow F73 branch at step 2 (high): when A shift is open on the till., **Refused.** Changing the rules under an open shift means it closes against rules it did not open under.

#### Acceptance for the design

- [ ] Every input above is drawn (76), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (37 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#POS-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Save venue settings.
- [ ] Every transition is wired: `POS-001`, `POS-015`.
- [ ] Every gated control is gated: `REPORT_VIEW_WORKSTATION`, `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `POS-024` Outlet Setup

**A manager configures this outlet from the floor.**

| | |
|---|---|
| App · platform | TICVAI POS · P04 Venue POS (terminal) |
| Module | Sell · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #17952 (APP-POS-POS-024) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW` (1 configure, 2 read) |
| Device and orientation | This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. · LTR and RTL · light, dark theme |
| Pattern | listDetail (touchLarge density): `listOutlets` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Configuration is refused offline.** A table layout edited on two disconnected tablets is two layouts, and the room only has one. |
| Opens with | `workstationId` (session), `outletId` (session), `itemId` (deepLink) · cold entry: **Resolves from the session, which carries the workstation and its outlet.** A till is signed into, not navigated to — and the outlet is a property of where … |
| Route | `/sell/outlet-setup` |

**What the spec says about it.** **Configuration on the till, gated by permission rather than by device.** P04 is *Terminal and Tablet* (`reactNativeTablet`) and ADR-0002 makes authorisation user-driven — **a manager signs into the same till a cashier uses and sees screens the cashier does not.** **A table layout is decided standing in the room.** A manager at a desk cannot see whether two four-tops push together, which is why `setTableLayout` and `setTableCombinations` belong within reach of the floor and not only in the back office.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listOutlets`. | `listOutlets` ?venueId |
| Kind | select | optional | — | Shop · Restaurant · Bar · Cafe · Kiosk · Game floor · Ticket office · Mobile | — | Sends `?kind=` to `listOutlets`. | `listOutlets` ?kind |
| 86 an item | multi select | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet | picker: choose an outlet | — | — | `listMenus` ?outletId |
| Active at | date and time picker | — | — | `listMenus` ?activeAt |

**Form: Save table layout** (modal, opened by *Save table layout*; *Save table layout* calls `setTableLayout`, *Cancel* sends nothing)

**Collects what `setTableLayout` sends before it is called.** Required: `tables`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tables `tables` | repeatable rows | required | — | — | — | — | `setTableLayout` body |
| ID `tables[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setTableLayout` body |
| Label `tables[].label` | text field | required | — | max length 32 | — | The table code, unique per venue (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is … | `setTableLayout` body |
| Capacity `tables[].capacity` | number field | required | — | min 1 | — | — | `setTableLayout` body |
| Zone `tables[].zone` | text field | optional | — | — | — | — | `setTableLayout` body |
| Position `tables[].position` | group | optional | — | — | — | — | `setTableLayout` body |
| X `tables[].position.x` | number field | optional | — | — | — | — | `setTableLayout` body |
| Y `tables[].position.y` | number field | optional | — | — | — | — | `setTableLayout` body |
| Shape `tables[].shape` | radio group | optional | — | Round · Square · Rectangle · Booth · Bar | — | — | `setTableLayout` body |
| Is out of service `tables[].isOutOfService` | toggle | optional | off | `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`. | — | Damaged, or its section closed. `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`. | `setTableLayout` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Save table combinations** (modal, opened by *Save table combinations*; *Save table combinations* calls `setTableCombinations`, *Cancel* sends nothing)

**Collects what `setTableCombinations` sends before it is called.** Required: `combinations`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Combinations `combinations` | repeatable rows | required | — | — | — | — | `setTableCombinations` body |
| Tables `combinations[].tableIds` | multi-picker: choose tables | required | — | at least 2 | — | — | `setTableCombinations` body |
| Combined covers `combinations[].combinedCovers` | number field | required | — | min 1 | — | — | `setTableCombinations` body |
| Setup minutes `combinations[].setupMinutes` | number field (minutes) | optional | 5 | — | — | — | `setTableCombinations` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Save item availability** (modal, opened by *Save item availability*; *Save item availability* calls `setItemAvailability`, *Cancel* sends nothing)

**Collects what `setItemAvailability` sends before it is called.** Required: `isAvailable`, `recordedAt`. Optional: `reason`, `restoreAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Is available `isAvailable` | toggle | required | — | — | — | — | `setItemAvailability` body |
| Reason `reason` | radio group | optional | — | Sold out · Ingredient unavailable · Equipment down · Seasonal · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `setItemAvailability` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `setItemAvailability` body |
| Restore at `restoreAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Automatic restore, typically at next service. Kept as `MenuItem.restoreAt`. | `setItemAvailability` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `setItemAvailability` body |

Errors to draw in the form: 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

#### Outputs: what the screen shows and produces

**Shown**

**Every outlet** (data table, from `listOutlets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Shop, Restaurant, Bar, Cafe, Kiosk, Game floor… | — |
| Zone | text | — |
| Stock location | the name it points at, never the id | Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not. |
| Cost center | the name it points at, never the id | Revenue and cost attribution. Outlet is the natural grain for both. |
| Opening hours | list or chips (count when long) | The weekly pattern, one entry per window. Several windows on a day are allowed. |
| Is active | yes / no (icon or chip) | — |

**Every menu** (data table, from `listMenus`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Availability | grouped details | When this menu is in force. Absent means always. |
| Sections | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |
| Published version | 1,234 | The `MenuVersion.version` live now. Null for a menu never published. |
| Published at | 1 Oct 2026, 14:30 | — |

**Floor** (card list)

**Combinations** (detail panel): **Declared, not inferred.** Two adjacent tables do not always combine — a pillar, a step, a service run. A host knows which pairs work and a floor plan does not.

**The selected outlet** (detail panel, from `listOutlets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Shop, Restaurant, Bar, Cafe, Kiosk, Game floor… | — |
| Zone | text | — |
| Stock location | the name it points at, never the id | Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not. |
| Cost center | the name it points at, never the id | Revenue and cost attribution. Outlet is the natural grain for both. |
| Opening hours | list or chips (count when long) | The weekly pattern, one entry per window. Several windows on a day are allowed. |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Apply (primary button) | navigation or local | — | — | — | — |
| Save table layout (primary button) | `setTableLayout` PUT `/outlets/{outletId}/tables` | inline | TableMap | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Save table combinations (secondary button) | `setTableCombinations` PUT `/outlets/{outletId}/table-combinations` | inline | inline | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Save item availability (secondary button) | `setItemAvailability` PUT `/menu-items/{itemId}/availability` | inline | MenuItem | 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | works offline; opens modal first |

**Data it reads**: `listOutlets` (onLoad, List outlets); `listMenus` (onLoad, List menus)

**Where the user goes next**

- → `POS-002` Sell — Ticket Catalogue: *Sell — Ticket Catalogue*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | This outlet, its tables and its menu. |
| Error (`?state=error`) | Could not load configuration. **Selling is unaffected.** |
| Empty, first run (`?state=emptyFirstRun`) | **A new outlet with no layout.** The one action that draws the first table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches. |
| Permission denied (`?state=emptyNoAccess`) | **You are signed in as a cashier.** Configuration needs a manager role — ADR-0002 makes that the person, not the device, so signing in again on this same till is the way through. |
| Offline (`?state=offline`) | **Configuration is refused offline.** A table layout edited on two disconnected tablets is two layouts, and the room only has one. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listOutlets` → `SCOPE_VIEW` (read) · staff
- `setTableLayout` → `PRODUCT_CONFIGURE` (configure) · staff
- `setTableCombinations` → `PRODUCT_CONFIGURE` (configure) · staff
- `setItemAvailability` → `PRODUCT_CONFIGURE` (configure) · staff
- `listMenus` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** **You are signed in as a cashier.** Configuration needs a manager role — ADR-0002 makes that the person, not the device, so signing in again on this same till is the way through.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.9.6 | The system should be able to create, modify, delete a restaurant floor plan. | Bundles and Promotions | CONTRACTED | `setTableLayout` |
| 4.6.9 | The system should be able to allow the back office to limit the sale of a particular item per day or per timeslot.(example: Happy hour time slot based sales). | Bundles and Promotions | CONTRACTED | `setItemAvailability` |
| 2.1.32 | System shall allow guests to purchase food and beverage items through self-service kiosks. The kiosk shall support menu browsing, product customization, combo meals, upsell recommendations … | Ticketing Sales | CONTRACTED | data `Menu` |
| 2.1.33 | System shall allow guests to purchase retail merchandise through self-service kiosks. The kiosk shall support product browsing, inventory validation, variant selection (size, color, style) … | Ticketing Sales | CONTRACTED | data `Menu` |
| 4.6.13 | The system should have a interface for kiosks where the guest should be able to place order via the self service option all the way till completing payments. | Bundles and Promotions | CONTRACTED | data `Menu` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P04 · Sell, 41 for all of P04, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P04 Venue POS.dc.html#pos-024` · status **notStarted** · provenance designed
- Prototype (TICVAI OS 4.2.1, build 2026.08.14, verified —, match none): `sources/designs/TICVAI_POS_Terminal_client_approved.html`, view **
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state (400, 403, 412).
- [ ] Every output is drawn (29 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#POS-024?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Apply, Save table layout, Save table combinations, Save item availability.
- [ ] Every transition is wired: `POS-002`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P04 reference designs** (from `handoff/design-batches/apps/2-pos/README.md`)

- `sources/designs/TICVAI_POS_Terminal_v2.html`: **the POS reference from 1 October.** Our improved build of the client-approved terminal (`TICVAI POS Terminal (3).html`). It is a **candidate, not client-approved**: the 14 screens captured from it are `designed`, in `review`, with a `wireframe.candidate` block, never client-verified (tools/applied/pos-v2-1-october.py). The file is 9.7 MB and **kept out of git**: it is on Chinmay's disk at that path, and the captures in `wireframes/incoming/P04-pos-v2/` are the record.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the build the client signed off (10 September). It stays as it is; each screen's `wireframe.prototype` block still cites its view. When the client approves v2, v2 takes its place.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-035, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P04 as a whole** (21: 0 open, 21 closed). Open first; a closed row says where it went on 30 September.

- **A17** Design the offline POS and handheld-validation architecture *(Softlabs Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A19** Prepare case study: online-first vs offline-first POS architecture (pros/cons) *(Chinmay Parab · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A23** Review and preserve the POS prototype for UI/UX reference *(Softlabs Team · Low · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A24** Propose an enhanced POS user experience (redesign, not a copy) *(Softlabs Team · High · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A26** Recommend a UX approach combining quick-access 'hot function' buttons with search-driven POS functionality *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · 9 Sep 2026 · workshop tracker)*
- **A37** Complete and share mockups for the food ordering / POS counter app *(Aishwarya More · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A51** Design ticket + F&B combo redemption flow: single QR encodes admission + meal entitlement, redeemable once at the F&B counter after entry; support both a shared group QR (redeemed together) and individually … *(Softlabs Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker)*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker)*
- **A79** Complete outstanding finance/infrastructure due diligence: review the ticketing system's manuals for additional revenue-recognition rules, finalize chart-of-accounts/ERP mapping due diligence, confirm the … *(Chinmay Parab / Qossai / Allam · Medium · Ongoing → 30 Sep: Closed, Rolled into S7 (HLD/LLD) · 12 Aug 2026 · workshop tracker)*
- **A83** Design the Menu & Product Command Center and Menu Builder (recipe/product mapping alerts, drag-and-drop POS layout, chargeable/free modifiers with min/max rules, combo meals with upgrade options) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker)*
- **A173** Expose wallet APIs for both patterns (external systems consuming the API directly, and third-party F&B/retail POS such as Micros or Symphony verifying and deducting balance) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker)*
- **A267** Revise POS prototype with 09-Sep feedback and share *(Pradnya Yeram · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Sep 2026 · workshop tracker)*
- … 7 more in `handoff/design-inputs/task-tracker-index.json`

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

### Across P04 Venue POS

- No driver is ever installed on the workstation OS: drivers are built into the TICVAI app; staff only connect the device and test print/scan from within the app; new models are supported by a back-end driver update, not a code release. *(agreed · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-897)*
- Qossai: dim/fade the background ("foggy") when a side panel or modal opens so the cashier's attention stays on the active task. *(client request · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-785)*
- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*
- Funding approval rules: a top-up above a configured threshold requires supervisor or finance approval via supervisor login. Top-up reversal (full or partial, back to the original payment method) requires manual verification/authorisation before processing. *(agreed · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-520)*
- Top-up rules set minimum and maximum amounts per transaction; channel/funding-source mapping restricts which payment methods each channel offers (e.g. cash top-up on-site only, not online), so each channel's top-up screen offers only its allowed methods. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-517)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*
- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Each device gets a unique workstation ID, but what a user sees is set by their role, not the device: e.g. a cashier sees the full park ticket range at a main-gate POS but only the F&B menu at a restaurant POS. Applies to the roaming "flying" POS too. *(agreed · MoM 12 Aug 2026, 2. Flying POS Setup and Permission Configuration · DI-246)*
- Built-in help menu with step-by-step tutorials with screenshots for common tasks (e.g. how to sell a ticket at the POS). *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-160)*
- In-system task assignment between staff (e.g. a cashier flagging something for a supervisor) without email or messaging apps. *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-159)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- F&B is reached from the same top-level navigation as other experiences (tours, guides); table management only appears for venues with a restaurant configuration. *(client request · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-107)*
- Allam: the cashier design must work consistently across all cashier device types: POS terminals, tablets, iPads and kiosks. *(agreed · MoM 3 Aug 2026, 3. UX Design Approach Discussion · DI-101)*
- Prefer the demoed cleaner, better-spaced layout over the cluttered PDF: adequate spacing and large touch targets to prevent mis-taps on touchscreens and tablets. *(agreed · MoM 3 Aug 2026, 3. UX Design Approach Discussion · DI-100)*
- Shift-level settings: light/dark mode, currency selection (displayed pricing follows the cashier's location), language selection, screen brightness, and manual online/offline toggling. *(agreed · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-098)*
- Notification system with ticket alerts (cancellations, capacity nearing or at its limit) and system alerts (printer offline, POS offline). *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-093)*
- Embedded AI assistant the cashier can query directly, e.g. to find today's promo code, process a refund, or switch between light/night themes. *(agreed · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-092)*
- Header metrics show tickets sold and revenue for the current shift. *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-090)*
- **Open question.** Allam: alongside search, provide always-visible "hot function" buttons for high-frequency actions (refund, check transaction, print last receipt). Softlabs to recommend the right balance of hot buttons and search. *(open · MoM 3 Aug 2026, 3. UX Design Approach Discussion · DI-088)*
- A prominent search ("magic banner") lets the cashier reach functionality such as refunds or resending a ticket by searching, rather than through static menus or sidebars. *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-087)*
- Qossai's demoed cashier interface is the primary reference/baseline, to be enhanced and redesigned enough that it does not look like a copy while keeping its UX ideas; the earlier AI-generated PDF is secondary colour/theme inspiration only. *(agreed · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-086)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- POS product names and menus may be Arabic-only for certain regions. *(client request · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-082)*
- Selling a capacity-based product (e.g. seat-assigned tickets) while offline is blocked with a clear notification, never allowed through or silently failing; non-capacity products stay sellable offline. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-074)*
- Qossai: the POS raises an alert when a venue goes offline. *(client request · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-073)*
- Offline state must be clearly visible in the UI, e.g. a visible mode indicator or greyed-out unavailable functions; exact visual treatment to be settled in the UI/UX session. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-072)*
- Allam: the app detects loss of connectivity and switches to offline mode automatically, without cashier action, then restores online mode and syncs pending transactions automatically. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-071)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*
- Allam: the platform is device-agnostic (Android, iOS and web) so sales can continue on any available device. *(agreed · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-068)*
- **Open question.** Qossai asked whether a cashier on a tablet could use the POS via a browser URL. A lightweight web POS will be considered; it would have no offline support (installed thick client required for offline). *(open · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-067)*
- **Open question.** POS catalogue: Chinmay's middle ground is an online real-time catalogue that falls back automatically to the last-synced catalogue if connectivity is lost; local-first vs online-first still to be compared (case study). *(open · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-066)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- POS: sell tickets, memberships, F&B, retail and services from one unified cashier experience. Access Control: real-time entry validation, occupancy monitoring, offline mode and gate management. *(agreed · Design Vision Book 29 Jul 2026, 07 Modules Overview (p7) - 04 Point of Sale; 03 Access Control · DI-035)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- POS must keep selling general admission tickets during an internet outage, and access-control apps must keep scanning and validating tickets during a connectivity failure. *(agreed · MoM 28 Jul 2026, 15. Offline POS and Access-Control Operations · DI-012)*

### In P04 · Sell

- A guest is not repeatedly re-offered something already declined (e.g. a fast pass rejected three times), and an offer ignored online is not re-presented on another channel, e.g. at POS after the guest bought it there. *(agreed · MoM 21 Sep 2026, 4.6 Personalized Offer Delivery & Omni-Channel Orchestration · DI-962)*
- Navigation depends on ticket type: admission has no date/time and goes straight to quantity/cart; dated asks date only; timed asks date then time; seated asks date, then time, then seat. *(agreed · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-116)*
- Add-to-cart offers upsell add-ons, including an AI-generated upsell prompt (e.g. suggesting the cashier add two more items to unlock a bundle discount). *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-096)*
- A "Build Your Experience" workflow helps cashiers sell bundled experiences without searching through hundreds of ticket types. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-010)*
- POS allows notes to be added against individual tickets in the cart. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-005)*

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acceptShiftVariance": {"method":"POST","path":"/shifts/{shiftId}/accept-variance","contract":"shift","summary":"Accept an over/short beyond the threshold","permission":"OVERSHORT_ACCEPT","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"appendEntitlementToMedia": {"method":"POST","path":"/media/{mediaCode}/entitlements","contract":"orders","summary":"Add something to a ticket the guest already holds","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AppendEntitlementRequest","responds":"AppendEntitlementResult"},
"approveShiftOpen": {"method":"POST","path":"/shifts/{shiftId}/approve-open","contract":"shift","summary":"Approve a shift opening outside tolerance","permission":"SHIFT_APPROVE_OPEN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"closeShift": {"method":"POST","path":"/shifts/{shiftId}/close","contract":"shift","summary":"Blind close-out","permission":"SHIFT_CLOSE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CloseShiftRequest","responds":"ShiftCloseResult"},
"createCashMovement": {"method":"POST","path":"/shifts/{shiftId}/cash-movements","contract":"shift","summary":"Record a cash lift or add","permission":"CASH_LIFT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCashMovementRequest","responds":"CashMovement"},
"createRotaAssignment": {"method":"POST","path":"/rota-assignments","contract":"workforce","summary":"Put someone on the rota","permission":"WORKFORCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RotaAssignment","responds":"RotaAssignment"},
"exchangeOrderLines": {"method":"POST","path":"/orders/{orderId}/exchanges","contract":"orders","summary":"Exchange lines for different products or dates","permission":"ORDER_EXCHANGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ExchangeOrderRequest","responds":"OrderExchangeResult"},
"getCart": {"method":"GET","path":"/carts/{cartId}","contract":"orders","summary":"The cart, priced and checked, right now","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Cart"},
"getCurrentShift": {"method":"GET","path":"/shifts/current","contract":"shift","summary":"The open or suspended shift on the session's workstation","permission":"SHIFT_OPEN","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Shift"},
"getMediaAsset": {"method":"GET","path":"/media/{mediaId}","contract":"assets","summary":"Read an asset with derivatives and usage","permission":"ASSET_LIBRARY_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaAssetDetail"},
"getMediaEntitlements": {"method":"GET","path":"/media/{mediaCode}/entitlements","contract":"orders","summary":"What is already on this media","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaEntitlements"},
"getShift": {"method":"GET","path":"/shifts/{shiftId}","contract":"shift","summary":"Read a shift","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Shift"},
"getVenueSettings": {"method":"GET","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Operational settings for this venue","permission":"TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"listAlerts": {"method":"GET","path":"/alerts","contract":"reporting","summary":"What is currently wrong","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"itemId","in":"query","required":null}],"requestBody":null,"responds":"Alert"},
"listCashMovements": {"method":"GET","path":"/shifts/{shiftId}/cash-movements","contract":"shift","summary":"Lifts, adds and the opening float","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDepositBoxes": {"method":"GET","path":"/deposit-boxes","contract":"shift","summary":"Cash boxes and who holds them","permission":"SHIFT_OPEN","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"openOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMenus": {"method":"GET","path":"/menus","contract":"fnb","summary":"List menus","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOutlets": {"method":"GET","path":"/outlets","contract":"tenancy","summary":"List outlets","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"Outlet"},
"listPrincipals": {"method":"GET","path":"/principals","contract":"identity","summary":"List principals","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopePath","in":"query","required":null},{"name":"isActive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRotaAssignments": {"method":"GET","path":"/rota-assignments","contract":"workforce","summary":"The rota","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"departmentId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listShifts": {"method":"GET","path":"/shifts","contract":"shift","summary":"List shifts","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"openedFrom","in":"query","required":null},{"name":"openedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkstations": {"method":"GET","path":"/workstations","contract":"tenancy","summary":"List workstations","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"saleBoardKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"openShift": {"method":"POST","path":"/shifts","contract":"shift","summary":"Open a shift","permission":"SHIFT_OPEN","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OpenShiftRequest","responds":"Shift"},
"recordAttendance": {"method":"POST","path":"/attendance/clock","contract":"workforce","summary":"Clock in, clock out, or take a break","permission":"ATTENDANCE_RECORD","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"recordNoSale": {"method":"POST","path":"/shifts/{shiftId}/no-sale","contract":"shift","summary":"Open the Deposit Box without a sale","permission":"CASH_NO_SALE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NoSaleEvent"},
"reopenShift": {"method":"POST","path":"/shifts/{shiftId}/reopen","contract":"shift","summary":"Reopen a shift closed in error","permission":"SHIFT_REOPEN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"resumeShift": {"method":"POST","path":"/shifts/{shiftId}/resume","contract":"shift","summary":"Resume a suspended shift","permission":"SHIFT_OPEN","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"setItemAvailability": {"method":"PUT","path":"/menu-items/{itemId}/availability","contract":"fnb","summary":"Mark an item available or eighty-sixed","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuItem"},
"setTableCombinations": {"method":"PUT","path":"/outlets/{outletId}/table-combinations","contract":"fnb","summary":"Which tables can be pushed together, and to what capacity","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setTableLayout": {"method":"PUT","path":"/outlets/{outletId}/tables","contract":"fnb","summary":"Configure the table layout","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableMap"},
"setVenueSettings": {"method":"PUT","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Set support hours, quiet hours, segregated access and alerting","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VenueSettings","responds":"VenueSettings"},
"suspendShift": {"method":"POST","path":"/shifts/{shiftId}/suspend","contract":"shift","summary":"Suspend a shift so another user can log in","permission":"SHIFT_SUSPEND","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"withdrawFromDepositBox": {"method":"POST","path":"/deposit-boxes/{boxId}/withdraw","contract":"shift","summary":"A supervisor takes cash out mid-shift","permission":"CASH_LIFT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DepositBox"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Alert": {"type":"object","x-ticvai-persistence":"reporting.alert","description":"A raised alert. **Acknowledged rather than dismissed** — CF-134 asked for it markable, and the difference is that an acknowledgement records who saw it.\n","required":["id","ruleId","raisedAt","severity","status"],"properties":{"id":{"type":"string","format":"uuid"},"ruleId":{"type":"string","format":"uuid"},"ruleName":{"type":"string","description":"`AlertRule.name` as it stood when the alert was raised. **The line a person reads** — a list of rule ids is not an alert panel, and a screen should not need `listAlertRules` to label one.\n"},"metric":{"allOf":[{"$ref":"#/components/schemas/MetricSource"}],"description":"The rule's metric, carried so the alert says what went out of range."},"raisedAt":{"type":"string","format":"date-time"},"severity":{"$ref":"#/components/schemas/AlertSeverity"},"status":{"$ref":"#/components/schemas/AlertStatus"},"observedValue":{"$ref":"#/components/schemas/MetricValue"},"threshold":{"$ref":"#/components/schemas/MetricValue"},"scopePath":{"type":"string"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation the reading was taken for, where the metric is measured per workstation (`salesByWorkstation`). Null otherwise. `listAlerts` filters on it."},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The till shift (`orders.pos_shift`) the reading belongs to, where it was taken for a workstation with a shift open. Null otherwise. `listAlerts` filters on it."},"itemId":{"type":"string","format":"uuid","nullable":true,"description":"The inventory item the reading is about, where the metric is measured per item (`stockAgeing`, `stockTurnover`, `wastageRate`, `inventoryValuation`). Null otherwise. **What a replenishment screen prefills a requisition from.**\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true},"acknowledgementNote":{"type":"string","maxLength":300,"nullable":true,"description":"The `note` given to `acknowledgeAlert`. Kept, because an acknowledgement that says what is being done about it is the one escalation can skip."},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"description":"**Set when the metric returns to range, automatically.** An alert that only a person can close is an alert list that only grows.\n"},"escalatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. **A critical alert nobody acknowledged is the case escalation exists for.**\n"}}},
"AlertSeverity": {"type":"string","description":"How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter.","enum":["info","warning","critical"]},
"AlertStatus": {"type":"string","description":"Where a raised alert is. Shared by `Alert` and the `listAlerts` filter.","enum":["raised","acknowledged","resolved","expired"]},
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"AppendEntitlementRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the new order this creates, and its idempotency key — it must equal the `Idempotency-Key` header."},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["variantId","quantity"],"properties":{"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true}}}},"paymentMethod":{"type":"string","enum":["card","cash","wallet","giftCard","chargeToAccount"]},"note":{"type":"string","maxLength":300},"recordedAt":{"type":"string","format":"date-time"}}},
"AppendEntitlementResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["order","media"],"properties":{"order":{"allOf":[{"$ref":"#/components/schemas/Order"}],"description":"A **new** order. The original is untouched — it was paid, receipted and possibly reported on, and editing it would move yesterday's revenue.\n"},"media":{"allOf":[{"$ref":"#/components/schemas/MediaEntitlements"}],"description":"The full set now on the media, so the cashier can say what the QR does."},"addedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"AttendanceAmendment": {"type":"object","x-ticvai-persistence":"workforce.attendance_amendment","description":"One correction to an attendance record, appended by `amendAttendance` and never updated (decided 28 September, audit R129 (7)).\n","required":["id","attendanceRecordId","amendedByPrincipalId","amendedAt","occurredAtBefore","occurredAtAfter","reason"],"properties":{"id":{"type":"string","format":"uuid"},"attendanceRecordId":{"type":"string","format":"uuid"},"amendedByPrincipalId":{"type":"string","format":"uuid"},"amendedAt":{"type":"string","format":"date-time"},"occurredAtBefore":{"type":"string","format":"date-time","description":"The record's time before this correction."},"occurredAtAfter":{"type":"string","format":"date-time","description":"The time this correction set (`correctedAt` on the request)."},"reason":{"type":"string","maxLength":300}}},
"AttendanceRecord": {"type":"object","x-ticvai-persistence":"workforce.attendance","required":["id","principalId","kind","occurredAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"assignmentId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["clockIn","clockOut","breakStart","breakEnd"]},"occurredAt":{"type":"string","format":"date-time","description":"Device time — when it happened."},"recordedAt":{"type":"string","format":"date-time","description":"When the server received it. **Both are kept**: a steward clocking in offline at a gate is not late because the sync was.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"latitude":{"type":"number","nullable":true},"longitude":{"type":"number","nullable":true},"isAmended":{"type":"boolean","readOnly":true},"amendedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who made the latest amendment. The full history is `amendments` (audit R129 (7))."},"amendmentReason":{"type":"string","nullable":true,"readOnly":true,"description":"The latest amendment's reason. The full history is `amendments` (audit R129 (7))."},"originalOccurredAt":{"type":"string","format":"date-time","nullable":true,"description":"**The original is never overwritten.** Attendance feeds pay, and a record that can be quietly rewritten is not evidence.\n"},"amendments":{"type":"array","readOnly":true,"description":"**Every correction, oldest first, one row each** (decided 28 September, audit R129 (7)). A single set of amendment columns holds only the last one, and the second correction to a record would erase the evidence of the first.\n","items":{"$ref":"#/components/schemas/AttendanceAmendment"}},"exception":{"type":"string","nullable":true,"enum":["late","earlyLeave","missingClockOut","noShow","outOfGeofence","unscheduled"],"description":"Computed against the rota. Null where the record matches what was expected."}}},
"Cart": {"type":"object","x-ticvai-persistence":"orders.cart","required":["id","venueId","channel","status","lines"],"properties":{"id":{"type":"string","format":"uuid"},"token":{"type":"string","readOnly":true,"description":"**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null while anonymous. Set by `claimCart`."},"status":{"$ref":"#/components/schemas/CartStatus"},"lines":{"type":"array","items":{"$ref":"#/components/schemas/CartLine"}},"conflicts":{"type":"array","items":{"$ref":"#/components/schemas/CartConflict"}},"consentQuestions":{"type":"array","readOnly":true,"description":"**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n","items":{"allOf":[{"$ref":"../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"},{"type":"object","properties":{"lineIds":{"type":"array","description":"The cart lines that ask it. Empty for a question the flow asks.","items":{"type":"string","format":"uuid"}},"answered":{"type":"boolean","description":"Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."}}}]}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","description":"**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n","items":{"type":"string","format":"uuid"}},"couponCodes":{"type":"array","readOnly":true,"description":"The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n","items":{"type":"string","maxLength":100}},"expiresAt":{"type":"string","format":"date-time","description":"The earliest lease expiry in the cart, or the cart's own window where it holds none."},"extensionsUsed":{"type":"integer","readOnly":true},"maxExtensions":{"type":"integer","readOnly":true},"locale":{"type":"string"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time"}}},
"CartConflict": {"type":"object","x-ticvai-persistence":"none — computed on read","description":"2.9.5. Golf at 13:00 and karting at 13:00 for the same guest. **A prompt, not a refusal** — a party of four may legitimately split, and refusing would be wrong more often than right.\n","properties":{"kind":{"type":"string","enum":["overlappingTime","sameSessionDifferentVenue","exceedsPartySize","requiresPrerequisite","consentBlocksBooking"]},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"message":{"type":"string"},"isBlocking":{"type":"boolean","description":"Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold. So is `consentBlocksBooking`: a consent question answered with the answer the venue set to block the booking (decided 29 September, rev 3 REV3-26).\n"}}},
"CartLine": {"type":"object","x-ticvai-persistence":"orders.cart_line","required":["id","variantId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string","readOnly":true},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Set from `addCartLine`; checkout copies it to the order line.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"Set on a table deposit line only (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` this line secures. Priced from the deposit the booking snapshotted, not from the variant. Becomes an `orders.deposit` row at checkout, not revenue. A table booking with no deposit never has a line (rev 3 REV3-8).\n"},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"The `resources.ResourceHold` this line buys (decided 29 September, rev 3 REV3-15). While set, `leaseExpiresAt` is the hold's `expiresAt` and `inventoryHoldId` is null."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"The line this add-on is attached to, from `AddCartLineRequest.parentLineId`. Kept on the line because **removing the parent removes the child**, and `removeCartLine` has to be able to find the children.\n"},"overridePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"overrideReason":{"type":"string","nullable":true,"enum":["priceMatch","serviceRecovery","negotiated","damagedGoods","staffSale","error"],"description":"BL-085. **An operator could apply an approved discount and not enter a price.** A price match against a competitor and a service-recovery gesture are not discounts off a list — they are a number somebody decided.\n**Escalated above a configured threshold, and the reason is a closed set**: a free-text override reason is an override nobody can report on, and this is the field an auditor reads first.\n"},"feeKind":{"type":"string","nullable":true,"enum":["booking","transaction","service","delivery","convenience","cancellation"],"description":"**A fee is a line, not an adjustment.** `orders` already separates a service charge from a tip for the reason that applies here: **a guest is entitled to see what they are being charged for**, and a fee folded into the ticket price is a fee nobody can question.\nItemised at checkout, taxed on its own code, and refundable separately — **a cancellation fee is usually the one thing not refunded**, which only works if it is its own line.\n"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"inventoryHoldId":{"type":"string","nullable":true,"description":"The capacity held for this line — a `catalogue.InventoryHold.id`, typed as that id is. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"},"leaseExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"Shown to the guest. *\"Your seats are held for 6 minutes\"* is better than discovering it at checkout.\n"},"isAvailable":{"type":"boolean","readOnly":true,"description":"Re-checked on every read. **A line can become unavailable while the cart sits** — a lease expiring is not the same as the product selling out, and both land here.\n"}}},
"CartStatus": {"type":"string","enum":["active","expiring","expired","abandoned","checkedOut"]},
"CashMovement": {"x-ticvai-persistence":"orders.cash_movement","allOf":[{"$ref":"#/components/schemas/CreateCashMovementRequest"},{"type":"object","required":["shiftId","authorisedByPrincipalId","sequence"],"properties":{"shiftId":{"type":"string","format":"uuid"},"depositBoxId":{"type":"string","format":"uuid","nullable":true,"description":"The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099).\n"},"witnessPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The cashier who countersigned a withdrawal. Null on other movements."},"withdrawalReason":{"allOf":[{"$ref":"#/components/schemas/WithdrawalReason"}],"nullable":true},"authorisedByPrincipalId":{"type":"string","format":"uuid","description":"The principal who authorised the movement, recorded for audit."},"sequence":{"type":"integer","description":"Monotonic within the shift. Preserves order across an offline batch."},"syncedAt":{"type":"string","format":"date-time","nullable":true}}}]},
"CashMovementKind": {"type":"string","enum":["openingFloat","lift","add"],"description":"`openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`.\n"},
"CatalogueState": {"x-ticvai-persistence":"none — computed from workstation bundle_version","type":"object","description":"The workstation's local catalogue position. A terminal beyond `staleAfter` must refuse to trade rather than transact against stale prices.\n","required":["appliedBundleVersion","appliedAt","staleAfter","isStale"],"properties":{"appliedBundleVersion":{"type":"string"},"appliedAt":{"type":"string","format":"date-time"},"staleAfter":{"type":"string","format":"date-time","description":"Beyond this the terminal refuses to trade."},"isStale":{"type":"boolean"},"pendingBundleVersion":{"type":"string","nullable":true,"description":"Published but not yet applied."}}},
"CloseShiftRequest": {"type":"object","required":["countedCash","recordedAt"],"properties":{"countedCash":{"type":"array","minItems":1,"description":"**The cashier's blind count, one line per denomination counted** (decided 29 September, readiness close-out; our build plan). The server writes each line as one `CashCountLine` (`countKind` close) against the shift, taking the face value from `platform.denomination`. A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`.\n","items":{"$ref":"#/components/schemas/CountedDenominationLine"}},"nonCashDeclared":{"type":"array","description":"Declared totals per non-cash tender, for reconciliation against captured payments.\n","items":{"type":"object","required":["tender","amount"],"properties":{"tender":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"notes":{"type":"string","maxLength":1000},"releaseHeldLeases":{"type":"boolean","default":true,"description":"Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"CountedDenominationLine": {"type":"object","x-ticvai-persistence":"none — request only; lands as `CashCountLine` rows","description":"**One line of a cash count as the cashier types it: which note or coin, how many, and what they come to** (decided 29 September, readiness close-out; our build plan). The shape of the blind count on close (`closeShift`) and of the count columns on the till screens (POS-007, POS-011). It is the request side of `CashCountLine`, which is the stored row and adds the shift, the count kind, who counted and when.\n**`total` is shown to the cashier and checked, not trusted**: the server recomputes `count` times the denomination's face value and refuses a line whose `total` disagrees with 422 `count-total-mismatch`. An inactive or unknown denomination is refused with 422 `unknown-denomination`.\n","required":["denominationId","count"],"properties":{"denominationId":{"type":"string","format":"uuid","description":"References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there."},"count":{"type":"integer","minimum":0,"maximum":100000,"description":"**How many of this note or coin were counted.** Zero is a line, not an omission: a denomination counted and found empty."},"total":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"`count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent.\n"}}},
"CreateCashMovementRequest": {"type":"object","required":["id","kind","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7."},"kind":{"$ref":"#/components/schemas/CashMovementKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"denominations":{"$ref":"#/components/schemas/DenominationCount","x-ticvai-persisted":false,"description":"**Stored as `orders.cash_count_line` rows** with `countKind: movement` and this movement's `cashMovementId`, not as a column. The jsonb blob this used to land in is what `Denomination` was created to replace (26 September, pull audit R099).\n"},"reference":{"type":"string","maxLength":64,"description":"Safe drop reference or bag number."},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","variantId","quantity","quotedUnitPrice"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."},"variantId":{"type":"string","format":"uuid"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"inventoryHoldId":{"type":"string","nullable":true,"description":"Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"},"description":"Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"quantity":{"type":"integer","minimum":1},"eligibilityDeclaration":{"type":"array","nullable":true,"x-ticvai-note":"One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n","items":{"type":"object","properties":{"ageBand":{"type":"string","enum":["infant","child","junior","adult","senior"],"description":"Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."},"ageYears":{"type":"integer","nullable":true},"heightBandIndex":{"type":"integer","nullable":true},"confidentSwimmer":{"type":"boolean","nullable":true,"description":"**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"},"guardianSigned":{"type":"boolean"}}},"description":"What was declared for each guest on this line, kept as the record staff check at the gate."},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the client charged, from its local bundle."},"holderName":{"type":"string","nullable":true},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"}}},
"DenominationCount": {"type":"array","description":"**A count is a list of lines and the line is the row.** Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — `shift_id` — and a count line had no denomination, no quantity and no variance.\n**The array is the transport; `CashCountLine` is the row.**\n","items":{"$ref":"#/components/schemas/CashCountLine"},"minItems":1},
"DeploymentProfile": {"type":"string","description":"How this workstation obtains catalogue and inventory (ADR-0013).\n- `terminalLocal` — own SQLite, leases direct from the cell. Small venues, 4G sites - `venueEdge` — own SQLite, distributed via the venue edge node which holds the\n  venue lease and sub-leases to terminals. Mid and large venues, stadium gates\n- `thin` — no local catalogue, server reads. Non-transactional surfaces only\n","enum":["terminalLocal","venueEdge","thin"]},
"DepositBox": {"type":"object","x-ticvai-persistence":"orders.deposit_box + orders.deposit_box_opening_denomination + orders.deposit_box_foreign_holding","description":"5.8. **Allocated to a cashier, not to a workstation.** A cashier moving between tills takes their float with them, which is what makes a variance attributable to a person.\n**`openingDenominations` and `foreignHoldings` are child rows** (26 September, pull audit R099): `orders.deposit_box_opening_denomination` and `orders.deposit_box_foreign_holding`, one row per item, keyed to the box. Until then the contract carried both and the table had nowhere to put either.\n","required":["cashierPrincipalId","venueId","openingFloat"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"cashierPrincipalId":{"type":"string","format":"uuid"},"cashierName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where it is being used now. **Changes during a shift; the box does not.**"},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The shift trading from this box. A UUIDv7, as `Shift.id` is."},"status":{"$ref":"#/components/schemas/DepositBoxStatus"},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"openingDenominations":{"type":"array","description":"5.8.3. **Either this or a total** — a supervisor handing over a counted bag should not have to re-count it into fields. POS-001 offered only denominations until 14 August.\n","items":{"type":"object","required":["denominationId","count"],"properties":{"denominationId":{"type":"string","format":"uuid","description":"References `platform.denomination`, as `CashCountLine.denominationId` does. Until 26 September this was `denomination: number` — a face value as a JSON float, which naming-and-style 5.1 forbids and which could disagree with the note it named (pull audit R122).\n"},"count":{"type":"integer","minimum":0}}}},"withdrawnTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"**Reduces the expected close figure.** Cash skimmed for banking is not a shortfall, and a system that treats it as one makes every busy cashier look short.\n"},"foreignHoldings":{"type":"array","description":"4.6.11 and 6.1.10. **Foreign cash accepted at this till, counted separately by currency.** A till taking USD and EUR alongside AED has three counts and three variances — collapsing them into a base-currency total makes a variance unattributable to the currency that caused it.\n**No opening float in a foreign currency and no change given in one.** Foreign cash only ever comes in, which is what keeps this to one number per currency rather than a full reconciliation each.\n","items":{"type":"object","required":["currency","countedAmount"],"properties":{"currency":{"type":"string","pattern":"^[A-Z]{3}$","description":"**Stored, because it is the one thing that is not the region's.** A foreign holding is by definition cash in a currency the till does not trade in, so it cannot resolve from the region (ADR-0018) the way the box's own amounts do; it is the key of the row, one per currency per box. The amounts on this item are in this currency.\n"},"expectedAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The sum of tenders taken in this currency during the shift."},"countedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"baseEquivalent":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**At the rates on the payments, not today's.** A shift closed on Friday and reviewed on Monday is reviewed at Friday's rates (CF-37).\n"}}}},"expectedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"countedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**Flagged where it is not the holder.** A box closed without its holder present is allowed — the cash is counted by somebody, and who counted it is the record.\n"},"allocatedAt":{"type":"string","format":"date-time","description":"When the device recorded the allocation. `allocateDepositBox` is offline-capable, so for a box allocated offline this differs from the server's receipt time.\n"},"closedAt":{"type":"string","format":"date-time","nullable":true}}},
"DepositBoxStatus": {"type":"string","enum":["allocated","open","suspended","closing","closed","reconciled"]},
"DeviceBinding": {"x-ticvai-persistence":"platform.device","type":"object","required":["kind","driver"],"properties":{"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen.\n"},"identifier":{"type":"string","description":"Serial","port or network address.":null},"isRequired":{"type":"boolean","default":false,"description":"When true, the workstation refuses to open a shift if the device is absent.\n"}}},
"EntitlementStatus": {"type":"string","description":"**What the storage layer holds, and what a guest is shown.** `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot distinguish a ticket that was used from one that expired, was refunded, or was transferred to somebody else, and those are four different conversations at a gate.\nAdded 17 August. `states/entitlement.yaml` had modelled these six since 14 August and the contract had no enum behind it, which the state checker reported correctly for three days.\n","enum":["issued","partiallyConsumed","fullyConsumed","expired","cancelled","surrendered"]},
"ExchangeOrderRequest": {"type":"object","required":["id","outgoingLineIds","incomingLines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header."},"outgoingLineIds":{"type":"array","minItems":1,"items":{"type":"string","format":"uuid"}},"incomingLines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"waiveFee":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaAssetDetail": {"x-ticvai-persistence":"assets.media_asset","allOf":[{"$ref":"#/components/schemas/MediaAsset"},{"type":"object","properties":{"derivatives":{"type":"array","description":"Generated from the original, never uploaded separately. A new breakpoint is a re-render rather than a re-upload of everything.\n","items":{"type":"object","properties":{"label":{"type":"string"},"width":{"type":"integer"},"height":{"type":"integer"},"sizeBytes":{"type":"integer"},"url":{"type":"string"}}}},"usage":{"type":"array","description":"Every place this asset is referenced.","items":{"$ref":"#/components/schemas/MediaUsage"}},"collections":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"}}}},"previousVersions":{"type":"array","items":{"type":"object","properties":{"version":{"type":"integer"},"replacedAt":{"type":"string","format":"date-time"},"replacedByPrincipalId":{"type":"string","format":"uuid"}}}}}}]},
"MediaEntitlements": {"type":"object","x-ticvai-persistence":"none — projection over entitlement and scan history","required":["mediaCode","isValid","entitlements"],"properties":{"mediaCode":{"type":"string"},"mediaKind":{"type":"string","enum":["qr","wristband","card","nfc","mobilePass"]},"subjectId":{"type":"string","format":"uuid","nullable":true},"isValid":{"type":"boolean"},"invalidReason":{"type":"string","nullable":true},"canAcceptMore":{"type":"boolean","description":"False where the media has been surrendered, expired or blocked. A cashier should know before taking money, not after.\n"},"entitlements":{"type":"array","items":{"type":"object","properties":{"entitlementId":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["admission","locker","fnb","retail","parking","rental","experience","membership"]},"orderId":{"type":"string","format":"uuid"},"addedAt":{"type":"string","format":"date-time"},"status":{"allOf":[{"$ref":"#/components/schemas/EntitlementStatus"}],"description":"**Replaced `isRedeemed` on 17 August.** A boolean could not distinguish a ticket that was used from one that expired, was refunded, or was transferred — four different conversations at a gate, and the steward could see only \"not valid\".\n"},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true},"redeemedAt":{"type":"string","format":"date-time","nullable":true},"transferredToSubjectId":{"type":"string","format":"uuid","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true}}}}}},
"MediaUsage": {"x-ticvai-persistence":"assets.media_usage","type":"object","description":"One place an asset is used. **`surface: product` is written by catalogue** for each item of `Product.media` (decided 29 September, rev 3 23SEP-4): `referenceId` is the product id and `isLive` is true while the product is listed to guests, which is what stops an asset in use on a ticket card being archived from under it.\n","required":["surface","referenceId"],"properties":{"extractedText":{"type":"string","description":"**Text pulled out of an uploaded document**, after extraction. The generic retrieval path for anything a tenant uploads — a PDF nobody can search is a PDF nobody reads.\n"},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"surface":{"type":"string","enum":["tenantBranding","homepageBanner","promoBlock","contentPage","product","event","menuItem","merchandise","workOrder","incident","inspection","campaign"]},"referenceId":{"type":"string"},"label":{"type":"string"},"isLive":{"type":"boolean","description":"True where the referencing surface is published to guests."}}},
"Menu": {"x-ticvai-persistence":"fnb.menu","type":"object","required":["id","code","name","outletId","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"outletId":{"type":"string","format":"uuid"},"availability":{"$ref":"#/components/schemas/MenuAvailability"},"sections":{"type":"array","items":{"$ref":"#/components/schemas/MenuSection"}},"isActive":{"type":"boolean"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `MenuVersion.version` live now. Null for a menu never published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"MenuAvailability": {"x-ticvai-persistence":"none — embedded in menu","type":"object","description":"When this menu is in force. Absent means always. Days, times and dates are all read in the Region's time zone, not UTC.","properties":{"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}},"startTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"endTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"validFrom":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."},"validTo":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."}}},
"MenuItem": {"x-ticvai-persistence":"fnb.menu_item","type":"object","required":["id","productVariantId","name","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"productVariantId":{"type":"string","format":"uuid","description":"The catalogue variant this item sells. Pricing and tax come from there — a menu is a presentation of the catalogue, not a second catalogue.\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"sortOrder":{"type":"integer"},"modifierGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"stationId":{"type":"string","format":"uuid","nullable":true},"menuSectionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."},"isStockTracked":{"type":"boolean","description":"True where a recipe exists. Stock-tracked items cannot be sold offline."},"isAvailable":{"type":"boolean"},"unavailableReason":{"type":"string","nullable":true},"restoreAt":{"type":"string","format":"date-time","nullable":true,"description":"When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."},"preparationMinutes":{"type":"integer","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}},
"MenuSection": {"x-ticvai-persistence":"fnb.menu_section","type":"object","required":["code","name","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string"},"name":{"type":"string"},"sortOrder":{"type":"integer"},"items":{"type":"array","description":"The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`.","items":{"$ref":"#/components/schemas/MenuItem"}}}},
"MetricSource": {"type":"string","description":"**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` was deliberately absent from the first cut** because it needed the staff-assignment link CL-01 covers. It was added on 18 August once `resources.Resource` produced it — see `x-ticvai-extension-note` below. Naming a metric with no source is still the defect this enum exists to prevent.\n**Money-valued metrics are listed in `x-ticvai-money-valued`.** A reading or threshold on one of them is a `Money`, never a float (`MetricValue`).\n","enum":["occupancy","capacityUtilisation","admissionRate","noShowRate","conversion","salesByOperator","salesByWorkstation","waitTime","throughput","abandonmentRate","inventoryValuation","stockTurnover","stockAgeing","wastageRate","resaleVolume","resaleCommission","salesByInstructor","resourceUtilisation","allocationUtilisation","channelAllocationBurn","membershipChurn","membershipRenewalRate","supplierDeliveryPerformance","revenuePerEntitlement","revenuePerVisitor","assetDowntime","meanTimeToRepair","challengeCompletionRate","attributedRevenue","loyaltyActiveMembers","loyaltyTierDistribution","loyaltyPointsLiability","loyaltyBreakageRate","loyaltyMemberRetention","challengeParticipationRate","gamificationLoyaltyImpact","gamificationMembershipImpact","gamificationRetention","accreditationApplications","accreditationTimeToDecision","accreditationCredentialsIssued","accreditationActiveHolders","accreditationRenewalsDue","staffingShortfall"],"x-ticvai-money-valued":["inventoryValuation","resaleCommission","revenuePerEntitlement","revenuePerVisitor","attributedRevenue","loyaltyPointsLiability"],"x-ticvai-extended-29-september":"**Fourteen metrics added 29 September (build pass)**, each checked against the schema of the contract that produces it.\n\n| Metric | Source | Requirement | |---|---|---| | `loyaltyActiveMembers` | `marketing.loyalty_position` members with a `marketing.loyalty_points` movement in the period | 5.4.27 | | `loyaltyTierDistribution` | `marketing.loyalty_position.tier_id` against `marketing.programme_tier`, members per tier | 5.4.27 | | `loyaltyPointsLiability` | the balance of `ledger.journal_line` on each programme's `pointsLiabilityAccountId`, where points post on accrual and release on redemption or expiry | 5.4.27 | | `loyaltyBreakageRate` | `marketing.loyalty_points` expiry movements over points earned, in the period | 5.4.27 | | `loyaltyMemberRetention` | members with a movement in the previous period who also have one in this period | 5.4.27 | | `challengeParticipationRate` | distinct `marketing.challenge_progress.subject_id` over active loyalty members | 22.6.20 | | `gamificationLoyaltyImpact` | points earned per member, challenge participants against non-participants (`marketing.loyalty_points` split by `marketing.challenge_progress`) | 22.6.20 | | `gamificationMembershipImpact` | joins and renewals in `identity.customer_membership`, participants against non-participants | 22.6.20 | | `gamificationRetention` | return visits (`access.scan_event`, in-direction) of participants against non-participants | 22.6.20 | | `accreditationApplications` | `accreditation.application` by `status` | 12.1.50 | | `accreditationTimeToDecision` | `accreditation.application.decided_at` minus `submitted_at` | 12.1.50 | | `accreditationCredentialsIssued` | `accreditation.credential.issued_at` | 12.1.50 | | `accreditationActiveHolders` | `accreditation.holder` `active`, by `category_code` | 12.1.50 | | `accreditationRenewalsDue` | `accreditation.holder.valid_to` inside `accreditation.validity.renewal_window_days` | 12.1.50 |\n\n**`staffingShortfall` added the same evening (build pass, group G2; 8.2.49)**: the largest gap in the window between the staff rostered and the staff the forecast requires, per venue and position, from `workforce.forecast_requirement` (the handed-over AI staff requirement) against `workforce.rota_assignment` and `workforce.open_shift`, computed as `workforce.getStaffingCoverage` with `basis` `forecastRequirement`. An `AlertRule` on it with `comparator` `above` and `threshold` 0 is the staffing shortage alert; `windowMinutes` looks ahead rather than back for this metric (the rota for the coming window), and `cooldownMinutes` stops one short shift alerting every quarter hour.\n\n**Points issued, points redeemed, campaign performance and reward redemption were already served** by the `loyalty` and `campaigns` sources, and challenge completion and revenue attribution by `challengeCompletionRate` and `attributedRevenue`.\n","x-ticvai-money-valued-note":"**`salesByOperator`, `salesByWorkstation` and `resaleVolume` are not listed because the package does not say whether they count sales or sum their value.** Until that is decided, a rule on them carries a plain number.\n","x-ticvai-extended":"18 August 2026","x-ticvai-extension-note":"**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"NoSaleEvent": {"type":"object","x-ticvai-persistence":"orders.no_sale_event","required":["id","shiftId","reason","principalId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"reason":{"type":"string"},"note":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"},"countThisShift":{"type":"integer","description":"Running count. Returned so the terminal can show it — a cashier who can see they are on their ninth no-sale behaves differently from one who cannot.\n"}}},
"OpenShiftRequest": {"type":"object","required":["workstationId","openingFloat"],"properties":{"workstationId":{"type":"string","format":"uuid"},"openingFloat":{"$ref":"#/components/schemas/DenominationCount"},"depositBoxCode":{"type":"string","maxLength":64,"description":"Physical container assigned to this shift. Required where the venue configures deposit box allocation.\n"},"bagNumber":{"type":"string","maxLength":64,"description":"Required where the venue configures bag numbers as mandatory."},"recordedAt":{"type":"string","format":"date-time","description":"When the device recorded it. `openShift` is online-only (F32), so this differs from server receipt time only by transit; it is kept because the shift's other device writes are ordered against it.\n"}}},
"OpeningHoursWindow": {"type":"object","description":"26 September, pull audit R088. **One weekly window an outlet is open.** `Outlet.openingHours` was an array of untyped objects. The shape is the one `supportHours.windows` already uses — a day and a from/to — with the times as local `HH:MM` in the region's time zone. Several windows on one day are a split shift, such as lunch and dinner.\n","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet opens."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet closes."}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderExchangeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["orderId","outgoingValue","incomingValue","difference"],"properties":{"orderId":{"type":"string","format":"uuid"},"outgoingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incomingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exchangeFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Only the difference settles. The replacement is held before the original is released, never the other way round.\n"},"newLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"Outlet": {"type":"object","x-ticvai-persistence":"platform.outlet","required":["id","code","name","venueId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/OutletKind"},"zone":{"type":"string","nullable":true},"stockLocationId":{"type":"string","format":"uuid","nullable":true,"description":"Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not.\n"},"costCenterId":{"type":"string","format":"uuid","nullable":true,"description":"Revenue and cost attribution. Outlet is the natural grain for both."},"openingHours":{"type":"array","description":"The weekly pattern, one entry per window. Several windows on a day are allowed.","items":{"$ref":"#/components/schemas/OpeningHoursWindow"}},"isActive":{"type":"boolean"}}},
"OutletKind": {"type":"string","enum":["shop","restaurant","bar","cafe","kiosk","gameFloor","ticketOffice","mobile"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Principal": {"x-ticvai-persistence":"identity.principal","type":"object","required":["id","username","displayName","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"username":{"type":"string"},"displayName":{"type":"string"},"isActive":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"Past this, resolution returns DENY regardless of grants."},"primaryRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Determines the landing screen when the principal holds several roles and picks one at login.\n"},"roles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"lastLoginAt":{"type":"string","format":"date-time","nullable":true}}},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"RotaAssignment": {"type":"object","x-ticvai-persistence":"workforce.rota_assignment","required":["principalId","venueId","startsAt","endsAt","position"],"properties":{"overtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"description":"BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"},"restPeriodBefore":{"type":"integer","nullable":true,"description":"Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"},"breachesWorkingHourLimit":{"type":"boolean","default":false,"readOnly":true,"description":"**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"},"labourCost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"},"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"position":{"type":"string","description":"What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"},"requiredRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/RotaStatus"},"breakMinutes":{"type":"integer","nullable":true},"note":{"type":"string","nullable":true}}},
"RotaStatus": {"type":"string","enum":["planned","published","confirmed","swapPending","cancelled","completed","noShow"]},
"SaleBoardKind": {"type":"string","enum":["ticketing","fnb","retail","mixed"]},
"Shift": {"x-ticvai-persistence":"orders.pos_shift + orders.pos_shift_approval + orders.pos_shift_incident","description":"**`approvals` and `incidents` are child rows** (26 September, pull audit R099): `orders.pos_shift_approval` and `orders.pos_shift_incident`, one row per item, keyed to the shift. Until then the contract carried both and `orders.pos_shift` had nowhere to put either.\n","type":"object","required":["id","workstationId","venueId","scopePath","principalId","status","currency","currencyScale","openedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key."},"workstationId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"principalId":{"type":"string","format":"uuid","description":"Who opened it. Cash reconciles to a person and a drawer."},"principalDisplayName":{"type":"string"},"incidents":{"type":"array","description":"BL-097. **A till has exceptions and there was nowhere to write them** — a no-sale, a drawer opened without a transaction, a manager override, a guest dispute.\n**This is the log a cash-up investigation starts from**, and a shift that balances with four unexplained no-sales is not a shift that balanced.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["noSale","drawerOpen","override","voidAfterPayment","guestDispute","tillJam","priceQuery","other"]},"at":{"type":"string","format":"date-time"},"principalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true}}}},"status":{"$ref":"#/components/schemas/ShiftStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"depositBoxCode":{"type":"string","nullable":true},"bagNumber":{"type":"string","nullable":true},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"salesTotal":{"x-ticvai-column":"gross_sales_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till took in sales, as the guest paid it — tax included."},"refundsTotal":{"x-ticvai-column":"gross_refunded_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till paid back, as the guest was refunded it — tax included."},"liftsTotal":{"x-ticvai-column":"lifted_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net."},"expectedCash":{"x-ticvai-column":"expected_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"26 September, pull audit R207. **The figure the blind count was measured against**, revealed once the count is in — null until then. Until this date only `ShiftCloseResult` carried it, returned once by `closeShift`, so BO-040 could not show the over/short it exists to accept.\n"},"countedCash":{"x-ticvai-column":"counted_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"What the close count found. Null until the shift is counted."},"variance":{"x-ticvai-column":"variance_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"Counted minus expected, as `ShiftCloseResult.variance`. Negative is short."},"heldLeaseCount":{"type":"integer","description":"Inventory leases currently held by this workstation. Surfaced so an operator closing a shift can see what will be returned.\n"},"openedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time","description":"When the device recorded the open. `openedAt` is the server's time."},"suspendedAt":{"type":"string","format":"date-time","nullable":true},"suspendReason":{"type":"string","maxLength":200,"nullable":true,"description":"The `reason` given to `suspendShift`. Cleared on resume."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who submitted the close count. `reopenShift` refuses an approver who is this principal, and until 26 September there was nothing to compare against (pull audit R099).\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while the shift has unsynced operations."},"approvals":{"type":"array","items":{"type":"object","required":["kind","principalId","at"],"properties":{"kind":{"type":"string","enum":["open","close","variance"],"description":"`open` from `approveShiftOpen`, `close` from `approveShiftClose`, `variance` from `acceptShiftVariance`.\n"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"reason":{"type":"string"}}}}}},
"ShiftCloseResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["shift","expectedCash","countedCash","variance","requiresAcceptance"],"properties":{"shift":{"$ref":"#/components/schemas/Shift"},"expectedCash":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"countedCash":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Counted minus expected. Negative is short."},"requiresAcceptance":{"type":"boolean","description":"True when the variance exceeds the venue's `shiftVarianceThreshold` (audit R094). The shift is then `pendingVariance` and only `acceptShiftVariance` finalises it (audit R080 (e)).\n"},"nonCashVariances":{"type":"array","items":{"type":"object","required":["tender","declared","captured","variance"],"properties":{"tender":{"type":"string"},"declared":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"captured":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"ShiftStatus": {"type":"string","enum":["pendingApproval","open","suspended","pendingVariance","pendingClosure","closed","autoClosed"]},
"SupervisorStepUp": {"type":"object","description":"**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid","description":"The supervisor signing. Recorded against the act."},"credential":{"type":"string","maxLength":512,"writeOnly":true,"description":"The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."}}},
"TableCombination": {"type":"object","x-ticvai-persistence":"fnb.table_combination","description":"**Tables that can be pushed together, and what they seat together.** Declared by a host rather than inferred from a floor plan — a pillar, a step or a service run stops two adjacent tables combining. `setTableCombinations` writes the outlet's set.\n","required":["tableIds","combinedCovers"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"outletId":{"type":"string","format":"uuid","readOnly":true,"description":"The outlet in the path."},"tableIds":{"type":"array","minItems":2,"items":{"type":"string","format":"uuid"}},"combinedCovers":{"type":"integer","minimum":1},"setupMinutes":{"type":"integer","default":5},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `outlet` scope."}}},
"TableDefinition": {"x-ticvai-persistence":"fnb.dining_table","type":"object","description":"A restaurant (dining) table, reserved with `createTableReservation`. Not a map-bookable `resources` table, which is a non-dining spot sold like a cabana (decided 29 September, rev 3 GAP-C2).","required":["id","label","capacity"],"properties":{"id":{"type":"string","format":"uuid"},"label":{"type":"string","maxLength":32,"x-ticvai-unique":"venue","description":"**The table code, unique per venue** (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is read. `createTable` and `updateTable` refuse a duplicate with `409` `duplicate-code`.\n"},"capacity":{"type":"integer","minimum":1},"zone":{"type":"string","nullable":true},"position":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"shape":{"type":"string","enum":["round","square","rectangle","booth","bar"]},"isOutOfService":{"type":"boolean","default":false,"description":"**Damaged, or its section closed.** `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`."}}},
"TableMap": {"x-ticvai-persistence":"none — projection","type":"object","required":["outletId","tables"],"properties":{"outletId":{"type":"string","format":"uuid"},"zones":{"type":"array","items":{"type":"string"}},"tables":{"type":"array","items":{"$ref":"#/components/schemas/TableState"}}}},
"TableState": {"x-ticvai-persistence":"none — projection over table and visit","allOf":[{"$ref":"#/components/schemas/TableDefinition"},{"type":"object","required":["status"],"properties":{"status":{"$ref":"#/components/schemas/TableStatus"},"visitId":{"type":"string","format":"uuid","nullable":true},"covers":{"type":"integer","nullable":true},"seatedAt":{"type":"string","format":"date-time","nullable":true},"serverPrincipalId":{"type":"string","format":"uuid","nullable":true},"billTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}]},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}},
"WithdrawalReason": {"type":"string","description":"Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records.","enum":["banking","safeDrop","changeOrder","other"]},
"Workstation": {"x-ticvai-persistence":"platform.workstation","type":"object","required":["id","code","name","venueId","regionId","scopePath","saleBoard","currency","currencyScale","timeZone"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"saleBoard":{"type":"object","description":"Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. What the operator may then DO within it is governed by their permissions.\n","required":["id","kind"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"name":{"type":"string"}}},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point.\n"},"devices":{"type":"array","items":{"$ref":"#/components/schemas/DeviceBinding"}},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"timeZone":{"type":"string"},"deploymentProfile":{"$ref":"#/components/schemas/DeploymentProfile"},"edgeNodeId":{"type":"string","format":"uuid","nullable":true,"description":"Present when `deploymentProfile` is `venueEdge`."},"healthScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"readOnly":true,"description":"Board 1 of the client's POS set. **A number a manager can sort by** — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a score.\nThe client's board shows 1,248 workstations at 96% healthy, and **the value of that figure is that it ranks**: a fleet dashboard exists so somebody can open the worst one first.\n**Derived from its devices, its heartbeat age, its firmware currency and its error rate.** Read-only, because a workstation that could set its own score would.\n**The formula, proposed, client to correct (audit R096 (2)):** score = 40% device online share (the share of its devices reporting online) + 25% heartbeat freshness (100 at one minute old or less, 0 at 15 minutes or more, linear between) + 20% firmware and profile currency (100 on the latest, 50 one version behind, 0 older) + 15% error rate (100 at 0 errors an hour, 0 at 10 or more, linear between), rounded to a whole number. **Below 80 is a warning and below 60 a failure.**\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"description":"Which profile this workstation runs, and at which version. **The client's board shows a fleet split four ways — 72% latest, 18.8% one behind, 6.1% outdated** — and the package had a firmware version field and no profile.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks*.\n"},"catalogueState":{"$ref":"#/components/schemas/CatalogueState"},"offlineCapable":{"type":"boolean","description":"Derived from `deploymentProfile`. False only for `thin`. Under local-first, catalogue READS are always local on transactional surfaces; this flag governs whether WRITES can be queued.\n"},"isActive":{"type":"boolean"}}}
}
```
