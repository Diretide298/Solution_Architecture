# WS18 — Approval Workflows and Governance board 6

**10 screens · 16 operations · 16 schemas · 6 permissions**

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
  `APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_VIEW, ROLE_MANAGE, TENANT_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
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
| `ADM-339` | Governance & Compliance Command Center | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-340` | Segregation of Duties Policy Manager | B–D | 1 | 0 | 5 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-341` | Four-Eyes & Dual-Control Policy | B–D | 7 | 0 | 5 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-342` | Authentication & MFA Policy Manager | A | 16 | 0 | 6 | 11 | 2 | 0 | — | notStarted (—) |
| `ADM-343` | Sensitive Action Confirmation | B–D | 6 | 0 | 5 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-344` | Digital Signature Management | B–D | 7 | 0 | 5 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-345` | Immutable Approval Record & Tamper Detection | B–D | 0 | 18 | 6 | 0 | 0 | 3 | — | notStarted (—) |
| `ADM-346` | Approval Record Retention Policy | B–D | 8 | 0 | 5 | 2 | 1 | 3 | — | notStarted (—) |
| `ADM-347` | Regulatory Audit & Evidence Center | B–D | 2 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-348` | Governance Risk & AI Compliance Advisor | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-340, ADM-345, ADM-347, ADM-348 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-339` Governance & Compliance Command Center

**Provide administrators, auditors and security teams with an overview of approval governance health across the organization.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/governance-compliance-command-center-adm-339` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApprovalAnalytics` ?from |
| Group by | radio group | — | Kind · Approver · Venue · Day · Week | `getApprovalAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Governance Compliance %** (metric tile)

**SoD Conflicts** (metric tile)

**Four-Eyes Protected Actions** (metric tile)

**MFA-Protected Approvals** (metric tile)

**Digital Signatures** (metric tile)

**Tamper Alerts** (metric tile)

**Retention Exceptions** (metric tile)

**Audit Findings** (metric tile)

**Data it reads**: `listApprovalControlPolicies` (onLoad, Controls in force); `getApprovalAnalytics` (onLoad, Governance posture)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-348` Governance Risk & AI Compliance Advisor: *Governance Risk & AI Compliance Advisor*
- → `ADM-340` Segregation of Duties Policy Manager: *Segregation of Duties Policy Manager*
- → `ADM-341` Four-Eyes & Dual-Control Policy: *Four-Eyes & Dual-Control Policy*
- → `ADM-342` Authentication & MFA Policy Manager: *Authentication & MFA Policy Manager*
- → `ADM-343` Sensitive Action Confirmation: *Sensitive Action Confirmation*
- → `ADM-344` Digital Signature Management: *Digital Signature Management*
- → `ADM-345` Immutable Approval Record & Tamper Detection: *Immutable Approval Record & Tamper Detection*
- → `ADM-346` Approval Record Retention Policy: *Approval Record Retention Policy*
- → `ADM-347` Regulatory Audit & Evidence Center: *Regulatory Audit & Evidence Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance compliance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance compliance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance compliance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance compliance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listApprovalControlPolicies` → `APPROVAL_VIEW` (read) · staff
- `getApprovalAnalytics` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Governance board manages segregation of duties, MFA policy, digital signature where applicable, data retention and audit trail, and shows identified compliance risks. *(client request · MoM 8 Sep 2026, 4.17 Governance, Security, Compliance & Audit · DI-732)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-339` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-339`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 6
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 1: Opens Governance & Compliance Command Center → Provide administrators, auditors and security teams with an overview of approval governance health across the organization.
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F128 branch at step 1 (expected): when Nothing has been set up on Governance & Compliance Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F128 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-339?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-348`, `ADM-340`, `ADM-341`, `ADM-342`, `ADM-343`, `ADM-344`, `ADM-345`, `ADM-346`, `ADM-347`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-340` Segregation of Duties Policy Manager

**Define combinations of actions that the same person must not be allowed to perform. The matrix explicitly states that users shall be prevented from approving their own requests.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ROLE_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Price Configuration User) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/segregation-of-duties-policy-manager-adm-340` |

