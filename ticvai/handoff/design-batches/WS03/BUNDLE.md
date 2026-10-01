# WS03 — Access Control board 3

**10 screens · 17 operations · 24 schemas · 5 permissions**

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
  `ACCESS_POINT_CONFIGURE, AUDIT_VIEW, GUEST_MANAGE, SCOPE_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
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
| `BO-164` | Digital Credential Security Command Center | A | 4 | 2 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-165` | Dynamic QR Security Profile Builder | B–D | 13 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-166` | Credential Activation & Display Rules | A | 6 | 0 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-167` | Device Binding & Session Security | B–D | 5 | 16 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-168` | BLE Beacon & Geofence Configuration | A | 8 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-169` | Credential Transfer & Rebinding | B–D | 10 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-170` | Credential Revocation & Lifecycle Events | B–D | 7 | 2 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-171` | Offline Cryptographic Validation Profile | B–D | 7 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-172` | Embedded Entitlement Payload Designer | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-173` | Credential Security Simulation, Audit & Publication | B–D | 0 | 13 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-166, BO-170, BO-171, BO-172, BO-173 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-164` Digital Credential Security Command Center

**Central configuration and monitoring page for all secure digital credentials.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #20673 (APP-SETUP-BO-164) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `AUDIT_VIEW`, `SCOPE_VIEW` (1 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/digital-credential-security-command-center-bo-164` |

#### Inputs: what the user enters or picks

**Form: Save device binding policy** (modal, opened by *Save device binding policy*; *Save device binding policy* calls `setDeviceBindingPolicy`, *Cancel* sends nothing)

**Collects what `setDeviceBindingPolicy` sends before it is called.** Required: `venueId`. Optional: `maximumActiveDevices`, `concurrentSessions`, `deviceChangePolicy`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setDeviceBindingPolicy` body |
| Maximum active devices `maximumActiveDevices` | number field | optional | 1 | min 1 | — | Devices the credential may be active on at once | `setDeviceBindingPolicy` body |
| Concurrent sessions `concurrentSessions` | number field | optional | 1 | min 1 | — | — | `setDeviceBindingPolicy` body |
| Device change policy `deviceChangePolicy` | radio group | optional | OTP verification required | Not allowed · Allowed before first use · OTP verification required · Operator approval required · Supervisor approval required | — | — | `setDeviceBindingPolicy` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Active Digital Credentials** (metric tile)

**Dynamic QR Enabled** (metric tile)

**Device-Bound Credentials** (metric tile)

**Location-Protected Credentials** (metric tile)

**Offline-Ready Credentials** (metric tile)

**Credentials Revoked Today** (metric tile)

**Transfer Events** (metric tile)

**Security Alerts** (metric tile)

**Suspicious Sessions** (metric tile)

**Every digital credential security** (data table, from `listDigitalCredentialSecurity`)

| Shows | Format | Notes |
|---|---|---|
| Credential type | chip: Dynamic QR ticket, Membership, Annual pass, Mobile wallet, Loyalty, Digital pass… | — |

**The selected digital credential security** (detail panel): The pack groups this record's detail under its own headings: “For each credential profile”.

| Shows | Format | Notes |
|---|---|---|
| Credential type | chip: Dynamic QR ticket, Membership, Annual pass, Mobile wallet, Loyalty, Digital pass… | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save device binding policy (primary button) | `setDeviceBindingPolicy` PUT `/device-binding-policy` | DeviceBindingPolicyInput | AccessCredentialPolicy | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Data it reads**: `listDigitalCredentialSecurity` (onLoad, Digital Credential Security Command Center); `listCredentialSecurity` (onLoad, Credential Security Simulation, Audit & Publication)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-165` Dynamic QR Security Profile Builder: *Works in Dynamic QR Security Profile Builder*; calls `listDigitalCredentialSecurity`
- → `BO-166` Credential Activation & Display Rules: *Works in Credential Activation & Display Rules*; calls `listDigitalCredentialSecurity`
- → `BO-167` Device Binding & Session Security: *Works in Device Binding & Session Security*; calls `listDigitalCredentialSecurity`
- → `BO-168` BLE Beacon & Geofence Configuration: *Works in BLE Beacon & Geofence Configuration*; calls `listDigitalCredentialSecurity`
- → `BO-169` Credential Transfer & Rebinding: *Works in Credential Transfer & Rebinding*; calls `listDigitalCredentialSecurity`
- → `BO-170` Credential Revocation & Lifecycle Events: *Works in Credential Revocation & Lifecycle Events*; calls `listDigitalCredentialSecurity`
- → `BO-171` Offline Cryptographic Validation Profile: *Works in Offline Cryptographic Validation Profile*; calls `listDigitalCredentialSecurity`
- → `BO-172` Embedded Entitlement Payload Designer: *Works in Embedded Entitlement Payload Designer*; calls `listDigitalCredentialSecurity`
- → `BO-173` Credential Security Simulation, Audit & Publication: *Works in Credential Security Simulation, Audit & Publication*; calls `listDigitalCredentialSecurity`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital credential security list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital credential security untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital credential security yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the digital credential security are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listDigitalCredentialSecurity` → `SCOPE_VIEW` (read) · staff
- `listCredentialSecurity` → `AUDIT_VIEW` (read) · staff
- `setDynamicSecurityProfile` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `setDeviceBindingPolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-164` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-164`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 1: Opens Digital Credential Security Command Center → Central configuration and monitoring page for all secure digital credentials.
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F113 branch at step 1 (expected): when Nothing has been set up on Digital Credential Security Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F113 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-164?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save device binding policy.
- [ ] Every transition is wired: `BO-100`, `BO-165`, `BO-166`, `BO-167`, `BO-168`, `BO-169`, `BO-170`, `BO-171`, `BO-172`, `BO-173`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `AUDIT_VIEW`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-165` Dynamic QR Security Profile Builder

**Configure how a dynamic QR is generated and protected. The matrix requires a unique QR per issued ticket/pass and periodic QR refresh to reduce screenshot and duplication fraud.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Options; Configuration may include) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/dynamic-qr-security-profile-builder-bo-165` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Refresh Every: 30 seconds | text field | — | — | — | — | — | — |
| 15 sec | select field | — | — | — | — | — | — |
| 30 sec | select field | — | — | — | — | — | — |
| 45 sec | select field | — | — | — | — | — | — |
| 60 sec | select field | — | — | — | — | — | — |
| Custom | select field | — | — | — | — | — | — |
| Credential ID | select field | — | — | — | — | — | — |
| Ticket ID | select field | — | — | — | — | — | — |
| Timestamp | select field | — | — | — | — | — | — |
| Nonce / OTP | select field | — | — | — | — | — | — |
| Device binding reference | select field | — | — | — | — | — | — |
| Venue context | select field | — | — | — | — | — | — |
| Entitlement payload | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `setDynamicSecurityProfile`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic security profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic security profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic security profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setDynamicSecurityProfile` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dynamic QR is chosen per event (fully dynamic, normal, or mixed); a per-product override disables it for exceptions such as physically delivered VIP invitations and B2B/reseller tickets, which fall back to standard QR or RFID. *(agreed · MoM 2 Sep 2026, 4.7 Dynamic QR Code - Business Flexibility & Exceptions · DI-633)*
- **Open question.** Dynamic QR refreshes periodically to cut fraud/resale. Open: beacon-based (code hidden until the phone is near a gate beacon via Bluetooth, then refreshes ~every 2 minutes; Qossai: more secure) vs app-generated; GPS geofencing also raised. Chinmay to propose. *(open · MoM 2 Sep 2026, 4.6 Dynamic QR Code - Concept & Generation Approach · DI-630)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-165` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-165`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 2: Works in Dynamic QR Security Profile Builder → Configure how a dynamic QR is generated and protected. The matrix requires a unique QR per issued ticket/pass and periodic QR refresh to reduce screenshot and duplication fraud.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-165?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-166` Credential Activation & Display Rules

