# P13-white-label-01 — P13 · White Label (1 of 2)

**10 screens · 54 operations · 54 schemas · 8 permissions**

Platform P13 Venue CMS · ships as **venue-management** ·
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
| `screens.json` | Every field of every screen in the batch. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_VIEW, ORDER_CREATE, ORDER_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, TENANT_CONFIGURE, TENANT_PUBLISH`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `CMS-001` | Tenant Workspace | statusTracker | 7 | 3 | — |
| `CMS-002` | Brand Kit | statusTracker | 4 | 3 | — |
| `CMS-003` | Typography | statusTracker | 4 | 2 | — |
| `CMS-004` | Logo & Assets | statusTracker | 4 | 2 | — |
| `CMS-005` | Theme Editor | statusTracker | 2 | 1 | — |
| `CMS-006` | Component Preview | listDetail | 5 | 2 | — |
| `CMS-007` | Page Builder | statusTracker | 9 | 4 | — |
| `CMS-008` | Content Blocks | listDetail | 8 | 5 | — |
| `CMS-009` | Navigation & Menus | listDetail | 6 | 3 | — |
| `CMS-010` | Media Library | listDetail | 12 | 9 | — |

## Thin screens in this batch

**CMS-005 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "CMS-001",
  "name": "Tenant Workspace",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/tenant-workspace",
   "component": "apps/venue-management-web/src/routes/white-label/TenantWorkspaceDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-002",
    "CMS-003",
    "CMS-004",
    "CMS-008",
    "CMS-009",
    "CMS-010",
    "CMS-011",
    "CMS-016",
    "CMS-015",
    "CMS-019",
    "CMS-021",
    "CMS-031",
    "CMS-041",
    "CMS-051",
    "CMS-061",
    "CMS-071",
    "CMS-081",
    "CMS-091"
   ],
   "inferred": true,
   "isEntryPoint": true,
   "transitions": [
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "structural — CMS-001 is P13's home screen and its exits are its launcher"
    },
    {
     "to": "CMS-004",
     "trigger": "Logo & Assets",
     "provenance": "structural — CMS-001 is P13's home screen and its exits are its launcher"
    },
    {
     "to": "CMS-061",
     "trigger": "Digital Asset Management Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "CMS-071",
     "trigger": "AI Asset Intelligence Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "CMS-081",
     "trigger": "DAM Governance & Rights Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "CMS-091",
     "trigger": "Asset Distribution & Delivery Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "CMS-008",
     "trigger": "Content Blocks",
     "provenance": "derived — CMS-008 declares entryState.params bannerId, promoBlockId and CMS-001 holds none of them, so the edge carries nothing and CMS-008 opens cold"
    },
    {
     "to": "CMS-009",
     "trigger": "Navigation & Menus",
     "provenance": "derived — CMS-009 declares entryState.params menuId and CMS-001 holds none of them, so the edge carries nothing and CMS-009 opens cold"
    },
    {
     "to": "CMS-010",
     "trigger": "Media Library",
     "provenance": "derived — CMS-010 declares entryState.params mediaCode, mediaId, uploadId and CMS-001 holds none of them, so the edge carries nothing and CMS-010 opens cold"
    },
    {
     "to": "CMS-011",
     "trigger": "Translations",
     "provenance": "structural — CMS-001 is P13's home screen and its exits are its launcher"
    },
    {
     "to": "CMS-016",
     "trigger": "Site Settings",
     "provenance": "structural — CMS-001 is P13's home screen and its exits are its launcher"
    },
    {
     "to": "CMS-019",
     "trigger": "User Access",
     "provenance": "structural — CMS-001 is P13's home screen and its exits are its launcher"
    },
    {
     "to": "CMS-015",
     "trigger": "Version History",
     "provenance": "structural — CMS-001 is P13's home screen and its exits are its launcher",
     "carries": [
      "version"
     ]
    },
    {
     "to": "CMS-021",
     "trigger": "Privacy & Consent Configuration Command Center",
     "provenance": "structural — CMS-001 is P13's home screen and its exits are its launcher"
    },
    {
     "to": "CMS-031",
     "trigger": "Privacy Operations Command Center",
     "provenance": "structural — CMS-001 is P13's home screen and its exits are its launcher"
    },
    {
     "to": "CMS-041",
     "trigger": "Waiver & Consent Command Center",
     "provenance": "structural — CMS-001 is P13's home screen and its exits are its launcher"
    },
    {
     "to": "CMS-051",
     "trigger": "Waiver Operations Command Center",
     "provenance": "structural — CMS-001 is P13's home screen and its exits are its launcher"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "provenance": "flow F102 step 1→2",
     "carries": [
      "version"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **The tenant workspace.** Lands a tenant on what is live rather than on a form. **Declared 20 August** — `isEntryPoint` existed in the schema and five platforms used none, so every screen in them read as unreachable. **Drawn 31 August** — `Marketing Board 7.dc.html` frame `crm-7f` (*Agent Workspace*), matched on title at 0.84 within this board’s platforms.\n\n**Rewired 23 September (L7).** The screen called the maintenance equipment register, guest CRM or subscription billing where its purpose names White Labelling. Its operations now match its purpose.",
  "density": "compact",
  "boardFrames": [
   "Marketing Board 7.dc.html#crm-7f"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getTenantAppStatus` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Land a tenant somewhere that shows what is live and what is not.",
  "states": {
   "loading": "The tenant, read by `getTenantAppStatus`.",
   "error": "Could not load. Names which read failed and leaves the tenant untouched.",
   "emptyFirstRun": "No tenant yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `getTenantConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getTenantAppStatus",
    "contract": "white-label",
    "purpose": "Whether the guest web and app are live",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTenantConfig",
    "contract": "white-label",
    "purpose": "The published configuration",
    "trigger": "onLoad"
   },
   {
    "operationId": "getModuleEnablement",
    "contract": "white-label",
    "purpose": "Which modules guests can see",
    "trigger": "onLoad"
   },
   {
    "operationId": "getFeatureToggles",
    "contract": "white-label",
    "purpose": "Which features are switched on",
    "trigger": "onLoad"
   },
   {
    "operationId": "setModuleEnablement",
    "contract": "white-label",
    "purpose": "Switch a module on or off for guests",
    "trigger": "onAction"
   },
   {
    "operationId": "setFeatureToggles",
    "contract": "white-label",
    "purpose": "Switch a feature on or off",
    "trigger": "onAction"
   },
   {
    "operationId": "setMaintenanceMode",
    "contract": "white-label",
    "purpose": "Put the guest web and app into maintenance, and set the rest of the live app status — minimum app version, contact details, availability (decided 28 September, audit R073)",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-001",
   "derivedFrom": "wireframes/reference/Marketing Board 7.dc.html",
   "note": "**Drawn by Claude Design on `Marketing Board 7.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The tenant app status",
       "bindsTo": "TenantAppStatus",
       "columns": [
        "TenantAppStatus.isPublished",
        "TenantAppStatus.publishedVersion",
        "TenantAppStatus.publishedAt",
        "TenantAppStatus.draftVersion",
        "TenantAppStatus.hasUnpublishedChanges",
        "TenantAppStatus.activeModuleCount",
        "TenantAppStatus.licensedModuleCount",
        "TenantAppStatus.activePageCount",
        "TenantAppStatus.isInMaintenance",
        "TenantAppStatus.maintenanceMessage",
        "TenantAppStatus.expectedBackAt",
        "TenantAppStatus.minimumAppVersion",
        "TenantAppStatus.contact",
        "TenantAppStatus.availability",
        "TenantAppStatus.availabilityMessage",
        "TenantAppStatus.recentChanges"
       ],
       "operation": "getTenantAppStatus",
       "provenance": "contract white-label.yaml GET /tenant-config/status"
      },
      {
       "kind": "detailPanel",
       "label": "The tenant config",
       "bindsTo": "TenantConfig",
       "columns": [
        "TenantConfig.isDraft",
        "TenantConfig.brand",
        "TenantConfig.appIcons",
        "TenantConfig.bookingFlow",
        "TenantConfig.theme",
        "TenantConfig.fonts",
        "TenantConfig.footer",
        "TenantConfig.notificationBranding",
        "TenantConfig.enabledPaymentMethods",
        "TenantConfig.accessibility",
        "TenantConfig.header",
        "TenantConfig.navigation",
        "TenantConfig.homepage",
        "TenantConfig.modules",
        "TenantConfig.features",
        "TenantConfig.languages"
       ],
       "operation": "getTenantConfig",
       "provenance": "contract white-label.yaml GET /tenant-config"
      },
      {
       "kind": "detailPanel",
       "label": "The module enablement",
       "bindsTo": "ModuleEnablement",
       "columns": [
        "ModuleEnablement.moduleKey",
        "ModuleEnablement.displayName",
        "ModuleEnablement.isLicensed",
        "ModuleEnablement.isEnabled",
        "ModuleEnablement.referencedBy"
       ],
       "operation": "getModuleEnablement",
       "provenance": "contract white-label.yaml GET /tenant-config/modules"
      },
      {
       "kind": "detailPanel",
       "label": "The feature toggle",
       "bindsTo": "FeatureToggle",
       "columns": [
        "FeatureToggle.featureKey",
        "FeatureToggle.displayName",
        "FeatureToggle.isEnabled",
        "FeatureToggle.changeScope",
        "FeatureToggle.requiresConfiguration"
       ],
       "operation": "getFeatureToggles",
       "provenance": "contract white-label.yaml GET /tenant-config/features"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save module enablement",
       "operation": "setModuleEnablement",
       "provenance": "contract white-label.yaml PUT /tenant-config/modules"
      },
      {
       "kind": "secondaryButton",
       "label": "Save feature toggles",
       "operation": "setFeatureToggles",
       "provenance": "contract white-label.yaml PUT /tenant-config/features"
      },
      {
       "kind": "secondaryButton",
       "label": "Save maintenance mode",
       "operation": "setMaintenanceMode",
       "provenance": "contract white-label.yaml PUT /tenant-config/status"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "formSetModuleEnablement",
    "component": "modal",
    "trigger": "Save module enablement",
    "body": "**Collects what `setModuleEnablement` sends before it is called.** Required: `modules`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save module enablement",
     "operation": "setModuleEnablement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "modules"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/modules"
   },
   {
    "id": "formSetFeatureToggles",
    "component": "modal",
    "trigger": "Save feature toggles",
    "body": "**Collects what `setFeatureToggles` sends before it is called.** Required: `features`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save feature toggles",
     "operation": "setFeatureToggles"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "features"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/features"
   },
   {
    "id": "formSetMaintenanceMode",
    "component": "modal",
    "trigger": "Save maintenance mode",
    "body": "**Collects what `setMaintenanceMode` sends before it is called.** Required: `isInMaintenance`. Optional: `message`, `expectedBackAt`, `minimumAppVersion` (`ios`, `android`), `contact` (`phone`, `email`, `whatsapp`, `address`, `openingHours`), `availability` (`open`, `soldOut`, `closed`) and `availabilityMessage`. **The live app status is set here, not published** (decided 28 September, audit R073 (b)(f)): a guest app below `minimumAppVersion` for its platform is sent to the forced upgrade (GST-047), the contact details feed WEB-028 and the availability feeds WEB-029's sold-out and closed states. A field not sent is left as it is, so clearing maintenance does not clear the contact details. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save maintenance mode",
     "operation": "setMaintenanceMode"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "isInMaintenance",
      "message",
      "expectedBackAt",
      "minimumAppVersion",
      "contact",
      "availability",
      "availabilityMessage"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/status"
   }
  ],
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-002",
  "name": "Brand Kit",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/brand-kit",
   "component": "apps/venue-management-web/src/routes/white-label/BrandKitDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-003",
    "CMS-004",
    "CMS-005"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "CMS-005",
     "trigger": "Sets the colour theme",
     "provenance": "flow F22 step 1→2"
    },
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-002 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-002 holds none of them, so the edge carries nothing and CMS-003 opens cold"
    },
    {
     "to": "CMS-004",
     "trigger": "Logo & Assets",
     "provenance": "derived — CMS-004 declares entryState.params  and CMS-002 holds none of them, so the edge carries nothing and CMS-004 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getBrandIdentity` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Set the things every surface reads.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The brand identity",
       "bindsTo": "BrandIdentity",
       "columns": [
        "BrandIdentity.logoAssetRef",
        "BrandIdentity.logoDarkAssetRef",
        "BrandIdentity.logoVariant",
        "BrandIdentity.faviconAssetRef",
        "BrandIdentity.splashImageAssetRefs",
        "BrandIdentity.splashDurationSeconds",
        "BrandIdentity.splashBackgroundColour",
        "BrandIdentity.showLoadingIndicator",
        "BrandIdentity.splashChangeScope"
       ],
       "operation": "getBrandIdentity",
       "provenance": "contract white-label.yaml GET /tenant-config/brand"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save brand identity",
       "operation": "setBrandIdentity",
       "provenance": "contract white-label.yaml PUT /tenant-config/brand"
      },
      {
       "kind": "secondaryButton",
       "label": "Create upload",
       "operation": "createUpload",
       "provenance": "contract assets.yaml POST /media/uploads"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete upload",
       "operation": "completeUpload",
       "provenance": "contract assets.yaml POST /media/uploads/{uploadId}/complete"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The brand kit, read by `getBrandIdentity`.",
   "error": "Could not load. Names which read failed and leaves the brand kit untouched.",
   "emptyFirstRun": "No brand kit yet. Offers Create upload (`createUpload`).",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `getBrandIdentity` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getBrandIdentity",
    "contract": "white-label",
    "purpose": "Read brand identity",
    "trigger": "onLoad"
   },
   {
    "operationId": "setBrandIdentity",
    "contract": "white-label",
    "purpose": "Set logo, favicon and splash",
    "trigger": "onAction"
   },
   {
    "operationId": "createUpload",
    "contract": "assets",
    "purpose": "Request a signed upload URL",
    "trigger": "onAction"
   },
   {
    "operationId": "completeUpload",
    "contract": "assets",
    "purpose": "Confirm an upload and create the asset",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "uploadId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `uploadId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-002"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetBrandIdentity",
    "component": "modal",
    "trigger": "Save brand identity",
    "body": "**Collects what `setBrandIdentity` sends before it is called.** Required: `logoAssetRef`. Optional: `logoVariant` (light, dark or duotone: which lockup sits in the nav bar and which colour reading of it drives the theme, decided 29 September, rev 3 CFG-4), `logoDarkAssetRef`, `faviconAssetRef`, `splashImageAssetRefs`, `splashDurationSeconds`, `splashBackgroundColour`, `showLoadingIndicator`, `splashChangeScope`. Dismissing sends nothing; the screen behind is unchanged.",
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
      "logoVariant",
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
    "id": "formCreateUpload",
    "component": "modal",
    "trigger": "Create upload",
    "body": "**Collects what `createUpload` sends before it is called.** Required: `filename`, `contentType`, `sizeBytes`. Optional: `venueId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Create upload",
     "operation": "createUpload"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "filename",
      "contentType",
      "sizeBytes",
      "venueId"
     ]
    },
    "provenance": "contract assets.yaml POST /media/uploads"
   },
   {
    "id": "formCompleteUpload",
    "component": "modal",
    "trigger": "Complete upload",
    "body": "**Collects what `completeUpload` sends before it is called.** Nothing in the body is required. Optional: `title`, `altText`, `tags`, `collectionIds`, `rights`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Complete upload",
     "operation": "completeUpload"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "title",
      "altText",
      "tags",
      "collectionIds",
      "rights"
     ]
    },
    "provenance": "contract assets.yaml POST /media/uploads/{uploadId}/complete"
   }
  ],
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-003",
  "name": "Typography",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/typography",
   "component": "apps/venue-management-web/src/routes/white-label/TypographyDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-004",
    "CMS-006"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-003 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-003 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-004",
     "trigger": "Logo & Assets",
     "provenance": "derived — CMS-004 declares entryState.params  and CMS-003 holds none of them, so the edge carries nothing and CMS-004 opens cold"
    },
    {
     "to": "CMS-006",
     "trigger": "Component Preview",
     "provenance": "flow F102 step 2→3",
     "carries": [
      "bannerId",
      "pageId",
      "policyKind",
      "version"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **37 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getFonts` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Choose the two typefaces and the scale under them.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The font config",
       "bindsTo": "FontConfig",
       "columns": [
        "FontConfig.primaryLatin",
        "FontConfig.primaryArabic",
        "FontConfig.secondaryLatin",
        "FontConfig.secondaryArabic",
        "FontConfig.customFontAssetRefs",
        "FontConfig.changeScope"
       ],
       "operation": "getFonts",
       "provenance": "contract white-label.yaml GET /tenant-config/fonts"
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
        "Theme.cornerRadius",
        "Theme.surfaceStyle",
        "Theme.buttonStyle"
       ],
       "operation": "getTheme",
       "provenance": "contract white-label.yaml GET /tenant-config/theme"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save fonts",
       "operation": "setFonts",
       "provenance": "contract white-label.yaml PUT /tenant-config/fonts"
      },
      {
       "kind": "secondaryButton",
       "label": "Save theme",
       "operation": "setTheme",
       "provenance": "contract white-label.yaml PUT /tenant-config/theme"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The typography, read by `getFonts`.",
   "error": "Could not load. Names which read failed and leaves the typography untouched.",
   "emptyFirstRun": "No typography yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `getFonts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getFonts",
    "contract": "white-label",
    "purpose": "Read font configuration",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTheme",
    "contract": "white-label",
    "purpose": "Read colour theme",
    "trigger": "onLoad"
   },
   {
    "operationId": "setFonts",
    "contract": "white-label",
    "purpose": "Set fonts",
    "trigger": "onAction"
   },
   {
    "operationId": "setTheme",
    "contract": "white-label",
    "purpose": "Set colour theme",
    "trigger": "onAction"
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
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `bannerId`, `pageId`, `policyKind`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-003"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetFonts",
    "component": "modal",
    "trigger": "Save fonts",
    "body": "**Collects what `setFonts` sends before it is called.** Required: `primaryLatin`. Optional: `primaryArabic`, `secondaryLatin`, `secondaryArabic`, `customFontAssetRefs`, `changeScope`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "FontConfig",
    "confirm": {
     "label": "Save fonts",
     "operation": "setFonts"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "primaryLatin",
      "primaryArabic",
      "secondaryLatin",
      "secondaryArabic",
      "customFontAssetRefs",
      "changeScope"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/fonts"
   },
   {
    "id": "formSetTheme",
    "component": "modal",
    "trigger": "Save theme",
    "body": "**Collects what `setTheme` sends before it is called.** Required: `primaryColour`, `secondaryColour`, `backgroundColour`, `textColour`. Optional: `accentColour`, `darkMode`, `cornerRadius`, `surfaceStyle` (glass or solid, default glass) and `buttonStyle` (solid, outline or pill, default solid; decided 29 September, rev 3 CFG-3). Dismissing sends nothing; the screen behind is unchanged.",
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
      "cornerRadius",
      "surfaceStyle",
      "buttonStyle"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/theme"
   }
  ],
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-004",
  "name": "Logo & Assets",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/logo-assets",
   "component": "apps/venue-management-web/src/routes/white-label/LogoAssetsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-004 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-004 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-004 holds none of them, so the edge carries nothing and CMS-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.\n\n**Rewired 23 September (L7).** The screen called the maintenance equipment register, guest CRM or subscription billing where its purpose names White Labelling. Its operations now match its purpose.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getBrandIdentity` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Hold the marks every surface needs, at the sizes it needs them.",
  "states": {
   "loading": "The logo assets, read by `getBrandIdentity`.",
   "error": "Could not load. Names which read failed and leaves the logo assets untouched.",
   "emptyFirstRun": "No logo assets yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `getBrandIdentity` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getBrandIdentity",
    "contract": "white-label",
    "purpose": "The logo, favicon and splash in use",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAppIcons",
    "contract": "white-label",
    "purpose": "The app icon set at every size",
    "trigger": "onLoad"
   },
   {
    "operationId": "setAppIcons",
    "contract": "white-label",
    "purpose": "Replace the app icon set",
    "trigger": "onAction"
   },
   {
    "operationId": "setBrandIdentity",
    "contract": "white-label",
    "purpose": "Replace a logo, favicon or splash",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-004"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The brand identity",
       "bindsTo": "BrandIdentity",
       "columns": [
        "BrandIdentity.logoAssetRef",
        "BrandIdentity.logoDarkAssetRef",
        "BrandIdentity.logoVariant",
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
       "label": "Save app icons",
       "operation": "setAppIcons",
       "provenance": "contract white-label.yaml PUT /tenant-config/app-icons"
      },
      {
       "kind": "secondaryButton",
       "label": "Save brand identity",
       "operation": "setBrandIdentity",
       "provenance": "contract white-label.yaml PUT /tenant-config/brand"
      }
     ]
    }
   ]
  },
  "overlays": [
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
    "body": "**Collects what `setBrandIdentity` sends before it is called.** Required: `logoAssetRef`. Optional: `logoVariant` (light, dark or duotone: which lockup sits in the nav bar and which colour reading of it drives the theme, decided 29 September, rev 3 CFG-4), `logoDarkAssetRef`, `faviconAssetRef`, `splashImageAssetRefs`, `splashDurationSeconds`, `splashBackgroundColour`, `showLoadingIndicator`, `splashChangeScope`. Dismissing sends nothing; the screen behind is unchanged.",
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
      "logoVariant",
      "faviconAssetRef",
      "splashImageAssetRefs",
      "splashDurationSeconds",
      "splashBackgroundColour",
      "showLoadingIndicator",
      "splashChangeScope"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/brand"
   }
  ],
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-005",
  "name": "Theme Editor",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/theme-editor",
   "component": "apps/venue-management-web/src/routes/white-label/ThemeEditorDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003",
    "CMS-006",
    "CMS-007"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "CMS-007",
     "trigger": "Rearranges the homepage",
     "provenance": "flow F22 step 2→3"
    },
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-005 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-005 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-005 holds none of them, so the edge carries nothing and CMS-003 opens cold"
    },
    {
     "to": "CMS-006",
     "trigger": "Component Preview",
     "provenance": "derived — CMS-006 declares entryState.params bannerId, pageId, policyKind, version and CMS-005 holds none of them, so the edge carries nothing and CMS-006 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.\n\n**A failing colour contrast is refused, not warned (decided 28 September, audit R139 (a)).** `setTheme` answers `400` with a `ContrastProblem` naming each failing pair (foreground, background, ratio, the ratio required, where it is used); the theme is not saved, and the editor keeps the entered colours and marks the failing pairs so they can be corrected. There is no save-anyway.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getTheme` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Tune the theme and watch it apply everywhere at once.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
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
        "Theme.cornerRadius",
        "Theme.surfaceStyle",
        "Theme.buttonStyle"
       ],
       "operation": "getTheme",
       "provenance": "contract white-label.yaml GET /tenant-config/theme"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save theme",
       "operation": "setTheme",
       "provenance": "contract white-label.yaml PUT /tenant-config/theme"
      },
      {
       "kind": "banner",
       "label": "Contrast refused",
       "bindsTo": "ContrastProblem",
       "columns": [
        "ContrastProblem.failures"
       ],
       "operation": "setTheme",
       "notes": "Shown when `setTheme` answers 400. Lists every failing pair; the theme was not saved (decided 28 September, audit R139 (a)).",
       "provenance": "contract white-label.yaml PUT /tenant-config/theme"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The theme editor, read by `getTheme`.",
   "error": "Could not load. Names which read failed and leaves the theme editor untouched.",
   "emptyFirstRun": "No theme editor yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `getTheme` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getTheme",
    "contract": "white-label",
    "purpose": "Read colour theme",
    "trigger": "onLoad"
   },
   {
    "operationId": "setTheme",
    "contract": "white-label",
    "purpose": "Set colour theme",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-005"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetTheme",
    "component": "modal",
    "trigger": "Save theme",
    "body": "**Collects what `setTheme` sends before it is called.** Required: `primaryColour`, `secondaryColour`, `backgroundColour`, `textColour`. Optional: `accentColour`, `darkMode`, `cornerRadius`, `surfaceStyle` (glass or solid, default glass) and `buttonStyle` (solid, outline or pill, default solid; decided 29 September, rev 3 CFG-3). **A colour pair that fails contrast is refused** (`400 ContrastProblem`, decided 28 September, audit R139 (a)): the modal stays open with the failing pairs marked. Dismissing sends nothing; the screen behind is unchanged.",
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
      "cornerRadius",
      "surfaceStyle",
      "buttonStyle"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/theme"
   }
  ],
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-006",
  "name": "Component Preview",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/component-preview",
   "component": "apps/venue-management-web/src/routes/white-label/ComponentPreviewDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003"
   ],
   "inferred": false,
   "entryFrom": [
    "CMS-003",
    "CMS-005"
   ],
   "notes": "**Reached from CMS-005** — a preview shows the component being edited. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-006 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-006 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "bannerId",
      "pageId",
      "policyKind",
      "version"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-006 holds bannerId, pageId, policyKind, version, so an edge into it carries them"
    },
    {
     "to": "ADM-016",
     "trigger": "White-Label Branding Management",
     "provenance": "flow F102 step 3→4",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "bannerId",
      "pageId",
      "policyKind",
      "version"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **36 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listConfigVersions` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Check the theme against the components that carry it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
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
        "ConfigVersion.scopePath"
       ],
       "operation": "listConfigVersions",
       "provenance": "contract white-label.yaml GET /tenant-config/versions"
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
   "loading": "The component preview list.",
   "error": "Could not load. Names which read failed and leaves the component preview untouched.",
   "emptyFirstRun": "No component preview yet. Offers Create preview (`createPreview`).",
   "emptyNoResults": "Never shown: `listConfigVersions` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listConfigVersions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-006"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
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
   }
  ],
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-007",
  "name": "Page Builder",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/page-builder",
   "component": "apps/venue-management-web/src/routes/white-label/PageBuilderDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003",
    "CMS-012"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "CMS-012",
     "trigger": "Previews in both directions",
     "provenance": "flow F22 step 3→4"
    },
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-007 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-007 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "pageId"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-007 holds pageId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.\n\n**A section whose module is off is disabled in the builder (decided 28 September, audit R163 (4)).** The builder reads `getModuleEnablement` and applies the mapping on `HomepageSectionKind`: `tickets` needs `ticketsAndBooking`, `whatsOn` needs `events`, `attractions` needs `attractions`, `membership` needs `membership`, `dining` needs `diningAndFnb`, `shop` needs `shop`, `map` needs `map`; `heroBanner`, `quickActions`, `promotions`, `customContent` and `spacer` need none. A section whose module is off cannot be added or made visible, and says which module to switch on (on CMS-001). `setHomepageLayout` refuses such a section with 400 in any case.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getHomepageLayout` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Assemble a storefront page from blocks the tenant cannot break.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The homepage layout",
       "bindsTo": "HomepageLayout",
       "columns": [
        "HomepageLayout.id",
        "HomepageLayout.sections"
       ],
       "operation": "getHomepageLayout",
       "provenance": "contract white-label.yaml GET /tenant-config/homepage"
      },
      {
       "kind": "detailPanel",
       "label": "Modules the sections need",
       "bindsTo": "ModuleEnablement",
       "columns": [
        "ModuleEnablement.moduleKey",
        "ModuleEnablement.displayName",
        "ModuleEnablement.isEnabled"
       ],
       "operation": "getModuleEnablement",
       "notes": "A section whose module is off (mapping on `HomepageSectionKind`) is shown disabled and cannot be added or made visible (decided 28 September, audit R163 (4)).",
       "provenance": "contract white-label.yaml GET /tenant-config/modules"
      },
      {
       "kind": "dataTable",
       "label": "Every content page",
       "bindsTo": "ContentPage",
       "columns": [
        "ContentPage.id",
        "ContentPage.slug",
        "ContentPage.title",
        "ContentPage.body",
        "ContentPage.isEnabled",
        "ContentPage.status",
        "ContentPage.iconAssetRef",
        "ContentPage.categoryCode",
        "ContentPage.sortOrder",
        "ContentPage.isReferenced",
        "ContentPage.scopePath"
       ],
       "operation": "listContentPages",
       "provenance": "contract white-label.yaml GET /tenant-config/pages"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save homepage layout",
       "operation": "setHomepageLayout",
       "provenance": "contract white-label.yaml PUT /tenant-config/homepage"
      },
      {
       "kind": "secondaryButton",
       "label": "Create content page",
       "operation": "createContentPage",
       "provenance": "contract white-label.yaml POST /tenant-config/pages"
      },
      {
       "kind": "secondaryButton",
       "label": "Save content page",
       "operation": "updateContentPage",
       "provenance": "contract white-label.yaml PUT /tenant-config/pages/{pageId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save footer",
       "operation": "setFooter",
       "provenance": "contract white-label.yaml PUT /footer"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The record, read by `getHomepageLayout`.",
   "error": "Could not load. Names which read failed and leaves the record untouched.",
   "emptyFirstRun": "No record yet. Offers Create content page (`createContentPage`).",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listContentPages` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listContentPages",
    "contract": "white-label",
    "purpose": "The guest app's content pages",
    "trigger": "onLoad"
   },
   {
    "operationId": "createContentPage",
    "contract": "white-label",
    "purpose": "Create a content page",
    "trigger": "onAction",
    "invalidates": [
     "listContentPages"
    ]
   },
   {
    "operationId": "updateContentPage",
    "contract": "white-label",
    "purpose": "Edit a content page",
    "trigger": "onAction",
    "invalidates": [
     "listContentPages"
    ]
   },
   {
    "operationId": "setFooter",
    "contract": "white-label",
    "purpose": "Set the guest web and app footer",
    "trigger": "onAction"
   },
   {
    "operationId": "getHomepageLayout",
    "contract": "white-label",
    "purpose": "Read homepage layout",
    "trigger": "onLoad"
   },
   {
    "operationId": "setHomepageLayout",
    "contract": "white-label",
    "purpose": "Set homepage section order",
    "trigger": "onAction"
   },
   {
    "operationId": "getModuleEnablement",
    "contract": "white-label",
    "purpose": "Which modules are on, so a section whose module is off is disabled in the builder (decided 28 September, audit R163 (4))",
    "trigger": "onLoad"
   },
   {
    "operationId": "setHeader",
    "contract": "white-label",
    "purpose": "Configure the header",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listContentPages",
     "getHomepageLayout",
     "getModuleEnablement"
    ]
   },
   {
    "operationId": "deleteContentPage",
    "contract": "white-label",
    "purpose": "Delete a content page",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listContentPages",
     "getHomepageLayout",
     "getModuleEnablement"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-007"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "entryState": {
   "params": [
    {
     "name": "pageId",
     "from": "navigation"
    }
   ]
  },
  "overlays": [
   {
    "id": "formCreateContentPage",
    "component": "modal",
    "trigger": "Create content page",
    "body": "**Collects what `createContentPage` sends before it is called.** Required: `id`, `slug`, `title`, `body`, `status`. Optional: `isEnabled`, `iconAssetRef`, `categoryCode`, `sortOrder`, `isReferenced`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ContentPage",
    "confirm": {
     "label": "Create content page",
     "operation": "createContentPage"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "slug",
      "title",
      "body",
      "status",
      "isEnabled",
      "iconAssetRef",
      "categoryCode",
      "sortOrder",
      "isReferenced",
      "scopePath"
     ]
    },
    "provenance": "contract white-label.yaml POST /tenant-config/pages"
   },
   {
    "id": "formUpdateContentPage",
    "component": "modal",
    "trigger": "Save content page",
    "body": "**Collects what `updateContentPage` sends before it is called.** Required: `slug`, `title`, `body`. Optional: `isEnabled`, `iconAssetRef`, `categoryCode`, `sortOrder`, `status`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "UpdateContentPageRequest",
    "confirm": {
     "label": "Save content page",
     "operation": "updateContentPage"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "slug",
      "title",
      "body",
      "isEnabled",
      "iconAssetRef",
      "categoryCode",
      "sortOrder",
      "status"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/pages/{pageId}"
   },
   {
    "id": "formSetFooter",
    "component": "modal",
    "trigger": "Save footer",
    "body": "**Collects what `setFooter` sends before it is called.** Required: `id`, `scopePath`. Optional: `columns`, `legalLinks`, `copyrightText`, `socialLinks`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "FooterConfig",
    "confirm": {
     "label": "Save footer",
     "operation": "setFooter"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "columns",
      "legalLinks",
      "copyrightText",
      "socialLinks"
     ]
    },
    "provenance": "contract white-label.yaml PUT /footer"
   },
   {
    "id": "formSetHomepageLayout",
    "component": "modal",
    "trigger": "Save homepage layout",
    "body": "**Collects what `setHomepageLayout` sends before it is called.** Required: `sections`. Optional: `id`. A section whose module is off is disabled here and cannot be made visible (audit R163 (4)). Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "HomepageLayout",
    "confirm": {
     "label": "Save homepage layout",
     "operation": "setHomepageLayout"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "sections",
      "id"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/homepage"
   }
  ],
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-008",
  "name": "Content Blocks",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/content-blocks",
   "component": "apps/venue-management-web/src/routes/white-label/ContentBlocksDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003"
   ],
   "inferred": false,
   "entryFrom": [
    "CMS-001"
   ],
   "notes": "**Reached from CMS-001** — a top-level workspace section. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-008 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-008 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "bannerId"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-008 holds bannerId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPromoBlocks` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Define what a block can and cannot contain.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every promo block",
       "bindsTo": "PromoBlock",
       "columns": [
        "PromoBlock.id",
        "PromoBlock.title",
        "PromoBlock.description",
        "PromoBlock.iconAssetRef",
        "PromoBlock.promotionId",
        "PromoBlock.linkTarget",
        "PromoBlock.startsAt",
        "PromoBlock.endsAt",
        "PromoBlock.state",
        "PromoBlock.sortOrder",
        "PromoBlock.scopePath"
       ],
       "operation": "listPromoBlocks",
       "provenance": "contract white-label.yaml GET /tenant-config/promo-blocks"
      },
      {
       "kind": "dataTable",
       "label": "Every banner",
       "bindsTo": "Banner",
       "columns": [
        "Banner.id",
        "Banner.title",
        "Banner.subtitle",
        "Banner.imageAssetRef",
        "Banner.placement",
        "Banner.linkTarget",
        "Banner.startsAt",
        "Banner.endsAt",
        "Banner.state",
        "Banner.sortOrder",
        "Banner.isActive"
       ],
       "operation": "listBanners",
       "provenance": "contract white-label.yaml GET /tenant-config/banners"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected promo block",
       "bindsTo": "PromoBlock",
       "columns": [
        "PromoBlock.id",
        "PromoBlock.title",
        "PromoBlock.description",
        "PromoBlock.iconAssetRef",
        "PromoBlock.promotionId",
        "PromoBlock.linkTarget",
        "PromoBlock.startsAt",
        "PromoBlock.endsAt",
        "PromoBlock.state",
        "PromoBlock.sortOrder",
        "PromoBlock.scopePath"
       ],
       "operation": "listPromoBlocks",
       "provenance": "contract white-label.yaml GET /tenant-config/promo-blocks"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create banner",
       "operation": "createBanner",
       "provenance": "contract white-label.yaml POST /tenant-config/banners"
      },
      {
       "kind": "secondaryButton",
       "label": "Save banner",
       "operation": "updateBanner",
       "provenance": "contract white-label.yaml PATCH /tenant-config/banners/{bannerId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Create promo block",
       "operation": "createPromoBlock",
       "provenance": "contract white-label.yaml POST /tenant-config/promo-blocks"
      },
      {
       "kind": "secondaryButton",
       "label": "Save promo block",
       "operation": "updatePromoBlock",
       "provenance": "contract white-label.yaml PATCH /tenant-config/promo-blocks/{promoBlockId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete promo block",
       "operation": "deletePromoBlock",
       "provenance": "contract white-label.yaml DELETE /tenant-config/promo-blocks/{promoBlockId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The content blocks list.",
   "error": "Could not load. Names which read failed and leaves the content blocks untouched.",
   "emptyFirstRun": "No content blocks yet. Offers Create banner (`createBanner`).",
   "emptyNoResults": "Never shown: `listPromoBlocks` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listPromoBlocks` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createBanner",
    "contract": "white-label",
    "purpose": "Create a banner",
    "trigger": "onAction",
    "invalidates": [
     "listBanners"
    ]
   },
   {
    "operationId": "updateBanner",
    "contract": "white-label",
    "purpose": "Change or schedule a banner",
    "trigger": "onAction",
    "invalidates": [
     "listBanners"
    ]
   },
   {
    "operationId": "createPromoBlock",
    "contract": "white-label",
    "purpose": "Create a promo block",
    "trigger": "onAction",
    "invalidates": [
     "listPromoBlocks"
    ]
   },
   {
    "operationId": "updatePromoBlock",
    "contract": "white-label",
    "purpose": "Change a promo block",
    "trigger": "onAction",
    "invalidates": [
     "listPromoBlocks"
    ]
   },
   {
    "operationId": "deletePromoBlock",
    "contract": "white-label",
    "purpose": "Remove a promo block",
    "trigger": "onAction",
    "invalidates": [
     "listPromoBlocks"
    ]
   },
   {
    "operationId": "listPromoBlocks",
    "contract": "white-label",
    "purpose": "List promotional blocks",
    "trigger": "onLoad"
   },
   {
    "operationId": "listBanners",
    "contract": "white-label",
    "purpose": "List banners",
    "trigger": "onLoad"
   },
   {
    "operationId": "deleteBanner",
    "contract": "white-label",
    "purpose": "Delete a banner",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listPromoBlocks",
     "listBanners"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "PromoBlock.id",
    "PromoBlock.title",
    "PromoBlock.description",
    "PromoBlock.iconAssetRef",
    "PromoBlock.promotionId"
   ],
   "params": [
    {
     "name": "bannerId",
     "from": "navigation"
    },
    {
     "name": "promoBlockId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-008"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateBanner",
    "component": "modal",
    "trigger": "Create banner",
    "body": "**Collects what `createBanner` sends before it is called.** Required: `id`, `title`, `imageAssetRef`, `startsAt`. Optional: `subtitle`, `placement`, `linkTarget`, `endsAt`, `state`, `sortOrder`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "Banner",
    "confirm": {
     "label": "Create banner",
     "operation": "createBanner"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "title",
      "imageAssetRef",
      "startsAt",
      "subtitle",
      "placement",
      "linkTarget",
      "endsAt",
      "state",
      "sortOrder",
      "isActive"
     ]
    },
    "provenance": "contract white-label.yaml POST /tenant-config/banners"
   },
   {
    "id": "formUpdateBanner",
    "component": "modal",
    "trigger": "Save banner",
    "body": "**Collects what `updateBanner` sends before it is called.** Nothing in the body is required. Optional: `title`, `subtitle`, `imageAssetRef`, `placement`, `linkTarget`, `startsAt`, `endsAt`, `sortOrder`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save banner",
     "operation": "updateBanner"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "title",
      "subtitle",
      "imageAssetRef",
      "placement",
      "linkTarget",
      "startsAt",
      "endsAt",
      "sortOrder",
      "isActive"
     ]
    },
    "provenance": "contract white-label.yaml PATCH /tenant-config/banners/{bannerId}"
   },
   {
    "id": "formCreatePromoBlock",
    "component": "modal",
    "trigger": "Create promo block",
    "body": "**Collects what `createPromoBlock` sends before it is called.** Required: `id`, `title`. Optional: `description`, `iconAssetRef`, `promotionId`, `linkTarget`, `startsAt`, `endsAt`, `state`, `sortOrder`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PromoBlock",
    "confirm": {
     "label": "Create promo block",
     "operation": "createPromoBlock"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "title",
      "description",
      "iconAssetRef",
      "promotionId",
      "linkTarget",
      "startsAt",
      "endsAt",
      "state",
      "sortOrder",
      "scopePath"
     ]
    },
    "provenance": "contract white-label.yaml POST /tenant-config/promo-blocks"
   },
   {
    "id": "formUpdatePromoBlock",
    "component": "modal",
    "trigger": "Save promo block",
    "body": "**Collects what `updatePromoBlock` sends before it is called.** Nothing in the body is required. Optional: `title`, `description`, `iconAssetRef`, `promotionId`, `linkTarget`, `startsAt`, `endsAt`, `sortOrder`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save promo block",
     "operation": "updatePromoBlock"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "title",
      "description",
      "iconAssetRef",
      "promotionId",
      "linkTarget",
      "startsAt",
      "endsAt",
      "sortOrder"
     ]
    },
    "provenance": "contract white-label.yaml PATCH /tenant-config/promo-blocks/{promoBlockId}"
   },
   {
    "id": "confirmDeletePromoBlock",
    "component": "confirmDialog",
    "trigger": "Delete promo block",
    "body": "**Names what `deletePromoBlock` changes and what it leaves alone**, in the consequence rather than the verb. A content blocks this affects should be identified in the dialog, not just counted.",
    "provenance": "contract white-label.yaml DELETE /tenant-config/promo-blocks/{promoBlockId}"
   }
  ],
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-009",
  "name": "Navigation & Menus",
  "module": "White Label",
  "requiresModule": "fnb",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/navigation-menus",
   "component": "apps/venue-management-web/src/routes/white-label/NavigationMenusDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003"
   ],
   "inferred": false,
   "entryFrom": [
    "CMS-001"
   ],
   "notes": "**Reached from CMS-001** — a top-level workspace section. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-009 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-009 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-009 holds none of them, so the edge carries nothing and CMS-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listMenus` reads the population and `getMenu` reads one of them — list, select, act",
  "purpose": "Decide what appears in the header and the footer.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Outlet id",
       "operation": "listMenus",
       "notes": "Sends `?outletId=` to `listMenus`.",
       "provenance": "contract fnb.yaml GET /menus"
      },
      {
       "kind": "datePicker",
       "label": "Active at",
       "operation": "listMenus",
       "notes": "Sends `?activeAt=` to `listMenus`.",
       "provenance": "contract fnb.yaml GET /menus"
      },
      {
       "kind": "dataTable",
       "label": "Every menu",
       "bindsTo": "Menu",
       "columns": [
        "Menu.id",
        "Menu.code",
        "Menu.name",
        "Menu.outletId",
        "Menu.availability",
        "Menu.sections",
        "Menu.isActive"
       ],
       "operation": "listMenus",
       "provenance": "contract fnb.yaml GET /menus"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected menu",
       "bindsTo": "Menu",
       "columns": [
        "Menu.id",
        "Menu.code",
        "Menu.name",
        "Menu.outletId",
        "Menu.availability",
        "Menu.sections",
        "Menu.isActive"
       ],
       "operation": "getMenu",
       "provenance": "contract fnb.yaml GET /menus/{menuId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create menu",
       "operation": "createMenu",
       "provenance": "contract fnb.yaml POST /menus"
      },
      {
       "kind": "secondaryButton",
       "label": "Save menu sections",
       "operation": "setMenuSections",
       "provenance": "contract fnb.yaml PUT /menus/{menuId}/sections"
      },
      {
       "kind": "secondaryButton",
       "label": "Save menu",
       "operation": "updateMenu",
       "provenance": "contract fnb.yaml PATCH /menus/{menuId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The navigation menus list.",
   "error": "Could not load. Names which read failed and leaves the navigation menus untouched.",
   "emptyFirstRun": "No navigation menus yet. Offers Create menu (`createMenu`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on outletId, activeAt and the navigation menus are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listMenus` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMenus",
    "contract": "fnb",
    "purpose": "List menus",
    "trigger": "onLoad"
   },
   {
    "operationId": "getMenu",
    "contract": "fnb",
    "purpose": "Read a menu with sections and items",
    "trigger": "onAction"
   },
   {
    "operationId": "createMenu",
    "contract": "fnb",
    "purpose": "Create a menu",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "setMenuSections",
    "contract": "fnb",
    "purpose": "Set menu sections and their item ordering",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "updateMenu",
    "contract": "fnb",
    "purpose": "Amend a menu",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "setNavigation",
    "contract": "white-label",
    "purpose": "Set main and overflow navigation",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "menuId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `menuId`.",
   "preloaded": [
    "Menu.id",
    "Menu.code",
    "Menu.name",
    "Menu.outletId",
    "Menu.availability"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-009"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateMenu",
    "component": "modal",
    "trigger": "Create menu",
    "body": "**Collects what `createMenu` sends before it is called.** Required: `code`, `name`, `outletId`. Optional: `availability`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateMenuRequest",
    "confirm": {
     "label": "Create menu",
     "operation": "createMenu"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "outletId",
      "availability"
     ]
    },
    "provenance": "contract fnb.yaml POST /menus"
   },
   {
    "id": "formSetMenuSections",
    "component": "modal",
    "trigger": "Save menu sections",
    "body": "**Collects what `setMenuSections` sends before it is called.** Required: `sections`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save menu sections",
     "operation": "setMenuSections"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "sections"
     ]
    },
    "provenance": "contract fnb.yaml PUT /menus/{menuId}/sections"
   },
   {
    "id": "formUpdateMenu",
    "component": "modal",
    "trigger": "Save menu",
    "body": "**Collects what `updateMenu` sends before it is called.** Nothing in the body is required. Optional: `name`, `availability`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save menu",
     "operation": "updateMenu"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "availability",
      "isActive"
     ]
    },
    "provenance": "contract fnb.yaml PATCH /menus/{menuId}"
   }
  ],
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-010",
  "name": "Media Library",
  "module": "White Label",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/media-library",
   "component": "apps/venue-management-web/src/routes/white-label/MediaLibraryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003"
   ],
   "inferred": false,
   "entryFrom": [
    "CMS-001"
   ],
   "notes": "**Reached from CMS-001** — a top-level workspace section. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-010 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-010 holds uploadId, so an edge into it carries them"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-010 holds none of them, so the edge carries nothing and CMS-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.\n\n**Archive and quarantine are reversible; deletion is the only end of an asset's life (decided 28 September, audit STATE-MEDIA).** An archived asset offers **Restore** (`updateMediaAsset` with `status: ready`); a quarantined one offers **Release**, which is the same call after a reviewer has cleared the scan flag (the state model marks that move as needing approval). **Delete media asset** (`deleteMediaAsset`) removes the asset for good and is refused while it is referenced.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`searchMedia` reads the population and `getMediaEntitlements` reads one of them — list, select, act",
  "purpose": "Hold the imagery, and know where it is used.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "searchMedia",
       "notes": "Sends `?kind=` to `searchMedia`.",
       "provenance": "contract assets.yaml GET /media"
      },
      {
       "kind": "textField",
       "label": "Tag",
       "operation": "searchMedia",
       "notes": "Sends `?tag=` to `searchMedia`.",
       "provenance": "contract assets.yaml GET /media"
      },
      {
       "kind": "textField",
       "label": "Collection id",
       "operation": "searchMedia",
       "notes": "Sends `?collectionId=` to `searchMedia`.",
       "provenance": "contract assets.yaml GET /media"
      },
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "searchMedia",
       "notes": "Sends `?venueId=` to `searchMedia`.",
       "provenance": "contract assets.yaml GET /media"
      },
      {
       "kind": "searchField",
       "label": "Search",
       "operation": "searchMedia",
       "notes": "Sends `?search=` to `searchMedia`.",
       "provenance": "contract assets.yaml GET /media"
      },
      {
       "kind": "toggle",
       "label": "Unused only",
       "operation": "searchMedia",
       "notes": "Sends `?unusedOnly=` to `searchMedia`.",
       "provenance": "contract assets.yaml GET /media"
      },
      {
       "kind": "numberField",
       "label": "Rights expiring within days",
       "operation": "searchMedia",
       "notes": "Sends `?rightsExpiringWithinDays=` to `searchMedia`.",
       "provenance": "contract assets.yaml GET /media"
      },
      {
       "kind": "dataTable",
       "label": "Every media asset",
       "bindsTo": "MediaAsset",
       "columns": [
        "MediaAsset.id",
        "MediaAsset.kind",
        "MediaAsset.status",
        "MediaAsset.filename",
        "MediaAsset.contentType",
        "MediaAsset.sizeBytes",
        "MediaAsset.title",
        "MediaAsset.altText",
        "MediaAsset.width",
        "MediaAsset.height",
        "MediaAsset.durationSeconds",
        "MediaAsset.customMetadata"
       ],
       "operation": "searchMedia",
       "provenance": "contract assets.yaml GET /media"
      },
      {
       "kind": "dataTable",
       "label": "Every collection",
       "bindsTo": "Collection",
       "columns": [
        "Collection.id",
        "Collection.name",
        "Collection.description",
        "Collection.venueId",
        "Collection.parentCollectionId",
        "Collection.assetCount",
        "Collection.coverAssetId"
       ],
       "operation": "listCollections",
       "provenance": "contract assets.yaml GET /media/collections"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
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
       "label": "The selected media asset",
       "bindsTo": "MediaAsset",
       "columns": [
        "MediaAsset.id",
        "MediaAsset.kind",
        "MediaAsset.status",
        "MediaAsset.filename",
        "MediaAsset.contentType",
        "MediaAsset.sizeBytes",
        "MediaAsset.title",
        "MediaAsset.description",
        "MediaAsset.altText",
        "MediaAsset.width",
        "MediaAsset.height",
        "MediaAsset.durationSeconds",
        "MediaAsset.customMetadata",
        "MediaAsset.sharedWithTenantIds",
        "MediaAsset.tags",
        "MediaAsset.venueId"
       ],
       "operation": "searchMedia",
       "provenance": "contract assets.yaml GET /media"
      },
      {
       "kind": "detailPanel",
       "label": "The expiring media",
       "bindsTo": "ExpiringMedia",
       "columns": [
        "ExpiringMedia.assetId",
        "ExpiringMedia.filename",
        "ExpiringMedia.thumbnailUrl",
        "ExpiringMedia.licensor",
        "ExpiringMedia.validTo",
        "ExpiringMedia.daysRemaining",
        "ExpiringMedia.isExpired",
        "ExpiringMedia.isInUse",
        "ExpiringMedia.liveUsageCount"
       ],
       "operation": "getExpiringRights",
       "provenance": "contract assets.yaml GET /media/rights-expiring"
      },
      {
       "kind": "detailPanel",
       "label": "The media asset",
       "bindsTo": "MediaAssetDetail",
       "columns": [
        "MediaAssetDetail.id",
        "MediaAssetDetail.kind",
        "MediaAssetDetail.status",
        "MediaAssetDetail.filename",
        "MediaAssetDetail.contentType",
        "MediaAssetDetail.sizeBytes",
        "MediaAssetDetail.title",
        "MediaAssetDetail.description",
        "MediaAssetDetail.altText",
        "MediaAssetDetail.width",
        "MediaAssetDetail.height",
        "MediaAssetDetail.durationSeconds",
        "MediaAssetDetail.customMetadata",
        "MediaAssetDetail.sharedWithTenantIds",
        "MediaAssetDetail.tags",
        "MediaAssetDetail.venueId"
       ],
       "operation": "getMediaAsset",
       "provenance": "contract assets.yaml GET /media/{mediaId}"
      },
      {
       "kind": "detailPanel",
       "label": "The media entitlements",
       "bindsTo": "MediaEntitlements",
       "columns": [
        "MediaEntitlements.mediaCode",
        "MediaEntitlements.mediaKind",
        "MediaEntitlements.subjectId",
        "MediaEntitlements.isValid",
        "MediaEntitlements.invalidReason",
        "MediaEntitlements.canAcceptMore",
        "MediaEntitlements.entitlements"
       ],
       "operation": "getMediaEntitlements",
       "provenance": "contract orders.yaml GET /media/{mediaCode}/entitlements"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Append entitlement to media",
       "operation": "appendEntitlementToMedia",
       "provenance": "contract orders.yaml POST /media/{mediaCode}/entitlements"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete upload",
       "operation": "completeUpload",
       "provenance": "contract assets.yaml POST /media/uploads/{uploadId}/complete"
      },
      {
       "kind": "secondaryButton",
       "label": "Create collection",
       "operation": "createCollection",
       "provenance": "contract assets.yaml POST /media/collections"
      },
      {
       "kind": "secondaryButton",
       "label": "Create upload",
       "operation": "createUpload",
       "provenance": "contract assets.yaml POST /media/uploads"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete media asset",
       "operation": "deleteMediaAsset",
       "provenance": "contract assets.yaml DELETE /media/{mediaId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Replace media asset",
       "operation": "replaceMediaAsset",
       "provenance": "contract assets.yaml POST /media/{mediaId}/replace"
      },
      {
       "kind": "secondaryButton",
       "label": "Save media asset",
       "operation": "updateMediaAsset",
       "provenance": "contract assets.yaml PATCH /media/{mediaId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Restore media asset",
       "operation": "updateMediaAsset",
       "notes": "Shown on an `archived` asset. Sends `status: ready` (decided 28 September, audit STATE-MEDIA).",
       "provenance": "contract assets.yaml PATCH /media/{mediaId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Release from quarantine",
       "operation": "updateMediaAsset",
       "notes": "Shown on a `quarantined` asset, to a reviewer, after the scan flag has been reviewed and cleared. Sends `status: ready` (decided 28 September, audit STATE-MEDIA).",
       "provenance": "contract assets.yaml PATCH /media/{mediaId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDeleteMediaAsset",
    "component": "confirmDialog",
    "trigger": "Delete media asset",
    "body": "**Names what `deleteMediaAsset` changes and what it leaves alone**, in the consequence rather than the verb. A media this affects should be identified in the dialog, not just counted. **Deletion is the only end of an asset's life and cannot be undone** (decided 28 September, audit STATE-MEDIA); the dialog offers archiving instead where the asset may be wanted again, and lists every reference when it is refused as in use.",
    "provenance": "contract assets.yaml DELETE /media/{mediaId}"
   },
   {
    "id": "confirmRestoreMediaAsset",
    "component": "confirmDialog",
    "trigger": "Restore media asset",
    "body": "**Returns an archived asset to `ready`**, so it can be used again (decided 28 September, audit STATE-MEDIA). Names the asset.",
    "confirm": {
     "label": "Restore",
     "operation": "updateMediaAsset"
    },
    "provenance": "contract assets.yaml PATCH /media/{mediaId}"
   },
   {
    "id": "confirmReleaseMediaAsset",
    "component": "confirmDialog",
    "trigger": "Release from quarantine",
    "body": "**Releases a quarantined asset to `ready` after review** (decided 28 September, audit STATE-MEDIA). Names the asset and the scan finding, and records the reviewer; the state model marks this reversal as needing approval.",
    "confirm": {
     "label": "Release",
     "operation": "updateMediaAsset"
    },
    "provenance": "contract assets.yaml PATCH /media/{mediaId}"
   },
   {
    "id": "formAppendEntitlementToMedia",
    "component": "modal",
    "trigger": "Append entitlement to media",
    "body": "**Collects what `appendEntitlementToMedia` sends before it is called.** Required: `id`, `lines`, `recordedAt`. Optional: `paymentMethod`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AppendEntitlementRequest",
    "confirm": {
     "label": "Append entitlement to media",
     "operation": "appendEntitlementToMedia"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "lines",
      "recordedAt",
      "paymentMethod",
      "note"
     ]
    },
    "provenance": "contract orders.yaml POST /media/{mediaCode}/entitlements"
   },
   {
    "id": "formCompleteUpload",
    "component": "modal",
    "trigger": "Complete upload",
    "body": "**Collects what `completeUpload` sends before it is called.** Nothing in the body is required. Optional: `title`, `altText`, `tags`, `collectionIds`, `rights`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Complete upload",
     "operation": "completeUpload"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "title",
      "altText",
      "tags",
      "collectionIds",
      "rights"
     ]
    },
    "provenance": "contract assets.yaml POST /media/uploads/{uploadId}/complete"
   },
   {
    "id": "formCreateCollection",
    "component": "modal",
    "trigger": "Create collection",
    "body": "**Collects what `createCollection` sends before it is called.** Required: `name`. Optional: `description`, `venueId`, `parentCollectionId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Create collection",
     "operation": "createCollection"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "description",
      "venueId",
      "parentCollectionId"
     ]
    },
    "provenance": "contract assets.yaml POST /media/collections"
   },
   {
    "id": "formCreateUpload",
    "component": "modal",
    "trigger": "Create upload",
    "body": "**Collects what `createUpload` sends before it is called.** Required: `filename`, `contentType`, `sizeBytes`. Optional: `venueId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Create upload",
     "operation": "createUpload"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "filename",
      "contentType",
      "sizeBytes",
      "venueId"
     ]
    },
    "provenance": "contract assets.yaml POST /media/uploads"
   },
   {
    "id": "formReplaceMediaAsset",
    "component": "modal",
    "trigger": "Replace media asset",
    "body": "**Collects what `replaceMediaAsset` sends before it is called.** Required: `uploadId`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Replace media asset",
     "operation": "replaceMediaAsset"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "uploadId",
      "note"
     ]
    },
    "provenance": "contract assets.yaml POST /media/{mediaId}/replace"
   },
   {
    "id": "formUpdateMediaAsset",
    "component": "modal",
    "trigger": "Save media asset",
    "body": "**Collects what `updateMediaAsset` sends before it is called.** Nothing in the body is required. Optional: `title`, `description`, `altText`, `tags`, `collectionIds`, `rights`, `status`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save media asset",
     "operation": "updateMediaAsset"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "title",
      "description",
      "altText",
      "tags",
      "collectionIds",
      "rights",
      "status"
     ]
    },
    "provenance": "contract assets.yaml PATCH /media/{mediaId}"
   }
  ],
  "states": {
   "loading": "The media list.",
   "error": "Could not load. Names which read failed and leaves the media untouched.",
   "emptyFirstRun": "No media yet. Offers Create collection (`createCollection`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on kind, tag, collectionId, venueId, search, unusedOnly and the media are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getMediaEntitlements",
    "contract": "orders",
    "purpose": "What is already on this media",
    "trigger": "onAction"
   },
   {
    "operationId": "searchMedia",
    "contract": "assets",
    "purpose": "Search the asset library",
    "trigger": "onLoad"
   },
   {
    "operationId": "appendEntitlementToMedia",
    "contract": "orders",
    "purpose": "Add something to a ticket the guest already holds",
    "trigger": "onAction",
    "invalidates": [
     "searchMedia"
    ]
   },
   {
    "operationId": "completeUpload",
    "contract": "assets",
    "purpose": "Confirm an upload and create the asset",
    "trigger": "onAction",
    "invalidates": [
     "searchMedia"
    ]
   },
   {
    "operationId": "createCollection",
    "contract": "assets",
    "purpose": "Create a collection",
    "trigger": "onAction",
    "invalidates": [
     "searchMedia"
    ]
   },
   {
    "operationId": "createUpload",
    "contract": "assets",
    "purpose": "Request a signed upload URL",
    "trigger": "onAction",
    "invalidates": [
     "searchMedia"
    ]
   },
   {
    "operationId": "deleteMediaAsset",
    "contract": "assets",
    "purpose": "Delete an asset",
    "trigger": "onAction",
    "invalidates": [
     "searchMedia"
    ]
   },
   {
    "operationId": "getExpiringRights",
    "contract": "assets",
    "purpose": "Assets whose licence is expiring or expired",
    "trigger": "onLoad"
   },
   {
    "operationId": "getMediaAsset",
    "contract": "assets",
    "purpose": "Read an asset with derivatives and usage",
    "trigger": "onAction"
   },
   {
    "operationId": "listCollections",
    "contract": "assets",
    "purpose": "List collections",
    "trigger": "onLoad"
   },
   {
    "operationId": "replaceMediaAsset",
    "contract": "assets",
    "purpose": "Replace the file behind an asset",
    "trigger": "onAction",
    "invalidates": [
     "searchMedia"
    ]
   },
   {
    "operationId": "updateMediaAsset",
    "contract": "assets",
    "purpose": "Amend metadata, tags or rights",
    "trigger": "onAction",
    "invalidates": [
     "searchMedia"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "mediaCode",
     "from": "deepLink"
    },
    {
     "name": "mediaId",
     "from": "deepLink"
    },
    {
     "name": "uploadId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `mediaCode`, `mediaId`, `uploadId`.",
   "preloaded": [
    "MediaAsset.id",
    "MediaAsset.kind",
    "MediaAsset.status",
    "MediaAsset.filename",
    "MediaAsset.contentType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-010"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 12 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
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
 "appendEntitlementToMedia": {
  "method": "POST",
  "path": "/media/{mediaCode}/entitlements",
  "contract": "orders",
  "summary": "Add something to a ticket the guest already holds",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AppendEntitlementRequest",
  "responds": "AppendEntitlementResult"
 },
 "completeUpload": {
  "method": "POST",
  "path": "/media/uploads/{uploadId}/complete",
  "contract": "assets",
  "summary": "Confirm an upload and create the asset",
  "permission": "ASSET_LIBRARY_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "MediaAsset"
 },
 "createBanner": {
  "method": "POST",
  "path": "/tenant-config/banners",
  "contract": "white-label",
  "summary": "Create a banner",
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
  "requestBody": "Banner",
  "responds": "Banner"
 },
 "createCollection": {
  "method": "POST",
  "path": "/media/collections",
  "contract": "assets",
  "summary": "Create a collection",
  "permission": "ASSET_LIBRARY_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Collection"
 },
 "createContentPage": {
  "method": "POST",
  "path": "/tenant-config/pages",
  "contract": "white-label",
  "summary": "Create a content page",
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
  "requestBody": "ContentPage",
  "responds": "ContentPage"
 },
 "createMenu": {
  "method": "POST",
  "path": "/menus",
  "contract": "fnb",
  "summary": "Create a menu",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateMenuRequest",
  "responds": "Menu"
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
 "createPromoBlock": {
  "method": "POST",
  "path": "/tenant-config/promo-blocks",
  "contract": "white-label",
  "summary": "Create a promotional block",
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
  "requestBody": "PromoBlock",
  "responds": "PromoBlock"
 },
 "createUpload": {
  "method": "POST",
  "path": "/media/uploads",
  "contract": "assets",
  "summary": "Request a signed upload URL",
  "permission": "ASSET_LIBRARY_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "UploadTicket"
 },
 "deleteBanner": {
  "method": "DELETE",
  "path": "/tenant-config/banners/{bannerId}",
  "contract": "white-label",
  "summary": "Delete a banner",
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
 "deleteContentPage": {
  "method": "DELETE",
  "path": "/tenant-config/pages/{pageId}",
  "contract": "white-label",
  "summary": "Delete a content page",
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
 "deleteMediaAsset": {
  "method": "DELETE",
  "path": "/media/{mediaId}",
  "contract": "assets",
  "summary": "Delete an asset",
  "permission": "ASSET_LIBRARY_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
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
 "deletePromoBlock": {
  "method": "DELETE",
  "path": "/tenant-config/promo-blocks/{promoBlockId}",
  "contract": "white-label",
  "summary": "Delete a promotional block",
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
 "getExpiringRights": {
  "method": "GET",
  "path": "/media/rights-expiring",
  "contract": "assets",
  "summary": "Assets whose licence is expiring or expired",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "withinDays",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ExpiringMedia"
 },
 "getFeatureToggles": {
  "method": "GET",
  "path": "/tenant-config/features",
  "contract": "white-label",
  "summary": "Read tenant feature toggles",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "FeatureToggle"
 },
 "getFonts": {
  "method": "GET",
  "path": "/tenant-config/fonts",
  "contract": "white-label",
  "summary": "Read font configuration",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "FontConfig"
 },
 "getHomepageLayout": {
  "method": "GET",
  "path": "/tenant-config/homepage",
  "contract": "white-label",
  "summary": "Read homepage layout",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "HomepageLayout"
 },
 "getMediaAsset": {
  "method": "GET",
  "path": "/media/{mediaId}",
  "contract": "assets",
  "summary": "Read an asset with derivatives and usage",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaAssetDetail"
 },
 "getMediaEntitlements": {
  "method": "GET",
  "path": "/media/{mediaCode}/entitlements",
  "contract": "orders",
  "summary": "What is already on this media",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaEntitlements"
 },
 "getMenu": {
  "method": "GET",
  "path": "/menus/{menuId}",
  "contract": "fnb",
  "summary": "Read a menu with sections and items",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Menu"
 },
 "getModuleEnablement": {
  "method": "GET",
  "path": "/tenant-config/modules",
  "contract": "white-label",
  "summary": "Read module enablement",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "ModuleEnablement"
 },
 "getTenantAppStatus": {
  "method": "GET",
  "path": "/tenant-config/status",
  "contract": "white-label",
  "summary": "App status and recent changes",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "TenantAppStatus"
 },
 "getTenantConfig": {
  "method": "GET",
  "path": "/tenant-config",
  "contract": "white-label",
  "summary": "Full working configuration",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "version",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TenantConfig"
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
 "listBanners": {
  "method": "GET",
  "path": "/tenant-config/banners",
  "contract": "white-label",
  "summary": "List banners",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "state",
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
 "listCollections": {
  "method": "GET",
  "path": "/media/collections",
  "contract": "assets",
  "summary": "List collections",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Collection"
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
 "listContentPages": {
  "method": "GET",
  "path": "/tenant-config/pages",
  "contract": "white-label",
  "summary": "List custom content pages",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryCode",
    "in": "query",
    "required": null
   },
   {
    "name": "slug",
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
 "listMenus": {
  "method": "GET",
  "path": "/menus",
  "contract": "fnb",
  "summary": "List menus",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "outletId",
    "in": "query",
    "required": null
   },
   {
    "name": "activeAt",
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
 "listPromoBlocks": {
  "method": "GET",
  "path": "/tenant-config/promo-blocks",
  "contract": "white-label",
  "summary": "List promotional blocks",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PromoBlock"
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
 "replaceMediaAsset": {
  "method": "POST",
  "path": "/media/{mediaId}/replace",
  "contract": "assets",
  "summary": "Replace the file behind an asset",
  "permission": "ASSET_LIBRARY_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "MediaReplaceResult"
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
 "searchMedia": {
  "method": "GET",
  "path": "/media",
  "contract": "assets",
  "summary": "Search the asset library",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "tag",
    "in": "query",
    "required": null
   },
   {
    "name": "collectionId",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "search",
    "in": "query",
    "required": null
   },
   {
    "name": "unusedOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "rightsExpiringWithinDays",
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
 "setFeatureToggles": {
  "method": "PUT",
  "path": "/tenant-config/features",
  "contract": "white-label",
  "summary": "Set feature toggles",
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
  "responds": "FeatureToggle"
 },
 "setFonts": {
  "method": "PUT",
  "path": "/tenant-config/fonts",
  "contract": "white-label",
  "summary": "Set fonts",
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
  "requestBody": "FontConfig",
  "responds": "FontConfig"
 },
 "setFooter": {
  "method": "PUT",
  "path": "/footer",
  "contract": "white-label",
  "summary": "Footer columns, legal links and social",
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
  "requestBody": "FooterConfig",
  "responds": "FooterConfig"
 },
 "setHeader": {
  "method": "PUT",
  "path": "/tenant-config/header",
  "contract": "white-label",
  "summary": "Configure the header",
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
  "requestBody": "HeaderConfig",
  "responds": "HeaderConfig"
 },
 "setHomepageLayout": {
  "method": "PUT",
  "path": "/tenant-config/homepage",
  "contract": "white-label",
  "summary": "Set homepage section order",
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
  "requestBody": "HomepageLayout",
  "responds": "HomepageLayout"
 },
 "setMaintenanceMode": {
  "method": "PUT",
  "path": "/tenant-config/status",
  "contract": "white-label",
  "summary": "Enable or clear maintenance mode, and set the live app status",
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
  "responds": "TenantAppStatus"
 },
 "setMenuSections": {
  "method": "PUT",
  "path": "/menus/{menuId}/sections",
  "contract": "fnb",
  "summary": "Set menu sections and their item ordering",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Menu"
 },
 "setModuleEnablement": {
  "method": "PUT",
  "path": "/tenant-config/modules",
  "contract": "white-label",
  "summary": "Enable or disable modules",
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
  "responds": "ModuleEnablement"
 },
 "setNavigation": {
  "method": "PUT",
  "path": "/tenant-config/navigation",
  "contract": "white-label",
  "summary": "Set main and overflow navigation",
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
  "requestBody": "NavigationConfig",
  "responds": "NavigationConfig"
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
   }
  ],
  "requestBody": "Theme",
  "responds": "Theme"
 },
 "updateBanner": {
  "method": "PATCH",
  "path": "/tenant-config/banners/{bannerId}",
  "contract": "white-label",
  "summary": "Amend or activate a banner",
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
  "responds": "Banner"
 },
 "updateContentPage": {
  "method": "PUT",
  "path": "/tenant-config/pages/{pageId}",
  "contract": "white-label",
  "summary": "Amend a content page",
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
  "requestBody": "UpdateContentPageRequest",
  "responds": "ContentPage"
 },
 "updateMediaAsset": {
  "method": "PATCH",
  "path": "/media/{mediaId}",
  "contract": "assets",
  "summary": "Amend metadata, tags or rights",
  "permission": "ASSET_LIBRARY_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "MediaAsset"
 },
 "updateMenu": {
  "method": "PATCH",
  "path": "/menus/{menuId}",
  "contract": "fnb",
  "summary": "Amend a menu",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Menu"
 },
 "updatePromoBlock": {
  "method": "PATCH",
  "path": "/tenant-config/promo-blocks/{promoBlockId}",
  "contract": "white-label",
  "summary": "Amend a promotional block",
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
  "responds": "PromoBlock"
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
 "AppendEntitlementRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "lines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of the new order this creates, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "variantId",
      "quantity"
     ],
     "properties": {
      "variantId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "integer",
       "minimum": 1
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "paymentMethod": {
    "type": "string",
    "enum": [
     "card",
     "cash",
     "wallet",
     "giftCard",
     "chargeToAccount"
    ]
   },
   "note": {
    "type": "string",
    "maxLength": 300
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AppendEntitlementResult": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "required": [
   "order",
   "media"
  ],
  "properties": {
   "order": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Order"
     }
    ],
    "description": "A **new** order. The original is untouched — it was paid, receipted and possibly reported on, and editing it would move yesterday's revenue.\n"
   },
   "media": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MediaEntitlements"
     }
    ],
    "description": "The full set now on the media, so the cashier can say what the QR does."
   },
   "addedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   }
  }
 },
 "Banner": {
  "x-ticvai-persistence": "whitelabel.banner",
  "type": "object",
  "required": [
   "id",
   "title",
   "imageAssetRef",
   "startsAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "subtitle": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "imageAssetRef": {
    "type": "string",
    "format": "uuid"
   },
   "placement": {
    "type": "string",
    "enum": [
     "homepageHero",
     "homepageBlock",
     "explore",
     "checkout"
    ]
   },
   "linkTarget": {
    "$ref": "#/components/schemas/LinkTarget"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Must follow `startsAt` when set (decided 28 September, audit R163). Null runs the banner with no end."
   },
   "state": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ScheduleState"
     }
    ],
    "readOnly": true,
    "x-ticvai-derived": "sweeper",
    "description": "Moved by `updateBanner` between `draft` and `scheduled`, and by the schedule timer from `scheduled` to `active` and `active` to `expired` at `startsAt` and `endsAt`, in the tenant's timezone (`states/schedule.yaml`)."
   },
   "sortOrder": {
    "type": "integer"
   },
   "isActive": {
    "type": "boolean"
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
   }
  }
 },
 "ChangeScope": {
  "type": "string",
  "description": "Whether a change reaches guests on publish or needs a store release.\n",
  "enum": [
   "runtime",
   "buildTime"
  ]
 },
 "Collection": {
  "x-ticvai-persistence": "assets.media_collection",
  "type": "object",
  "required": [
   "id",
   "name",
   "assetCount"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "x-ticvai-unique": "tenant",
    "description": "**Unique per tenant** (decided 28 September, audit R108). A name already used by any collection in the tenant, at any venue or level, is refused with `409 duplicate-code`.\n"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "parentCollectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assetCount": {
    "type": "integer"
   },
   "coverAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
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
 "ContentPage": {
  "x-ticvai-persistence": "whitelabel.content_page",
  "type": "object",
  "required": [
   "id",
   "slug",
   "title",
   "body",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "slug": {
    "type": "string",
    "pattern": "^[a-z0-9-]+$"
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "body": {
    "$ref": "#/components/schemas/LocalisedRichText"
   },
   "isEnabled": {
    "type": "boolean",
    "default": true,
    "description": "BL-005. **Enablement is not publication.** A published page that is disabled exists, keeps its URL and its history, and does not render — which is what a tenant wants when a section is seasonal.\n**Unpublishing loses the version; disabling does not.** Collapsing them means a venue turning off its water-park section for winter has to republish it every spring.\n"
   },
   "status": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ContentStatus"
     }
    ],
    "readOnly": true,
    "description": "Created as `draft`, published by `publishTenantConfig`, archived through `updateContentPage` (`states/content.yaml`)."
   },
   "iconAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "categoryCode": {
    "type": "string",
    "nullable": true
   },
   "sortOrder": {
    "type": "integer"
   },
   "isReferenced": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "True when navigation or the homepage links to this page. Blocks deletion. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "ContentStatus": {
  "type": "string",
  "enum": [
   "draft",
   "published",
   "archived"
  ]
 },
 "CreateMenuRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "outletId"
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
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "availability": {
    "$ref": "#/components/schemas/MenuAvailability"
   }
  }
 },
 "EntitlementStatus": {
  "type": "string",
  "description": "**What the storage layer holds, and what a guest is shown.** `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot distinguish a ticket that was used from one that expired, was refunded, or was transferred to somebody else, and those are four different conversations at a gate.\nAdded 17 August. `states/entitlement.yaml` had modelled these six since 14 August and the contract had no enum behind it, which the state checker reported correctly for three days.\n",
  "enum": [
   "issued",
   "partiallyConsumed",
   "fullyConsumed",
   "expired",
   "cancelled",
   "surrendered"
  ]
 },
 "ExpiringMedia": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "assetId",
   "filename",
   "validTo",
   "isExpired",
   "isInUse"
  ],
  "properties": {
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "filename": {
    "type": "string"
   },
   "thumbnailUrl": {
    "type": "string",
    "nullable": true
   },
   "licensor": {
    "type": "string",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date"
   },
   "daysRemaining": {
    "type": "integer"
   },
   "isExpired": {
    "type": "boolean"
   },
   "isInUse": {
    "type": "boolean",
    "description": "True while `liveUsageCount` is above zero, that is, while live (published) content references the asset (audit R106 (10)). Drafts and collections do not count."
   },
   "liveUsageCount": {
    "type": "integer",
    "description": "References from live (published) content only (audit R106 (10)). Expired and live is the combination that matters."
   }
  }
 },
 "FeatureKey": {
  "type": "string",
  "description": "The feature toggles a tenant can set — one list for `FeatureToggle` and the `setFeatureToggles` body, which took a free string where the response had this enum.\n",
  "enum": [
   "digitalCompanionMode",
   "aiConciergeChat",
   "lostAndFound",
   "pushNotifications",
   "socialSharing",
   "multiLanguage",
   "appleWallet",
   "googlePay",
   "applePay",
   "cashOnDelivery",
   "guestCheckout",
   "uaePassLogin"
  ]
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
       "nullable": true
      }
     }
    }
   }
  }
 },
 "HomepageSectionKind": {
  "type": "string",
  "description": "**Which module each section needs, proposed, client to correct (decided 28 September, audit R163).** `tickets` needs `ticketsAndBooking`; `whatsOn` needs `events`; `attractions` needs `attractions`; `membership` needs `membership`; `dining` needs `diningAndFnb`; `shop` needs `shop`; `map` needs `map`. `heroBanner`, `quickActions`, `promotions`, `customContent` and `spacer` need no module. `setHomepageLayout` refuses a visible section whose module is not enabled, and `setModuleEnablement` refuses to disable a module a section still needs.\n",
  "enum": [
   "heroBanner",
   "quickActions",
   "tickets",
   "whatsOn",
   "attractions",
   "membership",
   "dining",
   "shop",
   "promotions",
   "map",
   "customContent",
   "spacer"
  ]
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
 "LinkTarget": {
  "x-ticvai-persistence": "none — embedded",
  "type": "object",
  "required": [
   "kind"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "module",
     "contentPage",
     "product",
     "event",
     "externalUrl",
     "none"
    ]
   },
   "moduleKey": {
    "$ref": "#/components/schemas/ModuleKey"
   },
   "contentPageId": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "url": {
    "type": "string"
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
 "MediaAsset": {
  "x-ticvai-persistence": "assets.media_asset",
  "type": "object",
  "required": [
   "id",
   "kind",
   "status",
   "filename",
   "contentType",
   "sizeBytes",
   "referenceCount",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MediaKind"
   },
   "status": {
    "$ref": "#/components/schemas/MediaStatus"
   },
   "filename": {
    "type": "string"
   },
   "contentType": {
    "type": "string"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "description": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"
   },
   "altText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "Required before use in a guest-facing surface. WCAG 2.2 AA."
   },
   "width": {
    "type": "integer",
    "nullable": true
   },
   "height": {
    "type": "integer",
    "nullable": true
   },
   "durationSeconds": {
    "type": "number",
    "nullable": true
   },
   "customMetadata": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true,
    "description": "BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"
   },
   "sharedWithTenantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "url": {
    "type": "string",
    "description": "Signed and expiring for private assets; stable CDN URL for public ones."
   },
   "thumbnailUrl": {
    "type": "string",
    "nullable": true
   },
   "referenceCount": {
    "type": "integer",
    "description": "How many surfaces reference this asset. Non-zero refuses deletion.\n"
   },
   "rights": {
    "$ref": "#/components/schemas/MediaRights"
   },
   "isRightsExpired": {
    "type": "boolean"
   },
   "version": {
    "type": "integer"
   },
   "uploadedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "MediaAssetDetail": {
  "x-ticvai-persistence": "assets.media_asset",
  "allOf": [
   {
    "$ref": "#/components/schemas/MediaAsset"
   },
   {
    "type": "object",
    "properties": {
     "derivatives": {
      "type": "array",
      "description": "Generated from the original, never uploaded separately. A new breakpoint is a re-render rather than a re-upload of everything.\n",
      "items": {
       "type": "object",
       "properties": {
        "label": {
         "type": "string"
        },
        "width": {
         "type": "integer"
        },
        "height": {
         "type": "integer"
        },
        "sizeBytes": {
         "type": "integer"
        },
        "url": {
         "type": "string"
        }
       }
      }
     },
     "usage": {
      "type": "array",
      "description": "Every place this asset is referenced.",
      "items": {
       "$ref": "#/components/schemas/MediaUsage"
      }
     },
     "collections": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "id": {
         "type": "string",
         "format": "uuid"
        },
        "name": {
         "type": "string"
        }
       }
      }
     },
     "previousVersions": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "version": {
         "type": "integer"
        },
        "replacedAt": {
         "type": "string",
         "format": "date-time"
        },
        "replacedByPrincipalId": {
         "type": "string",
         "format": "uuid"
        }
       }
      }
     }
    }
   }
  ]
 },
 "MediaEntitlements": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over entitlement and scan history",
  "required": [
   "mediaCode",
   "isValid",
   "entitlements"
  ],
  "properties": {
   "mediaCode": {
    "type": "string"
   },
   "mediaKind": {
    "type": "string",
    "enum": [
     "qr",
     "wristband",
     "card",
     "nfc",
     "mobilePass"
    ]
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isValid": {
    "type": "boolean"
   },
   "invalidReason": {
    "type": "string",
    "nullable": true
   },
   "canAcceptMore": {
    "type": "boolean",
    "description": "False where the media has been surrendered, expired or blocked. A cashier should know before taking money, not after.\n"
   },
   "entitlements": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "entitlementId": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
      },
      "name": {
       "type": "string"
      },
      "kind": {
       "type": "string",
       "enum": [
        "admission",
        "locker",
        "fnb",
        "retail",
        "parking",
        "rental",
        "experience",
        "membership"
       ]
      },
      "orderId": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
      },
      "addedAt": {
       "type": "string",
       "format": "date-time"
      },
      "status": {
       "allOf": [
        {
         "$ref": "#/components/schemas/EntitlementStatus"
        }
       ],
       "description": "**Replaced `isRedeemed` on 17 August.** A boolean could not distinguish a ticket that was used from one that expired, was refunded, or was transferred — four different conversations at a gate, and the steward could see only \"not valid\".\n"
      },
      "entriesUsed": {
       "type": "integer"
      },
      "entriesAllowed": {
       "type": "integer",
       "nullable": true
      },
      "redeemedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "transferredToSubjectId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "validTo": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "MediaKind": {
  "type": "string",
  "enum": [
   "image",
   "video",
   "audio",
   "document",
   "vector",
   "font",
   "archive"
  ]
 },
 "MediaReplaceResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "asset",
   "affectedSurfaces"
  ],
  "properties": {
   "asset": {
    "$ref": "#/components/schemas/MediaAsset"
   },
   "affectedSurfaces": {
    "type": "integer",
    "description": "How many surfaces now show the new file."
   },
   "liveSurfaces": {
    "type": "integer",
    "description": "Of those, how many are published to guests right now."
   },
   "derivativesRegenerating": {
    "type": "boolean"
   }
  }
 },
 "MediaRights": {
  "x-ticvai-persistence": "none — embedded in asset",
  "type": "object",
  "description": "Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n",
  "properties": {
   "licenceKind": {
    "type": "string",
    "enum": [
     "owned",
     "royaltyFree",
     "rightsManaged",
     "creativeCommons",
     "editorialOnly",
     "unknown"
    ]
   },
   "licensor": {
    "type": "string",
    "nullable": true
   },
   "licenceReference": {
    "type": "string",
    "nullable": true
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "permittedUses": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "web",
      "print",
      "socialMedia",
      "inVenue",
      "advertising",
      "internal"
     ]
    }
   },
   "attributionRequired": {
    "type": "boolean",
    "default": false
   },
   "attributionText": {
    "type": "string",
    "nullable": true
   },
   "permittedTerritories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"
   },
   "permittedChannels": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"
   },
   "modelReleaseHeld": {
    "type": "boolean",
    "default": false
   },
   "renewalOwner": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "MediaStatus": {
  "type": "string",
  "enum": [
   "processing",
   "ready",
   "quarantined",
   "failed",
   "archived"
  ]
 },
 "MediaUsage": {
  "x-ticvai-persistence": "assets.media_usage",
  "type": "object",
  "description": "One place an asset is used. **`surface: product` is written by catalogue** for each item of `Product.media` (decided 29 September, rev 3 23SEP-4): `referenceId` is the product id and `isLive` is true while the product is listed to guests, which is what stops an asset in use on a ticket card being archived from under it.\n",
  "required": [
   "surface",
   "referenceId"
  ],
  "properties": {
   "extractedText": {
    "type": "string",
    "description": "**Text pulled out of an uploaded document**, after extraction. The generic retrieval path for anything a tenant uploads — a PDF nobody can search is a PDF nobody reads.\n"
   },
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "surface": {
    "type": "string",
    "enum": [
     "tenantBranding",
     "homepageBanner",
     "promoBlock",
     "contentPage",
     "product",
     "event",
     "menuItem",
     "merchandise",
     "workOrder",
     "incident",
     "inspection",
     "campaign"
    ]
   },
   "referenceId": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "isLive": {
    "type": "boolean",
    "description": "True where the referencing surface is published to guests."
   }
  }
 },
 "Menu": {
  "x-ticvai-persistence": "fnb.menu",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "outletId",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "availability": {
    "$ref": "#/components/schemas/MenuAvailability"
   },
   "sections": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/MenuSection"
    }
   },
   "isActive": {
    "type": "boolean"
   },
   "publishedVersion": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "The `MenuVersion.version` live now. Null for a menu never published."
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "MenuAvailability": {
  "x-ticvai-persistence": "none — embedded in menu",
  "type": "object",
  "description": "When this menu is in force. Absent means always. Days, times and dates are all read in the Region's time zone, not UTC.",
  "properties": {
   "daysOfWeek": {
    "type": "array",
    "items": {
     "type": "integer",
     "minimum": 0,
     "maximum": 6
    }
   },
   "startTime": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
    "description": "Wall-clock time, in the Region's time zone."
   },
   "endTime": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
    "description": "Wall-clock time, in the Region's time zone."
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Calendar day, in the Region's time zone, not UTC."
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Calendar day, in the Region's time zone, not UTC."
   }
  }
 },
 "MenuSection": {
  "x-ticvai-persistence": "fnb.menu_section",
  "type": "object",
  "required": [
   "code",
   "name",
   "sortOrder"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "sortOrder": {
    "type": "integer"
   },
   "items": {
    "type": "array",
    "description": "The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`.",
    "items": {
     "$ref": "#/components/schemas/MenuItem"
    }
   }
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
   }
  }
 },
 "Order": {
  "x-ticvai-persistence": "orders.sales_order + orders.order_line",
  "type": "object",
  "required": [
   "id",
   "venueId",
   "scopePath",
   "channel",
   "status",
   "currency",
   "currencyScale",
   "grossAmount",
   "taxAmount",
   "netAmount",
   "lines",
   "createdAt",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The client ULID from `CreateOrderRequest.id`."
   },
   "orderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "droppedPromotions": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n",
    "items": {
     "type": "object",
     "required": [
      "promotionId"
     ],
     "properties": {
      "promotionId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "budgetCapReached"
       ]
      }
     }
    }
   },
   "totalPriceVariance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Sum across lines. Zero on a normal order."
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/OrderLine"
    }
   },
   "payments": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Payment"
    }
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "shiftId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "holdLabel": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "readOnly": true,
    "description": "The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."
   },
   "heldUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "PromoBlock": {
  "x-ticvai-persistence": "whitelabel.promo_block",
  "type": "object",
  "required": [
   "id",
   "title"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "description": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "iconAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "promotionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Presentation only. A block may point at a promotion; it does not create or price one.\n"
   },
   "linkTarget": {
    "$ref": "#/components/schemas/LinkTarget"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "endsAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Must follow `startsAt` when both are set (decided 28 September, audit R163)."
   },
   "state": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ScheduleState"
     }
    ],
    "readOnly": true,
    "x-ticvai-derived": "sweeper",
    "description": "Moved by the schedule timer at `startsAt` and `endsAt`, in the tenant's timezone, as for `Banner.state`. Once `active` or `expired` the block may only be withdrawn (audit R163)."
   },
   "sortOrder": {
    "type": "integer"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "ScheduleState": {
  "type": "string",
  "enum": [
   "draft",
   "scheduled",
   "active",
   "expired"
  ]
 },
 "TenantAppStatus": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "description": "Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n",
  "required": [
   "tenantId",
   "isPublished",
   "isInMaintenance"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "isPublished": {
    "type": "boolean",
    "x-ticvai-derived": "onRead",
    "description": "True once any version has been published."
   },
   "publishedVersion": {
    "type": "string",
    "nullable": true
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "draftVersion": {
    "type": "string",
    "description": "Staff only."
   },
   "hasUnpublishedChanges": {
    "type": "boolean",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. The working draft differs from the current version's `snapshot`."
   },
   "activeModuleCount": {
    "type": "integer",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. `ModuleEnablement` rows with `isEnabled` true."
   },
   "licensedModuleCount": {
    "type": "integer",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. `ModuleEnablement` rows with `isLicensed` true."
   },
   "activePageCount": {
    "type": "integer",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. Content pages that are `published` and enabled."
   },
   "isInMaintenance": {
    "type": "boolean"
   },
   "maintenanceMessage": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "expectedBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "minimumAppVersion": {
    "$ref": "#/components/schemas/MinimumAppVersion"
   },
   "contact": {
    "$ref": "#/components/schemas/VenueContact"
   },
   "availability": {
    "$ref": "#/components/schemas/AppAvailability"
   },
   "availabilityMessage": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "What the sold-out or closed screen says (WEB-029). Null shows the default wording."
   },
   "venues": {
    "type": "array",
    "maxItems": 200,
    "x-ticvai-derived": "onRead",
    "description": "**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n",
    "items": {
     "type": "object",
     "required": [
      "venueId",
      "name"
     ],
     "properties": {
      "venueId": {
       "type": "string",
       "format": "uuid",
       "description": "**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."
      },
      "name": {
       "type": "string",
       "maxLength": 200,
       "description": "The venue's name (`tenancy.OrgUnit.name`)."
      },
      "city": {
       "type": "string",
       "maxLength": 120,
       "nullable": true,
       "description": "Shown under the name so two venues with similar names can be told apart."
      },
      "openingHoursToday": {
       "type": "object",
       "nullable": true,
       "description": "Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.",
       "properties": {
        "opens": {
         "type": "string",
         "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$"
        },
        "closes": {
         "type": "string",
         "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$"
        }
       }
      }
     }
    }
   },
   "whatsNew": {
    "type": "array",
    "maxItems": 10,
    "x-ticvai-derived": "onRead",
    "description": "**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n",
    "items": {
     "type": "object",
     "required": [
      "version",
      "publishedAt",
      "notes"
     ],
     "properties": {
      "version": {
       "type": "string",
       "description": "The release version."
      },
      "publishedAt": {
       "type": "string",
       "format": "date-time",
       "description": "When the release reached the tenant's cell."
      },
      "notes": {
       "$ref": "#/components/schemas/LocalisedText"
      }
     }
    }
   },
   "recentChanges": {
    "type": "array",
    "description": "Staff only. Names the principal behind each change, so it never reaches a public response.",
    "items": {
     "type": "object",
     "properties": {
      "area": {
       "type": "string"
      },
      "description": {
       "type": "string"
      },
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "at": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
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
   }
  }
 },
 "UpdateContentPageRequest": {
  "x-ticvai-persistence": "none — request only; the fields land on whitelabel.content_page",
  "type": "object",
  "description": "The body of `updateContentPage`: the fields a tenant edits. `id`, `isReferenced` and `scopePath` are the server's, and `status` moves only to `archived` here — publishing is `publishTenantConfig` (`states/content.yaml`).\n",
  "required": [
   "slug",
   "title",
   "body"
  ],
  "properties": {
   "slug": {
    "type": "string",
    "pattern": "^[a-z0-9-]+$"
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "body": {
    "$ref": "#/components/schemas/LocalisedRichText"
   },
   "isEnabled": {
    "type": "boolean",
    "default": true
   },
   "iconAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "categoryCode": {
    "type": "string",
    "nullable": true
   },
   "sortOrder": {
    "type": "integer"
   },
   "status": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ContentStatus"
     }
    ],
    "description": "Only `archived` is taken — send it to withdraw a published page or abandon a draft (`states/content.yaml`). Any other value is a 400 `validation`. Omit to leave the status as it is."
   }
  }
 },
 "UploadTicket": {
  "x-ticvai-persistence": "assets.media_upload",
  "type": "object",
  "required": [
   "uploadId",
   "uploadUrl",
   "method",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "uploadId": {
    "type": "string",
    "format": "uuid"
   },
   "uploadUrl": {
    "type": "string",
    "description": "Signed. PUT the file here, then confirm with `/complete`."
   },
   "method": {
    "type": "string",
    "enum": [
     "PUT",
     "POST"
    ]
   },
   "headers": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "maxSizeBytes": {
    "type": "integer"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "filename": {
    "type": "string"
   },
   "contentType": {
    "type": "string"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The asset this upload became — created by `completeUpload`, or the asset whose file `replaceMediaAsset` swapped. Null while the transfer is outstanding.\n"
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
 }
}
```
