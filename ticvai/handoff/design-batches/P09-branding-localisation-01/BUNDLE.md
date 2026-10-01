# P09-branding-localisation-01 — P09 · Branding & Localisation

**4 screens · 23 operations · 33 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `PLATFORM_TENANT_ACCESS, TENANT_CONFIGURE, TENANT_PUBLISH, TENANT_VIEW`. A control nobody can use must say so,
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
| `ADM-016` | White-Label Branding Management | A | 54 | 46 | 7 | 12 | 0 | 6 | configures | notStarted (generated) |
| `ADM-017` | Domain & Certificate Management | A | 9 | 25 | 7 | 1 | 1 | 0 | configures | notStarted (generated) |
| `ADM-018` | Localisation & Language Pack | A | 21 | 25 | 7 | 10 | 2 | 0 | configures | notStarted (generated) |
| `ADM-019` | Global Configuration & Defaults | B–D | 78 | 43 | 7 | 20 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-016` White-Label Branding Management

**See white-label branding management for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Branding & Localisation · wave 2 · needs the `core` module |
| Block | Block A · ticket #18118 (APP-WL-ADM-016) |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_ACCESS`, `TENANT_CONFIGURE`, `TENANT_PUBLISH` (1 operate, 2 configure); in the flows as platform admin, venue manager |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listConfigVersions` reads the population and `getAppIcons` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `bannerId` (deepLink), `pageId` (deepLink), `policyKind` (deepLink), `version` (deepLink) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/general/white-label-branding-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **30 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | select field | — | — | — | — | **Pick a tenant first** (decided 28 September, audit R098). This screen's operations run in that tenant's cell, and a platform token carries no tenant permission there until a platform-staff grant … | — |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client UUIDv7), `permissions` (tenant permissions only — the ones this screen's operations need, preselected), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Create preview** (modal, opened by *Create preview*; *Create preview* calls `createPreview`, *Cancel* sends nothing)

**Collects what `createPreview` sends before it is called.** Nothing in the body is required. Optional: `platform`, `theme`, `language`, `expiresInHours`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Platform `platform` | segmented control | optional | — | Ios · Android · Web | — | — | `createPreview` body |
| Theme `theme` | segmented control | optional | — | Light · Dark | — | — | `createPreview` body |
| Language `language` | language picker | optional | — | — | ISO 639-1 code, shown as the language name | — | `createPreview` body |
| Expires in hours `expiresInHours` | number field (hours) | optional | 24 | min 1; max 168 | — | — | `createPreview` body |

**Form: Publish tenant config** (modal, opened by *Publish tenant config*; *Publish tenant config* calls `publishTenantConfig`, *Cancel* sends nothing)

**Collects what `publishTenantConfig` sends before it is called.** Required: `note`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | required | — | min length 3; max length 500 | — | — | `publishTenantConfig` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Publish at a future time. Useful for a campaign launch. | `publishTenantConfig` body |

Errors to draw in the form: 409 Validation failed. (ConfigValidationProblem)

**Form: Save app icons** (modal, opened by *Save app icons*; *Save app icons* calls `setAppIcons`, *Cancel* sends nothing)

**Collects what `setAppIcons` sends before it is called.** Required: `sourceAssetRef`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Source image `sourceAssetRef` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The `MediaAsset` id of the 1024×1024 source, from `assets` `createUpload` then `completeUpload`. | `setAppIcons` body |

Errors to draw in the form: 400 Source is not 1024×1024, or contains transparency

**Form: Save brand identity** (modal, opened by *Save brand identity*; *Save brand identity* calls `setBrandIdentity`, *Cancel* sends nothing)

**Collects what `setBrandIdentity` sends before it is called.** Required: `logoAssetRef`. Optional: `logoDarkAssetRef`, `faviconAssetRef`, `splashImageAssetRefs`, `splashDurationSeconds`, `splashBackgroundColour`, `showLoadingIndicator`, `splashChangeScope`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Logo `logoAssetRef` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The primary logo. | `setBrandIdentity` body |
| Logo dark image `logoDarkAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Used on dark backgrounds. Falls back to the primary logo. | `setBrandIdentity` body |
| Logo variant `logoVariant` | segmented control | optional | Light | Light · Dark · Duotone | — | Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4). | `setBrandIdentity` body |
| Favicon `faviconAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The browser tab icon for the guest web app. | `setBrandIdentity` body |
| Splash image `splashImageAssetRefs` | media picker (several) | optional | — | — | PNG, JPG, SVG or MP4 from the media library | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). | `setBrandIdentity` body |
| Splash duration seconds `splashDurationSeconds` | stepper or slider (seconds) | optional | 3 | min 0; max 10 | — | — | `setBrandIdentity` body |
| Splash background colour `splashBackgroundColour` | colour picker | optional | — | — | #RRGGBB | — | `setBrandIdentity` body |
| Show loading indicator `showLoadingIndicator` | toggle | optional | on | — | — | — | `setBrandIdentity` body |
| Intro video `introVideoAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). | `setBrandIdentity` body |
| Intro video mode `introVideoMode` | segmented control | optional | Off | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | — | When GST-001 plays it full screen. "Skip introduction" is always shown. | `setBrandIdentity` body |

Errors to draw in the form: 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270)

**Form: Save theme** (modal, opened by *Save theme*; *Save theme* calls `setTheme`, *Cancel* sends nothing)

**Collects what `setTheme` sends before it is called.** Required: `primaryColour`, `secondaryColour`, `backgroundColour`, `textColour`. Optional: `accentColour`, `darkMode`, `cornerRadius`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Primary colour `primaryColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Secondary colour `secondaryColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Accent colour `accentColour` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Background colour `backgroundColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Text colour `textColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Dark mode `darkMode` | group | optional | — | — | — | Optional dark variant. Derived from the light theme when absent. | `setTheme` body |
| Primary colour `darkMode.primaryColour` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Background colour `darkMode.backgroundColour` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text colour `darkMode.textColour` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Corner radius `cornerRadius` | stepper or slider | optional | — | min 0; max 32 | — | The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). | `setTheme` body |
| Surface style `surfaceStyle` | segmented control | optional | Glass | Glass · Solid | — | Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3). | `setTheme` body |
| Button style `buttonStyle` | segmented control | optional | Solid | Solid · Outline · Pill | — | Button shape (decided 29 September, rev 3 CFG-3). | `setTheme` body |
| Component colours `componentColours` | group | optional | — | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. | `setTheme` body |
| Primary CTA `componentColours.primaryCta` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.primaryCta.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.primaryCta.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Pay button `componentColours.payButton` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.payButton.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.payButton.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Add to cart `componentColours.addToCart` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.addToCart.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.addToCart.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Buy tickets button `componentColours.buyTicketsButton` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.buyTicketsButton.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.buyTicketsButton.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Link `componentColours.link` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.link.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.link.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Badge `componentColours.badge` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.badge.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.badge.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |

Errors to draw in the form: 400 A colour pair fails the contrast requirement. (ContrastProblem)

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (detail panel, from `openPlatformStaffGrant`): **Always visible while the screen acts on a tenant** (decided 28 September, audit R098): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Every config version** (data table, from `listConfigVersions`)

| Shows | Format | Notes |
|---|---|---|
| Published at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published by name | text | — |
| Note | text | — |
| Is current | yes / no (icon or chip) | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Content hash | text | — |
| Pending build time changes | list or chips (count when long) | Changes in this version that will not reach guests until the next store release. |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected config version** (detail panel, from `listConfigVersions`)

| Shows | Format | Notes |
|---|---|---|
| Published at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published by name | text | — |
| Note | text | — |
| Is current | yes / no (icon or chip) | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Content hash | text | — |
| Pending build time changes | list or chips (count when long) | Changes in this version that will not reach guests until the next store release. |
| Snapshot | grouped details | What this version contained. The working draft exactly as published, in the shape `getTenantConfig` returns (`TenantConfig`) — so … |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The brand identity** (detail panel, from `getBrandIdentity`)

| Shows | Format | Notes |
|---|---|---|
| Logo | the image or video | The primary logo. |
| Logo dark image | the image or video | Used on dark backgrounds. Falls back to the primary logo. |
| Favicon | the image or video | The browser tab icon for the guest web app. |
| Splash image | list or chips (count when long) | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish … |
| Splash duration seconds | 1,234 | — |
| Splash background colour | colour swatch | — |
| Show loading indicator | yes / no (icon or chip) | — |
| Splash change scope | chip: Runtime, Build time | Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163). |

**The theme** (detail panel, from `getTheme`)

| Shows | Format | Notes |
|---|---|---|
| Primary colour | colour swatch | — |
| Secondary colour | colour swatch | — |
| Accent colour | colour swatch | — |
| Background colour | colour swatch | — |
| Text colour | colour swatch | — |
| Dark mode | grouped details | Optional dark variant. Derived from the light theme when absent. |
| Corner radius | 1,234 | The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). |

**The app icons** (detail panel, from `getAppIcons`)