**Configure when the guest is permitted to see/use the credential. The matrix specifies that after registration, a ticket may appear as a blurred QR and only become clear and usable near the park entrance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #20674 (APP-SETUP-BO-166) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-activation-display-rules-bo-166` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Sent by *Save activation and display rule*** (`setCredentialActivationDisplay`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rule `ruleId` | picker: choose a rule | optional | — | — | shows names, sends the id | Absent creates a rule | `setCredentialActivationDisplay` body |
| Venue `venueId` | text field | required | — | — | — | Venue the rule applies to | `setCredentialActivationDisplay` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setCredentialActivationDisplay` body |
| Before activation display `beforeActivationDisplay` | multi-select chips | required | — | Hide QR · Blur QR · Show countdown · Show available at venue · Show venue directions | — | What the guest sees before the credential activates | `setCredentialActivationDisplay` body |
| Active display `activeDisplay` | multi-select chips | required | — | Dynamic QR · Activation timer · Credential status · Remaining entitlements | — | What the guest sees once it is active | `setCredentialActivationDisplay` body |
| Activation triggers `activationTriggers` | list of values (chips) | required | — | at least 1 | — | What activates the credential, e.g. | `setCredentialActivationDisplay` body |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save activation and display rule (primary button) | `setCredentialActivationDisplay` PUT `/credential-activation-display` | CredentialActivationDisplayRulesInput | CredentialActivationDisplayRulesView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 No activation trigger, or a display option that contradicts another (hideQr with blurQr) | — |

**Data it reads**: `listCredentialActivationDisplay` (onLoad, Credential Activation & Display Rules)

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `listCredentialActivationDisplay`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential activation display list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential activation display untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential activation display yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential activation display are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 No activation trigger, or a display option that contradicts another (hideQr with blurQr) |

#### Permissions

- `listCredentialActivationDisplay` → `SCOPE_VIEW` (read) · staff
- `setCredentialActivationDisplay` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dynamic QR is chosen per event (fully dynamic, normal, or mixed); a per-product override disables it for exceptions such as physically delivered VIP invitations and B2B/reseller tickets, which fall back to standard QR or RFID. *(agreed · MoM 2 Sep 2026, 4.7 Dynamic QR Code - Business Flexibility & Exceptions · DI-633)*
- The dynamic QR stays blurred until beacon proximity is detected, then activates and refreshes on a short interval (e.g. every 6-12 seconds); screenshot capture of the active code is prevented. *(client request · MoM 2 Sep 2026, 4.6 Credential activation and display rules · DI-632)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-166` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-166`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 4: Works in Credential Activation & Display Rules → Configure when the guest is permitted to see/use the credential. The matrix specifies that after registration, a ticket may appear as a blurred QR and only become clear and usable near the park …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-166?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save activation and display rule.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-167` Device Binding & Session Security

**Prevent one credential from being shared across unauthorized devices. The source explicitly requires tickets to be linked to a specific device/user and suspicious patterns such as device sharing and multiple simultaneous sessions to be detected.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `GUEST_MANAGE`, `SCOPE_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `bindingId` (navigation) |
| Route | `/access-venue/device-binding-session-security-bo-167` |

#### Inputs: what the user enters or picks

**Form: Save device binding policy** (modal, opened by *Save device binding policy*; *Save device binding policy* calls `setDeviceBindingPolicy`, *Cancel* sends nothing)

**Collects what `setDeviceBindingPolicy` sends before it is called.** Required: `venueId`. Optional: `maximumActiveDevices`, `concurrentSessions`, `deviceChangePolicy`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setDeviceBindingPolicy` body |
| Maximum active devices `maximumActiveDevices` | number field | optional | 1 | min 1 | — | Devices the credential may be active on at once | `setDeviceBindingPolicy` body |
| Concurrent sessions `concurrentSessions` | number field | optional | 1 | min 1 | — | — | `setDeviceBindingPolicy` body |
| Device change policy `deviceChangePolicy` | radio group | optional | OTP verification required | Not allowed · Allowed before first use · OTP verification required · Operator approval required · Supervisor approval required | — | — | `setDeviceBindingPolicy` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Release credential device** (modal, opened by *Release credential device*; *Release credential device* calls `releaseCredentialDevice`, *Cancel* sends nothing)

**Collects what `releaseCredentialDevice` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `releaseCredentialDevice` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `binding-released`: the binding is already released.

#### Outputs: what the screen shows and produces

**Shown**

**Every device binding session** (data table, from `listDeviceBindingSession`)

| Shows | Format | Notes |
|---|---|---|
| User | text | User |
| Credential | text | Credential |
| Device id/reference | text | not in the schema: `Device ID/reference` |
| App installation | text | App installation |
| Os | text | OS |
| Registration date | 1 Oct 2026, 14:30 | Registration date |
| Last activation | 1 Oct 2026, 14:30 | Last activation |
| Last known venue | text | Last known venue |

**The selected device binding session** (detail panel): The pack groups this record's detail under its own headings: “Maximum Active Devices”, “Concurrent Sessions”, “Device Change”, “Credential active on Device A”, “Response”.

| Shows | Format | Notes |
|---|---|---|
| User | text | User |
| Credential | text | Credential |
| Device id/reference | text | not in the schema: `Device ID/reference` |
| App installation | text | App installation |
| Os | text | OS |
| Registration date | 1 Oct 2026, 14:30 | Registration date |
| Last activation | 1 Oct 2026, 14:30 | Last activation |
| Last known venue | text | Last known venue |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save device binding policy (primary button) | `setDeviceBindingPolicy` PUT `/device-binding-policy` | DeviceBindingPolicyInput | AccessCredentialPolicy | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | gated `ACCESS_POINT_CONFIGURE`; opens modal first |
| Release credential device (secondary button) | `releaseCredentialDevice` POST `/device-bindings/{bindingId}/release` | inline | AccessDeviceBinding | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `GUEST_MANAGE`; opens modal first |

**Data it reads**: `listDeviceBindingSession` (onLoad, Device Binding & Session Security)

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `listDeviceBindingSession`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The device binding session list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the device binding session untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No device binding session yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the device binding session are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `binding-released`: the binding is already released. |