**Known gaps.** **Segregation of Duties Policy Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| =R | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save segregation rules (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-339` Governance & Compliance Command Center: *Back to Governance & Compliance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The segregation duties policy configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the segregation duties policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No segregation duties policy configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setSegregationRules` → `ROLE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Governance board manages segregation of duties, MFA policy, digital signature where applicable, data retention and audit trail, and shows identified compliance risks. *(client request · MoM 8 Sep 2026, 4.17 Governance, Security, Compliance & Audit · DI-732)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-340` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-340`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 6
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 2: Works in Segregation of Duties Policy Manager → Define combinations of actions that the same person must not be allowed to perform. The matrix explicitly states that users shall be prevented from approving their own requests.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-340?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save segregation rules, Cancel.
- [ ] Every transition is wired: `ADM-339`.
- [ ] Every gated control is gated: `ROLE_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-341` Four-Eyes & Dual-Control Policy

**Configure sensitive actions requiring approval from at least two independent authorized persons. The source explicitly requires dual approval capability for sensitive operations.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_CONFIGURE`, `APPROVAL_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators should configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/four-eyes-dual-control-policy-adm-341` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Two different users required | text field | — | — | — | — | — | — |
| Different roles required | select field | — | — | — | — | — | — |
| Different departments if required | text field | — | — | — | — | — | — |
| No delegated duplicate identity | text field | — | — | — | — | — | — |
| Minimum authority level | select field | — | — | — | — | — | — |
| Sequential or parallel approval | text field | — | — | — | — | — | — |
| Both approvals mandatory | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listApprovalControlPolicies` (onLoad, What is already required)

**Where the user goes next**

- → `ADM-339` Governance & Compliance Command Center: *Back to Governance & Compliance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The four-eyes dual- policy configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the four-eyes dual- policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No four-eyes dual- policy configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setApprovalControlPolicy` → `APPROVAL_CONFIGURE` (configure) · staff
- `listApprovalControlPolicies` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-341` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-341`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 6
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 4: Works in Four-Eyes & Dual-Control Policy → Configure sensitive actions requiring approval from at least two independent authorized persons. The source explicitly requires dual approval capability for sensitive operations.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-341?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-339`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-342` Authentication & MFA Policy Manager

**Define the authentication strength required before an approver can execute sensitive approval decisions. The source requires authentication before approval actions and supports MFA for sensitive approvals.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block A · ticket #20614 (APP-SETUP-ADM-342) |
| Who uses it | ticvai staff holding `APPROVAL_CONFIGURE`, `TENANT_CONFIGURE` (2 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/authentication-mfa-policy-manager-adm-342` |

**Known gaps.** **`setPasswordPolicy` replaces the whole policy and nothing reads it.** identity has no `getPasswordPolicy`, so this screen cannot show the tenant's current `mfaRequiredForPermissions` (or the rest … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Permissions that require MFA | multi select | — | — | — | — | **MFA is required by permission (decided 28 September, audit R135).** A principal holding any permission listed here must present a second factor at sign-in and keep an active method. The floor — … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Effective | toggle | off | — | `listStepUpPolicies` ?effective |

**Sent by *Save MFA requirement*** (`setPasswordPolicy`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Min length `minLength` | number field | required | 12 | min 8 | — | A tenant may raise the length and never set it below 8 (decided 28 September, audit R126 (7)). | `setPasswordPolicy` body |
| Require breach check `requireBreachCheck` | toggle | optional | on | — | — | The single most effective rule. Refusing a password known to be breached stops more account takeovers than every composition rule combined. | `setPasswordPolicy` body |
| Max age days `maxAgeDays` | number field (days) | optional | — | — | — | Null is the recommended value. Forced rotation produces `Summer2026!` becoming `Summer2027!`, and it is offered because some tenants are contractually obliged to have it rather … | `setPasswordPolicy` body |
| Recovery methods `recoveryMethods` | multi-select chips | optional | — | Email · SMS · Security questions · In person verification · Support assisted | — | BL-132. A guest locked out had no path back — lockout existed and recovery did not, which turns a forgotten password into a support call. | `setPasswordPolicy` body |
| Max concurrent sessions `maxConcurrentSessions` | number field | optional | — | — | — | BL-145. Null, and that is the decision. | `setPasswordPolicy` body |
| Device restriction `deviceRestriction` | group | optional | — | — | — | BL-146. Device, browser, IP and location restriction on access. | `setPasswordPolicy` body |
| Allowed ip ranges `deviceRestriction.allowedIpRanges` | list of values (chips) | optional | — | — | — | — | `setPasswordPolicy` body |
| Allowed countries `deviceRestriction.allowedCountries` | list of values (chips) | optional | — | — | — | — | `setPasswordPolicy` body |
| Require registered device `deviceRestriction.requireRegisteredDevice` | toggle | optional | off | — | — | — | `setPasswordPolicy` body |
| On violation `deviceRestriction.onViolation` | segmented control | optional | Require step up | Warn · Require step up · Block | — | — | `setPasswordPolicy` body |
| Lockout after attempts `lockoutAfterAttempts` | number field | optional | 10 | — | — | — | `setPasswordPolicy` body |
| Lockout minutes `lockoutMinutes` | number field (minutes) | optional | 15 | — | — | A temporary lockout, not a permanent one. Permanent lockout on failed attempts is a denial-of-service anybody can run against a known username. | `setPasswordPolicy` body |
| Force change on first logon `forceChangeOnFirstLogon` | toggle | optional | on | — | — | — | `setPasswordPolicy` body |
| Reuse prevention count `reusePreventionCount` | stepper or slider | optional | 5 | min 0; max 24 | — | How many previous credentials a staff member may not reuse — the last 5 unless the tenant sets another (decided 28 September, audit R132). | `setPasswordPolicy` body |
| MFA required for permissions `mfaRequiredForPermissions` | multi-select chips | optional | ROLE MANAGE, LEDGER APPROVE, PLATFORM TENANT VIEW, PLATFORM TENANT MANAGE, PLATFORM TENANT TERMINATE, PLATFORM TENANT ACCESS, PLATFORM PLAN MANAGE, PLATFORM CELL VIEW, PLATFORM CELL MANAGE, PLATFORM BILLING VIEW, PLATFORM BILLING MANAGE, PLATFORM RELEASE VIEW, PLATFORM RELEASE MANAGE, PLATFORM RELEASE PROMOTE, PLATFORM MIGRATION VIEW, PLATFORM MIGRATION APPLY | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; A … | — | Step-up rather than blanket MFA. Requiring it for a refund approval and not for reading a rota is what stops people sharing devices to avoid it. | `setPasswordPolicy` body |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Save MFA requirement (primary button) | `setPasswordPolicy` PUT `/password-policy` | PasswordPolicy | PasswordPolicy | — | — |

**Data it reads**: `listStepUpPolicies` (onLoad, Every action that can demand a second factor, its contract …); `listMfaMethods` (onLoad, Which methods approvers have enrolled, because a policy …); `getGuestVerificationPolicy` (onLoad, The tenant's guest identity-verification workflow)

**Where the user goes next**

- → `ADM-339` Governance & Compliance Command Center: *Back to Governance & Compliance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The authentication mfa policy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the authentication mfa policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No authentication mfa policy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the authentication mfa policy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `required` is below the floor the operation's own `x-ticvai-step-up` sets. `refusedReason` is `belowContractFloor`, and `contractFloor` carries the lowest … (StepUpPolicyRefusedProblem) |

#### Permissions

- `listStepUpPolicies` → `APPROVAL_CONFIGURE` (configure) · staff
- `setStepUpPolicy` → `APPROVAL_CONFIGURE` (configure) · staff
- `setPasswordPolicy` → `TENANT_CONFIGURE` (configure) · staff
- `listMfaMethods` → no permission · staff, partner, guest
- `getGuestVerificationPolicy` → `TENANT_CONFIGURE` (configure) · staff
- `setGuestVerificationPolicy` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.3.8 | The system should allow guest to change his/her password. The system must include a forgotten password module. | F&B & Guest Management | CONTRACTED | data `PasswordPolicy` |
| 5.3.31 | Provide password reset, username recovery, OTP authentication, account unlocking, and profile recovery workflows. | F&B & Guest Management | CONTRACTED | data `PasswordPolicy` |
| 7.1.7 | The system should not be able to attempt logon to Back Office/POS with incorrect password. | F&B POS | CONTRACTED | data `PasswordPolicy` |
| 7.1.8 | The system should be able to set user to require new password at logon, Logon to Back Office/POS and change password. | F&B POS | CONTRACTED | data `PasswordPolicy` |
| 7.1.9 | The system should be able to ensure user can log off and log back in again multiple times without any limitations. | F&B POS | CONTRACTED | data `PasswordPolicy` |
| 7.1.10 | The system should allow configuration the number of concurrent logins to multiple terminals with the same user at the same time. | F&B POS | CONTRACTED | data `PasswordPolicy` |
| 7.1.18 | The system shall support configurable password policies including minimum length, complexity, expiry, password history, reset requirements, and lockout rules. | F&B POS | CONTRACTED | data `PasswordPolicy` |
| 7.1.19 | The system shall automatically lock accounts after a configurable number of failed login attempts and allow authorized administrators to unlock accounts. | F&B POS | CONTRACTED | data `PasswordPolicy` |
| 7.1.21 | The system shall support restricting user access based on registered devices, device type, browser, IP address, network range, country, location, or assigned POS terminal. | F&B POS | CONTRACTED | data `PasswordPolicy` |
| 7.1.26 | The system shall manage user statuses including Active, Inactive, Suspended, Locked, Disabled, Deleted, and Pending Approval. | F&B POS | CONTRACTED | data `PasswordPolicy` |
| 7.1.39 | Evaluate contextual information such as user role, department, venue assignment, membership status, device type, location, operational status and risk level before granting access. | F&B POS | CONTRACTED | data `PasswordPolicy` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Governance board manages segregation of duties, MFA policy, digital signature where applicable, data retention and audit trail, and shows identified compliance risks. *(client request · MoM 8 Sep 2026, 4.17 Governance, Security, Compliance & Audit · DI-732)*
- MFA / additional confirmation for sensitive approval actions is a business-configurable option (on or off), not mandatory, but the screens must support it when enabled. *(agreed · MoM 8 Sep 2026, 4.15 Execution & Decision Management · DI-729)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-342` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-342`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 6
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 6: Works in Authentication & MFA Policy Manager → Define the authentication strength required before an approver can execute sensitive approval decisions. The source requires authentication before approval actions and supports MFA for sensitive …
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-342?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel, Save MFA requirement.
- [ ] Every transition is wired: `ADM-339`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `TENANT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-343` Sensitive Action Confirmation

**Configure the final confirmation requirements before a sensitive approval becomes binding. The source specifically requires confirmation before execution of sensitive approvals.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/sensitive-action-confirmation-adm-343` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Action | select field | — | — | — | — | — | — |
| Amount | select field | — | — | — | — | — | — |
| Risk | select field | — | — | — | — | — | — |
| department | select field | — | — | — | — | — | — |
| venue | select field | — | — | — | — | — | — |
| tenant | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Effective | toggle | off | — | `listStepUpPolicies` ?effective |

#### Outputs: what the screen shows and produces

**Data it reads**: `listStepUpPolicies` (onLoad, Policies in force)

**Where the user goes next**

- → `ADM-339` Governance & Compliance Command Center: *Back to Governance & Compliance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sensitive action confirmation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sensitive action confirmation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sensitive action confirmation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `required` is below the floor the operation's own `x-ticvai-step-up` sets. `refusedReason` is `belowContractFloor`, and `contractFloor` carries the lowest … (StepUpPolicyRefusedProblem) |

#### Permissions

- `setStepUpPolicy` → `APPROVAL_CONFIGURE` (configure) · staff
- `listStepUpPolicies` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- MFA / additional confirmation for sensitive approval actions is a business-configurable option (on or off), not mandatory, but the screens must support it when enabled. *(agreed · MoM 8 Sep 2026, 4.15 Execution & Decision Management · DI-729)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-343` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-343`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 6
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 8: Works in Sensitive Action Confirmation → Configure the final confirmation requirements before a sensitive approval becomes binding. The source specifically requires confirmation before execution of sensitive approvals.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-343?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-339`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-344` Digital Signature Management

**Manage workflows where approval decisions require a digital signature. The matrix explicitly requires digital-signature support for sensitive approvals.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_DECIDE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `requestId` (navigation) |
| Route | `/platform/digital-signature-management-adm-344` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workflow requiring signature | select field | — | — | — | — | — | — |
| Approval stage | select field | — | — | — | — | — | — |
| Signer role | select field | — | — | — | — | — | — |
| Signature requirement | select field | — | — | — | — | — | — |
| Certificate information | select field | — | — | — | — | — | — |
| Timestamp | select field | — | — | — | — | — | — |
| Signature validation status | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-339` Governance & Compliance Command Center: *Back to Governance & Compliance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital signature configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital signature untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital signature configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `signApprovalDecision` → `APPROVAL_DECIDE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Governance board manages segregation of duties, MFA policy, digital signature where applicable, data retention and audit trail, and shows identified compliance risks. *(client request · MoM 8 Sep 2026, 4.17 Governance, Security, Compliance & Audit · DI-732)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-344` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-344`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 6
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 10: Works in Digital Signature Management → Manage workflows where approval decisions require a digital signature. The matrix explicitly requires digital-signature support for sensitive approvals.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-344?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-339`.
- [ ] Every gated control is gated: `APPROVAL_DECIDE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-345` Immutable Approval Record & Tamper Detection

**Protect completed approval records from unauthorized modification. The matrix requires completed approval records to be immutable and requires detection of unauthorized modification attempts.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `requestId` (navigation) |
| Route | `/platform/immutable-approval-record-tamper-detection-adm-345` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every immutable approval record** (data table)

| Shows | Format | Notes |
|---|---|---|
| Record integrity: VERIFIED ✓ | text | not in the schema: `Record Integrity: VERIFIED ✓` |
| 🔴 potential tamper event detected | text | not in the schema: `🔴 Potential Tamper Event Detected` |
| Record affected | text | not in the schema: `Record affected` |
| User/service | text | not in the schema: `User/service` |
| Date/time | text | not in the schema: `Date/time` |
| Attempted action | text | not in the schema: `attempted action` |
| Source | text | not in the schema: `source` |
| Severity | text | not in the schema: `severity` |
| Investigation status | text | not in the schema: `investigation status` |

**The selected immutable approval record** (detail panel): The pack groups this record's detail under its own headings: “APR-10543”, “Integrity Information”.

| Shows | Format | Notes |
|---|---|---|
| Record integrity: VERIFIED ✓ | text | not in the schema: `Record Integrity: VERIFIED ✓` |
| 🔴 potential tamper event detected | text | not in the schema: `🔴 Potential Tamper Event Detected` |
| Record affected | text | not in the schema: `Record affected` |
| User/service | text | not in the schema: `User/service` |
| Date/time | text | not in the schema: `Date/time` |
| Attempted action | text | not in the schema: `attempted action` |
| Source | text | not in the schema: `source` |
| Severity | text | not in the schema: `severity` |
| Investigation status | text | not in the schema: `investigation status` |

**Where the user goes next**

- → `ADM-339` Governance & Compliance Command Center: *Back to Governance & Compliance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The immutable approval record list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the immutable approval record untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No immutable approval record yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the immutable approval record are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getApprovalRecord` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-345` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-345`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 6
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 12: Works in Immutable Approval Record & Tamper Detection → Protect completed approval records from unauthorized modification. The matrix requires completed approval records to be immutable and requires detection of unauthorized modification attempts.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-345?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-339`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-346` Approval Record Retention Policy

**Define how long approval and governance records shall be retained. The matrix explicitly requires configurable approval record-retention policies.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_CONFIGURE`, `TENANT_CONFIGURE`, `TENANT_VIEW` (2 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `dataClass` (navigation) |
| Route | `/platform/approval-record-retention-policy-adm-346` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Retention duration | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Country / jurisdiction | select field | — | — | — | — | — | — |
| Record category | select field | — | — | — | — | — | — |
| Workflow | select field | — | — | — | — | — | — |
| Effective date | select field | — | — | — | — | — | — |
| archival behavior | select field | — | — | — | — | — | — |
| disposal behavior | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Data class | select | — | Guest profile · Payment record · Financial record · Audit record · Approval record · Compliance inspection · Face tag biometric · Face pass biometric · AI prompts · AI conversations · AI decision records · AI metadata index | `listDataRetentionSettings` ?dataClass |

#### Outputs: what the screen shows and produces

**Data it reads**: `listDataRetentionSettings` (onLoad, Retention period per data class)

**Where the user goes next**

- → `ADM-339` Governance & Compliance Command Center: *Back to Governance & Compliance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval record retention configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval record retention untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval record retention configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A period below the class's legal minimum or above its legal maximum, a period sent for `aiMetadataIndex`, or a `followsDataClass` chain that loops |

#### Permissions

- `setApprovalRetentionPolicy` → `APPROVAL_CONFIGURE` (configure) · staff
- `listDataRetentionSettings` → `TENANT_VIEW` (read) · staff
- `setDataRetentionSetting` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.58 | Approval Record Retention - System shall support configurable approval record retention policies. | Approval Workflows & Governance | CONTRACTED | `setApprovalRetentionPolicy` |
| 4.3.4 | The system should support payment servers that provide the following functions: - Record transactions below the authorization threshold - Procure authorizations over the automatic authorization … | Bundles and Promotions | CONTRACTED | `setDataRetentionSetting` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Governance board manages segregation of duties, MFA policy, digital signature where applicable, data retention and audit trail, and shows identified compliance risks. *(client request · MoM 8 Sep 2026, 4.17 Governance, Security, Compliance & Audit · DI-732)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-346` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-346`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 6
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 14: Works in Approval Record Retention Policy → Define how long approval and governance records shall be retained. The matrix explicitly requires configurable approval record-retention policies.
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-346?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-339`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-347` Regulatory Audit & Evidence Center

**Provide internal and external auditors with controlled access to complete approval evidence. The source specifically requires approval records suitable for regulatory audits.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/regulatory-audit-evidence-center-adm-347` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search regulatory audit evidence | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by request, transaction, customer, approver, requester, workflow and 6 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-339` Governance & Compliance Command Center: *Back to Governance & Compliance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The regulatory audit evidence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the regulatory audit evidence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No regulatory audit evidence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the regulatory audit evidence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `createApprovalEvidencePackage` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Governance board manages segregation of duties, MFA policy, digital signature where applicable, data retention and audit trail, and shows identified compliance risks. *(client request · MoM 8 Sep 2026, 4.17 Governance, Security, Compliance & Audit · DI-732)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-347` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-347`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 6
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 16: Works in Regulatory Audit & Evidence Center → Provide internal and external auditors with controlled access to complete approval evidence. The source specifically requires approval records suitable for regulatory audits.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-347?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-339`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-348` Governance Risk & AI Compliance Advisor

**Use AI to identify unusual governance patterns, potential policy weaknesses and compliance risks. This screen should assist compliance teams rather than automatically change governance policies.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/governance-risk-ai-compliance-advisor-adm-348` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApprovalAnalytics` ?from |
| Group by | radio group | — | Kind · Approver · Venue · Day · Week | `getApprovalAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Data it reads**: `getApprovalAnalytics` (onLoad, Risk and compliance posture)

**Where the user goes next**

- → `ADM-339` Governance & Compliance Command Center: *Back to Governance & Compliance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance risk compliance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance risk compliance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance risk compliance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance risk compliance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getApprovalAnalytics` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-348` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-348`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 6
- Flow F128 *Approval Workflows and Governance board 6: Governance & Compliance Command …*, step 18: Works in Governance Risk & AI Compliance Advisor → Use AI to identify unusual governance patterns, potential policy weaknesses and compliance risks. This screen should assist compliance teams rather than automatically change governance policies.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-348?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-339`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
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

### In P09 · Platform

- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createApprovalEvidencePackage": {"method":"POST","path":"/approval-evidence-packages","contract":"approvals","summary":"Assemble what an auditor asked for","permission":"APPROVAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getApprovalAnalytics": {"method":"GET","path":"/approval-analytics","contract":"approvals","summary":"Volumes, times, rejections and bottlenecks","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"ApprovalAnalytics"},
"getApprovalRecord": {"method":"GET","path":"/approval-requests/{requestId}/record","contract":"approvals","summary":"The immutable decision record, and whether it is intact","permission":"APPROVAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ApprovalRecord"},
"getGuestVerificationPolicy": {"method":"GET","path":"/guest-verification-policy","contract":"identity","summary":"The tenant's guest identity-verification workflow","permission":"TENANT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"IdentityGuestVerificationPolicy"},
"listApprovalControlPolicies": {"method":"GET","path":"/approval-control-policies","contract":"approvals","summary":"Segregation of duties, four-eyes and dual control","permission":"APPROVAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ApprovalControlPolicy"},
"listDataRetentionSettings": {"method":"GET","path":"/data-retention-settings","contract":"tenancy","summary":"How long the tenant keeps each class of data","permission":"TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"dataClass","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMfaMethods": {"method":"GET","path":"/auth/mfa/methods","contract":"identity","summary":"Enrolled MFA methods","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MfaMethod"},
"listStepUpPolicies": {"method":"GET","path":"/step-up-policies","contract":"approvals","summary":"What needs a second factor here","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"effective","in":"query","required":null}],"requestBody":null,"responds":"StepUpPolicy"},
"setApprovalControlPolicy": {"method":"PUT","path":"/approval-control-policies","contract":"approvals","summary":"Require a second, independent pair of eyes","permission":"APPROVAL_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalControlPolicy","responds":"ApprovalControlPolicy"},
"setApprovalRetentionPolicy": {"method":"PUT","path":"/approval-retention","contract":"approvals","summary":"How long decision records are kept, and what survives","permission":"APPROVAL_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalRetentionPolicy","responds":"ApprovalRetentionPolicy"},
"setDataRetentionSetting": {"method":"PUT","path":"/data-retention-settings/{dataClass}","contract":"tenancy","summary":"Set how long the tenant keeps one class of data","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TenantDataRetentionSetting","responds":"TenantDataRetentionSetting"},
"setGuestVerificationPolicy": {"method":"PUT","path":"/guest-verification-policy","contract":"identity","summary":"Set which verifications a guest must pass, and when","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"IdentityGuestVerificationPolicy","responds":"IdentityGuestVerificationPolicy"},
"setPasswordPolicy": {"method":"PUT","path":"/password-policy","contract":"identity","summary":"Length, breach check, lockout and step-up","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PasswordPolicy","responds":"PasswordPolicy"},
"setSegregationRules": {"method":"PUT","path":"/segregation-rules","contract":"identity","summary":"Which permissions may not be held together","permission":"ROLE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SegregationRule"},
"setStepUpPolicy": {"method":"PUT","path":"/step-up-policies","contract":"approvals","summary":"Raise what needs a second factor","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"StepUpPolicy","responds":"StepUpPolicy"},
"signApprovalDecision": {"method":"POST","path":"/approval-requests/{requestId}/signature","contract":"approvals","summary":"Sign a decision, so it can be proved later","permission":"APPROVAL_DECIDE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalSignature"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalAnalytics": {"type":"object","x-ticvai-persistence":"none — aggregated from approvals.request","properties":{"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"groupBy":{"type":"string","description":"The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it.","enum":["kind","approver","venue","day","week"]},"rows":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"raised":{"type":"integer"},"approved":{"type":"integer"},"rejected":{"type":"integer"},"withdrawn":{"type":"integer"},"expired":{"type":"integer","description":"**Requests nobody answered.** Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person.\n"},"escalated":{"type":"integer"},"slaBreached":{"type":"integer"},"medianMinutes":{"type":"number"},"p95Minutes":{"type":"number"}}}}}},
"ApprovalControlPolicy": {"type":"object","x-ticvai-persistence":"approvals.control_policy","description":"Approvals boards 6.2 and 6.3. **Which decisions one person may not take alone** — distinct from which roles one person may not hold, which is `identity.setSegregationRules`.\n","required":["code","control"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"appliesToRequestKinds":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalKind"}},"appliesAboveValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"control":{"type":"string","enum":["fourEyes","dualControl","separationFromRequester","separationFromExecutor"],"description":"**`fourEyes` is two different people; `dualControl` is two people from different groups.** The second is stronger and is what a finance auditor means, and collapsing them makes the stronger control unexpressible.\n"},"requiredApproverGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"minimumApprovers":{"type":"integer","default":2},"requiresStepUp":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"breakGlassAllowed":{"type":"boolean","default":false,"description":"**Whether the control may be overridden in an emergency**, and if so it raises an alert rather than passing quietly. A control with no break-glass will be worked around by hand at three in the morning, which is worse.\n"},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalRecord": {"type":"object","x-ticvai-persistence":"approvals.decision_record","description":"Approvals boards 4.10 and 6.6. **Tamper evidence, not tamper prevention** — each record chains to the one before it, so a changed entry breaks every hash after it.\n","properties":{"requestId":{"type":"string","format":"uuid"},"sequence":{"type":"integer"},"recordedAt":{"type":"string","format":"date-time"},"decision":{"type":"string"},"decidedBy":{"type":"string","format":"uuid"},"comment":{"type":"string","nullable":true},"policyVersions":{"type":"array","description":"**What the rules were at the time**, because they have changed since.","items":{"type":"object","properties":{"policyId":{"type":"string","format":"uuid"},"version":{"type":"integer"}}}},"payloadHash":{"type":"string"},"previousRecordHash":{"type":"string","nullable":true},"recordHash":{"type":"string"},"signatures":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalSignature"}},"integrity":{"type":"string","readOnly":true,"enum":["intact","broken","unverifiable"],"description":"**Verified on read.** A tamper check nobody runs reports the breach years late."},"scopePath":{"type":"string"}}},
"ApprovalRetentionPolicy": {"type":"object","x-ticvai-persistence":"approvals.retention_policy","description":"Approvals board 6.7. **Approval records outlive what they approved.**","properties":{"id":{"type":"string","format":"uuid"},"appliesToRequestKinds":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalKind"}},"retainYears":{"type":"integer","nullable":true,"description":"**Null takes the tenant's `approvalRecord` retention setting** (tenancy `setDataRetentionSetting`; decided 29 September, all data retention is tenant configuration). A value here applies to the request kinds this policy names and may only lengthen what the tenant setting keeps.\n"},"retainSignatures":{"type":"boolean","default":true},"retainAttachments":{"type":"boolean","default":false},"onExpiry":{"type":"string","enum":["delete","anonymise","archive"],"default":"archive"},"overridesPrivacyDeletion":{"type":"boolean","default":true,"description":"**Can extend, never shorten, what privacy retention would delete.** The interaction is decided once here instead of argued per data-subject request.\n"},"legalBasis":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"ApprovalSignature": {"type":"object","x-ticvai-persistence":"approvals.signature","description":"Approvals board 6.5. **What is signed is the request as it stood at the moment of decision**, so a later edit breaks its own signature.\n","properties":{"id":{"type":"string","format":"uuid"},"requestId":{"type":"string","format":"uuid"},"signedBy":{"type":"string","format":"uuid"},"signedAt":{"type":"string","format":"date-time"},"method":{"type":"string","enum":["platformKey","uaePass","externalCertificate","drawnSignature"]},"payloadHash":{"type":"string"},"signature":{"type":"string"},"certificateSubject":{"type":"string","nullable":true},"stepUpVerified":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"IdentityGuestVerificationPolicy": {"type":"object","x-ticvai-persistence":"identity.guest_verification_policy","description":"**The tenant's configurable identity workflow for guests** (5.3.21; decided 29 September, build pass). Which verifications registration needs, which moments need a verified ID document, what is accepted and who reviews it. Proposed defaults are ours (our build plan).","required":["registrationRequires"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The tenant, written by the server (`x-ticvai-config-scope: tenant`)."},"registrationRequires":{"type":"array","description":"Verifications a new account must pass before it is usable. Proposed default `[mobileOtp]`.","items":{"type":"string","enum":["email","mobileOtp"]}},"idDocumentRequiredFor":{"type":"array","description":"The moments that need a verified ID document. Empty (the default) asks for none.","items":{"type":"string","enum":["accountCreation","ageRestrictedPurchase","residentPricing","accountRecovery","walletTopUpAboveLimit"]}},"walletTopUpLimit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acceptedDocumentKinds":{"type":"array","description":"Proposed default passport, emiratesId, nationalId.","items":{"type":"string","enum":["passport","emiratesId","nationalId","drivingLicence","residencePermit","other"]}},"uaePassSatisfiesIdDocument":{"type":"boolean","default":true,"description":"A guest signed in with UAE Pass (`guestUaePassLogin`) counts as ID-verified, since the national identity has already checked the person."},"socialLoginCountsAsEmailVerified":{"type":"boolean","default":true},"selfieRequired":{"type":"boolean","default":false},"reviewMode":{"type":"string","enum":["manual","provider","providerThenManual"],"default":"manual","description":"Who checks a document. `provider` and `providerThenManual` need the client's verification provider (make-or-break on `setGuestVerificationPolicy`)."},"documentImageRetention":{"type":"string","enum":["deleteOnDecision","keepUntilDocumentExpiry"],"default":"deleteOnDecision","description":"How long the scan is kept. The outcome and the hashed number are kept either way."},"maxResubmissions":{"type":"integer","minimum":0,"maximum":10,"default":3},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"MfaKind": {"type":"string","enum":["totp","smsOtp","emailOtp","biometric","hardwareToken"]},
"MfaMethod": {"x-ticvai-persistence":"identity.mfa_method","type":"object","required":["id","kind","isActive","enrolledAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"label":{"type":"string","nullable":true},"maskedTarget":{"type":"string","nullable":true,"description":"Partially masked destination, so a person can tell two methods apart."},"isActive":{"type":"boolean"},"isPrimary":{"type":"boolean"},"enrolledAt":{"type":"string","format":"date-time"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PasswordPolicy": {"type":"object","x-ticvai-persistence":"identity.password_policy","description":"BL-144. **Written by `setPasswordPolicy`, which returns it**, at tenant scope. Before BL-144 the package had no password policy, no lockout and no forced change at first logon anywhere.\n**Modelled on NIST SP 800-63B rather than on habit.** Length beats composition, and forced rotation on a schedule makes passwords worse — people increment a digit. Rotation is here because some tenants are contractually required to have it, **not because it helps.**\n","required":["id","scopePath","minLength"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"Assigned by the server. Required in the response only; ignored if a request sends it."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005), written by the server from the caller's tenant (`x-ticvai-config-scope: tenant`). Required in the response only; ignored if a request sends it."},"minLength":{"type":"integer","default":12,"minimum":8,"description":"A tenant may raise the length and never set it below 8 (decided 28 September, audit R126 (7))."},"requireBreachCheck":{"type":"boolean","default":true,"description":"**The single most effective rule.** Refusing a password known to be breached stops more account takeovers than every composition rule combined.\n"},"maxAgeDays":{"type":"integer","nullable":true,"description":"**Null is the recommended value.** Forced rotation produces `Summer2026!` becoming `Summer2027!`, and it is offered because some tenants are contractually obliged to have it rather than because it works.\n"},"recoveryMethods":{"type":"array","description":"BL-132. **A guest locked out had no path back** — lockout existed and recovery did not, which turns a forgotten password into a support call.\n**Ordered by strength, and the venue chooses which it offers.** Email is weakest and universal; a verified phone is stronger; an in-person check at a desk is strongest and only available to a guest who is already at the venue.\n","items":{"type":"string","enum":["email","sms","securityQuestions","inPersonVerification","supportAssisted"]}},"maxConcurrentSessions":{"type":"integer","nullable":true,"description":"BL-145. **Null, and that is the decision.** A staff principal has one live session, full stop: ADR-0004 keeps a server-side session registry (the `sid` claim, `ActiveSession`), and §3.1.3 refuses a second sign-in rather than counting towards a limit (confirmed 28 September, audit R184). A number here would only ever mean 1.\nThe requirement asked for it configurable. **Configurable to null is still an answer.**\n"},"deviceRestriction":{"type":"object","nullable":true,"description":"BL-146. **Device, browser, IP and location restriction on access.** Applies to staff principals, not guests — a guest restricted to one device is a guest who cannot use their new phone.\n**Warn before block by default.** An IP restriction that blocks silently is a venue manager locked out on the day their ISP rotates an address.\n","properties":{"allowedIpRanges":{"type":"array","items":{"type":"string"}},"allowedCountries":{"type":"array","items":{"type":"string"}},"requireRegisteredDevice":{"type":"boolean","default":false},"onViolation":{"type":"string","enum":["warn","requireStepUp","block"],"default":"requireStepUp"}}},"lockoutAfterAttempts":{"type":"integer","default":10},"lockoutMinutes":{"type":"integer","default":15,"description":"**A temporary lockout, not a permanent one.** Permanent lockout on failed attempts is a denial-of-service anybody can run against a known username.\n"},"forceChangeOnFirstLogon":{"type":"boolean","default":true},"reusePreventionCount":{"type":"integer","default":5,"minimum":0,"maximum":24,"description":"**How many previous credentials a staff member may not reuse** — the last 5 unless the tenant sets another (decided 28 September, audit R132). `changeOwnCredential` refuses a match with `422`.\n"},"mfaRequiredForPermissions":{"type":"array","description":"**Step-up rather than blanket MFA.** Requiring it for a refund approval and not for reading a rota is what stops people sharing devices to avoid it.\n**MFA is required by permission, not by role** (decided 28 September, audit R135). A principal holding any permission listed here must keep an active method (`removeMfaMethod` refuses to remove the last one). **The default is the platform floor**: `ROLE_MANAGE`, `LEDGER_APPROVE` and every `PLATFORM_*` permission. A tenant may add to the list and never remove a floor entry; a body that drops one is refused `400`.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"},"default":["ROLE_MANAGE","LEDGER_APPROVE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_TENANT_ACCESS","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY"]}}},
"SegregationRule": {"type":"object","x-ticvai-persistence":"identity.segregation_rule","description":"BL-147, 3.3.31 and 11.1.24. **The package enforced segregation of duties in exactly one place** — the product lifecycle guard requiring the approver not be the author — and there was no general rule.\n**A conflict is between two permissions held by one principal**, and the check runs at grant time rather than at use time: **discovering the conflict when somebody exercises it means the conflict already existed.**\n","required":["id","permissionA","permissionB","severity"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"Assigned by the server. Required in the response only; ignored if a request sends it."},"name":{"type":"string"},"permissionA":{"type":"string"},"permissionB":{"type":"string"},"severity":{"type":"string","enum":["block","requireApproval","warn"]},"rationale":{"type":"string","description":"**Why these two conflict, in words an auditor reads.** A rule with no rationale is a rule somebody removes when it becomes inconvenient.\n"},"scopeSensitive":{"type":"boolean","default":true,"description":"**Whether the two permissions must overlap in scope to conflict**, and this is not `scopePath` below — that one is the partition key and says where the rule *row* lives (ADR-0005), not where the *conflict* applies.\n**True, and it should rarely be false.** `ACCREDITATION_ISSUE` at Yas Island beside `ACCREDITATION_MANAGE` at Warner Bros is two jobs at two sites; flagging it is a control crying wolf, and the first thing a venue does with one of those is switch it off. The comparison walks `scopePath` prefixes the same way `resolvePermissions` already does — `uae.dubai` contains `uae.dubai.marina`, so one is an overlap and two siblings are not.\n**False is for conflicts that are genuinely estate-wide**, such as holding both sides of a financial reconciliation anywhere at all.\n"},"allowWithCompensatingControl":{"type":"boolean","default":false,"description":"**A small venue cannot always separate duties**, and pretending otherwise means the rule gets disabled entirely. A named compensating control is better than no rule.\n"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope**; the server sets it and ignores it in a request."}}},
"StepUpPolicy": {"x-ticvai-persistence":"approvals.step_up_policy","type":"object","required":["operationId","required"],"properties":{"operationId":{"type":"string","description":"The action governed. Names an operation, never a screen."},"required":{"allOf":[{"$ref":"#/components/schemas/StepUpStrength"}],"description":"The strength in force at this scope."},"contractFloor":{"allOf":[{"$ref":"#/components/schemas/StepUpStrength"}],"description":"What `x-ticvai-step-up` sets on the operation. Read only, and the value `required` may not go below.\n"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"],"description":"Where this rule was set, not where it applies."},"reason":{"type":"string","maxLength":512,"description":"Why it was raised. **An unexplained control is one somebody removes** the first time it is inconvenient.\n"},"setBy":{"type":"string","format":"uuid"},"setAt":{"type":"string","format":"date-time"}}},
"StepUpStrength": {"type":"string","description":"**Ordered, weakest first, and that ordering is what makes *raise only* checkable.** `pin` is a supervisor PIN captured in place — `roles.yaml` already resolves escalation that way and it is right for an action taken several times a shift. `mfa` is a challenge against an enrolled method and is right for an action taken a few times a month.\n","enum":["none","pin","mfa"]},
"TenantDataRetentionClass": {"type":"string","description":"**The data classes a tenant sets a retention period for** (decided 29 September, Chinmay: all data retention is tenant configuration, one setting per class). Defaults are ADR-0047's and the AI system design's (section 8, decision 5); a legal limit is the only thing the platform enforces.\n| Class | Default | Counted from | Legal limit (refused) | |---|---|---|---| | `guestProfile` | 5 years | last activity | none | | `paymentRecord` | 10 years | created | at least 10 years (4.3.4) | | `financialRecord` | 7 years | created | at least 7 years (6.1.78) | | `auditRecord` | 2 years (authorisation and device audit) | created | none | | `approvalRecord` | 7 years (approvals board 6.7) | decided | none | | `complianceInspection` | 7 years | created | none | | `faceTagBiometric` | 7 days | ticket expiry | make-or-break | | `facePassBiometric` | follows `guestProfile` | last activity | make-or-break | | `aiPrompts` | 90 days (prompts and responses) | created | none | | `aiConversations` | 90 days | last activity | none | | `aiDecisionRecords` | follows `auditRecord` (decision records and the approvals of AI actions) | decided | none | | `aiMetadataIndex` | always follows `aiDecisionRecords` (summaries, entities, embeddings) | created | none |\n**ADR-0047's floors and ceilings that are not law are defaults now, not refusals** (the audit floor of one year, the proposed seven-year guest-profile ceiling, the Face Tag thirty-day ceiling). Platform-owned copies — the burst environment copy, a decommissioned cell — are not tenant data classes and are not here.\n","enum":["guestProfile","paymentRecord","financialRecord","auditRecord","approvalRecord","complianceInspection","faceTagBiometric","facePassBiometric","aiPrompts","aiConversations","aiDecisionRecords","aiMetadataIndex"]},
"TenantDataRetentionSetting": {"type":"object","x-ticvai-persistence":"tenancy.data_retention_setting","description":"**One tenant's retention period for one data class** (decided 29 September, Chinmay). One row per tenant and class, written by `setDataRetentionSetting`; a class with no row takes the platform default. The limit and default fields are the platform's catalogue, computed for the response and not stored on the row.\n","required":["dataClass"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"dataClass":{"allOf":[{"$ref":"#/components/schemas/TenantDataRetentionClass"}],"x-ticvai-unique":"tenant","description":"One row per class per tenant. On a write it comes from the path; a body value is ignored."},"retainAmount":{"type":"integer","nullable":true,"minimum":0,"description":"The tenant's period. Null with no `followsDataClass` means the platform default applies. Zero means the data is not kept past the transaction that produced it.\n"},"retainUnit":{"type":"string","nullable":true,"enum":["days","months","years"],"description":"Required with `retainAmount`."},"followsDataClass":{"allOf":[{"$ref":"#/components/schemas/TenantDataRetentionClass"}],"nullable":true,"description":"Keep this class for as long as another class is kept. Set by default for `aiDecisionRecords` (follows `auditRecord`), `facePassBiometric` (follows `guestProfile`) and `aiMetadataIndex` (follows `aiDecisionRecords`, and cannot be changed).\n"},"onExpiry":{"type":"string","enum":["archive","anonymise","delete"],"default":"archive","description":"ADR-0047's stages. `archive` moves the data to the archive instance, from where it is erased on the class's own schedule; derived stores (the AI index, search) purge at archive, not later.\n"},"anchor":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"enum":["createdAt","lastActivity","decidedAt","ticketExpiry"],"description":"What the period is counted from. Fixed per class by the platform."},"effectiveAmount":{"type":"integer","readOnly":true,"x-ticvai-persisted":false,"description":"The period actually applied, after follows and defaults are resolved."},"effectiveUnit":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"isDefault":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"True when the tenant has not set this class and the platform default applies."},"defaultAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false},"defaultUnit":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"legalMinimumAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"A floor the law sets. A shorter period is refused (`422`)."},"legalMaximumAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"A maximum the law sets. A longer period is refused (`422`). Null for every class until the biometric make-or-break is answered."},"legalLimitUnit":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"legalBasis":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"The law or requirement the limit comes from, e.g. `4.3.4`."},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"updatedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The tenant. Retention is set at tenant scope only."}}}
}
```
