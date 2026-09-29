# CMS-FLOW-BUILDER — P13 · CMS flow builder (Site Builder, Booking Flows, App Publishing, Help me choose, and the step screens they open)

**17 screens · 84 operations · 88 schemas · 8 permissions**

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
  `AI_USE, ASSET_LIBRARY_MANAGE, GUEST_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, SCOPE_VIEW, TENANT_CONFIGURE, TENANT_PUBLISH`. A control nobody can use must say so,
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
| `CMS-007` | Page Builder | statusTracker | 11 | 4 | — |
| `CMS-008` | Content Blocks | listDetail | 10 | 5 | — |
| `CMS-009` | Navigation & Menus | listDetail | 7 | 4 | — |
| `CMS-012` | RTL Preview | statusTracker | 2 | 0 | — |
| `CMS-014` | Publishing Workflow | statusTracker | 4 | 1 | — |
| `CMS-015` | Version History | listDetail | 3 | 1 | — |
| `CMS-016` | Site Settings | statusTracker | 6 | 1 | — |
| `CMS-101` | Help Me Choose | listDetail | 12 | 3 | — |
| `CMS-102` | Site Builder | multiStepForm | 7 | 1 | — |
| `CMS-103` | Booking Flows | listDetail | 14 | 3 | — |
| `CMS-104` | App Build & Store Publishing | listDetail | 7 | 2 | — |

## Thin screens in this batch