#### Permissions

- `listDeviceBindingSession` → `SCOPE_VIEW` (read) · staff
- `setDeviceBindingPolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `releaseCredentialDevice` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Once activated in the app a digital ticket is bound to one approved device; moving to a new device requires deactivating the prior binding. Credential transfer moves a ticket to another person's device and invalidates the original holder's copy. *(client request · MoM 2 Sep 2026, 4.8 Device Binding, Credential Transfer & Revocation · DI-636)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-167` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-167`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 6: Works in Device Binding & Session Security → Prevent one credential from being shared across unauthorized devices. The source explicitly requires tickets to be linked to a specific device/user and suspicious patterns such as device sharing and …

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-167?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save device binding policy, Release credential device.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `GUEST_MANAGE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-168` BLE Beacon & Geofence Configuration

**Configure location-aware credential activation. This is a major requirement under 3.1.9. The matrix requires BLE beacon proximity and geofence boundaries to activate/deactivate credentials at venue, attraction, zone and gate level.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #20675 (APP-SETUP-BO-168) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Map-Based Configuration; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/ble-beacon-geofence-configuration-bo-168` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Beacon Name | select field | — | — | — | — | — | — |
| Beacon ID | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Zone | select field | — | — | — | — | — | — |
| Gate | select field | — | — | — | — | — | — |
| Proximity threshold | select field | — | — | — | — | — | — |
| Active/Inactive | select field | — | — | — | — | — | — |
| Health | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Venue (primary button) | navigation or local | — | — | — | — |
| Attraction (secondary button) | navigation or local | — | — | — | — |
| Zone (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `setBleBeaconGeofence`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ble beacon geofence configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ble beacon geofence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ble beacon geofence configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setBleBeaconGeofence` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Dynamic QR refreshes periodically to cut fraud/resale. Open: beacon-based (code hidden until the phone is near a gate beacon via Bluetooth, then refreshes ~every 2 minutes; Qossai: more secure) vs app-generated; GPS geofencing also raised. Chinmay to propose. *(open · MoM 2 Sep 2026, 4.6 Dynamic QR Code - Concept & Generation Approach · DI-630)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-168` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-168`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 8: Works in BLE Beacon & Geofence Configuration → Configure location-aware credential activation. This is a major requirement under 3.1.9. The matrix requires BLE beacon proximity and geofence boundaries to activate/deactivate credentials at venue …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-168?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Venue, Attraction, Zone.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-169` Credential Transfer & Rebinding

**Securely manage digital-ticket transfers. The matrix requires tickets to be transferable through email/app, with the recipient required to authenticate before accessing and activating the transferred QR.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `bindingId` (navigation) |
| Route | `/access-venue/credential-transfer-rebinding-bo-169` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Transfer allowed | select field | — | — | — | — | — | — |
| Number of transfers | select field | — | — | — | — | — | — |
| Transfer deadline | select field | — | — | — | — | — | — |
| Before first validation only | text field | — | — | — | — | — | — |
| Require recipient account | select field | — | — | — | — | — | — |
| Require OTP | select field | — | — | — | — | — | — |
| Require acceptance | select field | — | — | — | — | — | — |
| Cancel pending transfer | select field | — | — | — | — | — | — |
| Return to sender | select field | — | — | — | — | — | — |

**Form: Release credential device** (modal, opened by *Release credential device*; *Release credential device* calls `releaseCredentialDevice`, *Cancel* sends nothing)

**Collects what `releaseCredentialDevice` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `releaseCredentialDevice` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `binding-released`: the binding is already released.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Release credential device (primary button) | `releaseCredentialDevice` POST `/device-bindings/{bindingId}/release` | inline | AccessDeviceBinding | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `GUEST_MANAGE`; opens modal first |

**Data it reads**: `listCredentialTransferRebinding` (onLoad, Credential Transfer & Rebinding)

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `listCredentialTransferRebinding`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential transfer rebinding configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential transfer rebinding untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential transfer rebinding configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `binding-released`: the binding is already released. |

#### Permissions

- `listCredentialTransferRebinding` → `SCOPE_VIEW` (read) · staff
- `releaseCredentialDevice` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Once activated in the app a digital ticket is bound to one approved device; moving to a new device requires deactivating the prior binding. Credential transfer moves a ticket to another person's device and invalidates the original holder's copy. *(client request · MoM 2 Sep 2026, 4.8 Device Binding, Credential Transfer & Revocation · DI-636)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-169` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-169`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 10: Works in Credential Transfer & Rebinding → Securely manage digital-ticket transfers. The matrix requires tickets to be transferable through email/app, with the recipient required to authenticate before accessing and activating the transferred …

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-169?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Release credential device.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-170` Credential Revocation & Lifecycle Events

**Immediately invalidate credentials when the underlying ticket changes. Requirement 3.1.4 specifically requires dynamic QR invalidation after refunds, cancellations, transfers, exchanges, upgrades or reissues.**

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
| Route | `/access-venue/credential-revocation-lifecycle-events-bo-170` |

#### Inputs: what the user enters or picks

**Form: Save credential event propagation rule** (modal, opened by *Save credential event propagation rule*; *Save credential event propagation rule* calls `setCredentialEventPropagationRule`, *Cancel* sends nothing)

**Collects what `setCredentialEventPropagationRule` sends before it is called.** Required: `id`, `triggerEvent`, `scopePath`. Optional: `revocationAction`, `propagationTargets`, `monitoredConditions`, `propagation`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setCredentialEventPropagationRule` body |
| Trigger event `triggerEvent` | select | required | — | Entry · Exit · Redemption · Partial consumption · Cancellation · Refund · Suspension · Reactivation · Transfer · Exchange · Upgrade · Reissue … | — | Unique per scope; one vocabulary for both screens that read it (decided 29 September, writers pass) | `setCredentialEventPropagationRule` body |
| Revocation action `revocationAction` | segmented control | optional | — | Invalidate · Suspend · Replace | — | What happens to the credential; refund, exchange and reissue always revoke | `setCredentialEventPropagationRule` body |
| Propagation targets `propagationTargets` | multi-select chips | optional | — | Central platform · Mobile app · Gate network · Offline revocation package · Wallet credential service | — | — | `setCredentialEventPropagationRule` body |
| Monitored conditions `monitoredConditions` | multi-select chips | optional | — | Delayed updates · Conflicting states · Offline transactions pending synchronization · Provider update failures · Stale wallet credentials | — | — | `setCredentialEventPropagationRule` body |
| Propagation `propagation` | text area | optional | — | max length 500 | — | How the Virtual Ticket state change reaches every bound medium | `setCredentialEventPropagationRule` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setCredentialEventPropagationRule` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Every credential revocation lifecycle** (data table, from `listCredentialRevocationLifecycle`)

| Shows | Format | Notes |
|---|---|---|
| Propagation targets | list or chips (count when long) | — |

**The selected credential revocation lifecycle** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Propagation targets | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save credential event propagation rule (primary button) | `setCredentialEventPropagationRule` PUT `/credential-event-propagation-rules` | AccessCredentialEventPropagationRule | AccessCredentialEventPropagationRule | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | gated `ACCESS_POINT_CONFIGURE`; opens modal first; produces a document or message: Set how a ticket lifecycle event propagates to the credential |

**Data it reads**: `listCredentialRevocationLifecycle` (onLoad, Credential Revocation & Lifecycle Events)

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `listCredentialRevocationLifecycle`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential revocation lifecycle list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential revocation lifecycle untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential revocation lifecycle yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential revocation lifecycle are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listCredentialRevocationLifecycle` → `SCOPE_VIEW` (read) · staff
- `setCredentialEventPropagationRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-170` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-170`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 12: Works in Credential Revocation & Lifecycle Events → Immediately invalidate credentials when the underlying ticket changes. Requirement 3.1.4 specifically requires dynamic QR invalidation after refunds, cancellations, transfers, exchanges, upgrades or …

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-170?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save credential event propagation rule.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-171` Offline Cryptographic Validation Profile

**Allow access devices to validate secure credentials without continuous backend connectivity. The matrix explicitly requires offline cryptographic validation and embedded entitlement validation without real-time backend connectivity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`, `TENANT_CONFIGURE` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/offline-cryptographic-validation-profile-bo-171` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Form: Save offline policy** (modal, opened by *Save offline policy*; *Save offline policy* calls `setOfflinePolicy`, *Cancel* sends nothing)

**Collects what `setOfflinePolicy` sends before it is called.** Required: `scopePath`. Optional: `id`, `maxOfflineHours`, `allowedOffline`, `offlineValueCeiling`, `offlineTransactionCeiling`, `onCeilingBreach`, `requiresManagerToExtend`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope path `scopePath` | text field | required | — | pattern `^[a-z0-9_]+(\.[a-z0-9_]+)*$` | — | The node this policy is for, and the key `setOfflinePolicy` upserts on. The body names its target here, because the path does not. | `setOfflinePolicy` body |
| Max offline hours `maxOfflineHours` | stepper or slider (hours) | optional | 24 | min 1; max 72 | — | After which the workstation refuses to sell rather than keep journalling. A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody … | `setOfflinePolicy` body |
| Allowed offline `allowedOffline` | multi-select chips | optional | — | Sale · Refund · Exchange · Entitlement issue · Entitlement validate · Loyalty accrual · Loyalty redemption · Wallet spend · Price override · Discount · Void line · No sale; Selling from a cached catalogue is safe; issuing a refund is not, because the original … | — | What may happen with no network, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale cannot be verified. | `setOfflinePolicy` body |
| Offline value ceiling `offlineValueCeiling` | money field | optional | — | Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129). | AED, 2 decimals shown (up to 4 accepted), currency from the … | Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129). | `setOfflinePolicy` body |
| Offline transaction ceiling `offlineTransactionCeiling` | number field | optional | — | min 1; max 5000 | — | A ceiling on count as well as value. Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second. | `setOfflinePolicy` body |
| On ceiling breach `onCeilingBreach` | segmented control | optional | Block new sales | Warn · Block new sales · Block all | — | — | `setOfflinePolicy` body |
| Requires manager to extend `requiresManagerToExtend` | toggle | optional | on | — | — | — | `setOfflinePolicy` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save offline policy (primary button) | `setOfflinePolicy` PUT `/offline-policy` | OfflinePolicy | OfflinePolicy | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `TENANT_CONFIGURE`; opens modal first |

