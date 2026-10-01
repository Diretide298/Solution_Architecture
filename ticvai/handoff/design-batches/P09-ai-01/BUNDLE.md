# P09-ai-01 — P09 · AI

**1 screens · 13 operations · 11 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `AI_APPROVE, AI_CONFIGURE, AI_USE, PLATFORM_AI_MANAGE, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_MANAGE, SCOPE_VIEW`. A control nobody can use must say so,
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
| `ADM-037` | AI Provider & Credentials | A | 28 | 69 | 7 | 13 | 4 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-037` AI Provider & Credentials

**Configure which model a tenant uses, within what its region allows, hold the key, and prove it works before anyone relies on it.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | AI · wave 1 · needs the `ai` module |
| Block | Block A · ticket #18094 (APP-SETUP-ADM-037) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE`, `PLATFORM_AI_MANAGE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_MANAGE`… (3 operate, 3 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAiProviders` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `providerId` (deepLink), `regionId` (navigation), `modelId` (navigation), `templateKey` (navigation), `tenantId` (session) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/ai/providers` |

**What the spec says about it.** Added 17 August. **The key is entered once and never returned** — the screen shows a reference, a rotation date and a last-verified date, never a secret. Test before activate. **Not on the wireframe board.** **Per tenant, not per region (decided 28 September, audit R203).** Platform staff pick a tenant, open a platform-staff grant into it (audit R098), and set that tenant's provider with `setAiProvider` (`PLATFORM_TENANT_MANAGE`, read from the operator's own token; the open grant ties the change to the tenant's audit); the region only restricts the choice. The screen shows the tenant's region's residency restriction before the form, and a provider whose `residency` is outside it is refused `409 residency-refused`, which the form shows against the residency field.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | select field | — | — | — | — | The provider is set per tenant (decided 28 September, audit R203); the list below is the picked tenant's providers. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Layer | segmented control | — | Platform · Tenant | `listAiModels` ?layer |
| Producer type | radio group | — | Llm · Embedding · Reranker · Classical · Rule | `listAiModels` ?producerType |
| Task | text field | — | — | `listPromptTemplates` ?task |
| Layer | segmented control | — | Platform · Tenant | `listPromptTemplates` ?layer |
| Status | segmented control | — | Draft · Published · Retired | `listPromptTemplates` ?status |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client UUIDv7), `permissions` (tenant permissions only; `AI_CONFIGURE` and `SCOPE_VIEW` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Save AI provider** (modal, opened by *Save AI provider*; *Save AI provider* calls `setAiProvider`, *Cancel* sends nothing)

**Collects what `setAiProvider` sends before it is called.** Required: `kind`, `capability`, `priority`, `isActive`. Optional: `id`, `model`, `failoverProviderId`, `degradeGracefully`, `scopeLevel`, `scopePath`, `credentialRef`, `credentialRotatedAt`, `credentialExpiresAt`, `lastVerifiedAt`, `endpoint`, `residency` and 1 more. **Set for the picked tenant**; a `residency` outside what the tenant's region allows is refused `409 residency-refused` and shown against that field (decided 28 September, audit R203). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | Assigned on create. Sent to `setAiProvider` to replace that provider; left out to create one. | `setAiProvider` body |
| Kind `kind` | select | required | — | Openai · Gemini · Anthropic · Azure openai · Local llm · Openai compatible | — | `openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). | `setAiProvider` body |
| Capability `capability` | select | required | — | Chat · Embedding · Vision · Rerank · Speech to text · Text to speech | — | What a capability needs, not which provider serves it. This indirection is what makes "no provider SDK in capability code" enforceable. | `setAiProvider` body |
| Model `model` | text field | optional | — | — | — | — | `setAiProvider` body |
| Failover provider `failoverProviderId` | picker: choose a failover provider | optional | — | — | shows names, sends the id | BL-151. A provider outage with no fallback is every AI surface going dark at once, and the surfaces most likely to be noticed are the guest-facing ones. | `setAiProvider` body |
| Degrade gracefully `degradeGracefully` | toggle | optional | on | — | — | Where no fallback answers, the surface degrades rather than errors. Semantic search falls back to keyword, the concierge offers a human, a recommendation returns the rule-based … | `setAiProvider` body |
| Priority `priority` | number field | required | — | — | — | Failover order (8.4.26). Lower is tried first. | `setAiProvider` body |
| Scope level `scopeLevel` | segmented control | optional | — | Platform · Tenant · Venue | — | Where this provider configuration applies, and therefore whose token pays for it. | `setAiProvider` body |
| Scope path `scopePath` | text field | optional | — | — | — | Resolved scope node. Nearest ancestor wins (ADR-0018). | `setAiProvider` body |
| Tenant `tenantId` | picker: choose a tenant | optional | — | Null only where `scopeLevel` is `platform`. | shows names, sends the id | Null only where `scopeLevel` is `platform`. | `setAiProvider` body |
| Credential ref `credentialRef` | text field | optional | — | — | — | A key-vault reference, never the key. A key typed into a form ends up in a screenshot. | `setAiProvider` body |
| Credential expires at `credentialExpiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Where the provider issues expiring keys. A key that lapses silently takes the assistant down without an error anyone reads — the expiry is surfaced so it can be chased before it … | `setAiProvider` body |
| Endpoint `endpoint` | text field | optional | — | — | — | — | `setAiProvider` body |
| Residency `residency` | text field | optional | — | — | — | Where inference physically happens. A prompt reaching a provider hosted elsewhere is a cross-border transfer (ADR-0009), and this field is what makes that auditable rather than … | `setAiProvider` body |
| Max tokens `maxTokens` | number field | optional | — | — | — | — | `setAiProvider` body |
| Is active `isActive` | toggle | required | — | — | — | — | `setAiProvider` body |
| Managed by `managedBy` | segmented control | optional | Ticvai | Ticvai · Tenant; `tenant`: bring-your-own-key, accepted only where TICVAI enabled it for the tenant (`setAiByokEnablement`); the tenant pays the provider and TICVAI meters for visibility. | — | Who holds the provider account, and so who pays (AI design 5.9, decided 29 September). | `setAiProvider` body |
| Model `modelId` | picker: choose a model | optional | — | — | shows names, sends the id | The model in the catalogue (`listAiModels`) this provider serves. Null for an older row that names its model only in `model`. | `setAiProvider` body |
| Task keys `taskKeys` | list of values (chips) | optional | — | AI-D02 stands: one managed provider (Azure OpenAI in UAE North) serves every task by default, with a small and a stronger model per task; a second provider or a tenant's own key is added only where … | — | Which agent tasks this provider serves (21 September minutes, M21-03: different agents may use different models chosen for the task). | `setAiProvider` body |

Errors to draw in the form: 403 The caller lacks `PLATFORM_TENANT_MANAGE` on their platform token, or has no platform-staff grant into this tenant open (`platform-grant-required`, audit R203).; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The provider's `residency` is not in the tenant's region's `allowedAiResidencies` (`residency-refused`, audit R203), or it is tenant-managed (`managedBy` is …

**Form: Save AI credential** (modal, opened by *Save AI credential*; *Save AI credential* calls `setAiCredential`, *Cancel* sends nothing)

**Collects what `setAiCredential` sends before it is called.** Required: `secret`. Optional: `expiresAt`, `graceMinutes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Secret `secret` | text field | required | — | — | — | Write-only, never returned, never logged, never in an `ai.interaction`. Masked in any audit record of this call. | `setAiCredential` body |
| Expires at `expiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setAiCredential` body |
| Grace minutes `graceMinutes` | number field (minutes) | optional | 1440 | min 0; max 1440 | — | How long the previous key stays valid, so in-flight requests survive. 24 hours by default (decided 28 September, audit R096); 0 revokes it at once. | `setAiCredential` body |

Errors to draw in the form: 409 The provider is TICVAI-managed; its key is provisioned by the platform (`provider-managed-by-ticvai`).

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (detail panel, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (decided 28 September, audit R098, R203). `setAiProvider` is checked against the operator's own `PLATFORM_TENANT_MANAGE`, and in addition needs a grant into the tenant open, so the change is audited against it; reading the providers and the region needs the grant to carry `AI_CONFIGURE` and `SCOPE_VIEW`. Found after a reload with …

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Region residency restriction** (banner, from `getRegionSettings`): Names the residencies the picked tenant's home region allows for AI processing (`RegionSettings.allowedAiResidencies`; empty means no restriction), and says that `setAiProvider` refuses any other residency with 409 `residency-refused` (decided 28 September, audit R203). The region is `Tenant.regionId`, read with `getRegionSettings`; a tenant with no region yet shows the 409 rule only.

| Shows | Format | Notes |
|---|---|---|
| Country code | text | ISO 3166-1 alpha-2. Determines the jurisdiction, and therefore the cell. |
| Currency code | text | — |
| Currency scale | 1,234 | Decimal places for this region's currency. Varies by currency — some use 2, some use 3. |
| Time zone | text | IANA zone, e.g. `Asia/Dubai`. |
| Date format | text | — |
| Number format | text | — |
| Fiscal year start month | 1,234 | Varies by country. |
| Allowed AI residencies | list or chips (count when long) | The region's compliance gate on AI providers (decided 28 September, audit R203; ADR-0009). |
| Placement | grouped details | Read-only here. Set by the Control Plane at provisioning. |
| Mode | chip: Shared, Dedicated, Isolated, Client hosted | — |
| Cell name | text | — |
| Cloud region | text | — |
| Cell name | text | The cell serving this region. One cell per tenant per region (ADR-0014). |

**Every AI provider** (data table, from `listAiProviders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Assigned on create. Sent to `setAiProvider` to replace that provider; left out to create one. |
| Kind | chip: Openai, Gemini, Anthropic, Azure openai, Local llm, Openai compatible | `openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development … |
| Capability | chip: Chat, Embedding, Vision, Rerank, Speech to text, Text to speech | What a capability needs, not which provider serves it. This indirection is what makes "no provider SDK in capability code" enforceable. |
| Model | text | — |
| Failover provider | the name it points at, never the id | BL-151. A provider outage with no fallback is every AI surface going dark at once, and the surfaces most likely to be noticed are the … |
| Degrade gracefully | yes / no (icon or chip) | Where no fallback answers, the surface degrades rather than errors. Semantic search falls back to keyword, the concierge offers a human, a … |
| Priority | 1,234 | Failover order (8.4.26). Lower is tried first. |
| Scope level | chip: Platform, Tenant, Venue | Where this provider configuration applies, and therefore whose token pays for it. |
| Scope path | text | Resolved scope node. Nearest ancestor wins (ADR-0018). |
| Credential ref | text | A key-vault reference, never the key. A key typed into a form ends up in a screenshot. |
| Credential rotated at | 1 Oct 2026, 14:30 | — |
| Credential expires at | 1 Oct 2026, 14:30 | Where the provider issues expiring keys. A key that lapses silently takes the assistant down without an error anyone reads — the expiry is … |

**The selected AI provider** (detail panel, from `listAiProviders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Assigned on create. Sent to `setAiProvider` to replace that provider; left out to create one. |
| Kind | chip: Openai, Gemini, Anthropic, Azure openai, Local llm, Openai compatible | `openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development … |
| Capability | chip: Chat, Embedding, Vision, Rerank, Speech to text, Text to speech | What a capability needs, not which provider serves it. This indirection is what makes "no provider SDK in capability code" enforceable. |
| Model | text | — |
| Failover provider | the name it points at, never the id | BL-151. A provider outage with no fallback is every AI surface going dark at once, and the surfaces most likely to be noticed are the … |
| Degrade gracefully | yes / no (icon or chip) | Where no fallback answers, the surface degrades rather than errors. Semantic search falls back to keyword, the concierge offers a human, a … |
| Priority | 1,234 | Failover order (8.4.26). Lower is tried first. |
| Scope level | chip: Platform, Tenant, Venue | Where this provider configuration applies, and therefore whose token pays for it. |
| Scope path | text | Resolved scope node. Nearest ancestor wins (ADR-0018). |
| Credential ref | text | A key-vault reference, never the key. A key typed into a form ends up in a screenshot. |
| Credential rotated at | 1 Oct 2026, 14:30 | — |
| Credential expires at | 1 Oct 2026, 14:30 | Where the provider issues expiring keys. A key that lapses silently takes the assistant down without an error anyone reads — the expiry is … |
| Last verified at | 1 Oct 2026, 14:30 | When `testAiProvider` last confirmed the key works. |
| Endpoint | text | — |
| Residency | text | Where inference physically happens. A prompt reaching a provider hosted elsewhere is a cross-border transfer (ADR-0009), and this field is … |
| Max tokens | 1,234 | — |

**Tasks and model fit** (detail panel, from `listAiProviders`): **One managed provider by default (AI-D02)**, with a small and a stronger model per agent task; a second provider or a tenant key only where TICVAI enabled it (AI-D14). `taskKeys` binds a provider to named agent tasks (M21-03). **Fitness warnings are shown, never blocking** (M21-09): a model below a task's floor is underpowered, one far above its ceiling is overpowered.

| Shows | Format | Notes |
|---|---|---|
| Task keys | list or chips (count when long) | Which agent tasks this provider serves (21 September minutes, M21-03: different agents may use different models chosen for the task). |
| Fitness warnings | list or chips (count when long) | The model-fitness check at the last write (21 September minutes, M21-09). For each task in `taskKeys` whose model scores outside the task's … |
| Managed by | chip: Ticvai, Tenant | Who holds the provider account, and so who pays (AI design 5.9, decided 29 September). |
| Model | the name it points at, never the id | The model in the catalogue (`listAiModels`) this provider serves. Null for an older row that names its model only in `model`. |

**Model fit warning** (banner, from `setAiProvider`): Shown after `setAiProvider` returns `fitnessWarnings`: names the task, the score and the band.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Assigned on create. Sent to `setAiProvider` to replace that provider; left out to create one. |
| Kind | chip: Openai, Gemini, Anthropic, Azure openai, Local llm, Openai compatible | `openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development … |
| Capability | chip: Chat, Embedding, Vision, Rerank, Speech to text, Text to speech | What a capability needs, not which provider serves it. This indirection is what makes "no provider SDK in capability code" enforceable. |
| Model | text | — |
| Failover provider | the name it points at, never the id | BL-151. A provider outage with no fallback is every AI surface going dark at once, and the surfaces most likely to be noticed are the … |
| Degrade gracefully | yes / no (icon or chip) | Where no fallback answers, the surface degrades rather than errors. Semantic search falls back to keyword, the concierge offers a human, a … |
| Priority | 1,234 | Failover order (8.4.26). Lower is tried first. |
| Scope level | chip: Platform, Tenant, Venue | Where this provider configuration applies, and therefore whose token pays for it. |
| Credential ref | text | A key-vault reference, never the key. A key typed into a form ends up in a screenshot. |
| Credential rotated at | 1 Oct 2026, 14:30 | — |
| Credential expires at | 1 Oct 2026, 14:30 | Where the provider issues expiring keys. A key that lapses silently takes the assistant down without an error anyone reads — the expiry is … |
| Last verified at | 1 Oct 2026, 14:30 | When `testAiProvider` last confirmed the key works. |
| Endpoint | text | — |
| Residency | text | Where inference physically happens. A prompt reaching a provider hosted elsewhere is a cross-border transfer (ADR-0009), and this field is … |
| Max tokens | 1,234 | — |
| Is active | yes / no (icon or chip) | — |
| Managed by | chip: Ticvai, Tenant | Who holds the provider account, and so who pays (AI design 5.9, decided 29 September). |
| Model | the name it points at, never the id | The model in the catalogue (`listAiModels`) this provider serves. Null for an older row that names its model only in `model`. |
| Task keys | list or chips (count when long) | Which agent tasks this provider serves (21 September minutes, M21-03: different agents may use different models chosen for the task). |
| Fitness warnings | list or chips (count when long) | The model-fitness check at the last write (21 September minutes, M21-09). For each task in `taskKeys` whose model scores outside the task's … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Save AI provider (primary button) | `setAiProvider` PUT `/providers` | AiProvider | AiProvider | 403 The caller lacks `PLATFORM_TENANT_MANAGE` on their platform token, or has no platform-staff grant into this tenant open (`platform-grant-required`, audit R203).; 404 The resource does not exist, or is outside the … | opens modal first |
| Save AI credential (secondary button) | `setAiCredential` PUT `/ai-providers/{providerId}/credential` | inline | AiProvider | 409 The provider is TICVAI-managed; its key is provisioned by the platform (`provider-managed-by-ticvai`). | opens modal first |
| Test AI provider (secondary button) | `testAiProvider` POST `/ai-providers/{providerId}/test` | — | inline | — | — |

**Data it reads**: `listAiProviders` (onLoad, Configured providers and their order); `listTenants` (onLoad, The tenant picker — the provider is a per-tenant setting …); `listAiModels` (onLoad, The model catalogue); `listPromptTemplates` (onLoad, The prompt registry); `getAiByokEnablement` (onLoad, Whether a tenant may bring its own key)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `BO-091` AI Policy & Spend: *AI Policy & Spend*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The provider credentials list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the provider credentials untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No provider credentials yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listAiProviders` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_CONFIGURE`, which `listAiProviders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so the provider list and every action are disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098, R203). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The provider is TICVAI-managed; its key is provisioned by the platform (`provider-managed-by-ticvai`).; 409 The provider's `residency` is not in the tenant's region's `allowedAiResidencies` (`residency-refused`, audit R203), or it is tenant-managed (`managedBy` is … |

#### Permissions

- `listAiProviders` → `AI_CONFIGURE` (configure) · staff
- `getRegionSettings` → `SCOPE_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `setAiProvider` → `PLATFORM_TENANT_MANAGE` (configure) · staff
- `setAiCredential` → `AI_CONFIGURE` (configure) · staff
- `testAiProvider` → `AI_CONFIGURE` (configure) · staff
- `listAiModels` → `AI_USE` (operate) · staff
- `setAiModel` → `PLATFORM_AI_MANAGE` (configure) · staff
- `listPromptTemplates` → `AI_USE` (operate) · staff
- `publishPromptTemplate` → `AI_APPROVE` (operate) · staff
- `setAiByokEnablement` → `PLATFORM_AI_MANAGE` (configure) · staff
- `getAiByokEnablement` → `AI_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `AI_CONFIGURE`, which `listAiProviders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

13 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.4.21 | System shall support OpenAI integration. | Unified Operations Dashboard | CONTRACTED | `setAiProvider` |
| 8.4.22 | System shall support Gemini integration. | Unified Operations Dashboard | CONTRACTED | `setAiProvider` |
| 8.4.23 | System shall support Claude integration. | Unified Operations Dashboard | CONTRACTED | `setAiProvider` |
| 8.4.24 | System shall support local LLM deployment. | Unified Operations Dashboard | CONTRACTED | `setAiProvider` |
| 8.4.25 | System shall support multiple AI providers simultaneously. | Unified Operations Dashboard | CONTRACTED | `setAiProvider` |
| 8.4.14 | System shall support AI-powered report generation. | Unified Operations Dashboard | CONTRACTED | data `AiProvider` |
| 8.4.15 | System shall support AI-powered dashboard generation. | Unified Operations Dashboard | CONTRACTED | data `AiProvider` |
| 8.4.16 | System shall support AI-powered data summarization. | Unified Operations Dashboard | CONTRACTED | data `AiProvider` |
| 8.4.26 | System shall support AI provider failover. | Unified Operations Dashboard | CONTRACTED | data `AiProvider` |
| 8.7.28 | System shall support data drill-down. | Unified Operations Dashboard | CONTRACTED | data `AiProvider` |
| 8.7.29 | System shall support embedded analytics. | Unified Operations Dashboard | CONTRACTED | data `AiProvider` |
| 8.7.31 | System shall support AI-generated dashboards. | Unified Operations Dashboard | CONTRACTED | data `AiProvider` |
| … 1 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The AI provider screen binds a provider to named agent tasks; model fitness warnings (underpowered / overpowered for a task) are shown, never blocking. *(agreed · MoM 21 Sep 2026, M21-03, M21-09 · DI-971)*
- AI operations monitoring shows health, cost/budget tracking and which AI agents consume the most resources and for what purpose, so the business can manage AI spend. *(client request · MoM 21 Sep 2026, 4.11 Core AI Platform — Operations & Consumption Monitoring · DI-968)*
- **Open question.** Proposed (Chinmay), not finalised: each pre-configured agent carries a complexity/fitness score; when a client switches models, an assessment flags whether the new model is under- or over-powered for that agent and recommends an adjustment. Exact end-user control over model switching is still open. *(open · MoM 21 Sep 2026, 4.10 Core AI Platform — Multi-Provider AI Model Strategy · DI-967)*
- Model selection per agent is system-managed by default (end users do not choose a model per task); a client may override the pre-selected model for an agent with its own API key, every change logged for audit. A client-hosted/private model plugs in the same way: API key plus endpoint address. *(agreed · MoM 21 Sep 2026, 4.10 Core AI Platform — Multi-Provider AI Model Strategy · DI-966)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-037` · status **notStarted** · provenance generated
- Flow F100 *An AI provider is configured, budgeted and audited*, step 1: AI Provider & Credentials. → 4 operations, 4 of them previously unwalked.
- Flow F100 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.
- ADR-0009 *AI Data Residency* (`docs/adr/0009-ai-data-residency.md`)
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (28), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (69 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-037?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: , Open access grant, Save AI provider, Save AI credential, Test AI provider.
- [ ] Every transition is wired: `ADM-001`, `BO-091`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE`, `PLATFORM_AI_MANAGE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_MANAGE`, `SCOPE_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getAiByokEnablement": {"method":"GET","path":"/tenants/{tenantId}/byok","contract":"ai","summary":"Whether a tenant may bring its own key","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AiByokEnablement"},
"getRegionSettings": {"method":"GET","path":"/regions/{regionId}/settings","contract":"tenancy","summary":"Read region settings","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"RegionSettings"},
"listAiModels": {"method":"GET","path":"/models","contract":"ai","summary":"The model catalogue","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"layer","in":"query","required":null},{"name":"producerType","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiProviders": {"method":"GET","path":"/providers","contract":"ai","summary":"Configured providers and their order","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AiProvider"},
"listOwnPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants/mine","contract":"identity","summary":"The calling platform operator's own grants into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPromptTemplates": {"method":"GET","path":"/prompt-templates","contract":"ai","summary":"The prompt registry","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"task","in":"query","required":null},{"name":"layer","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"publishPromptTemplate": {"method":"POST","path":"/prompt-templates/{templateKey}/versions","contract":"ai","summary":"Publish a prompt template version","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiPromptTemplate"},
"setAiByokEnablement": {"method":"PUT","path":"/tenants/{tenantId}/byok","contract":"ai","summary":"Enable or disable bring-your-own-key for a tenant (platform)","permission":"PLATFORM_AI_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiByokEnablement","responds":"AiByokEnablement"},
"setAiCredential": {"method":"PUT","path":"/ai-providers/{providerId}/credential","contract":"ai","summary":"Store or rotate a provider key","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiProvider"},
"setAiModel": {"method":"PUT","path":"/models/{modelId}","contract":"ai","summary":"Add or change a platform model (platform)","permission":"PLATFORM_AI_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiModel","responds":"AiModel"},
"setAiProvider": {"method":"PUT","path":"/providers","contract":"ai","summary":"Configure a provider","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiProvider","responds":"AiProvider"},
"testAiProvider": {"method":"POST","path":"/ai-providers/{providerId}/test","contract":"ai","summary":"Check the key works before anyone relies on it","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiByokEnablement": {"type":"object","x-ticvai-persistence":"ai.byok_enablement","description":"**Whether a tenant may bring its own model key** (decided 29 September, design 8 on 5.9). TICVAI decides it per tenant with `PLATFORM_AI_MANAGE`; it is not tenant self-service. Until it is enabled, `setAiProvider` refuses `managedBy: tenant`. One row per tenant.","required":["tenantId","enabled"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"tenantId":{"type":"string","format":"uuid"},"enabled":{"type":"boolean"},"coverage":{"type":"string","enum":["perTask","allTasks"],"default":"perTask","description":"Whether the tenant may supply a key per task or one key for everything."},"allowedTasks":{"type":"array","items":{"type":"string"},"description":"Where `coverage` is `perTask`: the gateway tasks a tenant key may serve. Empty means any."},"reason":{"type":"string","maxLength":1000},"platformStaffGrantId":{"type":"string","format":"uuid","readOnly":true,"description":"The open platform-staff grant the change was made under (audit R098)."},"decidedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"decidedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiCapability": {"type":"string","description":"What a capability needs, not which provider serves it. This indirection is what makes \"no provider SDK in capability code\" enforceable.\n**`speechToText` and `textToSpeech` added 18 August (BL-164)** — voice added rather than declined. **Speech is the capability where UAE residency is hardest to satisfy**: the major providers run it in fewer regions than text, and a guest speaking into a kiosk is producing personal data in the moment. `AiProvider.residency` already carries the constraint and **speech is the capability most likely to fail it**, which is why it is separate rather than folded into `chat`.\n","enum":["chat","embedding","vision","rerank","speechToText","textToSpeech"]},
"AiModel": {"type":"object","x-ticvai-persistence":"ai.model","description":"**The model catalogue** (design 3.1 Registry, 3.3; AIC-013, AIC-026). One row per model a task can be routed to: large language models, embedding and reranking models, and classical models (LightGBM, statistical forecasters) registered the same way so lifecycle, release and audit are uniform. **Platform rows** are mastered in the control plane and replicated read-only into each tenant database with the tenant root as `scopePath`; a tenant row exists only where bring-your-own-key is enabled for the tenant.","required":["layer","modelName","producerType"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"layer":{"type":"string","enum":["platform","tenant"]},"providerKind":{"allOf":[{"$ref":"#/components/schemas/AiProviderKind"}],"nullable":true},"producerType":{"type":"string","enum":["llm","embedding","reranker","classical","rule"]},"modelName":{"type":"string","description":"The deployment or model name as the provider knows it, or the package and version for a classical model."},"capabilities":{"type":"array","items":{"$ref":"#/components/schemas/AiCapability"}},"contextTokens":{"type":"integer","nullable":true},"toolCalling":{"type":"boolean","default":false},"structuredOutput":{"type":"boolean","default":false},"languages":{"type":"array","items":{"type":"string"}},"residency":{"type":"string","nullable":true,"description":"Where inference happens. Checked against `tenancy.RegionSettings.allowedAiResidencies`."},"inputCostPerMillionTokens":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"outputCostPerMillionTokens":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"lifecycle":{"type":"object","description":"Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.","properties":{"development":{"type":"string","enum":["draft","pilot","active","retired"]},"staging":{"type":"string","enum":["draft","pilot","active","retired"]},"production":{"type":"string","enum":["draft","pilot","active","retired"]}}},"isDefaultForTasks":{"type":"array","items":{"type":"string"},"description":"Tasks this model is the default for (AIC-010), e.g. `assistant.guest.answer`, `config.extract`."},"taskFitness":{"type":"array","readOnly":true,"description":"**Evaluated fitness per task** (21 September minutes, M21-09, our proposal): a score from the task's golden set (`runAiEvaluation`) and the band the task needs. Below `floor` the model is underpowered for the task; far above `ceiling` it is overpowered (it costs more than the task needs). `setAiProvider` returns a warning (`AiProvider.fitnessWarnings`) when a choice falls outside the band, and ADM-037 shows the band beside `setAiModel`; neither refuses on it.","items":{"type":"object","required":["taskKey","score"],"properties":{"taskKey":{"type":"string"},"score":{"type":"number","minimum":0,"maximum":1},"floor":{"type":"number","minimum":0,"maximum":1},"ceiling":{"type":"number","minimum":0,"maximum":1,"nullable":true},"evaluationRunId":{"type":"string","format":"uuid","nullable":true},"evaluatedAt":{"type":"string","format":"date-time"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiPromptTemplate": {"type":"object","x-ticvai-persistence":"ai.prompt_template","description":"**The prompt registry** (design 3.1 Registry, AIC-022). Versioned and **immutable once published**: a change is a new version, so every decision record can name the exact template it used. Platform templates are replicated read-only like platform models; a tenant may publish its own variant of a task's template.","required":["templateKey","version","layer","task","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"templateKey":{"type":"string"},"version":{"type":"integer","minimum":1},"layer":{"type":"string","enum":["platform","tenant"]},"task":{"type":"string","description":"The gateway task it serves (design 3.3), e.g. `assistant.guest.answer`, `case.summarise`, `guidedChoice.wording`."},"body":{"type":"string","description":"The template text. Stable content first, so the provider's prefix cache applies (ADR-0034)."},"variables":{"type":"array","items":{"type":"string"}},"outputSchema":{"type":"object","additionalProperties":true,"nullable":true,"description":"JSON Schema the structured output must satisfy, where the task has one."},"status":{"type":"string","enum":["draft","published","retired"]},"contentHash":{"type":"string","readOnly":true},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiProvider": {"type":"object","x-ticvai-persistence":"ai.provider","required":["kind","capability","priority","isActive"],"properties":{"id":{"type":"string","format":"uuid","description":"Assigned on create. Sent to `setAiProvider` to replace that provider; left out to create one."},"kind":{"$ref":"#/components/schemas/AiProviderKind"},"capability":{"$ref":"#/components/schemas/AiCapability"},"model":{"type":"string"},"failoverProviderId":{"type":"string","format":"uuid","nullable":true,"description":"BL-151. **A provider outage with no fallback is every AI surface going dark at once**, and the surfaces most likely to be noticed are the guest-facing ones.\n**Failover is declared per capability because a provider is** — a fallback covering chat and not embedding leaves search broken while the concierge works, which reads as a stranger failure than a clean outage.\n"},"degradeGracefully":{"type":"boolean","default":true,"description":"**Where no fallback answers, the surface degrades rather than errors.** Semantic search falls back to keyword, the concierge offers a human, a recommendation returns the rule-based set — **an AI feature that returns a 500 is worse than one that quietly becomes ordinary software.**\n"},"priority":{"type":"integer","description":"Failover order (8.4.26). Lower is tried first."},"scopeLevel":{"type":"string","enum":["platform","tenant","venue"],"description":"**Where this provider configuration applies, and therefore whose token pays for it.** A tenant-scoped provider means that tenant's usage bills against their own key at the provider — **an independent reconciliation source against our own meter**, which is the point of per-tenant tokens rather than one platform key.\n`venue` exists for the case where one venue's volume justifies its own key, or where a venue is billed separately from the rest of its tenant.\n**`tenant` is the decided level** (audit R203, ADR-0009): a tenant's provider is set per tenant, by platform staff on ADM-037. `venue` narrows inside a tenant; `platform` is only the platform's fallback. **No provider is configured per region**: a region restricts the choice through `tenancy.RegionSettings.allowedAiResidencies` and nothing else, and the table's `region_id` is the tenant's home region, recorded so that gate can be re-checked.\n"},"scopePath":{"type":"string","description":"Resolved scope node. Nearest ancestor wins (ADR-0018)."},"tenantId":{"type":"string","format":"uuid","nullable":true,"description":"Null only where `scopeLevel` is `platform`."},"credentialRef":{"type":"string","description":"A key-vault reference, never the key. A key typed into a form ends up in a screenshot.\n"},"credentialRotatedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"credentialExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"Where the provider issues expiring keys. **A key that lapses silently takes the assistant down without an error anyone reads** — the expiry is surfaced so it can be chased before it bites.\n"},"lastVerifiedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When `testAiProvider` last confirmed the key works."},"endpoint":{"type":"string","nullable":true},"residency":{"type":"string","description":"Where inference physically happens. **A prompt reaching a provider hosted elsewhere is a cross-border transfer** (ADR-0009), and this field is what makes that auditable rather than assumed.\n"},"maxTokens":{"type":"integer"},"isActive":{"type":"boolean"},"managedBy":{"type":"string","enum":["ticvai","tenant"],"default":"ticvai","description":"**Who holds the provider account, and so who pays** (AI design 5.9, decided 29 September). `ticvai`: TICVAI-managed, metered per tenant and re-billed per token. `tenant`: bring-your-own-key, accepted only where TICVAI enabled it for the tenant (`setAiByokEnablement`); the tenant pays the provider and TICVAI meters for visibility.\n"},"modelId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.model","description":"The model in the catalogue (`listAiModels`) this provider serves. Null for an older row that names its model only in `model`."},"taskKeys":{"type":"array","items":{"type":"string"},"description":"**Which agent tasks this provider serves** (21 September minutes, M21-03: different agents may use different models chosen for the task). Empty means every task of its `capability`. A task listed on two providers goes to the lower `priority`. **AI-D02 stands:** one managed provider (Azure OpenAI in UAE North) serves every task by default, with a small and a stronger model per task; a second provider or a tenant's own key is added only where TICVAI enables it for the tenant (AI-D14, `setAiByokEnablement`)."},"fitnessWarnings":{"type":"array","readOnly":true,"description":"**The model-fitness check at the last write** (21 September minutes, M21-09). For each task in `taskKeys` whose model scores outside the task's band in `AiModel.taskFitness`, or has no score, one warning. A warning never blocks the write; it is shown on ADM-037 and kept so the choice is auditable.","items":{"type":"object","properties":{"taskKey":{"type":"string"},"score":{"type":"number","nullable":true},"floor":{"type":"number"},"direction":{"type":"string","enum":["underpowered","overpowered","unscored"]}}}}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE"]},
"Placement": {"x-ticvai-persistence":"none — embedded in region_settings","type":"object","description":"Read-only here. Set by the Control Plane at provisioning.\nEvery region is its own logical cell. Placement determines the infrastructure backing it, which is how cost is controlled without varying the split rule: `shared` puts several regions' databases on one cluster; `dedicated` and `isolated` give a region its own. Regions in different countries MUST have placements in their respective jurisdictions.\n","readOnly":true,"required":["mode"],"properties":{"mode":{"type":"string","enum":["shared","dedicated","isolated","clientHosted"]},"cellName":{"type":"string"},"cloudRegion":{"type":"string"}}},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"RegionSettings": {"x-ticvai-persistence":"platform.region_settings","type":"object","required":["countryCode","currencyCode","currencyScale","timeZone","fiscalYearStartMonth"],"properties":{"countryCode":{"type":"string","pattern":"^[A-Z]{2}$","description":"ISO 3166-1 alpha-2. Determines the jurisdiction, and therefore the cell."},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"description":"Decimal places for this region's currency. Varies by currency — some use 2, some use 3. Money columns are numeric(18,4) and carry the scale explicitly, because a fixed 2-place type silently truncates 3-place currencies.\n"},"timeZone":{"type":"string","description":"IANA zone, e.g. `Asia/Dubai`."},"dateFormat":{"type":"string","default":"dd/MM/yyyy"},"numberFormat":{"type":"string","default":"#,##0.00"},"fiscalYearStartMonth":{"type":"integer","minimum":1,"maximum":12,"description":"Varies by country."},"allowedAiResidencies":{"type":"array","description":"**The region's compliance gate on AI providers** (decided 28 September, audit R203; ADR-0009). The `AiProvider.residency` values a tenant in this region may use; empty means no restriction. `ai.setAiProvider` refuses any other residency with `409 residency-refused`. A prompt carrying guest data that reaches a provider hosted elsewhere is a cross-border transfer, and this is where a region says which it allows.\n","default":[],"items":{"type":"string"}},"placement":{"$ref":"#/components/schemas/Placement"},"cellName":{"type":"string","readOnly":true,"description":"The cell serving this region. One cell per tenant per region (ADR-0014).\n"}}}
}
```
