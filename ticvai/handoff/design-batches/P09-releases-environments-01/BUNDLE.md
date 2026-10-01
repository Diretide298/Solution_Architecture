# P09-releases-environments-01 — P09 · Releases & Environments

**7 screens · 20 operations · 20 schemas · 6 permissions**

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
  `DEVELOPER_ADMIN, PLATFORM_MIGRATION_APPLY, PLATFORM_MIGRATION_VIEW, PLATFORM_RELEASE_MANAGE, PLATFORM_RELEASE_PROMOTE, PLATFORM_RELEASE_VIEW`. A control nobody can use must say so,
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
| `ADM-022` | Release & Version Management | B–D | 17 | 27 | 6 | 1 | 2 | 0 | — | notStarted (generated) |
| `ADM-023` | Staging Promotion & Approval | B–D | 17 | 25 | 6 | 1 | 2 | 5 | — | notStarted (generated) |
| `ADM-024` | Release Notification Composer | B–D | 7 | 27 | 6 | 1 | 1 | 0 | — | notStarted (generated) |
| `ADM-025` | Tenant Upgrade Scheduler | B–D | 8 | 14 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-026` | End-of-Support Notice Management | B–D | 10 | 14 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-027` | Database Migration Console | B–D | 14 | 37 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-028` | Environment Registry | B–D | 8 | 16 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-025, ADM-028 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-022` Release & Version Management

**Find release & version management for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_PROMOTE`, `PLATFORM_RELEASE_VIEW` (1 configure, 1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listReleases` reads the population and `getRelease` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `releaseId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/release-and-version-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — new scope, 30 Jul

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Draft · In dev · In staging · In production · Superseded · Withdrawn | — | Sends `?status=` to `listReleases`. | `listReleases` ?status |
| Environment | segmented control | optional | — | Dev · Staging · Production | — | Sends `?environment=` to `listReleases`. | `listReleases` ?environment |

**Form: Create release** (modal, opened by *Create release*; *Create release* calls `createRelease`, *Cancel* sends nothing)

**Collects what `createRelease` sends before it is called.** Required: `components`, `note`. Optional: `requiredMigrations`, `breakingChanges`, `guestReleaseNotes` (the public "what's new" for guests, one short text per locale, naming no person; decided 29 September, rev 3 GAP-B2). Guests read it on the Help screen once the release reaches their cell; `note` stays internal. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Version `version` | text field | required | — | — | — | — | `createRelease` body |
| Components `components` | repeatable rows | required | — | at least 1 | — | — | `createRelease` body |
| Component `components[].component` | radio group | required | — | Backend · Frontend · AI · Infra · Contracts | — | — | `createRelease` body |
| Version `components[].version` | text field | required | — | — | — | — | `createRelease` body |
| Image digest `components[].imageDigest` | text field | optional | — | — | — | — | `createRelease` body |
| Required migrations `requiredMigrations` | list of values (chips) | optional | — | — | — | Migration versions this release depends on. | `createRelease` body |
| Note `note` | text area | required | — | min length 3; max length 2000 | — | Internal. Never shown to guests; `guestReleaseNotes` is. | `createRelease` body |
| Guest release notes `guestReleaseNotes` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | The public, localised "what's new" for guests (decided 29 September, rev 3 GAP-B2), one short text per locale, written for a guest and naming no person. | `createRelease` body |
| Breaking changes `breakingChanges` | list of values (chips) | optional | — | — | — | — | `createRelease` body |

Errors to draw in the form: 400 A required migration is absent, or a component version does not exist in the registry.

**Form: Promote release** (modal, opened by *Promote release*; *Promote release* calls `promoteRelease`, *Cancel* sends nothing)

**Collects what `promoteRelease` sends before it is called.** Required: `targetEnvironment`, `note`. Optional: `approverPrincipalId`, `stepUpToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target environment `targetEnvironment` | segmented control | required | — | Dev · Staging · Production | — | — | `promoteRelease` body |
| Note `note` | text area | required | — | min length 3; max length 1000 | — | — | `promoteRelease` body |
| Approver principal `approverPrincipalId` | picker: choose an approver principal | optional | — | — | shows names, sends the id | Required for production. May not be the requester. | `promoteRelease` body |
| Step up token `stepUpToken` | text field | optional | — | — | — | Required for production. Proves a factor was presented just now. | `promoteRelease` body |

Errors to draw in the form: 403 Approver is the requester, or the step-up token is absent or expired; 409 Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. (PromotionBlockedProblem)