**Data it reads**: `listOfflineCryptographicValidation` (onLoad, Offline Cryptographic Validation Profile)

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `listOfflineCryptographicValidation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline cryptographic validation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline cryptographic validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline cryptographic validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offline cryptographic validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 The edge threshold is shorter than the central one. |

#### Permissions

- `setGateOfflinePolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `listOfflineCryptographicValidation` → `SCOPE_VIEW` (read) · staff
- `setOfflinePolicy` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Qossai: the dynamic QR must appear and work without internet, since crowded events (10,000+) suffer severe congestion; it must work offline via Bluetooth/beacon or an equivalent local mechanism. *(agreed · MoM 2 Sep 2026, 4.6 Hard requirement (offline) · DI-631)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-171` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-171`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 14: Works in Offline Cryptographic Validation Profile → Allow access devices to validate secure credentials without continuous backend connectivity. The matrix explicitly requires offline cryptographic validation and embedded entitlement validation …
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-171?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save offline policy.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-172` Embedded Entitlement Payload Designer

**Determine what operational information can be securely carried by the credential for offline decisions. The matrix permits embedded information including ticket type, seat assignment, event ID, venue access rights, timeslot, reservations, locker assignments, membership entitlements, guest category and validity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/embedded-entitlement-payload-designer-bo-172` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-164` Digital Credential Security Command Center: *Returns to the board's landing screen*; calls `setEmbeddedEntitlementPayload`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The embedded entitlement payload list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the embedded entitlement payload untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No embedded entitlement payload yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the embedded entitlement payload are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setEmbeddedEntitlementPayload` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-172` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-172`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 16: Works in Embedded Entitlement Payload Designer → Determine what operational information can be securely carried by the credential for offline decisions. The matrix permits embedded information including ticket type, seat assignment, event ID, venue …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-172?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-164`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-173` Credential Security Simulation, Audit & Publication

