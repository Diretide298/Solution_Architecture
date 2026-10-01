# WS05 — Access Control board 5

**10 screens · 16 operations · 21 schemas · 5 permissions**

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
  `ACCESS_POINT_CONFIGURE, AUDIT_VIEW, GUEST_MANAGE, SCOPE_VIEW, TENANT_VIEW`. A control nobody can use must say so,
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
| `BO-184` | Biometric Access Command Center | A | 0 | 240 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-185` | Biometric Verification Profile Builder | B–D | 8 | 0 | 5 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-186` | Face Pass Enrollment Configuration | B–D | 8 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-187` | Biometric Consent & Guardian Management | B–D | 5 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-188` | Face Tag Temporary Enrollment | A | 10 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-189` | Face Matching & Verification Thresholds | A | 19 | 0 | 5 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-190` | Face Change, Re-enrollment & Identity Protection | B–D | 2 | 16 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-191` | Biometric Validation at Gate | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-192` | Biometric Lifecycle, Retention & Deletion | B–D | 9 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-193` | Biometric Simulation, Audit & Publication | B–D | 7 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |

## Thin screens in this batch

**BO-188, BO-190, BO-191 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-184` Biometric Access Command Center

**Central dashboard for biometric access configuration and operational health.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #20676 (APP-SETUP-BO-184) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/biometric-access-command-center-bo-184` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Face Pass Profiles** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Active Face Tags** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Enrollments Today** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Successful Face Verifications** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Failed Verifications** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Manual Reviews** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Re-enrollment Requests** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Blocked Face Changes** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Profiles Pending Deletion** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Camera/Reader Health** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Biometric Security Alerts** (metric tile, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**Every biometric access** (data table, from `listBiometricAccess`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile | text | — |
| Profile name | text | e.g. |
| Biometric type | chip: Face pass, Face tag | — |
| Credential type | text | e.g. |
| Venue scope | text | Venue or 'all parks' |
| Status | chip: Active, Inactive | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active face pass profiles | 1,234 | Active Face Pass Profiles |
| Active face tags | 1,234 | Active Face Tags |
| Enrollments today | 1,234 | Enrollments Today |
| Successful face verifications | 1,234 | Successful Face Verifications |
| Failed verifications | 1,234 | Failed Verifications |
| Manual reviews | 1,234 | Manual Reviews |
| Re enrollment requests | 1,234 | Re-enrollment Requests |
| Blocked face changes | 1,234 | Blocked Face Changes |
| Profiles pending deletion | 1,234 | Profiles Pending Deletion |
| Camera reader health | chip: Healthy, Degraded, Down | Camera/Reader Health |

**The selected biometric access** (detail panel): The pack groups this record's detail under its own headings: “Profile Type Credential Venue Status”.