**CMS-005, CMS-012 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
    "CMS-091",
    "CMS-102"
   ],
   "inferred": true,
   "isEntryPoint": true,
   "transitions": [
    {
     "to": "CMS-102",
     "trigger": "Site Builder",
     "provenance": "authored 29 September, W12 and M24-05 (the step-based builder starts from the workspace)"
    },
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
     "provenance": "derived — CMS-008 declares entryState.params actionId, bannerId, promoBlockId and CMS-001 holds none of them, so the edge carries nothing and CMS-008 opens cold"
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
  "purpose": "Land a tenant somewhere that shows what is live and what is not, and hold step 1 of the Site Builder (venue and modules).",
  "purposeNote": "**Step 1 of CMS-102 Site Builder (decided 29 September, W12).** The modules and feature toggles here, including `guestCheckout` (which fields its pop-up asks is `guestContactFields` on CMS-016, W1) and the new `visitPlanner` module, which shows or hides the mobile Plan tab and WEB-050 (MOB-1). A Site Builder card leads new tenants into the seven steps.",
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
  "purpose": "Hold the marks every surface needs, at the sizes it needs them, and the mobile app's intro video (Site Builder steps 5 and 6).",
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
        "BrandIdentity.splashChangeScope",
        "BrandIdentity.introVideoAssetRef",
        "BrandIdentity.introVideoMode"
       ],
       "operation": "getBrandIdentity",
       "notes": "**Intro video (decided 29 September, MOB-5).** Picked from the media library (CMS-010); plays off, on first launch or on every launch, always with Skip introduction. Streamed, so it needs no app build, unlike the splash and icons.",
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
    "body": "**Collects what `setBrandIdentity` sends before it is called.** Required: `logoAssetRef`. Optional: `logoVariant` (light, dark or duotone: which lockup sits in the nav bar and which colour reading of it drives the theme, decided 29 September, rev 3 CFG-4), `logoDarkAssetRef`, `faviconAssetRef`, `splashImageAssetRefs`, `splashDurationSeconds`, `splashBackgroundColour`, `showLoadingIndicator`, `splashChangeScope`, `introVideoAssetRef` and `introVideoMode` (off, first launch or every launch; MOB-5). Dismissing sends nothing; the screen behind is unchanged.",
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
      "splashChangeScope",
      "introVideoAssetRef",
      "introVideoMode"
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
        "Theme.buttonStyle",
        "Theme.componentColours"
       ],
       "operation": "getTheme",
       "notes": "**Per-element colours (decided 17 September, M17-11).** Pickers for the main call to action, the pay button, add to cart, the Buy tickets button, links and badges, each with a live contrast warning; left empty they follow the theme. The guest flow itself stays standard.",
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
    "body": "**Collects what `setTheme` sends before it is called.** Required: `primaryColour`, `secondaryColour`, `backgroundColour`, `textColour`. Optional: `accentColour`, `darkMode`, `cornerRadius`, `surfaceStyle` (glass or solid, default glass) and `buttonStyle` (solid, outline or pill, default solid; decided 29 September, rev 3 CFG-3) and `componentColours` (M17-11). **A colour pair that fails contrast is refused** (`400 ContrastProblem`, decided 28 September, audit R139 (a)): the modal stays open with the failing pairs marked. Dismissing sends nothing; the screen behind is unchanged.",
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
      "buttonStyle",
      "componentColours"
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
       "notes": "**Also the mobile Home editor (decided 29 September, MOB-3; Site Builder steps 5 and 6).** The `venueOverview` section (description, opening hours, type tiles), the hero's style (carousel, video, poster or split) and 1 or 2 highlights for attractions, dining, what's on and shop (`maxItems`). The header and footer are set here too (`setHeader`, `setFooter`).",
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
   },
   {
    "operationId": "proposeMarketingContent",
    "contract": "ai",
    "purpose": "Draft subject lines, message bodies or content variants from a brief, for the author to edit and apply",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideProposedAction",
    "contract": "ai",
    "purpose": "Record which AI draft or proposal was used, or why it was refused",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
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
    },
    {
     "name": "actionId",
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
  "purpose": "Define what a block can and cannot contain, and set the banners (Site Builder step 5).",
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
   },
   {
    "operationId": "proposeMarketingContent",
    "contract": "ai",
    "purpose": "Draft subject lines, message bodies or content variants from a brief, for the author to edit and apply",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideProposedAction",
    "contract": "ai",
    "purpose": "Record which AI draft or proposal was used, or why it was refused",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
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
    },
    {
     "name": "actionId",
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
  "purpose": "Decide what appears in the header, the footer and the mobile tab bar, with the Buy tickets button (Site Builder steps 5 and 6).",
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
     "name": "navigationEditor",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Navigation and mobile tabs",
       "bindsTo": "NavigationConfig",
       "columns": [
        "NavigationConfig.kind",
        "NavigationConfig.items",
        "NavigationConfig.buyButton"
       ],
       "operation": "getNavigation",
       "notes": "**The mobile tab editor (decided 29 September, MOB-1 and MOB-2).** Which tabs, their order, labels and icons; each tab is an `appSection` link. The default is Home, Explore, Plan and Tickets; Map is optional; Plan needs the `visitPlanner` module. The Buy tickets button: raised in the centre (default), floating, flat or hidden, and its label. At most five tabs are visible.",
       "provenance": "contract white-label.yaml GET /tenant-config/navigation"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Save navigation and tabs",
       "operation": "setNavigation",
       "provenance": "contract white-label.yaml PUT /tenant-config/navigation"
      },
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
    "operationId": "getNavigation",
    "contract": "white-label",
    "purpose": "The navigation and the mobile tab set (MOB-1)",
    "trigger": "onLoad"
   },
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
    "purpose": "Save the navigation, the mobile tabs and the Buy tickets button (MOB-1, MOB-2)",
    "trigger": "onAction",
    "invalidates": [
     "getNavigation"
    ],
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
    "id": "formSetNavigation",
    "component": "modal",
    "trigger": "Save navigation and tabs",
    "body": "**Collects what `setNavigation` sends.** Required: `kind`, `items` (label, icon, target, visible, order; a mobile tab targets an `appSection`). Optional: `buyButton` (`style`, `label`). Refused `400` when a tab targets a disabled module or more than five are visible. Dismissing sends nothing.",
    "bindsTo": "NavigationConfig",
    "confirm": {
     "label": "Save navigation",
     "operation": "setNavigation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "items",
      "buyButton"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/navigation"
   },
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
  "id": "CMS-012",
  "name": "RTL Preview",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/rtl-preview",
   "component": "apps/venue-management-web/src/routes/white-label/RtlPreviewDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003",
    "CMS-014"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "CMS-014",
     "trigger": "Publishes",
     "provenance": "flow F22 step 4→5"
    },
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-012 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-012 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "version"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-012 holds version, so an edge into it carries them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getTenantConfig` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "See the site as an Arabic reader sees it.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The tenant config",
       "bindsTo": "TenantConfig",
       "columns": [
        "TenantConfig.isDraft",
        "TenantConfig.brand",
        "TenantConfig.appIcons",
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
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Validate tenant config",
       "operation": "validateTenantConfig",
       "provenance": "contract white-label.yaml POST /tenant-config/validate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rtl preview, read by `getTenantConfig`.",
   "error": "Could not load. Names which read failed and leaves the rtl preview untouched.",
   "emptyFirstRun": "No rtl preview yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `getTenantConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getTenantConfig",
    "contract": "white-label",
    "purpose": "Full working configuration",
    "trigger": "onLoad"
   },
   {
    "operationId": "validateTenantConfig",
    "contract": "white-label",
    "purpose": "Validate the working draft",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-012"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "CMS-014",
  "name": "Publishing Workflow",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/publishing-workflow",
   "component": "apps/venue-management-web/src/routes/white-label/PublishingWorkflowDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003",
    "CMS-015",
    "CMS-103",
    "CMS-104",
    "CMS-102"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-014 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-014 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "version"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-014 holds version, so an edge into it carries them"
    },
    {
     "to": "CMS-103",
     "trigger": "Fix a booking flow",
     "provenance": "authored 29 September, W12 (an invalid flow blocks the publish)",
     "carries": [
      "bookingFlowId"
     ]
    },
    {
     "to": "CMS-104",
     "trigger": "Build the mobile app",
     "provenance": "authored 29 September, M24-08 (build-time changes reach guests with a store release)"
    },
    {
     "to": "CMS-102",
     "trigger": "Back to the Site Builder",
     "provenance": "authored 29 September, W12 (step 7)"
    },
    {
     "to": "CMS-015",
     "trigger": "Rolls back when something is wrong",
     "provenance": "flow F22 step 5→6",
     "carries": [
      "version"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.\n\n**A rollback arrives here as a draft (decided 28 September, audit R139 (b)).** Version History (CMS-015) restores an old version into the working draft with `restoreConfigVersion` and reviews it with `diffConfigVersion`; only this screen's `publishTenantConfig` puts it live, with a note. A rollback is never one click.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getTenantAppStatus` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Move a change from draft to live, with someone accountable (Site Builder step 7).",
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
        "TenantAppStatus.recentChanges"
       ],
       "operation": "getTenantAppStatus",
       "provenance": "contract white-label.yaml GET /tenant-config/status"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishTenantConfig",
       "notes": "Declares `publishTenantConfig`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate. **Booking flows publish here with the rest of the site (decided 29 September, W12)**: the gate lists each venue flow that changed, and an invalid one (`bookingFlowInvalid`) or a bookable kind with no flow (`bookingFlowMissing`) blocks the publish with a link to CMS-103.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish tenant config",
       "operation": "publishTenantConfig",
       "provenance": "contract white-label.yaml POST /tenant-config/publish"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate tenant config",
       "operation": "validateTenantConfig",
       "provenance": "contract white-label.yaml POST /tenant-config/validate"
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
   "loading": "The publishing workflow, read by `getTenantAppStatus`.",
   "error": "Could not load. Names which read failed and leaves the publishing workflow untouched.",
   "emptyFirstRun": "No publishing workflow yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_PUBLISH`, which `publishTenantConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishTenantConfig",
    "contract": "white-label",
    "purpose": "Publish the working draft",
    "trigger": "onAction"
   },
   {
    "operationId": "validateTenantConfig",
    "contract": "white-label",
    "purpose": "Validate the working draft",
    "trigger": "onAction"
   },
   {
    "operationId": "getTenantAppStatus",
    "contract": "white-label",
    "purpose": "App status and recent changes",
    "trigger": "onLoad"
   },
   {
    "operationId": "listBookingFlows",
    "contract": "white-label",
    "purpose": "The venue's flows and whether each is valid, for the gate (W12)",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-014"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
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
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ]
  },
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
  "id": "CMS-015",
  "name": "Version History",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/version-history",
   "component": "apps/venue-management-web/src/routes/white-label/VersionHistoryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-001",
    "CMS-014"
   ],
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003",
    "CMS-014"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-015 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-015 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "version"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-015 holds version, so an edge into it carries them"
    },
    {
     "to": "CMS-014",
     "trigger": "Review and publish the restored draft",
     "provenance": "decided 28 September, audit R139 (b) — a restore lands in the working draft, and the publish is a separate, deliberate step"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.\n\n**Absorbed CMS-020 on 28 September (audit R276)**: the Change Log listed the same `listConfigVersions` rows (who published what, when, with which note) and nothing else, so it brought no operation; its entry from the Tenant Workspace (CMS-001) now lands here.\n\n**Rollback is restore, then review, then publish — never one click (decided 28 September, audit R139 (b)).** **Restore config version** calls `restoreConfigVersion`, which copies the chosen version into the working draft and publishes nothing. The screen then shows **Diff config version** of the live version against the restored draft (`diffConfigVersion`) as the review, and **Review and publish the restored draft** goes to the Publishing Workflow (CMS-014), where `publishTenantConfig` puts it live with a note.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listConfigVersions` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "See who changed what and go back if it was wrong — by restoring into the draft, reviewing, then publishing.",
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
       "label": "Diff config version",
       "operation": "diffConfigVersion",
       "notes": "After a restore this is the review step — the live version against the restored draft — before anything is published (decided 28 September, audit R139 (b)).",
       "provenance": "contract white-label.yaml GET /tenant-config/versions/{version}/diff"
      },
      {
       "kind": "secondaryButton",
       "label": "Restore config version",
       "operation": "restoreConfigVersion",
       "notes": "Restores into the working draft only; nothing goes live until it is reviewed and published on CMS-014 (decided 28 September, audit R139 (b)).",
       "provenance": "contract white-label.yaml POST /tenant-config/versions/{version}/restore"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The version history list.",
   "error": "Could not load. Names which read failed and leaves the version history untouched.",
   "emptyFirstRun": "No version history yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listConfigVersions` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listConfigVersions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listConfigVersions",
    "contract": "white-label",
    "purpose": "Version history",
    "trigger": "onLoad"
   },
   {
    "operationId": "diffConfigVersion",
    "contract": "white-label",
    "purpose": "Compare a version against the working draft",
    "trigger": "onAction"
   },
   {
    "operationId": "restoreConfigVersion",
    "contract": "white-label",
    "purpose": "Restore a previous version into the working draft; it does not publish (audit R139 (b))",
    "trigger": "onAction",
    "invalidates": [
     "listConfigVersions"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "version",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `version`.",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-015"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "confirmRestoreConfigVersion",
    "component": "confirmDialog",
    "trigger": "Restore config version",
    "body": "**Restores the chosen version into the working draft and publishes nothing** (decided 28 September, audit R139 (b)). Names the version and says that any unpublished changes in the draft are replaced. Guests keep seeing the live version until the restored draft is reviewed (`diffConfigVersion`) and published on CMS-014.",
    "confirm": {
     "label": "Restore into draft",
     "operation": "restoreConfigVersion"
    },
    "dismiss": {
     "label": "Cancel"
    },
    "provenance": "contract white-label.yaml POST /tenant-config/versions/{version}/restore"
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
  "id": "CMS-016",
  "name": "Site Settings",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/site-settings",
   "component": "apps/venue-management-web/src/routes/white-label/SiteSettingsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "CMS-001",
    "CMS-002",
    "CMS-003",
    "CMS-013",
    "CMS-017",
    "CMS-018",
    "CMS-101",
    "CMS-103"
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
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-016 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-016 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "version"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-016 holds version, so an edge into it carries them"
    },
    {
     "to": "CMS-017",
     "trigger": "Domain & Certificate",
     "provenance": "derived — CMS-017 declares entryState.params domainId and CMS-016 holds none of them, so the edge carries nothing and CMS-017 opens cold"
    },
    {
     "to": "CMS-018",
     "trigger": "Consent & Legal",
     "provenance": "derived — CMS-018 declares entryState.params policyKind, questionId and CMS-016 holds none of them, so the edge carries nothing and CMS-018 opens cold"
    },
    {
     "to": "CMS-103",
     "trigger": "Booking flows",
     "provenance": "authored 29 September, W12 (flow-level settings and step order moved to CMS-103)",
     "carries": [
      "bookingFlowId"
     ]
    },
    {
     "to": "CMS-101",
     "trigger": "Help me choose",
     "provenance": "authored 29 September, rev 3 REV3-11 — Help me choose sits on the booking page these settings shape, so it is set up from here"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getTenantConfig` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "The values the whole site inherits from, and the venue-wide booking settings each venue may override (decided 29 September, rev 3 CFG-11); the settings of one flow are on CMS-103 (W12).",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The tenant config",
       "bindsTo": "TenantConfig",
       "columns": [
        "TenantConfig.isDraft",
        "TenantConfig.brand",
        "TenantConfig.appIcons",
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
       "label": "The booking flow config",
       "bindsTo": "BookingFlowConfig",
       "columns": [
        "BookingFlowConfig.preset",
        "BookingFlowConfig.stepIndicator",
        "BookingFlowConfig.cartLayout",
        "BookingFlowConfig.cardLayout",
        "BookingFlowConfig.cardSize",
        "BookingFlowConfig.seatPicker",
        "BookingFlowConfig.mapView",
        "BookingFlowConfig.density",
        "BookingFlowConfig.embedMode",
        "BookingFlowConfig.heroBanner",
        "BookingFlowConfig.searchInBanner",
        "BookingFlowConfig.singleEventPage",
        "BookingFlowConfig.quantitiesOnAddOns",
        "BookingFlowConfig.cartSideInRtl",
        "BookingFlowConfig.eventBannerDates",
        "BookingFlowConfig.timesPerPage",
        "BookingFlowConfig.dayPartFilter",
        "BookingFlowConfig.dayPartBoundaries",
        "BookingFlowConfig.seatViewPosition",
        "BookingFlowConfig.seatTimeBar",
        "BookingFlowConfig.ticketCategories",
        "BookingFlowConfig.ticketTags",
        "BookingFlowConfig.cardInfo",
        "BookingFlowConfig.conciergeMascot",
        "BookingFlowConfig.showInfoOnly",
        "BookingFlowConfig.locationSwitcher",
        "BookingFlowConfig.guestContactFields",
        "BookingFlowConfig.dateStripDays",
        "BookingFlowConfig.venueOverrides"
       ],
       "operation": "getBookingFlowConfig",
       "notes": "**Venue-wide booking settings only (decided 29 September, W12).** The settings that belong to one flow (`performanceReveal`, `signInAt`, `seatEventDateMode`, `extrasStep`, `quickTour`, the flow's consent questions) moved to each flow on CMS-103, and `categoryDisplay` is gone (W7, superseding 23SEP-18: `cardLayout` carries rows or grid). Here: `timesPerPage` and the day-part chips (REV3-1); `seatViewPosition` (REV3-5); `seatTimeBar` (REV3-6); `cartLayout` and `cartSideInRtl` (REV3-10); `showInfoOnly` (REV3-14); `ticketCategories` (REV3-16); `locationSwitcher` (REV3-18); `ticketTags` (23SEP-3); `cardInfo` (23SEP-6); `eventBannerDates` (23SEP-19); `conciergeMascot` (CFG-5); the card and density enums (DG-6); **`guestContactFields`**, what the guest-checkout pop-up asks: email only, + name or + mobile (W1); **`dateStripDays`**, the days on the date strip before the calendar icon, default 7 (M17-08).",
       "provenance": "contract white-label.yaml GET /tenant-config/booking-flow"
      },
      {
       "kind": "selectField",
       "label": "Settings for",
       "operation": "getBookingFlowConfig",
       "notes": "**Which level is being edited** (decided 29 September, rev 3 CFG-11). *All venues* edits the tenant settings; picking a venue edits that venue's entry in `venueOverrides` and shows beside each field the tenant value it inherits. Sends `?effectiveForVenueId=` to show the settings in force at that venue, resolved field by field. Venues from `listOrgUnits`.",
       "provenance": "contract white-label.yaml GET /tenant-config/booking-flow"
      },
      {
       "kind": "dataTable",
       "label": "Venues that differ from the tenant",
       "bindsTo": "BookingFlowVenueOverride",
       "columns": [
        "BookingFlowVenueOverride.venueId",
        "BookingFlowVenueOverride.settings"
       ],
       "operation": "getBookingFlowConfig",
       "notes": "**One row per venue that overrides anything** (decided 29 September, rev 3 CFG-11). The editor sets only the fields that differ; a field left empty inherits the tenant value, and clearing one removes it from the override. A venue that is not one of the tenant's active venues, or a second row for the same venue, is refused `400` and the row is marked. An override kept for a closed venue is shown greyed: it has no effect.",
       "provenance": "contract white-label.yaml GET /tenant-config/booking-flow"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save booking flow config",
       "operation": "setBookingFlowConfig",
       "provenance": "contract white-label.yaml PUT /tenant-config/booking-flow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The site settings, read by `getTenantConfig`.",
   "error": "Could not load. Names which read failed and leaves the site settings untouched.",
   "emptyNoResults": "A venue picked in Settings for with no override shows the tenant settings it inherits, labelled as inherited, rather than an empty form (rev 3 CFG-11).",
   "emptyFirstRun": "No site settings yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `getBookingFlowConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getBookingFlowConfig",
    "contract": "white-label",
    "purpose": "How the guest booking flow looks and steps",
    "trigger": "onLoad"
   },
   {
    "operationId": "setBookingFlowConfig",
    "contract": "white-label",
    "purpose": "Preset, step indicator, cart layout, embed mode",
    "trigger": "onAction"
   },
   {
    "operationId": "getTenantConfig",
    "contract": "white-label",
    "purpose": "Full working configuration",
    "trigger": "onLoad"
   },
   {
    "operationId": "listOrgUnits",
    "contract": "tenancy",
    "purpose": "The tenant's venues, for the per-venue override picker (rev 3 CFG-11)",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAnalyticsProviders",
    "contract": "white-label",
    "purpose": "Connected analytics platforms",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setAnalyticsProvider",
    "contract": "white-label",
    "purpose": "Connect or change an analytics platform",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-016"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetBookingFlowConfig",
    "component": "modal",
    "trigger": "Save booking flow config",
    "body": "**Collects what `setBookingFlowConfig` sends before it is called.** Nothing in the body is required. Optional: `preset`, `stepIndicator`, `cartLayout`, `cardLayout`, `cardSize`, `seatPicker`, `mapView`, `density`, `embedMode`, `heroBanner`, `searchInBanner`, `singleEventPage`, `quantitiesOnAddOns`, the venue-wide rev 3 booking rules on the panel above, `guestContactFields` (W1), `dateStripDays` (M17-08) and `venueOverrides` (decided 29 September, rev 3 CFG-11). **The body is the tenant settings plus every venue override**: saving a venue's override sends the whole configuration with that venue's row changed. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "BookingFlowConfig",
    "confirm": {
     "label": "Save booking flow config",
     "operation": "setBookingFlowConfig"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "preset",
      "stepIndicator",
      "cartLayout",
      "cardLayout",
      "cardSize",
      "seatPicker",
      "mapView",
      "density",
      "embedMode",
      "heroBanner",
      "searchInBanner",
      "singleEventPage",
      "quantitiesOnAddOns",
      "cartSideInRtl",
      "eventBannerDates",
      "timesPerPage",
      "dayPartFilter",
      "dayPartBoundaries",
      "seatViewPosition",
      "seatTimeBar",
      "ticketCategories",
      "ticketTags",
      "cardInfo",
      "conciergeMascot",
      "showInfoOnly",
      "locationSwitcher",
      "guestContactFields",
      "dateStripDays",
      "venueOverrides"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/booking-flow"
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
  "id": "CMS-101",
  "name": "Help Me Choose",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/help-me-choose",
   "component": "apps/venue-management-web/src/routes/white-label/HelpMeChoose.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-016",
    "CMS-102"
   ],
   "exitTo": [
    "CMS-016",
    "CMS-102"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-016 Site Settings**, beside the booking-flow settings, because Help me choose sits on the booking page those settings shape (decided 29 September, rev 3 REV3-11).",
   "transitions": [
    {
     "to": "CMS-016",
     "trigger": "Back to Site Settings",
     "provenance": "authored 29 September, rev 3 REV3-11",
     "back": true
    },
    {
     "to": "CMS-102",
     "trigger": "Back to the Site Builder",
     "provenance": "authored 29 September, W12 (step 4)",
     "back": true
    }
   ]
  },
  "notes": "**Added 29 September for rev 3 REV3-11: Help me choose is venue configuration, never hard-coded.** A venue sets up one or two questions, each with two to four answers (title, one-liner, icon, optional badge), and the answer picked on the last question opens the product, category, event or booking module that fits through a result card. **Two sources, one review**: staff write a set-up here, and once the venue's products are uploaded the `ai` service proposes set-ups (`source` `aiSuggested`), which land here as drafts. **A suggestion is never published by itself**: a person reviews it, edits it or dismisses it, previews it and publishes it. One published set-up per venue; publishing another returns the old one to draft.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listGuidedChoices` reads the venue's set-ups and the editor acts on one of them — list, select, act",
  "purpose": "Set up a venue's Help me choose so its answers filter the catalogue, review the question set the assistant proposes from the venue's products, preview the filtered list and publish it (Site Builder step 4).",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Venue",
       "operation": "listGuidedChoices",
       "notes": "The venue whose set-ups are shown (path `venueId`); defaults to the session venue.",
       "provenance": "contract white-label.yaml GET /venues/{venueId}/guided-choices"
      },
      {
       "kind": "selectField",
       "label": "Source",
       "operation": "listGuidedChoices",
       "notes": "Sends `?source=`, `manual` or `aiSuggested`. **Suggestions awaiting review** is `aiSuggested` with status `draft`, and is the default view while any exist.",
       "provenance": "contract white-label.yaml GET /venues/{venueId}/guided-choices"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "operation": "listGuidedChoices",
       "notes": "Sends `?status=`, `draft` or `published`.",
       "provenance": "contract white-label.yaml GET /venues/{venueId}/guided-choices"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every Help me choose set-up at this venue",
       "bindsTo": "GuidedChoice",
       "columns": [
        "GuidedChoice.name",
        "GuidedChoice.status",
        "GuidedChoice.source",
        "GuidedChoice.mode",
        "GuidedChoice.showBanner",
        "GuidedChoice.publishedAt",
        "GuidedChoice.updatedAt"
       ],
       "operation": "listGuidedChoices",
       "notes": "**An AI suggestion is labelled as one** on its row, and keeps `source` `aiSuggested` after a person edits it, so a report can count how many proposals were published.",
       "provenance": "contract white-label.yaml GET /venues/{venueId}/guided-choices"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected set-up",
       "bindsTo": "GuidedChoice",
       "columns": [
        "GuidedChoice.name",
        "GuidedChoice.mode",
        "GuidedChoice.showBanner",
        "GuidedChoice.behaviour",
        "GuidedChoice.showEverything",
        "GuidedChoice.questions",
        "GuidedChoice.status",
        "GuidedChoice.source",
        "GuidedChoice.suggestionRef",
        "GuidedChoice.publishedAt",
        "GuidedChoice.publishedBy"
       ],
       "operation": "listGuidedChoices",
       "notes": "**The editor.** `mode`: a button on the booking page, a pop-up on the guest's first arrival as well, or off (configured but not shown). `showBanner`: the dark banner under the products. One or two questions, two to four answers each: title, one-liner (140 characters), icon, badge (24 characters), target (a product, category, event or booking module, picked from `listProducts`, `listProductCategories` and `listEvents`) and the result card (title, body, image; absent fields fall back to the target's own). Every text in every tenant language.\n**Help me choose filters (decided 29 September, W4).** `behaviour` filter (default) or recommend; up to four questions, each of a kind: choice, yes/no, age, level or certification. **The filter builder** sets what each answer keeps: products, categories, segment tags, an age range, swimmers only or never, a certificate held or not; a target may also be a booking flow (`listBookingFlows`). An answer may pre-fill a consent question, which the guest still confirms. The \"Show everything\" link is on by default.",
       "provenance": "contract white-label.yaml GET /venues/{venueId}/guided-choices"
      },
      {
       "kind": "livePreview",
       "label": "Preview",
       "notes": "**Renders the draft as a guest would meet it**: the button or pop-up, the banner, each question and the result card, in each language and in both directions. Drawn from the record in hand; it calls nothing and publishes nothing, and guests keep seeing the published set-up until Publish. **Preview the filtered list**: for each combination of answers, the products left (read with `listProducts` and the answer's filter), so an answer that leaves nothing bookable shows before it is published (W4).",
       "provenance": "authored 29 September, rev 3 REV3-11"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "impliedBy": "publishGuidedChoice",
       "notes": "Names the venue, says that guests there see this set-up from now on, and that **the set-up published there before returns to draft** (one published per venue). Refused `422` when an answer targets a product, category, event or module that is not on sale or not enabled, naming the answer; only staff publish (`TENANT_PUBLISH`), never the assistant.",
       "provenance": "contract white-label.yaml POST /guided-choices/{guidedChoiceId}/publish"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "New set-up",
       "operation": "createGuidedChoice",
       "provenance": "contract white-label.yaml POST /venues/{venueId}/guided-choices"
      },
      {
       "kind": "secondaryButton",
       "label": "Save draft",
       "operation": "updateGuidedChoice",
       "notes": "A draft only. A published set-up is refused `409`; unpublish it first or create a new draft.",
       "provenance": "contract white-label.yaml PATCH /guided-choices/{guidedChoiceId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish",
       "operation": "publishGuidedChoice",
       "provenance": "contract white-label.yaml POST /guided-choices/{guidedChoiceId}/publish"
      },
      {
       "kind": "secondaryButton",
       "label": "Unpublish",
       "operation": "unpublishGuidedChoice",
       "notes": "Guests stop seeing Help me choose at this venue; the set-up returns to draft.",
       "provenance": "contract white-label.yaml POST /guided-choices/{guidedChoiceId}/unpublish"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete draft or dismiss suggestion",
       "operation": "deleteGuidedChoice",
       "notes": "A draft only; a published set-up is refused `409`. Dismissing an AI suggestion is this delete.",
       "provenance": "contract white-label.yaml DELETE /guided-choices/{guidedChoiceId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue's Help me choose set-ups, read by `listGuidedChoices`.",
   "error": "Could not load. Names which read failed and leaves the set-ups untouched.",
   "emptyFirstRun": "**No Help me choose at this venue, so guests see none.** Offers New set-up, and says that once the venue's products are uploaded the assistant proposes set-ups here as drafts for review.",
   "emptyNoResults": "The source or status filter matched nothing and the venue's other set-ups are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listGuidedChoices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGuidedChoices",
    "contract": "white-label",
    "purpose": "The venue's set-ups, filtered by source and status (rev 3 REV3-11)",
    "trigger": "onLoad"
   },
   {
    "operationId": "createGuidedChoice",
    "contract": "white-label",
    "purpose": "Start a set-up by hand, as a draft",
    "trigger": "onAction",
    "invalidates": [
     "listGuidedChoices"
    ]
   },
   {
    "operationId": "updateGuidedChoice",
    "contract": "white-label",
    "purpose": "Edit a draft, including an AI suggestion under review",
    "trigger": "onAction",
    "invalidates": [
     "listGuidedChoices"
    ]
   },
   {
    "operationId": "deleteGuidedChoice",
    "contract": "white-label",
    "purpose": "Delete a draft or dismiss a suggestion",
    "trigger": "onAction",
    "invalidates": [
     "listGuidedChoices"
    ]
   },
   {
    "operationId": "publishGuidedChoice",
    "contract": "white-label",
    "purpose": "Make a reviewed set-up the one guests see at this venue",
    "trigger": "onAction",
    "invalidates": [
     "listGuidedChoices"
    ]
   },
   {
    "operationId": "unpublishGuidedChoice",
    "contract": "white-label",
    "purpose": "Stop showing it to guests; back to draft",
    "trigger": "onAction",
    "invalidates": [
     "listGuidedChoices"
    ]
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "Products an answer can open",
    "trigger": "onAction"
   },
   {
    "operationId": "listProductCategories",
    "contract": "catalogue",
    "purpose": "Categories an answer can open",
    "trigger": "onAction"
   },
   {
    "operationId": "listEvents",
    "contract": "catalogue",
    "purpose": "Events an answer can open",
    "trigger": "onAction"
   },
   {
    "operationId": "listBookingFlows",
    "contract": "white-label",
    "purpose": "The venue's flows an answer can open (target kind bookingFlow, W12)",
    "trigger": "onAction"
   },
   {
    "operationId": "suggestGuidedChoice",
    "contract": "ai",
    "purpose": "Ask the assistant for a question set from product attributes (age and height rules, level tags, certifications); it lands here as a draft through white-label proposeGuidedChoice (W4)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getGuidedChoiceSuggestion",
    "contract": "ai",
    "purpose": "The reasons behind a Help me choose suggestion",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "guidedChoiceId",
     "from": "navigation"
    },
    {
     "name": "suggestionId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves the venue from the session and opens on the suggestions awaiting review, or on the list when there are none."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-101"
  },
  "overlays": [
   {
    "id": "formCreateGuidedChoice",
    "component": "modal",
    "trigger": "New set-up",
    "body": "**Collects what `createGuidedChoice` sends before it is called.** Required: `name` (staff-facing), `mode`, `questions` (one or two, each with two to four answers and a target per answer). Optional: `showBanner` (default on). Created as a draft; guests see nothing until it is published. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "GuidedChoice",
    "confirm": {
     "label": "Create draft",
     "operation": "createGuidedChoice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "mode",
      "showBanner",
      "questions"
     ]
    },
    "provenance": "contract white-label.yaml POST /venues/{venueId}/guided-choices"
   },
   {
    "id": "confirmPublishGuidedChoice",
    "component": "confirmDialog",
    "trigger": "Publish",
    "body": "**Names the venue and the set-up that stops showing there**, since only one is published per venue. An answer whose target is not on sale or not enabled blocks the publish and is named (`422`).",
    "confirm": {
     "label": "Publish to guests",
     "operation": "publishGuidedChoice"
    },
    "dismiss": {
     "label": "Cancel"
    },
    "provenance": "contract white-label.yaml POST /guided-choices/{guidedChoiceId}/publish"
   },
   {
    "id": "confirmDeleteGuidedChoice",
    "component": "confirmDialog",
    "trigger": "Delete draft or dismiss suggestion",
    "body": "Names the set-up and, for an AI suggestion, says that dismissing it removes it and the assistant's reasoning with it. A published set-up cannot be deleted (`409`).",
    "confirm": {
     "label": "Delete",
     "operation": "deleteGuidedChoice"
    },
    "dismiss": {
     "label": "Keep it"
    },
    "provenance": "contract white-label.yaml DELETE /guided-choices/{guidedChoiceId}"
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
  "id": "CMS-102",
  "name": "Site Builder",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/site-builder",
   "component": "apps/venue-management-web/src/routes/white-label/SiteBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-001"
   ],
   "exitTo": [
    "CMS-001",
    "CMS-103",
    "CMS-101",
    "CMS-007",
    "CMS-009",
    "CMS-002",
    "CMS-004",
    "CMS-008",
    "CMS-005",
    "CMS-003",
    "CMS-006",
    "CMS-012",
    "CMS-014",
    "CMS-015",
    "CMS-104"
   ],
   "inferred": false,
   "notes": "**The step-based CMS (decided 29 September, W12 and M24-05).** Each of the seven steps opens the full screen for its details and comes back here; progress is saved on every return, so the builder reopens where the operator left it.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "1 Venue and modules",
     "provenance": "authored 29 September, W12 (step 1 reuses CMS-001 for modules, feature toggles and guest checkout)",
     "back": true
    },
    {
     "to": "CMS-103",
     "trigger": "2 Ticketing flows",
     "provenance": "authored 29 September, W12 (steps 2 and 3 are CMS-103)",
     "back": true,
     "carries": [
      "bookingFlowId"
     ]
    },
    {
     "to": "CMS-103",
     "trigger": "3 Compose steps",
     "carries": [
      "bookingFlowId"
     ],
     "provenance": "authored 29 September, W12 (step order and step settings)",
     "back": true
    },
    {
     "to": "CMS-101",
     "trigger": "4 Help me choose",
     "provenance": "authored 29 September, W12 and W4",
     "back": true
    },
    {
     "to": "CMS-007",
     "trigger": "5 Look and feel — header, footer and home",
     "provenance": "authored 29 September, W12 (header and footer on CMS-007 and CMS-009)",
     "back": true
    },
    {
     "to": "CMS-009",
     "trigger": "5 Look and feel — navigation and menus",
     "provenance": "authored 29 September, W12",
     "back": true
    },
    {
     "to": "CMS-002",
     "trigger": "5 Look and feel — brand kit",
     "provenance": "authored 29 September, W12 (logos on CMS-002 and CMS-004)",
     "back": true
    },
    {
     "to": "CMS-004",
     "trigger": "5 Look and feel — logos",
     "provenance": "authored 29 September, W12",
     "back": true
    },
    {
     "to": "CMS-008",
     "trigger": "5 Look and feel — banners",
     "provenance": "authored 29 September, W12",
     "back": true
    },
    {
     "to": "CMS-005",
     "trigger": "5 Look and feel — theme",
     "provenance": "authored 29 September, W12 (theme and fonts on CMS-005 and CMS-003)",
     "back": true
    },
    {
     "to": "CMS-003",
     "trigger": "5 Look and feel — fonts",
     "provenance": "authored 29 September, W12",
     "back": true,
     "carries": [
      "version"
     ]
    },
    {
     "to": "CMS-009",
     "trigger": "6 Mobile app — tabs and the Buy tickets button",
     "provenance": "authored 29 September, MOB-1 and MOB-2",
     "back": true
    },
    {
     "to": "CMS-004",
     "trigger": "6 Mobile app — intro video",
     "provenance": "authored 29 September, MOB-5",
     "back": true
    },
    {
     "to": "CMS-007",
     "trigger": "6 Mobile app — home sections",
     "provenance": "authored 29 September, MOB-3",
     "back": true
    },
    {
     "to": "CMS-006",
     "trigger": "7 Preview",
     "provenance": "authored 29 September, W12 (step 7 is CMS-006, CMS-012 and CMS-014)",
     "back": true,
     "carries": [
      "version"
     ]
    },
    {
     "to": "CMS-012",
     "trigger": "7 Preview right to left",
     "provenance": "authored 29 September, W12",
     "back": true
    },
    {
     "to": "CMS-014",
     "trigger": "7 Publish",
     "provenance": "authored 29 September, W12",
     "back": true
    },
    {
     "to": "CMS-015",
     "trigger": "Roll back a version",
     "provenance": "authored 29 September, W12 (CMS-015 handles rollback)",
     "back": true,
     "carries": [
      "version"
     ]
    },
    {
     "to": "CMS-104",
     "trigger": "Build the mobile app",
     "precondition": "the tenant has published at least once",
     "provenance": "authored 29 September, M24-08",
     "back": true
    }
   ]
  },
  "notes": "**Added 29 September for W12 and M24-05: the CMS is a flow builder with a step-based shell.** The configuration side panel of the rev 3 prototype is a reference tool only (W12). The builder is the white-labelling builder M24-05 asks for, not a new set of editors: every step opens a screen that already exists and holds its details.",
  "density": "compact",
  "pattern": "multiStepForm",
  "patternReason": "`getSiteSetupProgress` holds the seven steps and their state, and `setSiteSetupProgress` saves each one — progress, fields per step, review, submit",
  "purpose": "Build a working site in about 30 minutes: pick a preset, then walk seven saved steps (venue and modules, ticketing flows, compose steps, Help me choose, look and feel, mobile app, preview and publish), each opening the full screen for its details. **The preset keeps the minimum path short (M24-05)**: it proposes the modules, the booking flows with their default step order, the home sections and the mobile tabs, so the only things an operator must supply are a logo, four colours and a Publish; everything else keeps the preset or the contract default and can be refined later.",
  "layout": {
   "template": "wizard",
   "regions": [
    {
     "name": "progress",
     "slot": "progress",
     "components": [
      {
       "kind": "progressIndicator",
       "label": "Seven steps",
       "bindsTo": "SiteSetupProgress",
       "columns": [
        "SiteSetupProgress.currentStep",
        "SiteSetupProgress.steps",
        "SiteSetupProgress.minimumPathDone"
       ],
       "operation": "getSiteSetupProgress",
       "notes": "1 Venue and modules · 2 Ticketing flows · 3 Compose steps · 4 Help me choose · 5 Look and feel · 6 Mobile app · 7 Preview and publish. Each step shows not started, in progress, done or skipped; steps 4 and 6 may be skipped. **Minimum path** (logo, colours, one valid flow, a publish) is marked, so an operator in a hurry sees what is left before the site works.",
       "provenance": "contract white-label.yaml GET /tenant-config/site-setup"
      }
     ]
    },
    {
     "name": "fields",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Start from",
       "bindsTo": "SiteSetupProgress.presetKey",
       "operation": "setSiteSetupProgress",
       "notes": "Theme park, water park, museum, theatre and arena, single attraction, play centre, several venues. **Proposes, never writes**: each step opens pre-filled from the preset, and nothing changes until the operator saves that step.",
       "provenance": "contract white-label.yaml PUT /tenant-config/site-setup"
      },
      {
       "kind": "cardList",
       "label": "Flow types the preset proposes",
       "bindsTo": "BookingFlowType",
       "columns": [
        "BookingFlowType.key",
        "BookingFlowType.name",
        "BookingFlowType.productKinds"
       ],
       "operation": "listBookingFlowTypes",
       "notes": "Step 2 in one tap: the preset's flow types, ticked; **Add these flows** creates each with the type's default steps and order (`createBookingFlowDefinition`). Composing the order is step 3, on CMS-103.",
       "provenance": "contract white-label.yaml GET /booking-flow-types"
      },
      {
       "kind": "dataTable",
       "label": "Flows this venue has",
       "bindsTo": "BookingFlow",
       "columns": [
        "BookingFlow.name",
        "BookingFlow.flowTypeKey",
        "BookingFlow.isDefaultForType",
        "BookingFlow.isValid"
       ],
       "operation": "listBookingFlows",
       "notes": "Steps 2 and 3 are done when every flow here is valid and each bookable product kind has one.",
       "provenance": "contract white-label.yaml GET /venues/{venueId}/booking-flows"
      }
     ]
    },
    {
     "name": "review",
     "slot": "review",
     "components": [
      {
       "kind": "detailPanel",
       "label": "What is live",
       "bindsTo": "TenantAppStatus",
       "columns": [
        "TenantAppStatus.isPublished",
        "TenantAppStatus.publishedVersion",
        "TenantAppStatus.hasUnpublishedChanges"
       ],
       "operation": "getTenantAppStatus",
       "provenance": "contract white-label.yaml GET /tenant-config/status"
      },
      {
       "kind": "banner",
       "label": "What still blocks a publish",
       "bindsTo": "ConfigValidationReport",
       "columns": [
        "ConfigValidationReport.passed",
        "ConfigValidationReport.findings"
       ],
       "operation": "validateTenantConfig",
       "notes": "Each finding links to the step and screen that fixes it (a missing logo to CMS-004, an invalid flow to CMS-103).",
       "provenance": "contract white-label.yaml POST /tenant-config/validate"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "submit",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save and continue",
       "operation": "setSiteSetupProgress",
       "provenance": "contract white-label.yaml PUT /tenant-config/site-setup"
      },
      {
       "kind": "secondaryButton",
       "label": "Add these flows",
       "operation": "createBookingFlowDefinition",
       "provenance": "contract white-label.yaml POST /venues/{venueId}/booking-flows"
      },
      {
       "kind": "secondaryButton",
       "label": "Check what blocks a publish",
       "operation": "validateTenantConfig",
       "provenance": "contract white-label.yaml POST /tenant-config/validate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The builder's progress, read by `getSiteSetupProgress`.",
   "error": "Could not load. Names which read failed and leaves the progress untouched.",
   "emptyFirstRun": "**Nothing set up yet.** Opens on Start from, with every step not started, and says the minimum path is a logo, four colours, the preset's flows and a publish.",
   "emptyNoResults": "The venue has no flow of a type the preset proposes yet; the flow list says so and offers Add these flows rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `getSiteSetupProgress` requires, and names that permission. **Never an empty form** — that reads as *there is nothing to set up*."
  },
  "apis": [
   {
    "operationId": "getSiteSetupProgress",
    "contract": "white-label",
    "purpose": "Where the operator is in the seven steps, and the preset picked",
    "trigger": "onLoad"
   },
   {
    "operationId": "setSiteSetupProgress",
    "contract": "white-label",
    "purpose": "Save the preset and each step's state on every return",
    "trigger": "onAction",
    "invalidates": [
     "getSiteSetupProgress"
    ]
   },
   {
    "operationId": "listBookingFlowTypes",
    "contract": "white-label",
    "purpose": "The flow types the preset proposes for step 2",
    "trigger": "onLoad"
   },
   {
    "operationId": "listBookingFlows",
    "contract": "white-label",
    "purpose": "The venue's flows, to mark steps 2 and 3 done",
    "trigger": "onLoad"
   },
   {
    "operationId": "createBookingFlowDefinition",
    "contract": "white-label",
    "purpose": "Add the preset's flows with their default steps in one go",
    "trigger": "onAction",
    "invalidates": [
     "listBookingFlows"
    ]
   },
   {
    "operationId": "getTenantAppStatus",
    "contract": "white-label",
    "purpose": "Whether the site is live, for step 7",
    "trigger": "onLoad"
   },
   {
    "operationId": "validateTenantConfig",
    "contract": "white-label",
    "purpose": "What still blocks a publish, each finding linked to its step",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves the tenant and venue from the session and opens on the current step, or on Start from when nothing is saved."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-102"
  },
  "apisNote": "Authored 29 September 2026 (P29 pass, W12 and M24-05) from impact.md section b.",
  "overlays": [
   {
    "id": "formAddPresetFlows",
    "component": "modal",
    "trigger": "Add these flows",
    "body": "**Collects what `createBookingFlowDefinition` sends, once per ticked type.** Required: `flowTypeKey`, `name` (pre-filled from the type). `isDefaultForType` on. Steps are left out, so each flow gets the type's default steps and order. Dismissing sends nothing.",
    "bindsTo": "BookingFlow",
    "confirm": {
     "label": "Add flows",
     "operation": "createBookingFlowDefinition"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "flowTypeKey",
      "name"
     ]
    },
    "provenance": "contract white-label.yaml POST /venues/{venueId}/booking-flows"
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
  "id": "CMS-103",
  "name": "Booking Flows",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/booking-flows",
   "component": "apps/venue-management-web/src/routes/white-label/BookingFlows.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-102",
    "CMS-016",
    "CMS-014"
   ],
   "exitTo": [
    "CMS-102",
    "CMS-016",
    "CMS-101",
    "CMS-014"
   ],
   "inferred": false,
   "notes": "**Steps 2 and 3 of the Site Builder (decided 29 September, W12).** Also reached from Site Settings, which now holds only the venue-wide settings, and from Publishing when a flow blocks the publish.",
   "transitions": [
    {
     "to": "CMS-102",
     "trigger": "Back to the Site Builder",
     "provenance": "authored 29 September, W12",
     "back": true
    },
    {
     "to": "CMS-016",
     "trigger": "Venue-wide booking settings",
     "provenance": "authored 29 September, W12 (the settings every flow shares stay on CMS-016)"
    },
    {
     "to": "CMS-101",
     "trigger": "Help me choose",
     "provenance": "authored 29 September, W4 (an answer can point at a flow)"
    },
    {
     "to": "CMS-014",
     "trigger": "Publish with the site",
     "provenance": "authored 29 September, W12 (flows publish through publishTenantConfig)"
    }
   ]
  },
  "notes": "**Added 29 September for W12: operators pick their ticketing flows, see which steps are required, optional or conditional, and set their own order.** The catalogue (`listBookingFlowTypes`) is the same for every tenant: dated day pass, timed entry, open-dated, seated (fixed performance, or date and time then seat map), experience or workshop (product first, W8), surf or session (time then level), meeting room by the hour, cabana on a map or by size (W6), guided tour by language, transport, table reservation, membership, gift card and several locations. Flows reach guests with the rest of the site (`publishTenantConfig`); WEB-005..012, GST-007..009 and GST-041 order their steps from the published flow.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listBookingFlows` reads the venue's flows and `getBookingFlow` reads one of them to compose — list, select, act",
  "purpose": "Pick the venue's booking flows, turn optional steps on or off, set the step order within the allowed limits with a live preview, assign flows to products and categories, and validate them before they publish with the site.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Venue",
       "operation": "listBookingFlows",
       "notes": "The venue whose flows are shown (path `venueId`); defaults to the session venue.",
       "provenance": "contract white-label.yaml GET /venues/{venueId}/booking-flows"
      },
      {
       "kind": "selectField",
       "label": "Flow type",
       "operation": "listBookingFlows",
       "notes": "Sends `?flowTypeKey=`.",
       "provenance": "contract white-label.yaml GET /venues/{venueId}/booking-flows"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "The venue's flows",
       "bindsTo": "BookingFlow",
       "columns": [
        "BookingFlow.name",
        "BookingFlow.flowTypeKey",
        "BookingFlow.isDefaultForType",
        "BookingFlow.isEnabled",
        "BookingFlow.isValid",
        "BookingFlow.updatedAt"
       ],
       "operation": "listBookingFlows",
       "notes": "An invalid flow is marked and blocks the site's publish until it is fixed.",
       "provenance": "contract white-label.yaml GET /venues/{venueId}/booking-flows"
      },
      {
       "kind": "cardList",
       "label": "Flow types to pick from",
       "bindsTo": "BookingFlowType",
       "columns": [
        "BookingFlowType.key",
        "BookingFlowType.name",
        "BookingFlowType.description",
        "BookingFlowType.productKinds",
        "BookingFlowType.steps"
       ],
       "operation": "listBookingFlowTypes",
       "notes": "Each card lists the type's steps with their required, optional or conditional mark, so the choice is made knowing what the guest will go through.",
       "provenance": "contract white-label.yaml GET /booking-flow-types"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Compose the steps",
       "bindsTo": "BookingFlow",
       "columns": [
        "BookingFlow.name",
        "BookingFlow.flowTypeKey",
        "BookingFlow.isDefaultForType",
        "BookingFlow.isEnabled",
        "BookingFlow.steps",
        "BookingFlow.isValid"
       ],
       "operation": "getBookingFlow",
       "notes": "**The step list, in the venue's order.** Each step carries its mark: *Required* (locked on), *Optional* (a switch) or *Conditional* (a switch, with the condition in words, e.g. \"only when the tenant has more than one venue\"). Steps are dragged to reorder; **a drop that breaks a constraint is refused before it lands** (`validateBookingFlow` with the proposed `steps`), and the constraint is named (\"payment is always last\", \"the seat map comes after date and time\"). Each step opens its settings: the step's own (`BookingFlowStep.settings`, e.g. the tour languages or the room's hours) and, read-only with a link to CMS-016, the venue-wide settings it uses.",
       "provenance": "contract white-label.yaml GET /booking-flows/{bookingFlowId}"
      },
      {
       "kind": "detailPanel",
       "label": "This flow's settings",
       "bindsTo": "BookingFlowLevelSettings",
       "columns": [
        "BookingFlowLevelSettings.performanceReveal",
        "BookingFlowLevelSettings.signInAt",
        "BookingFlowLevelSettings.seatEventDateMode",
        "BookingFlowLevelSettings.extrasStep",
        "BookingFlowLevelSettings.quickTour",
        "BookingFlowLevelSettings.consentQuestionIds"
       ],
       "operation": "getBookingFlow",
       "notes": "**Moved here from Site Settings on 29 September (W12)**, because they belong to one flow: date, time then tickets or all at once (REV3-2); sign in after add-ons or at payment (REV3-3); a seated event's date inline or over the seat map (REV3-4, seated flows only); the extras step auto, always or never; the quick tour (REV3-20); the flow's consent questions (REV3-26).",
       "provenance": "contract white-label.yaml GET /booking-flows/{bookingFlowId}"
      },
      {
       "kind": "multiSelect",
       "label": "Consent questions this flow asks",
       "bindsTo": "BookingFlowLevelSettings.consentQuestionIds",
       "operation": "listConsentQuestions",
       "notes": "**The questions every booking in this flow asks, whatever the product** (rev 3 REV3-26), e.g. a water park's \"Are you able to swim?\". Options are the active questions from `listConsentQuestions`, written on CMS-018. A Help me choose answer may pre-fill one; the guest still confirms it (W4).",
       "provenance": "contract marketing-crm.yaml GET /consent-questions"
      },
      {
       "kind": "livePreview",
       "label": "Preview",
       "notes": "**The flow as a guest meets it, step by step, on web and on mobile**, redrawn on every change and drawn from the record in hand. Calls nothing and publishes nothing; guests keep the published flow (`getPublishedBookingFlow`, shown beside it for comparison) until the site is published.",
       "provenance": "authored 29 September, W12"
      },
      {
       "kind": "dataTable",
       "label": "Products and categories using this flow",
       "bindsTo": "Product",
       "columns": [
        "Product.name",
        "Product.kind",
        "Product.categoryId",
        "Product.bookingFlowId"
       ],
       "operation": "listProducts",
       "notes": "Assign the flow to a product (`updateProduct` `bookingFlowId`) or a category (`setProductCategories`, the category's `bookingFlowId`). A product naming no flow uses its category's, then the venue's default for its kind. Set up also on BO-007/BO-008 and BO-115.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "banner",
       "label": "Why this flow cannot publish",
       "bindsTo": "BookingFlowValidation",
       "columns": [
        "BookingFlowValidation.valid",
        "BookingFlowValidation.problems"
       ],
       "operation": "validateBookingFlow",
       "notes": "A required step turned off, a step out of its allowed order, a condition that can never hold, each naming the step and the fix.",
       "provenance": "contract white-label.yaml POST /booking-flows/{bookingFlowId}/validate"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "impliedBy": "publishTenantConfig",
       "notes": "**Flows publish with the whole site**, never alone: the gate names every venue flow that changed since the last version and the products whose steps will change for guests, and says the rest of the draft (theme, pages, navigation) goes live with it. Refused while any enabled flow is invalid (`409`, `bookingFlowInvalid`). Needs `TENANT_PUBLISH`.",
       "provenance": "contract white-label.yaml POST /tenant-config/publish"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add a flow",
       "operation": "createBookingFlowDefinition",
       "provenance": "contract white-label.yaml POST /venues/{venueId}/booking-flows"
      },
      {
       "kind": "secondaryButton",
       "label": "Save flow",
       "operation": "updateBookingFlowDefinition",
       "provenance": "contract white-label.yaml PATCH /booking-flows/{bookingFlowId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate",
       "operation": "validateBookingFlow",
       "provenance": "contract white-label.yaml POST /booking-flows/{bookingFlowId}/validate"
      },
      {
       "kind": "secondaryButton",
       "label": "Assign to product",
       "operation": "updateProduct",
       "provenance": "contract catalogue.yaml PATCH /products/{productId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Assign to category",
       "operation": "setProductCategories",
       "provenance": "contract catalogue.yaml PUT /product-categories"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish site",
       "operation": "publishTenantConfig",
       "permission": "TENANT_PUBLISH",
       "provenance": "contract white-label.yaml POST /tenant-config/publish"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove flow",
       "operation": "deleteBookingFlow",
       "notes": "Refused `409` while a product or category names the flow or it is the default for products on sale; the refusal names them and offers to reassign.",
       "provenance": "contract white-label.yaml DELETE /booking-flows/{bookingFlowId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue's flows and the flow-type catalogue, read by `listBookingFlows` and `listBookingFlowTypes`.",
   "error": "Could not load. Names which read failed and leaves the flows untouched.",
   "emptyFirstRun": "**No flows at this venue yet.** Guests book through each type's default order until one is picked. Offers the flow-type cards and, from the Site Builder, the preset's flows in one step.",
   "emptyNoResults": "The flow-type filter matched nothing and the venue's other flows are still there. Names the filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listBookingFlows` requires, and names that permission. **Never an empty table** — that reads as *there are no flows*."
  },
  "apis": [
   {
    "operationId": "listBookingFlows",
    "contract": "white-label",
    "purpose": "The venue's flows in the draft",
    "trigger": "onLoad"
   },
   {
    "operationId": "listBookingFlowTypes",
    "contract": "white-label",
    "purpose": "The flow types to pick from, with their steps and order constraints",
    "trigger": "onLoad"
   },
   {
    "operationId": "getBookingFlow",
    "contract": "white-label",
    "purpose": "One flow with every step, to compose",
    "trigger": "onAction"
   },
   {
    "operationId": "getPublishedBookingFlow",
    "contract": "white-label",
    "purpose": "What guests book through now, beside the draft in the preview",
    "trigger": "onAction"
   },
   {
    "operationId": "createBookingFlowDefinition",
    "contract": "white-label",
    "purpose": "Pick a flow type for the venue",
    "trigger": "onAction",
    "invalidates": [
     "listBookingFlows"
    ]
   },
   {
    "operationId": "updateBookingFlowDefinition",
    "contract": "white-label",
    "purpose": "Save the step order, the optional steps and the flow's settings",
    "trigger": "onAction",
    "invalidates": [
     "listBookingFlows",
     "getBookingFlow"
    ]
   },
   {
    "operationId": "validateBookingFlow",
    "contract": "white-label",
    "purpose": "Check a proposed order before it is dropped, or the saved flow",
    "trigger": "onAction"
   },
   {
    "operationId": "deleteBookingFlow",
    "contract": "white-label",
    "purpose": "Remove a flow nothing uses",
    "trigger": "onAction",
    "invalidates": [
     "listBookingFlows"
    ]
   },
   {
    "operationId": "publishTenantConfig",
    "contract": "white-label",
    "purpose": "Publish the site, flows included",
    "trigger": "onAction"
   },
   {
    "operationId": "listConsentQuestions",
    "contract": "marketing-crm",
    "purpose": "The consent questions a flow can ask (rev 3 REV3-26)",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "The products a flow is assigned to",
    "trigger": "onAction"
   },
   {
    "operationId": "updateProduct",
    "contract": "catalogue",
    "purpose": "Assign the flow to a product (`bookingFlowId`)",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "listProductCategories",
    "contract": "catalogue",
    "purpose": "The categories a flow can be assigned to",
    "trigger": "onAction"
   },
   {
    "operationId": "setProductCategories",
    "contract": "catalogue",
    "purpose": "Assign the flow to a category (`bookingFlowId`)",
    "trigger": "onAction",
    "invalidates": [
     "listProductCategories"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "bookingFlowId",
     "from": "CMS-102",
     "optional": true
    },
    {
     "name": "productId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves the venue from the session and opens on the flow list, or on the flow named in the link."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-103"
  },
  "apisNote": "Authored 29 September 2026 (P29 pass, W12, W6, W8) from impact.md section b.",
  "overlays": [
   {
    "id": "formCreateBookingFlowDefinition",
    "component": "modal",
    "trigger": "Add a flow",
    "body": "**Collects what `createBookingFlowDefinition` sends.** Required: `flowTypeKey` (from the cards), `name`. Optional: `isDefaultForType`, `steps` (left out, the type's defaults), `settings`. Dismissing sends nothing.",
    "bindsTo": "BookingFlow",
    "confirm": {
     "label": "Add flow",
     "operation": "createBookingFlowDefinition"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "flowTypeKey",
      "name",
      "isDefaultForType",
      "steps",
      "settings"
     ]
    },
    "provenance": "contract white-label.yaml POST /venues/{venueId}/booking-flows"
   },
   {
    "id": "confirmDeleteBookingFlow",
    "component": "confirmDialog",
    "trigger": "Remove flow",
    "body": "Names the flow and says guests keep it until the next publish. Refused `409` while products or categories name it, and names them.",
    "confirm": {
     "label": "Remove",
     "operation": "deleteBookingFlow"
    },
    "dismiss": {
     "label": "Keep it"
    },
    "provenance": "contract white-label.yaml DELETE /booking-flows/{bookingFlowId}"
   },
   {
    "id": "confirmPublishSite",
    "component": "confirmDialog",
    "trigger": "Publish site",
    "body": "**Names what goes live**: the changed flows and the products whose booking steps change, with the rest of the draft. Asks for the publish note `publishTenantConfig` requires.",
    "confirm": {
     "label": "Publish",
     "operation": "publishTenantConfig"
    },
    "dismiss": {
     "label": "Cancel"
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
  "id": "CMS-104",
  "name": "App Build & Store Publishing",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/app-publishing",
   "component": "apps/venue-management-web/src/routes/white-label/AppPublishing.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-102",
    "CMS-014"
   ],
   "exitTo": [
    "CMS-102",
    "CMS-004",
    "CMS-014"
   ],
   "inferred": false,
   "notes": "Reached from the Site Builder after the first publish, and from Publishing when a change is build-time.",
   "transitions": [
    {
     "to": "CMS-102",
     "trigger": "Back to the Site Builder",
     "provenance": "authored 29 September, M24-08",
     "back": true
    },
    {
     "to": "CMS-004",
     "trigger": "App icons and splash",
     "provenance": "authored 29 September, M24-08 (build-time assets)"
    },
    {
     "to": "CMS-014",
     "trigger": "Publish the configuration first",
     "provenance": "authored 29 September, M24-08 (a build is made from a published version)"
    }
   ]
  },
  "notes": "**Added 29 September for M24-08.** TICVAI never publishes a client's app under its own developer account: each client opens and owns its Apple Developer account (with a D-U-N-S number) and its Google Play account, builds its app here from the published configuration, and uploads it, or lets us submit it with its own API credential. The accounts are make-or-break client inputs (`setStoreAccounts`).",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAppBuilds` reads the builds and `getAppBuild` reads one — list, select, act; the checklist sits above the list",
  "purpose": "Get the tenant's own app into the App Store and Google Play under the client's own accounts — checklist, store listing, request a build, download or submit it, follow its review — with a guide for the steps only the client can take.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Before the first build",
       "bindsTo": "StorePublishingChecklist",
       "columns": [
        "StorePublishingChecklist.items",
        "StorePublishingChecklist.accounts"
       ],
       "operation": "getStoreAccounts",
       "notes": "Apple D-U-N-S number, Apple Developer account, Google Play developer account (**the client's to open; we cannot open them for them**), store listing, app icons, a published configuration. Each open item says what to do next.",
       "provenance": "contract white-label.yaml GET /tenant-config/store-accounts"
      },
      {
       "kind": "selectField",
       "label": "Platform",
       "operation": "listAppBuilds",
       "notes": "Sends `?platform=`, iOS or Android.",
       "provenance": "contract white-label.yaml GET /tenant-config/app-builds"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Builds",
       "bindsTo": "AppBuild",
       "columns": [
        "AppBuild.platform",
        "AppBuild.versionName",
        "AppBuild.buildNumber",
        "AppBuild.configVersion",
        "AppBuild.status",
        "AppBuild.requestedAt",
        "AppBuild.finishedAt"
       ],
       "operation": "listAppBuilds",
       "provenance": "contract white-label.yaml GET /tenant-config/app-builds"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected build",
       "bindsTo": "AppBuild",
       "columns": [
        "AppBuild.status",
        "AppBuild.failureReason",
        "AppBuild.packageAssetRef",
        "AppBuild.releaseNotes",
        "AppBuild.submitToStore"
       ],
       "operation": "getAppBuild",
       "notes": "Download the signed package to upload it in App Store Connect or the Play Console; with a credential recorded, the store review status follows here (submitted, in review, approved, rejected, released).",
       "provenance": "contract white-label.yaml GET /tenant-config/app-builds/{appBuildId}"
      },
      {
       "kind": "assistantPanel",
       "label": "App publishing guide",
       "operation": "sendAiMessage",
       "notes": "**The in-platform guide M24-08 asks for**: how to get a D-U-N-S number, open each account, fill the listing and answer store review. Grounded on a store-publishing knowledge source, no tenant data. `unavailable` until the ai \"app publishing guide\" assistant profile exists; the checklist guidance works without it.",
       "provenance": "authored 29 September, M24-08"
      },
      {
       "kind": "publishGate",
       "label": "What a build and a submission do",
       "impliedBy": "requestAppBuild",
       "notes": "Names the configuration version built, the build-time changes it carries (icons, splash, fonts, wallet and payment integrations) and the account it is signed for; with **Submit to the store**, says it goes to the client's store review under the client's account. Needs `TENANT_PUBLISH`.",
       "provenance": "contract white-label.yaml POST /tenant-config/app-builds"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Request a build",
       "operation": "requestAppBuild",
       "permission": "TENANT_PUBLISH",
       "provenance": "contract white-label.yaml POST /tenant-config/app-builds"
      },
      {
       "kind": "secondaryButton",
       "label": "Save store accounts and listing",
       "operation": "setStoreAccounts",
       "provenance": "contract white-label.yaml PUT /tenant-config/store-accounts"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The checklist and the builds, read by `getStoreAccounts` and `listAppBuilds`.",
   "error": "Could not load. Names which read failed.",
   "emptyFirstRun": "**No build yet.** Shows the checklist first: nothing can be built until the client's store account for the platform is recorded and a version is published.",
   "emptyNoResults": "No build for the platform picked. Names it and offers the other.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listAppBuilds` requires, and names that permission."
  },
  "apis": [
   {
    "operationId": "getStoreAccounts",
    "contract": "white-label",
    "purpose": "The client's store accounts and the checklist",
    "trigger": "onLoad"
   },
   {
    "operationId": "setStoreAccounts",
    "contract": "white-label",
    "purpose": "Record the client's own Apple and Google accounts and the store listing",
    "trigger": "onAction",
    "invalidates": [
     "getStoreAccounts"
    ]
   },
   {
    "operationId": "listAppBuilds",
    "contract": "white-label",
    "purpose": "The builds and their store status",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAppBuild",
    "contract": "white-label",
    "purpose": "One build, its package and its review status",
    "trigger": "onAction"
   },
   {
    "operationId": "requestAppBuild",
    "contract": "white-label",
    "purpose": "Build the app from a published version, for the client's account",
    "trigger": "onAction",
    "invalidates": [
     "listAppBuilds"
    ]
   },
   {
    "operationId": "createAiConversation",
    "contract": "ai",
    "purpose": "Open a conversation with the app publishing guide",
    "trigger": "onAction"
   },
   {
    "operationId": "sendAiMessage",
    "contract": "ai",
    "purpose": "Ask the app publishing guide a question",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "appBuildId",
     "from": "navigation",
     "optional": true
    },
    {
     "name": "conversationId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves the tenant from the session and opens on the checklist and the newest build."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-104"
  },
  "apisNote": "Authored 29 September 2026 (P29 pass, M24-08) from impact.json.",
  "overlays": [
   {
    "id": "formSetStoreAccounts",
    "component": "modal",
    "trigger": "Save store accounts and listing",
    "body": "**Collects what `setStoreAccounts` sends**: per store, `accountHolderName`, `developerAccountId`, `appIdentifier`, `dunsNumber` (Apple, nine digits), optional `apiCredentialSecretRef` and the `listing` (name, subtitle, description and keywords in every tenant language, category, support and privacy links, screenshots). Refused `400` for an Apple account without a D-U-N-S number. Dismissing sends nothing.",
    "bindsTo": "StoreAccount",
    "confirm": {
     "label": "Save",
     "operation": "setStoreAccounts"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "accounts"
     ]
    },
    "provenance": "contract white-label.yaml PUT /tenant-config/store-accounts"
   },
   {
    "id": "confirmRequestAppBuild",
    "component": "confirmDialog",
    "trigger": "Request a build",
    "body": "**Names the platform, the version built and the account it is signed for.** Optional release notes and Submit to the store (needs a recorded credential). Refused `409` with the reason when the account is missing, nothing is published, or a build is already running.",
    "confirm": {
     "label": "Build",
     "operation": "requestAppBuild"
    },
    "dismiss": {
     "label": "Cancel"
    },
    "provenance": "contract white-label.yaml POST /tenant-config/app-builds"
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
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
 "createAiConversation": {
  "method": "POST",
  "path": "/conversations",
  "contract": "ai",
  "summary": "Open a conversation",
  "permission": "AI_USE",
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
  "responds": "AiConversation"
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
 "createBookingFlowDefinition": {
  "method": "POST",
  "path": "/venues/{venueId}/booking-flows",
  "contract": "white-label",
  "summary": "Pick a booking flow for a venue",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "BookingFlow",
  "responds": "BookingFlow"
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
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ContentPage",
  "responds": "ContentPage"
 },
 "createGuidedChoice": {
  "method": "POST",
  "path": "/venues/{venueId}/guided-choices",
  "contract": "white-label",
  "summary": "Set up Help me choose for a venue",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "GuidedChoice",
  "responds": "GuidedChoice"
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
 "decideProposedAction": {
  "method": "POST",
  "path": "/proposed-actions/{actionId}/decide",
  "contract": "ai",
  "summary": "Approve or reject a proposal",
  "permission": "AI_USE",
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
  "responds": "ProposedAction"
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
 "deleteBookingFlow": {
  "method": "DELETE",
  "path": "/booking-flows/{bookingFlowId}",
  "contract": "white-label",
  "summary": "Remove a booking flow from a venue",
  "permission": "TENANT_CONFIGURE",
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
 "deleteGuidedChoice": {
  "method": "DELETE",
  "path": "/guided-choices/{guidedChoiceId}",
  "contract": "white-label",
  "summary": "Delete a Help me choose set-up, or dismiss a suggestion",
  "permission": "TENANT_CONFIGURE",
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
 "getAppBuild": {
  "method": "GET",
  "path": "/tenant-config/app-builds/{appBuildId}",
  "contract": "white-label",
  "summary": "One app build, with its package and store status",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "AppBuild"
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
 "getBookingFlow": {
  "method": "GET",
  "path": "/booking-flows/{bookingFlowId}",
  "contract": "white-label",
  "summary": "Read one of a venue's booking flows, every step included",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BookingFlow"
 },
 "getBookingFlowConfig": {
  "method": "GET",
  "path": "/tenant-config/booking-flow",
  "contract": "white-label",
  "summary": "How the guest booking flow looks and steps",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "effectiveForVenueId",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "BookingFlowConfig"
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
 "getGuidedChoiceSuggestion": {
  "method": "GET",
  "path": "/guided-choice-suggestions/{suggestionId}",
  "contract": "ai",
  "summary": "The reasons behind a Help me choose suggestion",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiGuidedChoiceSuggestion"
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
 "getNavigation": {
  "method": "GET",
  "path": "/tenant-config/navigation",
  "contract": "white-label",
  "summary": "Read navigation",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "NavigationConfig"
 },
 "getPublishedBookingFlow": {
  "method": "GET",
  "path": "/venues/{venueId}/booking-flow",
  "contract": "white-label",
  "summary": "The published booking flow a product or category books through",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "productCategoryId",
    "in": "query",
    "required": false
   },
   {
    "name": "flowTypeKey",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "BookingFlow"
 },
 "getSiteSetupProgress": {
  "method": "GET",
  "path": "/tenant-config/site-setup",
  "contract": "white-label",
  "summary": "Where the tenant is in the Site Builder",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "SiteSetupProgress"
 },
 "getStoreAccounts": {
  "method": "GET",
  "path": "/tenant-config/store-accounts",
  "contract": "white-label",
  "summary": "The client's store accounts and the publishing checklist",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "StorePublishingChecklist"
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
 "listAnalyticsProviders": {
  "method": "GET",
  "path": "/tenant-config/analytics-providers",
  "contract": "white-label",
  "summary": "The analytics platforms the storefront and app report to",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": false
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
 "listAppBuilds": {
  "method": "GET",
  "path": "/tenant-config/app-builds",
  "contract": "white-label",
  "summary": "The tenant's app builds, newest first",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "platform",
    "in": "query",
    "required": false
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
 "listBookingFlowTypes": {
  "method": "GET",
  "path": "/booking-flow-types",
  "contract": "white-label",
  "summary": "The booking flow types a venue can pick from, with their steps",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "productKind",
    "in": "query",
    "required": false
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
 "listBookingFlows": {
  "method": "GET",
  "path": "/venues/{venueId}/booking-flows",
  "contract": "white-label",
  "summary": "A venue's booking flows, in the working draft",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "flowTypeKey",
    "in": "query",
    "required": false
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
 "listConsentQuestions": {
  "method": "GET",
  "path": "/consent-questions",
  "contract": "marketing-crm",
  "summary": "The consent questions a venue asks at booking",
  "permission": "GUEST_VIEW",
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
    "name": "status",
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
 "listEvents": {
  "method": "GET",
  "path": "/events",
  "contract": "catalogue",
  "summary": "List events",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
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
 "listGuidedChoices": {
  "method": "GET",
  "path": "/venues/{venueId}/guided-choices",
  "contract": "white-label",
  "summary": "List a venue's Help me choose set-ups",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "source",
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
 "listOrgUnits": {
  "method": "GET",
  "path": "/org-units",
  "contract": "tenancy",
  "summary": "List scope nodes visible to the session",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "under",
    "in": "query",
    "required": null
   },
   {
    "name": "level",
    "in": "query",
    "required": null
   },
   {
    "name": "includeInactive",
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
 "listProductCategories": {
  "method": "GET",
  "path": "/product-categories",
  "contract": "catalogue",
  "summary": "The merchandise hierarchy — categories, brands, collections",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ProductCategoryNode"
 },
 "listProducts": {
  "method": "GET",
  "path": "/products",
  "contract": "catalogue",
  "summary": "List products",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "isSellable",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "segmentTag",
    "in": "query",
    "required": null
   },
   {
    "name": "guidedAnswerIds",
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
 "proposeMarketingContent": {
  "method": "POST",
  "path": "/ai/content-drafts",
  "contract": "ai",
  "summary": "Draft marketing content for a person to edit and apply",
  "permission": "AI_USE",
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
 "publishGuidedChoice": {
  "method": "POST",
  "path": "/guided-choices/{guidedChoiceId}/publish",
  "contract": "white-label",
  "summary": "Publish a Help me choose set-up to guests",
  "permission": "TENANT_PUBLISH",
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
  "responds": "GuidedChoice"
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
 "requestAppBuild": {
  "method": "POST",
  "path": "/tenant-config/app-builds",
  "contract": "white-label",
  "summary": "Build the branded app for a store",
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
 "sendAiMessage": {
  "method": "POST",
  "path": "/conversations/{conversationId}/messages",
  "contract": "ai",
  "summary": "Ask",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AiMessage"
 },
 "setAnalyticsProvider": {
  "method": "PUT",
  "path": "/tenant-config/analytics-providers",
  "contract": "white-label",
  "summary": "Connect the storefront and app to an analytics platform",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "StorefrontAnalyticsProvider",
  "responds": "StorefrontAnalyticsProvider"
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
 "setBookingFlowConfig": {
  "method": "PUT",
  "path": "/tenant-config/booking-flow",
  "contract": "white-label",
  "summary": "Set how the guest booking flow looks and steps",
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
  "requestBody": "BookingFlowConfig",
  "responds": "BookingFlowConfig"
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
   },
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
   },
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
   },
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
   },
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
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "NavigationConfig",
  "responds": "NavigationConfig"
 },
 "setProductCategories": {
  "method": "PUT",
  "path": "/product-categories",
  "contract": "catalogue",
  "summary": "Define the hierarchy, in the order a guest sees it",
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
  "responds": "ProductCategory"
 },
 "setSiteSetupProgress": {
  "method": "PUT",
  "path": "/tenant-config/site-setup",
  "contract": "white-label",
  "summary": "Save the Site Builder's progress",
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
  "requestBody": "SiteSetupProgress",
  "responds": "SiteSetupProgress"
 },
 "setStoreAccounts": {
  "method": "PUT",
  "path": "/tenant-config/store-accounts",
  "contract": "white-label",
  "summary": "Record the client's own Apple and Google store accounts and listings",
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
  "responds": "StorePublishingChecklist"
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
 "suggestGuidedChoice": {
  "method": "POST",
  "path": "/venues/{venueId}/guided-choice-suggestions",
  "contract": "ai",
  "summary": "Suggest a Help me choose set-up from the venue's catalogue",
  "permission": "AI_USE",
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
 "unpublishGuidedChoice": {
  "method": "POST",
  "path": "/guided-choices/{guidedChoiceId}/unpublish",
  "contract": "white-label",
  "summary": "Take a Help me choose set-up off the guest app",
  "permission": "TENANT_PUBLISH",
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
  "responds": "GuidedChoice"
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
 "updateBookingFlowDefinition": {
  "method": "PATCH",
  "path": "/booking-flows/{bookingFlowId}",
  "contract": "white-label",
  "summary": "Reorder a flow's steps, switch optional steps, change its settings",
  "permission": "TENANT_CONFIGURE",
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
  "responds": "BookingFlow"
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
 "updateGuidedChoice": {
  "method": "PATCH",
  "path": "/guided-choices/{guidedChoiceId}",
  "contract": "white-label",
  "summary": "Edit a Help me choose set-up, or review a suggestion",
  "permission": "TENANT_CONFIGURE",
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
  "responds": "GuidedChoice"
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
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Menu"
 },
 "updateProduct": {
  "method": "PATCH",
  "path": "/products/{productId}",
  "contract": "catalogue",
  "summary": "Update a product",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
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
  "requestBody": "UpdateProductRequest",
  "responds": "Product"
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
 },
 "validateBookingFlow": {
  "method": "POST",
  "path": "/booking-flows/{bookingFlowId}/validate",
  "contract": "white-label",
  "summary": "Check a flow against its type",
  "permission": "TENANT_CONFIGURE",
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
  "responds": "BookingFlowValidation"
 },
 "validateTenantConfig": {
  "method": "POST",
  "path": "/tenant-config/validate",
  "contract": "white-label",
  "summary": "Validate the working draft",
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
  "responds": "ConfigValidationReport"
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
 "AiConversation": {
  "type": "object",
  "x-ticvai-persistence": "ai.conversation",
  "required": [
   "id",
   "principalId",
   "module",
   "startedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "module": {
    "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
   },
   "locale": {
    "type": "string"
   },
   "messageCount": {
    "type": "integer"
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastMessageAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AiGuidedChoiceSuggestion": {
  "type": "object",
  "x-ticvai-persistence": "ai.guided_choice_suggestion",
  "description": "**One Help me choose suggestion for a venue** (design 3.11, decided 29 September; C7 at autonomy \"suggest\"). Holds the reasons: the products read, the one or two attributes chosen, the split each makes, the answer mapping and where the wording came from. Its `id` is the `suggestionRef` on the white-label draft (`white-label.proposeGuidedChoice`). Nothing is ever published from here.",
  "required": [
   "venueId",
   "trigger",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "trigger": {
    "type": "string",
    "enum": [
     "productsUploaded",
     "mappedProductWithdrawn",
     "productsUncovered",
     "manual"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "running",
     "proposed",
     "noSuggestion",
     "failed",
     "superseded"
    ],
    "readOnly": true
   },
   "productCount": {
    "type": "integer",
    "minimum": 0,
    "readOnly": true
   },
   "questions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "attribute": {
       "type": "string",
       "description": "The catalogue attribute asked about: audience, level, minimum height or age, duration, price band, format, language."
      },
      "order": {
       "type": "integer",
       "minimum": 1
      },
      "split": {
       "type": "object",
       "additionalProperties": true,
       "description": "How evenly it divides the bookable products: products per answer."
      },
      "droppedBecause": {
       "type": "string",
       "nullable": true,
       "description": "Set where an attribute was considered and dropped (an answer would leave nothing bookable)."
      },
      "answers": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "value": {
          "type": "string"
         },
         "leadsTo": {
          "type": "string",
          "enum": [
           "product",
           "category",
           "flow"
          ]
         },
         "targetRef": {
          "type": "string"
         }
        }
       }
      }
     }
    },
    "readOnly": true,
    "description": "The questions chosen, in the order asked. Deterministic: the same catalogue gives the same questions."
   },
   "wordingSource": {
    "type": "string",
    "enum": [
     "model",
     "attributeNames"
    ],
    "readOnly": true,
    "description": "Where the text came from. `attributeNames` when no model was available: the rules alone still make a usable draft."
   },
   "modelVersion": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "promptTemplateVersion": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "guidedChoiceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The white-label draft `GuidedChoice` it produced."
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiMessage": {
  "type": "object",
  "x-ticvai-persistence": "ai.message",
  "required": [
   "id",
   "conversationId",
   "role",
   "content",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "conversationId": {
    "type": "string",
    "format": "uuid"
   },
   "role": {
    "type": "string",
    "enum": [
     "user",
     "assistant",
     "system"
    ]
   },
   "content": {
    "type": "string"
   },
   "sources": {
    "$ref": "#/components/schemas/AiSourceList"
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "description": "8.1.5, 8.3.67. **Nullable on purpose** — a provider that does not report confidence must yield null rather than an invented number, and an interface showing 0.9 because the code defaulted it is worse than showing nothing.\n"
   },
   "rationale": {
    "type": "string",
    "nullable": true,
    "description": "8.3.68, 8.3.69."
   },
   "proposedAction": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProposedAction"
     }
    ],
    "nullable": true,
    "description": "Present where the answer suggests a change. **A draft, never applied here.**"
   },
   "traceId": {
    "type": "string"
   },
   "provider": {
    "$ref": "#/components/schemas/AiProviderKind"
   },
   "model": {
    "type": "string"
   },
   "promptTokens": {
    "type": "integer"
   },
   "completionTokens": {
    "type": "integer"
   },
   "latencyMs": {
    "type": "integer"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AiProviderKind": {
  "type": "string",
  "enum": [
   "openai",
   "gemini",
   "anthropic",
   "azureOpenai",
   "localLlm",
   "openaiCompatible"
  ],
  "description": "`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"
 },
 "AiSourceList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n",
  "items": {
   "$ref": "#/components/schemas/AiSource"
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
 "AppBuild": {
  "x-ticvai-persistence": "whitelabel.app_build",
  "type": "object",
  "description": "**One build of the tenant's branded app (decided 24 September, M24-08).** Made from a published `ConfigVersion`, signed for the client's own store account.\n",
  "required": [
   "id",
   "platform",
   "configVersion",
   "status",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "platform": {
    "type": "string",
    "enum": [
     "ios",
     "android"
    ]
   },
   "configVersion": {
    "type": "string",
    "description": "The `ConfigVersion.version` built."
   },
   "storeAccountId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "versionName": {
    "type": "string",
    "readOnly": true,
    "description": "The marketing version, e.g. 1.4.0."
   },
   "buildNumber": {
    "type": "integer",
    "readOnly": true
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "queued",
     "building",
     "built",
     "failed",
     "submitted",
     "inReview",
     "approved",
     "rejected",
     "released"
    ],
    "description": "`queued` to `built` or `failed` is the build service's; from `submitted` on it is read from the store with the client's credential, or stays `built` when the client uploads by hand."
   },
   "failureReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "packageAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The signed .ipa or .aab in the `assets` library, for the client to download and upload."
   },
   "releaseNotes": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "submitToStore": {
    "type": "boolean",
    "default": false
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "finishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The partition key (ADR-0005). Written at `tenant` scope."
   }
  }
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
 "BookingFlowLevelSettings": {
  "x-ticvai-persistence": "none — jsonb column on whitelabel.booking_flow",
  "type": "object",
  "description": "**The settings that belong to one flow, not to the venue (decided 29 September, W12).** Moved here from `BookingFlowSettings`, which keeps the venue-wide ones. Each keeps its rev 3 meaning and default. A field left out takes its default.\n",
  "properties": {
   "performanceReveal": {
    "type": "string",
    "enum": [
     "dateTimeTicket",
     "allAtOnce"
    ],
    "default": "dateTimeTicket",
    "description": "**Performance reveal (rev 3 REV3-2).** `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. Product-first (W8) is the step order of `experienceWorkshop`, not a value here.\n"
   },
   "signInAt": {
    "type": "string",
    "enum": [
     "afterAddOns",
     "atPayment"
    ],
    "default": "afterAddOns",
    "description": "**Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3).** `afterAddOns` asks as the guest leaves the extras step; `atPayment` asks at payment. The basket is kept either way.\n"
   },
   "seatEventDateMode": {
    "type": "string",
    "enum": [
     "inlineStep",
     "popupOnSeatMap"
    ],
    "default": "inlineStep",
    "description": "**Date and time on a seated event (rev 3 REV3-4).** `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. Read only by the seated flow types.\n"
   },
   "extrasStep": {
    "type": "string",
    "enum": [
     "auto",
     "always",
     "never"
    ],
    "default": "auto",
    "description": "`auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off."
   },
   "quickTour": {
    "type": "boolean",
    "default": false,
    "description": "**Quick tour (rev 3 REV3-20).** A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. Seen-state kept on the device only.\n"
   },
   "consentQuestionIds": {
    "type": "array",
    "maxItems": 10,
    "uniqueItems": true,
    "default": [],
    "description": "**The flow's own consent questions (rev 3 REV3-26).** Asked on every booking through this flow, together with those of each product in the cart, each question once. Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. A Help me choose answer may pre-fill one (`GuidedChoice` `consentPrefill`); the guest still confirms it.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "BookingFlowSettings": {
  "type": "object",
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "description": "**Every guest booking-flow setting, once.** `BookingFlowConfig` is these at tenant level plus `venueOverrides`; a `BookingFlowVenueOverride` carries any subset of them for one venue (decided 29 September, rev 3 CFG-11). The Rev 3 settings (`timesPerPage` onwards) are the options the client's rev 3 prototype shows under Config → Booking rules and Build your experience.\n**Venue-wide only (decided 29 September, W12).** The settings that belong to one flow moved to `BookingFlowLevelSettings` on each `BookingFlow`; `categoryDisplay` was removed (W7).\n",
  "properties": {
   "preset": {
    "type": "string",
    "enum": [
     "auto",
     "ticketBox",
     "playCentre",
     "venueSite",
     "marketplace",
     "singleEvent",
     "season",
     "custom"
    ],
    "default": "auto",
    "description": "L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. The UI preset of the prototype's drawer (rev 3 CFG-1, no change)."
   },
   "stepIndicator": {
    "type": "string",
    "enum": [
     "bar",
     "numbered",
     "dots",
     "segmented",
     "breadcrumb",
     "pills",
     "ticks",
     "none"
    ],
    "default": "bar"
   },
   "cartLayout": {
    "type": "string",
    "enum": [
     "sidebarRight",
     "sidebarLeft",
     "slideInRight",
     "slideUpBottom",
     "singleColumn",
     "floatingIcon"
    ],
    "default": "sidebarRight",
    "description": "`floatingIcon` is a round basket button with the item count that opens the cart (decided 29 September, rev 3 REV3-10). Which side a sidebar or the icon sits on in a right-to-left language is `cartSideInRtl`."
   },
   "cartSideInRtl": {
    "type": "string",
    "enum": [
     "keepRight",
     "mirror"
    ],
    "default": "keepRight",
    "description": "**The cart side when the guest reads Arabic or another right-to-left language (decided 29 September, rev 3 REV3-10).** `keepRight` keeps the cart (and the floating icon) on the right, as the client confirmed; `mirror` flips it to the left with the rest of the layout.\n"
   },
   "cardLayout": {
    "type": "string",
    "enum": [
     "stackedRows",
     "splitRows",
     "cardsAcross",
     "posterCards"
    ],
    "default": "stackedRows",
    "description": "How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked rows, Split rows, Cards across and Poster cards."
   },
   "cardSize": {
    "type": "string",
    "enum": [
     "compact",
     "standard",
     "large",
     "extraLarge"
    ],
    "default": "compact",
    "description": "Labels Compact, Standard, Large, Extra large (decided 29 September, rev 3 DG-6). `standard` replaces `regular`."
   },
   "seatPicker": {
    "type": "string",
    "enum": [
     "bowl",
     "zonesThenSeats",
     "zonesOnly",
     "seatsOnly"
    ],
    "default": "bowl",
    "description": "Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event."
   },
   "mapView": {
    "type": "string",
    "enum": [
     "2d",
     "3d"
    ],
    "default": "3d"
   },
   "density": {
    "type": "string",
    "enum": [
     "compact",
     "standard",
     "roomy"
    ],
    "default": "compact",
    "description": "Labels Compact, Standard, Roomy, default Compact as the design has it (decided 29 September, rev 3 DG-6). `standard` and `roomy` replace `comfortable` and `airy`."
   },
   "embedMode": {
    "type": "string",
    "enum": [
     "fullPage",
     "embedded"
    ],
    "default": "fullPage",
    "description": "`embedded` hides the hero banner, event page and venue header, for a flow placed inside the venue's own site."
   },
   "heroBanner": {
    "type": "boolean",
    "default": true
   },
   "searchInBanner": {
    "type": "boolean",
    "default": false,
    "description": "Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6)."
   },
   "eventBannerDates": {
    "type": "boolean",
    "default": false,
    "description": "**Dates in event banner (decided 29 September, rev 3 23SEP-19).** On, the event banner lists the next dates; off by default. Either way the date picker sits at the top of the booking step.\n"
   },
   "singleEventPage": {
    "type": "boolean",
    "default": false
   },
   "quantitiesOnAddOns": {
    "type": "boolean",
    "default": true
   },
   "timesPerPage": {
    "type": "string",
    "enum": [
     "8",
     "12",
     "24",
     "all"
    ],
    "default": "24",
    "description": "**Times per page (decided 29 September, rev 3 REV3-1).** When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` shows every one. A string because `all` is one of the values.\n"
   },
   "dayPartFilter": {
    "type": "boolean",
    "default": true,
    "description": "**Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1).** Where each part begins is `dayPartBoundaries`.\n"
   },
   "dayPartBoundaries": {
    "type": "object",
    "description": "**Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1).** Morning is before `afternoonStartsAt`, afternoon runs to `eveningStartsAt`, evening is from `eveningStartsAt`. A venue sets its own through `venueOverrides`. `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400.\n",
    "properties": {
     "afternoonStartsAt": {
      "type": "string",
      "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
      "default": "12:00"
     },
     "eveningStartsAt": {
      "type": "string",
      "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
      "default": "17:00"
     }
    }
   },
   "seatViewPosition": {
    "type": "string",
    "enum": [
     "bottom",
     "right",
     "left",
     "top"
    ],
    "default": "bottom",
    "description": "**Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5).** Web only; on mobile and on a narrow screen it is always below the map.\n"
   },
   "seatTimeBar": {
    "type": "boolean",
    "default": true,
    "description": "**Time bar above the seat map (decided 29 September, rev 3 REV3-6).** Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one.\n"
   },
   "ticketCategories": {
    "type": "string",
    "enum": [
     "categoryThenSubcategory",
     "flatList"
    ],
    "default": "categoryThenSubcategory",
    "description": "**How tickets are grouped (decided 29 September, rev 3 REV3-16).** `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once.\n"
   },
   "ticketTags": {
    "type": "boolean",
    "default": true,
    "description": "**Tags on tickets (decided 29 September, rev 3 23SEP-3).** Shows a product's display tags (such as \"2 Hours\", \"Min 1.10 m\", \"Valid 90 days\") on its card.\n"
   },
   "cardInfo": {
    "type": "boolean",
    "default": true,
    "description": "**Extra info on cards (decided 29 September, rev 3 23SEP-6).** Shows each ticket type's description, who it is for and what it includes, under its name.\n"
   },
   "conciergeMascot": {
    "type": "boolean",
    "default": true,
    "description": "**The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5).** Read only where the `aiConciergeChat` feature is on.\n"
   },
   "showInfoOnly": {
    "type": "boolean",
    "default": true,
    "description": "**Show info-only products (decided 29 September, rev 3 REV3-14).** On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it.\n"
   },
   "locationSwitcher": {
    "type": "boolean",
    "default": false,
    "description": "**Location switcher (decided 29 September, rev 3 REV3-18).** On, the booking screens carry a \"Booking at\" bar with Change location, reusing the guest's venue choice (audit R267). Off unless the tenant or venue enables it; it has no effect for a tenant with one venue.\n"
   },
   "guestContactFields": {
    "type": "array",
    "minItems": 1,
    "maxItems": 3,
    "uniqueItems": true,
    "default": [
     "email"
    ],
    "items": {
     "type": "string",
     "enum": [
      "email",
      "mobile",
      "name"
     ]
    },
    "description": "**What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1).** The prototype's Email only, + name and + mobile. Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.matchBy`), or 400. After the code is verified the guest is not asked for these again: the flow goes to the terms and payment, and the profile is completed later (WEB-020, GST-039). Read only where the `guestCheckout` feature is on.\n"
   },
   "dateStripDays": {
    "type": "integer",
    "minimum": 3,
    "maximum": 31,
    "default": 7,
    "description": "**The date strip (decided 17 September, M17-08).** How many days from today the date step shows as a strip before the calendar icon that opens the full month; later dates are picked from the calendar.\n"
   }
  }
 },
 "BookingFlowStep": {
  "x-ticvai-persistence": "whitelabel.booking_flow_step",
  "type": "object",
  "description": "One step of a venue's flow, in the venue's order (decided 29 September, W12).",
  "required": [
   "stepKey",
   "enabled",
   "sortOrder"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "stepKey": {
    "$ref": "#/components/schemas/BookingFlowStepKey"
   },
   "enabled": {
    "type": "boolean",
    "description": "A `required` step cannot be off; the flow saves and `isValid` turns false."
   },
   "sortOrder": {
    "type": "integer",
    "minimum": 0
   },
   "requirement": {
    "type": "string",
    "enum": [
     "required",
     "optional",
     "conditional"
    ],
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "From the flow type, so the CMS can mark the step without a second read."
   },
   "settings": {
    "type": "object",
    "additionalProperties": true,
    "default": {},
    "description": "The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. `languages` on `language`, `minHours` on `duration`). A name the type does not give is refused with 400."
   }
  }
 },
 "BookingFlowStepKey": {
  "type": "string",
  "description": "Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02; which types carry which steps is `x-ticvai-system-catalogue` on `BookingFlowType`. `payment` is always last. Sign-in is not a step: it is asked where the flow's `signInAt` says.\n",
  "enum": [
   "location",
   "helpMeChoose",
   "product",
   "date",
   "time",
   "performance",
   "level",
   "language",
   "duration",
   "route",
   "partySize",
   "resourceMap",
   "resourceSize",
   "seatMap",
   "tickets",
   "attendees",
   "membershipPlan",
   "giftCardValue",
   "recipient",
   "consent",
   "extras",
   "review",
   "payment"
  ]
 },
 "BookingFlowType": {
  "x-ticvai-persistence": "none — system catalogue, shipped with the service and the same for every tenant",
  "type": "object",
  "description": "**A flow type from the system catalogue (decided 29 September, W12).** Read-only: a venue picks one (`createBookingFlowDefinition`) and orders its steps within `orderConstraints`. `requirement` is `required` (cannot be turned off), `optional` (the venue chooses) or `conditional` (shown to a guest only when `condition` holds; the venue may still turn it off where it is not also required by law or by a product, as the condition says). `settingsOwned` names the settings, venue-wide (`BookingFlowSettings`) or flow-level (`BookingFlowLevelSettings`), that the CMS shows beside the step; `stepSettings` are the step's own settings, kept in `BookingFlowStep.settings`.\n",
  "x-ticvai-system-catalogue": {
   "commonConstraints": [
    {
     "kind": "last",
     "stepKey": "payment"
    },
    {
     "kind": "first",
     "stepKey": "location"
    },
    {
     "kind": "before",
     "stepKey": "helpMeChoose",
     "otherStepKey": "tickets"
    },
    {
     "kind": "before",
     "stepKey": "helpMeChoose",
     "otherStepKey": "product"
    },
    {
     "kind": "before",
     "stepKey": "tickets",
     "otherStepKey": "extras"
    },
    {
     "kind": "before",
     "stepKey": "tickets",
     "otherStepKey": "consent"
    },
    {
     "kind": "before",
     "stepKey": "review",
     "otherStepKey": "payment"
    }
   ],
   "commonConditions": {
    "location": "the tenant has more than one active venue and `locationSwitcher` is on",
    "helpMeChoose": "the venue has a published `GuidedChoice`",
    "consent": "the flow's `consentQuestionIds` or a product in the cart asks a consent question (REV3-26); cannot be turned off while either does",
    "attendees": "a product in the cart asks attendee details"
   },
   "types": [
    {
     "key": "datedDayPass",
     "productKinds": [
      "admission",
      "datedAdmission"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "helpMeChoose",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays",
        "performanceReveal"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketCategories",
        "ticketTags",
        "cardInfo",
        "cardLayout",
        "cardSize",
        "showInfoOnly"
       ]
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ]
    },
    {
     "key": "timedEntry",
     "productKinds": [
      "timedAdmission"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "helpMeChoose",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays",
        "performanceReveal"
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries",
        "performanceReveal"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketCategories",
        "ticketTags",
        "cardInfo",
        "cardLayout",
        "cardSize",
        "showInfoOnly"
       ]
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      }
     ]
    },
    {
     "key": "openDated",
     "productKinds": [
      "openDated",
      "admission"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "helpMeChoose",
       "requirement": "conditional"
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketCategories",
        "ticketTags",
        "cardInfo",
        "cardLayout",
        "cardSize",
        "showInfoOnly"
       ]
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ]
    },
    {
     "key": "seatedFixedPerformance",
     "productKinds": [
      "seated"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "performance",
       "requirement": "required",
       "condition": "skipped for the guest when the event has one on-sale performance"
      },
      {
       "stepKey": "seatMap",
       "requirement": "required",
       "settingsOwned": [
        "seatPicker",
        "seatViewPosition",
        "seatTimeBar",
        "mapView"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "conditional",
       "condition": "the seat's price category has more than one ticket type (adult or child)"
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "performance",
       "otherStepKey": "seatMap"
      }
     ]
    },
    {
     "key": "seatedDateTimeSeatMap",
     "productKinds": [
      "seated"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays",
        "seatEventDateMode"
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries",
        "seatEventDateMode"
       ]
      },
      {
       "stepKey": "seatMap",
       "requirement": "required",
       "settingsOwned": [
        "seatPicker",
        "seatViewPosition",
        "seatTimeBar",
        "mapView",
        "seatEventDateMode"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "conditional",
       "condition": "the seat's price category has more than one ticket type"
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      },
      {
       "kind": "before",
       "stepKey": "time",
       "otherStepKey": "seatMap"
      }
     ]
    },
    {
     "key": "experienceWorkshop",
     "productKinds": [
      "timedAdmission",
      "admission"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "helpMeChoose",
       "requirement": "conditional"
      },
      {
       "stepKey": "product",
       "requirement": "required",
       "settingsOwned": [
        "cardLayout",
        "cardSize",
        "cardInfo",
        "showInfoOnly"
       ]
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays",
        "performanceReveal"
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketCategories",
        "ticketTags"
       ]
      },
      {
       "stepKey": "attendees",
       "requirement": "conditional"
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "product",
       "otherStepKey": "date"
      },
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      }
     ]
    },
    {
     "key": "surfSession",
     "productKinds": [
      "timedAdmission",
      "rental"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays"
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries"
       ]
      },
      {
       "stepKey": "level",
       "requirement": "required",
       "stepSettings": [
        {
         "name": "levels",
         "type": "string[]",
         "note": "level tags offered",
         "from the products' segmentTags": null
        }
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketTags",
        "cardInfo"
       ]
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      },
      {
       "kind": "before",
       "stepKey": "time",
       "otherStepKey": "level"
      }
     ]
    },
    {
     "key": "meetingRoomHourly",
     "productKinds": [
      "rental"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays"
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries"
       ]
      },
      {
       "stepKey": "duration",
       "requirement": "required",
       "stepSettings": [
        {
         "name": "minHours",
         "type": "integer",
         "default": 1
        },
        {
         "name": "maxHours",
         "type": "integer",
         "default": 8
        },
        {
         "name": "stepMinutes",
         "type": "integer",
         "default": 60
        }
       ]
      },
      {
       "stepKey": "partySize",
       "requirement": "optional",
       "stepSettings": [
        {
         "name": "minGuests",
         "type": "integer",
         "default": 1
        },
        {
         "name": "maxGuests",
         "type": "integer"
        }
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      },
      {
       "kind": "before",
       "stepKey": "time",
       "otherStepKey": "duration"
      }
     ]
    },
    {
     "key": "cabanaMap",
     "productKinds": [
      "rental"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays"
       ]
      },
      {
       "stepKey": "resourceMap",
       "requirement": "required",
       "condition": "the venue's resource selection policy lets the guest choose (resources setResourceSelectionPolicy guestMayChoose; REV3-15)",
       "settingsOwned": [
        "mapView"
       ]
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "resourceMap"
      }
     ]
    },
    {
     "key": "cabanaBySize",
     "productKinds": [
      "rental"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays"
       ]
      },
      {
       "stepKey": "partySize",
       "requirement": "required",
       "stepSettings": [
        {
         "name": "minGuests",
         "type": "integer",
         "default": 1
        },
        {
         "name": "maxGuests",
         "type": "integer"
        }
       ]
      },
      {
       "stepKey": "resourceSize",
       "requirement": "required",
       "note": "the server assigns a unit of the chosen size"
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "resourceSize"
      },
      {
       "kind": "before",
       "stepKey": "partySize",
       "otherStepKey": "resourceSize"
      }
     ]
    },
    {
     "key": "guidedTourByLanguage",
     "productKinds": [
      "timedAdmission"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays"
       ]
      },
      {
       "stepKey": "language",
       "requirement": "required",
       "stepSettings": [
        {
         "name": "languages",
         "type": "string[]",
         "note": "ISO 639-1 codes the tours run in"
        }
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketCategories",
        "ticketTags"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      },
      {
       "kind": "before",
       "stepKey": "language",
       "otherStepKey": "time"
      }
     ]
    },
    {
     "key": "transport",
     "productKinds": [
      "admission",
      "timedAdmission"
     ],
     "steps": [
      {
       "stepKey": "route",
       "requirement": "required"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays"
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketCategories"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "route",
       "otherStepKey": "time"
      },
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      }
     ]
    },
    {
     "key": "tableReservation",
     "productKinds": [
      "fnb"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "conditional"
      },
      {
       "stepKey": "date",
       "requirement": "required",
       "settingsOwned": [
        "dateStripDays"
       ]
      },
      {
       "stepKey": "partySize",
       "requirement": "required",
       "stepSettings": [
        {
         "name": "minGuests",
         "type": "integer",
         "default": 1
        },
        {
         "name": "maxGuests",
         "type": "integer",
         "default": 12
        }
       ]
      },
      {
       "stepKey": "time",
       "requirement": "required",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "note": "pre-order",
       "settingsOwned": [
        "extrasStep"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "conditional",
       "condition": "the venue takes a deposit or pre-order for the table",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      },
      {
       "kind": "before",
       "stepKey": "partySize",
       "otherStepKey": "time"
      }
     ]
    },
    {
     "key": "membership",
     "productKinds": [
      "membership"
     ],
     "steps": [
      {
       "stepKey": "membershipPlan",
       "requirement": "required"
      },
      {
       "stepKey": "attendees",
       "requirement": "required",
       "note": "each member's details"
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "membershipPlan",
       "otherStepKey": "attendees"
      }
     ]
    },
    {
     "key": "giftCard",
     "productKinds": [
      "giftCard"
     ],
     "steps": [
      {
       "stepKey": "giftCardValue",
       "requirement": "required"
      },
      {
       "stepKey": "recipient",
       "requirement": "required"
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ]
    },
    {
     "key": "multiLocation",
     "productKinds": [
      "admission",
      "timedAdmission",
      "datedAdmission"
     ],
     "steps": [
      {
       "stepKey": "location",
       "requirement": "required",
       "settingsOwned": [
        "locationSwitcher"
       ]
      },
      {
       "stepKey": "helpMeChoose",
       "requirement": "conditional"
      },
      {
       "stepKey": "product",
       "requirement": "required",
       "settingsOwned": [
        "cardLayout",
        "cardSize",
        "cardInfo"
       ]
      },
      {
       "stepKey": "date",
       "requirement": "conditional",
       "condition": "the product is dated or timed",
       "settingsOwned": [
        "dateStripDays",
        "performanceReveal"
       ]
      },
      {
       "stepKey": "time",
       "requirement": "conditional",
       "condition": "the product is timed",
       "settingsOwned": [
        "timesPerPage",
        "dayPartFilter",
        "dayPartBoundaries"
       ]
      },
      {
       "stepKey": "tickets",
       "requirement": "required",
       "settingsOwned": [
        "ticketCategories",
        "ticketTags"
       ]
      },
      {
       "stepKey": "consent",
       "requirement": "conditional",
       "settingsOwned": [
        "consentQuestionIds"
       ]
      },
      {
       "stepKey": "extras",
       "requirement": "optional",
       "settingsOwned": [
        "extrasStep",
        "quantitiesOnAddOns"
       ]
      },
      {
       "stepKey": "review",
       "requirement": "optional"
      },
      {
       "stepKey": "payment",
       "requirement": "required",
       "settingsOwned": [
        "signInAt"
       ]
      }
     ],
     "orderConstraints": [
      {
       "kind": "before",
       "stepKey": "location",
       "otherStepKey": "product"
      },
      {
       "kind": "before",
       "stepKey": "date",
       "otherStepKey": "time"
      }
     ]
    }
   ]
  },
  "required": [
   "key",
   "name",
   "productKinds",
   "steps",
   "orderConstraints"
  ],
  "properties": {
   "key": {
    "$ref": "#/components/schemas/BookingFlowTypeKey"
   },
   "name": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "description": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "productKinds": {
    "type": "array",
    "description": "The catalogue `ProductKind` values this type books. A venue's default flow for a type serves every product of these kinds that names no flow of its own.",
    "items": {
     "type": "string"
    }
   },
   "steps": {
    "type": "array",
    "description": "In the type's default order.",
    "items": {
     "type": "object",
     "required": [
      "stepKey",
      "requirement",
      "defaultSortOrder"
     ],
     "properties": {
      "stepKey": {
       "$ref": "#/components/schemas/BookingFlowStepKey"
      },
      "requirement": {
       "type": "string",
       "enum": [
        "required",
        "optional",
        "conditional"
       ]
      },
      "condition": {
       "allOf": [
        {
         "$ref": "#/components/schemas/LocalisedText"
        }
       ],
       "nullable": true,
       "description": "For `conditional`, when a guest meets the step."
      },
      "defaultEnabled": {
       "type": "boolean",
       "default": true
      },
      "defaultSortOrder": {
       "type": "integer",
       "minimum": 0
      },
      "settingsOwned": {
       "type": "array",
       "description": "Names of `BookingFlowSettings` (venue-wide) or `BookingFlowLevelSettings` (this flow) fields shown beside the step.",
       "items": {
        "type": "string"
       }
      },
      "stepSettings": {
       "type": "array",
       "description": "The step's own settings, kept in `BookingFlowStep.settings`.",
       "items": {
        "type": "object",
        "required": [
         "name",
         "type"
        ],
        "properties": {
         "name": {
          "type": "string"
         },
         "type": {
          "type": "string"
         },
         "default": {
          "description": "The value when the venue sets none."
         }
        }
       }
      }
     }
    }
   },
   "orderConstraints": {
    "type": "array",
    "description": "`first` and `last` pin a step; `before` puts `stepKey` somewhere ahead of `otherStepKey`. The common constraints (payment last, location first, Help me choose before the products) apply to every type as well as these.",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "stepKey"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "first",
        "last",
        "before"
       ]
      },
      "stepKey": {
       "$ref": "#/components/schemas/BookingFlowStepKey"
      },
      "otherStepKey": {
       "allOf": [
        {
         "$ref": "#/components/schemas/BookingFlowStepKey"
        }
       ],
       "nullable": true,
       "description": "Required when `kind` is `before`."
      }
     }
    }
   }
  }
 },
 "BookingFlowTypeKey": {
  "type": "string",
  "description": "**The flow types the system catalogue offers (decided 29 September, W12; impact.md b).** `seatedFixedPerformance` and `seatedDateTimeSeatMap` are the two seated flows; `cabanaMap` and `cabanaBySize` are the two cabana flows (W6); `experienceWorkshop` puts the product before the date (W8); `multiLocation` opens on the location switcher.\n",
  "enum": [
   "datedDayPass",
   "timedEntry",
   "openDated",
   "seatedFixedPerformance",
   "seatedDateTimeSeatMap",
   "experienceWorkshop",
   "surfSession",
   "meetingRoomHourly",
   "cabanaMap",
   "cabanaBySize",
   "guidedTourByLanguage",
   "transport",
   "tableReservation",
   "membership",
   "giftCard",
   "multiLocation"
  ]
 },
 "BookingFlowValidation": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "valid",
   "problems"
  ],
  "properties": {
   "valid": {
    "type": "boolean"
   },
   "problems": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "stepKey",
      "message"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "requiredStepDisabled",
        "orderConstraintBroken",
        "conditionNeverHolds",
        "stepNotInType",
        "duplicateStep",
        "unknownStepSetting"
       ]
      },
      "stepKey": {
       "$ref": "#/components/schemas/BookingFlowStepKey"
      },
      "otherStepKey": {
       "allOf": [
        {
         "$ref": "#/components/schemas/BookingFlowStepKey"
        }
       ],
       "nullable": true,
       "description": "For `orderConstraintBroken`, the step it must come before or after."
      },
      "message": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "BookingFlowVenueOverride": {
  "type": "object",
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "description": "**One venue's booking-flow settings where they differ from the tenant's (decided 29 September, rev 3 CFG-11).** `settings` carries only the fields the venue changes; a field left out inherits the tenant value, and the schema defaults do not apply inside an override.\n",
  "required": [
   "venueId",
   "settings"
  ],
  "properties": {
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "One of the tenant's active venues. At most one override per venue."
   },
   "settings": {
    "$ref": "#/components/schemas/BookingFlowSettings"
   }
  }
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
 "ChangeScope": {
  "type": "string",
  "description": "Whether a change reaches guests on publish or needs a store release.\n",
  "enum": [
   "runtime",
   "buildTime"
  ]
 },
 "Channel": {
  "type": "string",
  "enum": [
   "pos",
   "kiosk",
   "web",
   "mobile",
   "b2b",
   "ota",
   "callCentre"
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
 "ConfigFindingKind": {
  "type": "string",
  "enum": [
   "missingTranslation",
   "navigationTargetsDisabledModule",
   "homepageReferencesMissingContent",
   "contrastFailure",
   "missingRequiredAsset",
   "policyVersionMissing",
   "noVisibleNavigationItems",
   "unlicensedModuleEnabled",
   "arabicFontMissing",
   "bookingFlowInvalid",
   "bookingFlowMissing"
  ]
 },
 "ConfigValidationReport": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "passed",
   "errorCount",
   "warningCount",
   "findings"
  ],
  "properties": {
   "passed": {
    "type": "boolean"
   },
   "errorCount": {
    "type": "integer"
   },
   "warningCount": {
    "type": "integer"
   },
   "findings": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "severity",
      "message"
     ],
     "properties": {
      "kind": {
       "$ref": "#/components/schemas/ConfigFindingKind"
      },
      "severity": {
       "type": "string",
       "enum": [
        "error",
        "warning"
       ]
      },
      "message": {
       "type": "string"
      },
      "area": {
       "type": "string"
      },
      "reference": {
       "type": "string",
       "nullable": true
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
 "ConsentQuestion": {
  "type": "object",
  "x-ticvai-persistence": "marketing.consent_question + marketing.consent_question_version",
  "description": "**A venue-defined consent question asked at booking** (decided 29 September, rev 3 REV3-26). Each version's text is kept in `consent_question_version`, so an answer always points at the exact words the guest saw. Attached to products by the catalogue and to booking flows by the white-label flow configuration; one or several per flow, as the venue chooses.\n",
  "required": [
   "id",
   "kind",
   "text",
   "version",
   "scope",
   "required",
   "blockingAnswer",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "readOnly": true
   },
   "kind": {
    "$ref": "#/components/schemas/ConsentQuestionKind"
   },
   "text": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "The question as the guest reads it, per locale."
   },
   "helpText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   },
   "version": {
    "type": "integer",
    "minimum": 1,
    "readOnly": true,
    "description": "Raised by one each time the question changes (`updateConsentQuestion`)."
   },
   "scope": {
    "type": "string",
    "enum": [
     "perPerson",
     "perBooking"
    ],
    "default": "perPerson",
    "description": "Asked for each declared person, or once for the whole booking."
   },
   "required": {
    "type": "boolean",
    "default": true,
    "description": "Checkout waits until it is answered (`orders.checkoutCart` 422 `consentRequired`)."
   },
   "blockingAnswer": {
    "type": "string",
    "enum": [
     "yes",
     "no",
     "none"
    ],
    "default": "none",
    "description": "The answer that stops the booking, for the person or the booking it covers. `none` records the answer and blocks nothing."
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "retired"
    ],
    "default": "active"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "ConsentQuestionKind": {
  "type": "string",
  "description": "What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others are recorded and checked as the venue set them.",
  "enum": [
   "swim",
   "scuba",
   "risk",
   "custom"
  ]
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
 "Event": {
  "x-ticvai-persistence": "catalogue.event",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "scopePath"
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
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "parentEventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For grouped events."
   },
   "performanceCount": {
    "type": "integer",
    "readOnly": true,
    "description": "How many performances the event has. Counted by the server; never sent by a client."
   },
   "isActive": {
    "type": "boolean"
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
 "GuestListing": {
  "type": "string",
  "enum": [
   "bookable",
   "infoOnly",
   "hidden"
  ],
  "default": "bookable",
  "description": "**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"
 },
 "GuidedChoice": {
  "x-ticvai-persistence": "whitelabel.guided_choice + whitelabel.guided_choice_question + whitelabel.guided_choice_answer",
  "type": "object",
  "description": "**Help me choose (decided 29 September, rev 3 REV3-11).** A venue's short set of questions that ends on a result card opening the booking flow, product, category or event that fits. Each question has a few answers with a title, a one-line body, an icon and an optional badge; **the answer the guest picks on the last question decides the result**, and each earlier answer carries a target too, so a one-question setting still ends on a result. Venue configuration, never hard-coded: set up in Venue Management, off unless the venue publishes one.\n**Two sources, one review.** `manual` is written by staff; `aiSuggested` is proposed by the `ai` service from the venue's uploaded products (a suggestion, reviewed and published by a person, never auto-published). Both arrive as `draft`.\n**Help me choose filters the catalogue (decided 29 September, W4).** With `behaviour` `filter`, the default, each answer's `filter` narrows the products the guest sees (web, mobile and kiosk alike, through catalogue `listProducts` and `searchCatalogue` `guidedAnswerIds`), with a \"Show everything\" link; `recommend` keeps the rev 3 result card from the last answer's `target`. **It is never a consent step**: an answer may pre-fill a REV3-26 consent question (`consentPrefill`), which the guest still confirms, so the question is not asked twice and the consent stays explicit.\n",
  "required": [
   "id",
   "venueId",
   "name",
   "mode",
   "questions",
   "status",
   "source"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "readOnly": true,
    "description": "ULID."
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of `createGuidedChoice`."
   },
   "name": {
    "type": "string",
    "maxLength": 80,
    "description": "Staff-facing name, e.g. \"Water park day planner\". Not shown to guests."
   },
   "mode": {
    "type": "string",
    "enum": [
     "button",
     "popupOnArrival",
     "off"
    ],
    "default": "button",
    "description": "**How the guest reaches it (rev 3 REV3-11).** `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on the guest's first arrival at the booking page (whether it was seen is kept on the device only); `off` keeps a published choice configured but not shown.\n"
   },
   "showBanner": {
    "type": "boolean",
    "default": true,
    "description": "The dark banner under the products (\"Choose from the experiences above or let us help you decide\") with a Help me choose button. Ignored when `mode` is `off`."
   },
   "behaviour": {
    "type": "string",
    "enum": [
     "filter",
     "recommend"
    ],
    "default": "filter",
    "description": "**`filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4).** With `filter`, every answer needs a `filter` and `target` is optional; with `recommend`, every answer on the last question needs a `target`. `publishGuidedChoice` refuses the other case with 422.\n"
   },
   "showEverything": {
    "type": "boolean",
    "default": true,
    "description": "The \"Show everything\" link under a filtered list, which clears the answers (W4)."
   },
   "questions": {
    "type": "array",
    "minItems": 1,
    "maxItems": 4,
    "description": "**One to four questions** (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). Shown in `sortOrder`.\n",
    "items": {
     "type": "object",
     "required": [
      "title",
      "sortOrder",
      "answers"
     ],
     "properties": {
      "id": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
       "readOnly": true,
       "description": "ULID. The row's own key."
      },
      "title": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "kind": {
       "type": "string",
       "enum": [
        "choice",
        "yesNo",
        "age",
        "level",
        "certification"
       ],
       "default": "choice",
       "description": "**What the question asks (decided 29 September, W4).** `choice` free answers; `yesNo` two answers (e.g. \"Can everyone swim?\"); `age` answers carrying an age range; `level` answers carrying a level tag; `certification` answers saying whether the guest holds a certificate (e.g. a diving licence). The kind decides which `filter` fields its answers use.\n"
      },
      "sortOrder": {
       "type": "integer",
       "minimum": 0
      },
      "answers": {
       "type": "array",
       "minItems": 2,
       "maxItems": 4,
       "description": "Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11).",
       "items": {
        "type": "object",
        "required": [
         "title",
         "sortOrder"
        ],
        "properties": {
         "id": {
          "type": "string",
          "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
          "readOnly": true,
          "description": "ULID. The row's own key."
         },
         "title": {
          "$ref": "#/components/schemas/LocalisedText"
         },
         "body": {
          "allOf": [
           {
            "$ref": "#/components/schemas/LocalisedText"
           }
          ],
          "description": "The one-liner under the title, at most 140 characters in each language."
         },
         "icon": {
          "type": "string",
          "maxLength": 40,
          "nullable": true,
          "description": "An icon name from the guest app's icon set."
         },
         "badge": {
          "allOf": [
           {
            "$ref": "#/components/schemas/LocalisedText"
           }
          ],
          "nullable": true,
          "description": "Optional, e.g. \"Best value\". At most 24 characters in each language."
         },
         "sortOrder": {
          "type": "integer",
          "minimum": 0
         },
         "target": {
          "allOf": [
           {
            "$ref": "#/components/schemas/GuidedChoiceTarget"
           }
          ],
          "nullable": true,
          "description": "Required with `behaviour` `recommend` on the last question; optional with `filter`, where it is the card shown above the filtered list."
         },
         "filter": {
          "type": "object",
          "nullable": true,
          "description": "**What this answer keeps in the list (decided 29 September, W4).** Every field set must hold; answers to different questions are combined with AND. Required with `behaviour` `filter`. The server applies it (catalogue `guidedAnswerIds`), so web, mobile and kiosk show the same list.\n",
          "properties": {
           "productIds": {
            "type": "array",
            "items": {
             "type": "string",
             "format": "uuid"
            }
           },
           "productCategoryIds": {
            "type": "array",
            "items": {
             "type": "string",
             "format": "uuid"
            }
           },
           "segmentTags": {
            "type": "array",
            "description": "Catalogue `Product.segmentTags`, e.g. a level tag.",
            "items": {
             "type": "string"
            }
           },
           "minAgeYears": {
            "type": "integer",
            "minimum": 0,
            "nullable": true
           },
           "maxAgeYears": {
            "type": "integer",
            "minimum": 0,
            "nullable": true,
            "description": "With `minAgeYears`, checked against each product's age rule (catalogue `ProductEligibilityRule`)."
           },
           "requiresSwimmer": {
            "type": "boolean",
            "nullable": true,
            "description": "False hides products whose eligibility needs a swimmer; true keeps only those."
           },
           "certificationCode": {
            "type": "string",
            "nullable": true,
            "maxLength": 40,
            "description": "Keeps products that need this certificate, or with `holdsCertification` false, hides them."
           },
           "holdsCertification": {
            "type": "boolean",
            "nullable": true
           }
          }
         },
         "consentPrefill": {
          "type": "object",
          "nullable": true,
          "description": "**Pre-fills a REV3-26 consent question from this answer (decided 29 September, W4).** The guest still ticks it at the consent step; nothing is recorded as consent until they do.\n",
          "required": [
           "consentQuestionId",
           "answer"
          ],
          "properties": {
           "consentQuestionId": {
            "type": "string",
            "format": "uuid"
           },
           "answer": {
            "type": "boolean"
           }
          }
         },
         "result": {
          "type": "object",
          "nullable": true,
          "description": "The result card when this answer decides the result. Absent fields fall back to the target's own name, summary and image.",
          "properties": {
           "title": {
            "$ref": "#/components/schemas/LocalisedText"
           },
           "body": {
            "$ref": "#/components/schemas/LocalisedText"
           },
           "imageAssetRef": {
            "type": "string",
            "format": "uuid",
            "nullable": true
           }
          }
         }
        }
       }
      }
     }
    }
   },
   "status": {
    "allOf": [
     {
      "$ref": "#/components/schemas/GuidedChoiceStatus"
     }
    ],
    "readOnly": true
   },
   "source": {
    "type": "string",
    "enum": [
     "manual",
     "aiSuggested"
    ],
    "readOnly": true,
    "description": "`manual` when staff created it; `aiSuggested` when the `ai` service proposed it (a service caller). Kept after a person edits a suggestion, so a report can say how many AI proposals were published."
   },
   "suggestionRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "For `aiSuggested`, the id of the `ai` job that proposed it. Null for `manual`."
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "publishedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The person who published it. Never a service."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "GuidedChoiceStatus": {
  "type": "string",
  "description": "**Draft until a person publishes it (decided 29 September, rev 3 REV3-11).** Guests see only a `published` choice. An AI-proposed choice arrives as `draft` and is never published by the system. Moves as `states/guided-choice.yaml` says: `publishGuidedChoice` and `unpublishGuidedChoice`, and a publish returns the venue's previously published choice to `draft`.\n",
  "enum": [
   "draft",
   "published"
  ],
  "default": "draft"
 },
 "GuidedChoiceTarget": {
  "x-ticvai-persistence": "none — embedded",
  "type": "object",
  "description": "**What an answer opens (decided 29 September, rev 3 REV3-11).** A product (its kind picks the booking flow), a product category (its tickets, as `ticketCategories` shows them), an event, or a module such as `membership`. Each id must belong to the choice's venue and be on sale or enabled when the choice is published, or `publishGuidedChoice` refuses it.\n",
  "required": [
   "kind"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "product",
     "productCategory",
     "event",
     "module",
     "bookingFlow"
    ]
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required when `kind` is `product`. A catalogue `Product`."
   },
   "productCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required when `kind` is `productCategory`. A catalogue `ProductCategory`."
   },
   "eventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required when `kind` is `event`."
   },
   "moduleKey": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ModuleKey"
     }
    ],
    "nullable": true,
    "description": "Required when `kind` is `module`. The module must be enabled."
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required when `kind` is `bookingFlow` (decided 29 September, W12; BUILD-YOUR-EXPERIENCE \"each answer points to one booking flow\"). One of the venue's enabled `BookingFlow`s."
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
 "HomepageSectionKind": {
  "type": "string",
  "description": "**Which module each section needs, proposed, client to correct (decided 28 September, audit R163).** `tickets` needs `ticketsAndBooking`; `whatsOn` needs `events`; `attractions` needs `attractions`; `membership` needs `membership`; `dining` needs `diningAndFnb`; `shop` needs `shop`; `map` needs `map`. `heroBanner`, `quickActions`, `promotions`, `customContent`, `venueOverview` and `spacer` need no module. `venueOverview` (decided 29 September, MOB-3) is the mobile Home's description, opening hours (from `getTenantAppStatus`) and type tiles. `setHomepageLayout` refuses a visible section whose module is not enabled, and `setModuleEnablement` refuses to disable a module a section still needs.\n",
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
   "venueOverview",
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
     "appSection",
     "none"
    ],
    "description": "`appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets."
   },
   "moduleKey": {
    "$ref": "#/components/schemas/ModuleKey"
   },
   "appSection": {
    "type": "string",
    "enum": [
     "home",
     "explore",
     "plan",
     "tickets",
     "map",
     "account",
     "buyTickets"
    ],
    "description": "Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it."
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
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"
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
 "MenuItem": {
  "x-ticvai-persistence": "fnb.menu_item",
  "type": "object",
  "required": [
   "id",
   "productVariantId",
   "name",
   "price",
   "isAvailable"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "productVariantId": {
    "type": "string",
    "format": "uuid",
    "description": "The catalogue variant this item sells. Pricing and tax come from there — a menu is a presentation of the catalogue, not a second catalogue.\n"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "price": {
    "x-ticvai-column": "list_price",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "sortOrder": {
    "type": "integer"
   },
   "modifierGroupIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "stationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "menuSectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."
   },
   "isStockTracked": {
    "type": "boolean",
    "description": "True where a recipe exists. Stock-tracked items cannot be sold offline."
   },
   "isAvailable": {
    "type": "boolean"
   },
   "unavailableReason": {
    "type": "string",
    "nullable": true
   },
   "restoreAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."
   },
   "preparationMinutes": {
    "type": "integer",
    "nullable": true
   },
   "allergens": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AllergenCode"
    }
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
 "OrgUnit": {
  "x-ticvai-persistence": "platform.scope",
  "type": "object",
  "required": [
   "id",
   "level",
   "path",
   "code",
   "name",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "level": {
    "$ref": "#/components/schemas/ScopeLevel"
   },
   "parentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "path": {
    "type": "string",
    "description": "Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.",
    "pattern": "^[a-z0-9_]+(\\.[a-z0-9_]+)*$"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "isActive": {
    "type": "boolean",
    "description": "False causes every permission query at or beneath this node to resolve to DENY.\n"
   },
   "childCount": {
    "type": "integer",
    "minimum": 0
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
 "Product": {
  "x-ticvai-persistence": "catalogue.product",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "kind",
   "venueId",
   "scopePath",
   "isSellable",
   "hasVariants"
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
   "familyKey": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9_-]+$",
    "nullable": true,
    "x-ticvai-unique": "venue",
    "description": "**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ProductKind"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "responsibleDepartmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who owns this product commercially. A scope node at `department` level."
   },
   "onSaleFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"
   },
   "onSaleTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"
   },
   "lifecycleState": {
    "$ref": "#/components/schemas/ProductLifecycleState"
   },
   "isSellable": {
    "type": "boolean",
    "readOnly": true,
    "description": "True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"
   },
   "isStockTracked": {
    "type": "boolean",
    "default": false,
    "description": "**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"
   },
   "hasVariants": {
    "type": "boolean"
   },
   "variantCount": {
    "type": "integer"
   },
   "segmentTags": {
    "type": "array",
    "description": "7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n",
    "items": {
     "type": "string"
    }
   },
   "codeSchema": {
    "type": "string",
    "readOnly": true,
    "description": "7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    }
   },
   "entitlementTemplateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"
   },
   "blockedOffline": {
    "type": "boolean",
    "description": "True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true,
    "description": "Custom fields. JSONB-backed, defined by the venue's data mask."
   },
   "guestListing": {
    "$ref": "#/components/schemas/GuestListing"
   },
   "notBookableLabel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"
   },
   "salesContact": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductSalesContact"
     }
    ],
    "nullable": true,
    "description": "**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"
   },
   "displayTags": {
    "type": "array",
    "maxItems": 6,
    "items": {
     "$ref": "#/components/schemas/ProductDisplayTag"
    },
    "description": "**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"
   },
   "media": {
    "type": "array",
    "maxItems": 20,
    "items": {
     "$ref": "#/components/schemas/ProductMedia"
    },
    "description": "**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"
   },
   "consentQuestionIds": {
    "type": "array",
    "maxItems": 10,
    "uniqueItems": true,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"
   },
   "requiresTimeWindow": {
    "type": "boolean",
    "default": false,
    "description": "**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"
   },
   "productOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."
   },
   "operationalContact": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "A principal id or a name, as the context screen takes it."
   },
   "businessUnitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `ledger.legal_entity`, read through finance."
   },
   "attractionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "siteId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "locationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The brand, as the context screen names it (a catalogue brand category)."
   },
   "marketCode": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "salesTerritory": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   }
  }
 },
 "ProductCategory": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.product_category",
  "description": "Retail Board 2 of the client's design set, 20 August. **`listSeatCategories` existed and a product category did not** — a seat category prices a seat, and a merchandise hierarchy groups a catalogue.\n**Brand sits here rather than as its own entity.** A venue with four brands and a hierarchy five levels deep can express that with a parent; a venue with one brand should not have to maintain a table containing one row.\n**`displayOrder` is not alphabetical and that is the point.** A retail category list runs in the order the merchandiser wants a guest to see it, and sorting by name puts *Accessories* above *Apparel* forever.\n",
  "required": [
   "id",
   "name",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "code": {
    "type": "string",
    "maxLength": 64,
    "nullable": true,
    "x-ticvai-unique": "tenant",
    "description": "**Taken from their category tables, 20 September.** Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a display string that a venue is free to translate.\n**Unique per tenant where set** (decided 28 September, audit R108): two categories in one tenant never share a code, and `setProductCategories` refuses a body that would, with `409 duplicate-code`.\n"
   },
   "nameLocalised": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "kind": {
    "type": "string",
    "enum": [
     "category",
     "brand",
     "collection",
     "season",
     "department"
    ]
   },
   "parentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**One tree, not four.** A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each level cannot express a venue that nests them differently.\n"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "Set by the server from the venue the caller acts at; not sent."
   },
   "displayOrder": {
    "type": "integer",
    "default": 100
   },
   "imageAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "description": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September, rev 3 REV3-19). Each language value at most 200 characters.\n"
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The booking flow for every product filed here** that names none of its own (decided 29 September, W12, BO-115). Null means the venue's flow for each product's `kind`. A white-label `BookingFlow` of the venue; `setProductCategories` refuses any other id with `422`.\n"
   },
   "isActive": {
    "type": "boolean",
    "default": true,
    "description": "**Deactivated rather than deleted.** A category with a season behind it still names the products sold under it, and removing it rewrites last year's report.\n"
   }
  }
 },
 "ProductCategoryNode": {
  "x-ticvai-persistence": "none — projection over catalogue.product_category",
  "description": "**One node of the tree `listProductCategories` returns.** A `ProductCategory` with its children nested under it, in `displayOrder`, so no caller reassembles the hierarchy from `parentId`. `setProductCategories` still takes the flat list, because a write names each parent by id.\n",
  "allOf": [
   {
    "$ref": "#/components/schemas/ProductCategory"
   },
   {
    "type": "object",
    "required": [
     "children"
    ],
    "properties": {
     "children": {
      "type": "array",
      "description": "Empty on a leaf.",
      "items": {
       "$ref": "#/components/schemas/ProductCategoryNode"
      }
     }
    }
   }
  ]
 },
 "ProductDisplayTag": {
  "x-ticvai-persistence": "none — jsonb column on catalogue.product",
  "type": "object",
  "required": [
   "kind",
   "label"
  ],
  "description": "One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.",
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "clock",
     "height",
     "free",
     "calendar",
     "id"
    ],
    "description": "`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."
   },
   "label": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."
   },
   "derived": {
    "type": "boolean",
    "readOnly": true,
    "default": false,
    "description": "True on a tag the server derived on read because the venue set none. Never sent."
   }
  }
 },
 "ProductKind": {
  "type": "string",
  "description": "**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n",
  "enum": [
   "admission",
   "timedAdmission",
   "datedAdmission",
   "openDated",
   "seated",
   "membership",
   "bundle",
   "fnb",
   "retail",
   "rental",
   "addOn",
   "giftCard"
  ]
 },
 "ProductLifecycleState": {
  "type": "string",
  "enum": [
   "draft",
   "inReview",
   "approved",
   "live",
   "withdrawn",
   "archived"
  ]
 },
 "ProductMedia": {
  "x-ticvai-persistence": "catalogue.product_media",
  "type": "object",
  "required": [
   "assetId",
   "kind",
   "isPrimary"
  ],
  "description": "One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n",
  "properties": {
   "assetId": {
    "type": "string",
    "format": "uuid",
    "description": "A `MediaAsset` of `assets.yaml`, in status `ready`."
   },
   "kind": {
    "type": "string",
    "enum": [
     "image",
     "video"
    ]
   },
   "isPrimary": {
    "type": "boolean",
    "default": false,
    "description": "The item *Read more* opens on and a listing shows. Exactly one per product."
   },
   "displayOrder": {
    "type": "integer",
    "default": 100
   },
   "altText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   }
  }
 },
 "ProductSalesContact": {
  "x-ticvai-persistence": "none — jsonb column on catalogue.product",
  "type": "object",
  "description": "Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n",
  "minProperties": 1,
  "properties": {
   "phone": {
    "type": "string",
    "maxLength": 32,
    "nullable": true
   },
   "email": {
    "type": "string",
    "format": "email",
    "maxLength": 254,
    "nullable": true
   },
   "note": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."
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
 "ProposedAction": {
  "type": "object",
  "x-ticvai-persistence": "ai.proposed_action",
  "required": [
   "id",
   "kind",
   "targetContract",
   "targetOperation",
   "payload",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "interactionId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "pricing",
     "promotion",
     "operational",
     "financial",
     "configuration",
     "content",
     "audience"
    ],
    "description": "`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."
   },
   "targetContract": {
    "type": "string",
    "description": "Which contract would perform it. The assistant never performs it itself."
   },
   "targetOperation": {
    "type": "string"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true,
    "description": "The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"
   },
   "summary": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "description": "**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n",
    "enum": [
     "proposed",
     "approved",
     "rejected",
     "applied",
     "expired"
    ]
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."
   },
   "approvalLevel": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2,
    "description": "8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decisionReason": {
    "type": "string",
    "nullable": true,
    "description": "Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"
   },
   "proposedAt": {
    "type": "string",
    "format": "date-time"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.action_plan",
    "description": "The plan this action presents for a decision (AI design 2.2 D, 3.8)."
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."
   },
   "changeSetHash": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."
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
 "ScopeLevel": {
  "type": "string",
  "description": "**The eight organisational levels, plus `subject`.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition of the eight levels and this mirrors them so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n\n**`subject` is the one value tenancy does not have, and it is not a level.** It is here because `check-package` reads this enum as the closed vocabulary for `x-ticvai-scope-level`, and some operations act on one guest's own resources, which sit in no node of the venue hierarchy. So `subject` is valid as an operation's scope level and never as a `ScopeRef.level`: every `ScopeRef` is a row of `platform.scope`, and those carry one of the eight.\n",
  "enum": [
   "tenant",
   "brand",
   "region",
   "venue",
   "department",
   "subDepartment",
   "workstation",
   "outlet",
   "subject"
  ]
 },
 "SiteSetupProgress": {
  "x-ticvai-persistence": "whitelabel.site_setup_progress",
  "type": "object",
  "description": "**The Site Builder's saved progress, one row per tenant (decided 29 September, W12 and M24-05).** Not configuration and not published. `presetKey` is the starting point the operator picked; the builder pre-fills each step from it, which is what keeps the minimum path to a working site at about 30 minutes.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "presetKey": {
    "type": "string",
    "nullable": true,
    "enum": [
     "themePark",
     "waterPark",
     "museum",
     "theatreAndArena",
     "singleAttraction",
     "playCentre",
     "multiVenue",
     null
    ],
    "description": "The starting point. Each preset proposes the modules, the booking flow types (with their default step order), the homepage sections, the mobile tabs and a booking-flow `preset`; nothing is written until the operator accepts a step."
   },
   "currentStep": {
    "allOf": [
     {
      "$ref": "#/components/schemas/SiteSetupStepKey"
     }
    ],
    "nullable": true
   },
   "steps": {
    "type": "object",
    "description": "One entry per `SiteSetupStepKey`.",
    "additionalProperties": {
     "type": "object",
     "required": [
      "status"
     ],
     "properties": {
      "status": {
       "type": "string",
       "enum": [
        "notStarted",
        "inProgress",
        "done",
        "skipped"
       ]
      },
      "completedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "completedByPrincipalId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "minimumPathDone": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "True once the minimum path is done: a logo, the four theme colours, at least one enabled valid booking flow and a published version. Everything else keeps its preset or schema default."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The partition key (ADR-0005). Written at `tenant` scope."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "SiteSetupStepKey": {
  "type": "string",
  "description": "The seven Site Builder steps, in order (decided 29 September, W12): venue and modules (CMS-001), ticketing flows (CMS-103), compose steps (CMS-103), Help me choose (CMS-101), look and feel (CMS-007, CMS-009, CMS-002, CMS-004, CMS-008, CMS-005, CMS-003), mobile app (CMS-009, CMS-004, CMS-007), preview and publish (CMS-006, CMS-012, CMS-014).\n",
  "enum": [
   "venueAndModules",
   "ticketingFlows",
   "composeSteps",
   "helpMeChoose",
   "lookAndFeel",
   "mobileApp",
   "previewAndPublish"
  ]
 },
 "StoreAccount": {
  "x-ticvai-persistence": "whitelabel.store_account",
  "type": "object",
  "description": "**One of the client's own store accounts (decided 24 September, M24-08).** TICVAI never publishes under its own developer account.\n",
  "required": [
   "store",
   "accountHolderName",
   "developerAccountId",
   "appIdentifier"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "store": {
    "type": "string",
    "enum": [
     "appleAppStore",
     "googlePlay"
    ]
   },
   "accountHolderName": {
    "type": "string",
    "maxLength": 200,
    "description": "The client's legal entity as the store knows it."
   },
   "dunsNumber": {
    "type": "string",
    "nullable": true,
    "pattern": "^[0-9]{9}$",
    "description": "Required for `appleAppStore`; Apple enrols an organisation only with its D-U-N-S number."
   },
   "developerAccountId": {
    "type": "string",
    "maxLength": 64,
    "description": "Apple Team ID, or the Google Play developer account id."
   },
   "appIdentifier": {
    "type": "string",
    "maxLength": 155,
    "pattern": "^[A-Za-z][A-Za-z0-9_]*(\\.[A-Za-z0-9_]+)+$",
    "description": "The bundle id (Apple) or application id (Google) the app is signed with."
   },
   "apiCredentialSecretRef": {
    "type": "string",
    "nullable": true,
    "writeOnly": true,
    "description": "App Store Connect API key or Play service-account key, sent once and kept in the secret store; this is its reference. Needed only for `submitToStore`."
   },
   "hasApiCredential": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onRead"
   },
   "listing": {
    "type": "object",
    "description": "The store listing.",
    "properties": {
     "appName": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "subtitle": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "description": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "keywords": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "category": {
      "type": "string"
     },
     "supportUrl": {
      "type": "string",
      "format": "uri"
     },
     "privacyPolicyUrl": {
      "type": "string",
      "format": "uri"
     },
     "screenshotAssetRefs": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The partition key (ADR-0005). Written at `tenant` scope."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "StorePublishingChecklist": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "accounts",
   "items"
  ],
  "properties": {
   "accounts": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/StoreAccount"
    }
   },
   "items": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "item",
      "done"
     ],
     "properties": {
      "item": {
       "type": "string",
       "enum": [
        "appleDunsNumber",
        "appleDeveloperAccount",
        "googlePlayDeveloperAccount",
        "storeListing",
        "appIcons",
        "publishedConfiguration"
       ]
      },
      "done": {
       "type": "boolean"
      },
      "clientOwned": {
       "type": "boolean",
       "description": "True for the three accounts, which only the client can open."
      },
      "guidance": {
       "type": "string",
       "description": "What to do next, in the operator's language."
      }
     }
    }
   }
  }
 },
 "StorefrontAnalyticsProvider": {
  "type": "object",
  "x-ticvai-persistence": "whitelabel.analytics_provider",
  "description": "**One analytics platform the storefront or app reports to** (22.10.29, 29 September build). Venue configuration: a null `venueId` is the tenant-wide default a venue's own row replaces.",
  "required": [
   "provider",
   "measurementId",
   "surfaces",
   "consentCategory",
   "isEnabled"
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
    "nullable": true
   },
   "provider": {
    "type": "string",
    "enum": [
     "googleAnalytics4",
     "googleTagManager",
     "adobeAnalytics",
     "metaPixel",
     "matomo",
     "other"
    ]
   },
   "providerLabel": {
    "type": "string",
    "maxLength": 100,
    "nullable": true,
    "description": "The name, when `provider` is `other`."
   },
   "measurementId": {
    "type": "string",
    "maxLength": 100,
    "description": "What the tag or SDK reports to (GA4 `G-...`, Tag Manager `GTM-...`, a pixel id)."
   },
   "surfaces": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string",
     "enum": [
      "guestWeb",
      "guestApp"
     ]
    }
   },
   "consentCategory": {
    "type": "string",
    "enum": [
     "functional",
     "analytics",
     "personalisation",
     "marketing"
    ],
    "default": "analytics",
    "description": "The cookie category the visitor must grant before this provider loads (marketing-crm `CookieCategory`)."
   },
   "isEnabled": {
    "type": "boolean",
    "default": true
   },
   "reportingPropertyId": {
    "type": "string",
    "maxLength": 100,
    "nullable": true,
    "description": "The property `getStorefrontInsights` asks the reporting API about (a GA4 property id). Staff only."
   },
   "reportingCredentialRef": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "writeOnly": true,
    "description": "The vault reference of the reporting credential. Accepted, never returned."
   },
   "hasReportingCredential": {
    "type": "boolean",
    "readOnly": true,
    "description": "Whether a reporting credential is held, since the reference itself is never returned."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
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
 "UpdateProductRequest": {
  "type": "object",
  "minProperties": 1,
  "properties": {
   "familyKey": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9_-]+$",
    "nullable": true,
    "x-ticvai-unique": "venue",
    "description": "The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. At most one product per venue in a family, else `409 duplicate-code`."
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    }
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true
   },
   "guestListing": {
    "$ref": "#/components/schemas/GuestListing"
   },
   "notBookableLabel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   },
   "salesContact": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductSalesContact"
     }
    ],
    "nullable": true,
    "description": "See `Product.salesContact` (W3, 29 September)."
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "See `Product.bookingFlowId` (W8, W12, 29 September)."
   },
   "displayTags": {
    "type": "array",
    "maxItems": 6,
    "items": {
     "$ref": "#/components/schemas/ProductDisplayTag"
    }
   },
   "media": {
    "type": "array",
    "maxItems": 20,
    "items": {
     "$ref": "#/components/schemas/ProductMedia"
    }
   },
   "consentQuestionIds": {
    "type": "array",
    "maxItems": 10,
    "uniqueItems": true,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requiresTimeWindow": {
    "type": "boolean"
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
