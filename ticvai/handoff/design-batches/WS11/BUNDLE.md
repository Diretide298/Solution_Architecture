# WS11 — Access Control board 11

**10 screens · 18 operations · 23 schemas · 5 permissions**

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
  `ACCESS_POINT_CONFIGURE, GUEST_MANAGE, INCIDENT_MANAGE, REPORT_VIEW_VENUE, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-244` | Access Security & Fraud Command Center | B–D | 11 | 262 | 6 | 1 | 3 | 0 | — | notStarted (generated) |
| `BO-245` | Fraud Detection Rule & Signal Library | B–D | 13 | 0 | 6 | 8 | 1 | 0 | — | notStarted (generated) |
| `BO-246` | Credential Sharing & Concurrent Usage Detection | B–D | 3 | 0 | 6 | 1 | 0 | 0 | — | notStarted (generated) |
| `BO-247` | Unified Identity & Credential Lock Manager | B–D | 9 | 2 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-248` | Biometric & Identity Integrity Monitoring | B–D | 5 | 6 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-249` | Relationship & Companion Fraud Monitoring | B–D | 12 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-250` | Access Risk Scoring & Decision Engine | B–D | 6 | 0 | 6 | 1 | 1 | 0 | — | notStarted (generated) |
| `BO-251` | Real-Time Security Response & Playbook Builder | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-252` | Security Investigation & Evidence Workspace | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-253` | Security Analytics, AI Detection & Governance | B–D | 5 | 32 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-245, BO-246, BO-250, BO-252 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-244` Access Security & Fraud Command Center

**Provide security teams with a real-time command center for access-related fraud and suspicious activity across all venues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `INCIDENT_MANAGE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | `alertId` (navigation) |
| Route | `/access-venue/access-security-fraud-command-center-bo-244` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listAccessSecurityFraud` ?venue |
| Park | text field | — | — | `listAccessSecurityFraud` ?park |
| Zone | text field | — | — | `listAccessSecurityFraud` ?zone |
| Gate | text field | — | — | `listAccessSecurityFraud` ?gate |

**Form: Lock identity** (modal, opened by *Lock identity*; *Lock identity* calls `lockIdentity`, *Cancel* sends nothing)

**Collects what `lockIdentity` sends before it is called.** Required: `subjectId`, `lockScope`, `lockDuration`, `lockReason`. Optional: `venueId`, `lockHours`, `associatedEntitlementIds`, `securityInvestigationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subjectId` | picker: choose a subject | required | — | — | shows names, sends the id | — | `lockIdentity` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | Required for a venue lock; null for allVenueAccess and fullIdentity | `lockIdentity` body |
| Lock scope `lockScope` | select | required | — | Credential only · Media only · Entitlement · Venue · All venue access · Full identity | — | — | `lockIdentity` body |
| Lock duration `lockDuration` | radio group | required | — | Until manually released · End of day · N hours · Until investigation complete · Permanent | — | — | `lockIdentity` body |
| Lock hours `lockHours` | number field (hours) | optional | — | min 1; max 720 | — | — | `lockIdentity` body |
| Lock reason `lockReason` | select | required | — | Credential sharing · Fraud suspected · Security incident · Identity mismatch · Stolen credential · Guest removal | — | — | `lockIdentity` body |
| Associated entitlements `associatedEntitlementIds` | multi-picker: choose associated entitlements | optional | — | — | — | — | `lockIdentity` body |
| Security investigation `securityInvestigationId` | picker: choose a security investigation | optional | — | — | shows names, sends the id | — | `lockIdentity` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 `already-locked`: an active lock covers this subject at this scope.; 422 `lockHours` missing for an nHours lock.

**Form: Save security alert** (modal, opened by *Save security alert*; *Save security alert* calls `updateSecurityAlert`, *Cancel* sends nothing)

**Collects what `updateSecurityAlert` sends before it is called.** Required: `status`. Optional: `note`, `securityInvestigationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | segmented control | required | — | Acknowledged · Resolved · Dismissed | — | — | `updateSecurityAlert` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `updateSecurityAlert` body |
| Security investigation `securityInvestigationId` | picker: choose a security investigation | optional | — | — | shows names, sends the id | — | `updateSecurityAlert` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The alert is already resolved or dismissed.

#### Outputs: what the screen shows and produces

**Shown**

**Active Security Alerts** (metric tile, from `listAccessSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Alert | text | — |
| Description | text | e.g. |
| Credential | text | — |
| Venue | text | — |
| Zone | text | — |
| Gate | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active security alerts | 1,234 | Active Security Alerts |
| High risk credentials | 1,234 | High-Risk Credentials |
| Credentials locked today | 1,234 | Credentials Locked Today |
| Suspicious QR activity | 1,234 | Suspicious QR Activity |
| Device sharing alerts | 1,234 | Device-Sharing Alerts |
| Biometric alerts | 1,234 | Biometric Alerts |
| Duplicate access attempts | 1,234 | — |
| Blacklisted credentials | 1,234 | Blacklisted Credentials |

