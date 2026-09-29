# P09-branding-localisation-01 — P09 · Branding & Localisation

**4 screens · 28 operations · 41 schemas · 6 permissions**

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
| `screens.json` | Every field of every screen in the batch. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_VIEW, TENANT_CONFIGURE, TENANT_PUBLISH, TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-016` | White-Label Branding Management | listDetail | 13 | 6 | — |
| `ADM-017` | Domain & Certificate Management | listDetail | 6 | 2 | — |
| `ADM-018` | Localisation & Language Pack | listDetail | 7 | 4 | — |
| `ADM-019` | Global Configuration & Defaults | listDetail | 8 | 4 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-016",
  "name": "White-Label Branding Management",
  "module": "Branding & Localisation",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C57",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/white-label-branding-management",
   "component": "apps/ticvai-web/src/routes/general/WhiteLabelBrandingManagementForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-017"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-016 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-016 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **30 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listConfigVersions` reads the population and `getAppIcons` reads one of them — list, select, act",
  "purpose": "See white-label branding management for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "selectField",
       "label": "Tenant",
       "bindsTo": "Tenant",
       "columns": [
        "Tenant.id",
        "Tenant.code",
        "Tenant.name",
        "Tenant.status"
       ],
       "operation": "listTenants",
       "notes": "**Pick a tenant first** (decided 28 September, audit R098). This screen's operations run in that tenant's cell, and a platform token carries no tenant permission there until a platform-staff grant into it is open.",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "detailPanel",
       "label": "Open grant into this tenant",
       "bindsTo": "PlatformStaffGrant",
       "columns": [
        "PlatformStaffGrant.id",
        "PlatformStaffGrant.operatorDisplayName",
        "PlatformStaffGrant.permissions",
        "PlatformStaffGrant.reason",
        "PlatformStaffGrant.ticketRef",
        "PlatformStaffGrant.openedAt",
        "PlatformStaffGrant.expiresAt"
       ],
       "operation": "openPlatformStaffGrant",
       "notes": "**Always visible while the screen acts on a tenant** (decided 28 September, audit R098): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log.",
       "provenance": "contract identity.yaml POST /platform-staff-grants"
      },
      {
       "kind": "primaryButton",
       "label": "Open access grant",
       "operation": "openPlatformStaffGrant",
       "notes": "Shown until a grant into the picked tenant is open; asks for the second factor first (step-up, audit R135).",
       "provenance": "contract identity.yaml POST /platform-staff-grants"
      },
      {
       "kind": "dataTable",
       "label": "Every config version",
       "bindsTo": "ConfigVersion",
       "columns": [
        "ConfigVersion.publishedAt",
        "ConfigVersion.publishedByPrincipalId",
        "ConfigVersion.publishedByName",
        "ConfigVersion.note",
        "ConfigVersion.isCurrent",
        "ConfigVersion.scheduledFor",
        "ConfigVersion.contentHash",
        "ConfigVersion.pendingBuildTimeChanges",
        "ConfigVersion.scopePath"
       ],
       "operation": "listConfigVersions",
       "provenance": "contract white-label.yaml GET /tenant-config/versions"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishTenantConfig",
       "notes": "Declares `publishTenantConfig`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected config version",
       "bindsTo": "ConfigVersion",
       "columns": [
        "ConfigVersion.publishedAt",
        "ConfigVersion.publishedByPrincipalId",
        "ConfigVersion.publishedByName",
        "ConfigVersion.note",
        "ConfigVersion.isCurrent",
        "ConfigVersion.scheduledFor",
        "ConfigVersion.contentHash",
        "ConfigVersion.pendingBuildTimeChanges",
        "ConfigVersion.snapshot",
        "ConfigVersion.scopePath"
       ],
       "operation": "listConfigVersions",
       "provenance": "contract white-label.yaml GET /tenant-config/versions"
      },
      {
       "kind": "detailPanel",
       "label": "The brand identity",
       "bindsTo": "BrandIdentity",
       "columns": [
        "BrandIdentity.logoAssetRef",
        "BrandIdentity.logoDarkAssetRef",
        "BrandIdentity.faviconAssetRef",
        "BrandIdentity.splashImageAssetRefs",
        "BrandIdentity.splashDurationSeconds",
        "BrandIdentity.splashBackgroundColour",
        "BrandIdentity.showLoadingIndicator",
        "BrandIdentity.splashChangeScope"
       ],
       "operation": "getBrandIdentity",
       "provenance": "contract white-label.yaml GET /tenant-config/brand"
      },
      {
       "kind": "detailPanel",
       "label": "The theme",
       "bindsTo": "Theme",
       "columns": [
        "Theme.primaryColour",
        "Theme.secondaryColour",
        "Theme.accentColour",
        "Theme.backgroundColour",
        "Theme.textColour",
        "Theme.darkMode",
        "Theme.cornerRadius"
       ],
       "operation": "getTheme",
       "provenance": "contract white-label.yaml GET /tenant-config/theme"
      },
      {
       "kind": "detailPanel",
       "label": "The app icons",
       "bindsTo": "AppIcons",
       "columns": [
        "AppIcons.sourceAssetRef",
        "AppIcons.derived",
        "AppIcons.changeScope",
        "AppIcons.liveVersion",
        "AppIcons.requiresRebuild"
       ],
       "operation": "getAppIcons",
       "provenance": "contract white-label.yaml GET /tenant-config/app-icons"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create preview",
       "operation": "createPreview",
       "provenance": "contract white-label.yaml POST /tenant-config/preview"
      },
      {
       "kind": "secondaryButton",
       "label": "Diff config version",
       "operation": "diffConfigVersion",
       "provenance": "contract white-label.yaml GET /tenant-config/versions/{version}/diff"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish tenant config",
       "operation": "publishTenantConfig",
       "provenance": "contract white-label.yaml POST /tenant-config/publish"
      },
      {
       "kind": "secondaryButton",
       "label": "Restore config version",
       "operation": "restoreConfigVersion",
       "provenance": "contract white-label.yaml POST /tenant-config/versions/{version}/restore"
      },
      {
       "kind": "secondaryButton",
       "label": "Save app icons",
       "operation": "setAppIcons",
       "provenance": "contract white-label.yaml PUT /tenant-config/app-icons"
      },
      {
       "kind": "secondaryButton",
       "label": "Save brand identity",
       "operation": "setBrandIdentity",
       "provenance": "contract white-label.yaml PUT /tenant-config/brand"
      },
      {
       "kind": "secondaryButton",
       "label": "Save theme",
       "operation": "setTheme",
       "provenance": "contract white-label.yaml PUT /tenant-config/theme"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The white-label branding list.",
   "error": "Could not load. Names which read failed and leaves the white-label branding untouched.",
   "emptyFirstRun": "No white-label branding yet. Offers Create preview (`createPreview`).",
   "emptyNoResults": "Never shown: `listConfigVersions` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `getAppIcons` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "grantRequired": "**No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098)."
  },
  "apis": [
   {
    "operationId": "openPlatformStaffGrant",
    "contract": "identity",
    "purpose": "Open a time-boxed, audited platform-staff grant into the picked tenant before any tenant-scoped operation here; the tenant sees it (decided 28 September, audit R098)",
    "trigger": "onAction"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "The tenant picker — the operator picks a tenant before acting in its cell (audit R098)",
    "trigger": "onLoad"
   },
   {
    "operationId": "createPreview",
    "contract": "white-label",
    "purpose": "Generate a preview link",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   },
   {
    "operationId": "diffConfigVersion",
    "contract": "white-label",
    "purpose": "Compare a version against the working draft",
    "trigger": "onAction"
   },
   {
    "operationId": "getAppIcons",
    "contract": "white-label",
    "purpose": "Read app icon set",
    "trigger": "onLoad"
   },
   {
    "operationId": "getBrandIdentity",
    "contract": "white-label",
    "purpose": "Read brand identity",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTheme",
    "contract": "white-label",
    "purpose": "Read colour theme",
    "trigger": "onLoad"
   },
   {
    "operationId": "listConfigVersions",
    "contract": "white-label",
    "purpose": "Version history",
    "trigger": "onLoad"
   },
   {
    "operationId": "publishTenantConfig",
    "contract": "white-label",
    "purpose": "Publish the working draft",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   },
   {
    "operationId": "restoreConfigVersion",
    "contract": "white-label",
    "purpose": "Restore a previous version",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   },
   {
    "operationId": "setAppIcons",
    "contract": "white-label",
    "purpose": "Set app icons",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   },
   {
    "operationId": "setBrandIdentity",
    "contract": "white-label",
    "purpose": "Set logo, favicon and splash",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   },
   {
    "operationId": "setTheme",
    "contract": "white-label",
    "purpose": "Set colour theme",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "bannerId",
     "from": "deepLink"
    },
    {
     "name": "pageId",
     "from": "deepLink"
    },
    {
     "name": "policyKind",
     "from": "deepLink"
    },
    {
     "name": "version",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `bannerId`, `pageId`, `policyKind`.",
   "preloaded": [
    "ConfigVersion.publishedAt",
    "ConfigVersion.publishedByPrincipalId",
    "ConfigVersion.publishedByName",
    "ConfigVersion.note",
    "ConfigVersion.isCurrent"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-016"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 11 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formOpenPlatformStaffGrant",
    "component": "modal",
    "trigger": "Open access grant",
    "body": "**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client ULID), `permissions` (tenant permissions only — the ones this screen's operations need, preselected), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Open access grant",
     "operation": "openPlatformStaffGrant"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "permissions",
      "reason",
      "ticketRef",
      "expiresAt"
     ]
    },
    "provenance": "contract identity.yaml POST /platform-staff-grants"
   },
   {
    "id": "formCreatePreview",
    "component": "modal",
    "trigger": "Create preview",
    "body": "**Collects what `createPreview` sends before it is called.** Nothing in the body is required. Optional: `platform`, `theme`, `language`, `expiresInHours`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Create preview",
     "operation": "createPreview"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "platform",
      "theme",
      "language",
      "expiresInHours"
     ]
    },
    "provenance": "contract white-label.yaml POST /tenant-config/preview"
   },
   {
    "id": "formPublishTenantConfig",
    "component": "modal",
    "trigger": "Publish tenant config",
    "body": "**Collects what `publishTenantConfig` sends before it is called.** Required: `note`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Publish tenant config",
     "operation": "publishTenantConfig"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "note",
      "scheduledFor"
     ]
    },
    "provenance": "contract white-label.yaml POST /tenant-config/publish"
   },
   {
    "id": "formSetAppIcons",
    "component": "modal",
    "trigger": "Save app icons",
    "body": "**Collects what `setAppIcons` sends before it is called.** Required: `sourceAssetRef`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save app icons",
     "operation": "setAppIcons"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "sourceAssetRef"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/app-icons"
   },
   {
    "id": "formSetBrandIdentity",
    "component": "modal",
    "trigger": "Save brand identity",
    "body": "**Collects what `setBrandIdentity` sends before it is called.** Required: `logoAssetRef`. Optional: `logoDarkAssetRef`, `faviconAssetRef`, `splashImageAssetRefs`, `splashDurationSeconds`, `splashBackgroundColour`, `showLoadingIndicator`, `splashChangeScope`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "BrandIdentity",
    "confirm": {
     "label": "Save brand identity",
     "operation": "setBrandIdentity"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "logoAssetRef",
      "logoDarkAssetRef",
      "faviconAssetRef",
      "splashImageAssetRefs",
      "splashDurationSeconds",
      "splashBackgroundColour",
      "showLoadingIndicator",
      "splashChangeScope"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/brand"
   },
   {
    "id": "formSetTheme",
    "component": "modal",
    "trigger": "Save theme",
    "body": "**Collects what `setTheme` sends before it is called.** Required: `primaryColour`, `secondaryColour`, `backgroundColour`, `textColour`. Optional: `accentColour`, `darkMode`, `cornerRadius`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "Theme",
    "confirm": {
     "label": "Save theme",
     "operation": "setTheme"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "primaryColour",
      "secondaryColour",
      "backgroundColour",
      "textColour",
      "accentColour",
      "darkMode",
      "cornerRadius"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/theme"
   }
  ],
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-017",
  "name": "Domain & Certificate Management",
  "module": "Branding & Localisation",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/domain-and-certificate-management",
   "component": "apps/ticvai-web/src/routes/general/DomainAndCertificateManagementForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-016"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-017 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-017 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-016",
     "trigger": "White-Label Branding Management",
     "provenance": "flow F103 step 1→2",
     "carries": [
      "bannerId",
      "pageId",
      "policyKind",
      "version"
     ]
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **41 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it. **Rebuilt 24 August.** This screen declared 41 operations and **not one was about a domain** — it carried the bulk-attached white-label set, and no domain or certificate operation existed anywhere in the package. **A white-label platform whose tenants cannot use their own domain is white-label in name only.**",
  "openQuestions": [
   "No contract — not specified"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCustomDomains` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "See domain & certificate management for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "selectField",
       "label": "Tenant",
       "bindsTo": "Tenant",
       "columns": [
        "Tenant.id",
        "Tenant.code",
        "Tenant.name",
        "Tenant.status"
       ],
       "operation": "listTenants",
       "notes": "**Pick a tenant first** (decided 28 September, audit R098). This screen's operations run in that tenant's cell, and a platform token carries no tenant permission there until a platform-staff grant into it is open.",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "detailPanel",
       "label": "Open grant into this tenant",
       "bindsTo": "PlatformStaffGrant",
       "columns": [
        "PlatformStaffGrant.id",
        "PlatformStaffGrant.operatorDisplayName",
        "PlatformStaffGrant.permissions",
        "PlatformStaffGrant.reason",
        "PlatformStaffGrant.ticketRef",
        "PlatformStaffGrant.openedAt",
        "PlatformStaffGrant.expiresAt"
       ],
       "operation": "openPlatformStaffGrant",
       "notes": "**Always visible while the screen acts on a tenant** (decided 28 September, audit R098): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log.",
       "provenance": "contract identity.yaml POST /platform-staff-grants"
      },
      {
       "kind": "primaryButton",
       "label": "Open access grant",
       "operation": "openPlatformStaffGrant",
       "notes": "Shown until a grant into the picked tenant is open; asks for the second factor first (step-up, audit R135).",
       "provenance": "contract identity.yaml POST /platform-staff-grants"
      },
      {
       "kind": "dataTable",
       "label": "Every custom domain",
       "bindsTo": "CustomDomain",
       "columns": [
        "CustomDomain.id",
        "CustomDomain.hostname",
        "CustomDomain.kind",
        "CustomDomain.status",
        "CustomDomain.verificationMethod",
        "CustomDomain.verificationToken",
        "CustomDomain.certificateExpiresAt",
        "CustomDomain.lastCheckedAt",
        "CustomDomain.failureReason"
       ],
       "operation": "listCustomDomains",
       "provenance": "contract white-label.yaml GET /tenant-domains"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected custom domain",
       "bindsTo": "CustomDomain",
       "columns": [
        "CustomDomain.id",
        "CustomDomain.hostname",
        "CustomDomain.kind",
        "CustomDomain.status",
        "CustomDomain.verificationMethod",
        "CustomDomain.verificationToken",
        "CustomDomain.certificateExpiresAt",
        "CustomDomain.lastCheckedAt",
        "CustomDomain.failureReason"
       ],
       "operation": "listCustomDomains",
       "provenance": "contract white-label.yaml GET /tenant-domains"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Claim custom domain",
       "operation": "claimCustomDomain",
       "provenance": "contract white-label.yaml POST /tenant-domains"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify custom domain",
       "operation": "verifyCustomDomain",
       "provenance": "contract white-label.yaml POST /tenant-domains/{domainId}/verify"
      },
      {
       "kind": "secondaryButton",
       "label": "Release custom domain",
       "operation": "relinquishCustomDomain",
       "provenance": "contract white-label.yaml DELETE /tenant-domains/{domainId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The domain certificate list.",
   "error": "Could not load. Names which read failed and leaves the domain certificate untouched.",
   "emptyFirstRun": "No domain certificate yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listCustomDomains` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listCustomDomains` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "grantRequired": "**No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098)."
  },
  "apis": [
   {
    "operationId": "openPlatformStaffGrant",
    "contract": "identity",
    "purpose": "Open a time-boxed, audited platform-staff grant into the picked tenant before any tenant-scoped operation here; the tenant sees it (decided 28 September, audit R098)",
    "trigger": "onAction"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "The tenant picker — the operator picks a tenant before acting in its cell (audit R098)",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCustomDomains",
    "contract": "white-label",
    "purpose": "The domains this tenant has claimed",
    "trigger": "onLoad"
   },
   {
    "operationId": "claimCustomDomain",
    "contract": "white-label",
    "purpose": "Claim a domain and get a verification token",
    "trigger": "onAction",
    "invalidates": [
     "listCustomDomains"
    ]
   },
   {
    "operationId": "verifyCustomDomain",
    "contract": "white-label",
    "purpose": "Check the record and issue the certificate",
    "trigger": "onAction",
    "invalidates": [
     "listCustomDomains"
    ]
   },
   {
    "operationId": "relinquishCustomDomain",
    "contract": "white-label",
    "purpose": "Give the domain up",
    "trigger": "onAction",
    "invalidates": [
     "listCustomDomains"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "bannerId",
     "from": "deepLink"
    },
    {
     "name": "pageId",
     "from": "deepLink"
    },
    {
     "name": "policyKind",
     "from": "deepLink"
    },
    {
     "name": "version",
     "from": "deepLink"
    },
    {
     "name": "domainId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `bannerId`, `pageId`, `policyKind`.",
   "preloaded": [
    "CustomDomain.id",
    "CustomDomain.hostname",
    "CustomDomain.kind",
    "CustomDomain.status",
    "CustomDomain.verificationMethod"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-017"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formOpenPlatformStaffGrant",
    "component": "modal",
    "trigger": "Open access grant",
    "body": "**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client ULID), `permissions` (tenant permissions only — the ones this screen's operations need, preselected), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Open access grant",
     "operation": "openPlatformStaffGrant"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "permissions",
      "reason",
      "ticketRef",
      "expiresAt"
     ]
    },
    "provenance": "contract identity.yaml POST /platform-staff-grants"
   },
   {
    "id": "formClaimCustomDomain",
    "component": "modal",
    "trigger": "Claim custom domain",
    "body": "**Collects what `claimCustomDomain` sends before it is called.** Required: `hostname`, `kind`. Optional: `verificationMethod`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Claim custom domain",
     "operation": "claimCustomDomain"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "hostname",
      "kind",
      "verificationMethod"
     ]
    },
    "provenance": "contract white-label.yaml POST /tenant-domains"
   }
  ],
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-018",
  "name": "Localisation & Language Pack",
  "module": "Branding & Localisation",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C57",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/localisation-and-language-pack",
   "component": "apps/ticvai-web/src/routes/general/LocalisationAndLanguagePackDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-018 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-018 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **36 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listFaqs` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Configure localisation & language pack for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "selectField",
       "label": "Tenant",
       "bindsTo": "Tenant",
       "columns": [
        "Tenant.id",
        "Tenant.code",
        "Tenant.name",
        "Tenant.status"
       ],
       "operation": "listTenants",
       "notes": "**Pick a tenant first** (decided 28 September, audit R098). This screen's operations run in that tenant's cell, and a platform token carries no tenant permission there until a platform-staff grant into it is open.",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "detailPanel",
       "label": "Open grant into this tenant",
       "bindsTo": "PlatformStaffGrant",
       "columns": [
        "PlatformStaffGrant.id",
        "PlatformStaffGrant.operatorDisplayName",
        "PlatformStaffGrant.permissions",
        "PlatformStaffGrant.reason",
        "PlatformStaffGrant.ticketRef",
        "PlatformStaffGrant.openedAt",
        "PlatformStaffGrant.expiresAt"
       ],
       "operation": "openPlatformStaffGrant",
       "notes": "**Always visible while the screen acts on a tenant** (decided 28 September, audit R098): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log.",
       "provenance": "contract identity.yaml POST /platform-staff-grants"
      },
      {
       "kind": "primaryButton",
       "label": "Open access grant",
       "operation": "openPlatformStaffGrant",
       "notes": "Shown until a grant into the picked tenant is open; asks for the second factor first (step-up, audit R135).",
       "provenance": "contract identity.yaml POST /platform-staff-grants"
      },
      {
       "kind": "dataTable",
       "label": "Every faq category",
       "bindsTo": "FaqCategory",
       "columns": [
        "FaqCategory.code",
        "FaqCategory.name",
        "FaqCategory.sortOrder",
        "FaqCategory.entries",
        "FaqCategory.scopePath"
       ],
       "operation": "listFaqs",
       "provenance": "contract white-label.yaml GET /tenant-config/faqs"
      },
      {
       "kind": "dataTable",
       "label": "Every policy",
       "bindsTo": "Policy",
       "columns": [
        "Policy.kind",
        "Policy.title",
        "Policy.body",
        "Policy.requiresReconsent",
        "Policy.effectiveFrom",
        "Policy.publishedByPrincipalId",
        "Policy.publishedAt",
        "Policy.scopePath"
       ],
       "operation": "listPolicies",
       "provenance": "contract white-label.yaml GET /tenant-config/policies"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected faq category",
       "bindsTo": "FaqCategory",
       "columns": [
        "FaqCategory.code",
        "FaqCategory.name",
        "FaqCategory.sortOrder",
        "FaqCategory.entries",
        "FaqCategory.scopePath"
       ],
       "operation": "listFaqs",
       "provenance": "contract white-label.yaml GET /tenant-config/faqs"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save languages",
       "operation": "setLanguages",
       "provenance": "contract white-label.yaml PUT /tenant-config/languages"
      },
      {
       "kind": "secondaryButton",
       "label": "Save faqs",
       "operation": "setFaqs",
       "provenance": "contract white-label.yaml PUT /tenant-config/faqs"
      },
      {
       "kind": "secondaryButton",
       "label": "Save policy",
       "operation": "setPolicy",
       "provenance": "contract white-label.yaml PUT /tenant-config/policies/{policyKind}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The localisation language pack list.",
   "error": "Could not load. Names which read failed and leaves the localisation language pack untouched.",
   "emptyFirstRun": "No localisation language pack yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listFaqs` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listFaqs` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "grantRequired": "**No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098)."
  },
  "apis": [
   {
    "operationId": "openPlatformStaffGrant",
    "contract": "identity",
    "purpose": "Open a time-boxed, audited platform-staff grant into the picked tenant before any tenant-scoped operation here; the tenant sees it (decided 28 September, audit R098)",
    "trigger": "onAction"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "The tenant picker — the operator picks a tenant before acting in its cell (audit R098)",
    "trigger": "onLoad"
   },
   {
    "operationId": "setLanguages",
    "contract": "white-label",
    "purpose": "from page inventory",
    "trigger": "onAction"
   },
   {
    "operationId": "listFaqs",
    "contract": "white-label",
    "purpose": "List FAQs",
    "trigger": "onLoad"
   },
   {
    "operationId": "listPolicies",
    "contract": "white-label",
    "purpose": "List legal policies",
    "trigger": "onLoad"
   },
   {
    "operationId": "setFaqs",
    "contract": "white-label",
    "purpose": "Set FAQ categories and entries",
    "trigger": "onAction",
    "invalidates": [
     "listFaqs"
    ]
   },
   {
    "operationId": "setPolicy",
    "contract": "white-label",
    "purpose": "Publish a policy version",
    "trigger": "onAction",
    "invalidates": [
     "listFaqs"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "bannerId",
     "from": "deepLink"
    },
    {
     "name": "pageId",
     "from": "deepLink"
    },
    {
     "name": "policyKind",
     "from": "deepLink"
    },
    {
     "name": "version",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `bannerId`, `pageId`, `policyKind`.",
   "preloaded": [
    "FaqCategory.code",
    "FaqCategory.name",
    "FaqCategory.sortOrder",
    "FaqCategory.entries",
    "FaqCategory.scopePath"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-018"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formOpenPlatformStaffGrant",
    "component": "modal",
    "trigger": "Open access grant",
    "body": "**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client ULID), `permissions` (tenant permissions only — the ones this screen's operations need, preselected), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Open access grant",
     "operation": "openPlatformStaffGrant"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "permissions",
      "reason",
      "ticketRef",
      "expiresAt"
     ]
    },
    "provenance": "contract identity.yaml POST /platform-staff-grants"
   },
   {
    "id": "formSetLanguages",
    "component": "modal",
    "trigger": "Save languages",
    "body": "**Collects what `setLanguages` sends before it is called.** Required: `languages`, `defaultLanguage`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save languages",
     "operation": "setLanguages"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "languages",
      "defaultLanguage"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/languages"
   },
   {
    "id": "formSetFaqs",
    "component": "modal",
    "trigger": "Save faqs",
    "body": "**Collects what `setFaqs` sends before it is called.** Required: `categories`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save faqs",
     "operation": "setFaqs"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "categories"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/faqs"
   },
   {
    "id": "formSetPolicy",
    "component": "modal",
    "trigger": "Save policy",
    "body": "**Collects what `setPolicy` sends before it is called.** Required: `body`, `requiresReconsent`. Optional: `effectiveFrom`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save policy",
     "operation": "setPolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "body",
      "requiresReconsent",
      "effectiveFrom"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/policies/{policyKind}"
   }
  ],
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-019",
  "name": "Global Configuration & Defaults",
  "module": "Branding & Localisation",
  "requiresModule": "membership",
  "wave": 2,
  "capability": "C95",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/global-configuration-and-defaults",
   "component": "apps/ticvai-web/src/routes/general/GlobalConfigurationAndDefaultsForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-019 holds none of them, so the edge carries nothing and ADM-001 opens cold"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-019 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.\n\n**Holds the tenant-level venue defaults (decided 28 September, audit R094).** `getVenueSettingsDefaults` and `setVenueSettingsDefaults` are the tenant row every venue inherits where its own value is null; a venue's own values are set on its venue settings screen. They run in the tenant's cell, so the operator picks a tenant and opens a platform-staff grant first (audit R098).",
  "openQuestions": [
   "No contract — platform defaults not specified"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPlans` reads the population and `getPlan` reads one of them — list, select, act",
  "purpose": "Change how global behaves here, and see which level the current value came from.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "selectField",
       "label": "Tenant",
       "bindsTo": "Tenant",
       "columns": [
        "Tenant.id",
        "Tenant.code",
        "Tenant.name",
        "Tenant.status"
       ],
       "operation": "listTenants",
       "notes": "**Pick a tenant first** (decided 28 September, audit R098). This screen's operations run in that tenant's cell, and a platform token carries no tenant permission there until a platform-staff grant into it is open.",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "detailPanel",
       "label": "Open grant into this tenant",
       "bindsTo": "PlatformStaffGrant",
       "columns": [
        "PlatformStaffGrant.id",
        "PlatformStaffGrant.operatorDisplayName",
        "PlatformStaffGrant.permissions",
        "PlatformStaffGrant.reason",
        "PlatformStaffGrant.ticketRef",
        "PlatformStaffGrant.openedAt",
        "PlatformStaffGrant.expiresAt"
       ],
       "operation": "openPlatformStaffGrant",
       "notes": "**Always visible while the screen acts on a tenant** (decided 28 September, audit R098): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log.",
       "provenance": "contract identity.yaml POST /platform-staff-grants"
      },
      {
       "kind": "primaryButton",
       "label": "Open access grant",
       "operation": "openPlatformStaffGrant",
       "notes": "Shown until a grant into the picked tenant is open; asks for the second factor first (step-up, audit R135).",
       "provenance": "contract identity.yaml POST /platform-staff-grants"
      },
      {
       "kind": "dataTable",
       "label": "Every plan",
       "bindsTo": "Plan",
       "columns": [
        "Plan.code",
        "Plan.name",
        "Plan.description",
        "Plan.cellTier",
        "Plan.licensedModules",
        "Plan.limits",
        "Plan.basePrice",
        "Plan.billingPeriod",
        "Plan.includesBrandedApp",
        "Plan.includedAiTokens",
        "Plan.id",
        "Plan.isActive"
       ],
       "operation": "listPlans",
       "provenance": "contract subscription.yaml GET /plans"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Tenant defaults for every venue",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.cartLeaseSeconds",
        "VenueSettings.cartHoldExtensionMinutes",
        "VenueSettings.cartMaxExtensions",
        "VenueSettings.resaleCutoffHours",
        "VenueSettings.exchangeCutoffHours",
        "VenueSettings.rescheduleCutoffHours",
        "VenueSettings.reservationMaxExtensions",
        "VenueSettings.shiftVarianceThreshold",
        "VenueSettings.quietHours",
        "VenueSettings.displayCurrencies"
       ],
       "operation": "getVenueSettingsDefaults",
       "notes": "**The tenant-level default each venue inherits** (decided 28 September, audit R094). A venue whose own value is null uses the value here; where the tenant has saved nothing these are the proposed defaults, client to correct. The venue facts on the schema (support hours, biometrics, segregated access) are not defaulted here.",
       "provenance": "contract tenancy.yaml GET /venue-settings-defaults"
      },
      {
       "kind": "detailPanel",
       "label": "The selected plan",
       "bindsTo": "Plan",
       "columns": [
        "Plan.code",
        "Plan.name",
        "Plan.description",
        "Plan.cellTier",
        "Plan.licensedModules",
        "Plan.limits",
        "Plan.basePrice",
        "Plan.billingPeriod",
        "Plan.includesBrandedApp",
        "Plan.includedAiTokens",
        "Plan.id",
        "Plan.isActive",
        "Plan.subscriberCount",
        "Plan.publishedAt"
       ],
       "operation": "getPlan",
       "provenance": "contract subscription.yaml GET /plans/{planId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Save venue defaults",
       "operation": "setVenueSettingsDefaults",
       "provenance": "contract tenancy.yaml PUT /venue-settings-defaults"
      },
      {
       "kind": "primaryButton",
       "label": "Create plan",
       "operation": "createPlan",
       "provenance": "contract subscription.yaml POST /plans"
      },
      {
       "kind": "secondaryButton",
       "label": "Create plan version",
       "operation": "createPlanVersion",
       "provenance": "contract subscription.yaml POST /plans/{planId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The global defaults list.",
   "error": "Could not load. Names which read failed and leaves the global defaults untouched.",
   "emptyFirstRun": "No global defaults yet. Offers Create plan (`createPlan`).",
   "emptyNoResults": "Never shown: `listPlans` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listPlans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "grantRequired": "**No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098)."
  },
  "apis": [
   {
    "operationId": "getVenueSettingsDefaults",
    "contract": "tenancy",
    "purpose": "The tenant-level default each venue inherits (decided 28 September, audit R094)",
    "trigger": "onLoad"
   },
   {
    "operationId": "setVenueSettingsDefaults",
    "contract": "tenancy",
    "purpose": "Set the tenant-level venue defaults; venues with their own values are untouched (audit R094)",
    "trigger": "onAction",
    "invalidates": [
     "getVenueSettingsDefaults"
    ]
   },
   {
    "operationId": "openPlatformStaffGrant",
    "contract": "identity",
    "purpose": "Open a time-boxed, audited platform-staff grant into the picked tenant before any tenant-scoped operation here; the tenant sees it (decided 28 September, audit R098)",
    "trigger": "onAction"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "The tenant picker — the operator picks a tenant before acting in its cell (audit R098)",
    "trigger": "onLoad"
   },
   {
    "operationId": "listPlans",
    "contract": "subscription",
    "purpose": "List subscription plans",
    "trigger": "onLoad"
   },
   {
    "operationId": "createPlan",
    "contract": "subscription",
    "purpose": "Create a subscription plan",
    "trigger": "onAction",
    "invalidates": [
     "listPlans"
    ]
   },
   {
    "operationId": "createPlanVersion",
    "contract": "subscription",
    "purpose": "Publish a new version of a plan",
    "trigger": "onAction",
    "invalidates": [
     "listPlans"
    ]
   },
   {
    "operationId": "getPlan",
    "contract": "subscription",
    "purpose": "Read a plan",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "planId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `planId`.",
   "preloaded": [
    "Plan.code",
    "Plan.name",
    "Plan.description",
    "Plan.cellTier",
    "Plan.licensedModules"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-019"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formOpenPlatformStaffGrant",
    "component": "modal",
    "trigger": "Open access grant",
    "body": "**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client ULID), `permissions` (tenant permissions only — the ones this screen's operations need, preselected), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Open access grant",
     "operation": "openPlatformStaffGrant"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "permissions",
      "reason",
      "ticketRef",
      "expiresAt"
     ]
    },
    "provenance": "contract identity.yaml POST /platform-staff-grants"
   },
   {
    "id": "formSetVenueSettingsDefaults",
    "component": "modal",
    "trigger": "Save venue defaults",
    "body": "**Collects what `setVenueSettingsDefaults` sends before it is called** (decided 28 September, audit R094). The whole row is replaced: an omitted limit returns to its proposed default. Each value must sit within its field's minimum and maximum, or the request is refused 400 naming the field. A venue's own values are untouched; a venue with none follows the new default at once. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "VenueSettings",
    "confirm": {
     "label": "Save venue defaults",
     "operation": "setVenueSettingsDefaults"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "cartLeaseSeconds",
      "cartHoldExtensionMinutes",
      "cartMaxExtensions",
      "resaleCutoffHours",
      "exchangeCutoffHours",
      "rescheduleCutoffHours",
      "reservationMaxExtensions",
      "shiftVarianceThreshold",
      "quietHours",
      "displayCurrencies"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /venue-settings-defaults"
   },
   {
    "id": "formCreatePlan",
    "component": "modal",
    "trigger": "Create plan",
    "body": "**Collects what `createPlan` sends before it is called.** Required: `code`, `name`, `cellTier`, `licensedModules`, `limits`, `basePrice`. Optional: `description`, `billingPeriod`, `includesBrandedApp`, `includedAiTokens`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePlanRequest",
    "confirm": {
     "label": "Create plan",
     "operation": "createPlan"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "cellTier",
      "licensedModules",
      "limits",
      "basePrice",
      "description",
      "billingPeriod",
      "includesBrandedApp",
      "includedAiTokens"
     ]
    },
    "provenance": "contract subscription.yaml POST /plans"
   },
   {
    "id": "formCreatePlanVersion",
    "component": "modal",
    "trigger": "Create plan version",
    "body": "**Collects what `createPlanVersion` sends before it is called.** Required: `code`, `name`, `cellTier`, `licensedModules`, `limits`, `basePrice`. Optional: `description`, `billingPeriod`, `includesBrandedApp`, `includedAiTokens`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePlanRequest",
    "confirm": {
     "label": "Create plan version",
     "operation": "createPlanVersion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "cellTier",
      "licensedModules",
      "limits",
      "basePrice",
      "description",
      "billingPeriod",
      "includesBrandedApp",
      "includedAiTokens"
     ]
    },
    "provenance": "contract subscription.yaml POST /plans/{planId}"
   }
  ],
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "claimCustomDomain": {
  "method": "POST",
  "path": "/tenant-domains",
  "contract": "white-label",
  "summary": "Claim a domain and get a verification token",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "CustomDomain"
 },
 "createPlan": {
  "method": "POST",
  "path": "/plans",
  "contract": "subscription",
  "summary": "Create a subscription plan",
  "permission": "PLATFORM_PLAN_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreatePlanRequest",
  "responds": "Plan"
 },
 "createPlanVersion": {
  "method": "POST",
  "path": "/plans/{planId}",
  "contract": "subscription",
  "summary": "Publish a new version of a plan",
  "permission": "PLATFORM_PLAN_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreatePlanRequest",
  "responds": "Plan"
 },
 "createPreview": {
  "method": "POST",
  "path": "/tenant-config/preview",
  "contract": "white-label",
  "summary": "Generate a preview link",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Preview"
 },
 "diffConfigVersion": {
  "method": "GET",
  "path": "/tenant-config/versions/{version}/diff",
  "contract": "white-label",
  "summary": "Compare a version against the working draft",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "against",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ConfigDiff"
 },
 "getAppIcons": {
  "method": "GET",
  "path": "/tenant-config/app-icons",
  "contract": "white-label",
  "summary": "Read app icon set",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "AppIcons"
 },
 "getBrandIdentity": {
  "method": "GET",
  "path": "/tenant-config/brand",
  "contract": "white-label",
  "summary": "Read brand identity",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "BrandIdentity"
 },
 "getPlan": {
  "method": "GET",
  "path": "/plans/{planId}",
  "contract": "subscription",
  "summary": "Read a plan",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Plan"
 },
 "getTheme": {
  "method": "GET",
  "path": "/tenant-config/theme",
  "contract": "white-label",
  "summary": "Read colour theme",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Theme"
 },
 "getVenueSettingsDefaults": {
  "method": "GET",
  "path": "/venue-settings-defaults",
  "contract": "tenancy",
  "summary": "The tenant's default for every venue setting",
  "permission": "TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueSettings"
 },
 "listConfigVersions": {
  "method": "GET",
  "path": "/tenant-config/versions",
  "contract": "white-label",
  "summary": "Version history",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listCustomDomains": {
  "method": "GET",
  "path": "/tenant-domains",
  "contract": "white-label",
  "summary": "The domains this tenant has claimed",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "CustomDomain"
 },
 "listFaqs": {
  "method": "GET",
  "path": "/tenant-config/faqs",
  "contract": "white-label",
  "summary": "List FAQs",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "FaqCategory"
 },
 "listPlans": {
  "method": "GET",
  "path": "/plans",
  "contract": "subscription",
  "summary": "List subscription plans",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "offeredToTenantId",
    "in": "query",
    "required": false
   },
   {
    "name": "packageKind",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "Plan"
 },
 "listPolicies": {
  "method": "GET",
  "path": "/tenant-config/policies",
  "contract": "white-label",
  "summary": "List legal policies",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "includeHistory",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Policy"
 },
 "listTenants": {
  "method": "GET",
  "path": "/tenants",
  "contract": "subscription",
  "summary": "List tenants",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "planId",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "openPlatformStaffGrant": {
  "method": "POST",
  "path": "/platform-staff-grants",
  "contract": "identity",
  "summary": "A platform operator opens a time-boxed grant into this tenant",
  "permission": "PLATFORM_TENANT_ACCESS",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PlatformStaffGrant"
 },
 "publishTenantConfig": {
  "method": "POST",
  "path": "/tenant-config/publish",
  "contract": "white-label",
  "summary": "Publish the working draft",
  "permission": "TENANT_PUBLISH",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ConfigVersion"
 },
 "relinquishCustomDomain": {
  "method": "DELETE",
  "path": "/tenant-domains/{domainId}",
  "contract": "white-label",
  "summary": "Give the domain up",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "restoreConfigVersion": {
  "method": "POST",
  "path": "/tenant-config/versions/{version}/restore",
  "contract": "white-label",
  "summary": "Restore a previous version",
  "permission": "TENANT_PUBLISH",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TenantConfig"
 },
 "setAppIcons": {
  "method": "PUT",
  "path": "/tenant-config/app-icons",
  "contract": "white-label",
  "summary": "Set app icons",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AppIcons"
 },
 "setBrandIdentity": {
  "method": "PUT",
  "path": "/tenant-config/brand",
  "contract": "white-label",
  "summary": "Set logo, favicon and splash",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "BrandIdentity",
  "responds": "BrandIdentity"
 },
 "setFaqs": {
  "method": "PUT",
  "path": "/tenant-config/faqs",
  "contract": "white-label",
  "summary": "Set FAQ categories and entries",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "FaqCategory"
 },
 "setLanguages": {
  "method": "PUT",
  "path": "/tenant-config/languages",
  "contract": "white-label",
  "summary": "Set enabled languages and default",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "LanguageConfig"
 },
 "setPolicy": {
  "method": "PUT",
  "path": "/tenant-config/policies/{policyKind}",
  "contract": "white-label",
  "summary": "Publish a policy version",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Policy"
 },
 "setTheme": {
  "method": "PUT",
  "path": "/tenant-config/theme",
  "contract": "white-label",
  "summary": "Set colour theme",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "Theme",
  "responds": "Theme"
 },
 "setVenueSettingsDefaults": {
  "method": "PUT",
  "path": "/venue-settings-defaults",
  "contract": "tenancy",
  "summary": "Set the tenant's default for every venue setting",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "VenueSettings",
  "responds": "VenueSettings"
 },
 "verifyCustomDomain": {
  "method": "POST",
  "path": "/tenant-domains/{domainId}/verify",
  "contract": "white-label",
  "summary": "Check the record and issue the certificate",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "CustomDomain"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessibilitySettings": {
  "type": "object",
  "description": "BL-065, 2.1.27. **POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated.**\n**A kiosk is the hard case.** A guest with low vision using a website brings their own assistive technology; a guest at a kiosk gets whatever the kiosk offers, so the settings have to be on the device rather than in the browser.\n",
  "properties": {
   "largeTextAvailable": {
    "type": "boolean",
    "default": true
   },
   "highContrastAvailable": {
    "type": "boolean",
    "default": true
   },
   "simplifiedNavigationAvailable": {
    "type": "boolean",
    "default": true
   },
   "screenReaderSupported": {
    "type": "boolean",
    "default": true
   },
   "reachableHeightModeAvailable": {
    "type": "boolean",
    "default": false,
    "description": "**Moves the interface to the lower half of the screen** for a guest using a wheelchair. A kiosk mounted at standing height is unusable otherwise, and no software setting fixes the mounting — this is the mitigation.\n"
   },
   "sessionTimeoutMultiplier": {
    "type": "number",
    "default": 1,
    "description": "**Timeouts are an accessibility barrier nobody counts.** A guest who needs three times as long to read a screen should not lose their basket to a 90-second inactivity timer.\n"
   }
  }
 },
 "AppAvailability": {
  "type": "string",
  "description": "**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n",
  "enum": [
   "open",
   "soldOut",
   "closed"
  ],
  "default": "open"
 },
 "AppIcons": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "sourceAssetRef",
   "changeScope"
  ],
  "properties": {
   "sourceAssetRef": {
    "type": "string",
    "format": "uuid",
    "description": "The `MediaAsset` id of the 1024×1024 source."
   },
   "derived": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on `setAppIcons` (audit R163).",
    "items": {
     "type": "object",
     "properties": {
      "platform": {
       "type": "string",
       "enum": [
        "ios",
        "android",
        "web"
       ]
      },
      "size": {
       "type": "string"
      },
      "assetRef": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Always `buildTime` — icons are baked into the binary."
   },
   "liveVersion": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Icon currently shipped. Differs from the draft until the next release."
   },
   "requiresRebuild": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "True while the draft's source differs from the icon in `liveVersion`."
   }
  }
 },
 "BookingFlow": {
  "x-ticvai-persistence": "whitelabel.booking_flow",
  "type": "object",
  "description": "**A venue's booking flow (decided 29 September, W12: operators pick their flows, see which steps are required, set their own order).** Made from a `BookingFlowType`; lives in the working draft and reaches guests with `publishTenantConfig`, which copies the venue's flows into the version's snapshot. A product or category names its flow (catalogue `bookingFlowId`); otherwise the venue's default for the type serving its kind applies.\n",
  "required": [
   "flowTypeKey",
   "name"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of `createBookingFlowDefinition`."
   },
   "flowTypeKey": {
    "$ref": "#/components/schemas/BookingFlowTypeKey"
   },
   "name": {
    "type": "string",
    "maxLength": 80,
    "description": "Staff-facing, e.g. \"Day pass, date first\". Not shown to guests."
   },
   "isDefaultForType": {
    "type": "boolean",
    "default": false,
    "description": "At most one per venue and type; setting it takes it from the previous default."
   },
   "isEnabled": {
    "type": "boolean",
    "default": true,
    "description": "A disabled flow is kept and not published; products naming it fall back to the default."
   },
   "steps": {
    "type": "array",
    "maxItems": 30,
    "description": "Every step of the type, in the venue's order. Filled from the type when left out on create.",
    "items": {
     "$ref": "#/components/schemas/BookingFlowStep"
    }
   },
   "settings": {
    "$ref": "#/components/schemas/BookingFlowLevelSettings"
   },
   "isValid": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. `publishTenantConfig` refuses a draft holding an invalid enabled flow."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The partition key (ADR-0005). Written at `venue` scope."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "BookingFlowConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "description": "**Set per tenant, with a per-venue override (decided 29 September, rev 3 CFG-11).** One tenant with several venues (the Kids Club branches, Coastal Aqua beside Union Arena) needs them to differ. The settings in force at a venue are the tenant's, with that venue's entry in `venueOverrides` laid over them field by field. The guest app resolves them for the venue the guest picked (audit R267); `effectiveForVenueId` on `getBookingFlowConfig` returns them resolved.\n",
  "allOf": [
   {
    "$ref": "#/components/schemas/BookingFlowSettings"
   },
   {
    "type": "object",
    "properties": {
     "venueOverrides": {
      "type": "array",
      "maxItems": 200,
      "default": [],
      "description": "Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. An override for a venue later closed is kept and has no effect.",
      "items": {
       "$ref": "#/components/schemas/BookingFlowVenueOverride"
      }
     }
    }
   }
  ]
 },
 "BrandIdentity": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "description": "Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB (decided 28 September, audit R270).\n",
  "required": [
   "logoAssetRef"
  ],
  "properties": {
   "logoAssetRef": {
    "type": "string",
    "format": "uuid",
    "description": "The primary logo."
   },
   "logoDarkAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Used on dark backgrounds. Falls back to the primary logo."
   },
   "logoVariant": {
    "type": "string",
    "enum": [
     "light",
     "dark",
     "duotone"
    ],
    "default": "light",
    "description": "**Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4).** `light` uses `logoAssetRef`, `dark` uses `logoDarkAssetRef` (falling back to the primary logo), and `duotone` the two-colour reading of the primary logo.\n"
   },
   "faviconAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The browser tab icon for the guest web app."
   },
   "splashImageAssetRefs": {
    "type": "array",
    "description": "Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163).",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "splashDurationSeconds": {
    "type": "integer",
    "minimum": 0,
    "maximum": 10,
    "default": 3
   },
   "splashBackgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "showLoadingIndicator": {
    "type": "boolean",
    "default": true
   },
   "splashChangeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163)."
   },
   "introVideoAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The optional intro video (decided 29 September, MOB-5).** A video `MediaAsset` from the media library (CMS-010). Streamed, so a change reaches guests with the publish and needs no app build.\n"
   },
   "introVideoMode": {
    "type": "string",
    "enum": [
     "off",
     "firstLaunch",
     "everyLaunch"
    ],
    "default": "off",
    "description": "When GST-001 plays it full screen. \"Skip introduction\" is always shown. Anything but `off` needs `introVideoAssetRef`, or 400."
   }
  }
 },
 "CellTier": {
  "type": "string",
  "enum": [
   "shared",
   "dedicated",
   "isolated",
   "clientHosted"
  ]
 },
 "ChangeScope": {
  "type": "string",
  "description": "Whether a change reaches guests on publish or needs a store release.\n",
  "enum": [
   "runtime",
   "buildTime"
  ]
 },
 "ConfigDiff": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "fromVersion",
   "toVersion",
   "changes"
  ],
  "properties": {
   "fromVersion": {
    "type": "string"
   },
   "toVersion": {
    "type": "string"
   },
   "changes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "area",
      "path",
      "changeKind"
     ],
     "properties": {
      "area": {
       "type": "string"
      },
      "path": {
       "type": "string"
      },
      "changeKind": {
       "type": "string",
       "enum": [
        "added",
        "removed",
        "modified"
       ]
      },
      "before": {
       "type": "string",
       "nullable": true
      },
      "after": {
       "type": "string",
       "nullable": true
      },
      "changeScope": {
       "$ref": "#/components/schemas/ChangeScope"
      }
     }
    }
   }
  }
 },
 "ConfigVersion": {
  "x-ticvai-persistence": "whitelabel.config_version",
  "type": "object",
  "required": [
   "version",
   "publishedAt",
   "publishedByPrincipalId",
   "note",
   "isCurrent"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedByName": {
    "type": "string"
   },
   "note": {
    "type": "string"
   },
   "isCurrent": {
    "type": "boolean"
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "contentHash": {
    "type": "string"
   },
   "pendingBuildTimeChanges": {
    "type": "array",
    "description": "Changes in this version that will not reach guests until the next store release. Surfaced at publish so nobody expects a new icon tomorrow.\n",
    "items": {
     "type": "object",
     "properties": {
      "area": {
       "type": "string"
      },
      "description": {
       "type": "string"
      },
      "platforms": {
       "type": "array",
       "items": {
        "type": "string",
        "enum": [
         "ios",
         "android",
         "web"
        ]
       }
      }
     }
    }
   },
   "snapshot": {
    "type": "object",
    "additionalProperties": true,
    "readOnly": true,
    "description": "**What this version contained.** The working draft exactly as published, in the shape `getTenantConfig` returns (`TenantConfig`) — so `restoreConfigVersion` has something to copy back and `diffConfigVersion` something to compare. Deliberately an open object here: its shape is `TenantConfig`, and a `$ref` would make it a key to a `tenant_config` row rather than a copy. Written once by `publishTenantConfig` and never changed. Left out of `listConfigVersions` items; a version's content is read with `getTenantConfig?version=`.\n"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "CreatePlanRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "cellTier",
   "licensedModules",
   "limits",
   "basePrice"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "cellTier": {
    "$ref": "#/components/schemas/CellTier"
   },
   "licensedModules": {
    "type": "array",
    "minItems": 1,
    "description": "**A closed set as of 24 August.** `moduleKey` was a free string, so nothing could join a licence to a screen — **a tenant without an F&B licence was still served every F&B screen**, because no screen said which module it belonged to in a form the licence could match.\n**The key is the join.** `screen.requiresModule` names one of these, and navigation is built from the intersection of what a tenant licensed and what their role permits.\n",
    "items": {
     "$ref": "#/components/schemas/ModuleKey"
    }
   },
   "limits": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/EntitlementLimit"
    }
   },
   "basePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "billingPeriod": {
    "type": "string",
    "enum": [
     "monthly",
     "quarterly",
     "annual"
    ]
   },
   "includesBrandedApp": {
    "type": "boolean",
    "description": "Branded native publishing carries per-tenant operational cost and is priced, not absorbed.\n"
   },
   "includedAiTokens": {
    "type": "integer",
    "nullable": true,
    "description": "AI tokens the package includes per billing period. Usage beyond it is a `metered` invoice line at the AI module's price (decided 29 September)."
   },
   "packageKind": {
    "type": "string",
    "enum": [
     "standard",
     "custom"
    ],
    "default": "standard",
    "description": "**Three standard packages, and custom ones allowed** (decided 29 September, Chinmay)."
   },
   "offeredToTenantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Private to one tenant** (decided 29 September, Chinmay): a custom package offered only to this tenant; `listPlans` shows it to no other tenant and `setSubscription` refuses it for any other (422 `plan-not-offered`). Null for a package any tenant may buy. Custom packages only."
   }
  }
 },
 "CustomDomain": {
  "type": "object",
  "x-ticvai-persistence": "whitelabel.custom_domain",
  "description": "24 August. **`ADM-017 Domain & Certificate Management` declared 41 operations and not one of them was about a domain** — it carried the same bulk-attached set as every other white-label screen, and **no domain or certificate operation existed anywhere in 1,010.**\nA white-label platform whose tenants cannot use their own domain is a white-label platform in name only.\n**Verification before issuance, always.** A certificate issued for a domain the tenant does not control is a certificate issued to whoever asked.\n",
  "required": [
   "id",
   "tenantId",
   "hostname",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "hostname": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "guestWeb",
     "guestApp",
     "partnerPortal",
     "developerPortal"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "verifying",
     "verified",
     "issuing",
     "active",
     "failed",
     "expired",
     "revoked"
    ]
   },
   "verificationMethod": {
    "type": "string",
    "enum": [
     "dnsTxt",
     "cname",
     "httpFile"
    ]
   },
   "verificationToken": {
    "type": "string",
    "readOnly": true
   },
   "verificationRecord": {
    "type": "object",
    "readOnly": true,
    "description": "**The record the tenant must publish**, which `claimCustomDomain` promises and the claim had nowhere to hold. Set when the claim is made, from `hostname`, `verificationMethod` and `verificationToken`: a TXT record for `dnsTxt`, a CNAME for `cname`, and for `httpFile` the URL path to serve and the file's content.\n",
    "required": [
     "type",
     "name",
     "value"
    ],
    "properties": {
     "type": {
      "type": "string",
      "enum": [
       "TXT",
       "CNAME",
       "httpFile"
      ]
     },
     "name": {
      "type": "string",
      "description": "The DNS name to create, or for `httpFile` the URL path on `hostname`."
     },
     "value": {
      "type": "string",
      "description": "The record's value, CNAME target or file content."
     }
    }
   },
   "certificateExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Renewal is a job, not a reminder.** A certificate that expires on a Saturday takes a tenant's storefront down, and nobody reads a reminder email on a Saturday.\n"
   },
   "lastCheckedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "failureReason": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "EntitlementLimit": {
  "type": "object",
  "required": [
   "metric",
   "limit"
  ],
  "properties": {
   "metric": {
    "$ref": "#/components/schemas/UsageMetric"
   },
   "limit": {
    "type": "integer",
    "nullable": true,
    "x-ticvai-column": "limit_value",
    "description": "Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure `limit_value`."
   },
   "overageAllowed": {
    "type": "boolean",
    "default": false
   },
   "overageUnitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "FaqCategory": {
  "x-ticvai-persistence": "whitelabel.faq_category + whitelabel.faq_entry",
  "type": "object",
  "required": [
   "code",
   "name",
   "entries"
  ],
  "properties": {
   "code": {
    "type": "string"
   },
   "name": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "sortOrder": {
    "type": "integer"
   },
   "entries": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "id",
      "question",
      "answer"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "question": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "answer": {
       "$ref": "#/components/schemas/LocalisedRichText"
      },
      "sortOrder": {
       "type": "integer"
      },
      "isPublished": {
       "type": "boolean"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "FeatureToggle": {
  "x-ticvai-persistence": "whitelabel.feature_toggle",
  "type": "object",
  "required": [
   "featureKey",
   "isEnabled",
   "changeScope"
  ],
  "properties": {
   "featureKey": {
    "allOf": [
     {
      "$ref": "#/components/schemas/FeatureKey"
     }
    ],
    "description": "`guestCheckout` is **off by default** (decided 17 September 2026, matrix 2.6.28, placement settled by [ADR-0045](../../docs/adr/0045-every-order-carries-a-proven-contact.md) 18 September): **the venue sets this from the configuration menu**, and it decides which routes the checkout page offers — off, the guest signs in verified at checkout; on, a guest may also check out without an account after proving their contact with a one-time code. **It gates checkout, never the cart.** The kiosk is not governed by it. Rule on `identity` `verifyGuestEmail`.\n"
   },
   "displayName": {
    "type": "string"
   },
   "isEnabled": {
    "type": "boolean"
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Wallet and payment integrations are `buildTime` on native apps — enabling one needs a release, not a publish.\n"
   },
   "requiresConfiguration": {
    "type": "boolean",
    "description": "True where the feature needs credentials or setup elsewhere first."
   }
  }
 },
 "FontConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "primaryLatin"
  ],
  "properties": {
   "primaryLatin": {
    "type": "string"
   },
   "primaryArabic": {
    "type": "string",
    "nullable": true,
    "description": "Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match.\n"
   },
   "secondaryLatin": {
    "type": "string",
    "nullable": true
   },
   "secondaryArabic": {
    "type": "string",
    "nullable": true,
    "description": "Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163)."
   },
   "customFontAssetRefs": {
    "type": "array",
    "description": "Uploaded font files, as `MediaAsset` ids.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "Custom font files are `buildTime`; selecting a bundled face is `runtime`."
   }
  }
 },
 "FooterConfig": {
  "type": "object",
  "x-ticvai-persistence": "whitelabel.footer_config + whitelabel.footer_config_column + whitelabel.footer_config_social_link",
  "description": "BL-002. **`setHeader` and `HeaderConfig` exist and the footer does not**, which looked like symmetry until you notice it is not: **a header is chrome and a footer is a link surface.**\nA footer carries the legal links — terms, privacy, accessibility statement, cookie preferences — and **those are the ones a regulator checks.** Treating it as a mirror of the header would have given it a logo and no way to reach a privacy notice.\n**Where it is stored.** `legalLinks` and `copyrightText` are columns of `whitelabel.footer_config`; each entry of `columns` is a `whitelabel.footer_config_column` row and each entry of `socialLinks` a `whitelabel.footer_config_social_link` row. Part of the working draft (see the header). **In the tenant's own database, not the control plane (decided 28 September, audit R163)**: it moved from `control.footer_config` and its two child tables.\n",
  "required": [
   "id",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The partition key (ADR-0005), written at `tenant` scope by the server."
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "heading": {
       "type": "string"
      },
      "links": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "label": {
          "type": "string"
         },
         "url": {
          "type": "string"
         },
         "opensCookiePreferences": {
          "type": "boolean",
          "default": false
         }
        }
       }
      }
     }
    }
   },
   "legalLinks": {
    "type": "object",
    "description": "**Required links, held separately from the free-form columns** — a tenant reorganising their footer must not be able to remove the privacy notice by accident.\n",
    "properties": {
     "termsUrl": {
      "type": "string"
     },
     "privacyUrl": {
      "type": "string"
     },
     "accessibilityUrl": {
      "type": "string",
      "nullable": true
     },
     "cookiePolicyUrl": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "copyrightText": {
    "type": "string"
   },
   "socialLinks": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "platform": {
       "type": "string"
      },
      "url": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "HeaderConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "layout"
  ],
  "properties": {
   "layout": {
    "type": "string",
    "enum": [
     "logoLeft",
     "logoCentre",
     "logoWithMenu"
    ]
   },
   "showLogo": {
    "type": "boolean",
    "default": true
   },
   "showMenu": {
    "type": "boolean",
    "default": true
   },
   "showNotifications": {
    "type": "boolean",
    "default": true
   },
   "backgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   }
  }
 },
 "HomepageLayout": {
  "x-ticvai-persistence": "whitelabel.homepage_section",
  "type": "object",
  "required": [
   "sections"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "sections": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "sortOrder",
      "isVisible"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true,
       "description": "**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"
      },
      "kind": {
       "$ref": "#/components/schemas/HomepageSectionKind"
      },
      "title": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "sortOrder": {
       "type": "integer"
      },
      "isVisible": {
       "type": "boolean"
      },
      "contentPageId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "maxItems": {
       "type": "integer",
       "nullable": true,
       "description": "How many items the section shows. On the mobile Home, `attractions`, `dining`, `whatsOn` and `shop` show 1 or 2 highlights (decided 29 September, MOB-3)."
      },
      "heroStyle": {
       "type": "string",
       "nullable": true,
       "enum": [
        "carousel",
        "video",
        "poster",
        "split",
        null
       ],
       "description": "For `heroBanner` only (decided 29 September, MOB-3)."
      }
     }
    }
   }
  }
 },
 "LanguageConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "languages",
   "defaultLanguage"
  ],
  "properties": {
   "languages": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[a-z]{2}$"
    }
   },
   "defaultLanguage": {
    "type": "string",
    "pattern": "^[a-z]{2}$"
   },
   "rtlLanguages": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "The enabled languages written right to left — those whose Unicode CLDR character order is `right-to-left` (Arabic, `ar`, among them). Not configured; it follows from `languages`.",
    "items": {
     "type": "string",
     "pattern": "^[a-z]{2}$"
    }
   },
   "translationGaps": {
    "type": "array",
    "readOnly": true,
    "description": "Content lacking a version in an enabled language.",
    "items": {
     "type": "object",
     "properties": {
      "language": {
       "type": "string"
      },
      "missingCount": {
       "type": "integer"
      },
      "areas": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
   }
  }
 },
 "LocalisedRichText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "description": "Keyed by language code. Values are sanitised HTML.",
  "additionalProperties": {
   "type": "string"
  }
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "MinimumAppVersion": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "nullable": true,
  "description": "**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n",
  "properties": {
   "ios": {
    "type": "string",
    "nullable": true,
    "pattern": "^\\d+\\.\\d+\\.\\d+$"
   },
   "android": {
    "type": "string",
    "nullable": true,
    "pattern": "^\\d+\\.\\d+\\.\\d+$"
   }
  }
 },
 "ModuleEnablement": {
  "x-ticvai-persistence": "whitelabel.module_enablement",
  "type": "object",
  "required": [
   "moduleKey",
   "isLicensed",
   "isEnabled"
  ],
  "properties": {
   "moduleKey": {
    "$ref": "#/components/schemas/ModuleKey"
   },
   "displayName": {
    "type": "string"
   },
   "isLicensed": {
    "type": "boolean",
    "description": "From the tenant's subscription. False makes enablement impossible."
   },
   "isEnabled": {
    "type": "boolean"
   },
   "referencedBy": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Navigation items and homepage sections pointing at this module. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write.",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "ModuleKey": {
  "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
 },
 "NavigationConfig": {
  "x-ticvai-persistence": "whitelabel.navigation_item",
  "type": "object",
  "description": "**The mobile tab set is venue configuration (decided 29 September, MOB-1; 29 September brief decision 6).** Before a tenant saves its own, `bottomNavigation` is Home, Explore, Plan and Tickets (each an `appSection` link), with the Buy tickets button beside them; Map is an optional tab. Plan is left out while `visitPlanner` is off.\n",
  "required": [
   "kind",
   "items"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "kind": {
    "type": "string",
    "enum": [
     "bottomNavigation",
     "drawer",
     "tabs"
    ]
   },
   "items": {
    "type": "array",
    "maxItems": 12,
    "items": {
     "type": "object",
     "required": [
      "label",
      "target",
      "isVisible",
      "sortOrder"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true,
       "description": "**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"
      },
      "label": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "icon": {
       "type": "string"
      },
      "target": {
       "$ref": "#/components/schemas/LinkTarget"
      },
      "isVisible": {
       "type": "boolean",
       "description": "At most five may be visible in bottom navigation; the rest overflow."
      },
      "sortOrder": {
       "type": "integer"
      }
     }
    }
   },
   "buyButton": {
    "type": "object",
    "nullable": true,
    "description": "**The persistent Buy tickets button (decided 29 September, MOB-2).** On every screen of the mobile app except the booking and checkout steps; it opens GST-003. Read with `bottomNavigation`.\n",
    "properties": {
     "style": {
      "type": "string",
      "enum": [
       "raised",
       "floating",
       "flat",
       "hidden"
      ],
      "default": "raised",
      "description": "`raised` sits in the centre of the tab bar, as the v4 prototype shows; `hidden` turns it off."
     },
     "label": {
      "$ref": "#/components/schemas/LocalisedText"
     }
    }
   }
  }
 },
 "Page": {
  "type": "object",
  "required": [
   "items",
   "hasMore"
  ],
  "properties": {
   "items": {
    "type": "array",
    "items": {}
   },
   "nextCursor": {
    "type": "string"
   },
   "hasMore": {
    "type": "boolean"
   }
  }
 },
 "Permission": {
  "type": "string",
  "enum": [
   "SESSION_FORCE_LOGOUT",
   "USER_MANAGE",
   "ROLE_MANAGE",
   "PERMISSION_GRANT",
   "PERMISSION_VIEW",
   "PERMISSION_MANAGE",
   "PLATFORM_TENANT_VIEW",
   "PLATFORM_TENANT_MANAGE",
   "PLATFORM_TENANT_TERMINATE",
   "PLATFORM_PLAN_MANAGE",
   "PLATFORM_CELL_VIEW",
   "PLATFORM_CELL_MANAGE",
   "PLATFORM_BILLING_VIEW",
   "PLATFORM_AI_MANAGE",
   "PLATFORM_BILLING_MANAGE",
   "PLATFORM_RELEASE_VIEW",
   "PLATFORM_RELEASE_MANAGE",
   "PLATFORM_RELEASE_PROMOTE",
   "PLATFORM_MIGRATION_VIEW",
   "PLATFORM_MIGRATION_APPLY",
   "PLATFORM_TENANT_ACCESS",
   "TENANT_CONFIGURE",
   "TENANT_VIEW",
   "TENANT_PUBLISH",
   "SCOPE_VIEW",
   "SCOPE_MANAGE",
   "REGION_CONFIGURE",
   "WORKSTATION_CONFIGURE",
   "PRODUCT_VIEW",
   "PRODUCT_CONFIGURE",
   "PRODUCT_APPROVE",
   "PRODUCT_PUBLISH",
   "PRICE_VIEW",
   "PRICE_CONFIGURE",
   "EVENT_CONFIGURE",
   "PERFORMANCE_CONFIGURE",
   "CAPACITY_CONFIGURE",
   "ORDER_VIEW",
   "ORDER_VIEW_OTHER",
   "ORDER_CREATE",
   "ORDER_MODIFY",
   "ORDER_DISCOUNT",
   "ORDER_CANCEL",
   "ORDER_VOID",
   "ORDER_REFUND",
   "ORDER_REFUND_APPROVE",
   "ORDER_REFUND_BULK",
   "ORDER_EXCHANGE",
   "ORDER_RESCHEDULE",
   "ORDER_REPRINT",
   "PRICE_OVERRIDE",
   "DISCOUNT_APPLY",
   "CREDIT_MANAGE",
   "CREDIT_OVERRIDE",
   "WALLET_VIEW",
   "WALLET_OPERATE",
   "WALLET_CONFIGURE",
   "PAYMENT_VIEW",
   "PAYMENT_CONFIGURE",
   "PAYMENT_PROVIDER_MANAGE",
   "PAYMENT_DISPUTE",
   "SHIFT_OPEN",
   "SHIFT_CLOSE",
   "SHIFT_SUSPEND",
   "SHIFT_CLOSE_OTHER",
   "SHIFT_APPROVE_OPEN",
   "SHIFT_APPROVE_CLOSE",
   "SHIFT_REOPEN",
   "CASH_LIFT",
   "CASH_ADD",
   "CASH_NO_SALE",
   "DEPOSIT_BOX_MODIFY_OWN",
   "DEPOSIT_BOX_MODIFY_OTHER",
   "OVERSHORT_ACCEPT",
   "ACCESS_VALIDATE",
   "ACCESS_OVERRIDE",
   "ACCESS_POINT_CONFIGURE",
   "TURNSTILE_MODE_SET",
   "TICKET_LOOKUP",
   "ACCREDITATION_VIEW",
   "ACCREDITATION_APPLY",
   "ACCREDITATION_APPROVE",
   "ACCREDITATION_ISSUE",
   "ACCREDITATION_MANAGE",
   "ACCREDITATION_CONFIGURE",
   "REPORT_VIEW_OWN",
   "REPORT_VIEW_WORKSTATION",
   "REPORT_VIEW_VENUE",
   "REPORT_VIEW_REGION",
   "REPORT_VIEW_TENANT",
   "REPORT_EXPORT",
   "REPORT_EXPORT_PII",
   "REPORT_MANAGE",
   "REPORT_SCHEDULE",
   "LEDGER_VIEW",
   "LEDGER_POST",
   "LEDGER_APPROVE",
   "TAX_CONFIGURE",
   "ACCOUNT_CONFIGURE",
   "SETTLEMENT_VIEW",
   "SETTLEMENT_RECONCILE",
   "GUEST_VIEW",
   "GUEST_VIEW_PII",
   "GUEST_MANAGE",
   "VENUE_MAP_VIEW",
   "VENUE_MAP_MANAGE",
   "VENUE_MAP_PUBLISH",
   "RESOURCE_VIEW",
   "RESOURCE_BOOK",
   "RESOURCE_MANAGE",
   "RESOURCE_CONFIGURE",
   "RENTAL_VIEW",
   "RENTAL_BOOK",
   "RENTAL_OPERATE",
   "RENTAL_MANAGE",
   "RENTAL_CONFIGURE",
   "RENTAL_PRICE",
   "RENTAL_APPROVE",
   "RENTAL_OVERRIDE",
   "DEVELOPER_VIEW",
   "DEVELOPER_MANAGE",
   "DEVELOPER_ADMIN",
   "LOYALTY_ACCRUE",
   "LOYALTY_REDEEM",
   "LOYALTY_ADJUST",
   "MARKETING_VIEW",
   "MARKETING_MANAGE",
   "MARKETING_SEND",
   "CASE_VIEW",
   "CASE_MANAGE",
   "ASSET_LIBRARY_VIEW",
   "ASSET_LIBRARY_MANAGE",
   "ASSET_LIBRARY_APPROVE",
   "ASSET_LIBRARY_SHARE",
   "QUEUE_VIEW",
   "QUEUE_MANAGE",
   "QUEUE_REDEEM",
   "QUEUE_OVERRIDE",
   "TRANSPORT_VIEW",
   "TRANSPORT_MANAGE",
   "TRANSPORT_PRICE",
   "ASSET_VIEW",
   "ASSET_MANAGE",
   "WORK_ORDER_VIEW",
   "WORK_ORDER_MANAGE",
   "WORK_ORDER_VERIFY",
   "INSPECTION_VIEW",
   "INSPECTION_SUBMIT",
   "INSPECTION_MANAGE",
   "INCIDENT_REPORT",
   "INCIDENT_VIEW",
   "INCIDENT_MANAGE",
   "KIOSK_ATTEND",
   "DEVICE_VIEW",
   "DEVICE_CONFIGURE",
   "DEVICE_MANAGE",
   "APPROVAL_ACT",
   "APPROVAL_DELEGATE",
   "AI_USE",
   "AI_CONFIGURE",
   "AI_APPROVE",
   "AI_AUDIT_VIEW",
   "RISK_REVIEW",
   "RISK_INVESTIGATE",
   "AUDIT_VIEW",
   "APPROVAL_VIEW",
   "APPROVAL_REQUEST",
   "APPROVAL_DECIDE",
   "APPROVAL_CONFIGURE",
   "MAINTENANCE_EXECUTE",
   "MAINTENANCE_APPROVE",
   "WORKFORCE_VIEW",
   "WORKFORCE_MANAGE",
   "ATTENDANCE_RECORD",
   "ANNOUNCEMENT_PUBLISH",
   "ANNOUNCEMENT_EMERGENCY",
   "PARTNER_VIEW",
   "PARTNER_MANAGE",
   "PARKING_CONFIGURE",
   "PAYMENT_VOID",
   "PROCUREMENT_VIEW",
   "PROCUREMENT_REQUEST",
   "PROCUREMENT_MANAGE",
   "PROCUREMENT_RECEIVE"
  ]
 },
 "Plan": {
  "x-ticvai-persistence": "subscription.plan + subscription.plan_module + subscription.plan_limit",
  "description": "**A plan's modules and limits are rows, keyed on `plan_id`.** `licensedModules` and `limits` are required on every plan, and `subscription.plan` alone had no column for either — so the licence position, the downgrade check and every module gate had nothing to read. `plan_module` holds one row per licensed `ModuleKey`; `plan_limit` one row per `EntitlementLimit`. Both belong to the plan version the row is, so a subscriber on an earlier version keeps the modules and limits they were sold.",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreatePlanRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "version",
     "isActive",
     "subscriberCount"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "version": {
      "type": "string",
      "description": "Existing subscribers stay on the version they were sold. A price change never applies retroactively.\n"
     },
     "isActive": {
      "type": "boolean"
     },
     "subscriberCount": {
      "type": "integer"
     },
     "publishedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "PlatformStaffGrant": {
  "type": "object",
  "x-ticvai-persistence": "identity.platform_staff_grant",
  "description": "**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n",
  "required": [
   "id",
   "operatorPrincipalId",
   "permissions",
   "reason",
   "openedAt",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "operatorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The platform operator, from the Control Plane token. Set by the server."
   },
   "operatorDisplayName": {
    "type": "string",
    "readOnly": true
   },
   "permissions": {
    "type": "array",
    "items": {
     "$ref": "../shared/permissions.yaml#/components/schemas/Permission"
    }
   },
   "reason": {
    "type": "string"
   },
   "ticketRef": {
    "type": "string",
    "nullable": true
   },
   "openedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The tenant root. **Operations write it at `tenant` scope**; the server sets it."
   }
  }
 },
 "Policy": {
  "x-ticvai-persistence": "whitelabel.policy",
  "type": "object",
  "required": [
   "kind",
   "version",
   "body",
   "effectiveFrom",
   "publishedAt"
  ],
  "properties": {
   "kind": {
    "$ref": "#/components/schemas/PolicyKind"
   },
   "title": {
    "type": "string",
    "description": "The heading a guest sees, and the field a refund question retrieves against.\n"
   },
   "version": {
    "type": "string",
    "description": "Immutable. A guest who consented to version 3 consented to version 3, and a policy that changes under a recorded consent is a compliance failure.\n"
   },
   "body": {
    "$ref": "#/components/schemas/LocalisedRichText"
   },
   "requiresReconsent": {
    "type": "boolean"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date"
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "PolicyKind": {
  "type": "string",
  "enum": [
   "privacy",
   "termsAndConditions",
   "refund",
   "cookie",
   "accessibility"
  ]
 },
 "Preview": {
  "x-ticvai-persistence": "none — short-lived, cache only",
  "type": "object",
  "required": [
   "previewId",
   "url",
   "expiresAt"
  ],
  "properties": {
   "previewId": {
    "type": "string",
    "format": "uuid"
   },
   "url": {
    "type": "string"
   },
   "platform": {
    "type": "string",
    "enum": [
     "ios",
     "android",
     "web"
    ]
   },
   "theme": {
    "type": "string",
    "enum": [
     "light",
     "dark"
    ]
   },
   "language": {
    "type": "string",
    "pattern": "^[a-z]{2}$"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "SuspensionMode": {
  "type": "string",
  "description": "Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n",
  "enum": [
   "readOnly",
   "noNewSales",
   "fullLockout"
  ]
 },
 "Tenant": {
  "x-ticvai-persistence": "control.tenant",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/TenantStatus"
   },
   "suspensionMode": {
    "$ref": "#/components/schemas/SuspensionMode"
   },
   "suspensionReason": {
    "type": "string",
    "nullable": true
   },
   "suspensionEffectiveAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."
   },
   "suspensionNoticeMessage": {
    "$ref": "#/components/schemas/LocalisedText",
    "description": "The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."
   },
   "terminationScheduledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When `terminateTenant` started the retention window. Null when no termination is under way."
   },
   "terminationRetentionUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."
   },
   "terminationReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "terminationRequestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "planName": {
    "type": "string",
    "nullable": true
   },
   "cellCount": {
    "type": "integer"
   },
   "venueCount": {
    "type": "integer"
   },
   "regionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"
   },
   "billingEmail": {
    "type": "string"
   },
   "billingAddress": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."
   },
   "accountManagerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "activatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "TenantConfig": {
  "x-ticvai-persistence": "whitelabel.tenant_config",
  "type": "object",
  "description": "**The tenant's working draft**, one row per tenant (see the header). Published versions are `ConfigVersion.snapshot`, not further rows here.\n**Only `tenantId` and `version` are required**, because the draft is built one part at a time: the first `set*` call creates the row with that part alone. A part that is still unset is what `validateTenantConfig` reports (`missingRequiredAsset` and the like) and what blocks `publishTenantConfig` — a storage rule that every part exist would stop the first save.\n",
  "required": [
   "tenantId",
   "version"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "version": {
    "type": "string",
    "description": "The draft's working version label; the published one is `ConfigVersion.version`."
   },
   "isDraft": {
    "type": "boolean",
    "readOnly": true,
    "description": "True for the working draft, which is the only row."
   },
   "brand": {
    "$ref": "#/components/schemas/BrandIdentity"
   },
   "appIcons": {
    "$ref": "#/components/schemas/AppIcons"
   },
   "bookingFlow": {
    "$ref": "#/components/schemas/BookingFlowConfig"
   },
   "bookingFlows": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "Every venue's booking flows in the draft (`whitelabel.booking_flow`), so a publish snapshots them with the rest (decided 29 September, W12).",
    "items": {
     "$ref": "#/components/schemas/BookingFlow"
    }
   },
   "theme": {
    "$ref": "#/components/schemas/Theme"
   },
   "fonts": {
    "$ref": "#/components/schemas/FontConfig"
   },
   "footer": {
    "$ref": "#/components/schemas/FooterConfig"
   },
   "notificationBranding": {
    "type": "object",
    "nullable": true,
    "description": "BL-003. **`marketing-crm` holds the templates and nothing said whose identity they wear.** A message sent on behalf of a venue carries that venue's sender name, reply-to and logo — **an operational alert arriving from `noreply@ticvai.com` is one a guest marks as spam.**\nResolved on the template at send time rather than duplicated per template.\n",
    "properties": {
     "senderName": {
      "type": "string"
     },
     "replyToEmail": {
      "type": "string",
      "format": "email"
     },
     "smsSenderId": {
      "type": "string",
      "nullable": true
     },
     "whatsappBusinessId": {
      "type": "string",
      "nullable": true
     },
     "logoAssetId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   },
   "enabledPaymentMethods": {
    "type": "array",
    "nullable": true,
    "description": "BL-004. **`FeatureToggle` could turn Apple Pay on and could not say which cards a tenant accepts.** Resolved against `orders.PaymentProvider.supportedMethods` — the tenant's choice within what the gateway offers, and **a tenant enabling a method their provider does not support should fail here rather than at checkout.**\n",
    "items": {
     "type": "string"
    }
   },
   "accessibility": {
    "$ref": "#/components/schemas/AccessibilitySettings"
   },
   "header": {
    "$ref": "#/components/schemas/HeaderConfig"
   },
   "navigation": {
    "$ref": "#/components/schemas/NavigationConfig"
   },
   "homepage": {
    "$ref": "#/components/schemas/HomepageLayout"
   },
   "modules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ModuleEnablement"
    }
   },
   "features": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FeatureToggle"
    }
   },
   "languages": {
    "$ref": "#/components/schemas/LanguageConfig"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "isInMaintenance": {
    "type": "boolean",
    "default": false,
    "description": "Written by `setMaintenanceMode`; read by `getTenantAppStatus`."
   },
   "maintenanceMessage": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "The message on the branded maintenance screen."
   },
   "expectedBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "minimumAppVersion": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MinimumAppVersion"
     }
    ],
    "description": "Live state, written by `setMaintenanceMode` (audit R073)."
   },
   "contact": {
    "allOf": [
     {
      "$ref": "#/components/schemas/VenueContact"
     }
    ],
    "description": "Live state, written by `setMaintenanceMode` (audit R073)."
   },
   "availability": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AppAvailability"
     }
    ],
    "description": "Live state, written by `setMaintenanceMode` (audit R073)."
   },
   "availabilityMessage": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "Live state, written by `setMaintenanceMode` (audit R073)."
   },
   "venues": {
    "type": "array",
    "x-ticvai-derived": "onRead",
    "description": "The tenant's active venues, for the guest venue picker on WEB-001 and GST-001 (decided 28 September, audit R267). Public: returned without a session and cached with the rest of the response. Read from `tenancy` venues; a closed or archived venue is left out.\n",
    "items": {
     "type": "object",
     "required": [
      "venueId",
      "name"
     ],
     "properties": {
      "venueId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "city": {
       "type": "string",
       "nullable": true
      },
      "openingHours": {
       "allOf": [
        {
         "$ref": "#/components/schemas/LocalisedText"
        }
       ],
       "nullable": true,
       "description": "Today's hours as shown to a guest, e.g. \"10:00 to 22:00\"."
      }
     }
    }
   }
  }
 },
 "TenantStatus": {
  "type": "string",
  "enum": [
   "onboarding",
   "active",
   "suspended",
   "terminating",
   "terminated"
  ]
 },
 "Theme": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "primaryColour",
   "secondaryColour",
   "backgroundColour",
   "textColour"
  ],
  "properties": {
   "primaryColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "secondaryColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "accentColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "backgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "textColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "darkMode": {
    "type": "object",
    "description": "Optional dark variant. Derived from the light theme when absent.",
    "properties": {
     "primaryColour": {
      "type": "string",
      "pattern": "^#[0-9A-Fa-f]{6}$"
     },
     "backgroundColour": {
      "type": "string",
      "pattern": "^#[0-9A-Fa-f]{6}$"
     },
     "textColour": {
      "type": "string",
      "pattern": "^#[0-9A-Fa-f]{6}$"
     }
    }
   },
   "cornerRadius": {
    "type": "integer",
    "minimum": 0,
    "maximum": 32,
    "description": "The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). Its named palettes, font pairs and background tones are presets over the colours here and `FontConfig`, not stored values."
   },
   "surfaceStyle": {
    "type": "string",
    "enum": [
     "glass",
     "solid"
    ],
    "default": "glass",
    "description": "Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3)."
   },
   "buttonStyle": {
    "type": "string",
    "enum": [
     "solid",
     "outline",
     "pill"
    ],
    "default": "solid",
    "description": "Button shape (decided 29 September, rev 3 CFG-3)."
   },
   "componentColours": {
    "type": "object",
    "description": "**Colours for single interactive elements (decided 17 September, M17-11).** Each is optional and falls back to the theme colours. Every pair passes the same contrast check as the theme (`ContrastProblem`), or `setTheme` refuses it with 400. The guest flow stays the standard one; only the colours change.\n",
    "properties": {
     "primaryCta": {
      "$ref": "#/components/schemas/ThemeComponentColour"
     },
     "payButton": {
      "$ref": "#/components/schemas/ThemeComponentColour"
     },
     "addToCart": {
      "$ref": "#/components/schemas/ThemeComponentColour"
     },
     "buyTicketsButton": {
      "$ref": "#/components/schemas/ThemeComponentColour"
     },
     "link": {
      "$ref": "#/components/schemas/ThemeComponentColour"
     },
     "badge": {
      "$ref": "#/components/schemas/ThemeComponentColour"
     }
    }
   }
  }
 },
 "ThemeComponentColour": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "properties": {
   "background": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "text": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   }
  }
 },
 "VenueContact": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "nullable": true,
  "description": "How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n",
  "properties": {
   "phone": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "format": "email",
    "nullable": true
   },
   "whatsapp": {
    "type": "string",
    "nullable": true
   },
   "address": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   },
   "openingHours": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "Prose, as the guest reads it. The bookable hours are the catalogue's."
   }
  }
 },
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of `setVenueSettings`."
   },
   "calendarDayStartHour": {
    "type": "integer",
    "minimum": 0,
    "maximum": 23,
    "nullable": true,
    "default": 6,
    "description": "**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"
   },
   "currencyCode": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "readOnly": true,
    "description": "**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "nullable": true,
    "readOnly": true,
    "description": "**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"
   },
   "supportHours": {
    "type": "object",
    "description": "CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n",
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "alwaysOn",
       "businessHours",
       "custom",
       "none"
      ]
     },
     "timezone": {
      "type": "string",
      "description": "IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"
     },
     "windows": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string",
         "enum": [
          "mon",
          "tue",
          "wed",
          "thu",
          "fri",
          "sat",
          "sun"
         ]
        },
        "from": {
         "type": "string",
         "description": "Wall-clock time the desk opens."
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time the desk closes."
        }
       }
      }
     },
     "outOfHoursMessage": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "quietHours": {
    "type": "object",
    "nullable": true,
    "description": "**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n",
    "properties": {
     "from": {
      "type": "string",
      "description": "Wall-clock time sending stops",
      "in the region's time zone.": null
     },
     "to": {
      "type": "string",
      "description": "Wall-clock time sending resumes",
      "in the region's time zone.": null
     }
    }
   },
   "biometrics": {
    "type": "object",
    "nullable": true,
    "description": "CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false,
      "description": "**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"
     },
     "dpiaReference": {
      "type": "string",
      "nullable": true,
      "maxLength": 200,
      "description": "**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"
     },
     "consentNoticeAcknowledgedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "description": "**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"
     },
     "acknowledgedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "readOnly": true,
      "description": "**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"
     },
     "faceTagPurgeMinutesAfterClose": {
      "type": "integer",
      "nullable": true,
      "default": 0,
      "description": "BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"
     }
    }
   },
   "segregatedAccess": {
    "type": "object",
    "nullable": true,
    "description": "CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false
     },
     "appliesToAccessPointIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "schedule": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string",
         "enum": [
          "mon",
          "tue",
          "wed",
          "thu",
          "fri",
          "sat",
          "sun"
         ]
        },
        "from": {
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
        },
        "admits": {
         "type": "string",
         "enum": [
          "all",
          "women",
          "womenAndChildren",
          "families",
          "members"
         ]
        }
       }
      }
     },
     "entitlementGated": {
      "type": "boolean",
      "default": true,
      "readOnly": true,
      "description": "**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"
     },
     "genderVerification": {
      "type": "string",
      "enum": [
       "off",
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": "off",
      "description": "`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"
     },
     "overrideRateAlertThreshold": {
      "type": "number",
      "nullable": true,
      "description": "Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"
     }
    }
   },
   "alerting": {
    "type": "object",
    "description": "CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n",
    "properties": {
     "channel": {
      "type": "string",
      "enum": [
       "dashboardPanel",
       "dashboardAndEmail",
       "dashboardAndWhatsapp"
      ],
      "default": "dashboardPanel"
     },
     "acknowledgementRequired": {
      "type": "boolean",
      "default": true
     },
     "escalateAfterMinutes": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "displayCurrencies": {
    "type": "array",
    "nullable": true,
    "description": "**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n",
    "items": {
     "type": "string",
     "pattern": "^[A-Z]{3}$"
    }
   },
   "cartLeaseSeconds": {
    "type": "integer",
    "nullable": true,
    "minimum": 30,
    "maximum": 3600,
    "default": 900,
    "description": "**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"
   },
   "cartHoldExtensionMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "maximum": 30,
    "default": 5,
    "description": "How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."
   },
   "cartMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."
   },
   "resaleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 168,
    "default": 24,
    "description": "Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."
   },
   "exchangeCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."
   },
   "rescheduleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."
   },
   "reservationMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."
   },
   "shiftVarianceThreshold": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"
   },
   "catalogue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxVariantsPerProduct": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 2000,
      "default": 200,
      "description": "Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."
     },
     "waitlistOfferHoldMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 1440,
      "default": 30,
      "description": "How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 10,
      "description": "A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationCount": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 50,
      "description": "A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     }
    }
   },
   "inventory": {
    "type": "object",
    "nullable": true,
    "properties": {
     "overReceiptTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 5,
      "description": "Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."
     },
     "countVarianceTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 2,
      "description": "Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."
     },
     "countVarianceApprovalAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"
     }
    }
   },
   "seating": {
    "type": "object",
    "nullable": true,
    "properties": {
     "seatHoldExtensionSeconds": {
      "type": "integer",
      "nullable": true,
      "minimum": 60,
      "maximum": 1800,
      "default": 300,
      "description": "What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."
     },
     "seatHoldMaxExtensions": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 5,
      "default": 2,
      "description": "How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."
     },
     "maxSeatsPerGuestOrder": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 50,
      "default": 10,
      "description": "**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"
     }
    }
   },
   "promotions": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxDiscountPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 30,
      "description": "The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."
     },
     "nearZeroLinePrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"
     }
    }
   },
   "fnb": {
    "type": "object",
    "nullable": true,
    "properties": {
     "recallWindowMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 60,
      "default": 10,
      "description": "Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."
     },
     "compEscalationAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"
     },
     "foodSafetyLeadPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"
     }
    }
   },
   "queue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "crossQueueLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 10,
      "default": 2,
      "description": "Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "reporting": {
    "type": "object",
    "nullable": true,
    "properties": {
     "inlineRunRowLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1000,
      "maximum": 100000,
      "default": 5000,
      "description": "Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."
     },
     "dashboardRefreshBudgetPerMinute": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 24,
      "description": "Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."
     }
    }
   },
   "marketing": {
    "type": "object",
    "nullable": true,
    "properties": {
     "attributionWindowDays": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 30,
      "default": 7,
      "description": "Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "identity": {
    "type": "object",
    "nullable": true,
    "properties": {
     "guestOtpMaxAttempts": {
      "type": "integer",
      "nullable": true,
      "minimum": 3,
      "maximum": 10,
      "default": 5,
      "description": "Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"
     },
     "guestTwoStep": {
      "type": "object",
      "nullable": true,
      "description": "**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n",
      "properties": {
       "enabled": {
        "type": "boolean",
        "default": false,
        "description": "Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."
       },
       "stepUpActions": {
        "type": "array",
        "uniqueItems": true,
        "description": "The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n",
        "items": {
         "type": "string",
         "enum": [
          "changeContactDetails",
          "changePassword",
          "managePaymentMethods",
          "transferTickets",
          "deleteAccount"
         ]
        },
        "default": [
         "changeContactDetails",
         "changePassword",
         "managePaymentMethods",
         "deleteAccount"
        ]
       }
      }
     }
    }
   }
  }
 }
}
```