**Data it reads**: `listBiometricAccess` (onLoad, Biometric Access Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-185` Biometric Verification Profile Builder: *Works in Biometric Verification Profile Builder*; calls `listBiometricAccess`
- → `BO-186` Face Pass Enrollment Configuration: *Works in Face Pass Enrollment Configuration*; calls `listBiometricAccess`
- → `BO-187` Biometric Consent & Guardian Management: *Works in Biometric Consent & Guardian Management*; calls `listBiometricAccess`
- → `BO-188` Face Tag Temporary Enrollment: *Works in Face Tag Temporary Enrollment*; calls `listBiometricAccess`
- → `BO-189` Face Matching & Verification Thresholds: *Works in Face Matching & Verification Thresholds*; calls `listBiometricAccess`
- → `BO-190` Face Change, Re-enrollment & Identity Protection: *Works in Face Change, Re-enrollment & Identity Protection*; calls `listBiometricAccess`
- → `BO-191` Biometric Validation at Gate: *Works in Biometric Validation at Gate*; calls `listBiometricAccess`
- → `BO-192` Biometric Lifecycle, Retention & Deletion: *Works in Biometric Lifecycle, Retention & Deletion*; calls `listBiometricAccess`
- → `BO-193` Biometric Simulation, Audit & Publication: *Works in Biometric Simulation, Audit & Publication*; calls `listBiometricAccess`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The biometric access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the biometric access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No biometric access yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the biometric access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listBiometricAccess` → `SCOPE_VIEW` (read) · staff
- `setBiometricVerificationProfile` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `setFacePassEnrollment` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-184` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-184`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 1: Opens Biometric Access Command Center → Central dashboard for biometric access configuration and operational health.
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F115 branch at step 1 (expected): when Nothing has been set up on Biometric Access Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F115 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (240 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-184?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-185`, `BO-186`, `BO-187`, `BO-188`, `BO-189`, `BO-190`, `BO-191`, `BO-192`, `BO-193`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-185` Biometric Verification Profile Builder

**Configure which ticket/credential types can or must use biometric verification. The matrix specifically requires biometric checks to be configurable by ticket type, including memberships, annual passes, multi-day and multi-attraction products.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/biometric-verification-profile-builder-bo-185` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Ticket Product | select field | — | — | — | — | — | — |
| Ticket Type | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Annual Pass | select field | — | — | — | — | — | — |
| Multi-Day Ticket | select field | — | — | — | — | — | — |
| Multi-Attraction Ticket | select field | — | — | — | — | — | — |
| VIP Credential | select field | — | — | — | — | — | — |
| Accreditation | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `setBiometricVerificationProfile`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The biometric verification profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the biometric verification profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No biometric verification profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setBiometricVerificationProfile` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-185` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-185`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 2: Works in Biometric Verification Profile Builder → Configure which ticket/credential types can or must use biometric verification. The matrix specifically requires biometric checks to be configurable by ticket type, including memberships, annual …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-185?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-186` Face Pass Enrollment Configuration

**Configure persistent Face Pass registration. The source specifies that Face Pass may be registered through the App, ticket counters or Annual Pass counter.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture Required Consent; Capture Face; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/face-pass-enrollment-configuration-bo-186` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| → | select field | — | — | — | — | — | — |
| Account login required | select field | — | — | — | — | — | — |
| Valid ticket/pass required | select field | — | — | — | — | — | — |
| Identity check required | select field | — | — | — | — | — | — |
| Number of capture attempts | text field | — | — | — | — | — | — |
| minimum image quality | select field | — | — | — | — | — | — |
| duplicate face detection | select field | — | — | — | — | — | — |
| operator verification | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `setFacePassEnrollment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The face pass enrollment configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the face pass enrollment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No face pass enrollment configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setFacePassEnrollment` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Two face credentials: Face Pass (long-term, renewable, for memberships/season passes) and Face Tag (short-lived, single day or event). Retention is venue-configurable per tier. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-640)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-186` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-186`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 4: Works in Face Pass Enrollment Configuration → Configure persistent Face Pass registration. The source specifies that Face Pass may be registered through the App, ticket counters or Annual Pass counter.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-186?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-187` Biometric Consent & Guardian Management

**Manage consent requirements associated with persistent biometric enrollment. The matrix requires App users to provide consent before Face Pass registration and requires guardian consent for minors. On-site enrollment also requires consent before facial data is captured.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure by) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/biometric-consent-guardian-management-bo-187` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Country/Jurisdiction | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Credential | select field | — | — | — | — | — | — |
| Enrollment Channel | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Country jurisdiction | text field | — | — | `listBiometricConsentGuardian` ?countryJurisdiction |
| Credential type | text field | — | — | `listBiometricConsentGuardian` ?credentialType |
| Enrollment channel | text field | — | — | `listBiometricConsentGuardian` ?enrollmentChannel |
| Guest category | text field | — | — | `listBiometricConsentGuardian` ?guestCategory |

#### Outputs: what the screen shows and produces

**Data it reads**: `listBiometricConsentGuardian` (onLoad, Biometric Consent & Guardian Management)

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `listBiometricConsentGuardian`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The biometric consent guardian configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the biometric consent guardian untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No biometric consent guardian configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listBiometricConsentGuardian` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Qossai: use an existing major venue-group client's live app and published privacy policy as the model for how facial-recognition consent, data use and retention are explained to guests. *(client request · MoM 2 Sep 2026, 4.11 Privacy & Biometric Data Retention · DI-642)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-187` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-187`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 6: Works in Biometric Consent & Guardian Management → Manage consent requirements associated with persistent biometric enrollment. The matrix requires App users to provide consent before Face Pass registration and requires guardian consent for minors. …

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-187?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-188` Face Tag Temporary Enrollment

**Configure the temporary biometric model separately from Face Pass. The matrix describes Face Tag as temporarily stored facial data, enrollable at ticket counters or entry gates, with biometric data permanently deleted once the associated ticket is fully redeemed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #20677 (APP-SETUP-BO-188) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Face Captured) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/face-tag-temporary-enrollment-bo-188` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| → | select field | — | — | — | — | — | — |

**Sent by *Save Face Tag profile*** (`setFaceTagTemporaryEnrollment`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Profile `profileId` | picker: choose a profile | optional | — | — | shows names, sends the id | Absent creates a Face Tag profile | `setFaceTagTemporaryEnrollment` body |
| Venue `venueId` | text field | required | — | — | — | — | `setFaceTagTemporaryEnrollment` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setFaceTagTemporaryEnrollment` body |
| Enrollment channels `enrollmentChannels` | multi-select chips | required | — | Ticket counter · Entry gate; at least 1 | — | Where a Face Tag may be captured | `setFaceTagTemporaryEnrollment` body |
| Bind to `bindTo` | segmented control | required | Ticket | Ticket · Visit · Temporary credential | — | What the Face Tag is bound to | `setFaceTagTemporaryEnrollment` body |
| Deletion trigger `deletionTrigger` | radio group | required | Ticket fully redeemed | Ticket fully redeemed · End of visit · Ticket expiration · Credential cancellation · Operational retention threshold | — | When the Face Tag is deleted automatically. | `setFaceTagTemporaryEnrollment` body |
| Retention threshold hours `retentionThresholdHours` | number field (hours) | optional | — | min 1; Used only when deletionTrigger is operationalRetentionThreshold, and then required. | — | Used only when deletionTrigger is operationalRetentionThreshold, and then required. | `setFaceTagTemporaryEnrollment` body |
| Consent capture `consentCapture` | segmented control | optional | On screen acknowledgement | On screen acknowledgement · Signed form | — | How consent is taken when a Face Tag is captured (3.2.44; added 29 September, build pass). | `setFaceTagTemporaryEnrollment` body |
| Status `status` | segmented control | optional | Active | Active · Inactive | — | Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass) | `setFaceTagTemporaryEnrollment` body |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save Face Tag profile (primary button) | `setFaceTagTemporaryEnrollment` PUT `/face-tag-temporary` | FaceTagTemporaryEnrollmentInput | FaceTagTemporaryEnrollmentView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 operationalRetentionThreshold chosen with no retentionThresholdHours | — |

**Data it reads**: `listFaceTagTemporary` (onLoad, Face Tag Temporary Enrollment)

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `listFaceTagTemporary`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The face tag temporary configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the face tag temporary untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No face tag temporary configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 operationalRetentionThreshold chosen with no retentionThresholdHours |

#### Permissions

- `listFaceTagTemporary` → `SCOPE_VIEW` (read) · staff
- `setFaceTagTemporaryEnrollment` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Two face credentials: Face Pass (long-term, renewable, for memberships/season passes) and Face Tag (short-lived, single day or event). Retention is venue-configurable per tier. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-640)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-188` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-188`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 8: Works in Face Tag Temporary Enrollment → Configure the temporary biometric model separately from Face Pass. The matrix describes Face Tag as temporarily stored facial data, enrollable at ticket counters or entry gates, with biometric data …

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-188?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save Face Tag profile.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-189` Face Matching & Verification Thresholds

**Configure biometric verification behavior. The source requires a configurable Biometric Check Level determining the scoring of biometric comparison.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #20678 (APP-SETUP-BO-189) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/face-matching-verification-thresholds-bo-189` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Liveness check | select field | — | — | — | — | — | — |
| Duplicate-face check | select field | — | — | — | — | — | — |
| image quality | select field | — | — | — | — | — | — |
| capture timeout | select field | — | — | — | — | — | — |
| retry quantity | select field | — | — | — | — | — | — |
| mask/obstruction handling | select field | — | — | — | — | — | — |

**Sent by *Save thresholds*** (`setFaceMatchingVerification`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Profile `profileId` | picker: choose a profile | optional | — | — | shows names, sends the id | Absent creates a threshold profile | `setFaceMatchingVerification` body |
| Venue `venueId` | text field | required | — | — | — | — | `setFaceMatchingVerification` body |
| Access context `accessContext` | text field | required | — | max length 100 | — | Where the thresholds apply, e.g. | `setFaceMatchingVerification` body |
| High confidence min `highConfidenceMin` | stepper or slider | required | — | min 0; max 1 | — | Score at or above which the match is high confidence (allow if every other rule passes) | `setFaceMatchingVerification` body |
| Review range min `reviewRangeMin` | stepper or slider | required | — | min 0; max 1 | — | Score at or above which the match goes to operator review; below it is denied. | `setFaceMatchingVerification` body |
| Retry quantity `retryQuantity` | stepper or slider | optional | 2 | min 0; max 5 | — | — | `setFaceMatchingVerification` body |
| Liveness check `livenessCheck` | toggle | optional | on | — | — | — | `setFaceMatchingVerification` body |
| Duplicate face check `duplicateFaceCheck` | toggle | optional | on | — | — | — | `setFaceMatchingVerification` body |
| Image quality `imageQuality` | segmented control | optional | Medium | Low · Medium · High | — | Minimum image quality accepted | `setFaceMatchingVerification` body |
| Capture timeout `captureTimeout` | stepper or slider | optional | 10 | min 1; max 60 | — | Seconds | `setFaceMatchingVerification` body |
| Mask obstruction handling `maskObstructionHandling` | segmented control | optional | Operator review | Deny · Operator review · Fallback method | — | — | `setFaceMatchingVerification` body |
| Operator fallback `operatorFallback` | toggle | optional | on | — | — | Review-range results go to operator verification | `setFaceMatchingVerification` body |
| Status `status` | segmented control | optional | Active | Active · Inactive | — | Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass) | `setFaceMatchingVerification` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save thresholds (primary button) | `setFaceMatchingVerification` PUT `/face-matching-verification` | FaceMatchingVerificationThresholdsInput | FaceMatchingVerificationThresholdsView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 reviewRangeMin is not below highConfidenceMin | — |

**Data it reads**: `listFaceMatchingVerification` (onLoad, Face Matching & Verification Thresholds)

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `listFaceMatchingVerification`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The face matching verification configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the face matching verification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No face matching verification configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 reviewRangeMin is not below highConfidenceMin |

#### Permissions

- `listFaceMatchingVerification` → `SCOPE_VIEW` (read) · staff
- `setFaceMatchingVerification` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-189` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-189`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 10: Works in Face Matching & Verification Thresholds → Configure biometric verification behavior. The source requires a configurable Biometric Check Level determining the scoring of biometric comparison.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-189?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save thresholds.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-190` Face Change, Re-enrollment & Identity Protection

**Prevent guests from replacing a registered biometric identity with another person's face. The source explicitly states that customers may re-register Face Pass, but the system must compare the new facial data with the previous profile. If the difference exceeds an acceptable threshold, the update is blocked and venue assistance is required.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `attemptId` (navigation) |
| Route | `/access-venue/face-change-re-enrollment-identity-protection-bo-190` |

#### Inputs: what the user enters or picks

**Form: Review face reenrolment** (modal, opened by *Review face reenrolment*; *Review face reenrolment* calls `reviewFaceReenrolment`, *Cancel* sends nothing)

**Collects what `reviewFaceReenrolment` sends before it is called.** Required: `decision`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | segmented control | required | — | Approve · Block | — | — | `reviewFaceReenrolment` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `reviewFaceReenrolment` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `not-pending`: the attempt is not awaiting review.

#### Outputs: what the screen shows and produces

**Shown**

**Every face change re-enrollment** (data table, from `listFaceChangeEnrollment`)

| Shows | Format | Notes |
|---|---|---|
| Existing profile reference | text | Existing profile reference |
| New capture reference | text | New capture reference |
| Match result | chip: Within policy, Significant difference | match result |
| Credential | text | credential |
| Guest | text | guest |
| Reason for re enrollment | chip: Appearance change, Poor original capture, Technical issue, Guest request, Recovery … | reason for re-enrollment |
| Previous changes | 1,234 | previous changes |
| Operator | text | operator |

**The selected face change re-enrollment** (detail panel): The pack groups this record's detail under its own headings: “Current Face”, “SIGNIFICANT IDENTITY DIFFERENCE”, “CHANGE BLOCKED”, “Change Reasons”.

| Shows | Format | Notes |
|---|---|---|
| Existing profile reference | text | Existing profile reference |
| New capture reference | text | New capture reference |
| Match result | chip: Within policy, Significant difference | match result |
| Credential | text | credential |
| Guest | text | guest |
| Reason for re enrollment | chip: Appearance change, Poor original capture, Technical issue, Guest request, Recovery … | reason for re-enrollment |
| Previous changes | 1,234 | previous changes |
| Operator | text | operator |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Review face reenrolment (primary button) | `reviewFaceReenrolment` POST `/face-reenrolment-attempts/{attemptId}/review` | inline | AccessFaceReenrolmentAttempt | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `GUEST_MANAGE`; opens modal first |

**Data it reads**: `listFaceChangeEnrollment` (onLoad, Face Change, Re-enrollment & Identity Protection)

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `listFaceChangeEnrollment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The face change re-enrollment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the face change re-enrollment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No face change re-enrollment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the face change re-enrollment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `not-pending`: the attempt is not awaiting review. |

#### Permissions

- `listFaceChangeEnrollment` → `SCOPE_VIEW` (read) · staff
- `reviewFaceReenrolment` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-190` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-190`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 12: Works in Face Change, Re-enrollment & Identity Protection → Prevent guests from replacing a registered biometric identity with another person's face. The source explicitly states that customers may re-register Face Pass, but the system must compare the new …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-190?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Review face reenrolment.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-191` Biometric Validation at Gate

**Configure how facial verification interacts with the physical access-control journey.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/biometric-validation-at-gate-bo-191` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listBiometricValidationGate` (onLoad, Biometric Validation at Gate)

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `listBiometricValidationGate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The biometric validation gate list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the biometric validation gate untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No biometric validation gate yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the biometric validation gate are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listBiometricValidationGate` → `SCOPE_VIEW` (read) · staff
- `setBiometricVerificationProfile` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-191` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-191`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 14: Works in Biometric Validation at Gate → Configure how facial verification interacts with the physical access-control journey.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-191?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-192` Biometric Lifecycle, Retention & Deletion

**Manage biometric-data lifecycle and deletion rules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`, `TENANT_VIEW` (1 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure separately for) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/biometric-lifecycle-retention-deletion-bo-192` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Face Pass | select field | — | — | — | — | — | — |
| Face Tag | select field | — | — | — | — | — | — |
| Failed enrollment captures | select field | — | — | — | — | — | — |
| abandoned registrations | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Data class | select | — | Guest profile · Payment record · Financial record · Audit record · Approval record · Compliance inspection · Face tag biometric · Face pass biometric · AI prompts · AI conversations · AI decision records · AI metadata index | `listDataRetentionSettings` ?dataClass |

**Sent by *Save retention rule*** (`setBiometricLifecycleRetention`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Policy `policyId` | picker: choose a policy | optional | — | — | shows names, sends the id | Absent creates a retention rule | `setBiometricLifecycleRetention` body |
| Venue `venueId` | text field | required | — | — | — | — | `setBiometricLifecycleRetention` body |
| Data category `dataCategory` | radio group | required | — | Face pass · Face tag · Failed enrollment captures · Abandoned registrations · Temporary captures | — | Biometric data category this rule governs | `setBiometricLifecycleRetention` body |
| Retention days `retentionDays` | number field (days) | required | — | min 0 | — | Maximum retention in days. | `setBiometricLifecycleRetention` body |
| Deletion trigger `deletionTrigger` | select | required | — | Deletion request · Ticket fully redeemed · End of visit · Ticket expiration · Membership ended · Capture failed · Registration abandoned | — | Event that starts the retention clock | `setBiometricLifecycleRetention` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save retention rule (primary button) | `setBiometricLifecycleRetention` PUT `/biometric-lifecycle-retention` | BiometricLifecycleRetentionDeletionInput | BiometricLifecycleRetentionDeletionView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A second rule for the same venue and data category; 422 `retentionDays` longer than the tenant's effective … | step-up: mfa (Sets how long biometric data is kept; a wrong value is a data protection breach.) |

**Data it reads**: `listBiometricLifecycleRetention` (onLoad, Biometric Lifecycle, Retention & Deletion); `listDataRetentionSettings` (onLoad, Tenant biometric retention and its legal limit)

**Where the user goes next**

- → `BO-184` Biometric Access Command Center: *Returns to the board's landing screen*; calls `listBiometricLifecycleRetention`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The biometric lifecycle retention configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the biometric lifecycle retention untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No biometric lifecycle retention configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A second rule for the same venue and data category; 422 `retentionDays` longer than the tenant's effective `faceTagBiometric` or `facePassBiometric` period (tenancy `setDataRetentionSetting`); a rule here may only … |

#### Permissions

- `listBiometricLifecycleRetention` → `SCOPE_VIEW` (read) · staff
- `setBiometricLifecycleRetention` → `ACCESS_POINT_CONFIGURE` (configure) · staff · step-up mfa
- `listDataRetentionSettings` → `TENANT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Two face credentials: Face Pass (long-term, renewable, for memberships/season passes) and Face Tag (short-lived, single day or event). Retention is venue-configurable per tier. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-640)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-192` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-192`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 16: Works in Biometric Lifecycle, Retention & Deletion → Manage biometric-data lifecycle and deletion rules.
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-192?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save retention rule.
- [ ] Every transition is wired: `BO-184`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`, `TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-193` Biometric Simulation, Audit & Publication

**Test biometric configurations before live deployment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `AUDIT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/biometric-simulation-audit-publication-bo-193` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search biometric simulation audit | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by guest, credential, face profile reference, gate, device, operator and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Guest | text field | — | — | `listBiometric` ?guest |
| Credential | text field | — | — | `listBiometric` ?credential |
| Face profile reference | text field | — | — | `listBiometric` ?faceProfileReference |
| Gate | text field | — | — | `listBiometric` ?gate |
| Device | text field | — | — | `listBiometric` ?device |
| Operator | text field | — | — | `listBiometric` ?operator |
| Date | text field | — | — | `listBiometric` ?date |
| Result | text field | — | — | `listBiometric` ?result |
| Reason code | text field | — | — | `listBiometric` ?reasonCode |

**Sent by *Run simulation*** (`simulateBiometricConfiguration`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scenario `scenario` | select | required | — | Valid face pass · Face mismatch · No biometric profile · Low confidence match · Liveness failure · Duplicate profile · Re enrollment attempt · Child assigned adult · Face tag expired · Face tag deleted · Offline biometric · Camera unavailable … | — | — | `simulateBiometricConfiguration` body |
| Venue `venueId` | text field | required | — | — | — | — | `simulateBiometricConfiguration` body |
| Gate group `gateGroupId` | text field | optional | — | — | — | Empty simulates at every gate group of the venue | `simulateBiometricConfiguration` body |
| Credential type `credentialType` | text field | optional | — | — | — | — | `simulateBiometricConfiguration` body |
| Profile `profileId` | text field | optional | — | — | — | The draft biometric verification profile to test; empty tests the published one | `simulateBiometricConfiguration` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Low-confidence match (primary button) | navigation or local | — | — | — | — |
| Duplicate profile (secondary button) | navigation or local | — | — | — | — |
| Run simulation (primary button) | `simulateBiometricConfiguration` POST `/biometric/simulate` | BiometricSimulationInput | BiometricSimulationAuditPublicationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Data it reads**: `listBiometric` (onLoad, Biometric Simulation, Audit & Publication)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The biometric simulation audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the biometric simulation audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No biometric simulation audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the biometric simulation audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listBiometric` → `AUDIT_VIEW` (read) · staff
- `simulateBiometricConfiguration` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-193` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS22 Access Control Board 5.dc.html#bo-193`
- Workshop pack: Access Control Module_Reference.pdf board 5
- Flow F115 *Access Control board 5: Biometric Access Command Center*, step 18: Works in Biometric Simulation, Audit & Publication → Test biometric configurations before live deployment.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-193?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Low-confidence match, Duplicate profile, Run simulation.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `AUDIT_VIEW`.
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

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listBiometric": {"method":"GET","path":"/biometric","contract":"access","summary":"Biometric Simulation, Audit & Publication","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"guest","in":"query","required":false},{"name":"credential","in":"query","required":false},{"name":"faceProfileReference","in":"query","required":false},{"name":"gate","in":"query","required":false},{"name":"device","in":"query","required":false},{"name":"operator","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"result","in":"query","required":false},{"name":"reasonCode","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBiometricAccess": {"method":"GET","path":"/biometric-access","contract":"access","summary":"Biometric Access Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBiometricConsentGuardian": {"method":"GET","path":"/biometric-consent-guardian","contract":"access","summary":"Biometric Consent & Guardian Management","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"countryJurisdiction","in":"query","required":false},{"name":"tenantId","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"credentialType","in":"query","required":false},{"name":"enrollmentChannel","in":"query","required":false},{"name":"guestCategory","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBiometricLifecycleRetention": {"method":"GET","path":"/biometric-lifecycle-retention","contract":"access","summary":"Biometric Lifecycle, Retention & Deletion","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BiometricLifecycleRetentionDeletionView"},
"listBiometricValidationGate": {"method":"GET","path":"/biometric-validation-gate","contract":"access","summary":"Biometric Validation at Gate","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BiometricValidationAtGateView"},
"listDataRetentionSettings": {"method":"GET","path":"/data-retention-settings","contract":"tenancy","summary":"How long the tenant keeps each class of data","permission":"TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"dataClass","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFaceChangeEnrollment": {"method":"GET","path":"/face-change-enrollment","contract":"access","summary":"Face Change, Re-enrollment & Identity Protection","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFaceMatchingVerification": {"method":"GET","path":"/face-matching-verification","contract":"access","summary":"Face Matching & Verification Thresholds","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FaceMatchingVerificationThresholdsView"},
"listFaceTagTemporary": {"method":"GET","path":"/face-tag-temporary","contract":"access","summary":"Face Tag Temporary Enrollment","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FaceTagTemporaryEnrollmentView"},
"reviewFaceReenrolment": {"method":"POST","path":"/face-reenrolment-attempts/{attemptId}/review","contract":"access","summary":"Review a blocked Face Pass re-enrolment","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessFaceReenrolmentAttempt"},
"setBiometricLifecycleRetention": {"method":"PUT","path":"/biometric-lifecycle-retention","contract":"access","summary":"Save a biometric retention rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BiometricLifecycleRetentionDeletionInput","responds":"BiometricLifecycleRetentionDeletionView"},
"setBiometricVerificationProfile": {"method":"PUT","path":"/biometric-verification-profile","contract":"access","summary":"Biometric Verification Profile Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BiometricVerificationProfileBuilderInput","responds":"BiometricVerificationProfileBuilderView"},
"setFaceMatchingVerification": {"method":"PUT","path":"/face-matching-verification","contract":"access","summary":"Save face matching and verification thresholds","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FaceMatchingVerificationThresholdsInput","responds":"FaceMatchingVerificationThresholdsView"},
"setFacePassEnrollment": {"method":"PUT","path":"/face-pass-enrollment","contract":"access","summary":"Face Pass Enrollment Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FacePassEnrollmentConfigurationInput","responds":"FacePassEnrollmentConfigurationView"},
"setFaceTagTemporaryEnrollment": {"method":"PUT","path":"/face-tag-temporary","contract":"access","summary":"Save a Face Tag profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FaceTagTemporaryEnrollmentInput","responds":"FaceTagTemporaryEnrollmentView"},
"simulateBiometricConfiguration": {"method":"POST","path":"/biometric/simulate","contract":"access","summary":"Run a biometric scenario before publishing","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BiometricSimulationInput","responds":"BiometricSimulationAuditPublicationView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessFaceReenrolmentAttempt": {"type":"object","x-ticvai-persistence":"access.face_reenrolment_attempt","description":"One Face Pass re-enrolment attempt - the existing and new capture references (opaque, never templates), the match result, the reason, the operator and the outcome, with the review of a blocked change (declared 29 September, data-model close-out DM1). Written by enrolFacePass when the subject already has a Face Pass; a pendingReview attempt is decided by reviewFaceReenrolment (decided 29 September, writers pass).","required":["id","venueId","scopePath","subjectId","existingProfileReference","newCaptureReference","matchResult","outcome","attemptedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The attemptId the list shows"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"subjectId":{"type":"string","format":"uuid","description":"The guest (pii.subject)"},"entitlementId":{"type":"string","format":"uuid","nullable":true,"description":"The credential the Face Pass belongs to"},"existingProfileReference":{"type":"string","maxLength":200,"description":"Opaque reference to the prior enrolment (pii.subject_biometric)"},"newCaptureReference":{"type":"string","maxLength":200,"description":"Opaque reference to the new capture"},"matchResult":{"type":"string","enum":["withinPolicy","significantDifference"]},"reasonForReEnrollment":{"type":"string","enum":["appearanceChange","poorOriginalCapture","technicalIssue","guestRequest","recovery","other"],"nullable":true},"verificationProcess":{"type":"string","maxLength":200,"nullable":true,"description":"How the guest was verified for the change"},"operatorPrincipalId":{"type":"string","format":"uuid","nullable":true},"outcome":{"type":"string","enum":["updated","blocked","pendingReview"]},"reviewedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Security or guest service reviewer of a blocked change (the integrity screen's approval)"},"reviewedAt":{"type":"string","format":"date-time","nullable":true},"attemptedAt":{"type":"string","format":"date-time"}}},
"BiometricAccessCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Biometric Access Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"profileId":{"type":"string"},"profileName":{"type":"string","description":"e.g. Annual Pass Face"},"biometricType":{"type":"string","enum":["facePass","faceTag"]},"credentialType":{"type":"string","description":"e.g. Annual Pass, Membership, Day Ticket"},"venueScope":{"type":"string","description":"Venue or 'all parks'"},"status":{"type":"string","enum":["active","inactive"]}}},
"BiometricAccessCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"activeFacePassProfiles":{"type":"integer","description":"Active Face Pass Profiles"},"activeFaceTags":{"type":"integer","description":"Active Face Tags"},"enrollmentsToday":{"type":"integer","description":"Enrollments Today"},"successfulFaceVerifications":{"type":"integer","description":"Successful Face Verifications"},"failedVerifications":{"type":"integer","description":"Failed Verifications"},"manualReviews":{"type":"integer","description":"Manual Reviews"},"reEnrollmentRequests":{"type":"integer","description":"Re-enrollment Requests"},"blockedFaceChanges":{"type":"integer","description":"Blocked Face Changes"},"profilesPendingDeletion":{"type":"integer","description":"Profiles Pending Deletion"},"cameraReaderHealth":{"type":"string","enum":["healthy","degraded","down"],"description":"Camera/Reader Health"},"biometricSecurityAlerts":{"type":"integer","description":"Biometric Security Alerts"},"ai":{"type":"array","items":{"type":"string"},"description":"Advisory AI findings (abnormal failure rates, suspicious re-enrolments, camera quality). Read-only; AI does not decide access."}}},
"BiometricConsentGuardianManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Biometric Consent & Guardian Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venue":{"type":"string","description":"Venue"},"consentRecordId":{"type":"string","description":"Consent record ID"},"policyVersion":{"type":"string","description":"Policy/version"},"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"channel":{"type":"string","description":"Channel"},"guardianReference":{"type":"string","description":"Guardian reference where applicable"},"operatorId":{"type":"string","description":"Operator where applicable"},"withdrawalDeletionStatus":{"type":"string","enum":["active","withdrawn","biometricDeleted"],"description":"withdrawal/deletion status"},"guestId":{"type":"string"}}},
"BiometricLifecycleRetentionDeletionInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Biometric Lifecycle, Retention & Deletion submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["venueId","dataCategory","retentionDays","deletionTrigger"],"properties":{"policyId":{"type":"string","format":"uuid","description":"Absent creates a retention rule"},"venueId":{"type":"string"},"dataCategory":{"type":"string","enum":["facePass","faceTag","failedEnrollmentCaptures","abandonedRegistrations","temporaryCaptures"],"description":"Biometric data category this rule governs"},"retentionDays":{"type":"integer","minimum":0,"description":"Maximum retention in days. **No default and no maximum here on purpose**: the lawful period per region is the client counsel's value (make-or-break (a), see the operation)"},"deletionTrigger":{"type":"string","enum":["deletionRequest","ticketFullyRedeemed","endOfVisit","ticketExpiration","membershipEnded","captureFailed","registrationAbandoned"],"description":"Event that starts the retention clock"}}},
"BiometricLifecycleRetentionDeletionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Biometric Lifecycle, Retention & Deletion displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"dataCategory":{"type":"string","enum":["facePass","faceTag","failedEnrollmentCaptures","abandonedRegistrations","temporaryCaptures"],"description":"Biometric data category this retention rule governs"},"policyId":{"type":"string"},"venueId":{"type":"string"},"retentionDays":{"type":"integer","description":"Maximum retention in days; value set per region once confirmed. No default (make-or-break (a), see `setBiometricLifecycleRetention`)"},"deletionTrigger":{"type":"string","enum":["deletionRequest","ticketFullyRedeemed","endOfVisit","ticketExpiration","membershipEnded","captureFailed","registrationAbandoned"],"description":"Event that starts the retention clock (decided 29 September, VM close-out)"}}},
"BiometricSimulationAuditPublicationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Biometric Simulation, Audit & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"scenario":{"type":"string","enum":["validFacePass","faceMismatch","noBiometricProfile","lowConfidenceMatch","livenessFailure","duplicateProfile","reEnrollmentAttempt","childAssignedAdult","faceTagExpired","faceTagDeleted","offlineBiometric","cameraUnavailable","alternativeVerificationFallback"],"description":"Simulated scenario (simulation rows only)"},"eventId":{"type":"string"},"occurredAt":{"type":"string","format":"date-time"},"isSimulation":{"type":"boolean"},"guestId":{"type":"string"},"credentialId":{"type":"string"},"faceProfileReference":{"type":"string"},"gateId":{"type":"string"},"deviceId":{"type":"string"},"operatorId":{"type":"string"},"result":{"type":"string","enum":["allowed","review","denied"]},"reasonCode":{"type":"string"},"decisionTrace":{"type":"array","items":{"type":"string"},"description":"Checks passed or failed, e.g. face profile active, match policy satisfied, ticket valid"}}},
"BiometricSimulationInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"One simulated biometric validation, run before a biometric profile is published (decided 29 September, VM close-out).","required":["scenario","venueId"],"properties":{"scenario":{"type":"string","enum":["validFacePass","faceMismatch","noBiometricProfile","lowConfidenceMatch","livenessFailure","duplicateProfile","reEnrollmentAttempt","childAssignedAdult","faceTagExpired","faceTagDeleted","offlineBiometric","cameraUnavailable","alternativeVerificationFallback"]},"venueId":{"type":"string"},"gateGroupId":{"type":"string","description":"Empty simulates at every gate group of the venue"},"credentialType":{"type":"string"},"profileId":{"type":"string","description":"The draft biometric verification profile to test; empty tests the published one"}}},
"BiometricValidationAtGateView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Biometric Validation at Gate displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"accessPointId":{"type":"string"},"outcome":{"type":"string","enum":["green","yellow","red"]},"conditions":{"type":"array","items":{"type":"string"},"description":"Conditions that give this outcome, e.g. uncertain match, face mismatch, revoked profile"},"outcomeProfileId":{"type":"string","description":"Gate response profile from the validation outcome designer"},"exitCaptureEnabled":{"type":"boolean","description":"Face capture at exit records exit time"}}},
"BiometricVerificationProfileBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Biometric Verification Profile Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"faceRequirement":{"type":"string","enum":["notUsed","optional","required"],"description":"Whether face verification is not used, allowed, or required at this location (e.g. main entry required, attractions credential only)"},"biometricType":{"type":"string","enum":["facePass","faceTag","otherProvider"],"description":"Biometric model this profile uses"},"profileId":{"type":"string","description":"The profile row's key (access.biometric_profile.id, a UUIDv7); absent creates one (decided 29 September, writers pass)","format":"uuid"},"selectType":{"type":"string","enum":["ticketProduct","ticketType","membership","annualPass","multiDayTicket","multiAttractionTicket","vipCredential","accreditation","selectedCustomerSegments"],"description":"Vocabulary listed under Select."},"venueId":{"type":"string","description":"Venue"},"parkId":{"type":"string","description":"Park"},"zoneId":{"type":"string","description":"Zone"},"attractionId":{"type":"string","description":"Attraction"},"gateId":{"type":"string","description":"Gate"},"name":{"type":"string"},"status":{"type":"string","enum":["active","inactive"],"default":"active","description":"Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass)"}},"required":["profileId","venueId","selectType","biometricType","faceRequirement"]},
"BiometricVerificationProfileBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Biometric Verification Profile Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"faceRequirement":{"type":"string","enum":["notUsed","optional","required"],"description":"Whether face verification is not used, allowed, or required at this location (e.g. main entry required, attractions credential only)"},"biometricType":{"type":"string","enum":["facePass","faceTag","otherProvider"],"description":"Biometric model this profile uses"},"profileId":{"type":"string","description":"Biometric verification profile identifier"},"selectType":{"type":"string","enum":["ticketProduct","ticketType","membership","annualPass","multiDayTicket","multiAttractionTicket","vipCredential","accreditation","selectedCustomerSegments"],"description":"Vocabulary listed under Select."},"venueId":{"type":"string","description":"Venue"},"parkId":{"type":"string","description":"Park"},"zoneId":{"type":"string","description":"Zone"},"attractionId":{"type":"string","description":"Attraction"},"gateId":{"type":"string","description":"Gate"},"name":{"type":"string"}},"required":["profileId","venueId","selectType","biometricType","faceRequirement"]},
"FaceChangeReEnrollmentIdentityProtectionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Face Change, Re-enrollment & Identity Protection displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"existingProfileReference":{"type":"string","description":"Existing profile reference"},"newCaptureReference":{"type":"string","description":"New capture reference"},"matchResult":{"type":"string","enum":["withinPolicy","significantDifference"],"description":"match result"},"credentialId":{"type":"string","description":"credential"},"guestId":{"type":"string","description":"guest"},"reasonForReEnrollment":{"type":"string","enum":["appearanceChange","poorOriginalCapture","technicalIssue","guestRequest","recovery","other"],"description":"reason for re-enrollment"},"previousChanges":{"type":"integer","description":"previous changes"},"operatorId":{"type":"string","description":"operator"},"attemptId":{"type":"string"},"attemptedAt":{"type":"string","format":"date-time"},"outcome":{"type":"string","enum":["updated","blocked","pendingReview"]}}},
"FaceMatchingVerificationThresholdsInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Face Matching & Verification Thresholds submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back. Proposed defaults are ours (our build plan); the scores are a 0-1 scale whatever the face vendor reports, normalised by the adapter (R077).","required":["venueId","accessContext","highConfidenceMin","reviewRangeMin"],"properties":{"profileId":{"type":"string","format":"uuid","description":"Absent creates a threshold profile"},"venueId":{"type":"string"},"accessContext":{"type":"string","maxLength":100,"description":"Where the thresholds apply, e.g. main entry, child protection"},"highConfidenceMin":{"type":"number","minimum":0,"maximum":1,"description":"Score at or above which the match is high confidence (allow if every other rule passes)"},"reviewRangeMin":{"type":"number","minimum":0,"maximum":1,"description":"Score at or above which the match goes to operator review; below it is denied. Must be below highConfidenceMin"},"retryQuantity":{"type":"integer","minimum":0,"maximum":5,"default":2},"livenessCheck":{"type":"boolean","default":true},"duplicateFaceCheck":{"type":"boolean","default":true},"imageQuality":{"type":"string","enum":["low","medium","high"],"default":"medium","description":"Minimum image quality accepted"},"captureTimeout":{"type":"integer","minimum":1,"maximum":60,"default":10,"description":"Seconds"},"maskObstructionHandling":{"type":"string","enum":["deny","operatorReview","fallbackMethod"],"default":"operatorReview"},"operatorFallback":{"type":"boolean","default":true,"description":"Review-range results go to operator verification"},"status":{"type":"string","enum":["active","inactive"],"default":"active","description":"Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass)"}}},
"FaceMatchingVerificationThresholdsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Face Matching & Verification Thresholds displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"livenessCheck":{"type":"boolean","description":"Liveness check"},"duplicateFaceCheck":{"type":"boolean","description":"Duplicate-face check"},"imageQuality":{"type":"string","enum":["low","medium","high"],"description":"Minimum image quality accepted (decided 29 September, VM close-out)"},"captureTimeout":{"type":"integer","description":"Seconds"},"maskObstructionHandling":{"type":"string","enum":["deny","operatorReview","fallbackMethod"],"description":"What a masked or obstructed face leads to (decided 29 September, VM close-out)"},"operatorFallback":{"type":"boolean","description":"Review-range results go to operator verification"},"profileId":{"type":"string"},"venueId":{"type":"string"},"accessContext":{"type":"string","description":"Where the thresholds apply, e.g. main entry, child protection"},"highConfidenceMin":{"type":"number","description":"Score at or above which the match is high confidence (allow if all other rules pass)"},"reviewRangeMin":{"type":"number","description":"Score at or above which the match goes to operator review; below it is denied"},"retryQuantity":{"type":"integer"}}},
"FacePassEnrollmentConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Face Pass Enrollment Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"venueId":{"type":"string","description":"Venue this enrolment configuration applies to"},"enrollmentChannels":{"type":"array","items":{"type":"string","enum":["ticvaiApp","ticketCounter","annualPassCounter","selfServiceKiosk","otherAuthorizedChannel"]},"description":"Channels where Face Pass enrolment is enabled"},"accountLoginRequired":{"type":"boolean","description":"Account login required"},"validTicketPassRequired":{"type":"boolean","description":"Valid ticket/pass required"},"identityCheckRequired":{"type":"boolean","description":"Identity check required"},"numberOfCaptureAttempts":{"type":"integer","description":"Number of capture attempts"},"minimumImageQuality":{"type":"string","description":"minimum image quality"},"operatorVerification":{"type":"boolean","description":"An operator must verify the capture"},"enrollmentExpiry":{"type":"integer","description":"Days an enrolment stays valid before re-enrolment is needed"},"duplicateFaceDetection":{"type":"boolean","description":"Block a face already associated with another annual pass"},"status":{"type":"string","enum":["active","inactive"],"default":"active","description":"Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass)"}},"required":["venueId"]},
"FacePassEnrollmentConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Face Pass Enrollment Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string","description":"Venue this enrolment configuration applies to"},"enrollmentChannels":{"type":"array","items":{"type":"string","enum":["ticvaiApp","ticketCounter","annualPassCounter","selfServiceKiosk","otherAuthorizedChannel"]},"description":"Channels where Face Pass enrolment is enabled"},"accountLoginRequired":{"type":"boolean","description":"Account login required"},"validTicketPassRequired":{"type":"boolean","description":"Valid ticket/pass required"},"identityCheckRequired":{"type":"boolean","description":"Identity check required"},"numberOfCaptureAttempts":{"type":"integer","description":"Number of capture attempts"},"minimumImageQuality":{"type":"string","description":"minimum image quality"},"operatorVerification":{"type":"boolean","description":"An operator must verify the capture"},"enrollmentExpiry":{"type":"integer","description":"Days an enrolment stays valid before re-enrolment is needed"},"duplicateFaceDetection":{"type":"boolean","description":"Block a face already associated with another annual pass"}},"required":["venueId"]},
"FaceTagTemporaryEnrollmentInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Face Tag Temporary Enrollment submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["venueId","name","enrollmentChannels","bindTo","deletionTrigger"],"properties":{"profileId":{"type":"string","format":"uuid","description":"Absent creates a Face Tag profile"},"venueId":{"type":"string"},"name":{"type":"string","maxLength":200},"enrollmentChannels":{"type":"array","items":{"type":"string","enum":["ticketCounter","entryGate"]},"minItems":1,"description":"Where a Face Tag may be captured"},"bindTo":{"type":"string","enum":["ticket","visit","temporaryCredential"],"default":"ticket","description":"What the Face Tag is bound to"},"deletionTrigger":{"type":"string","enum":["ticketFullyRedeemed","endOfVisit","ticketExpiration","credentialCancellation","operationalRetentionThreshold"],"default":"ticketFullyRedeemed","description":"When the Face Tag is deleted automatically. The matrix: deleted once the ticket is fully redeemed"},"retentionThresholdHours":{"type":"integer","minimum":1,"description":"Used only when deletionTrigger is operationalRetentionThreshold, and then required. **No default and no maximum here on purpose**: the longest lawful period is the client counsel's value (make-or-break (a), see the operation)"},"consentCapture":{"type":"string","enum":["onScreenAcknowledgement","signedForm"],"default":"onScreenAcknowledgement","description":"How consent is taken when a Face Tag is captured (3.2.44; added 29 September, build pass). `onScreenAcknowledgement` is a tap on the counter or gate screen after the notice: explicit, recorded, and no form to sign, which is what the matrix asks. `signedForm` for a venue that wants one. A notice-only capture is not offered (make-or-break on `enrolFaceTag`, CF-35)."},"status":{"type":"string","enum":["active","inactive"],"default":"active","description":"Switches the profile on or off; an inactive profile is not applied at any gate and stays for reuse (decided 29 September, writers pass)"}}},
"FaceTagTemporaryEnrollmentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Face Tag Temporary Enrollment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"enrollmentChannels":{"type":"array","items":{"type":"string","enum":["ticketCounter","entryGate"]},"description":"Where a Face Tag may be captured"},"bindTo":{"type":"string","enum":["ticket","visit","temporaryCredential"],"description":"What the Face Tag is bound to"},"deletionTrigger":{"type":"string","enum":["ticketFullyRedeemed","endOfVisit","ticketExpiration","credentialCancellation","operationalRetentionThreshold"],"description":"When the Face Tag is automatically deleted; default ticketFullyRedeemed"},"profileId":{"type":"string"},"venueId":{"type":"string"},"name":{"type":"string"},"retentionThresholdHours":{"type":"integer","description":"Used when deletionTrigger is operationalRetentionThreshold. No default (make-or-break (a), see `setFaceTagTemporaryEnrollment`)"},"consentCapture":{"type":"string","enum":["onScreenAcknowledgement","signedForm"],"description":"How consent is taken at capture; onScreenAcknowledgement (no form to sign) unless set"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"TenantDataRetentionClass": {"type":"string","description":"**The data classes a tenant sets a retention period for** (decided 29 September, Chinmay: all data retention is tenant configuration, one setting per class). Defaults are ADR-0047's and the AI system design's (section 8, decision 5); a legal limit is the only thing the platform enforces.\n| Class | Default | Counted from | Legal limit (refused) | |---|---|---|---| | `guestProfile` | 5 years | last activity | none | | `paymentRecord` | 10 years | created | at least 10 years (4.3.4) | | `financialRecord` | 7 years | created | at least 7 years (6.1.78) | | `auditRecord` | 2 years (authorisation and device audit) | created | none | | `approvalRecord` | 7 years (approvals board 6.7) | decided | none | | `complianceInspection` | 7 years | created | none | | `faceTagBiometric` | 7 days | ticket expiry | make-or-break | | `facePassBiometric` | follows `guestProfile` | last activity | make-or-break | | `aiPrompts` | 90 days (prompts and responses) | created | none | | `aiConversations` | 90 days | last activity | none | | `aiDecisionRecords` | follows `auditRecord` (decision records and the approvals of AI actions) | decided | none | | `aiMetadataIndex` | always follows `aiDecisionRecords` (summaries, entities, embeddings) | created | none |\n**ADR-0047's floors and ceilings that are not law are defaults now, not refusals** (the audit floor of one year, the proposed seven-year guest-profile ceiling, the Face Tag thirty-day ceiling). Platform-owned copies — the burst environment copy, a decommissioned cell — are not tenant data classes and are not here.\n","enum":["guestProfile","paymentRecord","financialRecord","auditRecord","approvalRecord","complianceInspection","faceTagBiometric","facePassBiometric","aiPrompts","aiConversations","aiDecisionRecords","aiMetadataIndex"]},
"TenantDataRetentionSetting": {"type":"object","x-ticvai-persistence":"tenancy.data_retention_setting","description":"**One tenant's retention period for one data class** (decided 29 September, Chinmay). One row per tenant and class, written by `setDataRetentionSetting`; a class with no row takes the platform default. The limit and default fields are the platform's catalogue, computed for the response and not stored on the row.\n","required":["dataClass"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"dataClass":{"allOf":[{"$ref":"#/components/schemas/TenantDataRetentionClass"}],"x-ticvai-unique":"tenant","description":"One row per class per tenant. On a write it comes from the path; a body value is ignored."},"retainAmount":{"type":"integer","nullable":true,"minimum":0,"description":"The tenant's period. Null with no `followsDataClass` means the platform default applies. Zero means the data is not kept past the transaction that produced it.\n"},"retainUnit":{"type":"string","nullable":true,"enum":["days","months","years"],"description":"Required with `retainAmount`."},"followsDataClass":{"allOf":[{"$ref":"#/components/schemas/TenantDataRetentionClass"}],"nullable":true,"description":"Keep this class for as long as another class is kept. Set by default for `aiDecisionRecords` (follows `auditRecord`), `facePassBiometric` (follows `guestProfile`) and `aiMetadataIndex` (follows `aiDecisionRecords`, and cannot be changed).\n"},"onExpiry":{"type":"string","enum":["archive","anonymise","delete"],"default":"archive","description":"ADR-0047's stages. `archive` moves the data to the archive instance, from where it is erased on the class's own schedule; derived stores (the AI index, search) purge at archive, not later.\n"},"anchor":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"enum":["createdAt","lastActivity","decidedAt","ticketExpiry"],"description":"What the period is counted from. Fixed per class by the platform."},"effectiveAmount":{"type":"integer","readOnly":true,"x-ticvai-persisted":false,"description":"The period actually applied, after follows and defaults are resolved."},"effectiveUnit":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"isDefault":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"True when the tenant has not set this class and the platform default applies."},"defaultAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false},"defaultUnit":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"legalMinimumAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"A floor the law sets. A shorter period is refused (`422`)."},"legalMaximumAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"A maximum the law sets. A longer period is refused (`422`). Null for every class until the biometric make-or-break is answered."},"legalLimitUnit":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"legalBasis":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"The law or requirement the limit comes from, e.g. `4.3.4`."},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"updatedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The tenant. Retention is set at tenant scope only."}}}
}
```