**Sent by *Reject release*** (`rejectRelease`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `rejectRelease` body |

**Sent by *Withdraw release*** (`withdrawRelease`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `withdrawRelease` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every release** (data table, from `listReleases`)

| Shows | Format | Notes |
|---|---|---|
| Components | list or chips (count when long) | — |
| Required migrations | list or chips (count when long) | Migration versions this release depends on. |
| Note | text | Internal. Never shown to guests; `guestReleaseNotes` is. |
| Guest release notes | in the reader's language | The public, localised "what's new" for guests (decided 29 September, rev 3 GAP-B2), one short text per locale, written for a guest and … |
| Breaking changes | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Status | chip: Draft, In dev, In staging, In production, Superseded, Withdrawn | — |
| Created by principal | the name it points at, never the id | — |
| Promoted to staging at | 1 Oct 2026, 14:30 | — |
| Promoted to production at | 1 Oct 2026, 14:30 | — |

**The selected release** (detail panel, from `listReleases`)

| Shows | Format | Notes |
|---|---|---|
| Components | list or chips (count when long) | — |
| Required migrations | list or chips (count when long) | Migration versions this release depends on. |
| Note | text | Internal. Never shown to guests; `guestReleaseNotes` is. |
| Guest release notes | in the reader's language | The public, localised "what's new" for guests (decided 29 September, rev 3 GAP-B2), one short text per locale, written for a guest and … |
| Breaking changes | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Status | chip: Draft, In dev, In staging, In production, Superseded, Withdrawn | — |
| Created by principal | the name it points at, never the id | — |
| Promoted to staging at | 1 Oct 2026, 14:30 | — |
| Promoted to production at | 1 Oct 2026, 14:30 | — |

**The release readiness** (detail panel, from `getReleaseReadiness`)

| Shows | Format | Notes |
|---|---|---|
| Release | the name it points at, never the id | — |
| Can promote | yes / no (icon or chip) | — |
| Target environment | chip: Dev, Staging, Production | — |
| Gates | list or chips (count when long) | — |

**The release** (detail panel, from `getRelease`)

| Shows | Format | Notes |
|---|---|---|
| Rollouts | list or chips (count when long) | — |
| Cells on this version | 1,234 | — |
| Cells total | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Create release (primary button) | `createRelease` POST `/releases` | CreateReleaseRequest | Release | 400 A required migration is absent, or a component version does not exist in the registry. | opens modal first |
| Promote release (secondary button) | `promoteRelease` POST `/releases/{releaseId}/promote` | inline | Rollout | 403 Approver is the requester, or the step-up token is absent or expired; 409 Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. (PromotionBlockedProblem) | opens modal first |
| Reject release (destructive button) | `rejectRelease` POST `/releases/{releaseId}/reject` | inline | no body | 409 Not in a state that permits this | — |
| Withdraw release (destructive button) | `withdrawRelease` POST `/releases/{releaseId}/withdraw` | inline | no body | 409 Not in a state that permits this | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listReleases` (onLoad, Release list)

**Where the user goes next**

- → `ADM-027` Database Migration Console: *Plans the migrations the release requires*
- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

**What opens over it**

- confirmDialog *Reject release*: **Names what `rejectRelease` changes and what it leaves alone**, in the consequence rather than the verb. A release version this affects should be identified in the dialog, not just counted. **Collects what `rejectRelease` sends before it is called.** Required: `reason`.
- confirmDialog *Withdraw release*: **Names what `withdrawRelease` changes and what it leaves alone**, in the consequence rather than the verb. A release version this affects should be identified in the dialog, not just counted. **Collects what `withdrawRelease` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The release version list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the release version untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No release version yet. Offers Create release (`createRelease`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, environment and the release version are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listReleases` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A required migration is absent, or a component version does not exist in the registry.; 409 Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. (PromotionBlockedProblem); 409 Not in a state that permits this |

#### Permissions

- `listReleases` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `getRelease` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `getReleaseReadiness` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `createRelease` → `PLATFORM_RELEASE_MANAGE` (configure) · staff
- `promoteRelease` → `PLATFORM_RELEASE_PROMOTE` (operate) · staff
- `rejectRelease` → `PLATFORM_RELEASE_PROMOTE` (operate) · staff
- `withdrawRelease` → `PLATFORM_RELEASE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listReleases` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.1 | All business functionality available through the TAIS user interface shall be exposed through documented APIs unless restricted by security, compliance or operational considerations. | Developer & API Management | CONTRACTED | `listReleases` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Minor releases are notified but optional and customers can postpone them. Major releases carry advance notice, a defined support lifecycle, end-of-support announcements for old versions and a mandatory upgrade (e.g. Version 3 -> End of Support Notice -> Version 4). *(agreed · MoM 30 Jul 2026, 6. Global Versioning Strategy · DI-054)*
- Releases go to staging first; customers are notified of each new version with new features, bug fixes and release notes, test in staging, and approve before promotion to production. *(agreed · MoM 30 Jul 2026, 4. Deployment Workflow Discussion · DI-053)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-022` · status **notStarted** · provenance generated
- Flow F04 *Platform admin ships a release*, step 1: Reviews the release and its readiness → Sees which gates pass and which block, before attempting anything

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-022?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Create release, Promote release, Reject release, Withdraw release, What publishing changes.
- [ ] Every transition is wired: `ADM-027`, `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_PROMOTE`, `PLATFORM_RELEASE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-023` Staging Promotion & Approval

**Work with staging promotion & approval for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_PROMOTE`, `PLATFORM_RELEASE_VIEW` (1 configure, 1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listReleases` reads the population and `getReleaseReadiness` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `releaseId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/staging-promotion-and-approval` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — new scope, 30 Jul

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Draft · In dev · In staging · In production · Superseded · Withdrawn | — | Sends `?status=` to `listReleases`. | `listReleases` ?status |
| Environment | segmented control | optional | — | Dev · Staging · Production | — | Sends `?environment=` to `listReleases`. | `listReleases` ?environment |

**Form: Promote release** (modal, opened by *Promote release*; *Promote release* calls `promoteRelease`, *Cancel* sends nothing)

**Collects what `promoteRelease` sends before it is called.** Required: `targetEnvironment`, `note`. Optional: `approverPrincipalId`, `stepUpToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target environment `targetEnvironment` | segmented control | required | — | Dev · Staging · Production | — | — | `promoteRelease` body |
| Note `note` | text area | required | — | min length 3; max length 1000 | — | — | `promoteRelease` body |
| Approver principal `approverPrincipalId` | picker: choose an approver principal | optional | — | — | shows names, sends the id | Required for production. May not be the requester. | `promoteRelease` body |
| Step up token `stepUpToken` | text field | optional | — | — | — | Required for production. Proves a factor was presented just now. | `promoteRelease` body |

Errors to draw in the form: 403 Approver is the requester, or the step-up token is absent or expired; 409 Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. (PromotionBlockedProblem)

**Form: Create release** (modal, opened by *Create release*; *Create release* calls `createRelease`, *Cancel* sends nothing)

**Collects what `createRelease` sends before it is called.** Required: `components`, `note`. Optional: `requiredMigrations`, `breakingChanges`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Version `version` | text field | required | — | — | — | — | `createRelease` body |
| Components `components` | repeatable rows | required | — | at least 1 | — | — | `createRelease` body |
| Component `components[].component` | radio group | required | — | Backend · Frontend · AI · Infra · Contracts | — | — | `createRelease` body |
| Version `components[].version` | text field | required | — | — | — | — | `createRelease` body |
| Image digest `components[].imageDigest` | text field | optional | — | — | — | — | `createRelease` body |
| Required migrations `requiredMigrations` | list of values (chips) | optional | — | — | — | Migration versions this release depends on. | `createRelease` body |
| Note `note` | text area | required | — | min length 3; max length 2000 | — | Internal. Never shown to guests; `guestReleaseNotes` is. | `createRelease` body |
| Guest release notes `guestReleaseNotes` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | The public, localised "what's new" for guests (decided 29 September, rev 3 GAP-B2), one short text per locale, written for a guest and naming no person. | `createRelease` body |
| Breaking changes `breakingChanges` | list of values (chips) | optional | — | — | — | — | `createRelease` body |

Errors to draw in the form: 400 A required migration is absent, or a component version does not exist in the registry.

**Sent by *Reject release*** (`rejectRelease`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `rejectRelease` body |

**Sent by *Withdraw release*** (`withdrawRelease`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `withdrawRelease` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every release** (data table, from `listReleases`)

| Shows | Format | Notes |
|---|---|---|
| Components | list or chips (count when long) | — |
| Required migrations | list or chips (count when long) | Migration versions this release depends on. |
| Note | text | Internal. Never shown to guests; `guestReleaseNotes` is. |
| Breaking changes | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Status | chip: Draft, In dev, In staging, In production, Superseded, Withdrawn | — |
| Created by principal | the name it points at, never the id | — |
| Promoted to staging at | 1 Oct 2026, 14:30 | — |
| Promoted to production at | 1 Oct 2026, 14:30 | — |

**The selected release** (detail panel, from `listReleases`)

| Shows | Format | Notes |
|---|---|---|
| Components | list or chips (count when long) | — |
| Required migrations | list or chips (count when long) | Migration versions this release depends on. |
| Note | text | Internal. Never shown to guests; `guestReleaseNotes` is. |
| Breaking changes | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Status | chip: Draft, In dev, In staging, In production, Superseded, Withdrawn | — |
| Created by principal | the name it points at, never the id | — |
| Promoted to staging at | 1 Oct 2026, 14:30 | — |
| Promoted to production at | 1 Oct 2026, 14:30 | — |

**The release** (detail panel, from `getRelease`)

| Shows | Format | Notes |
|---|---|---|
| Rollouts | list or chips (count when long) | — |
| Cells on this version | 1,234 | — |
| Cells total | 1,234 | — |

**The release readiness** (detail panel, from `getReleaseReadiness`)

| Shows | Format | Notes |
|---|---|---|
| Release | the name it points at, never the id | — |
| Can promote | yes / no (icon or chip) | — |
| Target environment | chip: Dev, Staging, Production | — |
| Gates | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Promote release (primary button) | `promoteRelease` POST `/releases/{releaseId}/promote` | inline | Rollout | 403 Approver is the requester, or the step-up token is absent or expired; 409 Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. (PromotionBlockedProblem) | opens modal first |
| Create release (secondary button) | `createRelease` POST `/releases` | CreateReleaseRequest | Release | 400 A required migration is absent, or a component version does not exist in the registry. | opens modal first |
| Reject release (destructive button) | `rejectRelease` POST `/releases/{releaseId}/reject` | inline | no body | 409 Not in a state that permits this | — |
| Withdraw release (destructive button) | `withdrawRelease` POST `/releases/{releaseId}/withdraw` | inline | no body | 409 Not in a state that permits this | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listReleases` (onLoad, List releases)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-029` Deployment Monitor: *Watches the rollout per cell*; carries `rolloutId`; calls `promoteRelease`

**What opens over it**

- confirmDialog *Reject release*: **Names what `rejectRelease` changes and what it leaves alone**, in the consequence rather than the verb. A staging promotion approval this affects should be identified in the dialog, not just counted. **Collects what `rejectRelease` sends before it is called.** Required: `reason`.
- confirmDialog *Withdraw release*: **Names what `withdrawRelease` changes and what it leaves alone**, in the consequence rather than the verb. A staging promotion approval this affects should be identified in the dialog, not just counted. **Collects what `withdrawRelease` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staging promotion approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staging promotion approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staging promotion approval yet. Offers Create release (`createRelease`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, environment and the staging promotion approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `getReleaseReadiness` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A required migration is absent, or a component version does not exist in the registry.; 409 Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. (PromotionBlockedProblem); 409 Not in a state that permits this |

#### Permissions

- `promoteRelease` → `PLATFORM_RELEASE_PROMOTE` (operate) · staff
- `getReleaseReadiness` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `createRelease` → `PLATFORM_RELEASE_MANAGE` (configure) · staff
- `getRelease` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `listReleases` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `rejectRelease` → `PLATFORM_RELEASE_PROMOTE` (operate) · staff
- `withdrawRelease` → `PLATFORM_RELEASE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `getReleaseReadiness` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.1 | All business functionality available through the TAIS user interface shall be exposed through documented APIs unless restricted by security, compliance or operational considerations. | Developer & API Management | CONTRACTED | `listReleases` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Post-go-live, only configuration changes tested in staging (e.g. a new product or package) should be promoted to production, never transactional data; feasibility pending the CI/CD engineer. *(open · MoM 10 Sep 2026, 4.13 Pre-Production to Production Configuration Promotion · DI-834)*
- Releases go to staging first; customers are notified of each new version with new features, bug fixes and release notes, test in staging, and approve before promotion to production. *(agreed · MoM 30 Jul 2026, 4. Deployment Workflow Discussion · DI-053)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-023` · status **notStarted** · provenance generated
- Flow F04 *Platform admin ships a release*, step 3: Requests promotion with an approver → Approval recorded against the release. The approver may not be the requester
- Flow F04 branch at step 3 (recoverable): when The plan has gone stale, Apply is refused. Cell state changed since the plan was computed, and applying it would run against a different world than the one reviewed.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-023?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Promote release, Create release, Reject release, Withdraw release, What publishing changes.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-029`.
- [ ] Every gated control is gated: `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_PROMOTE`, `PLATFORM_RELEASE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-024` Release Notification Composer

**Push live release notification composer for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSupportNotices` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/general/release-notification-composer` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — new scope, 30 Jul

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Draft · In dev · In staging · In production · Superseded · Withdrawn | `listReleases` ?status |
| Environment | segmented control | — | Dev · Staging · Production | `listReleases` ?environment |

**Form: Publish support notice** (modal, opened by *Publish support notice*; *Publish support notice* calls `publishSupportNotice`, *Cancel* sends nothing)

**Collects what `publishSupportNotice` sends before it is called.** Required: `id`, `supportEndsAt`, `publishedAt`. Optional: `message`, `affectedTenantIds`, `publishedByPrincipalId`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `publishSupportNotice` body |
| Version `version` | text field | required | — | — | — | — | `publishSupportNotice` body |
| Support ends at `supportEndsAt` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `publishSupportNotice` body |
| Message `message` | key and value settings | optional | — | — | — | — | `publishSupportNotice` body |
| Published by principal `publishedByPrincipalId` | picker: choose a published by principal | optional | — | — | shows names, sends the id | — | `publishSupportNotice` body |
| Published at `publishedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishSupportNotice` body |
| Scope path `scopePath` | text field | optional | — | — | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row … | `publishSupportNotice` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every support notice** (data table, from `listSupportNotices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Support ends at | 1 Oct 2026 | — |
| Message | grouped details | — |
| Affected tenants | list or chips (count when long) | Computed from cell versions, never typed. A notice to the wrong list is worse than none. |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Every release** (data table, from `listReleases`)

| Shows | Format | Notes |
|---|---|---|
| Components | list or chips (count when long) | — |
| Required migrations | list or chips (count when long) | Migration versions this release depends on. |
| Note | text | Internal. Never shown to guests; `guestReleaseNotes` is. |
| Guest release notes | in the reader's language | The public, localised "what's new" for guests (decided 29 September, rev 3 GAP-B2), one short text per locale, written for a guest and … |
| Breaking changes | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Status | chip: Draft, In dev, In staging, In production, Superseded, Withdrawn | — |
| Created by principal | the name it points at, never the id | — |
| Promoted to staging at | 1 Oct 2026, 14:30 | — |
| Promoted to production at | 1 Oct 2026, 14:30 | — |

**The selected support notice** (detail panel, from `listSupportNotices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Support ends at | 1 Oct 2026 | — |
| Message | grouped details | — |
| Affected tenants | list or chips (count when long) | Computed from cell versions, never typed. A notice to the wrong list is worse than none. |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**What's new for guests** (detail panel, from `listReleases`): **The public, localised release notes a guest reads on the Help screen** (decided 29 September, rev 3 GAP-B2; WEB-025, WEB-045, GST-040 through `getTenantAppStatus.whatsNew`, the ten newest). Written with the release on ADM-022 (`createRelease.guestReleaseNotes`); shown here beside the staff notice so the two are composed together and say the same thing. Distinct from the staff-only recent …

| Shows | Format | Notes |
|---|---|---|
| Version | text | — |
| Guest release notes | in the reader's language | The public, localised "what's new" for guests (decided 29 September, rev 3 GAP-B2), one short text per locale, written for a guest and … |
| Promoted to production at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Publish support notice (primary button) | `publishSupportNotice` POST `/support-notices` | SupportNotice | SupportNotice | — | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listSupportNotices` (onLoad, End-of-support notices); `listReleases` (onLoad, Releases and their readiness)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The release notification composer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the release notification composer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No release notification composer yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listSupportNotices` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `publishSupportNotice` → `PLATFORM_RELEASE_MANAGE` (configure) · staff
- `listSupportNotices` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `listReleases` → `PLATFORM_RELEASE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.1 | All business functionality available through the TAIS user interface shall be exposed through documented APIs unless restricted by security, compliance or operational considerations. | Developer & API Management | CONTRACTED | `listReleases` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Releases go to staging first; customers are notified of each new version with new features, bug fixes and release notes, test in staging, and approve before promotion to production. *(agreed · MoM 30 Jul 2026, 4. Deployment Workflow Discussion · DI-053)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-024` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-024?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Publish support notice, What publishing changes.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-025` Tenant Upgrade Scheduler

**Find tenant upgrade scheduler for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listUpgradeSchedules` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/general/tenant-upgrade-scheduler` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — new scope, 30 Jul

#### Inputs: what the user enters or picks

**Form: Schedule tenant upgrade** (modal, opened by *Schedule tenant upgrade*; *Schedule tenant upgrade* calls `scheduleTenantUpgrade`, *Cancel* sends nothing)

**Collects what `scheduleTenantUpgrade` sends before it is called.** Required: `releaseVersion`, `scheduledFor`. Optional: `tenantName`, `deferredByTenant`, `deferralReason`, `maxDeferralUntil`, `notifiedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tenant `tenantId` | picker: choose a tenant | required | — | — | shows names, sends the id | — | `scheduleTenantUpgrade` body |
| Tenant name `tenantName` | text field | optional | — | — | — | — | `scheduleTenantUpgrade` body |
| Release version `releaseVersion` | text field | required | — | — | — | — | `scheduleTenantUpgrade` body |
| Scheduled for `scheduledFor` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `scheduleTenantUpgrade` body |
| Deferred by tenant `deferredByTenant` | toggle | optional | — | — | — | — | `scheduleTenantUpgrade` body |
| Deferral reason `deferralReason` | text field | optional | — | — | — | — | `scheduleTenantUpgrade` body |
| Max deferral until `maxDeferralUntil` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Beyond this the platform proceeds. An indefinitely deferred tenant becomes a version nobody supports. | `scheduleTenantUpgrade` body |
| Notified at `notifiedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `scheduleTenantUpgrade` body |

Errors to draw in the form: 400 Deferral exceeds the maximum permitted window

#### Outputs: what the screen shows and produces

**Shown**

**Every upgrade schedule** (data table, from `listUpgradeSchedules`)

| Shows | Format | Notes |
|---|---|---|
| Tenant name | text | — |
| Release version | text | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Deferred by tenant | yes / no (icon or chip) | — |
| Deferral reason | text | — |
| Max deferral until | 1 Oct 2026, 14:30 | Beyond this the platform proceeds. An indefinitely deferred tenant becomes a version nobody supports. |
| Notified at | 1 Oct 2026, 14:30 | — |

**The selected upgrade schedule** (detail panel, from `listUpgradeSchedules`)

| Shows | Format | Notes |
|---|---|---|
| Tenant name | text | — |
| Release version | text | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Deferred by tenant | yes / no (icon or chip) | — |
| Deferral reason | text | — |
| Max deferral until | 1 Oct 2026, 14:30 | Beyond this the platform proceeds. An indefinitely deferred tenant becomes a version nobody supports. |
| Notified at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Schedule tenant upgrade (primary button) | `scheduleTenantUpgrade` POST `/upgrade-schedules` | UpgradeSchedule | UpgradeSchedule | 400 Deferral exceeds the maximum permitted window | opens modal first |

**Data it reads**: `listUpgradeSchedules` (onLoad, Scheduled tenant upgrades)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tenant upgrade scheduler list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tenant upgrade scheduler untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tenant upgrade scheduler yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listUpgradeSchedules` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listUpgradeSchedules` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Deferral exceeds the maximum permitted window |

#### Permissions

- `listUpgradeSchedules` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `scheduleTenantUpgrade` → `PLATFORM_RELEASE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listUpgradeSchedules` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Minor releases are notified but optional and customers can postpone them. Major releases carry advance notice, a defined support lifecycle, end-of-support announcements for old versions and a mandatory upgrade (e.g. Version 3 -> End of Support Notice -> Version 4). *(agreed · MoM 30 Jul 2026, 6. Global Versioning Strategy · DI-054)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-025` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-025?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Schedule tenant upgrade.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-026` End-of-Support Notice Management

**Answer a question without needing a person.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `DEVELOPER_ADMIN`, `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW` (2 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSupportNotices` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `version` (navigation) · cold entry: **Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one the screen says what is missing and offers that … |
| Route | `/general/end-of-support-notice-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — new scope, 30 Jul

#### Inputs: what the user enters or picks

**Form: Publish support notice** (modal, opened by *Publish support notice*; *Publish support notice* calls `publishSupportNotice`, *Cancel* sends nothing)

**Collects what `publishSupportNotice` sends before it is called.** Required: `id`, `supportEndsAt`, `publishedAt`. Optional: `message`, `affectedTenantIds`, `publishedByPrincipalId`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `publishSupportNotice` body |
| Version `version` | text field | required | — | — | — | — | `publishSupportNotice` body |
| Support ends at `supportEndsAt` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `publishSupportNotice` body |
| Message `message` | key and value settings | optional | — | — | — | — | `publishSupportNotice` body |
| Published by principal `publishedByPrincipalId` | picker: choose a published by principal | optional | — | — | shows names, sends the id | — | `publishSupportNotice` body |
| Published at `publishedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishSupportNotice` body |
| Scope path `scopePath` | text field | optional | — | — | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row … | `publishSupportNotice` body |

**Form: Deprecate API version** (modal, opened by *Deprecate API version*; *Deprecate API version* calls `deprecateApiVersion`, *Cancel* sends nothing)

**Collects what `deprecateApiVersion` sends before it is called.** Required: `sunsetAt`, `reason`. Optional: `migrationGuideUrl`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sunset at `sunsetAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `deprecateApiVersion` body |
| Reason `reason` | text area | required | — | — | — | — | `deprecateApiVersion` body |
| Migration guide URL `migrationGuideUrl` | text field | optional | — | — | — | — | `deprecateApiVersion` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every support notice** (data table, from `listSupportNotices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Support ends at | 1 Oct 2026 | — |
| Message | grouped details | — |
| Affected tenants | list or chips (count when long) | Computed from cell versions, never typed. A notice to the wrong list is worse than none. |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected support notice** (detail panel, from `listSupportNotices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Support ends at | 1 Oct 2026 | — |
| Message | grouped details | — |
| Affected tenants | list or chips (count when long) | Computed from cell versions, never typed. A notice to the wrong list is worse than none. |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Publish support notice (primary button) | `publishSupportNotice` POST `/support-notices` | SupportNotice | SupportNotice | — | opens modal first |
| Deprecate API version (secondary button) | `deprecateApiVersion` POST `/api-versions/{version}/deprecate` | inline | ApiVersion | — | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listSupportNotices` (onLoad, End-of-support notices)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The end-of-support notice list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the end-of-support notice untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No end-of-support notice yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listSupportNotices` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listSupportNotices` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `publishSupportNotice` → `PLATFORM_RELEASE_MANAGE` (configure) · staff
- `deprecateApiVersion` → `DEVELOPER_ADMIN` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listSupportNotices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Minor releases are notified but optional and customers can postpone them. Major releases carry advance notice, a defined support lifecycle, end-of-support announcements for old versions and a mandatory upgrade (e.g. Version 3 -> End of Support Notice -> Version 4). *(agreed · MoM 30 Jul 2026, 6. Global Versioning Strategy · DI-054)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-026` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-026?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Publish support notice, Deprecate API version, What publishing changes.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `DEVELOPER_ADMIN`, `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-027` Database Migration Console

**Find database migration console for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_MIGRATION_APPLY`, `PLATFORM_MIGRATION_VIEW` (1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listMigrations` reads the population and `getVersionSkew` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `runId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/database-migration-console` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — the unowned orchestrator

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Applied to | picker: choose an applied to (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?appliedTo=` to `listMigrations`. | `listMigrations` ?appliedTo |
| Pending only | toggle | optional | off | — | — | Sends `?pendingOnly=` to `listMigrations`. | `listMigrations` ?pendingOnly |

**Form: Plan migration** (modal, opened by *Plan migration*; *Plan migration* calls `planMigration`, *Cancel* sends nothing)

**Collects what `planMigration` sends before it is called.** Required: `targetVersion`. Optional: `cellIds`, `environment`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target version `targetVersion` | text field | required | — | — | — | — | `planMigration` body |
| Cells `cellIds` | multi-picker: choose cells | optional | — | — | — | Omit to plan across every cell in scope. | `planMigration` body |
| Environment `environment` | segmented control | optional | — | Dev · Staging · Production | — | — | `planMigration` body |

Errors to draw in the form: 400 Target version unknown, or the path between versions is not contiguous

**Form: Apply migration** (modal, opened by *Apply migration*; *Apply migration* calls `applyMigration`, *Cancel* sends nothing)

**Collects what `applyMigration` sends before it is called.** Required: `planId`, `stepUpToken`. Optional: `canaryCellId`, `haltOnFirstFailure`, `maintenanceWindow`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Plan `planId` | picker: choose a plan | required | — | — | shows names, sends the id | — | `applyMigration` body |
| Step up token `stepUpToken` | text field | required | — | — | — | — | `applyMigration` body |
| Canary cell `canaryCellId` | picker: choose a canary cell | optional | — | — | shows names, sends the id | Applied alone and verified before the rest proceed. Defaults to the smallest cell in the plan. | `applyMigration` body |
| Halt on first failure `haltOnFirstFailure` | toggle | optional | on | — | — | — | `applyMigration` body |
| Maintenance window `maintenanceWindow` | group | optional | — | — | — | — | `applyMigration` body |
| Starts at `maintenanceWindow.startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `applyMigration` body |
| Ends at `maintenanceWindow.endsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `applyMigration` body |

Errors to draw in the form: 409 The plan is stale — cell state changed since it was computed. Re-plan and review before applying.

**Form: Rollback migration run** (modal, opened by *Rollback migration run*; *Rollback migration run* calls `rollbackMigrationRun`, *Cancel* sends nothing)

**Collects what `rollbackMigrationRun` sends before it is called.** Required: `reason`, `stepUpToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `rollbackMigrationRun` body |
| Step up token `stepUpToken` | text field | required | — | — | — | — | `rollbackMigrationRun` body |

Errors to draw in the form: 409 A migration in this run is irreversible (IrreversibleProblem)

#### Outputs: what the screen shows and produces

**Shown**

**Every migration** (data table, from `listMigrations`)

| Shows | Format | Notes |
|---|---|---|
| Module | text | — |
| Description | text | — |
| Is reversible | yes / no (icon or chip) | A rollback section exists and CI has executed it against a restored snapshot. A rollback nobody has run is a comment, not a rollback. |
| Rollback tested at | 1 Oct 2026, 14:30 | — |
| Checksum | text | Compared on apply. A migration edited after it was applied somewhere is a defect the register catches, not a mystery to debug later. |
| Estimated lock ms | 1,234 | — |
| Touches partitioned table | yes / no (icon or chip) | — |
| Applied cell count | 1,234 | — |
| Pending cell count | 1,234 | — |

**The selected migration** (detail panel, from `listMigrations`)

| Shows | Format | Notes |
|---|---|---|
| Module | text | — |
| Description | text | — |
| Is reversible | yes / no (icon or chip) | A rollback section exists and CI has executed it against a restored snapshot. A rollback nobody has run is a comment, not a rollback. |
| Rollback tested at | 1 Oct 2026, 14:30 | — |
| Checksum | text | Compared on apply. A migration edited after it was applied somewhere is a defect the register catches, not a mystery to debug later. |
| Estimated lock ms | 1,234 | — |
| Touches partitioned table | yes / no (icon or chip) | — |
| Applied cell count | 1,234 | — |
| Pending cell count | 1,234 | — |

**The migration run** (detail panel, from `getMigrationRun`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Plan | the name it points at, never the id | — |
| Status | chip: Queued, Canary, Running, Paused, Complete, Failed… | — |
| Canary cell | the name it points at, never the id | Which region the canary tenant is in. The canary itself is a tenant — a first cell holding two hundred databases is not a cheap failure … |
| Canary tenant | the name it points at, never the id | — |
| Tenants total | 1,234 | — |
| Tenants complete | 1,234 | — |
| Tenants failed | 1,234 | — |
| Cells total | 1,234 | — |
| Cells complete | 1,234 | — |
| Cells failed | 1,234 | — |
| Started by principal | the name it points at, never the id | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Cells | list or chips (count when long) | — |
| Tenants | list or chips (count when long) | — |

**The version skew report** (detail panel, from `getVersionSkew`)

| Shows | Format | Notes |
|---|---|---|
| As at | 1 Oct 2026, 14:30 | — |
| Has unexplained skew | yes / no (icon or chip) | Skew during a rollout is expected. Skew outside one is a defect, and separating the two is the entire value of this report. |
| Cells | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Plan migration (primary button) | `planMigration` POST `/migrations/plan` | inline | MigrationPlan | 400 Target version unknown, or the path between versions is not contiguous | opens modal first |
| Apply migration (secondary button) | `applyMigration` POST `/migrations/apply` | inline | MigrationRun | 409 The plan is stale — cell state changed since it was computed. Re-plan and review before applying. | opens modal first |
| Rollback migration run (secondary button) | `rollbackMigrationRun` POST `/migrations/runs/{runId}/rollback` | inline | MigrationRun | 409 A migration in this run is irreversible (IrreversibleProblem) | opens modal first |

**Data it reads**: `listMigrations` (onLoad, The migration register); `getVersionSkew` (onLoad, Schema and application version per cell); `getMigrationRun` (onLoad, Migration run progress per cell)

**Where the user goes next**

- → `ADM-023` Staging Promotion & Approval: *Requests promotion with an approver*; calls `planMigration`
- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The database migration console list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the database migration console untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No database migration console yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on appliedTo, pendingOnly and the database migration console are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_MIGRATION_VIEW`, which `listMigrations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Target version unknown, or the path between versions is not contiguous; 409 A migration in this run is irreversible (IrreversibleProblem); 409 The plan is stale — cell state changed since it was computed. Re-plan and review before applying. |

#### Permissions

- `listMigrations` → `PLATFORM_MIGRATION_VIEW` (read) · staff
- `planMigration` → `PLATFORM_MIGRATION_VIEW` (read) · staff
- `applyMigration` → `PLATFORM_MIGRATION_APPLY` (operate) · staff
- `getVersionSkew` → `PLATFORM_MIGRATION_VIEW` (read) · staff
- `getMigrationRun` → `PLATFORM_MIGRATION_VIEW` (read) · staff
- `rollbackMigrationRun` → `PLATFORM_MIGRATION_APPLY` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_MIGRATION_VIEW`, which `listMigrations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-027` · status **notStarted** · provenance generated
- Flow F04 *Platform admin ships a release*, step 2: Plans the migrations the release requires → Sees per-cell migrations, estimated lock duration, and whether every one is reversible
- Flow F04 branch at step 2 (requiresStaff): when A migration in the release is irreversible, Named in the plan, not merely counted. A one-way door should be identified before it is walked through — promotion may still proceed, but knowingly.
- Flow F04 branch at step 2 (recoverable): when The plan predicts a long lock on a partitioned table, Surfaced as a warning with the affected cells. This is the output the plan step exists to produce.
- ADR-0014 *Cell Per Region* (`docs/adr/0014-cell-per-region.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (37 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-027?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Plan migration, Apply migration, Rollback migration run.
- [ ] Every transition is wired: `ADM-023`, `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_MIGRATION_APPLY`, `PLATFORM_MIGRATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-028` Environment Registry

**Find environment registry for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Releases & Environments · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listEnvironments` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/general/environment-registry` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — not specified

#### Inputs: what the user enters or picks

**Form: Register environment** (modal, opened by *Register environment*; *Register environment* calls `registerEnvironment`, *Cancel* sends nothing)

**Collects what `registerEnvironment` sends before it is called.** Required: `id`, `kind`, `name`. Optional: `cellIds`, `requiresApprovalToPromote`, `soakHours`, `currentReleaseVersion`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `registerEnvironment` body |
| Kind `kind` | segmented control | required | — | Dev · Staging · Production | — | — | `registerEnvironment` body |
| Name `name` | text field | required | — | — | — | — | `registerEnvironment` body |
| Cells `cellIds` | multi-picker: choose cells | optional | — | — | — | — | `registerEnvironment` body |
| Requires approval to promote `requiresApprovalToPromote` | toggle | optional | — | — | — | — | `registerEnvironment` body |
| Soak hours `soakHours` | number field (hours) | optional | — | — | — | How long a release must sit here before it may be promoted. Zero for dev; a real number for staging, or staging is a formality. | `registerEnvironment` body |
| Current release version `currentReleaseVersion` | text field | optional | — | — | — | — | `registerEnvironment` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `registerEnvironment` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every environment** (data table, from `listEnvironments`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Dev, Staging, Production | — |
| Name | text | — |
| Cells | list or chips (count when long) | — |
| Requires approval to promote | yes / no (icon or chip) | — |
| Soak hours | 1,234 | How long a release must sit here before it may be promoted. Zero for dev; a real number for staging, or staging is a formality. |
| Current release version | text | — |
| Is active | yes / no (icon or chip) | — |

**The selected environment** (detail panel, from `listEnvironments`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Dev, Staging, Production | — |
| Name | text | — |
| Cells | list or chips (count when long) | — |
| Requires approval to promote | yes / no (icon or chip) | — |
| Soak hours | 1,234 | How long a release must sit here before it may be promoted. Zero for dev; a real number for staging, or staging is a formality. |
| Current release version | text | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Register environment (primary button) | `registerEnvironment` POST `/environments` | Environment | Environment | — | opens modal first |

**Data it reads**: `listEnvironments` (onLoad, Environment registry)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The environment registry list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the environment registry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No environment registry yet. Offers Register environment (`registerEnvironment`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listEnvironments` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listEnvironments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listEnvironments` → `PLATFORM_RELEASE_VIEW` (read) · staff
- `registerEnvironment` → `PLATFORM_RELEASE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_RELEASE_VIEW`, which `listEnvironments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-028` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-028?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Register environment.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_RELEASE_MANAGE`, `PLATFORM_RELEASE_VIEW`.
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

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"applyMigration": {"method":"POST","path":"/migrations/apply","contract":"platform-ops","summary":"Apply a planned migration run","permission":"PLATFORM_MIGRATION_APPLY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createRelease": {"method":"POST","path":"/releases","contract":"platform-ops","summary":"Cut a release","permission":"PLATFORM_RELEASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReleaseRequest","responds":"Release"},
"deprecateApiVersion": {"method":"POST","path":"/api-versions/{version}/deprecate","contract":"public-api","summary":"Announce a sunset date and notify subscribers","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApiVersion"},
"getMigrationRun": {"method":"GET","path":"/migrations/runs/{runId}","contract":"platform-ops","summary":"Migration run progress per cell","permission":"PLATFORM_MIGRATION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MigrationRun"},
"getRelease": {"method":"GET","path":"/releases/{releaseId}","contract":"platform-ops","summary":"Read a release with its rollout state","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ReleaseDetail"},
"getReleaseReadiness": {"method":"GET","path":"/releases/{releaseId}/readiness","contract":"platform-ops","summary":"Whether a release can be promoted, and what blocks it","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ReleaseReadiness"},
"getVersionSkew": {"method":"GET","path":"/migrations/version-skew","contract":"platform-ops","summary":"Schema and application version across every cell","permission":"PLATFORM_MIGRATION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"VersionSkewReport"},
"listEnvironments": {"method":"GET","path":"/environments","contract":"platform-ops","summary":"The environment registry","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"Environment"},
"listMigrations": {"method":"GET","path":"/migrations","contract":"platform-ops","summary":"The migration register","permission":"PLATFORM_MIGRATION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"appliedTo","in":"query","required":null},{"name":"pendingOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReleases": {"method":"GET","path":"/releases","contract":"platform-ops","summary":"List releases","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"environment","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSupportNotices": {"method":"GET","path":"/support-notices","contract":"platform-ops","summary":"End-of-support notices","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SupportNotice"},
"listUpgradeSchedules": {"method":"GET","path":"/upgrade-schedules","contract":"platform-ops","summary":"Scheduled tenant upgrades","permission":"PLATFORM_RELEASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"UpgradeSchedule"},
"planMigration": {"method":"POST","path":"/migrations/plan","contract":"platform-ops","summary":"Plan a migration run without applying it","permission":"PLATFORM_MIGRATION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MigrationPlan"},
"promoteRelease": {"method":"POST","path":"/releases/{releaseId}/promote","contract":"platform-ops","summary":"Promote a release to the next environment","permission":"PLATFORM_RELEASE_PROMOTE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"publishSupportNotice": {"method":"POST","path":"/support-notices","contract":"platform-ops","summary":"Publish an end-of-support notice","permission":"PLATFORM_RELEASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SupportNotice","responds":"SupportNotice"},
"registerEnvironment": {"method":"POST","path":"/environments","contract":"platform-ops","summary":"Register an environment","permission":"PLATFORM_RELEASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Environment","responds":"Environment"},
"rejectRelease": {"method":"POST","path":"/releases/{releaseId}/reject","contract":"platform-ops","summary":"Reject a release back a stage","permission":"PLATFORM_RELEASE_PROMOTE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"rollbackMigrationRun": {"method":"POST","path":"/migrations/runs/{runId}/rollback","contract":"platform-ops","summary":"Roll a migration run back","permission":"PLATFORM_MIGRATION_APPLY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"scheduleTenantUpgrade": {"method":"POST","path":"/upgrade-schedules","contract":"platform-ops","summary":"Schedule or defer a tenant upgrade","permission":"PLATFORM_RELEASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"UpgradeSchedule","responds":"UpgradeSchedule"},
"withdrawRelease": {"method":"POST","path":"/releases/{releaseId}/withdraw","contract":"platform-ops","summary":"Withdraw a release","permission":"PLATFORM_RELEASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApiVersion": {"type":"object","x-ticvai-persistence":"control.api_version","description":"13.1.31 to 13.1.35, ADR-0026. **CF-141 is sharper under D1**: a single supported production version was tenable when only Softlabs called the API, and **with third parties a breaking change with no window breaks somebody else's business.**\n","required":["version","status"],"properties":{"version":{"type":"string"},"status":{"type":"string","enum":["preview","current","deprecated","sunset"]},"releasedAt":{"type":"string","format":"date-time"},"deprecatedAt":{"type":"string","format":"date-time","nullable":true},"sunsetAt":{"type":"string","format":"date-time","nullable":true},"minimumNoticeMonths":{"type":"integer","default":12,"description":"**The commitment, not the intention.** A deprecation policy without a stated minimum is a policy that shortens under pressure.\n"},"migrationGuideUrl":{"type":"string","nullable":true},"activeClientCount":{"type":"integer","readOnly":true},"changes":{"type":"array","description":"**The developer changelog for this version** (17 September minutes, M17-14): every operation added, changed, deprecated or removed, and whether the change is breaking under ADR-0026. Generated at release from the contract diff; shown on DEV-001.\n","items":{"type":"object","required":["operationId","kind"],"properties":{"operationId":{"type":"string"},"contract":{"type":"string"},"kind":{"type":"string","enum":["added","changed","deprecated","removed"]},"breaking":{"type":"boolean","default":false},"summary":{"type":"string"}}}}}},
"ComponentVersion": {"type":"object","required":["component","version"],"properties":{"component":{"type":"string","enum":["backend","frontend","ai","infra","contracts"]},"version":{"type":"string"},"imageDigest":{"type":"string","nullable":true}}},
"CreateReleaseRequest": {"type":"object","required":["version","components","note"],"properties":{"version":{"type":"string"},"components":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ComponentVersion"}},"requiredMigrations":{"type":"array","description":"Migration versions this release depends on.","items":{"type":"string"}},"note":{"type":"string","minLength":3,"maxLength":2000,"description":"Internal. Never shown to guests; `guestReleaseNotes` is."},"guestReleaseNotes":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"**The public, localised \"what's new\" for guests** (decided 29 September, rev 3 GAP-B2), one short text per locale, written for a guest and naming no person. Public once the release reaches the tenant's cell; read by the guest Help screen (WEB-025, WEB-045, GST-040) through `white-label.getTenantAppStatus`. Distinct from the staff-only `TenantAppStatus.recentChanges`, which names the principal behind each change and stays staff only.\n"},"breakingChanges":{"type":"array","items":{"type":"string"}}}},
"Environment": {"type":"object","x-ticvai-persistence":"control.environment","required":["id","kind","name"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/EnvironmentKind"},"name":{"type":"string"},"cellIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requiresApprovalToPromote":{"type":"boolean"},"soakHours":{"type":"integer","description":"How long a release must sit here before it may be promoted. Zero for dev; a real number for staging, or staging is a formality.\n"},"currentReleaseVersion":{"type":"string","nullable":true},"isActive":{"type":"boolean"}}},
"EnvironmentKind": {"type":"string","enum":["dev","staging","production"]},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"Migration": {"type":"object","x-ticvai-persistence":"control.migration","required":["version","module","isReversible","checksum"],"properties":{"version":{"type":"string"},"module":{"type":"string"},"description":{"type":"string"},"isReversible":{"type":"boolean","description":"A rollback section exists and CI has executed it against a restored snapshot. A rollback nobody has run is a comment, not a rollback.\n"},"rollbackTestedAt":{"type":"string","format":"date-time","nullable":true},"checksum":{"type":"string","description":"Compared on apply. A migration edited after it was applied somewhere is a defect the register catches, not a mystery to debug later.\n"},"estimatedLockMs":{"type":"integer","nullable":true},"touchesPartitionedTable":{"type":"boolean"},"appliedCellCount":{"type":"integer"},"pendingCellCount":{"type":"integer"}}},
"MigrationPlan": {"type":"object","x-ticvai-persistence":"control.migration_plan","required":["id","targetVersion","computedAt","cells","allReversible"],"properties":{"id":{"type":"string","format":"uuid"},"targetVersion":{"type":"string"},"computedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","description":"A plan is computed against cell state at a moment. Beyond this it is stale and apply refuses it rather than applying to a different world than it was made for.\n"},"allReversible":{"type":"boolean"},"irreversible":{"type":"array","items":{"type":"string"}},"totalEstimatedLockMs":{"type":"integer"},"cells":{"type":"array","items":{"type":"object","properties":{"cellId":{"type":"string","format":"uuid"},"cellName":{"type":"string"},"tenantSelection":{"type":"string","description":"Which of the cell's tenant databases the plan targets. **A plan that can only say \"this region\" cannot express the rollout ADR-0038 makes normal** — a cell is a region holding many tenants, and a wave may be a subset of one.","enum":["all","named"]},"tenantIds":{"type":"array","description":"Present only where `tenantSelection` is `named`. **Named rather than counted**, for the reason `migration_run_cell` gives about partial failure: a set recorded as a number cannot be checked against what actually ran.","items":{"type":"string","format":"uuid"}},"currentVersion":{"type":"string"},"migrationsToApply":{"type":"array","items":{"type":"string"}},"estimatedLockMs":{"type":"integer"},"warnings":{"type":"array","description":"A long lock on a partitioned table during trading hours is the output this endpoint exists to produce.\n","items":{"type":"string"}}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"MigrationRun": {"type":"object","x-ticvai-persistence":"control.migration_run + control.migration_run_cell + control.migration_run_tenant","description":"One run, its per-region rollup, and its per-tenant outcomes. **The third table exists because ADR-0038 made a cell a region holding many tenants**, and `migration_run_cell`'s own note says it is there so *\"a partial failure is named rather than counted\"* — which is exactly what it stopped doing. A run that fails for twenty of two hundred tenants had one row saying `failed`.\n\nThe rollup stays. *\"How is the UAE doing\"* is a real question and computing it from two hundred rows on every read is not.\n","required":["id","planId","status","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["queued","canary","running","paused","complete","failed","rolledBack"]},"canaryCellId":{"type":"string","format":"uuid","nullable":true,"description":"Which region the canary tenant is in. **The canary itself is a tenant** — a first cell holding two hundred databases is not a cheap failure, and cheap failure is the only thing a canary is for."},"canaryTenantId":{"type":"string","format":"uuid","nullable":true},"tenantsTotal":{"type":"integer"},"tenantsComplete":{"type":"integer"},"tenantsFailed":{"type":"integer"},"cellsTotal":{"type":"integer"},"cellsComplete":{"type":"integer"},"cellsFailed":{"type":"integer"},"startedByPrincipalId":{"type":"string","format":"uuid"},"startedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"cells":{"type":"array","items":{"$ref":"#/components/schemas/MigrationRunCell"}},"tenants":{"type":"array","items":{"$ref":"#/components/schemas/RolloutTenant"}}}},
"MigrationRunCell": {"type":"object","x-ticvai-persistence":"none — rows of control.migration_run_cell, stored through MigrationRun","description":"One cell's rollup within one migration run. **The fields of `RolloutCell` without its `rolloutId`**: a migration run is not a rollout, and its parent key `migration_run_id` comes from `MigrationRun.cells`.\n","required":["cellId","status"],"properties":{"cellId":{"type":"string","format":"uuid"},"cellName":{"type":"string"},"regionName":{"type":"string"},"countryCode":{"type":"string"},"isCanary":{"type":"boolean"},"wave":{"type":"integer"},"status":{"type":"string","enum":["pending","running","complete","failed","skipped","rolledBack"]},"fromVersion":{"type":"string","nullable":true},"toVersion":{"type":"string","nullable":true},"error":{"type":"string","nullable":true},"startedAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Release": {"allOf":[{"$ref":"#/components/schemas/CreateReleaseRequest"},{"type":"object","required":["id","status","createdAt"],"x-ticvai-persistence":"control.release + control.release_component","properties":{"id":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/ReleaseStatus"},"createdByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"promotedToStagingAt":{"type":"string","format":"date-time","nullable":true},"promotedToProductionAt":{"type":"string","format":"date-time","nullable":true}}}]},
"ReleaseDetail": {"allOf":[{"$ref":"#/components/schemas/Release"},{"type":"object","x-ticvai-persistence":"none — projection","properties":{"rollouts":{"type":"array","items":{"$ref":"#/components/schemas/Rollout"}},"cellsOnThisVersion":{"type":"integer"},"cellsTotal":{"type":"integer"}}}]},
"ReleaseReadiness": {"type":"object","x-ticvai-persistence":"none — computed","required":["releaseId","canPromote","gates"],"properties":{"releaseId":{"type":"string","format":"uuid"},"canPromote":{"type":"boolean"},"targetEnvironment":{"$ref":"#/components/schemas/EnvironmentKind"},"gates":{"type":"array","items":{"type":"object","required":["gate","passed"],"properties":{"gate":{"type":"string","enum":["priorEnvironmentHealthy","soakPeriodElapsed","migrationsReversible","noOpenIncidents","approvalRecorded","contractsCompatible"]},"passed":{"type":"boolean"},"detail":{"type":"string"}}}}}},
"ReleaseStatus": {"type":"string","enum":["draft","inDev","inStaging","inProduction","superseded","withdrawn"]},
"Rollout": {"type":"object","x-ticvai-persistence":"control.rollout","required":["id","releaseId","environment","status","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"releaseId":{"type":"string","format":"uuid"},"environment":{"$ref":"#/components/schemas/EnvironmentKind"},"status":{"$ref":"#/components/schemas/RolloutStatus"},"cellsTotal":{"type":"integer"},"cellsComplete":{"type":"integer"},"cellsFailed":{"type":"integer"},"startedByPrincipalId":{"type":"string","format":"uuid"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"pausedReason":{"type":"string","nullable":true},"startedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"RolloutTenant": {"type":"object","x-ticvai-persistence":"control.rollout_tenant","description":"What happened to one tenant database during one run. **The same shape as `RolloutCell` one level down**, and it serves the per-tenant rows of both a rollout and a migration run — the arrangement `RolloutCell` had with `rollout_cell` and `migration_run_cell` until `rollout_cell` needed its `rolloutId` parent key and the migration run's cells moved to `MigrationRunCell`.\n\n**`databaseName` is denormalised on purpose.** After a drop the run record still has to say what it touched, and a join to a row that no longer exists says nothing.\n","required":["tenantId","cellId","status"],"properties":{"tenantId":{"type":"string","format":"uuid"},"cellId":{"type":"string","format":"uuid"},"databaseName":{"type":"string"},"isCanary":{"type":"boolean"},"wave":{"type":"integer","description":"A wave is now a set of tenants and may be a subset of one cell."},"status":{"type":"string","enum":["pending","running","complete","failed","skipped","rolledBack"]},"fromVersion":{"type":"string","nullable":true},"toVersion":{"type":"string","nullable":true},"error":{"type":"string","nullable":true},"startedAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"SupportNotice": {"type":"object","x-ticvai-persistence":"control.support_notice","required":["id","version","supportEndsAt","publishedAt"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string"},"supportEndsAt":{"type":"string","format":"date"},"message":{"type":"object","additionalProperties":{"type":"string"}},"affectedTenantIds":{"type":"array","readOnly":true,"description":"Computed from cell versions, never typed. A notice to the wrong list is worse than none.","items":{"type":"string","format":"uuid"}},"publishedByPrincipalId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"UpgradeSchedule": {"type":"object","x-ticvai-persistence":"control.upgrade_schedule","required":["tenantId","releaseVersion","scheduledFor"],"properties":{"tenantId":{"type":"string","format":"uuid"},"tenantName":{"type":"string"},"releaseVersion":{"type":"string"},"scheduledFor":{"type":"string","format":"date-time"},"deferredByTenant":{"type":"boolean"},"deferralReason":{"type":"string","nullable":true},"maxDeferralUntil":{"type":"string","format":"date-time","description":"Beyond this the platform proceeds. An indefinitely deferred tenant becomes a version nobody supports.\n"},"notifiedAt":{"type":"string","format":"date-time","nullable":true}}},
"VersionSkewReport": {"type":"object","x-ticvai-persistence":"none — computed from cell state","required":["asAt","cells","hasUnexplainedSkew"],"properties":{"asAt":{"type":"string","format":"date-time"},"hasUnexplainedSkew":{"type":"boolean","description":"Skew during a rollout is expected. Skew outside one is a defect, and separating the two is the entire value of this report.\n**An on-premise cell is a third case: legitimately behind, indefinitely**, because the client has not scheduled the window and TICVAI cannot push. It is not counted here and must not appear as a defect (ADR-0017).\n"},"cells":{"type":"array","items":{"type":"object","properties":{"cellId":{"type":"string","format":"uuid"},"cellName":{"type":"string"},"schemaVersion":{"type":"string"},"applicationVersion":{"type":"string"},"isBehind":{"type":"boolean"},"versionsBehind":{"type":"integer"},"reason":{"type":"string","nullable":true,"enum":["midRollout","rolloutPaused","rolloutFailed","tenantDeferred","onPremiseNotScheduled","unexplained"]}}}}}}
}
```