**Test the complete secure credential lifecycle before production deployment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AUDIT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-security-simulation-audit-publication-bo-173` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Virtual ticket | text field | — | — | `listCredentialSecurityOperational` ?virtualTicket |
| Action | text field | — | — | `listCredentialSecurityOperational` ?action |
| Actor | text field | — | — | `listCredentialSecurityOperational` ?actor |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every credential security simulation** (data table, from `listCredentialSecurity`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Credential | text | Credential |
| Ticket | text | Ticket |
| Guest account reference | text | Guest/account reference |
| Device | text | Device |
| Gate | text | Gate |
| Location | text | Location |
| Timestamp | 1 Oct 2026, 14:30 | Timestamp |
| Operator | text | Operator |
| Event type | chip: Activation, Refresh, Validation, Transfer, Revocation | — |
| Result reason code | text | result/reason code |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**The selected credential security simulation** (detail panel): The pack groups this record's detail under its own headings: “QR age”, “Every important event records”, “Center health”, “Board 3 workflow”, “There is a deliberate distinction”, “Media, Credential & Verification Methods”.

**Data it reads**: `listCredentialSecurity` (onLoad, Credential Security Simulation, Audit & Publication); `listCredentialSecurityOperational` (onLoad, Credential Security, Audit & Operational Evidence)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential security simulation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential security simulation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential security simulation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential security simulation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCredentialSecurity` → `AUDIT_VIEW` (read) · staff
- `listCredentialSecurityOperational` → `AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-173` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS20 Access Control Board 3.dc.html#bo-173`
- Workshop pack: Access Control Module_Reference.pdf board 3
- Flow F113 *Access Control board 3: Digital Credential Security Command Center*, step 18: Works in Credential Security Simulation, Audit & Publication → Test the complete secure credential lifecycle before production deployment.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-173?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `AUDIT_VIEW`.
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
"listCredentialActivationDisplay": {"method":"GET","path":"/credential-activation-display","contract":"access","summary":"Credential Activation & Display Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CredentialActivationDisplayRulesView"},
"listCredentialRevocationLifecycle": {"method":"GET","path":"/credential-revocation-lifecycle","contract":"access","summary":"Credential Revocation & Lifecycle Events","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CredentialRevocationLifecycleEventsView"},
"listCredentialSecurity": {"method":"GET","path":"/credential-security","contract":"access","summary":"Credential Security Simulation, Audit & Publication","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialSecurityOperational": {"method":"GET","path":"/credential-security-operational","contract":"access","summary":"Credential Security, Audit & Operational Evidence","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"virtualTicket","in":"query","required":false},{"name":"action","in":"query","required":false},{"name":"actor","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialTransferRebinding": {"method":"GET","path":"/credential-transfer-rebinding","contract":"access","summary":"Credential Transfer & Rebinding","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CredentialTransferRebindingView"},
"listDeviceBindingSession": {"method":"GET","path":"/device-binding-session","contract":"access","summary":"Device Binding & Session Security","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDigitalCredentialSecurity": {"method":"GET","path":"/digital-credential-security","contract":"access","summary":"Digital Credential Security Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOfflineCryptographicValidation": {"method":"GET","path":"/offline-cryptographic-validation","contract":"access","summary":"Offline Cryptographic Validation Profile","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OfflineCryptographicValidationProfileView"},
"releaseCredentialDevice": {"method":"POST","path":"/device-bindings/{bindingId}/release","contract":"access","summary":"Release a credential from a device","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessDeviceBinding"},
"setBleBeaconGeofence": {"method":"PUT","path":"/ble-beacon-geofence","contract":"access","summary":"BLE Beacon & Geofence Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BleBeaconGeofenceConfigurationInput","responds":"BleBeaconGeofenceConfigurationView"},
"setCredentialActivationDisplay": {"method":"PUT","path":"/credential-activation-display","contract":"access","summary":"Save a credential activation and display rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CredentialActivationDisplayRulesInput","responds":"CredentialActivationDisplayRulesView"},
"setCredentialEventPropagationRule": {"method":"PUT","path":"/credential-event-propagation-rules","contract":"access","summary":"Set how a ticket lifecycle event propagates to the credential","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessCredentialEventPropagationRule","responds":"AccessCredentialEventPropagationRule"},
"setDeviceBindingPolicy": {"method":"PUT","path":"/device-binding-policy","contract":"access","summary":"Set the device binding policy of a venue","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DeviceBindingPolicyInput","responds":"AccessCredentialPolicy"},
"setDynamicSecurityProfile": {"method":"PUT","path":"/dynamic-security-profile","contract":"access","summary":"Dynamic QR Security Profile Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DynamicQrSecurityProfileBuilderInput","responds":"DynamicQrSecurityProfileBuilderView"},
"setEmbeddedEntitlementPayload": {"method":"PUT","path":"/embedded-entitlement-payload","contract":"access","summary":"Embedded Entitlement Payload Designer","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EmbeddedEntitlementPayloadDesignerInput","responds":"EmbeddedEntitlementPayloadDesignerView"},
"setGateOfflinePolicy": {"method":"PUT","path":"/offline-policies","contract":"access","summary":"Set the offline policy of a venue","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessOfflinePolicy","responds":"AccessOfflinePolicy"},
"setOfflinePolicy": {"method":"PUT","path":"/offline-policy","contract":"tenancy","summary":"What a workstation may do with no network, and for how long","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OfflinePolicy","responds":"OfflinePolicy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessCredentialEventPropagationRule": {"type":"object","x-ticvai-persistence":"access.credential_event_propagation_rule","description":"For one ticket lifecycle event, the revocation action on the credential and how the change propagates to every bound medium, with the conditions monitored (declared 29 September, data-model close-out DM1).","required":["id","triggerEvent","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"triggerEvent":{"type":"string","enum":["entry","exit","redemption","partialConsumption","cancellation","refund","suspension","reactivation","transfer","exchange","upgrade","reissue","expiry","replacement","manualInvalidation","fraudLock","accountSuspension"],"description":"Unique per scope; one vocabulary for both screens that read it (decided 29 September, writers pass)"},"revocationAction":{"type":"string","nullable":true,"enum":["invalidate","suspend","replace"],"description":"What happens to the credential; refund, exchange and reissue always revoke"},"propagationTargets":{"type":"array","items":{"type":"string","enum":["centralPlatform","mobileApp","gateNetwork","offlineRevocationPackage","walletCredentialService"]}},"monitoredConditions":{"type":"array","items":{"type":"string","enum":["delayedUpdates","conflictingStates","offlineTransactionsPendingSynchronization","providerUpdateFailures","staleWalletCredentials"]}},"propagation":{"type":"string","maxLength":500,"nullable":true,"description":"How the Virtual Ticket state change reaches every bound medium"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessCredentialPolicy": {"type":"object","x-ticvai-persistence":"access.credential_policy","description":"One credential policy of one kind for a venue - activation and display rule, transfer policy, Virtual Ticket identity configuration or device binding policy; merges the proposed credential_display_rule, transfer_policy and virtual_ticket_config (declared 29 September, data-model close-out DM1). The deviceBinding row is written by setDeviceBindingPolicy (decided 29 September, writers pass).","required":["id","kind","scopePath"],"properties":{"id":{"type":"string","format":"uuid","description":"The ruleId (display rule) or policyId (transfer policy) of the operations"},"kind":{"type":"string","enum":["activationDisplay","transfer","virtualTicketIdentity","deviceBinding"],"description":"Which policy this row is; the columns of the other kinds stay null"},"name":{"type":"string","maxLength":200,"nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Required for activationDisplay and virtualTicketIdentity (one virtualTicketIdentity row per venue)"},"beforeActivationDisplay":{"type":"array","items":{"type":"string","enum":["hideQr","blurQr","showCountdown","showAvailableAtVenue","showVenueDirections"]},"description":"activationDisplay - what the guest sees before the credential activates"},"activeDisplay":{"type":"array","items":{"type":"string","enum":["dynamicQr","activationTimer","credentialStatus","remainingEntitlements"]},"description":"activationDisplay - what the guest sees once it is active"},"activationTriggers":{"type":"array","items":{"type":"string"},"description":"activationDisplay - what activates the credential, e.g. beacon proximity, geofence entry, time before admission"},"transferAllowed":{"type":"boolean","nullable":true,"description":"transfer"},"numberOfTransfers":{"type":"integer","minimum":0,"nullable":true,"description":"transfer"},"beforeFirstValidationOnly":{"type":"boolean","nullable":true,"description":"transfer"},"requireRecipientAccount":{"type":"boolean","nullable":true,"description":"transfer"},"requireOtp":{"type":"boolean","nullable":true,"description":"transfer"},"requireAcceptance":{"type":"boolean","nullable":true,"description":"transfer"},"returnToSender":{"type":"boolean","nullable":true,"description":"transfer"},"transferDeadlineHours":{"type":"integer","minimum":0,"nullable":true,"description":"transfer - hours before the visit after which transfer closes"},"cancelPendingAllowed":{"type":"boolean","nullable":true,"description":"transfer"},"transferAuditRequired":{"type":"boolean","nullable":true,"description":"transfer"},"idGenerationPattern":{"type":"string","nullable":true,"description":"virtualTicketIdentity - Virtual Ticket ID format: prefix, suffix and length"},"ticketClassification":{"type":"string","nullable":true,"description":"virtualTicketIdentity"},"ticketOwnershipModel":{"type":"string","nullable":true,"description":"virtualTicketIdentity"},"holderAssignmentRequirements":{"type":"string","nullable":true,"description":"virtualTicketIdentity"},"transferabilityReference":{"type":"string","nullable":true,"description":"virtualTicketIdentity"},"validityModel":{"type":"string","nullable":true,"description":"virtualTicketIdentity"},"consumptionModel":{"type":"string","nullable":true,"description":"virtualTicketIdentity"},"entitlementModel":{"type":"string","nullable":true,"description":"virtualTicketIdentity"},"mediaRequirements":{"type":"array","items":{"type":"string"},"description":"virtualTicketIdentity - media types a ticket of this configuration must carry"},"maximumActiveDevices":{"type":"integer","minimum":1,"nullable":true,"description":"deviceBinding"},"concurrentSessions":{"type":"integer","minimum":1,"nullable":true,"description":"deviceBinding"},"deviceChangePolicy":{"type":"string","nullable":true,"enum":["notAllowed","allowedBeforeFirstUse","otpVerificationRequired","operatorApprovalRequired","supervisorApprovalRequired"],"description":"deviceBinding"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessDeviceBinding": {"type":"object","x-ticvai-persistence":"access.device_binding","description":"One guest device bound to a credential, with its registration, last activation and security status; the binding policy in force is a deviceBinding row of access.credential_policy (declared 29 September, data-model close-out DM1). Written by bindCredentialDevice (the guest app) and releaseCredentialDevice; securityStatus is set by the sharing detection job (decided 29 September, writers pass).","required":["id","entitlementId","deviceId","registeredAt","securityStatus","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest (pii.subject)"},"entitlementId":{"type":"string","format":"uuid"},"credentialBindingId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","maxLength":200},"deviceReference":{"type":"string","maxLength":200,"nullable":true},"appInstallationId":{"type":"string","maxLength":200,"nullable":true},"os":{"type":"string","maxLength":50,"nullable":true},"registeredAt":{"type":"string","format":"date-time"},"lastActivatedAt":{"type":"string","format":"date-time","nullable":true},"lastKnownVenueId":{"type":"string","format":"uuid","nullable":true},"securityStatus":{"type":"string","enum":["normal","suspicious","blocked"],"default":"normal"},"deactivatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Set when the binding is removed (deactivation, or a transfer of the credential)"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessOfflinePolicy": {"type":"object","x-ticvai-persistence":"access.offline_policy","description":"The offline policy of one venue: what gates validate locally and for how long, how old the revocation cache may get, and how devices step down through degraded modes. Merges access.offline_validation_profile, access.revocation_cache_policy and access.degraded_mode_policy (declared 29 September, data-model close-out DM1)","required":["id","venueId","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"maxOfflineDurationHours":{"type":"integer","minimum":0,"nullable":true,"description":"Hours a gate may validate offline"},"offlineChecks":{"type":"array","items":{"type":"string","enum":["credentialAuthenticity","digitalSignature","ticketId","venue","park","zone","visitDate","timeWindow","credentialStatusSnapshot","ticketType","guestCategory","seat","timeslot","reservation","entitlements","reEntryPermissions","validityPeriod"]},"description":"What a gate may validate locally"},"afterThresholdBehavior":{"type":"string","enum":["continueRestrictedValidation","operatorWarning","supervisorMode","failClosed","fallback"],"nullable":true},"revocationTriggerEvents":{"type":"array","items":{"type":"string","enum":["fraudLock","refund","cancellation","lostCredential","transfer","reissue","manualInvalidation"]},"description":"Events that push an invalidation into the offline cache"},"revocationMaxAllowedAgeMinutes":{"type":"integer","minimum":0,"nullable":true,"description":"Maximum allowed revocation cache age"},"revocationStalenessAction":{"type":"string","enum":["continue","continueWithWarning","restrictedProductsOnly","supervisorMode","denySelectedCredentialClasses","failClosed"],"nullable":true,"description":"What devices do when the cache is older than the maximum allowed age"},"operatingModes":{"type":"array","items":{"type":"string","enum":["online","degraded","edgeMode","localOffline","unsafeExpired"]},"description":"Operating modes a device moves through as connectivity fails"},"centralUnavailableAfterSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"Seconds without central services before switching to edge mode"},"edgeUnavailableAfterSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"Seconds without the venue edge before switching to local offline"},"automaticSwitch":{"type":"boolean","default":true,"description":"Switch modes automatically without stopping guest flow"},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"BleBeaconGeofenceConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What BLE Beacon & Geofence Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"beaconName":{"type":"string","description":"Beacon Name"},"beaconId":{"type":"string","description":"Beacon ID"},"venue":{"type":"string","description":"Venue"},"zone":{"type":"string","description":"Zone"},"gate":{"type":"string","description":"Gate"},"proximityThreshold":{"type":"integer","description":"Metres"},"activeInactive":{"type":"string","enum":["active","inactive"],"description":"Active/Inactive"},"health":{"type":"string","enum":["healthy","degraded","offline"],"description":"Read-only, reported by the beacon"},"lastDetected":{"type":"string","format":"date-time","description":"Last detected"},"park":{"type":"string","description":"Park"},"attraction":{"type":"string","description":"Attraction"},"geofenceRadiusMeters":{"type":"integer","description":"Radius of a circular activation zone"},"geofenceBoundary":{"type":"array","items":{"type":"string"},"description":"Polygon points as lat,lng when the zone is drawn"}},"required":["beaconId","venue"]},
"BleBeaconGeofenceConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What BLE Beacon & Geofence Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"beaconName":{"type":"string","description":"Beacon Name"},"beaconId":{"type":"string","description":"Beacon ID"},"venue":{"type":"string","description":"Venue"},"zone":{"type":"string","description":"Zone"},"gate":{"type":"string","description":"Gate"},"proximityThreshold":{"type":"integer","description":"Metres"},"activeInactive":{"type":"string","enum":["active","inactive"],"description":"Active/Inactive"},"health":{"type":"string","enum":["healthy","degraded","offline"],"description":"Read-only, reported by the beacon"},"lastDetected":{"type":"string","format":"date-time","description":"Last detected"},"park":{"type":"string","description":"Park"},"attraction":{"type":"string","description":"Attraction"},"geofenceRadiusMeters":{"type":"integer","description":"Radius of a circular activation zone"},"geofenceBoundary":{"type":"array","items":{"type":"string"},"description":"Polygon points as lat,lng when the zone is drawn"}},"required":["beaconId","venue"]},
"CredentialActivationDisplayRulesInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Credential Activation & Display Rules submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["venueId","name","beforeActivationDisplay","activeDisplay","activationTriggers"],"properties":{"ruleId":{"type":"string","format":"uuid","description":"Absent creates a rule"},"venueId":{"type":"string","description":"Venue the rule applies to"},"name":{"type":"string","maxLength":200},"beforeActivationDisplay":{"type":"array","items":{"type":"string","enum":["hideQr","blurQr","showCountdown","showAvailableAtVenue","showVenueDirections"]},"description":"What the guest sees before the credential activates"},"activeDisplay":{"type":"array","items":{"type":"string","enum":["dynamicQr","activationTimer","credentialStatus","remainingEntitlements"]},"description":"What the guest sees once it is active"},"activationTriggers":{"type":"array","items":{"type":"string"},"minItems":1,"description":"What activates the credential, e.g. beacon proximity, geofence entry, time before admission"}}},
"CredentialActivationDisplayRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Activation & Display Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"beforeActivationDisplay":{"type":"array","items":{"type":"string","enum":["hideQr","blurQr","showCountdown","showAvailableAtVenue","showVenueDirections"]}},"activeDisplay":{"type":"array","items":{"type":"string","enum":["dynamicQr","activationTimer","credentialStatus","remainingEntitlements"]}},"name":{"type":"string"},"activationTriggers":{"type":"array","items":{"type":"string"},"description":"Conditions that make the credential eligible, e.g. beaconProximity, geofence, timeWindow"}},"required":["ruleId"]},
"CredentialRevocationLifecycleEventsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Revocation & Lifecycle Events displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"revocationAction":{"type":"string","enum":["invalidate","suspend","replace"],"description":"What happens to the credential on the event"},"triggerEvent":{"type":"string","enum":["refund","cancellation","transfer","exchange","upgrade","reissue","expiry","manualInvalidation","fraudLock","accountSuspension"],"description":"Ticket event, in the access.credential_event_propagation_rule vocabulary (ticketExpiration is expiry) (decided 29 September, writers pass)"},"propagationTargets":{"type":"array","items":{"type":"string","enum":["centralPlatform","mobileApp","gateNetwork","offlineRevocationPackage","walletCredentialService"]}}},"required":["triggerEvent","revocationAction"]},
"CredentialSecurityAuditOperationalEvidenceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Security, Audit & Operational Evidence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicket":{"type":"string","description":"Virtual Ticket"},"credential":{"type":"string","description":"Credential"},"media":{"type":"string","description":"Media"},"action":{"type":"string","enum":["credentialRequested","generated","bound","delivered","activated","updated","presented","suspended","reactivated","replaced","revoked","expired","rebound","regenerated","deleted"],"description":"Lifecycle action recorded"},"before":{"type":"string","description":"Before"},"after":{"type":"string","description":"After"},"actor":{"type":"string","description":"Actor"},"source":{"type":"string","description":"Source"},"device":{"type":"string","description":"Device"},"dateTime":{"type":"string","format":"date-time","description":"Date/time"},"reason":{"type":"string","description":"Reason"},"approval":{"type":"string","description":"Approval"},"providerReference":{"type":"string","description":"Provider reference"},"relatedTransaction":{"type":"string","description":"Related transaction"},"anomalyFlags":{"type":"array","items":{"type":"string","enum":["excessiveRegeneration","repeatedReplacement","suspiciousRebinding","multipleCredentialAssignments","unexpectedProviderTokenChanges","unauthorizedAdministrativeActions"]},"description":"Suspicious patterns flagged on this entry"}}},
"CredentialSecuritySimulationAuditPublicationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Security Simulation, Audit & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"credential":{"type":"string","description":"Credential"},"ticket":{"type":"string","description":"Ticket"},"guestAccountReference":{"type":"string","description":"Guest/account reference"},"device":{"type":"string","description":"Device"},"gate":{"type":"string","description":"Gate"},"location":{"type":"string","description":"Location"},"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"operator":{"type":"string","description":"Operator"},"eventType":{"type":"string","enum":["activation","refresh","validation","transfer","revocation"]},"resultReasonCode":{"type":"string","description":"result/reason code"}}},
"CredentialTransferRebindingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Transfer & Rebinding displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"transferAllowed":{"type":"boolean"},"policyId":{"type":"string"},"numberOfTransfers":{"type":"integer","description":"Number of transfers"},"beforeFirstValidationOnly":{"type":"boolean","description":"Before first validation only"},"requireRecipientAccount":{"type":"boolean","description":"Require recipient account"},"requireOtp":{"type":"boolean","description":"Require OTP"},"requireAcceptance":{"type":"boolean","description":"Require acceptance"},"returnToSender":{"type":"boolean","description":"Return to sender"},"name":{"type":"string"},"transferDeadlineHours":{"type":"integer","description":"Hours before the visit after which transfer closes"},"cancelPendingAllowed":{"type":"boolean"},"transferAuditRequired":{"type":"boolean"}},"required":["policyId","transferAllowed"]},
"DeviceBindingPolicyInput": {"type":"object","x-ticvai-persistence":"none — request only; written as the deviceBinding row of access.credential_policy (declared 29 September, writers pass)","required":["venueId"],"properties":{"venueId":{"type":"string","format":"uuid"},"maximumActiveDevices":{"type":"integer","minimum":1,"default":1,"description":"Devices the credential may be active on at once"},"concurrentSessions":{"type":"integer","minimum":1,"default":1},"deviceChangePolicy":{"type":"string","enum":["notAllowed","allowedBeforeFirstUse","otpVerificationRequired","operatorApprovalRequired","supervisorApprovalRequired"],"default":"otpVerificationRequired"}}},
"DeviceBindingSessionSecurityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Device Binding & Session Security displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"user":{"type":"string","description":"User"},"credential":{"type":"string","description":"Credential"},"deviceId":{"type":"string","description":"Device ID"},"deviceReference":{"type":"string","description":"Device reference"},"appInstallation":{"type":"string","description":"App installation"},"os":{"type":"string","description":"OS"},"registrationDate":{"type":"string","format":"date-time","description":"Registration date"},"lastActivation":{"type":"string","format":"date-time","description":"Last activation"},"lastKnownVenue":{"type":"string","description":"Last known venue"},"securityStatus":{"type":"string","enum":["normal","suspicious","blocked"],"description":"Security status"}}},
"DeviceBindingSessionSecurityViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"maximumActiveDevices":{"type":"integer","description":"Maximum Active Devices (the pack shows 1)"},"concurrentSessions":{"type":"integer","description":"Concurrent Sessions (the pack shows 1)"},"deviceChangePolicy":{"type":"string","enum":["notAllowed","allowedBeforeFirstUse","otpVerificationRequired","operatorApprovalRequired","supervisorApprovalRequired"]}}},
"DigitalCredentialSecurityCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Digital Credential Security Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"credentialType":{"type":"string","enum":["dynamicQrTicket","membership","annualPass","mobileWallet","loyalty","digitalPass","event"]},"profileId":{"type":"string"},"profileName":{"type":"string","description":"Credential profile, e.g. Day Ticket"},"dynamic":{"type":"boolean"},"deviceBound":{"type":"string","enum":["required","optional","off"]},"locationScope":{"type":"string","description":"gate, venue, event or none"},"offlineReady":{"type":"boolean"},"securityLevel":{"type":"string","enum":["strong","standard"]}}},
"DigitalCredentialSecurityCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"activeDigitalCredentials":{"type":"integer","description":"Active Digital Credentials"},"dynamicQrEnabled":{"type":"integer","description":"Credentials with dynamic QR enabled"},"deviceBoundCredentials":{"type":"integer","description":"Device-Bound Credentials"},"locationProtectedCredentials":{"type":"integer","description":"Location-Protected Credentials"},"offlineReadyCredentials":{"type":"integer","description":"Offline-Ready Credentials"},"credentialsRevokedToday":{"type":"integer","description":"Credentials Revoked Today"},"transferEvents":{"type":"integer"},"securityAlerts":{"type":"integer","description":"Security Alerts"},"suspiciousSessions":{"type":"integer","description":"Suspicious Sessions"}}},
"DynamicQrSecurityProfileBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is access.scan_event at 7%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Dynamic QR Security Profile Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"name":{"type":"string"},"profileId":{"type":"string","maxLength":64,"description":"The credential security profile's code (access.credential_security_profile.code) (decided 29 September, writers pass)"},"qrMode":{"type":"string","enum":["static","dynamic","dynamicDeviceBound","dynamicLocationBound","dynamicDeviceLocationBound"]},"payloadComponents":{"type":"array","items":{"type":"string","enum":["credentialId","ticketId","timestamp","nonceOtp","deviceBindingReference","venueContext","entitlementPayload","signatureKeyReference"]},"description":"What the QR payload carries"},"venueId":{"type":"string"},"refreshIntervalSeconds":{"type":"integer","description":"QR rotation interval, e.g. 15, 30, 45, 60 or custom"}},"required":["profileId","name","qrMode"]},
"DynamicQrSecurityProfileBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Dynamic QR Security Profile Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string"},"profileId":{"type":"string"},"qrMode":{"type":"string","enum":["static","dynamic","dynamicDeviceBound","dynamicLocationBound","dynamicDeviceLocationBound"]},"payloadComponents":{"type":"array","items":{"type":"string","enum":["credentialId","ticketId","timestamp","nonceOtp","deviceBindingReference","venueContext","entitlementPayload","signatureKeyReference"]},"description":"What the QR payload carries"},"venueId":{"type":"string"},"refreshIntervalSeconds":{"type":"integer","description":"QR rotation interval, e.g. 15, 30, 45, 60 or custom"}},"required":["profileId","name","qrMode"]},
"EmbeddedEntitlementPayloadDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Embedded Entitlement Payload Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"profileId":{"type":"string","description":"The credential security profile's code (access.credential_security_profile.code) (decided 29 September, writers pass)","maxLength":64},"embeddedClaims":{"type":"array","items":{"type":"string","enum":["credentialId","ticketType","guestCategory","venue","park","zone","attractionPermissions","date","time","timeslot","expiry","admission","fastPass","membership","reservation","locker","seat","otherOperationalClaims"]},"description":"Claims carried in the credential for offline decisions"},"name":{"type":"string"}},"required":["profileId","embeddedClaims"]},
"EmbeddedEntitlementPayloadDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Embedded Entitlement Payload Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"profileId":{"type":"string","description":"Credential security profile the payload belongs to"},"embeddedClaims":{"type":"array","items":{"type":"string","enum":["credentialId","ticketType","guestCategory","venue","park","zone","attractionPermissions","date","time","timeslot","expiry","admission","fastPass","membership","reservation","locker","seat","otherOperationalClaims"]},"description":"Claims carried in the credential for offline decisions"},"name":{"type":"string"}},"required":["profileId","embeddedClaims"]},
"OfflineCryptographicValidationProfileView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Offline Cryptographic Validation Profile displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maxOfflineDurationHours":{"type":"integer","description":"e.g. 8"},"offlineChecks":{"type":"array","items":{"type":"string","enum":["credentialAuthenticity","digitalSignature","ticketId","venue","park","zone","visitDate","timeWindow","credentialStatusSnapshot","ticketType","guestCategory","seat","timeslot","reservation","entitlements","reEntryPermissions","validityPeriod"]},"description":"What a gate may validate locally"},"afterThresholdBehavior":{"type":"string","enum":["continueRestrictedValidation","operatorWarning","supervisorMode","failClosed","fallback"]}},"required":["offlineChecks","maxOfflineDurationHours","afterThresholdBehavior"]},
"OfflinePolicy": {"type":"object","x-ticvai-persistence":"platform.offline_policy","description":"Board 5 of the client's POS set. **ADR-0013 makes the POS local-first and nothing configured the policy** — one of only two things in 36 board screens the package genuinely could not do.\nCF-115 reframed offline into three data classes: catalogue and policy always local, contended inventory leased, transactional facts journalled. **This is where a venue says how far that goes for them.**\n**One per scope node, keyed on `scopePath`** (pull audit R162). `id` is server-owned and absent where `getOfflinePolicy` returns the defaults for a node with nothing saved.\n**The `minimum` and `maximum` on each field are proposed, client to correct (decided 28 September, audit R129).** A value outside them is refused `400`, `errors[]` naming the field.\n","required":["scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$","description":"**The node this policy is for, and the key `setOfflinePolicy` upserts on.** The body names its target here, because the path does not.\n"},"maxOfflineHours":{"type":"integer","default":24,"minimum":1,"maximum":72,"description":"**After which the workstation refuses to sell rather than keep journalling.** A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody can detect. Bounds 1 to 72 hours: proposed, client to correct (audit R129).\n"},"allowedOffline":{"type":"array","description":"**What may happen with no network**, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale cannot be verified.\n","items":{"type":"string","enum":["sale","refund","exchange","entitlementIssue","entitlementValidate","loyaltyAccrual","loyaltyRedemption","walletSpend","priceOverride","discount","voidLine","noSale"]}},"offlineValueCeiling":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129).\n"},"offlineTransactionCeiling":{"type":"integer","nullable":true,"minimum":1,"maximum":5000,"description":"**A ceiling on count as well as value.** Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second. Bounds 1 to 5,000: proposed, client to correct (audit R129).\n"},"onCeilingBreach":{"type":"string","enum":["warn","blockNewSales","blockAll"],"default":"blockNewSales"},"requiresManagerToExtend":{"type":"boolean","default":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