| Shows | Format | Notes |
|---|---|---|
| Source image | the image or video | The `MediaAsset` id of the 1024×1024 source. |
| Derived | list or chips (count when long) | Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on … |
| Change scope | chip: Runtime, Build time | Always `buildTime` — icons are baked into the binary. |
| Live version | text | Icon currently shipped. Differs from the draft until the next release. |
| Requires rebuild | yes / no (icon or chip) | True while the draft's source differs from the icon in `liveVersion`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (publish gate) | navigation or local | — | — | — | — |
| Create preview (primary button) | `createPreview` POST `/tenant-config/preview` | inline | Preview | — | opens modal first |
| Diff config version (secondary button) | `diffConfigVersion` GET `/tenant-config/versions/{version}/diff` | — | ConfigDiff | — | — |
| Publish tenant config (secondary button) | `publishTenantConfig` POST `/tenant-config/publish` | inline | ConfigVersion | 409 Validation failed. (ConfigValidationProblem) | opens modal first |
| Restore config version (secondary button) | `restoreConfigVersion` POST `/tenant-config/versions/{version}/restore` | — | TenantConfig | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Save app icons (secondary button) | `setAppIcons` PUT `/tenant-config/app-icons` | inline | AppIcons | 400 Source is not 1024×1024, or contains transparency | opens modal first |
| Save brand identity (secondary button) | `setBrandIdentity` PUT `/tenant-config/brand` | BrandIdentity | BrandIdentity | 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270) | opens modal first |
| Save theme (secondary button) | `setTheme` PUT `/tenant-config/theme` | Theme | Theme | 400 A colour pair fails the contrast requirement. (ContrastProblem) | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listTenants` (onLoad, The tenant picker — the operator picks a tenant before …); `getAppIcons` (onLoad, Read app icon set); `getBrandIdentity` (onLoad, Read brand identity); `getTheme` (onLoad, Read colour theme); `listConfigVersions` (onLoad, Version history)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The white-label branding list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the white-label branding untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No white-label branding yet. Offers Create preview (`createPreview`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listConfigVersions` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getAppIcons` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A colour pair fails the contrast requirement. (ContrastProblem); 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270); 400 Source is not 1024×1024, or contains transparency; 400 Validation failed |

#### Permissions

- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `createPreview` → `TENANT_CONFIGURE` (configure) · staff
- `diffConfigVersion` → `TENANT_CONFIGURE` (configure) · staff
- `getAppIcons` → `TENANT_CONFIGURE` (configure) · staff
- `getBrandIdentity` → `TENANT_CONFIGURE` (configure) · staff
- `getTheme` → `TENANT_CONFIGURE` (configure) · staff
- `listConfigVersions` → `TENANT_CONFIGURE` (configure) · staff
- `publishTenantConfig` → `TENANT_PUBLISH` (configure) · staff
- `restoreConfigVersion` → `TENANT_PUBLISH` (configure) · staff
- `setAppIcons` → `TENANT_CONFIGURE` (configure) · staff
- `setBrandIdentity` → `TENANT_CONFIGURE` (configure) · staff
- `setTheme` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getAppIcons` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.10.30 | CMS Audit Trail | Marketing & CRM | CONTRACTED | `listConfigVersions` |
| 19.1.24 | White Label Configuration Portal - System shall provide self-service white label configuration. | Guest Mobile App & Branding | CONTRACTED | `publishTenantConfig` |
| 22.10.10 | Version Management | Marketing & CRM | CONTRACTED | `restoreConfigVersion` |
| 22.10.11 | Rollback & Recovery | Marketing & CRM | CONTRACTED | `restoreConfigVersion` |
| 19.1.3 | App Icon Management - System shall support configurable app icons. | Guest Mobile App & Branding | CONTRACTED | `setAppIcons` |
| 19.1.1 | Logo Management - System shall allow changing the mobile app logo through configuration. | Guest Mobile App & Branding | CONTRACTED | `setBrandIdentity` |
| 19.1.2 | Splash Screen Management - System shall allow changing splash screens. | Guest Mobile App & Branding | CONTRACTED | `setBrandIdentity` |
| 19.1.4 | Color Theme Management - System shall support configurable color palettes. | Guest Mobile App & Branding | CONTRACTED | `setTheme` |
| 2.6.50 | System shall allow administrators to upload brand assets, logos, colors, fonts, content, images, and documents, and use AI to generate a white-label website layout including homepage, menus, headers … | Ticketing Sales | CONTRACTED | `setTheme` |
| 22.4.6 | Multi-Brand Support | Marketing & CRM | CONTRACTED | `setTheme` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |
| 2.6.4 | The system should offer white label e-commerce engine for B2C sales (internal CMS). The interface of e-commerce engine should have configurable theming: - Color scheme can be updated - Background … | Ticketing Sales | CONTRACTED | data `Theme` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every guest screen (web, app and kiosk) | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every guest screen (web, app and kiosk) | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | Light · Dark · Duotone | Light | every guest screen (web, app and kiosk) | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every P01 screen | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | PNG, JPG, SVG or MP4 from the media library | — | every P02 screen | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | min 0; max 10 | 3 | every guest screen (web, app and kiosk) | — |
| Splash background colour (`brand.splashBackgroundColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Show loading indicator (`brand.showLoadingIndicator`) | — | on | every guest screen (web, app and kiosk) | — |
| Intro video (`brand.introVideoAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | GST-001 | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | GST-001 | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Primary colour (`theme.primaryColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | body text on the background |
| Dark mode (`theme.darkMode`) | — | — | every guest screen (web, app and kiosk) | the dark variant on a device in dark mode (mobile app); derived from the light theme when absent |
| Dark mode: primary colour (`theme.darkMode.primaryColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Dark mode: background colour (`theme.darkMode.backgroundColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Dark mode: text colour (`theme.darkMode.textColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Corner radius (`theme.cornerRadius`) | min 0; max 32 | — | every guest screen (web, app and kiosk) | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | Glass · Solid | Glass | every guest screen (web, app and kiosk) | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | Solid · Outline · Pill | Solid | every guest screen (web, app and kiosk) | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | — | — | every guest screen (web, app and kiosk) | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | — | — | every guest screen (web, app and kiosk) | the one main call to action on each screen, when it should differ from the brand colour |
| Primary CTA: background (`theme.componentColours.primaryCta.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Primary CTA: text (`theme.componentColours.primaryCta.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: pay button (`theme.componentColours.payButton`) | — | — | every guest screen (web, app and kiosk) | the Pay button at checkout |
| Pay button: background (`theme.componentColours.payButton.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Pay button: text (`theme.componentColours.payButton.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: add to cart (`theme.componentColours.addToCart`) | — | — | every guest screen (web, app and kiosk) | every Add to cart button |
| Add to cart: background (`theme.componentColours.addToCart.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Add to cart: text (`theme.componentColours.addToCart.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: buy tickets button (`theme.componentColours.buyTicketsButton`) | — | — | every guest screen (web, app and kiosk) | the persistent Buy tickets button (mobile tab bar) |
| Buy tickets button: background (`theme.componentColours.buyTicketsButton.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Buy tickets button: text (`theme.componentColours.buyTicketsButton.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: link (`theme.componentColours.link`) | — | — | every guest screen (web, app and kiosk) | text links |
| Link: background (`theme.componentColours.link.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Link: text (`theme.componentColours.link.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: badge (`theme.componentColours.badge`) | — | — | every guest screen (web, app and kiosk) | badges on cards (LIMITED, NEW, 11 left) |
| Badge: background (`theme.componentColours.badge.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Badge: text (`theme.componentColours.badge.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Source image (`appIcons.sourceAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | no guest screen: the phone's home screen and the store listing | The `MediaAsset` id of the 1024×1024 source, from `assets` `createUpload` then `completeUpload`. |

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-016` · status **notStarted** · provenance generated
- Flow F102 *A brand is set, previewed, published and rolled back*, step 4: White-Label Branding Management. → 5 operations, 5 of them previously unwalked.
- Flow F103 *A tenant claims a domain and gets a certificate*, step 2: White-Label Branding Management. → 5 operations, 5 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (54), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (46 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-016?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Create preview, Diff config version, Publish tenant config, Restore config version, Save app icons, Save brand identity, Save theme, What publishing changes.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_ACCESS`, `TENANT_CONFIGURE`, `TENANT_PUBLISH`.
- [ ] The module and platform inputs below are applied.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-017` Domain & Certificate Management

**See domain & certificate management for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Branding & Localisation · wave 2 · needs the `core` module |
| Block | Block A · ticket #18097 (APP-WL-ADM-017) |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_ACCESS`, `TENANT_CONFIGURE` (1 operate, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCustomDomains` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `bannerId` (deepLink), `pageId` (deepLink), `policyKind` (deepLink), `version` (deepLink), `domainId` (deepLink) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/general/domain-and-certificate-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **41 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it. **Rebuilt 24 August.** This screen declared 41 operations and **not one was about a domain** — it carried the bulk-attached white-label set, and no domain or certificate operation existed anywhere in the package. **A white-label platform whose tenants cannot use their own domain is white-label in name only.**

**Known gaps.**  Open: No contract — not specified

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | select field | — | — | — | — | **Pick a tenant first** (decided 28 September, audit R098). This screen's operations run in that tenant's cell, and a platform token carries no tenant permission there until a platform-staff grant … | — |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client UUIDv7), `permissions` (tenant permissions only — the ones this screen's operations need, preselected), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Claim custom domain** (modal, opened by *Claim custom domain*; *Claim custom domain* calls `claimCustomDomain`, *Cancel* sends nothing)

**Collects what `claimCustomDomain` sends before it is called.** Required: `hostname`, `kind`. Optional: `verificationMethod`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Hostname `hostname` | text field | required | — | — | — | — | `claimCustomDomain` body |
| Kind `kind` | radio group | required | — | Guest web · Guest app · Partner portal · Developer portal | — | — | `claimCustomDomain` body |
| Verification method `verificationMethod` | segmented control | optional | Dns txt | Dns txt · Cname · Http file | — | — | `claimCustomDomain` body |

Errors to draw in the form: 409 Already claimed. Named as unavailable rather than attributed.

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (detail panel, from `openPlatformStaffGrant`): **Always visible while the screen acts on a tenant** (decided 28 September, audit R098): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Every custom domain** (data table, from `listCustomDomains`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Hostname | text | — |
| Kind | chip: Guest web, Guest app, Partner portal, Developer portal | — |
| Status | chip: Pending, Verifying, Verified, Issuing, Active, Failed… | — |
| Verification method | chip: Dns txt, Cname, Http file | — |
| Verification token | text | — |
| Certificate expires at | 1 Oct 2026, 14:30 | Renewal is a job, not a reminder. A certificate that expires on a Saturday takes a tenant's storefront down, and nobody reads a reminder … |
| Last checked at | 1 Oct 2026, 14:30 | — |
| Failure reason | text | — |

**The selected custom domain** (detail panel, from `listCustomDomains`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Hostname | text | — |
| Kind | chip: Guest web, Guest app, Partner portal, Developer portal | — |
| Status | chip: Pending, Verifying, Verified, Issuing, Active, Failed… | — |
| Verification method | chip: Dns txt, Cname, Http file | — |
| Verification token | text | — |
| Certificate expires at | 1 Oct 2026, 14:30 | Renewal is a job, not a reminder. A certificate that expires on a Saturday takes a tenant's storefront down, and nobody reads a reminder … |
| Last checked at | 1 Oct 2026, 14:30 | — |
| Failure reason | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Claim custom domain (primary button) | `claimCustomDomain` POST `/tenant-domains` | inline | CustomDomain | 409 Already claimed. Named as unavailable rather than attributed. | opens modal first |
| Verify custom domain (secondary button) | `verifyCustomDomain` POST `/tenant-domains/{domainId}/verify` | — | CustomDomain | 409 The hostname is already routed to another tenant (`hostname-taken`, from tenancy `setTenantDomainMapping`, SD-021); nothing was verified or issued. | — |
| Release custom domain (secondary button) | `relinquishCustomDomain` DELETE `/tenant-domains/{domainId}` | — | — | 409 The only active domain for a live app. Refused, naming what would break. | — |

**Data it reads**: `listTenants` (onLoad, The tenant picker — the operator picks a tenant before …); `listCustomDomains` (onLoad, The domains this tenant has claimed)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-016` White-Label Branding Management: *White-Label Branding Management*; carries `bannerId`, `pageId`, `policyKind`, `version`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The domain certificate list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the domain certificate untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No domain certificate yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCustomDomains` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listCustomDomains` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Already claimed. Named as unavailable rather than attributed.; 409 The hostname is already routed to another tenant (`hostname-taken`, from tenancy `setTenantDomainMapping`, SD-021); nothing was verified or issued.; 409 The only active domain for a live app. Refused, naming what would break. |

#### Permissions

- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `listCustomDomains` → `TENANT_CONFIGURE` (configure) · staff
- `claimCustomDomain` → `TENANT_CONFIGURE` (configure) · staff
- `verifyCustomDomain` → `TENANT_CONFIGURE` (configure) · staff
- `relinquishCustomDomain` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listCustomDomains` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Guest web hosting: small tenants run under a subdomain/subpath of the TICVAI domain; larger clients get a dedicated URL on their own domain. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-283)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Custom domain hostname (`domains.hostname`) | — | — | every website screen | — |
| Custom domain kind (`domains.kind`) | Guest web · Guest app · Partner portal · Developer portal | — | every website screen | — |
| Verification method (`domains.verificationMethod`) | Dns txt · Cname · Http file | Dns txt | every website screen | — |

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-017` · status **notStarted** · provenance generated
- Flow F103 *A tenant claims a domain and gets a certificate*, step 1: Domain & Certificate Management. → 4 operations, 4 of them previously unwalked.
- Flow F103 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-017?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Claim custom domain, Verify custom domain, Release custom domain.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-016`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_ACCESS`, `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-018` Localisation & Language Pack

**Configure localisation & language pack for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Branding & Localisation · wave 2 · needs the `core` module |
| Block | Block A · ticket #18098 (APP-WL-ADM-018) |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_ACCESS`, `TENANT_CONFIGURE` (1 operate, 1 configure) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listFaqs` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `bannerId` (deepLink), `pageId` (deepLink), `policyKind` (deepLink), `version` (deepLink) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/general/localisation-and-language-pack` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **36 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | select field | — | — | — | — | **Pick a tenant first** (decided 28 September, audit R098). This screen's operations run in that tenant's cell, and a platform token carries no tenant permission there until a platform-staff grant … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Include history | toggle | off | — | `listPolicies` ?includeHistory |
| Kind | radio group | — | Privacy · Terms and conditions · Refund · Cookie · Accessibility | `listPolicies` ?kind |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client UUIDv7), `permissions` (tenant permissions only — the ones this screen's operations need, preselected), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Save languages** (modal, opened by *Save languages*; *Save languages* calls `setLanguages`, *Cancel* sends nothing)

**Collects what `setLanguages` sends before it is called.** Required: `languages`, `defaultLanguage`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Languages `languages` | list of values (chips) | required | — | at least 1 | — | — | `setLanguages` body |
| Default language `defaultLanguage` | language picker | required | — | — | ISO 639-1 code, shown as the language name | — | `setLanguages` body |

Errors to draw in the form: 400 Default is not among the enabled languages

**Form: Save faqs** (modal, opened by *Save faqs*; *Save faqs* calls `setFaqs`, *Cancel* sends nothing)

**Collects what `setFaqs` sends before it is called.** Required: `categories`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Categories `categories` | repeatable rows | required | — | — | — | — | `setFaqs` body |
| Code `categories[].code` | text field | required | — | — | — | — | `setFaqs` body |
| Name `categories[].name` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `setFaqs` body |
| Sort order `categories[].sortOrder` | number field | optional | — | — | — | — | `setFaqs` body |
| Entries `categories[].entries` | repeatable rows | required | — | — | — | — | `setFaqs` body |
| ID `categories[].entries[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setFaqs` body |
| Question `categories[].entries[].question` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `setFaqs` body |
| Answer `categories[].entries[].answer` | rich text, one per language | required | — | — | English and Arabic (Arabic right to left) | Keyed by language code. Values are sanitised HTML. | `setFaqs` body |
| Sort order `categories[].entries[].sortOrder` | number field | optional | — | — | — | — | `setFaqs` body |
| Is published `categories[].entries[].isPublished` | toggle | optional | — | — | — | — | `setFaqs` body |

**Form: Save policy** (modal, opened by *Save policy*; *Save policy* calls `setPolicy`, *Cancel* sends nothing)

**Collects what `setPolicy` sends before it is called.** Required: `body`, `requiresReconsent`. Optional: `effectiveFrom`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Body `body` | rich text, one per language | required | — | — | English and Arabic (Arabic right to left) | Keyed by language code. Values are sanitised HTML. | `setPolicy` body |
| Requires reconsent `requiresReconsent` | toggle | required | — | — | — | True prompts existing guests to consent again on next launch. Material changes to a privacy notice generally require it. | `setPolicy` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setPolicy` body |

Errors to draw in the form: 400 The English (`en`) or Arabic (`ar`) version is missing (audit R096)

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (detail panel, from `openPlatformStaffGrant`): **Always visible while the screen acts on a tenant** (decided 28 September, audit R098): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Every faq category** (data table, from `listFaqs`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Sort order | 1,234 | — |
| Entries | list or chips (count when long) | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Every policy** (data table, from `listPolicies`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Privacy, Terms and conditions, Refund, Cookie, Accessibility | — |
| Title | text | The heading a guest sees, and the field a refund question retrieves against. |
| Body | in the reader's language | Keyed by language code. Values are sanitised HTML. |
| Requires reconsent | yes / no (icon or chip) | — |
| Effective from | 1 Oct 2026 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected faq category** (detail panel, from `listFaqs`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Sort order | 1,234 | — |
| Entries | list or chips (count when long) | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Save languages (primary button) | `setLanguages` PUT `/tenant-config/languages` | inline | LanguageConfig | 400 Default is not among the enabled languages | opens modal first |
| Save faqs (secondary button) | `setFaqs` PUT `/tenant-config/faqs` | inline | FaqCategory[] | — | opens modal first |
| Save policy (secondary button) | `setPolicy` PUT `/tenant-config/policies/{policyKind}` | inline | Policy | 400 The English (`en`) or Arabic (`ar`) version is missing (audit R096) | opens modal first |

**Data it reads**: `listTenants` (onLoad, The tenant picker — the operator picks a tenant before …); `listFaqs` (onLoad, List FAQs); `listPolicies` (onLoad, List legal policies)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The localisation language pack list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the localisation language pack untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No localisation language pack yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listFaqs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listFaqs` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Default is not among the enabled languages; 400 The English (`en`) or Arabic (`ar`) version is missing (audit R096); 400 Validation failed |

#### Permissions

- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `setLanguages` → `TENANT_CONFIGURE` (configure) · staff
- `listFaqs` → `TENANT_CONFIGURE` (configure) · staff, guest
- `listPolicies` → `TENANT_CONFIGURE` (configure) · staff
- `setFaqs` → `TENANT_CONFIGURE` (configure) · staff
- `setPolicy` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listFaqs` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.4.1 | The system should support multiple languages for the Ticketing POS, Self-Service Kiosks, websites mobile app and backend . | Ticketing Sales | CONTRACTED | `setLanguages` |
| 2.7.35 | The system should support: - Multilingual with language to be chosen by B2B client. Languages to include at a minimum Arabic and English. - Use of base system currency and all transactions performed … | Ticketing Sales | CONTRACTED | `setLanguages` |
| 2.16.12 | The system should allow usage of English and Arabic language on the ticket templates. | Ticketing Sales | CONTRACTED | `setLanguages` |
| 22.8.21 | Multi-Language Support | Marketing & CRM | CONTRACTED | `setLanguages` |
| 22.10.13 | Multi-Language Content Management | Marketing & CRM | CONTRACTED | `setLanguages` |
| 19.1.16 | FAQ Management - System shall support configurable FAQs. | Guest Mobile App & Branding | CONTRACTED | `setFaqs` |
| 19.1.17 | Policy Management - System shall support configurable policies. | Guest Mobile App & Branding | CONTRACTED | `setPolicy` |
| 19.1.18 | Terms & Conditions Management - System shall support configurable terms and conditions. | Guest Mobile App & Branding | CONTRACTED | `setPolicy` |
| 2.6.59 | Policy Management Manage cookie policy content centrally. Version control for policy updates. Publish updated policies automatically. Maintain historical policy versions. | Ticketing Sales | CONTRACTED | `setPolicy` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A new language is added as a configuration change, not development. Qossai wants a table-driven workflow like his prior project: a translation spreadsheet with a column per language reviewed by native speakers, then fed back through an AI translation pass. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-083)*
- Translation workflow: text entered in English, machine-translated, then reviewed and validated by the tenant's own team in the back office/CMS before publishing; applies to website, POS and mobile app. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-081)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Languages (`languages.languages`) | at least 1 | — | every guest screen (web, app and kiosk) | the language button in the header; Arabic flips every screen right to left |
| Default language (`languages.defaultLanguage`) | ISO 639-1 code, shown as the language name | — | every guest screen (web, app and kiosk) | the language a first visit opens in |
| Body (`policies.body`) | English and Arabic (Arabic right to left) | — | GST-040, GST-057, WEB-045 | Keyed by language code. Values are sanitised HTML. |
| Requires reconsent (`policies.requiresReconsent`) | — | — | GST-040, GST-057, WEB-045 | True prompts existing guests to consent again on next launch. Material changes to a privacy notice generally require it. |
| Effective from (`policies.effectiveFrom`) | 1 Oct 2026 (dd MMM yyyy) | — | GST-040, GST-057, WEB-045 | — |
| Categories (`faqs.categories`) | — | — | GST-040, WEB-045 | — |
| Categories: code (`faqs.categories[].code`) | — | — | GST-040, WEB-045 | — |
| Categories: name (`faqs.categories[].name`) | English and Arabic (Arabic right to left) | — | GST-040, WEB-045 | — |
| Categories: sort order (`faqs.categories[].sortOrder`) | — | — | GST-040, WEB-045 | — |
| Categories: entries (`faqs.categories[].entries`) | — | — | GST-040, WEB-045 | — |
| Entries: iD (`faqs.categories[].entries[].id`) | shows names, sends the id | — | GST-040, WEB-045 | — |
| Entries: question (`faqs.categories[].entries[].question`) | English and Arabic (Arabic right to left) | — | GST-040, WEB-045 | — |
| Entries: answer (`faqs.categories[].entries[].answer`) | English and Arabic (Arabic right to left) | — | GST-040, WEB-045 | Keyed by language code. Values are sanitised HTML. |
| Entries: sort order (`faqs.categories[].entries[].sortOrder`) | — | — | GST-040, WEB-045 | — |
| Entries: is published (`faqs.categories[].entries[].isPublished`) | — | — | GST-040, WEB-045 | — |

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-018` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Save languages, Save faqs, Save policy.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_ACCESS`, `TENANT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-019` Global Configuration & Defaults

**Change how global behaves here, and see which level the current value came from.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Branding & Localisation · wave 2 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_ACCESS`, `TENANT_CONFIGURE`, `TENANT_VIEW` (1 operate, 1 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPlans` reads the population and `getPlan` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `planId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/global-configuration-and-defaults` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Holds the tenant-level venue defaults (decided 28 September, audit R094).** `getVenueSettingsDefaults` and `setVenueSettingsDefaults` are the tenant row every venue inherits where its own value is null; a venue's own values are set on its venue settings screen. They run in the tenant's cell, so the operator picks a tenant and opens a platform-staff grant first (audit R098).

**Known gaps.**  Open: No contract — platform defaults not specified

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | select field | — | — | — | — | **Pick a tenant first** (decided 28 September, audit R098). This screen's operations run in that tenant's cell, and a platform token carries no tenant permission there until a platform-staff grant … | — |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client UUIDv7), `permissions` (tenant permissions only — the ones this screen's operations need, preselected), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Save venue defaults** (modal, opened by *Save venue defaults*; *Save venue defaults* calls `setVenueSettingsDefaults`, *Cancel* sends nothing)

**Collects what `setVenueSettingsDefaults` sends before it is called** (decided 28 September, audit R094). The whole row is replaced: an omitted limit returns to its proposed default. Each value must sit within its field's minimum and maximum, or the request is refused 400 naming the field. A venue's own values are untouched; a venue with none follows the new default at once. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Calendar day start hour `calendarDayStartHour` | stepper or slider | optional | 6 | min 0; max 23 | — | Where the venue's calendar day starts (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in … | `setVenueSettingsDefaults` body |
| Support hours `supportHours` | group | optional | — | — | — | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. | `setVenueSettingsDefaults` body |
| Mode `supportHours.mode` | radio group | optional | — | Always on · Business hours · Custom · None | — | — | `setVenueSettingsDefaults` body |
| Timezone `supportHours.timezone` | text field | optional | — | — | — | IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract. | `setVenueSettingsDefaults` body |
| Windows `supportHours.windows` | repeatable rows | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Day `supportHours.windows[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettingsDefaults` body |
| From `supportHours.windows[].from` | text field | optional | — | — | — | Wall-clock time the desk opens. | `setVenueSettingsDefaults` body |
| To `supportHours.windows[].to` | text field | optional | — | — | — | Wall-clock time the desk closes. | `setVenueSettingsDefaults` body |
| Out of hours message `supportHours.outOfHoursMessage` | text field | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Quiet hours `quietHours` | group | optional | — | — | — | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. | `setVenueSettingsDefaults` body |
| From `quietHours.from` | text field | optional | — | — | — | Wall-clock time sending stops | `setVenueSettingsDefaults` body |
| To `quietHours.to` | text field | optional | — | — | — | Wall-clock time sending resumes | `setVenueSettingsDefaults` body |
| Biometrics `biometrics` | group | optional | — | — | — | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. | `setVenueSettingsDefaults` body |
| Is enabled `biometrics.isEnabled` | toggle | optional | off | Off by default, and turning it on is refused without the two fields below. | — | Off by default, and turning it on is refused without the two fields below. `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — a DPIA nobody can … | `setVenueSettingsDefaults` body |
| Dpia reference `biometrics.dpiaReference` | text field | optional | — | max length 200 | — | The venue's own reference for its Article 21 assessment. The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is … | `setVenueSettingsDefaults` body |
| Consent notice acknowledged at `biometrics.consentNoticeAcknowledgedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When somebody confirmed the consent forms are in place at the point of capture. A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice … | `setVenueSettingsDefaults` body |
| Face tag purge minutes after close `biometrics.faceTagPurgeMinutesAfterClose` | number field (minutes) | optional | 0 | — | — | BL-106. How long a same-visit Face Tag survives past the close of the operating day, and zero is the default because that is what 3.2.44 describes. | `setVenueSettingsDefaults` body |
| Segregated access `segregatedAccess` | group | optional | — | — | — | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a prayer-time closure. | `setVenueSettingsDefaults` body |
| Is enabled `segregatedAccess.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettingsDefaults` body |
| Applies to access points `segregatedAccess.appliesToAccessPointIds` | multi-picker: choose applies to access points | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Schedule `segregatedAccess.schedule` | repeatable rows | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Day `segregatedAccess.schedule[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettingsDefaults` body |
| From `segregatedAccess.schedule[].from` | text field | optional | — | — | — | Wall-clock time | `setVenueSettingsDefaults` body |
| To `segregatedAccess.schedule[].to` | text field | optional | — | — | — | Wall-clock time | `setVenueSettingsDefaults` body |
| Admits `segregatedAccess.schedule[].admits` | radio group | optional | — | All · Women · Women and children · Families · Members | — | — | `setVenueSettingsDefaults` body |
| Gender verification `segregatedAccess.genderVerification` | segmented control | optional | Off | Off · Staff assisted · Device assisted; Available only where the driver reports the capability, and the result is advisory to the steward rather than decisive at the turnstile (3. | — | `off` — the entitlement decides and a steward handles exceptions. The default, and what is contracted. | `setVenueSettingsDefaults` body |
| Override rate alert threshold `segregatedAccess.overrideRateAlertThreshold` | number field | optional | — | — | — | Where `deviceAssisted` is on. An override rate near zero means the steward has stopped deciding, and that is the number that says whether the human safeguard is working or … | `setVenueSettingsDefaults` body |
| Alerting `alerting` | group | optional | — | The panel is the default and email or WhatsApp only where the matrix names them — an operational alert that arrives by email is an alert nobody sees in time. | — | CF-134. On-platform notification, marked as read. | `setVenueSettingsDefaults` body |
| Channel `alerting.channel` | segmented control | optional | Dashboard panel | Dashboard panel · Dashboard and email · Dashboard and whatsapp | — | — | `setVenueSettingsDefaults` body |
| Acknowledgement required `alerting.acknowledgementRequired` | toggle | optional | on | — | — | — | `setVenueSettingsDefaults` body |
| Escalate after minutes `alerting.escalateAfterMinutes` | number field (minutes) | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Display currencies `displayCurrencies` | list of values (chips) | optional | — | A code the region has no rate for is refused `400`. | — | Which currencies this venue shows guests (decided 28 September, audit R120 (a)). | `setVenueSettingsDefaults` body |
| Cart lease seconds `cartLeaseSeconds` | number field (seconds) | optional | 900 | min 30; max 3600 | — | How long a cart holds capacity (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. | `setVenueSettingsDefaults` body |
| Cart hold extension minutes `cartHoldExtensionMinutes` | stepper or slider (minutes) | optional | 5 | min 1; max 30 | — | How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094). | `setVenueSettingsDefaults` body |
| Cart max extensions `cartMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). | `setVenueSettingsDefaults` body |
| Resale cutoff hours `resaleCutoffHours` | number field (hours) | optional | 24 | min 0; max 168 | — | Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). | `setVenueSettingsDefaults` body |
| Exchange cutoff hours `exchangeCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). | `setVenueSettingsDefaults` body |
| Reschedule cutoff hours `rescheduleCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). | `setVenueSettingsDefaults` body |
| Reservation max extensions `reservationMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094). | `setVenueSettingsDefaults` body |
| Shift variance threshold `shiftVarianceThreshold` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. | `setVenueSettingsDefaults` body |
| Catalogue `catalogue` | group | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Max variants per product `catalogue.maxVariantsPerProduct` | number field | optional | 200 | min 1; max 2000 | — | Variants one product may generate from its attributes (`setProductAttributes` refuses above it). | `setVenueSettingsDefaults` body |
| Waitlist offer hold minutes `catalogue.waitlistOfferHoldMinutes` | number field (minutes) | optional | 30 | min 1; max 1440 | — | How long a waitlist offer holds the released capacity for the guest it was offered to. | `setVenueSettingsDefaults` body |
| Bulk price change escalation percent `catalogue.bulkPriceChangeEscalationPercent` | stepper or slider | optional | 10 | min 0; max 100; A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). | — | A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). | `setVenueSettingsDefaults` body |
| Bulk price change escalation count `catalogue.bulkPriceChangeEscalationCount` | number field | optional | 50 | min 1; A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). | — | A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). | `setVenueSettingsDefaults` body |
| … 27 more | | | | | | the rest are in `schemas.json` | `setVenueSettingsDefaults` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Create plan** (modal, opened by *Create plan*; *Create plan* calls `createPlan`, *Cancel* sends nothing)

**Collects what `createPlan` sends before it is called.** Required: `code`, `name`, `cellTier`, `licensedModules`, `limits`, `basePrice`. Optional: `description`, `billingPeriod`, `includesBrandedApp`, `includedAiTokens`. Dismissing sends nothing; the screen behind is unchanged.

`createPlan` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Create plan version** (modal, opened by *Create plan version*; *Create plan version* calls `createPlanVersion`, *Cancel* sends nothing)

**Collects what `createPlanVersion` sends before it is called.** Required: `code`, `name`, `cellTier`, `licensedModules`, `limits`, `basePrice`. Optional: `description`, `billingPeriod`, `includesBrandedApp`, `includedAiTokens`. Dismissing sends nothing; the screen behind is unchanged.

`createPlanVersion` is not in any contract: draw the form greyed and list it in FINDINGS.md.

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (detail panel, from `openPlatformStaffGrant`): **Always visible while the screen acts on a tenant** (decided 28 September, audit R098): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Every plan** (data table, from `listPlans`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | not in the schema: `Plan.code` |
| Name | text | not in the schema: `Plan.name` |
| Description | text | not in the schema: `Plan.description` |
| Cell tier | text | not in the schema: `Plan.cellTier` |
| Licensed modules | text | not in the schema: `Plan.licensedModules` |
| Limits | text | not in the schema: `Plan.limits` |
| Base price | text | not in the schema: `Plan.basePrice` |
| Billing period | text | not in the schema: `Plan.billingPeriod` |
| Includes branded app | text | not in the schema: `Plan.includesBrandedApp` |
| Included AI tokens | text | not in the schema: `Plan.includedAiTokens` |
| ID | text | not in the schema: `Plan.id` |
| Is active | text | not in the schema: `Plan.isActive` |

**Tenant defaults for every venue** (detail panel, from `getVenueSettingsDefaults`): **The tenant-level default each venue inherits** (decided 28 September, audit R094). A venue whose own value is null uses the value here; where the tenant has saved nothing these are the proposed defaults, client to correct. The venue facts on the schema (support hours, biometrics, segregated access) are not defaulted here.

| Shows | Format | Notes |
|---|---|---|
| Cart lease seconds | 1,234 | How long a cart holds capacity (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for … |
| Cart hold extension minutes | 1,234 | How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094). |
| Cart max extensions | 1,234 | How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). |
| Resale cutoff hours | 1,234 | Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). |
| Exchange cutoff hours | 1,234 | Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). |
| Reschedule cutoff hours | 1,234 | Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder` … |
| Reservation max extensions | 1,234 | How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094). |
| Shift variance threshold | AED 1,234.50 | Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| Display currencies | list or chips (count when long) | Which currencies this venue shows guests (decided 28 September, audit R120 (a)). |

**The selected plan** (detail panel, from `getPlan`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | not in the schema: `Plan.code` |
| Name | text | not in the schema: `Plan.name` |
| Description | text | not in the schema: `Plan.description` |
| Cell tier | text | not in the schema: `Plan.cellTier` |
| Licensed modules | text | not in the schema: `Plan.licensedModules` |
| Limits | text | not in the schema: `Plan.limits` |
| Base price | text | not in the schema: `Plan.basePrice` |
| Billing period | text | not in the schema: `Plan.billingPeriod` |
| Includes branded app | text | not in the schema: `Plan.includesBrandedApp` |
| Included AI tokens | text | not in the schema: `Plan.includedAiTokens` |
| ID | text | not in the schema: `Plan.id` |
| Is active | text | not in the schema: `Plan.isActive` |
| Subscriber count | text | not in the schema: `Plan.subscriberCount` |
| Published at | text | not in the schema: `Plan.publishedAt` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Save venue defaults (secondary button) | `setVenueSettingsDefaults` PUT `/venue-settings-defaults` | VenueSettings | VenueSettings | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Create plan (primary button) | `createPlan` (not in any contract) | — | — | — | — |
| Create plan version (secondary button) | `createPlanVersion` (not in any contract) | — | — | — | — |

**Data it reads**: `getVenueSettingsDefaults` (onLoad, The tenant-level default each venue inherits (decided 28 …); `listTenants` (onLoad, The tenant picker — the operator picks a tenant before …); `listPlans` (onLoad, List subscription plans)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The global defaults list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the global defaults untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No global defaults yet. Offers Create plan (`createPlan`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listPlans` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listPlans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getVenueSettingsDefaults` → `TENANT_VIEW` (read) · staff
- `setVenueSettingsDefaults` → `TENANT_CONFIGURE` (configure) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listPlans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

20 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.2.1 | Subscription Plans - System shall support configurable subscription plans. | Subscription & Licensing Management | CONTRACTED | `createPlan` |
| 20.4.8 | Module Pricing - System shall support module-specific pricing. | Subscription & Licensing Management | CONTRACTED | `createPlan` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| 3.2.46 | Face Pass shouldt restrict male guests attempting to enter during Friday Ladies Night, which needs to be validated with rule-based facial recognition validation. | Admission and Access | CONTRACTED | data `VenueSettings` |
| 8.9.3 | System shall display queue lengths, estimated wait times, queue utilization, queue alerts, and queue prediction metrics. | Unified Operations Dashboard | CONTRACTED | data `VenueSettings` |
| 11.1.15 | Approval Breach Alerts - System shall notify users when approval SLA thresholds are exceeded. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.17 | Approval Notifications - System shall notify approvers when new approval requests are assigned. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.18 | Approval Reminder Notifications - System shall send reminder notifications for pending approvals. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.19 | Approval Outcome Notifications - System shall notify requestors when approvals are approved, rejected or escalated. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 15.1.32 | Overstock Alerts - System shall generate overstock alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.33 | Stock Shortage Alerts - System shall generate stock shortage alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| … 8 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-019` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (78), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (43 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Save venue defaults, Create plan, Create plan version.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_ACCESS`, `TENANT_CONFIGURE`, `TENANT_VIEW`.
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

**3 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"claimCustomDomain": {"method":"POST","path":"/tenant-domains","contract":"white-label","summary":"Claim a domain and get a verification token","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CustomDomain"},
"createPreview": {"method":"POST","path":"/tenant-config/preview","contract":"white-label","summary":"Generate a preview link","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Preview"},
"diffConfigVersion": {"method":"GET","path":"/tenant-config/versions/{version}/diff","contract":"white-label","summary":"Compare a version against the working draft","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"against","in":"query","required":null}],"requestBody":null,"responds":"ConfigDiff"},
"getAppIcons": {"method":"GET","path":"/tenant-config/app-icons","contract":"white-label","summary":"Read app icon set","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AppIcons"},
"getBrandIdentity": {"method":"GET","path":"/tenant-config/brand","contract":"white-label","summary":"Read brand identity","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"BrandIdentity"},
"getTheme": {"method":"GET","path":"/tenant-config/theme","contract":"white-label","summary":"Read colour theme","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"Theme"},
"getVenueSettingsDefaults": {"method":"GET","path":"/venue-settings-defaults","contract":"tenancy","summary":"The tenant's default for every venue setting","permission":"TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"listConfigVersions": {"method":"GET","path":"/tenant-config/versions","contract":"white-label","summary":"Version history","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCustomDomains": {"method":"GET","path":"/tenant-domains","contract":"white-label","summary":"The domains this tenant has claimed","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"CustomDomain"},
"listFaqs": {"method":"GET","path":"/tenant-config/faqs","contract":"white-label","summary":"List FAQs","permission":"TENANT_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"FaqCategory"},
"listPolicies": {"method":"GET","path":"/tenant-config/policies","contract":"white-label","summary":"List legal policies","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"includeHistory","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"Policy"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"publishTenantConfig": {"method":"POST","path":"/tenant-config/publish","contract":"white-label","summary":"Publish the working draft","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConfigVersion"},
"relinquishCustomDomain": {"method":"DELETE","path":"/tenant-domains/{domainId}","contract":"white-label","summary":"Give the domain up","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"restoreConfigVersion": {"method":"POST","path":"/tenant-config/versions/{version}/restore","contract":"white-label","summary":"Restore a previous version","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TenantConfig"},
"setAppIcons": {"method":"PUT","path":"/tenant-config/app-icons","contract":"white-label","summary":"Set app icons","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AppIcons"},
"setBrandIdentity": {"method":"PUT","path":"/tenant-config/brand","contract":"white-label","summary":"Set logo, favicon and splash","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BrandIdentity","responds":"BrandIdentity"},
"setFaqs": {"method":"PUT","path":"/tenant-config/faqs","contract":"white-label","summary":"Set FAQ categories and entries","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FaqCategory"},
"setLanguages": {"method":"PUT","path":"/tenant-config/languages","contract":"white-label","summary":"Set enabled languages and default","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LanguageConfig"},
"setPolicy": {"method":"PUT","path":"/tenant-config/policies/{policyKind}","contract":"white-label","summary":"Publish a policy version","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Policy"},
"setTheme": {"method":"PUT","path":"/tenant-config/theme","contract":"white-label","summary":"Set colour theme","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"Theme","responds":"Theme"},
"setVenueSettingsDefaults": {"method":"PUT","path":"/venue-settings-defaults","contract":"tenancy","summary":"Set the tenant's default for every venue setting","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VenueSettings","responds":"VenueSettings"},
"verifyCustomDomain": {"method":"POST","path":"/tenant-domains/{domainId}/verify","contract":"white-label","summary":"Check the record and issue the certificate","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CustomDomain"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessibilitySettings": {"type":"object","description":"BL-065, 2.1.27. **POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated.**\n**A kiosk is the hard case.** A guest with low vision using a website brings their own assistive technology; a guest at a kiosk gets whatever the kiosk offers, so the settings have to be on the device rather than in the browser.\n","properties":{"largeTextAvailable":{"type":"boolean","default":true},"highContrastAvailable":{"type":"boolean","default":true},"simplifiedNavigationAvailable":{"type":"boolean","default":true},"screenReaderSupported":{"type":"boolean","default":true},"reachableHeightModeAvailable":{"type":"boolean","default":false,"description":"**Moves the interface to the lower half of the screen** for a guest using a wheelchair. A kiosk mounted at standing height is unusable otherwise, and no software setting fixes the mounting — this is the mitigation.\n"},"sessionTimeoutMultiplier":{"type":"number","default":1,"description":"**Timeouts are an accessibility barrier nobody counts.** A guest who needs three times as long to read a screen should not lose their basket to a 90-second inactivity timer.\n"}}},
"AppAvailability": {"type":"string","description":"**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n","enum":["open","soldOut","closed"],"default":"open"},
"AppIcons": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["sourceAssetRef","changeScope"],"properties":{"sourceAssetRef":{"type":"string","format":"uuid","description":"The `MediaAsset` id of the 1024×1024 source."},"derived":{"type":"array","readOnly":true,"x-ticvai-derived":"onWrite","description":"Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on `setAppIcons` (audit R163).","items":{"type":"object","properties":{"platform":{"type":"string","enum":["ios","android","web"]},"size":{"type":"string"},"assetRef":{"type":"string","format":"uuid"}}}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` — icons are baked into the binary."},"liveVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Icon currently shipped. Differs from the draft until the next release."},"requiresRebuild":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onRead","description":"True while the draft's source differs from the icon in `liveVersion`."}}},
"BookingFlow": {"x-ticvai-persistence":"whitelabel.booking_flow","type":"object","description":"**A venue's booking flow (decided 29 September, W12: operators pick their flows, see which steps are required, set their own order).** Made from a `BookingFlowType`; lives in the working draft and reaches guests with `publishTenantConfig`, which copies the venue's flows into the version's snapshot. A product or category names its flow (catalogue `bookingFlowId`); otherwise the venue's default for the type serving its kind applies.\n","required":["flowTypeKey","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createBookingFlowDefinition`."},"flowTypeKey":{"$ref":"#/components/schemas/BookingFlowTypeKey"},"name":{"type":"string","maxLength":80,"description":"Staff-facing, e.g. \"Day pass, date first\". Not shown to guests."},"isDefaultForType":{"type":"boolean","default":false,"description":"At most one per venue and type; setting it takes it from the previous default."},"isEnabled":{"type":"boolean","default":true,"description":"A disabled flow is kept and not published; products naming it fall back to the default."},"steps":{"type":"array","maxItems":30,"description":"Every step of the type, in the venue's order. Filled from the type when left out on create.","items":{"$ref":"#/components/schemas/BookingFlowStep"}},"settings":{"$ref":"#/components/schemas/BookingFlowLevelSettings"},"isValid":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. `publishTenantConfig` refuses a draft holding an invalid enabled flow."},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"BookingFlowConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","description":"**Set per tenant, with a per-venue override (decided 29 September, rev 3 CFG-11).** One tenant with several venues (the Kids Club branches, Coastal Aqua beside Union Arena) needs them to differ. The settings in force at a venue are the tenant's, with that venue's entry in `venueOverrides` laid over them field by field. The guest app resolves them for the venue the guest picked (audit R267); `effectiveForVenueId` on `getBookingFlowConfig` returns them resolved.\n","allOf":[{"$ref":"#/components/schemas/BookingFlowSettings"},{"type":"object","properties":{"venueOverrides":{"type":"array","maxItems":200,"default":[],"description":"Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. An override for a venue later closed is kept and has no effect.","items":{"$ref":"#/components/schemas/BookingFlowVenueOverride"}}}}]},
"BrandIdentity": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","description":"Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB (decided 28 September, audit R270).\n","required":["logoAssetRef"],"properties":{"logoAssetRef":{"type":"string","format":"uuid","description":"The primary logo."},"logoDarkAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"Used on dark backgrounds. Falls back to the primary logo."},"logoVariant":{"type":"string","enum":["light","dark","duotone"],"default":"light","description":"**Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4).** `light` uses `logoAssetRef`, `dark` uses `logoDarkAssetRef` (falling back to the primary logo), and `duotone` the two-colour reading of the primary logo.\n"},"faviconAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"The browser tab icon for the guest web app."},"splashImageAssetRefs":{"type":"array","description":"Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163).","items":{"type":"string","format":"uuid"}},"splashDurationSeconds":{"type":"integer","minimum":0,"maximum":10,"default":3},"splashBackgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"showLoadingIndicator":{"type":"boolean","default":true},"splashChangeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163)."},"introVideoAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"**The optional intro video (decided 29 September, MOB-5).** A video `MediaAsset` from the media library (CMS-010). Streamed, so a change reaches guests with the publish and needs no app build.\n"},"introVideoMode":{"type":"string","enum":["off","firstLaunch","everyLaunch"],"default":"off","description":"When GST-001 plays it full screen. \"Skip introduction\" is always shown. Anything but `off` needs `introVideoAssetRef`, or 400."}}},
"ChangeScope": {"type":"string","description":"Whether a change reaches guests on publish or needs a store release.\n","enum":["runtime","buildTime"]},
"ConfigDiff": {"x-ticvai-persistence":"none — computed","type":"object","required":["fromVersion","toVersion","changes"],"properties":{"fromVersion":{"type":"string"},"toVersion":{"type":"string"},"changes":{"type":"array","items":{"type":"object","required":["area","path","changeKind"],"properties":{"area":{"type":"string"},"path":{"type":"string"},"changeKind":{"type":"string","enum":["added","removed","modified"]},"before":{"type":"string","nullable":true},"after":{"type":"string","nullable":true},"changeScope":{"$ref":"#/components/schemas/ChangeScope"}}}}}},
"ConfigVersion": {"x-ticvai-persistence":"whitelabel.config_version","type":"object","required":["version","publishedAt","publishedByPrincipalId","note","isCurrent"],"properties":{"version":{"type":"string"},"publishedAt":{"type":"string","format":"date-time"},"publishedByPrincipalId":{"type":"string","format":"uuid"},"publishedByName":{"type":"string"},"note":{"type":"string"},"isCurrent":{"type":"boolean"},"scheduledFor":{"type":"string","format":"date-time","nullable":true},"contentHash":{"type":"string"},"pendingBuildTimeChanges":{"type":"array","description":"Changes in this version that will not reach guests until the next store release. Surfaced at publish so nobody expects a new icon tomorrow.\n","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"platforms":{"type":"array","items":{"type":"string","enum":["ios","android","web"]}}}}},"snapshot":{"type":"object","additionalProperties":true,"readOnly":true,"description":"**What this version contained.** The working draft exactly as published, in the shape `getTenantConfig` returns (`TenantConfig`) — so `restoreConfigVersion` has something to copy back and `diffConfigVersion` something to compare. Deliberately an open object here: its shape is `TenantConfig`, and a `$ref` would make it a key to a `tenant_config` row rather than a copy. Written once by `publishTenantConfig` and never changed. Left out of `listConfigVersions` items; a version's content is read with `getTenantConfig?version=`.\n"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"CustomDomain": {"type":"object","x-ticvai-persistence":"whitelabel.custom_domain","description":"24 August. **`ADM-017 Domain & Certificate Management` declared 41 operations and not one of them was about a domain** — it carried the same bulk-attached set as every other white-label screen, and **no domain or certificate operation existed anywhere in 1,010.**\nA white-label platform whose tenants cannot use their own domain is a white-label platform in name only.\n**Verification before issuance, always.** A certificate issued for a domain the tenant does not control is a certificate issued to whoever asked.\n","required":["id","tenantId","hostname","status"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"hostname":{"type":"string"},"kind":{"type":"string","enum":["guestWeb","guestApp","partnerPortal","developerPortal"]},"status":{"type":"string","enum":["pending","verifying","verified","issuing","active","failed","expired","revoked"]},"verificationMethod":{"type":"string","enum":["dnsTxt","cname","httpFile"]},"verificationToken":{"type":"string","readOnly":true},"verificationRecord":{"type":"object","readOnly":true,"description":"**The record the tenant must publish**, which `claimCustomDomain` promises and the claim had nowhere to hold. Set when the claim is made, from `hostname`, `verificationMethod` and `verificationToken`: a TXT record for `dnsTxt`, a CNAME for `cname`, and for `httpFile` the URL path to serve and the file's content.\n","required":["type","name","value"],"properties":{"type":{"type":"string","enum":["TXT","CNAME","httpFile"]},"name":{"type":"string","description":"The DNS name to create, or for `httpFile` the URL path on `hostname`."},"value":{"type":"string","description":"The record's value, CNAME target or file content."}}},"certificateExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**Renewal is a job, not a reminder.** A certificate that expires on a Saturday takes a tenant's storefront down, and nobody reads a reminder email on a Saturday.\n"},"lastCheckedAt":{"type":"string","format":"date-time","nullable":true},"failureReason":{"type":"string","nullable":true}}},
"FaqCategory": {"x-ticvai-persistence":"whitelabel.faq_category + whitelabel.faq_entry","type":"object","required":["code","name","entries"],"properties":{"code":{"type":"string"},"name":{"$ref":"#/components/schemas/LocalisedText"},"sortOrder":{"type":"integer"},"entries":{"type":"array","items":{"type":"object","required":["id","question","answer"],"properties":{"id":{"type":"string","format":"uuid"},"question":{"$ref":"#/components/schemas/LocalisedText"},"answer":{"$ref":"#/components/schemas/LocalisedRichText"},"sortOrder":{"type":"integer"},"isPublished":{"type":"boolean"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"FeatureToggle": {"x-ticvai-persistence":"whitelabel.feature_toggle","type":"object","required":["featureKey","isEnabled","changeScope"],"properties":{"featureKey":{"allOf":[{"$ref":"#/components/schemas/FeatureKey"}],"description":"`guestCheckout` is **off by default** (decided 17 September 2026, matrix 2.6.28, placement settled by [ADR-0045](../../docs/adr/0045-every-order-carries-a-proven-contact.md) 18 September): **the venue sets this from the configuration menu**, and it decides which routes the checkout page offers — off, the guest signs in verified at checkout; on, a guest may also check out without an account after proving their contact with a one-time code. **It gates checkout, never the cart.** The kiosk is not governed by it. Rule on `identity` `verifyGuestEmail`.\n"},"displayName":{"type":"string"},"isEnabled":{"type":"boolean"},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Wallet and payment integrations are `buildTime` on native apps — enabling one needs a release, not a publish.\n"},"requiresConfiguration":{"type":"boolean","description":"True where the feature needs credentials or setup elsewhere first."}}},
"FontConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["primaryLatin"],"properties":{"primaryLatin":{"type":"string"},"primaryArabic":{"type":"string","nullable":true,"description":"Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match.\n"},"secondaryLatin":{"type":"string","nullable":true},"secondaryArabic":{"type":"string","nullable":true,"description":"Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163)."},"customFontAssetRefs":{"type":"array","description":"Uploaded font files, as `MediaAsset` ids.","items":{"type":"string","format":"uuid"}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"x-ticvai-derived":"onRead","description":"Custom font files are `buildTime`; selecting a bundled face is `runtime`."}}},
"FooterConfig": {"type":"object","x-ticvai-persistence":"whitelabel.footer_config + whitelabel.footer_config_column + whitelabel.footer_config_social_link","description":"BL-002. **`setHeader` and `HeaderConfig` exist and the footer does not**, which looked like symmetry until you notice it is not: **a header is chrome and a footer is a link surface.**\nA footer carries the legal links — terms, privacy, accessibility statement, cookie preferences — and **those are the ones a regulator checks.** Treating it as a mirror of the header would have given it a logo and no way to reach a privacy notice.\n**Where it is stored.** `legalLinks` and `copyrightText` are columns of `whitelabel.footer_config`; each entry of `columns` is a `whitelabel.footer_config_column` row and each entry of `socialLinks` a `whitelabel.footer_config_social_link` row. Part of the working draft (see the header). **In the tenant's own database, not the control plane (decided 28 September, audit R163)**: it moved from `control.footer_config` and its two child tables.\n","required":["id","scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `tenant` scope by the server."},"columns":{"type":"array","items":{"type":"object","properties":{"heading":{"type":"string"},"links":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string"},"url":{"type":"string"},"opensCookiePreferences":{"type":"boolean","default":false}}}}}}},"legalLinks":{"type":"object","description":"**Required links, held separately from the free-form columns** — a tenant reorganising their footer must not be able to remove the privacy notice by accident.\n","properties":{"termsUrl":{"type":"string"},"privacyUrl":{"type":"string"},"accessibilityUrl":{"type":"string","nullable":true},"cookiePolicyUrl":{"type":"string","nullable":true}}},"copyrightText":{"type":"string"},"socialLinks":{"type":"array","items":{"type":"object","properties":{"platform":{"type":"string"},"url":{"type":"string"}}}}}},
"HeaderConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["layout"],"properties":{"layout":{"type":"string","enum":["logoLeft","logoCentre","logoWithMenu"]},"showLogo":{"type":"boolean","default":true},"showMenu":{"type":"boolean","default":true},"showNotifications":{"type":"boolean","default":true},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},
"HomepageLayout": {"x-ticvai-persistence":"whitelabel.homepage_section","type":"object","required":["sections"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"sections":{"type":"array","items":{"type":"object","required":["kind","sortOrder","isVisible"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"kind":{"$ref":"#/components/schemas/HomepageSectionKind"},"title":{"$ref":"#/components/schemas/LocalisedText"},"sortOrder":{"type":"integer"},"isVisible":{"type":"boolean"},"contentPageId":{"type":"string","format":"uuid","nullable":true},"maxItems":{"type":"integer","nullable":true,"description":"How many items the section shows. On the mobile Home, `attractions`, `dining`, `whatsOn` and `shop` show 1 or 2 highlights (decided 29 September, MOB-3)."},"heroStyle":{"type":"string","nullable":true,"enum":["carousel","video","poster","split",null],"description":"For `heroBanner` only (decided 29 September, MOB-3)."}}}}}},
"LanguageConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["languages","defaultLanguage"],"properties":{"languages":{"type":"array","items":{"type":"string","pattern":"^[a-z]{2}$"}},"defaultLanguage":{"type":"string","pattern":"^[a-z]{2}$"},"rtlLanguages":{"type":"array","readOnly":true,"x-ticvai-derived":"onRead","description":"The enabled languages written right to left — those whose Unicode CLDR character order is `right-to-left` (Arabic, `ar`, among them). Not configured; it follows from `languages`.","items":{"type":"string","pattern":"^[a-z]{2}$"}},"translationGaps":{"type":"array","readOnly":true,"description":"Content lacking a version in an enabled language.","items":{"type":"object","properties":{"language":{"type":"string"},"missingCount":{"type":"integer"},"areas":{"type":"array","items":{"type":"string"}}}}}}},
"LocalisedRichText": {"x-ticvai-persistence":"none — jsonb column","type":"object","description":"Keyed by language code. Values are sanitised HTML.","additionalProperties":{"type":"string"}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MinimumAppVersion": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n","properties":{"ios":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"},"android":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"}}},
"ModuleEnablement": {"x-ticvai-persistence":"whitelabel.module_enablement","type":"object","required":["moduleKey","isLicensed","isEnabled"],"properties":{"moduleKey":{"$ref":"#/components/schemas/ModuleKey"},"displayName":{"type":"string"},"isLicensed":{"type":"boolean","description":"From the tenant's subscription. False makes enablement impossible."},"isEnabled":{"type":"boolean"},"referencedBy":{"type":"array","readOnly":true,"x-ticvai-derived":"onWrite","description":"Navigation items and homepage sections pointing at this module. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write.","items":{"type":"string"}}}},
"NavigationConfig": {"x-ticvai-persistence":"whitelabel.navigation_item","type":"object","description":"**The mobile tab set is venue configuration (decided 29 September, MOB-1; 29 September brief decision 6).** Before a tenant saves its own, `bottomNavigation` is Home, Explore, Plan and Tickets (each an `appSection` link), with the Buy tickets button beside them; Map is an optional tab. Plan is left out while `visitPlanner` is off.\n","required":["kind","items"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"kind":{"type":"string","enum":["bottomNavigation","drawer","tabs"]},"items":{"type":"array","maxItems":12,"items":{"type":"object","required":["label","target","isVisible","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"label":{"$ref":"#/components/schemas/LocalisedText"},"icon":{"type":"string"},"target":{"$ref":"#/components/schemas/LinkTarget"},"isVisible":{"type":"boolean","description":"At most five may be visible in bottom navigation; the rest overflow."},"sortOrder":{"type":"integer"}}}},"buyButton":{"type":"object","nullable":true,"description":"**The persistent Buy tickets button (decided 29 September, MOB-2).** On every screen of the mobile app except the booking and checkout steps; it opens GST-003. Read with `bottomNavigation`.\n","properties":{"style":{"type":"string","enum":["raised","floating","flat","hidden"],"default":"raised","description":"`raised` sits in the centre of the tab bar, as the v4 prototype shows; `hidden` turns it off."},"label":{"$ref":"#/components/schemas/LocalisedText"}}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE"]},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"Policy": {"x-ticvai-persistence":"whitelabel.policy","type":"object","required":["kind","version","body","effectiveFrom","publishedAt"],"properties":{"kind":{"$ref":"#/components/schemas/PolicyKind"},"title":{"type":"string","description":"The heading a guest sees, and the field a refund question retrieves against.\n"},"version":{"type":"string","description":"Immutable. A guest who consented to version 3 consented to version 3, and a policy that changes under a recorded consent is a compliance failure.\n"},"body":{"$ref":"#/components/schemas/LocalisedRichText"},"requiresReconsent":{"type":"boolean"},"effectiveFrom":{"type":"string","format":"date"},"publishedByPrincipalId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"PolicyKind": {"type":"string","enum":["privacy","termsAndConditions","refund","cookie","accessibility"]},
"Preview": {"x-ticvai-persistence":"none — short-lived, cache only","type":"object","required":["previewId","url","expiresAt"],"properties":{"previewId":{"type":"string","format":"uuid"},"url":{"type":"string"},"platform":{"type":"string","enum":["ios","android","web"]},"theme":{"type":"string","enum":["light","dark"]},"language":{"type":"string","pattern":"^[a-z]{2}$"},"expiresAt":{"type":"string","format":"date-time"}}},
"TenantConfig": {"x-ticvai-persistence":"whitelabel.tenant_config","type":"object","description":"**The tenant's working draft**, one row per tenant (see the header). Published versions are `ConfigVersion.snapshot`, not further rows here.\n**Only `tenantId` and `version` are required**, because the draft is built one part at a time: the first `set*` call creates the row with that part alone. A part that is still unset is what `validateTenantConfig` reports (`missingRequiredAsset` and the like) and what blocks `publishTenantConfig` — a storage rule that every part exist would stop the first save.\n","required":["tenantId","version"],"properties":{"tenantId":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The draft's working version label; the published one is `ConfigVersion.version`."},"isDraft":{"type":"boolean","readOnly":true,"description":"True for the working draft, which is the only row."},"brand":{"$ref":"#/components/schemas/BrandIdentity"},"appIcons":{"$ref":"#/components/schemas/AppIcons"},"bookingFlow":{"$ref":"#/components/schemas/BookingFlowConfig"},"bookingFlows":{"type":"array","readOnly":true,"x-ticvai-derived":"onRead","description":"Every venue's booking flows in the draft (`whitelabel.booking_flow`), so a publish snapshots them with the rest (decided 29 September, W12).","items":{"$ref":"#/components/schemas/BookingFlow"}},"theme":{"$ref":"#/components/schemas/Theme"},"fonts":{"$ref":"#/components/schemas/FontConfig"},"footer":{"$ref":"#/components/schemas/FooterConfig"},"notificationBranding":{"type":"object","nullable":true,"description":"BL-003. **`marketing-crm` holds the templates and nothing said whose identity they wear.** A message sent on behalf of a venue carries that venue's sender name, reply-to and logo — **an operational alert arriving from `noreply@ticvai.com` is one a guest marks as spam.**\nResolved on the template at send time rather than duplicated per template.\n","properties":{"senderName":{"type":"string"},"replyToEmail":{"type":"string","format":"email"},"smsSenderId":{"type":"string","nullable":true},"whatsappBusinessId":{"type":"string","nullable":true},"logoAssetId":{"type":"string","format":"uuid","nullable":true}}},"enabledPaymentMethods":{"type":"array","nullable":true,"description":"BL-004. **`FeatureToggle` could turn Apple Pay on and could not say which cards a tenant accepts.** Resolved against `orders.PaymentProvider.supportedMethods` — the tenant's choice within what the gateway offers, and **a tenant enabling a method their provider does not support should fail here rather than at checkout.**\n","items":{"type":"string"}},"accessibility":{"$ref":"#/components/schemas/AccessibilitySettings"},"header":{"$ref":"#/components/schemas/HeaderConfig"},"navigation":{"$ref":"#/components/schemas/NavigationConfig"},"homepage":{"$ref":"#/components/schemas/HomepageLayout"},"modules":{"type":"array","items":{"$ref":"#/components/schemas/ModuleEnablement"}},"features":{"type":"array","items":{"$ref":"#/components/schemas/FeatureToggle"}},"languages":{"$ref":"#/components/schemas/LanguageConfig"},"updatedAt":{"type":"string","format":"date-time"},"isInMaintenance":{"type":"boolean","default":false,"description":"Written by `setMaintenanceMode`; read by `getTenantAppStatus`."},"maintenanceMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The message on the branded maintenance screen."},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"allOf":[{"$ref":"#/components/schemas/MinimumAppVersion"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"contact":{"allOf":[{"$ref":"#/components/schemas/VenueContact"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"availability":{"allOf":[{"$ref":"#/components/schemas/AppAvailability"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"venues":{"type":"array","x-ticvai-derived":"onRead","description":"The tenant's active venues, for the guest venue picker on WEB-001 and GST-001 (decided 28 September, audit R267). Public: returned without a session and cached with the rest of the response. Read from `tenancy` venues; a closed or archived venue is left out.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid"},"name":{"$ref":"#/components/schemas/LocalisedText"},"city":{"type":"string","nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Today's hours as shown to a guest, e.g. \"10:00 to 22:00\"."}}}}}},
"Theme": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["primaryColour","secondaryColour","backgroundColour","textColour"],"properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"secondaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"accentColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"darkMode":{"type":"object","description":"Optional dark variant. Derived from the light theme when absent.","properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},"cornerRadius":{"type":"integer","minimum":0,"maximum":32,"description":"The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). Its named palettes, font pairs and background tones are presets over the colours here and `FontConfig`, not stored values."},"surfaceStyle":{"type":"string","enum":["glass","solid"],"default":"glass","description":"Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3)."},"buttonStyle":{"type":"string","enum":["solid","outline","pill"],"default":"solid","description":"Button shape (decided 29 September, rev 3 CFG-3)."},"componentColours":{"type":"object","description":"**Colours for single interactive elements (decided 17 September, M17-11).** Each is optional and falls back to the theme colours. Every pair passes the same contrast check as the theme (`ContrastProblem`), or `setTheme` refuses it with 400. The guest flow stays the standard one; only the colours change.\n","properties":{"primaryCta":{"$ref":"#/components/schemas/ThemeComponentColour"},"payButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"addToCart":{"$ref":"#/components/schemas/ThemeComponentColour"},"buyTicketsButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"link":{"$ref":"#/components/schemas/ThemeComponentColour"},"badge":{"$ref":"#/components/schemas/ThemeComponentColour"}}}}},
"ThemeComponentColour": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","properties":{"background":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"text":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},
"VenueContact": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n","properties":{"phone":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"whatsapp":{"type":"string","nullable":true},"address":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Prose, as the guest reads it. The bookable hours are the catalogue's."}}},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}}
}
```