**High-Risk Credentials** (metric tile, from `listAccessSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Alert | text | — |
| Description | text | e.g. |
| Credential | text | — |
| Venue | text | — |
| Zone | text | — |
| Gate | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active security alerts | 1,234 | Active Security Alerts |
| High risk credentials | 1,234 | High-Risk Credentials |
| Credentials locked today | 1,234 | Credentials Locked Today |
| Suspicious QR activity | 1,234 | Suspicious QR Activity |
| Device sharing alerts | 1,234 | Device-Sharing Alerts |
| Biometric alerts | 1,234 | Biometric Alerts |
| Duplicate access attempts | 1,234 | — |
| Blacklisted credentials | 1,234 | Blacklisted Credentials |

**Credentials Locked Today** (metric tile, from `listAccessSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Alert | text | — |
| Description | text | e.g. |
| Credential | text | — |
| Venue | text | — |
| Zone | text | — |
| Gate | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active security alerts | 1,234 | Active Security Alerts |
| High risk credentials | 1,234 | High-Risk Credentials |
| Credentials locked today | 1,234 | Credentials Locked Today |
| Suspicious QR activity | 1,234 | Suspicious QR Activity |
| Device sharing alerts | 1,234 | Device-Sharing Alerts |
| Biometric alerts | 1,234 | Biometric Alerts |
| Duplicate access attempts | 1,234 | — |
| Blacklisted credentials | 1,234 | Blacklisted Credentials |

**Suspicious QR Activity** (metric tile, from `listAccessSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Alert | text | — |
| Description | text | e.g. |
| Credential | text | — |
| Venue | text | — |
| Zone | text | — |
| Gate | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active security alerts | 1,234 | Active Security Alerts |
| High risk credentials | 1,234 | High-Risk Credentials |
| Credentials locked today | 1,234 | Credentials Locked Today |
| Suspicious QR activity | 1,234 | Suspicious QR Activity |
| Device sharing alerts | 1,234 | Device-Sharing Alerts |
| Biometric alerts | 1,234 | Biometric Alerts |
| Duplicate access attempts | 1,234 | — |
| Blacklisted credentials | 1,234 | Blacklisted Credentials |

**Device-Sharing Alerts** (metric tile, from `listAccessSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Alert | text | — |
| Description | text | e.g. |
| Credential | text | — |
| Venue | text | — |
| Zone | text | — |
| Gate | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active security alerts | 1,234 | Active Security Alerts |
| High risk credentials | 1,234 | High-Risk Credentials |
| Credentials locked today | 1,234 | Credentials Locked Today |
| Suspicious QR activity | 1,234 | Suspicious QR Activity |
| Device sharing alerts | 1,234 | Device-Sharing Alerts |
| Biometric alerts | 1,234 | Biometric Alerts |
| Duplicate access attempts | 1,234 | — |
| Blacklisted credentials | 1,234 | Blacklisted Credentials |

**Biometric Alerts** (metric tile, from `listAccessSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Alert | text | — |
| Description | text | e.g. |
| Credential | text | — |
| Venue | text | — |
| Zone | text | — |
| Gate | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active security alerts | 1,234 | Active Security Alerts |
| High risk credentials | 1,234 | High-Risk Credentials |
| Credentials locked today | 1,234 | Credentials Locked Today |
| Suspicious QR activity | 1,234 | Suspicious QR Activity |
| Device sharing alerts | 1,234 | Device-Sharing Alerts |
| Biometric alerts | 1,234 | Biometric Alerts |
| Duplicate access attempts | 1,234 | — |
| Blacklisted credentials | 1,234 | Blacklisted Credentials |

**Blacklisted Credentials** (metric tile, from `listAccessSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Alert | text | — |
| Description | text | e.g. |
| Credential | text | — |
| Venue | text | — |
| Zone | text | — |
| Gate | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active security alerts | 1,234 | Active Security Alerts |
| High risk credentials | 1,234 | High-Risk Credentials |
| Credentials locked today | 1,234 | Credentials Locked Today |
| Suspicious QR activity | 1,234 | Suspicious QR Activity |
| Device sharing alerts | 1,234 | Device-Sharing Alerts |
| Biometric alerts | 1,234 | Biometric Alerts |
| Duplicate access attempts | 1,234 | — |
| Blacklisted credentials | 1,234 | Blacklisted Credentials |

**Active Investigations** (metric tile, from `listAccessSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Alert | text | — |
| Description | text | e.g. |
| Credential | text | — |
| Venue | text | — |
| Zone | text | — |
| Gate | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active security alerts | 1,234 | Active Security Alerts |
| High risk credentials | 1,234 | High-Risk Credentials |
| Credentials locked today | 1,234 | Credentials Locked Today |
| Suspicious QR activity | 1,234 | Suspicious QR Activity |
| Device sharing alerts | 1,234 | Device-Sharing Alerts |
| Biometric alerts | 1,234 | Biometric Alerts |
| Duplicate access attempts | 1,234 | — |
| Blacklisted credentials | 1,234 | Blacklisted Credentials |

**Fraud attempts prevented today** (metric tile, from `listAccessSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Alert | text | — |
| Description | text | e.g. |
| Credential | text | — |
| Venue | text | — |
| Zone | text | — |
| Gate | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active security alerts | 1,234 | Active Security Alerts |
| High risk credentials | 1,234 | High-Risk Credentials |
| Credentials locked today | 1,234 | Credentials Locked Today |
| Suspicious QR activity | 1,234 | Suspicious QR Activity |
| Device sharing alerts | 1,234 | Device-Sharing Alerts |
| Biometric alerts | 1,234 | Biometric Alerts |
| Duplicate access attempts | 1,234 | — |
| Blacklisted credentials | 1,234 | Blacklisted Credentials |

**Share of today's validations at low risk, percent** (metric tile, from `listAccessSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Alert | text | — |
| Description | text | e.g. |
| Credential | text | — |
| Venue | text | — |
| Zone | text | — |
| Gate | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active security alerts | 1,234 | Active Security Alerts |
| High risk credentials | 1,234 | High-Risk Credentials |
| Credentials locked today | 1,234 | Credentials Locked Today |
| Suspicious QR activity | 1,234 | Suspicious QR Activity |
| Device sharing alerts | 1,234 | Device-Sharing Alerts |
| Biometric alerts | 1,234 | Biometric Alerts |
| Duplicate access attempts | 1,234 | — |
| Blacklisted credentials | 1,234 | Blacklisted Credentials |

**Share at medium risk, percent** (metric tile, from `listAccessSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Alert | text | — |
| Description | text | e.g. |
| Credential | text | — |
| Venue | text | — |
| Zone | text | — |
| Gate | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active security alerts | 1,234 | Active Security Alerts |
| High risk credentials | 1,234 | High-Risk Credentials |
| Credentials locked today | 1,234 | Credentials Locked Today |
| Suspicious QR activity | 1,234 | Suspicious QR Activity |
| Device sharing alerts | 1,234 | Device-Sharing Alerts |
| Biometric alerts | 1,234 | Biometric Alerts |
| Duplicate access attempts | 1,234 | — |
| Blacklisted credentials | 1,234 | Blacklisted Credentials |

**Share at high risk, percent** (metric tile, from `listAccessSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Alert | text | — |
| Description | text | e.g. |
| Credential | text | — |
| Venue | text | — |
| Zone | text | — |
| Gate | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active security alerts | 1,234 | Active Security Alerts |
| High risk credentials | 1,234 | High-Risk Credentials |
| Credentials locked today | 1,234 | Credentials Locked Today |
| Suspicious QR activity | 1,234 | Suspicious QR Activity |
| Device sharing alerts | 1,234 | Device-Sharing Alerts |
| Biometric alerts | 1,234 | Biometric Alerts |
| Duplicate access attempts | 1,234 | — |
| Blacklisted credentials | 1,234 | Blacklisted Credentials |

**Share at critical risk, percent** (metric tile, from `listAccessSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Severity | chip: Low, Medium, High, Critical | — |
| Alert | text | — |
| Description | text | e.g. |
| Credential | text | — |
| Venue | text | — |
| Zone | text | — |
| Gate | text | — |
| Detected at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Active security alerts | 1,234 | Active Security Alerts |
| High risk credentials | 1,234 | High-Risk Credentials |
| Credentials locked today | 1,234 | Credentials Locked Today |
| Suspicious QR activity | 1,234 | Suspicious QR Activity |
| Device sharing alerts | 1,234 | Device-Sharing Alerts |
| Biometric alerts | 1,234 | Biometric Alerts |
| Duplicate access attempts | 1,234 | — |
| Blacklisted credentials | 1,234 | Blacklisted Credentials |

**Every access security fraud** (data table, from `listAccessSecurityFraud`)

| Shows | Format | Notes |
|---|---|---|
| Duplicate access attempts | text | not in the schema: `Duplicate Access Attempts` |

**The selected access security fraud** (detail panel): The pack groups this record's detail under its own headings: “CRITICAL”, “HIGH”, “MEDIUM”, “Display incidents geographically across”.

| Shows | Format | Notes |
|---|---|---|
| Duplicate access attempts | text | not in the schema: `Duplicate Access Attempts` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Lock identity (primary button) | `lockIdentity` POST `/identity-locks` | IdentityLockInput | AccessIdentityLock | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 `already-locked`: an active lock covers this subject at this scope. | gated `INCIDENT_MANAGE`; opens modal first |
| Save security alert (secondary button) | `updateSecurityAlert` POST `/security-alerts/{alertId}/status` | inline | AccessSecurityAlert | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `INCIDENT_MANAGE`; opens modal first |

**Data it reads**: `listAccessSecurityFraud` (onLoad, Access Security & Fraud Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-245` Fraud Detection Rule & Signal Library: *Works in Fraud Detection Rule & Signal Library*; calls `listAccessSecurityFraud`
- → `BO-247` Unified Identity & Credential Lock Manager: *Works in Unified Identity & Credential Lock Manager*; calls `listAccessSecurityFraud`
- → `BO-249` Relationship & Companion Fraud Monitoring: *Works in Relationship & Companion Fraud Monitoring*; calls `listAccessSecurityFraud`
- → `BO-250` Access Risk Scoring & Decision Engine: *Works in Access Risk Scoring & Decision Engine*; calls `listAccessSecurityFraud`
- → `BO-251` Real-Time Security Response & Playbook Builder: *Works in Real-Time Security Response & Playbook Builder*; calls `listAccessSecurityFraud`
- → `BO-252` Security Investigation & Evidence Workspace: *Works in Security Investigation & Evidence Workspace*; calls `listAccessSecurityFraud`
- → `BO-246` Credential Sharing & Concurrent Usage Detection: *Works in Credential Sharing & Concurrent Usage Detection*; carries `alertId`; calls `listAccessSecurityFraud`
- → `BO-248` Biometric & Identity Integrity Monitoring: *Works in Biometric & Identity Integrity Monitoring*; carries `alertId`; calls `listAccessSecurityFraud`
- → `BO-253` Security Analytics, AI Detection & Governance: *Works in Security Analytics, AI Detection & Governance*; carries `alertId`; calls `listAccessSecurityFraud`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access security fraud list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access security fraud untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access security fraud yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access security fraud are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The alert is already resolved or dismissed.; 409 `already-locked`: an active lock covers this subject at this scope.; 422 Not exactly one of subjectId, entitlementId and deviceId |

#### Permissions

- `listAccessSecurityFraud` → `SCOPE_VIEW` (read) · staff
- `lockIdentity` → `INCIDENT_MANAGE` (configure) · staff
- `updateSecurityAlert` → `INCIDENT_MANAGE` (configure) · staff
- `getAccessRiskScore` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.44 | Access Risk Scoring - System shall calculate access risk scores. | Admission and Access | CONTRACTED | `getAccessRiskScore` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Fraud monitoring shows a composite risk score per customer built from several signals: attempts and success/failure ratio (e.g. 10 attempts, 3 successes), distinct cards under one identity, refund volume or value, device/login anomalies, and repeated attempts to use an expired ticket at access control. *(agreed · MoM 21 Sep 2026, 4.12 / 4.13 AI Risk & Fraud Intelligence · DI-969)*
- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Fraud assessment view flags suspicious usage patterns or threats; live monitoring shows current attendance, in-park counts and entry/exit/crossover activity per venue in real time. *(client request · MoM 2 Sep 2026, 4.16 Fraud Detection & Live Monitoring · DI-651)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-244` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS28 Access Control Board 11.dc.html#bo-244`
- Workshop pack: Access Control Module_Reference.pdf board 11
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 1: Opens Access Security & Fraud Command Center → Provide security teams with a real-time command center for access-related fraud and suspicious activity across all venues.
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F121 branch at step 1 (expected): when Nothing has been set up on Access Security & Fraud Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F121 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (262 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-244?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Lock identity, Save security alert.
- [ ] Every transition is wired: `BO-100`, `BO-245`, `BO-247`, `BO-249`, `BO-250`, `BO-251`, `BO-252`, `BO-246`, `BO-248`, `BO-253`.
- [ ] Every gated control is gated: `INCIDENT_MANAGE`, `SCOPE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-245` Fraud Detection Rule & Signal Library

**Configure the signals TICVAI uses to identify suspicious access behavior.**

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
| Route | `/access-venue/fraud-detection-rule-signal-library-bo-245` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Sent by *Save fraud rule*** (`setFraudDetectionRule`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rule `ruleId` | picker: choose a rule | optional | — | — | shows names, sends the id | Absent creates a rule | `setFraudDetectionRule` body |
| Signal `signal` | select | required | — | Excessive QR activations · Multiple active sessions · Credential copied · Excessive refresh attempts · Invalid signature · Expired credential · Revoked credential · Screenshot replay attempt · Abnormal transfer frequency · Repeated failed validation · New … | — | — | `setFraudDetectionRule` body |
| Signal category `signalCategory` | radio group | optional | — | Credential · Device · Access · Identity | — | — | `setFraudDetectionRule` body |
| Severity `severity` | radio group | required | — | Low · Medium · High · Critical | — | — | `setFraudDetectionRule` body |
| Weight `weight` | stepper or slider | optional | — | min 0; max 100 | — | Contribution to the access risk score | `setFraudDetectionRule` body |
| Threshold `threshold` | number field | required | — | min 1 | — | Occurrences within timeWindow that fire the rule | `setFraudDetectionRule` body |
| Time window `timeWindow` | number field | required | — | min 1 | — | Minutes | `setFraudDetectionRule` body |
| Scope `scope` | text field | optional | — | — | — | Scope path the rule applies to; empty is the whole tenant | `setFraudDetectionRule` body |
| Applicable credential types `applicableCredentialTypes` | list of values (chips) | optional | — | — | — | — | `setFraudDetectionRule` body |
| Applicable venues `applicableVenues` | list of values (chips) | optional | — | — | — | — | `setFraudDetectionRule` body |
| Offline availability `offlineAvailability` | toggle | optional | off | — | — | Evaluated on the gate when offline | `setFraudDetectionRule` body |
| Response `response` | select | required | Alert only | Alert only · Increase risk score · Require additional verification · Require supervisor · Temporarily lock · Full identity lock · Blacklist | — | — | `setFraudDetectionRule` body |
| Enabled `enabled` | toggle | optional | on | — | — | — | `setFraudDetectionRule` body |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save fraud rule (primary button) | `setFraudDetectionRule` PUT `/fraud-detection-rule` | FraudDetectionRuleSignalLibraryInput | FraudDetectionRuleSignalLibraryView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Data it reads**: `listFraudDetectionRule` (onLoad, Fraud Detection Rule & Signal Library)

**Where the user goes next**

- → `BO-244` Access Security & Fraud Command Center: *Returns to the board's landing screen*; calls `listFraudDetectionRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fraud detection rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fraud detection rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fraud detection rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the fraud detection rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listFraudDetectionRule` → `SCOPE_VIEW` (read) · staff
- `setFraudDetectionRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.45 | Access Anomaly Detection - System shall detect anomalous access behavior. | Admission and Access | CONTRACTED | `setFraudDetectionRule` |
| 8.3.23 | System shall detect duplicate ticket scans. | Unified Operations Dashboard | CONTRACTED | `setFraudDetectionRule` |
| 8.3.24 | System shall detect duplicate ticket usage. | Unified Operations Dashboard | CONTRACTED | `setFraudDetectionRule` |
| 8.3.26 | System shall detect passback attempts. | Unified Operations Dashboard | CONTRACTED | `setFraudDetectionRule` |
| 8.3.27 | System shall detect ticket cloning attempts. | Unified Operations Dashboard | CONTRACTED | `setFraudDetectionRule` |
| 8.3.28 | System shall detect abnormal entitlement usage. | Unified Operations Dashboard | CONTRACTED | `setFraudDetectionRule` |
| 8.3.29 | System shall detect unauthorized ticket transfers. | Unified Operations Dashboard | CONTRACTED | `setFraudDetectionRule` |
| 8.3.42 | System shall detect unusual access behavior. | Unified Operations Dashboard | CONTRACTED | `setFraudDetectionRule` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Fraud monitoring shows a composite risk score per customer built from several signals: attempts and success/failure ratio (e.g. 10 attempts, 3 successes), distinct cards under one identity, refund volume or value, device/login anomalies, and repeated attempts to use an expired ticket at access control. *(agreed · MoM 21 Sep 2026, 4.12 / 4.13 AI Risk & Fraud Intelligence · DI-969)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-245` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS28 Access Control Board 11.dc.html#bo-245`
- Workshop pack: Access Control Module_Reference.pdf board 11
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 2: Works in Fraud Detection Rule & Signal Library → Configure the signals TICVAI uses to identify suspicious access behavior.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-245?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save fraud rule.
- [ ] Every transition is wired: `BO-244`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-246` Credential Sharing & Concurrent Usage Detection

**Detect one of the most important access-control fraud scenarios: One valid ticket being shared by multiple people or devices.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `INCIDENT_MANAGE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `alertId` (navigation) |
| Route | `/access-venue/credential-sharing-concurrent-usage-detection-bo-246` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Form: Save security alert** (modal, opened by *Save security alert*; *Save security alert* calls `updateSecurityAlert`, *Cancel* sends nothing)

**Collects what `updateSecurityAlert` sends before it is called.** Required: `status`. Optional: `note`, `securityInvestigationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | segmented control | required | — | Acknowledged · Resolved · Dismissed | — | — | `updateSecurityAlert` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `updateSecurityAlert` body |
| Security investigation `securityInvestigationId` | picker: choose a security investigation | optional | — | — | shows names, sends the id | — | `updateSecurityAlert` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The alert is already resolved or dismissed.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save security alert (primary button) | `updateSecurityAlert` POST `/security-alerts/{alertId}/status` | inline | AccessSecurityAlert | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `INCIDENT_MANAGE`; opens modal first |

**Data it reads**: `listCredentialSharingConcurrent` (onLoad, Credential Sharing & Concurrent Usage Detection)

**Where the user goes next**

- → `BO-244` Access Security & Fraud Command Center: *Returns to the board's landing screen*; carries `alertId`; calls `listCredentialSharingConcurrent`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential sharing concurrent list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential sharing concurrent untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential sharing concurrent yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential sharing concurrent are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The alert is already resolved or dismissed. |

#### Permissions

- `listCredentialSharingConcurrent` → `SCOPE_VIEW` (read) · staff
- `updateSecurityAlert` → `INCIDENT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.3.25 | System shall detect ticket sharing activities. | Unified Operations Dashboard | CONTRACTED | `listCredentialSharingConcurrent` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-246` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS28 Access Control Board 11.dc.html#bo-246`
- Workshop pack: Access Control Module_Reference.pdf board 11
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 4: Works in Credential Sharing & Concurrent Usage Detection → Detect one of the most important access-control fraud scenarios: One valid ticket being shared by multiple people or devices.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-246?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save security alert.
- [ ] Every transition is wired: `BO-244`.
- [ ] Every gated control is gated: `INCIDENT_MANAGE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-247` Unified Identity & Credential Lock Manager

**Provide the single security lock required by the matrix so suspicious activity can immediately stop all access associated with an identity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `INCIDENT_MANAGE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `lockId` (navigation) |
| Route | `/access-venue/unified-identity-credential-lock-manager-bo-247` |

#### Inputs: what the user enters or picks

**Form: Lock identity** (modal, opened by *Lock identity*; *Lock identity* calls `lockIdentity`, *Cancel* sends nothing)

**Collects what `lockIdentity` sends before it is called.** Required: `subjectId`, `lockScope`, `lockDuration`, `lockReason`. Optional: `venueId`, `lockHours`, `associatedEntitlementIds`, `securityInvestigationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subjectId` | picker: choose a subject | required | — | — | shows names, sends the id | — | `lockIdentity` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | Required for a venue lock; null for allVenueAccess and fullIdentity | `lockIdentity` body |
| Lock scope `lockScope` | select | required | — | Credential only · Media only · Entitlement · Venue · All venue access · Full identity | — | — | `lockIdentity` body |
| Lock duration `lockDuration` | radio group | required | — | Until manually released · End of day · N hours · Until investigation complete · Permanent | — | — | `lockIdentity` body |
| Lock hours `lockHours` | number field (hours) | optional | — | min 1; max 720 | — | — | `lockIdentity` body |
| Lock reason `lockReason` | select | required | — | Credential sharing · Fraud suspected · Security incident · Identity mismatch · Stolen credential · Guest removal | — | — | `lockIdentity` body |
| Associated entitlements `associatedEntitlementIds` | multi-picker: choose associated entitlements | optional | — | — | — | — | `lockIdentity` body |
| Security investigation `securityInvestigationId` | picker: choose a security investigation | optional | — | — | shows names, sends the id | — | `lockIdentity` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 `already-locked`: an active lock covers this subject at this scope.; 422 `lockHours` missing for an nHours lock.

**Form: Release identity lock** (modal, opened by *Release identity lock*; *Release identity lock* calls `releaseIdentityLock`, *Cancel* sends nothing)

**Collects what `releaseIdentityLock` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `releaseIdentityLock` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `investigation-open` or `lock-released`.

#### Outputs: what the screen shows and produces

**Shown**

**Every unified identity credential** (data table, from `listUnifiedIdentityCredential`)

| Shows | Format | Notes |
|---|---|---|
| Propagated to | list or chips (count when long) | Channels the lock has reached |

**The selected unified identity credential** (detail panel): The pack groups this record's detail under its own headings: “Identity”, “Associated Credentials”, “Lock Duration”, “Unlock”.

| Shows | Format | Notes |
|---|---|---|
| Propagated to | list or chips (count when long) | Channels the lock has reached |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Lock identity (primary button) | `lockIdentity` POST `/identity-locks` | IdentityLockInput | AccessIdentityLock | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 `already-locked`: an active lock covers this subject at this scope. | gated `INCIDENT_MANAGE`; opens modal first |
| Release identity lock (secondary button) | `releaseIdentityLock` POST `/identity-locks/{lockId}/release` | inline | AccessIdentityLock | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `INCIDENT_MANAGE`; opens modal first |

**Data it reads**: `listUnifiedIdentityCredential` (onLoad, Unified Identity & Credential Lock Manager)

**Where the user goes next**

- → `BO-244` Access Security & Fraud Command Center: *Returns to the board's landing screen*; calls `listUnifiedIdentityCredential`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The unified identity credential list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the unified identity credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No unified identity credential yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the unified identity credential are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `already-locked`: an active lock covers this subject at this scope.; 409 `investigation-open` or `lock-released`.; 422 `lockHours` missing for an nHours lock. |

#### Permissions

- `listUnifiedIdentityCredential` → `SCOPE_VIEW` (read) · staff
- `lockIdentity` → `INCIDENT_MANAGE` (configure) · staff
- `releaseIdentityLock` → `INCIDENT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-247` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS28 Access Control Board 11.dc.html#bo-247`
- Workshop pack: Access Control Module_Reference.pdf board 11
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 6: Works in Unified Identity & Credential Lock Manager → Provide the single security lock required by the matrix so suspicious activity can immediately stop all access associated with an identity.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-247?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Lock identity, Release identity lock.
- [ ] Every transition is wired: `BO-244`.
- [ ] Every gated control is gated: `INCIDENT_MANAGE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-248` Biometric & Identity Integrity Monitoring

**Detect suspicious biometric and identity-related changes without duplicating Board 5's biometric configuration. Board 5 configures biometrics. Board 11 monitors biometric security risk.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `GUEST_MANAGE`, `INCIDENT_MANAGE`, `SCOPE_VIEW` (3 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Monitor) and no metric row |
| Offline | online only |
| Opens with | `alertId` (navigation), `attemptId` (navigation) |
| Route | `/access-venue/biometric-identity-integrity-monitoring-bo-248` |

#### Inputs: what the user enters or picks

**Form: Save security alert** (modal, opened by *Save security alert*; *Save security alert* calls `updateSecurityAlert`, *Cancel* sends nothing)

**Collects what `updateSecurityAlert` sends before it is called.** Required: `status`. Optional: `note`, `securityInvestigationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | segmented control | required | — | Acknowledged · Resolved · Dismissed | — | — | `updateSecurityAlert` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `updateSecurityAlert` body |
| Security investigation `securityInvestigationId` | picker: choose a security investigation | optional | — | — | shows names, sends the id | — | `updateSecurityAlert` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The alert is already resolved or dismissed.

**Form: Review face reenrolment** (modal, opened by *Review face reenrolment*; *Review face reenrolment* calls `reviewFaceReenrolment`, *Cancel* sends nothing)

**Collects what `reviewFaceReenrolment` sends before it is called.** Required: `decision`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | segmented control | required | — | Approve · Block | — | — | `reviewFaceReenrolment` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `reviewFaceReenrolment` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `not-pending`: the attempt is not awaiting review.

#### Outputs: what the screen shows and produces

**Shown**

**Every biometric identity integrity** (data table, from `listBiometricIdentityIntegrity`)

| Shows | Format | Notes |
|---|---|---|
| Anomaly type | chip: Face changed, Re enrollment, Repeated face mismatch, Multiple faces one credential … | — |
| Multiple faces associated with one credential | text | not in the schema: `multiple faces associated with one credential` |
| One face associated with multiple credentials | text | not in the schema: `one face associated with multiple credentials` |

**The selected biometric identity integrity** (detail panel): The pack groups this record's detail under its own headings: “Original Face Enrollment”, “Successful Visits”, “Face Changed”, “Reason”, “Enrollment 1”, “Enrollment 2”.

| Shows | Format | Notes |
|---|---|---|
| Anomaly type | chip: Face changed, Re enrollment, Repeated face mismatch, Multiple faces one credential … | — |
| Multiple faces associated with one credential | text | not in the schema: `multiple faces associated with one credential` |
| One face associated with multiple credentials | text | not in the schema: `one face associated with multiple credentials` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save security alert (primary button) | `updateSecurityAlert` POST `/security-alerts/{alertId}/status` | inline | AccessSecurityAlert | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `INCIDENT_MANAGE`; opens modal first |
| Review face reenrolment (secondary button) | `reviewFaceReenrolment` POST `/face-reenrolment-attempts/{attemptId}/review` | inline | AccessFaceReenrolmentAttempt | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `GUEST_MANAGE`; opens modal first |

**Data it reads**: `listBiometricIdentityIntegrity` (onLoad, Biometric & Identity Integrity Monitoring)

**Where the user goes next**

- → `BO-244` Access Security & Fraud Command Center: *Returns to the board's landing screen*; carries `alertId`; calls `listBiometricIdentityIntegrity`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The biometric identity integrity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the biometric identity integrity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No biometric identity integrity yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the biometric identity integrity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The alert is already resolved or dismissed.; 409 `not-pending`: the attempt is not awaiting review. |

#### Permissions

- `listBiometricIdentityIntegrity` → `SCOPE_VIEW` (read) · staff
- `setSecurityInvestigationEvidence` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `updateSecurityAlert` → `INCIDENT_MANAGE` (configure) · staff
- `reviewFaceReenrolment` → `GUEST_MANAGE` (configure) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-248` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS28 Access Control Board 11.dc.html#bo-248`
- Workshop pack: Access Control Module_Reference.pdf board 11
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 8: Works in Biometric & Identity Integrity Monitoring → Detect suspicious biometric and identity-related changes without duplicating Board 5's biometric configuration. Board 5 configures biometrics. Board 11 monitors biometric security risk.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-248?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save security alert, Review face reenrolment.
- [ ] Every transition is wired: `BO-244`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `GUEST_MANAGE`, `INCIDENT_MANAGE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-249` Relationship & Companion Fraud Monitoring

**Detect abuse involving linked guests such as: Child + Adult POD + Companion Guest + Nanny Group Leader + Group Membership dependents.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/relationship-companion-fraud-monitoring-bo-249` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Companion changed during visit | text field | — | — | — | — | — | — |
| Nanny credential used without primary guest | text field | — | — | — | — | — | — |
| Child enters/exits with unauthorized adult | text field | — | — | — | — | — | — |
| excessive relationship changes | select field | — | — | — | — | — | — |

**Form: Save relationship fraud rule** (modal, opened by *Save relationship fraud rule*; *Save relationship fraud rule* calls `setRelationshipFraudRule`, *Cancel* sends nothing)

**Collects what `setRelationshipFraudRule` sends before it is called.** Required: `relationshipRuleType`, `severity`, `relationshipResponses`. Optional: `ruleId`, `relationshipType`, `weight`, `applicableVenues`, `enabled`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rule `ruleId` | picker: choose a rule | optional | — | — | shows names, sends the id | Absent creates a rule | `setRelationshipFraudRule` body |
| Relationship rule type `relationshipRuleType` | select | required | — | Companion changed during visit · Nanny credential without primary guest · Child with unauthorized adult · Companion linked to multiple primaries · Excessive relationship changes · Group leader across unrelated groups | — | relationship rules (the list's ruleType) | `setRelationshipFraudRule` body |
| Relationship type `relationshipType` | radio group | optional | — | Child adult · Pod companion · Guest nanny · Group leader group · Membership dependent | — | relationship rules | `setRelationshipFraudRule` body |
| Severity `severity` | radio group | required | — | Low · Medium · High · Critical | — | — | `setRelationshipFraudRule` body |
| Weight `weight` | stepper or slider | optional | — | min 0; max 100 | — | — | `setRelationshipFraudRule` body |
| Relationship responses `relationshipResponses` | multi-select chips | required | — | Yellow intervention · Supervisor verification · ID verification · Biometric verification · Security escalation · Access denial | — | relationship rules (the list's responses) | `setRelationshipFraudRule` body |
| Applicable venues `applicableVenues` | multi-picker: choose applicable venues | optional | — | — | — | — | `setRelationshipFraudRule` body |
| Enabled `enabled` | toggle | optional | on | — | — | — | `setRelationshipFraudRule` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `wrong-rule-kind`: the ruleId names a signal rule.; 422 `accessDenial` without a person in the loop.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save relationship fraud rule (primary button) | `setRelationshipFraudRule` PUT `/relationship-fraud-rules` | RelationshipFraudRuleInput | AccessFraudRule | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Data it reads**: `listRelationshipCompanionFraud` (onLoad, Relationship & Companion Fraud Monitoring)

**Where the user goes next**

- → `BO-244` Access Security & Fraud Command Center: *Returns to the board's landing screen*; calls `listRelationshipCompanionFraud`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The relationship companion fraud configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the relationship companion fraud untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No relationship companion fraud configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `wrong-rule-kind`: the ruleId names a signal rule.; 422 `accessDenial` without a person in the loop. |

#### Permissions

- `listRelationshipCompanionFraud` → `SCOPE_VIEW` (read) · staff
- `setRelationshipFraudRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-249` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS28 Access Control Board 11.dc.html#bo-249`
- Workshop pack: Access Control Module_Reference.pdf board 11
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 10: Works in Relationship & Companion Fraud Monitoring → Detect abuse involving linked guests such as: Child + Adult POD + Companion Guest + Nanny Group Leader + Group Membership dependents.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-249?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save relationship fraud rule.
- [ ] Every transition is wired: `BO-244`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-250` Access Risk Scoring & Decision Engine

**Convert multiple security signals into a unified access risk score.**

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
| Route | `/access-venue/access-risk-scoring-decision-engine-bo-250` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Form: Save risk scoring config** (modal, opened by *Save risk scoring config*; *Save risk scoring config* calls `setRiskScoringConfig`, *Cancel* sends nothing)

**Collects what `setRiskScoringConfig` sends before it is called.** Required: `id`, `scopePath`, `mediumThreshold`, `highThreshold`, `criticalThreshold`. Optional: `riskFactors`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setRiskScoringConfig` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node; one row per scope | `setRiskScoringConfig` body |
| Medium threshold `mediumThreshold` | number field | required | — | min 0 | — | Score from which risk is medium (pack 30) | `setRiskScoringConfig` body |
| High threshold `highThreshold` | number field | required | — | min 0 | — | Score from which risk is high (pack 60) | `setRiskScoringConfig` body |
| Critical threshold `criticalThreshold` | number field | required | — | min 0 | — | Score from which risk is critical (pack 80) | `setRiskScoringConfig` body |
| Risk factors `riskFactors` | multi-select chips | optional | — | Venue · Product · Ticket value · Event · Access zone · Time · Credential type · Historical behavior | — | Context the score may depend on | `setRiskScoringConfig` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 Thresholds not rising, or out of 0 to 100.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save risk scoring config (primary button) | `setRiskScoringConfig` PUT `/risk-scoring-config` | AccessRiskScoringConfig | AccessRiskScoringConfig | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 Thresholds not rising, or out of 0 to 100. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

**Data it reads**: `listAccessRiskScoring` (onLoad, Access Risk Scoring & Decision Engine)

**Where the user goes next**

- → `BO-244` Access Security & Fraud Command Center: *Returns to the board's landing screen*; calls `listAccessRiskScoring`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access risk scoring list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access risk scoring untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access risk scoring yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access risk scoring are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 Not exactly one of subjectId, entitlementId and deviceId; 422 Thresholds not rising, or out of 0 to 100. |

#### Permissions

- `listAccessRiskScoring` → `SCOPE_VIEW` (read) · staff
- `setRiskScoringConfig` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `getAccessRiskScore` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.44 | Access Risk Scoring - System shall calculate access risk scores. | Admission and Access | CONTRACTED | `getAccessRiskScore` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Fraud monitoring shows a composite risk score per customer built from several signals: attempts and success/failure ratio (e.g. 10 attempts, 3 successes), distinct cards under one identity, refund volume or value, device/login anomalies, and repeated attempts to use an expired ticket at access control. *(agreed · MoM 21 Sep 2026, 4.12 / 4.13 AI Risk & Fraud Intelligence · DI-969)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-250` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS28 Access Control Board 11.dc.html#bo-250`
- Workshop pack: Access Control Module_Reference.pdf board 11
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 12: Works in Access Risk Scoring & Decision Engine → Convert multiple security signals into a unified access risk score.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-250?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save risk scoring config.
- [ ] Every transition is wired: `BO-244`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-251` Real-Time Security Response & Playbook Builder

**Configure what TICVAI automatically does when security conditions are detected.**

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
| Route | `/access-venue/real-time-security-response-playbook-builder-bo-251` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Alert Only (primary button) | navigation or local | — | — | — | — |
| Increase Risk Score (secondary button) | navigation or local | — | — | — | — |
| Require Additional Verification (secondary button) | navigation or local | — | — | — | — |
| Require Supervisor (secondary button) | navigation or local | — | — | — | — |
| Temporarily Lock (secondary button) | navigation or local | — | — | — | — |
| Full Identity Lock (secondary button) | navigation or local | — | — | — | — |
| Blacklist (secondary button) | navigation or local | — | — | — | — |
| Notify Security (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-244` Access Security & Fraud Command Center: *Returns to the board's landing screen*; calls `setRealTimeSecurity`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The real-time security response list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the real-time security response untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No real-time security response yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the real-time security response are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRealTimeSecurity` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-251` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS28 Access Control Board 11.dc.html#bo-251`
- Workshop pack: Access Control Module_Reference.pdf board 11
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 14: Works in Real-Time Security Response & Playbook Builder → Configure what TICVAI automatically does when security conditions are detected.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-251?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Alert Only, Increase Risk Score, Require Additional Verification, Require Supervisor, Temporarily Lock, Full Identity Lock, Blacklist, Notify Security.
- [ ] Every transition is wired: `BO-244`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-252` Security Investigation & Evidence Workspace

**Provide security specialists with a deeper investigation environment than Board 9's operational incident workspace.**

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
| Route | `/access-venue/security-investigation-evidence-workspace-bo-252` |

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

- → `BO-244` Access Security & Fraud Command Center: *Returns to the board's landing screen*; calls `setSecurityInvestigationEvidence`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The security investigation evidence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the security investigation evidence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No security investigation evidence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the security investigation evidence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setSecurityInvestigationEvidence` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-252` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS28 Access Control Board 11.dc.html#bo-252`
- Workshop pack: Access Control Module_Reference.pdf board 11
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 16: Works in Security Investigation & Evidence Workspace → Provide security specialists with a deeper investigation environment than Board 9's operational incident workspace.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-252?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-244`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-253` Security Analytics, AI Detection & Governance

**Provide long-term intelligence on fraud patterns, security controls and effectiveness.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `INCIDENT_MANAGE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show; Measure) and no metric row |
| Offline | online only |
| Opens with | `alertId` (navigation) |
| Route | `/access-venue/security-analytics-ai-detection-governance-bo-253` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search security analytics detection | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, park, event, product, channel, reseller and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listSecurityDetectionGovernance` ?venue |
| Park | text field | — | — | `listSecurityDetectionGovernance` ?park |
| Event | text field | — | — | `listSecurityDetectionGovernance` ?event |
| Product | text field | — | — | `listSecurityDetectionGovernance` ?product |
| Channel | text field | — | — | `listSecurityDetectionGovernance` ?channel |
| Reseller | text field | — | — | `listSecurityDetectionGovernance` ?reseller |
| Credential type | text field | — | — | `listSecurityDetectionGovernance` ?credentialType |
| Media | text field | — | — | `listSecurityDetectionGovernance` ?media |
| Device | text field | — | — | `listSecurityDetectionGovernance` ?device |
| Gate | text field | — | — | `listSecurityDetectionGovernance` ?gate |
| Time day | text field | — | — | `listSecurityDetectionGovernance` ?timeDay |

**Form: Save security alert** (modal, opened by *Save security alert*; *Save security alert* calls `updateSecurityAlert`, *Cancel* sends nothing)

**Collects what `updateSecurityAlert` sends before it is called.** Required: `status`. Optional: `note`, `securityInvestigationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | segmented control | required | — | Acknowledged · Resolved · Dismissed | — | — | `updateSecurityAlert` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `updateSecurityAlert` body |
| Security investigation `securityInvestigationId` | picker: choose a security investigation | optional | — | — | shows names, sends the id | — | `updateSecurityAlert` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The alert is already resolved or dismissed.

#### Outputs: what the screen shows and produces

**Shown**

**Every security analytics detection** (data table, from `listSecurityDetectionGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Fraud attempts | 1,234 | Fraud Attempts |
| Prevented fraud | 1,234 | Prevented Fraud |
| Credential sharing | 1,234 | Credential Sharing |
| Duplicate usage | text | not in the schema: `Duplicate Usage` |
| Biometric alerts | 1,234 | Biometric Alerts |
| Device binding violations | 1,234 | Device-Binding Violations |
| Companion violations | 1,234 | Companion Violations |
| Blacklist hits | 1,234 | Blacklist Hits |
| Identity locks | 1,234 | Identity Locks |
| Detection rate | 12.5% | Detection Rate |
| False positive indicator | 1,234.5 | False Positive Indicator |
| Operator override rate | 12.5% | Operator Override Rate |
| Average investigation time | 1,234 | Minutes |
| Average response time | 1,234 | Minutes |
| Recurring fraud rate | 12.5% | Recurring Fraud Rate |
| Financial exposure | AED 1,234.50 | Financial Exposure |

**The selected security analytics detection** (detail panel): The pack groups this record's detail under its own headings: “Fraud Attempts by Sales Channel”, “Emerging Pattern Detected”, “Record changes to”, “Board 11 Key Workflow”, “A key distinction”.

| Shows | Format | Notes |
|---|---|---|
| Fraud attempts | 1,234 | Fraud Attempts |
| Prevented fraud | 1,234 | Prevented Fraud |
| Credential sharing | 1,234 | Credential Sharing |
| Duplicate usage | text | not in the schema: `Duplicate Usage` |
| Biometric alerts | 1,234 | Biometric Alerts |
| Device binding violations | 1,234 | Device-Binding Violations |
| Companion violations | 1,234 | Companion Violations |
| Blacklist hits | 1,234 | Blacklist Hits |
| Identity locks | 1,234 | Identity Locks |
| Detection rate | 12.5% | Detection Rate |
| False positive indicator | 1,234.5 | False Positive Indicator |
| Operator override rate | 12.5% | Operator Override Rate |
| Average investigation time | 1,234 | Minutes |
| Average response time | 1,234 | Minutes |
| Recurring fraud rate | 12.5% | Recurring Fraud Rate |
| Financial exposure | AED 1,234.50 | Financial Exposure |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save security alert (primary button) | `updateSecurityAlert` POST `/security-alerts/{alertId}/status` | inline | AccessSecurityAlert | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `INCIDENT_MANAGE`; opens modal first |

**Data it reads**: `listSecurityDetectionGovernance` (onLoad, Security Analytics, AI Detection & Governance)

**Where the user goes next**

- → `BO-244` Access Security & Fraud Command Center: *Access Security & Fraud Command Center*; carries `alertId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The security analytics detection list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the security analytics detection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No security analytics detection yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the security analytics detection are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The alert is already resolved or dismissed. |

#### Permissions

- `listSecurityDetectionGovernance` → `REPORT_VIEW_VENUE` (operate) · staff
- `updateSecurityAlert` → `INCIDENT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-253` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS28 Access Control Board 11.dc.html#bo-253`
- Workshop pack: Access Control Module_Reference.pdf board 11
- Flow F121 *Access Control board 11: Access Security & Fraud Command Center*, step 18: Works in Security Analytics, AI Detection & Governance → Provide long-term intelligence on fraud patterns, security controls and effectiveness.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (32 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-253?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save security alert.
- [ ] Every transition is wired: `BO-244`.
- [ ] Every gated control is gated: `INCIDENT_MANAGE`, `REPORT_VIEW_VENUE`.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getAccessRiskScore": {"method":"GET","path":"/access-risk-scores","contract":"access","summary":"The current access risk score of a person, credential or device, with its signals","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"subjectId","in":"query","required":null},{"name":"entitlementId","in":"query","required":null},{"name":"deviceId","in":"query","required":null},{"name":"venueId","in":"query","required":null}],"requestBody":null,"responds":"AccessRiskScore"},
"listAccessRiskScoring": {"method":"GET","path":"/access-risk-scoring","contract":"access","summary":"Access Risk Scoring & Decision Engine","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessRiskScoringDecisionEngineView"},
"listAccessSecurityFraud": {"method":"GET","path":"/access-security-fraud","contract":"access","summary":"Access Security & Fraud Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"park","in":"query","required":false},{"name":"zone","in":"query","required":false},{"name":"gate","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBiometricIdentityIntegrity": {"method":"GET","path":"/biometric-identity-integrity","contract":"access","summary":"Biometric & Identity Integrity Monitoring","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialSharingConcurrent": {"method":"GET","path":"/credential-sharing-concurrent","contract":"access","summary":"Credential Sharing & Concurrent Usage Detection","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFraudDetectionRule": {"method":"GET","path":"/fraud-detection-rule","contract":"access","summary":"Fraud Detection Rule & Signal Library","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FraudDetectionRuleSignalLibraryView"},
"listRelationshipCompanionFraud": {"method":"GET","path":"/relationship-companion-fraud","contract":"access","summary":"Relationship & Companion Fraud Monitoring","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RelationshipCompanionFraudMonitoringView"},
"listSecurityDetectionGovernance": {"method":"GET","path":"/security-detection-governance","contract":"access","summary":"Security Analytics, AI Detection & Governance","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venue","in":"query","required":false},{"name":"park","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"reseller","in":"query","required":false},{"name":"credentialType","in":"query","required":false},{"name":"media","in":"query","required":false},{"name":"device","in":"query","required":false},{"name":"gate","in":"query","required":false},{"name":"timeDay","in":"query","required":false}],"requestBody":null,"responds":"SecurityAnalyticsAiDetectionGovernanceView"},
"listUnifiedIdentityCredential": {"method":"GET","path":"/unified-identity-credential","contract":"access","summary":"Unified Identity & Credential Lock Manager","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"lockIdentity": {"method":"POST","path":"/identity-locks","contract":"access","summary":"Lock an identity","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"IdentityLockInput","responds":"AccessIdentityLock"},
"releaseIdentityLock": {"method":"POST","path":"/identity-locks/{lockId}/release","contract":"access","summary":"Release an identity lock","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessIdentityLock"},
"reviewFaceReenrolment": {"method":"POST","path":"/face-reenrolment-attempts/{attemptId}/review","contract":"access","summary":"Review a blocked Face Pass re-enrolment","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessFaceReenrolmentAttempt"},
"setFraudDetectionRule": {"method":"PUT","path":"/fraud-detection-rule","contract":"access","summary":"Save an access fraud detection rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FraudDetectionRuleSignalLibraryInput","responds":"FraudDetectionRuleSignalLibraryView"},
"setRealTimeSecurity": {"method":"PUT","path":"/real-time-security","contract":"access","summary":"Real-Time Security Response & Playbook Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RealTimeSecurityResponsePlaybookBuilderInput","responds":"RealTimeSecurityResponsePlaybookBuilderView"},
"setRelationshipFraudRule": {"method":"PUT","path":"/relationship-fraud-rules","contract":"access","summary":"Create or replace a relationship / companion fraud rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RelationshipFraudRuleInput","responds":"AccessFraudRule"},
"setRiskScoringConfig": {"method":"PUT","path":"/risk-scoring-config","contract":"access","summary":"Set the access risk scoring bands","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessRiskScoringConfig","responds":"AccessRiskScoringConfig"},
"setSecurityInvestigationEvidence": {"method":"PUT","path":"/security-investigation-evidence","contract":"access","summary":"Security Investigation & Evidence Workspace","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SecurityInvestigationEvidenceWorkspaceInput","responds":"SecurityInvestigationEvidenceWorkspaceView"},
"updateSecurityAlert": {"method":"POST","path":"/security-alerts/{alertId}/status","contract":"access","summary":"Acknowledge, resolve or dismiss a security alert","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessSecurityAlert"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessFaceReenrolmentAttempt": {"type":"object","x-ticvai-persistence":"access.face_reenrolment_attempt","description":"One Face Pass re-enrolment attempt - the existing and new capture references (opaque, never templates), the match result, the reason, the operator and the outcome, with the review of a blocked change (declared 29 September, data-model close-out DM1). Written by enrolFacePass when the subject already has a Face Pass; a pendingReview attempt is decided by reviewFaceReenrolment (decided 29 September, writers pass).","required":["id","venueId","scopePath","subjectId","existingProfileReference","newCaptureReference","matchResult","outcome","attemptedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The attemptId the list shows"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"subjectId":{"type":"string","format":"uuid","description":"The guest (pii.subject)"},"entitlementId":{"type":"string","format":"uuid","nullable":true,"description":"The credential the Face Pass belongs to"},"existingProfileReference":{"type":"string","maxLength":200,"description":"Opaque reference to the prior enrolment (pii.subject_biometric)"},"newCaptureReference":{"type":"string","maxLength":200,"description":"Opaque reference to the new capture"},"matchResult":{"type":"string","enum":["withinPolicy","significantDifference"]},"reasonForReEnrollment":{"type":"string","enum":["appearanceChange","poorOriginalCapture","technicalIssue","guestRequest","recovery","other"],"nullable":true},"verificationProcess":{"type":"string","maxLength":200,"nullable":true,"description":"How the guest was verified for the change"},"operatorPrincipalId":{"type":"string","format":"uuid","nullable":true},"outcome":{"type":"string","enum":["updated","blocked","pendingReview"]},"reviewedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Security or guest service reviewer of a blocked change (the integrity screen's approval)"},"reviewedAt":{"type":"string","format":"date-time","nullable":true},"attemptedAt":{"type":"string","format":"date-time"}}},
"AccessFraudRule": {"type":"object","x-ticvai-persistence":"access.fraud_rule","description":"One access fraud rule (not payment fraud, which is orders) - either a signal rule with its severity, weight, threshold, window, credential types, venues, offline availability and response, or a relationship/companion rule with its rule type, relationship and responses; ruleKind tells them apart (declared 29 September, data-model close-out DM1). Signal rows are written by setFraudDetectionRule and relationship rows by setRelationshipFraudRule (decided 29 September, writers pass).","required":["id","scopePath","ruleKind","severity","enabled"],"properties":{"id":{"type":"string","format":"uuid","description":"The ruleId setFraudDetectionRule is keyed by"},"scopePath":{"type":"string","description":"ltree of the scope the rule applies to (the operation's scope; the tenant when empty)"},"ruleKind":{"type":"string","enum":["signal","relationship"]},"signal":{"type":"string","enum":["excessiveQrActivations","multipleActiveSessions","credentialCopied","excessiveRefreshAttempts","invalidSignature","expiredCredential","revokedCredential","screenshotReplayAttempt","abnormalTransferFrequency","repeatedFailedValidation","newDevice","multipleDevices","deviceBindingMismatch","rootedCompromisedDevice","abnormalDeviceChanges","impossibleDeviceMovement","suspiciousScannerDeviceActivity","duplicateEntry","simultaneousUse","antiPassbackViolations","unusualReEntry","unusualCrossover","excessiveAttractionUse","repeatedWrongGateAttempts","abnormalFastPassConsumption","faceMismatch","unusualFaceChange","multipleIdentitiesLinked","suspiciousCompanionChanges","podNannyRelationshipAnomalies","excessiveRefunds"],"nullable":true,"description":"signal rules. `excessiveRefunds` (added 29 September, build pass, 5.3.33) counts one guest's refund-driven credential revocations (`access.credential_event`, event refund) within timeWindow against threshold: the buy, use, refund pattern of ticket abuse."},"signalCategory":{"type":"string","enum":["credential","device","access","identity"],"nullable":true},"relationshipRuleType":{"type":"string","enum":["companionChangedDuringVisit","nannyCredentialWithoutPrimaryGuest","childWithUnauthorizedAdult","companionLinkedToMultiplePrimaries","excessiveRelationshipChanges","groupLeaderAcrossUnrelatedGroups"],"nullable":true,"description":"relationship rules (the list's ruleType)"},"relationshipType":{"type":"string","enum":["childAdult","podCompanion","guestNanny","groupLeaderGroup","membershipDependent"],"nullable":true,"description":"relationship rules"},"severity":{"type":"string","enum":["low","medium","high","critical"]},"weight":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Contribution to the access risk score"},"threshold":{"type":"integer","minimum":1,"nullable":true,"description":"signal rules. Occurrences within timeWindow that fire the rule"},"timeWindow":{"type":"integer","minimum":1,"nullable":true,"description":"signal rules. Minutes"},"applicableCredentialTypes":{"type":"array","items":{"type":"string"}},"applicableVenueIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"The operation's applicableVenues"},"offlineAvailability":{"type":"boolean","default":false,"description":"Evaluated on the gate when offline"},"response":{"type":"string","enum":["alertOnly","increaseRiskScore","requireAdditionalVerification","requireSupervisor","temporarilyLock","fullIdentityLock","blacklist"],"nullable":true,"description":"signal rules; alertOnly on a new rule"},"relationshipResponses":{"type":"array","items":{"type":"string","enum":["yellowIntervention","supervisorVerification","idVerification","biometricVerification","securityEscalation","accessDenial"]},"description":"relationship rules (the list's responses)"},"enabled":{"type":"boolean","default":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessIdentityLock": {"type":"object","x-ticvai-persistence":"access.identity_lock","description":"One lock on an identity - its scope, duration, reason, the credentials linked to it, where it has propagated and whether it is still active (declared 29 September, data-model close-out DM1). Written by lockIdentity and releaseIdentityLock, by the fraud detection job where a rule's response is temporarilyLock or fullIdentityLock, and released by a timer for endOfDay and nHours locks (decided 29 September, writers pass).","required":["id","scopePath","subjectId","lockScope","lockDuration","lockReason","status","lockedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The lockId"},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Set when lockScope is venue"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"subjectId":{"type":"string","format":"uuid","description":"The locked identity (the list's identityId, pii.subject)"},"lockScope":{"type":"string","enum":["credentialOnly","mediaOnly","entitlement","venue","allVenueAccess","fullIdentity"]},"lockDuration":{"type":"string","enum":["untilManuallyReleased","endOfDay","nHours","untilInvestigationComplete","permanent"]},"lockHours":{"type":"integer","minimum":1,"nullable":true,"description":"Used when lockDuration is nHours"},"lockReason":{"type":"string","enum":["credentialSharing","fraudSuspected","securityIncident","identityMismatch","stolenCredential","guestRemoval"]},"associatedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"The linked credentials (the list's associatedCredentialIds)"},"associatedCredentialTypes":{"type":"array","items":{"type":"string","enum":["ticket","rfidWristband","dynamicQr","walletCredential","facePass","membership","fastPass"]}},"propagatedTo":{"type":"array","items":{"type":"string","enum":["centralPlatform","venueEdge","onlineGates","offlineRevocationPackage","mobileDevices"]},"description":"Channels the lock has reached"},"securityInvestigationId":{"type":"string","format":"uuid","nullable":true,"description":"The investigation an untilInvestigationComplete lock waits for"},"status":{"type":"string","enum":["active","released"],"default":"active"},"lockedAt":{"type":"string","format":"date-time"},"lockedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"releasedAt":{"type":"string","format":"date-time","nullable":true},"releasedByPrincipalId":{"type":"string","format":"uuid","nullable":true}}},
"AccessRiskScore": {"type":"object","x-ticvai-persistence":"none — computed at read time from access.risk_scoring_config, access.fraud_rule, access.security_alert, access.identity_lock and access.blacklist","description":"The current access risk score of one subject, credential or device, with what produced it (3.3.44; decided 29 September, build pass).","required":["score","band","calculatedAt"],"properties":{"subjectId":{"type":"string","format":"uuid","nullable":true},"entitlementId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"The scope whose risk configuration was applied."},"score":{"type":"integer","minimum":0,"maximum":100},"band":{"type":"string","enum":["low","medium","high","critical"],"description":"From the scope's mediumThreshold, highThreshold and criticalThreshold."},"signals":{"type":"array","description":"Every fraud signal that contributed, highest weight first.","items":{"type":"object","properties":{"fraudRuleId":{"type":"string","format":"uuid"},"signal":{"type":"string"},"weight":{"type":"integer"},"occurrences":{"type":"integer"},"lastDetectedAt":{"type":"string","format":"date-time"},"alertIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"contextFactors":{"type":"array","description":"The configured context factors and what each added.","items":{"type":"object","properties":{"factor":{"type":"string","enum":["venue","product","ticketValue","event","accessZone","time","credentialType","historicalBehavior"]},"contribution":{"type":"integer"}}}},"identityLocked":{"type":"boolean","description":"An active identity lock forces the critical band."},"blacklisted":{"type":"boolean","description":"A blacklist entry forces the critical band."},"calculatedAt":{"type":"string","format":"date-time"}}},
"AccessRiskScoringConfig": {"type":"object","x-ticvai-persistence":"access.risk_scoring_config","description":"The access risk scoring configuration of a scope - the score thresholds of the medium, high and critical bands and the context factors the score uses; per-signal weights live on access.fraud_rule (declared 29 September, data-model close-out DM1).","required":["id","scopePath","mediumThreshold","highThreshold","criticalThreshold"],"properties":{"id":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"ltree of the owning scope node; one row per scope"},"mediumThreshold":{"type":"integer","minimum":0,"description":"Score from which risk is medium (pack 30)"},"highThreshold":{"type":"integer","minimum":0,"description":"Score from which risk is high (pack 60)"},"criticalThreshold":{"type":"integer","minimum":0,"description":"Score from which risk is critical (pack 80)"},"riskFactors":{"type":"array","items":{"type":"string","enum":["venue","product","ticketValue","event","accessZone","time","credentialType","historicalBehavior"]},"description":"Context the score may depend on"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessRiskScoringDecisionEngineView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Risk Scoring & Decision Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"riskFactors":{"type":"array","items":{"type":"string","enum":["venue","product","ticketValue","event","accessZone","time","credentialType","historicalBehavior"]},"description":"Context the score may depend on"},"mediumThreshold":{"type":"integer","description":"Score from which risk is medium (pack: 30)"},"highThreshold":{"type":"integer","description":"Score from which risk is high (pack: 60)"},"criticalThreshold":{"type":"integer","description":"Score from which risk is critical (pack: 80)"}}},
"AccessSecurityAlert": {"type":"object","x-ticvai-persistence":"access.security_alert","description":"One access security or fraud alert - severity, what was detected, where and on which credential, identity or device - including biometric anomalies and edge security events (certificate, credential or package-signature failures, unauthorised connections, device authorisation and revocation). Merges the proposed access.security_alert and access.edge_security_event (declared 29 September, data-model close-out DM1). Created `open` by the detection jobs (fraud rules, sharing detection, biometric anomaly, edge security events) and moved by updateSecurityAlert; the lifecycle is states/access-security-alert.yaml (decided 29 September, writers pass).","required":["id","scopePath","category","severity","status","detectedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The alertId / anomalyId the lists show"},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"category":{"type":"string","enum":["fraudSignal","credentialSharing","duplicateAccess","blacklist","biometric","companion","edgeSecurity"]},"alertType":{"type":"string","maxLength":60,"nullable":true,"description":"The kind within the category - for fraudSignal the fraud rule's signal; for biometric one of faceChanged, reEnrollment, repeatedFaceMismatch, multipleFacesOneCredential, oneFaceMultipleCredentials, suspiciousEnrollmentFrequency, unusualVerificationFailures; for edgeSecurity one of certificateFailure, credentialFailure, packageSignatureFailure, unauthorizedConnection, deviceAuthorized, deviceRevoked"},"severity":{"type":"string","enum":["low","medium","high","critical"]},"description":{"type":"string","maxLength":500,"nullable":true,"description":"e.g. Credential attempted simultaneous entry at two gates"},"fraudRuleId":{"type":"string","format":"uuid","nullable":true,"description":"The access fraud rule that raised the alert, if one did"},"entitlementId":{"type":"string","format":"uuid","nullable":true,"description":"The credential (the list's credentialId)"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The identity concerned, where known"},"zoneId":{"type":"string","format":"uuid","nullable":true},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"The gate (the list's gateId)"},"deviceId":{"type":"string","format":"uuid","nullable":true,"description":"The device concerned, for device-sharing and edge events"},"faceReenrolmentAttemptId":{"type":"string","format":"uuid","nullable":true,"description":"Biometric alerts raised on a re-enrolment; the attempt holds the old and new references, operator, reason and review"},"faceProfileReference":{"type":"string","maxLength":200,"nullable":true,"description":"Biometric alerts. Opaque Face Pass reference; never a template"},"securityInvestigationId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["open","acknowledged","resolved","dismissed"],"default":"open"},"detectedAt":{"type":"string","format":"date-time"},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true}}},
"AccessSecurityFraudCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Security & Fraud Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"severity":{"type":"string","enum":["low","medium","high","critical"]},"alertId":{"type":"string"},"description":{"type":"string","description":"e.g. Credential attempted simultaneous entry at two gates"},"credentialId":{"type":"string"},"venueId":{"type":"string"},"zoneId":{"type":"string"},"gateId":{"type":"string"},"detectedAt":{"type":"string","format":"date-time"}},"required":["alertId","severity"]},
"AccessSecurityFraudCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"activeSecurityAlerts":{"type":"integer","description":"Active Security Alerts"},"highRiskCredentials":{"type":"integer","description":"High-Risk Credentials"},"credentialsLockedToday":{"type":"integer","description":"Credentials Locked Today"},"suspiciousQrActivity":{"type":"integer","description":"Suspicious QR Activity"},"deviceSharingAlerts":{"type":"integer","description":"Device-Sharing Alerts"},"biometricAlerts":{"type":"integer","description":"Biometric Alerts"},"duplicateAccessAttempts":{"type":"integer"},"blacklistedCredentials":{"type":"integer","description":"Blacklisted Credentials"},"activeInvestigations":{"type":"integer","description":"Active Investigations"},"fraudPrevented":{"type":"integer","description":"Fraud attempts prevented today"},"lowRisk":{"type":"number","description":"Share of today's validations at low risk, percent"},"mediumRisk":{"type":"number","description":"Share at medium risk, percent"},"highRisk":{"type":"number","description":"Share at high risk, percent"},"critical":{"type":"number","description":"Share at critical risk, percent"}}},
"BiometricIdentityIntegrityMonitoringView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Biometric & Identity Integrity Monitoring displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"anomalyId":{"type":"string"},"anomalyType":{"type":"string","enum":["faceChanged","reEnrollment","repeatedFaceMismatch","multipleFacesOneCredential","oneFaceMultipleCredentials","suspiciousEnrollmentFrequency","unusualVerificationFailures"]},"successfulVisits":{"type":"integer","description":"Successful Visits (the pack shows 28)"},"oldBiometricReference":{"type":"string","description":"Opaque reference to the prior enrolment; never the raw template"},"newBiometricReference":{"type":"string","description":"Opaque reference to the new enrolment; never the raw template"},"changeDate":{"type":"string","format":"date-time","description":"change date"},"location":{"type":"string","description":"location"},"operator":{"type":"string","description":"operator"},"verificationProcess":{"type":"string","description":"verification process"},"reason":{"type":"string","description":"reason"},"approval":{"type":"string","description":"approval"},"facePassId":{"type":"string"},"originalEnrollmentAt":{"type":"string","format":"date-time"}},"required":["anomalyId","anomalyType"]},
"CredentialSharingConcurrentUsageDetectionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Sharing & Concurrent Usage Detection displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"credentialId":{"type":"string"},"additionalDevices":{"type":"integer","description":"Additional Devices (the pack shows 3)"},"maximumActiveDevices":{"type":"integer","description":"Maximum Active Devices (the pack shows 1)"},"responseActions":{"type":"array","items":{"type":"string","enum":["increaseRisk","requireId","requireBiometric","requireOperator","lockSecondaryDevice","lockCredential","securityAlert"]},"description":"Responses applied when the limits are exceeded"},"primaryDeviceId":{"type":"string"},"maximumDeviceChangesPerVisit":{"type":"integer"},"detectedAt":{"type":"string","format":"date-time"}},"required":["credentialId"]},
"FraudDetectionRuleSignalLibraryInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Fraud Detection Rule & Signal Library submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["signal","severity","threshold","timeWindow","response"],"properties":{"ruleId":{"type":"string","format":"uuid","description":"Absent creates a rule"},"signal":{"type":"string","enum":["excessiveQrActivations","multipleActiveSessions","credentialCopied","excessiveRefreshAttempts","invalidSignature","expiredCredential","revokedCredential","screenshotReplayAttempt","abnormalTransferFrequency","repeatedFailedValidation","newDevice","multipleDevices","deviceBindingMismatch","rootedCompromisedDevice","abnormalDeviceChanges","impossibleDeviceMovement","suspiciousScannerDeviceActivity","duplicateEntry","simultaneousUse","antiPassbackViolations","unusualReEntry","unusualCrossover","excessiveAttractionUse","repeatedWrongGateAttempts","abnormalFastPassConsumption","faceMismatch","unusualFaceChange","multipleIdentitiesLinked","suspiciousCompanionChanges","podNannyRelationshipAnomalies","excessiveRefunds"]},"signalCategory":{"type":"string","enum":["credential","device","access","identity"]},"severity":{"type":"string","enum":["low","medium","high","critical"]},"weight":{"type":"integer","minimum":0,"maximum":100,"description":"Contribution to the access risk score"},"threshold":{"type":"integer","minimum":1,"description":"Occurrences within timeWindow that fire the rule"},"timeWindow":{"type":"integer","minimum":1,"description":"Minutes"},"scope":{"type":"string","description":"Scope path the rule applies to; empty is the whole tenant"},"applicableCredentialTypes":{"type":"array","items":{"type":"string"}},"applicableVenues":{"type":"array","items":{"type":"string"}},"offlineAvailability":{"type":"boolean","default":false,"description":"Evaluated on the gate when offline"},"response":{"type":"string","enum":["alertOnly","increaseRiskScore","requireAdditionalVerification","requireSupervisor","temporarilyLock","fullIdentityLock","blacklist"],"default":"alertOnly"},"enabled":{"type":"boolean","default":true}}},
"FraudDetectionRuleSignalLibraryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Fraud Detection Rule & Signal Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"signal":{"type":"string","enum":["excessiveQrActivations","multipleActiveSessions","credentialCopied","excessiveRefreshAttempts","invalidSignature","expiredCredential","revokedCredential","screenshotReplayAttempt","abnormalTransferFrequency","repeatedFailedValidation","newDevice","multipleDevices","deviceBindingMismatch","rootedCompromisedDevice","abnormalDeviceChanges","impossibleDeviceMovement","suspiciousScannerDeviceActivity","duplicateEntry","simultaneousUse","antiPassbackViolations","unusualReEntry","unusualCrossover","excessiveAttractionUse","repeatedWrongGateAttempts","abnormalFastPassConsumption","faceMismatch","unusualFaceChange","multipleIdentitiesLinked","suspiciousCompanionChanges","podNannyRelationshipAnomalies","excessiveRefunds"],"description":"The fraud signal this rule configures"},"severity":{"type":"string","enum":["low","medium","high","critical"],"description":"Severity"},"weight":{"type":"integer","description":"Points the signal adds to the access risk score"},"threshold":{"type":"integer","description":"Threshold"},"scope":{"type":"string","description":"Scope"},"applicableCredentialTypes":{"type":"array","items":{"type":"string"},"description":"Applicable credential types"},"applicableVenues":{"type":"array","items":{"type":"string"},"description":"Applicable venues"},"timeWindow":{"type":"integer","description":"Window the threshold is counted over, in minutes"},"offlineAvailability":{"type":"boolean","description":"Whether the signal is evaluated offline at the edge"},"response":{"type":"string","enum":["alertOnly","increaseRiskScore","requireAdditionalVerification","requireSupervisor","temporarilyLock","fullIdentityLock","blacklist"],"description":"Response"},"signalCategory":{"type":"string","enum":["credential","device","access","identity"]},"enabled":{"type":"boolean"}},"required":["ruleId","signal"]},
"IdentityLockInput": {"type":"object","x-ticvai-persistence":"none — request only; written as access.identity_lock (declared 29 September, writers pass)","required":["subjectId","lockScope","lockDuration","lockReason"],"properties":{"subjectId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Required for a venue lock; null for allVenueAccess and fullIdentity"},"lockScope":{"type":"string","enum":["credentialOnly","mediaOnly","entitlement","venue","allVenueAccess","fullIdentity"]},"lockDuration":{"type":"string","enum":["untilManuallyReleased","endOfDay","nHours","untilInvestigationComplete","permanent"]},"lockHours":{"type":"integer","minimum":1,"maximum":720,"nullable":true},"lockReason":{"type":"string","enum":["credentialSharing","fraudSuspected","securityIncident","identityMismatch","stolenCredential","guestRemoval"]},"associatedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"securityInvestigationId":{"type":"string","format":"uuid","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RealTimeSecurityResponsePlaybookBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Real-Time Security Response & Playbook Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"triggerCondition":{"type":"string","description":"e.g. Risk Score > 75 AND signal = simultaneousUse"},"name":{"type":"string"},"playbookId":{"type":"string"},"responseActions":{"type":"array","items":{"type":"string","enum":["alertOnly","increaseRiskScore","requireAdditionalVerification","requireSupervisor","temporarilyLock","fullIdentityLock","blacklist","notifySecurity","createIncident","notifyGuestServices","triggerEdgeDistribution"]},"description":"Actions the playbook runs when triggered"},"acknowledgeWithinMinutes":{"type":"integer"},"escalateToRole":{"type":"string","description":"e.g. Security Supervisor"},"escalateAfterMinutes":{"type":"integer"},"enabled":{"type":"boolean"}},"required":["playbookId","name","triggerCondition","responseActions"]},
"RealTimeSecurityResponsePlaybookBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Real-Time Security Response & Playbook Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"triggerCondition":{"type":"string","description":"e.g. Risk Score > 75 AND signal = simultaneousUse"},"name":{"type":"string"},"playbookId":{"type":"string"},"responseActions":{"type":"array","items":{"type":"string","enum":["alertOnly","increaseRiskScore","requireAdditionalVerification","requireSupervisor","temporarilyLock","fullIdentityLock","blacklist","notifySecurity","createIncident","notifyGuestServices","triggerEdgeDistribution"]},"description":"Actions the playbook runs when triggered"},"acknowledgeWithinMinutes":{"type":"integer"},"escalateToRole":{"type":"string","description":"e.g. Security Supervisor"},"escalateAfterMinutes":{"type":"integer"},"enabled":{"type":"boolean"}},"required":["playbookId","name","triggerCondition","responseActions"]},
"RelationshipCompanionFraudMonitoringView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Relationship & Companion Fraud Monitoring displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"ruleType":{"type":"string","enum":["companionChangedDuringVisit","nannyCredentialWithoutPrimaryGuest","childWithUnauthorizedAdult","companionLinkedToMultiplePrimaries","excessiveRelationshipChanges","groupLeaderAcrossUnrelatedGroups"]},"responses":{"type":"array","items":{"type":"string","enum":["yellowIntervention","supervisorVerification","idVerification","biometricVerification","securityEscalation","accessDenial"]}},"relationshipType":{"type":"string","enum":["childAdult","podCompanion","guestNanny","groupLeaderGroup","membershipDependent"]},"severity":{"type":"string","enum":["low","medium","high","critical"]},"enabled":{"type":"boolean"}},"required":["ruleId","ruleType"]},
"RelationshipFraudRuleInput": {"type":"object","x-ticvai-persistence":"none — request only; written as a relationship row of access.fraud_rule (declared 29 September, writers pass)","required":["relationshipRuleType","severity","relationshipResponses"],"properties":{"ruleId":{"type":"string","format":"uuid","description":"Absent creates a rule"},"relationshipRuleType":{"type":"string","enum":["companionChangedDuringVisit","nannyCredentialWithoutPrimaryGuest","childWithUnauthorizedAdult","companionLinkedToMultiplePrimaries","excessiveRelationshipChanges","groupLeaderAcrossUnrelatedGroups"],"description":"relationship rules (the list's ruleType)"},"relationshipType":{"type":"string","enum":["childAdult","podCompanion","guestNanny","groupLeaderGroup","membershipDependent"],"nullable":true,"description":"relationship rules"},"severity":{"type":"string","enum":["low","medium","high","critical"]},"weight":{"type":"integer","minimum":0,"maximum":100,"nullable":true},"relationshipResponses":{"type":"array","items":{"type":"string","enum":["yellowIntervention","supervisorVerification","idVerification","biometricVerification","securityEscalation","accessDenial"]},"description":"relationship rules (the list's responses)"},"applicableVenues":{"type":"array","items":{"type":"string","format":"uuid"}},"enabled":{"type":"boolean","default":true}}},
"SecurityAnalyticsAiDetectionGovernanceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Security Analytics, AI Detection & Governance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"fraudAttempts":{"type":"integer","description":"Fraud Attempts"},"preventedFraud":{"type":"integer","description":"Prevented Fraud"},"credentialSharing":{"type":"integer","description":"Credential Sharing"},"biometricAlerts":{"type":"integer","description":"Biometric Alerts"},"deviceBindingViolations":{"type":"integer","description":"Device-Binding Violations"},"companionViolations":{"type":"integer","description":"Companion Violations"},"blacklistHits":{"type":"integer","description":"Blacklist Hits"},"identityLocks":{"type":"integer","description":"Identity Locks"},"securityOverrides":{"type":"integer","description":"Security Overrides"},"detectionRate":{"type":"number","description":"Detection Rate"},"falsePositiveIndicator":{"type":"number","description":"False Positive Indicator"},"operatorOverrideRate":{"type":"number","description":"Operator Override Rate"},"averageInvestigationTime":{"type":"integer","description":"Minutes"},"averageResponseTime":{"type":"integer","description":"Minutes"},"recurringFraudRate":{"type":"number","description":"Recurring Fraud Rate"},"financialExposure":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Financial Exposure"},"estimatedFraudPrevented":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated Fraud Prevented"},"duplicateUsage":{"type":"integer"}}},
"SecurityInvestigationEvidenceWorkspaceInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Security Investigation & Evidence Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"investigationId":{"type":"string"},"evidenceSources":{"type":"array","items":{"type":"string","enum":["credentialHistory","scanRecords","gate","deviceIds","qrActivations","mediaChanges","transferHistory","biometricEvents","companionRelationships","posTicketTransactionReference","overrides","blacklistEvents","securityPolicies"]},"description":"Sources correlated into this investigation"},"subjectCredentialId":{"type":"string"},"status":{"type":"string","enum":["open","investigating","actionTaken","resolved","closed"]},"riskScore":{"type":"integer"},"riskLevel":{"type":"string","enum":["low","medium","high","critical"]},"notes":{"type":"string"},"linkedIncidentId":{"type":"string"}},"required":["investigationId"]},
"SecurityInvestigationEvidenceWorkspaceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Security Investigation & Evidence Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"investigationId":{"type":"string"},"evidenceSources":{"type":"array","items":{"type":"string","enum":["credentialHistory","scanRecords","gate","deviceIds","qrActivations","mediaChanges","transferHistory","biometricEvents","companionRelationships","posTicketTransactionReference","overrides","blacklistEvents","securityPolicies"]},"description":"Sources correlated into this investigation"},"subjectCredentialId":{"type":"string"},"status":{"type":"string","enum":["open","investigating","actionTaken","resolved","closed"]},"riskScore":{"type":"integer"},"riskLevel":{"type":"string","enum":["low","medium","high","critical"]},"notes":{"type":"string"},"linkedIncidentId":{"type":"string"}},"required":["investigationId"]},
"UnifiedIdentityCredentialLockManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Unified Identity & Credential Lock Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"identityId":{"type":"string"},"lockId":{"type":"string"},"associatedCredentialTypes":{"type":"array","items":{"type":"string","enum":["ticket","rfidWristband","dynamicQr","walletCredential","facePass","membership","fastPass"]},"description":"Kinds of credential linked to the locked identity"},"lockScope":{"type":"string","enum":["credentialOnly","mediaOnly","entitlement","venue","allVenueAccess","fullIdentity"],"description":"Vocabulary listed under Select."},"lockDuration":{"type":"string","enum":["untilManuallyReleased","endOfDay","nHours","untilInvestigationComplete","permanent"]},"propagatedTo":{"type":"array","items":{"type":"string","enum":["centralPlatform","venueEdge","onlineGates","offlineRevocationPackage","mobileDevices"]},"description":"Channels the lock has reached"},"associatedCredentialIds":{"type":"array","items":{"type":"string"}},"lockHours":{"type":"integer","description":"Used when lockDuration is nHours"},"lockReason":{"type":"string","enum":["credentialSharing","fraudSuspected","securityIncident","identityMismatch","stolenCredential","guestRemoval"]},"status":{"type":"string","enum":["active","released"]},"lockedAt":{"type":"string","format":"date-time"},"lockedBy":{"type":"string"}},"required":["lockId","identityId","lockScope","lockDuration"]}
}
```
