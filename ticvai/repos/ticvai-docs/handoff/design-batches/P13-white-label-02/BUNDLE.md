# P13-white-label-02 — P13 · White Label (2 of 3)

**10 screens · 40 operations · 64 schemas · 10 permissions**

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

- **Every control that can be refused must be gated.** 10 permissions apply here:
  `AI_USE, GUEST_MANAGE, GUEST_VIEW, MARKETING_MANAGE, PRODUCT_VIEW, ROLE_MANAGE, SCOPE_VIEW, TENANT_CONFIGURE, TENANT_PUBLISH, USER_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `CMS-013` | SEO & Metadata | configEditor | 1 | 0 | — |
| `CMS-011` | Translations | configEditor | 1 | 0 | — |
| `CMS-012` | RTL Preview | statusTracker | 2 | 0 | — |
| `CMS-014` | Publishing Workflow | statusTracker | 4 | 1 | — |
| `CMS-015` | Version History | listDetail | 3 | 1 | — |
| `CMS-016` | Site Settings | statusTracker | 6 | 1 | — |
| `CMS-017` | Domain & Certificate | listDetail | 4 | 1 | — |
| `CMS-018` | Consent & Legal | listDetail | 8 | 4 | — |
| `CMS-019` | User Access | listDetail | 2 | 0 | — |
| `CMS-101` | Help Me Choose | listDetail | 12 | 3 | — |

## Thin screens in this batch

**CMS-011, CMS-012 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "CMS-013",
  "name": "SEO & Metadata",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/seo-metadata",
   "component": "apps/venue-management-web/src/routes/white-label/SeoMetadataDetail.tsx",
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
    "CMS-016"
   ],
   "notes": "**Reached from CMS-016** — metadata is a site setting. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-013 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-013 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-013 holds none of them, so the edge carries nothing and CMS-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`setSeoMetadata`) and no read of a population — it is settings, not a list",
  "purpose": "Control how a page looks everywhere it is not the page.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "SeoMetadata.id",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      },
      {
       "kind": "textField",
       "label": "entityKind",
       "bindsTo": "SeoMetadata.entityKind",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      },
      {
       "kind": "textField",
       "label": "entityId",
       "bindsTo": "SeoMetadata.entityId",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      },
      {
       "kind": "textField",
       "label": "locale",
       "bindsTo": "SeoMetadata.locale",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      },
      {
       "kind": "textField",
       "label": "title",
       "bindsTo": "SeoMetadata.title",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      },
      {
       "kind": "textField",
       "label": "metaDescription",
       "bindsTo": "SeoMetadata.metaDescription",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      },
      {
       "kind": "textField",
       "label": "keywords",
       "bindsTo": "SeoMetadata.keywords",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      },
      {
       "kind": "textField",
       "label": "canonicalUrl",
       "bindsTo": "SeoMetadata.canonicalUrl",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      },
      {
       "kind": "textField",
       "label": "slug",
       "bindsTo": "SeoMetadata.slug",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      },
      {
       "kind": "textField",
       "label": "hreflang",
       "bindsTo": "SeoMetadata.hreflang",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      },
      {
       "kind": "textField",
       "label": "schemaOrgType",
       "bindsTo": "SeoMetadata.schemaOrgType",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      },
      {
       "kind": "textField",
       "label": "openGraph",
       "bindsTo": "SeoMetadata.openGraph",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      },
      {
       "kind": "textField",
       "label": "isAutoGenerated",
       "bindsTo": "SeoMetadata.isAutoGenerated",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      },
      {
       "kind": "textField",
       "label": "noIndex",
       "bindsTo": "SeoMetadata.noIndex",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      },
      {
       "kind": "textField",
       "label": "scopePath",
       "bindsTo": "SeoMetadata.scopePath",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save SEO metadata",
       "operation": "setSeoMetadata",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Detail loads",
   "error": "Could not load",
   "emptyFirstRun": "Not found — it may have been deleted or moved out of scope",
   "emptyNoAccess": "Shown when the caller lacks `MARKETING_MANAGE`, which `setSeoMetadata` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeoMetadata",
    "contract": "marketing-crm",
    "purpose": "Title, description and share image",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-013"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "CMS-011",
  "name": "Translations",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/translations",
   "component": "apps/venue-management-web/src/routes/white-label/TranslationsDetail.tsx",
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
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-011 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-011 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-011 holds none of them, so the edge carries nothing and CMS-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`setLanguages`) and no read of a population — it is settings, not a list",
  "purpose": "Fill in what every language is missing.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save languages",
       "operation": "setLanguages",
       "provenance": "contract white-label.yaml PUT /tenant-config/languages"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Languages",
       "operation": "setLanguages",
       "notes": "Required.",
       "provenance": "contract white-label.yaml PUT /tenant-config/languages"
      },
      {
       "kind": "textField",
       "label": "Default language",
       "operation": "setLanguages",
       "notes": "Required.",
       "provenance": "contract white-label.yaml PUT /tenant-config/languages"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved translations.",
   "error": "Could not load. Names which read failed and leaves the translations untouched.",
   "emptyFirstRun": "No translations configured. The form opens empty and `setLanguages` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `setLanguages` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setLanguages",
    "contract": "white-label",
    "purpose": "Set enabled languages and default",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-011"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "CMS-017",
  "name": "Domain & Certificate",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/domain-certificate",
   "component": "apps/venue-management-web/src/routes/white-label/DomainCertificateDetail.tsx",
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
    "CMS-016"
   ],
   "notes": "**Reached from CMS-016** — a domain is a site setting. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-017 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-017 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-017 holds none of them, so the edge carries nothing and CMS-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCustomDomains` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Point the tenant’s own domain at their site.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
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
   "loading": "Detail loads",
   "error": "Could not load",
   "emptyFirstRun": "Not found — it may have been deleted or moved out of scope",
   "emptyNoResults": "Never shown: `listCustomDomains` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listCustomDomains` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCustomDomains",
    "contract": "white-label",
    "purpose": "Domains claimed, and their state",
    "trigger": "onLoad"
   },
   {
    "operationId": "claimCustomDomain",
    "contract": "white-label",
    "purpose": "Claim a domain",
    "trigger": "onAction",
    "invalidates": [
     "listCustomDomains"
    ]
   },
   {
    "operationId": "verifyCustomDomain",
    "contract": "white-label",
    "purpose": "Prove control before it serves traffic",
    "trigger": "onAction",
    "invalidates": [
     "listCustomDomains"
    ]
   },
   {
    "operationId": "relinquishCustomDomain",
    "contract": "white-label",
    "purpose": "Release a domain",
    "trigger": "onAction",
    "invalidates": [
     "listCustomDomains"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "domainId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Verification and release act on one domain**, taken from the row. A release issued against a domain nobody can see is a site going dark with no record of who asked.",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-017"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
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
  "id": "CMS-018",
  "name": "Consent & Legal",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/consent-legal",
   "component": "apps/venue-management-web/src/routes/white-label/ConsentLegalDetail.tsx",
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
    "CMS-016"
   ],
   "notes": "**Reached from CMS-016** — consent and legal are site settings. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-018 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-018 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "carries": [
      "policyKind",
      "version"
     ],
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-018 holds policyKind, version, so an edge into it carries them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.\n\n**Rewired 23 September (L7).** The screen called the maintenance equipment register, guest CRM or subscription billing where its purpose names White Labelling. Its operations now match its purpose.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPolicies` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Manage the notices every consent is captured against, and the booking consent questions a venue asks (\"Are you able to swim?\", \"I accept the risk\"), with the record of every answer (decided 29 September, rev 3 REV3-26).",
  "states": {
   "loading": "The consent legal list.",
   "error": "Could not load. Names which read failed and leaves the consent legal untouched.",
   "emptyFirstRun": "No consent legal yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "`listPolicies` takes no filter. The consent questions (kind, status) and the consent records (order, guest, question) do: an empty result names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listPolicies` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPolicies",
    "contract": "white-label",
    "purpose": "Privacy, terms and cookie notices",
    "trigger": "onLoad"
   },
   {
    "operationId": "setPolicy",
    "contract": "white-label",
    "purpose": "Edit and publish a notice",
    "trigger": "onAction",
    "invalidates": [
     "listPolicies"
    ]
   },
   {
    "operationId": "listConsentPurposes",
    "contract": "marketing-crm",
    "purpose": "What guests can consent to",
    "trigger": "onLoad"
   },
   {
    "operationId": "setConsentPurposes",
    "contract": "marketing-crm",
    "purpose": "Set the consent purposes",
    "trigger": "onAction",
    "invalidates": [
     "listPolicies"
    ]
   },
   {
    "operationId": "listConsentQuestions",
    "contract": "marketing-crm",
    "purpose": "The venue's booking consent questions (rev 3 REV3-26)",
    "trigger": "onLoad"
   },
   {
    "operationId": "createConsentQuestion",
    "contract": "marketing-crm",
    "purpose": "Define a consent question, created at version 1",
    "trigger": "onAction",
    "invalidates": [
     "listConsentQuestions"
    ]
   },
   {
    "operationId": "updateConsentQuestion",
    "contract": "marketing-crm",
    "purpose": "Change a question (a new version) or retire it",
    "trigger": "onAction",
    "invalidates": [
     "listConsentQuestions"
    ]
   },
   {
    "operationId": "listConsentAnswers",
    "contract": "marketing-crm",
    "purpose": "The consent records, filtered by order, guest or question",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-018"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
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
      },
      {
       "kind": "dataTable",
       "label": "Every consent purpose config",
       "bindsTo": "ConsentPurposeConfig",
       "columns": [
        "ConsentPurposeConfig.purpose",
        "ConsentPurposeConfig.displayName",
        "ConsentPurposeConfig.description",
        "ConsentPurposeConfig.channels",
        "ConsentPurposeConfig.noticeVersion",
        "ConsentPurposeConfig.isRequiredForService",
        "ConsentPurposeConfig.expiresAfterMonths"
       ],
       "operation": "listConsentPurposes",
       "provenance": "contract marketing-crm.yaml GET /consent-purposes"
      },
      {
       "kind": "dataTable",
       "label": "Every booking consent question",
       "bindsTo": "ConsentQuestion",
       "columns": [
        "ConsentQuestion.kind",
        "ConsentQuestion.text",
        "ConsentQuestion.version",
        "ConsentQuestion.scope",
        "ConsentQuestion.required",
        "ConsentQuestion.blockingAnswer",
        "ConsentQuestion.status",
        "ConsentQuestion.updatedAt"
       ],
       "operation": "listConsentQuestions",
       "notes": "**A consent, not a data field** (decided 29 September, rev 3 REV3-26). Each question has its own text per locale, a version, and whether it is asked for each person or once per booking. Filter by `kind` and `status`. **Attaching** is done where the question is used: to a booking flow on CMS-016 (`BookingFlowConfig.consentQuestionIds`, per venue), to a product on BO-008 (`Product.consentQuestionIds`).",
       "provenance": "contract marketing-crm.yaml GET /consent-questions"
      },
      {
       "kind": "dataTable",
       "label": "Consent records",
       "bindsTo": "BookingConsentRecord",
       "columns": [
        "BookingConsentRecord.answeredAt",
        "BookingConsentRecord.questionId",
        "BookingConsentRecord.questionVersion",
        "BookingConsentRecord.answer",
        "BookingConsentRecord.scope",
        "BookingConsentRecord.personName",
        "BookingConsentRecord.orderId",
        "BookingConsentRecord.answeredBySubjectId",
        "BookingConsentRecord.answeredByPrincipalId",
        "BookingConsentRecord.source",
        "BookingConsentRecord.blocksBooking",
        "BookingConsentRecord.supersededAt"
       ],
       "operation": "listConsentAnswers",
       "notes": "**What was asked, at which version, what was answered, for whom, by whom and when** (rev 3 REV3-26). Filter by order, guest or question. Read-only: an answer is never edited here, and a superseded answer stays listed with `supersededAt`.",
       "provenance": "contract marketing-crm.yaml GET /consent-answers"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected policy",
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
      },
      {
       "kind": "detailPanel",
       "label": "The selected consent question",
       "bindsTo": "ConsentQuestion",
       "columns": [
        "ConsentQuestion.kind",
        "ConsentQuestion.text",
        "ConsentQuestion.helpText",
        "ConsentQuestion.version",
        "ConsentQuestion.scope",
        "ConsentQuestion.required",
        "ConsentQuestion.blockingAnswer",
        "ConsentQuestion.status"
       ],
       "operation": "listConsentQuestions",
       "provenance": "contract marketing-crm.yaml GET /consent-questions"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save policy",
       "operation": "setPolicy",
       "provenance": "contract white-label.yaml PUT /tenant-config/policies/{policyKind}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save consent purposes",
       "operation": "setConsentPurposes",
       "provenance": "contract marketing-crm.yaml PUT /consent-purposes"
      },
      {
       "kind": "secondaryButton",
       "label": "New consent question",
       "operation": "createConsentQuestion",
       "provenance": "contract marketing-crm.yaml POST /consent-questions"
      },
      {
       "kind": "secondaryButton",
       "label": "Save as new version",
       "operation": "updateConsentQuestion",
       "notes": "**A change to what the guest is asked is a new version, never an edit** (rev 3 REV3-26): changing the text, scope, required or blocking answer raises `version` by one, and every answer already given keeps the version it was given against.",
       "provenance": "contract marketing-crm.yaml PATCH /consent-questions/{questionId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Retire question",
       "operation": "updateConsentQuestion",
       "notes": "Sets `status` to `retired`. It stops being asked on every flow and product it is attached to and changes no version; the answers already given stay on record.",
       "provenance": "contract marketing-crm.yaml PATCH /consent-questions/{questionId}"
      }
     ]
    }
   ]
  },
  "entryState": {
   "params": [
    {
     "name": "policyKind",
     "from": "navigation"
    },
    {
     "name": "questionId",
     "from": "navigation"
    }
   ],
   "preloaded": [
    "Policy.kind",
    "Policy.title",
    "Policy.body",
    "Policy.requiresReconsent",
    "Policy.effectiveFrom"
   ]
  },
  "overlays": [
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
   },
   {
    "id": "formSetConsentPurposes",
    "component": "modal",
    "trigger": "Save consent purposes",
    "body": "**Collects what `setConsentPurposes` sends before it is called.** Required: `purposes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save consent purposes",
     "operation": "setConsentPurposes"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "purposes"
     ]
    },
    "provenance": "contract marketing-crm.yaml PUT /consent-purposes"
   },
   {
    "id": "formCreateConsentQuestion",
    "component": "modal",
    "trigger": "New consent question",
    "body": "**Collects what `createConsentQuestion` sends before it is called.** Required: `kind`, `text` (every tenant language). Optional: `helpText`, `scope` (`perPerson`, the default, or `perBooking`), `required` (default true: checkout waits for it) and `blockingAnswer` (`yes`, `no` or `none`, the default: the answer that stops the booking for the person or booking it covers). Created at version 1 (rev 3 REV3-26). Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ConsentQuestion",
    "confirm": {
     "label": "Create question",
     "operation": "createConsentQuestion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "text",
      "helpText",
      "scope",
      "required",
      "blockingAnswer"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /consent-questions"
   },
   {
    "id": "formUpdateConsentQuestion",
    "component": "modal",
    "trigger": "Save as new version",
    "body": "**Says, before saving, that the guest will be asked version N+1 from the next cart read** and that answers already given keep their version (rev 3 REV3-26). Optional: `text`, `helpText`, `scope`, `required`, `blockingAnswer`, `status`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ConsentQuestion",
    "confirm": {
     "label": "Save new version",
     "operation": "updateConsentQuestion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "text",
      "helpText",
      "scope",
      "required",
      "blockingAnswer",
      "status"
     ]
    },
    "provenance": "contract marketing-crm.yaml PATCH /consent-questions/{questionId}"
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
  "id": "CMS-019",
  "name": "User Access",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/user-access",
   "component": "apps/venue-management-web/src/routes/white-label/UserAccessDetail.tsx",
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
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-019 holds none of them, so the edge carries nothing and CMS-001 opens cold"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "provenance": "derived — CMS-002 declares entryState.params uploadId and CMS-019 holds none of them, so the edge carries nothing and CMS-002 opens cold"
    },
    {
     "to": "CMS-003",
     "trigger": "Typography",
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version and CMS-019 holds none of them, so the edge carries nothing and CMS-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPrincipals` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Say who in the tenant may change what.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Scope path",
       "operation": "listPrincipals",
       "notes": "Sends `?scopePath=` to `listPrincipals`.",
       "provenance": "contract identity.yaml GET /principals"
      },
      {
       "kind": "toggle",
       "label": "Is active",
       "operation": "listPrincipals",
       "notes": "Sends `?isActive=` to `listPrincipals`.",
       "provenance": "contract identity.yaml GET /principals"
      },
      {
       "kind": "dataTable",
       "label": "Every principal",
       "bindsTo": "Principal",
       "columns": [
        "Principal.id",
        "Principal.username",
        "Principal.displayName",
        "Principal.isActive",
        "Principal.validFrom",
        "Principal.validTo",
        "Principal.primaryRoleId",
        "Principal.roles",
        "Principal.lastLoginAt"
       ],
       "operation": "listPrincipals",
       "provenance": "contract identity.yaml GET /principals"
      },
      {
       "kind": "dataTable",
       "label": "Every role",
       "bindsTo": "Role",
       "columns": [
        "Role.id",
        "Role.code",
        "Role.name",
        "Role.description",
        "Role.permissions",
        "Role.inheritsFromRoleId",
        "Role.isSystem",
        "Role.principalCount",
        "Role.grantCount"
       ],
       "operation": "listRoles",
       "provenance": "contract identity.yaml GET /roles"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected principal",
       "bindsTo": "Principal",
       "columns": [
        "Principal.id",
        "Principal.username",
        "Principal.displayName",
        "Principal.isActive",
        "Principal.validFrom",
        "Principal.validTo",
        "Principal.primaryRoleId",
        "Principal.roles",
        "Principal.lastLoginAt"
       ],
       "operation": "listPrincipals",
       "provenance": "contract identity.yaml GET /principals"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The user access list.",
   "error": "Could not load. Names which read failed and leaves the user access untouched.",
   "emptyFirstRun": "No user access yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on scopePath, isActive and the user access are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPrincipals",
    "contract": "identity",
    "purpose": "List principals",
    "trigger": "onLoad"
   },
   {
    "operationId": "listRoles",
    "contract": "identity",
    "purpose": "List roles",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Principal.id",
    "Principal.username",
    "Principal.displayName",
    "Principal.isActive",
    "Principal.validFrom"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-019"
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
 "createConsentQuestion": {
  "method": "POST",
  "path": "/consent-questions",
  "contract": "marketing-crm",
  "summary": "Define a consent question",
  "permission": "GUEST_MANAGE",
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
  "requestBody": "ConsentQuestion",
  "responds": "ConsentQuestion"
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
 "listConsentAnswers": {
  "method": "GET",
  "path": "/consent-answers",
  "contract": "marketing-crm",
  "summary": "The consent records given at booking",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "orderId",
    "in": "query",
    "required": null
   },
   {
    "name": "subjectId",
    "in": "query",
    "required": null
   },
   {
    "name": "questionId",
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
 "listConsentPurposes": {
  "method": "GET",
  "path": "/consent-purposes",
  "contract": "marketing-crm",
  "summary": "Configured consent purposes",
  "permission": "GUEST_VIEW",
  "offlineCapable": true,
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
 "listPrincipals": {
  "method": "GET",
  "path": "/principals",
  "contract": "identity",
  "summary": "List principals",
  "permission": "USER_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "isActive",
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
 "listRoles": {
  "method": "GET",
  "path": "/roles",
  "contract": "identity",
  "summary": "List roles",
  "permission": "ROLE_MANAGE",
  "offlineCapable": true,
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
 "setConsentPurposes": {
  "method": "PUT",
  "path": "/consent-purposes",
  "contract": "marketing-crm",
  "summary": "Configure consent purposes",
  "permission": "GUEST_MANAGE",
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
  "responds": "ConsentPurposeConfig"
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
 "setSeoMetadata": {
  "method": "PUT",
  "path": "/seo-metadata",
  "contract": "marketing-crm",
  "summary": "Titles, descriptions, canonicals and hreflang",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "SeoMetadata",
  "responds": "SeoMetadata"
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
 "updateConsentQuestion": {
  "method": "PATCH",
  "path": "/consent-questions/{questionId}",
  "contract": "marketing-crm",
  "summary": "Reword, re-scope or retire a consent question",
  "permission": "GUEST_MANAGE",
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
  "requestBody": "ConsentQuestion",
  "responds": "ConsentQuestion"
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
 "BookingConsentRecord": {
  "type": "object",
  "x-ticvai-persistence": "marketing.booking_consent_record",
  "description": "**One answer to one consent question, as given** (decided 29 September, rev 3 REV3-26). Append-only: a changed answer is a new record and this one gets `supersededAt`. Distinct from `ConsentRecord`, which is a guest's standing decision about a data-processing purpose; this is an answer given for a booking.\n",
  "required": [
   "id",
   "questionId",
   "questionVersion",
   "questionKind",
   "answer",
   "scope",
   "source",
   "answeredAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "questionId": {
    "type": "string",
    "format": "uuid"
   },
   "questionVersion": {
    "type": "integer",
    "minimum": 1
   },
   "questionKind": {
    "$ref": "#/components/schemas/ConsentQuestionKind"
   },
   "answer": {
    "type": "string",
    "enum": [
     "yes",
     "no"
    ]
   },
   "scope": {
    "type": "string",
    "enum": [
     "perPerson",
     "perBooking"
    ]
   },
   "blocksBooking": {
    "type": "boolean",
    "readOnly": true,
    "description": "The answer is the question's `blockingAnswer` at that version."
   },
   "cartId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "cartLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "Set by `orders.checkoutCart` when the cart becomes an order."
   },
   "orderLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "personIndex": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "personName": {
    "type": "string",
    "maxLength": 120,
    "nullable": true
   },
   "personSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "answeredBySubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The guest who answered, from the session. Null for an anonymous cart."
   },
   "answeredByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The staff member who answered on the guest's behalf."
   },
   "source": {
    "$ref": "#/components/schemas/ConsentSource"
   },
   "answeredAt": {
    "type": "string",
    "format": "date-time"
   },
   "supersededAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
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
 "ConsentPurpose": {
  "type": "string",
  "enum": [
   "marketing",
   "personalisation",
   "profiling",
   "thirdPartySharing",
   "aiProcessing",
   "transactional"
  ]
 },
 "ConsentPurposeConfig": {
  "x-ticvai-persistence": "marketing.consent_purpose + marketing.consent_purpose_channel",
  "type": "object",
  "required": [
   "purpose",
   "channels",
   "noticeVersion",
   "isRequiredForService"
  ],
  "properties": {
   "purpose": {
    "$ref": "#/components/schemas/ConsentPurpose"
   },
   "displayName": {
    "type": "string"
   },
   "description": {
    "type": "string"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "noticeVersion": {
    "type": "string",
    "description": "Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured.\n"
   },
   "isRequiredForService": {
    "type": "boolean",
    "description": "True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently.\n"
   },
   "expiresAfterMonths": {
    "type": "integer",
    "nullable": true
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
    "format": "uuid",
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
 "ConsentSource": {
  "type": "string",
  "enum": [
   "guestApp",
   "website",
   "kiosk",
   "pos",
   "callCentre",
   "import",
   "agentRecorded",
   "cookieBanner",
   "checkout"
  ],
  "description": "`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."
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
    "format": "uuid",
    "readOnly": true,
    "description": "UUIDv7."
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
       "format": "uuid",
       "readOnly": true,
       "description": "UUIDv7. The row's own key."
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
          "format": "uuid",
          "readOnly": true,
          "description": "UUIDv7. The row's own key."
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
 "MessageChannel": {
  "type": "string",
  "enum": [
   "email",
   "sms",
   "whatsapp",
   "push",
   "inApp",
   "post"
  ]
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
 "Principal": {
  "x-ticvai-persistence": "identity.principal",
  "type": "object",
  "required": [
   "id",
   "username",
   "displayName",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "username": {
    "type": "string"
   },
   "displayName": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Past this, resolution returns DENY regardless of grants."
   },
   "primaryRoleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Determines the landing screen when the principal holds several roles and picks one at login.\n"
   },
   "roles": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/RoleSummary"
    }
   },
   "lastLoginAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "Role": {
  "x-ticvai-persistence": "identity.role",
  "type": "object",
  "required": [
   "id",
   "code",
   "name"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "x-ticvai-unique": "tenant",
    "description": "**Unique within the tenant** (decided 28 September, audit R108). A seeded role's code is reserved in every tenant. Unique per tenant, not per venue, because a grant names a role anywhere in the tree; `createRole` refuses a duplicate with `409 duplicate-code`.\n"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string"
   },
   "permissions": {
    "type": "array",
    "description": "**A role that grants no permissions is not a role.** `Role` carried a code, a name and two counts until 18 August, and `identity.role_permission` derived from it with exactly one column — `role_id`. **A join table that joins to nothing**, found by Hrushikant in review and missed by the schema audit that ran the same day.\n**The audit asked whether every table had columns, a relationship and an owner, and this table had all three.** What it did not ask is whether a table with one column can do the job its name claims.\n",
    "items": {
     "$ref": "../shared/permissions.yaml#/components/schemas/Permission"
    }
   },
   "inheritsFromRoleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Role composition, one level deep and no deeper.** A supervisor role that is a cashier plus three permissions is how venues actually describe them.\n**Cycles are refused and depth is capped at one**, because a permission set nobody can read off the screen is a permission set nobody audits.\n"
   },
   "isSystem": {
    "type": "boolean",
    "default": false,
    "description": "**Seeded roles ship and are editable; deleting one is refused.** A venue that removes `cashier` and rebuilds it has two roles with one name in the audit log.\n**The seeded system roles are Cashier, Supervisor, Venue Manager, Finance and Tenant Admin** (proposed in `docs/active/seed-data-proposal.md` section 2, client to correct; audit R229).\n"
   },
   "principalCount": {
    "type": "integer"
   },
   "grantCount": {
    "type": "integer"
   }
  }
 },
 "RoleSummary": {
  "x-ticvai-persistence": "none — projection over role",
  "type": "object",
  "required": [
   "id",
   "code",
   "name"
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
   "isPrimary": {
    "type": "boolean"
   }
  }
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
 "SeoMetadata": {
  "type": "object",
  "x-ticvai-persistence": "control.seo_metadata",
  "description": "22.11.1 to 22.11.12, CF-137. **Twelve requirements, checked against the matrix.**\n**SEO is not a marketing nicety for a venue selling online** — an attraction that does not appear in search sells through OTAs at OTA commission, which is the cost this avoids.\n",
  "required": [
   "id",
   "entityKind",
   "entityId"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "entityKind": {
    "type": "string",
    "enum": [
     "contentPage",
     "product",
     "event",
     "performance",
     "membership",
     "promotion",
     "venue"
    ]
   },
   "entityId": {
    "type": "string",
    "format": "uuid"
   },
   "locale": {
    "type": "string"
   },
   "title": {
    "type": "string",
    "nullable": true
   },
   "metaDescription": {
    "type": "string",
    "nullable": true
   },
   "keywords": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "canonicalUrl": {
    "type": "string",
    "nullable": true
   },
   "slug": {
    "type": "string",
    "nullable": true,
    "description": "22.11.6. **Human-readable, and changing one is a redirect rather than an edit** — a slug that changes without a 301 is a page that was ranking and now is not.\n"
   },
   "hreflang": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    },
    "description": "22.11.11. **Which URL serves which language**, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page.\n"
   },
   "schemaOrgType": {
    "type": "string",
    "nullable": true
   },
   "openGraph": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "isAutoGenerated": {
    "type": "boolean",
    "default": true,
    "description": "22.11.2. **Generated by default and overridable.** A venue with 400 products will not write 400 meta descriptions, and one with an important landing page will not accept a generated one.\n"
   },
   "noIndex": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "readOnly": true,
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
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
