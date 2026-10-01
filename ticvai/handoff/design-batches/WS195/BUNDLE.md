# WS195 — Wallet Configuration Backend Structure v1.0 board 10

**10 screens · 21 operations · 23 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `APPROVAL_REQUEST, DEVELOPER_MANAGE, DEVELOPER_VIEW, PERMISSION_VIEW, WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
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
| `BO-1173` | Wallet Integration Command Center | B–D | 5 | 12 | 6 | 1 | 0 | 6 | — | notStarted (—) |
| `BO-1174` | Wallet API Catalogue & Endpoint Configuration | B–D | 30 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1175` | Integration Profile & System Mapping | B–D | 32 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-1176` | Wallet Events, Webhooks & Notification Orchestration | B–D | 11 | 0 | 6 | 2 | 0 | 6 | — | notStarted (—) |
| `BO-1177` | API Security, Access & Integration Permissions | B–D | 15 | 17 | 6 | 1 | 2 | 5 | — | notStarted (—) |
| `BO-1178` | Synchronization, Retry & Resilience Configuration | B–D | 12 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1179` | Integration Monitoring & Exception Workbench | B–D | 25 | 26 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-1180` | Wallet Configuration Governance & Version Control | B–D | 0 | 8 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1181` | Approval, Publication & Change Management | B–D | 7 | 0 | 6 | 5 | 0 | 3 | — | notStarted (—) |
| `BO-1182` | Wallet Platform Health, Audit & Administration Center | B–D | 0 | 2 | 6 | 0 | 0 | 6 | — | notStarted (—) |

## Thin screens in this batch

**BO-1180 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1173` Wallet Integration Command Center

**Provide administrators and technical operations teams with a centralized view of all Wallet integrations and API activity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`, `WALLET_CONFIGURE` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each integration displays) — counts over a population, then the population |
| Offline | online only |
| Opens with | `clientId` (navigation), `subscriptionId` (navigation) |
| Route | `/orders-money/wallet-integration-command-center-bo-1173` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search wallet integration | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, integration, api, environment, status and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Client | picker: choose a client | — | — | `listWebhookSubscriptions` ?clientId |

**Sent by *Suspend Integration*** (`setApiClientStatus`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | segmented control | required | — | Active · Suspended | — | — | `setApiClientStatus` body |
| Reason `reason` | text area | optional | — | max length 500 | — | Required with `suspended`. | `setApiClientStatus` body |

**Sent by *Test Connection*** (`testWebhookSubscription`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Event type `eventType` | select | optional | — | Access.validated · Accreditation.application decided · Accreditation.credential issued · Accreditation.holder status changed · Accreditation.renewal due · Ai.ceiling approaching · API client.anomaly detected · Approval.escalated · Approval.expired · … | — | The webhook event catalogue: every event a subscription may name (29 September, build pass). | `testWebhookSubscription` body |

#### Outputs: what the screen shows and produces

**Shown**

**Active Integrations** (metric tile)

**Connected TICVAI Modules** (metric tile)

**External Integrations** (metric tile)

**API Requests Today** (metric tile)

**Successful API Requests** (metric tile)

**Failed API Requests** (metric tile)

**API Success Rate** (metric tile)

**Average Response Time** (metric tile)

**Webhook Events** (metric tile)

**Failed Webhooks** (metric tile)

**Synchronization Failures** (metric tile)

**Integration Alerts** (metric tile)

**Connected TICVAI Domains** (metric tile)

**Every wallet integration** (data table)

| Shows | Format | Notes |
|---|---|---|
| Healthy | text | not in the schema: `Healthy` |
| Degraded | text | not in the schema: `Degraded` |
| Delayed | text | not in the schema: `Delayed` |
| Failed | text | not in the schema: `Failed` |
| Suspended | text | not in the schema: `Suspended` |
| Maintenance | text | not in the schema: `Maintenance` |

**The selected wallet integration** (detail panel): The pack groups this record's detail under its own headings: “Display connectivity with”.

| Shows | Format | Notes |
|---|---|---|
| Healthy | text | not in the schema: `Healthy` |
| Degraded | text | not in the schema: `Degraded` |
| Delayed | text | not in the schema: `Delayed` |
| Failed | text | not in the schema: `Failed` |
| Suspended | text | not in the schema: `Suspended` |
| Maintenance | text | not in the schema: `Maintenance` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
| Create Integration (primary button) | navigation or local | — | — | — | — |
| View API Health (secondary button) | navigation or local | — | — | — | — |
| Retry Failed Event (secondary button) | navigation or local | — | — | — | — |
| Open Error Log (secondary button) | navigation or local | — | — | — | — |
| Suspend Integration (destructive button) | `setApiClientStatus` POST `/api-clients/{clientId}/status` | inline | ApiClient | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The client is `revoked`, which is terminal.; 422 `suspended` without a `reason`. | — |
| Test Connection (secondary button) | `testWebhookSubscription` POST `/webhook-subscriptions/{subscriptionId}/test` | inline | WebhookDelivery | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `eventType` is not one this subscription takes. | — |

**Data it reads**: `publishWalletConfiguration` (onLoad, Configuration state); `listWebhookSubscriptions` (onLoad, The webhook subscriptions to test or replay)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1174` Wallet API Catalogue & Endpoint Configuration: *Wallet API Catalogue & Endpoint Configuration*
- → `BO-1175` Integration Profile & System Mapping: *Integration Profile & System Mapping*
- → `BO-1176` Wallet Events, Webhooks & Notification Orchestration: *Wallet Events, Webhooks & Notification Orchestration*
- → `BO-1177` API Security, Access & Integration Permissions: *API Security, Access & Integration Permissions*
- → `BO-1178` Synchronization, Retry & Resilience Configuration: *Synchronization, Retry & Resilience Configuration*
- → `BO-1179` Integration Monitoring & Exception Workbench: *Integration Monitoring & Exception Workbench*; carries `clientId`, `subscriptionId`
- → `BO-1180` Wallet Configuration Governance & Version Control: *Wallet Configuration Governance & Version Control*
- → `BO-1181` Approval, Publication & Change Management: *Approval, Publication & Change Management*
- → `BO-1182` Wallet Platform Health, Audit & Administration Center: *Wallet Platform Health, Audit & Administration Center*

**What opens over it**

- confirmDialog *Suspend Integration*: **Suspend Integration on a wallet integration is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet integration list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet integration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet integration yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet integration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A `production` client without a current certification, or asked for by a developer rather than issued by TICVAI (`certification-required`, M17-06).; 409 The client is `revoked`, which is terminal.; 422 A `production` client with an empty `ipAllowList` (`ip-allow-list-required`, M17-07), or a scope that is not in the scope catalogue (`unknown-scope`, M17-05).; 422 `eventType` is not one this … |

#### Permissions

- `publishWalletConfiguration` → `WALLET_CONFIGURE` (configure) · staff
- `createApiClient` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `replayEvents` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `listWebhookSubscriptions` → `DEVELOPER_VIEW` (read) · staff, partner
- `setApiClientStatus` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `testWebhookSubscription` → `DEVELOPER_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.19 | System shall support replay of historical events for recovery, synchronization, troubleshooting, and integration reprocessing purposes. | Developer & API Management | CONTRACTED | `replayEvents` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1173` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1173`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 10
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 1: Opens Wallet Integration Command Center → Provide administrators and technical operations teams with a centralized view of all Wallet integrations and API activity.
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F302 branch at step 1 (expected): when Nothing has been set up on Wallet Integration Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F302 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1173?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes, Create Integration, View API Health, Retry Failed Event, Open Error Log, Suspend Integration, Test Connection.
- [ ] Every transition is wired: `BO-100`, `BO-1174`, `BO-1175`, `BO-1176`, `BO-1177`, `BO-1178`, `BO-1179`, `BO-1180`, `BO-1181`, `BO-1182`.
- [ ] Every gated control is gated: `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`, `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1174` Wallet API Catalogue & Endpoint Configuration

**Define and govern the API services exposed by the TICVAI Wallet Engine. Requirement 4.3.34 explicitly requires APIs supporting wallet operations. Core Wallet APIs**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure APIs for; For each API define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-api-catalogue-endpoint-configuration-bo-1174` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Wallet Management | select field | — | — | — | — | — | — |
| Create Wallet | select field | — | — | — | — | — | — |
| Retrieve Wallet | select field | — | — | — | — | — | — |
| Update Wallet | select field | — | — | — | — | — | — |
| Block Wallet | select field | — | — | — | — | — | — |
| Unblock Wallet | select field | — | — | — | — | — | — |
| Balance | select field | — | — | — | — | — | — |
| Balance Inquiry | select field | — | — | — | — | — | — |
| Balance by Credit Type | text field | — | — | — | — | — | — |
| Available Balance | select field | — | — | — | — | — | — |
| Reserved Balance | select field | — | — | — | — | — | — |
| Transactions | select field | — | — | — | — | — | — |
| Transaction History | select field | — | — | — | — | — | — |
| Transaction Detail | select field | — | — | — | — | — | — |
| Wallet Payment | select field | — | — | — | — | — | — |
| Wallet Redemption | select field | — | — | — | — | — | — |
| Funding | select field | — | — | — | — | — | — |
| Fund Wallet | select field | — | — | — | — | — | — |
| Top-Up | select field | — | — | — | — | — | — |
| Auto-Reload | select field | — | — | — | — | — | — |
| Transfers | select field | — | — | — | — | — | — |
| Wallet-to-Wallet Transfer | select field | — | — | — | — | — | — |
| Transfer Status | select field | — | — | — | — | — | — |
| Refunds | select field | — | — | — | — | — | — |
| Refund to Wallet | select field | — | — | — | — | — | — |
| Refund Status | select field | — | — | — | — | — | — |
| Gift Cards / Benefits | text field | — | — | — | — | — | — |
| Gift Card Balance | select field | — | — | — | — | — | — |
| Voucher Validation | select field | — | — | — | — | — | — |
| Benefit Inquiry | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listWalletTypes` (onLoad, What the API exposes)

**Where the user goes next**

- → `BO-1173` Wallet Integration Command Center: *Back to Wallet Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet api catalogue configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet api catalogue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet api catalogue configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listWalletTypes` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1174` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1174`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 10
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 2: Works in Wallet API Catalogue & Endpoint Configuration → Define and govern the API services exposed by the TICVAI Wallet Engine. Requirement 4.3.34 explicitly requires APIs supporting wallet operations. Core Wallet APIs

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1174?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1173`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1175` Integration Profile & System Mapping

**Configure how TICVAI Wallet communicates with internal modules and approved external systems. Requirement 4.3.20 requires wallet integration with both internal and external systems through APIs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/integration-profile-system-mapping-bo-1175` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Integration name | select field | — | — | — | — | — | — |
| System type | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Environment | select field | — | — | — | — | — | — |
| Base endpoint | select field | — | — | — | — | — | — |
| Authentication profile | select field | — | — | — | — | — | — |
| Supported operations | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Timeout | select field | — | — | — | — | — | — |
| Retry policy | select field | — | — | — | — | — | — |
| Error handling | select field | — | — | — | — | — | — |
| Data mapping | select field | — | — | — | — | — | — |
| Effective dates | select field | — | — | — | — | — | — |

**Sent by *Save mapping*** (`setWalletIntegrationMapping`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| API client `apiClientId` | picker: choose an api client | required | — | — | shows names, sends the id | The `public-api` ApiClient the integration authenticates as. | `setWalletIntegrationMapping` body |
| Field mappings `fieldMappings` | repeatable rows | optional | — | — | — | — | `setWalletIntegrationMapping` body |
| External field `fieldMappings[].externalField` | text field | required | — | — | — | — | `setWalletIntegrationMapping` body |
| Wallet field `fieldMappings[].walletField` | text field | required | — | — | — | — | `setWalletIntegrationMapping` body |
| Transform `fieldMappings[].transform` | text field | optional | — | — | — | — | `setWalletIntegrationMapping` body |
| Currency mappings `currencyMappings` | repeatable rows | optional | — | — | — | — | `setWalletIntegrationMapping` body |
| External code `currencyMappings[].externalCode` | text field | required | — | — | — | — | `setWalletIntegrationMapping` body |
| Currency `currencyMappings[].currency` | text field | required | — | pattern `^[A-Z]{3}$` | — | — | `setWalletIntegrationMapping` body |
| Status mappings `statusMappings` | repeatable rows | optional | — | — | — | — | `setWalletIntegrationMapping` body |
| External status `statusMappings[].externalStatus` | text field | required | — | — | — | — | `setWalletIntegrationMapping` body |
| Wallet status `statusMappings[].walletStatus` | text field | required | — | — | — | — | `setWalletIntegrationMapping` body |
| Credit type mappings `creditTypeMappings` | repeatable rows | optional | — | — | — | — | `setWalletIntegrationMapping` body |
| External code `creditTypeMappings[].externalCode` | text field | required | — | — | — | — | `setWalletIntegrationMapping` body |
| Credit type `creditTypeMappings[].creditTypeId` | picker: choose a credit type | required | — | — | shows names, sends the id | — | `setWalletIntegrationMapping` body |
| Date time format `dateTimeFormat` | text field | optional | ISO-8601 | — | — | The format the integration sends, e.g. ISO-8601 or a pattern such as dd/MM/yyyy HH:mm. | `setWalletIntegrationMapping` body |
| Time zone `timeZone` | text field | optional | — | — | — | IANA zone the integration's local times are in. Null means UTC offsets are sent. | `setWalletIntegrationMapping` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setWalletIntegrationMapping` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Field mapping (primary button) | navigation or local | — | — | — | — |
| Currency mapping (secondary button) | navigation or local | — | — | — | — |
| Status mapping (secondary button) | navigation or local | — | — | — | — |
| Credit-type mapping (secondary button) | navigation or local | — | — | — | — |
| Date/time mapping (secondary button) | navigation or local | — | — | — | — |
| Save mapping (primary button) | `setWalletIntegrationMapping` PUT `/wallet-integration-mappings` | WalletIntegrationMapping | WalletIntegrationMapping | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.; 422 A credit-type mapping names a credit type that does not exist or is retired, or an external value is mapped twice within one … | — |

**Where the user goes next**

- → `BO-1173` Wallet Integration Command Center: *Back to Wallet Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The integration profile system configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the integration profile system untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No integration profile system configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A credit-type mapping names a credit type that does not exist or is retired, or an external value is mapped twice within one list. |

#### Permissions

- `setWalletChannelRules` → `WALLET_CONFIGURE` (configure) · staff
- `setWalletIntegrationMapping` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Financial year/period setup varies by country (UAE Jan–Dec, India Apr–Mar); closing a period locks further postings. An ERP integration centre manages external connections. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-263)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1175` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1175`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 10
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 4: Works in Integration Profile & System Mapping → Configure how TICVAI Wallet communicates with internal modules and approved external systems. Requirement 4.3.20 requires wallet integration with both internal and external systems through APIs.

#### Acceptance for the design

- [ ] Every input above is drawn (32), with its required mark, default, format and its error state (412, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1175?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Field mapping, Currency mapping, Status mapping, Credit-type mapping, Date/time mapping, Save mapping.
- [ ] Every transition is wired: `BO-1173`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1176` Wallet Events, Webhooks & Notification Orchestration

**Configure event-driven communication when something changes in Wallet.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVELOPER_MANAGE`, `WALLET_CONFIGURE` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§For each subscriber configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-events-webhooks-notification-orchestration-bo-1176` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Event | select field | — | — | — | — | — | — |
| Destination | select field | — | — | — | — | — | — |
| Authentication | select field | — | — | — | — | — | — |
| Payload version | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Retry count | select field | — | — | — | — | — | — |
| Retry interval | select field | — | — | — | — | — | — |
| Timeout | select field | — | — | — | — | — | — |
| Signing/security | select field | — | — | — | — | — | — |
| Failure behavior | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Wallet Created (primary button) | navigation or local | — | — | — | — |
| Wallet Activated (secondary button) | navigation or local | — | — | — | — |
| Wallet Blocked (secondary button) | navigation or local | — | — | — | — |
| Wallet Unblocked (secondary button) | navigation or local | — | — | — | — |
| Balance Changed (secondary button) | navigation or local | — | — | — | — |
| Top-Up Failed (secondary button) | navigation or local | — | — | — | — |
| Payment Completed (secondary button) | navigation or local | — | — | — | — |
| Payment Declined (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1173` Wallet Integration Command Center: *Back to Wallet Integration Command Center*; carries `clientId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet events webhooks configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet events webhooks untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet events webhooks configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 An entry in `eventTypes` is not in the webhook event catalogue. |

#### Permissions

- `setWalletRiskRules` → `WALLET_CONFIGURE` (configure) · staff
- `createWebhookSubscription` → `DEVELOPER_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.31 | Apply fraud and security controls. | Bundles and Promotions | CONTRACTED | `setWalletRiskRules` |
| 4.3.32 | AI identifies suspicious wallet activity. | Bundles and Promotions | CONTRACTED | `setWalletRiskRules` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1176` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1176`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 10
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 6: Works in Wallet Events, Webhooks & Notification Orchestration → Configure event-driven communication when something changes in Wallet.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (412, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1176?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Wallet Created, Wallet Activated, Wallet Blocked, Wallet Unblocked, Balance Changed, Top-Up Failed, Payment Completed, Payment Declined.
- [ ] Every transition is wired: `BO-1173`.
- [ ] Every gated control is gated: `DEVELOPER_MANAGE`, `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1177` API Security, Access & Integration Permissions

**Ensure integrations receive only the wallet permissions and data required for their function.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`, `PERMISSION_VIEW` (1 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/api-security-access-integration-permissions-bo-1177` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Integration identity | select field | — | — | — | — | — | — |
| Application/client | select field | — | — | — | — | — | — |
| Tenant scope | select field | — | — | — | — | — | — |
| Venue scope | select field | — | — | — | — | — | — |
| API scope | select field | — | — | — | — | Module scopes (`{module}.read`/`{module}.write`) from `listApiScopes`, grouped by module (M17-05, applied 30 September); no scope opens a catalogue write (M17-04). | — |
| Allowed operations | select field | — | — | — | — | — | — |
| Allowed wallet types | select field | — | — | — | — | — | — |
| Maximum transaction | select field | — | — | — | — | — | — |
| Environment | select field | — | — | — | — | — | — |
| IP/network restrictions where applicable | text field | — | — | — | — | — | — |
| Credential expiry | select field | — | — | — | — | — | — |
| Secret/key rotation | select field | — | — | — | — | — | — |
| MFA for administration | select field | — | — | — | — | — | — |
| Certificate configuration | select field | — | — | — | — | — | — |
| Access Models | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | select | — | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | `listApiScopes` ?module |
| Status | radio group | — | Pending · Approved · Rejected · Withdrawn | `listProductionAccessRequests` ?status |
| Status | radio group | — | Draft · Pending approval · Active · Suspended · Retired | `listAuthorisationPolicies` ?status |
| Scope path | text field | — | — | `listAuthorisationPolicies` ?scopePath |

#### Outputs: what the screen shows and produces

**Shown**

**Production access** (banner, from `listProductionAccessRequests`): **Where production access stands** (M17-06): sandbox only, requested (pending), approved (a production client issued by TICVAI) or rejected with the reason. Production keys only after certification; a sandbox key is never promoted.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Developer | the name it points at, never the id | — |
| Sandbox client | the name it points at, never the id | — |
| Listing | the name it points at, never the id | — |
| Scopes | list or chips (count when long) | — |
| Allowed tenants | list or chips (count when long) | — |
| Ip allow list | list or chips (count when long) | — |
| Note | text | — |
| Status | chip: Pending, Approved, Rejected, Withdrawn | — |
| Decided by principal | the name it points at, never the id | — |
| Decided at | 1 Oct 2026, 14:30 | — |
| Reason | text | — |
| Production client | the name it points at, never the id | — |
| Requested at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Read Only (primary button) | navigation or local | — | — | — | — |
| Finance (secondary button) | navigation or local | — | — | — | — |
| Partner (secondary button) | navigation or local | — | — | — | — |
| Internal Service (secondary button) | navigation or local | — | — | — | — |
| High-Risk Operations (secondary button) | navigation or local | — | — | — | — |
| Balance Adjustment (secondary button) | navigation or local | — | — | — | — |
| Wallet Block (secondary button) | navigation or local | — | — | — | — |
| High-Value Refund (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listApiScopes` (onLoad, Scopes to choose from, by module); `listProductionAccessRequests` (onLoad, Where production access stands for these clients); `listAuthorisationPolicies` (onLoad, API access and permissions)

**Where the user goes next**

- → `BO-1173` Wallet Integration Command Center: *Back to Wallet Integration Command Center*; carries `clientId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The api security access configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the api security access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No api security access configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A `production` client without a current certification, or asked for by a developer rather than issued by TICVAI (`certification-required`, M17-06).; 422 A `production` client with an empty `ipAllowList` (`ip-allow-list-required`, M17-07), or a scope that is not in the scope catalogue (`unknown-scope`, M17-05). |

#### Permissions

- `listApiScopes` → `DEVELOPER_VIEW` (read) · public, staff, partner
- `listProductionAccessRequests` → `DEVELOPER_VIEW` (read) · staff, partner
- `listAuthorisationPolicies` → `PERMISSION_VIEW` (read) · staff
- `createApiClient` → `DEVELOPER_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.24 | To provide the ability to enable license for the API only for the specific module. Example. APIs are exposed only for ticketing excluding resource management, Seating Module, etc | Developer & API Management | CONTRACTED | `listApiScopes` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Production access status is shown: sandbox only, requested (pending), approved, or rejected with the reason. Production keys only after certification; the request form says a new production key is issued and the sandbox key stays sandbox. *(agreed · MoM 17 Sep 2026, M17-06 · DI-927)*
- API scopes are picked from a list grouped by module ({module}.read / {module}.write), with unlicensed modules shown disabled rather than hidden; the API reference is grouped by licensable module, then contract. *(agreed · MoM 17 Sep 2026, M17-05, M17-12 · DI-926)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1177` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1177`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 10
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 8: Works in API Security, Access & Integration Permissions → Ensure integrations receive only the wallet permissions and data required for their function.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1177?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Read Only, Finance, Partner, Internal Service, High-Risk Operations, Balance Adjustment, Wallet Block, High-Value Refund.
- [ ] Every transition is wired: `BO-1173`.
- [ ] Every gated control is gated: `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`, `PERMISSION_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1178` Synchronization, Retry & Resilience Configuration

**Configure how Wallet behaves when dependent services or external systems are temporarily unavailable.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/synchronization-retry-resilience-configuration-bo-1178` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Retry attempts | select field | — | — | — | — | — | — |
| Retry interval | select field | — | — | — | — | — | — |
| Exponential backoff | select field | — | — | — | — | — | — |
| Timeout | select field | — | — | — | — | — | — |
| Idempotency | select field | — | — | — | — | — | — |
| Duplicate prevention | select field | — | — | — | — | — | — |
| Queue behavior | select field | — | — | — | — | — | — |
| Dead-letter queue | select field | — | — | — | — | — | — |
| Event retention | select field | — | — | — | — | — | — |
| Replay permission | select field | — | — | — | — | — | — |
| Dependency priority | select field | — | — | — | — | — | — |
| Example | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getWalletReconciliation` ?from |
| To | date picker | — | — | `getWalletReconciliation` ?to |

#### Outputs: what the screen shows and produces

**Data it reads**: `getWalletReconciliation` (onLoad, Synchronisation state)

**Where the user goes next**

- → `BO-1173` Wallet Integration Command Center: *Back to Wallet Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The synchronization retry resilience configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the synchronization retry resilience untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No synchronization retry resilience configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getWalletReconciliation` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1178` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1178`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 10
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 10: Works in Synchronization, Retry & Resilience Configuration → Configure how Wallet behaves when dependent services or external systems are temporarily unavailable.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1178?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1173`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1179` Integration Monitoring & Exception Workbench

**Give technical and operational teams a dedicated workspace for failed integrations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`, `WALLET_CONFIGURE`, `WALLET_OPERATE`, `WALLET_VIEW` (2 configure, 2 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `clientId` (navigation), `disputeId` (navigation), `subscriptionId` (navigation) |
| Route | `/orders-money/integration-monitoring-exception-workbench-bo-1179` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listWalletDisputes` ?status |
| Client | picker: choose a client | — | — | `listWebhookSubscriptions` ?clientId |

**Sent by *Correct mapping*** (`setWalletIntegrationMapping`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| API client `apiClientId` | picker: choose an api client | required | — | — | shows names, sends the id | The `public-api` ApiClient the integration authenticates as. | `setWalletIntegrationMapping` body |
| Field mappings `fieldMappings` | repeatable rows | optional | — | — | — | — | `setWalletIntegrationMapping` body |
| External field `fieldMappings[].externalField` | text field | required | — | — | — | — | `setWalletIntegrationMapping` body |
| Wallet field `fieldMappings[].walletField` | text field | required | — | — | — | — | `setWalletIntegrationMapping` body |
| Transform `fieldMappings[].transform` | text field | optional | — | — | — | — | `setWalletIntegrationMapping` body |
| Currency mappings `currencyMappings` | repeatable rows | optional | — | — | — | — | `setWalletIntegrationMapping` body |
| External code `currencyMappings[].externalCode` | text field | required | — | — | — | — | `setWalletIntegrationMapping` body |
| Currency `currencyMappings[].currency` | text field | required | — | pattern `^[A-Z]{3}$` | — | — | `setWalletIntegrationMapping` body |
| Status mappings `statusMappings` | repeatable rows | optional | — | — | — | — | `setWalletIntegrationMapping` body |
| External status `statusMappings[].externalStatus` | text field | required | — | — | — | — | `setWalletIntegrationMapping` body |
| Wallet status `statusMappings[].walletStatus` | text field | required | — | — | — | — | `setWalletIntegrationMapping` body |
| Credit type mappings `creditTypeMappings` | repeatable rows | optional | — | — | — | — | `setWalletIntegrationMapping` body |
| External code `creditTypeMappings[].externalCode` | text field | required | — | — | — | — | `setWalletIntegrationMapping` body |
| Credit type `creditTypeMappings[].creditTypeId` | picker: choose a credit type | required | — | — | shows names, sends the id | — | `setWalletIntegrationMapping` body |
| Date time format `dateTimeFormat` | text field | optional | ISO-8601 | — | — | The format the integration sends, e.g. ISO-8601 or a pattern such as dd/MM/yyyy HH:mm. | `setWalletIntegrationMapping` body |
| Time zone `timeZone` | text field | optional | — | — | — | IANA zone the integration's local times are in. Null means UTC offsets are sent. | `setWalletIntegrationMapping` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setWalletIntegrationMapping` body |

**Sent by *Reprocess*** (`resolveWalletDispute`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | segmented control | required | — | Reprocess · Escalate · Resolve | — | — | `resolveWalletDispute` body |
| Outcome `outcome` | segmented control | optional | — | Upheld · Rejected | — | Required with `resolve`. | `resolveWalletDispute` body |
| Resolution note `resolutionNote` | text area | optional | — | max length 2000 | — | Required with `resolve`. | `resolveWalletDispute` body |
| Escalate to role `escalateToRoleId` | picker: choose an escalate to role | optional | — | — | shows names, sends the id | Required with `escalate`. | `resolveWalletDispute` body |
| Adjustment `adjustmentId` | picker: choose an adjustment | optional | — | — | shows names, sends the id | The `adjustWallet` adjustment that settled an upheld dispute, if any. | `resolveWalletDispute` body |

**Sent by *Suspend integration*** (`setApiClientStatus`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | segmented control | required | — | Active · Suspended | — | — | `setApiClientStatus` body |
| Reason `reason` | text area | optional | — | max length 500 | — | Required with `suspended`. | `setApiClientStatus` body |

**Sent by *Withdraw dispute*** (`withdrawWalletDispute`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 500 | — | — | `withdrawWalletDispute` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every integration monitoring exception** (data table)

| Shows | Format | Notes |
|---|---|---|
| Exception ID | text | not in the schema: `Exception ID` |
| Integration | text | not in the schema: `Integration` |
| Wallet | text | not in the schema: `Wallet` |
| Transaction | text | not in the schema: `Transaction` |
| Endpoint/event | text | not in the schema: `Endpoint/event` |
| Error code | text | not in the schema: `Error code` |
| Error message | text | not in the schema: `Error message` |
| Attempt count | text | not in the schema: `Attempt count` |
| First failure | text | not in the schema: `First failure` |
| Last retry | text | not in the schema: `Last retry` |
| Priority | text | not in the schema: `Priority` |
| Owner | text | not in the schema: `Owner` |
| Status | text | not in the schema: `Status` |

**The selected integration monitoring exception** (detail panel): The pack groups this record's detail under its own headings: “Exception Categories”, “Workflow”.

| Shows | Format | Notes |
|---|---|---|
| Exception ID | text | not in the schema: `Exception ID` |
| Integration | text | not in the schema: `Integration` |
| Wallet | text | not in the schema: `Wallet` |
| Transaction | text | not in the schema: `Transaction` |
| Endpoint/event | text | not in the schema: `Endpoint/event` |
| Error code | text | not in the schema: `Error code` |
| Error message | text | not in the schema: `Error message` |
| Attempt count | text | not in the schema: `Attempt count` |
| First failure | text | not in the schema: `First failure` |
| Last retry | text | not in the schema: `Last retry` |
| Priority | text | not in the schema: `Priority` |
| Owner | text | not in the schema: `Owner` |
| Status | text | not in the schema: `Status` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Retry (primary button) | navigation or local | — | — | — | — |
| Replay (secondary button) | navigation or local | — | — | — | — |
| Correct mapping (secondary button) | `setWalletIntegrationMapping` PUT `/wallet-integration-mappings` | WalletIntegrationMapping | WalletIntegrationMapping | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.; 422 A credit-type mapping names a credit type that does not exist or is retired, or an external value is mapped twice within one … | — |
| Reprocess (secondary button) | `resolveWalletDispute` POST `/wallet-disputes/{disputeId}/resolve` | inline | WalletDispute | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The dispute is already closed (`upheld`, `rejected` or `withdrawn`).; 422 `resolve` without `outcome` or … | — |
| Escalate (secondary button) | `resolveWalletDispute` POST `/wallet-disputes/{disputeId}/resolve` | inline | WalletDispute | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The dispute is already closed (`upheld`, `rejected` or `withdrawn`).; 422 `resolve` without `outcome` or … | — |
| Suspend integration (destructive button) | `setApiClientStatus` POST `/api-clients/{clientId}/status` | inline | ApiClient | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The client is `revoked`, which is terminal.; 422 `suspended` without a `reason`. | — |
| Mark resolved (secondary button) | `resolveWalletDispute` POST `/wallet-disputes/{disputeId}/resolve` | inline | WalletDispute | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The dispute is already closed (`upheld`, `rejected` or `withdrawn`).; 422 `resolve` without `outcome` or … | — |
| Withdraw dispute (primary button) | `withdrawWalletDispute` POST `/wallet-disputes/{disputeId}/withdraw` | inline | WalletDispute | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The dispute is already closed (`upheld`, `rejected` or `withdrawn`). | — |

**Data it reads**: `listWalletDisputes` (onLoad, Integration exceptions); `listApiClients` (onLoad, The integrations whose exceptions are worked here); `listWebhookSubscriptions` (onLoad, The webhook subscriptions whose events are replayed)

**Where the user goes next**

- → `BO-1173` Wallet Integration Command Center: *Back to Wallet Integration Command Center*; carries `clientId`, `subscriptionId`

**What opens over it**

- confirmDialog *Suspend integration*: **Suspend integration on a integration monitoring exception is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The integration monitoring exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the integration monitoring exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No integration monitoring exception yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the integration monitoring exception are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The client is `revoked`, which is terminal.; 409 The dispute is already closed (`upheld`, `rejected` or `withdrawn`).; 422 A credit-type mapping names a credit type that does not exist or is retired, or an external value is mapped twice within one list.; 422 `resolve` without `outcome` or `resolutionNote`, or `escalate` without `escalateToRoleId`. |

#### Permissions

- `listWalletDisputes` → `WALLET_VIEW` (read) · staff
- `replayEvents` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `listApiClients` → `DEVELOPER_VIEW` (read) · staff, partner
- `listWebhookSubscriptions` → `DEVELOPER_VIEW` (read) · staff, partner
- `setWalletIntegrationMapping` → `WALLET_CONFIGURE` (configure) · staff
- `resolveWalletDispute` → `WALLET_OPERATE` (operate) · staff
- `withdrawWalletDispute` → `WALLET_OPERATE` (operate) · staff, guest
- `setApiClientStatus` → `DEVELOPER_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.19 | System shall support replay of historical events for recovery, synchronization, troubleshooting, and integration reprocessing purposes. | Developer & API Management | CONTRACTED | `replayEvents` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1179` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1179`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 10
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 12: Works in Integration Monitoring & Exception Workbench → Give technical and operational teams a dedicated workspace for failed integrations.

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (404, 409, 412, 422).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1179?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Retry, Replay, Correct mapping, Reprocess, Escalate, Suspend integration, Mark resolved, Withdraw dispute.
- [ ] Every transition is wired: `BO-1173`.
- [ ] Every gated control is gated: `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`, `WALLET_CONFIGURE`, `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1180` Wallet Configuration Governance & Version Control

**Provide centralized governance for configuration changes across all ten Wallet boards. This screen becomes the master configuration governance layer for the entire Wallet module.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-configuration-governance-version-control-bo-1180` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every wallet governance version** (data table)

| Shows | Format | Notes |
|---|---|---|
| Cash priority: 3 → 5 | text | not in the schema: `Cash Priority: 3 → 5` |
| Bonus priority: 2 → 1 | text | not in the schema: `Bonus Priority: 2 → 1` |
| FEFO: enabled → enabled | text | not in the schema: `FEFO: Enabled → Enabled` |
| Gift card priority: 4 → 3 | text | not in the schema: `Gift Card Priority: 4 → 3` |

**The selected wallet governance version** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Cash priority: 3 → 5 | text | not in the schema: `Cash Priority: 3 → 5` |
| Bonus priority: 2 → 1 | text | not in the schema: `Bonus Priority: 2 → 1` |
| FEFO: enabled → enabled | text | not in the schema: `FEFO: Enabled → Enabled` |
| Gift card priority: 4 → 3 | text | not in the schema: `Gift Card Priority: 4 → 3` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1173` Wallet Integration Command Center: *Back to Wallet Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet governance version list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet governance version untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet governance version yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet governance version are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `publishWalletConfiguration` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1180` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1180`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 10
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 14: Works in Wallet Configuration Governance & Version Control → Provide centralized governance for configuration changes across all ten Wallet boards. This screen becomes the master configuration governance layer for the entire Wallet module.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1180?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes.
- [ ] Every transition is wired: `BO-1173`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1181` Approval, Publication & Change Management

**Control how Wallet configuration moves safely from draft into production.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_REQUEST`, `WALLET_CONFIGURE` (1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/approval-publication-change-management-bo-1181` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Immediate publication | select field | — | — | — | — | — | — |
| Scheduled publication | select field | — | — | — | — | — | — |
| Tenant-specific rollout | select field | — | — | — | — | — | — |
| Venue-specific rollout | select field | — | — | — | — | — | — |
| Effective date | select field | — | — | — | — | — | — |
| Pilot rollout | select field | — | — | — | — | — | — |
| Emergency rollback | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1173` Wallet Integration Command Center: *Back to Wallet Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval publication change configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval publication change untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval publication change configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. (ApprovalStateProblem) |

#### Permissions

- `publishWalletConfiguration` → `WALLET_CONFIGURE` (configure) · staff
- `createApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.59 | Complimentary entitlement redemption | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.64 | Employees shall submit requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.65 | Managers shall approve requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 11.1.51 | Draft Approval Requests - System shall support saving approval requests in draft status. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |
| 11.1.63 | API-Based Approval Processing - System shall expose approval workflows through APIs. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1181` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1181`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 10
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 16: Works in Approval, Publication & Change Management → Control how Wallet configuration moves safely from draft into production.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1181?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes.
- [ ] Every transition is wired: `BO-1173`.
- [ ] Every gated control is gated: `APPROVAL_REQUEST`, `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1182` Wallet Platform Health, Audit & Administration Center

**Provide the final master-administration screen for the entire TICVAI Wallet ecosystem. This should become the control tower for all ten Wallet boards.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Master Health KPIs) and a per-row directory (§Display) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-platform-health-audit-administration-center-bo-1182` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| As of | date picker | — | — | `getWalletLiability` ?asOf |
| Group by | radio group | — | Credit type · Wallet type · Venue · Age band | `getWalletLiability` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Wallet Service Availability** (metric tile)

**API Success Rate** (metric tile)

**Average Authorization Time** (metric tile)

**Failed Transactions** (metric tile)

**Pending Events** (metric tile)

**Reconciliation Exceptions** (metric tile)

**Fraud Alerts** (metric tile)

**Ledger Integrity** (metric tile)

**Configuration Errors** (metric tile)

**Every wallet platform health** (data table)

| Shows | Format | Notes |
|---|---|---|
| Wallet engine | text | not in the schema: `Wallet Engine` |

**The selected wallet platform health** (detail panel): The pack groups this record's detail under its own headings: “Healthy”, “Search across”, “Every record should contain”, “Authorized super administrators can”.

| Shows | Format | Notes |
|---|---|---|
| Wallet engine | text | not in the schema: `Wallet Engine` |

**Data it reads**: `getWalletLiability` (onLoad, Platform health and audit)

**Where the user goes next**

- → `BO-1173` Wallet Integration Command Center: *Back to Wallet Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet platform health list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet platform health untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet platform health yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet platform health are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getWalletLiability` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1182` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS195 Wallet Configuration Backend Structure v1.0 Board 10.dc.html#bo-1182`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 10
- Flow F302 *Wallet Configuration Backend Structure v1.0 board 10: Wallet Integration …*, step 18: Works in Wallet Platform Health, Audit & Administration Center → Provide the final master-administration screen for the entire TICVAI Wallet ecosystem. This should become the control tower for all ten Wallet boards.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1182?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1173`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
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

### In P08 · Orders & Money

- AI-assisted reporting for accountants/finance managers is phase two; phase-one finance screens do not include it. *(agreed · MoM 12 Aug 2026, 6. Finance & Ledger Architecture Overview · DI-278)*
- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*
- Legal entities view lists all tenant sites with country, currency and active/inactive status. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-261)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*

**3 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createApiClient": {"method":"POST","path":"/api-clients","contract":"public-api","summary":"Create a client with scopes and an environment","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApiClient","responds":null},
"createApprovalRequest": {"method":"POST","path":"/approval-requests","contract":"approvals","summary":"Raise a request","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateApprovalRequest","responds":"ApprovalRequest"},
"createWebhookSubscription": {"method":"POST","path":"/webhook-subscriptions","contract":"public-api","summary":"Subscribe to business events","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WebhookSubscription","responds":"WebhookSubscription"},
"getWalletLiability": {"method":"GET","path":"/wallet-liability","contract":"wallet","summary":"What is outstanding, and what is breakage","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"asOf","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"WalletLiabilityRow"},
"getWalletReconciliation": {"method":"GET","path":"/wallet-reconciliation","contract":"wallet","summary":"The wallet sub-ledger against the general ledger and the acquirer","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true}],"requestBody":null,"responds":"WalletReconciliation"},
"listApiClients": {"method":"GET","path":"/api-clients","contract":"public-api","summary":"Registered clients for this developer","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ApiClient"},
"listApiScopes": {"method":"GET","path":"/api-scopes","contract":"public-api","summary":"The scope catalogue, one read and one write scope per module","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"module","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAuthorisationPolicies": {"method":"GET","path":"/authorisation-policies","contract":"identity","summary":"Attribute-based authorisation policies","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"scopePath","in":"query","required":null}],"requestBody":null,"responds":"AuthorisationPolicy"},
"listProductionAccessRequests": {"method":"GET","path":"/production-access-requests","contract":"public-api","summary":"Production access requests, pending first","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWalletDisputes": {"method":"GET","path":"/wallet-disputes","contract":"wallet","summary":"Contested transactions and operational exceptions","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"WalletDispute"},
"listWalletTypes": {"method":"GET","path":"/wallet-types","contract":"wallet","summary":"The kinds of wallet that may exist — who owns one","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"WalletType"},
"listWebhookSubscriptions": {"method":"GET","path":"/webhook-subscriptions","contract":"public-api","summary":"The tenant's webhook subscriptions, filterable by API client","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"clientId","in":"query","required":false}],"requestBody":null,"responds":"WebhookSubscription"},
"publishWalletConfiguration": {"method":"POST","path":"/wallet-configuration/publish","contract":"wallet","summary":"Validate and publish the wallet configuration as a version","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletConfigurationVersion"},
"replayEvents": {"method":"POST","path":"/webhook-subscriptions/{subscriptionId}/replay","contract":"public-api","summary":"Re-deliver events from a point in time","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"resolveWalletDispute": {"method":"POST","path":"/wallet-disputes/{disputeId}/resolve","contract":"wallet","summary":"Work a wallet dispute or integration exception","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletDispute"},
"setApiClientStatus": {"method":"POST","path":"/api-clients/{clientId}/status","contract":"public-api","summary":"Suspend or reactivate an integration, reversibly","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApiClient"},
"setWalletChannelRules": {"method":"PUT","path":"/wallet-channel-rules","contract":"wallet","summary":"Where a wallet may be used, on what, and when it may not","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletChannelRules","responds":"WalletChannelRules"},
"setWalletIntegrationMapping": {"method":"PUT","path":"/wallet-integration-mappings","contract":"wallet","summary":"How one integration's fields, currencies, statuses and credit types map onto the wallet","permission":"WALLET_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletIntegrationMapping","responds":"WalletIntegrationMapping"},
"setWalletRiskRules": {"method":"PUT","path":"/wallet-risk-rules","contract":"wallet","summary":"Velocity, behaviour and what happens when a rule trips","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletRiskRules","responds":"WalletRiskRules"},
"testWebhookSubscription": {"method":"POST","path":"/webhook-subscriptions/{subscriptionId}/test","contract":"public-api","summary":"Send a signed test event to the endpoint, now","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WebhookDelivery"},
"withdrawWalletDispute": {"method":"POST","path":"/wallet-disputes/{disputeId}/withdraw","contract":"wallet","summary":"Withdraw a wallet dispute that is still open or under review","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletDispute"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessCondition": {"type":"object","description":"**One attribute, one operator, one value** — and the attribute names are an enum rather than free text, because a policy that reads `venu.type` silently never matches.\nThe enum is the matrix, row by row: user (3.3.7), employee (3.3.8), membership (3.3.9), accreditation (3.3.10), customer segment (3.3.11), resource classification (3.3.12), venue (3.3.13), attraction (3.3.14), device (3.3.15), day of week (3.3.16), season (3.3.17), event (3.3.18), capacity (3.3.19), occupancy (3.3.20), risk score (3.3.21), location (3.3.2) and time (3.3.3).\n","required":["attribute","operator"],"properties":{"attribute":{"type":"string","enum":["user.attribute","employee.attribute","employee.onShift","membership.tier","membership.status","accreditation.type","accreditation.status","customer.segment","resource.classification","venue.attribute","venue.id","attraction.attribute","device.kind","device.id","device.trusted","time.ofDay","time.dayOfWeek","time.season","time.withinOperatingHours","event.id","event.status","capacity.utilisationPercent","occupancy.level","risk.score","ticket.status","location.scopePath"]},"key":{"type":"string","nullable":true,"description":"For the `*.attribute` forms — which attribute, by code."},"operator":{"type":"string","enum":["equals","notEquals","in","notIn","greaterThan","lessThan","between","contains","startsWith","exists"]},"value":{"nullable":true,"description":"The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. Null for `exists`; `in`, `notIn` and `between` use `values`.\n"},"values":{"type":"array","items":{"type":"string"}}}},
"ApiClient": {"type":"object","x-ticvai-persistence":"control.api_client","description":"CF-135a. **The one credential model.** 2.7.52, 7.1.25 and 7.1.30 each asserted their own, so a partner API key, a POS integration credential and a webstore credential were three unrelated things with three lifecycles.\n","required":["id","developerId","name","environment","scopes","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid"},"name":{"type":"string"},"clientId":{"type":"string","readOnly":true},"environment":{"type":"string","enum":["sandbox","production"],"description":"**Bound to one, stated on the object rather than by naming convention.** A key that works in both is a key somebody will use in the wrong one.\n"},"scopes":{"type":"array","description":"**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing. **Module scopes** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, one of `listApiScopes`.\n","items":{"type":"string","pattern":"^[a-zA-Z]+\\.(read|write)$"}},"issuedBy":{"type":"string","enum":["partner","ticvai"],"readOnly":true,"description":"Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`.\n"},"certificationListingId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"control.integration_listing","description":"For a production client, the certified integration it was issued against."},"credentialTtlDays":{"type":"integer","minimum":1,"maximum":730,"nullable":true,"description":"Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry)."},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the key stops working unless rotated. No token is issued after it."},"allowedTenantIds":{"type":"array","description":"13.1.46. **Which tenants this client may act for.** A developer integrating for one venue must not reach another, and a client with an empty list reaches none.\n","items":{"type":"string","format":"uuid"}},"ipAllowList":{"type":"array","description":"13.1.38. **Required on a production client** (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the internet); optional in the sandbox. CIDR ranges. Checked at token issue and on every call.\n","items":{"type":"string"}},"status":{"type":"string","enum":["active","suspended","revoked"],"readOnly":true},"lastUsedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**A credential unused for a year is a credential nobody will notice being stolen.**\n"}}},
"ApiScope": {"type":"object","x-ticvai-persistence":"none — generated at release from x-ticvai-api-scope on each partner-callable operation","description":"**One module scope** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, and the operations it opens.\n**A write scope never opens a catalogue write** (M17-04): `ticketing.write` opens carts, orders and holds for a partner or developer client, and no product, price list, price, channel capacity, lifecycle or alternative-code write, since those operations are not partner-callable and carry no `x-ticvai-api-scope`. Only a platform-staff `ApiLicence.catalogueWriteException` opens one, for one named client.\n","required":["scope","module","access"],"properties":{"scope":{"type":"string","description":"e.g. `ticketing.read`."},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"access":{"type":"string","enum":["read","write"]},"description":{"type":"string"},"operations":{"type":"array","items":{"type":"object","properties":{"contract":{"type":"string"},"operationId":{"type":"string"}}}},"licensed":{"type":"boolean","description":"Whether the caller's tenant licenses the module (`ApiLicence.licensedModules`)."}}},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"AuthorisationPolicy": {"type":"object","x-ticvai-persistence":"identity.authorisation_policy","description":"3.3. **Conditions and an effect, evaluated by one engine.** A role says who you are; a policy says under what circumstances that is enough.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). The package has two: this one, and the access contract's `AccessDynamicPolicy` (`access.dynamic_policy`). **This one governs who may do what in the software**: a principal's permissions on operations and screens (`permissions` names them), narrowed or extended by who, where, when and on what device, and decided by `evaluateAccess`. **`AccessDynamicPolicy` governs who may pass which gate**: a guest's, holder's or employee's admission at an access point, decided in the gate's validation with results such as `requireId` or `requireSupervisor` that mean nothing to a permission check. A staff member's badge opening a staff door is a gate decision (access); the same staff member approving a refund is a permission decision (here).\n**Settled by ADR-0068 (accepted 1 October): guest admission lives in Access only.** This engine keeps staff authorisation and was renamed to say so: `identity.access_policy` became `identity.authorisation_policy`, its versions `identity.authorisation_policy_version`, and its operations `*AuthorisationPolicy*`. \"Access policy\" now means `AccessDynamicPolicy` and nothing else.\n","required":["code","name","effect"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"Assigned by the server on `createAuthorisationPolicy`; the path names the policy on update."},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"isTemplate":{"type":"boolean","default":false},"permissions":{"type":"array","items":{"type":"string"},"description":"**Which permissions this policy speaks to.** A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about.\n"},"conditions":{"type":"array","items":{"$ref":"#/components/schemas/AccessCondition"}},"combining":{"type":"string","enum":["allMustMatch","anyMayMatch"],"default":"allMustMatch"},"effect":{"type":"string","enum":["permit","deny"],"description":"**Deny wins over permit when two policies disagree.** 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of every mistake anybody has made.\n"},"priority":{"type":"integer","default":0},"scopePath":{"type":"string","description":"3.3.40 to 3.3.43. **Tenant, venue and cross-venue policies are one mechanism**, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance is the prefix walk rather than a second table.\n"},"appliesToRoleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"status":{"type":"string","readOnly":true,"description":"**Moved only by `setAuthorisationPolicyState`.** A policy is created as a `draft`, and a status sent in a create or update body is ignored — otherwise a write could skip the approval 3.3.26 requires.\n","enum":["draft","pendingApproval","active","suspended","retired"]},"version":{"type":"integer","default":1,"readOnly":true,"description":"Set by the server; every `updateAuthorisationPolicy` writes a new version."},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"delegatedAdminRoleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"3.3.35. **Who may edit this policy without being a platform administrator.** A venue manager tuning their own opening-hours rule should not need someone who can edit every tenant's.\n"}}},
"CreateApprovalRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","kind","subjectContract","subjectType","subjectId","scopePath","summary"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"subjectContract":{"type":"string","description":"Which contract owns the thing being approved."},"subjectType":{"type":"string"},"subjectId":{"type":"string","description":"**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"},"scopePath":{"type":"string"},"summary":{"type":"string","maxLength":300,"description":"What the approver sees in their queue before opening it."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"attributes":{"type":"object","additionalProperties":true},"justification":{"type":"string","maxLength":1000},"isDraft":{"type":"boolean","default":false,"description":"True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProductionAccessRequest": {"type":"object","x-ticvai-persistence":"control.production_access_request","description":"**A developer's request for production keys** (17 September minutes, M17-06): sandbox, then certification, then production.\n","required":["id","developerId","sandboxClientId","listingId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid","readOnly":true},"sandboxClientId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"control.api_client"},"listingId":{"type":"string","format":"uuid","x-ticvai-references":"control.integration_listing"},"scopes":{"type":"array","items":{"type":"string"}},"allowedTenantIds":{"type":"array","items":{"type":"string","format":"uuid"}},"ipAllowList":{"type":"array","items":{"type":"string"}},"note":{"type":"string","nullable":true},"status":{"type":"string","enum":["pending","approved","rejected","withdrawn"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"reason":{"type":"string","nullable":true,"readOnly":true},"productionClientId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"control.api_client"},"requestedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WalletChannelRules": {"type":"object","x-ticvai-persistence":"wallet.channel_rules","description":"Board 6. **The offline rule is stated once, not per device.**","properties":{"allowedChannels":{"type":"array","items":{"type":"string"}},"allowedCredentialKinds":{"type":"array","items":{"type":"string","enum":["card","wristband","nfc","rfid","qr","mobileApp","digitalKey"]}},"requiresPin":{"type":"boolean","default":false},"pinAboveAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"offlineAllowed":{"type":"boolean","default":false},"offlineFloorLimit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"offlineMaximumAgeMinutes":{"type":"integer","nullable":true,"description":"**How stale a cached balance may be before the device refuses.** Without a ceiling an offline terminal spends a balance that ran out yesterday.\n"},"acceptancePointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"scopePath":{"type":"string"}}},
"WalletConfigurationVersion": {"type":"object","x-ticvai-persistence":"wallet.configuration_version","description":"Boards 1.10 and 10.8. **Ten boards of configuration that interact.**","properties":{"version":{"type":"integer"},"publishedAt":{"type":"string","format":"date-time","nullable":true},"publishedBy":{"type":"string","format":"uuid","nullable":true},"note":{"type":"string","nullable":true},"findings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["blocking","warning"]},"code":{"type":"string"},"message":{"type":"string"}}}},"scopePath":{"type":"string"}}},
"WalletDispute": {"type":"object","x-ticvai-persistence":"wallet.dispute","description":"Board 7.9. **Internal, and the venue decides it** — unlike a card chargeback.","required":["walletId","description"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"transactionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"description":{"type":"string"},"raisedBy":{"type":"string","format":"uuid"},"raisedAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["open","investigating","escalated","upheld","rejected","withdrawn"],"description":"`escalated` added with `resolveWalletDispute` (VM close-out, 29 September). `upheld`, `rejected` and `withdrawn` are closed."},"resolution":{"type":"string","nullable":true},"escalatedToRoleId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"reprocessedTransactionIds":{"type":"array","readOnly":true,"description":"Transactions created by a `reprocess` action.","items":{"type":"string","format":"uuid"}},"resolvedBy":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"adjustmentId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"WalletIntegrationMapping": {"type":"object","x-ticvai-persistence":"wallet.integration_mapping","description":"Board 10, pp.118 and 122. **One per integration**, keyed by the `public-api` client. An unmapped inbound value is parked as an exception, never guessed.","required":["apiClientId"],"properties":{"apiClientId":{"type":"string","format":"uuid","description":"The `public-api` ApiClient the integration authenticates as."},"fieldMappings":{"type":"array","items":{"type":"object","required":["externalField","walletField"],"properties":{"externalField":{"type":"string"},"walletField":{"type":"string"},"transform":{"type":"string","nullable":true}}}},"currencyMappings":{"type":"array","items":{"type":"object","required":["externalCode","currency"],"properties":{"externalCode":{"type":"string"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"}}}},"statusMappings":{"type":"array","items":{"type":"object","required":["externalStatus","walletStatus"],"properties":{"externalStatus":{"type":"string"},"walletStatus":{"type":"string"}}}},"creditTypeMappings":{"type":"array","items":{"type":"object","required":["externalCode","creditTypeId"],"properties":{"externalCode":{"type":"string"},"creditTypeId":{"type":"string","format":"uuid"}}}},"dateTimeFormat":{"type":"string","default":"ISO-8601","description":"The format the integration sends, e.g. ISO-8601 or a pattern such as dd/MM/yyyy HH:mm."},"timeZone":{"type":"string","nullable":true,"description":"IANA zone the integration's local times are in. Null means UTC offsets are sent."},"scopePath":{"type":"string"}}},
"WalletLiabilityRow": {"type":"object","description":"Boards 9.5 and 9.6. **The number the finance director asks for.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"outstanding":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expiringThisPeriod":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"breakageRecognised":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"walletCount":{"type":"integer"},"oldestLotAt":{"type":"string","format":"date","nullable":true}}},
"WalletReconciliation": {"type":"object","description":"Board 9.4. **Three sources, and the exception names which pair disagrees.**","properties":{"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"subLedgerTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"generalLedgerTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquirerTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exceptions":{"type":"array","items":{"type":"object","properties":{"pair":{"type":"string","enum":["subLedgerVsGeneralLedger","subLedgerVsAcquirer","generalLedgerVsAcquirer"]},"difference":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"transactionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"likelyCause":{"type":"string","nullable":true}}}}}},
"WalletRiskRules": {"type":"object","x-ticvai-persistence":"wallet.risk_rules","description":"Boards 8.2 to 8.7. **A risk rule with no action is a report.**","properties":{"rules":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"signal":{"type":"string","enum":["velocityCount","velocityAmount","newCredential","geographyJump","deviceChange","dormantThenLarge","repeatedFailure","refundPattern","accountSharing","duplicateTransaction","aiRiskScore"],"description":"4.3.32 (29 September, build pass). **`accountSharing`**: one wallet or credential used from more devices or places at once than one person can be (`threshold` concurrent devices within `windowMinutes`). **`duplicateTransaction`**: the same amount at the same acceptance point within `windowMinutes` (`threshold` repeats). **`aiRiskScore`**: the score the `ai` risk engine returns for the wallet operation (`scoreTransactionRisk`, rules first and statistical baselines as history builds, ai-system-design 3.10); `threshold` is the score at or above which the rule acts. The wallet keeps its own rules and actions; the AI finding and its case are the `ai` contract's (`listRiskAlerts`)."},"threshold":{"type":"number"},"windowMinutes":{"type":"integer"},"action":{"type":"string","enum":["scoreOnly","challenge","holdTransaction","freezeWallet","raiseCase"]},"minimumConfidence":{"type":"number","nullable":true,"description":"**Required before an automated freeze.** A rule that freezes on a false positive will eventually freeze a family in a queue.\n"},"alertOnAction":{"type":"boolean","default":true},"status":{"type":"string","readOnly":true,"enum":["active","suspended","emergencyDisabled"],"default":"active","description":"Set by `setWalletRiskRuleStatus`, not by publishing the rule set. A rule not `active` is evaluated for nothing (VM close-out, 29 September)."},"statusReason":{"type":"string","nullable":true,"readOnly":true},"statusUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a `suspended` rule returns to `active` by itself."}}}},"scopePath":{"type":"string"}}},
"WalletType": {"type":"object","x-ticvai-persistence":"wallet.wallet_type","description":"Board 1.2. **Who owns a wallet** — the first of the two vocabularies.","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"ownerKind":{"type":"string","enum":["guest","registeredCustomer","family","parent","child","corporate","school","employee"]},"storedValueCapability":{"type":"boolean","default":true,"description":"Board 1.2. Whether this wallet holds a balance at all. A pure entitlement wallet — passes and vouchers, no money — does not.\n"},"topUpCapability":{"type":"boolean","default":false},"transferCapability":{"type":"boolean","default":false},"refundCapability":{"type":"boolean","default":false},"giftCardSupport":{"type":"boolean","default":false},"voucherSupport":{"type":"boolean","default":false},"membershipCreditSupport":{"type":"boolean","default":false},"wearableSupport":{"type":"boolean","default":false},"usageChannels":{"type":"array","description":"**Where this wallet may be used, declared on the type itself.** Board 1.2 configures online, POS, mobile-app and API usage per wallet type, and this is what lets one `topUpWallet` serve every caller: the operation is shared and the type says which channel may reach it. `WalletChannelRules` still governs the per-credential detail — PIN thresholds, offline floor limits — and this governs whether the channel is open at all.\n","items":{"type":"string","enum":["online","pos","mobileApp","api","kiosk","reader"]}},"presetName":{"type":"string","description":"**The client's own name for this composition** — \"Resort Wallet\", \"Cashless Venue Wallet\", \"Closed-Loop Wallet\". Board 1.2 lists thirteen such names as examples, not as kinds: they are combinations of `ownerKind`, `allowedCreditTypeIds` and `scopePath`. Naming the preset keeps the client's vocabulary without hard-coding it into an enum.\n"},"holderMayDifferFromOwner":{"type":"boolean","default":false,"description":"**A child wallet's owner is the parent.** Without this the model has to pretend a seven-year-old holds an account.\n"},"requiresIdentification":{"type":"boolean","default":false},"maximumBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"allowedCreditTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"allowNegativeBalance":{"type":"boolean","default":false},"sharedStructureAllowed":{"type":"boolean","default":false},"lifecycleStates":{"type":"array","items":{"type":"string"}},"numberingPattern":{"type":"string","nullable":true},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"WebhookDelivery": {"type":"object","x-ticvai-persistence":"control.webhook_delivery","description":"13.1.30. **The log a developer needs most**, and without it every question becomes a support ticket.\n","required":["id","subscriptionId","eventType","status"],"properties":{"id":{"type":"string","format":"uuid"},"subscriptionId":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"eventType":{"type":"string"},"status":{"type":"string","enum":["pending","delivered","failed","retrying","abandoned"]},"attemptCount":{"type":"integer"},"responseCode":{"type":"integer","nullable":true},"responseBodyExcerpt":{"type":"string","nullable":true,"description":"**Truncated, and it is what makes the log useful** — a 500 with the receiver's own error message in it answers the question without a conversation.\n"},"isReplay":{"type":"boolean","default":false},"isTest":{"type":"boolean","default":false,"description":"Sent by `testWebhookSubscription` (VM close-out, 29 September). Marked in the payload so a receiver never books it, and never counted towards `consecutiveFailures`.\n"},"deliveredAt":{"type":"string","format":"date-time","nullable":true}}},
"WebhookEventType": {"type":"string","description":"**The webhook event catalogue: every event a subscription may name** (29 September, build pass). Each value is the `name` of an event in `events/` — `aggregate.pastTenseFact`, published through `platform.outbox` by exactly one context. A name is added here in the same change that adds its event file, and never before.\n**Added 29 September**, each closing a requirement that had the webhook mechanism and nothing to subscribe to:\n| Events | Publisher | Requirement | |---|---|---| | `device.statusChanged`, `device.tamperDetected`, `device.enrolmentChanged`, `device.firmwareReleased`, `device.firmwareRolloutCompleted` | tenancy | 16.9.56 | | `accreditation.applicationDecided`, `accreditation.holderStatusChanged`, `accreditation.credentialIssued`, `accreditation.renewalDue` | accreditation | 12.1.53 | | `approval.requested`, `approval.escalated`, `approval.stepCompleted`, `approval.expired` | approvals | 11.1.64, 11.1.66 | | `seat.held`, `seat.released`, `seat.blocked`, `seatMap.published` | seating | 21.13.4 | | `consent.deviceConsentRecorded`, `consent.deviceConsentClaimed` | marketing | 2.6.65 | | `order.chargebackRecorded` | orders | 8.3.11 to 8.3.15 (a tenant's own finance or fraud tooling) | | `entitlement.expiringSoon` | access | 5.5.30 (a tenant's own CRM) | | `apiClient.anomalyDetected` | public-api | 17 September minutes M17-07 (added 30 September with its event file) |\n**Deprecated** (1 October, ADR-0067 amendment): `device.enrolmentChanged` is still offered but nothing inside the platform consumes it any more; it is removed at the next major version of this API. Subscribers are told in the release note.\n**Published and deliberately not offered** (29 September, build pass, group G2): `identity.credentialResetRequested` and `identity.loginRecorded` are security signals, and a stream of them to an outside receiver is a map of which accounts are under attack; `storefront.sessionEvent` is high-volume fraud telemetry, not a business fact a receiver acts on.\n","x-ticvai-deprecated-values":["device.enrolmentChanged"],"enum":["access.validated","accreditation.applicationDecided","accreditation.credentialIssued","accreditation.holderStatusChanged","accreditation.renewalDue","ai.ceilingApproaching","apiClient.anomalyDetected","approval.escalated","approval.expired","approval.granted","approval.rejected","approval.requested","approval.stepCompleted","assets.documentIndexed","cart.abandoned","catalogue.productPublished","consent.deviceConsentClaimed","consent.deviceConsentRecorded","conversation.handedOver","device.enrolmentChanged","device.firmwareReleased","device.firmwareRolloutCompleted","device.statusChanged","device.tamperDetected","entitlement.expiringSoon","entitlement.issued","entitlement.statusChanged","fnb.menuPublished","fnb.orderReady","inventory.purchaseOrderReceived","ledger.journalPosted","ledger.periodClosed","maintenance.assetReturnedToService","maintenance.templatePublished","maintenance.workOrderCompleted","marketing.caseClosed","order.chargebackRecorded","order.completed","order.paid","order.refunded","performance.cancelled","reporting.definitionPublished","retail.merchandisePublished","seat.blocked","seat.held","seat.released","seat.sold","seatMap.published","shift.closed","stock.depleted","tenant.suspended","whitelabel.contentPublished"]},
"WebhookSubscription": {"type":"object","x-ticvai-persistence":"control.webhook_subscription","description":"13.1.26, 13.3.18 and 13.3.22. **The 29 events already exist and nothing outside could receive one.**\n","required":["id","clientId","endpointUrl","eventTypes","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"clientId":{"type":"string","format":"uuid"},"endpointUrl":{"type":"string"},"eventTypes":{"type":"array","description":"**Filtered at subscription, not at delivery.** A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to. Each entry is a name from the webhook event catalogue (`WebhookEventType`).\n","items":{"$ref":"#/components/schemas/WebhookEventType"}},"filters":{"type":"object","nullable":true,"description":"13.3.22. Tenant, venue, or a business condition on the payload.","additionalProperties":true},"signingSecret":{"type":"string","format":"password","writeOnly":true,"description":"**How the receiver knows it was TICVAI.** Without a signature an endpoint accepts a ticket-sale event from anybody who learns the URL.\n**Write-only: accepted on create, never returned.** The same rule as `clientSecret` — a system that can show you a secret later is a system that hands it to whoever reads the subscription.\n"},"status":{"type":"string","enum":["pendingVerification","active","paused","failing","disabled"],"readOnly":true},"consecutiveFailures":{"type":"integer","readOnly":true},"disabledReason":{"type":"string","nullable":true,"readOnly":true,"description":"13.1.29. **An endpoint failing for days is disabled rather than retried forever**, and the developer is told — a queue growing against a dead endpoint is a cost the platform carries silently.\n"}}}
}
```
